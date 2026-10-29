"""Build NLI training pairs from the knowledge graph only (no student answers).

Pairs are (premise, hypothesis, label) with label 0 = contradiction,
1 = entailment, 2 = neutral (the label order of cross-encoder/nli-deberta-v3).

* entailment
  - paraphrases the graph already holds: a misconception edge's correct rule
    (twin_logic) and the node's correct_rule; the "Right rule" of an L0 way
    and the correct rule of the misconception it links; an edge's wrong belief
    and the node's wrong_belief;
  - an edge-logic part and a way text / correct rule of the same endpoint
    concept, kept only when the two state the same rule (embedding
    similarity >= SAME_RULE, a fixed value - nothing is tuned on answers);
* contradiction
  - each misconception's wrong belief against its correct rule (both ways);
  - an edge-logic part against the wrong belief of a misconception on the
    same concept whose correct rule restates that part (same filter);
  - a parallel edge: one endpoint's name put into the other endpoint's part
    ("print moves the cursor to the next line");
* neutral
  - edge parts of edges far apart in the graph (hop distance >= 4), and
    same-concept texts that state different rules (below DIFFERENT_RULE).

The split is by concept (a hash of the concept id): pairs of dev concepts
never appear in training, so the dev score measures new concepts.

    python scripts/build_nli_pairs.py   -> data/nli_pairs.json
"""

from __future__ import annotations

import hashlib
import json
import os
import random
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from lp_graph.graph import KG  # noqa: E402

DEV_SHARE = 0.15
SEED = 13
MAX_LEN = 500
SAME_RULE = 0.5        # fixed in advance: two texts state the same rule
DIFFERENT_RULE = 0.2   # fixed in advance: two texts of one concept are about different things
EMBEDDER = "sentence-transformers/all-MiniLM-L6-v2"
CLEAN_KINDS = frozenset({"right~wrong", "wrong~right", "paraphrase_right", "paraphrase_wrong",
                         "way_right~correct_rule", "edge~own_part", "same_concept_compatible",
                         "same_edge_other_part"})


def is_dev(concept: str) -> bool:
    h = int(hashlib.sha1(concept.encode()).hexdigest(), 16)
    return (h % 1000) / 1000 < DEV_SHARE


def clip(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= MAX_LEN:
        return text
    cut = text[:MAX_LEN]
    end = max(cut.rfind(". "), cut.rfind("; "))
    return cut[:end + 1] if end > 100 else cut


def name_in(text: str, names: list[str]) -> str | None:
    for n in sorted(names, key=len, reverse=True):
        if len(n) >= 3 and re.search(rf"(?<![\w.]){re.escape(n)}(?![\w])", text, re.I):
            return n
    return None


def main() -> int:
    from sentence_transformers import SentenceTransformer

    kg = KG()
    emb = SentenceTransformer(EMBEDDER)
    rng = random.Random(SEED)
    raw = kg.knowledge.raw
    nodes = {m["id"]: m for m in raw.get("misconceptions_and_errors", [])}
    parts = kg.parts["edges"]

    pairs: list[dict] = []
    seen: set[tuple[str, str]] = set()

    def add(p: str, h: str, label: int, concept: str, kind: str) -> None:
        p, h = clip(p), clip(h)
        if not p or not h or p == h or (p, h) in seen:
            return
        seen.add((p, h))
        pairs.append({"premise": p, "hypothesis": h, "label": label, "concept": concept,
                      "kind": kind, "split": "dev" if is_dev(concept) else "train"})

    # paraphrases the graph holds
    for c in kg.concepts:
        for m in kg.mis_edges[c]:
            node = nodes.get(m.mis, {})
            if m.right and node.get("correct_rule"):
                add(m.right, node["correct_rule"], 1, c, "paraphrase_right")
            if m.wrong and node.get("wrong_belief"):
                add(m.wrong, node["wrong_belief"], 1, c, "paraphrase_wrong")
            if m.wrong and m.right:
                add(m.right, m.wrong, 0, c, "right~wrong")
                add(m.wrong, m.right, 0, c, "wrong~right")
        for w in kg.ways(c, "L0"):
            for mid in w.misconceptions:
                node = nodes.get(mid, {})
                if w.right and node.get("correct_rule"):
                    add(w.right, node["correct_rule"], 1, c, "way_right~correct_rule")

    # edge parts against texts of the same endpoint, filtered by "same rule"
    edge_parts = [(eid, p["concept"], p["text"]) for eid, info in sorted(parts.items())
                  for p in info["parts"] if p["from"] == "logic" and p["concept"] and len(p["text"]) >= 15]
    texts = sorted({t for _, _, t in edge_parts}
                   | {clip(m.right) for c in kg.concepts for m in kg.mis_edges[c] if m.right}
                   | {clip(w.text) for c in kg.concepts for w in kg.ways(c, "L1") if w.way == "states_the_rule"}
                   | {clip(w.right) for c in kg.concepts for w in kg.ways(c, "L0") if w.right})
    vec = dict(zip(texts, emb.encode(texts, normalize_embeddings=True, batch_size=64)))
    sim = lambda a, b: float(vec[clip(a)] @ vec[clip(b)])  # noqa: E731
    for eid, c, t in edge_parts:
        partners = [(clip(w.text), "way") for w in kg.ways(c, "L1") if w.way == "states_the_rule"]
        partners += [(clip(w.right), "way") for w in kg.ways(c, "L0") if w.right]
        for text, kind in partners:
            s = sim(t, text)
            if s >= SAME_RULE:
                add(t, text, 1, c, "edge~way")
            elif s < DIFFERENT_RULE:
                add(t, text, 2, c, "edge~other_rule")
        for m in kg.mis_edges[c]:
            if not (m.wrong and m.right):
                continue
            s = sim(t, m.right)
            if s >= SAME_RULE:
                add(t, m.right, 1, c, "edge~right_rule")
                add(t, m.wrong, 0, c, "edge~wrong_belief")

    # parallel edges: one endpoint's name in the other endpoint's part
    for eid, info in sorted(parts.items()):
        if info["kind"] != "parallel":
            continue
        a, b = info["src"], info["dst"]
        names = {a: kg.aliases.get(a, []) + [a, a.replace("_", " ")],
                 b: kg.aliases.get(b, []) + [b, b.replace("_", " ")]}
        tagged = {p["concept"]: p["text"] for p in info["parts"] if p["from"] == "logic" and p["concept"]}
        if set(tagged) != {a, b}:
            continue
        for own, other in ((a, b), (b, a)):
            n_other = name_in(tagged[other], names[other])
            n_own = name_in(tagged[own], names[own])
            if not n_other or not n_own:
                continue
            swapped = re.sub(rf"(?<![\w.]){re.escape(n_other)}(?![\w])", n_own, tagged[other], count=1, flags=re.I)
            if swapped != tagged[other]:
                add(tagged[own], swapped, 0, own, "swapped_endpoints")

    # an edge's whole logic entails each of its own parts
    for eid, info in sorted(parts.items()):
        lp = [x for x in info["parts"] if x["from"] == "logic"]
        whole = kg.relation_edges[eid].logic
        if len(lp) >= 2:
            for x in lp:
                add(whole, x["text"], 1, x["concept"] or info["src"], "edge~own_part")

    # two different correct statements about the same concept are compatible,
    # not a contradiction: without these pairs the model learns "same topic,
    # different words = contradiction" (it did, on the first run)
    for c in kg.concepts:
        correct = [w.text for lv in ("L1", "L2", "L3") for w in kg.ways(c, lv) if w.text]
        correct += [x["text"] for info in parts.values() for x in info["parts"]
                    if x["from"] == "logic" and x["concept"] == c]
        correct = [clip(x) for x in dict.fromkeys(correct) if len(x) >= 15]
        rng.shuffle(correct)
        for x, y in zip(correct[0::2], correct[1::2]):
            add(x, y, 2, c, "same_concept_compatible")
    for eid, info in sorted(parts.items()):
        lp = [x for x in info["parts"] if x["from"] == "logic" and len(x["text"]) >= 15]
        for x, y in zip(lp, lp[1:]):
            add(x["text"], y["text"], 2, x["concept"] or info["src"], "same_edge_other_part")

    # only pair kinds whose label is certain from the graph's structure are kept;
    # same-concept pairs (edge~way, edge~right_rule, edge~wrong_belief, swapped
    # endpoints) turned out to be on the same topic without stating the same rule
    pairs[:] = [x for x in pairs if x["kind"] in CLEAN_KINDS]
    seen.clear()
    seen.update((x["premise"], x["hypothesis"]) for x in pairs)

    # neutral: far apart edges
    n_target = max(Counter(x["label"] for x in pairs).values())
    all_parts = [(c, t) for _, c, t in edge_parts]
    tries = 0
    while sum(1 for x in pairs if x["label"] == 2) < n_target and tries < n_target * 30:
        tries += 1
        (c1, t1), (c2, t2) = rng.sample(all_parts, 2)
        if kg.hop_distance(c1, c2) >= 4:
            add(t1, t2, 2, c1, "far_edges")
    pairs[:] = [x for x in pairs if x["kind"] in CLEAN_KINDS or x["kind"] == "far_edges"]

    pairs.sort(key=lambda x: (x["split"], x["concept"], x["kind"], x["premise"], x["hypothesis"]))
    json.dump(pairs, open(ROOT / "data" / "nli_pairs.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("pairs", len(pairs))
    print("by split/label", sorted(Counter((x["split"], x["label"]) for x in pairs).items()))
    print("by kind", sorted(Counter(x["kind"] for x in pairs).items()))
    print("dev concepts", len({x["concept"] for x in pairs if x["split"] == "dev"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
