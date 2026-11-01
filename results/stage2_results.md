# Stage 2 vs gold

Gold is used here only for checking. A tick means the prediction matches the gold (held set equal; every gold correct misconception found; root cause equal; overall level in the accept list). levels = gold-scored concepts whose level is in the accept list; edges = gold confirmed/broken edges labelled the same.

## default  (10 scenarios)

held 9/10, correct 8/10, root 10/10, overall level 8/10, points 46/72, prompts 195

| scenario | held | correct | root | overall | levels | edges | stop | prompts | points |
|---|---|---|---|---|---|---|---|---|---|
| S001 | yes [] | yes ['PrintEqualsPrintln', 'PrintNewLineFirst'] | yes | yes L3 (gold L1) | 2/2 | 0/1 | sufficient | 16 | 6/7 |
| S007 | yes ['OffByOneBound'] | yes ['PrintEqualsPrintln'] | yes | yes L0 (gold L0) | 1/2 | 1/2 | sufficient | 32 | 6/8 |
| S008 | yes [] | yes ['AssignmentIsEquation', 'OffByOneBound', 'VariableKeepsOldValue'] | yes | yes L2 (gold L2) | 0/4 | 0/0 | half_stop | 24 | 4/8 |
| S021 | yes [] | yes ['BranchChosenByIntent', 'CodeAfterIfSkipped', 'FalseConditionRestartsProgram', 'RemainderIsSubtraction', 'StatementsRunInAnyOrder', 'ThenAlwaysExecutes'] | yes | yes L2 (gold L2) | 0/3 | 0/1 | half_stop | 22 | 4/8 |
| S026 | yes [] | no [] | yes | yes L1 (gold L3) | 1/1 | 0/0 | sufficient | 7 | 4/5 |
| S047 | yes [] | no [] | yes | yes L4 (gold L4) | 1/1 | 0/0 | sufficient | 7 | 4/5 |
| S052 | yes [] | yes ['RedirectionIsArgument'] | yes | no L3 (gold L2) | 0/3 | 0/4 | half_stop | 22 | 3/11 |
| S057 | yes [] | yes ['CastAfterIntDivision', 'IntegerDivisionGivesFraction', 'IntegerProbability', 'RowsNeedNotSumToOne', 'TargetTyping'] | yes | no L2 (gold L4) | 1/2 | 0/1 | sufficient | 20 | 4/7 |
| S134 | no ['AssignmentIsEquation', 'VariablesHoldExpressions'] | yes [] | yes | yes L0 (gold L0) | 2/2 | 1/1 | sufficient | 17 | 6/7 |
| S137 | yes ['PrintedTextIsExecuted'] | yes [] | yes | yes L0 (gold L0) | 1/1 | 0/1 | half_stop | 28 | 5/6 |
