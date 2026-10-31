"""ToG traversal over the Stage 1 subgraph (Stage 2).

Inputs: G = data/processed/<sid>_subgraph.json; the scenario (code, question, answer) from data/raw/scenarios_20.json;
the "traversal" block of experiments/config.json (width N, depth D, model, prune_tools, ...).
Output: data/processed/<sid>_diagnosis.json.

    python src/traverse.py S007                       # one scenario
    python src/traverse.py S007 --prune-tools bm25    # rank edges by similarity instead of the prune prompt
    python src/traverse.py --all                      # every scenario in the file

Part 1 builds lookups from G (ToG's SPARQL server). Part 2 picks the start concepts and the clauses. Part 3 is the
main loop: edge search (no LLM), edge prune (LLM or bm25/sentencebert), target lookup, edge label (LLM), keep the
best N, sufficiency check (LLM), next nodes. Part 4 diagnoses from the kept paths: held misconceptions, broken edges,
root cause along prerequisite edges, level per concept (level_mis_links, else the level ladder prompt), overall level.
The LLM never answers from its own knowledge: every label is tied to an edge of G and a quote from the answer.
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


# ====================================================================== LLM client

class LLM:
    """One place that calls the model. Backends: 'anthropic' (SDK) or 'claude-cli' (the claude CLI, `claude -p`).
    Replies are cached on disk by prompt hash so a re-run is deterministic and free."""

    def __init__(self, cfg: dict[str, Any]):
        self.cfg = cfg
        self.calls = 0
        self.cache_hits = 0
        self.cache_dir = ROOT / cfg.get("cache_dir", "experiments/llm_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.backend = cfg.get("backend", "claude-cli")
        self.model = cfg.get("model", "claude-opus-5-5")
        self._client = None
        if self.backend == "anthropic":
            import anthropic  # noqa: F401  (pip install anthropic)
            self._client = anthropic.Anthropic()

    def ask(self, prompt: str) -> str:
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

_CLAUSE_SPLIT = re.compile(r"(?<=[.!?])\s+|\s*;\s*|\s+because\s+|\s+so\s+|\s*/\s*", re.I)


def split_clauses(answer: str) -> list[str]:
    parts = [p.strip(" \"'\n\t") for p in _CLAUSE_SPLIT.split(answer)]
    return [p for p in parts if len(p) >= 1]


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def quote_in_answer(quote: str, answer: str) -> bool:
    q = _norm(quote)
    return bool(q) and q != "none" and q in _norm(answer)


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


def parse_yes_no(reply: str) -> bool:
    return bool(re.search(r"\{\s*Yes\s*\}", reply, re.I))


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
    code, question, answer = sc["code"], sc.get("question", ""), sc.get("answer", "")
    ex = prompts.few_shot_fields()

    # ---- Part 2: start
    topic = sorted(c for c, rec in g.concepts.items() if not rec.get("generic"))
    clauses = split_clauses(answer)
    clause_text = "\n".join(f"c{i + 1}: {c}" for i, c in enumerate(clauses))
    log.append(f"start concepts ({len(topic)}): {', '.join(topic)}")
    log.append("clauses: " + " | ".join(clauses))
    if not topic:
        return {"scenario": sc["id"], "status": "not diagnosable from the graph", "clauses": clauses, "llm_calls": llm.calls}

    current = list(topic)
    paths: list[dict[str, Any]] = []
    used: set[str] = set()
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
            # 3b edge prune
            if prune_tool == "llm":
                p = prompts.PRUNE.format(code=code, question=question, answer=answer, concept=concept, n=min(N, len(edges)),
                                         edges="\n".join("- " + g.edge_text(e) for e in edges), **ex)
                kept = parse_prune(llm.ask(p), {e["id"] for e in edges}, N)
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
                if is_mis:
                    target = e["target"]
                    p = prompts.LABEL_MIS.format(code=code, question=question, clauses=clause_text, edge_id=eid,
                                                 logic=e.get("logic") or "", twin_logic=e.get("twin_logic") or "", **ex)
                    label, quote, conf = parse_label(llm.ask(p), ("held", "correct", "not applied"))
                else:
                    target = g.other_end(e, concept)
                    p = prompts.LABEL_CONCEPT.format(code=code, question=question, clauses=clause_text, edge_id=eid,
                                                     source=e["source"], target=e["target"], etype=e["type"], logic=e.get("logic") or "")
                    label, quote, conf = parse_label(llm.ask(p), ("confirmed", "broken", "not applied"))
                if label != "not applied" and not quote_in_answer(quote, answer):
                    log.append(f"    {eid}: quote not found in the answer ({quote!r}) -> not applied")
                    label = "not applied"
                score = pscore * conf if label != "not applied" else 0.0
                candidates.append({"depth": depth, "source": concept, "edge": eid, "target": target, "kind": "misconception" if is_mis else e["type"],
                                   "label": label, "quote": quote, "confidence": conf, "prune_score": pscore, "score": round(score, 4),
                                   "logic": e.get("logic"), "twin_logic": e.get("twin_logic")})
                log.append(f"    {eid} -> {label} ({score:.2f}) \"{quote}\"")
        # 3e keep the best
        kept_now = sorted([c for c in candidates if c["label"] != "not applied" and c["score"] > 0], key=lambda c: -c["score"])[:N]
        if not kept_now:
            stop_reason = "half_stop"
            log.append("  nothing kept -> half_stop")
            break
        paths.extend(kept_now)
        used.update(c["edge"] for c in kept_now)
        # 3f sufficiency check
        path_text = "\n".join(_path_line(c) for c in paths)
        suff = llm.ask(prompts.SUFFICIENCY.format(question=question, clauses=clause_text, paths=path_text))
        log.append("  sufficiency: " + suff.splitlines()[0] if suff else "  sufficiency: (empty reply)")
        if parse_yes_no(suff):
            stop_reason = "sufficient"
            break
        # 3g next current nodes
        nxt: list[str] = []
        for c in kept_now:
            if c["kind"] == "misconception":
                if c["label"] == "held" and c["source"] not in nxt:
                    nxt.append(c["source"])
            elif c["target"] not in nxt:
                nxt.append(c["target"])
        if not nxt:
            stop_reason = "half_stop"
            log.append("  no next nodes -> half_stop")
            break
        current = nxt

    # ---- Part 4: diagnose
    held = [c for c in paths if c["label"] == "held"]
    broken = [c for c in paths if c["label"] == "broken"]
    held_by_concept: dict[str, list[str]] = defaultdict(list)
    for c in held:
        held_by_concept[c["source"]].append(c["target"])
    broken_concepts = {c["source"] for c in broken} | {c["target"] for c in broken}
    pre_in: dict[str, list[str]] = defaultdict(list)   # concept -> sources of its prerequisite edges
    for e in sg["concept_edges"]:
        if e["type"] == "prerequisite":
            pre_in[e["target"]].append(e["source"])

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
        reply = llm.ask(prompts.LEVEL_LADDER.format(code=code, question=question, clauses=clause_text, concept=concept, levels="\n".join(lines)))
        lvl, way, quote = parse_level(reply)
        levels[concept] = {"level": lvl, "way": way, "quote": quote, "source": "level_ladder"}
        log.append(f"  level {concept}: {lvl} via {way} \"{quote}\"")

    overall = levels.get(root["concept"], {}).get("level") if root else None
    explained = set()
    for c in paths:
        q = _norm(c["quote"])
        for i, cl in enumerate(clauses):
            n = _norm(cl)
            if q and (q in n or n in q):
                explained.add(i)
    unexplained = [cl for i, cl in enumerate(clauses) if i not in explained]

    return {
        "scenario": sc["id"],
        "settings": {"width": N, "depth": D, "prune_tools": prune_tool, "model": llm.model, "backend": llm.backend},
        "clauses": clauses,
        "start_concepts": topic,
        "held_misconceptions": [{"concept": c["source"], "misconception": c["target"], "quote": c["quote"], "score": c["score"]} for c in held],
        "broken_edges": [{"edge": c["edge"], "quote": c["quote"], "score": c["score"]} for c in broken],
        "root_cause": root,
        "levels": levels,
        "overall_level": overall,
        "paths": paths,
        "unexplained_clauses": unexplained,
        "stop_reason": stop_reason,
        "depth_reached": depth_reached,
        "llm_calls": llm.calls,
        "llm_cache_hits": llm.cache_hits,
    }


def _path_line(c: dict[str, Any]) -> str:
    if c["kind"] == "misconception":
        return f"{c['source']} —[wrong: \"{c['logic']}\"]→ {c['target']} ({c['label']}: \"{c['quote']}\")"
    return f"{c['source']} —[{c['kind']}: \"{c['logic']}\"]→ {c['target']} ({c['label']}: \"{c['quote']}\")"


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
    a = ap.parse_args(argv)
    tcfg.update(prune_tools=a.prune_tools, backend=a.backend, model=a.model, width=a.width, depth=a.depth)

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
        out = Path(a.processed) / f"{sid}_diagnosis.json"
        out.write_text(json.dumps(diag, indent=1, ensure_ascii=False), encoding="utf-8")
        (ROOT / "experiments/logs").mkdir(parents=True, exist_ok=True)
        (ROOT / "experiments/logs" / f"traverse_{sid}.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
        held = [h["misconception"] for h in diag.get("held_misconceptions", [])]
        lv = ", ".join(f"{k}:{v['level']}" for k, v in diag.get("levels", {}).items())
        print(f"{sid}: held={held} root={diag.get('root_cause')} overall={diag.get('overall_level')} levels={{{lv}}} "
              f"stop={diag.get('stop_reason')} calls={diag['llm_calls']} -> {out}")


if __name__ == "__main__":
    main()
