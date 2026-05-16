"""
Rubric Grader — the DYNAMIC LP-level tier for CPAL Stage 1.

docs/cpal_trainable_dynamic_design.md §4b: instead of guessing the student's
LP level from vocabulary (the keyword classifier) or a tiny trained head,
this asks an LLM to grade the student's text directly against the concept's
own L1-L4 rubric — the rubric the catalogue already ships.

Why this is the "dynamic" tier (non-parametric): there is no model to
retrain. Edit a rubric line in wrong_models_catalogue.json and grading
changes on the very next call. The catalogue rubric becomes the grading
*instrument*, not just prompt decoration.

Graceful degradation: if the local Ollama server is unreachable or returns
unparseable output, grade() returns level=None and the caller falls back to
the keyword classifier (classify_lp_level). The system never hard-depends on
the LLM being up — so wiring this in is risk-free.
"""
from __future__ import annotations

from typing import Dict, Optional
import hashlib
import json
import re

LP_LEVELS = ("L1", "L2", "L3", "L4")


class RubricGrader:
    """LLM-as-rubric-grader. One Ollama call per (concept, text), cached."""

    def __init__(self,
                 ollama_url: str = "http://localhost:11434/api/generate",
                 tags_url: str = "http://localhost:11434/api/tags",
                 model: Optional[str] = None,
                 timeout: float = 30.0,
                 min_confidence: float = 0.50):
        self.ollama_url = ollama_url
        self.tags_url = tags_url
        self.timeout = timeout
        self.min_confidence = min_confidence
        self.model = model or self._detect_model()
        self._cache: Dict[str, Dict] = {}

    # -- setup -------------------------------------------------------------

    def _detect_model(self) -> str:
        """Pick an installed Ollama model (prefer a code-specialised one)."""
        try:
            import requests
            r = requests.get(self.tags_url, timeout=2)
            names = [m.get("name") for m in r.json().get("models", [])
                     if m.get("name")]
            for pred in (
                lambda n: "qwen" in n.lower() and "coder" in n.lower(),
                lambda n: "deepseek" in n.lower() and "coder" in n.lower(),
                lambda n: "llama3.1" in n.lower() or "llama3.3" in n.lower(),
                lambda n: "llama3" in n.lower(),
                lambda n: True,
            ):
                for n in names:
                    if pred(n):
                        return n
        except Exception:
            pass
        return "llama3.2"

    # -- grading -----------------------------------------------------------

    @staticmethod
    def _cache_key(concept: str, text: str) -> str:
        h = hashlib.sha1(text.strip().lower().encode("utf-8")).hexdigest()[:16]
        return f"{concept}:{h}"

    @staticmethod
    def _build_prompt(student_text: str, concept: str,
                      rubric: Dict[str, str]) -> str:
        lines = []
        for lvl in LP_LEVELS:
            r = (rubric.get(lvl) or "").strip()
            if r:
                lines.append(f"{lvl}: {r}")
        rubric_block = "\n".join(lines)
        # Anchor examples are concept-agnostic but show the SHAPE of evidence
        # the grader should treat as L3 / L4. Without these, qwen2.5-coder
        # systematically pinned plain-language mechanism reasoning at L2.
        return (
            f"You are grading a student's understanding of the Java concept "
            f"'{concept}' on a 4-level Learning Progression rubric.\n\n"
            f"RUBRIC:\n{rubric_block}\n\n"
            f"STUDENT MESSAGE:\n\"{student_text}\"\n\n"
            f"GRADING RULES — read carefully, do NOT under-grade:\n"
            f"  * L1: only a symptom or question, NO rule and NO mechanism. "
            f"\"why is == false, they look the same\" -> L1.\n"
            f"  * L2: names the rule or fix but does NOT explain WHY at the "
            f"execution level. \"I have to use .equals() for strings\" -> L2.\n"
            f"  * L3: explains the EXECUTION-LEVEL MECHANISM (what the "
            f"compiler/runtime/heap/stack/reference is doing). PLAIN WORDS "
            f"COUNT AS L3. JARGON IS NOT REQUIRED. If the student traces a "
            f"causal chain that matches the L3 rubric in their own words, it "
            f"is L3.\n"
            f"  * L4: applies the same mechanism to a NOVEL case, names a "
            f"design rationale, OR explicitly generalises with phrases like "
            f"\"same idea as ...\", \"applies to any ...\", \"why Java "
            f"chose ...\".\n\n"
            f"ADVERSARIAL ANCHORS — these are the exact failure patterns "
            f"under-graders hit. Do NOT repeat them:\n"
            f"\n"
            f"  Anchor L3 (do NOT pin to L2):\n"
            f"    Student says: \"each new String() call makes its own object "
            f"somewhere in memory, so == checks if those two memory spots are "
            f"the same (they aren't), while .equals() walks the characters\"\n"
            f"    Verdict: L3.  Reason: contains rule tokens (==, .equals) AND "
            f"a complete causal mechanism trace (separate objects in memory -> "
            f"address comparison -> character walking). The rule tokens being "
            f"present does NOT make it L2; the trace makes it L3.\n"
            f"\n"
            f"  Anchor L3 alt (do NOT pin to L2):\n"
            f"    Student says: \"the loop condition gets checked before each "
            f"iteration and since nothing updates i, the condition stays true\"\n"
            f"    Verdict: L3.  Reason: explicit before-each-iteration timing "
            f"AND causal explanation. Plain words; no jargon required.\n"
            f"\n"
            f"  Anchor L4 (do NOT pin to L2 or L3):\n"
            f"    Student says: \"== is identity comparison for any reference "
            f"type — for custom classes I'd override .equals() and hashCode() "
            f"if I want content equality\"\n"
            f"    Verdict: L4.  Reason: generalises to ALL reference types "
            f"(not just String) AND names the design contract (.equals + "
            f"hashCode pairing). The mechanism is implicit; the GENERALISATION "
            f"makes it L4. Do not pin to L3 just because no design-rationale "
            f"phrase is present.\n"
            f"\n"
            f"  Anchor L4 alt (do NOT pin to L3):\n"
            f"    Student says: \"the same idea about infinite loops applies "
            f"to any for/while/do-while: if the condition variable is never "
            f"updated, the condition is always true. Why did Java's designers "
            f"make == reference equality by default?\"\n"
            f"    Verdict: L4.  Reason: \"applies to any\" generalisation "
            f"phrase + explicit design-rationale question. Two L4 signals at "
            f"once; should not land below L4.\n"
            f"\n"
            f"  * Tiebreaker: when in doubt between two adjacent levels, "
            f"choose the HIGHER one if the student's text contains a real "
            f"causal-mechanism trace OR a real generalisation. Do not be "
            f"conservative — under-grading is as bad as over-grading.\n\n"
            f"Respond with ONLY a JSON object, no other text, no markdown "
            f"fences:\n"
            f'{{"level": "L1" or "L2" or "L3" or "L4", '
            f'"confidence": a number 0.0-1.0, '
            f'"justification": "one short sentence naming the EVIDENCE that '
            f'put it at this level (mechanism/generalisation/rule/symptom)"}}'
        )

    def grade(self, student_text: str, concept: str,
              rubric: Dict[str, str]) -> Dict:
        """Grade student_text against the concept's L1-L4 rubric.

        Returns:
          {
            "level": "L1".."L4" or None,   # None => LLM unavailable/garbage
            "confidence": float 0-1,
            "justification": str,
            "source": "rubric_grader" | "rubric_grader:unavailable" | ...
          }
        The caller should use `level` only when it is not None AND
        `confidence >= self.min_confidence`; otherwise fall back to the
        keyword classifier.
        """
        out = {"level": None, "confidence": 0.0,
               "justification": "", "source": "rubric_grader"}
        text = (student_text or "").strip()
        if not text or not rubric:
            out["source"] = "rubric_grader:no_input"
            return out

        key = self._cache_key(concept, text)
        if key in self._cache:
            return dict(self._cache[key])

        try:
            import requests
            prompt = self._build_prompt(text, concept, rubric)
            resp = requests.post(self.ollama_url, json={
                "model":   self.model,
                "prompt":  prompt,
                "stream":  False,
                "format":  "json",
                "options": {"temperature": 0.0, "num_predict": 200},
            }, timeout=self.timeout)
            resp.raise_for_status()
            parsed = self._parse(resp.json().get("response", ""))
            if parsed["level"] in LP_LEVELS:
                out.update(parsed)
            else:
                out["source"] = "rubric_grader:unparseable"
        except Exception as e:
            out["source"] = "rubric_grader:unavailable"
            out["justification"] = type(e).__name__

        self._cache[key] = dict(out)
        return out

    @staticmethod
    def _parse(raw: str) -> Dict:
        """Parse the LLM's JSON reply; tolerant of stray text around it."""
        result = {"level": None, "confidence": 0.0, "justification": ""}
        if not raw:
            return result
        obj = None
        try:
            obj = json.loads(raw)
        except Exception:
            m = re.search(r"\{.*\}", raw, re.DOTALL)
            if m:
                try:
                    obj = json.loads(m.group(0))
                except Exception:
                    obj = None
        if not isinstance(obj, dict):
            return result
        lvl = str(obj.get("level", "")).upper().strip()
        if lvl in LP_LEVELS:
            result["level"] = lvl
        try:
            result["confidence"] = max(0.0, min(1.0, float(obj.get("confidence", 0.0))))
        except Exception:
            result["confidence"] = 0.0
        result["justification"] = str(obj.get("justification", ""))[:200]
        return result


# Module-level singleton — built lazily so import stays cheap.
_SINGLETON: Optional[RubricGrader] = None


def get_grader() -> RubricGrader:
    global _SINGLETON
    if _SINGLETON is None:
        _SINGLETON = RubricGrader()
    return _SINGLETON


if __name__ == "__main__":
    g = RubricGrader()
    print(f"model = {g.model}")
    demo_rubric = {
        "L1": "Sees the error but cannot say why.",
        "L2": "Knows the rule (use .equals()) but cannot explain the mechanism.",
        "L3": "Can trace: == compares addresses; two new String() calls are "
              "two heap objects at different addresses, so == is false.",
        "L4": "Understands string interning; extends to all Java objects.",
    }
    for t in ["why is == false, they look the same",
              "you have to use .equals for strings",
              "== checks the memory address and the two strings are "
              "different objects on the heap so it returns false"]:
        r = g.grade(t, "string_equality", demo_rubric)
        print(f"  [{r['level']}] conf={r['confidence']:.2f} src={r['source']} :: {t[:50]}")
