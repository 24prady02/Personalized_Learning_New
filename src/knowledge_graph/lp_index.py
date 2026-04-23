"""
Self-contained learning-progression index.

Loads data/pedagogical_kg/learning_progressions.json at init time and exposes
a single query: get_path(target_concept, current_mastery) -> ordered path to
the target, annotated with prerequisites, mastery, thresholds, and a
next_concept pointer.

This is a lighter-weight alternative to pedagogical_kg_integration.py for
callers that only need the LP lookup and don't want to drag in the full
pedagogical-KG builder + its dependencies.
"""
from pathlib import Path
from typing import Dict, List, Optional
import json


class LPIndex:
    def __init__(self, json_path: str = "data/pedagogical_kg/learning_progressions.json"):
        self.json_path = Path(json_path)
        self.progressions: List[Dict] = []
        self._by_concept: Dict[str, List[Dict]] = {}
        self._load()

    def _load(self) -> None:
        if not self.json_path.exists():
            print(f"[LP] no progressions file at {self.json_path}")
            return
        with open(self.json_path) as f:
            self.progressions = json.load(f)
        for lp in self.progressions:
            for c in lp.get("concept_sequence", []):
                self._by_concept.setdefault(c, []).append(lp)
        print(f"[LP] loaded {len(self.progressions)} progressions "
              f"covering {len(self._by_concept)} concepts")

    def find_progression_for(self, target_concept: str) -> Optional[Dict]:
        """Return the shortest LP that contains target_concept, or None."""
        cands = self._by_concept.get(target_concept, [])
        if not cands:
            return None
        return min(cands, key=lambda lp: len(lp.get("concept_sequence", [])))

    def get_path(self, target_concept: str,
                 current_mastery: Optional[Dict[str, float]] = None) -> Optional[Dict]:
        """Return structured path up to (and including) target_concept.

        Each step: {concept, current_mastery, required_mastery, ready,
                    difficulty, prerequisites}
        Top-level: {progression_id, path, next_concept, on_track}
        """
        current_mastery = current_mastery or {}
        lp = self.find_progression_for(target_concept)
        if lp is None:
            return None

        seq = lp["concept_sequence"]
        thresholds = lp.get("mastery_thresholds", {})
        difficulties = lp.get("difficulty_levels", [])
        prereqs = lp.get("prerequisites", {})
        path = []
        for i, concept in enumerate(seq):
            mastery = float(current_mastery.get(concept, 0.0))
            threshold = float(thresholds.get(concept, 0.7))
            diff = int(difficulties[i]) if i < len(difficulties) else 2
            path.append({
                "concept":          concept,
                "current_mastery":  mastery,
                "required_mastery": threshold,
                "ready":            mastery >= threshold,
                "difficulty":       diff,
                "prerequisites":    list(prereqs.get(concept, [])),
            })
            if concept == target_concept:
                break

        # next concept = first step not-yet-ready; if all are ready, target itself
        next_concept = next(
            (p["concept"] for p in path if not p["ready"]),
            target_concept,
        )
        # on_track iff every step strictly before target is ready
        on_track = all(p["ready"] for p in path[:-1]) if len(path) > 1 else True

        return {
            "progression_id":  lp["id"],
            "target_concept":  target_concept,
            "path":            path,
            "next_concept":    next_concept,
            "on_track":        on_track,
            "path_length":     len(path),
        }

    def render_prompt_block(self, lp_path: Dict, window: int = 2) -> str:
        """Format a path dict for inclusion in the Ollama prompt.

        Windows the path to [next_concept - window, next_concept + window]
        to keep the prompt compact on long progressions (22-step aggregate
        LPs would otherwise blow up token count).
        """
        path = lp_path["path"]
        # locate next_concept
        try:
            n_idx = next(i for i, p in enumerate(path)
                         if p["concept"] == lp_path["next_concept"])
        except StopIteration:
            n_idx = len(path) - 1
        lo = max(0, n_idx - window)
        hi = min(len(path), n_idx + window + 1)
        windowed = path[lo:hi]
        truncated = (lo > 0) or (hi < len(path))

        lines = [
            f"Progression: {lp_path['progression_id']}",
            f"Target concept: {lp_path['target_concept']}  (next step: {lp_path['next_concept']})",
            f"On track: {lp_path['on_track']}  "
            f"(showing steps {lo+1}-{hi} of {len(path)})",
        ]
        if lo > 0:
            lines.append(f"  ... {lo} earlier steps already covered ...")
        for i, step in enumerate(windowed, start=lo+1):
            status = "[ready]" if step["ready"] else "[NOT ready]"
            prereqs_short = step["prerequisites"][-3:]  # most recent prereqs
            prereq = (", ".join(prereqs_short)
                      if prereqs_short else "none")
            if len(step["prerequisites"]) > 3:
                prereq = f"...+{len(step['prerequisites'])-3} earlier, {prereq}"
            marker = "=>" if step["concept"] == lp_path["next_concept"] else "  "
            lines.append(
                f"  {marker} {i}. {step['concept']:<22} "
                f"diff={step['difficulty']}  "
                f"mastery={step['current_mastery']:.2f}/{step['required_mastery']:.2f} "
                f"{status}  prereqs=[{prereq}]"
            )
        if hi < len(path):
            lines.append(f"  ... {len(path) - hi} later steps (not yet in scope) ...")
        lines.append(
            "MUST: teach strictly up to and including the 'next step' (=>). "
            "Do not introduce concepts from later in the path until the next "
            "step crosses its mastery threshold."
        )
        return "\n".join(lines)


if __name__ == "__main__":
    # smoke test
    idx = LPIndex()
    for target in ["recursion", "null_pointer", "type_mismatch", "not_a_real_concept"]:
        print("\n" + "-" * 60)
        print(f"target: {target}")
        m = {"type_mismatch": 0.9, "infinite_loop": 0.85, "null_pointer": 0.5,
             "string_equality": 0.3, "variable_scope": 0.6, "functions": 0.4}
        path = idx.get_path(target, m)
        if path is None:
            print(f"  no progression contains {target}")
            continue
        print(idx.render_prompt_block(path))
