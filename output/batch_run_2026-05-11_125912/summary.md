# Full-stack batch run summary

Ran 10 scenarios at 2026-05-11_125912.

## Wrong-belief identification (classifier vs RAG hybrid)

| # | id | expected | classifier | hybrid (RAG) | flipped | cls✓ | rag✓ |
|---|---|---|---|---|---|---|---|
| 1 | `01_null_pointer_NP-A` | **NP-A** | NP-B | NP-B |  | ✗ | ✗ |
| 2 | `02_type_mismatch_TM-B` | **TM-B** | TM-A | TM-B | ⟲ | ✗ | ✓ |
| 3 | `03_infinite_loop_IL-B` | **IL-B** | IL-A | IL-A |  | ✗ | ✗ |
| 4 | `04_integer_division_ID-A` | **ID-A** | ID-B | ID-A | ⟲ | ✗ | ✓ |
| 5 | `05_array_index_AI-A` | **AI-A** | AI-C | AI-B | ⟲ | ✗ | ✗ |
| 6 | `06_string_equality_SE-A` | **SE-A** | SE-B | SE-A | ⟲ | ✗ | ✓ |
| 7 | `07_variable_scope_VS-A` | **VS-A** | VS-C | VS-C |  | ✗ | ✗ |
| 8 | `08_assignment_vs_compare_AC-A` | **AC-A** | AC-B | AC-C | ⟲ | ✗ | ✗ |
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
| `01_null_pointer_NP-A` | 8 | 7 | 15.3 | 68.1 | 3116 |
| `02_type_mismatch_TM-B` | 14 | 13 | 5.1 | 8.5 | 221 |
| `03_infinite_loop_IL-B` | 9 | 8 | 5.3 | 20.1 | 930 |
| `04_integer_division_ID-A` | 5 | 4 | 5.4 | 29.7 | 1456 |
| `05_array_index_AI-A` | 8 | 7 | 4.9 | 58.9 | 2829 |
| `06_string_equality_SE-A` | 8 | 7 | 5.6 | 39.7 | 1814 |
| `07_variable_scope_VS-A` | 5 | 4 | 5.5 | 42.7 | 2340 |
| `08_assignment_vs_compare_AC-A` | 5 | 4 | 5.4 | 69.8 | 3513 |
| `09_scanner_buffer_SB-A` | 5 | 4 | 5.5 | 46.9 | 2333 |
| `10_null_pointer_NP-B` | 8 | 7 | 50.1 | 79.4 | 1809 |

## Headline metrics

- Scenarios completed: 10/10
- Classifier wrong-model accuracy: 1/10 (10%)
- RAG hybrid wrong-model accuracy: 5/10 (50%)
- Times RAG flipped the classifier: 6