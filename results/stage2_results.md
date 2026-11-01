# Stage 2 vs gold

Gold is used here only for checking. A tick means the prediction matches the gold (held set equal; every gold correct misconception found; root cause equal; overall level in the accept list). levels = gold-scored concepts whose level is in the accept list; edges = gold confirmed/broken edges labelled the same.

## default  (10 scenarios)

held 9/10, correct 7/10, root 10/10, overall level 6/10, points 42/72, prompts 114

| scenario | held | correct | root | overall | levels | edges | stop | prompts | points |
|---|---|---|---|---|---|---|---|---|---|
| S001 | yes [] | yes ['PrintEqualsPrintln', 'PrintNewLineFirst'] | yes | yes L1 (gold L1) | 1/2 | 0/1 | sufficient | 7 | 5/7 |
| S007 | yes ['OffByOneBound'] | yes ['PrintEqualsPrintln'] | yes | yes L0 (gold L0) | 2/2 | 1/2 | sufficient | 23 | 7/8 |
| S008 | yes [] | yes ['AssignmentIsEquation', 'OffByOneBound', 'VariableKeepsOldValue'] | yes | yes L2 (gold L2) | 0/4 | 0/0 | half_stop | 14 | 4/8 |
| S021 | yes [] | yes ['BranchChosenByIntent', 'CodeAfterIfSkipped', 'FalseConditionRestartsProgram', 'RemainderIsSubtraction', 'StatementsRunInAnyOrder', 'ThenAlwaysExecutes'] | yes | yes L2 (gold L2) | 0/3 | 0/1 | half_stop | 13 | 4/8 |
| S026 | yes [] | no [] | yes | no None (gold L3) | 0/1 | 0/0 | half_stop | 3 | 2/5 |
| S047 | yes [] | no [] | yes | no None (gold L4) | 0/1 | 0/0 | half_stop | 4 | 2/5 |
| S052 | yes [] | yes ['RedirectionIsArgument'] | yes | yes L2 (gold L2) | 2/3 | 0/4 | half_stop | 12 | 6/11 |
| S057 | yes [] | no ['AllDoublesToAvoidDivision', 'IntegerDivisionGivesFraction', 'IntegerProbability', 'RowsNeedNotSumToOne', 'TargetTyping'] | yes | no L3 (gold L4) | 1/2 | 0/1 | sufficient | 11 | 3/7 |
| S134 | no ['AssignmentIsEquation', 'VariablesHoldExpressions'] | yes [] | yes | yes L0 (gold L0) | 2/2 | 1/1 | half_stop | 10 | 6/7 |
| S137 | yes ['PrintedTextIsExecuted'] | yes [] | yes | no L1 (gold L0) | 0/1 | 0/1 | half_stop | 17 | 3/6 |
