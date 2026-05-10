"""
Run demo_full_stack.run() over 10 distinct CS1 scenarios + write an
aggregate summary so the wrong-belief, LP transition, RAG behaviour, and
response can be compared across scenarios.

Output:
  output/batch_run_<timestamp>/
    summary.json   - structured per-scenario row (lp, wm, rag, mastery, etc.)
    summary.md     - human-readable table
    responses/<id>.md  - each LLM response

Plus the per-scenario folders that demo_full_stack auto-creates under
output/full_stack_run_<timestamp>_<id>/.
"""
import sys, os, json, time, re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

import demo_full_stack as dfs


# Each scenario writes a paraphrase of the targeted wrong-model's
# conversation_signals so the WM head + RAG layer have something concrete
# to match against. expected_wm is for verification only.
SCENARIOS = [
    {
        "id": "01_null_pointer_NP-A",
        "concept": "null_pointer",
        "expected_wm": "NP-A",
        "message": (
            "I created a Room object but calling describe() on it crashes "
            "with NullPointerException. I declared the field right at the "
            "top of the class so it should exist already. What am I missing?"
        ),
        "code": (
            "public class Game {\n"
            "    Room currentRoom;\n"
            "    public void start() { currentRoom.describe(); }\n"
            "}"
        ),
        "prior_mastery": {"null_pointer": 0.25, "type_mismatch": 0.70,
                          "infinite_loop": 0.65},
    },
    {
        "id": "02_type_mismatch_TM-B",
        "concept": "type_mismatch",
        "expected_wm": "TM-B",
        "message": (
            "I thought + would just combine an int and a string into one "
            "string the way Python does. Why won't Java do this "
            "automatically? It worked fine when I tested it in Python."
        ),
        "code": (
            "int score = 100;\n"
            "String msg = \"Score: \" + score + 5;\n"
            "// expected \"Score: 105\" but got \"Score: 1005\""
        ),
        "prior_mastery": {"type_mismatch": 0.20, "string_immutability": 0.50,
                          "null_pointer": 0.55},
    },
    {
        "id": "03_infinite_loop_IL-B",
        "concept": "infinite_loop",
        "expected_wm": "IL-B",
        "message": (
            "My while loop keeps running forever. I use i in the condition "
            "so I thought i would automatically increase each iteration. "
            "Doesn't i update on its own when it's used in the loop?"
        ),
        "code": (
            "int i = 0;\n"
            "while (i < 10) {\n"
            "    System.out.println(i);\n"
            "    // I thought i would increase here automatically\n"
            "}"
        ),
        "prior_mastery": {"infinite_loop": 0.15, "type_mismatch": 0.60,
                          "null_pointer": 0.55},
    },
    {
        "id": "04_integer_division_ID-A",
        "concept": "integer_division",
        "expected_wm": "ID-A",
        "message": (
            "I divided 5 by 2 in Java and got 2, not 2.5. That's not the "
            "right answer mathematically. Java rounded it down for no "
            "reason — five divided by two is two and a half!"
        ),
        "code": (
            "double half = 5 / 2;\n"
            "System.out.println(half);   // expected 2.5, got 2.0"
        ),
        "prior_mastery": {"integer_division": 0.20, "type_mismatch": 0.50,
                          "null_pointer": 0.55},
    },
    {
        "id": "05_array_index_AI-A",
        "concept": "array_index",
        "expected_wm": "AI-A",
        "message": (
            "I have an array with 5 numbers: 10, 20, 30, 40, 50. When I "
            "try arr[5] to get the fifth element I get "
            "ArrayIndexOutOfBoundsException. The fifth slot holds 50, why "
            "isn't arr[5] giving me 50?"
        ),
        "code": (
            "int[] arr = {10, 20, 30, 40, 50};\n"
            "int fifth = arr[5];   // crashes"
        ),
        "prior_mastery": {"array_index": 0.30, "type_mismatch": 0.55,
                          "null_pointer": 0.55},
    },
    {
        "id": "06_string_equality_SE-A",
        "concept": "string_equality",
        "expected_wm": "SE-A",
        "message": (
            "I have two strings that both say \"hello\" and I'm comparing "
            "them with ==. The check returns false but they're clearly "
            "the same text. Java should compare the content, right? "
            "Otherwise how would you ever check if two strings match?"
        ),
        "code": (
            "String a = new String(\"hello\");\n"
            "String b = new String(\"hello\");\n"
            "if (a == b) System.out.println(\"same\");   // never prints"
        ),
        "prior_mastery": {"string_equality": 0.20, "string_immutability": 0.50,
                          "null_pointer": 0.55},
    },
    {
        "id": "07_variable_scope_VS-A",
        "concept": "variable_scope",
        "expected_wm": "VS-A",
        "message": (
            "I declared total inside the if block but now I can't use it "
            "outside. The compiler says \"cannot find symbol\". The braces "
            "are just for organisation, right? I already declared the "
            "variable, why does Java forget it?"
        ),
        "code": (
            "if (x > 0) {\n"
            "    int total = x * 2;\n"
            "}\n"
            "System.out.println(total);  // compile error"
        ),
        "prior_mastery": {"variable_scope": 0.20, "type_mismatch": 0.55,
                          "null_pointer": 0.55},
    },
    {
        "id": "08_assignment_vs_compare_AC-A",
        "concept": "assignment_vs_compare",
        "expected_wm": "AC-A",
        "message": (
            "My if-statement always enters the true branch even when x "
            "isn't 5. I wrote if (x = 5) and it seems to just set x to 5 "
            "and then the if is always true. Why does Java behave this way?"
        ),
        "code": (
            "int x = 10;\n"
            "if (x = 5) {\n"
            "    System.out.println(\"x is 5\");   // always prints\n"
            "}"
        ),
        "prior_mastery": {"assignment_vs_compare": 0.15, "boolean_operators": 0.50,
                          "null_pointer": 0.55},
    },
    {
        "id": "09_scanner_buffer_SB-A",
        "concept": "scanner_buffer",
        "expected_wm": "SB-A",
        "message": (
            "I called nextLine() right after nextInt() and now my string "
            "is empty. The Scanner is skipping my input completely. Each "
            "method should read its own line of input, right?"
        ),
        "code": (
            "Scanner sc = new Scanner(System.in);\n"
            "int age = sc.nextInt();\n"
            "String name = sc.nextLine();    // always empty\n"
            "System.out.println(\"Hello \" + name);"
        ),
        "prior_mastery": {"scanner_buffer": 0.20, "type_mismatch": 0.55,
                          "null_pointer": 0.55},
    },
    {
        "id": "10_null_pointer_NP-B",
        "concept": "null_pointer",
        "expected_wm": "NP-B",
        "message": (
            "I have a Widget with a label field. When I call describe() "
            "before setting label, it crashes. Can't null just mean "
            "\"nothing\" and return an empty string? Why does calling a "
            "method on null have to blow up?"
        ),
        "code": (
            "public class Widget {\n"
            "    String label;\n"
            "    public String describe() { return label.toUpperCase(); }\n"
            "}\n"
            "// Widget w = new Widget(); w.describe();  // NullPointerException"
        ),
        "prior_mastery": {"null_pointer": 0.30, "string_immutability": 0.50,
                          "infinite_loop": 0.60},
    },
]


def run_scenario(s):
    """Patch demo_full_stack module globals + invoke run(). Returns the
    artifacts dict. Per-scenario output folder is created by demo_full_stack
    main(); we don't call main() here so we skip that and capture directly."""
    dfs.STUDENT_MESSAGE = s["message"]
    dfs.STUDENT_CODE    = s["code"]
    dfs.TARGET_CONCEPT  = s["concept"]
    dfs.PRIOR_MASTERY   = s["prior_mastery"]

    # Reset module-level state that might cache between runs (e.g. CSO
    # ontology/LP index could be cached, but they're singletons internally)
    t0 = time.time()
    artifacts = dfs.run()
    artifacts["_scenario_id"]    = s["id"]
    artifacts["_expected_wm"]    = s["expected_wm"]
    artifacts["_elapsed_s"]      = time.time() - t0
    return artifacts


def main():
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    out_dir = ROOT / "output" / f"batch_run_{stamp}"
    (out_dir / "responses").mkdir(parents=True, exist_ok=True)
    print(f"[batch] writing to: {out_dir}")
    print(f"[batch] running {len(SCENARIOS)} scenarios sequentially "
          f"(~60s/scenario, total ~10-12 min)")

    rows = []
    for i, s in enumerate(SCENARIOS, 1):
        print("\n" + "=" * 80)
        print(f"[batch] scenario {i}/{len(SCENARIOS)}: {s['id']}")
        print(f"[batch] concept={s['concept']}  expected_wm={s['expected_wm']}")
        print("=" * 80)
        try:
            art = run_scenario(s)
        except Exception as e:
            print(f"[batch] FAILED: {e}")
            rows.append({"id": s["id"], "concept": s["concept"],
                         "expected_wm": s["expected_wm"],
                         "error": str(e)[:200]})
            continue

        lp = art.get("lp_diagnostic", {}) or {}
        kg = art.get("knowledge_graph", {}) or {}
        rag = kg.get("catalogue_rag", {}) or {}
        skg = kg.get("student_knowledge_graph", {}) or {}
        bkt = art.get("bkt", {}) or {}
        dina = art.get("dina", {}) or {}

        row = {
            "id":              s["id"],
            "concept":         s["concept"],
            "expected_wm":     s["expected_wm"],
            "lp_current":      lp.get("current_lp_level"),
            "lp_target":       lp.get("target_lp_level"),
            "lp_transition":   lp.get("transition"),
            "wm_classifier":   lp.get("wrong_model_id"),
            "wm_classifier_score": lp.get("match_score"),
            "wm_rag_top":      rag.get("hybrid_top"),
            "wm_rag_flipped":  rag.get("flipped"),
            "wm_rag_alpha":    rag.get("alpha"),
            "wm_correct":      lp.get("wrong_model_id") == s["expected_wm"],
            "wm_rag_correct":  rag.get("hybrid_top") == s["expected_wm"],
            "bkt_before":      bkt.get("before"),
            "bkt_after":       bkt.get("after_failure"),
            "dina_before":     dina.get("before"),
            "dina_after":      dina.get("after_failure"),
            "skg_nodes":       len(skg.get("subgraph_nodes", [])),
            "skg_edges":       len(skg.get("subgraph_edges", [])),
            "ollama_ttft_s":   (art.get("ollama") or {}).get("ttft_s"),
            "ollama_total_s":  (art.get("ollama") or {}).get("total_s"),
            "response_chars":  (art.get("ollama") or {}).get("response_chars"),
            "elapsed_s":       art.get("_elapsed_s"),
        }
        rows.append(row)

        # Save the LLM response
        (out_dir / "responses" / f"{s['id']}.md").write_text(
            f"# {s['id']} — {s['concept']} (expected {s['expected_wm']})\n\n"
            f"## Student message\n{s['message']}\n\n"
            f"## Student code\n```java\n{s['code']}\n```\n\n"
            f"## Diagnosis\n"
            f"- LP: {row['lp_current']} -> {row['lp_target']}\n"
            f"- Classifier WM: {row['wm_classifier']} "
            f"(score={row['wm_classifier_score']})\n"
            f"- RAG hybrid WM: {row['wm_rag_top']}  "
            f"(flipped={row['wm_rag_flipped']})\n"
            f"- BKT mastery: {row['bkt_before']:.2f} -> {row['bkt_after']:.2f}\n"
            f"- DINA mastery: {row['dina_before']:.2f} -> {row['dina_after']:.2f}\n\n"
            f"## LLM response\n\n{art.get('ollama_response', '')}",
            encoding="utf-8",
        )

    # ── Aggregate output ────────────────────────────────────────────────────
    (out_dir / "summary.json").write_text(
        json.dumps(rows, indent=2, default=str), encoding="utf-8")

    # Markdown table
    md = ["# Full-stack batch run summary",
          f"\nRan {len(SCENARIOS)} scenarios at {stamp}.\n",
          "## Wrong-belief identification (classifier vs RAG hybrid)",
          ""]
    md.append("| # | id | expected | classifier | hybrid (RAG) | flipped | "
              "cls✓ | rag✓ |")
    md.append("|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        md.append(f"| {i} | `{r.get('id','')}` | "
                  f"**{r.get('expected_wm','')}** | "
                  f"{r.get('wm_classifier') or '—'} | "
                  f"{r.get('wm_rag_top') or '—'} | "
                  f"{'⟲' if r.get('wm_rag_flipped') else ''} | "
                  f"{'✓' if r.get('wm_correct') else '✗'} | "
                  f"{'✓' if r.get('wm_rag_correct') else '✗'} |")

    md.extend(["", "## Learning-progression transitions", ""])
    md.append("| id | concept | LP current | LP target | transition |")
    md.append("|---|---|---|---|---|")
    for r in rows:
        md.append(f"| `{r.get('id','')}` | {r.get('concept','')} | "
                  f"{r.get('lp_current') or '—'} | "
                  f"{r.get('lp_target') or '—'} | "
                  f"{r.get('lp_transition') or '—'} |")

    md.extend(["", "## Mastery updates (BKT + DINA, after failure)", ""])
    md.append("| id | concept | BKT before | BKT after | DINA before | "
              "DINA after |")
    md.append("|---|---|---|---|---|---|")
    for r in rows:
        def f(x): return f"{x:.2f}" if isinstance(x, (int, float)) else "—"
        md.append(f"| `{r.get('id','')}` | {r.get('concept','')} | "
                  f"{f(r.get('bkt_before'))} | {f(r.get('bkt_after'))} | "
                  f"{f(r.get('dina_before'))} | {f(r.get('dina_after'))} |")

    md.extend(["", "## Student knowledge graphs + Ollama timing", ""])
    md.append("| id | SKG nodes | SKG edges | TTFT (s) | Total (s) | "
              "Response chars |")
    md.append("|---|---|---|---|---|---|")
    for r in rows:
        def f(x, fmt="{}"): return fmt.format(x) if x is not None else "—"
        md.append(f"| `{r.get('id','')}` | {f(r.get('skg_nodes'))} | "
                  f"{f(r.get('skg_edges'))} | "
                  f"{f(r.get('ollama_ttft_s'), '{:.1f}')} | "
                  f"{f(r.get('ollama_total_s'), '{:.1f}')} | "
                  f"{f(r.get('response_chars'))} |")

    # Aggregate accuracy
    n = len([r for r in rows if "error" not in r])
    cls_correct = sum(1 for r in rows if r.get("wm_correct"))
    rag_correct = sum(1 for r in rows if r.get("wm_rag_correct"))
    rag_flipped = sum(1 for r in rows if r.get("wm_rag_flipped"))
    md.extend(["", "## Headline metrics", "",
               f"- Scenarios completed: {n}/{len(SCENARIOS)}",
               f"- Classifier wrong-model accuracy: {cls_correct}/{n} "
               f"({100*cls_correct/max(n,1):.0f}%)",
               f"- RAG hybrid wrong-model accuracy: {rag_correct}/{n} "
               f"({100*rag_correct/max(n,1):.0f}%)",
               f"- Times RAG flipped the classifier: {rag_flipped}",
               ""])

    (out_dir / "summary.md").write_text("\n".join(md), encoding="utf-8")

    print("\n" + "=" * 80)
    print(f"[batch] DONE. {n}/{len(SCENARIOS)} scenarios completed.")
    print(f"[batch] Classifier accuracy: {cls_correct}/{n}, "
          f"RAG accuracy: {rag_correct}/{n}, RAG flipped: {rag_flipped}")
    print(f"[batch] Output in {out_dir}")
    for f in sorted(out_dir.iterdir()):
        if f.is_dir():
            n_files = len(list(f.iterdir()))
            print(f"   - {f.name}/  ({n_files} files)")
        else:
            print(f"   - {f.name}  ({f.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
