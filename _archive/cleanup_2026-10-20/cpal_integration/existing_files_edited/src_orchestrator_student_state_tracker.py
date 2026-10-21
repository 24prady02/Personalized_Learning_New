"""
Student State Tracker — Psychological Integration Update
=========================================================
Tracks the full THREE-GRAPH learner state in parallel:

  Cognitive Graph   → encoding_strength per concept node (9 nodes, 3 tiers)
  Progression Graph → developmental stage (7 stages) + ZPD boundary
  Psychological Graph → 9 motivation/belief nodes + SRL phase + imposter flag

All 12 psychological theories write to one of these three graphs.
The Language Channel classifies attribution, self-efficacy, and SRL
phase markers from every prompt before any graph update occurs.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import re
from pathlib import Path

# ─── Psychological Graph Node Definitions ────────────────────────────────────
PSYCH_NODES = {
    "high_anxiety":               {"valence": "NEGATIVE",  "theories": ["T10_Flow", "T08_SCT"]},
    "low_self_efficacy":          {"valence": "NEGATIVE",  "theories": ["T08_SCT", "T09_SRL"]},
    "fixed_attribution":          {"valence": "NEGATIVE",  "theories": ["T11_Attribution"]},
    "forethought_planning":       {"valence": "NEUTRAL+",  "theories": ["T09_SRL"]},
    "performance_monitoring":     {"valence": "NEUTRAL+",  "theories": ["T09_SRL"]},
    "self_reflection_evaluation": {"valence": "NEUTRAL+",  "theories": ["T09_SRL", "T12_Imposter"]},
    "flow_state":                 {"valence": "POSITIVE",  "theories": ["T10_Flow"]},
    "growth_self_efficacy":       {"valence": "POSITIVE",  "theories": ["T08_SCT"]},
    "adaptive_attribution":       {"valence": "POSITIVE",  "theories": ["T11_Attribution"]},
}

PROGRESSION_STAGES = {
    1: "Observation", "2a": "Guided_Modification", "2b": "Scaffolded_Practice",
    3: "Coached_Problem_Solving", "4a": "Independent_Solution",
    "4b": "Transfer_Application", 5: "Expert_Autonomy",
}

# Java CSCI 1301 concept nodes — 20 concepts across 5 experience weeks
# Tier maps to week group: 1=wk1-2, 2=wk3-4, 3=wk5
CONCEPT_NODES = {
    # ── Week 1 ──────────────────────────────────────────────────────────────
    "type_mismatch":         {"tier": 1, "week": 1, "error": "compile",  "dual_coding": "verbal+visual", "load": "low",      "java_concept": "Type system, concatenation"},
    "infinite_loop":         {"tier": 1, "week": 1, "error": "logic",    "dual_coding": "visual_dominant","load": "med",      "java_concept": "Loop update step"},
    # ── Week 2 ──────────────────────────────────────────────────────────────
    "null_pointer":          {"tier": 1, "week": 2, "error": "runtime",  "dual_coding": "visual_dominant","load": "med_high", "java_concept": "References, object creation"},
    "string_equality":       {"tier": 1, "week": 2, "error": "logic",    "dual_coding": "verbal+visual", "load": "med_high", "java_concept": "Reference equality"},
    "variable_scope":        {"tier": 1, "week": 2, "error": "compile",  "dual_coding": "verbal_dominant","load": "med",      "java_concept": "Block scope, braces"},
    "assignment_vs_compare": {"tier": 1, "week": 2, "error": "compile",  "dual_coding": "verbal_dominant","load": "low",      "java_concept": "Assignment vs comparison"},
    "integer_division":      {"tier": 1, "week": 2, "error": "logic",    "dual_coding": "verbal+visual", "load": "med",      "java_concept": "Type promotion, casting"},
    "scanner_buffer":        {"tier": 1, "week": 2, "error": "logic",    "dual_coding": "verbal_dominant","load": "med_high", "java_concept": "Input buffer"},
    # ── Week 3 ──────────────────────────────────────────────────────────────
    "array_index":           {"tier": 2, "week": 3, "error": "runtime",  "dual_coding": "visual_dominant","load": "med_high", "java_concept": "Zero-indexing, loops"},
    "missing_return":        {"tier": 2, "week": 3, "error": "compile",  "dual_coding": "verbal_dominant","load": "med",      "java_concept": "Control flow, methods"},
    "array_not_allocated":   {"tier": 2, "week": 3, "error": "compile",  "dual_coding": "visual_dominant","load": "med_high", "java_concept": "Array creation, new keyword"},
    "boolean_operators":     {"tier": 2, "week": 3, "error": "logic",    "dual_coding": "verbal+visual", "load": "med",      "java_concept": "AND vs OR logic"},
    "sentinel_loop":         {"tier": 2, "week": 3, "error": "logic",    "dual_coding": "visual_dominant","load": "med_high", "java_concept": "Priming read pattern"},
    "unreachable_code":      {"tier": 2, "week": 3, "error": "compile",  "dual_coding": "verbal_dominant","load": "med",      "java_concept": "Control flow analysis"},
    "string_immutability":   {"tier": 2, "week": 3, "error": "logic",    "dual_coding": "verbal+visual", "load": "med_high", "java_concept": "Immutable objects"},
    # ── Week 4 ──────────────────────────────────────────────────────────────
    "no_default_constructor":{"tier": 2, "week": 4, "error": "compile",  "dual_coding": "verbal+visual", "load": "high",     "java_concept": "Constructors, OOP"},
    "static_vs_instance":    {"tier": 2, "week": 4, "error": "compile",  "dual_coding": "verbal_dominant","load": "high",     "java_concept": "Static context, objects"},
    "foreach_no_modify":     {"tier": 2, "week": 4, "error": "logic",    "dual_coding": "visual_dominant","load": "high",     "java_concept": "Pass-by-value, iteration"},
    "overloading":           {"tier": 2, "week": 4, "error": "logic",    "dual_coding": "verbal_dominant","load": "high",     "java_concept": "Method selection"},
    # ── Week 5 ──────────────────────────────────────────────────────────────
    "generics_primitives":   {"tier": 3, "week": 5, "error": "compile",  "dual_coding": "verbal+visual", "load": "very_high","java_concept": "Generics, wrapper classes"},
}

# Keyword patterns for each concept — used by LP classifier for initial matching
CONCEPT_KEYWORDS = {
    "type_mismatch":         ["int", "String", "concatenat", "type", "cannot convert", "+ "", ""+"],
    "infinite_loop":         ["infinite", "forever", "never stop", "while", "loop", "update", "increment"],
    "null_pointer":          ["null", "NullPointer", "NPE", "reference", "not initialized", "object"],
    "string_equality":       ["==", ".equals", "reference", "content", "same string", "equal string"],
    "variable_scope":        ["scope", "not defined", "cannot find symbol", "block", "local", "global"],
    "assignment_vs_compare": ["= vs ==", "assign", "compare", "boolean", "condition", "if statement"],
    "integer_division":      ["division", "integer", "truncat", "cast", "double", "float", "decimal"],
    "scanner_buffer":        ["nextLine", "nextInt", "scanner", "buffer", "newline", "input"],
    "array_index":           ["ArrayIndex", "index", "bounds", "zero", "length", "off by one"],
    "missing_return":        ["return", "missing", "control flow", "all paths", "method"],
    "array_not_allocated":   ["new", "array", "allocat", "NullPointer", "declare", "[]"],
    "boolean_operators":     ["&&", "||", "AND", "OR", "boolean", "condition", "both", "either"],
    "sentinel_loop":         ["sentinel", "priming", "read", "do-while", "while", "off by one"],
    "unreachable_code":      ["unreachable", "dead code", "after return", "never executes"],
    "string_immutability":   ["immutable", "String", "new String", "concat", "replace", "+="],
    "no_default_constructor":["constructor", "no args", "default", "super", "OOP", "class"],
    "static_vs_instance":    ["static", "instance", "non-static", "this", "class method", "object method"],
    "foreach_no_modify":     ["for each", "forEach", "cannot modify", "enhanced for", "copy", "pass by value"],
    "overloading":           ["overload", "method", "same name", "parameter", "signature"],
    "generics_primitives":   ["ArrayList", "int", "Integer", "wrapper", "generic", "primitive", "<int>"],
}


class LanguageChannelAnalyser:
    """
    Language Channel of the Prompt Analysis Engine.
    Detects: attribution type, self-efficacy, SRL phase, imposter signals, anxiety.
    All 12 theories (T08-T12) write to the Psychological Graph through this channel.
    """

    _PATTERNS = {
        "fixed_attr": [
            r"\bi('m| am) (just |always |never )?(bad|terrible|hopeless|awful) at",
            r"\b(always|never) (get|understand|figure|know)",
            r"\bi('m| am) not (good enough|cut out for|meant for)",
            r"\b(can't|cannot) (do|learn|understand) (this|it|coding|programming)",
            r"\bstupid( mistake| me)",
            r"\b(it's|it is) (just |always )?(too hard|impossible)",
        ],
        "adaptive_attr": [
            r"\b(let me|i('ll| will)) try (a |another |different )?approach",
            r"\b(next time|from now on) i('ll| will)",
            r"\bi (need to|should) (study|practice|review|learn) (more|better|this)",
            r"\b(my approach|my strategy) (was|is) wrong",
        ],
        "low_efficacy": [
            r"\bi (don't|do not) (think|believe) (i|i'll|i can)",
            r"\bi('m| am) (totally|completely) (lost|confused|stuck)",
            r"\bno (idea|clue) (what|how|why) (to|i should)",
            r"\bwhy (can't|don't) i (get|understand) (this|it)",
        ],
        "growth_efficacy": [
            r"\bi (think|believe) i (see|understand|get|have) (it|this|now)",
            r"\b(that makes|makes a lot of) sense( now)?",
            r"\bnow i (understand|get|see|know)",
            r"\bi (can|could) (do|try|figure) (this|it) out",
        ],
        "forethought": [
            r"\b(before|first)(,| i| let me) (plan|think|figure|understand)",
            r"\bmy (plan|approach|strategy) (is|will be)",
            r"\bi('m| am) going to (first|start by|begin with)",
        ],
        "monitoring": [
            r"\bi('m| am) trying|i tried|i ran|i tested",
            r"\b(it's|it is) (still |)not working|keeps? (giving|throwing|failing)",
            r"\bwhen i (run|execute|call) (it|this|the code)",
        ],
        "reflection": [
            r"\bi (got|get) (it|the right answer) but (i'm not sure|i don't understand) why",
            r"\b(i think|maybe) i (just got|was) lucky",
            r"\bit (works|worked) but i('m| am) not (sure|confident)",
            r"\b(looking back|in hindsight|after thinking)",
        ],
        "imposter": [
            r"\b(i got|i was) (just )?lucky",
            r"\b(they('ll| will)|someone will) (find out|know|realize) (i'm|that i'm)",
            r"\bi don't (deserve|belong|know why i)",
            r"\bit (was|is) an (accident|fluke|coincidence)",
        ],
        "high_anxiety": [
            r"\bi('m| am) (panicking|freaking out|stressed|overwhelmed|scared)",
            r"\b(deadline|exam|test) (is|in) (tomorrow|today|soon)",
            r"\b(please|urgent|asap) help",
            r"\bwhat do i do",
        ],
    }

    def __init__(self):
        flags = re.IGNORECASE
        self._compiled = {
            k: [re.compile(p, flags) for p in pats]
            for k, pats in self._PATTERNS.items()
        }

    def _score(self, text: str, key: str) -> int:
        return sum(1 for p in self._compiled[key] if p.search(text))

    def analyse(self, text: str) -> Dict:
        if not text:
            return self._neutral()
        t = text.lower()

        fixed_s    = self._score(t, "fixed_attr")
        adaptive_s = self._score(t, "adaptive_attr")
        low_s      = self._score(t, "low_efficacy")
        growth_s   = self._score(t, "growth_efficacy")
        f_s        = self._score(t, "forethought")
        m_s        = self._score(t, "monitoring")
        r_s        = self._score(t, "reflection")
        imp_s      = self._score(t, "imposter")
        anx_s      = self._score(t, "high_anxiety")

        attribution   = "fixed" if fixed_s > 0 and fixed_s >= adaptive_s else ("adaptive" if adaptive_s > 0 else "neutral")
        self_efficacy = "low"   if low_s > 0   and low_s   >= growth_s   else ("growth"   if growth_s > 0   else "neutral")
        max_srl = max(f_s, m_s, r_s)
        srl_phase = "unknown" if max_srl == 0 else (
            "forethought" if f_s == max_srl else ("monitoring" if m_s == max_srl else "reflection")
        )
        imposter_signal = imp_s > 0 or (srl_phase == "reflection" and self_efficacy != "growth")
        high_anxiety    = anx_s > 0

        nodes = []
        if attribution   == "fixed":       nodes.append("fixed_attribution")
        elif attribution == "adaptive":    nodes.append("adaptive_attribution")
        if self_efficacy == "low":         nodes.append("low_self_efficacy")
        elif self_efficacy == "growth":    nodes.append("growth_self_efficacy")
        if high_anxiety:                   nodes.append("high_anxiety")
        if srl_phase == "forethought":     nodes.append("forethought_planning")
        elif srl_phase == "monitoring":    nodes.append("performance_monitoring")
        elif srl_phase == "reflection":    nodes.append("self_reflection_evaluation")
        if (not high_anxiety and self_efficacy == "growth"
                and attribution in ("adaptive", "neutral")):
            nodes.append("flow_state")

        return {
            "attribution": attribution, "self_efficacy": self_efficacy,
            "srl_phase": srl_phase, "imposter_signal": imposter_signal,
            "high_anxiety": high_anxiety, "psych_nodes_activated": nodes,
            "fixed_score": fixed_s, "adaptive_score": adaptive_s,
            "low_efficacy_score": low_s, "growth_efficacy_score": growth_s,
        }

    def _neutral(self) -> Dict:
        return {
            "attribution": "neutral", "self_efficacy": "neutral",
            "srl_phase": "unknown",   "imposter_signal": False,
            "high_anxiety": False,    "psych_nodes_activated": [],
            "fixed_score": 0, "adaptive_score": 0,
            "low_efficacy_score": 0, "growth_efficacy_score": 0,
        }


class StructureChannelAnalyser:
    """
    Structure Channel — infers Progression Graph stage and ZPD status.
    Operationalises T04 (Constructivism), T05 (ZPD), T06 (Apprenticeship), T07 (Situated Learning).
    """

    _STAGE_PATTERNS = {
        5:    [r"\b(design|architect|tradeoff|architectural)\b",
               r"\bwhy (do|does|would|should) (we|you|one) (use|prefer|choose|implement)"],
        "4b": [r"\b(in my|for my|for a real|for production)\b",
               r"\b(project|app|application|website|system)\b"],
        "4a": [r"\b(i (solved|fixed|got) it|it works)\b.*\b(but|now|and)\b",
               r"\bhow (can|do) i (improve|optimize|clean|refactor)"],
        3:    [r"\b(my approach|my idea|my plan|my logic|my solution) (is|was|would be)\b",
               r"\b(is|am) i (on the right|in the right) (track|direction|path)\b",
               r"\b(does|do) (this|my approach|my solution) (look|seem|make sense)\b"],
        "2b": [r"\b(i tried|i attempted|here('s| is) my attempt)\b",
               r"\b(it's|it is) (still |)not working|keeps? (giving|throwing|failing)\b"],
        "2a": [r"\bi (modified|changed|edited|added|removed) (the|your|this)\b"],
        1:    [r"\b(can you|please|could you) (write|give me|provide|show me) (the|a) (code|solution|answer)\b",
               r"\bi have no (idea|clue)|i don't know (where|what|how) to (start|begin)"],
    }

    def __init__(self):
        flags = re.IGNORECASE
        self._compiled = {
            k: [re.compile(p, flags) for p in pats]
            for k, pats in self._STAGE_PATTERNS.items()
        }

    def _score(self, text: str, key) -> int:
        return sum(1 for p in self._compiled[key] if p.search(text))

    def analyse(self, text: str, has_code: bool = False, has_error: bool = False) -> Dict:
        if not text:
            return {"stage": 1, "zpd_status": "overwhelmed", "has_attempt": False, "has_realworld_framing": False}
        t = text.lower()
        has_attempt = has_code or any(kw in t for kw in ["i tried", "i wrote", "my code", "here's what"])
        for stage_key in [5, "4b", "4a", 3, "2b", "2a", 1]:
            if self._score(t, stage_key) > 0:
                stage = stage_key
                break
        else:
            stage = "2a" if (has_code and not any(kw in t for kw in ["can you write", "give me", "show me the"])) else 1
        return {
            "stage": stage,
            "zpd_status": self._zpd(stage),
            "has_attempt": has_attempt,
            "has_realworld_framing": self._score(t, "4b") > 0,
        }

    def _zpd(self, stage) -> str:
        if stage in (1, "2a"):   return "overwhelmed"
        if stage in ("2b", 3):   return "at_boundary"
        if stage in ("4a","4b"): return "at_boundary"
        return "internalized"


class ContentChannelAnalyser:
    """
    Content Channel — infers encoding strength and dual coding profile.
    Operationalises T01 (IPT), T02 (Dual Coding), T03 (Elaboration).
    """

    _DEEP_PATTERNS = [
        r"\b(because|therefore|which means|so that|in order to|the reason|that's why)\b",
        r"\b(compared to|unlike|similar to|the difference between|vs\.?)\b",
        r"\b(the (problem|issue|bug) is (that|because|when))\b",
    ]
    _SURFACE_PATTERNS = [
        r"\b(it (doesn't|don't|won't|can't) work)\b",
        r"\b(why (is|does|do|won't|can't|doesn't) (it|this))\b",
        r"\b(help|fix|error|broken|wrong)\b",
    ]
    _DUAL_PATTERNS = [r"```|`[^`]+`", r"\b(diagram|picture|visual|chart|example|output)\b"]
    _CROSS_PATTERNS = [r"\b(using|with|inside|together with|alongside)\b"]

    def __init__(self):
        flags = re.IGNORECASE
        self._deep    = [re.compile(p, flags) for p in self._DEEP_PATTERNS]
        self._surface = [re.compile(p, flags) for p in self._SURFACE_PATTERNS]
        self._dual    = [re.compile(p, flags) for p in self._DUAL_PATTERNS]
        self._cross   = [re.compile(p, flags) for p in self._CROSS_PATTERNS]

    def _score(self, text: str, patterns) -> int:
        return sum(1 for p in patterns if p.search(text))

    def analyse(self, text: str, has_code: bool = False) -> Dict:
        if not text:
            return {"encoding_strength": "surface", "dual_coding": "verbal_only", "elaboration": False}
        deep_s    = self._score(text, self._deep)
        surface_s = self._score(text, self._surface)
        dual_s    = self._score(text, self._dual) + (1 if has_code else 0)
        cross_s   = self._score(text, self._cross)

        if deep_s >= 2 and cross_s > 0:      enc = "deep"
        elif deep_s >= 1:                     enc = "solid"
        elif surface_s > deep_s:              enc = "surface"
        else:                                 enc = "partial"

        dual = "dual" if dual_s >= 2 else ("verbal+code" if dual_s == 1 else "verbal_only")
        return {
            "encoding_strength": enc, "encoding_score": deep_s - surface_s,
            "dual_coding": dual, "elaboration": cross_s > 0,
            "deep_score": deep_s, "surface_score": surface_s,
        }


class InterventionSelector:
    """
    Applies the 8-intervention decision logic from the reference document.
    Fixed Attribution and Imposter Flag are NON-NEGOTIABLE gates that must
    be cleared BEFORE any instructional advance.
    """

    def select(self, cognitive: Dict, progression: Dict, psychological: Dict, bkt_mastery: float) -> Dict:
        enc   = cognitive.get("encoding_strength", "surface")
        stage = progression.get("stage", 1)
        attr  = psychological.get("attribution", "neutral")
        eff   = psychological.get("self_efficacy", "neutral")
        imp   = psychological.get("imposter_signal", False)
        anx   = psychological.get("high_anxiety", False)

        # GATE 1 — Non-negotiable: Attribution or Imposter
        if attr == "fixed" or imp:
            return {"type": "attribution_reframe", "priority": 1.0, "gate_triggered": True,
                    "rationale": f"Fixed Attribution ({attr=='fixed'}) OR Imposter ({imp}) — must clear before advance.",
                    "blocks_advance": True}

        # GATE 2 — Crisis de-escalation
        if stage == 1 and (anx or eff == "low"):
            return {"type": "reduce_challenge", "priority": 0.95, "gate_triggered": True,
                    "rationale": "Stage 1 + Anxiety/Low Efficacy — overwhelmed student.", "blocks_advance": False}

        # Mastery surface (high mastery + imposter-like low efficacy)
        if enc in ("solid", "deep") and eff == "low":
            return {"type": "mastery_surface", "priority": 0.90, "gate_triggered": False,
                    "rationale": "High encoding + Low Efficacy: surface prior successes.", "blocks_advance": False}

        # All positive → validate and advance (checked BEFORE generic growth shortcut)
        if (enc in ("solid", "deep")
                and stage in ("4a", "4b", 5)
                and eff == "growth"
                and attr == "adaptive"):
            return {"type": "validate_and_advance", "priority": 0.87, "gate_triggered": False,
                    "rationale": "All three graphs positive — confirm mastery and advance.",
                    "blocks_advance": False}

        # Growth efficacy + Stage 4+ → increase challenge even without deep encoding
        # (student solved it independently — T08 SCT signals readiness)
        if eff == "growth" and stage in ("4a", "4b", 5):
            return {"type": "increase_challenge", "priority": 0.72, "gate_triggered": False,
                    "rationale": "Growth Efficacy + Stage 4+: student solved independently, advance challenge.",
                    "blocks_advance": False}

        # Worked example
        if enc == "surface" and stage in (1, "2a", "2b"):
            return {"type": "worked_example", "priority": 0.75, "gate_triggered": False,
                    "rationale": "Surface encoding + early stage: dual-coded walkthrough.", "blocks_advance": False}

        # Socratic prompt
        if enc == "partial" and stage in ("2b", 3):
            return {"type": "socratic_prompt", "priority": 0.70, "gate_triggered": False,
                    "rationale": "Partial encoding + scaffold-stage: targeted questioning.", "blocks_advance": False}

        # Transfer task
        if enc == "deep" and stage in ("4a","4b",5):
            return {"type": "transfer_task", "priority": 0.80, "gate_triggered": False,
                    "rationale": "Deep encoding + Stage 4+: novel real-world application.", "blocks_advance": False}

        # Increase challenge
        if enc in ("solid","deep") and stage == 3 and eff in ("growth","neutral"):
            return {"type": "increase_challenge", "priority": 0.70, "gate_triggered": False,
                    "rationale": "Solid + Stage 3 + positive efficacy: advance challenge.", "blocks_advance": False}

        # Default
        return {"type": "worked_example", "priority": 0.50, "gate_triggered": False,
                "rationale": "Default: scaffolded worked example.", "blocks_advance": False}


class StudentStateTracker:
    """
    Full three-graph student state machine.

    Cognitive Graph    → encoding_strength per concept node (9 nodes, 3 tiers)
    Progression Graph  → developmental stage (7 stages) + ZPD + scaffold_level
    Psychological Graph → 9 motivation/belief nodes + SRL + imposter_flag

    Primary entry point: analyse_prompt() — call this FIRST on every message
    before selecting an intervention.
    """

    def __init__(self, config: Dict):
        self.config = config
        self.student_states: Dict[str, Dict] = {}
        self.state_file = Path(
            config.get("student_state", {}).get("state_file", "data/student_states.json")
        )
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

        self.language_channel      = LanguageChannelAnalyser()
        self.structure_channel     = StructureChannelAnalyser()
        self.content_channel       = ContentChannelAnalyser()
        self.intervention_selector = InterventionSelector()

        self._load_states()

    def _load_states(self):
        if self.state_file.exists():
            try:
                with open(self.state_file, "r") as f:
                    self.student_states = json.load(f)
            except Exception as e:
                print(f"[WARN] Failed to load student states: {e}")

    def _save_states(self):
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.student_states, f, indent=2, default=str)
        except Exception as e:
            print(f"[WARN] Failed to save student states: {e}")

    def get_student_state(self, student_id: str) -> Dict:
        if student_id not in self.student_states:
            self.student_states[student_id] = self._init_state(student_id)
        return self.student_states[student_id]

    def _init_state(self, student_id: str) -> Dict:
        concept_nodes = {
            c: {"mastery": 0.30, "encoding": "surface", "dual_coding": "verbal_only",
                "elaboration": False, "encoding_history": [],
                # CPAL Stage 5 — per-concept LP state. See
                # mental_models_cpal_methodology.docx Part 4 (lp_diagnostic
                # object → persistence). Defaults match a fresh L1 student
                # with no history.
                "lp_state": {
                    "lp_level":             "L1",
                    "lp_streak":            0,
                    "logical_step":         False,
                    "logical_step_detail":  False,
                    "lp_history":           [],    # list of {ts, level, delta}
                    "last_intervention":    None,
                    "delta_lp_last":        0,
                    "session_state_vectors": [],   # historical 12-d vectors
                }}
            for c in CONCEPT_NODES
        }
        return {
            "student_id": student_id,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "cognitive_graph": {"concept_nodes": concept_nodes, "active_concepts": []},
            "progression_graph": {
                "stage": 1, "zpd_status": "overwhelmed",
                "scaffold_level": 5, "has_attempt": False, "stage_history": [],
            },
            "psychological_graph": {
                "active_nodes": [], "attribution": "neutral", "self_efficacy": "neutral",
                "srl_phase": "unknown", "imposter_flag": False, "high_anxiety": False,
                "flow_state": False, "psych_history": [],
            },
            "recommended_intervention": {},
            # legacy compatibility
            "cognitive_state": {"current_state": "engaged", "confidence": 0.5, "state_history": []},
            "knowledge_state": {"concept_mastery": {}, "mastery_history": [], "last_updated": None},
            "conversation_history": [],
            "session_count": 0,
            "total_interactions": 0,
        }

    # ── Primary Entry Point ──────────────────────────────────────────────────

    def analyse_prompt(self, student_id: str, session_data: Dict) -> Dict:
        """
        Run all three channels simultaneously on a student prompt.
        Call this BEFORE selecting an intervention.
        Returns full three-graph analysis + recommended_intervention.
        """
        state     = self.get_student_state(student_id)
        question  = session_data.get("question", "")
        code      = session_data.get("code", "")
        error     = session_data.get("error_message", "")
        has_code  = bool(code and code.strip())
        has_error = bool(error and error.strip())
        full_text = f"{question} {error}".strip()

        lang   = self.language_channel.analyse(full_text)
        struct = self.structure_channel.analyse(full_text, has_code=has_code, has_error=has_error)
        cont   = self.content_channel.analyse(full_text, has_code=has_code)

        # ── Psychological Graph update ────────────────────────────────────
        pg = state["psychological_graph"]
        pg["attribution"]   = lang["attribution"]
        pg["self_efficacy"] = lang["self_efficacy"]
        pg["srl_phase"]     = lang["srl_phase"]
        pg["high_anxiety"]  = lang["high_anxiety"]
        pg["flow_state"]    = "flow_state" in lang["psych_nodes_activated"]

        if lang["imposter_signal"]:
            pg["imposter_flag"] = True
        avg_m = self._avg_mastery(state)
        if (pg["imposter_flag"]
                and lang["self_efficacy"] == "growth"
                and lang["attribution"] == "adaptive"
                and avg_m > 0.70):
            pg["imposter_flag"] = False
            print(f"[PsychGraph] Imposter flag cleared for {student_id}")

        pg["active_nodes"] = lang["psych_nodes_activated"]
        pg["psych_history"].append({
            "timestamp": datetime.now().isoformat(),
            "nodes": lang["psych_nodes_activated"],
            "attribution": lang["attribution"],
            "srl_phase": lang["srl_phase"],
            "imposter": pg["imposter_flag"],
        })
        if len(pg["psych_history"]) > 100:
            pg["psych_history"] = pg["psych_history"][-100:]

        # ── Progression Graph update ──────────────────────────────────────
        prg = state["progression_graph"]
        new_stage = struct["stage"]
        if self._stage_int(new_stage) >= self._stage_int(prg["stage"]):
            prg["stage"]      = new_stage
            prg["zpd_status"] = struct["zpd_status"]
        prg["has_attempt"]    = struct["has_attempt"]
        prg["scaffold_level"] = self._stage_to_scaffold(new_stage)
        prg["stage_history"].append({
            "timestamp": datetime.now().isoformat(), "stage": new_stage, "zpd": struct["zpd_status"]
        })
        if len(prg["stage_history"]) > 100:
            prg["stage_history"] = prg["stage_history"][-100:]

        # ── Cognitive Graph update ────────────────────────────────────────
        concept = session_data.get("concept") or self._infer_concept(session_data)
        cg = state["cognitive_graph"]
        if concept and concept in cg["concept_nodes"]:
            node = cg["concept_nodes"][concept]
            node["encoding"]    = cont["encoding_strength"]
            node["dual_coding"] = cont["dual_coding"]
            node["elaboration"] = cont["elaboration"]
            node["encoding_history"].append({
                "timestamp": datetime.now().isoformat(), "encoding": cont["encoding_strength"]
            })
            if len(node["encoding_history"]) > 50:
                node["encoding_history"] = node["encoding_history"][-50:]
        cg["active_concepts"] = [concept] if concept else []

        # ── Select Intervention ───────────────────────────────────────────
        intervention = self.intervention_selector.select(
            cognitive=cont, progression=struct, psychological=lang, bkt_mastery=avg_m
        )
        state["recommended_intervention"] = intervention
        state["last_updated"] = datetime.now().isoformat()
        self._save_states()

        print(f"[StateTracker] {student_id}: stage={prg['stage']}, "
              f"enc={cont['encoding_strength']}, attr={lang['attribution']}, "
              f"imp={pg['imposter_flag']}, -> {intervention['type']}")

        return {
            "language_channel": lang, "structure_channel": struct, "content_channel": cont,
            "cognitive_graph": state["cognitive_graph"],
            "progression_graph": state["progression_graph"],
            "psychological_graph": state["psychological_graph"],
            "recommended_intervention": intervention,
            "concept": concept, "avg_mastery": avg_m,
        }

    # ── BKT Mastery Update ───────────────────────────────────────────────────

    def update_from_session(self, student_id: str, session_data: Dict,
                            cognitive_state: str, concepts_identified: List[str],
                            code_correctness: float, response_quality: float):
        state = self.get_student_state(student_id)
        BKT_P_T, BKT_P_S, BKT_P_G = 0.20, 0.10, 0.25

        cg = state["cognitive_graph"]
        for concept in concepts_identified:
            if concept not in cg["concept_nodes"]:
                cg["concept_nodes"][concept] = {
                    "mastery": 0.30, "encoding": "surface",
                    "dual_coding": "verbal_only", "elaboration": False, "encoding_history": []
                }
            node = cg["concept_nodes"][concept]
            p_l = node["mastery"]
            if code_correctness > 0.5:
                p_ev = p_l * (1 - BKT_P_S) + (1 - p_l) * BKT_P_G
                p_l_new = (p_l * (1 - BKT_P_S)) / max(p_ev, 1e-9)
            else:
                p_ev = p_l * BKT_P_S + (1 - p_l) * (1 - BKT_P_G)
                p_l_new = (p_l * BKT_P_S) / max(p_ev, 1e-9)
            node["mastery"] = float(min(1.0, max(0.0, p_l_new + (1 - p_l_new) * BKT_P_T)))

        # Legacy
        ks = state["knowledge_state"]
        for c in concepts_identified:
            ks["concept_mastery"][c] = cg["concept_nodes"].get(c, {}).get("mastery", 0.5)
        overall = self._avg_mastery(state)
        ks["mastery_history"].append({
            "timestamp": datetime.now().isoformat(),
            "overall_mastery": overall, "concepts_tested": concepts_identified
        })
        if len(ks["mastery_history"]) > 100:
            ks["mastery_history"] = ks["mastery_history"][-100:]
        ks["last_updated"] = datetime.now().isoformat()

        state["cognitive_state"]["current_state"] = cognitive_state
        state["cognitive_state"]["state_history"].append({
            "state": cognitive_state, "timestamp": datetime.now().isoformat()
        })
        if len(state["cognitive_state"]["state_history"]) > 50:
            state["cognitive_state"]["state_history"] = state["cognitive_state"]["state_history"][-50:]

        state["conversation_history"].append({
            "timestamp": datetime.now().isoformat(),
            "question": session_data.get("question", ""),
            "code": session_data.get("code", "")[:200],
            "error": session_data.get("error_message", ""),
            "cognitive_state": cognitive_state,
            "concepts": concepts_identified,
            "correctness": code_correctness,
        })
        if len(state["conversation_history"]) > 100:
            state["conversation_history"] = state["conversation_history"][-100:]

        state["session_count"]      += 1
        state["total_interactions"] += 1
        state["last_updated"]        = datetime.now().isoformat()
        self._save_states()

    # ── Public Getters ───────────────────────────────────────────────────────

    def get_cognitive_state(self, student_id: str) -> Dict:
        return self.get_student_state(student_id)["cognitive_state"]

    def get_knowledge_state(self, student_id: str) -> Dict:
        return self.get_student_state(student_id)["knowledge_state"]

    def get_psychological_graph(self, student_id: str) -> Dict:
        return self.get_student_state(student_id)["psychological_graph"]

    def get_progression_graph(self, student_id: str) -> Dict:
        return self.get_student_state(student_id)["progression_graph"]

    def get_cognitive_graph(self, student_id: str) -> Dict:
        return self.get_student_state(student_id)["cognitive_graph"]

    def get_recommended_intervention(self, student_id: str) -> Dict:
        return self.get_student_state(student_id).get("recommended_intervention", {})

    def is_intervention_gated(self, student_id: str) -> bool:
        pg = self.get_psychological_graph(student_id)
        return pg["attribution"] == "fixed" or pg["imposter_flag"]

    def get_conversation_history(self, student_id: str, limit: int = 10) -> List[Dict]:
        return self.get_student_state(student_id)["conversation_history"][-limit:]

    def get_learning_trajectory(self, student_id: str) -> Dict:
        history = self.get_student_state(student_id)["knowledge_state"]["mastery_history"]
        if len(history) < 2:
            return {"trend": "insufficient_data", "slope": 0.0}
        recent = history[-5:] if len(history) >= 5 else history
        older  = history[:5]  if len(history) >= 10 else history[: len(history) // 2]
        r_avg  = sum(h["overall_mastery"] for h in recent) / len(recent)
        o_avg  = sum(h["overall_mastery"] for h in older) / len(older) if older else r_avg
        slope  = r_avg - o_avg
        return {"trend": "improving" if slope > 0.1 else ("declining" if slope < -0.1 else "stable"),
                "slope": slope, "current_mastery": r_avg, "previous_mastery": o_avg,
                "data_points": len(history)}

    # ── LP State Accessors (CPAL Stage 5 — persistence across sessions) ─────
    # These are the Stage 5 hooks the methodology document calls out.
    # process_session() loads LP state BEFORE running Stage 1 so the
    # plateau rule has a lp_streak to read; _learn_from_session() persists
    # the updated state after Stage 4 computes delta_lp.

    _DEFAULT_LP_STATE = {
        "lp_level":              "L1",
        "lp_streak":             0,
        "logical_step":          False,
        "logical_step_detail":   False,
        "lp_history":            [],
        "last_intervention":     None,
        "delta_lp_last":         0,
        "session_state_vectors": [],
    }

    def _ensure_lp_state(self, node: Dict) -> Dict:
        """Back-compat: old saved states don't have an lp_state block.
        Create one on first access so loads never KeyError."""
        if "lp_state" not in node:
            # copy defaults — don't share the list references
            node["lp_state"] = {
                **self._DEFAULT_LP_STATE,
                "lp_history":            [],
                "session_state_vectors": [],
            }
        return node["lp_state"]

    def load_lp_state(self, student_id: str, concept: str) -> Dict:
        """Return this student's persisted LP state for a concept.

        If the concept isn't in the cognitive graph yet, create a fresh
        node with default LP state and return that. Callers should treat
        the returned dict as read-only; use persist_lp_state to write.
        """
        state = self.get_student_state(student_id)
        nodes = state["cognitive_graph"]["concept_nodes"]
        if concept not in nodes:
            nodes[concept] = {
                "mastery": 0.30, "encoding": "surface",
                "dual_coding": "verbal_only", "elaboration": False,
                "encoding_history": [],
                "lp_state": {
                    **self._DEFAULT_LP_STATE,
                    "lp_history":            [],
                    "session_state_vectors": [],
                },
            }
        return self._ensure_lp_state(nodes[concept])

    def persist_lp_state(self, student_id: str, concept: str,
                         new_lp_level: str,
                         logical_step: bool,
                         logical_step_detail: bool,
                         delta_lp: int,
                         last_intervention: Optional[str],
                         session_state_vector: Optional[List[float]] = None,
                         max_history: int = 200) -> None:
        """Write updated LP state after a Stage 4 post-reply assessment.

        Streak rule (matches LPDiagnostician.diagnose convention): any
        level change — advance or regress — resets the streak to 0. A
        session at the same level as the previous one increments the
        streak. So if a student is at L2 and stays at L2 across three
        sessions, the streaks are 0 → 1 → 2; if they advance to L3 on
        session 4, the streak resets to 0.
        """
        state = self.get_student_state(student_id)
        nodes = state["cognitive_graph"]["concept_nodes"]
        if concept not in nodes:
            # Pre-populate the node shape if Stage 1 created a diagnosis
            # for a concept that hadn't been mastered yet.
            nodes[concept] = {
                "mastery": 0.30, "encoding": "surface",
                "dual_coding": "verbal_only", "elaboration": False,
                "encoding_history": [],
                "lp_state": {
                    **self._DEFAULT_LP_STATE,
                    "lp_history":            [],
                    "session_state_vectors": [],
                },
            }
        lp = self._ensure_lp_state(nodes[concept])
        prev_level = lp.get("lp_level", "L1")
        # Streak convention (matches LPDiagnostician.diagnose in
        # lp_diagnostic.py): on any level change (advance or regress)
        # the streak resets to 0 — a change breaks the streak. On the
        # next session, if the student stays at the same level, the
        # streak increments to 1.
        if new_lp_level != prev_level:
            new_streak = 0
        else:
            new_streak = int(lp.get("lp_streak", 0)) + 1

        lp["lp_level"]            = new_lp_level
        lp["lp_streak"]           = new_streak
        lp["logical_step"]        = bool(logical_step)
        lp["logical_step_detail"] = bool(logical_step_detail)
        lp["last_intervention"]   = last_intervention
        lp["delta_lp_last"]       = int(delta_lp)
        lp.setdefault("lp_history", []).append({
            "timestamp":        datetime.now().isoformat(),
            "level":            new_lp_level,
            "prev_level":       prev_level,
            "delta_lp":         int(delta_lp),
            "streak":           new_streak,
            "intervention":     last_intervention,
        })
        if len(lp["lp_history"]) > max_history:
            lp["lp_history"] = lp["lp_history"][-max_history:]

        if session_state_vector is not None:
            lp.setdefault("session_state_vectors", []).append(
                list(session_state_vector)
            )
            if len(lp["session_state_vectors"]) > max_history:
                lp["session_state_vectors"] = lp["session_state_vectors"][-max_history:]

        state["last_updated"] = datetime.now().isoformat()
        self._save_states()

    def get_session_state_vectors(self, student_id: str, concept: str,
                                   max_len: int = 20) -> List[List[float]]:
        """Return the last `max_len` session state vectors for a concept
        — input sequence to LPProgressionRNN."""
        lp = self.load_lp_state(student_id, concept)
        seq = lp.get("session_state_vectors", []) or []
        return seq[-max_len:] if max_len else list(seq)

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _avg_mastery(self, state: Dict) -> float:
        nodes = state["cognitive_graph"]["concept_nodes"]
        if not nodes: return 0.30
        return sum(n["mastery"] for n in nodes.values()) / len(nodes)

    def _infer_concept(self, session_data: Dict) -> Optional[str]:
        """Infer Java concept from code, error, and question using CONCEPT_KEYWORDS."""
        text = (session_data.get("code", "") + " "
                + session_data.get("error_message", "") + " "
                + session_data.get("question", "")).lower()
        # Score each concept by keyword hit count — pick highest
        best_concept, best_score = None, 0
        for concept, kws in CONCEPT_KEYWORDS.items():
            score = sum(1 for kw in kws if kw.lower() in text)
            if score > best_score:
                best_score, best_concept = score, concept
        return best_concept if best_score > 0 else None

    def _stage_int(self, stage) -> int:
        order = [1, "2a", "2b", 3, "4a", "4b", 5]
        try:    return order.index(stage)
        except: return 0

    def _stage_to_scaffold(self, stage) -> int:
        return {1: 5, "2a": 4, "2b": 4, 3: 3, "4a": 1, "4b": 1, 5: 0}.get(stage, 3)
