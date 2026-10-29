"""TF-IDF pair classifier: agree / contradict / unrelated, learned from graph pairs.

Features of a pair (graph text, statement): the anchors of
``edgelogic.EdgeLogicReader`` (with negated words marked), as shared /
graph-only / statement-only, weighted by their rarity in the graph, plus the
overlap score and each side's negation. The model is trained by
scripts/train_tfidf_nli.py on data/nli_pairs.json (graph text only) and saved
to models/tfidf-nli.pkl. No language model is involved.

``side(...)`` decides which side of a misconception edge a statement
expresses: it must agree with one side and not agree with the other.
"""

from __future__ import annotations

import pickle
from functools import lru_cache
from pathlib import Path
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:  # pragma: no cover
    from .edgelogic import EdgeLogicReader

MODEL = Path(__file__).resolve().parents[2] / "models" / "tfidf-nli.pkl"
CONTRADICTION, ENTAILMENT, NEUTRAL = 0, 1, 2
MIN_PROB = 0.5


def pair_features(r: "EdgeLogicReader", premise: str, hypothesis: str, variables: Iterable[str] = ()) -> dict:
    a = set(r.tokens(premise))
    b = set(r.tokens(hypothesis, variables))
    f: dict[str, float] = {}
    for t in a & b:
        f["S:" + t] = r.weight(t)
    for t in a - b:
        f["P:" + t] = r.weight(t)
    for t in b - a:
        f["H:" + t] = r.weight(t)
    f["score"] = r.score(hypothesis, premise, variables)
    f["neg_p"] = float(r.negated(premise))
    f["neg_h"] = float(r.negated(hypothesis))
    f["neg_diff"] = float(r.negated(premise) != r.negated(hypothesis))
    f["shared_not"] = float(any(t.startswith("not_") for t in a & b))
    return f


@lru_cache(maxsize=1)
def load() -> dict | None:
    if not MODEL.exists():
        return None
    with open(MODEL, "rb") as fh:
        return pickle.load(fh)


def probs(r: "EdgeLogicReader", model: dict, premise: str, hypothesis: str,
          variables: Iterable[str] = ()) -> list[float]:
    x = model["vec"].transform([pair_features(r, premise, hypothesis, variables)])
    p = model["clf"].predict_proba(x)[0]
    out = [0.0, 0.0, 0.0]
    for k, v in zip(model["clf"].classes_, p):
        out[int(k)] = float(v)
    return out


def side(r: "EdgeLogicReader", model: dict, statement: str, wrong: str, right: str,
         variables: Iterable[str] = ()) -> str | None:
    """"wrong" | "right" | None: the statement agrees with one side of a
    misconception edge (P(agree) >= MIN_PROB and the higher) and does not
    agree with the other."""
    pw = probs(r, model, wrong, statement, variables)
    pr = probs(r, model, right, statement, variables)
    if pw[ENTAILMENT] >= MIN_PROB and pw[ENTAILMENT] > pr[ENTAILMENT] and pr[ENTAILMENT] < MIN_PROB:
        return "wrong"
    if pr[ENTAILMENT] >= MIN_PROB and pr[ENTAILMENT] > pw[ENTAILMENT] and pw[ENTAILMENT] < MIN_PROB:
        return "right"
    return None
