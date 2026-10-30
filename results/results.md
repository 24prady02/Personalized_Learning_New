# Results: code-only subgraph for each scenario

Stage 1 reads only the scenario's code. Every concept node below was found by a regex stored on that concept node of the knowledge graph; the subgraph is then the knowledge graph's edges between those concepts, their misconception and error nodes and edges, and their level nodes L0..L4 with the has_level edges. Figures: `figures/<sid>.png`.


## Summary

| scenario | concept nodes | concept edges | misconception edges | misconception nodes | level nodes | pieces | edges traced | misconception nodes |
|---|---|---|---|---|---|---|---|---|
| S000 | 4 | 2 | 18 | 17 | 20 | 2 | `pre:declaration->definite_assignment`, `pre:statement->println` | `AnyValueInAnyVariable`, `ComputerFillsInIntent`, `DeclarationWithoutType`, `DeclaredVariableHasNoMemory`, `IdentifierCaseInsensitive`, `LocalVariablesAutoInitialized`, `ParenthesesOnlyIfArgument`, `PrintEqualsPrintln`, `PrintNewLineFirst`, `PrintWithoutFinalNewline`, `PrintedTextIsExecuted`, `ProgramLooksAhead`, `RedeclareToReassign`, `StatementNeedsNoTerminator`, `StatementsRunInAnyOrder`, `UndeclaredOrRenamedVariable`, `WhitespaceIsSignificant` |
| S001 | 4 | 5 | 18 | 15 | 20 | 1 | `par:print~println`, `pre:statement->print`, `pre:statement->println`, `pre:string_literal->print`, `pre:string_literal->println` | `ComputerFillsInIntent`, `IdentifierCaseInsensitive`, `ParenthesesOnlyIfArgument`, `PrintEqualsPrintln`, `PrintNewLineFirst`, `PrintWithoutFinalNewline`, `PrintedTextIsExecuted`, `ProgramLooksAhead`, `RepeatedOutputVariablePrintedOnce`, `SingleQuotedString`, `StatementNeedsNoTerminator`, `StatementsRunInAnyOrder`, `StringLiteralSpansLines`, `UnclosedStringLiteral`, `WhitespaceIsSignificant` |
| S007 | 17 | 14 | 141 | 104 | 85 | 3 | `par:assignment~comparison_operators`, `par:println~formatted_output`, `pre:assignment->increment_operators`, `pre:comparison_operators->boolean_expression`, `pre:expression->comparison_operators`, `pre:for_loop->loop_scope`, `pre:for_loop->nested_loops`, `pre:loop_control->for_loop`, `pre:loop_control->increment_operators`, `pre:loop_variable->loop_control`, `pre:standard_output->formatted_output`, `pre:statement->control_flow`, `pre:statement->println`, `pre:string_literal->println` | `AccumulatorDeclaredInLoop`, `ArithmeticInsteadOfBoolean`, `AssignCompares`, `AssignToFinal`, `AssignmentAddsToTarget`, `AssignmentCopiesObject`, `AssignmentEmptiesSource`, `AssignmentExchangesValues`, `AssignmentIsEquation`, `AssignmentNotExpression`, `AssignmentOppositeDirection`, `BodyChangeIgnoredByCondition`, `BracelessMultiStatementBody`, `ChainedComparison`, `CodeAfterIfSkipped`, `ComparisonWithBooleanLiteral`, `ComputerFillsInIntent`, `DoubleLoopIndexCount`, `ElseWithCondition`, `EmptyInnerLoopSkipsRest`, `EqualityOperatorComparesObjectsValues`, `EqualsComparesReferences`, `ExpressionOnLeftOfAssignment`, `FalseConditionRestartsProgram`, `FalseLoopRepeatsNextCode`, `FieldWidthIsIntegerDigits`, `ForCommaSeparators`, `ForInitRepeats`, `ForIsConditional`, `ForLoopPartSkipped`, `ForUpdateBeforeBody`, `ForVariableScopeBeyondLoop`, `ForWhileNotInterchangeable`, `IdentifierCaseInsensitive`, `IdiomOverridesCode`, `IfConditionWatched`, `IfInLoopUnchecked`, `IfWaitsForCondition`, `InconsistentIndentation`, `IncrementByTwo`, `InfiniteLoopUnnoticed`, `InnerCounterOverwritesOuter`, `InnerOuterSwapped`, `LessGreaterSwapped`, `LocalVarOutsideScope`, `LoopBodyAlwaysOnce`, `LoopBodyScopeImpliesLoopLifetime`, `LoopBodyStatementOutsideLoop`, `LoopCountIsStatementCount`, `LoopForOneTimeTest`, `LoopHeaderIsEquations`, `LoopImpliedByOneTest`, `LoopOutputSameEachPass`, `LoopRunsStatementsSeparately`, `LoopStepAlwaysOne`, `LoopUpdateChangesDirection`, `LoopVariableLifetimeScope`, `LoopVariableLimitsValues`, `ManyDigitsMeanAccurate`, `MapToBooleanWithConditionalOperator`, `MapToBooleanWithIf`, `MissingBraces`, `NestedIfsInsteadOfLogicalOperators`, `NestedLoopsLockstep`, `NestedLoopsSequential`, `NoAtomicExpression`, `NoShortCircuit`, `OffByOneBound`, `OuterLoopIgnored`, `OutsideInMethodNesting`, `ParenthesesOnlyIfArgument`, `PostIncrementAssignsLater`, `PreIncrementBeforeLoop`, `PrePostIncrementSameValue`, `PrintEqualsPrintln`, `PrintNewLineFirst`, `PrintWithoutFinalNewline`, `PrintedTextIsExecuted`, `PrintfAddsNewline`, `PrintfAnyConversion`, `ProgramEndsAfterLoop`, `ProgramLooksAhead`, `RedeclareToReassign`, `RepeatedOutputVariablePrintedOnce`, `ReturnDoesNotExitLoop`, `ReversedRelationalOperator`, `SemicolonAfterIfHeader`, `SemicolonAfterLoopHeader`, `SingleIterationInsteadOfLoop`, `SingleQuotedString`, `StateChangeIgnoredAcrossPasses`, `StatementAfterLoopInBody`, `StatementNeedsNoTerminator`, `StatementsRunInAnyOrder`, `StringLiteralSpansLines`, `StringRelationalComparison`, `SwapWithoutTemp`, `TargetTyping`, `UnclosedStringLiteral`, `VariableKeepsOldValue`, `VariablesHoldExpressions`, `WhileStopsMidBody`, `WhitespaceIsSignificant`, `WrongIterationCount` |
| S008 | 19 | 16 | 141 | 108 | 95 | 4 | `par:assignment~comparison_operators`, `par:comparison_operators~logical_operators`, `pre:arithmetic_operators->expression`, `pre:assignment->increment_operators`, `pre:boolean_expression->if_statement`, `pre:comparison_operators->boolean_expression`, `pre:control_flow->if_statement`, `pre:expression->comparison_operators`, `pre:expression->operator_precedence`, `pre:if_statement->if_else_statement`, `pre:logical_operators->boolean_expression`, `pre:logical_operators->short_circuit`, `pre:loop_control->increment_operators`, `pre:loop_variable->loop_control`, `pre:standard_output->formatted_output`, `pre:statement->control_flow` | `ArithmeticInsteadOfBoolean`, `ArithmeticOnNumericStrings`, `ArithmeticPlusPrecedes`, `AssignCompares`, `AssignToFinal`, `AssignmentAddsToTarget`, `AssignmentCopiesObject`, `AssignmentEmptiesSource`, `AssignmentExchangesValues`, `AssignmentIsEquation`, `AssignmentNotExpression`, `AssignmentOppositeDirection`, `BodyChangeIgnoredByCondition`, `BooleanPrecedence`, `BothBranchesExecute`, `BracelessMultiStatementBody`, `BranchChosenByIntent`, `CaretIsPower`, `CastAppliesToWholeExpression`, `ChainedComparison`, `CodeAfterIfSkipped`, `ComparisonWithBooleanLiteral`, `ComputerFillsInIntent`, `ConditionalIsSequence`, `CurlyIfCondition`, `DoWhileTestsFirst`, `DoubleLoopIndexCount`, `DuplicateCodeInBranches`, `ElseAlwaysExecutes`, `ElseWithCondition`, `EqualityOperatorComparesObjectsValues`, `EqualsComparesReferences`, `ExpressionOnLeftOfAssignment`, `FalseConditionEndsProgram`, `FalseConditionRestartsProgram`, `FalseLoopRepeatsNextCode`, `FieldWidthIsIntegerDigits`, `ForInitRepeats`, `ForLoopPartSkipped`, `ForUpdateBeforeBody`, `IdiomOverridesCode`, `IfConditionCheckedInHindsight`, `IfConditionWatched`, `IfInLoopUnchecked`, `IfIsLoop`, `IfRequiresElse`, `IfWaitsForCondition`, `IncrementByTwo`, `InfiniteLoopUnnoticed`, `LessGreaterSwapped`, `LoopBodyAlwaysOnce`, `LoopBodyStatementOutsideLoop`, `LoopCountIsStatementCount`, `LoopForOneTimeTest`, `LoopHeaderIsEquations`, `LoopImpliedByOneTest`, `LoopOutputSameEachPass`, `LoopRunsStatementsSeparately`, `LoopStepAlwaysOne`, `LoopUpdateChangesDirection`, `LoopVariableLifetimeScope`, `LoopVariableLimitsValues`, `ManyDigitsMeanAccurate`, `MapToBooleanWithConditionalOperator`, `MapToBooleanWithIf`, `MissingBraces`, `MissingClarifyingParentheses`, `NestedIfsInsteadOfLogicalOperators`, `NextStatementIsElse`, `NoAtomicExpression`, `NoShortCircuit`, `NoSingleLogicAnd`, `OffByOneBound`, `OutsideInMethodNesting`, `ParenthesesOnlyIfArgument`, `PostIncrementAssignsLater`, `PreIncrementBeforeLoop`, `PrePostIncrementSameValue`, `PrintEqualsPrintln`, `PrintedTextIsExecuted`, `PrintfAddsNewline`, `PrintfAnyConversion`, `ProgramEndsAfterLoop`, `ProgramLooksAhead`, `RedeclareToReassign`, `RemainderIsSubtraction`, `RepeatedOutputVariablePrintedOnce`, `ReturnDoesNotExitLoop`, `ReversedRelationalOperator`, `SemicolonAfterIfHeader`, `SequentialIfsAreNested`, `SingleAmpersandForAnd`, `StateChangeIgnoredAcrossPasses`, `StatementAfterIfInBranch`, `StatementAfterLoopInBody`, `StatementNeedsNoTerminator`, `StatementsRunInAnyOrder`, `StringPlusLeftToRight`, `StringRelationalComparison`, `SwapWithoutTemp`, `TargetTyping`, `ThenAlwaysExecutes`, `VariableKeepsOldValue`, `VariablesHoldExpressions`, `WhileStopsMidBody`, `WhitespaceIsSignificant`, `WrongIterationCount`, `WrongOperatorOrder` |
| S021 | 12 | 10 | 87 | 69 | 60 | 2 | `pre:arithmetic_operators->expression`, `pre:boolean_expression->if_statement`, `pre:comparison_operators->boolean_expression`, `pre:control_flow->if_statement`, `pre:expression->comparison_operators`, `pre:if_else_statement->nested_conditionals`, `pre:if_statement->if_else_statement`, `pre:statement->control_flow`, `pre:statement->print`, `pre:string_literal->print` | `ArithmeticInsteadOfBoolean`, `ArithmeticOnNumericStrings`, `AssignCompares`, `AssignmentIsEquation`, `AssignmentNotExpression`, `BothBranchesExecute`, `BracelessMultiStatementBody`, `BranchChosenByIntent`, `CaretIsPower`, `ChainedComparison`, `CodeAfterIfSkipped`, `ComparisonWithBooleanLiteral`, `ComputerFillsInIntent`, `ConditionalIsSequence`, `CurlyIfCondition`, `DuplicateCodeInBranches`, `ElseAlwaysExecutes`, `ElseMatchesIndentation`, `ElseWithCondition`, `EqualityOperatorComparesObjectsValues`, `EqualsComparesReferences`, `ExpressionOnLeftOfAssignment`, `FalseConditionEndsProgram`, `FalseConditionRestartsProgram`, `FalseLoopRepeatsNextCode`, `IfConditionCheckedInHindsight`, `IfConditionWatched`, `IfInLoopUnchecked`, `IfIsLoop`, `IfRequiresElse`, `IfWaitsForCondition`, `InconsistentIndentation`, `InnerIfIgnoresOuter`, `LessGreaterSwapped`, `LoopForOneTimeTest`, `LoopImpliedByOneTest`, `MapToBooleanWithConditionalOperator`, `MapToBooleanWithIf`, `MissingBraces`, `MultipleElseIfBranchesRun`, `NegativeRemainderSign`, `NestedIfsInsteadOfLogicalOperators`, `NextStatementIsElse`, `NoAtomicExpression`, `NoShortCircuit`, `OutsideInMethodNesting`, `ParenthesesOnlyIfArgument`, `PrintWithoutFinalNewline`, `PrintedTextIsExecuted`, `ProgramEndsAfterLoop`, `ProgramLooksAhead`, `RemainderIsQuotient`, `RemainderIsSubtraction`, `RepeatedOutputVariablePrintedOnce`, `ReturnDoesNotExitLoop`, `ReversedRelationalOperator`, `SemicolonAfterIfHeader`, `SequentialIfsAreNested`, `SingleQuotedString`, `StatementAfterIfInBranch`, `StatementNeedsNoTerminator`, `StatementsRunInAnyOrder`, `StringLiteralSpansLines`, `StringRelationalComparison`, `TargetTyping`, `ThenAlwaysExecutes`, `UnclosedStringLiteral`, `VariablesHoldExpressions`, `WhitespaceIsSignificant` |
| S026 | 2 | 1 | 17 | 15 | 10 | 1 | `pre:assignment->variable_swap` | `AssignCompares`, `AssignToFinal`, `AssignmentAddsToTarget`, `AssignmentCopiesObject`, `AssignmentEmptiesSource`, `AssignmentExchangesValues`, `AssignmentIsEquation`, `AssignmentNotExpression`, `AssignmentOppositeDirection`, `ExpressionOnLeftOfAssignment`, `PrintedTextIsExecuted`, `RedeclareToReassign`, `SwapWithoutTemp`, `VariableKeepsOldValue`, `VariablesHoldExpressions` |
| S047 | 2 | 1 | 7 | 6 | 10 | 1 | `pre:standard_output->formatted_output` | `FieldWidthIsIntegerDigits`, `ManyDigitsMeanAccurate`, `PrintEqualsPrintln`, `PrintfAddsNewline`, `PrintfAnyConversion`, `RepeatedOutputVariablePrintedOnce` |
| S052 | 8 | 7 | 17 | 16 | 40 | 2 | `par:standard_input~command_line_args`, `par:standard_input~standard_output`, `pre:command_line_args->black_box_model`, `pre:redirection->data_driven_code`, `pre:redirection->piping`, `pre:standard_input->redirection`, `pre:standard_output->redirection` | `ArgsAlwaysPresent`, `ArgsAreNumbers`, `AudioProgramHangs`, `CompileRunsProgram`, `FirstArgIsArgsOne`, `InputReadOnceBeforeLoop`, `InputTypeMismatch`, `NextLineAfterNextInt`, `PrintEqualsPrintln`, `PrintfAddsNewline`, `ReadPastEndOfInput`, `RedirectionIsArgument`, `RepeatedOutputVariablePrintedOnce`, `RereadIntoVariableInvalid`, `StdInRereads`, `StdLibraryNotInDirectory` |
| S057 | 26 | 22 | 167 | 120 | 130 | 4 | `par:assignment~comparison_operators`, `pre:arithmetic_operators->expression`, `pre:arithmetic_operators->integer_division`, `pre:array_creation->array_default_values`, `pre:array_creation->array_initializer`, `pre:array_creation->indexing`, `pre:array_declaration->array_creation`, `pre:assignment->increment_operators`, `pre:comparison_operators->boolean_expression`, `pre:data_type->data_structure`, `pre:data_type->primitive_type`, `pre:expression->comparison_operators`, `pre:for_loop->array_traversal`, `pre:for_loop->loop_scope`, `pre:indexing->array_traversal`, `pre:integer_division->normalization`, `pre:loop_control->for_loop`, `pre:loop_control->increment_operators`, `pre:loop_variable->loop_control`, `pre:primitive_type->type_conversion`, `pre:statement->control_flow`, `pre:type_conversion->widening_conversion` | `AccumulatorDeclaredInLoop`, `AllDoublesToAvoidDivision`, `AnyValueInAnyVariable`, `ArithmeticInsteadOfBoolean`, `ArithmeticOnNumericStrings`, `ArrayAccessWithParentheses`, `ArrayAllocationWithoutNew`, `ArrayBracketCountIsLength`, `ArrayCreationIsFree`, `ArrayElementNotVariable`, `ArrayElementsUntyped`, `ArrayIndexStartsAtOne`, `ArrayInitializerContentsInBrackets`, `ArrayLengthCannotBeZero`, `ArrayListIsArray`, `ArrayRangeInclusive`, `ArrayUseScansAllCells`, `ArraysGrow`, `AssignCompares`, `AssignToFinal`, `AssignmentAddsToTarget`, `AssignmentCopiesObject`, `AssignmentEmptiesSource`, `AssignmentExchangesValues`, `AssignmentIsEquation`, `AssignmentNotExpression`, `AssignmentOppositeDirection`, `BodyChangeIgnoredByCondition`, `BracelessMultiStatementBody`, `CaretIsPower`, `CastAfterIntDivision`, `ChainedComparison`, `CodeAfterIfSkipped`, `ComparisonWithBooleanLiteral`, `ComputerFillsInIntent`, `DeclarationCreatesArray`, `DoubleLoopIndexCount`, `EarlyReturnInLoop`, `ElementBoundToOldIndex`, `ElementNameIsWholeArray`, `ElseWithCondition`, `EqualityOperatorComparesObjectsValues`, `EqualsComparesReferences`, `ExpressionOnLeftOfAssignment`, `FalseConditionRestartsProgram`, `FalseLoopRepeatsNextCode`, `ForCommaSeparators`, `ForInitRepeats`, `ForIsConditional`, `ForLoopPartSkipped`, `ForUpdateBeforeBody`, `ForVariableScopeBeyondLoop`, `ForWhileNotInterchangeable`, `IdiomOverridesCode`, `IfConditionWatched`, `IfInLoopUnchecked`, `IfWaitsForCondition`, `IncrementByTwo`, `IndexIsValue`, `InfiniteLoopUnnoticed`, `IntegerDivisionGivesFraction`, `IntegerProbability`, `LaterDoubleLiteralFixesDivision`, `LessGreaterSwapped`, `LocalVarOutsideScope`, `LoopBodyAlwaysOnce`, `LoopBodyScopeImpliesLoopLifetime`, `LoopBodyStatementOutsideLoop`, `LoopCountIsStatementCount`, `LoopForOneTimeTest`, `LoopHeaderIsEquations`, `LoopImpliedByOneTest`, `LoopOutputSameEachPass`, `LoopRunsStatementsSeparately`, `LoopStepAlwaysOne`, `LoopUpdateChangesDirection`, `LoopVariableLifetimeScope`, `LoopVariableLimitsValues`, `MapToBooleanWithConditionalOperator`, `MapToBooleanWithIf`, `MissingBraces`, `NarrowingAssignmentAllowed`, `NegativeArraySize`, `NegativeRemainderSign`, `NestedIfsInsteadOfLogicalOperators`, `NewArrayHoldsGarbage`, `NoAtomicExpression`, `NoCastIfSameSize`, `NoShortCircuit`, `OffByOneBound`, `OutsideInMethodNesting`, `ParenthesesOnlyIfArgument`, `PostIncrementAssignsLater`, `PreIncrementBeforeLoop`, `PrePostIncrementSameValue`, `PrintedTextIsExecuted`, `ProgramEndsAfterLoop`, `ProgramLooksAhead`, `RedeclareToReassign`, `RemainderIsSubtraction`, `ReturnDoesNotExitLoop`, `ReversedRelationalOperator`, `RowsNeedNotSumToOne`, `SemicolonAfterIfHeader`, `SemicolonAfterLoopHeader`, `SingleIterationInsteadOfLoop`, `StateChangeIgnoredAcrossPasses`, `StatementAfterLoopInBody`, `StatementNeedsNoTerminator`, `StatementsRunInAnyOrder`, `StringIsPrimitive`, `StringRelationalComparison`, `SwapWithoutTemp`, `TargetTyping`, `VariableKeepsOldValue`, `VariablesHoldExpressions`, `WhileStopsMidBody`, `WhitespaceIsSignificant`, `WholeArrayArithmetic`, `WrongIterationCount` |
| S134 | 2 | 1 | 17 | 15 | 10 | 1 | `pre:assignment->variable_swap` | `AssignCompares`, `AssignToFinal`, `AssignmentAddsToTarget`, `AssignmentCopiesObject`, `AssignmentEmptiesSource`, `AssignmentExchangesValues`, `AssignmentIsEquation`, `AssignmentNotExpression`, `AssignmentOppositeDirection`, `ExpressionOnLeftOfAssignment`, `PrintedTextIsExecuted`, `RedeclareToReassign`, `SwapWithoutTemp`, `VariableKeepsOldValue`, `VariablesHoldExpressions` |
| S137 | 4 | 5 | 18 | 15 | 20 | 1 | `par:print~println`, `pre:statement->print`, `pre:statement->println`, `pre:string_literal->print`, `pre:string_literal->println` | `ComputerFillsInIntent`, `IdentifierCaseInsensitive`, `ParenthesesOnlyIfArgument`, `PrintEqualsPrintln`, `PrintNewLineFirst`, `PrintWithoutFinalNewline`, `PrintedTextIsExecuted`, `ProgramLooksAhead`, `RepeatedOutputVariablePrintedOnce`, `SingleQuotedString`, `StatementNeedsNoTerminator`, `StatementsRunInAnyOrder`, `StringLiteralSpansLines`, `UnclosedStringLiteral`, `WhitespaceIsSignificant` |

## S000

```java
int count;
System.out.println(count);
```

![S000](figures/S000.png)

**Concept nodes (4)**: `declaration` (generic), `definite_assignment`, `println`, `statement` (generic)


**Concept edges traced (2)**

| edge | logic |
|---|---|
| `pre:declaration->definite_assignment` | A declared local variable has no defined value until it is assigned, and the compiler rejects any read before that assignment. |
| `pre:statement->println` | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |

**Misconception and error nodes (17) via 18 edges**: `AnyValueInAnyVariable`, `ComputerFillsInIntent`, `DeclarationWithoutType`, `DeclaredVariableHasNoMemory`, `IdentifierCaseInsensitive`, `LocalVariablesAutoInitialized`, `ParenthesesOnlyIfArgument`, `PrintEqualsPrintln`, `PrintNewLineFirst`, `PrintWithoutFinalNewline`, `PrintedTextIsExecuted`, `ProgramLooksAhead`, `RedeclareToReassign`, `StatementNeedsNoTerminator`, `StatementsRunInAnyOrder`, `UndeclaredOrRenamedVariable`, `WhitespaceIsSignificant`

**Level nodes**: 20 (L0..L4 for each concept), **has_level edges**: 20, **level→misconception links**: 20, **connected pieces**: 2

Notes: concept nodes form 2 pieces (the KG has no edge between them): declaration,definite_assignment | println,statement


## S001

```java
System.out.print("Welcome to Java. This is ");
System.out.println("A nice programming language ");
System.out.print("that I have to learn.");
```

![S001](figures/S001.png)

**Concept nodes (4)**: `print`, `println`, `statement` (generic), `string_literal` (generic)


**Concept edges traced (5)**

| edge | logic |
|---|---|
| `par:print~println` | print leaves the cursor on the same line after printing; println moves the cursor to the next line after printing. |
| `pre:statement->print` | System.out.print(s); is itself a statement, so it runs at its own place in the sequence of statements. |
| `pre:statement->println` | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |
| `pre:string_literal->print` | print("s") outputs exactly the characters between the quotes, without the quotes. |
| `pre:string_literal->println` | println("s") outputs exactly the characters between the quotes and then ends the line. |

**Misconception and error nodes (15) via 18 edges**: `ComputerFillsInIntent`, `IdentifierCaseInsensitive`, `ParenthesesOnlyIfArgument`, `PrintEqualsPrintln`, `PrintNewLineFirst`, `PrintWithoutFinalNewline`, `PrintedTextIsExecuted`, `ProgramLooksAhead`, `RepeatedOutputVariablePrintedOnce`, `SingleQuotedString`, `StatementNeedsNoTerminator`, `StatementsRunInAnyOrder`, `StringLiteralSpansLines`, `UnclosedStringLiteral`, `WhitespaceIsSignificant`

**Level nodes**: 20 (L0..L4 for each concept), **has_level edges**: 20, **level→misconception links**: 16, **connected pieces**: 1


## S007

```java
for (int i = 3; i >= 0; i--) {
  for (int j = i; j > 0; j--) {
    System.out.printf("%d ", j);
  }
  System.out.println();
}
```

![S007](figures/S007.png)

**Concept nodes (17)**: `assignment` (generic), `boolean_expression`, `comparison_operators`, `control_flow`, `expression` (generic), `for_loop`, `formatted_output`, `increment_operators`, `loop_body`, `loop_control`, `loop_scope`, `loop_variable`, `nested_loops`, `println`, `standard_output` (generic), `statement` (generic), `string_literal` (generic)


**Concept edges traced (14)**

| edge | logic |
|---|---|
| `par:assignment~comparison_operators` | x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands. |
| `par:println~formatted_output` | println prints each number with all its digits and ends the line; printf formats each value by its conversion code and starts a new line only when \n is in the format string. |
| `pre:assignment->increment_operators` | i++ is shorthand for the assignment i = i + 1. |
| `pre:comparison_operators->boolean_expression` | A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making. |
| `pre:expression->comparison_operators` | Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b. |
| `pre:for_loop->loop_scope` | A variable declared in the for header exists only from its declaration to the end of the for statement's block. |
| `pre:for_loop->nested_loops` | In nested loops the inner for runs its complete set of passes for every single pass of the outer for. |
| `pre:loop_control->for_loop` | The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |
| `pre:loop_control->increment_operators` | The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update. |
| `pre:loop_variable->loop_control` | The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |
| `pre:standard_output->formatted_output` | printf writes to standard output, like print, but formats each value first. |
| `pre:statement->control_flow` | Control flow is the order in which statements run. |
| `pre:statement->println` | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |
| `pre:string_literal->println` | println("s") outputs exactly the characters between the quotes and then ends the line. |

**Misconception and error nodes (104) via 141 edges**: `AccumulatorDeclaredInLoop`, `ArithmeticInsteadOfBoolean`, `AssignCompares`, `AssignToFinal`, `AssignmentAddsToTarget`, `AssignmentCopiesObject`, `AssignmentEmptiesSource`, `AssignmentExchangesValues`, `AssignmentIsEquation`, `AssignmentNotExpression`, `AssignmentOppositeDirection`, `BodyChangeIgnoredByCondition`, `BracelessMultiStatementBody`, `ChainedComparison`, `CodeAfterIfSkipped`, `ComparisonWithBooleanLiteral`, `ComputerFillsInIntent`, `DoubleLoopIndexCount`, `ElseWithCondition`, `EmptyInnerLoopSkipsRest`, `EqualityOperatorComparesObjectsValues`, `EqualsComparesReferences`, `ExpressionOnLeftOfAssignment`, `FalseConditionRestartsProgram`, `FalseLoopRepeatsNextCode`, `FieldWidthIsIntegerDigits`, `ForCommaSeparators`, `ForInitRepeats`, `ForIsConditional`, `ForLoopPartSkipped`, `ForUpdateBeforeBody`, `ForVariableScopeBeyondLoop`, `ForWhileNotInterchangeable`, `IdentifierCaseInsensitive`, `IdiomOverridesCode`, `IfConditionWatched`, `IfInLoopUnchecked`, `IfWaitsForCondition`, `InconsistentIndentation`, `IncrementByTwo`, `InfiniteLoopUnnoticed`, `InnerCounterOverwritesOuter`, `InnerOuterSwapped`, `LessGreaterSwapped`, `LocalVarOutsideScope`, `LoopBodyAlwaysOnce`, `LoopBodyScopeImpliesLoopLifetime`, `LoopBodyStatementOutsideLoop`, `LoopCountIsStatementCount`, `LoopForOneTimeTest`, `LoopHeaderIsEquations`, `LoopImpliedByOneTest`, `LoopOutputSameEachPass`, `LoopRunsStatementsSeparately`, `LoopStepAlwaysOne`, `LoopUpdateChangesDirection`, `LoopVariableLifetimeScope`, `LoopVariableLimitsValues`, `ManyDigitsMeanAccurate`, `MapToBooleanWithConditionalOperator`, `MapToBooleanWithIf`, `MissingBraces`, `NestedIfsInsteadOfLogicalOperators`, `NestedLoopsLockstep`, `NestedLoopsSequential`, `NoAtomicExpression`, `NoShortCircuit`, `OffByOneBound`, `OuterLoopIgnored`, `OutsideInMethodNesting`, `ParenthesesOnlyIfArgument`, `PostIncrementAssignsLater`, `PreIncrementBeforeLoop`, `PrePostIncrementSameValue`, `PrintEqualsPrintln`, `PrintNewLineFirst`, `PrintWithoutFinalNewline`, `PrintedTextIsExecuted`, `PrintfAddsNewline`, `PrintfAnyConversion`, `ProgramEndsAfterLoop`, `ProgramLooksAhead`, `RedeclareToReassign`, `RepeatedOutputVariablePrintedOnce`, `ReturnDoesNotExitLoop`, `ReversedRelationalOperator`, `SemicolonAfterIfHeader`, `SemicolonAfterLoopHeader`, `SingleIterationInsteadOfLoop`, `SingleQuotedString`, `StateChangeIgnoredAcrossPasses`, `StatementAfterLoopInBody`, `StatementNeedsNoTerminator`, `StatementsRunInAnyOrder`, `StringLiteralSpansLines`, `StringRelationalComparison`, `SwapWithoutTemp`, `TargetTyping`, `UnclosedStringLiteral`, `VariableKeepsOldValue`, `VariablesHoldExpressions`, `WhileStopsMidBody`, `WhitespaceIsSignificant`, `WrongIterationCount`

**Level nodes**: 85 (L0..L4 for each concept), **has_level edges**: 85, **level→misconception links**: 145, **connected pieces**: 3

Notes: concept nodes form 3 pieces (the KG has no edge between them): assignment,boolean_expression,comparison_operators,expression,for_loop,increment_operators,loop_control,loop_scope,loop_variable,nested_loops | control_flow,formatted_output,println,standard_output,statement,string_literal | loop_body


## S008

```java
int num = 8, num1 = num + 1, num2 = num1 + 3;
int i = num;
do {
  if (i != num1 && i != num2) {
    System.out.printf("%d, ", i);
  } else {
    num2--;
  }
  i++;
} while (i < 14);
```

![S008](figures/S008.png)

**Concept nodes (19)**: `arithmetic_operators`, `assignment` (generic), `boolean_expression`, `comparison_operators`, `control_flow`, `do_while_loop`, `expression` (generic), `formatted_output`, `if_else_statement`, `if_statement`, `increment_operators`, `logical_operators`, `loop_body`, `loop_control`, `loop_variable`, `operator_precedence`, `short_circuit`, `standard_output` (generic), `statement` (generic)


**Concept edges traced (16)**

| edge | logic |
|---|---|
| `par:assignment~comparison_operators` | x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands. |
| `par:comparison_operators~logical_operators` | Relational operators compare two numbers to give a boolean; logical operators combine booleans into one boolean. |
| `pre:arithmetic_operators->expression` | An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones. |
| `pre:assignment->increment_operators` | i++ is shorthand for the assignment i = i + 1. |
| `pre:boolean_expression->if_statement` | An if runs its block only when its boolean expression evaluates to true. |
| `pre:comparison_operators->boolean_expression` | A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making. |
| `pre:control_flow->if_statement` | An if changes the default top-to-bottom flow by running a block only when its condition is true. |
| `pre:expression->comparison_operators` | Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b. |
| `pre:expression->operator_precedence` | When an expression has several operators, precedence decides which operands are combined first, and equal-precedence operators go left to right. |
| `pre:if_statement->if_else_statement` | if-else extends if with a second block that runs exactly when the condition is false. |
| `pre:logical_operators->boolean_expression` | &&, // and ! combine conditions p and q into one larger condition that is still true or false. |
| `pre:logical_operators->short_circuit` | && and // evaluate their second operand only when the first has not already decided the result (false && x is false, true // x is true). |
| `pre:loop_control->increment_operators` | The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update. |
| `pre:loop_variable->loop_control` | The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |
| `pre:standard_output->formatted_output` | printf writes to standard output, like print, but formats each value first. |
| `pre:statement->control_flow` | Control flow is the order in which statements run. |

**Misconception and error nodes (108) via 141 edges**: `ArithmeticInsteadOfBoolean`, `ArithmeticOnNumericStrings`, `ArithmeticPlusPrecedes`, `AssignCompares`, `AssignToFinal`, `AssignmentAddsToTarget`, `AssignmentCopiesObject`, `AssignmentEmptiesSource`, `AssignmentExchangesValues`, `AssignmentIsEquation`, `AssignmentNotExpression`, `AssignmentOppositeDirection`, `BodyChangeIgnoredByCondition`, `BooleanPrecedence`, `BothBranchesExecute`, `BracelessMultiStatementBody`, `BranchChosenByIntent`, `CaretIsPower`, `CastAppliesToWholeExpression`, `ChainedComparison`, `CodeAfterIfSkipped`, `ComparisonWithBooleanLiteral`, `ComputerFillsInIntent`, `ConditionalIsSequence`, `CurlyIfCondition`, `DoWhileTestsFirst`, `DoubleLoopIndexCount`, `DuplicateCodeInBranches`, `ElseAlwaysExecutes`, `ElseWithCondition`, `EqualityOperatorComparesObjectsValues`, `EqualsComparesReferences`, `ExpressionOnLeftOfAssignment`, `FalseConditionEndsProgram`, `FalseConditionRestartsProgram`, `FalseLoopRepeatsNextCode`, `FieldWidthIsIntegerDigits`, `ForInitRepeats`, `ForLoopPartSkipped`, `ForUpdateBeforeBody`, `IdiomOverridesCode`, `IfConditionCheckedInHindsight`, `IfConditionWatched`, `IfInLoopUnchecked`, `IfIsLoop`, `IfRequiresElse`, `IfWaitsForCondition`, `IncrementByTwo`, `InfiniteLoopUnnoticed`, `LessGreaterSwapped`, `LoopBodyAlwaysOnce`, `LoopBodyStatementOutsideLoop`, `LoopCountIsStatementCount`, `LoopForOneTimeTest`, `LoopHeaderIsEquations`, `LoopImpliedByOneTest`, `LoopOutputSameEachPass`, `LoopRunsStatementsSeparately`, `LoopStepAlwaysOne`, `LoopUpdateChangesDirection`, `LoopVariableLifetimeScope`, `LoopVariableLimitsValues`, `ManyDigitsMeanAccurate`, `MapToBooleanWithConditionalOperator`, `MapToBooleanWithIf`, `MissingBraces`, `MissingClarifyingParentheses`, `NestedIfsInsteadOfLogicalOperators`, `NextStatementIsElse`, `NoAtomicExpression`, `NoShortCircuit`, `NoSingleLogicAnd`, `OffByOneBound`, `OutsideInMethodNesting`, `ParenthesesOnlyIfArgument`, `PostIncrementAssignsLater`, `PreIncrementBeforeLoop`, `PrePostIncrementSameValue`, `PrintEqualsPrintln`, `PrintedTextIsExecuted`, `PrintfAddsNewline`, `PrintfAnyConversion`, `ProgramEndsAfterLoop`, `ProgramLooksAhead`, `RedeclareToReassign`, `RemainderIsSubtraction`, `RepeatedOutputVariablePrintedOnce`, `ReturnDoesNotExitLoop`, `ReversedRelationalOperator`, `SemicolonAfterIfHeader`, `SequentialIfsAreNested`, `SingleAmpersandForAnd`, `StateChangeIgnoredAcrossPasses`, `StatementAfterIfInBranch`, `StatementAfterLoopInBody`, `StatementNeedsNoTerminator`, `StatementsRunInAnyOrder`, `StringPlusLeftToRight`, `StringRelationalComparison`, `SwapWithoutTemp`, `TargetTyping`, `ThenAlwaysExecutes`, `VariableKeepsOldValue`, `VariablesHoldExpressions`, `WhileStopsMidBody`, `WhitespaceIsSignificant`, `WrongIterationCount`, `WrongOperatorOrder`

**Level nodes**: 95 (L0..L4 for each concept), **has_level edges**: 95, **level→misconception links**: 161, **connected pieces**: 4

Notes: concept nodes form 4 pieces (the KG has no edge between them): arithmetic_operators,assignment,boolean_expression,comparison_operators,control_flow,expression,if_else_statement,if_statement,increment_operators,logical_operators,loop_control,loop_variable,operator_precedence,short_circuit,statement | do_while_loop | formatted_output,standard_output | loop_body


## S021

```java
System.out.print("A");
if (x % 2 == 0) {
  System.out.print("B");
  if (x % 5 == 2) { System.out.print("C"); } else { System.out.print("D"); }
} else {
  if (x % 5 == 2) { System.out.print("E"); } else { System.out.print("F"); }
  System.out.print("G");
}
```

![S021](figures/S021.png)

**Concept nodes (12)**: `arithmetic_operators`, `boolean_expression`, `comparison_operators`, `control_flow`, `expression` (generic), `if_else_statement`, `if_statement`, `nested_conditionals`, `print`, `remainder_operator`, `statement` (generic), `string_literal` (generic)


**Concept edges traced (10)**

| edge | logic |
|---|---|
| `pre:arithmetic_operators->expression` | An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones. |
| `pre:boolean_expression->if_statement` | An if runs its block only when its boolean expression evaluates to true. |
| `pre:comparison_operators->boolean_expression` | A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making. |
| `pre:control_flow->if_statement` | An if changes the default top-to-bottom flow by running a block only when its condition is true. |
| `pre:expression->comparison_operators` | Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b. |
| `pre:if_else_statement->nested_conditionals` | Nesting puts an if or if-else inside a branch of another if-else; an else-if chain is the common case where the else branch is itself an if. |
| `pre:if_statement->if_else_statement` | if-else extends if with a second block that runs exactly when the condition is false. |
| `pre:statement->control_flow` | Control flow is the order in which statements run. |
| `pre:statement->print` | System.out.print(s); is itself a statement, so it runs at its own place in the sequence of statements. |
| `pre:string_literal->print` | print("s") outputs exactly the characters between the quotes, without the quotes. |

**Misconception and error nodes (69) via 87 edges**: `ArithmeticInsteadOfBoolean`, `ArithmeticOnNumericStrings`, `AssignCompares`, `AssignmentIsEquation`, `AssignmentNotExpression`, `BothBranchesExecute`, `BracelessMultiStatementBody`, `BranchChosenByIntent`, `CaretIsPower`, `ChainedComparison`, `CodeAfterIfSkipped`, `ComparisonWithBooleanLiteral`, `ComputerFillsInIntent`, `ConditionalIsSequence`, `CurlyIfCondition`, `DuplicateCodeInBranches`, `ElseAlwaysExecutes`, `ElseMatchesIndentation`, `ElseWithCondition`, `EqualityOperatorComparesObjectsValues`, `EqualsComparesReferences`, `ExpressionOnLeftOfAssignment`, `FalseConditionEndsProgram`, `FalseConditionRestartsProgram`, `FalseLoopRepeatsNextCode`, `IfConditionCheckedInHindsight`, `IfConditionWatched`, `IfInLoopUnchecked`, `IfIsLoop`, `IfRequiresElse`, `IfWaitsForCondition`, `InconsistentIndentation`, `InnerIfIgnoresOuter`, `LessGreaterSwapped`, `LoopForOneTimeTest`, `LoopImpliedByOneTest`, `MapToBooleanWithConditionalOperator`, `MapToBooleanWithIf`, `MissingBraces`, `MultipleElseIfBranchesRun`, `NegativeRemainderSign`, `NestedIfsInsteadOfLogicalOperators`, `NextStatementIsElse`, `NoAtomicExpression`, `NoShortCircuit`, `OutsideInMethodNesting`, `ParenthesesOnlyIfArgument`, `PrintWithoutFinalNewline`, `PrintedTextIsExecuted`, `ProgramEndsAfterLoop`, `ProgramLooksAhead`, `RemainderIsQuotient`, `RemainderIsSubtraction`, `RepeatedOutputVariablePrintedOnce`, `ReturnDoesNotExitLoop`, `ReversedRelationalOperator`, `SemicolonAfterIfHeader`, `SequentialIfsAreNested`, `SingleQuotedString`, `StatementAfterIfInBranch`, `StatementNeedsNoTerminator`, `StatementsRunInAnyOrder`, `StringLiteralSpansLines`, `StringRelationalComparison`, `TargetTyping`, `ThenAlwaysExecutes`, `UnclosedStringLiteral`, `VariablesHoldExpressions`, `WhitespaceIsSignificant`

**Level nodes**: 60 (L0..L4 for each concept), **has_level edges**: 60, **level→misconception links**: 91, **connected pieces**: 2

Notes: concept nodes form 2 pieces (the KG has no edge between them): arithmetic_operators,boolean_expression,comparison_operators,control_flow,expression,if_else_statement,if_statement,nested_conditionals,print,statement,string_literal | remainder_operator


## S026

```java
int t = a;
a = b;
b = t;
```

![S026](figures/S026.png)

**Concept nodes (2)**: `assignment` (generic), `variable_swap`


**Concept edges traced (1)**

| edge | logic |
|---|---|
| `pre:assignment->variable_swap` | The three assignments int t = a; a = b; b = t; exchange the values of a and b, as a trace of the variable values after each statement shows. |

**Misconception and error nodes (15) via 17 edges**: `AssignCompares`, `AssignToFinal`, `AssignmentAddsToTarget`, `AssignmentCopiesObject`, `AssignmentEmptiesSource`, `AssignmentExchangesValues`, `AssignmentIsEquation`, `AssignmentNotExpression`, `AssignmentOppositeDirection`, `ExpressionOnLeftOfAssignment`, `PrintedTextIsExecuted`, `RedeclareToReassign`, `SwapWithoutTemp`, `VariableKeepsOldValue`, `VariablesHoldExpressions`

**Level nodes**: 10 (L0..L4 for each concept), **has_level edges**: 10, **level→misconception links**: 17, **connected pieces**: 1


## S047

```java
double price = 3.14159;
System.out.printf("%6.2f", price);
System.out.printf("|%d items%n", 4);
```

![S047](figures/S047.png)

**Concept nodes (2)**: `formatted_output`, `standard_output` (generic)


**Concept edges traced (1)**

| edge | logic |
|---|---|
| `pre:standard_output->formatted_output` | printf writes to standard output, like print, but formats each value first. |

**Misconception and error nodes (6) via 7 edges**: `FieldWidthIsIntegerDigits`, `ManyDigitsMeanAccurate`, `PrintEqualsPrintln`, `PrintfAddsNewline`, `PrintfAnyConversion`, `RepeatedOutputVariablePrintedOnce`

**Level nodes**: 10 (L0..L4 for each concept), **has_level edges**: 10, **level→misconception links**: 11, **connected pieces**: 1


## S052

```java
% java RandomSeq 5 > data.txt
% java Average < data.txt
% java RandomSeq 5 | java Average
(RandomSeq N prints N random numbers; Average reads numbers from standard input and prints their average)
```

![S052](figures/S052.png)

**Concept nodes (8)**: `black_box_model`, `command_line_args`, `data_driven_code`, `piping`, `redirection`, `run`, `standard_input`, `standard_output` (generic)


**Concept edges traced (7)**

| edge | logic |
|---|---|
| `par:standard_input~command_line_args` | Command-line arguments are a fixed number of strings given once when the program starts (args[]); standard input is a stream of any length read while the program runs (StdIn.readInt()). Both arrive as text and must be parsed into numbers. |
| `par:standard_input~standard_output` | StdIn takes values in from the input stream; StdOut sends values out to the output stream. |
| `pre:command_line_args->black_box_model` | The black-box view treats the command-line argument as the input string and what the program prints as the output string. |
| `pre:redirection->data_driven_code` | Redirecting a file to standard input lets the same program process different data files without being changed. |
| `pre:redirection->piping` | A pipe A / B connects A's standard output directly to B's standard input, with no file in between. |
| `pre:standard_input->redirection` | < file makes the contents of the file the standard input stream. |
| `pre:standard_output->redirection` | > file sends everything written to standard output into the file instead of the screen. |

**Misconception and error nodes (16) via 17 edges**: `ArgsAlwaysPresent`, `ArgsAreNumbers`, `AudioProgramHangs`, `CompileRunsProgram`, `FirstArgIsArgsOne`, `InputReadOnceBeforeLoop`, `InputTypeMismatch`, `NextLineAfterNextInt`, `PrintEqualsPrintln`, `PrintfAddsNewline`, `ReadPastEndOfInput`, `RedirectionIsArgument`, `RepeatedOutputVariablePrintedOnce`, `RereadIntoVariableInvalid`, `StdInRereads`, `StdLibraryNotInDirectory`

**Level nodes**: 40 (L0..L4 for each concept), **has_level edges**: 40, **level→misconception links**: 23, **connected pieces**: 2

Notes: concept nodes form 2 pieces (the KG has no edge between them): black_box_model,command_line_args,data_driven_code,piping,redirection,standard_input,standard_output | run


## S057

```java
int[] counts = {0, 0, 2, 2, 1};
int outDegree = 5;
double[] p = new double[5];
for (int j = 0; j < 5; j++) {
  p[j] = counts[j] / outDegree;
}
```

![S057](figures/S057.png)

**Concept nodes (26)**: `arithmetic_operators`, `array_creation`, `array_declaration`, `array_default_values`, `array_initializer`, `array_traversal`, `assignment` (generic), `boolean_expression`, `comparison_operators`, `control_flow`, `data_structure`, `data_type` (generic), `expression` (generic), `for_loop`, `increment_operators`, `indexing`, `integer_division`, `loop_body`, `loop_control`, `loop_scope`, `loop_variable`, `normalization`, `primitive_type` (generic), `statement` (generic), `type_conversion`, `widening_conversion`


**Concept edges traced (22)**

| edge | logic |
|---|---|
| `par:assignment~comparison_operators` | x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands. |
| `pre:arithmetic_operators->expression` | An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones. |
| `pre:arithmetic_operators->integer_division` | For ints a and b, / gives the whole quotient q and % gives the remainder r, so that a = b * q + r. |
| `pre:array_creation->array_default_values` | new fills every slot with the type's default value: 0, 0.0, false or null. |
| `pre:array_creation->array_initializer` | {v0, v1, ..., vk} is a shorthand that creates an array of length k + 1 and fills it in one step. |
| `pre:array_creation->indexing` | An array must be created with new before any of its elements a[i] can be accessed. |
| `pre:array_declaration->array_creation` | double[] a; declares the array name and type; a = new double[N]; then creates the array. |
| `pre:assignment->increment_operators` | i++ is shorthand for the assignment i = i + 1. |
| `pre:comparison_operators->boolean_expression` | A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making. |
| `pre:data_type->data_structure` | A data structure organizes many values of a data type; the array holds a sequence of values of one type. |
| `pre:data_type->primitive_type` | Java has eight primitive data types (boolean, char, byte, short, int, long, float, double); each, like any data type, is a set of values and a set of operations on those values. |
| `pre:expression->comparison_operators` | Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b. |
| `pre:for_loop->array_traversal` | for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order. |
| `pre:for_loop->loop_scope` | A variable declared in the for header exists only from its declaration to the end of the for statement's block. |
| `pre:indexing->array_traversal` | A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass. |
| `pre:integer_division->normalization` | Normalising must divide as doubles, because with two ints counts / total truncates to 0 whenever counts < total. |
| `pre:loop_control->for_loop` | The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |
| `pre:loop_control->increment_operators` | The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update. |
| `pre:loop_variable->loop_control` | The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |
| `pre:primitive_type->type_conversion` | Conversion moves a value between primitive types: int to double happens automatically, while double to int needs a cast that drops the fraction. |
| `pre:statement->control_flow` | Control flow is the order in which statements run. |
| `pre:type_conversion->widening_conversion` | Widening is the automatic kind of type conversion. |

**Misconception and error nodes (120) via 167 edges**: `AccumulatorDeclaredInLoop`, `AllDoublesToAvoidDivision`, `AnyValueInAnyVariable`, `ArithmeticInsteadOfBoolean`, `ArithmeticOnNumericStrings`, `ArrayAccessWithParentheses`, `ArrayAllocationWithoutNew`, `ArrayBracketCountIsLength`, `ArrayCreationIsFree`, `ArrayElementNotVariable`, `ArrayElementsUntyped`, `ArrayIndexStartsAtOne`, `ArrayInitializerContentsInBrackets`, `ArrayLengthCannotBeZero`, `ArrayListIsArray`, `ArrayRangeInclusive`, `ArrayUseScansAllCells`, `ArraysGrow`, `AssignCompares`, `AssignToFinal`, `AssignmentAddsToTarget`, `AssignmentCopiesObject`, `AssignmentEmptiesSource`, `AssignmentExchangesValues`, `AssignmentIsEquation`, `AssignmentNotExpression`, `AssignmentOppositeDirection`, `BodyChangeIgnoredByCondition`, `BracelessMultiStatementBody`, `CaretIsPower`, `CastAfterIntDivision`, `ChainedComparison`, `CodeAfterIfSkipped`, `ComparisonWithBooleanLiteral`, `ComputerFillsInIntent`, `DeclarationCreatesArray`, `DoubleLoopIndexCount`, `EarlyReturnInLoop`, `ElementBoundToOldIndex`, `ElementNameIsWholeArray`, `ElseWithCondition`, `EqualityOperatorComparesObjectsValues`, `EqualsComparesReferences`, `ExpressionOnLeftOfAssignment`, `FalseConditionRestartsProgram`, `FalseLoopRepeatsNextCode`, `ForCommaSeparators`, `ForInitRepeats`, `ForIsConditional`, `ForLoopPartSkipped`, `ForUpdateBeforeBody`, `ForVariableScopeBeyondLoop`, `ForWhileNotInterchangeable`, `IdiomOverridesCode`, `IfConditionWatched`, `IfInLoopUnchecked`, `IfWaitsForCondition`, `IncrementByTwo`, `IndexIsValue`, `InfiniteLoopUnnoticed`, `IntegerDivisionGivesFraction`, `IntegerProbability`, `LaterDoubleLiteralFixesDivision`, `LessGreaterSwapped`, `LocalVarOutsideScope`, `LoopBodyAlwaysOnce`, `LoopBodyScopeImpliesLoopLifetime`, `LoopBodyStatementOutsideLoop`, `LoopCountIsStatementCount`, `LoopForOneTimeTest`, `LoopHeaderIsEquations`, `LoopImpliedByOneTest`, `LoopOutputSameEachPass`, `LoopRunsStatementsSeparately`, `LoopStepAlwaysOne`, `LoopUpdateChangesDirection`, `LoopVariableLifetimeScope`, `LoopVariableLimitsValues`, `MapToBooleanWithConditionalOperator`, `MapToBooleanWithIf`, `MissingBraces`, `NarrowingAssignmentAllowed`, `NegativeArraySize`, `NegativeRemainderSign`, `NestedIfsInsteadOfLogicalOperators`, `NewArrayHoldsGarbage`, `NoAtomicExpression`, `NoCastIfSameSize`, `NoShortCircuit`, `OffByOneBound`, `OutsideInMethodNesting`, `ParenthesesOnlyIfArgument`, `PostIncrementAssignsLater`, `PreIncrementBeforeLoop`, `PrePostIncrementSameValue`, `PrintedTextIsExecuted`, `ProgramEndsAfterLoop`, `ProgramLooksAhead`, `RedeclareToReassign`, `RemainderIsSubtraction`, `ReturnDoesNotExitLoop`, `ReversedRelationalOperator`, `RowsNeedNotSumToOne`, `SemicolonAfterIfHeader`, `SemicolonAfterLoopHeader`, `SingleIterationInsteadOfLoop`, `StateChangeIgnoredAcrossPasses`, `StatementAfterLoopInBody`, `StatementNeedsNoTerminator`, `StatementsRunInAnyOrder`, `StringIsPrimitive`, `StringRelationalComparison`, `SwapWithoutTemp`, `TargetTyping`, `VariableKeepsOldValue`, `VariablesHoldExpressions`, `WhileStopsMidBody`, `WhitespaceIsSignificant`, `WholeArrayArithmetic`, `WrongIterationCount`

**Level nodes**: 130 (L0..L4 for each concept), **has_level edges**: 130, **level→misconception links**: 193, **connected pieces**: 4

Notes: concept nodes form 4 pieces (the KG has no edge between them): arithmetic_operators,array_creation,array_declaration,array_default_values,array_initializer,array_traversal,assignment,boolean_expression,comparison_operators,expression,for_loop,increment_operators,indexing,integer_division,loop_control,loop_scope,loop_variable,normalization | control_flow,statement | data_structure,data_type,primitive_type,type_conversion,widening_conversion | loop_body


## S134

```java
int t = a;
a = b;
b = t;
```

![S134](figures/S134.png)

**Concept nodes (2)**: `assignment` (generic), `variable_swap`


**Concept edges traced (1)**

| edge | logic |
|---|---|
| `pre:assignment->variable_swap` | The three assignments int t = a; a = b; b = t; exchange the values of a and b, as a trace of the variable values after each statement shows. |

**Misconception and error nodes (15) via 17 edges**: `AssignCompares`, `AssignToFinal`, `AssignmentAddsToTarget`, `AssignmentCopiesObject`, `AssignmentEmptiesSource`, `AssignmentExchangesValues`, `AssignmentIsEquation`, `AssignmentNotExpression`, `AssignmentOppositeDirection`, `ExpressionOnLeftOfAssignment`, `PrintedTextIsExecuted`, `RedeclareToReassign`, `SwapWithoutTemp`, `VariableKeepsOldValue`, `VariablesHoldExpressions`

**Level nodes**: 10 (L0..L4 for each concept), **has_level edges**: 10, **level→misconception links**: 17, **connected pieces**: 1


## S137

```java
System.out.print("Welcome to Java. This is ");
System.out.println("A nice programming language ");
System.out.print("that I have to learn.");
```

![S137](figures/S137.png)

**Concept nodes (4)**: `print`, `println`, `statement` (generic), `string_literal` (generic)


**Concept edges traced (5)**

| edge | logic |
|---|---|
| `par:print~println` | print leaves the cursor on the same line after printing; println moves the cursor to the next line after printing. |
| `pre:statement->print` | System.out.print(s); is itself a statement, so it runs at its own place in the sequence of statements. |
| `pre:statement->println` | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |
| `pre:string_literal->print` | print("s") outputs exactly the characters between the quotes, without the quotes. |
| `pre:string_literal->println` | println("s") outputs exactly the characters between the quotes and then ends the line. |

**Misconception and error nodes (15) via 18 edges**: `ComputerFillsInIntent`, `IdentifierCaseInsensitive`, `ParenthesesOnlyIfArgument`, `PrintEqualsPrintln`, `PrintNewLineFirst`, `PrintWithoutFinalNewline`, `PrintedTextIsExecuted`, `ProgramLooksAhead`, `RepeatedOutputVariablePrintedOnce`, `SingleQuotedString`, `StatementNeedsNoTerminator`, `StatementsRunInAnyOrder`, `StringLiteralSpansLines`, `UnclosedStringLiteral`, `WhitespaceIsSignificant`

**Level nodes**: 20 (L0..L4 for each concept), **has_level edges**: 20, **level→misconception links**: 16, **connected pieces**: 1
