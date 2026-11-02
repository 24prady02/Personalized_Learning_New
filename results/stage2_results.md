# Stage 2 vs gold

Gold is used here only for checking. A tick means the prediction matches the gold (every gold held misconception held and each extra held one resting on the same words as a gold one; every gold correct misconception found; root cause equal; overall level in the accept list). levels = gold-scored concepts whose level is in the accept list; edges = gold confirmed/broken edges labelled the same.

## default  (27 scenarios)

held 27/27, correct 24/27, root 26/27, overall level 25/27, points 148/191, prompts 839

| scenario | held | correct | root | overall | levels | edges | stop | prompts | points |
|---|---|---|---|---|---|---|---|---|---|
| S001 | yes [] | yes ['PrintEqualsPrintln', 'PrintNewLineFirst'] | yes | yes L3 (gold L1) | 2/2 | 0/1 | sufficient | 16 | 6/7 |
| S007 | yes ['OffByOneBound'] | yes ['PrintEqualsPrintln'] | yes | yes L0 (gold L0) | 1/2 | 1/2 | sufficient | 32 | 6/8 |
| S008 | yes [] | yes ['AssignmentIsEquation', 'ForLoopPartSkipped', 'OffByOneBound', 'VariableKeepsOldValue'] | yes | yes L2 (gold L2) | 0/4 | 0/0 | sufficient | 24 | 4/8 |
| S021 | yes [] | yes ['BranchChosenByIntent', 'CodeAfterIfSkipped', 'RemainderIsSubtraction', 'StatementsRunInAnyOrder', 'ThenAlwaysExecutes'] | yes | yes L2 (gold L2) | 0/3 | 0/1 | half_stop | 22 | 4/8 |
| S026 | yes [] | no ['AssignmentExchangesValues'] | yes | yes L1 (gold L3) | 1/1 | 0/0 | sufficient | 7 | 4/5 |
| S047 | yes [] | no [] | yes | yes L4 (gold L4) | 1/1 | 0/0 | half_stop | 7 | 4/5 |
| S052 | yes [] | yes ['RedirectionIsArgument'] | yes | no L3 (gold L2) | 0/3 | 0/4 | half_stop | 22 | 3/11 |
| S057 | yes [] | no ['IntegerDivisionGivesFraction', 'IntegerProbability', 'TargetTyping'] | yes | yes L4 (gold L4) | 1/2 | 0/1 | sufficient | 20 | 4/7 |
| S134 | yes ['VariablesHoldExpressions'] | yes ['AssignmentExchangesValues'] | yes | yes L0 (gold L0) | 2/2 | 0/1 | sufficient | 15 | 6/7 |
| S137 | yes ['PrintedTextIsExecuted'] | yes [] | yes | yes L0 (gold L0) | 1/1 | 0/1 | half_stop | 28 | 5/6 |
| T001 | yes ['ArithmeticPlusPrecedes'] | yes [] | yes | yes L0 (gold L0) | 1/1 | 1/1 | sufficient | 21 | 6/6 |
| T002 | yes ['TargetTyping'] | yes [] | yes | yes L0 (gold L0) | 1/1 | 1/1 | sufficient | 19 | 6/6 |
| T003 | yes ['IfConditionWatched', 'IfWaitsForCondition'] | yes ['CodeAfterIfSkipped'] | yes | yes L0 (gold L0) | 1/1 | 2/2 | sufficient | 24 | 7/7 |
| T004 | yes ['RemainderIsQuotient'] | yes ['IntegerDivisionGivesFraction'] | yes | yes L0 (gold L0) | 2/2 | 1/1 | sufficient | 20 | 7/7 |
| T005 | yes [] | yes ['ForInitRepeats', 'ForIsConditional', 'ForLoopPartSkipped', 'LoopOutputSameEachPass', 'LoopUpdateChangesDirection', 'OffByOneBound', 'RemainderIsQuotient', 'RemainderIsSubtraction'] | yes | yes L2 (gold L2) | 2/3 | 0/2 | sufficient | 36 | 6/9 |
| T006 | yes ['OffByOneBound'] | yes ['ForInitRepeats', 'ForUpdateBeforeBody', 'LoopOutputSameEachPass', 'LoopUpdateChangesDirection'] | yes | yes L0 (gold L0) | 2/2 | 0/0 | sufficient | 34 | 6/6 |
| T007 | yes ['IncrementByTwo'] | yes ['ForIsConditional', 'LoopOutputSameEachPass', 'OffByOneBound', 'RemainderIsQuotient', 'RemainderIsSubtraction'] | yes | yes L0 (gold L0) | 1/2 | 0/2 | max depth | 38 | 5/8 |
| T008 | yes ['BothBranchesExecute', 'IntegerDivisionGivesFraction'] | yes ['CodeAfterIfSkipped'] | yes | yes L0 (gold L0) | 2/2 | 2/2 | max depth | 59 | 8/8 |
| T012 | yes [] | yes ['AllDoublesToAvoidDivision', 'AssignmentIsEquation', 'ForInitRepeats', 'ForUpdateBeforeBody', 'IntegerDivisionGivesFraction', 'LoopOutputSameEachPass', 'LoopUpdateChangesDirection', 'OffByOneBound', 'TargetTyping', 'VariablesHoldExpressions'] | yes | yes L3 (gold L4) | 1/4 | 2/3 | max depth | 41 | 7/11 |
| T013 | yes [] | yes ['ArithmeticInsteadOfBoolean', 'ChainedComparison', 'LessGreaterSwapped', 'NestedIfsInsteadOfLogicalOperators'] | yes | yes L2 (gold L2) | 0/2 | 2/2 | max depth | 36 | 6/8 |
| T014 | yes [] | yes ['ForInitRepeats', 'ForIsConditional', 'LoopBodyStatementOutsideLoop', 'LoopOutputSameEachPass', 'LoopStepAlwaysOne', 'LoopUpdateChangesDirection', 'StateChangeIgnoredAcrossPasses', 'VariableKeepsOldValue'] | yes | yes L2 (gold L2) | 1/2 | 2/2 | max depth | 58 | 7/8 |
| T015 | yes ['AssignmentOppositeDirection'] | yes ['AssignCompares', 'AssignmentEmptiesSource', 'AssignmentExchangesValues'] | yes | yes L0 (gold L0) | 1/1 | 0/0 | sufficient | 36 | 5/5 |
| T016 | yes ['PrintEqualsPrintln'] | yes ['StatementsRunInAnyOrder'] | yes | yes L0 (gold L0) | 1/1 | 1/1 | sufficient | 34 | 6/6 |
| T017 | yes ['RemainderIsSubtraction'] | yes [] | no | yes L0 (gold L0) | 1/1 | 0/0 | sufficient | 28 | 4/5 |
| T018 | yes [] | yes ['AssignmentIsEquation', 'BodyChangeIgnoredByCondition', 'FalseLoopRepeatsNextCode', 'IncrementByTwo', 'InfiniteLoopUnnoticed', 'LessGreaterSwapped', 'LoopOutputSameEachPass', 'LoopTerminatingCondition', 'LoopUpdateChangesDirection', 'ProgramEndsAfterLoop', 'StatementAfterLoopInBody', 'StatementsRunInAnyOrder', 'VariableKeepsOldValue'] | yes | yes L2 (gold L2) | 1/2 | 1/1 | max depth | 76 | 6/7 |
| T019 | yes [] | yes ['AssignmentIsEquation', 'AssignmentOppositeDirection', 'IncrementByTwo', 'PrePostIncrementSameValue', 'VariablesHoldExpressions'] | yes | no L2 (gold L4) | 1/1 | 1/1 | sufficient | 35 | 5/6 |
| T020 | yes [] | yes ['BranchChosenByIntent', 'ThenAlwaysExecutes'] | yes | yes L2 (gold L2) | 0/1 | 1/1 | max depth | 51 | 5/6 |
