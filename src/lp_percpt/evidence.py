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

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from . import claims as claimlib
from . import models
from .execution import MUTATIONS, Run, Trace, get_tracer, input_of
from .identify import ConceptHit, _word_hit
from .knowledge import Concept, PercptKnowledge, Way
from .thresholds import (ATTR_MARGIN, BAND_LO, CONTRA, FACT_CONTRA_MAX, FACT_ENT, FACT_SIM,
                         HELD_ENT, HELD_SIM, HELD_SIM_STRONG, PARROT_SIM,
                         REF_SIM, WAY_ENT, WAY_SIM, WEAK_LINK)

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
# L4 predict_a_change / transfer: reasoning about changed code, or for any input
_TRANSFER = re.compile(r"\b(if (we|you|i) (change|changed|used|use|swap|swapped|replace|replaced|made|make)|if it were|instead of|would (be|print|give|run|stop|throw)|in general|for any|any (array|loop|string|value|number|int)|every (array|loop|string))\b", re.I)
# L3 diagnose_an_error: a fix for the given code ("fixing one given failing case is L3")
_FIX_GIVEN = re.compile(r"\b(to fix|should (be|use|start|end))\b", re.I)
_TRACE_BIND = re.compile(r"\b[a-z_]\w*(\s*\[\s*\w+\s*\])?\s*(=|==|is|becomes|equals|will be|gets|goes to|stays|holds|is now|turns into)\s*-?\d+(\.\d+)?\b", re.I)
_STEP = re.compile(r"\b(first|then|next|after that|afterwards|second|third|each (time|pass|iteration)|on the (first|second|third|last|next) (pass|iteration|time)|iteration|pass)\b", re.I)
_OUTPUT = re.compile(r"\b(prints?|outputs?|displays?|shows?)\b[^.]*?(\"[^\"]*\"|'[^']*'|-?\d+(\.\d+)?|true|false|null)", re.I)
_OBSERVED = re.compile(r"\b(it (says|said|gives|gave|prints|printed|shows|showed|returns|returned|outputs|throws|threw|crashes|crashed)|i (get|got|see|saw)|(says|gives|prints|shows) me|keeps? (saying|giving|printing|running)|even though|my (code|loop|program|array|string|method|output|condition|class|variable))\b", re.I)
_HELP = re.compile(r"\b(just (tell|give) me|what('?s| is) the (answer|solution)|give me the (answer|code|solution)|tell me the answer|solve it for me|do it for me)\b", re.I)
_CODE_TOKEN = re.compile(r"-?\d+(?:\.\d+)?|[=<>!]=|[-+*/%]=|\+\+|--|&&|\|\||[=<>]|\b[a-zA-Z_]\w*(?=\s*[\[(=])")
_NUM = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w.]*\w)")
# What the question part asks for (the tutor knows which part it asked). The
# graph's L4 ways reason beyond the given code: a changed program, another
# input, an error case or a new program; its L3 ways relate the parts (why /
# how do they differ). A correct answer to such a part shows that way.
_ASK_BEYOND = re.compile(r"\bwhat if\b|\bwhat (?:can |would |will |does )?happens?\b|\bwhat changes\b"
                         r"|\bwould\b.{0,40}\bthe same\b|\bswap (?:the|them|it|these)\b"
                         r"|\bdoes\b.{0,50}\b(?:compile|end|wait|play correctly)\b|\bwill\b.{0,40}\b(?:compile|play|work)\b"
                         r"|\bcan it know\b|\bclassmate (?:wrote|always)\b|\bwrite (?:a|the)\b|\bplan the\b"
                         r"|\breplace (?:a|an|the)\b|\bhow would you test\b|\bdoes not come back\b"
                         r"|\balways gets\b", re.I)
# fixing the given code: L3 diagnose_an_error ("fixing one given failing case is L3")
_ASK_FIX = re.compile(r"\bfix\b|\badd braces\b|\bfind the (?:cause|bug|error)\b", re.I)
_ASK_INPUT = re.compile(r"\bfor (?:the input )?([a-z]\w*)\s*=\s*(-?[\d.,]+)", re.I)
_ASK_DIAGNOSE = re.compile(r"\bcompile\b|\bclassmate\b|\bfix\b|\bcome back\b|\balways gets\b|\bcrash", re.I)
_ASK_WRITE = re.compile(r"\bwrite (?:a|the)\b|\bplan the\b|\breplace (?:a|an|the)\b|\badd braces\b|\bfix\b", re.I)
_ASK_RELATE = re.compile(r"^\s*why\b|\bwhy (?:is|are|does|do|did|would|can)\b|\bdiffer\b|\bdifference\b"
                         r"|\bwhat does the (?:loop|program|code) do\b|\boverall\b|\bblack box\b", re.I)
# an answer that fixes or rewrites the code (imperative), or names an error
_FIX = re.compile(r"^\s*(?:use|cast|add|change|replace|move|put|write|declare|initiali[sz]e|remove|swap|call)\b"
                  r"|\.\s*(?:use|cast|add|change|replace|move|put|write|declare|initiali[sz]e|remove|swap|call)\b"
                  r"|\b(?:the )?order matters\b", re.I)
_ERROR_TALK = re.compile(r"\b(?:will not|won't|does not|doesn't|cannot|can't|not) compile\b|\bcompile(?:-| )time\b"
                         r"|\bcompiler\b|\bcrash(?:es|ed)?\b|\bthrows?\b|\bexception\b|\bout of bounds\b"
                         r"|\bnever (?:ends|stops|erased|returns)\b|\bdoes not come back\b|\btrapped\b", re.I)
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
    way: str = ""               # the has_level way this evidence shows, e.g. "L2 output_prediction"

    def to_dict(self) -> Dict:
        return {"check": self.check, "clause": self.clause, "statement": self.statement,
                "score": round(self.score, 3), "status": self.status, "way": self.way}


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
    reason: str = ""           # why the prompt is at its level (the way shown)
    wrong_reading: List[str] = field(default_factory=list)  # L0 everyday-reading ways the prompt shows
    n_good: int = 0             # claims the run confirms
    n_wrong: int = 0            # claims the run (or Java) contradicts
    source: str = ""            # what set the level: run, question, relation cue, judge, similarity, a weak reader
    judged: Optional[Dict] = None   # the judge's item for this concept (judge.py), when it ran
    wrong_rule: bool = False    # L0 because the run or the judge found a rule that contradicts Java

    def ways(self) -> Dict[int, str]:
        """Level -> the first way shown for it (met evidence only)."""
        out: Dict[int, str] = {}
        for i in self.items:
            if i.way and i.status == MET and i.check in ("E1", "E2", "E3", "E4"):
                out.setdefault(int(i.check[1]), i.way)
        return out

    @property
    def l0_way(self) -> Optional[str]:
        """The L0 way the prompt shows: a held misconception, an everyday reading of
        the code, or a trace that applies the rule unevenly (wrong at least as often
        as right). A single slip in an otherwise correct trace is not L0 (graph)."""
        if self.held:
            return "misconception (" + ", ".join(sorted(self.held)) + ")"
        if self.wrong_reading:
            return "everyday_reading"
        if self.wrong_trace and self.n_wrong >= max(1, self.n_good):
            return "inconsistent_trace"
        return None

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
                and not self.refuted and not self.wrong_trace and not self.wrong_reading)

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
    """G1: True when the prompt has too little content to classify. Values,
    operators and code names count as content, so a value trace is read."""
    t = text or ""
    return bool(_FILLER.match(t)) or len(content_words(t)) + len(_CODE_TOKEN.findall(t)) < min_words


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


JAVA_WORDS = set("""abstract boolean break byte case catch char class continue default do double else
false final float for if int long new null private protected public return short static String
switch this throw true try void while var System out println print printf args main Math StdIn
StdOut StdDraw length""".split())


def _code_names(code: str) -> Set[str]:
    """The names a piece of code uses (variables, arrays), without Java words."""
    return {w for w in re.findall(r"\b[A-Za-z_]\w*\b", code or "") if w not in JAVA_WORDS}


def _applied(text: str, names: Set[str], step: bool = False) -> bool:
    """A clause applies a rule to the code when it works with the code's values,
    or follows several of its parts in order (L2 per the graph: "line by line or
    value by value"). Naming one part, or stating the rule alone, is L1."""
    named = sum(1 for n in names if re.search(rf"\b{re.escape(n)}\b", text))
    return bool(_NUM.search(text) or '"' in text or (named >= 2 and step))


# a call written in the question part: "What is  Math.abs(Integer.MIN_VALUE) ?"
_INLINE_CALL = re.compile(r"\b[A-Za-z_][\w.]*\s*\((?:[^()?]|\([^()?]*\))*\)")


def _new_calls(asked: str, code: str) -> List[str]:
    """Calls the part asks about that do not occur in the given code."""
    given = _norm(code)
    return [e for e in _INLINE_CALL.findall(asked or "") if "." in e.split("(")[0] and _norm(e) not in given]


def _standalone(expr: str) -> bool:
    """An expression jshell can evaluate on its own: library classes and literals only."""
    names = re.findall(r"(?<![\w.])[A-Za-z_]\w*", expr)
    return all(n[0].isupper() or n in JAVA_WORDS for n in names)


# "because" + a named neighbour = L3, and L3 / L4 ways decided by NLI alone: on by
# default; LP_SHORTCUTS=off leaves L3 / L4 to the code run and the question-form rules
SHORTCUTS = os.environ.get("LP_SHORTCUTS", "on").lower() != "off"

# a statement the student writes in the answer ("int c;", 'System.out.println("x is 5");')
_STUDENT_STMT = re.compile(r"(?:(?:final\s+)?(?:int|long|double|boolean|char|String)\s+[A-Za-z_]\w*[^;]*"
                           r"|[A-Za-z_][\w.]*\s*(?:\([^;]*\)|=[^;=][^;]*|\+\+|--))\s*;")
# "sets x to 5", "assigns 5 to x", "stores 5 in x": an assignment the student says happens
_SETS = re.compile(r"\b(?:sets|assigns)\s+([A-Za-z_]\w*)\s+(?:to|as)\s+(-?\d+(?:\.\d+)?)\b"
                   r"|\b(?:stores|puts|assigns)\s+(-?\d+(?:\.\d+)?)\s+(?:in|into|to)\s+([A-Za-z_]\w*)\b", re.I)


def _probe_claims(text: str, code: str, names: Set[str], tracer) -> List[claimlib.Claim]:
    """Value claims about a variable the given code never gives a value: one the
    student declares ("int c; ... so c is 0") or one the code does not have ("sets x
    to 5"). Each is decided by compiling the code (with the student's statements)
    as a Java method, plus a read of the variable: "might not have been
    initialized" or "cannot find symbol" proves the claimed value wrong."""
    if not code or not re.search(r"[;{}]", code) or tracer is None or not tracer.available:
        return []
    stmts = [m.group(0).strip() for m in _STUDENT_STMT.finditer(text)]
    stmts = [x for x in stmts if _norm(x) not in _norm(code)]
    declared = set(re.findall(r"\b(?:int|long|double|boolean|char|String)\s+([A-Za-z_]\w*)", " ".join(stmts)))
    claims = []
    for m in claimlib._BIND_RE.finditer(text):
        if m.group(1) in declared and m.group(1) not in names:
            claims.append(claimlib.Claim("value", text, var=m.group(1), value=m.group(2), final=True))
    for m in _SETS.finditer(text):
        var, val = (m.group(1), m.group(2)) if m.group(1) else (m.group(4), m.group(3))
        if var not in names and var.lower() not in JAVA_WORDS:
            claims.append(claimlib.Claim("value", text, var=var, value=val, final=True))
    if not claims:
        return []
    base = code + "\n" + "\n".join(stmts)
    ok, _ = tracer.compiles(base)
    if not ok:
        return []                          # the code does not compile as a method anyway: no verdict
    out = []
    for c in claims:
        ok, err = tracer.compiles(base + f"\nObject __probe = {c.var};")
        if ok is False and "might not have been initialized" in err:
            c.note = f"in Java {c.var} has no value until one is assigned; reading it does not compile"
            out.append(c)
        elif ok is False and "cannot find symbol" in err:
            c.note = f"the code has no variable {c.var}, so nothing sets it"
            out.append(c)
    return out


def asks_beyond(asked: str, code: str) -> bool:
    """The question part asks about code other than the given code: a change, a
    new program or code fragment, an error case, or an input the code does not
    use ("for t = 5" when the code sets t = 25). The part's first sentence and
    every later question must ask that, so a part that also asks about the
    given code ("What does p hold? ... Fix it") is checked against its run."""
    sents = [q for q in re.split(r"(?<=[?.])\s+(?=[A-Z])", (asked or "").strip()) if q.strip()]
    if not sents:
        return False
    given = _norm(code)

    def beyond(q: str) -> bool:
        if _ASK_BEYOND.search(q):
            return True
        for name, value in _ASK_INPUT.findall(q):
            m = re.search(rf"\b{re.escape(name)}\s*=\s*(-?[\d.]+)\s*;", code or "")
            if m and m.group(1) != value.rstrip(".,"):
                return True
        # a call that is not part of the given code ("What is  Math.abs(Integer.MIN_VALUE) ?")
        if _new_calls(q, code):
            return True
        # a statement that is not part of the given code ("What does  int k2 = Math.round(2.5);  do?")
        return any(_norm(s) not in given for s in re.findall(r"\b(?:int|long|double|char|boolean|String|[a-z]\w*)\b[^;?]*=[^;?]*;", q))
    return beyond(sents[0]) and all(beyond(q) for q in sents[1:] if q.rstrip().endswith("?"))


_FIRST_PERSON = re.compile(r"\b(?:I|my)\b(?!\s+(?:think|guess|believe|would say|get|got|see|saw)\b)")
_ASK_OWN_CODE = re.compile(r"\bwrite (?:a|the)\b|\badd braces\b|\breplace (?:a|an|the)\b|\brewrite\b", re.I)
_CODE_START = re.compile(r"^\s*(?:(?:int|long|double|boolean|char|String)\b|for\s*\(|while\s*\(|if\s*\(|do\s*\{|\{"
                         r"|[A-Za-z_]\w*(?:\[[^\]]*\])?\s*(?:=|\+=|-=|\+\+|\())")
_TOP_DECL = re.compile(r"(?:^|;|\{|\})\s*(?:final\s+)?(?:int|long|double|boolean|char|String)(?:\s*\[\s*\])*\s+([A-Za-z_]\w*)")
_TARGET_OUTPUT = re.compile(r"\bprints?\s*:?\s*\n(.+)$", re.S)
_SAME_BEHAVIOUR = re.compile(r"\bwithout changing what it (?:prints|does)\b|\bsame output\b|\bequivalent\b", re.I)


def _code_declared(code: str) -> Set[str]:
    return set(re.findall(r"\b(?:int|long|double|boolean|char|String)(?:\s*\[\s*\])*\s+([A-Za-z_]\w*)", code or ""))


def _judge_own_code(text: str, code: str, shown_text: str, asked: str, tracer) -> Tuple[Optional[bool], str]:
    """Run the code a student wrote for a write / rewrite part. Wrong when it does
    not compile, never ends or throws; right when it prints the output the part
    asks for; undecided otherwise (the program ran, but nothing says what it
    should do). New code that only adds to the given code runs after it."""
    if not asked or not _ASK_OWN_CODE.search(asked) or not _CODE_START.match(text or ""):
        return None, ""
    cut = max(text.rfind(";"), text.rfind("}"))
    own = text[:cut + 1] if cut >= 0 else ""
    if not own:
        return None, ""
    code = code if re.search(r"[;{}]", code or "") else ""      # "(writing task)": no code given
    given_top = set(_TOP_DECL.findall(re.sub(r"for\s*\([^)]*\)", "", code)))
    own_top = set(_TOP_DECL.findall(re.sub(r"for\s*\([^)]*\)", "", own)))
    # a rewrite of the given code runs alone; new code that uses the given code runs after it
    rewrite = re.search(r"\badd braces\b|\brewrite\b|\breplace\b", asked, re.I)
    program = own if (rewrite or own_top & given_top or not code) else f"{code}\n{own}"
    hint = shown_text or ""
    if "StdIn." in program and not input_of(hint):
        # no input given: a short test input that ends with the values the part names (a sentinel)
        hint = "for the input 3 5 " + " ".join(re.findall(r"-?\d+", asked)) + "\n" + hint
    # names the given code uses without declaring them may be declared for the
    # student's code too; any other undeclared name is a compile error
    run = tracer.run_code(program, hint, allowed=set(re.findall(r"\b[A-Za-z_]\w*\b", code)))
    if run is None:
        return None, ""
    if not run.ok:
        return False, "the student's code does not compile"
    if run.error == "timeout":
        return False, "the student's code never ends"
    if run.error and run.error != "NoSuchElementException":
        return False, f"the student's code throws {run.error}"
    if code and _SAME_BEHAVIOUR.search(asked):
        # "without changing what it prints for any x": run both for several values
        free = [n for n in dict.fromkeys(re.findall(r"\b([a-z]\w*)\b", code))
                if n not in _code_declared(code) and n not in JAVA_WORDS and not re.search(rf"\b{n}\s*\(", code)]
        for v in (-3, 0, 4):
            h = "".join(f"{n} = {v}\n" for n in free) + hint
            mine, theirs = tracer.run_code(program, h, allowed=set(free)), tracer.run_code(code, h, allowed=set(free))
            if mine and theirs and mine.ok and theirs.ok and mine.output.strip() != theirs.output.strip():
                return False, (f"for {free[0] if free else 'the input'} = {v} the student's code prints "
                               f"{' / '.join(mine.output.split())[:40]!r}, the original {' / '.join(theirs.output.split())[:40]!r}")
        return True, "the student's code prints the same as the original for every value tried"
    m = _TARGET_OUTPUT.search(asked)
    if m:
        want = [l.rstrip() for l in m.group(1).strip().splitlines()]
        got = [l.rstrip() for l in run.output.strip().splitlines()]
        return (got == want), ("the student's code prints what was asked" if got == want
                               else "the student's code prints " + " / ".join(got)[:80])
    return None, "the student's code runs" + _state_change(code, own, program, hint, run, tracer)


def _state_change(code: str, own: str, program: str, hint: str, run, tracer) -> str:
    """The variables of the given code (or declared by the student) whose final
    value the student's code changes, before and after: "a = [5, 4, 3, 2, 1] ->
    [50, 40, 30, 20, 10]". The judge checks it against what the part asks."""
    names = set(_TOP_DECL.findall(re.sub(r"for\s*\([^)]*\)", "", code or ""))) | \
        set(_TOP_DECL.findall(re.sub(r"for\s*\([^)]*\)", "", own)))
    base = tracer.trace(code, hint=hint) if code else None
    before = base.run.final if base else {}
    after = run.final
    changed = [f"{n} = {before[n]} -> {after[n]}" if n in before else f"{n} = {after[n]}"
               for n in sorted(names) if n in after and before.get(n) != after[n]]
    out = f"; output {' / '.join(run.output.split())[:60]!r}" if run.output.strip() else ""
    return ("; after it: " + ", ".join(changed) if changed else "; it changes no variable") + out


# a definition: "A loop that ...", "It is a table to ..." (L1 names_the_element)
_DEFINITION = re.compile(r"^\s*(?:(?:it|this|that) is |it's )?(?:a|an)\s+[a-z]+(?:\s+[a-z]+)?\s+(?:that|which|to|of|plus|is|where|with)\b", re.I)


def _actual(c: claimlib.Claim, trace: Optional[Trace], evaluated: Dict[str, str]) -> str:
    """What the run really shows, for the claim a student got wrong."""
    if c.note:
        return c.note
    run = trace.run if trace else None
    if c.kind == "expr":
        return f"Java gives {c.expr} = {evaluated.get(c.expr, '?')}"
    if run is None:
        return ""
    if c.kind == "value":
        seq = run.values.get(c.var.split("[")[0], [])
        return f"the code gives {c.var.split('[')[0]} = {seq[-1] if seq else '?'}" + ("" if c.final else f" (values {', '.join(seq[:8])})")
    if c.kind == "output":
        return f"the code prints {' '.join(run.output.split())[:100]}"
    if c.kind == "count":
        return f"the loop bodies run {', '.join(str(v) for v in run.passes.values()) or '0'} times"
    if c.kind == "endless":
        return "the loop ends"
    if c.kind == "crash":
        return "the code runs without an exception"
    if c.kind == "lines":
        return f"the lines that run are {', '.join(str(n) for n in dict.fromkeys(run.lines))}"
    return ""


@dataclass
class _Scores:
    desc: object
    fact: object
    mis: object
    nb: object
    nli_f: Dict[Tuple[int, int], Dict]
    nli_m: Dict[Tuple[int, int], Dict]
    way: Dict[str, object] = field(default_factory=dict)                      # L0 / L3 / L4 -> sim matrix
    nli_w: Dict[Tuple[str, int, int], Dict] = field(default_factory=dict)
    way_of: Dict[str, List[Tuple[str, Way]]] = field(default_factory=dict)    # level -> (rule, way) per column


def _way_rules(c: Concept, level: str) -> List[Tuple[str, Way]]:
    """(rule sentence, way) pairs a clause is matched against: the L3 and L4 ways,
    and the everyday readings of the L0 ways (misconception ways are matched
    through their misconception nodes)."""
    out: List[Tuple[str, Way]] = []
    for w in c.ways.get(level, []):
        if level == "L0" and w.name != "everyday_reading":
            continue
        out += [(r, w) for r in w.rules]
    return out


def _score(c: Concept, kg: PercptKnowledge, texts: List[str]) -> _Scores:
    facts = c.facts
    mis_txt = [kg.misconceptions[m].wrong_belief for m in sorted(c.misconceptions)]
    nb_txt = [_desc(kg.concepts[n]) for n in sorted(c.neighbours)]
    sim_desc = models.similarity(texts, [_desc(c)])
    sim_fact = models.similarity(texts, facts) if facts else None
    sim_mis = models.similarity(texts, mis_txt) if mis_txt else None
    sim_nb = models.similarity(texts, nb_txt) if nb_txt else None
    way_of = {lv: _way_rules(c, lv) for lv in ("L0", "L3", "L4")}
    way_of = {lv: rw for lv, rw in way_of.items() if rw}
    sim_way = {lv: models.similarity(texts, [r for r, _ in rw]) for lv, rw in way_of.items()}
    pairs, where = [], []
    for i in range(len(texts)):
        for j in range(len(facts)):
            if sim_fact is not None and sim_fact[i, j] >= 0.35:
                pairs.append((texts[i], facts[j])); where.append(("f", i, j))
        for j in range(len(mis_txt)):
            if sim_mis is not None and sim_mis[i, j] >= REF_SIM:
                pairs.append((texts[i], mis_txt[j])); where.append(("m", i, j))
        for lv, sim in sim_way.items():
            for j, (rule, _) in enumerate(way_of[lv]):
                if sim is not None and sim[i, j] >= BAND_LO:
                    pairs.append((texts[i], rule)); where.append((lv, i, j))
    res = models.nli(pairs) or [NO_NLI] * len(pairs)
    nli_f, nli_m, nli_w = {}, {}, {}
    for (kind, i, j), r in zip(where, res):
        if kind == "f":
            nli_f[(i, j)] = r
        elif kind == "m":
            nli_m[(i, j)] = r
        else:
            nli_w[(kind, i, j)] = r
    return _Scores(sim_desc, sim_fact, sim_mis, sim_nb, nli_f, nli_m, sim_way, nli_w, way_of)


def _way_hit(sc: _Scores, level: str, i: int, text: str = "",
             kg: Optional[PercptKnowledge] = None) -> Optional[Tuple[str, float, Way]]:
    """The way rule of a has_level edge a clause states: it must entail the rule,
    not only be on the same topic (similarity alone matches restatements of the
    L2 rule). A relation way also needs the concept it relates to (its
    requires_concept) to be named in the clause."""
    sim = sc.way.get(level)
    if sim is None:
        return None
    best = None
    for j, (rule, way) in enumerate(sc.way_of.get(level, [])):
        s = float(sim[i, j])
        r = sc.nli_w.get((level, i, j), NO_NLI)
        if s >= WAY_SIM and r["entailment"] >= WAY_ENT and r["contradiction"] < FACT_CONTRA_MAX:
            if way.requires and kg is not None and not any(
                    t in kg.concepts and _cue_in(kg.concepts[t], text) for t in way.requires):
                continue
            if best is None or r["entailment"] > best[1]:
                best = (rule, r["entailment"], way)
    return best


def _topic_sim(sc: _Scores, i: int) -> float:
    vals = []
    if sc.desc is not None:
        vals.append(float(sc.desc[i, 0]))
    if sc.fact is not None and sc.fact.shape[1]:
        vals.append(float(sc.fact[i].max()))
    return max(vals) if vals else 0.0


# ── Steps 4-7 ───────────────────────────────────────────────────────────────
def collect(text: str, clauses_txt: List[str], hits: List[ConceptHit], kg: PercptKnowledge,
            shown_text: str = "", code: str = "", asked: str = "") -> Tuple[Dict[str, ConceptEvidence], List[Dict]]:
    """Evidence for every linked concept, plus review-log entries (Step 13).

    Every check is tagged with the has_level way of the graph it shows
    (Item.way), so the level is the highest level whose way the prompt shows.
    `asked` is the question part the student answers: a correct, reasoned
    answer to a part that asks beyond the given code shows an L4 way, and one
    to a why / how-do-they-differ part an L3 way.

    Correctness is decided by running the code, not by the language models:
    the claims each clause makes (values, output, loop counts, lines that run,
    literal expressions; claims.py) are checked against a traced run of `code`
    (execution.py). A false claim is a wrong trace (G9); a set of false claims
    that one misconception's run reproduces means that misconception is held.
    The NLI model only finds which graph statement a clause is about; its
    contradictions go to the review log."""
    clauses = [Clause.of(i, t) for i, t in enumerate(clauses_txt)]
    texts = [cl.text for cl in clauses]
    review: List[Dict] = []
    linked = [kg.concepts[h.concept] for h in hits]

    # Claims and their verdicts against the real run (and each misconception's run)
    tracer = get_tracer()
    trace = tracer.trace(code, hint=shown_text) if code else None
    names = set(trace.run.values) if trace else _code_names(code)
    letters = bool(trace and re.search(r"[A-Za-z]", trace.run.output))
    question = (shown_text or "").replace(code or "", "")
    final = claimlib.asks_final(question)
    clause_claims = [claimlib.extract(t, names, letters, final) or claimlib.extract_answer(t, asked, names)
                     for t in texts]
    # a value asked for an expression beyond the given code is checked by evaluating it
    asked_exprs = [e for e in _new_calls(asked, code) if _standalone(e)]
    if asked_exprs:
        for i, t in enumerate(texts):
            m = re.search(r"-?\d+(?:\.\d+)?", t)
            if m and not any(c.kind == "expr" for c in clause_claims[i]):
                clause_claims[i] = list(clause_claims[i]) + [
                    claimlib.Claim("expr", t, value=m.group(0), expr=asked_exprs[0])]
                break
    exprs = [c.expr for cc in clause_claims for c in cc if c.kind == "expr"]
    exprs += [e.replace("/", "* 1.0 /") for e in exprs if "/" in e]
    evaluated = tracer.evaluate(sorted(set(exprs))) if exprs else {}
    real = trace.run if trace else Run(False)
    # a part that asks about changed code (another input, a swap, a fix) is not
    # answered by the given code's run: only literal expressions are checked
    ask_beyond = asks_beyond(asked, code)
    # "I read two numbers ... it crashes": a report about the student's own code,
    # not a claim about the given code
    own = [bool(_FIRST_PERSON.search(t)) for t in texts]
    verdicts = [[(c, claimlib.check(c, real, evaluated)
                  if (((trace and not ask_beyond) or c.kind == "expr") and not own[i]) else None)
                 for c in cc]
                for i, cc in enumerate(clause_claims)]
    probed = {i: _probe_claims(t, code, names, tracer) for i, t in enumerate(texts) if not own[i]}
    for i, cs in probed.items():
        verdicts[i] = list(verdicts[i]) + [(c, False) for c in cs]
    false_claims = [c for vs in verdicts for c, v in vs if v is False]
    predicted: List[str] = []
    if false_claims:
        # a misconception explains the answer when every checkable claim of it
        # (right and wrong ones) holds in the run of the code under that misconception
        checked = [c for vs in verdicts for c, v in vs if v is not None and c.kind != "expr"]
        if trace and any(c.kind != "expr" for c in false_claims):
            predicted = [mid for mid, mrun in trace.mutants.items()
                         if all(claimlib.check(c, mrun, evaluated) is True for c in checked)]
        for c in false_claims:
            if c.kind == "expr" and "/" in c.expr and claimlib._num(evaluated.get(c.expr.replace("/", "* 1.0 /"), "")) == claimlib._num(c.value):
                predicted.append("IntegerDivisionGivesFraction")
        predicted = [m for m in dict.fromkeys(predicted) if m in kg.misconceptions]
    code_names = _code_names(code)
    ask_relate = bool(_ASK_RELATE.search(asked or "")) and not ask_beyond
    ask_fix = bool(_ASK_FIX.search(asked or "")) and not ask_beyond
    # code the student wrote for a write / rewrite part: run it (True / False / None)
    own_ok, own_note = _judge_own_code(text, code, shown_text, asked, tracer)
    own_fact = own_note if own_ok is not False and own_note else ""

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
    # G4 Attribution: each clause belongs to the linked concepts it names, and to
    # every linked concept it is about almost as much as the one it is most about.
    belongs: Dict[int, Set[str]] = {}
    for i in range(len(texts)):
        tsim = {c.id: _topic_sim(scores[c.id], i) for c in linked}
        best = max(tsim.values())
        belongs[i] = {cid for cid, s in tsim.items()
                      if s == best or (s >= BAND_LO and s >= best - ATTR_MARGIN)}

    out: Dict[str, ConceptEvidence] = {}
    orphan_placed: Dict[str, bool] = {}
    for hit, c in zip(hits, linked):
        ev = ConceptEvidence(c.id)
        out[c.id] = ev
        if own_fact:
            ev.items.append(Item("own_run", text[:200], own_fact, 1.0, MET))
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

        for i, cl in enumerate(clauses):
            if len(linked) > 1 and not _cue_in(c, cl.text) and c.id not in belongs[i]:
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

            # E1 Reference (L1 names_the_element)
            on_topic = _cue_in(c, cl.text) or desc_sim >= BAND_LO or best_f_sim >= BAND_LO
            if on_topic:
                ev.set("E1", MET, Item("E1", cl.text, _desc(c), max(desc_sim, best_f_sim), way="L1 names_the_element"))

            # G9 Wrong trace: a claim of the clause that the run (or Java) contradicts.
            # An NLI contradiction with a graph fact is only logged for review.
            wrong = None
            good: List[claimlib.Claim] = []
            if not cl.bare_question:
                for claim, verdict in verdicts[i]:
                    if verdict is False and wrong is None:
                        wrong = (f"stated {claim.describe()}; {_actual(claim, trace, evaluated)}", 1.0)
                    elif verdict is True:
                        good.append(claim)
                if wrong is None and best_f_ent < FACT_ENT:
                    for j, fact in enumerate(facts):
                        if (f_sims[j] >= BAND_LO and f_sims[j] >= best_f_sim - BEST_MARGIN
                                and f_nli[j]["contradiction"] >= CONTRA):
                            review.append({"kind": "contradicts_fact_unchecked", "concept": c.id,
                                           "clause": cl.text, "fact": fact})
                            break
            run_match = bool(good) and wrong is None
            if not cl.bare_question:
                ev.n_good += len(good)
                ev.n_wrong += sum(1 for _, v in verdicts[i] if v is False)

            # Misconception status, by the best-match principle. Only prose is read
            # for beliefs: the NLI model misreads code lines ("System.out.println")
            # as statements about them
            if not cl.bare_question and not re.search(r"[;{}]", cl.text):
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
                    if held and trace is not None and mid in MUTATIONS:
                        # the code ran and this misconception has a program form: the run
                        # decides it (it is held only when its run gives the student's values)
                        review.append({"kind": "held_by_wording_only", "concept": c.id, "clause": cl.text,
                                       "misconception": mid})
                    elif held and kg.misconceptions[mid].kind == "error" and _ERROR_TALK.search(cl.text):
                        # describing an error node as an error ("it will not compile: no closing
                        # quote") diagnoses it; it is not a belief the student holds
                        ev.set("E4" if ask_beyond else "E3", MET,
                               Item("E4" if ask_beyond else "E3", cl.text, f"diagnoses {mid}: {mis_txt[j]}", s,
                                    way=("L4" if ask_beyond else "L3") + " diagnose_an_error"))
                    elif held:
                        ev.held.add(mid); ev.items.append(Item("held", cl.text, mis_txt[j], s))
                    elif refuted:
                        ev.refuted.add(mid); ev.items.append(Item("refuted", cl.text, mis_txt[j], s))

            # L0 everyday reading: the clause states the everyday reading of an L0
            # way better than any correct rule of the concept
            if not cl.bare_question and not cl.negated and not wrong:
                er = _way_hit(sc, "L0", i)
                if er is not None and er[1] > best_f_ent:
                    ev.wrong_reading.append(cl.text)
                    ev.items.append(Item("L0", cl.text, er[0], er[1], NOT_MET, way="L0 everyday_reading"))
                    continue

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
            # a definition with no value of the code names the element (L1) and no more
            if _DEFINITION.match(cl.text) and not _NUM.search(cl.text):
                ev.items.append(Item("E1", cl.text, "definition", 1.0, way="L1 names_the_element"))
                continue

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
            if fact_hit and _applied(cl.text, code_names, cl.step):
                ev.set("E2", fact_hit[2], Item("E2", cl.text, fact_hit[0], fact_hit[1], fact_hit[2],
                                               way="L2 one_step_execution"))
            elif fact_hit and fact_hit[2] == MET:
                # the rule is stated but not applied to any part of the code: L1 (S way)
                ev.set("E1", MET, Item("E1", cl.text, f"rule stated, not applied: {fact_hit[0]}", fact_hit[1],
                                       way="L1 states_the_rule"))

            # E2 Execution: claims the run confirms. Several, or one with its
            # reason, apply the rules to the code; a bare result is not levelled
            # beyond L1 (graph: "a correct output with no justification")
            binds = len(_TRACE_BIND.findall(cl.text))
            if run_match:
                status = MET if (len(good) >= 2 or cl.causal or cl.step or len(clauses) > 1) else UNCERTAIN
                kinds = {g.kind for g in good}
                way = ("L2 output_prediction" if kinds & {"output", "crash", "endless"}
                       else "L2 line_by_line_trace" if len(good) >= 2 or kinds & {"count", "lines"}
                       else "L2 one_step_execution")
                ev.set("E2", status, Item("E2", cl.text, "confirmed by the run: "
                                          + "; ".join(g.describe() for g in good), 1.0, status, way=way))
            elif not trace and (binds >= 2 or (binds >= 1 and cl.step) or (_OUTPUT.search(cl.text) and cl.step)):
                ev.set("E2", MET, Item("E2", cl.text, "value trace", 1.0, way="L2 line_by_line_trace"))

            # E3 Integration: an L3 way of the concept. relation_to_neighbour needs
            # the concept it relates to (requires_concept on the edge) named in the
            # clause; purpose_of_the_whole needs the purpose stated. A reason given
            # for this concept's own rule is the rule applied (L2), not a relation.
            code_like = bool(re.search(r"[;{}]|\[\w*\]|\b\w+\s*=\s*[\w(]", cl.text))
            named: List[str] = []
            if not jargon_only:
                targets = c.relation_targets() or c.neighbours
                named = [n for n in sorted(targets) if n in kg.concepts and _cue_in(kg.concepts[n], cl.text)]
                if cl.causal and named and SHORTCUTS:
                    ev.set("E3", MET, Item("E3", cl.text, f"edge {c.id} - {named[0]}", 1.0,
                                           way="L3 relation_to_neighbour"))
                elif _PURPOSE.search(cl.text):
                    ev.set("E3", MET, Item("E3", cl.text, "overall purpose", 1.0, way="L3 purpose_of_the_whole"))
                elif SHORTCUTS and (way := _way_hit(sc, "L3", i, cl.text, kg)) is not None:
                    ev.set("E3", MET, Item("E3", cl.text, f"L3 way: {way[0]}", way[1], way=f"L3 {way[2].name}"))
                elif ask_fix and on_topic and own_ok is not False and (cl.causal or code_like or _FIX.search(cl.text)):
                    # a reasoned fix of the given code
                    ev.set("E3", MET, Item("E3", cl.text, f"answers: {asked.strip()[:80]}", 1.0,
                                           way="L3 diagnose_an_error"))
                elif ask_relate and on_topic and (cl.causal or named or code_like):
                    # a reasoned answer to a why / how-do-they-differ part
                    ev.set("E3", MET, Item("E3", cl.text, f"answers: {asked.strip()[:80]}", 1.0,
                                           way="L3 relation_to_neighbour"))

            # E4 Transfer / debug: an L4 way of the concept, by its rule, by the
            # form of the answer (a change predicted, a fix, an error diagnosed),
            # or as a reasoned answer to a part that asks beyond the given code
            if _FIX_GIVEN.search(cl.text) and on_topic and not ask_beyond:
                ev.set("E3", MET, Item("E3", cl.text, "fix for the given code", 1.0, way="L3 diagnose_an_error"))
            if _TRANSFER.search(cl.text) and (fact_hit or binds or cl.step):
                ev.set("E4", MET, Item("E4", cl.text, "change predicted", 1.0, way="L4 predict_a_change"))
            elif SHORTCUTS and not jargon_only and (way := _way_hit(sc, "L4", i, cl.text, kg)) is not None:
                ev.set("E4", MET, Item("E4", cl.text, f"L4 way: {way[0]}", way[1], way=f"L4 {way[2].name}"))
            elif ask_beyond and on_topic and not jargon_only:
                fix, err = bool(_FIX.search(cl.text)), bool(_ERROR_TALK.search(cl.text))
                status = MET
                if _ASK_WRITE.search(asked) and (code_like or fix):
                    # new code is L4 only when it is correct: shown by its run, else
                    # uncertain toward L4 (the follow-up asks the deciding question)
                    way, status = "L4 transfer_to_a_new_program", (MET if own_ok else UNCERTAIN)
                    if own_ok is False:
                        way = ""
                elif (_ASK_DIAGNOSE.search(asked) or err) and (cl.causal or err or fix):
                    way = "L4 diagnose_an_error"
                elif cl.causal or fix:
                    way = "L4 predict_a_change"
                else:
                    way = ""                    # a bare result for the changed code is L2 on the new code
                if way:
                    ev.set("E4", status, Item("E4", cl.text, f"answers: {asked.strip()[:80]}", 1.0, status, way=way))

        # Misconception held by prediction: the code, run the way a misconception
        # says it runs, gives the student's wrong values. It is held on the linked
        # concepts it belongs to, or else on the first concept with the wrong trace.
        for mid in predicted:
            listed = mid in c.misconceptions
            if listed or (ev.wrong_trace and not orphan_placed.get(mid)
                          and not any(mid in lc.misconceptions for lc in linked)):
                ev.held.add(mid)
                ev.refuted.discard(mid)
                ev.items.append(Item("held", "", f"{mid}: the student's values match a run of the code under "
                                     f"this belief ({kg.misconceptions[mid].wrong_belief})", 1.0))
                if not listed:
                    orphan_placed[mid] = True

        # The student's own code ran wrong (does not compile, never ends, throws,
        # prints something else): a wrong trace of that code
        if own_ok is False and not ev.empty:
            ev.wrong_trace = True
            ev.n_wrong += 1
            ev.gate("wrong_trace")
            ev.items.append(Item("wrong_trace", text[:200], own_note, 1.0, NOT_MET))

        # E4 via a refuted boundary misconception, with the parts related (E3): the
        # predict_a_change way reasons about what the misconception gets wrong
        rep = ev.refuted & c.boundary
        if rep and ev.checks["E2"] == MET and ev.checks["E3"] == MET:
            ev.set("E4", MET, Item("E4", "", f"refuted {', '.join(sorted(rep))}", 1.0, way="L4 predict_a_change"))

        # G12 Self-contradiction: held and refuted together. A wrong claim next to
        # correct ones is either a slip (fewer wrong than right: L2 with an error,
        # per the graph) or an uneven trace (L0 inconsistent_trace, see l0_way)
        if ev.wrong_trace and 0 < ev.n_wrong < ev.n_good:
            ev.gate("slip")
        if ev.held & ev.refuted:
            ev.mixed = True
            ev.gate("self_contradiction")
            ev.refuted -= ev.held           # held wins when both appear

    return out, review
