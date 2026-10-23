# Step-by-step: "It will print 0."

| | |
|---|---|
| Question | What does the system print? |
| Code | `int count;` / `System.out. Println(count);` |
| Answer | It will print 0. |
| Pipeline | pick + max_level + relation check (`LP_JUDGE=claude LP_NO_NLI=1 LP_JUDGE_EDGES=1 LP_LINK_PICK=1 LP_FINAL=max_level LP_JUDGE_RELATIONS=1 LP_JUDGE_CACHE=judge_cache_rel`) |
| Claude calls | 1 (~9.5k tokens) |
| **Final level** | **L0** |

## Step 0 — Prompt gates

| Gate | Calculation | Result |
|---|---|---|
| G2 help-seeking | — | False |
| G2b no-claim | — | False |
| G1 content | content words `['print']` = 1 + values/code tokens `['0']` = 1 → **2** vs MIN_WORDS 3 | would fire |
| Output claim (new) | matches `'print 0'` → passes whatever the count | **gate does not fire** |

Prompt gates: none.

## Step 1 — Semantic matching (concept linking)

```
score = 2*codecue_in_answer(max 2) + 1*codecue_only_in_question_code(max 1) + 1*cue_in_question_asked
      + 1*word_cue_pts(max 3) + 4*max(0, meaning_sim - 0.40) + 3*max(0, misconception_sim - 0.50)
kept: score >= 1.0, best first, up to 8 (LP_LINK_PICK shortlist)
```

| Concept | Code in answer | Code only in question | Asked | Word | 4·(meaning − 0.40) | 3·(misconc. − 0.50) | **Score** |
|---|---|---|---|---|---|---|---|
| print | 0 | 0 | 1 | 1 | 4·(0.486−0.4) = 0.344 | 3·(0.589−0.5) = 0.267 | **2.610** |
| standard_output | 0 | 1 | 0 | 0 | 4·(0.584−0.4) = 0.736 | 0 (0.440) | **1.737** |
| declaration | 0 | 1 | 0 | 0 | 4·(0.488−0.4) = 0.352 | 0 (0.366) | **1.353** |
| statement | 0 | 1 | 0 | 0 | 4·(0.462−0.4) = 0.248 | 0 (0.376) | **1.247** |
| array_creation | 0 | 0 | 0 | 0 | 4·(0.655−0.4) = 1.020 | 0 (0.368) | **1.021** |
| empty_statement | 0 | 1 | 0 | 0 | 0 (0.377) | 0 (0.482) | **1.000** |
| int | 0 | 1 | 0 | 0 | 0 (0.348) | 0 (0.293) | **1.000** |
| variable | 0 | 1 | 0 | 0 | 0 (0.336) | 0 (0.302) | **1.000** |

Cues and best matches:

- **print**: word cue `print`; cue in the question asked; misconception match `PrintWithoutFinalNewline`; meaning: *"print(String s) prints the string (or "null" for a null reference)…"*
- **standard_output**: code cue `System\.out\.` in the question code; meaning: *"It changes no variables and returns nothing."*
- **declaration**: code cue `int count;` in the question code; meaning: *"A declaration produces no value and no output."*
- **statement**: code cue `;` at line end; meaning: *"A statement has no value; its result is its effect…"*
- **array_creation**: no cue, meaning only: *"It produces no output; printing it shows an address, not the elements."*
- **empty_statement**: code cue `)\s*;` at line end; meaning: *"An empty statement does nothing…"*
- **int**: code cue `int \w+` in the question code
- **variable**: code cue `int count;` in the question code; meaning: *"A later read simply overwrites the variable's current value."*

## Step 2 — Code run

```
compiles = False
  Error: cannot find symbol
    symbol:   method Println(int)
  Error: variable count might not have been initialized
run output = none (no trace: the code does not compile)
run facts given to the judge: none
```

Evidence checks (E1 names the element, E2 execution, E3 relates, E4 beyond):

| Concept | E1 | E2 | E3 | E4 | Evidence (similarity) |
|---|---|---|---|---|---|
| print | met | uncertain | not met | not met | E1 `System.out.print -- output with no newline` (0.486); E2 library-call fact (0.473) |
| standard_output | met | uncertain | not met | not met | E1 `StdOut / System.out` (0.584); E2 `A null String prints as "null"` (0.456) |
| array_creation | met | not met | not met | not met | E1 `new int[n] -- allocates n slots` (0.655) |
| statement, empty_statement, int | not met | not met | not met | not met | — |

## Step 3 — LLM judge (Claude)

Prompt: 38,101 chars (~9.5k tokens). Concepts offered: print, standard_output, declaration, statement, array_creation, empty_statement, int, variable, stream_model.

| Concept | Level | Way | Quote | Correct | Why |
|---|---|---|---|---|---|
| print | **L0** | diagnose_an_error (missed) | "It will print 0." | false | Treats `System.out.Println(count)` as a working call; Java is case-sensitive, `Println` does not exist, so the code does not compile. |
| declaration | **L0** | misconception: local variables get a default value on their own | "It will print 0." | false | Assumes `int count;` sets count to 0; a local variable left without a value is unassigned. |
| variable | **L0** | misconception: local variables get a default value on their own | "It will print 0." | false | A local variable must be assigned before it is read; reading count is a compile error, not 0. |
| standard_output | none | — | — | — | Says nothing about the output stream itself. |
| statement | none | — | — | — | Does not talk about statements or their order. |
| array_creation | none | — | — | — | No arrays in the code or the answer. |
| empty_statement | none | — | — | — | Does not mention empty statements. |
| int | none | — | — | — | No rule about the int type; the error is about initialization. |
| stream_model | none | — | — | — | Does not mention streams. |

## Step 4 — Fusion

Rules: run L0 → L0 (wrong rule) · run L2 + judge L1 → L1 · **judge L0 → L0 (wrong rule)** · weak reader (nli / relation cue / similarity) → judge's level · else keep · no level from Claude (pick mode) → not stored.

| Concept | Judge | → Level | Set by | Wrong rule | Stored |
|---|---|---|---|---|---|
| print | L0 | **L0** | judge | True | levelled (gate: ambiguity) |
| declaration | L0 | **L0** | judge | True | levelled (judge only) |
| variable | L0 | **L0** | judge | True | levelled (judge only) |
| standard_output | — | L0 | similarity | False | no: judge_no_level |
| array_creation | — | L0 | similarity | False | no: weak_link, judge_no_level |
| statement | — | L0 | none | False | no: attribution, no_evidence |
| empty_statement | — | L0 | none | False | no: attribution, no_evidence |
| int | — | L0 | none | False | no: attribution, no_evidence |

## Step 5 — Relation edges

Student edge = stated AND quote found in answer AND both ends stored.

No prerequisite/parallel edges between the shortlisted concepts.

## Final — `LP_FINAL=max_level`

```
levelled concepts: print L0 (wrong rule), declaration L0 (wrong rule), variable L0 (wrong rule)
any wrong rule = True  ->  L0
Claude's overall level: not given (edges mode), not used by max_level

FINAL LEVEL: L0
```

## Notes

- Before the gate change this answer came out **none**: G1 stopped it at 2 content items < 3, so no judge call was made.
- `declaration` and `variable` hold the real misconception (locals have no default value) but were linked only by code cues in the question code (1.353 and 1.000).
- The compile error is not passed to the judge as a run fact; the L0 comes from Claude alone.
- `array_creation` (meaning only) and `empty_statement` (`);` cue) are linking noise; Claude filtered them out.
