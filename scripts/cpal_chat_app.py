"""
CPAL chat interface (quiz-first) — Gradio app wrapping the full diagnosis +
grounded-response pipeline.

Flow:
  1. Pick a quiz from the bank (or enter a custom one)
  2. See the question + code + multiple-choice options
  3. Select the option you'd pick
  4. Write your reasoning for that pick
  5. Submit → diagnosis panel fills in (LP + wrong-model distributions),
     tutor response streams in the chat below

Run:
    python scripts/cpal_chat_app.py                   # localhost:7860
    python scripts/cpal_chat_app.py --share           # public gradio.live
    python scripts/cpal_chat_app.py --port 8080       # custom port
"""
import os, re, sys, argparse
from pathlib import Path
from threading import Lock
from typing import Optional
import torch

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT))

import gradio as gr

from src.models.hvsae import HVSAE
from src.knowledge_graph.mental_models import get_catalogue
from src.orchestrator.lp_diagnostic import (
    LPDiagnostician, filter_interventions_by_lp, LP_INDEX, LP_ORDER,
)
from src.orchestrator.enhanced_personalized_generator import (
    EnhancedPersonalizedGenerator,
)


# =========================================================================
# Quiz bank
# =========================================================================
QUIZZES = [
    {
        "id": "SE-1",
        "concept": "string_equality",
        "question": "What does this print?",
        "code": (
            'String a = new String("hello");\n'
            'String b = new String("hello");\n'
            'System.out.println(a == b);'
        ),
        "options": {
            "A": "true — both strings contain 'hello'",
            "B": "false — they are different objects",
            "C": "Compile error",
            "D": "The word 'hello' prints twice",
        },
        "correct_answer": "B",
    },
    {
        "id": "ID-1",
        "concept": "integer_division",
        "question": "What does this print?",
        "code": (
            'double result = 5 / 2;\n'
            'System.out.println(result);'
        ),
        "options": {
            "A": "2.5",
            "B": "2.0",
            "C": "2",
            "D": "Compile error — mismatched types",
        },
        "correct_answer": "B",
    },
    {
        "id": "NP-1",
        "concept": "null_pointer",
        "question": "What happens at runtime when this is called?",
        "code": (
            'public class Widget {\n'
            '    private String label;\n'
            '    public String describe() {\n'
            '        return label.toUpperCase();\n'
            '    }\n'
            '}\n'
            '// elsewhere:\n'
            'Widget w = new Widget();\n'
            'System.out.println(w.describe());'
        ),
        "options": {
            "A": "Prints empty string",
            "B": 'Prints "LABEL" (the field name, uppercased)',
            "C": "Throws NullPointerException",
            "D": "Compile error — label not initialized",
        },
        "correct_answer": "C",
    },
    {
        "id": "AI-1",
        "concept": "array_index",
        "question": "What does this print?",
        "code": (
            'int[] arr = {10, 20, 30, 40, 50};\n'
            'System.out.println(arr[5]);'
        ),
        "options": {
            "A": "50 (the fifth element)",
            "B": "10 (the first element)",
            "C": "0 (default int)",
            "D": "ArrayIndexOutOfBoundsException",
        },
        "correct_answer": "D",
    },
    {
        "id": "VS-1",
        "concept": "variable_scope",
        "question": "What happens here?",
        "code": (
            'for (int i = 0; i < 3; i++) {\n'
            '    int total = i * 10;\n'
            '}\n'
            'System.out.println(total);'
        ),
        "options": {
            "A": "Prints 20 (last value of total)",
            "B": "Prints 0 (initial value)",
            "C": "Compile error",
            "D": "Prints 30",
        },
        "correct_answer": "C",
    },
    {
        "id": "BO-1",
        "concept": "boolean_operators",
        "question": "What does this print when score = 200?",
        "code": (
            'int score = 200;\n'
            'if (score >= 0 || score <= 100) {\n'
            '    System.out.println("Valid");\n'
            '} else {\n'
            '    System.out.println("Out of range");\n'
            '}'
        ),
        "options": {
            "A": "Valid",
            "B": "Out of range",
            "C": "Nothing — compile error",
            "D": "Valid, then Out of range",
        },
        "correct_answer": "A",
    },
    {
        "id": "IL-1",
        "concept": "infinite_loop",
        "question": "What happens when this runs?",
        "code": (
            'int i = 0;\n'
            'while (i < 10) {\n'
            '    System.out.println("value: " + i);\n'
            '}'
        ),
        "options": {
            "A": "Prints 'value: 0' through 'value: 9' and stops",
            "B": "Prints 'value: 0' forever",
            "C": "Prints nothing",
            "D": "Compile error",
        },
        "correct_answer": "B",
    },
]
QUIZ_BY_ID = {q["id"]: q for q in QUIZZES}
QUIZ_CHOICES = [(f"{q['id']} — {q['concept']} — {q['question'][:48]}", q["id"])
                for q in QUIZZES]


# =========================================================================
# Load models once
# =========================================================================
print("Loading HVSAE + catalogue + heads + generator...")
_ck = torch.load(ROOT / "checkpoints" / "best.pt",
                 map_location="cpu", weights_only=False)
HVSAE_MODEL = HVSAE(_ck["config"])
HVSAE_MODEL.load_state_dict(_ck["hvsae_state"])
HVSAE_MODEL.eval()
CATALOGUE = get_catalogue(
    ROOT / "data" / "mental_models" / "wrong_models_catalogue.json"
)
DX = LPDiagnostician(catalogue=CATALOGUE, hvsae_model=HVSAE_MODEL)
GEN = EnhancedPersonalizedGenerator()
try:
    from transformers import AutoTokenizer
    TOKENIZER = AutoTokenizer.from_pretrained("bert-base-uncased")
except Exception:
    TOKENIZER = None
_GEN_LOCK = Lock()
print("Ready.")


# =========================================================================
# Diagnosis helpers
# =========================================================================
def _hvsae_forward(text):
    if TOKENIZER is not None:
        ids = TOKENIZER(text, return_tensors="pt", padding=True,
                        truncation=True, max_length=128
                        )["input_ids"].long() % 6000
    else:
        ids = torch.randint(1, 5999, (1, 16))
    batch = {"code_tokens": torch.zeros(1, 10, dtype=torch.long),
             "text_tokens": ids,
             "action_sequence": torch.ones(1, 8, dtype=torch.long)}
    with torch.no_grad():
        out = HVSAE_MODEL.forward(batch, compute_graph=False)
    return out["latent"], torch.softmax(out["misconception_logits"], dim=-1)


def _diagnose(student_reasoning, concept_id, code, question, picked_option):
    full_text = (
        f"Quiz: {question}\n"
        f"My pick: {picked_option}\n"
        f"My reasoning: {student_reasoning}\n"
        f"Code:\n{code}"
    )
    latent, mp = _hvsae_forward(full_text)
    diag = DX.diagnose(
        student_id="chat_user",
        concept=concept_id,
        question_text=student_reasoning,
        stored_lp_level="L1", stored_lp_streak=0,
        hvsae_latent=latent, hvsae_misconception_probs=mp,
    ).to_dict()
    lvl_idx = LP_INDEX.get(diag["current_lp_level"], 0)
    if diag.get("wrong_model_id") and diag.get("match_score", 0) >= 0.4 \
            and lvl_idx >= LP_INDEX["L3"]:
        diag["fusion_note"] = (
            f"wrong-model {diag['wrong_model_id']} with conf "
            f"{diag['match_score']:.2f} → cap LP at L2")
        lvl_idx = LP_INDEX["L2"]
    else:
        diag["fusion_note"] = None
    diag["current_lp_level"] = LP_ORDER[lvl_idx]
    diag["target_lp_level"]  = LP_ORDER[min(lvl_idx + 1, 3)]
    return diag


def _format_diag(diag, concept_id):
    out = []
    out.append(f"### 🔍 Diagnosis\n")
    out.append(f"- **Concept**: `{concept_id}`\n")
    out.append(f"- **Wrong model**: **{diag.get('wrong_model_id') or '—'}** "
               f"(via `{diag.get('source')}`)\n")
    wm = CATALOGUE.get_wrong_model(concept_id,
                                    diag.get("wrong_model_id") or "")
    if wm:
        out.append(f"  - *belief*: {wm.wrong_belief}\n")
        out.append(f"  - *origin*: {wm.origin}\n")
    out.append(f"- **LP**: {diag['current_lp_level']} → target "
               f"{diag['target_lp_level']}\n")
    if diag.get("fusion_note"):
        out.append(f"- **Fusion rule fired**: {diag['fusion_note']}\n")
    out.append(f"\n#### LP-level distribution\n")
    for lvl in ("L1", "L2", "L3", "L4"):
        p = diag.get("trained_lp_probs", {}).get(lvl, 0.0)
        bar_len = int(round(p * 25))
        out.append(f"`{lvl}` {p*100:5.1f}% {'█'*bar_len}{'·'*(25-bar_len)}\n")
    out.append(f"\n#### Wrong-model distribution (within concept)\n")
    for t in diag.get("trained_wm_probs", []):
        p = t["prob"]
        bar_len = int(round(p * 25))
        out.append(f"`{t['wm_id']:6s}` {p*100:5.1f}% "
                   f"{'█'*bar_len}{'·'*(25-bar_len)}\n")
    out.append(f"\n#### Expert benchmark (L3 mechanism)\n")
    for k in diag.get("expert_benchmark_key_ideas", [])[:5]:
        out.append(f"- {k}\n")
    return "".join(out)


# =========================================================================
# UI callbacks
# =========================================================================
_PICKED_STYLE = (
    "display:block; background:#1e293b; color:#ffffff; font-style:italic; "
    "padding:8px 12px; border-radius:0 0 8px 8px; margin-top:-2px; "
    "border:1px solid #334155; border-top:none;"
)

def _quiz_card_md(q, picked_option_full=None):
    md = (
        f"**Quiz {q['id']} — `{q['concept']}`**  \n"
        f"{q['question']}\n"
        f"```java\n{q['code']}\n```"
    )
    if picked_option_full:
        safe = picked_option_full.replace("<", "&lt;").replace(">", "&gt;")
        md += f'\n<span style="{_PICKED_STYLE}">Your pick: {safe}</span>'
    return md


def on_select_quiz(quiz_id):
    q = QUIZ_BY_ID.get(quiz_id)
    if not q:
        return "", "", gr.update(choices=[], value=None), gr.update(value="", visible=False)
    md = _quiz_card_md(q)
    choices = [f"{k}. {v}" for k, v in q["options"].items()]
    return md, "", gr.update(choices=choices, value=None), gr.update(value="", visible=False)


def on_pick_option(quiz_id, picked_option_full):
    """Re-render the quiz card so the picked option appears in white italic
    directly under the code snippet."""
    q = QUIZ_BY_ID.get(quiz_id)
    if q is None:
        return gr.update()
    return _quiz_card_md(q, picked_option_full)


def _render_user_bubble(q, picked_option_text, reasoning):
    safe_pick = (picked_option_text or "").replace("<", "&lt;").replace(">", "&gt;")
    return (
        f"**Quiz {q['id']}** — *{q['concept']}*  \n"
        f"{q['question']}\n"
        f"```java\n{q['code']}\n```\n"
        f'<span style="{_PICKED_STYLE}">My pick: {safe_pick}</span>\n\n'
        f"**My reasoning:** {reasoning}"
    )


# =========================================================================
# Ongoing chat — multi-turn probe ladder + comprehensive-answer stage
# =========================================================================
# The system keeps probing as long as the student's belief isn't confidently
# at the target level. When a "stage" is reached (confidence high enough OR
# most sub-criteria demonstrated OR student requested OR chat depth cap),
# the tutor stops probing and produces a COMPREHENSIVE synthesis instead of
# another short reply. Probes themselves are dynamic — the question text is
# generated by the LLM per turn (see src/orchestrator/depth_probe.py).

CHAT_PROBE_CONFIDENCE_FLOOR   = 0.55   # under this -> still probing
CHAT_COMPREHENSIVE_CONF_FLOOR = 0.82   # at/above this -> stage reached
CHAT_MAX_PROBES               = 8      # hard cap; before this, the
                                       #   stage-reached detector usually
                                       #   triggers earlier.
# Regex patterns indicating the student is asking us to just give the answer.
_STUDENT_GIVE_UP = re.compile(
    r"\b(just (tell|give|show) me|"
    r"i give up|i don't know|idk\b|"
    r"reveal( the)? answer|show( the)? answer|"
    r"explain it|skip the (quiz|check))\b",
    re.I,
)


def _student_requested_answer(text: str) -> bool:
    return bool(_STUDENT_GIVE_UP.search(text or ""))


def _detect_other_concepts(student_text: str, quiz_concept: str) -> list:
    """Run ConceptResolver on the student's free-form text and return concept
    IDs OTHER than the quiz's tagged concept that the student also mentioned
    — so the chat can surface multi-concept awareness even though the quiz
    item is single-concept by design.

    Returns up to 3 other concepts, ranked by ConceptResolver confidence,
    above a low floor. Empty list when nothing additional was detected.
    """
    try:
        from src.orchestrator.concept_resolver import ConceptResolver
        # Lazily build a resolver — cheap (signature scoring + RAG lazy).
        global _CONCEPT_RESOLVER
        if "_CONCEPT_RESOLVER" not in globals():
            _CONCEPT_RESOLVER = ConceptResolver()
        ranked = _CONCEPT_RESOLVER.resolve({"question": student_text or ""})
    except Exception:
        return []
    others = [(c, s) for c, s in ranked
              if c != quiz_concept and c != "unknown" and s >= 0.25]
    return others[:3]


def _status_pill_with_diag(state: dict, diag: dict, base_status: str) -> str:
    """Append a per-concept/per-facet diagnostic line to the status pill so
    the student can see the ladder progressing in the UI. The base_status
    is the existing correct/wrong template; this prepends a second line
    with the live diagnostic state."""
    if not state or not diag:
        return base_status
    try:
        # `other_concepts` empty when the student hasn't strayed; resolver
        # call is cheap (signature scoring + RAG lazy).
        others = _detect_other_concepts(
            state.get("accumulated_belief", ""),
            QUIZ_BY_ID[state["quiz_id"]]["concept"] if state.get("quiz_id") else "",
        )
        diag_line = _status_md(state, diag, others)
    except Exception:
        diag_line = ""
    if not diag_line:
        return base_status
    return f"{base_status}  \n<small>{diag_line}</small>"


def _status_md(state: dict, diag: dict, other_concepts: list) -> str:
    """Compose the one-line status header shown above the chat input.

    Shows: focus concept · LP transition · facets probed · diagnostic
    confidence · stage trigger (if set) · OTHER concepts the student touched
    on in their free-form belief.
    """
    focus = state.get("pending_concept_id") or (state.get("quiz_id")
                                                  and QUIZ_BY_ID[state["quiz_id"]]["concept"])
    cur   = diag.get("current_lp_level", "?")
    tgt   = diag.get("target_lp_level", "?")
    target_sub = (diag.get("lp_sub_criteria") or {}).get(tgt) or []
    probed = [c for c in (state.get("probed_criteria") or [])
              if c in target_sub]
    facets_done = len(probed)
    facets_total = len(target_sub)
    conf  = float(diag.get("diagnostic_confidence", 0.0))

    parts = [f"**{focus or '—'}** · {cur} → {tgt}"]
    if facets_total:
        parts.append(f"facets {facets_done}/{facets_total}")
    parts.append(f"conf {conf:.2f}")
    trig = state.get("stage_trigger")
    if trig:
        parts.append(f"_stage_: **{trig}**")
    if other_concepts:
        also = ", ".join(c for c, _ in other_concepts)
        parts.append(f"also detected: {also}")
    return " · ".join(parts)


def _stage_reached(state: dict, diag: dict) -> Optional[str]:
    """Return a non-empty string naming the stage trigger, or None if not yet.

    Triggers (any one is sufficient):
      * 'force'              — caller forced via 'Reveal full answer'
      * 'student_request'    — accumulated belief contains an explicit request
      * 'high_confidence'    — diagnostic_confidence >= CHAT_COMPREHENSIVE_CONF_FLOOR
      * 'sub_criteria_done'  — every sub-criterion at target level has been probed
      * 'cap'                — CHAT_MAX_PROBES probes already issued
    """
    if state.get("force_comprehensive"):
        return "force"
    if _student_requested_answer(state.get("accumulated_belief", "")):
        return "student_request"
    conf = float(diag.get("diagnostic_confidence", 0.0))
    if conf >= CHAT_COMPREHENSIVE_CONF_FLOOR:
        return "high_confidence"
    target = diag.get("target_lp_level") or "L3"
    sub_map = diag.get("lp_sub_criteria") or {}
    sub = sub_map.get(target) or []
    if sub and all(c in state.get("probed_criteria", []) for c in sub):
        return "sub_criteria_done"
    if state.get("probe_count", 0) >= CHAT_MAX_PROBES:
        return "cap"
    return None


def _decide_probe_or_teach(state: dict):
    """Re-diagnose on the accumulated belief and decide probe vs teach.

    Composes deep-diagnostic with multi-turn / multi-facet:
      Tier 1 — DEPTH PROBE (jargon trap or embedding-similarity gate). Asks
               the student what they actually mean before accepting a
               vocabulary-rich belief at face value.
      Tier 2 — sub-criterion probe (next un-probed sentence at target LP).
      Tier 3 — teach.

    All three share the same `probe_count` / `probed_criteria` bookkeeping
    so depth probes naturally count toward the bounded ladder.

    Returns:
      ("probe", criterion_key_or_text, target_level, state, diag)
      ("teach", None,                   None,         state, diag)
    """
    q = QUIZ_BY_ID[state["quiz_id"]]
    diag = _diagnose(
        state["accumulated_belief"], q["concept"], q["code"],
        q["question"], state["picked_option_full"],
    )
    conf = float(diag.get("diagnostic_confidence", 1.0))

    # Stage-reached check FIRST — covers high confidence, student request,
    # sub-criteria exhausted, and the hard probe cap. When fired, the caller
    # streams a comprehensive synthesis instead of another short probe.
    stage = _stage_reached(state, diag)
    if stage is not None:
        state["stage_trigger"] = stage
        return ("teach", None, None, state, diag)

    if (conf < CHAT_PROBE_CONFIDENCE_FLOOR
            and state["probe_count"] < CHAT_MAX_PROBES):
        target = diag.get("target_lp_level") or "L3"

        # Tier 1 — depth probe. select_depth_probe returns a DepthProbe whose
        # `question` text is the ready-to-show probe. We stash it on `state`
        # so _probe_question_md_for can render the depth question (not a
        # generic "in your own words why is this true" wrapper).
        try:
            from src.orchestrator.depth_probe import select_depth_probe
            dp = select_depth_probe(
                state["accumulated_belief"], CATALOGUE, q["concept"],
                already_probed=state["probed_criteria"],
            )
        except Exception as _e:
            dp = None
        if dp is not None:
            state["probed_criteria"].append(dp.criterion_key)
            state["probe_count"] += 1
            state["pending_probe_text"]   = dp.question
            state["pending_probe_reason"] = dp.reason
            state["pending_concept_id"]   = q["concept"]
            state["pending_facet_pos"]    = None     # depth probes aren't facet-numbered
            state["pending_facet_total"]  = None
            return ("probe", dp.criterion_key, target, state, diag)

        # Tier 2 — per-criterion sub-rubric (multi-facet ladder).
        sub_map = diag.get("lp_sub_criteria") or {}
        sub = sub_map.get(target) or []
        for i, c in enumerate(sub, start=1):
            if c not in state["probed_criteria"]:
                state["probed_criteria"].append(c)
                state["probe_count"] += 1
                state["pending_probe_text"]   = None    # render via wrapper
                state["pending_probe_reason"] = "sub_criterion"
                state["pending_concept_id"]   = q["concept"]
                # Position of THIS criterion in the target-level facet list,
                # 1-indexed, plus total facets. Lets the UI show e.g.
                # "facet 2/5" so the student sees the multi-facet ladder
                # progressing.
                state["pending_facet_pos"]    = i
                state["pending_facet_total"]  = len(sub)
                return ("probe", c, target, state, diag)
    return ("teach", None, None, state, diag)


def _probe_question_md(criterion: str, target: str,
                       round_n: int, round_max: int,
                       depth_text: Optional[str] = None,
                       depth_reason: Optional[str] = None,
                       concept_id: Optional[str] = None,
                       facet_pos: Optional[int] = None,
                       facet_total: Optional[int] = None) -> str:
    """Render the probe question with FULL per-facet / per-concept labelling
    so the student can see which sub-skill of which concept is being probed.

    Format (sub-criterion probe):
       **Quick check 2** · `null_pointer` · facet 2/5 (L3 mechanism)
       In your own words — can you explain *why* this is true?
       > new allocates a heap object and returns its address

    Format (depth probe — jargon / similarity):
       **Quick check 3** · `string_equality` · depth check — vocabulary
       [LLM-generated probe text targeting the specific student wording]
    """
    # Header line — concept + facet position make the multi-facet / multi-
    # concept progression visible.
    parts = [f"**Quick check {round_n}**"]
    if concept_id:
        parts.append(f"`{concept_id}`")
    if depth_text:
        tag = {
            "jargon_trap":            "depth check — vocabulary",
            "high_sim_to_wrong":      "depth check — commit to the mechanism",
            "dynamic_sim_to_wrong":   "depth check — surface vs mechanism",
            "dynamic_vocab_density":  "depth check — trace your terms",
        }.get(depth_reason or "", "depth check")
        parts.append(f"<span style=\"color:#64748b\">({tag})</span>")
        header = " · ".join(parts)
        return f"{header}\n\n{depth_text}"

    if facet_pos and facet_total:
        parts.append(f"facet {facet_pos}/{facet_total}")
    if target:
        parts.append(f"<span style=\"color:#64748b\">({target} criterion)</span>")
    header = " · ".join(parts)
    c = (criterion or "").strip().rstrip(".")
    return (
        f"{header}\n\n"
        f"In your own words — can you explain *why* this is true?\n\n"
        f"> {c}"
    )


def stream_response(quiz_id, picked_option_full, reasoning, history, state):
    """Initial submit. Validates inputs, initialises the probe-ladder state,
    then either fires a probe (showing the probe panel) or streams the tutor
    teach reply. Outputs:
      (history, status, probe_panel_visibility, probe_question_md,
       probe_input_clear, state)
    """
    if not quiz_id:
        yield (history, gr.update(value="⚠️ Select a quiz first.", visible=True),
               gr.update(visible=False), "", "", state)
        return
    q = QUIZ_BY_ID.get(quiz_id)
    if q is None:
        yield (history, gr.update(value="⚠️ Unknown quiz.", visible=True),
               gr.update(visible=False), "", "", state)
        return
    if not picked_option_full:
        yield (history, gr.update(value="⚠️ Pick an option (A/B/C/D) before submitting.", visible=True),
               gr.update(visible=False), "", "", state)
        return
    if not reasoning.strip():
        yield (history, gr.update(value="⚠️ Write your reasoning for this pick, then submit.", visible=True),
               gr.update(visible=False), "", "", state)
        return

    # Parse letter off the option string "A. ..."
    picked_letter = picked_option_full.strip()[:1].upper()
    picked_text   = q["options"].get(picked_letter, picked_option_full)
    correct = (picked_letter == q["correct_answer"])

    # Build the correct/wrong status pill text up front so we can show it
    # IMMEDIATELY on submission — before diagnosis and the LLM run.
    if correct:
        status_template = "✅ **Correct!** Read your tutor's explanation below."
    else:
        status_template = (
            f"❌ You picked **{picked_letter}**, but the correct answer is "
            f"**{q['correct_answer']}** — {q['options'][q['correct_answer']]}. "
            f"Your tutor will walk you through it below."
        )

    # Fresh chat state for this question (multi-turn + dynamic-depth keys).
    state = {
        "quiz_id":             quiz_id,
        "picked_option_full":  picked_option_full,
        "picked_letter":       picked_letter,
        "picked_text":         picked_text,
        "is_correct":          correct,
        "status_template":     status_template,
        "accumulated_belief":  reasoning.strip(),
        "probe_count":         0,
        "probed_criteria":     [],
        "user_bubble":         _render_user_bubble(q, picked_text, reasoning),
        "pending_probe_text":  None,
        "pending_probe_reason": None,
        "force_comprehensive": False,
        "stage_trigger":       None,
    }

    # Decide on the FIRST belief: probe or teach?
    decision, criterion, target_level, state, diag = _decide_probe_or_teach(state)
    if decision == "probe":
        # Push the user bubble so the conversation shows what the student wrote,
        # then surface the probe panel with the targeted question.
        history = list(history) + [
            {"role": "user", "content": state["user_bubble"]},
            {"role": "assistant",
             "content": _probe_question_md(
                 criterion, target_level, state["probe_count"], CHAT_MAX_PROBES,
                 depth_text=state.get("pending_probe_text"),
                 depth_reason=state.get("pending_probe_reason"),
                 concept_id=state.get("pending_concept_id"),
                 facet_pos=state.get("pending_facet_pos"),
                 facet_total=state.get("pending_facet_total"),
             )},
        ]
        enriched = _status_pill_with_diag(
            state, diag,
            status_template + "  ·  *quick check before the answer…*",
        )
        yield (history,
               gr.update(value=enriched, visible=True),
               gr.update(visible=True),
               _probe_question_md(
                   criterion, target_level, state["probe_count"], CHAT_MAX_PROBES,
                   depth_text=state.get("pending_probe_text"),
                   depth_reason=state.get("pending_probe_reason"),
                   concept_id=state.get("pending_concept_id"),
                   facet_pos=state.get("pending_facet_pos"),
                   facet_total=state.get("pending_facet_total"),
               ),
               "",
               state)
        return

    # Otherwise stream the full teach reply.
    yield from _stream_teach(state, diag, history)


def _stream_teach(state, diag, history):
    """Stream the LLM tutor reply using the accumulated belief in `state`.
    Outputs the 6-tuple shape stream_response uses so Gradio reconciles it
    with the same set of outputs."""
    q = QUIZ_BY_ID[state["quiz_id"]]
    correct        = state["is_correct"]
    picked_letter  = state["picked_letter"]
    picked_text    = state["picked_text"]
    status_template = state["status_template"]
    reasoning      = state["accumulated_belief"]

    # Append user bubble + assistant placeholder. Skip user bubble if we
    # already appended it during a prior probe round.
    thinking_placeholder = (
        '<span style="color:#64748b; font-style:italic;">'
        'Tutor is thinking…</span>'
    )
    already_has_user = (history and history[-1].get("role") == "assistant"
                        and "Quick check" in (history[-1].get("content") or ""))
    if already_has_user:
        # Last turn was a probe — replace the probe question with the typing
        # indicator and add a fresh user bubble for the probe answer trail.
        history = list(history[:-1]) + [
            {"role": "user",
             "content": f"*(probe answers so far)* {reasoning}"},
            {"role": "assistant", "content": thinking_placeholder},
        ]
    else:
        history = list(history) + [
            {"role": "user", "content": state["user_bubble"]},
            {"role": "assistant", "content": thinking_placeholder},
        ]

    # Ongoing-chat mode: keep the chat panel VISIBLE through every teach
    # reply (was visible=False = hide-after-teach in the old one-shot mode).
    # The student can keep messaging until they start a new quiz.
    enriched = _status_pill_with_diag(state, diag, status_template)
    yield (history,
           gr.update(value=enriched, visible=True),
           gr.update(visible=True), "", "", state)

    # Intervention via LP-validity gate
    cands = [("transfer_task", 0.92), ("worked_example", 0.80),
             ("socratic_prompt", 0.70), ("trace_scaffold", 0.65)]
    filt = filter_interventions_by_lp(cands, diag["current_lp_level"])
    chosen = filt[0][0] if filt else "worked_example"

    student_state = {
        "student_id": "chat_user",
        "lp_diagnostic": diag,
        "recommended_intervention": {"type": chosen},
        "personality_profile": {"communication_style": "direct",
                                "learning_preference": "visual"},
        "bkt_mastery": {q["concept"]: 0.30},
        "emotional_state": "confused" if not correct else "engaged",
        "interaction_count": len(history) + 1,
    }
    analysis = {"emotion": {"primary": "confused" if not correct else "engaged",
                             "confidence": 0.7},
                "knowledge_gaps": [q["concept"]],
                "pedagogical_kg": {}}

    # Build the message the generator sees. When stage_trigger is set we
    # inject COMPREHENSIVE MODE instructions so the generator produces a
    # multi-section synthesis (confirm what student showed → address gaps
    # → walk the full L3 mechanism → transfer question), not just another
    # short probe-style reply.
    stage_trigger = state.get("stage_trigger")
    probed_so_far = state.get("probed_criteria") or []
    comprehensive_header = ""
    if stage_trigger:
        comprehensive_header = (
            "COMPREHENSIVE MODE — the student has reached the stage where "
            f"a full synthesis is appropriate (trigger: {stage_trigger}). "
            "Produce a multi-section reply with these parts, in order:\n"
            "  1. **What you understood** — name SPECIFIC parts of the "
            "     student's reasoning that were correct (quote them briefly).\n"
            "  2. **Where you were close** — name any parts that were "
            "     incomplete or partly wrong, in one or two short sentences.\n"
            "  3. **The full mechanism** — walk through what Java actually "
            "     does, end-to-end, in plain words. Use a short code trace "
            "     if it helps.\n"
            "  4. **Extension** — one question that would only be answerable "
            "     after grasping the full mechanism (transfer to a related "
            "     case, or design rationale).\n"
            "Tone: confident, no praise filler. Skip section headers if the "
            "student's answer was uniformly correct — go straight to the "
            "full mechanism + extension.\n\n"
            "Probe rounds so far: "
            f"{len(probed_so_far)} (criteria touched: {probed_so_far[:5]})\n\n"
        )
    tutor_input = (
        f"{comprehensive_header}"
        f"Student was given this quiz:\n"
        f"Q: {q['question']}\n\n"
        f"Code:\n```java\n{q['code']}\n```\n\n"
        f"Options:\n" + "\n".join(f"  {k}. {v}" for k, v in q["options"].items()) +
        f"\n\nStudent picked {picked_letter}: {picked_text}\n"
        f"Correct answer is {q['correct_answer']}: "
        f"{q['options'][q['correct_answer']]}\n"
        f"Student was {'CORRECT' if correct else 'INCORRECT'}.\n\n"
        f"Student's accumulated reasoning across the chat:\n{reasoning}"
    )

    buffer = {"text": ""}
    def on_chunk(piece):
        buffer["text"] += piece

    import threading, time
    done = {"flag": False, "err": None}

    def runner():
        try:
            GEN._stream_callback = on_chunk
            GEN.generate_personalized_response(
                student_id="chat_user",
                student_message=tutor_input,
                student_state=student_state,
                analysis=analysis,
                code=q["code"],
            )
        except Exception as e:
            done["err"] = str(e)
        finally:
            done["flag"] = True

    t = threading.Thread(target=runner, daemon=True)
    t.start()

    typing_enriched = _status_pill_with_diag(
        state, diag, status_template + "  ·  *tutor is typing…*",
    )
    last_len = 0
    while not done["flag"]:
        time.sleep(0.15)
        if len(buffer["text"]) > last_len:
            last_len = len(buffer["text"])
            history[-1]["content"] = buffer["text"]
            yield (history,
                   gr.update(value=typing_enriched, visible=True),
                   gr.update(visible=True), "", "", state)

    if done["err"]:
        history[-1]["content"] = f"❌ Generation failed: {done['err']}"
    else:
        history[-1]["content"] = buffer["text"] or "(empty response)"

    # After a comprehensive answer, reset force_comprehensive (and the probe
    # counter) so the student can keep following up — each new question
    # re-runs the diagnose/probe/teach loop fresh.
    if state.get("stage_trigger"):
        state["force_comprehensive"] = False
        state["stage_trigger"]       = None
        state["probe_count"]         = 0
    # Keep the chat panel visible for ongoing follow-ups.
    enriched_final = _status_pill_with_diag(state, diag, status_template)
    yield (history,
           gr.update(value=enriched_final, visible=True),
           gr.update(visible=True), "", "", state)


def on_reveal_answer(history, state):
    """Force the comprehensive synthesis on the next turn, regardless of
    confidence or remaining probe budget. Sets the force flag and routes
    through _decide_probe_or_teach — which returns ('teach', ...) when
    force_comprehensive is set, taking the comprehensive branch in
    _stream_teach."""
    if not state or not state.get("quiz_id"):
        yield (history,
               gr.update(value="(no active question — submit your reasoning first)",
                          visible=True),
               gr.update(visible=False), "", "", state)
        return
    state["force_comprehensive"] = True
    # Re-decide with the force flag — will land in the teach branch with
    # stage_trigger="force".
    decision, criterion, target_level, state, diag = _decide_probe_or_teach(state)
    # decision is always "teach" when force_comprehensive is True.
    yield from _stream_teach(state, diag, history)


def on_probe_answer(probe_answer, history, state):
    """Multi-turn probe ladder — the student answered a Quick check. Append
    to the accumulated belief, re-diagnose, then either probe again (up to
    CHAT_MAX_PROBES) or stream the final tutor reply with the whole trail."""
    if not state or not state.get("quiz_id"):
        yield (history, gr.update(value="(no active question)", visible=True),
               gr.update(visible=False), "", "", state)
        return
    ans = (probe_answer or "").strip()
    if not ans:
        yield (history, gr.update(value="⚠️ Write your answer to the quick check first.",
                                   visible=True),
               gr.update(visible=True),    # keep panel visible
               "",                          # don't overwrite the question
               "",                          # clear input
               state)
        return

    # Append the probe answer to accumulated belief.
    state["accumulated_belief"] = (
        (state["accumulated_belief"] + "  " + ans).strip()
    )

    decision, criterion, target_level, state, diag = _decide_probe_or_teach(state)
    if decision == "probe":
        # Replace the last assistant bubble (the previous probe question)
        # with the next probe question.
        next_q_md = _probe_question_md(
            criterion, target_level, state["probe_count"], CHAT_MAX_PROBES,
            depth_text=state.get("pending_probe_text"),
            depth_reason=state.get("pending_probe_reason"),
            concept_id=state.get("pending_concept_id"),
            facet_pos=state.get("pending_facet_pos"),
            facet_total=state.get("pending_facet_total"),
        )
        if history and history[-1].get("role") == "assistant":
            history = list(history[:-1]) + [
                {"role": "user",  "content": f"*(quick-check answer)* {ans}"},
                {"role": "assistant", "content": next_q_md},
            ]
        else:
            history = list(history) + [
                {"role": "user",  "content": f"*(quick-check answer)* {ans}"},
                {"role": "assistant", "content": next_q_md},
            ]
        yield (history,
               gr.update(value=state["status_template"]
                                + "  ·  *one more check before the answer…*",
                          visible=True),
               gr.update(visible=True),
               next_q_md, "", state)
        return

    # Teach — stream the full reply using the accumulated belief.
    yield from _stream_teach(state, diag, history)


def clear_chat():
    # Resets the chat state and hides the chat input panel until the
    # student submits initial reasoning again.
    empty_state = {
        "quiz_id": None, "picked_option_full": None, "picked_letter": None,
        "picked_text": None, "is_correct": False, "status_template": "",
        "accumulated_belief": "", "probe_count": 0, "probed_criteria": [],
        "user_bubble": "",
        # Dynamic-chat additions
        "pending_probe_text": None, "pending_probe_reason": None,
        "force_comprehensive": False, "stage_trigger": None,
    }
    return ([], gr.update(value="", visible=False),
            gr.update(visible=False), "", "", empty_state)


# =========================================================================
# UI
# =========================================================================
def build_app():
    with gr.Blocks(
        title="CPAL Tutor",
        theme=gr.themes.Soft(primary_hue="indigo", neutral_hue="slate"),
        css="""
        .gradio-container { max-width: 900px !important; margin: 0 auto !important; }
        .quiz-card  { background: transparent !important;
                      border: none !important; padding: 4px 0 !important; }
        .quiz-card p           { margin: 4px 0 !important; }
        .quiz-card pre         { margin: 6px 0 2px !important; }
        .quiz-card h1, .quiz-card h2, .quiz-card h3, .quiz-card h4 {
            margin: 0 0 6px !important;
        }

        /* ───── Kill the white code-block background EVERYWHERE ───── */
        /* Cover every wrapper Gradio / Prism may put around a code block:
           the <pre>, the <code> child, any div with code/codeblock/highlight
           in its class, and every descendant element. */
        .gradio-container pre,
        .gradio-container pre *,
        .gradio-container code,
        .gradio-container pre code,
        .gradio-container [class*="code"],
        .gradio-container [class*="codeblock"],
        .gradio-container [class*="code-block"],
        .gradio-container [class*="highlight"],
        .gradio-container .md pre,
        .gradio-container .md pre *,
        .gradio-container .message pre,
        .gradio-container .message pre *,
        .quiz-card pre,
        .quiz-card pre * {
            background: #1e293b !important;
            background-color: #1e293b !important;
            color: #f1f5f9 !important;
        }
        /* Outer pre keeps padding + rounded border; inner spans/code stay flat */
        .gradio-container pre {
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
            padding: 12px !important;
        }
        .gradio-container pre code,
        .gradio-container pre code * {
            background: transparent !important;
            background-color: transparent !important;
        }

        /* The "picked option" line that sits with the code snippet */
        .picked-option {
            display: block;
            background: #1e293b;
            color: #ffffff;
            font-style: italic;
            padding: 8px 12px;
            border-radius: 0 0 8px 8px;
            margin-top: -2px;
            border: 1px solid #334155;
            border-top: none;
        }
        .status-pill { padding: 10px 14px; border-radius: 8px;
                       background: #eef2ff; border: 1px solid #c7d2fe;
                       font-size: 14px; }
        .status-pill p { margin: 0 !important; }
        .hero h1 { margin-bottom: 4px; }
        .hero p  { color: #4b5563; margin-top: 0; }

        /* ───── Kill the white "generating" overlay flash ─────
           Gradio shows a translucent white loading layer over the chatbot
           while a function is running. That's the white patch with no text.
           Hide every loader / progress / status indicator. */
        .gradio-container .progress,
        .gradio-container .progress-bar,
        .gradio-container .progress-text,
        .gradio-container .status,
        .gradio-container [class*="status-tracker"],
        .gradio-container [class*="generating"],
        .gradio-container [class*="loading"],
        .gradio-container .eta-bar,
        .gradio-container [data-testid="progress"] {
            display: none !important;
        }
        /* Make sure the chatbot frame itself is transparent, not white */
        .gradio-container .chatbot { background: transparent !important; }
        """,
    ) as app:
        gr.Markdown(
            """
            <div class="hero">

            # 🎓 CPAL Tutor

            Your personalized Java learning assistant. Pick a quiz, share your
            thinking, and get a tailored explanation.

            </div>
            """
        )

        quiz_dd = gr.Dropdown(
            choices=QUIZ_CHOICES,
            value=QUIZ_CHOICES[0][1],
            label="📝 Choose a quiz",
            interactive=True,
        )
        quiz_card = gr.Markdown("", elem_classes=["quiz-card"])
        option_radio = gr.Radio(
            choices=[],
            label="Your answer",
            interactive=True,
        )
        reasoning_box = gr.Textbox(
            label="Why did you pick that?",
            lines=3,
            placeholder="Tell the tutor what made you choose this answer…",
        )
        with gr.Row():
            submit_btn = gr.Button("Get tutor response  →",
                                    variant="primary", scale=3)
            clear_btn  = gr.Button("Clear chat", scale=1)
        status = gr.Markdown("", elem_classes=["status-pill"], visible=False)

        # Ongoing chat panel — hidden until first submit, then always
        # visible. Per-concept / per-facet progress is shown in the status
        # pill above the chatbot (focus concept · LP → target · facets
        # probed / total · confidence · stage trigger · also-detected).
        with gr.Group(visible=False) as probe_panel:
            probe_question_md = gr.Markdown("")   # mirrors last tutor probe
            probe_input = gr.Textbox(
                label="Your message to the tutor",
                lines=3,
                placeholder="Reply, ask a follow-up, or paste more reasoning…",
            )
            with gr.Row():
                probe_submit_btn = gr.Button("Send  →", variant="primary",
                                              scale=3)
                reveal_btn = gr.Button("Reveal full answer", scale=1)

        chatbot = gr.Chatbot(
            label="Your tutor",
            type="messages",
            height=560,
            show_copy_button=True,
            avatar_images=(None, None),
        )

        # Ongoing-chat state — accumulated belief grows with every turn;
        # probed_criteria de-dups depth + sub-criterion probes;
        # force_comprehensive triggers the "Reveal full answer" path.
        probe_state = gr.State({
            "quiz_id": None, "picked_option_full": None, "picked_letter": None,
            "picked_text": None, "is_correct": False, "status_template": "",
            "accumulated_belief": "", "probe_count": 0, "probed_criteria": [],
            "user_bubble": "",
            "pending_probe_text": None, "pending_probe_reason": None,
            "force_comprehensive": False, "stage_trigger": None,
        })

        # Populate quiz card on load + on dropdown change.
        # show_progress="hidden" kills Gradio's white loading overlay so the
        # UI doesn't flash white while these events run.
        app.load(on_select_quiz, inputs=[quiz_dd],
                 outputs=[quiz_card, reasoning_box, option_radio, status],
                 show_progress="hidden")
        quiz_dd.change(on_select_quiz, inputs=[quiz_dd],
                       outputs=[quiz_card, reasoning_box, option_radio, status],
                       show_progress="hidden")

        # When the user picks an option, re-render the card to overlay the
        # picked option in white italic right under the code snippet.
        option_radio.change(on_pick_option,
                            inputs=[quiz_dd, option_radio],
                            outputs=[quiz_card],
                            show_progress="hidden")

        # Submit — initial belief. Either fires a probe (shows probe_panel)
        # or streams the tutor reply. The 6-tuple output reconciles
        # chatbot/status/probe_panel/probe_question_md/probe_input/state.
        submit_btn.click(
            stream_response,
            inputs=[quiz_dd, option_radio, reasoning_box, chatbot, probe_state],
            outputs=[chatbot, status, probe_panel, probe_question_md,
                     probe_input, probe_state],
            show_progress="hidden",
        )

        # Probe answer / chat message — appends to accumulated belief,
        # re-decides. After the first submit this becomes the persistent
        # chat input; works for both probe rounds and post-comprehensive
        # follow-ups.
        probe_submit_btn.click(
            on_probe_answer,
            inputs=[probe_input, chatbot, probe_state],
            outputs=[chatbot, status, probe_panel, probe_question_md,
                     probe_input, probe_state],
            show_progress="hidden",
        )

        # Reveal full answer — skips remaining probes and produces the
        # comprehensive synthesis on the next turn.
        reveal_btn.click(
            on_reveal_answer,
            inputs=[chatbot, probe_state],
            outputs=[chatbot, status, probe_panel, probe_question_md,
                     probe_input, probe_state],
            show_progress="hidden",
        )

        clear_btn.click(
            clear_chat, None,
            [chatbot, status, probe_panel, probe_question_md,
             probe_input, probe_state],
            show_progress="hidden",
        )

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--share", action="store_true",
                        help="expose via gradio.live public URL (72h)")
    parser.add_argument("--port", type=int, default=7860)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()

    app = build_app()
    app.launch(
        server_name=args.host,
        server_port=args.port,
        share=args.share,
    )
