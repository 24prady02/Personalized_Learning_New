# Full-stack batch run summary

Ran 10 scenarios at 2026-05-09_231427.

## Wrong-belief identification (classifier vs RAG hybrid)

| # | id | expected | classifier | hybrid (RAG) | flipped | cls✓ | rag✓ |
|---|---|---|---|---|---|---|---|
| 1 | `01_null_pointer_NP-A` | **NP-A** | NP-C | NP-B | ⟲ | ✗ | ✗ |
| 2 | `02_type_mismatch_TM-B` | **TM-B** | TM-B | TM-B |  | ✓ | ✓ |
| 3 | `03_infinite_loop_IL-B` | **IL-B** | IL-B | IL-B |  | ✓ | ✓ |
| 4 | `04_integer_division_ID-A` | **ID-A** | ID-A | ID-A |  | ✓ | ✓ |
| 5 | `05_array_index_AI-A` | **AI-A** | AI-C | AI-B | ⟲ | ✗ | ✗ |
| 6 | `06_string_equality_SE-A` | **SE-A** | SE-C | SE-C |  | ✗ | ✗ |
| 7 | `07_variable_scope_VS-A` | **VS-A** | VS-A | VS-A |  | ✓ | ✓ |
| 8 | `08_assignment_vs_compare_AC-A` | **AC-A** | AC-A | AC-C | ⟲ | ✓ | ✗ |
| 9 | `09_scanner_buffer_SB-A` | **SB-A** | SB-B | SB-A | ⟲ | ✗ | ✓ |
| 10 | `10_null_pointer_NP-B` | **NP-B** | NP-B | NP-B |  | ✓ | ✓ |

## Learning-progression transitions

| id | concept | LP current | LP target | transition |
|---|---|---|---|---|
| `01_null_pointer_NP-A` | null_pointer | L1 | L2 | L1->L2 |
| `02_type_mismatch_TM-B` | type_mismatch | L2 | L3 | L2->L3 |
| `03_infinite_loop_IL-B` | infinite_loop | L3 | L4 | L3->L4 |
| `04_integer_division_ID-A` | integer_division | L1 | L2 | L1->L2 |
| `05_array_index_AI-A` | array_index | L3 | L4 | L3->L4 |
| `06_string_equality_SE-A` | string_equality | L4 | L4 | L4->L4 |
| `07_variable_scope_VS-A` | variable_scope | L2 | L3 | L2->L3 |
| `08_assignment_vs_compare_AC-A` | assignment_vs_compare | L3 | L4 | L3->L4 |
| `09_scanner_buffer_SB-A` | scanner_buffer | L3 | L4 | L3->L4 |
| `10_null_pointer_NP-B` | null_pointer | L4 | L4 | L4->L4 |

## Mastery updates (BKT + DINA, after failure)

| id | concept | BKT before | BKT after | DINA before | DINA after |
|---|---|---|---|---|---|
| `01_null_pointer_NP-A` | null_pointer | 0.25 | 0.23 | 0.15 | 0.00 |
| `02_type_mismatch_TM-B` | type_mismatch | 0.20 | 0.23 | 0.20 | 0.00 |
| `03_infinite_loop_IL-B` | infinite_loop | 0.15 | 0.22 | 0.17 | 0.00 |
| `04_integer_division_ID-A` | integer_division | 0.20 | 0.23 | 0.20 | 0.00 |
| `05_array_index_AI-A` | array_index | 0.30 | 0.24 | 0.17 | 0.00 |
| `06_string_equality_SE-A` | string_equality | 0.20 | 0.23 | 0.15 | 0.00 |
| `07_variable_scope_VS-A` | variable_scope | 0.20 | 0.23 | 0.20 | 0.00 |
| `08_assignment_vs_compare_AC-A` | assignment_vs_compare | 0.15 | 0.22 | 0.22 | 0.00 |
| `09_scanner_buffer_SB-A` | scanner_buffer | 0.20 | 0.23 | 0.15 | 0.00 |
| `10_null_pointer_NP-B` | null_pointer | 0.30 | 0.24 | 0.15 | 0.00 |

## Student knowledge graphs + Ollama timing

| id | SKG nodes | SKG edges | TTFT (s) | Total (s) | Response chars |
|---|---|---|---|---|---|
| `01_null_pointer_NP-A` | 8 | 7 | 12.0 | 42.5 | 2159 |
| `02_type_mismatch_TM-B` | 14 | 13 | 5.4 | 38.4 | 2136 |
| `03_infinite_loop_IL-B` | 9 | 8 | 5.8 | 31.8 | 1602 |
| `04_integer_division_ID-A` | 5 | 4 | 5.8 | 39.2 | 2097 |
| `05_array_index_AI-A` | 8 | 7 | 5.6 | 47.9 | 2236 |
| `06_string_equality_SE-A` | 8 | 7 | 6.1 | 54.7 | 3561 |
| `07_variable_scope_VS-A` | 5 | 4 | 6.1 | 35.2 | 2091 |
| `08_assignment_vs_compare_AC-A` | 5 | 4 | 6.2 | 37.7 | 1796 |
| `09_scanner_buffer_SB-A` | 5 | 4 | 5.9 | 49.7 | 3054 |
| `10_null_pointer_NP-B` | 8 | 7 | 5.5 | 58.0 | 3882 |

## Headline metrics

- Scenarios completed: 10/10
- Classifier wrong-model accuracy: 6/10 (60%)
- RAG hybrid wrong-model accuracy: 6/10 (60%)
- Times RAG flipped the classifier: 4
