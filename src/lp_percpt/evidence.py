"""
evidence.py — Steps 4-7: what a prompt shows about one concept.

For each concept linked in Step 3 this module
  * assigns clauses to the concept                    (G4 Attribution, G5 Weak link)
  * drops clauses that are not evidence               (G6 Question / symptom report, G7 Parroting of shown text,
                                                       G8 Pasted code)
  * detects E1-E4 and each misconception's status     (Evidence sheet)
  * drops evidence that is not correct                (G9 Wrong trace, G10 Wrong mechanism,
                                                       G11 Jargon, G12 Self-contradiction)
and records, for every decision, the clause and the graph statement behind it.

Best-match principle: a clause is judged against the graph statement it is
most about. A misconception is held only when the clause matches its wrong
belief better than any correct fact of the concept, and a contradiction
counts as a wrong trace only against the clause's best-matching fact, and
only when the clause entails none of the concept's facts. (The NLI model alone
flags contradictions with statements a clause is not about.)
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from . import models
from .identify import ConceptHit, _word_hit
from .knowledge import Concept, PercptKnowledge
from .thresholds import (BAND_LO, CONTRA, FACT_CONTRA_MAX, FACT_ENT, FACT_SIM,
                         HELD_ENT, HELD_SIM, HELD_SIM_STRONG, PARROT_SIM,
                         REF_SIM, WEAK_LINK)

MET, UNCERTAIN, NOT_MET = "met", "uncertain", "not_met"
NO_NLI = {"entailment": 0.0, "contradiction": 0.0, "neutral": 1.0}
BEST_MARGIN = 0.05          # a fact within this similarity of the best counts as "best-matching"

# ── Clause features ─────────────────────────────────────────────────────────
_Q_START = re.compile(r"^\s*(why|how|what|when|where|which|who|does|do|did|is|are|can|could|should|would|will|isn't|doesn't|won't)\b", re.I)
_HYPOTHESIS = re.compile(r"\b(because|since|is it|maybe it|could it be|i think|so that)\b", re.I)
_NEGATION = re.compile(r"\b(not|never|no longer|isn't|doesn't|don't|won't|cannot|can't|aren't|wasn't|didn't|nothing|no)\b|n't\b", re.I)
_HEDGE = re.compile(r"\b(i think|maybe|probably|i guess|not sure|perhaps|might|i believe)\b", re.I)
_CAUSAL = re.compile(r"\b(because|since|so|therefore|thus|hence|that's why|which means|which makes|causes?|caused|until|as long as|unless|otherwise|so that|which is why|that is why)\b", re.I)
_PURPOSE = re.compile(r"\b(so that|in order to|overall|as a whole|the (whole|entire) (loop|program|code|method)|(this|the) (loop|code|program|method) (computes|calculates|finds|counts|sums|adds up|prints|builds|returns)|(computes|calculates|finds|counts|sums|adds up|accumulates|totals) (the|all|every|each))\b", re.I)
_TRANSFER = re.compile(r"\b(if (we|you|i) (change|changed|used|use|swap|swapped|replace|replaced|made|make)|if it (were|was)|instead of|to fix|should (be|use|start|end)|would (be|print|give|run|stop|throw)|in general|for any|any (array|loop|string|value|number|int)|every (array|loop|string|time)|always)\b", re.I)
_TRACE_BIND = re.compile(r"\b[a-z_]\w*(\s*\[\s*\w+\s*\])?\s*(=|==|is|becomes|equals|will be|gets|goes to|stays|holds|is now|turns into)\s*-?\d+(\.\d+)?\b", re.I)
_STEP = re.compile(r"\b(first|then|next|after that|afterwards|second|third|each (time|pass|iteration)|on the (first|second|third|last|next) (pass|iteration|time)|iteration|pass)\b", re.I)
_OUTPUT = re.compile(r"\b(prints?|outputs?|displays?|shows?)\b[^.]*?(\"[^\"]*\"|'[^']*'|-?\d+(\.\d+)?|true|false|null)", re.I)
_OBSERVED = re.compile(r"\b(it (says|said|gives|gave|prints|printed|shows|showed|returns|returned|outputs|throws|threw|crashes|crashed)|i (get|got|see|saw)|(says|gives|prints|shows) me|keeps? (saying|giving|printing|running)|even though|my (code|loop|program|array|string|method|output|condition|class|variable))\b", re.I)
_HELP = re.compile(r"\b(just (tell|give) me|what('?s| is) the (answer|solution)|give me the (answer|code|solution)|tell me the answer|solve it for me|do it for me)\b", re.I)
_FILLER = re.compile(r"^\s*(idk|i don'?t know|no idea|dunno|not sure|nothing|ok|okay|yes|no|hmm+|\?+)\s*[.!?]*\s*$", re.I)

STOPWORDS = set("""a an the and or but if then else of to in on at by for with from as is are was were be been
being it its this that these those i you he she we they me my your our their do does did doing have has had
so not no can could should would will just very also too there here what why how when where which who whom
about into over under than out up down off again once all any both each few more most other some such only own
same s t don now""".split())
JARGON = set("""heap stack reference references pointer pointers memory address addresses iteration iterations
bytecode jvm object objects instance instances scope runtime compile compiler compiled syntax semantic
semantics primitive primitives allocate allocation""".split())


def content_words(text: str) -> List[str]:
    return [w for w in re.findall(r"[a-zA-Z_][a-zA-Z_']+", text.lower()) if w not in STOPWORDS]


@dataclass
class Clause:
    idx: int
    text: str
    is_question: bool
    has_hypothesis: bool
    negated: bool
    hedged: bool
    causal: bool
    step: bool

    @classmethod
    def of(cls, idx: int, text: str) -> "Clause":
        q = text.rstrip().endswith("?") or bool(_Q_START.match(text))
        return cls(idx, text, q, bool(_HYPOTHESIS.search(text)), bool(_NEGATION.search(text)),
                   bool(_HEDGE.search(text)), bool(_CAUSAL.search(text)), bool(_STEP.search(text)))

    @property
    def bare_question(self) -> bool:
        return self.is_question and not self.has_hypothesis

    @property
    def symptom_report(self) -> bool:
        """Reports an observed result only: no cause, no steps."""
        return bool(_OBSERVED.search(self.text)) and not self.causal and not self.step


@dataclass
class Item:
    """One piece of evidence: which check, which clause, which graph statement."""
    check: str                  # E1..E4, held, refuted, wrong_trace
    clause: str
    statement: str = ""
    score: float = 0.0
    status: str = MET

    def to_dict(self) -> Dict:
        return {"check": self.check, "clause": self.clause, "statement": self.statement,
                "score": round(self.score, 3), "status": self.status}


@dataclass
class ConceptEvidence:
    concept: str
    checks: Dict[str, str] = field(default_factory=lambda: {"E1": NOT_MET, "E2": NOT_MET, "E3": NOT_MET, "E4": NOT_MET})
    items: List[Item] = field(default_factory=list)
    held: Set[str] = field(default_factory=set)
    refuted: Set[str] = field(default_factory=set)
    gates: List[str] = field(default_factory=list)          # reason codes that fired
    hedged: bool = False
    mixed: bool = False
    wrong_trace: bool = False
    weak_link: bool = False
    clause_keys: List[str] = field(default_factory=list)    # normalised clause texts used (G18)
    prompt_level: int = 0

    def set(self, check: str, status: str, item: Optional[Item] = None) -> None:
        order = {NOT_MET: 0, UNCERTAIN: 1, MET: 2}
        if order[status] > order[self.checks[check]]:
            self.checks[check] = status
        if item is not None:
            self.items.append(item)

    def drop(self, check: str) -> None:
        self.checks[check] = NOT_MET
        self.items = [i for i in self.items if i.check != check]

    @property
    def empty(self) -> bool:
        """No evidence of any kind for this concept in the prompt."""
        return (all(v == NOT_MET for v in self.checks.values()) and not self.held
                and not self.refuted and not self.wrong_trace)

    def gate(self, code: str) -> None:
        if code not in self.gates:
            self.gates.append(code)

    def to_dict(self) -> Dict:
        return {"concept": self.concept, "checks": dict(self.checks),
                "held": sorted(self.held), "refuted": sorted(self.refuted),
                "gates": list(self.gates), "hedged": self.hedged, "mixed": self.mixed,
                "wrong_trace": self.wrong_trace, "weak_link": self.weak_link,
                "items": [i.to_dict() for i in self.items]}


# ── Prompt-level gates (Layer 1) ────────────────────────────────────────────
def content_gate(text: str, min_words: int) -> bool:
    """G1: True when the prompt has too little content to classify."""
    return bool(_FILLER.match(text or "")) or len(content_words(text or "")) < min_words


def help_seeking(text: str) -> bool:
    """G2: the prompt only asks for the answer."""
    if not _HELP.search(text or ""):
        return False
    return len(content_words(_HELP.sub("", text or ""))) < 4


# ── helpers ─────────────────────────────────────────────────────────────────
def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", (text or "").lower())).strip()


def _cue_in(c: Concept, text: str) -> bool:
    low = text.lower()
    return any(p.search(text) for p in c.code_cues) or any(_word_hit(w, low) for w in c.word_cues)


def _desc(c: Concept) -> str:
    return f"{c.label.replace('_', ' ')}: {c.description}"


@dataclass
class _Scores:
    desc: object
    fact: object
    mis: object
    nb: object
    nli_f: Dict[Tuple[int, int], Dict]
    nli_m: Dict[Tuple[int, int], Dict]


def _score(c: Concept, kg: PercptKnowledge, texts: List[str]) -> _Scores:
    facts = c.facts
    mis_txt = [kg.misconceptions[m].wrong_belief for m in sorted(c.misconceptions)]
    nb_txt = [_desc(kg.concepts[n]) for n in sorted(c.neighbours)]
    sim_desc = models.similarity(texts, [_desc(c)])
    sim_fact = models.similarity(texts, facts) if facts else None
    sim_mis = models.similarity(texts, mis_txt) if mis_txt else None
    sim_nb = models.similarity(texts, nb_txt) if nb_txt else None
    pairs, where = [], []
    for i in range(len(texts)):
        for j in range(len(facts)):
            if sim_fact is not None and sim_fact[i, j] >= 0.35:
                pairs.append((texts[i], facts[j])); where.append(("f", i, j))
        for j in range(len(mis_txt)):
            if sim_mis is not None and sim_mis[i, j] >= REF_SIM:
                pairs.append((texts[i], mis_txt[j])); where.append(("m", i, j))
    res = models.nli(pairs) or [NO_NLI] * len(pairs)
    nli_f, nli_m = {}, {}
    for (kind, i, j), r in zip(where, res):
        (nli_f if kind == "f" else nli_m)[(i, j)] = r
    return _Scores(sim_desc, sim_fact, sim_mis, sim_nb, nli_f, nli_m)


def _topic_sim(sc: _Scores, i: int) -> float:
    vals = []
    if sc.desc is not None:
        vals.append(float(sc.desc[i, 0]))
    if sc.fact is not None and sc.fact.shape[1]:
        vals.append(float(sc.fact[i].max()))
    return max(vals) if vals else 0.0


# ── Steps 4-7 ───────────────────────────────────────────────────────────────
def collect(text: str, clauses_txt: List[str], hits: List[ConceptHit], kg: PercptKnowledge,
            shown_text: str = "", code: str = "") -> Tuple[Dict[str, ConceptEvidence], List[Dict]]:
    """Evidence for every linked concept, plus review-log entries (Step 13)."""
    clauses = [Clause.of(i, t) for i, t in enumerate(clauses_txt)]
    texts = [cl.text for cl in clauses]
    review: List[Dict] = []
    linked = [kg.concepts[h.concept] for h in hits]

    # G7 Parroting against what the student was shown
    shown_parts = [s for s in re.split(r"(?<=[.!?;])\s+|\n+", shown_text or "") if len(s.strip()) > 3]
    parroted_shown: Set[int] = set()
    if shown_parts and texts:
        sim = models.similarity(texts, shown_parts)
        if sim is not None:
            parroted_shown = {i for i in range(len(texts)) if sim[i].max() >= PARROT_SIM}

    # G8 Pasted code: code identical to the code the student was shown is ignored
    student_code = code or ""
    if student_code and _norm(student_code) and _norm(student_code) in _norm(shown_text):
        student_code = ""

    scores = {c.id: _score(c, kg, texts) for c in linked} if texts else {}
    # G4 Attribution: each clause belongs to the linked concepts it names, or to the
    # linked concept it is most about.
    owner: Dict[int, str] = {}
    for i in range(len(texts)):
        owner[i] = max(linked, key=lambda c: _topic_sim(scores[c.id], i)).id

    out: Dict[str, ConceptEvidence] = {}
    for hit, c in zip(hits, linked):
        ev = ConceptEvidence(c.id)
        out[c.id] = ev
        if not hit.cue_linked and hit.confidence < WEAK_LINK:
            ev.weak_link = True
            ev.gate("weak_link")
        if not hit.cue_linked:
            review.append({"kind": "meaning_only_match", "concept": c.id,
                           "matched": hit.meaning_match or hit.misconception_match, "text": text})
        if student_code and _cue_in(c, student_code):
            ev.set("E1", MET, Item("E1", "(student code)", "code cue"))
        if not texts:
            continue

        sc = scores[c.id]
        facts = c.facts
        mis_ids = sorted(c.misconceptions)
        mis_txt = [kg.misconceptions[m].wrong_belief for m in mis_ids]
        neighbours = sorted(c.neighbours)

        for i, cl in enumerate(clauses):
            if len(linked) > 1 and not _cue_in(c, cl.text) and owner[i] != c.id:
                ev.gate("attribution")
                continue
            desc_sim = float(sc.desc[i, 0]) if sc.desc is not None else 0.0
            f_sims = [float(sc.fact[i, j]) for j in range(len(facts))] if sc.fact is not None else []
            f_nli = [sc.nli_f.get((i, j), NO_NLI) for j in range(len(facts))]
            best_f_sim = max(f_sims, default=0.0)
            best_f_ent = max((r["entailment"] for r in f_nli), default=0.0)

            # G7 Parroting: only text the student was actually shown counts as copied
            if i in parroted_shown:
                ev.gate("parroting")
                continue
            ev.clause_keys.append(_norm(cl.text))
            ev.hedged = ev.hedged or cl.hedged

            # E1 Reference
            if _cue_in(c, cl.text) or desc_sim >= BAND_LO or best_f_sim >= BAND_LO:
                ev.set("E1", MET, Item("E1", cl.text, _desc(c), max(desc_sim, best_f_sim)))

            # G9 Wrong trace: the clause contradicts the fact it is most about
            # and entails none of the concept's facts (the graph's rules are
            # long sentences; the NLI model misreads some against a correct clause)
            wrong = None
            if not cl.bare_question and best_f_ent < FACT_ENT:
                for j, fact in enumerate(facts):
                    if (f_sims[j] >= BAND_LO and f_sims[j] >= best_f_sim - BEST_MARGIN
                            and f_nli[j]["contradiction"] >= CONTRA):
                        wrong = (fact, f_nli[j]["contradiction"])
                        break

            # Misconception status, by the best-match principle
            if not cl.bare_question:
                for j, mid in enumerate(mis_ids):
                    if sc.mis is None:
                        break
                    s = float(sc.mis[i, j])
                    r = sc.nli_m.get((i, j), NO_NLI)
                    held = (s >= HELD_SIM and s >= best_f_sim
                            and ((r["entailment"] >= HELD_ENT and r["entailment"] > best_f_ent)
                                 or (s >= HELD_SIM_STRONG and r["contradiction"] < FACT_CONTRA_MAX and not cl.negated)))
                    # a clause that is itself a wrong trace never refutes anything
                    refuted = not wrong and (
                        (s >= REF_SIM and r["contradiction"] >= CONTRA and best_f_ent >= FACT_ENT)
                        or (s >= HELD_SIM and s >= best_f_sim and cl.negated and r["entailment"] < HELD_ENT))
                    if held:
                        ev.held.add(mid); ev.items.append(Item("held", cl.text, mis_txt[j], s))
                    elif refuted:
                        ev.refuted.add(mid); ev.items.append(Item("refuted", cl.text, mis_txt[j], s))

            # G6 Question / symptom report: E1 only
            if cl.bare_question:
                ev.gate("question")
                continue
            if cl.symptom_report:
                ev.gate("symptom_report")
                continue

            words = content_words(cl.text)
            label_words = set(c.label.lower().split("_"))
            substantive = [w for w in words if w not in JARGON and w not in label_words]
            jargon_only = len(substantive) < 3 and any(w in JARGON for w in words)

            if wrong:
                ev.wrong_trace = True
                ev.gate("wrong_trace")
                ev.items.append(Item("wrong_trace", cl.text, wrong[0], wrong[1], NOT_MET))
                review.append({"kind": "contradicts_fact", "concept": c.id, "clause": cl.text, "fact": wrong[0]})
                if cl.causal:                                   # G10: a causal claim that is wrong
                    ev.gate("wrong_mechanism")
                    review.append({"kind": "wrong_mechanism", "concept": c.id, "clause": cl.text})
                continue

            # E2 Execution: fact match (fact, score, status, via_nli)
            fact_hit = None
            for j, fact in enumerate(facts):
                r = f_nli[j]
                if r["contradiction"] >= FACT_CONTRA_MAX:
                    continue
                if r["entailment"] >= FACT_ENT and (fact_hit is None or not fact_hit[3]):
                    fact_hit = (fact, r["entailment"], MET, True)
                elif f_sims[j] >= FACT_SIM and (fact_hit is None or fact_hit[2] != MET):
                    fact_hit = (fact, f_sims[j], MET, False)
                elif f_sims[j] >= BAND_LO and fact_hit is None:
                    fact_hit = (fact, f_sims[j], UNCERTAIN, False)
            if jargon_only and fact_hit and not fact_hit[3]:      # G11
                ev.gate("jargon")
                fact_hit = None
            if fact_hit:
                ev.set("E2", fact_hit[2], Item("E2", cl.text, fact_hit[0], fact_hit[1], fact_hit[2]))

            # E2 Execution: value trace
            binds = len(_TRACE_BIND.findall(cl.text))
            if binds >= 2 or (binds >= 1 and cl.step) or (_OUTPUT.search(cl.text) and cl.step):
                ev.set("E2", MET, Item("E2", cl.text, "value trace", 1.0))

            # E3 Integration: causal link across an edge, a causal mechanism, or the purpose
            if not jargon_only:
                nb_hit = None
                for k, n in enumerate(neighbours):
                    s = float(sc.nb[i, k]) if sc.nb is not None else 0.0
                    if _cue_in(kg.concepts[n], cl.text) or s >= BAND_LO:
                        nb_hit = (n, s)
                        break
                if cl.causal and nb_hit:
                    ev.set("E3", MET, Item("E3", cl.text, f"edge {c.id} - {nb_hit[0]}", nb_hit[1]))
                elif cl.causal and fact_hit and fact_hit[2] == MET:
                    ev.set("E3", MET, Item("E3", cl.text, f"mechanism: {fact_hit[0]}", fact_hit[1]))
                elif _PURPOSE.search(cl.text):
                    ev.set("E3", MET, Item("E3", cl.text, "overall purpose", 1.0))
                elif cl.causal and fact_hit and fact_hit[2] == UNCERTAIN:
                    ev.set("E3", UNCERTAIN, Item("E3", cl.text, "causal, weak fact match", fact_hit[1], UNCERTAIN))

            # E4 Transfer / debug: transfer marker with execution content
            if _TRANSFER.search(cl.text) and (fact_hit or binds or cl.step):
                ev.set("E4", MET, Item("E4", cl.text, "transfer / fix", 1.0))

        # E4 via a refuted boundary misconception, with a correct fact stated
        rep = ev.refuted & c.boundary
        if rep and ev.checks["E2"] == MET:
            ev.set("E4", MET, Item("E4", "", f"refuted {', '.join(sorted(rep))}", 1.0))

        # G12 Self-contradiction: held and refuted together, or a correct E2 next to a wrong trace
        if (ev.held & ev.refuted) or (ev.wrong_trace and ev.checks["E2"] == MET):
            ev.mixed = True
            ev.gate("self_contradiction")
            ev.refuted -= ev.held           # held wins when both appear

    return out, review
