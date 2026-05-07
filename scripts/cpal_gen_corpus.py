"""
Generate a student-voice training corpus for LP-level and wrong-model
classification heads.

Unlike the earlier approach (paraphrasing the rubric text + signal text),
this targets *student voice* — how a real student at LP level X on concept
C, or a student holding wrong model M, would write a message to a tutor.

Output: data/mental_models/training_corpus.json
  {
    "lp": [
      {"text": "...", "concept": "null_pointer", "lp_level": "L2"},
      ...
    ],
    "wm": [
      {"text": "...", "concept": "null_pointer", "wm_id": "NP-A"},
      ...
    ]
  }

Incrementally cached — safe to kill and resume.
"""
import os, sys, json, time
from pathlib import Path
import requests

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOGUE_PATH = ROOT / "data" / "mental_models" / "wrong_models_catalogue.json"
CORPUS_PATH    = ROOT / "data" / "mental_models" / "training_corpus.json"
CACHE_PATH     = ROOT / "data" / "mental_models" / "gen_cache.json"

OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_MODEL = os.environ.get("CPAL_OLLAMA_MODEL", "llama3.2:latest")
PER_GROUP    = int(os.environ.get("CPAL_PER_GROUP", "20"))   # 20 examples per (concept,level) or (concept,wm)
TIMEOUT      = 60.0


LP_LEVELS = ["L1", "L2", "L3", "L4"]
LP_DESCRIPTORS = {
    "L1": (
        "beginner who only observes the symptom. "
        "They see an error or unexpected output but cannot name the rule, "
        "distinction, or mechanism. They often say things like 'it doesn't "
        "work' or 'I don't understand why' without further articulation."
    ),
    "L2": (
        "student who knows the rule but cannot explain the mechanism. "
        "They know what to do or what distinction applies, but cannot "
        "articulate why the language/runtime behaves that way at the "
        "execution level. They use rule words without causal traces."
    ),
    "L3": (
        "student who can trace the mechanism at the execution level. "
        "They explain what the compiler checks, what the runtime allocates, "
        "where references point, how steps sequence. They use mechanism "
        "vocabulary (heap, stack, reference, compile-time, runtime, trace) "
        "and causal language (because, therefore, when)."
    ),
    "L4": (
        "student who generalises the mechanism to novel cases. They "
        "spontaneously connect this concept to other concepts sharing "
        "the same underlying principle, name design choices, or predict "
        "behaviour in unfamiliar scenarios. They use language like "
        "'same principle', 'applies to', 'why Java chose', 'in general'."
    ),
}


def load_cache():
    if CACHE_PATH.exists():
        with open(CACHE_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=1)


def ollama(prompt: str, num_predict: int = 700) -> str:
    r = requests.post(OLLAMA_URL, json={
        "model":   OLLAMA_MODEL,
        "prompt":  prompt,
        "stream":  False,
        "options": {"temperature": 0.9, "top_p": 0.95,
                    "num_predict": num_predict},
    }, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json().get("response", "")


def parse_lines(text: str, n: int) -> list:
    """Extract student-voice lines, filter rubbish, return up to n."""
    out = []
    for raw in text.splitlines():
        s = raw.strip().strip("-•*.0123456789:)] \t\"'")
        if not s: continue
        # Skip headers like "Here are 20 messages:" etc.
        if s.lower().startswith(("here are", "here's", "message ",
                                  "output", "as a ", "note:")):
            continue
        if 15 < len(s) < 320 and s[0].isalpha():
            out.append(s)
            if len(out) >= n: break
    return out


def build_lp_prompt(concept_id: str, java_concept: str, level: str,
                    rubric: str) -> str:
    desc = LP_DESCRIPTORS[level]
    return (
        f"You are simulating a student learning Java. The concept is "
        f"'{concept_id}' ({java_concept}).\n\n"
        f"Write {PER_GROUP} short messages (1-3 sentences each) that a {desc}\n\n"
        f"Rubric for this level: {rubric}\n\n"
        f"RULES:\n"
        f"- Each message is what a student would say to a tutor.\n"
        f"- Vary vocabulary significantly across the {PER_GROUP} messages.\n"
        f"- Do NOT repeat the rubric. Do NOT use the phrase 'logical_step'.\n"
        f"- Sound like a real student, not a textbook.\n"
        f"- Output one message per line. No numbering, no bullets, no quotes.\n"
    )


def build_wm_prompt(concept_id: str, java_concept: str, wm) -> str:
    return (
        f"You are simulating a student learning Java. The concept is "
        f"'{concept_id}' ({java_concept}).\n\n"
        f"The student holds this specific wrong mental model:\n"
        f"  Belief: {wm['wrong_belief']}\n"
        f"  Origin: {wm['origin']}\n\n"
        f"Write {PER_GROUP} short messages (1-3 sentences each) that a "
        f"confused student holding this exact misconception would send "
        f"to a tutor.\n\n"
        f"RULES:\n"
        f"- Each message demonstrates the misconception in their own words.\n"
        f"- Vary vocabulary significantly — each of the {PER_GROUP} should "
        f"use different phrasings.\n"
        f"- Do NOT copy the documented signals verbatim.\n"
        f"- Sound like a real student, not a textbook.\n"
        f"- Output one message per line. No numbering, no bullets, no quotes.\n"
    )


def main():
    with open(CATALOGUE_PATH, encoding="utf-8") as f:
        cat = json.load(f)
    concepts = sorted(cat["concepts"].keys())
    cache = load_cache()

    lp_examples = []
    wm_examples = []
    total_groups = len(concepts) * (len(LP_LEVELS) + 3)  # 3 wm per concept typically
    done = 0
    t0 = time.time()

    # --- LP groups ---
    for cid in concepts:
        entry = cat["concepts"][cid]
        java_concept = entry.get("java_concept", "")
        for lvl in LP_LEVELS:
            key = f"lp|{cid}|{lvl}"
            if key in cache:
                examples = cache[key]
            else:
                rubric = entry.get("lp_rubric", {}).get(lvl, "")
                prompt = build_lp_prompt(cid, java_concept, lvl, rubric)
                try:
                    raw = ollama(prompt, num_predict=700)
                    examples = parse_lines(raw, PER_GROUP)
                except Exception as e:
                    print(f"  [ERR] LP {cid} {lvl}: {e}", flush=True)
                    examples = []
                cache[key] = examples
                save_cache(cache)
            for t in examples:
                lp_examples.append(
                    {"text": t, "concept": cid, "lp_level": lvl}
                )
            done += 1
            if done % 5 == 0 or done == total_groups:
                elapsed = time.time() - t0
                print(f"  LP [{cid}/{lvl}] group {done}  "
                      f"lp_total={len(lp_examples)}  elapsed={elapsed:.0f}s",
                      flush=True)

    # --- WM groups ---
    for cid in concepts:
        entry = cat["concepts"][cid]
        java_concept = entry.get("java_concept", "")
        for wm in entry.get("wrong_models", []):
            key = f"wm|{cid}|{wm['id']}"
            if key in cache:
                examples = cache[key]
            else:
                prompt = build_wm_prompt(cid, java_concept, wm)
                try:
                    raw = ollama(prompt, num_predict=700)
                    examples = parse_lines(raw, PER_GROUP)
                except Exception as e:
                    print(f"  [ERR] WM {cid} {wm['id']}: {e}", flush=True)
                    examples = []
                cache[key] = examples
                save_cache(cache)
            for t in examples:
                wm_examples.append(
                    {"text": t, "concept": cid, "wm_id": wm["id"]}
                )
            done += 1
            if done % 5 == 0:
                elapsed = time.time() - t0
                print(f"  WM [{cid}/{wm['id']}] group {done}  "
                      f"wm_total={len(wm_examples)}  elapsed={elapsed:.0f}s",
                      flush=True)

    with open(CORPUS_PATH, "w", encoding="utf-8") as f:
        json.dump({"lp": lp_examples, "wm": wm_examples}, f, indent=1)

    print(f"\nDone.  Corpus written: {CORPUS_PATH}")
    print(f"  LP examples: {len(lp_examples)}")
    print(f"  WM examples: {len(wm_examples)}")


if __name__ == "__main__":
    main()
