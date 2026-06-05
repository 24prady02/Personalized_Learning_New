"""
Lightweight student-facing FastAPI app for the 3-step learning flow:
  1) MCQ on a code snippet
  2) Free-text "what do you believe is happening"
  3) Theory-grounded correction (wrong-model + LP rubric)

Mastery state (DINA) is updated server-side per session but never returned
to the student. Run with:
    uvicorn api.student_app:app --host 0.0.0.0 --port 8001
"""
from __future__ import annotations

import sys as _sys
for _stream in (_sys.stdout, _sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import json
import random
import re
import time
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent.parent
_sys.path.insert(0, str(ROOT))

from src.models.dina import DINAModel  # noqa: E402
# Production-hardening additions wired in 2026-05-30 — see
# scripts/cpal_chat_app.py for the chat-flow equivalents.
from src.persistence.auth import validate_token            # noqa: E402
from src.persistence.db_store import get_db                # noqa: E402
from src.persistence.ab_testing import assign_variant      # noqa: E402


# ── Injection guard (mirror of cpal_chat_app._INJECTION_PATTERNS) ────────────
_INJECTION_PATTERNS = [
    re.compile(p, re.IGNORECASE) for p in [
        r"\bignore (previous|all|prior|the above|your) (instructions?|prompts?|rules?)\b",
        r"\b(system|developer) (prompt|mode|message)\b",
        r"\byou (are|will be) now\b.*\b(dan|developer|jailbreak|unrestricted)\b",
        r"\b(reveal|show|tell me) (your|the) (system prompt|instructions|hidden)\b",
        r"\bact as (if you (are|were)|though)\b.*\b(no longer|not bound|free|jailbroken)\b",
        r"\bjust (give|tell) me the (answer|solution|code)\b",
        r"\bpretend (you are|to be)\b.*\b(no rules|no restrictions)\b",
    ]
]


def _sanitise_student_input(text: str) -> str:
    """Wrap obvious prompt-injection markers in [STUDENT-QUOTE: ...] so the
    LLM prompt-builder downstream treats them as the student's words, not
    instructions. Idempotent. Mirrors cpal_chat_app._sanitise_student_input.
    """
    if not text or "[STUDENT-QUOTE" in text:
        return text or ""
    out = text
    matched = False
    for pat in _INJECTION_PATTERNS:
        if pat.search(out):
            matched = True
            out = pat.sub(lambda m: f"[STUDENT-QUOTE: {m.group(0)}]", out)
    if matched:
        out = "[contains-quoted-instruction] " + out
    return out


def _resolve_student_id(request: Optional[Request]) -> Dict[str, str]:
    """Pick the student identity for this session, in priority order:
       1. ?token=...  (issued by scripts/issue_token.py — validated HMAC)
       2. ?student=... (unauthenticated, demo-mode)
       3. fallback "anon"
    Returns {"student_id", "role", "course"}. Mirrors cpal_chat_app's
    resolver so the two surfaces share the same per-student persistence key.
    """
    sid: Optional[str] = None
    role = "student"
    course = "default"
    try:
        if request is not None:
            qp = dict(request.query_params)
            tok = (qp.get("token") or "").strip()
            if tok:
                parsed = validate_token(tok)
                if parsed:
                    sid, role, course = parsed
            if not sid:
                sid = (qp.get("student") or qp.get("student_id") or "").strip() or None
    except Exception as e:
        print(f"[student_app] resolve fell through: {e}")
        sid = None
    if not sid:
        sid = "anon"
    # Sanitise: alphanumeric + dash/underscore only (avoids path-injection
    # into per-student state keys).
    sid = re.sub(r"[^a-zA-Z0-9_\-]", "_", sid)[:64] or "anon"
    return {"student_id": sid, "role": role, "course": course}


# ── data loading ──────────────────────────────────────────────────────────────

QUIZ_BANK_PATH = ROOT / "data" / "quiz_bank.json"
CATALOGUE_PATH = ROOT / "data" / "mental_models" / "wrong_models_catalogue.json"

_quiz_bank: Dict = json.loads(QUIZ_BANK_PATH.read_text(encoding="utf-8"))
_catalogue: Dict = json.loads(CATALOGUE_PATH.read_text(encoding="utf-8"))

QUIZ_ITEMS: List[Dict] = _quiz_bank["items"]
QUIZ_BY_ID: Dict[str, Dict] = {q["id"]: q for q in QUIZ_ITEMS}

CONCEPTS = _catalogue.get("concepts", {})


def _wm_lookup(concept: str, wm_id: str) -> Optional[Dict]:
    entry = CONCEPTS.get(concept)
    if not entry:
        return None
    for wm in entry.get("wrong_models", []):
        if wm.get("id") == wm_id:
            return wm
    return None


def _lp_rubric(concept: str) -> Dict:
    return (CONCEPTS.get(concept, {}) or {}).get("lp_rubric", {}) or {}


# ── DINA + session state (server-side only) ──────────────────────────────────

_dina = DINAModel({"dina": {"data_dir": str(ROOT / "data" / "dina")}})

# session_id -> {student_id, current_item_id, choice, is_correct, belief}
_sessions: Dict[str, Dict] = {}


# ── API schema ────────────────────────────────────────────────────────────────

class StartResp(BaseModel):
    session_id: str
    item: Dict  # safe payload (no `correct` flags, no wm_id)


class AnswerReq(BaseModel):
    session_id: str
    choice: str           # "A" | "B" | "C" | "D"
    belief: Optional[str] = ""


class AnswerResp(BaseModel):
    accepted: bool
    needs_belief: bool


class CorrectReq(BaseModel):
    session_id: str
    belief: str           # student's free-text reasoning


class CorrectResp(BaseModel):
    # `type` lets the frontend branch — "probe" pops a follow-up question
    # before showing the answer, "explanation" goes straight to Step 3.
    type: str             # "probe" | "explanation"
    title: str
    correct_choice: str
    your_choice: str
    # Set when type == "explanation"
    explanation: Optional[str] = None
    next_item_id: Optional[str] = None
    # Set when type == "probe"
    probe_question: Optional[str] = None
    probe_target_level: Optional[str] = None
    probe_round: Optional[int] = None          # 1, 2, ... (1-indexed)
    probe_round_max: Optional[int] = None      # cap (e.g. 2 in quiz mode)


class ProbeAnswerReq(BaseModel):
    session_id: str
    probe_answer: str


# ── app ───────────────────────────────────────────────────────────────────────

app = FastAPI(title="Personalized Learning — Student App", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)


def _safe_item(item: Dict) -> Dict:
    """Strip server-only fields (`correct`, `wm_id`) before sending to client."""
    return {
        "id": item["id"],
        "concept": item["concept"],
        "title": item["title"],
        "code": item["code"],
        "question": item["question"],
        "options": [{"key": o["key"], "text": o["text"]} for o in item["options"]],
    }


#: Maximum probes per concept in QUIZ mode (chat-flow allows 3; we cap at 2
#: here so the student isn't stuck behind too many follow-ups before the answer).
QUIZ_MAX_PROBES = 2
#: Below this grader confidence, the quiz triggers a follow-up probe instead
#: of going straight to the answer.
QUIZ_PROBE_CONFIDENCE_FLOOR = 0.55


def _new_session(student_id: str = "anon",
                  role: str = "student",
                  course: str = "default") -> str:
    sid = uuid.uuid4().hex[:12]
    _sessions[sid] = {
        "student_id": student_id,
        "role":       role,
        "course":     course,
        "current_item_id": None,
        "choice": None,
        "is_correct": None,
        "belief": None,
        # --- multi-turn probe ladder (Phase 4) ---
        "probe_count":      0,           # probes issued for THIS item so far
        "probed_criteria":  [],          # criterion text strings already asked
        "probe_answers":    [],          # student's probe-answer texts in order
        "history": [],
        # --- per-turn telemetry (wired to audit_log for progression queries) ---
        "item_started_at":  time.time(),
    }
    return sid


# ── CPAL backend (lazy singletons for the quiz path) ────────────────────────
#
# Two layers: RubricGrader (the LLM grader) runs inside LPDiagnostician, but
# we also call it stand-alone for paths that don't need the full diagnosis.
# LPDiagnostician.diagnose() is the FULL CPAL pipeline — keyword classifier
# (concept-rubric grounded) + RubricGrader + trained ST head + HVSAE semantic
# + CatalogueRAG retrieval — producing the bias-corrected blended LP level,
# diagnostic_confidence, lp_sub_criteria, and the matched wrong-model.
#
# The quiz path uses the full diagnostician so:
#   - the probe gate trusts the same blended `diagnostic_confidence` the
#     chat-flow uses (not just qwen's raw confidence),
#   - the explanation can be shaped by the graded LP level (L1/L2/L3/L4),
#   - probe questions can target ANY level's sub-criterion via lp_sub_criteria.

_grader = None
_diag   = None
_mm_cat = None    # MentalModelsCatalogue OBJECT (with jargon-trap getters)


def _catalogue_as_catalogue_obj():
    """Lazy MentalModelsCatalogue instance — exposes get_jargon_traps() etc.
    student_app's existing `_catalogue` is just the raw JSON dict; this
    returns the proper object that depth_probe expects."""
    global _mm_cat
    if _mm_cat is None:
        try:
            from src.knowledge_graph.mental_models import get_catalogue
            _mm_cat = get_catalogue()
        except Exception as e:
            print(f"[QuizApp] MentalModelsCatalogue unavailable ({e})")
            _mm_cat = False
    return _mm_cat or None

def _get_grader():
    global _grader
    if _grader is None:
        try:
            from src.orchestrator.rubric_grader import RubricGrader
            _grader = RubricGrader()
        except Exception as e:
            print(f"[QuizApp] RubricGrader unavailable ({e}); "
                  f"probing disabled, going straight to explanation.")
            _grader = False
    return _grader or None


def _get_diagnostician():
    """Lazy LPDiagnostician — the full CPAL Stage-1 pipeline. Returns None on
    failure so the quiz still serves explanations even if model loads fail."""
    global _diag
    if _diag is None:
        try:
            from src.orchestrator.lp_diagnostic import LPDiagnostician
            _diag = LPDiagnostician(enable_rubric_grader=True,
                                    enable_catalogue_rag=True)
        except Exception as e:
            print(f"[QuizApp] LPDiagnostician unavailable ({e}); "
                  f"falling back to RubricGrader-only.")
            _diag = False
    return _diag or None


def _accumulated_belief(sess: Dict) -> str:
    """Concatenate the original belief + every probe answer for re-grading."""
    parts = []
    if sess.get("belief"):
        parts.append(sess["belief"])
    for ans in sess.get("probe_answers", []) or []:
        parts.append(ans)
    return "  ".join(p.strip() for p in parts if p and p.strip())


def _pick_next_criterion(item: Dict, probed: list,
                          diag_dict: Optional[Dict] = None,
                          target_level: str = "L3") -> Optional[str]:
    """Pick a sub-criterion at the target LP level that has not been probed
    yet for this item.

    Priority order:
      1. Use the FULL CPAL diagnosis's lp_sub_criteria[target_level]
         (sentence-split per level), so probes can target any level — not
         just L3 — and stay aligned with the chat-flow probe ladder.
      2. Fall back to splitting the catalogue rubric prose inline.
      3. Last fallback: return the whole-level rubric string.
    Returns None when every criterion has been probed already.
    """
    # Tier 1 — full diagnosis already has the decomposition.
    if diag_dict and diag_dict.get("lp_sub_criteria"):
        sub = diag_dict["lp_sub_criteria"].get(target_level) or []
        for c in sub:
            if c not in probed:
                return c

    # Tier 2 — fall back to splitting the catalogue rubric.
    rubric = _lp_rubric(item["concept"])
    level_text = (rubric.get(target_level) or rubric.get("L3")
                  or rubric.get("L4") or "").strip()
    if not level_text:
        return None
    import re
    sub_criteria = [s.strip() for s in re.split(r"(?<=[.!?])\s+", level_text)
                    if s.strip()]
    for c in sub_criteria:
        if c not in probed:
            return c

    # Tier 3 — last resort: whole-level rubric.
    if level_text not in probed:
        return level_text
    return None


def _make_probe_question(criterion: str) -> str:
    """Turn a rubric criterion into a conversational probe question."""
    c = criterion.strip().rstrip(".")
    return (f"Quick check before the answer — in your own words, can you "
            f"explain *why* this is true: \"{c}\"?")


def _decide_probe_or_explain(sess: Dict, item: Dict) -> Dict:
    """Run the FULL CPAL diagnosis on the accumulated belief and decide:
      - if blended diagnostic_confidence is high enough OR probe cap hit
        → return an explanation payload (Step-3 path),
      - otherwise → return a probe payload (Step-2.5 path).

    Uses LPDiagnostician.diagnose() — the bias-corrected blend of keyword
    classifier + RubricGrader + trained ST head + HVSAE + CatalogueRAG —
    so the quiz path trusts the same confidence the chat-flow uses.
    Stores the diagnosis on the session so _build_explanation can shape the
    Step-3 prompt by the graded LP level.
    """
    rubric = _lp_rubric(item["concept"])
    accumulated = _accumulated_belief(sess)

    # Run the full pipeline; fall back to RubricGrader-only if it fails;
    # finally fall back to skipping probes entirely.
    diag_dict: Dict = {}
    if accumulated and rubric:
        d = _get_diagnostician()
        if d is not None:
            try:
                diag_obj = d.diagnose(
                    student_id=sess.get("student_id", "anon"),
                    concept=item["concept"],
                    question_text=accumulated,
                )
                diag_dict = diag_obj.to_dict()
            except Exception as e:
                print(f"[QuizApp] LPDiagnostician.diagnose failed: {e}")
                diag_dict = {}
        if not diag_dict:
            # Bare grader fallback.
            g = _get_grader()
            if g is not None:
                try:
                    grade = g.grade(accumulated, item["concept"], rubric)
                    diag_dict = {
                        "current_lp_level":      grade.get("level"),
                        "target_lp_level":       _next_level(grade.get("level")),
                        "diagnostic_confidence": grade.get("confidence", 0.0),
                        "rubric_grade":          grade,
                        "lp_sub_criteria":       {},
                    }
                except Exception as e:
                    print(f"[QuizApp] grader fallback failed: {e}")

    # Stash the diagnosis on the session so the explanation step can read it.
    sess["lp_diagnosis"] = diag_dict

    diag_conf = float(diag_dict.get("diagnostic_confidence", 1.0))
    probe_count = int(sess.get("probe_count", 0))
    should_probe = (
        diag_dict and
        diag_dict.get("current_lp_level") and
        diag_conf < QUIZ_PROBE_CONFIDENCE_FLOOR and
        probe_count < QUIZ_MAX_PROBES
    )

    if should_probe:
        target_level = diag_dict.get("target_lp_level") or "L3"

        # Tier 1 — DEPTH PROBE (jargon trap or surface-similarity gate).
        # Highest priority: depth signals indicate the level grader may have
        # been fooled by surface vocabulary. Counts toward the same ladder
        # bookkeeping as the sub-criterion picker (probe_count + probed_criteria).
        depth_question = None
        depth_reason   = None
        try:
            from src.orchestrator.depth_probe import select_depth_probe
            cat = _catalogue_as_catalogue_obj()
            if cat is not None:
                dp = select_depth_probe(
                    accumulated, cat, item["concept"],
                    already_probed=sess.get("probed_criteria") or [],
                )
                if dp is not None:
                    sess["probed_criteria"].append(dp.criterion_key)
                    sess["probe_count"] = probe_count + 1
                    return {
                        "type":               "probe",
                        "probe_question":     dp.question,
                        "probe_target_level": target_level,
                        "probe_round":        sess["probe_count"],
                        "probe_round_max":    QUIZ_MAX_PROBES,
                    }
        except Exception as e:
            print(f"[QuizApp] depth_probe failed: {e}")

        # Tier 2 — per-criterion sub-rubric picker (multi-facet ladder).
        criterion = _pick_next_criterion(
            item, sess.get("probed_criteria", []) or [],
            diag_dict=diag_dict, target_level=target_level,
        )
        if criterion:
            sess["probed_criteria"].append(criterion)
            sess["probe_count"] = probe_count + 1
            return {
                "type": "probe",
                "probe_question":      _make_probe_question(criterion),
                "probe_target_level":  target_level,
                "probe_round":         sess["probe_count"],
                "probe_round_max":     QUIZ_MAX_PROBES,
            }

    # Explanation path — use the FULL diagnosis to shape the Step-3 prompt.
    correct_opt = next(o for o in item["options"] if o.get("correct"))
    chosen_opt  = next(o for o in item["options"] if o["key"] == sess["choice"])
    chosen_wm   = None
    if not sess["is_correct"]:
        wm_id = chosen_opt.get("wm_id")
        chosen_wm = _wm_lookup(item["concept"], wm_id) if wm_id else None

    explanation = _build_explanation(
        item=item,
        student_belief=accumulated,
        is_correct=sess["is_correct"],
        chosen_opt=chosen_opt,
        correct_opt=correct_opt,
        chosen_wm=chosen_wm,
        diag_dict=diag_dict,
        teach_variant=sess.get("teach_variant", "control"),
    )
    return {
        "type":            "explanation",
        "explanation":     explanation,
        "correct_choice":  correct_opt["key"],
        "your_choice":     chosen_opt["key"],
    }


def _next_level(lvl: Optional[str]) -> str:
    """Step LP level up by one (capped at L4)."""
    order = ["L1", "L2", "L3", "L4"]
    if lvl not in order:
        return "L2"
    idx = order.index(lvl)
    return order[min(idx + 1, 3)]


def _pick_next_item(used: List[str]) -> Optional[Dict]:
    remaining = [q for q in QUIZ_ITEMS if q["id"] not in used]
    if not remaining:
        return None
    return random.choice(remaining)


# ── endpoints ─────────────────────────────────────────────────────────────────

@app.get("/api/start", response_model=StartResp)
def start(request: Request):
    """Start a new session and return the first MCQ (without answer keys).

    Resolves the student from ?token=... (HMAC-validated) or ?student=...
    (demo-mode) so DINA mastery and progression are scoped per-student
    instead of clobbering the shared "anon" key. Wired 2026-05-30 — see
    _resolve_student_id."""
    ident = _resolve_student_id(request)
    sid = _new_session(student_id=ident["student_id"],
                        role=ident["role"],
                        course=ident["course"])
    item = _pick_next_item([])
    sess = _sessions[sid]
    sess["current_item_id"] = item["id"]
    sess["item_started_at"] = time.time()
    # A/B variant for explanation phrasing (sticky-per-student).
    try:
        sess["teach_variant"] = assign_variant(
            ident["student_id"], "teach_prompt_v2") or "control"
    except Exception:
        sess["teach_variant"] = "control"
    # Audit the session-start event so the cohort/dashboard queries can
    # see active sessions per student.
    try:
        get_db().audit("quiz_session_start",
                       student_id=ident["student_id"],
                       payload={"session_id": sid, "role": ident["role"],
                                 "course": ident["course"],
                                 "first_item_id": item["id"]})
    except Exception as e:
        print(f"[student_app] audit fell through: {e}")
    return StartResp(session_id=sid, item=_safe_item(item))


@app.post("/api/answer", response_model=AnswerResp)
def answer(req: AnswerReq):
    """Record the student's MCQ choice and silently update DINA mastery."""
    sess = _sessions.get(req.session_id)
    if sess is None:
        raise HTTPException(status_code=404, detail="session not found")
    item = QUIZ_BY_ID.get(sess["current_item_id"])
    if item is None:
        raise HTTPException(status_code=400, detail="no active item")

    opt = next((o for o in item["options"] if o["key"] == req.choice), None)
    if opt is None:
        raise HTTPException(status_code=400, detail="invalid choice")

    is_correct = bool(opt.get("correct"))
    sess["choice"] = req.choice
    sess["is_correct"] = is_correct
    # Sanitise belief BEFORE any downstream LLM concatenation — quoted
    # injection markers are wrapped so the prompt builder treats them as
    # student-quoted text rather than instructions.
    sess["belief"] = _sanitise_student_input((req.belief or "").strip())

    # Capture mastery BEFORE the update so the audit row carries both
    # mastery_before and mastery_after for progression queries.
    try:
        m_before = float(_dina.get_mastery(
            sess["student_id"], item["concept"]).get(item["concept"], 0.0))
    except Exception:
        m_before = 0.0

    # Update DINA silently — the student never sees mastery.
    update_result = _dina.update(
        student_id=sess["student_id"],
        skill=item["concept"],
        is_correct=is_correct,
    )
    sess["mastery_before"] = m_before
    sess["mastery_after"]  = float(update_result.get("mastery_after", m_before))

    return AnswerResp(accepted=True, needs_belief=True)


def _log_turn_completed(sess: Dict, item: Dict) -> None:
    """Write a `turn_completed` audit row so progression / forecast /
    cohort queries (db_store.progression_for, forecast_lp_advance,
    cohort_percentile) include quiz turns alongside chat-flow turns.

    Schema matches what the chat-flow writes (06a58ae / 11e38b0 commits)
    so the dashboard joins cleanly across surfaces.
    """
    diag = sess.get("lp_diagnosis") or {}
    payload = {
        "session_id":      None,  # quiz sessions don't have a chat session_id
        "surface":         "quiz",
        "skill":           item.get("concept"),
        "item_id":         sess.get("current_item_id"),
        "choice":          sess.get("choice"),
        "is_correct":      sess.get("is_correct"),
        "belief":          sess.get("belief") or "",
        "probe_count":     sess.get("probe_count", 0),
        "lp_before":       sess.get("lp_before", "L1"),
        "lp_after":        diag.get("current_lp_level") or "L1",
        "mastery_before":  sess.get("mastery_before", 0.0),
        "mastery_after":   sess.get("mastery_after",  0.0),
        "intervention":    "quiz_explanation",
        "conf":            float(diag.get("diagnostic_confidence") or 0.0),
        "dwell_s":         round(time.time() - sess.get("item_started_at",
                                                          time.time()), 2),
        "teach_variant":   sess.get("teach_variant", "control"),
    }
    try:
        get_db().audit("turn_completed",
                       student_id=sess.get("student_id"),
                       payload=payload)
    except Exception as e:
        print(f"[student_app] turn_completed audit fell through: {e}")


def _advance_to_next_item(sess: Dict) -> Optional[str]:
    """Bookkeeping when the student finishes a quiz item — record history,
    write the audit row, reset belief / probe state, and return the next
    item id (or None)."""
    item = QUIZ_BY_ID.get(sess["current_item_id"])
    if item is not None:
        _log_turn_completed(sess, item)

    sess["history"].append({
        "item_id":      sess["current_item_id"],
        "choice":       sess["choice"],
        "is_correct":   sess["is_correct"],
        "probe_count":  sess.get("probe_count", 0),
    })
    used_ids = [h["item_id"] for h in sess["history"]]
    next_item = _pick_next_item(used_ids)
    if next_item is not None:
        sess["current_item_id"] = next_item["id"]
        sess["choice"]          = None
        sess["is_correct"]      = None
        sess["belief"]          = None
        sess["probe_count"]     = 0
        sess["probed_criteria"] = []
        sess["probe_answers"]   = []
        sess["item_started_at"] = time.time()
        sess["mastery_before"]  = None
        sess["mastery_after"]   = None
        sess["lp_before"]       = (sess.get("lp_diagnosis") or {}).get(
            "current_lp_level") or "L1"
        sess["lp_diagnosis"]    = None
        return next_item["id"]
    return None


@app.post("/api/correct", response_model=CorrectResp)
def correct(req: CorrectReq):
    """Grade the student's belief and either probe further or return the
    theory-grounded correction. Multi-turn ladder enabled — see
    _decide_probe_or_explain."""
    sess = _sessions.get(req.session_id)
    if sess is None:
        raise HTTPException(status_code=404, detail="session not found")
    item = QUIZ_BY_ID.get(sess["current_item_id"])
    if item is None:
        raise HTTPException(status_code=400, detail="no active item")

    sess["belief"]          = _sanitise_student_input((req.belief or "").strip())
    sess["probe_count"]     = 0     # fresh ladder per item
    sess["probed_criteria"] = []
    sess["probe_answers"]   = []

    decision = _decide_probe_or_explain(sess, item)
    correct_opt = next(o for o in item["options"] if o.get("correct"))
    chosen_opt  = next(o for o in item["options"] if o["key"] == sess["choice"])

    if decision["type"] == "probe":
        return CorrectResp(
            type="probe",
            title=item["title"],
            correct_choice=correct_opt["key"],
            your_choice=chosen_opt["key"],
            probe_question=decision["probe_question"],
            probe_target_level=decision["probe_target_level"],
            probe_round=decision["probe_round"],
            probe_round_max=decision["probe_round_max"],
        )

    # explanation path — advance to next item bookkeeping
    next_id = _advance_to_next_item(sess)
    return CorrectResp(
        type="explanation",
        title=item["title"],
        explanation=decision["explanation"],
        correct_choice=decision["correct_choice"],
        your_choice=decision["your_choice"],
        next_item_id=next_id,
    )


@app.post("/api/probe_answer", response_model=CorrectResp)
def probe_answer(req: ProbeAnswerReq):
    """Accept the student's reply to a follow-up probe, re-grade with the
    ACCUMULATED belief, and either probe again (up to QUIZ_MAX_PROBES) or
    return the explanation."""
    sess = _sessions.get(req.session_id)
    if sess is None:
        raise HTTPException(status_code=404, detail="session not found")
    item = QUIZ_BY_ID.get(sess["current_item_id"])
    if item is None:
        raise HTTPException(status_code=400, detail="no active item")

    sess.setdefault("probe_answers", []).append(
        _sanitise_student_input((req.probe_answer or "").strip()))

    decision = _decide_probe_or_explain(sess, item)
    correct_opt = next(o for o in item["options"] if o.get("correct"))
    chosen_opt  = next(o for o in item["options"] if o["key"] == sess["choice"])

    if decision["type"] == "probe":
        return CorrectResp(
            type="probe",
            title=item["title"],
            correct_choice=correct_opt["key"],
            your_choice=chosen_opt["key"],
            probe_question=decision["probe_question"],
            probe_target_level=decision["probe_target_level"],
            probe_round=decision["probe_round"],
            probe_round_max=decision["probe_round_max"],
        )

    next_id = _advance_to_next_item(sess)
    return CorrectResp(
        type="explanation",
        title=item["title"],
        explanation=decision["explanation"],
        correct_choice=decision["correct_choice"],
        your_choice=decision["your_choice"],
        next_item_id=next_id,
    )


@app.get("/api/item/{item_id}")
def get_item(item_id: str):
    item = QUIZ_BY_ID.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="item not found")
    return _safe_item(item)


@app.get("/api/health")
def health():
    return {"status": "ok", "items": len(QUIZ_ITEMS)}


# ── Identity / consent / GDPR endpoints (wired 2026-05-30) ───────────────────

class WhoAmIResp(BaseModel):
    student_id: str
    role: str
    course: str
    teach_variant: Optional[str] = None
    consent_given: bool = False


@app.get("/api/me", response_model=WhoAmIResp)
def whoami(request: Request):
    """Identity probe — returns the resolved student_id + role + course +
    the sticky A/B variant + current consent status. The UI calls this on
    page load to know which student key it's bound to."""
    ident = _resolve_student_id(request)
    sid = ident["student_id"]
    try:
        consent = bool(get_db().has_consent(sid))
    except Exception:
        consent = False
    try:
        variant = assign_variant(sid, "teach_prompt_v2") or "control"
    except Exception:
        variant = "control"
    return WhoAmIResp(student_id=sid, role=ident["role"], course=ident["course"],
                       teach_variant=variant, consent_given=consent)


class ConsentReq(BaseModel):
    given: bool


@app.post("/api/me/consent")
def set_consent(req: ConsentReq, request: Request):
    """Record (or revoke) consent for storing the student's progression
    data. Audited so the dashboard can show "consent received YYYY-MM-DD"."""
    ident = _resolve_student_id(request)
    sid = ident["student_id"]
    try:
        get_db().set_consent(sid, bool(req.given))
        get_db().audit("consent_set", student_id=sid,
                       payload={"given": bool(req.given)})
        return {"ok": True, "student_id": sid, "consent_given": bool(req.given)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"consent write failed: {e}")


@app.post("/api/me/delete")
def gdpr_delete(request: Request):
    """GDPR Article 17 — right to erasure. Removes mastery, audit rows,
    A/B assignments, and student-state for the resolved student. Writes a
    tombstone audit row that survives the deletion. Mirrors
    scripts/gdpr_admin.py for self-serve use from the UI."""
    ident = _resolve_student_id(request)
    sid = ident["student_id"]
    if sid in ("anon", ""):
        raise HTTPException(status_code=400,
                              detail="cannot delete the anonymous shared key")
    try:
        result = get_db().delete_student(sid)
        # Also drop any in-memory sessions for this student.
        for s_id, s in list(_sessions.items()):
            if s.get("student_id") == sid:
                _sessions.pop(s_id, None)
        return {"ok": True, "student_id": sid, "deleted_rows": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"delete failed: {e}")


# ── Fact-check pass (added 2026-05-30) ──────────────────────────────────────
# Why: the LP-shape forces mechanism vocabulary (compile-time / runtime,
# heap / stack, reference / value). On smaller backbones, the model
# sometimes confuses the categories — e.g. "the loop condition is checked
# at compile-time" (wrong — runtime per iteration). A factually wrong tutor
# is worse than no tutor. This second LLM pass narrowly checks for those
# specific category errors and, if found, strips the offending sentence
# rather than letting it reach the student.
#
# Scoped intentionally tight: we do NOT try to fact-check Java in general
# (the small model isn't reliable enough to grade itself on arbitrary
# claims). We only flag the four error patterns that the prior run
# (output/tutor_comparison_2026-05-30_152306/) actually surfaced.

_FACTCHECK_PROMPT_LEGACY_UNUSED = """You are a Java expert reviewing a tutor's reply for ONE specific category of factual error.

ONLY flag a sentence if it makes ONE of these specific mistakes:
  A. Says something happens "at compile-time" when it actually happens at runtime
     (e.g. "Java creates new String objects on the heap at compile-time" — WRONG;
      the allocation happens at runtime).
  B. Says a loop condition is "checked at compile-time" or "initialized at compile-time"
     (loop conditions are evaluated at runtime, every iteration).
  C. Says a primitive int / boolean is stored "on the heap" (primitives in local
     variables and parameters live on the stack; only object fields live on the heap).
  D. Says == on String objects compares values / contents (== compares references).

Reply with a JSON object:
  {{"ok": true}}                                if no error of the above kinds
  {{"ok": false, "bad_sentences": ["<verbatim sentence to remove>", ...]}}

Do NOT flag anything outside the four categories above. Do NOT flag stylistic issues.
Do NOT explain. Only output the JSON.

Tutor reply to review:
\"\"\"
{reply}
\"\"\"
"""


import re as _fc_re

# Regex patterns for the specific factually-wrong phrase-shapes the
# prior comparison runs surfaced. Each pattern must match a LITERAL
# wrong claim — false positives are a worse outcome than false negatives
# (a fact-check that strips correct sentences damages the response).
# Calibrated from output/tutor_comparison_2026-05-30_152306/ + 172527/.
_FACTCHECK_PATTERNS = [
    # A-fwd: "at compile-time" followed by a runtime-implying verb
    (_fc_re.compile(
        r"\bat compile[- ]time\b[^.!?]*\b("
        r"allocate[ds]?|create[ds]?|check[ds]?|initiali[sz]e[ds]?|"
        r"stor(?:e[ds]?|ing)|happen[ds]?|evaluate[ds]?|"
        r"hands? back|knows? (?:you'?re )?dividing|performs? an integer division"
        r")\b",
        _fc_re.IGNORECASE),
     "compile-time confused with runtime"),
    # A-rev: runtime verb preceding "at compile-time"
    # (e.g. "checking references at compile-time", "evaluating the loop condition at compile-time")
    (_fc_re.compile(
        r"\b(check(?:s|ing|ed)?|evaluat(?:es|ing|ed)?|compar(?:es|ing|ed)?|"
        r"compute[ds]?|computing|resolv(?:es|ing|ed)?|"
        r"allocate[ds]?|allocating|caus(?:es|ed|ing)|"
        r"throw(?:s|ing|n)?|raise[ds]?|raising|"
        r"happen[s]?|happening|occur[s]?|occurring|"
        r"(?:integer )?division|"
        r"executes?|executing|run[s]?|running)\b[^.!?]*"
        r"\bat compile[- ]time\b",
        _fc_re.IGNORECASE),
     "runtime operation incorrectly placed at compile-time"),
    # B specifically: loop condition "checked at compile-time"
    (_fc_re.compile(
        r"\bloop (?:condition|index|counter)[^.!?]*\bat compile[- ]time\b",
        _fc_re.IGNORECASE),
     "loop condition incorrectly said to be compile-time"),
    # C: primitive "stored on the heap"
    (_fc_re.compile(
        r"\b(?:primitive|local int|local boolean|local variable)\b[^.!?]*"
        r"\bstor(?:e[ds]?|ing)\b[^.!?]*\bon the heap\b",
        _fc_re.IGNORECASE),
     "primitive incorrectly said to be on the heap"),
    # D: == on Strings "compares contents/values"
    (_fc_re.compile(
        r"==[^.!?]*\bString[s]?\b[^.!?]*\bcompares? (?:contents?|values?)\b",
        _fc_re.IGNORECASE),
     "== said to compare contents on String"),
]


def _factcheck_mechanism_claims(reply: str, model: str = None) -> str:
    """Deterministic regex fact-check. Strips sentences containing literal
    phrase-shapes known to be factually wrong. Zero false positives by
    construction.

    v1 used an 8B LLM grader and produced 2/3 false positives — stripping
    CORRECT sentences. Regex is more precise, recall is lower but the
    failure cases it does catch are the recurring ones.

    `model` accepted but unused (kept for API stability).
    """
    if not reply or len(reply.split()) < 6:
        return reply
    try:
        sentences = _fc_re.split(r'(?<=[.!?])\s+', reply)
        clean = []
        stripped = []
        for s in sentences:
            hit = None
            for pat, label in _FACTCHECK_PATTERNS:
                if pat.search(s):
                    hit = label
                    break
            if hit:
                stripped.append((hit, s.strip()))
            else:
                clean.append(s)
        if not stripped:
            return reply
        cleaned = " ".join(clean).strip()
        # Don't gut the response. If stripping leaves <25 tokens, the
        # remainder is too short to teach. Keep the original (with the
        # error in the logs) — a partial error in 60 useful tokens beats
        # 20 useless tokens.
        if len(cleaned.split()) < 25:
            for label, s in stripped:
                print(f"[factcheck] WOULD strip ({label}) but result would be "
                      f"<25 tok; keeping original. Bad: {s[:90]}")
            return reply
        for label, s in stripped:
            print(f"[factcheck] stripped ({label}): {s[:90]}{'...' if len(s)>90 else ''}")
        return cleaned
    except Exception as e:
        print(f"[factcheck] pass fell through: {e}")
        return reply


# ── theory-grounded correction text ──────────────────────────────────────────

def _build_explanation(
    item: Dict,
    student_belief: str,
    is_correct: bool,
    chosen_opt: Dict,
    correct_opt: Dict,
    chosen_wm: Optional[Dict],
    diag_dict: Optional[Dict] = None,
    teach_variant: str = "control",
) -> str:
    """Compose a level-aware, theory-grounded teaching message.

    `diag_dict` is the FULL CPAL diagnosis dict (LPDiagnostic.to_dict()) for
    the student's belief on this concept — when present it drives the shape
    of the explanation (L1 worked example, L2 mechanism scaffold, L3
    transfer prompt, L4 design rationale). Falls back to the legacy generic
    shape when no diagnosis is available.
    """
    rubric = _lp_rubric(item["concept"])
    target_level = rubric.get("L3") or rubric.get("L4") or ""
    lp_level = (diag_dict or {}).get("current_lp_level")

    llm_text = _try_ollama(
        item=item,
        student_belief=student_belief,
        is_correct=is_correct,
        chosen_opt=chosen_opt,
        correct_opt=correct_opt,
        chosen_wm=chosen_wm,
        target_level=target_level,
        lp_level=lp_level,
        diag_dict=diag_dict,
        teach_variant=teach_variant,
    )
    if llm_text:
        return llm_text

    return _template_explanation(
        item=item,
        student_belief=student_belief,
        is_correct=is_correct,
        chosen_opt=chosen_opt,
        correct_opt=correct_opt,
        chosen_wm=chosen_wm,
        target_level=target_level,
    )


def _template_explanation(item, student_belief, is_correct, chosen_opt,
                          correct_opt, chosen_wm, target_level) -> str:
    lines: List[str] = []
    if is_correct:
        lines.append(
            f"Yes — option {chosen_opt['key']} is the right one. "
            f"{correct_opt['text']}"
        )
    else:
        lines.append(
            f"Not quite. You chose {chosen_opt['key']}, but the right answer "
            f"is {correct_opt['key']}: {correct_opt['text']}"
        )
        if chosen_wm:
            lines.append("")
            lines.append("Where that reasoning comes from:")
            lines.append(f"  • Belief in play: {chosen_wm.get('wrong_belief', '')}")
            origin = chosen_wm.get("origin")
            if origin:
                lines.append(f"  • Why it feels right: {origin}")

    if student_belief:
        lines.append("")
        lines.append("On your own words:")
        lines.append(f"  “{student_belief}”")
        lines.append(
            "  — keep the part that matches the rule below, and revise the rest "
            "so your mental model lines up with how Java actually evaluates this."
        )

    if target_level:
        lines.append("")
        lines.append("The underlying idea (target understanding):")
        lines.append(f"  {target_level}")

    return "\n".join(lines).strip()


def _try_ollama(item, student_belief, is_correct, chosen_opt, correct_opt,
                chosen_wm, target_level,
                lp_level: Optional[str] = None,
                diag_dict: Optional[Dict] = None,
                teach_variant: str = "control") -> Optional[str]:
    """Best-effort LLM call — now level-aware + anti-cliche guarded.

    The explanation SHAPE branches by the student's LP level:
      L1 → worked example (rule + 4-line snippet + key mechanism + check)
      L2 → mechanism scaffold (compile-time / runtime / heap / reference)
      L3 → confirm + transfer prompt (novel application, no re-teach)
      L4 → design rationale + edge case (no basics, generalisation-level)

    Anti-cliche guardrails applied in all branches.
    """
    try:
        import os, requests
        tags = requests.get("http://localhost:11434/api/tags", timeout=1.5)
        models = [m.get("name") for m in tags.json().get("models", []) if m.get("name")]
        if not models:
            return None
        # Backbone selection (2026-05-30 — reverted to llama3.1:8b after
        # qwen2.5:14b proved ~2x slower per token on this hardware. The
        # fact-check pass + tighter LP-shape remain — those are
        # model-independent improvements that benefit any backbone).
        # Env var override lets ops upgrade later (e.g. CPAL_OLLAMA_MODEL=qwen2.5:14b).
        model = (
            os.environ.get("CPAL_OLLAMA_MODEL")
            or next((m for m in models
                     if "llama3.3" in m.lower() or "llama3.1" in m.lower()), None)
            or next((m for m in models if "llama3" in m.lower()), None)
            or next((m for m in models if "qwen" in m.lower() and "coder" not in m.lower()), None)
            or models[0]
        )

        wm_block = ""
        if chosen_wm:
            wm_block = (
                "The student's choice maps to this catalogued misconception:\n"
                f"  belief: {chosen_wm.get('wrong_belief', '')}\n"
                f"  origin: {chosen_wm.get('origin', '')}\n\n"
                "Address THIS specific false belief in your reply — name it "
                "in the student's voice, then correct it.\n"
            )

        # Level-aware shape — one of four pedagogical templates.
        lp_shape = _shape_for_level(lp_level)

        # Anti-cliche guardrails — compact, same banned list as the chat-flow.
        anti_cliche = (
            "STYLE: open with the diagnosis or the example, never a preamble. "
            "Every sentence must either name a specific false belief, name a "
            "specific Java mechanism, show concrete code/trace, or ask a "
            "concrete predict-this question. Reassurance (if any) comes after "
            "teaching, one short sentence.\n"
            "Banned phrases: \"great question\", \"good question\", "
            "\"let's dive\", \"let's dive deeper\", \"dive into\", "
            "\"delve into\", \"let's break this down\", \"let's understand\", "
            "\"let's see\", \"let us\", \"don't worry\", \"no worries\", "
            "\"as a beginner\", \"it's important to know\", \"remember that\", "
            "\"hopefully\", \"we'll come back to that\", \"in summary\", "
            "\"to recap\", \"great job\"."
        )

        # A/B variant — "verbose" asks the model to restate the question
        # in the student's words before answering (encoding-prompt
        # experiment teach_prompt_v2, ab_testing.py).
        variant_prefix = ""
        if teach_variant == "verbose":
            variant_prefix = (
                "Before answering, restate the question in one sentence "
                "in your own words to make sure you understood it. Then proceed.\n\n"
            )

        prompt = (
            "You are a Java tutor for a first-year student. Respond in 3-4 "
            "short sentences — be disciplined and tight, every sentence must "
            "earn its place. Do NOT mention mastery, scores, levels, models, "
            "BKT, DINA, LP, or any internal metric. Address the student "
            "directly.\n\n"
            f"{variant_prefix}"
            f"{anti_cliche}\n\n"
            f"Topic: {item['title']} ({item['concept']})\n\n"
            f"Code:\n{item['code']}\n\n"
            f"Question: {item['question']}\n"
            f"Correct option ({correct_opt['key']}): {correct_opt['text']}\n"
            f"Student's choice ({chosen_opt['key']}): {chosen_opt['text']}\n"
            f"Was the student correct? {'yes' if is_correct else 'no'}\n\n"
            f"Student wrote in their own words: \"{student_belief or '(nothing)'}\"\n\n"
            f"{wm_block}"
            f"Target understanding to land on: {target_level}\n\n"
            f"PEDAGOGICAL SHAPE for this turn ({lp_level or 'unknown'}):\n"
            f"{lp_shape}\n\n"
            "Write the response now."
        )

        r = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=60,
        )
        r.raise_for_status()
        reply = (r.json().get("response") or "").strip() or None
        if reply:
            # Fact-check pass — strip sentences that confuse compile-time
            # vs runtime, heap vs stack, or reference vs value equality.
            # See _factcheck_mechanism_claims for the four categories.
            reply = _factcheck_mechanism_claims(reply, model)
        return reply
    except Exception:
        return None


def _shape_for_level(lp_level: Optional[str]) -> str:
    """Return a compact, level-appropriate pedagogical instruction block.

    Tightened 2026-05-30: was 4-7 sentences (~140 tok responses), now 3-4
    sentences (~80 tok responses). Closer to Ruffle & Riley's discipline,
    reduces cognitive load, forces the prompt to earn each sentence.
    Reduces the surface area where the small backbone can hallucinate
    mechanism details.
    """
    if lp_level == "L4":
        return (
            "L4 — generalising student. Do NOT re-teach. Confirm the "
            "generalisation in one sentence; name ONE edge case that stretches "
            "the principle (string interning, autoboxing identity, "
            "primitive-vs-reference); end with a design-rationale question."
        )
    if lp_level == "L3":
        return (
            "L3 — student traced the mechanism. Confirm in one sentence; "
            "present ONE novel application of the same mechanism; ask the "
            "student to name the SHARED mechanism between the two cases."
        )
    if lp_level == "L2":
        return (
            "L2 — student knows the rule, not the mechanism. Acknowledge the "
            "rule in ONE phrase; name the operative mechanism step (compile-"
            "time vs runtime; heap vs stack vs reference; condition checked "
            "before/after iteration); end with a predict-this question on a "
            "small variant."
        )
    # L1 or unknown
    return (
        "L1 — symptom level. Name the RULE the student missed in one plain "
        "sentence; show 2-3 lines of annotated Java; end with a predict-this "
        "check question on a tiny variant."
    )


# ── static frontend ──────────────────────────────────────────────────────────

STATIC_DIR = Path(__file__).resolve().parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    @app.get("/")
    def index():
        return FileResponse(str(STATIC_DIR / "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.student_app:app", host="0.0.0.0", port=8001, reload=False)
