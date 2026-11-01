"""ToG traversal over the Stage 1 subgraph (Stage 2).

Inputs: G = data/processed/<sid>_subgraph.json; the scenario (code, question, answer) from data/raw/scenarios_20.json;
the "traversal" block of experiments/config.json (width N, depth D, model, prune_tools, ...).
Output: data/processed/<sid>_diagnosis.json.

    python src/traverse.py S007                       # one scenario, default settings (start stage1, stop rule)
    python src/traverse.py S007 --prune-tools bm25    # rank edges by similarity instead of the prune prompt
    python src/traverse.py --all                      # every scenario in the file

The LLM is used in three places only: edge pruning (replaceable by BM25 / sentence-BERT), edge labelling, and the
level ladder for a concept that has no misconception link. Start concepts and the stop decision are not model calls.

Part 1 builds lookups from G (ToG's SPARQL server). Part 2 splits the answer into clauses and selects at most N start
concepts, with no model call: Stage 1's tagged (non-generic) concepts, the given topic entities that ToG's released
code reads from the dataset, plus a generic concept whose tagging text the answer repeats (e.g. "=" for assignment);
more than N of them are ranked by BM25 of the answer against each concept's text. Part 3 is the main loop: edge search
(no LLM), edge prune (LLM or bm25/sentencebert), target lookup, edge label (LLM, quote checked against the answer),
keep the best N in two tiers (held misconception / broken edge first, then held errors, then confirmations), stop
test, next nodes. Every labelled candidate whose quote is in the answer is recorded as evidence, kept or not. The
stop test is a rule, no model call: (i) graph check, a held or broken concept with unexamined prerequisites in G
sends the walk one hop back; (ii) clause coverage, stop when the quote of some evidence edge covers every clause.
Part 4 diagnoses from the kept paths: held misconceptions (a held error beside a held misconception on the same
concept is evidence, not a second diagnosis), broken edges, root cause along prerequisite edges, level per concept
(level_mis_links, else the level ladder prompt), overall level, and the clauses no evidence covers. The LLM never
answers from its own knowledge: every label is tied to an edge of G and a quote.
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

STEPS = ("prune", "label", "level")   # the only places the model is asked


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
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8", timeout=180, env=env, shell=(os.name == "nt"))
        if r.returncode != 0:
            raise RuntimeError(f"claude CLI failed ({r.returncode}): {r.stderr.strip()[:300]}")
        return r.stdout.strip()


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
        for l in sg["level_mis_links"]:
            concept = l["level_node"].split("@")[0]
            self.level_link.setdefault((concept, l["misconception"]), l["level_node"])
        self.levels = {l["id"]: l for l in sg["levels"]}
        self.level_edges_by_concept: dict[str, list[dict]] = defaultdict(list)
        for le in sg["level_edges"]:
            self.level_edges_by_concept[le["source"]].append(le)
        self.edge_by_id = {e["id"]: e for e in sg["mis_edges"] + sg["concept_edges"]}

    def other_end(self, edge: dict, concept: str) -> str:
        return edge["target"] if edge["source"] == concept else edge["source"]

    def edge_text(self, e: dict) -> str:
        if e["id"].startswith(("mis:", "err:")):
            return f"{e['id']} | wrong rule: {e.get('logic') or ''} | right rule: {e.get('twin_logic') or ''}"
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


def covered_clauses(evidence: list[dict[str, Any]], clauses: list[str]) -> dict[int, str]:
    """Clause index -> id of the first evidence edge whose quote covers it. A clause is covered when the normalised
    quote is contained in the normalised clause or the clause in the quote (the same matching as Part 4)."""
    covered: dict[int, str] = {}
    for c in evidence:
        q = _norm(c["quote"])
        if not q:
            continue
        for i, cl in enumerate(clauses):
            if i in covered:
                continue
            n = _norm(cl)
            if q in n or n in q:
                covered[i] = c["edge"]
    return covered


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


def parse_label(reply: str, allowed: tuple[str, ...]) -> tuple[str, str, float]:
    label, quote, conf = "not applied", "", 0.0
    m = re.search(r"Label:\s*([A-Za-z ]+)", reply)
    if m:
        cand = m.group(1).strip().lower()
        for a in allowed:
            if cand.startswith(a):
                label = a
    m = re.search(r"Quote:\s*(.+)", reply)
    if m:
        quote = m.group(1).strip().strip('"').strip()
    m = re.search(r"Confidence:\s*([0-9]*\.?[0-9]+)", reply)
    if m:
        conf = max(0.0, min(1.0, float(m.group(1))))
    return label, quote, conf


def parse_level(reply: str) -> tuple[str | None, str | None, str]:
    lvl = re.search(r"Level:\s*(L[0-4]|none)", reply, re.I)
    way = re.search(r"Way:\s*(.+)", reply)
    quote = re.search(r"Quote:\s*(.+)", reply)
    level = lvl.group(1).upper() if lvl and lvl.group(1).lower() != "none" else None
    w = way.group(1).strip() if way else None
    return level, (None if not w or w.lower() == "none" else w), (quote.group(1).strip().strip('"') if quote else "")


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
    stop_reason = "max depth"
    depth_reached = 0

    for depth in range(1, D + 1):
        depth_reached = depth
        candidates: list[dict[str, Any]] = []
        log.append(f"--- depth {depth}: current concepts {current}")
        for concept in current:
            # 3a edge search
            if depth == 1:
                edges = list(g.mis_by_concept.get(concept, []))
            else:
                edges = [e for e in g.cedges_by_concept.get(concept, []) if g.piece_of.get(g.other_end(e, concept)) == g.piece_of.get(concept)]
            edges = [e for e in edges if e["id"] not in used]
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
            log.append(f"  {concept}: {len(edges)} candidates -> kept " + ", ".join(f"{e} ({s:.2f})" for e, s in kept))
            # 3c target lookup + 3d edge label
            for eid, pscore in kept:
                e = g.edge_by_id[eid]
                is_mis = eid.startswith(("mis:", "err:"))
                kind = ("error" if eid.startswith("err:") else "misconception") if is_mis else e["type"]
                if is_mis:
                    target = e["target"]
                    p = prompts.LABEL_MIS.format(code=code, question=question, clauses=clause_text, edge_id=eid,
                                                 logic=e.get("logic") or "", twin_logic=e.get("twin_logic") or "", **ex)
                    label, quote, conf = parse_label(llm.ask(p, "label"), ("held", "correct", "not applied"))
                else:
                    target = g.other_end(e, concept)
                    p = prompts.LABEL_CONCEPT.format(code=code, question=question, clauses=clause_text, edge_id=eid,
                                                     source=e["source"], target=e["target"], etype=e["type"], logic=e.get("logic") or "")
                    label, quote, conf = parse_label(llm.ask(p, "label"), ("confirmed", "broken", "not applied"))
                if label != "not applied" and not quote_in_answer(quote, answer):
                    log.append(f"    {eid}: quote not found in the answer ({quote!r}) -> not applied")
                    label = "not applied"
                score = pscore * conf if label != "not applied" else 0.0
                cand = {"depth": depth, "source": concept, "edge": eid, "target": target, "kind": kind,
                        "label": label, "quote": quote, "confidence": conf, "prune_score": pscore, "score": round(score, 4),
                        "logic": e.get("logic"), "twin_logic": e.get("twin_logic")}
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
        kept_now = sorted(best_by_edge.values(), key=lambda c: (tier(c), -c["score"]))[:N]
        if not kept_now:
            stop_reason = "half_stop"
            log.append("  nothing kept -> half_stop")
            break
        paths.extend(kept_now)
        used.update(c["edge"] for c in kept_now)
        log.append("  kept: " + ", ".join(f"{c['edge']} [{c['label']}, tier {tier(c)}, {c['score']:.2f}]" for c in kept_now))
        # 3f stop test, two parts. (i) Graph check, no LLM: a concept with a held misconception or a broken edge whose
        # prerequisite edges inside G have not been examined yet means the root cause may lie further back -> go deeper.
        pending = []
        for c in paths:
            if tier(c) != 0:
                continue
            for src in pre_in.get(c["source"], []):
                eid = f"pre:{src}->{c['source']}"
                if eid not in examined and g.piece_of.get(src) == g.piece_of.get(c["source"]):
                    pending.append(eid)
        if pending:
            log.append("  root cause not settled, unexamined prerequisites: " + ", ".join(sorted(set(pending))))
        else:
            # (ii) clause coverage, no LLM: every clause is covered by the quote of some verified evidence edge (kept or not)
            covered = covered_clauses(evidence, clauses)
            log.append("  clause coverage: " + "; ".join(
                f"c{i + 1} <- {covered[i]}" if i in covered else f"c{i + 1} uncovered" for i in range(len(clauses))))
            if len(covered) == len(clauses):
                stop_reason = "sufficient"
                break
        # 3g next current nodes: walk back from concepts with a held misconception / broken edge; forward along concept edges
        nxt: list[str] = []
        for c in kept_now:
            if c["kind"] in ("misconception", "error"):
                if c["label"] == "held" and c["source"] not in nxt:
                    nxt.append(c["source"])
            else:
                for end in (c["target"], c["source"]):
                    if end not in nxt:
                        nxt.append(end)
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
    broken = [c for c in paths if c["label"] == "broken"]
    held_by_concept: dict[str, list[str]] = defaultdict(list)
    for c in held:
        held_by_concept[c["source"]].append(c["target"])
    # a broken prerequisite edge A -> B says the student did not carry A's rule into B: the fault sits at B, the concept
    # that failed to use its prerequisite. A is the root cause only if it has its own held misconception or broken edge.
    # (a candidate's "target" is the far end seen from the concept being expanded, so read B from the edge id)
    broken_concepts = {c["edge"].split("->", 1)[1] if c["edge"].startswith("pre:") else c["source"] for c in broken}

    log.append(f"  root-cause walk: held on {sorted(held_by_concept)}, broken at {sorted(broken_concepts)}, prerequisites {dict(pre_in)}")
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

    on_paths = sorted({c["source"] for c in paths} | {c["target"] for c in paths if c["kind"] != "misconception"})
    levels: dict[str, dict[str, Any]] = {}
    for concept in on_paths:
        linked = [(m, g.level_link[(concept, m)]) for m in held_by_concept.get(concept, []) if (concept, m) in g.level_link]
        if linked:
            m, node = linked[0]
            levels[concept] = {"level": node.split("@")[1], "way": "misconception", "misconception": m, "source": "level_mis_links"}
            continue
        lines = []
        for le in sorted(g.level_edges_by_concept.get(concept, []), key=lambda x: x["level"]):
            rec = g.levels.get(le["target"], {})
            ways = "; ".join(f"{w.get('way')} ({w.get('rule_type')}): {(w.get('exact_rule') or '')[:160]}" for w in le["ways"])
            lines.append(f"{le['level']} {rec.get('name', '')}\n  deciding question: {rec.get('deciding_question', '')}\n  ways: {ways}")
        if not lines:
            continue
        reply = llm.ask(prompts.LEVEL_LADDER.format(code=code, question=question, clauses=clause_text, concept=concept, levels="\n".join(lines)), "level")
        lvl, way, quote = parse_level(reply)
        levels[concept] = {"level": lvl, "way": way, "quote": quote, "source": "level_ladder"}
        log.append(f"  level {concept}: {lvl} via {way} \"{quote}\"")

    if root:
        overall = levels.get(root["concept"], {}).get("level")
    else:  # no error found: the student stands at the lowest level reached on any concept the answer touched
        got = [v["level"] for v in levels.values() if v.get("level")]
        overall = min(got) if got else None
    covered = covered_clauses(evidence, clauses)
    unexplained = [cl for i, cl in enumerate(clauses) if i not in covered]

    return {
        "scenario": sc["id"],
        "settings": settings,
        "clauses": clauses,
        "start_concepts": topic,
        "held_misconceptions": [{"concept": c["source"], "misconception": c["target"], "kind": c["kind"], "quote": c["quote"], "score": c["score"]} for c in held],
        "error_evidence": [{"concept": c["source"], "error": c["target"], "quote": c["quote"]} for c in evidence_errors],
        "broken_edges": [{"edge": c["edge"], "quote": c["quote"], "score": c["score"]} for c in broken],
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
