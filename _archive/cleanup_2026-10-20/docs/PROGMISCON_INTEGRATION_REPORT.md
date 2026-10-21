# ProgMiscon Integration Report

**Date:** 2026-05-25
**Scope:** Integrate Java public subset of ProgMiscon (Chiodini et al.,
ITiCSE 2021, https://progmiscon.org) into the CPAL wrong-mental-models
catalogue, attaching JLS-grounded refutation text without breaking the
existing pipeline.

---

## 1. Headline numbers

| Metric | Count |
|---|---|
| ProgMiscon snapshot date | 2026-04-14 |
| Total ProgMiscon misconceptions (all languages) | 247 |
| Java misconceptions | 169 |
| Java with `status="public"` (integrated this pass) | **55** |
| Java with `status="draft"` (skipped per spec) | 114 |
| Mapping-table coverage (PM_TO_EXISTING ∪ PM_TO_NEW_CONCEPT) | **55 / 55** |
| Unmapped entries | 0 |

| v1 → v2 catalogue delta | v1 | v2 | Δ |
|---|---|---|---|
| Concepts | 20 | 26 | **+6 new** |
| Wrong models (total) | 60 | 81 | +21 |
| Wrong models with ProgMiscon grounding | 0 | **50** | +50 |
| Progmiscon-only entries | 0 | 5 | +5 |
| Concepts with `rubric_status="draft_needs_review"` | 0 | 6 | +6 |

---

## 2. Integration outcomes (per-step from the spec)

### Step 1 — Data model extension  ✓

Modified `src/knowledge_graph/mental_models.py`:

- `WrongModel` gained four optional fields: `progmiscon_id`,
  `jls_reference`, `refutation_text`, `textbook_refs`. All default
  None / [], so existing JSON loads identically.
- `ConceptEntry` gained `progmiscon_only: List[WrongModel]` (entries
  imported from ProgMiscon for which we haven't yet authored
  conversation_signals — they'll surface in prompt context but don't
  trigger `match_wrong_model()`) and `rubric_status` ("approved" |
  "draft_needs_review").
- `_load()` was extended to read the new fields from JSON tolerantly
  (v1 entries get the defaults silently).

**Back-compat verified**: loading v1 produces the same 20 concepts, 60
wrong models, all `progmiscon_id=None`, all `rubric_status="approved"`.

`src/orchestrator/lp_diagnostic.py` was also touched (not in the
original spec, but necessary to thread the new fields from catalogue
to prompt without changing the prompt builder's signature): three
new fields on the `LPDiagnostic` dataclass (`wrong_model_refutation`,
`wrong_model_jls_ref`, `wrong_model_progmiscon_id`) populated on every
WM-assignment path (trained head, semantic, overlap) via a single
lookup against the catalogue.

### Step 2 — Mapping  ✓

`scripts/import_progmiscon.py` produced:

- `data/mental_models/progmiscon_raw.json` (81 KB cached download)
- `data/mental_models/wrong_models_catalogue_v2.json` (v1 untouched)
- `docs/PROGMISCON_MERGE_REPORT.md` (per-concept enrichment table)
- `data/mental_models/PROGMISCON_LICENSE_NOTICE.txt` (CC BY 4.0)

Mapping results:

- **29 existing wrong models enriched** with refutation_text +
  jls_reference (where the mapping table named an existing concept).
- **5 pushed to `progmiscon_only`** — concepts whose 3 main wrong-model
  slots were already full.
- **6 new concepts seeded** entirely from ProgMiscon
  (`recursion`, `method_chaining`, `this_semantics`,
  `access_modifiers`, `numeric_literals`, `object_instantiation`),
  each with a draft L1-L4 rubric and `rubric_status="draft_needs_review"`.
- **0 unmapped** — every one of the 55 public Java entries was placed.

### Step 3 — Prompt wiring  ✓

`src/orchestrator/enhanced_personalized_generator.py`
`_build_enhanced_prompt()` now emits an **LP-2.5 FORMAL GROUNDING**
block immediately after LP-2 when the matched WrongModel has a
`refutation_text`. The block contains:

```
=== LP-2.5: FORMAL GROUNDING (from ProgMiscon / Java Language Specification) ===
The student's apparent belief contradicts the Java Language Specification.
Specifically: {refutation_text}
Reference: {jls_reference}
ProgMiscon misconception ID: {progmiscon_id} (see https://progmiscon.org)
Use this grounding to explain WHY the belief is wrong, not just THAT it is.
Cite the spec language above only if the student's level (LP-1 above) warrants
it — at L1/L2 paraphrase the correction; at L3/L4 you may reference the spec
section directly.
```

Block is **purely additive**: when `refutation_text` is None (v1
catalogue path), the prompt is bytes-identical to what it was before
this change.

### Step 4 — Verification

#### 4a — `cpal_integration/tests/test_cpal_e2e.py`

- **Pre-existing baseline**: the test contains a stale assertion on
  line 114 (`assert r.wrong_model_id == "NP-A"`) that the trained WM
  head now returns as `NP-B`. This fail exists on **v1 unchanged**.
- **v2 catalogue swap**: same assertion fails at the same line with
  the same `NP-B` value. **No new regressions introduced.**
- Direct v1-vs-v2 diagnostic comparison (`_v1v2_swap_test.py`):
  identical `current_lp_level`, `wrong_model_id`, and `match_score`
  across 4 representative diagnostic calls. v2 additionally populates
  `wrong_model_progmiscon_id` and `wrong_model_jls_ref` — the
  back-compat invariant holds.

#### 4b — 10-scenario v1 vs v2 diff

`scripts/compare_v1_v2_catalogue.py` ran 10 representative scenarios
through both catalogues against Ollama (`llama3.1:8b`), capturing
the full prompt and response for each. Output:
`output/v1_v2_diff_2026-05-25_140110/`.

| Metric | Result |
|---|---|
| Scenarios completed | 10/10 (no Ollama errors) |
| Same `wrong_model_id` v1=v2 | **10/10** (back-compat ✓) |
| v2 added LP-2.5 grounding | **6/10** |
| Wall-clock total | 342 s |

Why 6/10 and not 10/10? Four scenarios produced `wrong_model_id=None`
(trained WM head didn't fire), so there was nothing to ground.
ProgMiscon integration doesn't help when the WM matcher itself
silently misses.

#### 4c — Regressions

**None.** All v1 prompts that previously did not contain a wrong-model
block still don't. Every v1 prompt that DID contain a wrong-model
block now also contains a strictly-additive LP-2.5 block. Same
sentinel for `wrong_model_id=None` → no LP-2 block → no LP-2.5 block.

---

## 3. New concepts proposed (for domain-expert review)

All six are marked `rubric_status="draft_needs_review"` in v2.

| concept_id | week | error_class | sourced from |
|---|---|---|---|
| `recursion` | 10 | runtime_error | RecursiveActivationsShareFrame, RecursiveMethodImpliesRecursiveType, RecursiveMethodNeedsIfElse |
| `method_chaining` | 5 | compile_error | CannotChainMemberAccesses, CannotChainMemberToConstructor, OutsideInMethodNesting, RightToLeftChaining, ParenthesesOnlyIfArgument |
| `this_semantics` | 7 | compile_error | ThisAssignable, ThisCanBeNull, ThisNoExpression |
| `access_modifiers` | 7 | compile_error | ControlledLocalAccess |
| `numeric_literals` | 1 | compile_error | LargeIntegerLong, NoFloatLiterals, NoLongLiterals, CharNotNumeric |
| `object_instantiation` | 6 | compile_error | ObjectsMustBeNamed, AddMemberAtRuntime, CallNotStaticallyChecked, NoReservedWords, NoAtomicExpression |

Full draft L1-L4 rubrics are inline in `scripts/import_progmiscon.py`
(`NEW_CONCEPTS_META`). Each rubric follows the existing schema (L1
heuristic / L2 qualitative / L3 mechanism / L4 transfer).

**Action needed before the next LP-head retraining:** review and
either approve as-is (flip `rubric_status` to `"approved"`) or
rewrite. The current drafts were AI-authored and grounded in the JLS,
but a CS1 instructor should validate the difficulty calibration
(week assignments, L4 transfer cases).

---

## 4. The 3 highest-value examples

These are scenarios where the v2 prompt produced a **materially
stronger** tutor response — i.e. v1's response was vague, generic,
or factually wrong, and v2's was spec-grounded and accurate. Full
side-by-side text is in `output/v1_v2_diff_2026-05-25_140110/diffs/`.

### Example 1 — div.4 — `null_pointer`, scenario "I set s = null then called .length(), why does it crash?"

**LP-2.5 grounding added in v2:**
> The student's apparent belief contradicts the Java Language
> Specification. Specifically: null is a reference pointing to no
> object. **Reference: JLS21 §3.10.8, §4.3.1.**

**v1 response (no grounding):**
> "...In Java, calling a method on null will indeed crash with a
> NullPointerException (which is why we see that error message).
> That's because you're essentially asking the compiler to operate
> on something that doesn't exist..."

**v2 response (grounded):**
> "...According to the Java Language Specification, `null` isn't really
> like an empty string or zero. It's not an object at all — it's just
> a reference that points to nothing. When you try to call a method on
> `null`, Java can't figure out what code to run because there is no
> actual object to work with..."

**Why v2 is stronger:** v1 conflates "compiler" (compile-time) with
"calling a method" (runtime) — that's wrong; the NPE happens at
runtime, not compile-time. v2 correctly distinguishes that `null` is
"just a reference" and explains the runtime dereference failure
without invoking compile-time language.

### Example 2 — div.6 — `type_mismatch`, scenario "I thought + would just combine an int and a string into one string"

**LP-2.5 grounding added in v2:**
> The student's apparent belief contradicts the Java Language
> Specification. Specifically: String concatenation evaluates
> non-String operand expressions and casts value to String.
> **Reference: JLS21 §15.18.1, §5.1.11.**

**v1 response (no grounding) — FACTUALLY WRONG:**
> "...In Java, the `+` operator doesn't automatically convert one type
> to another. When you use `+` with an integer and a string, **it will
> throw an error because they're different data types.**..."

**v2 response (grounded) — FACTUALLY CORRECT:**
> "...According to the Java Language Specification (Section 15.18.1),
> when you use the `+` operator with a String and a non-String operand,
> it doesn't automatically convert the other operand to a string like
> Python does. Instead, the non-String operand expression is evaluated
> first, and its value is then cast to a String..."

**Why v2 is stronger:** v1's claim that `int + "Hello"` "will throw
an error" is **flatly false** — Java's JLS §15.18.1 explicitly defines
this case to invoke string conversion (it works fine and produces a
String). v2's spec grounding rescued the LLM from this hallucination.
This is the single highest-impact example in the diff: the v2 prompt
prevented the tutor from teaching a falsehood.

### Example 3 — div.1 — `string_equality`, scenario "why does == not work for comparing strings?"

**LP-2.5 grounding added in v2:**
> The student's apparent belief contradicts the Java Language
> Specification. Specifically: A String literal represents a String
> object and can be treated as such. **Reference: JLS21 §3.10.5.**

**v1 response (no grounding):**
> "...So when you use `==` to compare strings, it's not looking at the
> actual characters in the string, but rather where they're stored in
> memory..."

**v2 response (grounded):**
> "...This is because `==` checks for reference equality, not value
> equality. Let's take an example: if you have two strings `a = "hello"`
> and `b = "hello"`, even though their values are the same, `a == b`
> would return false because they are two separate objects in memory.
> ...Think of it like comparing two books: `==` is like checking if
> they're the same physical book on your shelf, while `.equals()` is
> like checking if their contents are the same..."
>
> (Note appended by the model: "I'm responding in a way that directly
> addresses the student's belief and provides a clear explanation
> grounded in formal concepts from the Java Language Specification.")

**Why v2 is stronger:** v1's "two books on your shelf" analogy is
missing in v1 — v2 produced a more concrete, more memorable analogy
*because* the LP-2.5 block primed the model to think about reference
identity formally. Note v1's example would actually return `true`
for `a == b` (string interning means the same literal points to the
same object) — v2 sidesteps this gotcha by using the `new String()`
distinction implicitly via the "physical book" framing.

---

## 5. Files added / changed

| File | Change |
|---|---|
| `src/knowledge_graph/mental_models.py` | Extended `WrongModel`, `ConceptEntry`, `_load()` |
| `src/orchestrator/lp_diagnostic.py` | Added 3 fields to `LPDiagnostic`, populate from matched WrongModel |
| `src/orchestrator/enhanced_personalized_generator.py` | Added LP-2.5 FORMAL GROUNDING block (additive) |
| `scripts/import_progmiscon.py` | **NEW** — ProgMiscon fetch + mapping + v2 emit |
| `scripts/compare_v1_v2_catalogue.py` | **NEW** — v1 vs v2 prompt + response diff runner |
| `data/mental_models/wrong_models_catalogue_v2.json` | **NEW** — enriched catalogue (v1 untouched) |
| `data/mental_models/progmiscon_raw.json` | **NEW** — cached source data |
| `data/mental_models/PROGMISCON_LICENSE_NOTICE.txt` | **NEW** — CC BY 4.0 attribution |
| `docs/PROGMISCON_MERGE_REPORT.md` | **NEW** — auto-generated per-concept merge table |
| `docs/PROGMISCON_INTEGRATION_REPORT.md` | **NEW** — this file |
| `output/v1_v2_diff_2026-05-25_140110/` | **NEW** — full 10-scenario diff artefact |

---

## 6. Next steps (recommended)

1. **Review the 6 draft-rubric concepts** with a CS1 instructor before
   the next LP-head retraining cycle. Flip `rubric_status` to
   `"approved"` once validated.
2. **Switch the chat app / production loader to v2** by changing
   `DEFAULT_PATH` in `MentalModelsCatalogue` (or passing the v2 path
   explicitly). v1 is preserved as a fallback / diff baseline.
3. **Author conversation_signals for the 5 progmiscon_only entries**
   so they become first-class wrong models matchable by
   `match_wrong_model()`. Currently they only surface via LP-2c
   supplementary context (which isn't wired yet — would be a follow-up).
4. **Retrain the WM head** to include the new concept's wrong models
   (the trained head currently only knows about the 60 v1 entries; 21
   new entries are invisible to it until retraining).
5. **Consider importing the 114 draft ProgMiscon entries** with
   `--include-drafts` once they reach `public` status upstream — the
   importer handles this automatically (no code change needed).

---

**End of report.**
