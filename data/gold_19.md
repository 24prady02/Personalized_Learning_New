# Gold answer key - 19 scenarios (KG v3.9.5)

Every text below is copied from the KG. Edge ids use the pipeline format. `accept` = levels that also count as right.

## S001 - partially_correct

**Answer:** println adds a newline after the text and print does not.

**Main concept:** `println` (also accept: `print`)

**Overall level:** L1 (accept L1, L3)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `println` | L1 | L1, L3 | L1[1] states_the_rule | println(String x) behaves as though it calls print(x) and then println(); println() terminates the current line by writing the line separator string. | println adds a newline after the text |
| `print` | L1 | L1, L3 | L1[1] states_the_rule | print(String s) prints the string (or "null" for a null reference); print(int) etc. print the value's string form; no line terminator is written. | print does not |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `par:print~println` | confirmed | print leaves the cursor on the same line after printing; println moves the cursor to the next line after printing. | println adds a newline after the text and print does not |

**Correct side shown (must NOT be flagged):** `mis:println->PrintEqualsPrintln`  

## S005 - correct

**Main concept:** `do_while_loop` (also accept: `while_loop`)

**Overall level:** L4 (accept L3, L4)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `do_while_loop` | L4 | L3, L4 | L4[0] predict_a_change | | |
| `while_loop` | L3 | L1, L3 | via pre:while_loop->do_while_loop | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:while_loop->do_while_loop` | confirmed | do { body } while (c); is a while loop whose test is moved to the bottom. | |

**Correct side shown (must NOT be flagged):** `mis:do_while_loop->DoWhileTestsFirst`  

## S007 - wrong

**Main concept:** `nested_loops` (also accept: `loop_control`, `for_loop`)

**Overall level:** L0 (accept L0)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `nested_loops` | L0 | L0, L2 | L0[6] misconception | | |
| `loop_control` | L0 | L0 | L0[2] misconception | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:for_loop->nested_loops` | confirmed | | |
| `pre:loop_control->for_loop` | broken | | |

**Misconception held:** `mis:loop_control->OffByOneBound`  

**Root cause:** `loop_control` / `OffByOneBound`

## S008 - correct

**Main concept:** `do_while_loop` (also accept: `if_else_statement`)

**Overall level:** L2 (accept L2)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `do_while_loop` | L2 | L2 | | | |
| `if_else_statement` | L2 | L2 | | | |
| `logical_operators` | L2 | L1, L2 | | | |
| `formatted_output` | L2 | L2 | | | |

## S009 - correct

**Main concept:** `length_field` (also accept: `indexing`)

**Overall level:** L2 (accept L2, L3)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `length_field` | L2 | L2, L3 | | | |
| `indexing` | L2 | L2 | | | |
| `array_bounds` | L1 | L1, L2 | | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:indexing->array_bounds` | confirmed | | |
| `pre:array_creation->length_field` | context | | |

**Correct side shown (must NOT be flagged):** `mis:indexing->ArrayRangeInclusive`  

## S010 - wrong

**Main concept:** `array_copy` (also accept: `array_traversal`, `off_by_one_error`, `array_bounds`)

**Overall level:** L0 (accept L0)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `array_copy` | L0 | L0 | | | |
| `array_traversal` | L0 | L0 | | | |
| `off_by_one_error` | L0 | L0 | | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:array_traversal->array_copy` | confirmed | | |
| `pre:for_loop->array_traversal` | broken | | |
| `pre:indexing->array_bounds` | broken | | |
| `pre:indexing->off_by_one_error` | broken | | |

**Misconception held:** `mis:array_traversal->OffByOneBound`  

**Root cause:** `array_traversal` / `OffByOneBound`

## S015 - wrong

**Main concept:** `naming_convention` (also accept: -)

**Overall level:** L0 (accept L0)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `naming_convention` | L0 | L0 | | | |
| `char` | L1 | L1, L2 | | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:variable->naming_convention` | context | | |

**Misconception held:** `mis:naming_convention->NameNotCamelCase`  

**Root cause:** `naming_convention` / `NameNotCamelCase`

## S016 - wrong

**Main concept:** `remainder_operator` (also accept: `arithmetic_operators`)

**Overall level:** L0 (accept L0)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `remainder_operator` | L0 | L0 | | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:integer_division->remainder_operator` | broken | | |

**Misconception held:** `mis:remainder_operator->RemainderIsSubtraction`  

**Root cause:** `remainder_operator` / `RemainderIsSubtraction`

## S021 - correct

**Main concept:** `nested_conditionals` (also accept: `if_else_statement`)

**Overall level:** L2 (accept L2)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `nested_conditionals` | L2 | L2 | | | |
| `if_else_statement` | L2 | L2 | | | |
| `remainder_operator` | L2 | L2 | | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:if_else_statement->nested_conditionals` | confirmed | | |

## S023 - correct

**Main concept:** `switch_statement` (also accept: `break_statement`)

**Overall level:** L2 (accept L2)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `switch_statement` | L2 | L2 | | | |
| `break_statement` | L1 | L1 | | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:break_statement->switch_statement` | confirmed | | |

**Correct side shown (must NOT be flagged):** `mis:switch_statement->SwitchNoFallThrough`  

## S026 - correct

**Main concept:** `variable_swap` (also accept: `assignment`)

**Overall level:** L3 (accept L1, L3)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `variable_swap` | L3 | L1, L3 | | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:assignment->variable_swap` | context | | |

**Correct side shown (must NOT be flagged):** `mis:variable_swap->SwapWithoutTemp`  

**Correct side shown (must NOT be flagged):** `mis:assignment->AssignmentExchangesValues`  

## S047 - correct

**Main concept:** `formatted_output` (also accept: -)

**Overall level:** L4 (accept L4)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `formatted_output` | L4 | L4 | | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:standard_output->formatted_output` | context | | |

**Correct side shown (must NOT be flagged):** `mis:formatted_output->FieldWidthIsIntegerDigits`  

## S052 - correct

**Main concept:** `redirection` (also accept: `piping`, `standard_input`)

**Overall level:** L2 (accept L2)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `redirection` | L2 | L2 | | | |
| `piping` | L2 | L2 | | | |
| `command_line_args` | L2 | L1, L2 | | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:standard_output->redirection` | confirmed | | |
| `pre:standard_input->redirection` | confirmed | | |
| `pre:redirection->piping` | confirmed | | |
| `par:standard_input~command_line_args` | confirmed | | |

**Correct side shown (must NOT be flagged):** `mis:redirection->RedirectionIsArgument`  

## S057 - correct

**Main concept:** `integer_division` (also accept: `normalization`)

**Overall level:** L4 (accept L4)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `integer_division` | L4 | L4 | | | |
| `normalization` | L3 | L2, L3 | | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:integer_division->normalization` | confirmed | | |

**Correct side shown (must NOT be flagged):** `mis:integer_division->IntegerDivisionGivesFraction`  

**Correct side shown (must NOT be flagged):** `mis:integer_division->CastAfterIntDivision`  

**Correct side shown (must NOT be flagged):** `mis:normalization->IntegerProbability`  

## S068 - wrong

**Main concept:** `two_models` (also accept: `markov_chain`, `power_method`)

**Overall level:** L0 (accept L0)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `two_models` | L0 | L0 | | | |
| `frequency_counting` | L3 | L1, L3 | | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:frequency_counting->two_models` | confirmed | | |
| `pre:markov_chain->power_method` | broken | | |

**Misconception held:** `mis:two_models->StartPageMatters`  

**Correct side shown (must NOT be flagged):** `mis:two_models->FewTrialsAreExact`  

**Root cause:** `markov_chain` / `StartPageMatters`

## S073 - correct_after_self_correction

**Main concept:** `switch_statement` (also accept: -)

**Overall level:** L2 (accept L2)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `switch_statement` | L2 | L2 | | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:break_statement->switch_statement` | context | | |

**Correct side shown (must NOT be flagged):** `mis:switch_statement->SwitchNoFallThrough`  

## S080 - correct

**Main concept:** `compile_time_error` (also accept: `run_time_error`, `class_declaration`)

**Overall level:** L4 (accept L3, L4)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `compile_time_error` | L4 | L4 | | | |
| `class_declaration` | L4 | L2, L4 | | | |
| `run_time_error` | L4 | L3, L4 | | | |
| `command_line_args` | L4 | L2, L4 | | | |
| `comment` | L2 | L1, L2 | | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:program_text->class_declaration` | confirmed | | |
| `pre:compile->compile_time_error` | confirmed | | |
| `pre:compile->run` | confirmed | | |
| `pre:run->run_time_error` | confirmed | | |
| `par:compile_time_error~run_time_error` | confirmed | | |
| `pre:program_text->comment` | confirmed | | |

**Correct side shown (must NOT be flagged):** `mis:class_declaration->ClassNameMatchesFile`  

**Correct side shown (must NOT be flagged):** `err:compile_time_error->StatementNeedsNoTerminator`  

**Correct side shown (must NOT be flagged):** `err:command_line_args->FirstArgIsArgsOne`  

## S134 - wrong

**Main concept:** `variable_swap` (also accept: `assignment`)

**Overall level:** L0 (accept L0)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `variable_swap` | L0 | L0 | | | |
| `assignment` | L0 | L0 | | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:assignment->variable_swap` | broken | | |

**Misconception held:** `mis:assignment->VariablesHoldExpressions`  

**Root cause:** `assignment` / `VariablesHoldExpressions`

## S137 - wrong

**Main concept:** `println` (also accept: `string_literal`)

**Overall level:** L0 (accept L0)

| Concept | Level | Accept | Way | Rule (from KG) | Student evidence |
|---|---|---|---|---|---|
| `println` | L0 | L0 | | | |

| Edge | Status | Edge logic | Student evidence |
|---|---|---|---|
| `pre:string_literal->println` | broken | | |

**Misconception held:** `mis:println->PrintedTextIsExecuted`  

**Root cause:** `println` / `PrintedTextIsExecuted`
