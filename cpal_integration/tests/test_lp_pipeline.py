"""Standalone smoke test for the on-disk LP pipeline.

Loads mental_models.py and lp_diagnostic.py directly, bypassing the
src.knowledge_graph package __init__ which pulls in SPARQLWrapper and
other heavy deps that aren't installed in this sandbox.
"""
import sys
import importlib.util
import types
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))


def _load(mod_name: str, file_path: str):
    spec = importlib.util.spec_from_file_location(mod_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[mod_name] = mod
    spec.loader.exec_module(mod)
    return mod


# Stub the package __init__ files so relative imports inside the real
# modules don't drag in unrelated deps.
for pkg in ("src", "src.knowledge_graph", "src.orchestrator"):
    if pkg not in sys.modules:
        sys.modules[pkg] = types.ModuleType(pkg)

mm = _load("src.knowledge_graph.mental_models",
           "src/knowledge_graph/mental_models.py")
ld = _load("src.orchestrator.lp_diagnostic",
           "src/orchestrator/lp_diagnostic.py")


def main():
    d = ld.get_diagnostician()

    cases = [
        ("L1 (pure symptom)", "null_pointer",
         "it's not working, I get an error",
         None, 0),
        ("L2 (rule named, no mechanism)", "string_equality",
         "I need to use .equals() instead of == for strings",
         None, 0),
        ("L3 (mechanism trace)", "null_pointer",
         "declaring String s creates a reference slot holding null. "
         "new allocates a heap object and returns its address. Method "
         "call dereferences the reference - if null, NPE.",
         None, 0),
        ("L4 (transfer)", "null_pointer",
         "This applies to all reference types in Java. The same "
         "principle - dereferencing a null address - explains why "
         "Java chose to require explicit null checks.",
         None, 0),
        ("L2 plateau (streak=2)", "string_equality",
         "I use .equals() for strings",
         "L2", 2),
        ("L2 streak=1 (not yet plateau)", "string_equality",
         "I use .equals() for strings",
         "L2", 1),
        ("Wrong-model match", "null_pointer",
         "I declared it so why is it null, I created s right there at the top",
         None, 0),
    ]

    header = f"\n{'tag':<34}{'level':<6}{'step':<7}{'detail':<8}" \
             f"{'streak':<8}{'plateau':<9}{'wm':<6}{'score':<7}"
    print(header)
    print("-" * 85)
    for tag, concept, text, stored_lvl, stored_streak in cases:
        r = d.diagnose(
            student_id="test",
            concept=concept,
            question_text=text,
            stored_lp_level=stored_lvl,
            stored_lp_streak=stored_streak,
        )
        plateau = "Y" if r.plateau_flag else "-"
        wm = r.wrong_model_id or "-"
        print(f"{tag:<34}{r.current_lp_level:<6}"
              f"{str(r.logical_step):<7}"
              f"{str(r.logical_step_detail):<8}"
              f"{r.lp_streak:<8}"
              f"{plateau:<9}"
              f"{wm:<6}"
              f"{r.match_score:<7.2f}")

    # --- Stage 2 LP-validity gate ---
    print("\n--- LP-validity gate (filter_interventions_by_lp) ---")
    ranked = [("transfer_task", 0.9), ("worked_example", 0.8),
              ("socratic_prompt", 0.7), ("trace_scaffold", 0.65)]
    for lvl in ("L1", "L2", "L3", "L4"):
        filt = ld.filter_interventions_by_lp(ranked, lvl)
        print(f"  {lvl}: {filt}")

    # --- Stage 4 post-reply classifier ---
    print("\n--- Stage 4 post-reply classification ---")
    replies = [
        ("confused", "I still don't get it"),
        ("rule", "so I should use .equals()"),
        ("mechanism", "the new operator allocates on the heap and returns the address"),
        ("transfer", "so this applies to all reference types — same principle"),
    ]
    for tag, text in replies:
        ls, lsd, lvl = ld.classify_post_reply(text)
        print(f"  {tag:<12}  level={lvl}  step={ls}  detail={lsd}")


if __name__ == "__main__":
    main()
