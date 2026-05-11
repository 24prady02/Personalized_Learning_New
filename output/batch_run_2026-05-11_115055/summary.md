# Full-stack batch run summary

Ran 10 scenarios at 2026-05-11_115055.

## Wrong-belief identification (classifier vs RAG hybrid)

| # | id | expected | classifier | hybrid (RAG) | flipped | cls✓ | rag✓ |
|---|---|---|---|---|---|---|---|
| 1 | `01_null_pointer_NP-A` | **NP-A** | NP-B | NP-B |  | ✗ | ✗ |
| 2 | `02_type_mismatch_TM-B` | **TM-B** | TM-A | TM-B | ⟲ | ✗ | ✓ |
| 3 | `03_infinite_loop_IL-B` | **IL-B** | IL-B | IL-B |  | ✓ | ✓ |
| 4 | `04_integer_division_ID-A` | **ID-A** | ID-A | ID-A |  | ✓ | ✓ |
| 5 | `05_array_index_AI-A` | **AI-A** | AI-C | AI-B | ⟲ | ✗ | ✗ |
| 6 | `06_string_equality_SE-A` | **SE-A** | SE-A | SE-A |  | ✓ | ✓ |
| 7 | `07_variable_scope_VS-A` | **VS-A** | VS-A | VS-A |  | ✓ | ✓ |
| 8 | `08_assignment_vs_compare_AC-A` | **AC-A** | AC-C | AC-C |  | ✗ | ✗ |
| 9 | `09_scanner_buffer_SB-A` | **SB-A** | SB-A | SB-A |  | ✓ | ✓ |
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

## Mastery updates (BKT, after failure)

| id | concept | BKT before | BKT after |
|---|---|---|---|
| `01_null_pointer_NP-A` | null_pointer | 0.25 | 0.23 |
| `02_type_mismatch_TM-B` | type_mismatch | 0.20 | 0.23 |
| `03_infinite_loop_IL-B` | infinite_loop | 0.15 | 0.22 |
| `04_integer_division_ID-A` | integer_division | 0.20 | 0.23 |
| `05_array_index_AI-A` | array_index | 0.30 | 0.24 |
| `06_string_equality_SE-A` | string_equality | 0.20 | 0.23 |
| `07_variable_scope_VS-A` | variable_scope | 0.20 | 0.23 |
| `08_assignment_vs_compare_AC-A` | assignment_vs_compare | 0.15 | 0.22 |
| `09_scanner_buffer_SB-A` | scanner_buffer | 0.20 | 0.23 |
| `10_null_pointer_NP-B` | null_pointer | 0.30 | 0.24 |

## Student knowledge graphs + Ollama timing

| id | SKG nodes | SKG edges | TTFT (s) | Total (s) | Response chars |
|---|---|---|---|---|---|
| `01_null_pointer_NP-A` | 8 | 7 | 5.1 | 28.1 | 1860 |
| `02_type_mismatch_TM-B` | 14 | 13 | 5.0 | 40.9 | 2585 |
| `03_infinite_loop_IL-B` | 9 | 8 | 5.2 | 31.9 | 2112 |
| `04_integer_division_ID-A` | 5 | 4 | 5.6 | 31.0 | 1788 |
| `05_array_index_AI-A` | 8 | 7 | 5.1 | 67.4 | 3903 |
| `06_string_equality_SE-A` | 8 | 7 | 5.8 | 43.2 | 2562 |
| `07_variable_scope_VS-A` | 5 | 4 | 5.6 | 37.9 | 2310 |
| `08_assignment_vs_compare_AC-A` | 5 | 4 | 5.6 | 41.7 | 2350 |
| `09_scanner_buffer_SB-A` | 5 | 4 | 5.8 | 32.3 | 1614 |
| `10_null_pointer_NP-B` | 8 | 7 | 5.0 | 47.0 | 3307 |

## Headline metrics

- Scenarios completed: 10/10
- Classifier wrong-model accuracy: 6/10 (60%)
- RAG hybrid wrong-model accuracy: 7/10 (70%)
- Times RAG flipped the classifier: 2