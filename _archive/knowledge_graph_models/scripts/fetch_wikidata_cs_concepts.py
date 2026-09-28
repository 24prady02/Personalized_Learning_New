"""
Fetch CS1-relevant Wikidata concepts and their 1-hop neighbors.

Augments the CSO-based CSE-KG with Wikidata entries that CSO is missing
(e.g. null_pointer dereference, recursion, integer_division, off-by-one
errors). CSO is research-paper-topic granularity; Wikidata fills the
CS1-teaching granularity gap.

Source: Wikidata SPARQL endpoint
  https://query.wikidata.org/sparql
  CC0 licensed.

Output: data/cse_kg_external/wikidata_cs_concepts.json
  list of {qid, label, description, neighbors:[{qid, label, relation}]}
"""
import json, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
EXT_DIR = ROOT / "data" / "cse_kg_external"
UA = "PLS-Education-Research/1.0 (https://anthropic.com; magnus14chase@gmail.com)"
ENDPOINT = "https://query.wikidata.org/sparql"


# Mapping Java teaching skill -> Wikidata Q-ID. Verified against
# wbsearchentities; corrected after first-pass mapping found 7 wrong Q-IDs
# (e.g. Q1140510 was "Critica Botanica", not null pointer).
# NULL entries mean no satisfactory Wikidata match exists for that skill.
JAVA_TO_WIKIDATA = {
    "type_mismatch":           "Q865760",     # type system
    "infinite_loop":           "Q862372",     # infinite loop
    "null_pointer":            "Q19848926",   # null pointer  (FIXED)
    "string_equality":         None,
    "variable_scope":          None,          # no clean CS-specific Wikidata entry
    "assignment_vs_compare":   None,
    "integer_division":        None,          # no clean Wikidata entry
    "scanner_buffer":          None,
    "array_index":             "Q186152",     # array data structure
    "missing_return":          None,
    "array_not_allocated":     "Q2308807",    # memory management  (FIXED)
    "boolean_operators":       "Q942353",     # Boolean function   (FIXED)
    "sentinel_loop":           "Q838119",     # for loop
    "unreachable_code":        "Q2482534",    # unreachable code   (FIXED)
    "string_immutability":     "Q23828",      # immutable object
    "no_default_constructor":  "Q4231567",    # default constructor (FIXED -- now real)
    "static_vs_instance":      "Q1896011",    # static variable
    "foreach_no_modify":       "Q1326388",    # iterator
    "overloading":             "Q1091461",    # function overloading
    "generics_primitives":     "Q1051282",    # generic programming
}

# Companion CS1 concepts not directly mapped to JAVA_SKILLS but relevant
EXTRA_CONCEPTS = [
    "Q179976",   # recursion
    "Q1423448",  # integer overflow
    "Q1439356",  # off-by-one error
    "Q471748",   # exception handling
    "Q3240252",  # polymorphism
    "Q179550",   # software bug                 (FIXED)
    "Q868299",   # control flow                 (FIXED)
    "Q1305241",  # encapsulation
    "Q5261748",  # dereference operator
    "Q71826074", # sentinel value
    "Q1770035",  # dead code
    "Q1061927",  # dynamic memory allocation
    "Q848539",   # division by zero
]


REL_PROPS = {
    "P279": "subclass_of",
    "P31":  "instance_of",
    "P460": "same_as",
    "P1889":"different_from",
    "P527": "has_part",
    "P361": "part_of",
}


def get_entities(qids):
    """Fetch claims/labels via Wikidata's wbgetentities API (NOT SPARQL,
    so unaffected by the WDQS outage rate limit). Up to 50 ids per call."""
    url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({
        "action":  "wbgetentities",
        "ids":     "|".join(qids),
        "props":   "labels|descriptions|claims",
        "languages": "en",
        "format":  "json",
    })
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def label_lookup(qids):
    """Fetch labels for a batch of Q-IDs."""
    if not qids: return {}
    url = "https://www.wikidata.org/w/api.php?" + urllib.parse.urlencode({
        "action": "wbgetentities", "ids": "|".join(qids),
        "props": "labels", "languages": "en", "format": "json",
    })
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.loads(r.read())
    except Exception:
        return {q: q for q in qids}
    out = {}
    for q, e in d.get("entities", {}).items():
        out[q] = e.get("labels", {}).get("en", {}).get("value", q)
    return out


def fetch_concept_with_neighbors(qid):
    """Get label/description/neighbors for one Q-ID via wbgetentities."""
    try:
        d = get_entities([qid])
    except Exception as e:
        print(f"  [!] {qid} fetch failed: {e}")
        return None

    e = d.get("entities", {}).get(qid)
    if not e:
        return None

    info = {
        "qid":         qid,
        "label":       e.get("labels", {}).get("en", {}).get("value", qid),
        "description": e.get("descriptions", {}).get("en", {}).get("value", ""),
        "neighbors":   [],
    }

    neighbor_qids = []
    pending_neighbors = []  # [(rel, qid)]
    for prop_id, rel in REL_PROPS.items():
        for claim in (e.get("claims", {}).get(prop_id, []) or []):
            try:
                tgt = claim["mainsnak"]["datavalue"]["value"]["id"]
            except (KeyError, TypeError):
                continue
            pending_neighbors.append((rel, tgt))
            neighbor_qids.append(tgt)

    # Resolve labels in one batched call
    labels = label_lookup(list(set(neighbor_qids))[:50])
    seen = set()
    for rel, nq in pending_neighbors:
        key = (rel, nq)
        if key in seen: continue
        seen.add(key)
        info["neighbors"].append({
            "qid":      nq,
            "label":    labels.get(nq, nq),
            "relation": rel,
        })
    return info


def main():
    EXT_DIR.mkdir(parents=True, exist_ok=True)
    qids = set(EXTRA_CONCEPTS)
    for v in JAVA_TO_WIKIDATA.values():
        if v: qids.add(v)
    print(f"[fetch] {len(qids)} root Wikidata Q-IDs to fetch")

    out = []
    for i, qid in enumerate(sorted(qids), 1):
        info = fetch_concept_with_neighbors(qid)
        if info:
            print(f"  [{i:>2}/{len(qids)}] {qid:<10} {info['label']:<35} "
                  f"({len(info['neighbors'])} neighbors)")
            out.append(info)
        else:
            print(f"  [{i:>2}/{len(qids)}] {qid:<10} no data returned")
        time.sleep(0.3)  # be polite to the public endpoint

    summary = {
        "java_to_wikidata": JAVA_TO_WIKIDATA,
        "extra_concepts":   EXTRA_CONCEPTS,
        "concepts":         out,
        "total_qids":       len(out),
        "total_neighbors":  sum(len(c["neighbors"]) for c in out),
    }
    (EXT_DIR / "wikidata_cs_concepts.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n[fetch] saved {summary['total_qids']} concepts + "
          f"{summary['total_neighbors']} neighbor edges to "
          f"{EXT_DIR / 'wikidata_cs_concepts.json'}")


if __name__ == "__main__":
    main()
