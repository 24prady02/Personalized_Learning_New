"""
Concept Resolver — multi-label concept detection for CPAL Stage 1.

Replaces the single-concept `_extract_concept` heuristic with a ranked,
multi-label resolver: one student message can mention several Java concepts
("my loop never stops and the array index is off"), and `resolve()` returns
ALL of them above a confidence floor so the LP diagnostic can probe and level
each one independently.

Tier 1 (this module): deterministic signature scoring over the 20 catalogue
concepts — no model dependencies, always available, debuggable. This is the
"dynamic" cold-start floor described in docs/cpal_trainable_dynamic_design.md
§4a. A retrieval / trained-head tier can be layered behind the same
`resolve()` interface later without touching callers.

Output contract:
    resolve(session_data) -> List[(concept_id, confidence)]
        ranked desc by confidence, always >= 1 entry. confidence is in
        [0, 1]; ("unknown", 0.0) is returned only when nothing matches.
    top_concept(session_data) -> str
        the single best concept (back-compat with the old _extract_concept).

The CONCEPT_SIGNATURES table is the single source of truth for the 20
catalogue concept IDs — orchestrator.py imports it from here so concept
detection and the wrong-models catalogue can never drift apart again.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple


# ─────────────────────────────────────────────────────────────────────────
# Concept-detection signature table.
#
# Maps each of the 20 wrong-models-catalogue concept IDs to detection
# patterns. Weighting: an error-message hit is the strongest signal (Java's
# compiler / runtime diagnostics are concept-specific and unambiguous), a
# code hit is moderate, a free-text hit is weakest.
# ─────────────────────────────────────────────────────────────────────────
CONCEPT_ERROR_WEIGHT = 3
CONCEPT_CODE_WEIGHT  = 2
CONCEPT_TEXT_WEIGHT  = 1

CONCEPT_SIGNATURES: Dict[str, Dict[str, List[str]]] = {
    "type_mismatch": {
        "error": ["incompatible types", "cannot convert",
                  "bad operand type", "int cannot be converted to string",
                  "string cannot be converted to int"],
        "code":  [],
        "text":  ["int to string", "string to int", "concatenat",
                  "combine them", "won't work with the string"],
    },
    "infinite_loop": {
        "error": [],
        "code":  [],
        "text":  ["infinite loop", "runs forever", "loop never stops",
                  "never ends", "doesn't stop", "won't stop",
                  "keeps going", "loop hangs"],
    },
    "null_pointer": {
        "error": ["nullpointerexception"],
        "code":  [],
        "text":  ["null pointer", "is null", "why is it null", " npe"],
    },
    "string_equality": {
        "error": [],
        "code":  [".equals("],
        "text":  ["== false", "== returns false", "string equality",
                  "equals instead of ==", "comparing strings",
                  "two strings", "both hello", "same characters",
                  # also catch the same misconception when phrased about
                  # reference identity more broadly — the catalogue covers
                  # this whether the student talks about strings OR any
                  # object reference (the L4 generalisation case)
                  ".equals", "reference equality",
                  "compares addresses", "compares the address",
                  "compares memory address", "object reference",
                  "comparing object references", "identity comparison"],
    },
    "variable_scope": {
        "error": ["cannot find symbol"],
        "code":  [],
        "text":  ["out of scope", "variable scope", "block scope",
                  "declared in the if", "declared inside the loop",
                  "use it after the", "use it outside"],
    },
    "assignment_vs_compare": {
        "error": ["int cannot be converted to boolean"],
        "code":  [],
        "text":  ["= instead of ==", "assignment in the condition",
                  "single equals", "using = in", "if x ="],
    },
    "integer_division": {
        "error": [],
        "code":  [],
        "text":  ["integer division", "5/2", "5 / 2", "divided by",
                  "truncat", "rounds down", "rounded it",
                  "decimal", "why 2 instead"],
    },
    "scanner_buffer": {
        "error": [],
        "code":  ["nextline", "nextint", "scanner"],
        "text":  ["nextline", "nextint", "scanner", "skipping input",
                  "input buffer", "leftover newline", "reading nothing"],
    },
    "array_index": {
        "error": ["arrayindexoutofboundsexception", "indexoutofbounds"],
        "code":  [],
        "text":  ["index out of bound", "array index", "off by one",
                  "off-by-one", "last element", "arr[5]"],
    },
    "missing_return": {
        "error": ["missing return statement"],
        "code":  [],
        "text":  ["missing return", "not all paths return",
                  "missing a return"],
    },
    "array_not_allocated": {
        "error": [],
        "code":  ["new int[", "new double[", "new string["],
        "text":  ["array is null", "didn't allocate", "without new",
                  "array not allocated", "declared it as an array"],
    },
    "boolean_operators": {
        "error": [],
        "code":  [],
        # Tightened: removed "always true"/"always false" — they were firing
        # on infinite-loop discussions ("the condition is always true") and
        # silently mis-routing the message to boolean_operators.
        "text":  ["&& vs ||", "|| vs &&", "and vs or", "boolean operator",
                  "logical operator", "de morgan", "short-circuit",
                  "short circuit", "boolean and", "boolean or"],
    },
    "sentinel_loop": {
        "error": [],
        "code":  [],
        "text":  ["sentinel", "priming read", "first value skipped",
                  "read before the loop", "read input twice"],
    },
    "unreachable_code": {
        "error": ["unreachable statement", "unreachable code"],
        "code":  [],
        "text":  ["unreachable", "after the return", "code after return",
                  "dead code"],
    },
    "string_immutability": {
        "error": [],
        "code":  [".replace(", ".substring(", ".touppercase("],
        "text":  ["immutable", "string didn't change",
                  "string did not change", "replace didn't",
                  "modify the string", "modify a string"],
    },
    "no_default_constructor": {
        "error": ["no suitable constructor",
                  "actual and formal argument lists differ",
                  "constructor in class"],
        "code":  [],
        "text":  ["default constructor", "no-arg constructor",
                  "no argument constructor", "no-argument constructor"],
    },
    "static_vs_instance": {
        "error": ["non-static",
                  "cannot be referenced from a static context"],
        "code":  [],
        "text":  ["static context", "static method", "instance method",
                  "static vs instance", "from a static"],
    },
    "foreach_no_modify": {
        "error": [],
        "code":  [],
        "text":  ["for-each", "for each loop", "enhanced for",
                  "loop variable", "array didn't change",
                  "didn't modify the array", "modifying the element"],
    },
    "overloading": {
        "error": [],
        "code":  [],
        "text":  ["overload", "overloading", "wrong method called",
                  "wrong version called", "method selection",
                  "which version is called"],
    },
    "generics_primitives": {
        "error": ["unexpected type",
                  "type argument cannot be of primitive type"],
        "code":  ["arraylist<int>", "arraylist<double>", "list<int>"],
        "text":  ["arraylist<int>", "wrapper class", "<integer>",
                  "primitive in arraylist", "generics with int"],
    },
}

#: A secondary concept must reach at least this confidence to count as
#: "also mentioned" in the message. The single top-scoring concept is always
#: returned even if it is below the floor, so there is always a focus.
CONCEPT_CONFIDENCE_FLOOR = 0.20

#: When the strongest signature-derived confidence is below this, the resolver
#: also runs the embedding-retrieval tier (CatalogueRAG) and blends. Above
#: this we trust signatures and skip the heavier RAG call.
SIGNATURE_STRONG_FLOOR = 0.55

#: Cosine-similarity floor for a RAG-derived concept hit to count as evidence.
#: Below ~0.25 is essentially unrelated in MiniLM-L6 embedding space.
RAG_SIM_FLOOR = 0.30


def all_catalogue_concepts() -> List[str]:
    """The 20 catalogue concept IDs, sorted — the valid concept vocabulary."""
    return sorted(CONCEPT_SIGNATURES.keys())


class ConceptResolver:
    """Multi-label concept detector — two tiers.

    Tier 1: signature scoring (deterministic, offline, always on).
    Tier 2: CatalogueRAG embedding retrieval (optional, lazy). Fires when
            signatures are WEAK on a message — typical for rich generalising
            text that doesn't use the literal catalogue phrasings. The
            previous run missed `string_equality` in "== compares addresses
            for any object reference" because the signature table only
            matched literal "== false" / "both hello" patterns; retrieval
            catches it semantically.
    """

    def __init__(self, signatures: Optional[Dict] = None,
                 confidence_floor: float = CONCEPT_CONFIDENCE_FLOOR,
                 enable_rag: bool = True):
        self.signatures = signatures or CONCEPT_SIGNATURES
        self.confidence_floor = confidence_floor
        self.enable_rag = enable_rag
        self._rag = None              # CatalogueRAG, built lazily
        self._rag_failed = False

    # -- scoring -----------------------------------------------------------

    def _raw_scores(self, session_data: Dict) -> Dict[str, int]:
        """Weighted signature-hit count per concept (0-score concepts dropped)."""
        error    = (session_data.get("error_message") or "").lower()
        code     = (session_data.get("code") or "").lower()
        question = (session_data.get("question") or "").lower()
        free_text = f"{question}\n{error}\n{code}"

        scores: Dict[str, int] = {}
        for concept, sig in self.signatures.items():
            s  = CONCEPT_ERROR_WEIGHT * sum(p in error     for p in sig["error"])
            s += CONCEPT_CODE_WEIGHT  * sum(p in code      for p in sig["code"])
            s += CONCEPT_TEXT_WEIGHT  * sum(p in free_text for p in sig["text"])
            if s > 0:
                scores[concept] = s
        return scores

    # -- Tier 2: RAG -------------------------------------------------------

    def _get_rag(self):
        """Lazily build the CatalogueRAG retriever. Returns None if disabled,
        not built yet AND deps missing, or build failed earlier."""
        if not self.enable_rag or self._rag_failed:
            return None
        if self._rag is None:
            try:
                from src.orchestrator.catalogue_rag import CatalogueRAG
                self._rag = CatalogueRAG()
            except Exception as e:
                print(f"[ConceptResolver] RAG unavailable ({e}); "
                      f"signature-only.")
                self._rag_failed = True
                return None
        return self._rag

    def _rag_concept_scores(self, session_data: Dict) -> Dict[str, float]:
        """Per-concept evidence score derived from CatalogueRAG retrieval.

        Pulls the top wrong-model matches across the WHOLE catalogue (no
        concept filter), groups by concept, takes the max cosine similarity
        per concept, and maps it into [0,1] via a sigmoid-ish floor mapping
        so similarities below RAG_SIM_FLOOR contribute nothing.
        """
        rag = self._get_rag()
        if rag is None:
            return {}
        text = (session_data.get("question") or "") + " " + \
               (session_data.get("error_message") or "")
        text = text.strip()
        if not text:
            return {}
        try:
            rows = rag.retrieve_wrong_models(text, top_k=10,
                                             concept_filter=None)
        except Exception as e:
            print(f"[ConceptResolver] RAG retrieve failed: {e}")
            return {}
        per_concept_max: Dict[str, float] = {}
        for r in rows:
            c = r.get("concept")
            s = float(r.get("similarity", 0.0))
            if c and s > per_concept_max.get(c, 0.0):
                per_concept_max[c] = s
        # Map cosine -> [0,1] confidence: below the floor contributes 0,
        # 0.30 -> 0.0, 0.80 -> 1.0 (linear). Caps at 1.0.
        denom = max(1e-6, 1.0 - RAG_SIM_FLOOR)
        scaled = {}
        for c, s in per_concept_max.items():
            if s < RAG_SIM_FLOOR:
                continue
            scaled[c] = round(min(1.0, (s - RAG_SIM_FLOOR) / denom), 3)
        return scaled

    @staticmethod
    def _to_confidence(score: int, total: int) -> float:
        """Map a raw signature score to a [0,1] confidence.

        Blends two views so neither dominates:
          share    = score / total          — how dominant this concept is
                                               among everything that matched
          strength = score / (score + 3)    — absolute-evidence saturation, so
                                               a lone weak hit is not falsely
                                               "confident"
        strength is weighted higher: a concept with strong evidence is
        confident even when the message also mentions other concepts.
        """
        share    = score / total if total else 0.0
        strength = score / (score + 3)
        return round(0.35 * share + 0.65 * strength, 3)

    # -- public API --------------------------------------------------------

    def resolve(self, session_data: Dict,
                max_concepts: int = 3) -> List[Tuple[str, float]]:
        """Return ranked [(concept_id, confidence), ...] — always >= 1 entry.

        Two-tier:
          - Tier 1 (always on): signature scoring over the 20 catalogue
            concepts. Deterministic, debuggable.
          - Tier 2 (fires when Tier 1 is weak): CatalogueRAG embedding
            retrieval. Catches concepts in rich generalising prose where
            literal signature phrases don't appear.

        - An explicit catalogue-valid `concept`/`concept_id` on session_data
          short-circuits to [(that, 1.0)].
        - The top concept is always returned (so there is always a focus).
        - Additional concepts are returned only above the floor, capped at
          `max_concepts`.
        - ("unknown", 0.0) is returned only when BOTH tiers find nothing.
        """
        explicit = session_data.get("concept") or session_data.get("concept_id")
        if explicit in self.signatures:
            return [(explicit, 1.0)]

        # --- Tier 1: signatures ------------------------------------------
        raw = self._raw_scores(session_data)
        total = sum(raw.values())
        sig_conf: Dict[str, float] = {
            c: self._to_confidence(s, total) for c, s in raw.items()
        } if raw else {}
        sig_top = max(sig_conf.values(), default=0.0)

        # --- Tier 2: RAG (only when signatures are weak) -----------------
        # Weak = the strongest signature confidence is below SIGNATURE_STRONG_FLOOR.
        # That covers two regimes:
        #   (a) nothing matched at all (raw empty)
        #   (b) something matched but ambiguously
        rag_conf: Dict[str, float] = {}
        if sig_top < SIGNATURE_STRONG_FLOOR:
            rag_conf = self._rag_concept_scores(session_data)

        if not sig_conf and not rag_conf:
            return [("unknown", 0.0)]

        # Blend per-concept: take the MAX of signature-derived and RAG-derived
        # confidence. Either source alone is sufficient evidence; both being
        # present is corroboration but we don't double-count.
        all_concepts = set(sig_conf) | set(rag_conf)
        blended: Dict[str, float] = {
            c: round(max(sig_conf.get(c, 0.0), rag_conf.get(c, 0.0)), 3)
            for c in all_concepts
        }
        ranked = sorted(blended.items(), key=lambda t: t[1], reverse=True)

        out = [ranked[0]]                       # focus is always kept
        for concept, conf in ranked[1:max_concepts]:
            if conf >= self.confidence_floor:
                out.append((concept, conf))
        return out

    def top_concept(self, session_data: Dict) -> str:
        """Single best concept — back-compat replacement for _extract_concept."""
        return self.resolve(session_data)[0][0]


# Module-level singleton (cheap to build — no I/O, no model load).
_SINGLETON: Optional[ConceptResolver] = None


def get_resolver() -> ConceptResolver:
    """Lazy module-level resolver. Subsequent calls reuse it."""
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = ConceptResolver()
    return _SINGLETON


if __name__ == "__main__":
    r = get_resolver()
    cases = [
        {"error_message": "Exception in thread main java.lang.NullPointerException"},
        {"question": "my loop never stops and I think the array index is off by one"},
        {"question": "5 divided by 2 gives 2 and == is false for my two strings"},
        {"question": "what is the weather today"},
        {"concept": "scanner_buffer", "question": "anything"},
    ]
    for sd in cases:
        print(f"  {sd}")
        for concept, conf in r.resolve(sd):
            print(f"      {concept:24s} {conf:.3f}")
