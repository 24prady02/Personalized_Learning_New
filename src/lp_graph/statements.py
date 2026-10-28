"""Step 1 of the pipeline - split code, question and answer into statements.

* **Code**: ``execution.parse`` gives one statement per simple statement or
  header; concepts come from the code-cue regexes (``CUES[c]["code"]``) and
  the declared types; static checks add decisive concepts (a declaration
  without initializer that is later read is tagged ``definite_assignment``).
  One extra *result* statement carries the run: the output, or the compile /
  run error.
* **Question**: spaCy sentences of the asked part, a question type by rules
  (``output | explain | why | fix``) and concepts by aliases.
* **Answer**: spaCy sentences split further into clauses (on so / because /
  but / then / whereas); per clause the concepts (aliases with a one-edit
  spelling tolerance on words of >=5 letters, code variable names -> the
  concepts of their declaration, "it" -> the last named variable), slots,
  negation and linking words.

spaCy (``en_core_web_sm``) only splits and parses; without it a regex
splitter gives the same statements for ordinary punctuation.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import TYPE_CHECKING

from . import lexicon
from .execution import CodeStmt, Trace, parse, variables
from .slots import Mention, Slot, extract_slots, find_mentions, implied_slots, normalize

if TYPE_CHECKING:  # pragma: no cover
    from .graph import KG

log = logging.getLogger(__name__)

_TYPE_CONCEPT = {"int": "int", "double": "double", "boolean": "boolean", "char": "char",
                 "long": "long_type", "String": "string_type", "float": "double"}


@dataclass(frozen=True)
class Statement:
    """One statement of code, question or answer."""

    id: str
    source: str               # code | question | answer
    text: str
    concepts: tuple[str, ...]
    slots: tuple[Slot, ...] = ()
    negated: bool = False
    link_words: tuple[str, ...] = ()
    order: int = 0
    sentence: int = 0
    variables: tuple[str, ...] = ()     # code variables named (after pronoun resolution)
    direct: tuple[str, ...] = ()        # concepts named by an alias in the text itself
    qtype: str = ""
    is_result: bool = False
    meta: dict = field(default_factory=dict, compare=False, hash=False)

    def short(self) -> str:
        return self.text if len(self.text) <= 60 else self.text[:57] + "..."


@dataclass(frozen=True)
class CodeContext:
    """What answer reading needs to know about the code."""

    stmts: tuple[CodeStmt, ...]
    var_types: dict
    var_concepts: dict        # variable -> concepts of its declaration (+ decisive)
    code_concepts: tuple[str, ...]
    printed_vars: tuple[str, ...]


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
        return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    out: list[str] = []
    for s in (x.text.strip() for x in nlp(text).sents):
        if not s:
            continue
        # the small model sometimes splits before "so"; a sentence ends at . ! ?
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
    words = "|".join(lexicon.CLAUSE_SPLIT)
    parts = re.split(rf"(?:,\s*|;\s*|\s+)(?=(?:{words})\b)", sentence, flags=re.I)
    out = []
    for p in parts:
        p = p.strip(" ,;")
        if re.fullmatch(rf"(?:{words})\.?", p, flags=re.I) or not p:
            continue
        out.append(p)
    return out


# -------------------------------------------------------------------- code

def code_context(kg: "KG", code_program: str, trace: Trace | None) -> CodeContext:
    stmts = tuple(parse(code_program)) if code_program else ()
    types = variables(list(stmts))
    var_concepts: dict[str, list[str]] = {}
    for s in stmts:
        for typ, name, _ in s.declares:
            cs = ["declaration", "variable"]
            base = typ.replace("[]", "")
            if base in _TYPE_CONCEPT:
                cs.append(_TYPE_CONCEPT[base])
            if typ.endswith("[]"):
                cs.append("array_declaration")
            var_concepts.setdefault(name, cs)
    decisive = _decisive(trace)
    for f in (trace.findings if trace else ()):
        if f.variable and f.variable in var_concepts and f.pattern in lexicon.DECISIVE:
            var_concepts[f.variable].append(lexicon.DECISIVE[f.pattern])
    concepts = sorted({c for s in stmts for c in code_concepts(kg, s)} | set(decisive.values()))
    printed = tuple(dict.fromkeys(s.printed.strip() for s in stmts
                                  if s.kind == "print" and s.printed and s.printed.strip() in types))
    return CodeContext(stmts, types, {k: tuple(sorted(set(v), key=v.index))
                                      for k, v in var_concepts.items()},
                       tuple(c for c in concepts if c in kg.knowledge.concepts), printed)


def _decisive(trace: Trace | None) -> dict[int, str]:
    out: dict[int, str] = {}
    for f in (trace.findings if trace else ()):
        if f.pattern in lexicon.DECISIVE:
            out.setdefault(f.stmt_index, lexicon.DECISIVE[f.pattern])
    return out


def code_concepts(kg: "KG", s: CodeStmt) -> list[str]:
    """Concepts a code statement shows (code-cue regexes + declared types)."""
    from .execution import mask_literals

    masked = mask_literals(s.text)
    found = []
    for cid in kg.concepts:
        for rx in kg.cues.get(cid, {}).get("code", []):
            target = s.text if cid in ("string_literal", "string_concatenation", "char",
                                       "escape_sequences") else masked
            if re.search(rx, target):
                found.append(cid)
                break
    for typ, _, _ in s.declares:
        base = typ.replace("[]", "")
        if base in _TYPE_CONCEPT:
            found.append(_TYPE_CONCEPT[base])
    if s.kind == "print" and "println" in found and "print" in found:
        found.remove("print")
    return sorted(set(c for c in found if c in kg.knowledge.concepts))


def code_statements(kg: "KG", ctx: CodeContext, trace: Trace | None) -> list[Statement]:
    """One statement per code statement + one result statement."""
    decisive = _decisive(trace)
    uninit_decl = {f.variable for f in (trace.findings if trace else ())
                   if f.pattern == "uninitialized_read"}
    out: list[Statement] = []
    for s in ctx.stmts:
        if s.kind == "close":
            continue
        cs = set(code_concepts(kg, s))
        slots: list[Slot] = []
        for typ, name, has_init in s.declares:
            if not has_init:
                slots.append(Slot("value", "none", False, f"var:{name}"))
                if name in uninit_decl:
                    cs.add("definite_assignment")
        if s.index in decisive:
            cs.add(decisive[s.index])
        k = len(out) + 1
        out.append(Statement(
            id=f"k{k}", source="code", text=s.text, concepts=tuple(sorted(cs)),
            slots=tuple(slots), order=len(out),
            variables=tuple(sorted({n for _, n, _ in s.declares} | set(s.reads) | set(s.assigns))),
            direct=tuple(sorted(cs)),
            meta={"kind": s.kind, "line": s.line, "reads": list(s.reads),
                  "declares": [list(d) for d in s.declares]}))
    if trace is not None and (trace.run.available or trace.run.error_kind):
        out.append(result_statement(trace, len(out), decisive))
    return out


def result_statement(trace: Trace, order: int, decisive: dict[int, str]) -> Statement:
    run = trace.run
    slots: list[Slot] = []
    cs: set[str] = set()
    if run.error_kind == "compile":
        text = f"compile error: {run.error}"
        slots.append(Slot("compile", "compile_error"))
        slots.append(Slot("error_time", "compile"))
        cs.add("compile_time_error")
        m = re.search(r"variable (\w+) might not have been initialized", run.error)
        if m:
            slots.append(Slot("value", "none", False, f"var:{m.group(1)}"))
    elif run.error_kind == "run":
        text = f"run-time error: {run.error}"
        slots += [Slot("compile", "compiles"), Slot("crash", "run_error"), Slot("error_time", "run")]
        cs.add("run_time_error")
    elif run.error_kind == "timeout":
        text = "runs without stopping (timeout)"
        slots += [Slot("compile", "compiles"), Slot("runs", "endless")]
        cs.add("infinite_loop")
    else:
        shown = run.output.strip().replace("\n", " | ")
        text = f"output: {shown}" if shown else "output: (nothing)"
        slots += [Slot("compile", "compiles"), Slot("crash", "no_error"),
                  Slot("output", run.output.strip())]
    cs |= set(decisive.values())
    return Statement(id="kr", source="code", text=text, concepts=tuple(sorted(cs)),
                     slots=tuple(slots), order=order, is_result=True,
                     direct=tuple(sorted(cs)),
                     meta={"run_available": run.available, "error_kind": run.error_kind})


# ---------------------------------------------------------------- question

def question_type(text: str) -> str:
    t = normalize(text)
    for qtype, words in lexicon.QUESTION_TYPES:
        if any(re.search(rf"(?<!\w){re.escape(w)}(?!\w)", t) for w in words):
            return qtype
    return "explain"


def question_statements(kg: "KG", question: str, ctx: CodeContext) -> list[Statement]:
    qtype = question_type(question)
    out = []
    for i, sent in enumerate(sentences(question)):
        norm = normalize(sent)
        mentions = collapse(find_mentions(norm, kg.alias_index, tuple(ctx.var_types)), ctx)
        cs, direct, vars_named = _resolve(mentions, ctx, None)
        out.append(Statement(id=f"q{i + 1}", source="question", text=sent,
                             concepts=cs, order=i, sentence=i, variables=vars_named,
                             direct=direct, qtype=qtype))
    return out


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


def _resolve(mentions: list[Mention], ctx: CodeContext,
             pronoun_var: str | None) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """Concepts of a clause: aliases (already collapsed) + variables' concepts."""
    direct = [m.concepts[0] for m in mentions if not m.var and m.concepts]
    vars_named = [m.var for m in mentions if m.var]
    if pronoun_var:
        vars_named.append(pronoun_var)
    via_vars = [c for v in vars_named for c in ctx.var_concepts.get(v, ())]
    concepts = sorted(set(direct) | set(via_vars))
    return tuple(concepts), tuple(sorted(set(direct))), tuple(sorted(set(vars_named)))


def _pronoun(norm: str) -> bool:
    return any(re.search(rf"(?<!\w){re.escape(p)}(?!\w)", norm) for p in lexicon.PRONOUNS)


def answer_statements(kg: "KG", answer: str, ctx: CodeContext) -> list[Statement]:
    """Clauses of the answer with concepts, slots, negation and link words."""
    out: list[Statement] = []
    last_var: str | None = None
    fallback_var = (ctx.printed_vars[-1] if ctx.printed_vars
                    else (list(ctx.var_types)[-1] if ctx.var_types else None))
    for si, sent in enumerate(sentences(answer)):
        for clause in clauses(sent):
            norm = normalize(clause)
            mentions = collapse(find_mentions(norm, kg.alias_index, tuple(ctx.var_types),
                                             fuzzy=True), ctx)
            named = [m.var for m in mentions if m.var]
            pron = None
            if _pronoun(norm):
                pron = last_var or fallback_var
            cs, direct, vars_named = _resolve(mentions, ctx, pron)
            slots = extract_slots(norm, mentions, resolve_pronoun=pron)
            slots = _attach_printed_value(slots, ctx, vars_named)
            slots = slots + implied_slots(slots)
            words = norm.split()
            links = tuple(w for w in lexicon.LINK_WORDS if w in words)
            negated = (any(w in lexicon.NEGATION for w in words) or _spacy_negated(clause))
            out.append(Statement(
                id=f"c{len(out) + 1}", source="answer", text=clause, concepts=cs,
                slots=tuple(sorted(slots, key=lambda s: (s.span, s.key()))),
                negated=negated, link_words=links, order=len(out), sentence=si,
                variables=vars_named, direct=direct))
            if named:
                last_var = named[-1]
            elif pron:
                last_var = pron
    return out


def _attach_printed_value(slots: list[Slot], ctx: CodeContext,
                          vars_named: tuple[str, ...]) -> list[Slot]:
    """"It prints 0" when the code prints one variable also says that
    variable's value is 0 (an implied value slot)."""
    extra = []
    for s in slots:
        if s.name != "output" or s.negated or not ctx.printed_vars:
            continue
        var = next((v for v in vars_named if v in ctx.printed_vars), None)
        if var is None and len(ctx.printed_vars) == 1:
            var = ctx.printed_vars[0]
        if var and not any(x.name == "value" and x.subject == f"var:{var}" for x in slots):
            extra.append(Slot("value", s.value, False, f"var:{var}", True, s.span))
    return slots + extra
