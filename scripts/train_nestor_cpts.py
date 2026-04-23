"""
Train Nestor Bayesian Profiler CPTs from the 10k synthetic dataset.
Replaces the hand-written weights in nestor_bayesian_profiler.py with
MLE-fit linear regressions, saves to data/nestor/nestor_cpts.json so the
profiler's _try_load picks it up.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
import numpy as np
import pandas as pd

from src.models.nestor.nestor_bayesian_profiler import (
    NestorBayesianProfiler, LEARNING_ELEMENTS,
)

DATA_CSV = Path("data/nestor/synthetic_10000/nestor_synthetic_personality_data.csv")
CKPT = Path("data/nestor/nestor_cpts.json")


def fit_linear(X, y):
    X_aug = np.column_stack([X, np.ones(len(X))])
    coef, *_ = np.linalg.lstsq(X_aug, y, rcond=None)
    return coef[:-1], coef[-1]  # weights, bias


def main():
    print(f"[Nestor] training on {DATA_CSV}")
    df = pd.read_csv(DATA_CSV)
    print(f"  {len(df)} rows, {len(df.columns)} columns")

    p_cols = ["P1_openness", "P2_conscientiousness", "P3_extraversion",
              "P4_agreeableness", "P5_neuroticism"]
    P = df[p_cols].values.astype(float)

    # 1) learning-style weights (P -> D)
    style_weights = {}
    style_biases = {}
    for d in ["D1_visual_verbal", "D2_sensing_intuitive",
              "D3_active_reflective", "D4_sequential_global"]:
        y = df[d].values.astype(float)
        w, b = fit_linear(P, y)
        style_weights[d] = w.tolist()
        style_biases[d]  = float(b)
        pred = P @ w + b
        r = np.corrcoef(pred, y)[0, 1]
        print(f"  style   {d:<25} corr={r:+.3f}  bias={b:+.3f}  w={np.round(w,3).tolist()}")

    # 2) strategy weights (P -> T)
    strategy_weights = {}
    strategy_biases  = {}
    for t in ["T1_deep_processing", "T2_elaboration",
              "T3_organization", "T4_metacognition"]:
        y = df[t].values.astype(float)
        w, b = fit_linear(P, y)
        strategy_weights[t] = w.tolist()
        strategy_biases[t]  = float(b)
        pred = P @ w + b
        r = np.corrcoef(pred, y)[0, 1]
        print(f"  strat   {t:<25} corr={r:+.3f}  bias={b:+.3f}  w={np.round(w,3).tolist()}")

    # 3) element weights (P, D, T -> L one-hot) — multinomial logistic as
    #    per-element binary regression (one-vs-rest)
    d_cols = ["D1_visual_verbal", "D2_sensing_intuitive",
              "D3_active_reflective", "D4_sequential_global"]
    t_cols = ["T1_deep_processing", "T2_elaboration",
              "T3_organization", "T4_metacognition"]
    X = df[p_cols + d_cols + t_cols].values.astype(float)  # (N, 13)

    element_weights = {}
    element_biases  = {}
    for elem in LEARNING_ELEMENTS:
        y = (df["L_learning_element"] == elem).astype(float).values
        if y.sum() < 5:
            # rare class — fall back to zeros
            element_weights[elem] = [0.0] * 13
            element_biases[elem]  = 0.0
            print(f"  elem    {elem:<4} skipped (only {int(y.sum())} positives)")
            continue
        w, b = fit_linear(X, y)
        element_weights[elem] = w.tolist()
        element_biases[elem]  = float(b)
        pred = X @ w + b
        acc = ((pred > 0.5) == (y > 0.5)).mean()
        print(f"  elem    {elem:<4} pos={int(y.sum()):<4}  acc={acc:.3f}  bias={b:+.3f}")

    # save
    CKPT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "style_weights":    style_weights,
        "style_biases":     style_biases,
        "strategy_weights": strategy_weights,
        "strategy_biases":  strategy_biases,
        "element_weights":  element_weights,
        "element_biases":   element_biases,
        "is_trained":       True,
        "format_version":   2,
    }
    with open(CKPT, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"[Nestor] saved {CKPT}")

    # verify round-trip
    prof = NestorBayesianProfiler({"nestor": {"data_dir": str(CKPT.parent)}})
    print(f"[Nestor] reload check: is_trained={prof.is_trained}")
    sample = {"exploration_rate": 0.8, "persistence": 0.3,
              "organization": 0.4, "social_interaction": 0.2,
              "emotional_variability": 0.7}
    out = prof.complete_inference(sample)
    print(f"[Nestor] sample inference:")
    print(f"   personality={ {k: round(v,2) for k,v in out['personality'].items()} }")
    print(f"   styles={ {k: v for k,v in out['learning_styles'].items() if not k.endswith('_score')} }")
    print(f"   top-3 elements={out['recommended_elements']}")
    print(f"   intervention={out['intervention_preference']}")


if __name__ == "__main__":
    main()
