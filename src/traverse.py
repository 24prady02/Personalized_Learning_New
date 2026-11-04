"""ToG traversal over the Stage 1 subgraph (Stage 2).

Inputs: G = data/processed/<sid>_subgraph.json; the scenario (code, question, answer) from data/raw/scenarios_20.json;
the "traversal" block of experiments/config.json (width N, depth D, model, prune_tools, ...).
Output: data/processed/<sid>_diagnosis.json.

    python src/traverse.py S007                       # one scenario
    python src/traverse.py S007 --prune-tools bm25    # rank edges by similarity instead of the prune prompt
    python src/traverse.py --all                      # every scenario in the file

The LLM is used in two places only: edge pruning (replaceable by BM25 / sentence-BERT) and edge labelling. Start
concepts, the stop decision and the levels are read from the graph by rule.

Part 1 builds lookups from G (ToG's SPARQL server); each way of a has_level edge becomes an edge of its own
(lvl:<concept>@<L>#i, logic = the way's exact rule), so levels are searched like everything else. Part 2 splits the
answer into clauses and selects at most N start concepts, with no model call: Stage 1's tagged (non-generic)
concepts, the given topic entities that ToG's released code reads from the dataset, plus a generic concept whose
tagging text the answer repeats (e.g. "=" for assignment); more than N of them are ranked by BM25 of the answer
against each concept's text. Part 3 is the main loop: edge search (no LLM; depth 1 = misconception / error edges and
level ways, deeper = prerequisite / parallel edges in the same piece), edge prune (LLM or bm25/sentencebert, each
family to N on its own), target lookup, edge label (LLM, quote checked against the answer: held / correct for a
misconception edge, confirmed / broken for a concept edge, shown for a level way), keep the best N in tiers (held
misconception / broken edge first, then held errors, then correct / confirmed / shown), stop test, next nodes. Every
labelled candidate whose quote is in the answer is recorded as evidence, kept or not. The stop test is a rule, no
model call: (i) graph check, a held or broken concept with unexamined prerequisites in G sends the walk one hop
back; (ii) clause coverage, stop when the quote of some evidence edge covers every clause. Part 4 diagnoses: held
misconceptions (a held error beside a held misconception on the same concept is evidence, not a second diagnosis),
broken edges, root cause along prerequisite edges, level per concept by rule (L0 when a misconception is held or an
L0 way is shown, otherwise the highest level with a shown way), overall level, and the clauses no evidence covers.
The LLM never answers from its own knowledge: every label is tied to an edge of G and a quote.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import prompts
from utils import PROCESSED_DIR, ROOT, SCENARIOS_PATH, load_config, load_scenarios

DEFAULT_TRAVERSAL = {
    "width": 3, "depth": 3, "temperature": 0, "max_output": 256,
    "prune_tools": "llm", "backend": "claude-cli", "model": "claude-opus-5-5",
    "few_shot_scenario": "S000", "cache_dir": "experiments/llm_cache",
}

STEPS = ("prune", "label")   # the only places the model is asked


# ====================================================================== LLM client

class LLM:
    """One place that calls the model. Backends: 'anthropic' (SDK) or 'claude-cli' (the claude CLI, `claude -p`).
    Replies are cached on disk by prompt hash so a re-run is deterministic and free."""

    def __init__(self, cfg: dict[str, Any]):
        self.cfg = cfg
        self.calls = 0
        self.cache_hits = 0
        self.asks_by_step: Counter = Counter()   # every prompt sent, by traversal step (cached or not)
        self.cache_dir = ROOT / cfg.get("cache_dir", "experiments/llm_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.backend = cfg.get("backend", "claude-cli")
        self.model = cfg.get("model", "claude-opus-5-5")
        self._client = None
        if self.backend == "anthropic":
            import anthropic  # noqa: F401  (pip install anthropic)
            self._client = anthropic.Anthropic()

    def ask(self, prompt: str, step: str = "other") -> str:
        self.asks_by_step[step] += 1
        key = hashlib.sha256((self.backend + "|" + self.model + "|" + prompt).encode("utf-8")).hexdigest()[:24]
        f = self.cache_dir / f"{key}.json"
        if f.exists():
            self.cache_hits += 1
            return json.loads(f.read_text(encoding="utf-8"))["reply"]
        self.calls += 1
        reply = self._anthropic(prompt) if self.backend == "anthropic" else self._cli(prompt)
        f.write_text(json.dumps({"model": self.model, "backend": self.backend, "prompt": prompt, "reply": reply}, indent=1, ensure_ascii=False), encoding="utf-8")
        return reply

    def _anthropic(self, prompt: str) -> str:
        kwargs: dict[str, Any] = dict(model=self.model, max_tokens=max(int(self.cfg.get("max_output", 256)), 256),
                                      messages=[{"role": "user", "content": prompt}])
        # temperature is accepted only by models before the 4.6 generation; current models reject it (400).
        if self.cfg.get("temperature") is not None and not re.search(r"-(4-[6-9]|5(-\d)?)\b|fable|mythos", self.model):
            kwargs["temperature"] = self.cfg["temperature"]
        if re.search(r"opus-5|sonnet-5|haiku-5|fable|mythos", self.model):
            kwargs["output_config"] = {"effort": "low"}
        r = self._client.messages.create(**kwargs)
        if r.stop_reason == "refusal":
            return ""
        return "".join(b.text for b in r.content if b.type == "text")

    def _cli(self, prompt: str) -> str:
        cmd = ["claude", "-p", "--output-format", "text"]
        if self.model:
            cmd += ["--model", self.model]
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}  # allow running inside a Claude Code session
        # the CLI occasionally fails for a moment (its executable is swapped while it updates itself): retry briefly
        last = ""
        for attempt in range(3):
            r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8", timeout=180, env=env, shell=(os.name == "nt"))
            if r.returncode == 0:
                return r.stdout.strip()
            last = r.stderr.strip()[:300]
            time.sleep(5 * (attempt + 1))
        raise RuntimeError(f"claude CLI failed ({r.returncode}) after 3 attempts: {last}")


# ====================================================================== similarity prune tools (ToG's bm25 / sentencebert)

_TOKEN = re.compile(r"[A-Za-z_][A-Za-z_0-9]*|\d+|[^\sA-Za-z0-9_]")


def _tokens(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN.findall(text)]


def bm25_scores(query: str, docs: list[str], k1: float = 1.5, b: float = 0.75) -> list[float]:
    q = _tokens(query)
    toks = [_tokens(d) for d in docs]
    n = len(docs)
    avg = sum(len(t) for t in toks) / max(1, n)
    df: Counter = Counter()
    for t in toks:
        df.update(set(t))
    out = []
    for t in toks:
        tf = Counter(t)
        s = 0.0
        for w in q:
            if w not in tf:
                continue
            idf = math.log(1 + (n - df[w] + 0.5) / (df[w] + 0.5))
            s += idf * tf[w] * (k1 + 1) / (tf[w] + k1 * (1 - b + b * len(t) / max(avg, 1)))
        out.append(s)
    return out


_sbert = None


def sbert_scores(query: str, docs: list[str]) -> list[float]:
    global _sbert
    from sentence_transformers import SentenceTransformer, util
    if _sbert is None:
        _sbert = SentenceTransformer("all-MiniLM-L6-v2")
    e = _sbert.encode([query] + docs, convert_to_tensor=True, normalize_embeddings=True)
    return util.cos_sim(e[0:1], e[1:])[0].tolist()


# ====================================================================== Part 1: lookups from G

class Graph:
    def __init__(self, sg: dict[str, Any]):
        self.sg = sg
        self.concepts = {c["id"]: c for c in sg["concepts"]}
        self.mis_by_concept: dict[str, list[dict]] = defaultdict(list)       # lookup 1
        for e in sg["mis_edges"]:
            self.mis_by_concept[e["source"]].append(e)
        self.cedges_by_concept: dict[str, list[dict]] = defaultdict(list)    # lookup 2
        for e in sg["concept_edges"]:
            self.cedges_by_concept[e["source"]].append(e)
            self.cedges_by_concept[e["target"]].append(e)
        self.mis_records = {m["id"]: m for m in sg["misconceptions"]}         # lookup 3
        self.piece_of: dict[str, int] = {}                                    # lookup 4
        for i, comp in enumerate(sg["components"]):
            for c in comp:
                self.piece_of[c] = i
        self.level_link: dict[tuple[str, str], str] = {}                      # lookup 5
        self.level_link_rule: dict[tuple[str, str], str] = {}                 # (concept, misconception) -> the L0 way's own text
        for l in sg["level_mis_links"]:
            concept = l["level_node"].split("@")[0]
            self.level_link.setdefault((concept, l["misconception"]), l["level_node"])
            if l.get("way") == "misconception" or (concept, l["misconception"]) not in self.level_link_rule:
                self.level_link_rule[(concept, l["misconception"])] = l.get("exact_rule") or ""
        self.levels = {l["id"]: l for l in sg["levels"]}
        # lookup 6: level ways as edges. Each way of a has_level edge becomes one edge concept -> level node, with the
        # way's exact rule as its logic, so the search can prune and label it like any other edge. Ways of kind
        # "misconception" are left out: they restate misconception edges, which the search already has.
        self.ways_by_concept: dict[str, list[dict]] = defaultdict(list)
        for le in sorted(sg["level_edges"], key=lambda x: (x["source"], x["level"])):
            rec = self.levels.get(le["target"], {})
            for i, w in enumerate(le.get("ways") or []):
                if (w.get("way") or "") == "misconception":
                    continue
                self.ways_by_concept[le["source"]].append({
                    "id": f"lvl:{le['target']}#{i}", "source": le["source"], "target": le["target"], "type": "level_way",
                    "level": le["level"], "level_name": rec.get("name", ""), "deciding_question": rec.get("deciding_question", ""),
                    "way": w.get("way"), "rule_type": w.get("rule_type_name") or w.get("rule_type"), "logic": w.get("exact_rule") or w.get("edge_logic") or ""})
        self.edge_by_id = {e["id"]: e for e in sg["mis_edges"] + sg["concept_edges"]}
        for ws in self.ways_by_concept.values():
            for e in ws:
                self.edge_by_id[e["id"]] = e

    def other_end(self, edge: dict, concept: str) -> str:
        return edge["target"] if edge["source"] == concept else edge["source"]

    def edge_text(self, e: dict) -> str:
        if e["id"].startswith(("mis:", "err:")):
            return f"{e['id']} | wrong rule: {e.get('logic') or ''} | right rule: {e.get('twin_logic') or ''}"
        if e["id"].startswith("lvl:"):
            return f"{e['id']} | level {e['level']} way {e['way']}: {e.get('logic') or ''}"
        return f"{e['id']} | rule: {e.get('logic') or ''}"


# ====================================================================== Part 2: start

_QUOTES = re.compile(r"[\"'“”‘’]")
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\s*;\s*")
_PAREN = re.compile(r"\(([^()]*\s[^()]*)\)")   # a remark of two or more words; "(double)" or "(x)" stays in its clause
_CONNECTIVE = re.compile(r"(?:,\s*|\s+)(?=(?:because|so)\b)", re.I)
_CLAUSE_STRIP = " ,.;:!?\n\t"


def split_clauses(answer: str) -> list[str]:
    """Clauses of the answer. Quote characters are removed first. Splits: sentence ends and ';'; before 'because' /
    'so' when a comma, a space or a (removed) closing quote precedes them; a parenthetical remark '(...)' becomes its
    own clause. '/' is kept inside a clause: in a written output it stands for a line break."""
    text = _QUOTES.sub("", answer)
    out: list[str] = []
    for sentence in _SENTENCE_SPLIT.split(text):
        for i, piece in enumerate(_PAREN.split(sentence)):   # odd indices are the insides of parentheses
            pieces = [piece] if i % 2 else _CONNECTIVE.split(piece)
            for p in pieces:
                p = p.strip(_CLAUSE_STRIP)
                if p:
                    out.append(p)
    return out


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def quote_in_answer(quote: str, answer: str) -> bool:
    q = _norm(quote)
    return bool(q) and q != "none" and q in _norm(answer)


def quotes_overlap(a: str, b: str) -> bool:
    """Two quotes point at the same words when one normalised quote contains the other."""
    na, nb = _norm(a), _norm(b)
    return bool(na) and bool(nb) and (na in nb or nb in na)


def mark_shared_evidence(held: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Every held misconception stays (a student can hold several at once). A held misconception on a concept whose
    quote points at the same words as a stronger one on that concept is marked ``shares_evidence_with`` that edge:
    the graph words one wrong idea in several ways, and the two then rest on the same words. Nothing is dropped."""
    out = sorted(held, key=lambda x: -x["score"])
    for i, c in enumerate(out):
        if c["kind"] != "misconception":
            continue
        for k in out[:i]:
            if k["kind"] == "misconception" and k["source"] == c["source"] and same_words(k, c):
                c["shares_evidence_with"] = k["edge"]
                break
    return out


def filed_at_dependent(held: list[dict[str, Any]], pre_in: dict[str, list[str]]) -> list[dict[str, Any]]:
    """The same misconception held at both ends of a prerequisite edge is one fault seen twice. It is filed at the
    dependent concept (the target of the edge), so the prerequisite end does not pose as a root cause of its own."""
    out = []
    for c in held:
        twins = [k for k in held if k["kind"] == c["kind"] == "misconception" and k["target"] == c["target"] and k["source"] != c["source"]]
        if any(c["source"] in pre_in.get(k["source"], []) for k in twins):
            continue
        out.append(c)
    return out


def shadowed(kept: list[dict[str, Any]], all_held: list[dict[str, Any]], pre_in: dict[str, list[str]], generic: set[str]) -> dict[str, str]:
    """Reconcile held misconception labels across concepts: edge id -> the edge it is a shadow of.

    Each concept is labelled on its own against the same clauses, so one wrong sentence lights up the misconception
    that states the student's claim at the specific concept and, beside it, a broader one on a prerequisite of that
    concept or on a generic concept (expression, statement) that names no rule of its own. The broader label rests
    on no words of its own, so it is a shadow of the specific one, not a second fault:
      * on a prerequisite (any number of prerequisite hops above the specific concept): its clauses are among the
        specific label's clauses and its confidence is no higher;
      * on a generic concept, against a label on a non-generic concept: its clauses are among that label's clauses.
    A shadow does not pose as a root cause and does not set its concept to L0. Only kept, non-shadow labels can cast
    a shadow (generic ones are tested first, then by rising confidence, so the specific finding is the one that stays)."""
    anc: dict[str, set[str]] = {}

    def ancestors(c: str) -> set[str]:
        if c not in anc:
            seen, stack = set(), list(pre_in.get(c, []))
            while stack:
                x = stack.pop()
                if x not in seen:
                    seen.add(x)
                    stack.extend(pre_in.get(x, []))
            anc[c] = seen
        return anc[c]

    def is_shadow(x: dict[str, Any], y: dict[str, Any]) -> bool:
        if x["edge"] == y["edge"] or not x.get("clauses") or not set(x["clauses"]) <= set(y.get("clauses") or []):
            return False
        if x["source"] in generic:
            return y["source"] not in generic
        return x["source"] in ancestors(y["source"]) and x["confidence"] <= y["confidence"]

    accepted = sorted(kept, key=lambda c: (0 if c["source"] in generic else 1, c["confidence"], c["score"]))
    out: dict[str, str] = {}
    for x in list(accepted):
        y = next((k for k in accepted if k["edge"] != x["edge"] and is_shadow(x, k)), None)
        if y is not None:
            out[x["edge"]] = y["edge"]
            accepted.remove(x)
    for x in all_held:
        if x["edge"] not in out and not any(k["edge"] == x["edge"] for k in accepted):
            y = next((k for k in accepted if is_shadow(x, k)), None)
            if y is not None:
                out[x["edge"]] = y["edge"]
    return out


def covered_clauses(evidence: list[dict[str, Any]], clauses: list[str], rules_only: bool = False) -> dict[int, str]:
    """Clause index -> id of the first evidence edge that covers it. An edge labelled with clause numbers covers
    exactly those clauses; an edge with a free quote (older records) covers a clause when the normalised quote is
    contained in the normalised clause or the clause in the quote. With ``rules_only`` a level way does not count:
    it says how the student reads the code, not which rule the clause applies, so the walk goes on looking."""
    covered: dict[int, str] = {}
    for c in evidence:
        if rules_only and c.get("kind") == "level":
            continue
        if c.get("clauses"):
            for k in c["clauses"]:
                covered.setdefault(k - 1, c["edge"])
            continue
        q = _norm(c.get("quote", ""))
        if not q:
            continue
        for i, cl in enumerate(clauses):
            if i in covered:
                continue
            n = _norm(cl)
            if q in n or n in q:
                covered[i] = c["edge"]
    return covered


def same_words(a: dict[str, Any], b: dict[str, Any]) -> bool:
    """Two labelled edges rest on the same words when they share a clause (or, for free quotes, when one quote
    contains the other)."""
    if a.get("clauses") and b.get("clauses"):
        return bool(set(a["clauses"]) & set(b["clauses"]))
    return quotes_overlap(a.get("quote", ""), b.get("quote", ""))


def concept_text(g: "Graph", c: str) -> str:
    """A concept's text for BM25: its id with underscores turned into spaces, plus the texts of its misconception
    edges and concept edges."""
    return " ".join([c.replace("_", " ")] + [g.edge_text(e) for e in g.mis_by_concept.get(c, []) + g.cedges_by_concept.get(c, [])])


def _names_in_code(match: str, answer: str) -> bool:
    """Does the code text that tagged a concept occur in the answer? A word-like text must stand as a whole word
    ("int" does not count inside "prints"); a symbol like "=" or ";" may stand anywhere."""
    if not match:
        return False
    w = r"[A-Za-z0-9_]"
    pat = (f"(?<!{w})" if re.match(w, match[0]) else "") + re.escape(match) + (f"(?!{w})" if re.match(w, match[-1]) else "")
    return re.search(pat, answer) is not None


def select_start(g: "Graph", answer: str, n: int, log: list[str]) -> list[str]:
    """ToG's topic entities, with no model call. Candidates: the non-generic concepts of G, that is, the concepts
    Stage 1 tagged in the code (ToG's released code reads the given topic_entity from the dataset the same way), plus
    a generic concept whose tagging text the answer repeats (e.g. "=" for assignment in "a = b": the student names
    the concept in code rather than in words). All of them when there are at most n; otherwise the top n by BM25 of
    the student's answer against each concept's text, ties broken by the number of Stage 1 code hits, then by id."""
    ids = sorted(g.concepts)
    cands = [c for c in ids if not g.concepts[c].get("generic")]
    named = [c for c in ids if g.concepts[c].get("generic") and any(
        _names_in_code((h.get("match") or "").strip(), answer) for h in g.concepts[c].get("hits") or [])]
    if named:
        log.append("start: generic concepts whose tagging text occurs in the answer: " + ", ".join(named))
        cands += named
    if len(cands) <= n:
        log.append(f"start: {len(cands)} tagged concepts, all used")
        return cands
    scores = bm25_scores(answer, [concept_text(g, c) for c in cands])
    hits = {c: len(g.concepts[c].get("hits") or []) for c in cands}
    ranked = sorted(cands, key=lambda c: (-scores[cands.index(c)], -hits[c], c))
    log.append("start: BM25 of the answer against each tagged concept: " +
               ", ".join(f"{c} {scores[cands.index(c)]:.2f} (hits {hits[c]})" for c in ranked))
    log.append(f"start: chosen {', '.join(ranked[:n])}")
    return ranked[:n]


# ====================================================================== Part 3 helpers: parsing replies (ToG regexes)

_SCORE_RE = re.compile(r"\{\s*([^{}()]+?)\s*\(Score:\s*([0-9]*\.?[0-9]+)\)\s*\}")


def parse_prune(reply: str, valid: set[str], n: int) -> list[tuple[str, float]]:
    out = []
    for eid, s in _SCORE_RE.findall(reply):
        eid = eid.strip()
        if eid in valid:
            out.append((eid, float(s)))
    # unknown ids dropped; renormalise so the kept scores sum to 1
    out = sorted(out, key=lambda x: -x[1])[:n]
    tot = sum(s for _, s in out)
    return [(e, s / tot if tot else 0.0) for e, s in out]


def _label_of(text: str, allowed: tuple[str, ...]) -> str:
    cand = text.strip().lower()
    for a in allowed:
        if cand.startswith(a):
            return a
    return "not applied"


def _clause_ids(text: str, n_clauses: int) -> list[int]:
    """'2, 4' / 'c2 and c4' -> [1, 3] (0-based, in range, no repeats); 'none' -> []."""
    ids: list[int] = []
    for tok in re.findall(r"\d+", text):
        i = int(tok) - 1
        if 0 <= i < n_clauses and i not in ids:
            ids.append(i)
    return ids


def parse_label(reply: str, allowed: tuple[str, ...], n_clauses: int) -> tuple[str, list[int], float]:
    """Three-line reply (Label / Clauses / Confidence) -> (label, clause indices, confidence). Evidence is given as
    clause numbers, not a free quote, so the code knows exactly which words each label rests on."""
    label, ids, conf = "not applied", [], 0.0
    m = re.search(r"Label:\s*([A-Za-z ]+)", reply)
    if m:
        label = _label_of(m.group(1), allowed)
    m = re.search(r"Clauses?:\s*(.+)", reply)
    if m:
        ids = _clause_ids(m.group(1), n_clauses)
    m = re.search(r"Confidence:\s*([0-9]*\.?[0-9]+)", reply)
    if m:
        conf = max(0.0, min(1.0, float(m.group(1))))
    return label, ids, conf


def parse_label_set(reply: str, valid: set[str], allowed: tuple[str, ...], n_clauses: int) -> dict[str, tuple[str, list[int], float]]:
    """One line per edge: ``edge_id | label | clauses: 2, 4 | confidence: 0.9`` -> edge id -> (label, clause indices,
    confidence). Edges the reply leaves out are not applied."""
    out: dict[str, tuple[str, list[int], float]] = {}
    for line in reply.splitlines():
        parts = [p.strip() for p in line.strip().strip("{}").split("|")]
        if len(parts) < 2 or parts[0] not in valid:
            continue
        label = _label_of(parts[1], allowed)
        rest = " | ".join(parts[2:])
        m = re.search(r"clauses?:\s*([^|]*)", rest, re.I)
        ids = _clause_ids(m.group(1), n_clauses) if m else []
        m = re.search(r"confidence:\s*([0-9]*\.?[0-9]+)", rest, re.I)
        conf = max(0.0, min(1.0, float(m.group(1)))) if m else 0.0
        out[parts[0]] = (label, ids, conf)
    for eid in valid:
        out.setdefault(eid, ("not applied", [], 0.0))
    return out


# ====================================================================== the traversal

def traverse(sg: dict[str, Any], sc: dict[str, Any], cfg: dict[str, Any], llm: LLM | None = None, log: list[str] | None = None) -> dict[str, Any]:
    g = Graph(sg)
    N, D = int(cfg.get("width", 3)), int(cfg.get("depth", 3))
    prune_tool = cfg.get("prune_tools", "llm")
    llm = llm or LLM(cfg)
    log = log if log is not None else []
    asks0 = Counter(llm.asks_by_step)
    code, question, answer = sc["code"], sc.get("question", ""), sc.get("answer", "")
    ex = prompts.few_shot_fields()
    settings = {"width": N, "depth": D, "prune_tools": prune_tool, "model": llm.model, "backend": llm.backend}

    def calls_by_step() -> dict[str, int]:
        return {s: llm.asks_by_step[s] - asks0[s] for s in STEPS}

    # ---- Part 2: start
    clauses = split_clauses(answer)
    clause_text = "\n".join(f"c{i + 1}: {c}" for i, c in enumerate(clauses))
    log.append("clauses: " + " | ".join(clauses))
    topic = select_start(g, answer, N, log)
    log.append(f"start concepts ({len(topic)}): {', '.join(topic)}")
    if not topic:
        return {"scenario": sc["id"], "status": "not diagnosable from the graph", "settings": settings, "clauses": clauses,
                "llm_calls": llm.calls, "llm_calls_by_step": calls_by_step()}

    pre_in: dict[str, list[str]] = defaultdict(list)   # concept -> sources of its prerequisite edges in G
    for e in sg["concept_edges"]:
        if e["type"] == "prerequisite":
            pre_in[e["target"]].append(e["source"])

    def tier(c: dict[str, Any]) -> int:
        """Ranking tier for the keep step: diagnosis first (held misconception, broken edge), then held errors, then confirmations."""
        if c["label"] == "broken" or (c["label"] == "held" and c["kind"] == "misconception"):
            return 0
        if c["label"] == "held":
            return 1
        return 2

    current = list(topic)
    paths: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []   # every labelled candidate (any depth) whose quote is in the answer, kept or not
    used: set[str] = set()        # edges kept on a path
    examined: set[str] = set()    # edges offered to the prune step at some depth
    starts_at = {c: 1 for c in topic}   # concept -> the depth at which it entered as a start concept (own edges read there)
    # concepts the uncovered clauses may bring in later: the same pool the start rule draws from
    pool = [c for c in sorted(g.concepts) if not g.concepts[c].get("generic")
            or any(_names_in_code((h.get("match") or "").strip(), answer) for h in g.concepts[c].get("hits") or [])]
    stop_reason = "max depth"
    depth_reached = 0

    for depth in range(1, D + 2):
        if depth > D:
            # one closing round past the depth cap: a concept the walk entered at the last depth still gets its own
            # edges (misconceptions, level ways) read, so no entered concept is left without a reading. Nothing new is
            # entered in this round.
            current = [c for c in current if starts_at.get(c) == depth]
            if not current:
                break
        depth_reached = depth
        candidates: list[dict[str, Any]] = []
        offered: set[str] = set()   # edges put to the prune step at this depth (an edge is offered once, not from each end)
        log.append(f"--- depth {depth}: current concepts {current}" + (" (closing round: own edges only)" if depth > D else ""))
        for concept in current:
            # 3a edge search. A concept entering as a start concept (depth 1, or later when the uncovered clauses bring
            # it in): its misconception / error edges and its level ways, as two families (each pruned to N on its own,
            # so a diagnosis edge and a level way never compete for the same slot). Otherwise: prerequisite / parallel
            # edges inside the same piece.
            if starts_at.get(concept) == depth:
                families = [("misconceptions", list(g.mis_by_concept.get(concept, []))), ("level ways", list(g.ways_by_concept.get(concept, [])))]
            else:
                families = [("concept edges", [e for e in g.cedges_by_concept.get(concept, []) if g.piece_of.get(g.other_end(e, concept)) == g.piece_of.get(concept)])]
            for family, edges in families:
                # not already on a path, and not already offered from its other end at this depth
                edges = [e for e in edges if e["id"] not in used and e["id"] not in offered]
                offered.update(e["id"] for e in edges)
                edges.sort(key=lambda e: (0 if e.get("role") == "primary" else 1, e["id"]))
                if not edges:
                    continue
                examined.update(e["id"] for e in edges)
                # 3b edge prune
                if prune_tool == "llm":
                    p = prompts.PRUNE.format(code=code, question=question, answer=answer, concept=concept, n=min(N, len(edges)),
                                             edges="\n".join("- " + g.edge_text(e) for e in edges), **ex)
                    kept = parse_prune(llm.ask(p, "prune"), {e["id"] for e in edges}, N)
                else:
                    docs = [g.edge_text(e) for e in edges]
                    scores = bm25_scores(answer, docs) if prune_tool == "bm25" else sbert_scores(answer, docs)
                    top = sorted(zip(edges, scores), key=lambda x: -x[1])[:N]
                    tot = sum(max(s, 0) for _, s in top) or 1.0
                    kept = [(e["id"], max(s, 0) / tot) for e, s in top]
                log.append(f"  {concept} ({family}): {len(edges)} candidates -> kept " + ", ".join(f"{e} ({s:.2f})" for e, s in kept))
                # 3c target lookup + 3d edge label. Misconception / error edges of a concept are judged together in one
                # call (the same words can fit several wrong rules; seeing them side by side the model gives held to the
                # one(s) whose claim the student makes). Concept edges and level ways are judged one by one. Evidence is
                # given as clause numbers, so the code knows exactly which words each label rests on.
                mis_kept = [(eid, s) for eid, s in kept if eid.startswith(("mis:", "err:"))]
                set_labels: dict[str, tuple[str, list[int], float]] = {}
                if mis_kept:
                    p = prompts.LABEL_MIS.format(code=code, question=question, clauses=clause_text, concept=concept,
                                                 edges="\n".join("- " + g.edge_text(g.edge_by_id[eid]) for eid, _ in mis_kept), **ex)
                    set_labels = parse_label_set(llm.ask(p, "label"), {eid for eid, _ in mis_kept}, ("held", "correct", "not applied"), len(clauses))
                for eid, pscore in kept:
                    e = g.edge_by_id[eid]
                    is_mis = eid.startswith(("mis:", "err:"))
                    is_way = eid.startswith("lvl:")
                    kind = ("error" if eid.startswith("err:") else "misconception") if is_mis else ("level" if is_way else e["type"])
                    if is_mis:
                        target = e["target"]
                        label, ids, conf = set_labels[eid]
                    elif is_way:
                        target = e["target"]
                        # the way is judged against its own text only: no level name, no deciding question, no level in an id.
                        # The level comes from where the way sits in the graph (Part 4).
                        p = prompts.LABEL_WAY.format(code=code, question=question, clauses=clause_text, concept=concept,
                                                     way=(e.get("way") or "").replace("_", " "), rule=e.get("logic") or "")
                        label, ids, conf = parse_label(llm.ask(p, "label"), ("shown", "not applied"), len(clauses))   # "not shown" reads as not applied
                    else:
                        target = g.other_end(e, concept)
                        p = prompts.LABEL_CONCEPT.format(code=code, question=question, clauses=clause_text, edge_id=eid,
                                                         source=e["source"], target=e["target"], etype=e["type"], logic=e.get("logic") or "")
                        label, ids, conf = parse_label(llm.ask(p, "label"), ("confirmed", "broken", "not applied"), len(clauses))
                    if label != "not applied" and not ids:
                        log.append(f"    {eid}: no clause given for the label -> not applied")
                        label = "not applied"
                    if label == "not applied":
                        ids = []
                    quote = "; ".join(clauses[i] for i in ids)
                    score = pscore * conf if label != "not applied" else 0.0
                    cand = {"depth": depth, "source": concept, "edge": eid, "target": target, "kind": kind,
                            "label": label, "clauses": [i + 1 for i in ids], "quote": quote, "confidence": conf, "prune_score": pscore,
                            "score": round(score, 4), "logic": e.get("logic"), "twin_logic": e.get("twin_logic")}
                    if is_way:
                        cand.update(level=e["level"], way=e.get("way"))
                    candidates.append(cand)
                    if label != "not applied":
                        evidence.append(cand)
                    log.append(f"    {eid} -> {label} ({score:.2f}) \"{quote}\"")
        # 3e keep the best: diagnosis tier first (held misconception, broken), then held errors, then confirmations; score within a tier
        # (the same edge reached from both of its ends in one round counts once, with its higher score)
        best_by_edge: dict[str, dict[str, Any]] = {}
        for c in sorted(candidates, key=lambda c: -c["score"]):
            if c["label"] != "not applied" and c["score"] > 0:
                best_by_edge.setdefault(c["edge"], c)
        # a diagnosis finding (tier 0) is never cut by the beam: every held misconception / broken edge is kept, and
        # the rest fill the N slots
        ranked_now = sorted(best_by_edge.values(), key=lambda c: (tier(c), -c["score"]))
        kept_now = [c for c in ranked_now if tier(c) == 0]
        kept_now += [c for c in ranked_now if tier(c) != 0][:max(0, N - len(kept_now))]
        if kept_now:
            paths.extend(kept_now)
            used.update(c["edge"] for c in kept_now)
            log.append("  kept: " + ", ".join(f"{c['edge']} [{c['label']}, tier {tier(c)}, {c['score']:.2f}]" for c in kept_now))
        else:
            log.append("  nothing kept at this depth")
        # 3f next concepts, then the stop test. Next: every entered concept whose concept edges are unread (it reads
        # them next); the far end of every kept concept edge, entered as a start concept so its own edges
        # (misconceptions, level ways) are read and it gets a level of its own; the source of each held misconception
        # (to walk back).
        nxt: list[str] = []
        for c in kept_now:
            if c["kind"] in ("misconception", "error"):
                if c["label"] == "held" and c["source"] not in nxt:
                    nxt.append(c["source"])
            elif c["kind"] == "level":
                continue   # a level way leads nowhere: it describes the concept itself
            else:
                for end in (c["target"], c["source"]):
                    if end not in starts_at:
                        starts_at[end] = depth + 1
                        log.append(f"  reached across {c['edge']}, entered next: {end}")
                    if end not in nxt:
                        nxt.append(end)
        # Graph check, no LLM: every concept the walk has entered has its own edges read and its concept edges
        # (prerequisite and parallel links to the other concepts of its piece) read before the walk may stop. For a
        # faulted concept that is where the root cause lies; for a concept the student got right it is the conceptual
        # trace, the confirmed links between the concepts, which is as much part of the diagnosis as the faults.
        pending = []
        for concept, at in starts_at.items():
            if at > depth:
                pending.append(f"own edges of {concept}")
                if concept not in nxt:
                    nxt.append(concept)
                continue
            for e in g.cedges_by_concept.get(concept, []):
                if e["id"] not in examined and g.piece_of.get(g.other_end(e, concept)) == g.piece_of.get(concept):
                    pending.append(e["id"])
                    if concept not in nxt:
                        nxt.append(concept)
        # Clause coverage, no LLM: every clause is covered by some verified rule edge (a misconception / error edge
        # labelled held or correct, a concept edge labelled confirmed or broken; kept or not). A shown level way does
        # not count here: it says how the student reads the code, not which rule the clause applies.
        covered = covered_clauses(evidence, clauses, rules_only=True)
        log.append("  clause coverage: " + "; ".join(
            f"c{i + 1} <- {covered[i]}" if i in covered else f"c{i + 1} uncovered" for i in range(len(clauses))))
        # Uncovered clauses bring in concepts the walk has not entered yet (no LLM): the clauses the evidence does not
        # explain are matched by BM25 against the concepts of the pool not yet visited, and the best N are entered as
        # start concepts (their own edges are read at the next depth). This has its own cap: it never competes with
        # the concepts that are only waiting to read their concept edges. Not in the closing round (nothing new enters).
        if len(covered) < len(clauses) and depth <= D:
            unseen = [c for c in pool if c not in starts_at and c not in nxt]
            if unseen:
                text = " ".join(cl for i, cl in enumerate(clauses) if i not in covered)
                scores = bm25_scores(text, [concept_text(g, c) for c in unseen])
                ranked = sorted(unseen, key=lambda c: (-scores[unseen.index(c)], c))
                brought = [c for c in ranked if scores[unseen.index(c)] > 0][:N]
                if brought:
                    log.append("  uncovered clauses bring in: " + ", ".join(f"{c} ({scores[unseen.index(c)]:.2f})" for c in brought))
                    for c in brought:
                        starts_at[c] = depth + 1
                        nxt.append(c)
                        pending.append(f"own edges of {c}")
        if pending:
            log.append("  not yet read: " + ", ".join(sorted(set(pending))))
        elif len(covered) == len(clauses):
            stop_reason = "sufficient"
            break
        if not nxt:
            stop_reason = "half_stop"
            log.append("  no next nodes -> half_stop")
            break
        current = nxt

    # ---- Part 4: diagnose
    held_all = [c for c in paths if c["label"] == "held"]
    held_mis_concepts = {c["source"] for c in held_all if c["kind"] == "misconception"}
    # an error node is a consequence: beside a held misconception on the same concept it is evidence, not a second diagnosis
    held = [c for c in held_all if c["kind"] == "misconception" or c["source"] not in held_mis_concepts]
    evidence_errors = [c for c in held_all if c not in held]
    # every held misconception stays; those resting on the same words as a stronger one on the concept are marked so.
    # One fault, one location: the same misconception at both ends of a prerequisite edge is filed at the dependent concept
    before = [c["edge"] for c in held]
    held = filed_at_dependent(mark_shared_evidence(held), pre_in)
    shared = [c for c in held if c.get("shares_evidence_with")]
    if shared or len(held) != len(before):
        log.append("  held: " + ", ".join(
            c["edge"] + (f" (same words as {c['shares_evidence_with']})" if c.get("shares_evidence_with") else "") for c in held)
            + ("; filed at the dependent concept: " + ", ".join(e for e in before if e not in {c["edge"] for c in held})
               if len(held) != len(before) else ""))
    # Reconcile across concepts: a held label on a prerequisite or a generic concept that rests on the clauses of a
    # stronger label at the specific concept is a shadow of that label (one wrong sentence, read twice), not a fault
    # of its own. Shadows stay in the output, marked, but mark no root cause and set no level.
    generic_ids = {c for c in g.concepts if g.concepts[c].get("generic")}
    all_held_mis = [c for c in evidence if c["kind"] == "misconception" and c["label"] == "held"]
    shadow = shadowed([c for c in held if c["kind"] == "misconception"], all_held_mis, pre_in, generic_ids)
    shadows = [c for c in all_held_mis if c["edge"] in shadow]
    if shadow:
        held = [c for c in held if c["edge"] not in shadow]
        log.append("  shadows: " + ", ".join(f"{e} (shadow of {s})" for e, s in shadow.items()))
    broken = [c for c in paths if c["label"] == "broken"]
    held_by_concept: dict[str, list[str]] = defaultdict(list)
    for c in held:
        held_by_concept[c["source"]].append(c["target"])
    # a broken prerequisite edge A -> B says the student did not carry A's rule into B: the fault sits at B, the concept
    # that failed to use its prerequisite. A is the root cause only if it has its own held misconception or broken edge.
    # (a candidate's "target" is the far end seen from the concept being expanded, so read B from the edge id)
    # A broken edge shown by the same words as a held misconception is that misconception's consequence, not a fault
    # of its own, so it marks no root-cause location (it stays in the output, marked consequence_of).
    held_mis = [c for c in held_all if c["kind"] == "misconception"]   # every held label, kept or folded
    for c in broken:
        src = next((h for h in held_mis if same_words(h, c)), None)
        if src is not None:
            c["consequence_of"] = src["edge"]
    broken_concepts = {c["edge"].split("->", 1)[1] if c["edge"].startswith("pre:") else c["source"] for c in broken if not c.get("consequence_of")}

    log.append(f"  root-cause walk: held on {sorted(held_by_concept)}, broken at {sorted(broken_concepts)}"
               + (f" (consequences: {', '.join(c['edge'] for c in broken if c.get('consequence_of'))})" if any(c.get("consequence_of") for c in broken) else "")
               + f", prerequisites {dict(pre_in)}")
    root = None
    for start in sorted(held_by_concept):
        best, seen, stack = start, {start}, [start]
        while stack:
            x = stack.pop()
            for src in pre_in.get(x, []):
                if src in seen:
                    continue
                seen.add(src)
                if src in held_by_concept or src in broken_concepts:
                    best = src
                stack.append(src)
        cand = {"concept": best, "misconception": (held_by_concept.get(best) or [None])[0]}
        if root is None or len(pre_in.get(cand["concept"], [])) < len(pre_in.get(root["concept"], [])):
            root = cand

    # Levels by rule, from the evidence, no model call. A concept's level is L0 when it holds a misconception or an L0
    # way is shown (the L0 deciding question: does every rule the answer applies agree with the language rule?).
    # Otherwise it is the highest level with a shown way: the levels are cumulative, an answer at L4 also does L3.
    # A concept with no held misconception and no shown way gets no level.
    held_mis_ev: dict[str, list[dict[str, Any]]] = defaultdict(list)
    shown_ev: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for c in evidence:
        if c["kind"] == "misconception" and c["label"] == "held" and c["edge"] not in shadow:
            held_mis_ev[c["source"]].append(c)
        elif c["kind"] == "level" and c["label"] == "shown":
            shown_ev[c["source"]].append(c)
    touched = sorted({c["source"] for c in evidence} | {c["target"] for c in evidence if c["kind"] not in ("misconception", "error", "level")})
    levels: dict[str, dict[str, Any]] = {}
    kept_held = {c["source"]: c for c in reversed(held) if c["kind"] == "misconception"}   # strongest kept finding per concept
    for concept in touched:
        held_here = sorted(held_mis_ev.get(concept, []), key=lambda c: -c["score"])
        ways_here = sorted(shown_ev.get(concept, []), key=lambda c: (c["level"], c["score"]), reverse=True)
        l0_ways = [c for c in ways_here if c["level"] == "L0"]
        if held_here:
            # L0 by the misconception way: the level reads the edge of that one misconception, the kept finding when
            # the concept has one, with the L0 way's own text from the graph
            m = kept_held.get(concept) or held_here[0]
            in_graph = (concept, m["target"]) in g.level_link
            levels[concept] = {"level": "L0", "way": "misconception", "misconception": m["target"], "quote": m["quote"], "edge": m["edge"],
                               "rule": g.level_link_rule.get((concept, m["target"])) or m.get("logic", ""),
                               "source": "level_mis_links" if in_graph else "held_misconception"}
            if not in_graph:   # a graph gap, reported, not hidden: the misconception edge exists, its L0 way does not
                levels[concept]["note"] = "no L0 way names this misconception at this concept in the graph"
            others = [c["target"] for c in held_here if c["target"] != m["target"]]
            if others:
                levels[concept]["also_held"] = others
        elif l0_ways and len(l0_ways) == len(ways_here):
            # an L0 way alone: the student reads this concept as everyday language and shows nothing above it
            w = l0_ways[0]
            levels[concept] = {"level": "L0", "way": w["way"], "quote": w["quote"], "edge": w["edge"], "source": "level_way",
                               "also_shown": [f"{c['level']} {c['way']}" for c in ways_here[1:]]}
        elif ways_here:
            # the levels are cumulative: a way shown at L2 has passed L0, so an L0 way shown beside it is the weaker
            # reading of the same words and is listed under also_shown, not taken as the level
            w = next(c for c in ways_here if c["level"] != "L0")
            levels[concept] = {"level": w["level"], "way": w["way"], "quote": w["quote"], "edge": w["edge"], "source": "level_way",
                               "also_shown": [f"{c['level']} {c['way']}" for c in ways_here if c is not w]}
        else:
            continue
        log.append(f"  level {concept}: {levels[concept]['level']} via {levels[concept]['way']} \"{levels[concept]['quote']}\"")

    if root:
        overall = levels.get(root["concept"], {}).get("level")
    else:
        # no error found: the student stands at the level reached on at least half of the concepts the answer touched
        # (the upper median); a single weaker concept keeps its own row and does not set the overall on its own
        got = sorted((v["level"] for v in levels.values() if v.get("level")), reverse=True)
        overall = got[(len(got) - 1) // 2] if got else None
    covered = covered_clauses(evidence, clauses)
    unexplained = [cl for i, cl in enumerate(clauses) if i not in covered]

    return {
        "scenario": sc["id"],
        "settings": settings,
        "clauses": clauses,
        "start_concepts": topic,
        "held_misconceptions": [{"concept": c["source"], "misconception": c["target"], "kind": c["kind"], "quote": c["quote"], "score": c["score"],
                                 **({"shares_evidence_with": c["shares_evidence_with"]} if c.get("shares_evidence_with") else {})} for c in held],
        "error_evidence": [{"concept": c["source"], "error": c["target"], "quote": c["quote"]} for c in evidence_errors],
        "shadowed": [{"concept": c["source"], "misconception": c["target"], "shadow_of": shadow[c["edge"]], "quote": c["quote"], "score": c["score"]} for c in shadows],
        "broken_edges": [{"edge": c["edge"], "quote": c["quote"], "score": c["score"],
                          **({"consequence_of": c["consequence_of"]} if c.get("consequence_of") else {})} for c in broken],
        "root_cause": root,
        "levels": levels,
        "overall_level": overall,
        "paths": paths,
        "evidence": evidence,
        "clause_coverage": {clauses[i]: eid for i, eid in sorted(covered.items())},
        "unexplained_clauses": unexplained,
        "stop_reason": stop_reason,
        "depth_reached": depth_reached,
        "llm_calls": llm.calls,
        "llm_cache_hits": llm.cache_hits,
        "llm_calls_by_step": calls_by_step(),
    }


# ====================================================================== CLI

def main(argv=None) -> None:
    cfg_all = load_config()
    tcfg = {**DEFAULT_TRAVERSAL, **cfg_all.get("traversal", {})}
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scenario", nargs="?", help="scenario id, e.g. S007")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--scenarios", default=cfg_all.get("scenarios", str(SCENARIOS_PATH)))
    ap.add_argument("--processed", default=str(PROCESSED_DIR))
    ap.add_argument("--prune-tools", choices=["llm", "bm25", "sentencebert"], default=tcfg["prune_tools"])
    ap.add_argument("--backend", choices=["claude-cli", "anthropic"], default=tcfg["backend"])
    ap.add_argument("--model", default=tcfg["model"])
    ap.add_argument("--width", type=int, default=tcfg["width"])
    ap.add_argument("--depth", type=int, default=tcfg["depth"])
    ap.add_argument("--tag", default="", help="suffix for the output files, e.g. --tag bm25 -> S007_diagnosis.bm25.json")
    a = ap.parse_args(argv)
    tcfg.update(prune_tools=a.prune_tools, backend=a.backend, model=a.model, width=a.width, depth=a.depth)
    tag = f".{a.tag}" if a.tag else ""

    scenarios = {s["id"]: s for s in load_scenarios(a.scenarios)}
    ids = sorted(scenarios) if a.all else [a.scenario]
    if not ids or ids == [None]:
        ap.error("give a scenario id or --all")
    llm = LLM(tcfg)
    for sid in ids:
        sg = json.loads((Path(a.processed) / f"{sid}_subgraph.json").read_text(encoding="utf-8"))
        calls0 = llm.calls
        log: list[str] = []
        diag = traverse(sg, scenarios[sid], tcfg, llm, log)
        diag["llm_calls"] = llm.calls - calls0
        out = Path(a.processed) / f"{sid}_diagnosis{tag}.json"
        out.write_text(json.dumps(diag, indent=1, ensure_ascii=False), encoding="utf-8")
        (ROOT / "experiments/logs").mkdir(parents=True, exist_ok=True)
        (ROOT / "experiments/logs" / f"traverse_{sid}{tag}.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
        held = [h["misconception"] for h in diag.get("held_misconceptions", [])]
        lv = ", ".join(f"{k}:{v['level']}" for k, v in diag.get("levels", {}).items())
        print(f"{sid}: held={held} root={diag.get('root_cause')} overall={diag.get('overall_level')} levels={{{lv}}} "
              f"stop={diag.get('stop_reason')} prompts={diag.get('llm_calls_by_step')} fresh_calls={diag['llm_calls']} -> {out}")


if __name__ == "__main__":
    main()
