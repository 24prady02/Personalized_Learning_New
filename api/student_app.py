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
    title: str
    explanation: str      # theory-grounded teaching message
    correct_choice: str
    your_choice: str
    next_item_id: Optional[str] = None


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


def _new_session(student_id: str = "anon") -> str:
    sid = uuid.uuid4().hex[:12]
    _sessions[sid] = {
        "student_id": student_id,
        "current_item_id": None,
        "choice": None,
        "is_correct": None,
        "belief": None,
        "history": [],
    }
    return sid


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


@app.post("/api/correct", response_model=CorrectResp)
def correct(req: CorrectReq):
    """Return a theory-grounded correction. Uses the wrong-model catalogue +
    LP rubric to teach the underlying idea, never disclosing mastery numbers."""
    sess = _sessions.get(req.session_id)
    if sess is None:
        raise HTTPException(status_code=404, detail="session not found")
    item = QUIZ_BY_ID.get(sess["current_item_id"])
    if item is None:
        raise HTTPException(status_code=400, detail="no active item")

    sess["belief"] = (req.belief or "").strip()

    correct_opt = next(o for o in item["options"] if o.get("correct"))
    chosen_opt = next(o for o in item["options"] if o["key"] == sess["choice"])
    chosen_wm = None
    if not sess["is_correct"]:
        wm_id = chosen_opt.get("wm_id")
        chosen_wm = _wm_lookup(item["concept"], wm_id) if wm_id else None

    explanation = _build_explanation(
        item=item,
        student_belief=sess["belief"],
        is_correct=sess["is_correct"],
        chosen_opt=chosen_opt,
        correct_opt=correct_opt,
        chosen_wm=chosen_wm,
    )

    sess["history"].append({
        "item_id": item["id"],
        "choice": sess["choice"],
        "is_correct": sess["is_correct"],
    })
    used_ids = [h["item_id"] for h in sess["history"]]
    next_item = _pick_next_item(used_ids)
    if next_item is not None:
        sess["current_item_id"] = next_item["id"]
        sess["choice"] = None
        sess["is_correct"] = None
        sess["belief"] = None
        next_id = next_item["id"]
    else:
        next_id = None

    return CorrectResp(
        title=item["title"],
        explanation=explanation,
        correct_choice=correct_opt["key"],
        your_choice=chosen_opt["key"],
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
) -> str:
    """Compose a teaching message that addresses the student's belief and
    explains the underlying theory using the wrong-model + LP rubric. Tries
    Ollama first; on any failure or absence, falls back to a deterministic
    catalogue-grounded template."""
    rubric = _lp_rubric(item["concept"])
    target_level = rubric.get("L3") or rubric.get("L4") or ""

    llm_text = _try_ollama(
        item=item,
        student_belief=student_belief,
        is_correct=is_correct,
        chosen_opt=chosen_opt,
        correct_opt=correct_opt,
        chosen_wm=chosen_wm,
        target_level=target_level,
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
                chosen_wm, target_level) -> Optional[str]:
    """Best-effort LLM call. Returns None if Ollama isn't reachable or fails."""
    try:
        import requests
        tags = requests.get("http://localhost:11434/api/tags", timeout=1.5)
        models = [m.get("name") for m in tags.json().get("models", []) if m.get("name")]
        if not models:
            return None
        model = next(
            (m for m in models if "qwen" in m.lower() and "coder" in m.lower()),
            None,
        ) or next(
            (m for m in models if "llama3" in m.lower()),
            None,
        ) or models[0]

        wm_block = ""
        if chosen_wm:
            wm_block = (
                "Underlying misconception the student's choice maps to:\n"
                f"  belief: {chosen_wm.get('wrong_belief', '')}\n"
                f"  origin: {chosen_wm.get('origin', '')}\n"
            )

        prompt = (
            "You are a Java tutor for a first-year student. Respond in 4-7 short "
            "sentences. Do NOT mention mastery, scores, levels, models, BKT, DINA, "
            "or any internal metric. Address the student directly. If they were "
            "right, confirm and reinforce the rule. If they were wrong, name the "
            "rule that actually applies, then re-explain it in light of what they "
            "wrote.\n\n"
            f"Topic: {item['title']} ({item['concept']})\n\n"
            f"Code:\n{item['code']}\n\n"
            f"Question: {item['question']}\n"
            f"Correct option ({correct_opt['key']}): {correct_opt['text']}\n"
            f"Student's choice ({chosen_opt['key']}): {chosen_opt['text']}\n"
            f"Was the student correct? {'yes' if is_correct else 'no'}\n\n"
            f"Student wrote in their own words: \"{student_belief or '(nothing)'}\"\n\n"
            f"{wm_block}"
            f"Target understanding to land on: {target_level}\n\n"
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
