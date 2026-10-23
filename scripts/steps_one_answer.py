"""Run one answer through the current pipeline (pick + max_level + relation check) and print every step
with its calculation.  Usage: python scripts/steps_one_answer.py . <out dir>  (edit CODE, QUESTION, ANSWER below)"""
import json, os, re, sys, shutil
from pathlib import Path
ROOT = Path(sys.argv[1]); OUT = Path(sys.argv[2])
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from src.lp_percpt.engine import LPPercptEngine
from src.lp_percpt.execution import get_tracer
from src.lp_percpt import judge as judgelib, identify as idl, evidence as evl
from src.lp_percpt.thresholds import (MIN_WORDS, W_CODE, W_CODE_SHOWN, W_ASKED, W_WORD, W_SEM, W_MIS,
                                      SEM_FLOOR, MIS_FLOOR, KEEP_SCORE, MAX_CONCEPTS_PICK)

CODE = "int count;\nSystem.out. Println(count);"
QUESTION = "What does the system print?"
ANSWER = "It will print 0."
shown = f"\n{QUESTION}\n{CODE}"

# capture what goes to Claude and what comes back
cap = {}
_bp, _jd = judgelib.build_prompt, judgelib.judge
def bp(*a, **k):
    cap["prompt"] = _bp(*a, **k)
    cap["facts"] = a[3] if len(a) > 3 else k.get("facts")
    return cap["prompt"]
def jd(p):
    cap["reply"] = _jd(p)
    return cap["reply"]
judgelib.build_prompt, judgelib.judge = bp, jd

if OUT.exists():
    shutil.rmtree(OUT)
eng = LPPercptEngine(store_dir=OUT / "students", map_dir=OUT / "maps", review_log=None)
kg = eng.kg
r = eng.process("NEW1", ANSWER, code=CODE, shown_text=shown, session_id="one", asked=QUESTION)
J = r.get("judge") or {}
cs = r["concepts"]
assessed = [c for c in cs if c.get("assessed")]
def L(): print("-" * 78)

print("=" * 78); print("INPUT")
print("  Question:", QUESTION)
print("  Code:    ", CODE.replace("\n", "  |  "))
print("  Answer:  ", ANSWER)
print("  Switches:", ", ".join(f"{k}={os.environ[k]}" for k in sorted(os.environ) if k.startswith("LP_")))

L(); print("STEP 0  prompt gates (G1 content, G2 help-seeking, G2b no-claim)")
cw = evl.content_words(ANSWER); ct = evl._CODE_TOKEN.findall(ANSWER); oc = evl._OUTPUT_CLAIM.search(ANSWER)
print(f"  help_seeking = {evl.help_seeking(ANSWER)}   no_claim = {evl.no_claim(ANSWER)}")
print(f"  content words {cw} = {len(cw)}  +  values/code tokens {ct} = {len(ct)}  ->  {len(cw) + len(ct)} vs MIN_WORDS {MIN_WORDS}")
print(f"  output claim: {oc.group(0)!r}" if oc else "  output claim: none")
print(f"  G1 content gate fires = {evl.content_gate(ANSWER, MIN_WORDS)}"
      + ("  (an output claim passes whatever the count)" if oc and len(cw) + len(ct) < MIN_WORDS else ""))
print(f"  -> prompt gates: {r['prompt_gates'] or 'none'}")

L(); print("STEP 1  semantic matching (concept linking)")
print(f"  score = {W_CODE}*codecue_in_answer(max 2) + {W_CODE_SHOWN}*codecue_only_in_question_code(max 1) + {W_ASKED}*cue_in_question_asked")
print(f"        + {W_WORD}*word_cue_pts(max 3) + {W_SEM}*max(0, meaning_sim - {SEM_FLOOR}) + {W_MIS}*max(0, misconception_sim - {MIS_FLOOR})")
print(f"  kept: score >= {KEEP_SCORE}, best first, up to {MAX_CONCEPTS_PICK} (LP_LINK_PICK shortlist)")
hits = idl.identify(ANSWER, kg, code=CODE, clauses=idl.split_clauses(ANSWER),
                    asked=QUESTION)
focus = idl._focus(QUESTION, CODE).lower()
for h in hits:
    c = kg.concepts[h.concept]
    code_h, shown_h, word_h = idl._cue_hits(c, ANSWER.lower(), ANSWER, CODE)
    wp = sum(2 if " " in w.strip() else 1 for w in word_h[:3])
    asked_h = int(any(p.search(focus) for p in c.code_cues) or any(idl._word_hit(w, focus) for w in c.word_cues))
    sem = W_SEM * max(0.0, h.meaning_sim - SEM_FLOOR)
    mis = W_MIS * max(0.0, h.misconception_sim - MIS_FLOOR)
    p = [W_CODE * min(len(code_h), 2), W_CODE_SHOWN * min(len(shown_h), 1), W_ASKED * asked_h, W_WORD * wp]
    print(f"\n  {h.concept}  = {p[0]} + {p[1]} + {p[2]} + {p[3]} + {W_SEM}*({h.meaning_sim:.3f}-{SEM_FLOOR})={sem:.3f}"
          f" + {W_MIS}*({h.misconception_sim:.3f}-{MIS_FLOOR})={mis:.3f}  =  {h.score:.3f}")
    print(f"      code cues in answer {code_h or '-'} | only in question code {shown_h or '-'} | word cues {word_h or '-'} | in question asked {bool(asked_h)}")
    print(f"      best meaning match: {h.meaning_match[:90]!r}")
    if h.misconception_match:
        print(f"      misconception match: {h.misconception_match}")

L(); print("STEP 2  code run")
tr = get_tracer()
ok, err = tr.compiles(CODE)
print(f"  compiles = {ok}")
for line in (err or "").strip().splitlines():
    print("    " + line)
trace = tr.trace(CODE, hint=shown)
print(f"  run output = {trace.run.output!r}" if trace else "  run output = none (no trace: the code does not compile)")
print(f"  run facts given to the judge: {cap.get('facts') or 'none'}")
for c in cs:
    ch = c.get("checks") or {}
    if ch:
        print(f"  {c['concept']:<24} checks {ch}  held {c.get('held') or '-'}  refuted {c.get('refuted') or '-'}")
    for e in c.get("evidence", []):
        print(f"      [{e['check']} {e.get('status', '')}] {e['statement'][:100]}  (score {e.get('score')})")

L(); print("STEP 3  LLM judge (Claude)")
if "prompt" not in cap:
    print("  not called")
else:
    print(f"  prompt sent: {len(cap['prompt'])} chars (~{len(cap['prompt']) // 4} tokens); concepts offered: {J.get('concepts')}")
    rep = cap.get("reply") or {}
    if rep.get("unavailable"):
        print("  UNAVAILABLE:", rep["unavailable"])
    print("  Claude's reply:")
    for line in json.dumps({k: v for k, v in rep.items() if k != "raw"}, indent=2, ensure_ascii=False).splitlines():
        print("    " + line)

L(); print("STEP 4  fusion (per concept)")
print("  rules: run L0 -> L0 (wrong rule) | run L2 + judge L1 -> L1 | judge L0 -> L0 (wrong rule)")
print("         | level from a weak reader (nli / relation cue / similarity) -> judge's level | else keep")
print("         | Claude gave the concept no level (pick mode) -> not stored")
for c in cs:
    j = c.get("judge") if isinstance(c.get("judge"), dict) else None
    st = "stored" if not c.get("gates") else "not stored: " + ", ".join(c["gates"])
    print(f"  {c['concept']:<24} judge {(j or {}).get('level') or '-':<4} -> {c.get('prompt_level')}  set by {c.get('level_source') or '-'}"
          f"  wrong_rule={c.get('wrong_rule')}  ({st})")
    print(f"      reason: {c.get('prompt_reason') or c.get('stop_reason')}")

L(); print("STEP 5  relation edges (student edge = stated AND quote found in answer AND both ends stored)")
norm = lambda t: " ".join(re.findall(r"\w+", (t or "").lower()))
stored = {c["concept"] for c in assessed if "judge_no_level" not in (c.get("gates") or [])}
rels = J.get("relations") or []
if not rels:
    print("  no prerequisite/parallel edges between the shortlisted concepts")
for rel in rels:
    m = re.match(r"\s*(\w+)\s*-(\w+)->\s*(\w+)", str(rel.get("edge", "")))
    if not m:
        continue
    a, t, b = m.groups()
    qf = bool(norm(rel.get("quote"))) and norm(rel.get("quote")) in norm(ANSWER)
    se = bool(rel.get("stated")) and qf and a in stored and b in stored
    print(f"  ({a}, {t}, {b}): stated={bool(rel.get('stated'))} AND quote_found={qf} AND {a} stored={a in stored}"
          f" AND {b} stored={b in stored}  ->  {se}   quote={rel.get('quote')!r}")

L(); print("FINAL  LP_FINAL=max_level")
lv = [(c["concept"], c["prompt_level"], c.get("wrong_rule")) for c in assessed if "judge_no_level" not in (c.get("gates") or [])]
print(f"  stored concepts (concept, level, wrong_rule): {lv or 'none'}")
wr = any(c.get("wrong_rule") for c in assessed)
max_level = "L0" if wr else max((c["prompt_level"] for c in assessed), default=None)
print(f"  any wrong rule = {wr}  ->  " + ("L0" if wr else f"highest level = {max_level}"))
final = None if set(r["prompt_gates"] or []) & {"no_claim", "help_seeking"} else max_level
print(f"  Claude's overall level (shown, not used by max_level): {J.get('answer_level')}  main concept: {J.get('main_concept')}")
print(f"\n  FINAL LEVEL: {final or 'none'}")
(OUT / "result.json").write_text(json.dumps({"engine": r, "judge_reply": cap.get("reply"), "final": final},
                                            indent=1, default=str, ensure_ascii=False), encoding="utf-8")
