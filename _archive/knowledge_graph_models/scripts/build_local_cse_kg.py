"""
Build a seed local CSE-KG from the project's existing assets.

Sources stitched together:
  - src/models/dina.py                                   -> 20 Java CS1 skills
  - data/mental_models/wrong_models_catalogue.json       -> 60 wrong models +
                                                            conversation signals
  - data/pedagogical_kg/learning_progressions.json       -> prereq edges
  - data/pedagogical_kg/misconceptions.json              -> misconception nodes

Outputs to data/cse_kg_local/:
  graph.pkl          -> nx.DiGraph(skill, misconception, wrong_model nodes)
  concepts.json      -> {concept_id: {label, week, error_class, description,
                          wrong_models: [...], misconceptions: [...]}}
  keyword_index.json -> {keyword: [concept_ids that mention it]}

This gives LocalCSEKGClient real data to query (prerequisites, related
concepts, common misconceptions, subgraph) instead of falling back to an
empty graph.
"""
import json, pickle
from pathlib import Path
from collections import defaultdict

import networkx as nx


ROOT = Path(__file__).parent.parent
OUT_DIR = ROOT / "data" / "cse_kg_local"


# Mirror src/models/dina.py JAVA_SKILLS so we don't import torch
JAVA_SKILLS = [
    "type_mismatch", "infinite_loop", "null_pointer", "string_equality",
    "variable_scope", "scanner_buffer", "integer_division", "array_index",
    "off_by_one", "operator_precedence", "boolean_logic", "string_immutability",
    "array_initialization", "for_loop_init", "method_returns",
    "static_vs_instance", "casting", "compound_assignment", "switch_fallthrough",
    "increment_semantics",
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def main():
    print(f"[build] writing local CSE-KG to {OUT_DIR}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    catalogue = load_json(ROOT / "data" / "mental_models" / "wrong_models_catalogue.json")
    progressions = load_json(ROOT / "data" / "pedagogical_kg" / "learning_progressions.json")
    misconceptions = load_json(ROOT / "data" / "pedagogical_kg" / "misconceptions.json")

    g = nx.DiGraph()
    concepts_meta = {}
    keyword_index = defaultdict(set)

    # 1) Skill nodes from JAVA_SKILLS (and catalogue if richer)
    cat_concepts = (catalogue or {}).get("concepts", {})
    for skill in JAVA_SKILLS:
        entry = cat_concepts.get(skill, {})
        g.add_node(skill, kind="concept", label=skill,
                   week=entry.get("week"),
                   error_class=entry.get("error_class"),
                   description=entry.get("java_concept", ""))
        concepts_meta[skill] = {
            "label": skill,
            "week": entry.get("week"),
            "error_class": entry.get("error_class"),
            "description": entry.get("java_concept", ""),
            "wrong_models": [],
            "misconceptions": [],
            "lp_rubric": entry.get("lp_rubric", {}),
        }

    # 2) Wrong-model nodes + concept -> wm edges + signal -> concept keywords
    for skill, entry in cat_concepts.items():
        if skill not in concepts_meta:
            # extra concepts beyond JAVA_SKILLS
            g.add_node(skill, kind="concept", label=skill,
                       description=entry.get("java_concept", ""))
            concepts_meta[skill] = {
                "label": skill,
                "week": entry.get("week"),
                "error_class": entry.get("error_class"),
                "description": entry.get("java_concept", ""),
                "wrong_models": [], "misconceptions": [],
                "lp_rubric": entry.get("lp_rubric", {}),
            }
        for wm in entry.get("wrong_models", []):
            wm_id = wm["id"]
            g.add_node(wm_id, kind="wrong_model", label=wm_id,
                       wrong_belief=wm.get("wrong_belief", ""),
                       origin=wm.get("origin", ""))
            g.add_edge(skill, wm_id, kind="has_wrong_model")
            concepts_meta[skill]["wrong_models"].append({
                "id": wm_id,
                "wrong_belief": wm.get("wrong_belief", ""),
                "origin": wm.get("origin", ""),
            })
            for sig in wm.get("conversation_signals", []):
                for token in sig.lower().replace("'", "").split():
                    if len(token) > 3:
                        keyword_index[token].add(skill)

    # 3) Misconception nodes from data/pedagogical_kg/misconceptions.json
    if isinstance(misconceptions, list):
        for mc in misconceptions:
            mc_id = mc.get("id") or mc.get("name")
            if not mc_id: continue
            related_concept = mc.get("concept", "")
            g.add_node(mc_id, kind="misconception", label=mc_id,
                       description=mc.get("description", ""),
                       severity=mc.get("severity", ""))
            if related_concept:
                if related_concept not in g:
                    g.add_node(related_concept, kind="concept",
                               label=related_concept)
                g.add_edge(related_concept, mc_id, kind="has_misconception")
                if related_concept in concepts_meta:
                    concepts_meta[related_concept]["misconceptions"].append({
                        "id": mc_id,
                        "description": mc.get("description", ""),
                    })

    # 4) Prerequisite edges from learning_progressions.json
    progs = progressions or []
    if isinstance(progs, dict):
        progs = list(progs.values())
    for prog in progs:
        prereqs_map = prog.get("prerequisite_relations") or prog.get("prerequisites") or {}
        # Some progression files store prereqs at the step level
        for step in prog.get("steps", []):
            step_concept = step.get("concept")
            if not step_concept: continue
            if step_concept not in g:
                g.add_node(step_concept, kind="concept", label=step_concept)
            for pre in step.get("prerequisites", []):
                if pre not in g:
                    g.add_node(pre, kind="concept", label=pre)
                # prereq points at the dependent
                g.add_edge(pre, step_concept, kind="prerequisite_of")
        for src, tgts in (prereqs_map.items() if isinstance(prereqs_map, dict) else []):
            if src not in g: g.add_node(src, kind="concept", label=src)
            for t in (tgts if isinstance(tgts, list) else [tgts]):
                if t not in g: g.add_node(t, kind="concept", label=t)
                g.add_edge(src, t, kind="prerequisite_of")

    # 5) Add concept-name keywords too
    for c in concepts_meta:
        for token in c.replace("_", " ").split():
            if len(token) > 3:
                keyword_index[token.lower()].add(c)

    # Persist
    with open(OUT_DIR / "graph.pkl", "wb") as f:
        pickle.dump(g, f)
    (OUT_DIR / "concepts.json").write_text(
        json.dumps(concepts_meta, indent=2), encoding="utf-8")
    (OUT_DIR / "keyword_index.json").write_text(
        json.dumps({k: sorted(v) for k, v in keyword_index.items()},
                   indent=2), encoding="utf-8")

    # Stats
    n_concept = sum(1 for n, d in g.nodes(data=True) if d.get("kind") == "concept")
    n_wm      = sum(1 for n, d in g.nodes(data=True) if d.get("kind") == "wrong_model")
    n_mc      = sum(1 for n, d in g.nodes(data=True) if d.get("kind") == "misconception")
    print(f"[build] nodes : {len(g.nodes())} "
          f"({n_concept} concepts, {n_wm} wrong_models, {n_mc} misconceptions)")
    print(f"[build] edges : {len(g.edges())}")
    print(f"[build] keyword index entries: {len(keyword_index)}")
    print(f"[build] files :")
    for f in sorted(OUT_DIR.iterdir()):
        print(f"   - {f.name}  ({f.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
