"""Step 1 of the pipeline - split code, question and answer into statements.

* **Code**: ``execution.classify_code`` tells Java from shell commands, a
  prose description of a run and a writing task. Java: one statement per
  simple statement, header or comment (``execution.parse``); concepts come
  from the code-cue regexes, the declared types and the static findings. One
  extra *result* statement carries the run: the output, or every compile /
  run error. Commands: one statement per command line, concepts from the
  command patterns (``> file``, ``< file``, ``|``, arguments). Prose: read
  like the question.
* **Question**: sentences, each with its own set of types (``output``,
  ``value``, ``fix``, ``why``, ``explain``); the variables it asks about
  (its *target*) and a name it asks the student to use.
* **Answer**: split into turns ("Turn 1:", "Turn 2:"), Java written by the
  student (kept unnormalised, ``source = "answer_code"``) and English
  clauses. Each clause has two concept fields: ``direct`` (named by an alias,
  a symbol such as ``%``, or code the student wrote) and ``context`` (the
  concepts of the code a variable or pronoun points at). Only ``direct``
  concepts count as the student naming a concept. Clauses with "would",
  "if ... started", "with ...", "after that" are hypothetical; "oh wait",
  "actually" mark a self-correction.

spaCy (``en_core_web_sm``) only splits sentences; without it a regex
splitter gives the same statements for ordinary punctuation.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field, replace
from functools import lru_cache
from typing import TYPE_CHECKING

from . import lexicon
from .execution import CodeKind, CodeStmt, Trace, _make_stmt, mask_literals, parse, variables
from .slots import Mention, Slot, extract_slots, find_mentions, implied_slots, normalize

if TYPE_CHECKING:  # pragma: no cover
    from .graph import KG

log = logging.getLogger(__name__)



@dataclass(frozen=True)
class Statement:
    """One statement of code, question or answer."""

    id: str
    source: str               # code | question | answer | answer_code
    text: str
    concepts: tuple[str, ...]           # direct + context
    slots: tuple[Slot, ...] = ()
    negated: bool = False
    link_words: tuple[str, ...] = ()
    order: int = 0
    sentence: int = 0
    variables: tuple[str, ...] = ()     # code variables named (after pronoun resolution)
    direct: tuple[str, ...] = ()        # concepts named in the text itself (alias, symbol, own code)
    qtype: str = ""                     # question types, joined by "+"
    is_result: bool = False
    context: tuple[str, ...] = ()       # concepts of the code the text points at
    turn: int = 0
    hypothetical: bool = False
    corrects: bool = False              # starts a self-correction ("oh wait")
    changes: tuple[tuple[tuple[str, str], ...], ...] = ()  # stated program changes (what-if)
    meta: dict = field(default_factory=dict, compare=False, hash=False)

    def short(self) -> str:
        return self.text if len(self.text) <= 60 else self.text[:57] + "..."

    @property
    def qtypes(self) -> frozenset[str]:
        return frozenset(t for t in self.qtype.split("+") if t)


@dataclass(frozen=True)
class CodeContext:
    """What question and answer reading need to know about the code."""

    stmts: tuple[CodeStmt, ...]
    var_types: dict
    var_concepts: dict        # variable -> concepts of the statements that compute it
    code_concepts: tuple[str, ...]
    printed_vars: tuple[str, ...]
    stmt_concepts: dict = field(default_factory=dict)   # statement index -> producer concepts
    kind: CodeKind | None = None
    has_print: bool = False
    target_vars: tuple[str, ...] = ()
    run_error: str = ""                 # compile | run | timeout | ""


# ------------------------------------------------------------------- spaCy

@lru_cache(maxsize=1)
def _nlp():
    try:
        import spacy

        return spacy.load("en_core_web_sm", disable=["ner", "lemmatizer"])
    except Exception as exc:  # pragma: no cover - depends on the install
        log.warning("spaCy model unavailable (%s); using the regex splitter", exc)
        return None


def sentences(text: str) -> list[str]:
    """Sentence split (spaCy, else punctuation)."""
    text = text.strip()
    if not text:
        return []
    nlp = _nlp()
    if nlp is None:
        return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[\"'(A-Za-z0-9])", text) if s.strip()]
    out: list[str] = []
    for s in (x.text.strip() for x in nlp(text).sents):
        if not s:
            continue
        if out and not re.search(r"[.!?][\"')]*$", out[-1]):
            out[-1] = f"{out[-1]} {s}"
        else:
            out.append(s)
    return out


def _spacy_negated(text: str) -> bool:
    nlp = _nlp()
    if nlp is None:
        return False
    return any(t.dep_ == "neg" for t in nlp(text))


def clauses(sentence: str) -> list[str]:
    """Split one sentence at clause words (the word starts the new clause)."""
    words = "|".join(re.escape(w) for w in lexicon.CLAUSE_SPLIT)
    parts = re.split(rf"(?:,\s*|;\s*|\s+)(?=(?:{words})\b)", sentence, flags=re.I)
    out = []
    for p in parts:
        p = p.strip(" ,;")
        if re.fullmatch(rf"(?:{words})\.?", p, flags=re.I) or not p:
            continue
        out.append(p)
    return out


# -------------------------------------------------------------------- code

def code_context(kg: "KG", code_program: str, trace: Trace | None,
                 kind: CodeKind | None = None) -> CodeContext:
    stmts = tuple(trace.stmts) if trace is not None and trace.stmts else (
        tuple(parse(code_program)) if code_program else ())
    types = variables(list(stmts))
    decisive = _decisive(trace)
    own = {s.index: set(code_concepts(kg, s)) | decisive.get(s.index, set()) for s in stmts}
    enclosing = _enclosing(stmts)
    producer = {s.index: own[s.index] | {c for h in enclosing[s.index] for c in own[h]}
                for s in stmts}
    var_concepts: dict[str, list[str]] = {}
    for name in types:
        cs: list[str] = []
        for s in stmts:
            if name in s.assigns:
                cs += sorted(producer[s.index] - lexicon.DECL_CONCEPTS)
        if not cs:
            for s in stmts:
                if name in s.reads:
                    cs += sorted(producer[s.index] - lexicon.DECL_CONCEPTS)
        if not cs:  # only declared: the concept the graph names for a declared name
            cs = [lexicon.ROLES["declared_name"]] if lexicon.ROLES.get("declared_name") else []
        var_concepts[name] = list(dict.fromkeys(cs))
    for f in (trace.findings if trace else ()):
        if f.variable in var_concepts and f.pattern in lexicon.DECISIVE:
            var_concepts[f.variable].append(lexicon.DECISIVE[f.pattern])
    concepts = sorted({c for v in own.values() for c in v})
    printed = tuple(dict.fromkeys(s.printed.strip() for s in stmts
                                  if s.kind == "print" and s.printed and s.printed.strip() in types))
    return CodeContext(stmts, types, {k: tuple(dict.fromkeys(v)) for k, v in var_concepts.items()},
                       tuple(c for c in concepts if c in kg.knowledge.concepts), printed,
                       {k: tuple(sorted(c for c in v if c in kg.knowledge.concepts)) for k, v in producer.items()},
                       kind, any(s.kind == "print" for s in stmts), (),
                       trace.run.error_kind if trace is not None else "")


def _enclosing(stmts: tuple[CodeStmt, ...]) -> dict[int, list[int]]:
    """Statement index -> indices of the headers whose block holds it."""
    out: dict[int, list[int]] = {}
    open_h: list[CodeStmt] = []
    label = re.compile(r"\s*(?:case|default)\b")
    for s in stmts:
        while open_h:
            h = open_h[-1]
            if label.match(h.text):  # a case label holds the statements after it
                if s.depth < h.depth or (s.depth == h.depth and s.kind == "header" and label.match(s.text)):
                    open_h.pop()
                    continue
                break
            if s.depth <= h.depth:
                open_h.pop()
                continue
            break
        out[s.index] = [h.index for h in open_h]
        if s.kind == "header":
            open_h.append(s)
    return out


def _decisive(trace: Trace | None) -> dict[int, set[str]]:
    out: dict[int, set[str]] = {}
    for f in (trace.findings if trace else ()):
        if f.pattern in lexicon.DECISIVE:
            out.setdefault(f.stmt_index, set()).add(lexicon.DECISIVE[f.pattern])
    return out


def code_concepts(kg: "KG", s: CodeStmt) -> list[str]:
    """Concepts a code statement shows (code-cue regexes + declared types)."""
    if s.kind == "comment":
        c = lexicon.OUTCOME.get("comment")
        return [c] if c in kg.knowledge.concepts else []
    masked = mask_literals(s.text)
    found = []
    for cid in kg.concepts:
        for rx in kg.cues.get(cid, {}).get("code", []):
            target = s.text if lexicon.CODE_TEXT.get(cid) == "raw" else masked
            if re.search(rx, target):
                found.append(cid)
                break
    for typ, _, _ in s.declares:
        base = typ.replace("[]", "")
        if base in lexicon.TYPE_CONCEPT:
            found.append(lexicon.TYPE_CONCEPT[base])
    # a pattern that also matches a more specific concept's code yields to it
    found = [c for c in found if lexicon.YIELDS.get(c) not in found]
    return sorted(set(c for c in found if c in kg.knowledge.concepts))


def code_statements(kg: "KG", ctx: CodeContext, trace: Trace | None) -> list[Statement]:
    """One statement per code statement (or command) + one result statement."""
    decisive = _decisive(trace)
    uninit_decl = {f.variable for f in (trace.findings if trace else ())
                   if f.pattern == "uninitialized_read"}
    out: list[Statement] = []
    kind = ctx.kind
    if kind is not None and kind.kind == "commands":
        for cmd in kind.commands:
            cs = sorted({c for rx, c in lexicon.COMMAND_PATTERNS if re.search(rx, cmd) and c in kg.knowledge.concepts})
            out.append(Statement(id=f"k{len(out) + 1}", source="code", text=cmd, concepts=tuple(cs),
                                 order=len(out), direct=tuple(cs), meta={"kind": "command"}))
        return out
    for s in ctx.stmts:
        if s.kind == "close":
            continue
        cs = set(code_concepts(kg, s))
        slots: list[Slot] = []
        for typ, name, has_init in s.declares:
            if not has_init:
                slots.append(Slot("value", "none", False, f"var:{name}"))
                if name in uninit_decl:  # the concept of the graph signal that found the read
                    cs |= {c for c, sig in lexicon.SIGNALS if sig.get("analysis") == "uninitialized_read"}
        cs |= decisive.get(s.index, set())
        out.append(Statement(
            id=f"k{len(out) + 1}", source="code", text=s.text, concepts=tuple(sorted(cs)),
            slots=tuple(slots), order=len(out),
            variables=tuple(sorted({n for _, n, _ in s.declares} | set(s.reads) | set(s.assigns))),
            direct=tuple(sorted(cs)),
            meta={"kind": s.kind, "line": s.line, "reads": list(s.reads), "index": s.index,
                  "assigns": list(s.assigns),
                  "declares": [list(d) for d in s.declares],
                  "producer": list(ctx.stmt_concepts.get(s.index, ()))}))
    if trace is not None and (trace.run.available or trace.run.error_kind):
        out.append(result_statement(trace, len(out), decisive))
    return out


def result_statement(trace: Trace, order: int, decisive: dict[int, set[str]]) -> Statement:
    run = trace.run
    slots: list[Slot] = []
    cs: set[str] = set()
    if run.error_kind == "compile":
        text = "compile error: " + "; ".join(run.errors or (run.error,))
        slots.append(Slot("compile", "compile_error"))
        slots.append(Slot("error_time", "compile"))
        cs.add(lexicon.OUTCOME.get("compile_error", ""))
        m = re.search(r"variable (\w+) might not have been initialized", run.error)
        if m:
            slots.append(Slot("value", "none", False, f"var:{m.group(1)}"))
    elif run.error_kind == "run":
        text = f"run-time error: {run.error}"
        slots += [Slot("compile", "compiles"), Slot("crash", "run_error"), Slot("error_time", "run")]
        cs.add(lexicon.OUTCOME.get("run_error", ""))
    elif run.error_kind == "timeout":
        text = "runs without stopping (timeout)"
        slots += [Slot("compile", "compiles"), Slot("runs", "endless")]
        cs.add(lexicon.OUTCOME.get("timeout", ""))
    else:
        shown = run.output.strip().replace("\n", " | ")
        text = f"output: {shown}" if shown else "output: (nothing)"
        slots += [Slot("compile", "compiles"), Slot("crash", "no_error"),
                  Slot("output", run.output.strip())]
    cs |= {c for v in decisive.values() for c in v}
    cs.discard("")
    return Statement(id="kr", source="code", text=text, concepts=tuple(sorted(cs)),
                     slots=tuple(slots), order=order, is_result=True,
                     direct=tuple(sorted(cs)),
                     meta={"run_available": run.available, "error_kind": run.error_kind})


# ---------------------------------------------------------------- question

def question_types(text: str) -> tuple[str, ...]:
    """All types of one question sentence (output / value before the rest)."""
    t = normalize(text)
    found = []
    for qtype, words in lexicon.QUESTION_TYPES:
        if any(re.search(rf"(?<!\w){re.escape(w)}(?!\w)", t) for w in words):
            found.append(qtype)
    return tuple(found) or ("explain",)


def question_type(text: str) -> str:
    return question_types(text)[0]


def asked_name(question: str) -> str | None:
    m = lexicon.rx("asked_name").search(question or "")
    return m.group(1) if m else None


@lru_cache(maxsize=1)
def _verb_keys() -> frozenset[str]:
    """Print/output verbs: they name no concept when the code has no print call."""
    return frozenset(normalize(v) for v in lexicon.VERB_RESOLVE)


def question_statements(kg: "KG", question: str, ctx: CodeContext) -> list[Statement]:
    out = []
    texts = list(sentences(question))
    if ctx.kind is not None and ctx.kind.kind in ("prose", "writing") and ctx.kind.prose:
        texts = list(sentences(re.sub(r"\(\s*writing task\s*\)", "", ctx.kind.prose, flags=re.I))) + texts
    for i, sent in enumerate(texts):
        norm = normalize(sent)
        mentions = collapse(find_mentions(norm, kg.alias_index, tuple(ctx.var_types)), ctx)
        mentions = [m for m in mentions if not (not m.var and not ctx.has_print and m.alias in _verb_keys())]
        cs, direct, vars_named = _resolve(mentions, ctx, None)
        cmd = sorted({c for line in re.findall(r"(?:^|[%$;])\s*(java[^%$;]*)", sent)
                      for rx, c in lexicon.COMMAND_PATTERNS if re.search(rx, line.strip()) and c in kg.knowledge.concepts})
        direct = tuple(sorted(set(direct) | set(cmd)))
        cs = tuple(sorted(set(cs) | set(cmd)))
        qt = question_types(sent)
        # a variable the question gives a value to ("when x = 17") is an input, not what is asked
        given = {v for v in vars_named if lexicon.rx("given_value", VAR=re.escape(v)).search(sent)}
        out.append(Statement(id=f"q{i + 1}", source="question", text=sent,
                             concepts=cs, order=i, sentence=i, variables=vars_named,
                             direct=direct, qtype="+".join(qt),
                             context=tuple(sorted(set(cs) - set(direct))),
                             meta={"targets": [v for v in vars_named if v not in given]}))
    return out


def target_vars(q_st: list[Statement], ctx: CodeContext) -> tuple[str, ...]:
    """Variables the question asks about ("what is result", "how num4 is computed")."""
    out = []
    for s in q_st:
        for v in s.meta.get("targets", s.variables):
            if v in ctx.var_types and v not in out:
                out.append(v)
    return tuple(out)


# ------------------------------------------------------------------ answer

def collapse(mentions: list[Mention], ctx: CodeContext) -> list[Mention]:
    """Give every ambiguous alias one concept: the first option the code
    uses, else the first option ("print" -> println when only println is
    called). Done before slot extraction so slots get the right subject."""
    out = []
    for m in mentions:
        if not m.var and len(m.concepts) > 1:
            in_code = [c for c in m.concepts if c in ctx.code_concepts]
            m = Mention(m.start, m.end, m.alias, ((in_code or list(m.concepts))[0],))
        out.append(m)
    return out


# nouns for printed text ("the output", "it displays"): they point at the
# print code (context) but do not name a print method
lexicon.OUTPUT_NOUNS = frozenset({"output", "outputs", "display", "displays", "shows"})


def _resolve(mentions: list[Mention], ctx: CodeContext,
             pronoun_var: str | None) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """Concepts of a clause: (all, direct, variables). Direct = named by an
    alias; a variable adds the concepts of the code that computes it."""
    direct = [m.concepts[0] for m in mentions if not m.var and m.concepts and m.alias not in lexicon.OUTPUT_NOUNS]
    nouns = [m.concepts[0] for m in mentions if not m.var and m.concepts and m.alias in lexicon.OUTPUT_NOUNS]
    vars_named = [m.var for m in mentions if m.var]
    if pronoun_var:
        vars_named.append(pronoun_var)
    via_vars = [c for v in vars_named for c in ctx.var_concepts.get(v, ())] + nouns
    concepts = sorted(set(direct) | set(via_vars))
    return tuple(concepts), tuple(sorted(set(direct))), tuple(sorted(set(vars_named)))


def _pronoun(norm: str) -> bool:
    return any(re.search(rf"(?<!\w){re.escape(p)}(?!\w)", norm) for p in lexicon.PRONOUNS)


# Java written in an answer: a statement ending in ';' (declaration,
# assignment, print call) or a for loop with its body statement.
_JAVA_IN_TEXT = re.compile(
    r"(?:\bfor\s*\([^;)]*;[^;)]*;[^)]*\)\s*\{?[^;{}]*;\s*\}?"
    r"|\b(?:int|double|char|boolean|String|long|float)(?:\s*\[\s*\])?\s+[A-Za-z_]\w*\s*=\s*[^;]+;"
    r"|\bSystem\.out\.\w+\s*\((?:\"[^\"]*\"|[^;\"])*\)\s*;"
    r"|\b[A-Za-z_][\w.]*(?:\s*\[[^\]]+\])?\s*[+\-*/%]?=(?!=)\s*[^;=\s][^;]*;)")
_SYMBOL_EXPR = re.compile(r"(?<![\w.%])(\w+)\s*(%|/|\*)\s*(\w+)(?![\w(])")


def split_turns(answer: str) -> list[tuple[int, str]]:
    """(turn number, text) pieces; probe / follow-up questions are dropped."""
    marks = list(lexicon.rx("turn").finditer(answer))
    if not marks:
        return [(0, answer)]
    out = []
    head = answer[:marks[0].start()].strip()
    if head:
        out.append((0, head))
    for k, m in enumerate(marks):
        end = marks[k + 1].start() if k + 1 < len(marks) else len(answer)
        if m.group(1):
            text = answer[m.end():end].strip().strip("“”\"").strip()
            out.append((int(m.group(1)), text))
    return out


def _looks_java(piece: str) -> bool:
    """No two plain words in a row outside quotes ("i = 9 num2 drops to 11;" is English)."""
    bare = re.sub(r"\"[^\"]*\"|'[^']*'", "0", piece)
    bare = re.sub(r"^\s*(?:for\s*\([^)]*\)|(?:int|double|char|boolean|String|long|float)(?:\s*\[\s*\])?\s+)", "", bare)
    return not re.search(r"\b[A-Za-z_]\w*\s+[A-Za-z_]\w*\b", bare) and not re.search(r"\d\s+[A-Za-z_]", bare)


def _pieces(text: str) -> list[tuple[str, str]]:
    """("code" | "text", piece) in order."""
    out, last = [], 0
    for m in _JAVA_IN_TEXT.finditer(text):
        if not _looks_java(m.group(0)):
            continue
        if m.start() > last and text[last:m.start()].strip(" —-–:;,"):
            out.append(("text", text[last:m.start()].strip(" —-–:;,")))
        out.append(("code", m.group(0).strip()))
        last = m.end()
    if text[last:].strip(" —-–:;,"):
        out.append(("text", text[last:].strip(" —-–:;,")))
    return out or [("text", text)]




_CHANGE_KINDS = ("loop_kind", "start", "start_bound", "for_value", "format", "repair", "cast")


def parse_changes(clause: str) -> tuple[tuple[tuple[str, str], ...], ...]:
    """Program changes a what-if clause states."""
    out = []
    for kind in _CHANGE_KINDS:
        for m in lexicon.rx(f"change_{kind}").finditer(clause):
            if kind == "loop_kind":
                out.append((("kind", "loop_kind"), ("to", m.group(1).lower())))
            elif kind in ("start", "for_value"):
                out.append((("kind", "start"), ("var", m.group(1)), ("value", m.group(2))))
            elif kind == "start_bound":
                n = int(m.group(3))
                val = n - 1 if m.group(2).lower() in ("below", "under") else n + 1
                out.append((("kind", "start"), ("var", m.group(1)), ("value", str(val)),
                            ("bound", f"{m.group(2).lower()} {n}")))
            elif kind == "format":
                out.append((("kind", "format"), ("spec", m.group(1))))
            elif kind == "cast":
                out.append((("kind", "cast"), ("cast", m.group(1)), ("expr", m.group(2))))
            else:
                out.append((("kind", "repair"),))
    return tuple(out)


def _hypothetical(norm: str) -> bool:
    return any(re.search(rx, norm) for rx in lexicon.HYPOTHETICAL_CLAUSE)




def _array_values(norm: str, q_types: frozenset[str], q_vars: tuple[str, ...]) -> list[Slot]:
    """"All zeros" / "gives 0, 0, 0.4" about the array the question asks about."""
    if "value" not in q_types or not q_vars:
        return []
    out = []
    m = lexicon.rx("all_same").match(norm)
    if m:
        v = "0" if m.group(1) in ("zeros", "zeroes", "0s", "zero", "0") else "1"
        out.append(Slot("value", f"all:{v}", False, f"var:{q_vars[-1]}", False, (0, len(norm)),
                        extra=(("verb", "is"),)))
    for m in lexicon.rx("list_values").finditer(norm):
        vals = ",".join(x.strip() for x in m.group(1).split(","))
        out.append(Slot("value", f"list:{vals}", False, f"var:{q_vars[-1]}", False, m.span(),
                        extra=(("verb", "is"),)))
    return out


def _symbol_concepts(kg: "KG", raw: str, ctx: CodeContext) -> list[str]:
    """Operators written as symbols between numbers or known variables."""
    out = []
    lines_like = len(re.findall(r"\d\s*/\s*\d", raw)) >= 2  # "3 2 1 / 2 1 / 1" separates lines
    for m in _SYMBOL_EXPR.finditer(raw):
        a, op, b = m.groups()
        if op == "/" and lines_like:
            continue
        ok = lambda x: x.isdigit() or x in ctx.var_types  # noqa: E731
        if not (ok(a) and ok(b)):
            continue
        cid = lexicon.OP_CONCEPT.get(op)
        if cid in kg.knowledge.concepts:
            out.append(cid)
    return out


def answer_statements(kg: "KG", answer: str, ctx: CodeContext,
                      q_types: frozenset[str] = frozenset(), q_vars: tuple[str, ...] = ()) -> list[Statement]:
    """Turns -> pieces (student code / English) -> clauses with concepts,
    slots, negation, link words, hypothetical changes and corrections."""
    out: list[Statement] = []
    last_var: str | None = None
    fallback_var = (q_vars[-1] if q_vars else (ctx.printed_vars[-1] if ctx.printed_vars
                    else (list(ctx.var_types)[-1] if ctx.var_types else None)))
    prev_vars: tuple[str, ...] = ()
    si = -1
    # an answer in parts "(a) ... (b) ..." answers several questions: its claims
    # cannot be matched to one run, so none of them is checked
    multipart = len(lexicon.rx("answer_parts").findall(answer)) >= 2
    for turn, text in split_turns(answer):
        correcting = False
        carried: tuple = ()
        for kind, piece in _pieces(text):
            if kind == "code":
                cst = _make_stmt(0, piece, 1, 0, "")
                cs = sorted(set(code_concepts(kg, cst)))
                si += 1
                out.append(Statement(
                    id=f"c{len(out) + 1}", source="answer_code", text=piece, concepts=tuple(cs),
                    order=len(out), sentence=si, direct=tuple(cs), turn=turn,
                    variables=tuple(sorted(set(cst.assigns) | set(cst.reads) | {d[1] for d in cst.declares})),
                    slots=(Slot("compile", "compiles", False, None, True), Slot("crash", "no_error", False, None, True)),
                    meta={"declares": [list(d) for d in cst.declares]}))
                continue
            code_ctx = [c for s in out[-1:] if s.source == "answer_code" for c in s.direct]
            for sent in sentences(piece):
                si += 1
                staged = False  # "after that ..." makes the rest of the sentence a what-if
                sent_norm = normalize(sent)
                # a marker keeps its own punctuation: "no," corrects, "no value" does not
                marks = [m.start() for c in lexicon.CORRECTION
                         for m in re.finditer(rf"(?<!\w){re.escape(c)}(?!\w)", sent_norm)]
                pos = 0
                for clause in clauses(sent):
                    norm = normalize(clause)
                    at = sent_norm.find(norm, pos)
                    pos = max(pos, at)
                    # a correction ("oh wait") holds from where it appears in the sentence on
                    if any(re.match(rf"{re.escape(c)}(?!\w)", norm) for c in lexicon.CORRECTION) or \
                            any(mk <= max(at, 0) for mk in marks):
                        correcting = True
                    mentions = collapse(find_mentions(norm, kg.alias_index, tuple(ctx.var_types),
                                                     fuzzy=True), ctx)
                    named = [m.var for m in mentions if m.var]
                    pron = None
                    if _pronoun(norm):
                        pron = last_var or fallback_var
                    cs, direct, vars_named = _resolve(mentions, ctx, pron)
                    direct = tuple(sorted(set(direct) | set(_symbol_concepts(kg, clause, ctx)) | set(code_ctx)))
                    context = tuple(sorted(set(cs) - set(direct)))
                    subj_mentions = [m for m in mentions if m.var or m.alias not in _verb_keys()]
                    slots = extract_slots(norm, subj_mentions, resolve_pronoun=pron, raw=clause,
                                          prev_vars=prev_vars)
                    slots = slots + _array_values(norm, q_types, q_vars)
                    slots = slots + _bare_output(clause, q_types, q_vars, slots)
                    slots = _attach_printed_value(slots, ctx, vars_named)
                    point = _code_point(clause, ctx)
                    if point is not None:
                        slots = [replace(s, extra=s.extra + (("point", str(point)),))
                                 if s.name == "value" else s for s in slots]
                    if lexicon.rx("mid_trace").search(norm):  # "at i = 9 num2 drops to 11": a value mid-loop
                        slots = [replace(s, extra=s.extra + (("point", "mid"),))
                                 if s.name == "value" else s for s in slots]
                    after_fix = ctx.run_error == "compile" and lexicon.rx("after_fix").search(norm)
                    claimed = [s.subject[4:] for s in slots if s.subject and s.subject.startswith("var:")]
                    printed = {c for st in ctx.stmts if st.kind == "print" for c in ctx.stmt_concepts.get(st.index, ())} \
                        if any(s.name in ("output", "printed") for s in slots) else set()
                    context = tuple(sorted((set(context) | {c for v in claimed for c in ctx.var_concepts.get(v, ())}
                                            | printed) - set(direct) - lexicon.GENERIC))
                    hyp = _hypothetical(norm) or bool(staged) or bool(after_fix) or multipart
                    changes = parse_changes(clause) if hyp else ()
                    if hyp:
                        # a what-if keeps the changes stated earlier in the turn
                        # ("with a while loop ... it would only differ if i started below 70")
                        kinds = {dict(c)["kind"] for c in changes}
                        changes = tuple(c for c in carried if dict(c)["kind"] not in kinds) + changes
                        carried = changes
                        if any(dict(c)["kind"] == "repair" for c in changes):
                            staged = True
                    if hyp:
                        slots = [replace(s, hypothetical=True) for s in slots]
                    slots = slots + implied_slots(slots)
                    words = norm.split()
                    links = tuple(w for w in lexicon.LINK_WORDS if w in words)
                    negated = (any(w in lexicon.NEGATION for w in words) or _spacy_negated(clause))
                    out.append(Statement(
                        id=f"c{len(out) + 1}", source="answer", text=clause,
                        concepts=tuple(sorted(set(direct) | set(context))),
                        slots=tuple(sorted(slots, key=lambda s: (s.span, s.key()))),
                        negated=negated, link_words=links, order=len(out), sentence=si,
                        variables=vars_named, direct=direct, context=context, turn=turn,
                        hypothetical=hyp, corrects=correcting, changes=changes))
                    if named:
                        last_var = named[-1]
                    elif pron:
                        last_var = pron
                    prev_vars = vars_named or prev_vars
                code_ctx = []
    return out




def _code_point(clause: str, ctx: CodeContext) -> int | None:
    """The last code statement a clause quotes ("after t = a and a = b"):
    its value claims are about that point of the run."""
    flat = re.sub(r"\s+", "", clause)
    hits = [s.index for s in ctx.stmts if s.kind in ("decl", "assign")
            and len(re.sub(r"[\s;]+", "", re.sub(r"^\w+\s+(?=\w+\s*=)", "", s.text))) >= 3
            and re.sub(r"[\s;]+", "", re.sub(r"^\w+\s+(?=\w+\s*=)", "", s.text)) in flat]
    return max(hits) if hits else None




def _bare_output(clause: str, q_types: frozenset[str], q_vars: tuple[str, ...],
                 slots: list[Slot]) -> list[Slot]:
    """A clause that is only printed tokens ("3 2 1 / 2 1 / 1", "10.") answers
    an output question (whole output) or a value question (the target)."""
    if any(s.name in ("output", "printed", "value") for s in slots):
        return []
    m = lexicon.rx("bare_sequence").match(clause)
    if not m:
        return []
    from .slots import _seq_value

    val = _seq_value(m.group(1))
    if "output" in q_types:
        return [Slot("output", val, False, None, False, (0, len(clause)))]
    if "value" in q_types and q_vars and re.fullmatch(r"-?\d+(?:\.\d+)?", val):
        return [Slot("value", val, False, f"var:{q_vars[-1]}", False, (0, len(clause)),
                     extra=(("verb", "is"),))]
    return []


def _attach_printed_value(slots: list[Slot], ctx: CodeContext,
                          vars_named: tuple[str, ...]) -> list[Slot]:
    """"It prints 0" when the code prints exactly one variable (the whole
    print argument) also says that variable's value is 0 (implied)."""
    extra = []
    for s in slots:
        if s.name not in ("output", "printed") or s.negated or not ctx.printed_vars:
            continue
        var = next((v for v in vars_named if v in ctx.printed_vars), None)
        if var is None and len(ctx.printed_vars) == 1:
            var = ctx.printed_vars[0]
        if var and not any(x.name == "value" and x.subject == f"var:{var}" for x in slots):
            extra.append(Slot("value", s.value, False, f"var:{var}", True, s.span))
    return slots + extra
