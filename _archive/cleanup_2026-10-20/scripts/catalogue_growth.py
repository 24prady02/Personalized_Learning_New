"""
Catalogue growth — the LIVING-CATALOGUE step of the CPAL dynamic tier.

docs/cpal_trainable_dynamic_design.md §4c: the wrong-models catalogue is no
longer a frozen 20x3 JSON. When a student's message matches NO catalogue
wrong model well, LPDiagnostician logs it to:

    data/mental_models/unmatched/unmatched.jsonl

This script turns that raw log into reviewable catalogue *candidates*:

    1. group the unmatched messages by concept
    2. cluster each concept's messages by embedding similarity (greedy,
       no sklearn dependency)
    3. LLM-summarise each cluster of >= MIN_CLUSTER_SIZE messages into a
       candidate { wrong_belief, origin, conversation_signals } block
    4. write data/mental_models/catalogue_candidates.json

Candidates are NEVER auto-merged into the catalogue — a human reviews
catalogue_candidates.json and promotes the good ones. That keeps the
catalogue growing from real student misconceptions while staying curated.

If Ollama is unreachable the script still emits each cluster (with the raw
messages as conversation_signals and wrong_belief=null) so a human reviewer
has the grouped evidence even without an LLM summary.

Usage:
    python scripts/catalogue_growth.py
    python scripts/catalogue_growth.py --min-cluster 2 --threshold 0.5
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

UNMATCHED_PATH  = ROOT / "data" / "mental_models" / "unmatched" / "unmatched.jsonl"
CANDIDATES_PATH = ROOT / "data" / "mental_models" / "catalogue_candidates.json"
CATALOGUE_PATH  = ROOT / "data" / "mental_models" / "wrong_models_catalogue.json"

ENCODER_NAME = "sentence-transformers/all-MiniLM-L6-v2"
OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_TAGS  = "http://localhost:11434/api/tags"

DEFAULT_MIN_CLUSTER  = 3      # need >= this many similar messages to propose
DEFAULT_THRESHOLD    = 0.55   # cosine: a message joins a cluster at >= this


# ─────────────────────────────────────────────────────────────────────────
# Load
# ─────────────────────────────────────────────────────────────────────────
def load_unmatched() -> list:
    if not UNMATCHED_PATH.exists():
        print(f"[grow] no unmatched log at {UNMATCHED_PATH} — nothing to do.")
        return []
    rows = []
    with open(UNMATCHED_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("text"):
                rows.append(obj)
    print(f"[grow] loaded {len(rows)} unmatched messages from {UNMATCHED_PATH.name}")
    return rows


# ─────────────────────────────────────────────────────────────────────────
# Cluster — greedy agglomerative by cosine, no sklearn needed
# ─────────────────────────────────────────────────────────────────────────
def cluster_texts(texts: list, threshold: float) -> list:
    """Return a list of clusters; each cluster is a list of indices into
    `texts`. A message joins the first cluster whose centroid it is within
    `threshold` cosine of, else it starts a new cluster."""
    if not texts:
        return []
    from sentence_transformers import SentenceTransformer
    import numpy as np

    enc = SentenceTransformer(ENCODER_NAME)
    embs = enc.encode(texts, normalize_embeddings=True,
                      show_progress_bar=False)
    embs = np.asarray(embs, dtype="float32")

    clusters: list = []          # list of {"idx": [...], "centroid": vec}
    for i, v in enumerate(embs):
        best_c, best_sim = None, threshold
        for c in clusters:
            sim = float(np.dot(c["centroid"], v))   # both normalised
            if sim >= best_sim:
                best_c, best_sim = c, sim
        if best_c is None:
            clusters.append({"idx": [i], "centroid": v.copy()})
        else:
            best_c["idx"].append(i)
            # incremental mean, then renormalise
            n = len(best_c["idx"])
            cen = best_c["centroid"] + (v - best_c["centroid"]) / n
            norm = np.linalg.norm(cen) or 1.0
            best_c["centroid"] = cen / norm
    return [c["idx"] for c in clusters]


# ─────────────────────────────────────────────────────────────────────────
# Summarise — LLM turns a cluster into a candidate wrong-model entry
# ─────────────────────────────────────────────────────────────────────────
def detect_model() -> str:
    try:
        import requests
        r = requests.get(OLLAMA_TAGS, timeout=2)
        names = [m.get("name") for m in r.json().get("models", []) if m.get("name")]
        for pred in (lambda n: "qwen" in n.lower() and "coder" in n.lower(),
                     lambda n: "llama3" in n.lower(),
                     lambda n: True):
            for n in names:
                if pred(n):
                    return n
    except Exception:
        pass
    return "llama3.2"


def summarise_cluster(concept: str, messages: list, model: str) -> dict:
    """LLM-summarise a cluster of student messages into a candidate wrong
    model. Returns {wrong_belief, origin, conversation_signals, llm_summary}.
    On any failure returns a stub with wrong_belief=None so the human
    reviewer still has the grouped evidence."""
    sample = messages[:8]
    stub = {
        "wrong_belief": None,
        "origin": None,
        "conversation_signals": sample,
        "llm_summary": False,
    }
    prompt = (
        f"These are real student messages about the Java concept '{concept}' "
        f"that did NOT match any documented wrong mental model in our "
        f"catalogue:\n\n"
        + "\n".join(f"- {m}" for m in sample)
        + "\n\nThey likely share ONE underlying misconception. Summarise it "
        f"as a catalogue entry. Respond with ONLY a JSON object:\n"
        f'{{"wrong_belief": "one or two sentences stating the false belief", '
        f'"origin": "a short phrase — where this belief comes from", '
        f'"conversation_signals": ["3-5 short paraphrases a student holding '
        f'it would say"]}}'
    )
    try:
        import requests
        resp = requests.post(OLLAMA_URL, json={
            "model": model, "prompt": prompt, "stream": False,
            "format": "json", "options": {"temperature": 0.2, "num_predict": 400},
        }, timeout=60)
        resp.raise_for_status()
        obj = json.loads(resp.json().get("response", "") or "{}")
        wb = obj.get("wrong_belief")
        if not wb:
            return stub
        sigs = obj.get("conversation_signals") or []
        if not isinstance(sigs, list):
            sigs = [str(sigs)]
        return {
            "wrong_belief": str(wb),
            "origin": str(obj.get("origin", "") or "unknown"),
            "conversation_signals": [str(s) for s in sigs][:6],
            "llm_summary": True,
        }
    except Exception as e:
        print(f"[grow]   LLM summary failed ({type(e).__name__}); "
              f"emitting raw cluster for review.")
        return stub


# ─────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-cluster", type=int, default=DEFAULT_MIN_CLUSTER,
                    help="minimum messages in a cluster to propose a candidate")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                    help="cosine threshold for joining a cluster")
    args = ap.parse_args()

    rows = load_unmatched()
    if not rows:
        return

    # existing catalogue concepts (so we can flag candidates for brand-new
    # concepts vs new wrong models under an existing concept)
    known = set()
    try:
        known = set(json.loads(CATALOGUE_PATH.read_text(encoding="utf-8"))
                    .get("concepts", {}).keys())
    except Exception:
        pass

    by_concept = defaultdict(list)
    for r in rows:
        by_concept[r.get("concept", "unknown")].append(r["text"])

    model = detect_model()
    print(f"[grow] clustering {len(by_concept)} concept buckets "
          f"(min_cluster={args.min_cluster}, threshold={args.threshold}, "
          f"ollama_model={model})")

    candidates = {}
    t0 = time.time()
    for concept, texts in sorted(by_concept.items()):
        clusters = cluster_texts(texts, args.threshold)
        kept = [c for c in clusters if len(c) >= args.min_cluster]
        if not kept:
            print(f"[grow] {concept:24s} {len(texts)} msgs -> "
                  f"{len(clusters)} clusters, none >= {args.min_cluster}")
            continue
        concept_cands = []
        for ci in kept:
            msgs = [texts[i] for i in ci]
            summary = summarise_cluster(concept, msgs, model)
            summary.update({
                "cluster_size":  len(ci),
                "source_messages": msgs,
                "concept_in_catalogue": concept in known,
            })
            concept_cands.append(summary)
        candidates[concept] = concept_cands
        print(f"[grow] {concept:24s} {len(texts)} msgs -> "
              f"{len(kept)} candidate(s)")

    out = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "source": str(UNMATCHED_PATH),
        "params": {"min_cluster": args.min_cluster, "threshold": args.threshold},
        "note": "REVIEW REQUIRED — promote good candidates into "
                "wrong_models_catalogue.json by hand. Nothing here is "
                "auto-merged.",
        "candidates": candidates,
    }
    CANDIDATES_PATH.parent.mkdir(parents=True, exist_ok=True)
    CANDIDATES_PATH.write_text(json.dumps(out, indent=2), encoding="utf-8")
    n = sum(len(v) for v in candidates.values())
    print(f"\n[grow] wrote {n} candidate(s) across {len(candidates)} concept(s) "
          f"to {CANDIDATES_PATH}  ({time.time()-t0:.1f}s)")
    print("[grow] next step: review catalogue_candidates.json and hand-merge "
          "approved entries into wrong_models_catalogue.json")


if __name__ == "__main__":
    main()
