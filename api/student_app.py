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
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parent.parent
_sys.path.insert(0, str(ROOT))

from src.models.dina import DINAModel  # noqa: E402


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


def _new_session(student_id: str = "anon") -> str:
    sid = uuid.uuid4().hex[:12]
    _sessions[sid] = {
        "student_id": student_id,
        "current_item_id": None,
        "choice": None,
        "is_correct": None,
        "belief": None,
        # --- multi-turn probe ladder (Phase 4) ---
        "probe_count":      0,           # probes issued for THIS item so far
        "probed_criteria":  [],          # criterion text strings already asked
        "probe_answers":    [],          # student's probe-answer texts in order
        "history": [],
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
def start():
    """Start a new session and return the first MCQ (without answer keys)."""
    sid = _new_session()
    item = _pick_next_item([])
    _sessions[sid]["current_item_id"] = item["id"]
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
    sess["belief"] = (req.belief or "").strip()

    # Update DINA silently — the student never sees mastery.
    _dina.update(
        student_id=sess["student_id"],
        skill=item["concept"],
        is_correct=is_correct,
    )

    return AnswerResp(accepted=True, needs_belief=True)


def _advance_to_next_item(sess: Dict) -> Optional[str]:
    """Bookkeeping when the student finishes a quiz item — record history,
    reset belief / probe state, and return the next item id (or None)."""
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

    sess["belief"]          = (req.belief or "").strip()
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

    sess.setdefault("probe_answers", []).append((req.probe_answer or "").strip())

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


# ── theory-grounded correction text ──────────────────────────────────────────

def _build_explanation(
    item: Dict,
    student_belief: str,
    is_correct: bool,
    chosen_opt: Dict,
    correct_opt: Dict,
    chosen_wm: Optional[Dict],
    diag_dict: Optional[Dict] = None,
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
                diag_dict: Optional[Dict] = None) -> Optional[str]:
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
        # Env var override (matches the chat-flow generator). Fall back to
        # llama3.1 → general-purpose models are less prompt-suspicious than
        # coder-specialised ones on long prescriptive prompts.
        model = (
            os.environ.get("CPAL_OLLAMA_MODEL")
            or next((m for m in models
                     if "llama3.1" in m.lower() or "llama3.3" in m.lower()), None)
            or next((m for m in models if "llama3" in m.lower()), None)
            or next((m for m in models if "qwen" in m.lower() and "coder" in m.lower()), None)
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

        prompt = (
            "You are a Java tutor for a first-year student. Respond in 4-7 "
            "short sentences. Do NOT mention mastery, scores, levels, models, "
            "BKT, DINA, LP, or any internal metric. Address the student "
            "directly.\n\n"
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
        return (r.json().get("response") or "").strip() or None
    except Exception:
        return None


def _shape_for_level(lp_level: Optional[str]) -> str:
    """Return a compact, level-appropriate pedagogical instruction block.

    Matches the LP-3 SIX-STEP shapes the chat-flow uses but pared down for
    the quiz's 4-7 sentence budget.
    """
    if lp_level == "L4":
        return (
            "L4 — generalising student. Do NOT re-teach the concept; the "
            "student already abstracted it. Confirm the generalisation and "
            "name the principle. Present ONE stretch / edge case where the "
            "principle interacts with another feature (e.g. string interning, "
            "autoboxing identity, primitive-vs-reference). End with a "
            "design-rationale question: why did Java's designers make this "
            "choice, or what is the trade-off?"
        )
    if lp_level == "L3":
        return (
            "L3 — student traced the mechanism. Do NOT re-explain what they "
            "already understand. Confirm their mechanism in ONE sentence, "
            "then present a NOVEL application of the same mechanism (a "
            "different concept or code pattern). End with a question asking "
            "the student to name the SHARED mechanism between the two cases."
        )
    if lp_level == "L2":
        return (
            "L2 — student knows the rule, not the mechanism. Acknowledge "
            "the rule briefly, then introduce the MECHANISM underneath — "
            "name the operative step (compile-time vs runtime; heap vs "
            "stack vs reference; condition checked before/after iteration; "
            "length-1 vs length). Walk one short example. End with a "
            "predict-this question on a small variant."
        )
    # L1 or unknown
    return (
        "L1 — pure symptom level. Name the RULE the student missed in one "
        "plain sentence. Show a 4-6 line annotated Java example. Walk what "
        "Java does at each line. Name the ONE key mechanism the student "
        "should take away. End with a predict-this check question."
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
