# Ollama scenario run summary

- Timestamp: 2026-05-23_144252
- Model: llama3.1:8b
- Scenarios run: 194
- Successful: 194
- Errors: 0
- Wall-clock total: 2190.7s
- Avg time per scenario: 11.29s

## Per-scenario table

| # | id | layer | kind | ok | total_s | tokens | chars | name |
|---|---|---|---|---|---|---|---|---|
| 1 | `0.1` | L0 | student | ✓ | 9.29 | 93 | 419 | completely empty |
| 2 | `0.2` | L0 | student | ✓ | 4.71 | 28 | 117 | whitespace-only |
| 3 | `0.3a` | L0 | student | ✓ | 5.27 | 34 | 134 | single token '?' |
| 4 | `0.3b` | L0 | student | ✓ | 6.67 | 57 | 241 | single token '😭' |
| 5 | `0.3c` | L0 | student | ✓ | 5.03 | 34 | 158 | single token '.' |
| 6 | `0.3d` | L0 | student | ✓ | 8.35 | 84 | 360 | single token 'k' |
| 7 | `0.4` | L0 | infra | ✓ | 8.22 | 79 | 417 | idle session timer |
| 8 | `0.5a` | L0 | student | ✓ | 7.81 | 76 | 373 | idk variant 'idk' |
| 9 | `0.5b` | L0 | student | ✓ | 11.0 | 121 | 511 | idk variant "i don't know" |
| 10 | `0.5c` | L0 | student | ✓ | 11.21 | 126 | 565 | idk variant 'no clue' |
| 11 | `0.5d` | L0 | student | ✓ | 14.54 | 169 | 735 | idk variant 'no idea' |
| 12 | `0.7` | L0 | student | ✓ | 7.21 | 65 | 310 | empty code, real error |
| 13 | `0.8` | L0 | student | ✓ | 18.31 | 217 | 837 | empty error, real code |
| 14 | `0.9` | L0 | student | ✓ | 9.95 | 74 | 335 | code dump no question |
| 15 | `0.10` | L0 | student | ✓ | 15.56 | 177 | 690 | text only no actions |
| 16 | `0.11` | L0 | infra | ✓ | 10.07 | 106 | 568 | actions only no text |
| 17 | `0.12a` | L0 | student | ✓ | 3.67 | 14 | 44 | filler '...' |
| 18 | `0.12b` | L0 | student | ✓ | 7.82 | 74 | 301 | filler 'ok' |
| 19 | `0.12c` | L0 | student | ✓ | 5.29 | 39 | 164 | filler 'hmm' |
| 20 | `0.13` | L0 | student | ✓ | 13.65 | 179 | 717 | reply is code only |
| 21 | `0.14` | L0 | student | ✓ | 6.02 | 58 | 237 | refusal |
| 22 | `0.15` | L0 | infra | ✓ | 7.42 | 81 | 477 | screenshot empty-text fallthrough |
| 23 | `0.16` | L0 | infra | ✓ | 11.09 | 125 | 574 | tab closed mid-probe |
| 24 | `0.17` | L0 | infra | ✓ | 9.93 | 107 | 579 | return after long absence |
| 25 | `0.18` | L0 | infra | ✓ | 7.98 | 90 | 473 | missing API fields |
| 26 | `0.19` | L0 | infra | ✓ | 7.25 | 80 | 450 | null API fields |
| 27 | `0.20` | L0 | student | ✓ | 10.6 | 131 | 594 | disengagement / quit |
| 28 | `1.1` | L1 | student | ✓ | 11.37 | 145 | 521 | detect type_mismatch |
| 29 | `1.2` | L1 | student | ✓ | 10.9 | 110 | 458 | detect infinite_loop |
| 30 | `1.3` | L1 | student | ✓ | 7.42 | 70 | 338 | detect null_pointer |
| 31 | `1.4` | L1 | student | ✓ | 13.65 | 173 | 746 | detect string_equality |
| 32 | `1.5` | L1 | student | ✓ | 12.3 | 160 | 646 | detect variable_scope |
| 33 | `1.6` | L1 | student | ✓ | 10.66 | 125 | 447 | detect assignment_vs_compare |
| 34 | `1.7` | L1 | student | ✓ | 15.24 | 182 | 759 | detect integer_division |
| 35 | `1.8` | L1 | student | ✓ | 14.71 | 171 | 768 | detect scanner_buffer |
| 36 | `1.9` | L1 | student | ✓ | 14.07 | 168 | 681 | detect array_index |
| 37 | `1.10` | L1 | student | ✓ | 7.47 | 71 | 311 | detect missing_return |
| 38 | `1.11` | L1 | student | ✓ | 17.34 | 216 | 891 | detect array_not_allocated |
| 39 | `1.12` | L1 | student | ✓ | 12.33 | 135 | 529 | detect boolean_operators |
| 40 | `1.13` | L1 | student | ✓ | 16.23 | 185 | 725 | detect sentinel_loop |
| 41 | `1.14` | L1 | student | ✓ | 16.08 | 187 | 777 | detect unreachable_code |
| 42 | `1.15` | L1 | student | ✓ | 13.69 | 151 | 626 | detect string_immutability |
| 43 | `1.16` | L1 | student | ✓ | 15.26 | 172 | 778 | detect no_default_constructor |
| 44 | `1.17` | L1 | student | ✓ | 20.57 | 254 | 1076 | detect static_vs_instance |
| 45 | `1.18` | L1 | student | ✓ | 18.08 | 218 | 988 | detect foreach_no_modify |
| 46 | `1.19` | L1 | student | ✓ | 15.45 | 165 | 795 | detect overloading |
| 47 | `1.20` | L1 | student | ✓ | 12.52 | 129 | 541 | detect generics_primitives |
| 48 | `1.21` | L1 | student | ✓ | 11.99 | 125 | 623 | two concepts in one msg |
| 49 | `1.22` | L1 | student | ✓ | 12.63 | 141 | 675 | three concepts in one msg |
| 50 | `1.23` | L1 | student | ✓ | 13.39 | 151 | 590 | error-only signal |
| 51 | `1.24` | L1 | student | ✓ | 13.93 | 150 | 590 | code-only signal |
| 52 | `1.25` | L1 | student | ✓ | 15.17 | 183 | 811 | free-text weak signal |
| 53 | `1.26` | L1 | student | ✓ | 7.97 | 79 | 360 | typos in concept words |
| 54 | `1.27` | L1 | student | ✓ | 22.01 | 286 | 1435 | off-topic |
| 55 | `1.28` | L1 | student | ✓ | 16.98 | 198 | 840 | out-of-catalogue concept |
| 56 | `1.29` | L1 | student | ✓ | 12.81 | 142 | 625 | ambiguous concepts |
| 57 | `1.30` | L1 | student | ✓ | 9.71 | 101 | 352 | non-English |
| 58 | `2.1` | L2 | student | ✓ | 10.08 | 107 | 419 | WM null_pointer |
| 59 | `2.2` | L2 | student | ✓ | 15.11 | 178 | 754 | WM null_pointer |
| 60 | `2.3` | L2 | student | ✓ | 10.7 | 116 | 446 | WM string_equality |
| 61 | `2.4` | L2 | student | ✓ | 14.99 | 181 | 760 | WM string_equality |
| 62 | `2.5` | L2 | student | ✓ | 13.67 | 163 | 666 | WM null_pointer |
| 63 | `2.6` | L2 | student | ✓ | 13.45 | 157 | 643 | WM string_equality |
| 64 | `2.7` | L2 | student | ✓ | 14.19 | 165 | 690 | WM infinite_loop |
| 65 | `2.8` | L2 | student | ✓ | 14.82 | 176 | 762 | WM string_equality |
| 66 | `2.9` | L2 | student | ✓ | 16.27 | 203 | 723 | WM integer_division |
| 67 | `3.1` | L3 | student | ✓ | 8.59 | 89 | 411 | classify L1 |
| 68 | `3.2` | L3 | student | ✓ | 13.25 | 158 | 686 | classify L2 |
| 69 | `3.3` | L3 | student | ✓ | 16.97 | 206 | 966 | classify L3 |
| 70 | `3.4` | L3 | student | ✓ | 17.35 | 221 | 928 | classify L4 |
| 71 | `3.5` | L3 | student | ✓ | 16.65 | 208 | 972 | classify L2 |
| 72 | `3.6` | L3 | student | ✓ | 13.61 | 156 | 619 | classify L3 |
| 73 | `3.7` | L3 | student | ✓ | 12.68 | 143 | 616 | multi-concept differential LP |
| 74 | `3.8` | L3 | student | ✓ | 10.78 | 119 | 489 | regression to L1 from L3 |
| 75 | `4.1` | L4 | student | ✓ | 15.4 | 188 | 787 | first L2 |
| 76 | `4.2` | L4 | student | ✓ | 14.58 | 172 | 698 | second L2 → plateau |
| 77 | `4.4` | L4 | student | ✓ | 14.94 | 177 | 688 | plateau cleared by L3 jump |
| 78 | `4.5` | L4 | student | ✓ | 8.65 | 90 | 400 | plateau cleared by regression |
| 79 | `4.6` | L4 | infra | ✓ | 10.03 | 110 | 523 | per-concept plateau independence |
| 80 | `4.7` | L4 | student | ✓ | 15.19 | 188 | 762 | very long L2 plateau |
| 81 | `5.1` | L5 | student | ✓ | 16.63 | 200 | 884 | confident answer skips probe |
| 82 | `5.2` | L5 | student | ✓ | 17.67 | 197 | 830 | vague answer triggers probe |
| 83 | `5.3` | L5 | student | ✓ | 13.77 | 162 | 736 | probe answered well |
| 84 | `5.4` | L5 | infra | ✓ | 9.22 | 94 | 434 | probe cap constant |
| 85 | `5.5` | L5 | student | ✓ | 13.67 | 163 | 694 | probe continuity across turns |
| 86 | `5.6` | L5 | infra | ✓ | 8.64 | 86 | 424 | pick unprobed sub-criterion |
| 87 | `5.7` | L5 | student | ✓ | 15.56 | 180 | 737 | credit different-sub-criterion answer |
| 88 | `6.1` | L6 | student | ✓ | 15.95 | 182 | 789 | label=frustrated |
| 89 | `6.2` | L6 | student | ✓ | 17.51 | 211 | 912 | label=confused |
| 90 | `6.3` | L6 | student | ✓ | 13.7 | 155 | 690 | label=anxious |
| 91 | `6.4` | L6 | student | ✓ | 15.6 | 180 | 716 | label=engaged |
| 92 | `6.5` | L6 | student | ✓ | 6.99 | 65 | 317 | label=neutral |
| 93 | `6.6` | L6 | student | ✓ | 11.83 | 135 | 667 | label=frustrated |
| 94 | `6.7` | L6 | student | ✓ | 13.4 | 155 | 630 | label=engaged |
| 95 | `6.8` | L6 | student | ✓ | 8.01 | 76 | 365 | label=engaged |
| 96 | `7.1` | L7 | infra | ✓ | 9.16 | 92 | 536 | trial-and-error |
| 97 | `7.2` | L7 | infra | ✓ | 8.91 | 91 | 513 | systematic debug |
| 98 | `7.3` | L7 | infra | ✓ | 7.62 | 72 | 379 | long pause stuck |
| 99 | `7.5` | L7 | infra | ✓ | 8.12 | 76 | 415 | manic burst |
| 100 | `7.6` | L7 | infra | ✓ | 7.5 | 68 | 374 | read-only |
| 101 | `7.7` | L7 | infra | ✓ | 9.01 | 88 | 459 | help-avoidant |
| 102 | `8.1` | L8 | infra | ✓ | 10.2 | 98 | 515 | cold-start prior (HARD_CONCEPTS-aware) |
| 103 | `8.2` | L8 | infra | ✓ | 9.02 | 79 | 394 | 5x correct climbs |
| 104 | `8.3` | L8 | infra | ✓ | 9.88 | 102 | 567 | slip case |
| 105 | `8.4` | L8 | infra | ✓ | 8.15 | 79 | 454 | guess case |
| 106 | `8.5` | L8 | infra | ✓ | 10.67 | 113 | 585 | across-skill independence (per-skill prior) |
| 107 | `8.6` | L8 | infra | ✓ | 9.16 | 94 | 477 | persistence across restart |
| 108 | `8.7` | L8 | infra | ✓ | 8.7 | 86 | 451 | concurrent updates race |
| 109 | `8.8` | L8 | infra | ✓ | 10.04 | 103 | 521 | unknown skill key |
| 110 | `9.1` | L9 | student | ✓ | 11.48 | 124 | 460 | compile error |
| 111 | `9.2` | L9 | student | ✓ | 12.81 | 148 | 601 | runtime error |
| 112 | `9.3` | L9 | student | ✓ | 7.62 | 74 | 322 | logic error no exception |
| 113 | `9.4` | L9 | student | ✓ | 6.98 | 63 | 294 | no code text only |
| 114 | `9.5` | L9 | student | ✓ | 8.81 | 63 | 284 | huge code paste |
| 115 | `9.6` | L9 | student | ✓ | 6.8 | 62 | 277 | no error keywords |
| 116 | `9.7` | L9 | student | ✓ | 13.93 | 159 | 579 | mixed lang python |
| 117 | `9.8` | L9 | student | ✓ | 14.66 | 175 | 690 | pseudocode |
| 118 | `9.9` | L9 | student | ✓ | 4.32 | 23 | 110 | sql/script text |
| 119 | `9.10` | L9 | student | ✓ | 11.25 | 121 | 527 | odd unicode |
| 120 | `11.1` | L11 | student | ✓ | 9.95 | 102 | 432 | L1 should not get challenge_problem |
| 121 | `11.3` | L11 | student | ✓ | 12.9 | 146 | 657 | frustrated low mastery |
| 122 | `11.4` | L11 | student | ✓ | 12.46 | 143 | 676 | high mastery engaged |
| 123 | `11.5` | L11 | student | ✓ | 15.17 | 185 | 732 | wrong-model identified |
| 124 | `11.6` | L11 | student | ✓ | 13.4 | 157 | 682 | imposter syndrome |
| 125 | `11.7` | L11 | student | ✓ | 15.41 | 179 | 854 | new concept first encounter |
| 126 | `12.1` | L12 | infra | ✓ | 8.9 | 89 | 500 | positive learning gain |
| 127 | `12.2` | L12 | infra | ✓ | 8.9 | 91 | 455 | negative gain |
| 128 | `12.3` | L12 | infra | ✓ | 9.15 | 97 | 506 | delta_lp positive |
| 129 | `12.4` | L12 | infra | ✓ | 9.57 | 104 | 540 | plateau-broken |
| 130 | `12.5` | L12 | infra | ✓ | 9.74 | 106 | 559 | engagement signal |
| 131 | `12.6` | L12 | infra | ✓ | 8.7 | 86 | 459 | ZPD reward |
| 132 | `12.7` | L12 | infra | ✓ | 10.62 | 112 | 589 | attribution reward |
| 133 | `12.8` | L12 | infra | ✓ | 7.02 | 64 | 333 | RL module importable |
| 134 | `14.1` | L14 | student | ✓ | 8.89 | 88 | 367 | extremely long input |
| 135 | `14.2` | L14 | student | ✓ | 14.37 | 163 | 680 | emoji-heavy |
| 136 | `14.3` | L14 | student | ✓ | 6.59 | 53 | 230 | prompt-injection |
| 137 | `14.4` | L14 | student | ✓ | 4.9 | 28 | 151 | html/sql injection |
| 138 | `14.5` | L14 | student | ✓ | 6.82 | 54 | 248 | duplicate submission |
| 139 | `14.8` | L14 | infra | ✓ | 9.25 | 84 | 458 | massive action_sequence |
| 140 | `14.9` | L14 | infra | ✓ | 8.93 | 86 | 506 | time_deltas length mismatch |
| 141 | `14.10` | L14 | infra | ✓ | 8.99 | 90 | 486 | negative time_stuck |
| 142 | `14.11` | L14 | infra | ✓ | 8.01 | 77 | 389 | NaN time_stuck |
| 143 | `15.1` | L15 | student | ✓ | 11.0 | 120 | 537 | imposter language |
| 144 | `15.2` | L15 | student | ✓ | 11.76 | 136 | 651 | external attribution |
| 145 | `15.3` | L15 | student | ✓ | 14.25 | 170 | 801 | internal healthy |
| 146 | `15.4` | L15 | student | ✓ | 9.45 | 97 | 424 | internal unhealthy |
| 147 | `15.5` | L15 | student | ✓ | 16.14 | 199 | 853 | high encoding |
| 148 | `15.6` | L15 | student | ✓ | 8.03 | 79 | 365 | low encoding |
| 149 | `15.8` | L15 | student | ✓ | 17.38 | 196 | 804 | factual question |
| 150 | `18.1` | L18 | student | ✓ | 16.68 | 201 | 1008 | external attribution → reframe gate |
| 151 | `18.2` | L18 | student | ✓ | 8.78 | 89 | 415 | imposter + external combo |
| 152 | `18.3` | L18 | student | ✓ | 13.84 | 164 | 679 | self-correction reads as adaptive |
| 153 | `18.4` | L18 | student | ✓ | 13.99 | 166 | 697 | breakthrough → growth_efficacy |
| 154 | `18.5` | L18 | student | ✓ | 9.63 | 98 | 424 | prolonged grind → high_anxiety |
| 155 | `18.6` | L18 | student | ✓ | 19.75 | 218 | 927 | WM threshold boundary |
| 156 | `18.7` | L18 | student | ✓ | 13.98 | 155 | 662 | substance penalty fires on 2 tokens |
| 157 | `18.8` | L18 | student | ✓ | 14.97 | 169 | 724 | short legit answer NOT floored |
| 158 | `18.9` | L18 | student | ✓ | 15.09 | 170 | 718 | code comment doesn't leak to wrong concept |
| 159 | `18.10` | L18 | student | ✓ | 15.33 | 177 | 743 | anxiety + L1 → de-escalation |
| 160 | `18.11` | L18 | student | ✓ | 11.73 | 128 | 533 | stack trace alone |
| 161 | `18.12` | L18 | student | ✓ | 16.38 | 189 | 810 | essay reply → solid/deep encoding |
| 162 | `19.1` | L19 | infra | ✓ | 8.29 | 77 | 412 | DBStore upsert+read roundtrip |
| 163 | `19.2` | L19 | infra | ✓ | 9.72 | 99 | 506 | DB handles 10-thread concurrent writes |
| 164 | `19.3` | L19 | infra | ✓ | 9.96 | 102 | 502 | mastery decay after 28 days (2x half-life) |
| 165 | `19.4` | L19 | infra | ✓ | 8.52 | 82 | 448 | A/B assignment is sticky per student |
| 166 | `19.5` | L19 | infra | ✓ | 9.7 | 99 | 475 | A/B balanced across 200 students |
| 167 | `19.6` | L19 | infra | ✓ | 9.82 | 100 | 478 | GDPR delete wipes all traces + tombstone |
| 168 | `19.7` | L19 | infra | ✓ | 9.58 | 98 | 492 | GDPR export contains all fields |
| 169 | `19.8` | L19 | infra | ✓ | 11.84 | 129 | 606 | auth token roundtrip |
| 170 | `19.9` | L19 | infra | ✓ | 10.18 | 98 | 542 | auth token rejects tampering |
| 171 | `19.10` | L19 | infra | ✓ | 10.5 | 116 | 564 | auth token rejects expiry |
| 172 | `19.11` | L19 | infra | ✓ | 8.74 | 91 | 475 | heatmap + struggle aggregation |
| 173 | `19.12` | L19 | infra | ✓ | 8.53 | 86 | 436 | intervention counts aggregation |
| 174 | `19.13` | L19 | infra | ✓ | 8.57 | 85 | 415 | consent default false + set + revoke |
| 175 | `19.14` | L19 | infra | ✓ | 8.72 | 81 | 401 | audit log preserves insertion order |
| 176 | `19.15` | L19 | infra | ✓ | 10.97 | 113 | 544 | decay after 100 days approaches prior |
| 177 | `20.1` | L20 | infra | ✓ | 12.11 | 137 | 623 | progression_for filters by skill + preserves order |
| 178 | `20.2` | L20 | infra | ✓ | 7.77 | 76 | 421 | mastery_trajectory points roundtrip |
| 179 | `20.3` | L20 | infra | ✓ | 8.78 | 92 | 450 | forecast: advancing student |
| 180 | `20.4` | L20 | infra | ✓ | 8.71 | 87 | 419 | forecast: plateaued student |
| 181 | `20.5` | L20 | infra | ✓ | 8.77 | 84 | 447 | forecast: insufficient data → None |
| 182 | `20.6` | L20 | infra | ✓ | 12.11 | 132 | 670 | cohort_percentile basic |
| 183 | `20.7` | L20 | infra | ✓ | 9.62 | 97 | 506 | cohort_percentile top student |
| 184 | `20.8` | L20 | infra | ✓ | 9.16 | 90 | 453 | trajectory empty for unknown student |
| 185 | `20.9` | L20 | infra | ✓ | 10.06 | 96 | 489 | full simulated 6-turn session flow |
| 186 | `20.10` | L20 | infra | ✓ | 10.09 | 107 | 575 | intervention captured per-turn AND aggregated |
| 187 | `20.11` | L20 | infra | ✓ | 8.24 | 80 | 411 | session_id preserved in turn audit |
| 188 | `20.12` | L20 | infra | ✓ | 9.49 | 98 | 508 | dwell_s preserved per turn |
| 189 | `21.1` | L21 | infra | ✓ | 7.61 | 79 | 436 | reasoning length+complexity per turn |
| 190 | `21.2` | L21 | infra | ✓ | 8.16 | 91 | 423 | correct_streak grows + resets |
| 191 | `21.3` | L21 | infra | ✓ | 8.44 | 95 | 509 | KG concept + counts per turn |
| 192 | `21.4` | L21 | infra | ✓ | 10.16 | 104 | 565 | COKE cognitive_state per turn |
| 193 | `21.5` | L21 | infra | ✓ | 11.32 | 117 | 582 | KG block sizes per turn |
| 194 | `21.6` | L21 | infra | ✓ | 8.19 | 72 | 367 | old + new fields coexist in one turn |