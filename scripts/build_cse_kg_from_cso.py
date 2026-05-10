"""
Build local CSE-KG from CSO (Computer Science Ontology, Salatino et al.) +
the project's pedagogical layer.

Sources:
  - data/cse_kg_external/cso_v3.5.csv     (14,637 concepts, 103,672 edges)
                                          Salatino, A. et al. "The Computer
                                          Science Ontology" — released 2018-,
                                          version 3.5 (Cybersecurity update).
                                          CC-BY 4.0. Downloaded from
                                          https://cso.kmi.open.ac.uk/
                                          download/version-3.5/cso_v3.5.csv
                                          and CSO.3.5.nt.zip.
  - data/mental_models/wrong_models_catalogue.json   60 Java CS1 wrong models
  - data/pedagogical_kg/misconceptions.json          21 misconception nodes
  - data/pedagogical_kg/learning_progressions.json   prereq edges

Output (overwrites data/cse_kg_local/):
  graph.pkl          nx.DiGraph with kinds: cso_concept, concept,
                     wrong_model, misconception
  concepts.json      per-concept metadata for the Java teaching layer
  keyword_index.json keyword -> [concept ids]  (built from CSO labels +
                     wrong-model conversation signals)

Used by src/knowledge_graph/local_cse_kg_client.py — the demo automatically
picks this up the next time LocalCSEKGClient is constructed.

Note: CSO uses URI-free string IDs (e.g. "computer science"). We prefix
those with "cso:" in the graph to disambiguate from Java-skill ids
("cso:computer science" vs "null_pointer").
"""
import csv, json, pickle
from pathlib import Path
from collections import defaultdict

import networkx as nx


ROOT = Path(__file__).parent.parent
EXT_DIR = ROOT / "data" / "cse_kg_external"
OUT_DIR = ROOT / "data" / "cse_kg_local"

CSO_CSV = EXT_DIR / "cso_v3.5.csv"
CSO_NT  = EXT_DIR / "CSO.3.5.nt"
WIKIDATA_JSON = EXT_DIR / "wikidata_cs_concepts.json"

# Java teaching layer (mirrors src/models/dina.py canonical list)
JAVA_SKILLS = [
    "type_mismatch", "infinite_loop", "null_pointer", "string_equality",
    "variable_scope", "assignment_vs_compare", "integer_division",
    "scanner_buffer", "array_index", "missing_return", "array_not_allocated",
    "boolean_operators", "sentinel_loop", "unreachable_code",
    "string_immutability", "no_default_constructor", "static_vs_instance",
    "foreach_no_modify", "overloading", "generics_primitives",
]

# CSO concepts the Java teaching layer maps onto. Used to anchor the seed
# graph into CSO so prerequisites/related lookups can traverse the larger
# ontology. Manually curated -- imperfect, but better than nothing.
JAVA_TO_CSO = {
    "type_mismatch":           "type system",
    "infinite_loop":           "infinite loop",
    "null_pointer":            "null pointer",
    "string_equality":         "string matching",
    "variable_scope":          "scope",
    "assignment_vs_compare":   "comparison operators",
    "integer_division":        "integer division",
    "scanner_buffer":          "input/output",
    "array_index":             "arrays",
    "missing_return":          "return statement",
    "array_not_allocated":     "memory allocation",
    "boolean_operators":       "boolean algebra",
    "sentinel_loop":           "loop",
    "unreachable_code":        "static analysis",
    "string_immutability":     "immutable objects",
    "no_default_constructor":  "constructor",
    "static_vs_instance":      "object-oriented programming",
    "foreach_no_modify":       "iteration",
    "overloading":             "polymorphism",
    "generics_primitives":     "generics",
}


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def cso_id(label):
    """Normalised CSO node id used inside the graph."""
    return f"cso:{label.strip().lower()}"


def parse_cso_csv(g, label_to_id):
    """Read cso_v3.5.csv -> add CSO nodes + edges to the graph."""
    if not CSO_CSV.exists():
        print(f"[!] {CSO_CSV} not found; skipping CSO ingest")
        return 0, 0

    edge_kind_map = {
        "klink:broadergeneric":     "broader_than",
        "klink:contributesto":      "contributes_to",
        "klink:relatedequivalent":  "same_as",
    }

    n_nodes_before = len(g.nodes())
    n_edges = 0

    with open(CSO_CSV, "r", encoding="utf-8") as f:
        rd = csv.reader(f, delimiter=";", quotechar='"')
        for row in rd:
            if len(row) != 3: continue
            s_label, p, o_label = row[0].strip(), row[1].strip().lower(), row[2].strip()
            if not s_label or not o_label: continue

            sid, oid = cso_id(s_label), cso_id(o_label)
            label_to_id[s_label.lower()] = sid
            label_to_id[o_label.lower()] = oid

            if p == "rdfs:label":
                # primary label of subject
                if sid in g:
                    g.nodes[sid]["label"] = o_label
                else:
                    g.add_node(sid, kind="cso_concept", label=o_label)
                continue
            if p == "rdf:type":
                continue  # all CSO topics are skos:Concept; not interesting here
            if p == "klink:primarylabel":
                if sid in g:
                    g.nodes[sid]["primary_label"] = o_label
                continue

            if sid not in g:
                g.add_node(sid, kind="cso_concept", label=s_label)
            if oid not in g:
                g.add_node(oid, kind="cso_concept", label=o_label)

            kind = edge_kind_map.get(p)
            if kind:
                g.add_edge(sid, oid, kind=kind, source="CSO_v3.5")
                n_edges += 1

    return len(g.nodes()) - n_nodes_before, n_edges


def parse_wikidata_json(g, label_to_id):
    """Ingest Wikidata CS concepts as wikidata:Q<id> nodes."""
    if not WIKIDATA_JSON.exists():
        return 0, 0
    data = json.loads(WIKIDATA_JSON.read_text(encoding="utf-8"))
    n_before = len(g.nodes())
    n_edges = 0
    for c in data.get("concepts", []):
        node_id = f"wikidata:{c['qid']}"
        g.add_node(node_id, kind="wikidata_concept",
                   label=c.get("label", c["qid"]),
                   description=c.get("description", ""))
        label_to_id[c.get("label", "").lower()] = node_id
        for nbr in c.get("neighbors", []):
            n_id = f"wikidata:{nbr['qid']}"
            if n_id not in g:
                g.add_node(n_id, kind="wikidata_concept",
                           label=nbr.get("label", nbr["qid"]))
            g.add_edge(node_id, n_id, kind=nbr["relation"],
                       source="Wikidata")
            n_edges += 1
    # Anchor JAVA skills to Wikidata via the saved java_to_wikidata mapping
    for skill, qid in (data.get("java_to_wikidata", {}) or {}).items():
        if qid and skill in g and f"wikidata:{qid}" in g:
            g.add_edge(skill, f"wikidata:{qid}", kind="wikidata_aligned",
                       source="manual_alignment")
            n_edges += 1
    return len(g.nodes()) - n_before, n_edges


def add_pedagogical_layer(g, label_to_id, concepts_meta, keyword_index):
    """Layer Java teaching nodes (concepts, wrong_models, misconceptions)
    on top of CSO, plus prereq edges from learning_progressions.json."""
    catalogue = load_json(ROOT / "data" / "mental_models" / "wrong_models_catalogue.json")
    misconceptions = load_json(ROOT / "data" / "pedagogical_kg" / "misconceptions.json")
    progressions = load_json(ROOT / "data" / "pedagogical_kg" / "learning_progressions.json")

    cat_concepts = (catalogue or {}).get("concepts", {})

    # 1) Java skill nodes + anchor edge to CSO
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
        # Anchor into CSO
        cso_label = JAVA_TO_CSO.get(skill, "").lower()
        if cso_label and cso_id(cso_label) in g:
            g.add_edge(skill, cso_id(cso_label), kind="cso_aligned",
                       source="manual_alignment")

    # 2) Wrong-model nodes + signal -> concept keywords
    for skill, entry in cat_concepts.items():
        if skill not in concepts_meta:
            g.add_node(skill, kind="concept", label=skill,
                       description=entry.get("java_concept", ""))
            concepts_meta[skill] = {
                "label": skill, "week": entry.get("week"),
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
            g.add_edge(skill, wm_id, kind="has_wrong_model",
                       source="wrong_models_catalogue.json")
            concepts_meta[skill]["wrong_models"].append({
                "id": wm_id,
                "wrong_belief": wm.get("wrong_belief", ""),
                "origin": wm.get("origin", ""),
            })
            for sig in wm.get("conversation_signals", []):
                for token in sig.lower().replace("'", "").split():
                    if len(token) > 3:
                        keyword_index[token].add(skill)

    # 3) Misconception nodes
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
                g.add_edge(related_concept, mc_id, kind="has_misconception",
                           source="misconceptions.json")
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
        for step in prog.get("steps", []):
            step_concept = step.get("concept")
            if not step_concept: continue
            if step_concept not in g:
                g.add_node(step_concept, kind="concept", label=step_concept)
            for pre in step.get("prerequisites", []):
                if pre not in g:
                    g.add_node(pre, kind="concept", label=pre)
                g.add_edge(pre, step_concept, kind="prerequisite_of",
                           source="learning_progressions.json")

    # 5) CSO labels -> keyword index (every multi-word concept)
    for nid, attrs in g.nodes(data=True):
        if attrs.get("kind") != "cso_concept": continue
        label = attrs.get("label", "")
        for token in str(label).lower().split():
            if len(token) > 3:
                keyword_index[token].add(nid)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[build] writing combined CSE-KG to {OUT_DIR}")

    g = nx.DiGraph()
    label_to_id = {}
    concepts_meta = {}
    keyword_index = defaultdict(set)

    n_cso_nodes, n_cso_edges = parse_cso_csv(g, label_to_id)
    print(f"[build] CSO ingested: +{n_cso_nodes} nodes, +{n_cso_edges} edges")

    n_wd_nodes, n_wd_edges = parse_wikidata_json(g, label_to_id)
    print(f"[build] Wikidata ingested: +{n_wd_nodes} nodes, +{n_wd_edges} edges")

    add_pedagogical_layer(g, label_to_id, concepts_meta, keyword_index)

    # Now that JAVA skill nodes exist, anchor them to Wikidata + CSO
    if WIKIDATA_JSON.exists():
        wd_data = json.loads(WIKIDATA_JSON.read_text(encoding="utf-8"))
        n_anchor = 0
        for skill, qid in (wd_data.get("java_to_wikidata", {}) or {}).items():
            if qid and skill in g and f"wikidata:{qid}" in g:
                g.add_edge(skill, f"wikidata:{qid}",
                           kind="wikidata_aligned",
                           source="manual_alignment")
                n_anchor += 1
        print(f"[build] Wikidata alignment edges: +{n_anchor}")

    # Stats
    counts = defaultdict(int)
    for _, d in g.nodes(data=True): counts[d.get("kind", "?")] += 1
    edge_counts = defaultdict(int)
    for _, _, d in g.edges(data=True): edge_counts[d.get("kind", "?")] += 1

    print(f"[build] total nodes : {len(g.nodes())}")
    for k, n in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"          {k:<20} {n:>6}")
    print(f"[build] total edges : {len(g.edges())}")
    for k, n in sorted(edge_counts.items(), key=lambda x: -x[1]):
        print(f"          {k:<20} {n:>6}")
    print(f"[build] keyword index entries: {len(keyword_index)}")

    # Persist
    with open(OUT_DIR / "graph.pkl", "wb") as f:
        pickle.dump(g, f)
    (OUT_DIR / "concepts.json").write_text(
        json.dumps(concepts_meta, indent=2), encoding="utf-8")
    (OUT_DIR / "keyword_index.json").write_text(
        json.dumps({k: sorted(v) for k, v in keyword_index.items()},
                   indent=2), encoding="utf-8")

    print(f"[build] files :")
    for f in sorted(OUT_DIR.iterdir()):
        print(f"   - {f.name:<25} {f.stat().st_size:>10} bytes")


if __name__ == "__main__":
    main()
