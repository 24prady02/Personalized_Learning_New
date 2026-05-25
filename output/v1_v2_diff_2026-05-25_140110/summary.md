# v1 vs v2 catalogue diff summary

- Timestamp: 2026-05-25_140110
- Model: llama3.1:8b
- Scenarios: 10
- Same wrong_model_id (v1=v2): **10/10** (back-compat invariant)
- v2 added LP-2.5 grounding: **6/10**
- Wall-clock total: 342.1s

## Per-scenario

| # | id | concept | v1_wm | v2_wm | same? | v2 added grounding | PM id | v1 chars | v2 chars |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `div.1` | string_equality | `SE-C` | `SE-C` | ✓ | YES | `StringLiteralNoObject` | 599 | 958 |
| 2 | `div.2` | string_equality | `SE-A` | `SE-A` | ✓ | YES | `EqualityOperatorComparesObjectsValues` | 670 | 675 |
| 3 | `div.3` | null_pointer | `NP-A` | `NP-A` | ✓ | YES | `AssignmentCopiesObject` | 805 | 535 |
| 4 | `div.4` | null_pointer | `NP-B` | `NP-B` | ✓ | YES | `NullIsObject` | 687 | 913 |
| 5 | `div.5` | assignment_vs_compare | `None` | `None` | ✓ | no | `-` | 494 | 398 |
| 6 | `div.6` | type_mismatch | `TM-B` | `TM-B` | ✓ | YES | `StringPlusStringifiesExpression` | 629 | 890 |
| 7 | `div.7` | string_immutability | `None` | `None` | ✓ | no | `-` | 844 | 418 |
| 8 | `div.8` | array_index | `AI-A` | `AI-A` | ✓ | YES | `ArrayHasLengthMethod` | 659 | 443 |
| 9 | `div.9` | no_default_constructor | `None` | `None` | ✓ | no | `-` | 599 | 559 |
| 10 | `div.10` | static_vs_instance | `None` | `None` | ✓ | no | `-` | 566 | 1063 |