"""
cso_traversal.py — Direct CSO v3.5 N-Triples traversal.

Builds a fast in-memory index over data/cse_kg_external/CSO.3.5.nt and exposes
the four relations the student-knowledge-graph layer needs:

    superTopicOf       (subject is parent of object)
    relatedEquivalent  (symmetric peer relation)
    contributesTo      (subject contributes to object)
    sameAs / preferentialEquivalent (lexical normalisation)

Lookup is by short topic slug (e.g. "string_matching", "object_oriented_programming",
"computer_programming"). The slug is the suffix of the CSO URI
`https://cso.kmi.open.ac.uk/topics/<slug>`.

Memory footprint: ~30 MB for the full 166K-triple v3.5 file. Build time: ~3 s
on first call, cached to data/cse_kg_local/cso_v35_index.pkl thereafter.

Why this module:
  - The existing LocalCSEKGClient only handles 20 CPAL-internal Java concepts
    and returns CPAL wrong-model IDs, not real CSO neighbours.
  - This module talks directly to the CSO triples so prereq / related queries
    actually traverse the 14k-node ontology.

Wired by:
  - src/knowledge_graph/student_knowledge_graph.py  (the per-student graph)
  - scripts/cpal_chat_app.py  (via _build_cse_kg_block)
"""
from __future__ import annotations

import os
import pickle
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


# Default location of the CSO N-Triples file
DEFAULT_CSO_NT = Path(__file__).resolve().parents[2] / "data" / "cse_kg_external" / "CSO.3.5.nt"
DEFAULT_INDEX_CACHE = Path(__file__).resolve().parents[2] / "data" / "cse_kg_local" / "cso_v35_index.pkl"

# CSO URI prefix
TOPIC_PREFIX = "https://cso.kmi.open.ac.uk/topics/"

# The four schema relations we care about (others are ignored to keep index small)
REL_SUPER_TOPIC_OF        = "http://cso.kmi.open.ac.uk/schema/cso#superTopicOf"
REL_RELATED_EQUIVALENT    = "http://cso.kmi.open.ac.uk/schema/cso#relatedEquivalent"
REL_CONTRIBUTES_TO        = "http://cso.kmi.open.ac.uk/schema/cso#contributesTo"
REL_PREFERENTIAL_EQUIV    = "http://cso.kmi.open.ac.uk/schema/cso#preferentialEquivalent"

# Compiled regex for the N-Triples line format
_LINE_RE = re.compile(r'^<([^>]+)>\s+<([^>]+)>\s+<([^>]+)>\s+\.\s*$')


def _slug(uri: str) -> Optional[str]:
    """Extract the topic slug from a CSO URI, or None if not a topic URI."""
    if uri.startswith(TOPIC_PREFIX):
        return uri[len(TOPIC_PREFIX):]
    return None


class CSOTraversal:
    """Direct traversal over CSO v3.5 triples.

    Indexes maintained:
      _parents[slug]   = set of super-topic slugs (broader topics)
      _children[slug]  = set of sub-topic slugs (narrower topics)
      _related[slug]   = set of slugs with relatedEquivalent
      _contributes[slug] = set of slugs this slug contributes_to
      _contributed_by[slug] = set of slugs that contribute_to this slug
      _alias[slug]     = canonical slug (via preferentialEquivalent)
    """

    def __init__(self, nt_path: Path = DEFAULT_CSO_NT,
                 cache_path: Path = DEFAULT_INDEX_CACHE,
                 use_cache: bool = True):
        self.nt_path = Path(nt_path)
        self.cache_path = Path(cache_path)
        self._parents: Dict[str, Set[str]] = defaultdict(set)
        self._children: Dict[str, Set[str]] = defaultdict(set)
        self._related: Dict[str, Set[str]] = defaultdict(set)
        self._contributes: Dict[str, Set[str]] = defaultdict(set)
        self._contributed_by: Dict[str, Set[str]] = defaultdict(set)
        self._alias: Dict[str, str] = {}
        self._loaded = False

        if use_cache and self._load_cache():
            self._loaded = True
        elif self.nt_path.exists():
            self._build_from_nt()
            if use_cache:
                self._save_cache()
            self._loaded = True

    # ── Build / cache ─────────────────────────────────────────────────────

    def _build_from_nt(self) -> None:
        """Stream the N-Triples file once, populate indexes."""
        print(f"[CSOTraversal] indexing {self.nt_path.name} (one-time, ~3 s)...")
        n = 0
        with open(self.nt_path, "r", encoding="utf-8") as fh:
            for line in fh:
                m = _LINE_RE.match(line)
                if not m:
                    continue
                subj_uri, pred_uri, obj_uri = m.groups()
                s, o = _slug(subj_uri), _slug(obj_uri)
                if s is None or o is None:
                    continue
                if pred_uri == REL_SUPER_TOPIC_OF:
                    # s is broader than o ; o is sub-topic of s
                    self._children[s].add(o)
                    self._parents[o].add(s)
                elif pred_uri == REL_RELATED_EQUIVALENT:
                    self._related[s].add(o)
                    self._related[o].add(s)
                elif pred_uri == REL_CONTRIBUTES_TO:
                    self._contributes[s].add(o)
                    self._contributed_by[o].add(s)
                elif pred_uri == REL_PREFERENTIAL_EQUIV:
                    # o is the canonical form of s
                    self._alias[s] = o
                n += 1
        print(f"[CSOTraversal] indexed {n} triples · "
              f"{len(self._parents)} topics with parents · "
              f"{len(self._related)} with related · "
              f"{len(self._contributes)} with contributes-to")

    def _save_cache(self) -> None:
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_path, "wb") as fh:
            pickle.dump({
                "parents":         dict(self._parents),
                "children":        dict(self._children),
                "related":         dict(self._related),
                "contributes":     dict(self._contributes),
                "contributed_by":  dict(self._contributed_by),
                "alias":           self._alias,
            }, fh, protocol=pickle.HIGHEST_PROTOCOL)
        print(f"[CSOTraversal] cached index -> {self.cache_path.name}")

    def _load_cache(self) -> bool:
        if not self.cache_path.exists():
            return False
        try:
            with open(self.cache_path, "rb") as fh:
                d = pickle.load(fh)
            self._parents       = defaultdict(set, {k: set(v) for k, v in d["parents"].items()})
            self._children      = defaultdict(set, {k: set(v) for k, v in d["children"].items()})
            self._related       = defaultdict(set, {k: set(v) for k, v in d["related"].items()})
            self._contributes   = defaultdict(set, {k: set(v) for k, v in d["contributes"].items()})
            self._contributed_by= defaultdict(set, {k: set(v) for k, v in d["contributed_by"].items()})
            self._alias         = d.get("alias", {})
            print(f"[CSOTraversal] loaded cached index from {self.cache_path.name} · "
                  f"{len(self._parents)} indexed topics")
            return True
        except Exception as e:
            print(f"[CSOTraversal] cache load failed ({e}); will rebuild")
            return False

    # ── Public lookup API ──────────────────────────────────────────────────

    def canonical(self, slug: str) -> str:
        """Return the canonical slug (follow preferentialEquivalent if any)."""
        return self._alias.get(slug, slug)

    def exists(self, slug: str) -> bool:
        s = self.canonical(slug)
        return (s in self._parents or s in self._children
                or s in self._related or s in self._contributes
                or s in self._contributed_by)

    def get_parents(self, slug: str) -> List[str]:
        """Direct super-topics (one hop up)."""
        return sorted(self._parents.get(self.canonical(slug), set()))

    def get_children(self, slug: str) -> List[str]:
        """Direct sub-topics (one hop down)."""
        return sorted(self._children.get(self.canonical(slug), set()))

    def get_related(self, slug: str) -> List[str]:
        """Symmetric peer topics."""
        return sorted(self._related.get(self.canonical(slug), set()))

    def get_contributes(self, slug: str) -> List[str]:
        """Topics this slug contributes_to."""
        return sorted(self._contributes.get(self.canonical(slug), set()))

    def get_contributed_by(self, slug: str) -> List[str]:
        """Topics that contribute_to this slug."""
        return sorted(self._contributed_by.get(self.canonical(slug), set()))

    def get_prerequisites(self, slug: str, depth: int = 1) -> List[str]:
        """Concepts you need first. Approximation: parents (broader topics) +
        topics that contribute_to this one. For depth > 1, walk transitively
        up the super-topic chain.
        """
        s = self.canonical(slug)
        out: Set[str] = set()
        # 1-hop: parents + things that contribute to me
        out.update(self._parents.get(s, set()))
        out.update(self._contributed_by.get(s, set()))
        # Walk up depth levels
        frontier = set(self._parents.get(s, set()))
        for _ in range(depth - 1):
            next_frontier: Set[str] = set()
            for p in frontier:
                next_frontier.update(self._parents.get(p, set()))
            out.update(next_frontier)
            frontier = next_frontier
        out.discard(s)
        return sorted(out)

    def get_neighbours(self, slug: str) -> Dict[str, List[str]]:
        """All four neighbour types for a topic, suitable for a graph render."""
        s = self.canonical(slug)
        return {
            "parents":         self.get_parents(s),
            "children":        self.get_children(s),
            "related":         self.get_related(s),
            "contributes_to":  self.get_contributes(s),
            "contributed_by":  self.get_contributed_by(s),
        }

    def shortest_path(self, src: str, dst: str, max_depth: int = 4) -> Optional[List[str]]:
        """Find the shortest path between two topics across {parents, children,
        related} edges. Returns the list of slugs including endpoints, or None."""
        src, dst = self.canonical(src), self.canonical(dst)
        if src == dst:
            return [src]
        seen = {src}
        frontier: List[Tuple[str, List[str]]] = [(src, [src])]
        for _ in range(max_depth):
            next_frontier: List[Tuple[str, List[str]]] = []
            for node, path in frontier:
                neighbours = (
                    self._parents.get(node, set())
                    | self._children.get(node, set())
                    | self._related.get(node, set())
                )
                for nb in neighbours:
                    if nb == dst:
                        return path + [nb]
                    if nb not in seen:
                        seen.add(nb)
                        next_frontier.append((nb, path + [nb]))
            frontier = next_frontier
            if not frontier:
                break
        return None

    def search(self, query: str, limit: int = 10) -> List[str]:
        """Substring search across all indexed slugs (slugs have underscores in
        place of spaces, e.g. 'object_oriented_programming')."""
        q = query.lower().replace(" ", "_")
        slugs = (set(self._parents.keys())
                 | set(self._children.keys())
                 | set(self._related.keys())
                 | set(self._contributes.keys())
                 | set(self._contributed_by.keys()))
        hits = [s for s in slugs if q in s]
        # Prefer exact / prefix matches
        hits.sort(key=lambda s: (s != q, not s.startswith(q), len(s)))
        return hits[:limit]


# Singleton (lazy)
_INSTANCE: Optional[CSOTraversal] = None

def get_cso() -> CSOTraversal:
    """Return the process-wide CSOTraversal singleton (loaded on first call)."""
    global _INSTANCE
    if _INSTANCE is None:
        _INSTANCE = CSOTraversal()
    return _INSTANCE


if __name__ == "__main__":
    # Quick smoke test
    cso = get_cso()
    for concept in ["computer_programming", "object_oriented_programming",
                    "string_matching", "java_(programming_language)"]:
        print(f"\n--- {concept} ---")
        print(f"  exists: {cso.exists(concept)}")
        print(f"  parents (broader):       {cso.get_parents(concept)[:4]}")
        print(f"  children (narrower):     {cso.get_children(concept)[:4]}")
        print(f"  related:                 {cso.get_related(concept)[:4]}")
        print(f"  prerequisites (1 hop):   {cso.get_prerequisites(concept)[:6]}")
