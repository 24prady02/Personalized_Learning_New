"""
engine.py — the complete per-prompt algorithm (Algorithm sheet, Steps 1-13).

    engine = get_engine()
    result = engine.process("maya", "the loop stops when i reaches 10 because ...",
                            shown_text=quiz_question_and_code, session_id="2026-10-02")

Returns, for every concept the prompt is about: the prompt's own level, the
student's level on that concept's L0-L4 ladder, confidence, the evidence and
the gates that fired. The student graph is saved after every prompt and the
concept map is redrawn.
"""
from __future__ import annotations

import json
import threading
import time
from pathlib import Path
from typing import Dict, List, Optional

from . import judge as judgelib
from . import models
from .evidence import asks_beyond, collect, content_gate, help_seeking
from .identify import identify, split_clauses
from .knowledge import ROOT, PercptKnowledge, get_knowledge
from .ladder import LEVELS, walk
from .render import write_map
from .student_graph import StudentGraph
from .thresholds import ID_CONF, MIN_WORDS

STORE_DIR = ROOT / "data" / "lp_percpt_students"
MAP_DIR = ROOT / "output" / "concept_maps"
REVIEW_LOG = ROOT / "data" / "lp_percpt_review.jsonl"
TIERS = ("low", "medium", "high")


class LPPercptEngine:
    def __init__(self, kg: Optional[PercptKnowledge] = None,
                 store_dir: Path = STORE_DIR, map_dir: Optional[Path] = MAP_DIR,
                 review_log: Optional[Path] = REVIEW_LOG):
        self.kg = kg or get_knowledge()
        self.store_dir = Path(store_dir)
        self.map_dir = Path(map_dir) if map_dir else None
        self.review_log = Path(review_log) if review_log else None
        self._lock = threading.Lock()
        self._graphs: Dict[str, StudentGraph] = {}

    # ── student graphs ──────────────────────────────────────────────────────
    def _path(self, student_id: str) -> Path:
        safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in student_id)[:80] or "anon"
        return self.store_dir / f"{safe}.json"

    def graph(self, student_id: str) -> StudentGraph:
        if student_id not in self._graphs:
            p = self._path(student_id)
            if p.exists():
                self._graphs[student_id] = StudentGraph.from_dict(
                    json.loads(p.read_text(encoding="utf-8")), self.kg)
            else:
                self._graphs[student_id] = StudentGraph(student_id, self.kg)
        return self._graphs[student_id]

    def map_path(self, student_id: str) -> Optional[Path]:
        return (self.map_dir / self._path(student_id).with_suffix(".html").name) if self.map_dir else None

    def forget(self, student_id: str) -> None:
        """Erase a student's graph and map (right to erasure)."""
        with self._lock:
            self._graphs.pop(student_id, None)
            for p in (self._path(student_id), self.map_path(student_id)):
                if p is not None and p.exists():
                    p.unlink()

    def override(self, student_id: str, concept: str, level: str) -> None:
        """G21 Teacher override."""
        with self._lock:
            g = self.graph(student_id)
            g.set_override(concept, LEVELS.index(level))
            g.infer()
            self._save(g)

    def _save(self, g: StudentGraph) -> None:
        g.save(self._path(g.student_id))
        if self.map_dir:
            write_map(g, self.map_path(g.student_id))

    def _log(self, entries: List[Dict], student_id: str) -> None:
        if not self.review_log or not entries:
            return
        self.review_log.parent.mkdir(parents=True, exist_ok=True)
        with open(self.review_log, "a", encoding="utf-8") as fh:
            for e in entries:
                fh.write(json.dumps({"ts": time.time(), "student": student_id, **e}) + "\n")

    # ── Steps 1-13 ──────────────────────────────────────────────────────────
    def process(self, student_id: str, text: str, code: str = "", shown_text: str = "",
                session_id: Optional[str] = None, asked: str = "") -> Dict:
        """code: the code the prompt reasons about; it is run to check the prompt's claims.
        asked: the question (part) the prompt answers, when the tutor knows it."""
        text = (text or "").strip()
        result: Dict = {"student_id": student_id, "text": text, "prompt_gates": [],
                        "concepts": [], "degraded": [k for k, ok in models.available().items() if not ok]}
        review: List[Dict] = []

        with self._lock:
            g = self.graph(student_id)
            g.begin_turn(session_id)
            result["turn"] = g.turn

            # Step 1 — Layer 1 prompt gates (G1 Content, G2 Help-seeking)
            if help_seeking(text):
                result["prompt_gates"].append("help_seeking")
                return self._finish(g, result, review)
            too_little = content_gate(text, MIN_WORDS)

            # Steps 2-3 — clauses, concept linking (G3 Off-topic)
            clauses = split_clauses(text)
            hits = identify(text, self.kg, code=code, clauses=clauses, asked=asked)
            if too_little:                                       # G1: L0, no evidence, node unchanged
                result["prompt_gates"].append("content")
                for h in hits:
                    n = g.nodes.get(h.concept)
                    result["concepts"].append(self._report(g, h, None, 0, n, ["content"], "low"))
                return self._finish(g, result, review)
            if not hits:
                result["prompt_gates"].append("unlinked")
                review.append({"kind": "unlinked_prompt", "text": text})
                return self._finish(g, result, review)

            # Steps 4-7 — evidence with Layer 2-3 gates
            evidence, rv = collect(text, clauses, hits, self.kg, shown_text=shown_text, code=code, asked=asked)
            review.extend(rv)

            # Step 7b — the judge reads the answer against the concepts' has_level edge logic
            judged, extra = {}, []
            if judgelib.enabled():
                linked = [h.concept for h in hits]
                extra = judgelib.extra_concept(text, self.kg, set(linked))
                question = (asked or (shown_text or "").replace(code or "", "")).strip()
                facts = _run_facts(evidence)
                if asks_beyond(asked, code):
                    facts.append("THE PART ASKED GOES BEYOND THE GIVEN CODE: it asks about code, a change or an input "
                                 "that is not in the given code, so correct reasoning about it shows an L4 way.")
                jprompt = judgelib.build_prompt(text, question, code, facts, linked + extra)
                jout = judgelib.judge(jprompt)
                judged = judgelib.levels(jout, linked + extra)
                result["judge"] = {"concepts": linked + extra, "levels": {c: i["level"] for c, i in judged.items()},
                                   "unavailable": jout.get("unavailable")}

            # Steps 8-10 — prompt level (highest way shown), node update
            for h in hits:
                ev = evidence[h.concept]
                c = self.kg.concepts[h.concept]
                pw = walk(ev.checks, ev.held & c.boundary, ev.ways(), ev.l0_way)
                prompt_level = pw.level
                ev.reason = pw.stop_reason
                if ev.weak_link and prompt_level > 1:          # G5: E1 only
                    for e in ("E2", "E3", "E4"):
                        ev.drop(e)
                    prompt_level = 1
                    ev.reason = "weak link: L1 only"
                if (ev.mixed or (ev.held and pw.level > 1)) and prompt_level > 0:   # G12: one level down
                    ev.drop(f"E{prompt_level}")
                    prompt_level -= 1
                    ev.reason += "; one level down: a misconception is held next to correct evidence"
                ev.source = _source(ev, prompt_level)
                if judgelib.enabled():
                    prompt_level = _fuse(ev, prompt_level, judged.get(h.concept))
                ev.prompt_level = prompt_level
                if ev.empty:                                   # nothing shown: node untouched
                    ev.gate("no_evidence")
                    continue
                g.apply(ev, prompt_level)

            # Step 12 — inference rules
            g.infer()

            # Step 11 — confidence, then report
            for h in hits:
                ev = evidence[h.concept]
                n = g.nodes.get(h.concept)
                if ev.empty:
                    result["concepts"].append(self._report(g, h, ev, 0, n, list(ev.gates), "low"))
                    continue
                tier = 2
                gates = list(n.last_gates)
                if n.uncertain_toward is not None:
                    tier -= 1; gates.append("ambiguity")          # G15
                if ev.hedged:
                    tier -= 1; gates.append("hedge")              # G22
                blocked = g.prerequisite_blocked(h.concept) if n.level >= 3 else []
                if blocked:
                    tier -= 1; gates.append("prerequisite")       # G14
                if h.confidence < ID_CONF:
                    tier -= 1
                if ev.mixed:
                    tier = 0
                n.confidence = TIERS[max(0, tier)]
                result["concepts"].append(self._report(g, h, ev, ev.prompt_level, n, gates, n.confidence))

            # concepts only the judge graded (the answer-graph candidate): reported, not stored
            for cid in extra:
                item = judged.get(cid)
                if item is None or cid not in self.kg.concepts:
                    continue
                c = self.kg.concepts[cid]
                lv = item["level"]
                result["concepts"].append({
                    "concept": cid, "label": c.label, "chapter": c.chapter, "link_score": 0.0,
                    "link_confidence": 0.0, "prompt_level": lv, "assessed": True, "level": None,
                    "level_name": None, "provisional": True, "uncertain_toward": None,
                    "stop_reason": "judge only",
                    "prompt_reason": f"judge: {lv} {item.get('way', '')}: {item.get('why', '')}",
                    "confidence": "low", "gates": ["judge_only"], "checks": {}, "held": [], "refuted": [],
                    "evidence": [], "descriptor": None, "follow_up": None, "level_source": "judge",
                    "wrong_rule": lv == "L0", "judge": item})

            return self._finish(g, result, review)

    def _finish(self, g: StudentGraph, result: Dict, review: List[Dict]) -> Dict:
        """Step 13 — save the graph, redraw the map, log for link review."""
        self._log(review, g.student_id)
        self._save(g)
        result["summary"] = g.summary()
        result["map_path"] = str(self.map_path(g.student_id)) if self.map_dir else None
        return result

    def _report(self, g: StudentGraph, hit, ev, prompt_level: int, n, gates, confidence) -> Dict:
        c = self.kg.concepts[hit.concept]
        return {
            "concept": c.id, "label": c.label, "chapter": c.chapter,
            "link_score": hit.score, "link_confidence": hit.confidence,
            "prompt_level": LEVELS[prompt_level],
            # False when the concept was linked but not examined (G1, or no evidence
            # in the prompt): prompt_level L0 then means "not assessed", not prestructural
            "assessed": not ({"content", "no_evidence"} & set(gates)),
            "level": LEVELS[n.level] if n is not None and n.observed else None,
            "level_name": self.kg.level_names.get(LEVELS[n.level]) if n is not None and n.observed else None,
            "provisional": bool(n and n.provisional),
            "uncertain_toward": (LEVELS[n.uncertain_toward] if n and n.uncertain_toward is not None else None),
            "stop_reason": (n.stop_reason if n is not None and n.observed
                            else "no evidence for this concept in the message"),
            # the has_level way that sets this prompt's level
            "prompt_reason": (ev.reason if ev is not None and ev.reason else
                              "no evidence for this concept in the message"),
            "confidence": confidence,
            "level_source": ev.source if ev is not None else "",
            "wrong_rule": bool(ev and ev.wrong_rule),
            "judge": ev.judged if ev is not None else None,
            "gates": gates,
            "checks": ev.checks if ev else {},
            "held": sorted(ev.held) if ev else [],
            "refuted": sorted(ev.refuted) if ev else [],
            "evidence": [i.to_dict() for i in ev.items] if ev else [],
            "descriptor": c.ladder.get(LEVELS[n.level]) if n is not None and n.observed else None,
            # when the next level is uncertain, the graph's deciding question for it (ask it next)
            "follow_up": (c.deciding.get(LEVELS[n.uncertain_toward]) if n is not None and n.observed
                          and n.uncertain_toward is not None else None),
        }


# ── Step 7b helpers: the judge's input and the fusion ───────────────────────
_WEAK = ("nli", "relation cue", "similarity fact")


def _run_facts(evidence) -> List[str]:
    """What the code run decided about the answer's claims, given to the judge as facts."""
    facts = []
    for ev in evidence.values():
        for it in ev.items:
            st = it.statement
            if st.startswith("confirmed by the run"):
                facts.append(f"CORRECT ({it.clause[:80]!r}): {st}")
            elif it.check == "wrong_trace":
                facts.append(f"WRONG ({it.clause[:80]!r}): {st}")
            elif it.check == "held" and "match a run" in st:
                facts.append(f"MISCONCEPTION: {st}")
            elif it.check == "own_run":
                facts.append(f"STUDENT'S CODE RUN ON THE QUESTION'S DATA: {st}")
    return list(dict.fromkeys(facts))


def _source(ev, level: int) -> str:
    """What set this level: the code run, the question-form rules, the relation
    cue shortcut, a weak reader (NLI, a similarity-only fact match), or similarity (L1)."""
    if level == 0:
        if "inconsistent_trace" in (ev.reason or "") or any(
                i.check == "held" and "match a run" in i.statement for i in ev.items):
            return "run"
        return "nli misconception" if ev.held else "none"
    items = [i for i in ev.items if i.check == f"E{level}" and i.status == "met"]
    if not items:
        return "none"
    it = max(items, key=lambda i: i.score)
    st = it.statement
    if st.startswith("confirmed by the run"):
        return "run"
    if st.startswith("answers:") or st in ("fix for the given code", "change predicted"):
        return "question"
    if st.startswith("edge ") or st == "overall purpose":
        return "relation cue"
    if st.startswith(("L3 way:", "L4 way:", "refuted ", "diagnoses ")):
        return "nli way"
    if it.check == "E2":
        return "similarity fact"
    return "similarity"


def _fuse(ev, level: int, item: Optional[Dict]) -> int:
    """Each source decides what it is reliable for (all from the graph's edge logic):
    a wrong rule found by the code run or by the judge is L0; a level set by the code
    run or the question-form rules stands; a level set by a weak reader is the judge's."""
    jl = LEVELS.index(item["level"]) if item else None
    ev.judged = item
    if ev.source == "run" and level == 0:
        ev.wrong_rule = True
        return 0
    if jl == 0:
        ev.wrong_rule = True
        ev.source = "judge"
        ev.reason = f"L0 {item.get('way', '')} (judge): {item.get('why', '')}"
        return 0
    if ev.source.startswith(_WEAK) and jl is not None:
        ev.source = "judge"
        ev.reason = f"L{jl} {item.get('way', '')} (judge): {item.get('why', '')}"
        return jl
    return level


_ENGINE: Optional[LPPercptEngine] = None


def get_engine() -> LPPercptEngine:
    global _ENGINE
    if _ENGINE is None:
        _ENGINE = LPPercptEngine()
    return _ENGINE
