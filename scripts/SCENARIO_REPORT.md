# CPAL scenario harness report

## Layer 0 — Silence / non-response

- [OK] **0.1** _completely empty_  (3.02s)
    - output: `{"resolved": [["unknown", 0.0]], "stage": 1}`
- [OK] **0.2** _whitespace-only_  (0.0s)
    - output: `{"resolved": [["unknown", 0.0]]}`
- [OK] **0.3a** _single token '?'_  (0.14s)
    - output: `{"top": "unknown", "encoding_strength": "partial"}`
- [OK] **0.3b** _single token '😭'_  (0.1s)
    - output: `{"top": "unknown", "encoding_strength": "partial"}`
- [OK] **0.3c** _single token '.'_  (0.1s)
    - output: `{"top": "unknown", "encoding_strength": "partial"}`
- [OK] **0.3d** _single token 'k'_  (0.09s)
    - output: `{"top": "unknown", "encoding_strength": "partial"}`
- [OK] **0.5a** _idk variant 'idk'_  (0.09s)
    - output: `{"confidence": 0.3, "lp": "L1"}`
- [OK] **0.5b** _idk variant "i don't know"_  (0.06s)
    - output: `{"confidence": 0.3, "lp": "L1"}`
- [OK] **0.5c** _idk variant 'no clue'_  (0.06s)
    - output: `{"confidence": 0.3, "lp": "L1"}`
- [OK] **0.5d** _idk variant 'no idea'_  (0.07s)
    - output: `{"confidence": 0.3, "lp": "L1"}`
- [OK] **0.7** _empty code, real error_  (0.0s)
    - output: `{"resolved": [["null_pointer", 0.675]]}`
- [~] **0.8** _empty error, real code_  (0.0s)
    - drawback: code-only → unknown
    - output: `{"resolved": [["unknown", 0.0]]}`
- [ok] **0.9** _code dump no question_  (0.07s)
    - output: `{"encoding_strength": "surface"}`
- [OK] **0.10** _text only no actions_  (0.1s)
    - output: `{"top": "string_equality", "stage": 1}`
- [OK] **0.11** _actions only no text_  (0.0s)
    - output: `{"top": "unknown"}`
- [OK] **0.12a** _filler '...'_  (0.04s)
    - output: `{"top": "unknown"}`
- [OK] **0.12b** _filler 'ok'_  (0.04s)
    - output: `{"top": "unknown"}`
- [OK] **0.12c** _filler 'hmm'_  (0.03s)
    - output: `{"top": "unknown"}`
- [OK] **0.13** _reply is code only_  (0.06s)
    - output: `{"logical_step": false}`
- [OK] **0.14** _refusal_  (0.03s)
    - output: `{"top": "unknown"}`
- [OK] **0.15** _screenshot empty-text fallthrough_  (0.0s)
    - output: `{"note": "same as 0.1"}`
- [ok] **0.20** _disengagement / quit_  (0.08s)
    - output: `{"intervention": "worked_example", "self_efficacy": "neutral", "attribution": "neutral", "high_anxiety": false}`
- [-] **0.4** _idle session timer_  (0.0s)
    - drawback: needs wall-clock or REST API
- [-] **0.16** _tab closed mid-probe_  (0.0s)
    - drawback: needs wall-clock or REST API
- [-] **0.17** _return after long absence_  (0.0s)
    - drawback: needs wall-clock or REST API
- [-] **0.18** _missing API fields_  (0.0s)
    - drawback: needs wall-clock or REST API
- [-] **0.19** _null API fields_  (0.0s)
    - drawback: needs wall-clock or REST API

## Layer 1 — Concept detection

- [OK] **1.1** _detect type_mismatch_  (0.04s)
    - output: `{"top": "type_mismatch", "conf": 0.22, "top3": [["type_mismatch", 0.22]]}`
- [OK] **1.2** _detect infinite_loop_  (0.03s)
    - output: `{"top": "infinite_loop", "conf": 0.512, "top3": [["infinite_loop", 0.512], ["variable_scope", 0.216]]}`
- [OK] **1.3** _detect null_pointer_  (0.04s)
    - output: `{"top": "null_pointer", "conf": 0.141, "top3": [["null_pointer", 0.141]]}`
- [OK] **1.4** _detect string_equality_  (0.03s)
    - output: `{"top": "string_equality", "conf": 0.647, "top3": [["string_equality", 0.647], ["assignment_vs_compare", 0.436], ["boolean_operators", 0.23]]}`
- [OK] **1.5** _detect variable_scope_  (0.0s)
    - output: `{"top": "variable_scope", "conf": 0.675, "top3": [["variable_scope", 0.675]]}`
- [OK] **1.6** _detect assignment_vs_compare_  (0.03s)
    - output: `{"top": "assignment_vs_compare", "conf": 0.436, "top3": [["assignment_vs_compare", 0.436], ["boolean_operators", 0.319], ["string_equality", 0.29]]}`
- [OK] **1.7** _detect integer_division_  (0.04s)
    - output: `{"top": "integer_division", "conf": 0.512, "top3": [["integer_division", 0.512]]}`
- [OK] **1.8** _detect scanner_buffer_  (0.0s)
    - output: `{"top": "scanner_buffer", "conf": 0.61, "top3": [["scanner_buffer", 0.61]]}`
- [OK] **1.9** _detect array_index_  (0.04s)
    - output: `{"top": "array_index", "conf": 0.315, "top3": [["array_index", 0.315]]}`
- [OK] **1.10** _detect missing_return_  (0.0s)
    - output: `{"top": "missing_return", "conf": 0.61, "top3": [["missing_return", 0.61]]}`
- [OK] **1.11** _detect array_not_allocated_  (0.03s)
    - output: `{"top": "array_not_allocated", "conf": 0.287, "top3": [["array_not_allocated", 0.287]]}`
- [OK] **1.12** _detect boolean_operators_  (0.03s)
    - output: `{"top": "boolean_operators", "conf": 0.122, "top3": [["boolean_operators", 0.122]]}`
- [OK] **1.13** _detect sentinel_loop_  (0.0s)
    - output: `{"top": "sentinel_loop", "conf": 0.61, "top3": [["sentinel_loop", 0.61]]}`
- [OK] **1.14** _detect unreachable_code_  (0.03s)
    - output: `{"top": "unreachable_code", "conf": 0.544, "top3": [["unreachable_code", 0.544], ["missing_return", 0.333]]}`
- [OK] **1.15** _detect string_immutability_  (0.0s)
    - output: `{"top": "string_immutability", "conf": 0.675, "top3": [["string_immutability", 0.675]]}`
- [OK] **1.16** _detect no_default_constructor_  (0.03s)
    - output: `{"top": "no_default_constructor", "conf": 0.362, "top3": [["no_default_constructor", 0.362]]}`
- [OK] **1.17** _detect static_vs_instance_  (0.04s)
    - output: `{"top": "static_vs_instance", "conf": 0.238, "top3": [["static_vs_instance", 0.238]]}`
- [OK] **1.18** _detect foreach_no_modify_  (0.03s)
    - output: `{"top": "foreach_no_modify", "conf": 0.512, "top3": [["foreach_no_modify", 0.512]]}`
- [OK] **1.19** _detect overloading_  (0.04s)
    - output: `{"top": "overloading", "conf": 0.207, "top3": [["overloading", 0.207], ["variable_scope", 0.206]]}`
- [OK] **1.20** _detect generics_primitives_  (0.03s)
    - output: `{"top": "generics_primitives", "conf": 0.512, "top3": [["generics_primitives", 0.512], ["array_not_allocated", 0.255]]}`
- [OK] **1.21** _two concepts in one msg_  (0.03s)
    - output: `{"top3": ["array_index", "infinite_loop"]}`
- [OK] **1.22** _three concepts in one msg_  (0.03s)
    - output: `{"top3": ["string_equality", "infinite_loop"]}`
- [OK] **1.23** _error-only signal_  (0.0s)
    - output: `{"top": "type_mismatch"}`
- [~] **1.24** _code-only signal_  (0.0s)
    - drawback: code-only got unknown
    - output: `{"top": "unknown"}`
- [~] **1.25** _free-text weak signal_  (0.05s)
    - drawback: weak text → assignment_vs_compare
    - output: `{"top": "assignment_vs_compare", "conf": 0.396}`
- [OK] **1.26** _typos in concept words_  (0.06s)
    - drawback: no fuzzy/typo matching — caught as unknown is acceptable, but inflexible
    - output: `{"top": "unknown"}`
- [OK] **1.27** _off-topic_  (0.02s)
    - output: `{"top": "unknown"}`
- [OK] **1.28** _out-of-catalogue concept_  (0.05s)
    - output: `{"top": "unknown"}`
- [OK] **1.29** _ambiguous concepts_  (0.04s)
    - output: `{"top3": ["string_equality", "assignment_vs_compare", "boolean_operators"]}`
- [~] **1.30** _non-English_  (0.03s)
    - output: `{"top": "infinite_loop"}`

## Layer 2 — Wrong-model identification (overlap matcher only — no HVSAE)

- [OK] **2.1** _WM null_pointer_  (0.06s)
    - output: `{"wm": "NP-A", "score": 0.927, "lp": "L1", "source": "trained_wm_head"}`
- [OK] **2.2** _WM null_pointer_  (0.06s)
    - output: `{"wm": "NP-B", "score": 0.607, "lp": "L1", "source": "trained_wm_head"}`
- [X] **2.3** _WM string_equality_  (0.07s)
    - drawback: false WM hit: wm=SE-C score=0.81
    - output: `{"wm": "SE-C", "score": 0.808, "lp": "L1", "source": "trained_wm_head"}`
- [OK] **2.4** _WM string_equality_  (0.06s)
    - output: `{"wm": null, "score": 0.0, "lp": "L3", "source": "overlap"}`
- [X] **2.5** _WM null_pointer_  (0.06s)
    - drawback: false WM hit: wm=NP-C score=0.74
    - output: `{"wm": "NP-C", "score": 0.742, "lp": "L1", "source": "trained_wm_head"}`
- [OK] **2.6** _WM string_equality_  (0.06s)
    - output: `{"wm": null, "score": 0.0, "lp": "L1", "source": "overlap"}`
- [OK] **2.7** _WM infinite_loop_  (0.05s)
    - output: `{"wm": "IL-A", "score": 0.653, "lp": "L1", "source": "trained_wm_head"}`
- [OK] **2.8** _WM string_equality_  (0.06s)
    - output: `{"wm": "SE-A", "score": 1.0, "lp": "L2", "source": "overlap"}`
- [OK] **2.9** _WM integer_division_  (0.07s)
    - output: `{"wm": "ID-A", "score": 0.657, "lp": "L1", "source": "trained_wm_head"}`

## Layer 3 — LP-level classification

- [OK] **3.1** _classify L1_  (0.06s)
    - output: `{"lp": "L1", "target": "L2", "logical_step": false, "logical_step_detail": false, "trained_probs": {"L1": 0.9894986152648926, "L2": 0.01050030067563057, "L3": 8.657730177219491e-07, "L4": 2.7122550250169297e-07}}`
- [OK] **3.2** _classify L2_  (0.07s)
    - output: `{"lp": "L2", "target": "L3", "logical_step": true, "logical_step_detail": false, "trained_probs": {"L1": 0.39112916588783264, "L2": 0.5990920066833496, "L3": 0.006470147054642439, "L4": 0.003308670362457633}}`
- [~] **3.3** _classify L3_  (0.07s)
    - drawback: expected L3, got L2
    - output: `{"lp": "L2", "target": "L3", "logical_step": true, "logical_step_detail": true, "trained_probs": {"L1": 0.01947147771716118, "L2": 0.47476449608802795, "L3": 0.18555083870887756, "L4": 0.32021331787109375}}`
- [~] **3.4** _classify L4_  (0.08s)
    - drawback: expected L4, got L3
    - output: `{"lp": "L3", "target": "L4", "logical_step": true, "logical_step_detail": false, "trained_probs": {"L1": 0.001275587361305952, "L2": 0.03409096226096153, "L3": 0.7382758855819702, "L4": 0.22635754942893982}}`
- [~] **3.5** _classify L2_  (0.07s)
    - drawback: expected L2, got L3
    - output: `{"lp": "L3", "target": "L4", "logical_step": true, "logical_step_detail": true, "trained_probs": {"L1": 0.00011333839211147279, "L2": 0.003952374681830406, "L3": 0.9945408701896667, "L4": 0.0013933631125837564}}`
- [~] **3.6** _classify L3_  (0.07s)
    - drawback: expected L3, got L2
    - output: `{"lp": "L2", "target": "L3", "logical_step": true, "logical_step_detail": true, "trained_probs": {"L1": 0.054709844291210175, "L2": 0.784259557723999, "L3": 0.1485370397567749, "L4": 0.012493588030338287}}`
- [OK] **3.7** _multi-concept differential LP_  (0.1s)
    - output: `{"per_concept_lp": {"null_pointer": "L4"}}`
- [~] **3.8** _regression to L1 from L3_  (0.07s)
    - drawback: regression-after-L3 still L3
    - output: `{"lp": "L3"}`

## Layer 4 — Plateau / streak

- [OK] **4.1** _first L2_  (0.06s)
    - output: `{"plateau_flag": false, "lp": "L1"}`
- [OK] **4.2** _second L2 → plateau_  (0.07s)
    - output: `{"plateau_flag": true, "intervention": "trace_scaffold"}`
- [OK] **4.4** _plateau cleared by L3 jump_  (0.06s)
    - output: `{"lp": "L3", "plateau_flag": false}`
- [~] **4.5** _plateau cleared by regression_  (0.06s)
    - drawback: regression missed (got L2)
    - output: `{"lp": "L2", "plateau_flag": true}`
- [OK] **4.6** _per-concept plateau independence_  (0.14s)
    - output: `{"np.plateau": true, "se.plateau": false}`
- [OK] **4.7** _very long L2 plateau_  (0.07s)
    - output: `{"plateau_flag": true, "intervention": "trace_scaffold"}`

## Layer 5 — Probe loop confidence branches

- [~] **5.1** _confident answer skips probe_  (0.07s)
    - drawback: L3 reply got conf=0.38
    - output: `{"confidence": 0.375}`
- [OK] **5.2** _vague answer triggers probe_  (0.05s)
    - output: `{"confidence": 0.3}`
- [OK] **5.3** _probe answered well_  (0.07s)
    - output: `{"confidence": 0.75}`
- [OK] **5.4** _probe cap constant_  (41.73s)
    - output: `{"cap": 8}`
- [-] **5.5** _probe continuity across turns_  (0.0s)
    - drawback: multi-turn — covered by chat app flow, not single-call harness
- [-] **5.6** _pick unprobed sub-criterion_  (0.0s)
    - drawback: multi-turn — covered by chat app flow, not single-call harness
- [-] **5.7** _credit different-sub-criterion answer_  (0.0s)
    - drawback: multi-turn — covered by chat app flow, not single-call harness

## Layer 6 — Emotion / behavioral surface signals

- [ok] **6.1** _label=frustrated_  (0.06s)
    - output: `{"expected_label": "frustrated", "attribution": "neutral", "self_efficacy": "neutral", "high_anxiety": true, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`
- [ok] **6.2** _label=confused_  (0.06s)
    - output: `{"expected_label": "confused", "attribution": "neutral", "self_efficacy": "neutral", "high_anxiety": false, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`
- [ok] **6.3** _label=anxious_  (0.05s)
    - output: `{"expected_label": "anxious", "attribution": "neutral", "self_efficacy": "neutral", "high_anxiety": true, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`
- [ok] **6.4** _label=engaged_  (0.05s)
    - output: `{"expected_label": "engaged", "attribution": "neutral", "self_efficacy": "growth", "high_anxiety": false, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`
- [ok] **6.5** _label=neutral_  (0.05s)
    - output: `{"expected_label": "neutral", "attribution": "neutral", "self_efficacy": "neutral", "high_anxiety": false, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`
- [ok] **6.6** _label=frustrated_  (0.05s)
    - output: `{"expected_label": "frustrated", "attribution": "neutral", "self_efficacy": "neutral", "high_anxiety": false, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`
- [ok] **6.7** _label=engaged_  (0.05s)
    - output: `{"expected_label": "engaged", "attribution": "neutral", "self_efficacy": "neutral", "high_anxiety": false, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`
- [ok] **6.8** _label=engaged_  (0.07s)
    - output: `{"expected_label": "engaged", "attribution": "neutral", "self_efficacy": "growth", "high_anxiety": false, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`

## Layer 7 — Behavioral actions (resolver smoke)

- [OK] **7.1** _trial-and-error_  (0.09s)
    - output: `{"top": "unknown", "stage": 1}`
- [OK] **7.2** _systematic debug_  (0.08s)
    - output: `{"top": "unknown", "stage": 1}`
- [OK] **7.3** _long pause stuck_  (0.1s)
    - output: `{"top": "unknown", "stage": 1}`
- [OK] **7.5** _manic burst_  (0.08s)
    - output: `{"top": "unknown", "stage": 1}`
- [OK] **7.6** _read-only_  (0.1s)
    - output: `{"top": "unknown", "stage": 1}`
- [OK] **7.7** _help-avoidant_  (0.07s)
    - output: `{"top": "unknown", "stage": 1}`

## Layer 8 — DINA mastery

- [~] **8.1** _cold-start prior_  (0.0s)
    - drawback: prior 0.15 not ~0.30
    - output: `{"prior": 0.15}`
- [OK] **8.2** _5x correct climbs_  (0.0s)
    - output: `{"after": 0.99}`
- [OK] **8.3** _slip case_  (0.0s)
    - output: `{"pre": 0.99, "post": 0.9295774647887324}`
- [OK] **8.4** _guess case_  (0.0s)
    - output: `{"before": 0.15, "after": 0.5107913669064748}`
- [~] **8.5** _across-skill independence_  (0.0s)
    - drawback: untouched skill drifted to 0.15
    - output: `{"untouched": 0.15}`
- [OK] **8.8** _unknown skill key_  (0.0s)
    - output: `{"result": {"skill": "totally_made_up_skill", "mastery": 0.3, "updated": false}}`
- [-] **8.6** _persistence across restart_  (0.0s)
    - drawback: requires restart/threading harness
- [-] **8.7** _concurrent updates race_  (0.0s)
    - drawback: requires restart/threading harness

## Layer 9 — Code input variations

- [OK] **9.1** _compile error_  (0.0s)
    - output: `{"top": "variable_scope", "conf": 0.675}`
- [OK] **9.2** _runtime error_  (0.0s)
    - output: `{"top": "null_pointer", "conf": 0.675}`
- [OK] **9.3** _logic error no exception_  (0.03s)
    - output: `{"top": "unknown", "conf": 0.0}`
- [OK] **9.4** _no code text only_  (0.02s)
    - output: `{"top": "unknown", "conf": 0.0}`
- [OK] **9.5** _huge code paste_  (0.03s)
    - output: `{"top": "unknown", "conf": 0.0}`
- [OK] **9.6** _no error keywords_  (0.02s)
    - output: `{"top": "unknown", "conf": 0.0}`
- [OK] **9.7** _mixed lang python_  (0.02s)
    - output: `{"top": "unknown", "conf": 0.0}`
- [OK] **9.8** _pseudocode_  (0.02s)
    - output: `{"top": "unknown", "conf": 0.0}`
- [OK] **9.9** _sql/script text_  (0.03s)
    - output: `{"top": "unknown", "conf": 0.0}`
- [OK] **9.10** _odd unicode_  (0.02s)
    - output: `{"top": "unknown", "conf": 0.0}`

## Layer 11 — Intervention selection

- [ok] **11.1** _L1 should not get challenge_problem_  (0.05s)
    - output: `{"intervention": "worked_example", "imposter_flag": true, "self_efficacy": "neutral", "attribution": "neutral"}`
- [ok] **11.3** _frustrated low mastery_  (0.06s)
    - output: `{"intervention": "reduce_challenge", "imposter_flag": true, "self_efficacy": "neutral", "attribution": "neutral"}`
- [ok] **11.4** _high mastery engaged_  (0.05s)
    - output: `{"intervention": "worked_example", "imposter_flag": true, "self_efficacy": "neutral", "attribution": "neutral"}`
- [ok] **11.5** _wrong-model identified_  (0.05s)
    - output: `{"intervention": "worked_example", "imposter_flag": true, "self_efficacy": "neutral", "attribution": "neutral"}`
- [ok] **11.6** _imposter syndrome_  (0.05s)
    - output: `{"intervention": "attribution_reframe", "imposter_flag": true, "self_efficacy": "neutral", "attribution": "fixed"}`
- [ok] **11.7** _new concept first encounter_  (0.05s)
    - output: `{"intervention": "worked_example", "imposter_flag": true, "self_efficacy": "neutral", "attribution": "neutral"}`

## Layer 12 — RL module

- [OK] **12.8** _RL module importable_  (0.0s)
- [-] **12.1** _positive learning gain_  (0.0s)
    - drawback: requires full session→reward loop
- [-] **12.2** _negative gain_  (0.0s)
    - drawback: requires full session→reward loop
- [-] **12.3** _delta_lp positive_  (0.0s)
    - drawback: requires full session→reward loop
- [-] **12.4** _plateau-broken_  (0.0s)
    - drawback: requires full session→reward loop
- [-] **12.5** _engagement signal_  (0.0s)
    - drawback: requires full session→reward loop
- [-] **12.6** _ZPD reward_  (0.0s)
    - drawback: requires full session→reward loop
- [-] **12.7** _attribution reward_  (0.0s)
    - drawback: requires full session→reward loop

## Layer 14 — Adversarial / robustness

- [OK] **14.1** _extremely long input_  (0.06s)
    - output: `{"top": "unknown"}`
- [OK] **14.2** _emoji-heavy_  (0.03s)
    - output: `{"top": "unknown"}`
- [OK] **14.3** _prompt-injection_  (0.02s)
    - output: `{"top": "unknown"}`
- [OK] **14.4** _html/sql injection_  (0.03s)
    - output: `{"top": "unknown"}`
- [OK] **14.5** _duplicate submission_  (0.02s)
    - output: `{"top": "unknown"}`
- [OK] **14.8** _massive action_sequence_  (0.02s)
    - output: `{"top": "null_pointer"}`
- [OK] **14.9** _time_deltas length mismatch_  (0.03s)
    - output: `{"top": "null_pointer"}`
- [OK] **14.10** _negative time_stuck_  (0.02s)
    - output: `{"top": "null_pointer"}`
- [OK] **14.11** _NaN time_stuck_  (0.03s)
    - output: `{"top": "null_pointer"}`

## Layer 15 — Three-channel analysis

- [ok] **15.1** _imposter language_  (0.05s)
    - output: `{"expected": "imposter_flag=True", "imposter_flag": true, "attribution": "fixed", "self_efficacy": "neutral", "encoding_strength": "partial", "lang_imposter": true}`
- [ok] **15.2** _external attribution_  (0.05s)
    - output: `{"expected": "attribution=external", "imposter_flag": true, "attribution": "external", "self_efficacy": "neutral", "encoding_strength": "partial", "lang_imposter": false}`
- [ok] **15.3** _internal healthy_  (0.05s)
    - output: `{"expected": "internal, not imposter", "imposter_flag": true, "attribution": "adaptive", "self_efficacy": "neutral", "encoding_strength": "partial", "lang_imposter": false}`
- [ok] **15.4** _internal unhealthy_  (0.05s)
    - output: `{"expected": "internal + imposter", "imposter_flag": true, "attribution": "fixed", "self_efficacy": "neutral", "encoding_strength": "partial", "lang_imposter": false}`
- [ok] **15.5** _high encoding_  (0.05s)
    - output: `{"expected": "encoding=high", "imposter_flag": true, "attribution": "neutral", "self_efficacy": "neutral", "encoding_strength": "partial", "lang_imposter": false}`
- [ok] **15.6** _low encoding_  (0.05s)
    - output: `{"expected": "encoding=low", "imposter_flag": true, "attribution": "neutral", "self_efficacy": "neutral", "encoding_strength": "partial", "lang_imposter": false}`
- [ok] **15.8** _factual question_  (0.05s)
    - output: `{"expected": "neutral psych", "imposter_flag": true, "attribution": "neutral", "self_efficacy": "neutral", "encoding_strength": "partial", "lang_imposter": false}`

## Layer 18 — Added scenarios (post-fix gap coverage)

- [OK] **18.1** _external attribution → reframe gate_  (0.05s)
    - output: `{"attribution": "external", "intervention": "attribution_reframe"}`
- [OK] **18.2** _imposter + external combo_  (0.05s)
    - output: `{"imposter": true, "attribution": "fixed", "intervention": "attribution_reframe"}`
- [OK] **18.3** _self-correction reads as adaptive_  (0.05s)
    - output: `{"attribution": "adaptive", "self_efficacy": "neutral"}`
- [OK] **18.4** _breakthrough → growth_efficacy_  (0.05s)
    - output: `{"self_efficacy": "growth", "attribution": "neutral"}`
- [OK] **18.5** _prolonged grind → high_anxiety_  (0.05s)
    - output: `{"high_anxiety": true}`
- [OK] **18.6** _WM threshold boundary_  (0.06s)
    - output: `{"wm": null, "score": 0.0}`
- [OK] **18.7** _substance penalty fires on 2 tokens_  (0.05s)
    - output: `{"confidence": 0.3}`
- [OK] **18.8** _short legit answer NOT floored_  (0.05s)
    - output: `{"confidence": 0.957}`
- [OK] **18.9** _code comment doesn't leak to wrong concept_  (0.03s)
    - output: `{"top": "unknown", "top3": ["unknown"]}`
- [OK] **18.10** _anxiety + L1 → de-escalation_  (0.14s)
    - output: `{"anxiety": true, "intervention": "reduce_challenge"}`
- [OK] **18.11** _stack trace alone_  (0.0s)
    - output: `{"top": "array_index", "conf": 0.783}`
- [OK] **18.12** _essay reply → solid/deep encoding_  (0.07s)
    - output: `{"encoding_strength": "solid", "elaboration": false}`

## Layer 19 — Production-hardening features

- [OK] **19.1** _DBStore upsert+read roundtrip_  (0.02s)
    - output: `{"stored": [0.42, "2026-05-22T02:21:05+00:00"]}`
- [OK] **19.2** _DB handles 10-thread concurrent writes_  (0.09s)
    - output: `{"concurrent_writers": 10, "rows_present": 10}`
- [OK] **19.3** _mastery decay after 28 days (2x half-life)_  (0.04s)
    - output: `{"fresh": 0.957, "after_28d": 0.352, "expected_factor": 0.25}`
- [OK] **19.4** _A/B assignment is sticky per student_  (0.03s)
    - output: `{"calls": ["verbose", "verbose", "verbose"]}`
- [OK] **19.5** _A/B balanced across 200 students_  (0.1s)
    - output: `{"counts": {"control": 103, "verbose": 97}}`
- [OK] **19.6** _GDPR delete wipes all traces + tombstone_  (0.02s)
    - output: `{"delete_counts": {"mastery": 2, "student_state": 1, "variant_assignment": 1, "consent": 1, "audit_log": 1}, "tombstone_rows": 1}`
- [OK] **19.7** _GDPR export contains all fields_  (0.02s)
    - output: `{"export_keys": ["student_id", "mastery", "state", "consent", "variants", "audit", "exported_at"]}`
- [OK] **19.8** _auth token roundtrip_  (0.01s)
    - output: `{"parsed": ["dave", "student", "CSCI1301"]}`
- [OK] **19.9** _auth token rejects tampering_  (0.0s)
    - output: `{"tampered_accepted": false}`
- [OK] **19.10** _auth token rejects expiry_  (0.0s)
    - output: `{"accepted": false}`
- [OK] **19.11** _heatmap + struggle aggregation_  (0.02s)
    - output: `{"n_students": 3, "top_struggle": ["null_pointer", 3, 0.19999999999999998]}`
- [OK] **19.12** _intervention counts aggregation_  (0.02s)
    - output: `{"counts": {"worked_example": 3, "socratic_prompt": 1, "attribution_reframe": 1}}`
- [OK] **19.13** _consent default false + set + revoke_  (0.02s)
    - output: `{"before": false, "after": true, "revoked": false}`
- [OK] **19.14** _audit log preserves insertion order_  (0.02s)
    - output: `{"n": 10, "first": "event_0", "last": "event_9"}`
- [OK] **19.15** _decay after 100 days approaches prior_  (0.08s)
    - output: `{"fresh": 0.99, "after_100d": 0.156, "prior": 0.15}`

## Summary

- **Components loaded:** {'ConceptResolver': True, 'MentalModelsCatalogue': True, 'DINAModel': True, 'StudentStateTracker': True, 'LPDiagnostician': True}
- **Total scenarios:** 176
  - PASS: 121
  - OK: 23
  - DEGRADED: 13
  - FAIL: 2
  - ERROR: 0
  - NOT_RUNNABLE: 17

**Per-layer breakdown:**
- L0: DEGRADED=1, NOT_RUNNABLE=5, OK=2, PASS=19
- L1: DEGRADED=3, PASS=27
- L2: FAIL=2, PASS=7
- L3: DEGRADED=5, PASS=3
- L4: DEGRADED=1, PASS=5
- L5: DEGRADED=1, NOT_RUNNABLE=3, PASS=3
- L6: OK=8
- L7: PASS=6
- L8: DEGRADED=2, NOT_RUNNABLE=2, PASS=4
- L9: PASS=10
- L11: OK=6
- L12: NOT_RUNNABLE=7, PASS=1
- L14: PASS=9
- L15: OK=7
- L18: PASS=12
- L19: PASS=15

## Drawbacks (auto-extracted)
- **L0 0.8** [DEGRADED] empty error, real code: code-only → unknown
- **L1 1.24** [DEGRADED] code-only signal: code-only got unknown
- **L1 1.25** [DEGRADED] free-text weak signal: weak text → assignment_vs_compare
- **L2 2.3** [FAIL] WM string_equality: false WM hit: wm=SE-C score=0.81
- **L2 2.5** [FAIL] WM null_pointer: false WM hit: wm=NP-C score=0.74
- **L3 3.3** [DEGRADED] classify L3: expected L3, got L2
- **L3 3.4** [DEGRADED] classify L4: expected L4, got L3
- **L3 3.5** [DEGRADED] classify L2: expected L2, got L3
- **L3 3.6** [DEGRADED] classify L3: expected L3, got L2
- **L3 3.8** [DEGRADED] regression to L1 from L3: regression-after-L3 still L3
- **L4 4.5** [DEGRADED] plateau cleared by regression: regression missed (got L2)
- **L5 5.1** [DEGRADED] confident answer skips probe: L3 reply got conf=0.38
- **L8 8.1** [DEGRADED] cold-start prior: prior 0.15 not ~0.30
- **L8 8.5** [DEGRADED] across-skill independence: untouched skill drifted to 0.15