# Stage 2 vs gold

Gold is used here only for checking. A tick means the prediction matches the gold (held set equal; every gold correct misconception found; root cause equal; overall level in the accept list). levels = gold-scored concepts whose level is in the accept list; edges = gold confirmed/broken edges labelled the same.

## default  (10 scenarios)

held 9/10, correct 7/10, root 9/10, overall level 5/10, points 37/72, prompts 103

| scenario | held | correct | root | overall | levels | edges | stop | prompts | points |
|---|---|---|---|---|---|---|---|---|---|
| S001 | yes [] | yes ['PrintEqualsPrintln', 'PrintNewLineFirst'] | yes | yes L1 (gold L1) | 1/2 | 0/1 | sufficient | 7 | 5/7 |
| S007 | yes ['OffByOneBound'] | yes ['PrintEqualsPrintln'] | yes | yes L0 (gold L0) | 2/2 | 1/2 | sufficient | 23 | 7/8 |
| S008 | yes [] | yes ['LoopOutputSameEachPass', 'LoopUpdateChangesDirection', 'OffByOneBound'] | yes | yes L2 (gold L2) | 0/4 | 0/0 | half_stop | 14 | 4/8 |
| S021 | yes [] | yes ['BranchChosenByIntent', 'CodeAfterIfSkipped', 'FalseConditionRestartsProgram', 'RemainderIsSubtraction', 'StatementsRunInAnyOrder', 'ThenAlwaysExecutes'] | yes | yes L2 (gold L2) | 0/3 | 0/1 | half_stop | 13 | 4/8 |
| S026 | yes [] | no [] | yes | no None (gold L3) | 0/1 | 0/0 | half_stop | 3 | 2/5 |
| S047 | yes [] | no [] | yes | no None (gold L4) | 0/1 | 0/0 | half_stop | 4 | 2/5 |
| S052 | yes [] | yes ['RedirectionIsArgument'] | yes | yes L2 (gold L2) | 2/3 | 0/4 | half_stop | 12 | 6/11 |
| S057 | yes [] | no ['AllDoublesToAvoidDivision', 'IntegerDivisionGivesFraction', 'IntegerProbability', 'RowsNeedNotSumToOne', 'TargetTyping'] | yes | no L3 (gold L4) | 1/2 | 0/1 | sufficient | 11 | 3/7 |
| S134 | no [] | yes [] | no | no None (gold L0) | 0/2 | 0/1 | half_stop | 3 | 1/7 |
| S137 | yes ['PrintedTextIsExecuted'] | yes [] | yes | no L1 (gold L0) | 0/1 | 0/1 | half_stop | 13 | 3/6 |

## llm_start  (10 scenarios)

held 8/10, correct 7/10, root 10/10, overall level 6/10, points 42/72, prompts 114

| scenario | held | correct | root | overall | levels | edges | stop | prompts | points |
|---|---|---|---|---|---|---|---|---|---|
| S001 | yes [] | yes ['PrintEqualsPrintln', 'PrintNewLineFirst'] | yes | yes L1 (gold L1) | 1/2 | 0/1 | sufficient | 8 | 5/7 |
| S007 | no ['EmptyInnerLoopSkipsRest', 'OffByOneBound'] | yes ['NestedLoopsLockstep', 'NestedLoopsSequential', 'PrintfAddsNewline'] | yes | yes L0 (gold L0) | 2/2 | 1/2 | sufficient | 21 | 6/8 |
| S008 | yes [] | yes ['BothBranchesExecute', 'BranchChosenByIntent', 'ElseAlwaysExecutes', 'IdiomOverridesCode', 'IncrementByTwo', 'LoopOutputSameEachPass', 'LoopUpdateChangesDirection'] | yes | yes L2 (gold L2) | 1/4 | 0/0 | half_stop | 16 | 5/8 |
| S021 | yes [] | yes ['BothBranchesExecute', 'BranchChosenByIntent', 'CodeAfterIfSkipped', 'ElseAlwaysExecutes', 'FalseConditionRestartsProgram', 'StatementsRunInAnyOrder'] | yes | yes L2 (gold L2) | 1/3 | 0/1 | half_stop | 15 | 5/8 |
| S026 | yes [] | no [] | yes | no None (gold L3) | 0/1 | 0/0 | half_stop | 4 | 2/5 |
| S047 | yes [] | no [] | yes | no None (gold L4) | 0/1 | 0/0 | half_stop | 5 | 2/5 |
| S052 | yes [] | yes ['RedirectionIsArgument'] | yes | yes L2 (gold L2) | 2/3 | 0/4 | half_stop | 11 | 6/11 |
| S057 | yes [] | no ['AllDoublesToAvoidDivision', 'IntegerDivisionGivesFraction', 'TargetTyping'] | yes | no L3 (gold L4) | 0/2 | 0/1 | sufficient | 13 | 2/7 |
| S134 | no ['AssignmentIsEquation', 'VariablesHoldExpressions'] | yes [] | yes | yes L0 (gold L0) | 2/2 | 1/1 | half_stop | 11 | 6/7 |
| S137 | yes ['PrintedTextIsExecuted'] | yes [] | yes | no L1 (gold L0) | 0/1 | 0/1 | half_stop | 10 | 3/6 |

## llm_stop  (10 scenarios)

held 9/10, correct 7/10, root 9/10, overall level 5/10, points 37/72, prompts 113

| scenario | held | correct | root | overall | levels | edges | stop | prompts | points |
|---|---|---|---|---|---|---|---|---|---|
| S001 | yes [] | yes ['PrintEqualsPrintln', 'PrintNewLineFirst'] | yes | yes L1 (gold L1) | 1/2 | 0/1 | sufficient | 8 | 5/7 |
| S007 | yes ['OffByOneBound'] | yes ['PrintEqualsPrintln'] | yes | yes L0 (gold L0) | 2/2 | 1/2 | half_stop | 28 | 7/8 |
| S008 | yes [] | yes ['LoopOutputSameEachPass', 'LoopUpdateChangesDirection', 'OffByOneBound'] | yes | yes L2 (gold L2) | 0/4 | 0/0 | half_stop | 15 | 4/8 |
| S021 | yes [] | yes ['BranchChosenByIntent', 'CodeAfterIfSkipped', 'FalseConditionRestartsProgram', 'RemainderIsSubtraction', 'StatementsRunInAnyOrder', 'ThenAlwaysExecutes'] | yes | yes L2 (gold L2) | 0/3 | 0/1 | half_stop | 14 | 4/8 |
| S026 | yes [] | no [] | yes | no None (gold L3) | 0/1 | 0/0 | half_stop | 3 | 2/5 |
| S047 | yes [] | no [] | yes | no None (gold L4) | 0/1 | 0/0 | half_stop | 4 | 2/5 |
| S052 | yes [] | yes ['RedirectionIsArgument'] | yes | yes L2 (gold L2) | 2/3 | 0/4 | half_stop | 13 | 6/11 |
| S057 | yes [] | no ['AllDoublesToAvoidDivision', 'IntegerDivisionGivesFraction', 'IntegerProbability', 'RowsNeedNotSumToOne', 'TargetTyping'] | yes | no L3 (gold L4) | 1/2 | 0/1 | half_stop | 12 | 3/7 |
| S134 | no [] | yes [] | no | no None (gold L0) | 0/2 | 0/1 | half_stop | 3 | 1/7 |
| S137 | yes ['PrintedTextIsExecuted'] | yes [] | yes | no L1 (gold L0) | 0/1 | 0/1 | half_stop | 13 | 3/6 |

## llm_ablation  (10 scenarios)

held 8/10, correct 7/10, root 10/10, overall level 6/10, points 42/72, prompts 126

| scenario | held | correct | root | overall | levels | edges | stop | prompts | points |
|---|---|---|---|---|---|---|---|---|---|
| S001 | yes [] | yes ['PrintEqualsPrintln', 'PrintNewLineFirst'] | yes | yes L1 (gold L1) | 1/2 | 0/1 | sufficient | 9 | 5/7 |
| S007 | no ['EmptyInnerLoopSkipsRest', 'OffByOneBound'] | yes ['NestedLoopsLockstep', 'NestedLoopsSequential', 'PrintfAddsNewline'] | yes | yes L0 (gold L0) | 2/2 | 1/2 | half_stop | 26 | 6/8 |
| S008 | yes [] | yes ['BothBranchesExecute', 'BranchChosenByIntent', 'ElseAlwaysExecutes', 'IdiomOverridesCode', 'IncrementByTwo', 'LoopOutputSameEachPass', 'LoopUpdateChangesDirection'] | yes | yes L2 (gold L2) | 1/4 | 0/0 | half_stop | 17 | 5/8 |
| S021 | yes [] | yes ['BothBranchesExecute', 'BranchChosenByIntent', 'CodeAfterIfSkipped', 'ElseAlwaysExecutes', 'FalseConditionRestartsProgram', 'StatementsRunInAnyOrder'] | yes | yes L2 (gold L2) | 1/3 | 0/1 | half_stop | 16 | 5/8 |
| S026 | yes [] | no [] | yes | no None (gold L3) | 0/1 | 0/0 | half_stop | 4 | 2/5 |
| S047 | yes [] | no [] | yes | no None (gold L4) | 0/1 | 0/0 | half_stop | 5 | 2/5 |
| S052 | yes [] | yes ['RedirectionIsArgument'] | yes | yes L2 (gold L2) | 2/3 | 0/4 | half_stop | 12 | 6/11 |
| S057 | yes [] | no ['AllDoublesToAvoidDivision', 'IntegerDivisionGivesFraction', 'TargetTyping'] | yes | no L3 (gold L4) | 0/2 | 0/1 | half_stop | 14 | 2/7 |
| S134 | no ['AssignmentIsEquation', 'VariablesHoldExpressions'] | yes [] | yes | yes L0 (gold L0) | 2/2 | 1/1 | half_stop | 13 | 6/7 |
| S137 | yes ['PrintedTextIsExecuted'] | yes [] | yes | no L1 (gold L0) | 0/1 | 0/1 | half_stop | 10 | 3/6 |
