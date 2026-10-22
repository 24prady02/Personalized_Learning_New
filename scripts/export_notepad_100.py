"""
export_notepad_100.py — one plain-text report (opens in Notepad) of the LP classifier on the
100 classified answers: the algorithm step by step, the knowledge graph's level and edge logic,
how the LLM judge is used, the results, and every answer's concept map and step outputs.

Usage: python scripts/export_notepad_100.py [run folder, default scenario_run_100_rubric]
Writes <run>/LP_classifier_report.txt (run scripts/report_100.py first).
With --one-file: writes <run>/LP_classifier_ONE_FILE.txt, the same steps and results with shorter
quotes of graph text and no line wrapping, small enough to upload to Claude as one file.
"""
from __future__ import annotations

import json
import os
import sys
import textwrap
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.environ["LP_JUDGE_PROMPT"] = "rubric"          # show the rubric judge's prompt and ladder

from run_student_scenarios import asked_part  # noqa: E402
from src.lp_percpt import judge as judgelib  # noqa: E402
from src.lp_percpt import models  # noqa: E402
from src.lp_percpt.identify import _cue_hits, _focus, _word_hit, identify, split_clauses  # noqa: E402
from src.lp_percpt.thresholds import (KEEP_SCORE, MAX_CONCEPTS, MIS_FLOOR, RELATIVE_KEEP,  # noqa: E402
                                      SEM_FLOOR, W_ASKED, W_CODE, W_CODE_SHOWN, W_MIS, W_SEM, W_WORD)
from src.lp_percpt.knowledge import get_knowledge  # noqa: E402

KG = get_knowledge()
COMPACT = "--one-file" in sys.argv


def cut(s, n):
    """Shorten graph text in the one-file report (the full text is in the knowledge graph)."""
    s = str(s or "")
    return s if not COMPACT or len(s) <= n else s[:n].rstrip() + "..."
STUDENTS = ROOT / "output" / "scenario_run_100_rubric" / "students"   # set in main() for the run exported


def link_detail(text, code, asked):
    """Step 2 recomputed with the run's inputs (MiniLM only): concept -> its score parts."""
    return {h.concept: h for h in identify(text, KG, code=code, clauses=split_clauses(text), asked=asked)}


def closest_rule(text, cid):
    """The L1-L4 way rule of a concept closest to the answer (why the extra concept was added)."""
    rules = [(lv, w.name, r) for lv in ("L1", "L2", "L3", "L4") for w in KG.concepts[cid].ways.get(lv, []) for r in w.rules]
    if not rules:
        return None
    sim = models.similarity([text], [r for _, _, r in rules])[0]
    j = int(sim.argmax())
    return rules[j], float(sim[j])


def level_logic(cid, level, way):
    """The has_level edge (cid -> cid@level): its logic and the chosen way's exact rule and boundary."""
    e = judgelib._edges().get((cid, level))
    if not e:
        return None, [], "no has_level edge"
    all_ways = e.get("ways", [])
    ws = [w for w in all_ways if w.get("way") == way]
    if not ws:
        names = ", ".join(dict.fromkeys(w.get("way") for w in all_ways))
        return e.get("logic", ""), [], f"the judge named way '{way}', which is not a way of this {level} edge; its ways are: {names}"
    note = f"{len(ws)} ways named '{way}' on this edge; the judge did not say which, all shown" if len(ws) > 1 else ""
    return e.get("logic", ""), ws, note

LV = ["L0", "L1", "L2", "L3", "L4", "none"]
W = 100
EDGE_MEANING = {
    "contains": "section -> topic: the section teaches the topic",
    "precedes": "section -> section: book order",
    "section_prerequisite": "section -> section: a section's ideas are needed before the next",
    "prerequisite": "concept A -> concept B: A must be understood before B (edge logic says why)",
    "parallel": "concept <-> concept: two constructs that differ in one rule (edge logic says how)",
    "misconception": "concept -> misconception node: a documented wrong belief (logic) and the right rule (twin_logic)",
    "error": "concept -> error node: a compile / run-time / logic error, the wrong rule and the right one",
    "has_level": "concept -> concept@Lk learning-level node: the WAYS of reaching level Lk (edge logic)",
}


def link_parts(h, cid, text, code, asked):
    """Workflow A, the link score of one concept split into its parts (identify.py formula)."""
    c = KG.concepts[cid]
    in_text, in_code, words = _cue_hits(c, text.lower(), text, code)
    focus = _focus(asked, code) if asked else ""
    asked_h = bool(focus) and (any(p.search(focus) for p in c.code_cues) or any(_word_hit(w, focus.lower()) for w in c.word_cues))
    word_pts = sum(2 if " " in w.strip() else 1 for w in words[:3])
    parts = [("code cues in the answer", W_CODE * min(len(in_text), 2), ", ".join(in_text)),
             ("code cue only in the question's code", W_CODE_SHOWN * min(len(in_code), 1), ", ".join(in_code[:1])),
             ("cue in the question part asked", W_ASKED * asked_h, ""),
             ("word cues", W_WORD * word_pts, ", ".join(words[:3])),
             ("meaning similarity", W_SEM * max(0.0, h.meaning_sim - SEM_FLOOR), f"cosine {h.meaning_sim} with \"{cut(h.meaning_match, 90)}\""),
             ("misconception-edge similarity", W_MIS * max(0.0, h.misconception_sim - MIS_FLOOR),
              f"cosine {h.misconception_sim} with {h.misconception_match}: \"{cut(KG.misconceptions[h.misconception_match].wrong_belief, 90)}\""
              if h.misconception_match else f"best cosine {h.misconception_sim} (below {MIS_FLOOR})")]
    return parts


def scenario_block(r, s, concepts, edges, pair_edges):
    """One scenario, in the order the algorithm runs: no-claim -> semantic matching (nodes singled out)
    -> intermediate graph -> graph evidence -> code run -> LLM judge (input, output) -> fusion (final
    level) -> final concept map."""
    out = []
    asked = asked_part(s.get("question_text", ""), s.get("scenario_type", ""))   # exactly what the engine got
    code = s.get("code", "") or ""
    lvname = {0: "L0", 1: "L1", 2: "L2", 3: "L3", 4: "L4"}
    I1, I2 = ("      ", "        ") if COMPACT else ("          ", "              ")
    out += ["", "#" * (40 if COMPACT else W), f"SCENARIO {r['id']}", "#" * (40 if COMPACT else W),
            wrap("Question part: " + (asked or s.get("question_text", "") + "  (whole question; no part named)"), "  "),
            wrap("Code: " + (code[:300] + (" ..." if len(code) > 300 else "") if code else "(none)"), "  "),
            wrap("Answer: " + r["text"], "  ")]

    # STEP 1
    if set(r["gates"]) & {"no_claim", "help_seeking"}:
        out += ["", "  STEP 1  NO-CLAIM CHECK -> NO CLAIM (a real question, no answer of its own)",
                "          the algorithm stops here: no semantic matching, no nodes, no judge call.",
                "  => FINAL LEVEL: none",
                "  => FINAL CONCEPT MAP: unchanged (no nodes, no edges)",
                f"  (classified level: {r['label']})"]
        return out
    out += ["", "  STEP 1  NO-CLAIM CHECK -> claim, continue"]

    # STEP 2 semantic matching
    out += ["", "  STEP 2  SEMANTIC MATCHING (answer -> graph concept nodes)"]
    out.append("    2a  clauses the answer is split into:")
    out += [wrap(f"({i + 1}) {c}", I1) for i, c in enumerate(split_clauses(r["text"]))]
    det = link_detail(r["text"], code, asked)
    best = max((h.score for h in det.values()), default=0.0)
    out.append("    2b  link score per candidate node (cue, meaning and misconception-edge matching):")
    for cc, sc in r["linked"]:
        h = det.get(cc)
        out.append(f"{I1}[{cc}]  link score {sc}")
        if h is None:
            continue
        for name, pts, what in link_parts(h, cc, r["text"], code, asked):
            if pts or (what and "below" not in what and name.startswith(("meaning", "misconception"))):
                out.append(wrap(f"+ {pts:.2f}  {name}" + (f": {what}" if what else ""), I2))
    out.append(wrap(f"2c  keep rule: score >= {KEEP_SCORE} and >= {RELATIVE_KEEP} x best ({best:.2f}), at most "
                    f"{MAX_CONCEPTS}", "    "))
    for cc in r["extra"]:
        bst = closest_rule(r["text"], cc)
        txt = f"2d  extra node for the judge: {cc}"
        if bst:
            (lv, wname, rule), sim = bst
            txt += f" (its {lv} way '{wname}' is the closest way rule, cosine {sim:.3f}: \"{cut(rule, 120)}\")"
        out.append(wrap(txt, "    "))
    if not r["extra"]:
        out.append("    2d  extra node for the judge: none")
    names = [cc for cc, _ in r["linked"]] + r["extra"]
    out.append(wrap("=> NODES SINGLED OUT: " + (", ".join(f"{cc} ({sc})" for cc, sc in r["linked"]) or "none")
                    + (f" + extra {', '.join(r['extra'])}" if r["extra"] else ""), "    "))

    # STEP 3 intermediate graph
    sp = STUDENTS / f"{s['student']}.json"
    nodes = json.loads(sp.read_text(encoding="utf-8")).get("nodes", {}) if sp.exists() else {}
    out += ["", "  STEP 3  INTERMEDIATE GRAPH (the singled-out nodes placed on the Chapter-1 graph)"]
    between = [e for i, a in enumerate(names) for b in names[i + 1:] for e in pair_edges.get(frozenset((a, b)), [])]
    out.append("    3a  edges between the singled-out nodes, with their edge logic:")
    out += [wrap(f"{e['source']} -{e['type']}-> {e['target']}: {cut(e.get('logic', ''), 200)}", I1) for e in between] \
        or [f"{I1}none"]
    out.append("    3b  each node's own edges in the graph:")
    for cc in names:
        pre = sorted({e["source"] for e in edges if e["type"] == "prerequisite" and e["target"] == cc})
        mis = [e["target"] for e in edges if e["type"] in ("misconception", "error") and e["source"] == cc]
        out.append(wrap(f"{cc}: prerequisites {', '.join(pre) or 'none'}; misconception/error edges "
                        f"{', '.join(mis[:4])}{' ...' if len(mis) > 4 else ''}", I1))
    nb = [cid for cid, n in nodes.items() if not n.get("observed")]
    out.append(wrap("3c  neighbour nodes added to the map (not assessed): " + (", ".join(nb) or "none")
                    + (" (inferred levels in STEP 9)" if COMPACT and nb else ""), "    "))

    # STEP 4 graph evidence
    out += ["", "  STEP 4  GRAPH EVIDENCE PER NODE (answer clause -> graph statement, check, score, status, level way)"]
    ev = [(c2["concept"], e) for c2 in s["concepts"] for e in c2.get("evidence", [])
          if not e["statement"].startswith("confirmed by the run") and e["check"] not in ("wrong_trace", "own_run")]
    cl = {c: i + 1 for i, c in enumerate(split_clauses(r["text"]))}
    quote = (lambda c: f"clause ({cl[c]})" if COMPACT and c in cl else f"\"{c[:80]}\"")
    out += [wrap(f"{cc} {e['check']}: {quote(e['clause'])} -> \"{cut(e['statement'][:120], 90)}\" ({e['score']}, "
                 f"{e['status']}, {e.get('way') or '-'})", I1) for cc, e in ev] or [f"{I1}none"]
    out.append("    rule level reached per node (ladder walk over E1-E4):")
    out += [f"{I1}{cid}: {lvname.get(n.get('level'), '-')} - {n.get('stop_reason')}" for cid, n in nodes.items()
            if n.get("observed")] or [f"{I1}none"]

    # STEP 5 code run
    out += ["", "  STEP 5  CODE RUN"]
    out.append(wrap("run output: " + (str(s.get("run_output"))[:300] if s.get("run_output") else "(not run)"), I1))
    out += [wrap(f, I1) for f in r["run_facts"]] or [f"{I1}no claim of the answer could be checked by the run"]

    # STEP 6-7 LLM judge
    sent = [c2["concept"] for c2 in s["concepts"]]
    out += ["", "  STEP 6  LLM JUDGE INPUT (Claude)",
            wrap(f"rubric (section 4) + question part + code + run output + answer + {len(r['run_facts'])} code-run "
                 f"fact(s) + the L0-L4 has_level ways of the nodes: {', '.join(sent)}", I1)]
    out += ["", "  STEP 7  LLM JUDGE OUTPUT"]
    out.append("    7a  level per node, and the has_level edge logic it lands on:")
    for c2 in s["concepts"]:
        j = c2.get("judge") if isinstance(c2.get("judge"), dict) else None
        if not j:
            out.append(f"{I1}[{c2['concept']}] -> none (the judge gave this node no level)")
            continue
        lv, way = j.get("level"), j.get("way") or ""
        out.append(f"{I1}[{c2['concept']}] -> {lv} via '{way or '-'}' (correct={j.get('correct')})")
        out.append(wrap(f"quote \"{j.get('quote', '')}\"; reason: {j.get('why', '')}", I2))
        if lv in LV[:5]:
            logic, ws, note = level_logic(c2["concept"], lv, way)
            if logic:
                out.append(wrap(f"edge {c2['concept']} -has_level-> {c2['concept']}@{lv}: {logic}", I2))
            if note:
                out.append(wrap(f"note: {note.replace('all shown', 'first shown') if COMPACT else note}", I2))
            for w in ws[:1 if COMPACT else 2]:
                out.append(wrap(f"way {w.get('way')} [{w.get('rule_type')}]: {cut(w.get('edge_logic') or w.get('exact_rule', ''), 200)}", I2))
                if w.get("boundary") and not COMPACT:
                    out.append(wrap(f"boundary: {w['boundary']}", I2))
    out.append(wrap(f"7b  overall level for the answer: {r['judge_answer'] or '-'}; main concept "
                    f"{r['judge_main'] or '-'}; reason: {r['judge_why'] or '-'}", "    "))

    # STEP 8 fusion
    run_l0 = r["set_by"] == "code run (L0)"
    chain = ["rule 1 no claim -> none: no",
             f"rule 2 code run proved a wrong trace / reproduced misconception -> L0: {'YES' if run_l0 else 'no'}"]
    if not run_l0:
        chain.append(f"rule 3 judge overall level: {'YES -> ' + r['judge_answer'] if r['judge_answer'] else 'no overall level'}")
        if not r["judge_answer"]:
            chain.append(f"rule 4 highest per-node level: {r['final']}")
    out += ["", "  STEP 8  FUSION", wrap("; ".join(chain), I1),
            f"  => FINAL LEVEL: {r['final']}   (set by {r['set_by']}; classified level: {r['label']})"]

    # STEP 9 final concept map
    out += ["", f"  STEP 9  FINAL CONCEPT MAP (nodes formed in students/{s['student']}.json, drawn in maps/{s['student']}.html)"]
    if COMPACT and nb:
        out.append(wrap("neighbour nodes (not assessed), inferred level: " + ", ".join(
            f"{cid} {lvname.get(nodes[cid].get('inferred_level'), '-')}" for cid in nb), I1))
    for cid, n in nodes.items():
        if not n.get("observed"):
            if COMPACT:
                continue
            out.append(f"{I1}node [{cid}]  not assessed (neighbour); inferred level {lvname.get(n.get('inferred_level'), '-')}")
            continue
        out.append(wrap(f"node [{cid}]  judge level {r['judge_concepts'].get(cid) or '-'}; rule level stored "
                        f"{lvname.get(n.get('level'), '-')}{' (provisional)' if n.get('provisional') else ''}; "
                        f"misconceptions held {', '.join((n.get('misconceptions') or {}).keys()) or 'none'}", I1))
    for cc in r["extra"]:
        out.append(f"{I1}node [{cc}]  judge level {r['judge_concepts'].get(cc) or '-'} (extra node, reported, not stored)")
    allnodes = list(nodes)
    map_edges = [e for i, a in enumerate(allnodes) for b in allnodes[i + 1:] for e in pair_edges.get(frozenset((a, b)), [])]
    out.append(wrap("edges: " + ("; ".join(f"{e['source']} -{e['type']}-> {e['target']}" for e in map_edges) or "none"), I1))
    out.append(f"  => FINAL CONCEPT MAP: {sum(1 for n in nodes.values() if n.get('observed'))} assessed node(s), "
               f"{len(nb)} neighbour node(s), {len(map_edges)} edge(s); main concept {r['judge_main'] or '-'}")
    return out


def wrap(text, indent="    ", width=W):
    text = " ".join(str(text or "").split())
    if COMPACT:
        return indent + text if text else indent + "-"
    return textwrap.fill(text, width=width, initial_indent=indent, subsequent_indent=indent) if text else indent + "-"


def h1(out, title):
    out += ["", "=" * W, title.upper(), "=" * W]


def h2(out, title):
    out += ["", title, "-" * len(title)]


def main() -> None:
    global STUDENTS
    args = [a for a in sys.argv[1:] if a != "--one-file"]
    run = ROOT / "output" / (args[0] if args else "scenario_run_100_rubric")
    STUDENTS = run / "students"
    rep = json.loads((run / "report_100.json").read_text(encoding="utf-8"))
    res = {s["id"]: s for s in json.loads((run / "results.json").read_text(encoding="utf-8"))["scenarios"]}
    g = json.loads((ROOT / "data" / "chapter1_kg.json").read_text(encoding="utf-8"))
    edges = g["edges"]
    concepts = {c["id"]: c for c in g["concepts"]}
    levels_of = defaultdict(dict)
    for ln in g["learning_levels"]:
        levels_of[ln["concept"]][ln["level"]] = ln
    pair_edges = defaultdict(list)
    for e in edges:
        if e["type"] in ("prerequisite", "parallel"):
            pair_edges[frozenset((e["source"], e["target"]))].append(e)
    mis_nodes = {m["id"]: m for m in g["misconceptions_and_errors"]} if isinstance(g["misconceptions_and_errors"], list) else {}

    out = ["LP CLASSIFIER - CONCEPT MATCHING AND LEVEL CLASSIFICATION",
           "Chapter-1 Java learning ladder (L0-L4), 100 student answers",
           f"Run: {run.name}   Graph: {g['version']}   Report date: 2026-10-21"]

    # 1 results
    h1(out, "1. Results at a glance")
    n = rep["n"]
    out += [f"Exact match with classify_100_classified.xlsx : {rep['exact']}/{n} ({rep['exact'] / n:.0%})",
            f"Within one level (both sides levelled)        : {rep['within']}/{rep['levelled_pairs']}",
            f"Average gap (levels)                          : {rep['mae']}",
            "", "Per classified level (correct / answers):"]
    out += [f"    {k:5s} {rep['per_level'][k][0]:3d} / {rep['per_level'][k][1]}" for k in LV]
    out += ["", "Accuracy by version (exact, of 100):",
            "    NLI graph matching only ............................ 22",
            "    NLI + LLM judge fusion ............................. 58",
            "    LLM judge, NLI off ................................. 59",
            "    + no-claim check, judge overrules similarity L1 ... 63",
            "    + bare-output and empty-evidence fixes ............. 65",
            f"    Rubric-aligned LLM judge (current) ................. {rep['exact']}",
            "", "Label source: the classified levels (classify_100_classified.xlsx) were generated by an LLM.",
            "No human levels are used. All accuracy here is against the classified levels only."]

    # 2 graph
    h1(out, "2. The knowledge graph and its edge logic")
    c = g["counts"]
    out += [f"Chapter-1 graph (data/chapter1_kg.json), version {g['version']}.",
            f"Concepts {c['concepts']}, misconception nodes {c['misconception_nodes']}, error nodes {c['error_nodes']}, "
            f"learning-level nodes {c['learning_level_nodes']}, ways in has_level edge logic {c['ways_in_has_level_edge_logic']}.",
            "Six node types: section, topic, concept, misconception, error, learning level (concept@L0..L4)."]
    h2(out, "2.1 Edge types (what each edge's logic says)")
    cnt = Counter(e["type"] for e in edges)
    for t, k in cnt.most_common():
        out.append(f"  {t:21s} {k:4d}  {EDGE_MEANING.get(t, '')}")
        ex = next(e for e in edges if e["type"] == t)
        if t != "has_level":
            out.append(wrap(f"example {ex['source']} -> {ex['target']}: {ex.get('logic', '')}"
                            + (f" | right rule: {ex['twin_logic']}" if ex.get("twin_logic") else ""), "        "))
    h2(out, "2.2 The level ladder (learning-level nodes, same for every concept)")
    any_c = next(iter(levels_of))
    for lv in LV[:5]:
        ln = levels_of[any_c][lv]
        out.append(f"  {lv} {ln['name']}")
        out.append(wrap("Criterion: " + ln["criterion_general"].replace(any_c.replace("_", " "), "the concept"), "      "))
        out.append(wrap("Deciding question: " + ln["deciding_question"].replace(any_c.replace("_", " "), "the concept"), "      "))
    h2(out, "2.3 has_level edge logic: the ways of reaching a level")
    out += [wrap("Each concept has 5 has_level edges (L0..L4). The edge logic of each holds its WAYS. A way = "
                 "way name + rule type (one of 13 rule categories) + exact_rule (the rule of the concept the way "
                 "tests) + boundary (what is NOT this level) + correctness (correct, or an error that still shows "
                 "the level). L0 ways hold the everyday or wrong reading; L3 ways relate the concept to a neighbour "
                 "(filled from prerequisite / parallel edges) or state a purpose; L4 ways predict a change, diagnose "
                 "an error class or transfer to a new program.", "  ")]
    rt = Counter((w["rule_type"], w.get("rule_type_name", "")) for e in edges if e["type"] == "has_level" for w in e["ways"])
    out.append("  Rule types used by the ways (count):")
    out += [f"      {a:3s} {b:28s} {k}" for (a, b), k in rt.most_common()]
    wn = Counter((e["level"], w["way"]) for e in edges if e["type"] == "has_level" for w in e["ways"])
    out.append("  Way names per level (count of concepts that have them):")
    for lv in LV[:5]:
        out.append(wrap(f"{lv}: " + ", ".join(f"{w} ({k})" for (l, w), k in sorted(wn.items(), key=lambda x: -x[1]) if l == lv), "      "))

    # 3 algorithm
    h1(out, "3. The algorithm, step by step (what each step outputs)")
    steps = [
        ("Step 0  Input", "The student answer, the question part asked, and the question's code."),
        ("Step 1  No-claim check (evidence.no_claim)",
         "If every question in the message is a real question (why / how / is / do ...), every statement only reports "
         "the student's own situation, and it gives no reason or guess, the answer is 'none' and stops here. A tentative "
         "answer such as 'It prints 5, right?' is a claim. OUTPUT: claim / no claim."),
        ("Step 2  Semantic matching = concept linking (identify.py, MiniLM all-MiniLM-L6-v2)",
         "The answer is split into clauses and scored against all 173 concepts: link score = 2 x code-cue hits in the "
         "answer (max 2) + 1 x a code cue only in the question's code (max 1) + 1 x a cue in the question part asked "
         "+ 1 x word-cue points (max 3) + 4 x max(0, meaning similarity - 0.40) + 3 x max(0, misconception "
         "similarity - 0.50). Meaning similarity = best cosine (MiniLM) between a clause and the concept's "
         "'label: description' or one of its facts; misconception similarity = best cosine with the wrong belief of "
         "one of its misconceptions. A concept is linked when its score >= 1.0 and >= half the best score; at most 3, "
         "best first. One extra concept is added for the judge: the one whose L1-L4 way rules are closest to the "
         "answer (judge.extra_concept). OUTPUT: linked concepts + link scores + 1 extra concept."),
        ("Step 3  Concept map",
         "The linked concepts are placed on the Chapter-1 graph: the prerequisite and parallel edges between them (with "
         "their edge logic), their own prerequisites, and their misconception / error edges. The student's concept map "
         "(maps/<id>.html) is updated with each concept's level. OUTPUT: the answer's sub-graph."),
        ("Step 4  Code run (execution.py)",
         "The question's code is run. Values and output the answer states are checked against the run: CONFIRMED, or "
         "WRONG (a wrong trace). Each misconception's mutated program is also run; if it reproduces the student's wrong "
         "values, that misconception is held. OUTPUT: run output + facts (confirmed / wrong / misconception)."),
        ("Step 5  LLM judge (judge.py, Claude, one call per answer, LP_JUDGE=claude LP_JUDGE_PROMPT=rubric)",
         "Claude gets the rubric (system prompt, section 4), the question part, the code, the run output, the answer, the "
         "code-run facts, and for each linked + extra concept its L0-L4 ways from the has_level edge logic. It returns "
         "one overall level for the answer as a whole, the main concept, a reason, and a level + way + quote per concept. "
         "OUTPUT: answer_level, main_concept, why, per-concept levels."),
        ("Step 6  Fusion = final level",
         "'none' if Step 1 found no claim; else L0 if the code run proved a wrong trace or reproduced a misconception; "
         "else the judge's overall level; if the judge gave none, the per-concept fusion (highest concept level). "
         "OUTPUT: the final level and the step that set it."),
    ]
    for t, d in steps:
        out.append("")
        out.append("  " + t)
        out.append(wrap(d, "      "))
    out += ["", "  NLI (DeBERTa) is switched off (LP_NO_NLI=1): the LLM judge replaced it as the reader of the answer."]

    # 4 judge
    h1(out, "4. How the LLM is used as the judge")
    out += [wrap("Backend: Claude Code in headless mode (claude -p) on the user's subscription, no tools, run outside "
                 "the repository so it sees only the prompt. Every reply is cached by the hash of system prompt + "
                 "prompt (output/judge_cache), so the same answer is never paid for twice; LP_JUDGE_DRYRUN=1 counts "
                 "uncached prompts without calling. This run: 98 new calls.", "  ")]
    h2(out, "4.1 System prompt (verbatim)")
    out += ["    " + line for line in judgelib.RUBRIC_SYSTEM.splitlines()]
    h2(out, "4.2 User prompt (template)")
    out += ["    QUESTION (part asked): <the part the student answers>", "    CODE: <the question's code>",
            "    RUN OUTPUT: <what the code prints>", "    STUDENT ANSWER: <the answer>",
            "    FACTS FROM RUNNING THE CODE: CORRECT (...) / WRONG (...) / MISCONCEPTION: ...",
            "    CONCEPTS AND THEIR WAYS: <for each concept, its L0-L4 ways from the has_level edges, as below>",
            "    Give the answer's overall level, its main concept, and a level for each concept: <ids>."]
    ex_cid = "remainder_operator"
    h2(out, f"4.3 Example of the graph's level logic the judge sees ({ex_cid})")
    out += ["    " + line for line in judgelib.ladder_text(ex_cid).splitlines()]

    # 5 results detail
    h1(out, "5. Level classification detail")
    out.append("  Which step set the final level (correct / answers):")
    out += [f"    {k:24s} {v[0]:3d} / {v[1]}" for k, v in rep["set_by"].items()]
    out += ["", "  Confusion (rows = classified level, columns = final level):",
            "    " + "".join(f"{x:>7s}" for x in [""] + LV)]
    for a in LV:
        out.append("    " + f"{a:>7s}" + "".join(f"{rep['confusion'][f'{a}>{b}']:7d}" for b in LV))
    out += ["", f"  Concepts linked per answer: {rep['concepts_per_answer']} on average (+1 extra for the judge)",
            "", "  Most-linked concepts (linked by semantic matching / shown, judge level L0-L4):"]
    shown = dict(rep["shown_counts"])
    out += [f"    {cid:28s} linked {k:3d}   shown {shown.get(cid, 0):3d}" for cid, k in rep["linked_counts"][:15]]
    out += ["", "  Graph edges most often linked inside one answer:"]
    out += [f"    {a} - {b}: {k} answers" for a, b, k in rep["linked_pairs"][:10]]

    # 6 per scenario: the two workflows
    h1(out, "6. Every scenario, step by step (semantic matching -> graph -> evidence -> code run -> LLM judge -> fusion -> concept map)")
    out.append(wrap("For each scenario: Workflow A builds its concept map (answer -> concepts -> graph sub-map), "
                    "Workflow B decides its level (no-claim -> graph evidence -> code run -> LLM judge on the "
                    "has_level edge logic -> fusion). Every intermediate output is listed in order; the final "
                    "concept map and the final level come last in each workflow.", "  "))
    for r in rep["rows"]:
        s = res[r["id"]]
        out += scenario_block(r, s, concepts, edges, pair_edges)

    h1(out, "7. Files and switches")
    out += ["  output/scenario_run_100_rubric/results.json        everything the engine returned",
            "  output/scenario_run_100_rubric/steps_100_rubric.xlsx  every step per answer (spreadsheet)",
            "  output/scenario_run_100_rubric/maps/<id>.html       each student's concept map",
            "  output/scenario_run_100_rubric/report_100.json      the scores in this report",
            "  output/judge_cache/                                 saved Claude replies",
            "  Switches: LP_JUDGE=claude  LP_JUDGE_PROMPT=rubric  LP_NO_NLI=1  LP_JUDGE_DRYRUN=1",
            "  Re-run:  python scripts/run_student_scenarios.py --ids <ids.json> --out output/<run>",
            "           python scripts/report_100.py <run>   then   python scripts/export_notepad_100.py <run>",
            "  Online report: https://claude.ai/artifact/EsSnNbD4zhqUskVsB4SVH2"]

    # index of every scenario: where its two workflows start (line numbers after the index is inserted)
    finals = {r["id"]: (r["final"], r["label"]) for r in rep["rows"]}
    lines = "\n".join(out).split("\n")
    idx_head = ["", "=" * W, "INDEX - ALL 100 SCENARIOS (line where each scenario's workflows start; Ctrl+G in Notepad)",
                "=" * W, f"  {'ID':6s} {'line':>6s}   final   classified"]
    n_idx = len(idx_head) + len(finals) + 1
    start = {ln.split()[1]: i + 1 + n_idx for i, ln in enumerate(lines) if ln.startswith("SCENARIO S")}
    idx = idx_head + [f"  {sid:6s} {start[sid]:6d}   {finals[sid][0]:5s}   {finals[sid][1]}" for sid in finals] + [""]
    lines = lines[:3] + idx + lines[3:]
    out = lines
    path = run / ("LP_classifier_ONE_FILE.txt" if COMPACT else "LP_classifier_report.txt")
    path.write_text("\n".join(out) + "\n", encoding="utf-8-sig")
    print("wrote", path, f"({len(out)} lines)")


if __name__ == "__main__":
    main()
