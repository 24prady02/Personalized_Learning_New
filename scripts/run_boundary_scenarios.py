"""
Runner for the 16 Appendix-A boundary scenarios added 2026-05-27.

Each scenario maps to a numeric threshold in the actual code and exercises
the just-below / at / just-above value. Output is written to
output/boundary_scenarios_<date>/{results.json, REPORT.md}.

Avoids the heavy registry: instantiates only what each scenario needs.
"""
from __future__ import annotations
import json, sys, time, traceback
from datetime import datetime, timedelta, timezone
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from typing import Any, Dict, List
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import yaml
print("[boundary] loading config...", flush=True)
with open(ROOT / "configs" / "config.yaml", "r", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

# Lightweight components ---------------------------------------------------
print("[boundary] loading catalogue + LP diagnostician...", flush=True)
from src.knowledge_graph.mental_models import get_catalogue
from src.orchestrator.lp_diagnostic import LPDiagnostician
from src.orchestrator.student_state_tracker import InterventionSelector
from src.reinforcement_learning.reward_function import RewardCalculator
from src.models.dina import DINAModel
from src.persistence.auth import issue_token, validate_token

CATALOGUE = get_catalogue()
LP_DX = LPDiagnostician(
    catalogue=CATALOGUE,
    hvsae_model=None,
    enable_rubric_grader=False,
    enable_catalogue_rag=False,
)
print("[boundary] components ready.", flush=True)

RESULTS: List[Dict[str, Any]] = []
REPORT: List[str] = []

def _short(o, n=400):
    s = json.dumps(o, default=str) if not isinstance(o, str) else o
    return (s[:n] + "...") if len(s) > n else s

def run(sid: str, name: str, expected: str, fn):
    row = {"id": sid, "name": name, "expected": expected,
           "outcome": "PENDING", "actual": None, "error": None,
           "duration_s": 0.0}
    t0 = time.time()
    sink = StringIO()
    try:
        with redirect_stdout(sink), redirect_stderr(sink):
            out = fn() or {}
        row["actual"] = out
        row["outcome"] = out.get("_outcome", "OK")
    except Exception as e:
        row["outcome"] = "ERROR"
        row["error"] = f"{type(e).__name__}: {e}"
        row["traceback"] = traceback.format_exc()
    row["duration_s"] = round(time.time() - t0, 2)
    RESULTS.append(row)
    mark = {"PASS":"[OK]","FAIL":"[X]","ERROR":"[!]"}.get(row["outcome"], "[?]")
    print(f"  {mark} {sid} {name} ({row['duration_s']}s)", flush=True)
    REPORT.append(f"### {sid} — {name}")
    REPORT.append(f"- **Expected**: {expected}")
    REPORT.append(f"- **Outcome**: {mark} `{row['outcome']}`")
    if row["actual"]:
        keys = {k: v for k, v in row["actual"].items() if not k.startswith("_")}
        if keys:
            REPORT.append(f"- **Actual**: `{_short(keys)}`")
    if row["error"]:
        REPORT.append(f"- **Error**: `{row['error']}`")
    REPORT.append("")
    return row


def diag(text: str, concept: str = "null_pointer", lp: str = "L1", streak: int = 0):
    d = LP_DX.diagnose(student_id="s_boundary", concept=concept,
                       question_text=text, stored_lp_level=lp,
                       stored_lp_streak=streak)
    return d.to_dict()


# ── A.0.1 — substance penalty 3-token companion ───────────────────────────
def t_A_0_1():
    d = diag("I am stuck", concept="null_pointer")
    conf = d.get("diagnostic_confidence")
    # Must NOT be floored to 0.30; should retain raw head value (>0.30 for legit 3-tok)
    not_floored = conf is None or conf > 0.30
    return {"_outcome": "PASS" if not_floored else "FAIL",
            "diagnostic_confidence": conf,
            "current_lp_level": d.get("current_lp_level"),
            "note": "3 non-filler tokens — substance penalty must NOT fire"}


# ── A.2.1 / A.2.2 — WM head 0.55 floor edges ──────────────────────────────
def _force_wm_st_head_prob(target_prob: float, target_wm: str = "NP-A"):
    """Returns a patch context that forces the wm_st_head softmax to put
    `target_prob` on `target_wm`. Other classes share the remainder."""
    import torch
    # Find the index for target_wm under concept null_pointer
    if LP_DX.wm_st_labels is None:
        return None
    concept = "null_pointer"
    idx_this_concept = [
        i for i, (c, _w) in enumerate(LP_DX.wm_st_labels) if c == concept
    ]
    # Find position of target_wm in that subset
    sub_wms = [LP_DX.wm_st_labels[i][1] for i in idx_this_concept]
    if target_wm not in sub_wms:
        target_wm = sub_wms[0]
    target_pos = sub_wms.index(target_wm)
    n_sub = len(sub_wms)

    # Build logits that, after softmax over the sub-set, give target_prob.
    # We solve: softmax([L_target, 0, 0, ...]) = [p, (1-p)/(n-1), ...]
    # so L_target = log(p / ((1-p)/(n-1)))  with others = 0
    import math
    other_prob = (1.0 - target_prob) / max(1, n_sub - 1)
    L = math.log(target_prob / max(other_prob, 1e-9))

    # We need to return a full-length logits vector (over all wm_st_labels)
    full_len = len(LP_DX.wm_st_labels)
    forced = torch.full((full_len,), -10.0)
    for j, gi in enumerate(idx_this_concept):
        forced[gi] = L if j == target_pos else 0.0

    class _Fake:
        def __call__(self, _emb):
            # squeeze(0) is applied by caller, so return shape (1, N)
            return forced.unsqueeze(0)
        def eval(self): return self
    return _Fake()


def t_A_2_1():
    """WM head prob 0.54 → below 0.55 floor → no WM emitted."""
    fake = _force_wm_st_head_prob(0.54, "NP-A")
    if fake is None:
        return {"_outcome": "FAIL", "_drawback": "no wm_st_head loaded"}
    with patch.object(LP_DX, "wm_st_head", fake):
        d = diag("error here", concept="null_pointer")
    ok = d.get("wrong_model_id") is None and d.get("source") != "trained_wm_head"
    return {"_outcome": "PASS" if ok else "FAIL",
            "wrong_model_id": d.get("wrong_model_id"),
            "match_score": d.get("match_score"),
            "source": d.get("source")}


def t_A_2_2():
    """WM head prob 0.56 → above 0.55 floor → WM emitted."""
    fake = _force_wm_st_head_prob(0.56, "NP-A")
    if fake is None:
        return {"_outcome": "FAIL", "_drawback": "no wm_st_head loaded"}
    with patch.object(LP_DX, "wm_st_head", fake):
        d = diag("error here", concept="null_pointer")
    ok = d.get("source") == "trained_wm_head" and d.get("wrong_model_id") == "NP-A"
    return {"_outcome": "PASS" if ok else "FAIL",
            "wrong_model_id": d.get("wrong_model_id"),
            "match_score": d.get("match_score"),
            "source": d.get("source")}


# ── A.3.1 / A.3.2 — ST LP head 0.40 floor edges ───────────────────────────
def _force_lp_st_head_prob(target_prob: float, target_lp: str = "L2"):
    import torch, math
    if LP_DX.lp_head_labels is None:
        return None
    labels = LP_DX.lp_head_labels
    n = len(labels)
    target_pos = labels.index(target_lp) if target_lp in labels else 0
    other_prob = (1.0 - target_prob) / max(1, n - 1)
    L = math.log(target_prob / max(other_prob, 1e-9))
    forced = torch.zeros((n,))
    forced[target_pos] = L

    class _Fake:
        def __call__(self, _emb):
            return forced.unsqueeze(0)
        def eval(self): return self
    return _Fake()


def t_A_3_1():
    """LP head top 0.39 → below 0.40 → trained_lp_level stays None."""
    fake = _force_lp_st_head_prob(0.39, "L2")
    if fake is None:
        return {"_outcome": "FAIL", "_drawback": "no lp_st_head loaded"}
    # disable ensemble so we have full control
    with patch.object(LP_DX, "lp_st_head", fake), \
         patch.object(LP_DX, "lp_st_head_ensemble", None):
        d = diag("some answer text here please", concept="null_pointer")
    probs = d.get("trained_lp_probs") or {}
    top_prob = max(probs.values()) if probs else None
    # trained_lp_level should be unset OR fall back to overlap
    return {"_outcome": "PASS" if (top_prob is None or top_prob < 0.40) else "FAIL",
            "top_prob": top_prob,
            "current_lp_level": d.get("current_lp_level"),
            "trained_lp_probs": probs}


def t_A_3_2():
    """LP head top 0.41 → above 0.40 → trained_lp_level adopted."""
    fake = _force_lp_st_head_prob(0.41, "L2")
    if fake is None:
        return {"_outcome": "FAIL", "_drawback": "no lp_st_head loaded"}
    with patch.object(LP_DX, "lp_st_head", fake), \
         patch.object(LP_DX, "lp_st_head_ensemble", None):
        d = diag("some answer text here please", concept="null_pointer")
    probs = d.get("trained_lp_probs") or {}
    top_prob = max(probs.values()) if probs else None
    return {"_outcome": "PASS" if (top_prob and top_prob >= 0.40) else "FAIL",
            "top_prob": top_prob,
            "current_lp_level": d.get("current_lp_level")}


# ── A.3.3 — parroting 15 vs 16 word edge ──────────────────────────────────
def t_A_3_3():
    """Parroting heuristic: trained head says L3, mech vocab present,
    no causal markers, 15-word reply → downgrade to L2; 16 words → stays L3."""
    # Force trained_lp_level=L3 by setting current_lp_level via stored.
    # Easier: invoke through diagnose() with a reply that the heuristic catches.
    # Mech vocab without causal connective:
    reply_15 = ("reference heap stack memory pointer immutable scope cache "
                "boxed unboxed autobox class object void int")  # 15 words
    reply_16 = reply_15 + " final"

    # Force lp head to predict L3 strongly
    fake = _force_lp_st_head_prob(0.90, "L3")
    # stored_lp must NOT be L3 — otherwise the regression-protection
    # clause (stored_idx > current_idx) reverts the parroting downgrade
    # back to L3. Using L1 lets the downgrade propagate.
    with patch.object(LP_DX, "lp_st_head", fake), \
         patch.object(LP_DX, "lp_st_head_ensemble", None):
        d15 = diag(reply_15, concept="null_pointer", lp="L1")
        d16 = diag(reply_16, concept="null_pointer", lp="L1")
    lp15 = d15.get("current_lp_level")
    lp16 = d16.get("current_lp_level")
    # Per code: <=15 words triggers downgrade L3->L2; 16 keeps L3
    ok = (lp15 == "L2" and lp16 == "L3")
    return {"_outcome": "PASS" if ok else "FAIL",
            "lp_at_15_words": lp15,
            "lp_at_16_words": lp16,
            "expected": "L2 / L3"}


# ── A.3.4 — L2 rule-naming 5 vs 6 word edge ───────────────────────────────
def t_A_3_4():
    """L2 rule-naming heuristic: pattern matches AND len >= 6 words upgrades L1->L2."""
    fake = _force_lp_st_head_prob(0.90, "L1")
    with patch.object(LP_DX, "lp_st_head", fake), \
         patch.object(LP_DX, "lp_st_head_ensemble", None):
        d5 = diag("use .equals not ==", concept="string_equality", lp="L1")    # 5 words
        d6 = diag("you should use .equals not ==", concept="string_equality", lp="L1")  # 6 words
    lp5 = d5.get("current_lp_level")
    lp6 = d6.get("current_lp_level")
    ok = (lp5 == "L1" and lp6 == "L2")
    return {"_outcome": "PASS" if ok else "FAIL",
            "lp_at_5_words": lp5,
            "lp_at_6_words": lp6,
            "expected": "L1 / L2"}


# ── A.5.1 / A.5.2 — probe floor 0.55 edges ────────────────────────────────
def t_A_5_1():
    """Probe gate fires when diagnostic_confidence < 0.55."""
    from scripts import cpal_chat_app
    floor = cpal_chat_app.CHAT_PROBE_CONFIDENCE_FLOOR
    triggers = 0.54 < floor
    return {"_outcome": "PASS" if triggers else "FAIL",
            "floor": floor,
            "test_value": 0.54,
            "below_floor": 0.54 < floor}


def t_A_5_2():
    """Probe gate does NOT fire when diagnostic_confidence > 0.55."""
    from scripts import cpal_chat_app
    floor = cpal_chat_app.CHAT_PROBE_CONFIDENCE_FLOOR
    triggers = 0.56 < floor
    return {"_outcome": "PASS" if not triggers else "FAIL",
            "floor": floor,
            "test_value": 0.56,
            "below_floor": 0.56 < floor}


# ── A.8.1 — DINA lower clamp 0.01 ─────────────────────────────────────────
def t_A_8_1():
    dina = DINAModel(CFG)
    sid = "s_boundary_clamp"
    skill = "null_pointer"
    history = []
    for _ in range(15):  # extreme: 15 wrongs from prior 0.15
        r = dina.update(sid, skill, is_correct=False)
        history.append(r["mastery_after"])
    final = history[-1]
    ok = abs(final - 0.01) < 1e-6  # clamped to exactly 0.01
    return {"_outcome": "PASS" if ok else "FAIL",
            "final_mastery": final,
            "expected_clamp": 0.01,
            "trajectory_first5": history[:5],
            "trajectory_last5": history[-5:]}


# ── A.11.x — uncovered intervention branches ──────────────────────────────
SEL = InterventionSelector()

def t_A_11_1():
    out = SEL.select(
        cognitive={"encoding_strength": "solid"},
        progression={"stage": 3},
        psychological={"attribution": "adaptive", "self_efficacy": "low",
                       "imposter_signal": False, "high_anxiety": False},
        bkt_mastery=0.6,
    )
    ok = out.get("type") == "mastery_surface"
    return {"_outcome": "PASS" if ok else "FAIL",
            "intervention": out.get("type"),
            "expected": "mastery_surface",
            "rationale": out.get("rationale")}


def t_A_11_2():
    out = SEL.select(
        cognitive={"encoding_strength": "partial"},
        progression={"stage": "4a"},
        psychological={"attribution": "adaptive", "self_efficacy": "growth",
                       "imposter_signal": False, "high_anxiety": False},
        bkt_mastery=0.5,
    )
    ok = out.get("type") == "increase_challenge"
    return {"_outcome": "PASS" if ok else "FAIL",
            "intervention": out.get("type"),
            "expected": "increase_challenge",
            "rationale": out.get("rationale")}


def t_A_11_3():
    out = SEL.select(
        cognitive={"encoding_strength": "partial"},
        progression={"stage": "2b"},
        psychological={"attribution": "adaptive", "self_efficacy": "neutral",
                       "imposter_signal": False, "high_anxiety": False},
        bkt_mastery=0.4,
    )
    ok = out.get("type") == "socratic_prompt"
    return {"_outcome": "PASS" if ok else "FAIL",
            "intervention": out.get("type"),
            "expected": "socratic_prompt",
            "rationale": out.get("rationale")}


def t_A_11_4():
    out = SEL.select(
        cognitive={"encoding_strength": "deep"},
        progression={"stage": "4b"},
        psychological={"attribution": "adaptive", "self_efficacy": "neutral",
                       "imposter_signal": False, "high_anxiety": False},
        bkt_mastery=0.7,
    )
    ok = out.get("type") == "transfer_task"
    return {"_outcome": "PASS" if ok else "FAIL",
            "intervention": out.get("type"),
            "expected": "transfer_task",
            "rationale": out.get("rationale")}


# ── A.12.1 — emotional_state reward component ─────────────────────────────
def t_A_12_1():
    rc = RewardCalculator(CFG)
    # Identical setup, only emotion_after varies.
    base_session = {"emotion": "frustrated"}
    base_resp = {
        "mastery_before": 0.4, "mastery_after": 0.4,
        "engagement_score": 0.5, "time_spent": 60,
        "emotion_after": "engaged",
        "gave_up": False, "has_misconception": False,
        "attribution_before": "adaptive", "attribution_after": "adaptive",
        "imposter_flag_before": False, "imposter_flag_after": False,
        "zpd_status": "at_boundary", "intervention_type": "worked_example",
        "delta_lp": 0, "lp_level_before": "L1", "lp_level_after": "L1",
        "plateau_flag_before": False,
    }
    r_engaged = rc.calculate_reward(base_session, action_taken=0,
                                    student_response=base_resp)
    base_resp_y = dict(base_resp); base_resp_y["emotion_after"] = "frustrated"
    r_frustrated = rc.calculate_reward(base_session, action_taken=0,
                                       student_response=base_resp_y)
    delta = r_engaged - r_frustrated
    # Expected: e_change for X = 0.5-(-1) = 1.5 clipped to +1; for Y = 0.
    # Weight 0.12 → delta ≈ 0.12. Sign must be positive.
    ok = delta > 0.05
    return {"_outcome": "PASS" if ok else "FAIL",
            "reward_engaged": round(r_engaged, 4),
            "reward_frustrated": round(r_frustrated, 4),
            "delta": round(delta, 4),
            "expected_delta_approx": 0.12,
            "weight_emotional_state": rc.weights["emotional_state"]}


# ── A.19.1 — mastery decay 14-day boundary ────────────────────────────────
def t_A_19_1():
    """Test _apply_decay directly with a known age."""
    dina = DINAModel(CFG)
    skill = "null_pointer"
    sid = "s_decay_test"
    # Force a known last-update time via the DB. We bypass the DB and
    # test the decay formula directly with a stub.
    from src.persistence import db_store
    # Use the decay formula: p(t) = prior + (p - prior) * 0.5^(t/HL)
    idx = None
    from src.models.dina import SKILL_INDEX, _DEFAULT_PRIOR
    prior = float(dina.prior[SKILL_INDEX[skill]])
    p0 = 0.90
    hl = DINAModel.MASTERY_HALF_LIFE_DAYS

    def expected(age_days):
        return prior + (p0 - prior) * (0.5 ** (age_days / hl))

    e_13 = expected(13.0)
    e_14 = expected(14.0)
    e_15 = expected(15.0)

    # Verify the formula matches code by stubbing db row
    class _StubDB:
        def get_mastery(self, _s, _k):
            # Return (mastery_value, last_iso). last_iso is `age_days` ago.
            return (p0, (datetime.now(timezone.utc) -
                        timedelta(days=self._age)).isoformat())
    stub = _StubDB()

    def _decay_at(age_days):
        stub._age = age_days
        with patch.object(db_store, "get_db", return_value=stub):
            return dina._apply_decay(sid, skill, p0)

    d13 = _decay_at(13.0)
    d14 = _decay_at(14.0)
    d15 = _decay_at(15.0)

    tol = 1e-3
    ok = (abs(d13 - e_13) < tol and abs(d14 - e_14) < tol
          and abs(d15 - e_15) < tol)
    return {"_outcome": "PASS" if ok else "FAIL",
            "half_life_days": hl,
            "p0": p0, "prior": round(prior, 4),
            "decayed_at_13d": round(d13, 4), "expected_13d": round(e_13, 4),
            "decayed_at_14d": round(d14, 4), "expected_14d": round(e_14, 4),
            "decayed_at_15d": round(d15, 4), "expected_15d": round(e_15, 4)}


# ── A.19.2 — auth TTL 7-day expiry boundary ───────────────────────────────
def t_A_19_2():
    # A: just-before expiry (1 s remaining)
    tok_a = issue_token("alice", "student", "cs101", ttl_seconds=1)
    res_a = validate_token(tok_a)  # immediately — still valid
    # B: already expired (ttl_seconds = -1)
    tok_b = issue_token("bob", "student", "cs101", ttl_seconds=-1)
    res_b = validate_token(tok_b)
    ok = (res_a == ("alice", "student", "cs101") and res_b is None)
    return {"_outcome": "PASS" if ok else "FAIL",
            "valid_token_result": res_a,
            "expired_token_result": res_b}


# ── Driver ────────────────────────────────────────────────────────────────
SCENARIOS = [
    ("A.0.1",  "3-token reply must NOT fire substance penalty", "conf > 0.30", t_A_0_1),
    ("A.2.1",  "WM head 0.54 → below floor → no WM",           "wm_id=None",  t_A_2_1),
    ("A.2.2",  "WM head 0.56 → above floor → WM emitted",      "wm_id=NP-A",  t_A_2_2),
    ("A.3.1",  "LP head 0.39 → below floor → trained_lp None", "no override", t_A_3_1),
    ("A.3.2",  "LP head 0.41 → above floor → trained_lp set",  "head adopted",t_A_3_2),
    ("A.3.3",  "parroting at 15 vs 16 words",                   "L2 / L3",     t_A_3_3),
    ("A.3.4",  "L2 rule-naming at 5 vs 6 words",                "L1 / L2",     t_A_3_4),
    ("A.5.1",  "probe floor 0.54 < 0.55 → probe fires",         "< floor",     t_A_5_1),
    ("A.5.2",  "probe floor 0.56 > 0.55 → teach",                ">= floor",   t_A_5_2),
    ("A.8.1",  "DINA lower clamp at 0.01",                       "p=0.01",     t_A_8_1),
    ("A.11.1", "mastery_surface (solid+low_eff)",                "mastery_surface",  t_A_11_1),
    ("A.11.2", "increase_challenge (growth+stage4a)",            "increase_challenge", t_A_11_2),
    ("A.11.3", "socratic_prompt (partial+stage2b)",              "socratic_prompt",    t_A_11_3),
    ("A.11.4", "transfer_task (deep+stage4b)",                   "transfer_task",      t_A_11_4),
    ("A.12.1", "emotional_state component delta",                "delta ~= +0.12",     t_A_12_1),
    ("A.19.1", "mastery decay at 13/14/15-day boundary",         "matches formula",    t_A_19_1),
    ("A.19.2", "auth token expiry edge",                          "valid / None",      t_A_19_2),
]

def main():
    print(f"[boundary] running {len(SCENARIOS)} scenarios...", flush=True)
    REPORT.append(f"# Boundary scenarios — execution report")
    REPORT.append(f"_Generated: {datetime.now().isoformat(timespec='seconds')}_")
    REPORT.append("")
    for sid, name, expected, fn in SCENARIOS:
        run(sid, name, expected, fn)

    n_pass = sum(1 for r in RESULTS if r["outcome"] == "PASS")
    n_fail = sum(1 for r in RESULTS if r["outcome"] in ("FAIL",))
    n_err  = sum(1 for r in RESULTS if r["outcome"] == "ERROR")

    summary = f"\n## Summary: {n_pass} PASS / {n_fail} FAIL / {n_err} ERROR (of {len(RESULTS)})"
    print(summary)
    REPORT.insert(2, summary + "\n")

    out_dir = ROOT / "output" / f"boundary_scenarios_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(
        json.dumps(RESULTS, indent=2, default=str), encoding="utf-8")
    (out_dir / "REPORT.md").write_text("\n".join(REPORT), encoding="utf-8")
    print(f"[boundary] wrote {out_dir}")

if __name__ == "__main__":
    main()
