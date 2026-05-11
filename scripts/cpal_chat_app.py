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
import os, sys, argparse
from pathlib import Path
from threading import Lock
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


def stream_response(quiz_id, picked_option_full, reasoning, history):
    if not quiz_id:
        yield history, gr.update(value="⚠️ Select a quiz first.", visible=True)
        return
    q = QUIZ_BY_ID.get(quiz_id)
    if q is None:
        yield history, gr.update(value="⚠️ Unknown quiz.", visible=True)
        return
    if not picked_option_full:
        yield history, gr.update(value="⚠️ Pick an option (A/B/C/D) before submitting.", visible=True)
        return
    if not reasoning.strip():
        yield history, gr.update(value="⚠️ Write your reasoning for this pick, then submit.", visible=True)
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

    # Append user bubble + assistant placeholder. The assistant bubble is
    # pre-filled with a typing indicator so it never shows up as an empty
    # white block while the LLM is warming up.
    thinking_placeholder = (
        '<span style="color:#64748b; font-style:italic;">'
        'Tutor is thinking…</span>'
    )
    history = list(history) + [
        {"role": "user", "content": _render_user_bubble(q, picked_text, reasoning)},
        {"role": "assistant", "content": thinking_placeholder},
    ]

    # First yield: show correct/wrong status + chat bubbles instantly.
    yield history, gr.update(value=status_template, visible=True)

    # Now do the heavier work: diagnosis (drives the generator).
    diag = _diagnose(reasoning, q["concept"], q["code"],
                     q["question"], picked_option_full)

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

    # Build the message the generator sees
    tutor_input = (
        f"Student was given this quiz:\n"
        f"Q: {q['question']}\n\n"
        f"Code:\n```java\n{q['code']}\n```\n\n"
        f"Options:\n" + "\n".join(f"  {k}. {v}" for k, v in q["options"].items()) +
        f"\n\nStudent picked {picked_letter}: {picked_text}\n"
        f"Correct answer is {q['correct_answer']}: "
        f"{q['options'][q['correct_answer']]}\n"
        f"Student was {'CORRECT' if correct else 'INCORRECT'}.\n\n"
        f"Student's reasoning: {reasoning}"
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

    last_len = 0
    while not done["flag"]:
        time.sleep(0.15)
        if len(buffer["text"]) > last_len:
            last_len = len(buffer["text"])
            history[-1]["content"] = buffer["text"]
            yield history, gr.update(value=status_template + "  ·  *tutor is typing…*", visible=True)

    if done["err"]:
        history[-1]["content"] = f"❌ Generation failed: {done['err']}"
    else:
        history[-1]["content"] = buffer["text"] or "(empty response)"

    yield history, gr.update(value=status_template, visible=True)


def clear_chat():
    return ([], gr.update(value="", visible=False))


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
        chatbot = gr.Chatbot(
            label="Your tutor",
            type="messages",
            height=560,
            show_copy_button=True,
            avatar_images=(None, None),
        )

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

        # Submit — this is the long one; the white "Generating…" overlay was
        # Gradio's default progress widget. Hide it.
        submit_btn.click(
            stream_response,
            inputs=[quiz_dd, option_radio, reasoning_box, chatbot],
            outputs=[chatbot, status],
            show_progress="hidden",
        )

        clear_btn.click(clear_chat, None, [chatbot, status],
                        show_progress="hidden")

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
