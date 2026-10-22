"""
judge.py — the sentence judge: Claude reads a student answer against the
has_level edge logic of its concepts (the ways and boundaries of L0-L4 from the
Chapter-1 graph) and says which way each concept's part of the answer shows,
and whether its reasoning is right.

It replaces the NLI model as the reader of explanations. It adds no rules: its
prompt is the graph's edge logic, and the code run's verdicts are given to it as
facts. The engine then fuses its levels with the rest (engine.py, _fuse).

Two backends, chosen by the environment variable LP_JUDGE:
  claude   Claude Code in headless mode (`claude -p`), on the user's subscription
  ollama   a local open-source model through Ollama (free, private, repeatable:
           temperature 0, fixed seed); LP_JUDGE_MODEL names it (default qwen3:14b)
Replies are cached by the hash of the prompt (output/judge_cache); local models'
replies are cached under their own key, so the backends never mix.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

from . import models
from .knowledge import ROOT, PercptKnowledge

CACHE = ROOT / "output" / os.environ.get("LP_JUDGE_CACHE", "judge_cache")   # LP_JUDGE_CACHE: a fresh folder forces live calls
LEVELS = ("L0", "L1", "L2", "L3", "L4")
LEVEL_NAMES = {"L0": "Prestructural", "L1": "Unistructural", "L2": "Multistructural",
               "L3": "Relational", "L4": "Extended abstract"}

SYSTEM = """You grade one student answer about Java on a 5-level learning ladder (L0-L4), for given concepts.
You are given, for each concept, the WAYS of reaching each level, taken from a knowledge graph. Use only them.
Rules:
- The level is the highest level whose way the answer actually shows, with correct content.
- L0 if the answer's reasoning states or uses a rule that contradicts Java (an everyday reading or a wrong rule listed under L0), even if it uses Java words. A wrong explanation is not L1-L4.
- L1: names the element or states one correct rule, not applied to this code.
- L2: applies the rules correctly to this code (values, trace, output). A bare result with no reasoning is L1.
- L3: correctly relates parts (why, purpose, relation to another concept) as the L3 ways say.
- L4: correctly reasons beyond the given code (a change, a new input, diagnosing an error, new code) as the L4 ways say.
- Respect each level's boundary text.
- FACTS FROM RUNNING THE CODE are certain: a value the run contradicts is wrong.
- If the answer says nothing about a concept, give "none".
Return JSON only: {"concepts":[{"concept":"<id>","level":"L0|L1|L2|L3|L4|none","way":"<way name>","quote":"<words from the answer>","correct":true|false,"why":"<one short sentence>"}]}"""

# LP_JUDGE_PROMPT=rubric: the graph's level definitions, deciding questions and boundary
# rules as one rubric, and one overall level for the answer as a whole (its own cache keys)
RUBRIC_SYSTEM = """You are an experienced Java teacher. You give the level one student answer shows on a 5-level learning ladder (L0-L4), or "none" if it makes no claim.
Work out what the code really does (FACTS FROM RUNNING THE CODE and its RUN OUTPUT are certain) and whether the student's reasoning is correct before you decide. Mark the answer as a whole, for the main thing the question part asks. Use only the definitions and rules below and the concepts' ways.

L0 Prestructural: no working model of the concept: reads the code with everyday or maths meanings, applies a documented wrong rule, or traces accurately only now and then. Deciding question: does every rule the answer applies agree with the language rule? A slip in an otherwise rule-correct trace is L2 with an error, not L0.
L1 Unistructural: one correct aspect: names or describes one part of the given code, or states the rule, without covering all parts or applying the rule to the values. Deciding question: does it cover every part of the code, in order, with the values (L2)? One part or only the rule is L1.
L2 Multistructural: covers all parts of the code that use the concept, line by line or value by value, without relating them to what the code is for. May be correct or a multistructural error. Deciding question: many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)?
L3 Relational: integrates the parts into one structure: relates the concept to another construct in the same code, or states in one sentence what the code does, deduced from the code. May be correct or a relational error. Deciding question: was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does it stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?
L4 Extended abstract: goes beyond the given code with the rule: predicts a change by reasoning about what is conserved, states the class of inputs under which an error shows, or solves an unseen problem. Re-tracing changed code value by value is L2; fixing one given failing case is L3.

Boundary rules:
- Reading the code with everyday meanings, or using a rule that contradicts Java, is L0, even with Java words.
- Copying the code back word for word with no interpretation is L0.
- A single slip in an otherwise rule-correct trace is L2 with an error, not L0.
- Naming the element, or stating one correct rule or definition without applying it to this code, is L1.
- A bare correct result or output with no justification is L1.
- Applying the rules to this code's values or lines, in order, with justification, is L2.
- Relating the concept to another construct, or stating the purpose of the code, with a reason, is L3 (correct or a relational error).
- Locating and fixing the mistake for one given failing case is L3.
- Correct reasoning about code, an input or a change that is NOT in the given code (predicting the effect of a change, diagnosing a class of error, writing correct new code) is L4. New code must be correct to be L4.
- A student's question that makes no claim is not levelled: "none".

Return JSON only: {"answer_level":"L0|L1|L2|L3|L4|none","main_concept":"<id of the concept the question part is about>","why":"<one sentence>","concepts":[{"concept":"<id>","level":"L0|L1|L2|L3|L4|none","way":"<way name>","quote":"<words from the answer>","correct":true|false,"why":"<one short sentence>"}]}"""


# LP_JUDGE_EDGES=1 (with the rubric): the judge reads the graph's edge logic itself: each has_level
# edge's logic, every way with its id, edge logic and boundary, and the prerequisite, parallel and
# misconception edges of the concepts; it names the way id the answer meets (its own cache keys)
EDGES_RULES = """

The concepts' ways are the has_level edges of a knowledge graph. For each concept, pick the way whose EDGE LOGIC the answer actually meets, and give its id (e.g. "remainder_operator@L2#1"); respect that way's boundary. An L3 way that relates the concept to another construct must match one of the GRAPH EDGES listed (prerequisite or parallel) and its logic. A reasoning that matches a MISCONCEPTION edge's wrong rule is L0 for that concept.
"""


def rubric() -> bool:
    return os.environ.get("LP_JUDGE_PROMPT", "").lower() == "rubric"


def pick_mode() -> bool:
    return os.environ.get("LP_LINK_PICK") == "1"


def edges_mode() -> bool:
    return rubric() and os.environ.get("LP_JUDGE_EDGES") == "1"


def relations_mode() -> bool:
    return edges_mode() and os.environ.get("LP_JUDGE_RELATIONS") == "1"


# LP_JUDGE_RELATIONS=1 (with the edges judge): a prerequisite or parallel edge between two of the
# concepts is the student's own only when the answer states that relation; the judge says which
RELATIONS_RULES = """
For each RELATION EDGE listed, say whether the student's own words state that relation between the two concepts (as the edge's logic describes it), and quote those words. Two concepts merely mentioned, or each explained separately, is not stated.
"""


def system() -> str:
    if edges_mode():
        head, schema = RUBRIC_SYSTEM.rsplit("\n\nReturn JSON only:", 1)
        schema = schema.replace('"way":"<way name>"', '"way":"<way name>","way_id":"<concept@Lk#n>"')
        if relations_mode():
            schema = (schema[:schema.rindex("]}")] + '],"relations":[{"edge":"<source -type-> target>",'
                      '"stated":true|false,"quote":"<words from the answer that state it, or empty>"}]}')
            return head + EDGES_RULES + RELATIONS_RULES + "\nReturn JSON only:" + schema
        return head + EDGES_RULES + "\nReturn JSON only:" + schema
    return RUBRIC_SYSTEM if rubric() else SYSTEM


OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")


def backend() -> str:
    return os.environ.get("LP_JUDGE", "").lower()


def enabled() -> bool:
    return backend() in ("claude", "ollama")


@lru_cache(maxsize=1)
def _edges() -> Dict:
    raw = json.loads((ROOT / "data" / "chapter1_kg.json").read_text(encoding="utf-8"))
    return {(e["source"], e["level"]): e for e in raw["edges"] if e.get("type") == "has_level"}


@lru_cache(maxsize=1)
def _graph_edges() -> List[Dict]:
    raw = json.loads((ROOT / "data" / "chapter1_kg.json").read_text(encoding="utf-8"))
    return [e for e in raw["edges"] if e.get("type") in ("prerequisite", "parallel", "misconception", "error")]


def _clip(s: str, n: int) -> str:
    s = re.sub(r"\s+", " ", s or "").strip()
    return s if len(s) <= n else s[:n].rstrip() + "..."


def edge_ladder_text(cid: str) -> str:
    """Edges mode: the concept's has_level edges L0-L4 as the graph has them: the edge's
    logic, then every way with its id, rule type, edge logic and boundary."""
    out = [f"### Concept: {cid}"]
    for lv in LEVELS:
        e = _edges().get((cid, lv))
        if not e:
            continue
        out.append(f"{lv} {LEVEL_NAMES[lv]} -- edge {cid} -has_level-> {cid}@{lv}: {_clip(e.get('logic', ''), 160)}")
        seen = set()
        for k, w in enumerate(e["ways"], 1):
            if w["way"] == "inconsistent_trace" or k > 6:
                continue
            logic = w.get("edge_logic") or w.get("exact_rule", "")
            b = w.get("boundary", "")
            out.append(f"  - {cid}@{lv}#{k} {w['way']} [{w.get('rule_type', '')}]: {_clip(logic, 200)}"
                       + (f" (boundary: {_clip(b, 120)})" if b and b not in seen else ""))
            seen.add(b)
    return "\n".join(out)


def graph_edges_text(concepts: List[str]) -> str:
    """Edges mode: the prerequisite, parallel, misconception and error edges of the concepts,
    each with its logic (misconceptions: the wrong rule and the right rule)."""
    out = []
    for cid in concepts:
        rel = [e for e in _graph_edges() if e["type"] in ("prerequisite", "parallel") and cid in (e["source"], e["target"])]
        mis = [e for e in _graph_edges() if e["type"] in ("misconception", "error") and e["source"] == cid]
        lines = [f"  {e['source']} -{e['type']}-> {e['target']}: {_clip(e.get('logic', ''), 170)}" for e in rel[:8]]
        lines += [f"  {cid} -{e['type']}-> {e['target']}: wrong rule: {_clip(e.get('logic', ''), 140)}"
                  + (f" | right rule: {_clip(e['twin_logic'], 120)}" if e.get("twin_logic") else "") for e in mis[:4]]
        if lines:
            out.append(f"{cid}:\n" + "\n".join(lines))
    return "\n".join(out)


def ladder_text(cid: str) -> str:
    """The concept's has_level edges L0-L4: each way's exact rule (L0: the
    everyday or wrong reading only) and the boundaries."""
    if edges_mode():
        return edge_ladder_text(cid)
    out = [f"### Concept: {cid}"]
    for lv in LEVELS:
        e = _edges().get((cid, lv))
        if not e:
            continue
        out.append(f"{lv} {LEVEL_NAMES[lv]}:")
        bounds: List[str] = []
        for w in e["ways"][:6 if lv == "L0" else 4]:
            if w["way"] == "inconsistent_trace":
                continue
            rule = re.sub(r"\s+", " ", w.get("exact_rule", ""))
            if lv == "L0":
                rule = rule.split("Right rule:")[0].split("Java rule:")[0].split("In Java,")[0]
            out.append(f"  - {w['way']}: {rule[:230]}")
            b = w.get("boundary", "")
            if b and b not in bounds:
                bounds.append(b)
        for b in ([] if rubric() else bounds[:2]):     # the rubric states the boundaries once, for all concepts
            out.append(f"  boundary: {b[:200]}")
    return "\n".join(out)


def extra_concept(text: str, kg: PercptKnowledge, have) -> List[str]:
    """The concept whose L1-L4 way rules are closest to the answer and not yet
    linked (the answer-graph candidate)."""
    rules, owner = [], []
    for cid, c in kg.concepts.items():
        for lv in ("L1", "L2", "L3", "L4"):
            for w in c.ways.get(lv, []):
                for r in w.rules:
                    rules.append(r); owner.append(cid)
    sim = models.similarity([text], rules)
    if sim is None:
        return []
    for j in sim[0].argsort()[::-1]:
        if owner[j] not in have:
            return [owner[j]]
    return []


def relation_edges(concepts: List[str]) -> List[Dict]:
    """The prerequisite and parallel edges with both ends among the concepts."""
    cs = set(concepts)
    return [e for e in _graph_edges() if e["type"] in ("prerequisite", "parallel")
            and e["source"] in cs and e["target"] in cs]


def build_prompt(text: str, question: str, code: str, facts: List[str], concepts: List[str],
                 run_output: Optional[str] = None) -> str:
    if rubric():
        return (f"QUESTION (part asked): {question}\n\nCODE:\n{(code or '(none)')[:1500]}\n\n"
                f"RUN OUTPUT: {(run_output or '(not run: no runnable code, or it needs input)')[:600]}\n\n"
                f"STUDENT ANSWER: {text}\n\nFACTS FROM RUNNING THE CODE:\n"
                + ("\n".join(facts) if facts else "(no claim of the answer could be checked by running the code)")
                + "\n\nCONCEPTS AND THEIR WAYS:\n\n" + "\n\n".join(ladder_text(c) for c in concepts)
                + (f"\n\nGRAPH EDGES OF THESE CONCEPTS:\n{graph_edges_text(concepts)}" if edges_mode() else "")
                + ("\n\nRELATION EDGES BETWEEN THESE CONCEPTS:\n" + ("\n".join(
                    f"  {e['source']} -{e['type']}-> {e['target']}: {_clip(e.get('logic', ''), 170)}"
                    for e in relation_edges(concepts)) or "  (none)") if relations_mode() else "")
                + f"\n\nGive the answer's overall level, its main concept, and a level for each concept: {', '.join(concepts)}."
                + (" For each concept give the id of the way it meets." if edges_mode() else "")
                + (" For each relation edge say whether the student states it." if relations_mode() and relation_edges(concepts) else "")
                + (" The concepts are a shortlist of candidates: give a level only to the concepts the student's own "
                   "statements or reasoning are about, and \"none\" to every other one." if pick_mode() else ""))
    return (f"QUESTION (part asked): {question}\n\nCODE:\n{(code or '(none)')[:1500]}\n\n"
            f"STUDENT ANSWER: {text}\n\nFACTS FROM RUNNING THE CODE:\n"
            + ("\n".join(facts) if facts else "(no claim of the answer could be checked by running the code)")
            + "\n\nCONCEPTS AND THEIR WAYS:\n\n" + "\n\n".join(ladder_text(c) for c in concepts)
            + f"\n\nGrade the answer for each concept: {', '.join(concepts)}.")


def _call_claude(prompt: str) -> str:
    import shutil
    exe = shutil.which("claude.cmd") or shutil.which("claude") or "claude"
    model = os.environ.get("LP_JUDGE_MODEL")
    # run outside the repository so the judge sees nothing but the prompt
    with tempfile.TemporaryDirectory() as tmp:
        sp = Path(tmp) / "system.txt"
        sp.write_text(system(), encoding="utf-8")
        cmd = [exe, "-p", "--output-format", "json", "--tools", "", "--no-session-persistence",
               "--system-prompt-file", str(sp)] + (["--model", model] if model else [])
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8",
                           cwd=tmp, timeout=600)
    if r.returncode != 0:
        raise RuntimeError(f"claude -p failed: {r.stderr[:300]}")
    return json.loads(r.stdout).get("result", "")


def _call_ollama(prompt: str) -> str:
    import urllib.request
    model = os.environ.get("LP_JUDGE_MODEL") or "qwen3:14b"
    body = {"model": model, "stream": False, "format": "json", "think": False,
            "options": {"temperature": 0, "seed": 1, "num_ctx": 8192},
            "messages": [{"role": "system", "content": system()}, {"role": "user", "content": prompt}]}
    req = urllib.request.Request(f"{OLLAMA_URL}/api/chat", data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1200) as r:
        return json.loads(r.read().decode("utf-8"))["message"]["content"]


def judge(prompt: str) -> Dict:
    """{"concepts": [...]} for the prompt; cached by its hash."""
    CACHE.mkdir(parents=True, exist_ok=True)
    local = backend() == "ollama"
    key = ("ollama:" + (os.environ.get("LP_JUDGE_MODEL") or "qwen3:14b") + "|" if local else "") + system() + prompt
    f = CACHE / (hashlib.sha256(key.encode("utf-8")).hexdigest()[:24] + ".json")
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
    # LP_JUDGE_DRYRUN=1: count the prompts that would need a call, without calling
    if os.environ.get("LP_JUDGE_DRYRUN") == "1":
        with (CACHE.parent / "judge_dryrun_misses.txt").open("a", encoding="utf-8") as fh:
            fh.write(f"{f.name}\t{len(system()) + len(prompt)}\n")     # file, prompt size in characters
        return {"concepts": [], "unavailable": "dry run: not in cache"}
    # retry: the CLI can be briefly missing (Claude Code updating itself) or busy;
    # if it still fails, the answer is graded without the judge (not cached)
    import time
    txt = None
    for wait in (0, 10, 30, 90):
        time.sleep(wait)
        try:
            txt = _call_ollama(prompt) if local else _call_claude(prompt)
            break
        except (RuntimeError, OSError, KeyError, subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            err = str(e)[:200]
    if txt is None:
        return {"concepts": [], "unavailable": err}
    out = _parse_reply(txt)
    f.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    return out


def _parse_reply(txt: str) -> Dict:
    """The JSON object(s) in the reply. Claude sometimes splits its answer into two objects
    ({"answer_level":...}{"concepts":[...]}) or repeats it: the first value of each key is kept
    and the concept lists are joined (a concept already given is not repeated)."""
    dec, out, i = json.JSONDecoder(), {}, 0
    while True:
        i = txt.find("{", i)
        if i < 0:
            break
        try:
            obj, end = dec.raw_decode(txt, i)
        except json.JSONDecodeError:
            i += 1
            continue
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == "concepts" and isinstance(v, list):
                    seen = {c.get("concept") for c in out.get("concepts", []) if isinstance(c, dict)}
                    out.setdefault("concepts", []).extend(
                        c for c in v if not (isinstance(c, dict) and c.get("concept") in seen))
                else:
                    out.setdefault(k, v)
        i = end
    if not out:
        return {"concepts": [], "unparsed": txt[:2000]}
    out.setdefault("concepts", [])
    return out


def levels(j: Dict, concepts: List[str]) -> Dict[str, Dict]:
    """concept -> the judge's item, for the levels it gave (not "none")."""
    out = {}
    for item in j.get("concepts", []):
        if item.get("concept") in concepts and str(item.get("level")) in LEVELS:
            out[item["concept"]] = item
    return out
