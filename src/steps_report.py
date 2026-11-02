"""Write every output of one Stage 1 + Stage 2 run into a single Markdown file, to read or to paste elsewhere.

    python src/steps_report.py MY01          -> results/viewer/MY01_steps.md (+ MY01_figureNN.png if the notebook saved them)

Contents, in the order the pipeline produces them: input; Stage 1 (masked code, tagging table, subgraph sizes, every
concept node and concept edge of G); clauses and start ranking; for each depth: the concepts expanded, each prune
prompt with the model's reply and the kept edges, each label prompt with the model's reply and the parsed label (prune
score, confidence, score, clauses), the kept paths, the clause coverage and the graph check; then the diagnosis (held,
errors, broken edges, root-cause walk, levels, overall), the evidence list, and the full diagnosis JSON. Prompts and
replies come from experiments/llm_cache (every call is cached), so nothing is re-asked.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import preprocessing  # noqa: E402
import prompts  # noqa: E402
import traverse  # noqa: E402
from utils import PROCESSED_DIR, RESULTS_DIR, ROOT, load_config, load_scenarios  # noqa: E402


def cached_reply(backend: str, model: str, prompt: str) -> str:
    key = hashlib.sha256((backend + "|" + model + "|" + prompt).encode("utf-8")).hexdigest()[:24]
    f = ROOT / "experiments/llm_cache" / f"{key}.json"
    return json.loads(f.read_text(encoding="utf-8"))["reply"] if f.exists() else "(not in cache)"


def table(rows: list[dict], cols: list[str]) -> str:
    if not rows:
        return "(none)\n"
    out = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        out.append("| " + " | ".join(str(r.get(c, "")).replace("|", "\\|").replace("\n", " ") for c in cols) + " |")
    return "\n".join(out) + "\n"


def main(sid: str) -> Path:
    sg = json.loads((PROCESSED_DIR / f"{sid}_subgraph.json").read_text(encoding="utf-8"))
    d = json.loads((PROCESSED_DIR / f"{sid}_diagnosis.json").read_text(encoding="utf-8"))
    log = (ROOT / "experiments/logs" / f"traverse_{sid}.txt").read_text(encoding="utf-8").splitlines()
    cfg = load_config()
    tcfg = {**traverse.DEFAULT_TRAVERSAL, **cfg.get("traversal", {})}
    backend, model = d["settings"]["backend"], d["settings"]["model"]
    # the scenario text: from the scenario file, else from the notebook's saved run
    sc = next((s for s in load_scenarios() if s["id"] == sid), None)
    if sc is None:
        sc = {"id": sid, "code": sg.get("code", ""), "question": "", "answer": " ".join(d["clauses"])}
        nbrun = PROCESSED_DIR / f"{sid}_input.json"
        if nbrun.exists():
            sc.update(json.loads(nbrun.read_text(encoding="utf-8")))
    code, question, answer = sc["code"], sc.get("question", ""), sc.get("answer", "")
    g = traverse.Graph(sg)
    clauses = d["clauses"]
    clause_text = "\n".join(f"c{i + 1}: {c}" for i, c in enumerate(clauses))
    ex = prompts.few_shot_fields()
    N = d["settings"]["width"]
    out: list[str] = []
    w = out.append

    w(f"# Think on the Graph: every output of the run {sid}\n")
    w("## 0. Input\n")
    w("Program:\n```java\n" + code + "\n```\n")
    w(f"Question: {question}\n\nStudent's answer: {answer}\n")
    w(f"Settings: width {N}, depth {d['settings']['depth']}, prune {d['settings']['prune_tools']}, backend {backend}, model {model}\n")

    w("## 1. Stage 1: the subgraph G from the code (no model)\n")
    w("Masked code (string and char literals and comments blanked; this is what the patterns see):\n```\n" + preprocessing.mask_java(code) + "\n```\n")
    rows = [{"concept": c["id"], "generic": c.get("generic", False), "channel": h.get("channel"), "matched text": repr(h.get("match")), "line": h.get("line")}
            for c in sg["concepts"] for h in c.get("hits") or []]
    w("Which code text tagged which concept (a generic concept fires on almost any Java line; it starts the walk only if the answer repeats its tag):\n")
    w(table(rows, ["concept", "generic", "channel", "matched text", "line"]))
    cnt = sg["counts"]
    w(f"\nG: {cnt['concepts']} concept nodes ({cnt['generic']} generic), {cnt['concept_edges']} concept edges, {cnt['mis_edges']} misconception / error edges, "
      f"{cnt['misconceptions']} misconception / error nodes, {cnt['levels']} level nodes, {cnt['level_mis_links']} level-misconception links, {cnt['components']} connected piece(s).\n")
    for warn in sg.get("warnings", []):
        w(f"Note: {warn}\n")
    w("\nConcept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):\n")
    w(table([{"edge": e["id"], "type": e["type"], "rule (logic)": e.get("logic", "")} for e in sg["concept_edges"]], ["edge", "type", "rule (logic)"]))
    w("\nMisconception / error edges per concept (count), and level ways per concept (count):\n")
    w(table([{"concept": c["id"], "misconception / error edges": len(g.mis_by_concept.get(c["id"], [])), "level ways (L1-L4 + L0 non-misconception)": len(g.ways_by_concept.get(c["id"], []))}
             for c in sg["concepts"]], ["concept", "misconception / error edges", "level ways (L1-L4 + L0 non-misconception)"]))
    for i in (1, 2):
        f = RESULTS_DIR / "viewer" / f"{sid}_figure{i:02d}.png"
        if f.exists():
            w(f"\nFigure {i}: {f}\n")

    w("\n## 2. Clauses and start concepts (no model)\n")
    w("The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):\n")
    w(table([{"clause": f"c{i + 1}", "text": c} for i, c in enumerate(clauses)], ["clause", "text"]))
    for line in log:
        if line.startswith("start"):
            w(f"\n{line}\n")
    w(f"\nStart concepts: {', '.join(d['start_concepts'])}\n")
    f = RESULTS_DIR / "viewer" / f"{sid}_figure03.png"
    if f.exists():
        w(f"\nFigure 3: {f}\n")

    w("\n## 3. The walk, depth by depth\n")
    w("At each depth, for each current concept: the edges offered (a concept entering as a start concept offers its misconception / error edges "
      "and its level ways, as two families; otherwise it offers its concept edges), the prune prompt and the model's reply, then the label "
      "prompt(s) and the model's reply, parsed into label / clauses / confidence. Score = prune score x confidence.\n")
    # rebuild the per-depth structure from the log and the diagnosis
    depth = 0
    cands_by_depth: dict[int, list[dict]] = {}
    for c in d["paths"] + d["evidence"]:
        cands_by_depth.setdefault(c["depth"], [])
    by_edge_depth = {}
    for c in d["evidence"]:
        by_edge_depth[(c["depth"], c["edge"])] = c
    R_DEPTH = re.compile(r"^--- depth (\d+): current concepts \[(.*)\]")
    R_PRUNE = re.compile(r"^  (\S+) \(([^)]+)\): (\d+) candidates -> kept ?(.*)$")
    R_LABEL = re.compile(r'^    (\S+) -> (.+?) \(([0-9.]+)\) "(.*)"$')
    fig_no = 4
    i = 0
    while i < len(log):
        line = log[i]
        m = R_DEPTH.match(line)
        if m:
            depth = int(m.group(1))
            w(f"\n### Depth {depth}: current concepts {m.group(2)}\n")
            i += 1
            continue
        m = R_PRUNE.match(line)
        if m and depth:
            concept, family, n_cand, kept_txt = m.group(1), m.group(2), int(m.group(3)), m.group(4)
            kept = re.findall(r"(\S+) \(([0-9.]+)\)", kept_txt)
            w(f"\n#### {concept}, {family}: {n_cand} edges offered\n")
            # rebuild the offered edge list and the prune prompt from the graph (same ordering as traverse.py)
            if family == "misconceptions":
                edges = list(g.mis_by_concept.get(concept, []))
            elif family == "level ways":
                edges = list(g.ways_by_concept.get(concept, []))
            else:
                edges = [e for e in g.cedges_by_concept.get(concept, []) if g.piece_of.get(g.other_end(e, concept)) == g.piece_of.get(concept)]
            w("Edges offered:\n")
            w(table([{"edge": g.edge_text(e)} for e in edges], ["edge"]))
            # labels that follow this prune line
            labels = []
            j = i + 1
            while j < len(log) and R_LABEL.match(log[j]):
                lm = R_LABEL.match(log[j])
                labels.append((lm.group(1), lm.group(2), float(lm.group(3)), lm.group(4)))
                j += 1
            kept_ids = [e for e, _ in kept]
            # the prune prompt actually sent (candidates = offered minus already used / offered this depth; we show the
            # cached reply if the exact prompt is found, else the kept line)
            offered_edges = [e for e in edges if e["id"] in kept_ids or True]
            p = prompts.PRUNE.format(code=code, question=question, answer=answer, concept=concept, n=min(N, n_cand),
                                     edges="\n".join("- " + g.edge_text(e) for e in offered_edges[:n_cand]), **ex)
            reply = cached_reply(backend, model, p)
            w("\nPrune: the model's reply (edge id and score; the kept edges sum to 1):\n```\n" + (reply if reply != "(not in cache)" else kept_txt) + "\n```\n")
            w("Kept by pruning: " + ", ".join(f"{e} ({s})" for e, s in kept) + "\n")
            # label prompts: misconception set (one call) or per edge
            mis_kept = [e for e in kept_ids if e.startswith(("mis:", "err:"))]
            if mis_kept:
                p = prompts.LABEL_MIS.format(code=code, question=question, clauses=clause_text, concept=concept,
                                             edges="\n".join("- " + g.edge_text(g.edge_by_id[e]) for e in mis_kept), **ex)
                w("\nLabel prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:\n")
                w(table([{"edge": g.edge_text(g.edge_by_id[e])} for e in mis_kept], ["edge"]))
                w("Model's reply:\n```\n" + cached_reply(backend, model, p) + "\n```\n")
            for e in kept_ids:
                if e.startswith("lvl:"):
                    ed = g.edge_by_id[e]
                    p = prompts.LABEL_WAY.format(code=code, question=question, clauses=clause_text, concept=concept,
                                                 way=(ed.get("way") or "").replace("_", " "), rule=ed.get("logic") or "")
                    w(f"\nLabel prompt for level way {e} (the model saw only the concept, the way's name '{(ed.get('way') or '').replace('_', ' ')}' and its text; no level):\n")
                    w(f"> {ed.get('logic') or ''}\n\nModel's reply:\n```\n" + cached_reply(backend, model, p) + "\n```\n")
                elif e.startswith(("pre:", "par:")):
                    ed = g.edge_by_id[e]
                    p = prompts.LABEL_CONCEPT.format(code=code, question=question, clauses=clause_text, edge_id=e,
                                                     source=ed["source"], target=ed["target"], etype=ed["type"], logic=ed.get("logic") or "")
                    w(f"\nLabel prompt for concept edge {e} ({ed['source']} -> {ed['target']}, {ed['type']}):\n")
                    w(f"> {ed.get('logic') or ''}\n\nModel's reply:\n```\n" + cached_reply(backend, model, p) + "\n```\n")
            # parsed labels
            rows = []
            for eid, label, score, quote in labels:
                ev = by_edge_depth.get((depth, eid), {})
                rows.append({"edge": eid, "label": label, "prune score": ev.get("prune_score", ""), "confidence": ev.get("confidence", ""),
                             "score": score, "clauses": ", ".join(f"c{k}" for k in ev.get("clauses", [])) or "", "words": quote})
            w("\nParsed labels:\n")
            w(table(rows, ["edge", "label", "prune score", "confidence", "score", "clauses", "words"]))
            i = j
            continue
        if line.startswith("  kept: "):
            w("\n**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):\n\n" + line.strip()[6:] + "\n")
        elif line.startswith("  nothing kept"):
            w("\n**Kept on a path at this depth:** nothing\n")
        elif line.startswith("  reached across"):
            w("\n" + line.strip() + "\n")
        elif line.startswith("  clause coverage:"):
            w("\n**Clause coverage after this depth:**\n")
            cov = {}
            for part in line.split(":", 1)[1].split(";"):
                mm = re.match(r"\s*c(\d+) <- (\S+)", part)
                if mm:
                    cov[int(mm.group(1))] = mm.group(2)
            w(table([{"clause": f"c{k + 1}", "text": c, "covered by": cov.get(k + 1, "not covered yet")} for k, c in enumerate(clauses)], ["clause", "text", "covered by"]))
        elif line.startswith("  uncovered clauses bring in:"):
            w("\n**Uncovered clauses bring in (BM25 of the uncovered clauses against unvisited concepts):** " + line.split(":", 1)[1].strip() + "\n")
        elif line.startswith("  not yet read:"):
            w("\n**Graph check, not yet read (the walk may not stop while these remain):** " + line.split(":", 1)[1].strip() + "\n")
            f = RESULTS_DIR / "viewer" / f"{sid}_figure{fig_no:02d}.png"
            if f.exists():
                w(f"\nFigure {fig_no}: {f}\n")
            fig_no += 1
        elif line.startswith("  no next nodes"):
            w("\n**No next nodes -> half_stop**\n")
        elif line.startswith("  root-cause walk:"):
            w("\n## 4. Diagnosis (rules over the labelled graph, no model)\n")
            w("Root-cause walk: " + line.split(":", 1)[1].strip() + "\n")
        elif line.startswith("  held:"):
            w("\nHeld set after the one-fault rules: " + line.split(":", 1)[1].strip() + "\n")
        elif line.startswith("  level "):
            w("- " + line.strip()[6:] + "\n")
        i += 1

    w(f"\n**Stop:** {d['stop_reason']} at depth {d['depth_reached']}; prompts {d['llm_calls_by_step']}, fresh model calls {d['llm_calls']}, cache hits {d.get('llm_cache_hits', '')}\n")
    w("\n### Held misconceptions\n")
    w(table(d["held_misconceptions"], ["concept", "misconception", "kind", "quote", "score", "shares_evidence_with"]))
    if d.get("error_evidence"):
        w("\n### Errors kept as evidence\n" + table(d["error_evidence"], ["concept", "error", "quote"]))
    w("\n### Broken concept edges\n" + table(d["broken_edges"], ["edge", "quote", "score", "consequence_of"]))
    r = d.get("root_cause") or {}
    w(f"\n### Root cause: {r.get('concept', 'none')}" + (f" / {r.get('misconception')}" if r.get("misconception") else "") + "\n")
    w("\n### Level per concept\n")
    w(table([{"concept": c, **v, "also": ", ".join(v.get("also_shown", []) or v.get("also_held", []))} for c, v in d["levels"].items()],
            ["concept", "level", "way", "misconception", "source", "quote", "rule", "also", "note"]))
    w(f"\n### Overall level: {d['overall_level']}\n")
    w("\nClause coverage (final):\n" + table([{"clause": k, "covered by": v} for k, v in d["clause_coverage"].items()], ["clause", "covered by"]))
    if d.get("unexplained_clauses"):
        w("\nClauses no evidence explains: " + " | ".join(d["unexplained_clauses"]) + "\n")
    f = RESULTS_DIR / "viewer" / f"{sid}_figure{fig_no:02d}.png"
    if f.exists():
        w(f"\nFigure {fig_no} (final picture): {f}\n")

    w("\n## 5. Every labelled edge (the evidence list, kept or not)\n")
    w(table(d["evidence"], ["depth", "source", "edge", "kind", "label", "prune_score", "confidence", "score", "clauses", "quote"]))
    w("\n## 6. The paths (what the keep step kept, depth by depth)\n")
    w(table(d["paths"], ["depth", "source", "edge", "kind", "label", "score", "clauses"]))
    w("\n## 7. Raw traversal log\n```\n" + "\n".join(log) + "\n```\n")
    w("\n## 8. Full diagnosis JSON\n```json\n" + json.dumps(d, indent=1, ensure_ascii=False) + "\n```\n")

    outp = RESULTS_DIR / "viewer" / f"{sid}_steps.md"
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text("".join(out), encoding="utf-8")
    return outp


if __name__ == "__main__":
    p = main(sys.argv[1])
    print("wrote", p, p.stat().st_size, "bytes")
