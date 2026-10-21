"""
Import ProgMiscon Java misconceptions into the CPAL wrong-model catalogue.

ProgMiscon (Chiodini et al., ITiCSE 2021, https://progmiscon.org) is a
peer-reviewed catalogue of programming misconceptions, each grounded in
the relevant language specification. This script merges the Java +
"public" subset (currently 55 entries) into our hand-authored catalogue,
attaching ProgMiscon's `shortCorrection` + JLS section references as
refutation_text + jls_reference on existing WrongModel entries (via the
mapping table below), and seeding 6 NEW concepts (recursion,
method_chaining, this_semantics, access_modifiers, numeric_literals,
object_instantiation) for entries that don't map to anything in our v1.

Output:
  data/mental_models/progmiscon_raw.json          (cached download)
  data/mental_models/wrong_models_catalogue_v2.json
  docs/PROGMISCON_MERGE_REPORT.md                 (per-concept merge table)

Usage:
  python scripts/import_progmiscon.py
  python scripts/import_progmiscon.py --no-fetch        # use cached raw only
  python scripts/import_progmiscon.py --include-drafts  # include status="draft"

Constraints honoured:
  - v1 catalogue (data/mental_models/wrong_models_catalogue.json) is NOT
    modified. v2 is a sibling file.
  - No function signatures change in mental_models.py. The new optional
    fields on WrongModel + ConceptEntry handle this transparently.
  - Attribution: data/mental_models/PROGMISCON_LICENSE_NOTICE.txt.

Literature grounding:
  Chiodini, L. et al. "A Curated Inventory of Programming Language
  Misconceptions." ITiCSE 2021. https://doi.org/10.1145/3430665.3456343
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests

ROOT = Path(__file__).resolve().parents[1]

PROGMISCON_URL  = "https://progmiscon.org/json/data.json"
RAW_CACHE       = ROOT / "data" / "mental_models" / "progmiscon_raw.json"
V1_CATALOGUE    = ROOT / "data" / "mental_models" / "wrong_models_catalogue.json"
V2_CATALOGUE    = ROOT / "data" / "mental_models" / "wrong_models_catalogue_v2.json"
MERGE_REPORT    = ROOT / "docs" / "PROGMISCON_MERGE_REPORT.md"
LICENSE_NOTICE  = ROOT / "data" / "mental_models" / "PROGMISCON_LICENSE_NOTICE.txt"


# Mapping table from the task spec. Maps ProgMiscon `name` -> our concept_id.
# 34 entries map to existing v1 concepts; 21 map to 6 NEW concepts.
PM_TO_EXISTING: Dict[str, str] = {
    # mapped to existing v1 concepts
    "AssignCompares":                       "assignment_vs_compare",
    "ArithmeticPlusPrecedes":               "type_mismatch",
    "StringPlusStringifiesExpression":      "type_mismatch",
    "EqualityOperatorComparesObjectsValues":"string_equality",
    "EqualsComparesReferences":             "string_equality",
    "StringLiteralNoObject":                "string_equality",
    "FinalReferenceImpliesImmutability":    "string_immutability",
    "NullIsObject":                         "null_pointer",
    "ArrayHasLengthMethod":                 "array_index",
    "ArraysGrow":                           "array_not_allocated",
    "ArrayListIsArray":                     "array_index",
    "ConstructorAllocates":                 "no_default_constructor",
    "ConstructorReturnsObject":             "no_default_constructor",
    "NoEmptyConstructor":                   "no_default_constructor",
    "MustInitializeFieldInConstructor":     "no_default_constructor",
    "ThisExistsInStaticMethod":             "static_vs_instance",
    "PrivateFromStatic":                    "static_vs_instance",
    "PrivateFromOtherInstance":             "static_vs_instance",
    "DeferredReturn":                       "missing_return",
    "ReturnUnwindsMultipleFrames":          "missing_return",
    "ReturnCall":                           "missing_return",
    "IfIsLoop":                             "boolean_operators",
    "ConditionalIsSequence":                "boolean_operators",
    "NoShortCircuit":                       "boolean_operators",
    "NoSingleLogicAnd":                     "boolean_operators",
    "ComparisonWithBooleanLiteral":         "boolean_operators",
    "MapToBooleanWithIf":                   "boolean_operators",
    "MapToBooleanWithConditionalOperator":  "boolean_operators",
    "VariablesHoldObjects":                 "null_pointer",
    "VariablesHoldExpressions":             "assignment_vs_compare",
    "AssignmentNotExpression":              "assignment_vs_compare",
    "AssignmentCopiesObject":               "null_pointer",
    "LocalVariablesAutoInitialized":        "variable_scope",
    "ReferenceToVariable":                  "variable_scope",
}

# New concepts seeded entirely from ProgMiscon. Each gets a stub L1-L4
# rubric (rubric_status="draft_needs_review") for a domain expert to refine.
PM_TO_NEW_CONCEPT: Dict[str, str] = {
    # recursion
    "RecursiveActivationsShareFrame":       "recursion",
    "RecursiveMethodImpliesRecursiveType":  "recursion",
    "RecursiveMethodNeedsIfElse":           "recursion",
    # method_chaining
    "CannotChainMemberAccesses":            "method_chaining",
    "CannotChainMemberToConstructor":       "method_chaining",
    "OutsideInMethodNesting":               "method_chaining",
    "RightToLeftChaining":                  "method_chaining",
    "ParenthesesOnlyIfArgument":            "method_chaining",
    # this_semantics
    "ThisAssignable":                       "this_semantics",
    "ThisCanBeNull":                        "this_semantics",
    "ThisNoExpression":                     "this_semantics",
    # access_modifiers
    "ControlledLocalAccess":                "access_modifiers",
    # numeric_literals
    "LargeIntegerLong":                     "numeric_literals",
    "NoFloatLiterals":                      "numeric_literals",
    "NoLongLiterals":                       "numeric_literals",
    "CharNotNumeric":                       "numeric_literals",
    # object_instantiation
    "ObjectsMustBeNamed":                   "object_instantiation",
    "AddMemberAtRuntime":                   "object_instantiation",
    "CallNotStaticallyChecked":             "object_instantiation",
    "NoReservedWords":                      "object_instantiation",
    "NoAtomicExpression":                   "object_instantiation",
}

# Per-new-concept metadata + draft L1-L4 rubric. Marked
# rubric_status="draft_needs_review" so a domain expert can refine before
# the LP head retraining cycle picks these up.
NEW_CONCEPTS_META: Dict[str, Dict] = {
    "recursion": {
        "week": 10, "error_class": "runtime_error",
        "java_concept": "Recursion. Method calls itself; each call has its "
                        "own activation record (stack frame). Base case must "
                        "exist or stack overflows.",
        "lp_rubric": {
            "L1": "Recognises that a method calling itself is 'recursion' "
                  "but can't predict what happens at runtime.",
            "L2": "Names the rule that every recursive method needs a base "
                  "case or it will infinitely recurse.",
            "L3": "Traces a small recursive call by hand, showing each "
                  "activation has its own local variables / parameters on "
                  "the call stack, and that returns unwind one frame at a time.",
            "L4": "Generalises to mutual recursion, tail-call optimisation "
                  "(JVM doesn't do it), and the relationship between "
                  "recursion depth and StackOverflowError.",
        },
    },
    "method_chaining": {
        "week": 5, "error_class": "compile_error",
        "java_concept": "Method chaining (a.foo().bar()). Each call evaluates "
                        "left-to-right; the return value of foo() becomes "
                        "the receiver of bar(). The chain works only if "
                        "each return type supports the next call.",
        "lp_rubric": {
            "L1": "Recognises a.foo().bar() syntactically as 'a dot foo dot bar'.",
            "L2": "Names that chained calls happen left-to-right and that "
                  "the return type of foo() determines what bar() can be.",
            "L3": "Traces a chain step-by-step, showing the intermediate "
                  "receiver objects/values and what would happen if any "
                  "step returns null or the wrong type.",
            "L4": "Generalises to fluent interfaces, builder pattern, and "
                  "when chaining hurts readability vs helps it.",
        },
    },
    "this_semantics": {
        "week": 7, "error_class": "compile_error",
        "java_concept": "`this` is an implicit reference to the current "
                        "object inside an instance method/constructor. It "
                        "is final, not assignable, never null at the point "
                        "of access in an instance context, and not defined "
                        "in static contexts.",
        "lp_rubric": {
            "L1": "Recognises `this` as 'the current object' but uses it "
                  "interchangeably with the variable name.",
            "L2": "Names the rule that `this` is implicit and refers to "
                  "the object the method was called on.",
            "L3": "Explains why `this = something` is a compile error "
                  "(implicit final), why `this` is unavailable in static "
                  "methods (no instance), and how `this.field` disambiguates "
                  "field from local.",
            "L4": "Generalises to qualified `this` in inner classes "
                  "(Outer.this), `this(...)` constructor delegation, and "
                  "the JLS guarantee that `this` is non-null in normal "
                  "instance contexts.",
        },
    },
    "access_modifiers": {
        "week": 7, "error_class": "compile_error",
        "java_concept": "Access modifiers (public/protected/package-private/"
                        "private) control where a member is accessible from. "
                        "Locally-scoped variables don't take modifiers.",
        "lp_rubric": {
            "L1": "Knows the words public/private but treats them as labels.",
            "L2": "Names the four levels and which is the default; knows "
                  "private can't be reached from outside the class.",
            "L3": "Explains the package vs subclass distinction for protected, "
                  "and why local variables can't be modified with "
                  "public/private (scope is already the smallest possible).",
            "L4": "Generalises to module system (Java 9+), reflection-based "
                  "access, and the difference between compile-time and "
                  "runtime access checks.",
        },
    },
    "numeric_literals": {
        "week": 1, "error_class": "compile_error",
        "java_concept": "Java numeric literals have implicit types: integer "
                        "literals default to int (need L suffix for long); "
                        "decimal literals default to double (need f for "
                        "float); char literals are integral, not strings.",
        "lp_rubric": {
            "L1": "Writes numbers without thinking about type; surprised "
                  "when 3000000000 doesn't compile.",
            "L2": "Names the rule that int literals max out at ~2.1 billion "
                  "and that L makes it long; that 3.14 is double; that "
                  "3.14f is float; that 'A' is a char (integer 65), not a "
                  "String.",
            "L3": "Explains the implicit widening conversions and why "
                  "(double)5/2 differs from 5/2; the exact-vs-approximation "
                  "distinction between long and double.",
            "L4": "Generalises to underscores in literals (Java 7+), "
                  "binary/hex/oct prefixes, and the IEEE 754 reasons for "
                  "double vs float precision differences.",
        },
    },
    "object_instantiation": {
        "week": 6, "error_class": "compile_error",
        "java_concept": "Object instantiation: `new Foo(args)` allocates an "
                        "object on the heap and runs Foo's constructor. "
                        "Result is a reference; usually assigned to a "
                        "variable but can be used as an expression. Java's "
                        "object set is class-defined at compile time, not "
                        "expandable at runtime.",
        "lp_rubric": {
            "L1": "Knows `new Foo()` makes a Foo but can't say what the "
                  "expression evaluates to or where the object lives.",
            "L2": "Names that `new` returns a reference, that the "
                  "constructor runs once, and that you usually store the "
                  "reference in a variable.",
            "L3": "Explains heap allocation, that `new Foo()` is an "
                  "expression (can be used inline as an argument), why "
                  "you can't add new fields at runtime, and why method "
                  "calls are statically checked.",
            "L4": "Generalises to anonymous inner classes, lambda vs "
                  "object instantiation, escape analysis (JVM optimisation), "
                  "and why dynamic-language idioms (monkey patching, "
                  "duck typing) don't translate.",
        },
    },
}


def fetch_progmiscon(force: bool = False) -> Dict:
    """Fetch the live JSON (or use cached). Returns the full data dict."""
    if RAW_CACHE.exists() and not force:
        print(f"[import] using cached raw at {RAW_CACHE}")
        with open(RAW_CACHE, encoding="utf-8") as f:
            return json.load(f)
    print(f"[import] fetching {PROGMISCON_URL} ...")
    r = requests.get(PROGMISCON_URL, timeout=30)
    r.raise_for_status()
    data = r.json()
    RAW_CACHE.parent.mkdir(parents=True, exist_ok=True)
    RAW_CACHE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"[import] cached {len(data.get('misconceptions', []))} "
          f"misconceptions to {RAW_CACHE}")
    return data


def format_jls(spec: List[Dict]) -> Optional[str]:
    """Render the spec block as 'JLS21 §15.21.1, §8.4.3.1' or None."""
    if not spec:
        return None
    parts = []
    for s in spec:
        spec_id = s.get("id", "").strip()
        sections = s.get("sections") or []
        spec_label = "JLS"
        if spec_id.lower().startswith("jls"):
            ver = spec_id[3:].strip()
            spec_label = f"JLS{ver}" if ver else "JLS"
        if sections:
            sec_part = ", ".join(f"§{s}" for s in sections)
            parts.append(f"{spec_label} {sec_part}")
        elif spec_id:
            parts.append(spec_label)
    return "; ".join(parts) if parts else None


def build_pm_wrong_model(pm_entry: Dict) -> Dict:
    """Build a v2-catalogue WrongModel dict from a ProgMiscon entry.

    For ProgMiscon-only imports (no hand-authored conversation_signals
    yet), we leave conversation_signals=[] so match_wrong_model() never
    fires on them, but the metadata is preserved for LP-2c surfacing.
    """
    pm_name = pm_entry["name"]
    return {
        "id": f"PM-{pm_name}",
        "wrong_belief": pm_entry.get("shortDescription", ""),
        "origin": ("Documented in ProgMiscon (Chiodini et al., ITiCSE 2021); "
                   "concepts: " + ", ".join(pm_entry.get("concepts", []))),
        "conversation_signals": [],
        "progmiscon_id": pm_name,
        "jls_reference": format_jls(pm_entry.get("spec", [])),
        "refutation_text": pm_entry.get("shortCorrection", ""),
        "textbook_refs": [],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-fetch", action="store_true",
                    help="Use cached raw only; don't hit progmiscon.org")
    ap.add_argument("--include-drafts", action="store_true",
                    help="Also import status='draft' entries (default: public only)")
    args = ap.parse_args()

    # 1. Fetch (or cached) — never re-download if --no-fetch
    if args.no_fetch and not RAW_CACHE.exists():
        print(f"[import] FATAL: --no-fetch but cache {RAW_CACHE} doesn't exist",
              file=sys.stderr)
        sys.exit(2)
    raw = fetch_progmiscon(force=False if args.no_fetch else False)

    # 2. Filter Java + status filter
    all_ms = raw.get("misconceptions", [])
    java_ms = [m for m in all_ms if m.get("pl") == "Java"]
    if args.include_drafts:
        filtered = java_ms
    else:
        filtered = [m for m in java_ms if m.get("status") == "public"]
    print(f"[import] {len(all_ms)} total → {len(java_ms)} Java → "
          f"{len(filtered)} after status filter "
          f"({'public+draft' if args.include_drafts else 'public only'})")

    by_name = {m["name"]: m for m in filtered}

    # 3. Load v1, deep-copy, attach ProgMiscon grounding
    with open(V1_CATALOGUE, encoding="utf-8") as f:
        v2 = json.load(f)

    # 3a. Mapping → enrich existing WrongModels.
    # Strategy: for each (pm_name -> concept_id) row, attach the ProgMiscon
    # fields to the FIRST WrongModel in that concept that doesn't already
    # have a progmiscon_id. If none exist, push it as a progmiscon_only
    # entry so the metadata isn't lost.
    enriched_existing: List[Tuple[str, str, str]] = []   # (pm_name, concept_id, wm_id)
    pushed_to_only:    List[Tuple[str, str]]      = []   # (pm_name, concept_id)
    unmapped:          List[str]                  = []   # pm_names not in either table

    for pm_name, pm_entry in by_name.items():
        concept_id = PM_TO_EXISTING.get(pm_name)
        if concept_id is None:
            if pm_name in PM_TO_NEW_CONCEPT:
                continue  # handled below
            unmapped.append(pm_name)
            continue

        concept = v2["concepts"].get(concept_id)
        if concept is None:
            print(f"[import] WARN: mapped concept {concept_id!r} not in v1")
            continue

        # Find first WrongModel without a progmiscon_id; enrich.
        target_wm = None
        for wm in concept.get("wrong_models", []):
            if not wm.get("progmiscon_id"):
                target_wm = wm; break

        if target_wm is not None:
            target_wm["progmiscon_id"]   = pm_name
            target_wm["jls_reference"]   = format_jls(pm_entry.get("spec", []))
            target_wm["refutation_text"] = pm_entry.get("shortCorrection", "")
            target_wm.setdefault("textbook_refs", [])
            enriched_existing.append((pm_name, concept_id, target_wm["id"]))
        else:
            # All wrong_models already grounded — push to progmiscon_only
            concept.setdefault("progmiscon_only", []).append(
                build_pm_wrong_model(pm_entry)
            )
            pushed_to_only.append((pm_name, concept_id))

    # 3b. New concepts from PM_TO_NEW_CONCEPT
    new_concept_entries: Dict[str, List[str]] = defaultdict(list)
    for pm_name, concept_id in PM_TO_NEW_CONCEPT.items():
        if pm_name not in by_name:
            continue   # skip if not in current ProgMiscon snapshot
        new_concept_entries[concept_id].append(pm_name)

    new_concepts_created: List[str] = []
    for concept_id, pm_names in new_concept_entries.items():
        meta = NEW_CONCEPTS_META.get(concept_id, {})
        wrong_models = []
        for pm_name in pm_names:
            wm = build_pm_wrong_model(by_name[pm_name])
            # For new concepts, ProgMiscon entries ARE the primary wrong
            # models (not progmiscon_only).
            wrong_models.append(wm)
        v2["concepts"][concept_id] = {
            "week":         meta.get("week", 0),
            "error_class":  meta.get("error_class", ""),
            "java_concept": meta.get("java_concept", ""),
            "wrong_models": wrong_models,
            "lp_rubric":    meta.get("lp_rubric", {}),
            "rubric_status":"draft_needs_review",
        }
        new_concepts_created.append(concept_id)

    # 4. Bump version + write v2
    v2["version"]       = "2.0"
    v2["source"]        = ("CPAL hand-authored catalogue (v1) + ProgMiscon "
                           "Java public subset (https://progmiscon.org, "
                           "CC BY 4.0, Chiodini et al. ITiCSE 2021)")
    v2["description"]   = v2.get("description", "") + (
        "\n\nVersion 2 (2026-05-25): integrated "
        f"{len(enriched_existing)} ProgMiscon refutations into existing "
        f"wrong models, seeded {len(new_concepts_created)} new concepts."
    )
    V2_CATALOGUE.write_text(
        json.dumps(v2, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[import] wrote {V2_CATALOGUE} "
          f"({len(v2['concepts'])} concepts; "
          f"{sum(len(c.get('wrong_models', [])) for c in v2['concepts'].values())} "
          f"wrong models)")

    # Also mirror to the git-tracked canonical location (cpal_integration/
    # data/ — the data/ tree itself is gitignored). v2 catalogue + raw +
    # license sit alongside the v1 catalogue so the canonical source of
    # truth in git matches the runtime files.
    tracked_dir = ROOT / "cpal_integration" / "data"
    if tracked_dir.exists():
        for src in (V2_CATALOGUE, RAW_CACHE, LICENSE_NOTICE):
            if src.exists():
                dst = tracked_dir / src.name
                dst.write_bytes(src.read_bytes())
        print(f"[import] mirrored v2 + raw + license to {tracked_dir}/")

    # 5. Write merge report
    MERGE_REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# ProgMiscon → CPAL catalogue merge report",
        "",
        f"- ProgMiscon snapshot: {raw.get('meta', {}).get('publicationDate', '?')}",
        f"- Java entries considered: {len(filtered)} "
        f"({'public+draft' if args.include_drafts else 'public only'})",
        f"- Enriched existing wrong models: **{len(enriched_existing)}**",
        f"- Pushed to progmiscon_only (no room in main): "
        f"**{len(pushed_to_only)}**",
        f"- New concepts created: **{len(new_concepts_created)}** "
        f"({', '.join(new_concepts_created)})",
        f"- Unmapped ProgMiscon entries (consider adding mappings): "
        f"**{len(unmapped)}**",
        "",
        "## Per-concept enrichment table",
        "",
        "| ProgMiscon ID | → concept | wm slot | refutation snippet |",
        "|---|---|---|---|",
    ]
    for pm_name, concept_id, wm_id in enriched_existing:
        snippet = (by_name[pm_name].get("shortCorrection") or "")[:80].replace("|", "\\|")
        lines.append(f"| `{pm_name}` | `{concept_id}` | `{wm_id}` | {snippet} |")

    if pushed_to_only:
        lines += [
            "", "## Pushed to `progmiscon_only` (concept's main slots full)",
            "",
            "| ProgMiscon ID | → concept |",
            "|---|---|",
        ]
        for pm_name, concept_id in pushed_to_only:
            lines.append(f"| `{pm_name}` | `{concept_id}` |")

    if new_concepts_created:
        lines += [
            "", "## New concepts seeded (rubric_status=draft_needs_review)",
            "",
        ]
        for c in new_concepts_created:
            lines.append(f"### `{c}` ({len(new_concept_entries[c])} PM entries)")
            for pm_name in new_concept_entries[c]:
                pm = by_name[pm_name]
                lines.append(f"- `{pm_name}`: {pm.get('shortDescription', '')[:100]}")
            lines.append("")
            rubric = NEW_CONCEPTS_META.get(c, {}).get("lp_rubric", {})
            for L in ("L1", "L2", "L3", "L4"):
                if L in rubric:
                    lines.append(f"  - **{L}**: {rubric[L]}")
            lines.append("")

    if unmapped:
        lines += [
            "## Unmapped ProgMiscon entries",
            "",
            "These are in the live Java public subset but don't appear in "
            "either PM_TO_EXISTING or PM_TO_NEW_CONCEPT. Decide whether to "
            "add to an existing concept, seed a new one, or skip.",
            "",
        ]
        for pm_name in unmapped:
            pm = by_name[pm_name]
            lines.append(f"- `{pm_name}` "
                         f"(concepts: {', '.join(pm.get('concepts', []))}): "
                         f"{pm.get('shortDescription', '')[:100]}")

    MERGE_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[import] wrote merge report {MERGE_REPORT}")

    # 6. License notice (idempotent)
    if not LICENSE_NOTICE.exists():
        LICENSE_NOTICE.write_text(
            "ProgMiscon misconception catalogue\n"
            "==================================\n\n"
            "Source: https://progmiscon.org\n"
            "Reference: Chiodini, L. et al. (2021). 'A Curated Inventory of "
            "Programming Language Misconceptions.' Proceedings of the 26th "
            "ACM Conference on Innovation and Technology in Computer Science "
            "Education (ITiCSE '21). https://doi.org/10.1145/3430665.3456343\n\n"
            "Licence: Creative Commons Attribution 4.0 International "
            "(CC BY 4.0). https://creativecommons.org/licenses/by/4.0/\n\n"
            "This project uses the Java subset of ProgMiscon's misconception "
            "catalogue (specifically the `shortCorrection` refutation text "
            "and the JLS section references) to enrich the CPAL "
            "wrong-mental-models catalogue. Cached snapshot: "
            "data/mental_models/progmiscon_raw.json.\n\n"
            "Attribution: When CPAL surfaces a ProgMiscon refutation in a "
            "tutor response (LP-2.5 prompt block), the ProgMiscon "
            "misconception ID is included so the source is traceable.\n",
            encoding="utf-8",
        )
        print(f"[import] wrote {LICENSE_NOTICE}")

    # 7. Summary
    print()
    print(f"=== summary ===")
    print(f"  Enriched existing wrong models : {len(enriched_existing)}")
    print(f"  Pushed to progmiscon_only      : {len(pushed_to_only)}")
    print(f"  New concepts seeded            : {len(new_concepts_created)} "
          f"({', '.join(new_concepts_created)})")
    print(f"  Unmapped entries               : {len(unmapped)}")
    print()
    print(f"  v2 catalogue: {V2_CATALOGUE}")
    print(f"  merge report: {MERGE_REPORT}")


if __name__ == "__main__":
    main()
