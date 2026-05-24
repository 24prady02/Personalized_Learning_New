# CPAL scenario harness report

## Layer 0 — Silence / non-response

- [OK] **0.1** _completely empty_  (1.4s)
    - output: `{"resolved": [["unknown", 0.0]], "stage": 1}`
- [OK] **0.2** _whitespace-only_  (0.0s)
    - output: `{"resolved": [["unknown", 0.0]]}`
- [OK] **0.3a** _single token '?'_  (0.06s)
    - output: `{"top": "unknown", "encoding_strength": "partial"}`
- [OK] **0.3b** _single token '😭'_  (0.04s)
    - output: `{"top": "unknown", "encoding_strength": "partial"}`
- [OK] **0.3c** _single token '.'_  (0.04s)
    - output: `{"top": "unknown", "encoding_strength": "partial"}`
- [OK] **0.3d** _single token 'k'_  (0.03s)
    - output: `{"top": "unknown", "encoding_strength": "partial"}`
- [OK] **0.5a** _idk variant 'idk'_  (0.04s)
    - output: `{"confidence": 0.3, "lp": "L1"}`
- [OK] **0.5b** _idk variant "i don't know"_  (0.02s)
    - output: `{"confidence": 0.3, "lp": "L1"}`
- [OK] **0.5c** _idk variant 'no clue'_  (0.02s)
    - output: `{"confidence": 0.3, "lp": "L1"}`
- [OK] **0.5d** _idk variant 'no idea'_  (0.02s)
    - output: `{"confidence": 0.3, "lp": "L1"}`
- [OK] **0.7** _empty code, real error_  (0.0s)
    - output: `{"resolved": [["null_pointer", 0.675]]}`
- [OK] **0.8** _empty error, real code_  (0.0s)
    - output: `{"resolved": [["string_equality", 0.61]]}`
- [ok] **0.9** _code dump no question_  (0.03s)
    - output: `{"encoding_strength": "surface"}`
- [OK] **0.10** _text only no actions_  (0.03s)
    - output: `{"top": "string_equality", "stage": 1}`
- [OK] **0.11** _actions only no text_  (0.0s)
    - output: `{"top": "unknown"}`
- [OK] **0.12a** _filler '...'_  (0.01s)
    - output: `{"top": "unknown"}`
- [OK] **0.12b** _filler 'ok'_  (0.01s)
    - output: `{"top": "unknown"}`
- [OK] **0.12c** _filler 'hmm'_  (0.01s)
    - output: `{"top": "unknown"}`
- [OK] **0.13** _reply is code only_  (0.02s)
    - output: `{"logical_step": false}`
- [OK] **0.14** _refusal_  (0.01s)
    - output: `{"top": "unknown"}`
- [OK] **0.15** _screenshot empty-text fallthrough_  (0.0s)
    - output: `{"note": "same as 0.1"}`
- [ok] **0.20** _disengagement / quit_  (0.03s)
    - output: `{"intervention": "worked_example", "self_efficacy": "neutral", "attribution": "neutral", "high_anxiety": false}`
- [OK] **0.4** _idle session timer_  (0.08s)
    - output: `{"turns": 3, "state_recovered": true}`
- [OK] **0.16** _tab closed mid-probe_  (0.02s)
    - output: `{"fresh_probe_count": 0, "vague_conf": 0.3}`
- [OK] **0.17** _return after long absence_  (0.02s)
    - output: `{"fresh": 0.99, "after_60d": 0.193}`
- [OK] **0.18** _missing API fields_  (0.04s)
    - output: `{"resolved_len": 1, "tracker_keys": ["avg_mastery", "cognitive_graph", "concept", "content_channel", "language_channel"]}`
- [OK] **0.19** _null API fields_  (0.03s)
    - output: `{"resolved_len": 1, "top": "unknown"}`

## Layer 1 — Concept detection

- [OK] **1.1** _detect type_mismatch_  (0.01s)
    - output: `{"top": "type_mismatch", "conf": 0.22, "top3": [["type_mismatch", 0.22]]}`
- [OK] **1.2** _detect infinite_loop_  (0.01s)
    - output: `{"top": "infinite_loop", "conf": 0.512, "top3": [["infinite_loop", 0.512], ["variable_scope", 0.216]]}`
- [OK] **1.3** _detect null_pointer_  (0.01s)
    - output: `{"top": "null_pointer", "conf": 0.141, "top3": [["null_pointer", 0.141]]}`
- [OK] **1.4** _detect string_equality_  (0.01s)
    - output: `{"top": "string_equality", "conf": 0.647, "top3": [["string_equality", 0.647], ["assignment_vs_compare", 0.436], ["boolean_operators", 0.23]]}`
- [OK] **1.5** _detect variable_scope_  (0.0s)
    - output: `{"top": "variable_scope", "conf": 0.675, "top3": [["variable_scope", 0.675]]}`
- [OK] **1.6** _detect assignment_vs_compare_  (0.01s)
    - output: `{"top": "assignment_vs_compare", "conf": 0.512, "top3": [["assignment_vs_compare", 0.512], ["boolean_operators", 0.319], ["string_equality", 0.29]]}`
- [OK] **1.7** _detect integer_division_  (0.01s)
    - output: `{"top": "integer_division", "conf": 0.512, "top3": [["integer_division", 0.512]]}`
- [OK] **1.8** _detect scanner_buffer_  (0.0s)
    - output: `{"top": "scanner_buffer", "conf": 0.61, "top3": [["scanner_buffer", 0.61]]}`
- [OK] **1.9** _detect array_index_  (0.01s)
    - output: `{"top": "array_index", "conf": 0.315, "top3": [["array_index", 0.315]]}`
- [OK] **1.10** _detect missing_return_  (0.0s)
    - output: `{"top": "missing_return", "conf": 0.61, "top3": [["missing_return", 0.61]]}`
- [OK] **1.11** _detect array_not_allocated_  (0.01s)
    - output: `{"top": "array_not_allocated", "conf": 0.287, "top3": [["array_not_allocated", 0.287]]}`
- [OK] **1.12** _detect boolean_operators_  (0.01s)
    - output: `{"top": "boolean_operators", "conf": 0.122, "top3": [["boolean_operators", 0.122]]}`
- [OK] **1.13** _detect sentinel_loop_  (0.0s)
    - output: `{"top": "sentinel_loop", "conf": 0.61, "top3": [["sentinel_loop", 0.61]]}`
- [OK] **1.14** _detect unreachable_code_  (0.01s)
    - output: `{"top": "unreachable_code", "conf": 0.544, "top3": [["unreachable_code", 0.544], ["missing_return", 0.333]]}`
- [OK] **1.15** _detect string_immutability_  (0.0s)
    - output: `{"top": "string_immutability", "conf": 0.675, "top3": [["string_immutability", 0.675]]}`
- [OK] **1.16** _detect no_default_constructor_  (0.01s)
    - output: `{"top": "no_default_constructor", "conf": 0.362, "top3": [["no_default_constructor", 0.362]]}`
- [OK] **1.17** _detect static_vs_instance_  (0.01s)
    - output: `{"top": "static_vs_instance", "conf": 0.238, "top3": [["static_vs_instance", 0.238]]}`
- [OK] **1.18** _detect foreach_no_modify_  (0.01s)
    - output: `{"top": "foreach_no_modify", "conf": 0.512, "top3": [["foreach_no_modify", 0.512]]}`
- [OK] **1.19** _detect overloading_  (0.01s)
    - output: `{"top": "overloading", "conf": 0.207, "top3": [["overloading", 0.207], ["variable_scope", 0.206]]}`
- [OK] **1.20** _detect generics_primitives_  (0.01s)
    - output: `{"top": "generics_primitives", "conf": 0.512, "top3": [["generics_primitives", 0.512], ["array_not_allocated", 0.255]]}`
- [OK] **1.21** _two concepts in one msg_  (0.01s)
    - output: `{"top3": ["infinite_loop", "array_index"]}`
- [OK] **1.22** _three concepts in one msg_  (0.01s)
    - output: `{"top3": ["string_equality", "infinite_loop"]}`
- [OK] **1.23** _error-only signal_  (0.0s)
    - output: `{"top": "type_mismatch"}`
- [OK] **1.24** _code-only signal_  (0.0s)
    - output: `{"top": "string_equality"}`
- [OK] **1.25** _free-text weak signal_  (0.0s)
    - output: `{"top": "string_equality", "conf": 0.61}`
- [OK] **1.26** _typos in concept words (acceptable: infinite_loop or unknown)_  (0.01s)
    - output: `{"top": "unknown"}`
- [OK] **1.27** _off-topic_  (0.01s)
    - output: `{"top": "unknown"}`
- [OK] **1.28** _out-of-catalogue concept_  (0.01s)
    - output: `{"top": "unknown"}`
- [OK] **1.29** _ambiguous concepts_  (0.01s)
    - output: `{"top3": ["string_equality", "assignment_vs_compare", "boolean_operators"]}`
- [OK] **1.30** _non-English (unknown OR infinite_loop both acceptable)_  (0.01s)
    - output: `{"top": "infinite_loop"}`

## Layer 2 — Wrong-model identification (overlap matcher only — no HVSAE)

- [OK] **2.1** _WM null_pointer_  (0.02s)
    - output: `{"wm": "NP-A", "score": 0.927, "lp": "L1", "source": "trained_wm_head"}`
- [OK] **2.2** _WM null_pointer_  (0.02s)
    - output: `{"wm": "NP-B", "score": 0.607, "lp": "L1", "source": "trained_wm_head"}`
- [OK] **2.3** _WM string_equality_  (0.02s)
    - output: `{"wm": "SE-C", "score": 0.808, "lp": "L1", "source": "trained_wm_head"}`
- [OK] **2.4** _WM string_equality_  (0.02s)
    - output: `{"wm": null, "score": 0.0, "lp": "L3", "source": "overlap"}`
- [OK] **2.5** _WM null_pointer_  (0.03s)
    - output: `{"wm": "NP-C", "score": 0.742, "lp": "L1", "source": "trained_wm_head"}`
- [OK] **2.6** _WM string_equality_  (0.07s)
    - output: `{"wm": null, "score": 0.0, "lp": "L2", "source": "overlap"}`
- [OK] **2.7** _WM infinite_loop_  (0.06s)
    - output: `{"wm": "IL-A", "score": 0.653, "lp": "L1", "source": "trained_wm_head"}`
- [OK] **2.8** _WM string_equality_  (0.03s)
    - output: `{"wm": "SE-A", "score": 1.0, "lp": "L2", "source": "overlap"}`
- [OK] **2.9** _WM integer_division_  (0.02s)
    - output: `{"wm": "ID-A", "score": 0.657, "lp": "L1", "source": "trained_wm_head"}`

## Layer 3 — LP-level classification

- [OK] **3.1** _classify L1_  (0.02s)
    - output: `{"lp": "L1", "target": "L2", "logical_step": false, "logical_step_detail": false, "trained_probs": {"L1": 0.9673216342926025, "L2": 0.029903313145041466, "L3": 0.001530802808701992, "L4": 0.0012443044688552618}}`
- [OK] **3.2** _classify L2_  (0.02s)
    - output: `{"lp": "L2", "target": "L3", "logical_step": true, "logical_step_detail": false, "trained_probs": {"L1": 0.5383917689323425, "L2": 0.350394070148468, "L3": 0.07964448630809784, "L4": 0.03156965225934982}}`
- [OK] **3.3** _classify L3_  (0.02s)
    - output: `{"lp": "L3", "target": "L4", "logical_step": true, "logical_step_detail": true, "trained_probs": {"L1": 0.052459508180618286, "L2": 0.23962289094924927, "L3": 0.5106215476989746, "L4": 0.19729608297348022}}`
- [OK] **3.4** _classify L4_  (0.02s)
    - output: `{"lp": "L4", "target": "L4", "logical_step": true, "logical_step_detail": false, "trained_probs": {"L1": 0.008478030562400818, "L2": 0.05677952989935875, "L3": 0.7295397520065308, "L4": 0.20520266890525818}}`
- [OK] **3.5** _classify L2_  (0.02s)
    - output: `{"lp": "L2", "target": "L3", "logical_step": true, "logical_step_detail": true, "trained_probs": {"L1": 0.002504544798284769, "L2": 0.013534673489630222, "L3": 0.9773744344711304, "L4": 0.006586279720067978}}`
- [OK] **3.6** _classify L3_  (0.02s)
    - output: `{"lp": "L3", "target": "L4", "logical_step": true, "logical_step_detail": true, "trained_probs": {"L1": 0.11991895735263824, "L2": 0.39977824687957764, "L3": 0.43630656599998474, "L4": 0.043996214866638184}}`
- [OK] **3.7** _multi-concept differential LP_  (0.03s)
    - output: `{"per_concept_lp": {"null_pointer": "L2"}}`
- [OK] **3.8** _regression to L1 from L3_  (0.02s)
    - output: `{"lp": "L1"}`

## Layer 4 — Plateau / streak

- [OK] **4.1** _first L2_  (0.02s)
    - output: `{"plateau_flag": false, "lp": "L2"}`
- [OK] **4.2** _second L2 → plateau_  (0.02s)
    - output: `{"plateau_flag": true, "intervention": "trace_scaffold"}`
- [OK] **4.4** _plateau cleared by L3 jump_  (0.02s)
    - output: `{"lp": "L3", "plateau_flag": false}`
- [OK] **4.5** _plateau cleared by regression_  (0.02s)
    - output: `{"lp": "L1", "plateau_flag": false}`
- [OK] **4.6** _per-concept plateau independence_  (0.03s)
    - output: `{"np.plateau": true, "se.plateau": false}`
- [OK] **4.7** _very long L2 plateau_  (0.02s)
    - output: `{"plateau_flag": true, "intervention": "trace_scaffold"}`

## Layer 5 — Probe loop confidence branches

- [OK] **5.1** _confident answer skips probe_  (0.02s)
    - output: `{"confidence": 0.65}`
- [OK] **5.2** _vague answer triggers probe_  (0.02s)
    - output: `{"confidence": 0.3}`
- [OK] **5.3** _probe answered well_  (0.02s)
    - output: `{"confidence": 0.75}`
- [OK] **5.4** _probe cap constant_  (41.88s)
    - output: `{"cap": 8}`
- [OK] **5.5** _probe continuity across turns_  (0.21s)
    - output: `{"confs": [0.3, 0.559, 0.65], "monotone_up": true, "final_strong": true}`
- [OK] **5.6** _pick unprobed sub-criterion_  (0.06s)
    - output: `{"target": "L3", "first_two_sub": ["Can trace: new String() allocates a heap object.", "Variable holds a reference (memory address)."], "picked_next": "Variable holds a reference (memory address)."}`
- [OK] **5.7** _credit different-sub-criterion answer_  (0.12s)
    - output: `{"vague_conf": 0.572, "strong_conf": 0.75, "strong_lp": "L3"}`

## Layer 6 — Emotion / behavioral surface signals

- [ok] **6.1** _label=frustrated_  (0.07s)
    - output: `{"expected_label": "frustrated", "attribution": "neutral", "self_efficacy": "neutral", "high_anxiety": true, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`
- [ok] **6.2** _label=confused_  (0.09s)
    - output: `{"expected_label": "confused", "attribution": "neutral", "self_efficacy": "neutral", "high_anxiety": false, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`
- [ok] **6.3** _label=anxious_  (0.07s)
    - output: `{"expected_label": "anxious", "attribution": "neutral", "self_efficacy": "neutral", "high_anxiety": true, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`
- [ok] **6.4** _label=engaged_  (0.09s)
    - output: `{"expected_label": "engaged", "attribution": "neutral", "self_efficacy": "growth", "high_anxiety": false, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`
- [ok] **6.5** _label=neutral_  (0.08s)
    - output: `{"expected_label": "neutral", "attribution": "neutral", "self_efficacy": "neutral", "high_anxiety": false, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`
- [ok] **6.6** _label=frustrated_  (0.08s)
    - output: `{"expected_label": "frustrated", "attribution": "neutral", "self_efficacy": "neutral", "high_anxiety": false, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`
- [ok] **6.7** _label=engaged_  (0.08s)
    - output: `{"expected_label": "engaged", "attribution": "neutral", "self_efficacy": "neutral", "high_anxiety": false, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`
- [ok] **6.8** _label=engaged_  (0.07s)
    - output: `{"expected_label": "engaged", "attribution": "neutral", "self_efficacy": "growth", "high_anxiety": false, "imposter_flag": true, "srl_phase": "unknown", "lang_imposter": false}`

## Layer 7 — Behavioral actions (resolver smoke)

- [OK] **7.1** _trial-and-error_  (0.11s)
    - output: `{"top": "unknown", "stage": 1}`
- [OK] **7.2** _systematic debug_  (0.09s)
    - output: `{"top": "unknown", "stage": 1}`
- [OK] **7.3** _long pause stuck_  (0.12s)
    - output: `{"top": "unknown", "stage": 1}`
- [OK] **7.5** _manic burst_  (0.11s)
    - output: `{"top": "unknown", "stage": 1}`
- [OK] **7.6** _read-only_  (0.12s)
    - output: `{"top": "unknown", "stage": 1}`
- [OK] **7.7** _help-avoidant_  (0.11s)
    - output: `{"top": "unknown", "stage": 1}`

## Layer 8 — DINA mastery

- [OK] **8.1** _cold-start prior (HARD_CONCEPTS-aware)_  (0.0s)
    - output: `{"prior": 0.15}`
- [OK] **8.2** _5x correct climbs_  (0.0s)
    - output: `{"after": 0.99}`
- [OK] **8.3** _slip case_  (0.0s)
    - output: `{"pre": 0.99, "post": 0.9295774647887324}`
- [OK] **8.4** _guess case_  (0.0s)
    - output: `{"before": 0.15, "after": 0.5107913669064748}`
- [OK] **8.5** _across-skill independence (per-skill prior)_  (0.0s)
    - output: `{"untouched": 0.15, "expected_prior": 0.15}`
- [OK] **8.8** _unknown skill key_  (0.0s)
    - output: `{"result": {"skill": "totally_made_up_skill", "mastery": 0.3, "updated": false}}`
- [OK] **8.6** _persistence across restart_  (0.06s)
    - output: `{"pre_np": 0.99, "post_np": 0.99, "pre_se": 0.8319, "post_se": 0.8319}`
- [OK] **8.7** _concurrent updates race_  (0.06s)
    - output: `{"threads": 8, "iters_per_thread": 20, "errors": [], "final_mastery": 0.99}`

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
- [OK] **9.6** _no error keywords_  (0.01s)
    - output: `{"top": "unknown", "conf": 0.0}`
- [OK] **9.7** _mixed lang python_  (0.05s)
    - output: `{"top": "unknown", "conf": 0.0}`
- [OK] **9.8** _pseudocode_  (0.04s)
    - output: `{"top": "unknown", "conf": 0.0}`
- [OK] **9.9** _sql/script text_  (0.04s)
    - output: `{"top": "unknown", "conf": 0.0}`
- [OK] **9.10** _odd unicode_  (0.03s)
    - output: `{"top": "unknown", "conf": 0.0}`

## Layer 11 — Intervention selection

- [ok] **11.1** _L1 should not get challenge_problem_  (0.1s)
    - output: `{"intervention": "worked_example", "imposter_flag": true, "self_efficacy": "neutral", "attribution": "neutral"}`
- [ok] **11.3** _frustrated low mastery_  (0.08s)
    - output: `{"intervention": "reduce_challenge", "imposter_flag": true, "self_efficacy": "neutral", "attribution": "neutral"}`
- [ok] **11.4** _high mastery engaged_  (0.08s)
    - output: `{"intervention": "worked_example", "imposter_flag": true, "self_efficacy": "neutral", "attribution": "neutral"}`
- [ok] **11.5** _wrong-model identified_  (0.08s)
    - output: `{"intervention": "worked_example", "imposter_flag": true, "self_efficacy": "neutral", "attribution": "neutral"}`
- [ok] **11.6** _imposter syndrome_  (0.08s)
    - output: `{"intervention": "attribution_reframe", "imposter_flag": true, "self_efficacy": "neutral", "attribution": "fixed"}`
- [ok] **11.7** _new concept first encounter_  (0.08s)
    - output: `{"intervention": "worked_example", "imposter_flag": true, "self_efficacy": "neutral", "attribution": "neutral"}`

## Layer 12 — RL module

- [OK] **12.8** _RL module importable_  (0.0s)
- [OK] **12.1** _positive learning gain_  (0.0s)
    - output: `{"reward": 0.19}`
- [OK] **12.2** _negative gain_  (0.0s)
    - output: `{"reward_drop": -0.586, "reward_flat": 0.15}`
- [OK] **12.3** _delta_lp positive_  (0.0s)
    - output: `{"reward_delta0": 0.15, "reward_delta1": 0.275}`
- [OK] **12.4** _plateau-broken_  (0.0s)
    - output: `{"reward_no_plateau": 0.391, "reward_plateau_broken": 0.466}`
- [OK] **12.5** _engagement signal_  (0.0s)
    - output: `{"reward_low_eng": 0.086, "reward_high_eng": 0.296}`
- [OK] **12.6** _ZPD reward_  (0.0s)
    - output: `{"reward_in_zpd": 0.24, "reward_overwhelmed": 0.212}`
- [OK] **12.7** _attribution reward_  (0.0s)
    - output: `{"reward_shift": 0.336, "reward_flat": 0.266}`

## Layer 14 — Adversarial / robustness

- [OK] **14.1** _extremely long input_  (0.08s)
    - output: `{"top": "unknown"}`
- [OK] **14.2** _emoji-heavy_  (0.03s)
    - output: `{"top": "unknown"}`
- [OK] **14.3** _prompt-injection_  (0.03s)
    - output: `{"top": "unknown"}`
- [OK] **14.4** _html/sql injection_  (0.03s)
    - output: `{"top": "unknown"}`
- [OK] **14.5** _duplicate submission_  (0.04s)
    - output: `{"top": "unknown"}`
- [OK] **14.8** _massive action_sequence_  (0.02s)
    - output: `{"top": "null_pointer"}`
- [OK] **14.9** _time_deltas length mismatch_  (0.03s)
    - output: `{"top": "null_pointer"}`
- [OK] **14.10** _negative time_stuck_  (0.03s)
    - output: `{"top": "null_pointer"}`
- [OK] **14.11** _NaN time_stuck_  (0.04s)
    - output: `{"top": "null_pointer"}`

## Layer 15 — Three-channel analysis

- [ok] **15.1** _imposter language_  (0.09s)
    - output: `{"expected": "imposter_flag=True", "imposter_flag": true, "attribution": "fixed", "self_efficacy": "neutral", "encoding_strength": "partial", "lang_imposter": true}`
- [ok] **15.2** _external attribution_  (0.08s)
    - output: `{"expected": "attribution=external", "imposter_flag": true, "attribution": "external", "self_efficacy": "neutral", "encoding_strength": "partial", "lang_imposter": false}`
- [ok] **15.3** _internal healthy_  (0.08s)
    - output: `{"expected": "internal, not imposter", "imposter_flag": true, "attribution": "adaptive", "self_efficacy": "neutral", "encoding_strength": "partial", "lang_imposter": false}`
- [ok] **15.4** _internal unhealthy_  (0.08s)
    - output: `{"expected": "internal + imposter", "imposter_flag": true, "attribution": "fixed", "self_efficacy": "neutral", "encoding_strength": "partial", "lang_imposter": false}`
- [ok] **15.5** _high encoding_  (0.07s)
    - output: `{"expected": "encoding=high", "imposter_flag": true, "attribution": "neutral", "self_efficacy": "neutral", "encoding_strength": "partial", "lang_imposter": false}`
- [ok] **15.6** _low encoding_  (0.07s)
    - output: `{"expected": "encoding=low", "imposter_flag": true, "attribution": "neutral", "self_efficacy": "neutral", "encoding_strength": "partial", "lang_imposter": false}`
- [ok] **15.8** _factual question_  (0.08s)
    - output: `{"expected": "neutral psych", "imposter_flag": true, "attribution": "neutral", "self_efficacy": "neutral", "encoding_strength": "partial", "lang_imposter": false}`

## Layer 18 — Added scenarios (post-fix gap coverage)

- [OK] **18.1** _external attribution → reframe gate_  (0.08s)
    - output: `{"attribution": "external", "intervention": "attribution_reframe"}`
- [OK] **18.2** _imposter + external combo_  (0.08s)
    - output: `{"imposter": true, "attribution": "fixed", "intervention": "attribution_reframe"}`
- [OK] **18.3** _self-correction reads as adaptive_  (0.08s)
    - output: `{"attribution": "adaptive", "self_efficacy": "neutral"}`
- [OK] **18.4** _breakthrough → growth_efficacy_  (0.09s)
    - output: `{"self_efficacy": "growth", "attribution": "neutral"}`
- [OK] **18.5** _prolonged grind → high_anxiety_  (0.07s)
    - output: `{"high_anxiety": true}`
- [OK] **18.6** _WM threshold boundary_  (0.16s)
    - output: `{"wm": null, "score": 0.0}`
- [OK] **18.7** _substance penalty fires on 2 tokens_  (0.12s)
    - output: `{"confidence": 0.3}`
- [OK] **18.8** _short legit answer NOT floored_  (0.06s)
    - output: `{"confidence": 0.957}`
- [OK] **18.9** _code comment doesn't leak to wrong concept_  (0.05s)
    - output: `{"top": "unknown", "top3": ["unknown"]}`
- [OK] **18.10** _anxiety + L1 → de-escalation_  (0.07s)
    - output: `{"anxiety": true, "intervention": "reduce_challenge"}`
- [OK] **18.11** _stack trace alone_  (0.0s)
    - output: `{"top": "array_index", "conf": 0.783}`
- [OK] **18.12** _essay reply → solid/deep encoding_  (0.08s)
    - output: `{"encoding_strength": "solid", "elaboration": false}`

## Layer 19 — Production-hardening features

- [OK] **19.1** _DBStore upsert+read roundtrip_  (0.04s)
    - output: `{"stored": [0.42, "2026-05-23T21:31:59+00:00"]}`
- [OK] **19.2** _DB handles 10-thread concurrent writes_  (0.12s)
    - output: `{"concurrent_writers": 10, "rows_present": 10}`
- [OK] **19.3** _mastery decay after 28 days (2x half-life)_  (0.06s)
    - output: `{"fresh": 0.957, "after_28d": 0.352, "expected_factor": 0.25}`
- [OK] **19.4** _A/B assignment is sticky per student_  (0.03s)
    - output: `{"calls": ["verbose", "verbose", "verbose"]}`
- [OK] **19.5** _A/B balanced across 200 students_  (0.12s)
    - output: `{"counts": {"control": 103, "verbose": 97}}`
- [OK] **19.6** _GDPR delete wipes all traces + tombstone_  (0.03s)
    - output: `{"delete_counts": {"mastery": 2, "student_state": 1, "variant_assignment": 1, "consent": 1, "audit_log": 1}, "tombstone_rows": 1}`
- [OK] **19.7** _GDPR export contains all fields_  (0.03s)
    - output: `{"export_keys": ["student_id", "mastery", "state", "consent", "variants", "audit", "exported_at"]}`
- [OK] **19.8** _auth token roundtrip_  (0.04s)
    - output: `{"parsed": ["dave", "student", "CSCI1301"]}`
- [OK] **19.9** _auth token rejects tampering_  (0.0s)
    - output: `{"tampered_accepted": false}`
- [OK] **19.10** _auth token rejects expiry_  (0.0s)
    - output: `{"accepted": false}`
- [OK] **19.11** _heatmap + struggle aggregation_  (0.03s)
    - output: `{"n_students": 3, "top_struggle": ["null_pointer", 3, 0.19999999999999998]}`
- [OK] **19.12** _intervention counts aggregation_  (0.04s)
    - output: `{"counts": {"worked_example": 3, "socratic_prompt": 1, "attribution_reframe": 1}}`
- [OK] **19.13** _consent default false + set + revoke_  (0.03s)
    - output: `{"before": false, "after": true, "revoked": false}`
- [OK] **19.14** _audit log preserves insertion order_  (0.03s)
    - output: `{"n": 10, "first": "event_0", "last": "event_9"}`
- [OK] **19.15** _decay after 100 days approaches prior_  (0.07s)
    - output: `{"fresh": 0.99, "after_100d": 0.156, "prior": 0.15}`

## Layer 20 — Progression reporting

- [OK] **20.1** _progression_for filters by skill + preserves order_  (0.04s)
    - output: `{"n": 5, "arc": ["L1", "L1", "L2", "L2", "L3"]}`
- [OK] **20.2** _mastery_trajectory points roundtrip_  (0.03s)
    - output: `{"n": 5, "first": 0.3, "last": 0.86}`
- [OK] **20.3** _forecast: advancing student_  (0.03s)
    - output: `{"forecast": {"status": "advancing", "turns_recent": 8, "advances": 3, "rate_per_turn": 0.375, "current_lp": "L4", "eta_turns_to_next": 0}}`
- [OK] **20.4** _forecast: plateaued student_  (0.03s)
    - output: `{"forecast": {"status": "plateau", "turns_recent": 8, "advances": 0, "current_lp": "L2", "eta_turns_to_next": null}}`
- [OK] **20.5** _forecast: insufficient data → None_  (0.03s)
    - output: `{"forecast": null}`
- [OK] **20.6** _cohort_percentile basic_  (0.03s)
    - output: `{"percentile": 0.4}`
- [OK] **20.7** _cohort_percentile top student_  (0.03s)
    - output: `{"percentile": 0.8}`
- [OK] **20.8** _trajectory empty for unknown student_  (0.02s)
    - output: `{"trajectory": []}`
- [OK] **20.9** _full simulated 6-turn session flow_  (0.03s)
    - output: `{"n_turns": 6, "mastery_arc": [0.32, 0.5, 0.62, 0.75, 0.78, 0.85], "lp_arc": ["L1", "L2", "L2", "L3", "L3", "L3"], "forecast": {"status": "advancing", "turns_recent": 6, "advances": 2, "rate_per_turn": 0.333, "current_lp": "L3", "eta_turns_to_next": 3}}`
- [OK] **20.10** _intervention captured per-turn AND aggregated_  (0.03s)
    - output: `{"counts": {"worked_example": 3, "socratic_prompt": 1, "attribution_reframe": 1}, "interventions_per_turn": ["worked_example", "worked_example", "socratic_prompt", "attribution_reframe", "worked_example"]}`
- [OK] **20.11** _session_id preserved in turn audit_  (0.03s)
    - output: `{"sessions": ["s1", "s1", "s1", "s2", "s2"]}`
- [OK] **20.12** _dwell_s preserved per turn_  (0.03s)
    - output: `{"dwells": [null, 8.4, 32.1, 60.0, 5.2]}`

## Layer 21 — Behavioral + KG signals per turn

- [OK] **21.1** _reasoning length+complexity per turn_  (0.03s)
    - output: `{"lengths": [3, 47, 220], "complexities": [1.5, 4.2, 7.8]}`
- [OK] **21.2** _correct_streak grows + resets_  (0.02s)
    - output: `{"expected": [1, 2, 3, 0, 1, 2], "got": [1, 2, 3, 0, 1, 2]}`
- [OK] **21.3** _KG concept + counts per turn_  (0.03s)
    - output: `{"row_keys": ["_ts", "cse_prerequisites_count", "cse_related_count", "kg_concept_queried", "lp_after", "lp_before", "mastery_after", "ped_interventions_count", "ped_misconceptions_count", "skill", "three_channel_fired"]}`
- [OK] **21.4** _COKE cognitive_state per turn_  (0.03s)
    - output: `{"states": ["confused", "engaged", "frustrated"]}`
- [OK] **21.5** _KG block sizes per turn_  (0.03s)
    - output: `{"sizes": [1200, 40]}`
- [OK] **21.6** _old + new fields coexist in one turn_  (0.03s)
    - output: `{"n_fields": 24, "sample_keys": ["_ts", "attribution", "coke_cognitive_state", "coke_confidence", "correct_streak", "cse_kg_block_chars", "cse_prerequisites_count", "cse_related_count", "dwell_s", "imposter", "intervention", "kg_concept_queried"]}`

## Layer 22 — Conceptual curiosity

- [ok] **22.1** _conceptual: what actually is null in Java?_  (0.03s)
    - output: `{"top": "null_pointer", "conf": 0.556, "expected_concept": "null_pointer"}`
- [ok] **22.2** _conceptual: why does Java even have null?_  (0.04s)
    - output: `{"top": "null_pointer", "conf": 0.487, "expected_concept": "null_pointer"}`
- [ok] **22.3** _conceptual: how do I check if something is null before using i_  (0.03s)
    - output: `{"top": "null_pointer", "conf": 0.512, "expected_concept": "null_pointer"}`
- [ok] **22.4** _conceptual: why are strings compared differently from numbers?_  (0.03s)
    - output: `{"top": "string_equality", "conf": 0.304, "expected_concept": "string_equality"}`
- [ok] **22.5** _conceptual: what is reference equality vs content equality?_  (0.03s)
    - output: `{"top": "string_equality", "conf": 0.512, "expected_concept": "string_equality"}`
- [ok] **22.6** _conceptual: when should I ever use == with strings?_  (0.03s)
    - output: `{"top": "string_equality", "conf": 0.516, "expected_concept": "string_equality"}`
- [ok] **22.7** _conceptual: how does a while loop know when to stop?_  (0.03s)
    - output: `{"top": "infinite_loop", "conf": 0.56, "expected_concept": "infinite_loop"}`
- [ok] **22.8** _conceptual: what makes a loop infinite?_  (0.03s)
    - output: `{"top": "infinite_loop", "conf": 0.335, "expected_concept": "infinite_loop"}`
- [ok] **22.9** _conceptual: why would anyone ever WANT an infinite loop?_  (0.05s)
    - output: `{"top": "infinite_loop", "conf": 0.512, "expected_concept": "infinite_loop"}`
- [ok] **22.10** _conceptual: why does Java care so much about types?_  (0.03s)
    - output: `{"top": "type_mismatch", "conf": 0.549, "expected_concept": "type_mismatch"}`
- [ok] **22.11** _conceptual: what is type coercion?_  (0.04s)
    - output: `{"top": "overloading", "conf": 0.175, "expected_concept": "type_mismatch"}`
- [ok] **22.12** _conceptual: how does Java decide which type wins in mixed expr_  (0.03s)
    - output: `{"top": "type_mismatch", "conf": 0.369, "expected_concept": "type_mismatch"}`
- [ok] **22.13** _conceptual: what does scope mean in programming?_  (0.03s)
    - output: `{"top": "variable_scope", "conf": 0.065, "expected_concept": "variable_scope"}`
- [ok] **22.14** _conceptual: why can't I use a variable outside its block?_  (0.03s)
    - output: `{"top": "variable_scope", "conf": 0.311, "expected_concept": "variable_scope"}`
- [ok] **22.15** _conceptual: what's the difference between local and global var_  (0.03s)
    - output: `{"top": "variable_scope", "conf": 0.171, "expected_concept": "variable_scope"}`
- [ok] **22.16** _conceptual: why does = mean assignment but == means compare?_  (0.03s)
    - output: `{"top": "string_equality", "conf": 0.631, "expected_concept": "assignment_vs_compare"}`
- [ok] **22.17** _conceptual: what's the difference between = and ==?_  (0.03s)
    - output: `{"top": "string_equality", "conf": 0.708, "expected_concept": "assignment_vs_compare"}`
- [ok] **22.18** _conceptual: why does 7/2 give 3 instead of 3.5?_  (0.03s)
    - output: `{"top": "integer_division", "conf": 0.437, "expected_concept": "integer_division"}`
- [ok] **22.19** _conceptual: how do I do real division in Java?_  (0.03s)
    - output: `{"top": "integer_division", "conf": 0.544, "expected_concept": "integer_division"}`
- [ok] **22.20** _conceptual: what does Scanner actually do under the hood?_  (0.03s)
    - output: `{"top": "scanner_buffer", "conf": 0.512, "expected_concept": "scanner_buffer"}`
- [ok] **22.21** _conceptual: why do I need nextLine after nextInt?_  (0.0s)
    - output: `{"top": "scanner_buffer", "conf": 0.61, "expected_concept": "scanner_buffer"}`
- [ok] **22.22** _conceptual: why do arrays start at 0?_  (0.03s)
    - output: `{"top": "array_index", "conf": 0.327, "expected_concept": "array_index"}`
- [ok] **22.23** _conceptual: what's the relationship between length and index?_  (0.03s)
    - output: `{"top": "array_index", "conf": 0.206, "expected_concept": "array_index"}`
- [ok] **22.24** _conceptual: why does a method have to return something?_  (0.03s)
    - output: `{"top": "missing_return", "conf": 0.33, "expected_concept": "missing_return"}`
- [ok] **22.25** _conceptual: what does void actually mean?_  (0.03s)
    - output: `{"top": "missing_return", "conf": 0.249, "expected_concept": "missing_return"}`
- [ok] **22.26** _conceptual: what's the difference between declaring and creati_  (0.03s)
    - output: `{"top": "array_not_allocated", "conf": 0.506, "expected_concept": "array_not_allocated"}`
- [ok] **22.27** _conceptual: why do I have to say new for arrays?_  (0.02s)
    - output: `{"top": "array_not_allocated", "conf": 0.472, "expected_concept": "array_not_allocated"}`
- [ok] **22.28** _conceptual: what's the difference between & and &&?_  (0.03s)
    - output: `{"top": "boolean_operators", "conf": 0.275, "expected_concept": "boolean_operators"}`
- [ok] **22.29** _conceptual: what does short-circuit evaluation mean?_  (0.02s)
    - output: `{"top": "boolean_operators", "conf": 0.512, "expected_concept": "boolean_operators"}`
- [ok] **22.30** _conceptual: what is a sentinel value?_  (0.03s)
    - output: `{"top": "sentinel_loop", "conf": 0.512, "expected_concept": "sentinel_loop"}`
- [ok] **22.31** _conceptual: when should I use a sentinel vs a counter?_  (0.03s)
    - output: `{"top": "sentinel_loop", "conf": 0.512, "expected_concept": "sentinel_loop"}`
- [ok] **22.32** _conceptual: what does unreachable code mean?_  (0.03s)
    - output: `{"top": "unreachable_code", "conf": 0.623, "expected_concept": "unreachable_code"}`
- [ok] **22.33** _conceptual: why does Java refuse to compile if some code can't_  (0.03s)
    - output: `{"top": "type_mismatch", "conf": 0.214, "expected_concept": "unreachable_code"}`
- [ok] **22.34** _conceptual: what does immutable mean for strings?_  (0.03s)
    - output: `{"top": "string_immutability", "conf": 0.512, "expected_concept": "string_immutability"}`
- [ok] **22.35** _conceptual: why are strings immutable in Java?_  (0.03s)
    - output: `{"top": "string_immutability", "conf": 0.512, "expected_concept": "string_immutability"}`
- [ok] **22.36** _conceptual: what is a constructor?_  (0.03s)
    - output: `{"top": "no_default_constructor", "conf": 0.462, "expected_concept": "no_default_constructor"}`
- [ok] **22.37** _conceptual: when do I need to write my own constructor?_  (0.03s)
    - output: `{"top": "no_default_constructor", "conf": 0.498, "expected_concept": "no_default_constructor"}`
- [ok] **22.38** _conceptual: what does static mean?_  (0.04s)
    - output: `{"top": "static_vs_instance", "conf": 0.56, "expected_concept": "static_vs_instance"}`
- [ok] **22.39** _conceptual: when should I make a method static vs instance?_  (0.03s)
    - output: `{"top": "static_vs_instance", "conf": 0.512, "expected_concept": "static_vs_instance"}`
- [ok] **22.40** _conceptual: why can't I modify a list while iterating it?_  (0.03s)
    - output: `{"top": "foreach_no_modify", "conf": 0.204, "expected_concept": "foreach_no_modify"}`
- [ok] **22.41** _conceptual: what is ConcurrentModificationException?_  (0.04s)
    - output: `{"top": "unknown", "conf": 0.0, "expected_concept": "foreach_no_modify"}`
- [ok] **22.42** _conceptual: what is method overloading?_  (0.0s)
    - output: `{"top": "overloading", "conf": 0.61, "expected_concept": "overloading"}`
- [ok] **22.43** _conceptual: how does Java pick which overload to call?_  (0.03s)
    - output: `{"top": "overloading", "conf": 0.512, "expected_concept": "overloading"}`
- [ok] **22.44** _conceptual: why can't I make an ArrayList of int?_  (0.05s)
    - output: `{"top": "generics_primitives", "conf": 0.462, "expected_concept": "generics_primitives"}`
- [ok] **22.45** _conceptual: what's the difference between int and Integer?_  (0.03s)
    - output: `{"top": "generics_primitives", "conf": 0.626, "expected_concept": "generics_primitives"}`
- [ok] **22.46** _conceptual: what's the difference between a class and an objec_  (0.03s)
    - output: `{"top": "static_vs_instance", "conf": 0.227, "expected_concept": "broad CS1"}`
- [ok] **22.47** _conceptual: what is happening in memory when I call new?_  (0.03s)
    - output: `{"top": "array_not_allocated", "conf": 0.288, "expected_concept": "broad CS1"}`
- [ok] **22.48** _conceptual: why does Java need a main method?_  (0.03s)
    - output: `{"top": "type_mismatch", "conf": 0.153, "expected_concept": "broad CS1"}`
- [ok] **22.49** _conceptual: what does public static void main actually mean?_  (0.02s)
    - output: `{"top": "static_vs_instance", "conf": 0.231, "expected_concept": "broad CS1"}`
- [ok] **22.50** _conceptual: what's the difference between compile time and run_  (0.03s)
    - output: `{"top": "unknown", "conf": 0.0, "expected_concept": "broad CS1"}`

## Layer 23 — Concept comparison

- [OK] **23.1** _compare: Should I use == or .equals when comparing strings?_  (0.0s)
    - output: `{"top3": ["string_equality"], "expected_any_of": ["string_equality", "assignment_vs_compare"]}`
- [OK] **23.2** _compare: When should I use a for loop vs a while loop?_  (0.04s)
    - output: `{"top3": ["infinite_loop"], "expected_any_of": ["infinite_loop", "sentinel_loop"]}`
- [ok] **23.3** _compare: Is there a difference between an array and an Arra_  (0.03s)
    - drawback: no expected concept (['array_index', 'array_not_allocated']) in top3=['generics_primitives']
    - output: `{"top3": ["generics_primitives"], "expected_any_of": ["array_index", "array_not_allocated"]}`
- [OK] **23.4** _compare: When should I use a static method vs an instance m_  (0.0s)
    - output: `{"top3": ["static_vs_instance"], "expected_any_of": ["static_vs_instance", "no_default_constructor"]}`
- [OK] **23.5** _compare: Should I use int[] or Integer[] for storing number_  (0.04s)
    - output: `{"top3": ["generics_primitives"], "expected_any_of": ["generics_primitives", "array_not_allocated"]}`
- [OK] **23.6** _compare: What's the difference between if (x) and if (x == _  (0.03s)
    - output: `{"top3": ["assignment_vs_compare", "string_equality", "boolean_operators"], "expected_any_of": ["assignment_vs_compare", "boolean_operators"]}`
- [OK] **23.7** _compare: Should I use a regular for loop or for-each loop?_  (0.03s)
    - output: `{"top3": ["foreach_no_modify"], "expected_any_of": ["foreach_no_modify"]}`
- [OK] **23.8** _compare: When should I overload a method instead of giving _  (0.05s)
    - output: `{"top3": ["overloading"], "expected_any_of": ["overloading", "no_default_constructor"]}`
- [OK] **23.9** _compare: What's the difference between an empty string and _  (0.03s)
    - output: `{"top3": ["null_pointer", "missing_return"], "expected_any_of": ["null_pointer", "string_immutability"]}`
- [OK] **23.10** _compare: Why does .equals work but == doesn't for strings?_  (0.03s)
    - output: `{"top3": ["string_equality", "assignment_vs_compare"], "expected_any_of": ["string_equality"]}`

## Layer 24 — Academic-dishonesty refusal

- [ok] **24.1** _refusal: just give me the answer to homework 3_  (0.13s)
    - output: `{"top": "unknown", "intervention": "worked_example"}`
- [ok] **24.2** _refusal: write the whole solution for me_  (0.12s)
    - output: `{"top": "unknown", "intervention": "worked_example"}`
- [ok] **24.3** _refusal: what's the answer to quiz 4 question 2?_  (0.1s)
    - output: `{"top": "unknown", "intervention": "worked_example"}`
- [ok] **24.4** _refusal: can you do my project for me?_  (0.11s)
    - output: `{"top": "unknown", "intervention": "worked_example"}`
- [ok] **24.5** _refusal: I don't want to learn, just give me code that work_  (0.11s)
    - output: `{"top": "unknown", "intervention": "worked_example"}`
- [ok] **24.6** _refusal: my friend already got the answer, just tell me wha_  (0.12s)
    - output: `{"top": "unknown", "intervention": "worked_example"}`
- [ok] **24.7** _refusal: skip explaining, just paste the working code_  (0.15s)
    - output: `{"top": "unknown", "intervention": "worked_example"}`
- [ok] **24.8** _refusal: can you write a full Java program that does my ass_  (0.14s)
    - output: `{"top": "assignment_vs_compare", "intervention": "worked_example"}`
- [ok] **24.9** _refusal: the deadline is in 30 mins, just give me something_  (0.09s)
    - output: `{"top": "unknown", "intervention": "worked_example"}`
- [ok] **24.10** _refusal: what would a professor accept for this exact assig_  (0.14s)
    - output: `{"top": "unknown", "intervention": "worked_example"}`

## Layer 25 — Off-topic adjacent + code review

- [ok] **25.1** _off_topic: should I learn Python instead of Java?_  (0.03s)
    - output: `{"kind": "off_topic", "top": "unknown", "conf": 0.0}`
- [ok] **25.2** _off_topic: is Java still relevant for jobs in 2026?_  (0.03s)
    - output: `{"kind": "off_topic", "top": "type_mismatch", "conf": 0.126}`
- [ok] **25.3** _off_topic: how long will it take me to learn Java?_  (0.06s)
    - output: `{"kind": "off_topic", "top": "unknown", "conf": 0.0}`
- [ok] **25.4** _off_topic: I'm thinking of dropping CS1 — what should I do?_  (0.09s)
    - output: `{"kind": "off_topic", "top": "unknown", "conf": 0.0}`
- [ok] **25.5** _off_topic: what should I learn after Java?_  (0.03s)
    - output: `{"kind": "off_topic", "top": "assignment_vs_compare", "conf": 0.068}`
- [ok] **25.6** _code_review: Here's my code. Is it well-written?_  (0.03s)
    - output: `{"kind": "code_review", "top": "unknown", "conf": 0.0}`
- [ok] **25.7** _code_review: Can you suggest improvements to my null check styl_  (0.03s)
    - output: `{"kind": "code_review", "top": "null_pointer", "conf": 0.214}`
- [ok] **25.8** _code_review: Is my variable naming good?_  (0.04s)
    - output: `{"kind": "code_review", "top": "variable_scope", "conf": 0.233}`
- [ok] **25.9** _code_review: Is using a try-catch always the right approach her_  (0.04s)
    - output: `{"kind": "code_review", "top": "unreachable_code", "conf": 0.049}`
- [ok] **25.10** _code_review: What's the more idiomatic Java way to write this?_  (0.03s)
    - output: `{"kind": "code_review", "top": "assignment_vs_compare", "conf": 0.24}`

## Layer 26 — Prior-knowledge transfer

- [OK] **26.1** _prior-knowledge: In Python I could just write 'hello' + 5, why does_  (0.03s)
    - output: `{"top3": ["type_mismatch"], "expected": "type_mismatch"}`
- [OK] **26.2** _prior-knowledge: In Python == works for string comparison, why is J_  (0.04s)
    - output: `{"top3": ["string_equality", "assignment_vs_compare", "type_mismatch"], "expected": "string_equality"}`
- [ok] **26.3** _prior-knowledge: Python lists let me go negative — does arr[-1] wor_  (0.03s)
    - drawback: expected array_index not in top3=['foreach_no_modify']
    - output: `{"top3": ["foreach_no_modify"], "expected": "array_index"}`
- [OK] **26.4** _prior-knowledge: Python 3 made / always return float — why didn't J_  (0.03s)
    - output: `{"top3": ["integer_division"], "expected": "integer_division"}`
- [OK] **26.5** _prior-knowledge: In Python I just call class methods directly — wha_  (0.03s)
    - output: `{"top3": ["static_vs_instance"], "expected": "static_vs_instance"}`
- [OK] **26.6** _prior-knowledge: Python lets me put anything in a list — why does J_  (0.03s)
    - output: `{"top3": ["generics_primitives", "type_mismatch"], "expected": "generics_primitives"}`
- [ok] **26.7** _prior-knowledge: In Python I can change a list while iterating, why_  (0.03s)
    - drawback: expected foreach_no_modify not in top3=['string_immutability']
    - output: `{"top3": ["string_immutability"], "expected": "foreach_no_modify"}`
- [OK] **26.8** _prior-knowledge: JavaScript functions don't require return — why do_  (0.13s)
    - output: `{"top3": ["missing_return", "unreachable_code"], "expected": "missing_return"}`
- [OK] **26.9** _prior-knowledge: In C I just say int arr[10]; why does Java need 'n_  (0.06s)
    - output: `{"top3": ["array_not_allocated", "no_default_constructor"], "expected": "array_not_allocated"}`
- [ok] **26.10** _prior-knowledge: In C I could modify chars in a string, why can't I_  (0.07s)
    - drawback: expected string_immutability not in top3=['type_mismatch']
    - output: `{"top3": ["type_mismatch"], "expected": "string_immutability"}`
- [ok] **26.11** _prior-knowledge: C lets me use 0/1 as booleans — why is Java so str_  (0.03s)
    - drawback: expected boolean_operators not in top3=['integer_division', 'assignment_vs_compare', 'overloading']
    - output: `{"top3": ["integer_division", "assignment_vs_compare", "overloading"], "expected": "boolean_operators"}`
- [OK] **26.12** _prior-knowledge: In Python input() just works — why is Java Scanner_  (0.03s)
    - output: `{"top3": ["scanner_buffer"], "expected": "scanner_buffer"}`
- [OK] **26.13** _prior-knowledge: JavaScript classes work without constructors — why_  (0.03s)
    - output: `{"top3": ["no_default_constructor"], "expected": "no_default_constructor"}`
- [ok] **26.14** _prior-knowledge: In Python a variable defined in if-block is still _  (0.03s)
    - drawback: expected variable_scope not in top3=['missing_return']
    - output: `{"top3": ["missing_return"], "expected": "variable_scope"}`
- [OK] **26.15** _prior-knowledge: Python doesn't have method overloading. How does J_  (0.0s)
    - output: `{"top3": ["overloading"], "expected": "overloading"}`

## Layer 27 — Linguistic edge cases

- [ok] **27.1** _text-speak_  (0.11s)
    - output: `{"kind": "text-speak", "top": "infinite_loop", "conf": 0.19}`
- [ok] **27.2** _all caps frustration_  (0.12s)
    - output: `{"kind": "all caps frustration", "top": "null_pointer", "conf": 0.195}`
- [ok] **27.3** _streaming consciousness_  (0.12s)
    - output: `{"kind": "streaming consciousness", "top": "string_equality", "conf": 0.686}`
- [ok] **27.4** _multiple questions_  (0.11s)
    - output: `{"kind": "multiple questions", "top": "string_equality", "conf": 0.524}`
- [ok] **27.5** _code-mixed (Hinglish)_  (0.08s)
    - output: `{"kind": "code-mixed (Hinglish)", "top": "array_index", "conf": 0.61}`
- [ok] **27.6** _very short_  (0.16s)
    - output: `{"kind": "very short", "top": "infinite_loop", "conf": 0.208}`
- [ok] **27.7** _very long_  (0.13s)
    - output: `{"kind": "very long", "top": "null_pointer", "conf": 0.132}`
- [ok] **27.8** _no punctuation_  (0.12s)
    - output: `{"kind": "no punctuation", "top": "infinite_loop", "conf": 0.512}`
- [ok] **27.9** _with emoji_  (0.12s)
    - output: `{"kind": "with emoji", "top": "null_pointer", "conf": 0.512}`
- [ok] **27.10** _academic tone_  (0.12s)
    - output: `{"kind": "academic tone", "top": "assignment_vs_compare", "conf": 0.452}`

## Summary

- **Components loaded:** {'ConceptResolver': True, 'MentalModelsCatalogue': True, 'DINAModel': True, 'StudentStateTracker': True, 'LPDiagnostician': True}
- **Total scenarios:** 299
  - PASS: 190
  - OK: 109
  - DEGRADED: 0
  - FAIL: 0
  - ERROR: 0
  - NOT_RUNNABLE: 0

**Per-layer breakdown:**
- L0: OK=2, PASS=25
- L1: PASS=30
- L2: PASS=9
- L3: PASS=8
- L4: PASS=6
- L5: PASS=7
- L6: OK=8
- L7: PASS=6
- L8: PASS=8
- L9: PASS=10
- L11: OK=6
- L12: PASS=8
- L14: PASS=9
- L15: OK=7
- L18: PASS=12
- L19: PASS=15
- L20: PASS=12
- L21: PASS=6
- L22: OK=50
- L23: OK=1, PASS=9
- L24: OK=10
- L25: OK=10
- L26: OK=5, PASS=10
- L27: OK=10

## Drawbacks (auto-extracted)