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

CACHE = ROOT / "output" / "judge_cache"
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


OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")


def backend() -> str:
    return os.environ.get("LP_JUDGE", "").lower()


def enabled() -> bool:
    return backend() in ("claude", "ollama")


@lru_cache(maxsize=1)
def _edges() -> Dict:
    raw = json.loads((ROOT / "data" / "chapter1_kg.json").read_text(encoding="utf-8"))
    return {(e["source"], e["level"]): e for e in raw["edges"] if e.get("type") == "has_level"}


def ladder_text(cid: str) -> str:
    """The concept's has_level edges L0-L4: each way's exact rule (L0: the
    everyday or wrong reading only) and the boundaries."""
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
        for b in bounds[:2]:
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


def build_prompt(text: str, question: str, code: str, facts: List[str], concepts: List[str]) -> str:
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
        sp.write_text(SYSTEM, encoding="utf-8")
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
            "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}]}
    req = urllib.request.Request(f"{OLLAMA_URL}/api/chat", data=json.dumps(body).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=1200) as r:
        return json.loads(r.read().decode("utf-8"))["message"]["content"]


def judge(prompt: str) -> Dict:
    """{"concepts": [...]} for the prompt; cached by its hash."""
    CACHE.mkdir(parents=True, exist_ok=True)
    local = backend() == "ollama"
    key = ("ollama:" + (os.environ.get("LP_JUDGE_MODEL") or "qwen3:14b") + "|" if local else "") + SYSTEM + prompt
    f = CACHE / (hashlib.sha256(key.encode("utf-8")).hexdigest()[:24] + ".json")
    if f.exists():
        return json.loads(f.read_text(encoding="utf-8"))
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
    m = re.search(r"\{.*\}", txt, re.S)
    try:
        out = json.loads(m.group(0)) if m else {"concepts": []}
    except json.JSONDecodeError:
        out = {"concepts": [], "unparsed": txt[:500]}
    f.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    return out


def levels(j: Dict, concepts: List[str]) -> Dict[str, Dict]:
    """concept -> the judge's item, for the levels it gave (not "none")."""
    out = {}
    for item in j.get("concepts", []):
        if item.get("concept") in concepts and str(item.get("level")) in LEVELS:
            out[item["concept"]] = item
    return out
