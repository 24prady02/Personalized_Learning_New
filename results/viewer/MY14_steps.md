# Think on the Graph: every output of the run MY14
## 0. Input
Program:
```java
for (int i = 0; i < 10; i += 3) {
    System.out.println(i);
}
```
Question: Explain how i changes from one pass of the loop to the next.

Student's answer: A for loop moves i on by one each pass, so i goes 0, 1, 2 and so on up to 9.
Settings: width 3, depth 3, prune llm, backend claude-cli, model claude-opus-5-5
## 1. Stage 1: the subgraph G from the code (no model)
Masked code (string and char literals and comments blanked; this is what the patterns see):
```
for (int i = 0; i < 10; i += 3) {
    System.out.println(i);
}
```
Which code text tagged which concept (a generic concept fires on almost any Java line; it starts the walk only if the answer repeats its tag):
| concept | generic | channel | matched text | line |
|---|---|---|---|---|
| accumulator_pattern | False | pattern | 'i += 3) {\n    System.out.println(i);' | 1 |
| assignment | True | pattern | '=' | 1 |
| boolean_expression | False | pattern | 'for (int i = 0; i < 10;' | 1 |
| comparison_operators | False | pattern | 'for (int i = 0; i <' | 1 |
| compound_assignment | False | pattern | '+=' | 1 |
| control_flow | False | pattern | 'for (' | 1 |
| expression | True | pattern | 'i < 1' | 1 |
| expression | True | pattern | '= 0;' | 1 |
| for_loop | False | pattern | 'for (' | 1 |
| loop_body | False | pattern | 'for (' | 1 |
| loop_control | False | signal | 'for (int i = 0; i < 10; i += 3)' | 1 |
| loop_scope | False | pattern | 'for (int i' | 1 |
| loop_variable | False | pattern | 'for (int i =' | 1 |
| println | False | pattern | 'System.out.println(' | 2 |
| statement | True | pattern | ';' | 1 |

G: 14 concept nodes (3 generic), 10 concept edges, 123 misconception / error edges, 89 misconception / error nodes, 70 level nodes, 128 level-misconception links, 4 connected piece(s).
Note: concept nodes form 4 pieces (the KG has no edge between them): accumulator_pattern,loop_body | assignment,boolean_expression,comparison_operators,compound_assignment,expression | control_flow,println,statement | for_loop,loop_control,loop_scope,loop_variable

Concept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):
| edge | type | rule (logic) |
|---|---|---|
| par:assignment~comparison_operators | parallel | x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands. |
| pre:assignment->compound_assignment | prerequisite | x op= e is shorthand for the assignment x = x op e. |
| pre:comparison_operators->boolean_expression | prerequisite | A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making. |
| pre:expression->comparison_operators | prerequisite | Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b. |
| pre:for_loop->loop_scope | prerequisite | A variable declared in the for header exists only from its declaration to the end of the for statement's block. |
| pre:loop_body->accumulator_pattern | prerequisite | The accumulator update sum += x sits inside the body, so it runs once on every pass. |
| pre:loop_control->for_loop | prerequisite | The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |
| pre:loop_variable->loop_control | prerequisite | The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |
| pre:statement->control_flow | prerequisite | Control flow is the order in which statements run. |
| pre:statement->println | prerequisite | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |

Misconception / error edges per concept (count), and level ways per concept (count):
| concept | misconception / error edges | level ways (L1-L4 + L0 non-misconception) |
|---|---|---|
| accumulator_pattern | 4 | 17 |
| assignment | 15 | 24 |
| boolean_expression | 8 | 19 |
| comparison_operators | 8 | 20 |
| compound_assignment | 2 | 15 |
| control_flow | 11 | 15 |
| expression | 8 | 19 |
| for_loop | 21 | 24 |
| loop_body | 12 | 14 |
| loop_control | 11 | 19 |
| loop_scope | 5 | 14 |
| loop_variable | 7 | 13 |
| println | 6 | 17 |
| statement | 5 | 19 |

Figure 1: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY14_figure01.png

Figure 2: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY14_figure02.png

## 2. Clauses and start concepts (no model)
The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):
| clause | text |
|---|---|
| c1 | A for loop moves i on by one each pass |
| c2 | so i goes 0, 1, 2 and |
| c3 | so on up to 9 |

start: BM25 of the answer against each tagged concept: loop_control 17.91 (hits 1), for_loop 15.17 (hits 1), loop_variable 11.17 (hits 1), loop_scope 8.35 (hits 1), compound_assignment 6.28 (hits 1), loop_body 6.04 (hits 1), accumulator_pattern 5.62 (hits 1), control_flow 5.15 (hits 1), boolean_expression 5.13 (hits 1), println 1.90 (hits 1), comparison_operators 1.52 (hits 1)

start: chosen loop_control, for_loop, loop_variable

start concepts (3): loop_control, for_loop, loop_variable

Start concepts: loop_control, for_loop, loop_variable

Figure 3: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY14_figure03.png

## 3. The walk, depth by depth
At each depth, for each current concept: the edges offered (a concept entering as a start concept offers its misconception / error edges and its level ways, as two families; otherwise it offers its concept edges), the prune prompt and the model's reply, then the label prompt(s) and the model's reply, parsed into label / clauses / confidence. Score = prune score x confidence.

### Depth 1: current concepts 'loop_control', 'for_loop', 'loop_variable'

#### loop_control, misconceptions: 11 edges offered
Edges offered:
| edge |
|---|
| err:loop_control->WrongIterationCount \| wrong rule: Updates the loop counter so that the loop runs the wrong number of times. \| right rule: The init, test and update together decide the number of passes; trace them to check the count. |
| mis:loop_control->DoubleLoopIndexCount \| wrong rule: for (double x = 0.0; x <= 1.0; x += 0.1) runs exactly 11 times. \| right rule: Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect. |
| mis:loop_control->ForLoopPartSkipped \| wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). \| right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start. |
| mis:loop_control->ForUpdateBeforeBody \| wrong rule: The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value. \| right rule: The update runs after the body, before the next condition test; the first pass uses the initial value. |
| mis:loop_control->IdiomOverridesCode \| wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. |
| mis:loop_control->InfiniteLoopUnnoticed \| wrong rule: A while loop always stops on its own, even if nothing in its body can make the condition false. \| right rule: A while loop stops only when its condition is false at a check, so if no pass changes the variables in the condition, it never stops. |
| mis:loop_control->LoopHeaderIsEquations \| wrong rule: The initialization, condition and update of a for header are equations that all hold at the same time. \| right rule: The three header parts are statements run at different moments: init once, then condition test, body, update, repeated. |
| mis:loop_control->LoopStepAlwaysOne \| wrong rule: A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--). \| right rule: The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i *= 2, ...). |
| mis:loop_control->LoopUpdateChangesDirection \| wrong rule: The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same. \| right rule: The update expression is the same on every pass; the loop variable changes by the rule written in the update. |
| mis:loop_control->OffByOneBound \| wrong rule: i < n and i <= n mean the same, so the loop runs until i equals n and the last pass can use a[n]. \| right rule: for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n. |
| mis:loop_control->PreIncrementBeforeLoop \| wrong rule: With ++i in the update of for (int i = s; i < n; ++i), i is increased before the body runs, so the first pass uses s + 1. \| right rule: The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:loop_control->LoopStepAlwaysOne (0.60), mis:loop_control->IdiomOverridesCode (0.25), err:loop_control->WrongIterationCount (0.15)
```
Kept by pruning: mis:loop_control->LoopStepAlwaysOne (0.60), mis:loop_control->IdiomOverridesCode (0.25), err:loop_control->WrongIterationCount (0.15)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:loop_control->LoopStepAlwaysOne \| wrong rule: A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--). \| right rule: The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i *= 2, ...). |
| mis:loop_control->IdiomOverridesCode \| wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. |
| err:loop_control->WrongIterationCount \| wrong rule: Updates the loop counter so that the loop runs the wrong number of times. \| right rule: The init, test and update together decide the number of passes; trace them to check the count. |
Model's reply:
```
mis:loop_control->LoopStepAlwaysOne | held | clauses: 1, 2, 3 | confidence: 0.95
mis:loop_control->IdiomOverridesCode | not applied | clauses: none | confidence: 0.85
err:loop_control->WrongIterationCount | held | clauses: 2, 3 | confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:loop_control->LoopStepAlwaysOne | held | 0.6 | 0.95 | 0.57 | c1, c2, c3 | A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9 |
| mis:loop_control->IdiomOverridesCode | not applied |  |  | 0.0 |  |  |
| err:loop_control->WrongIterationCount | held | 0.15 | 0.6 | 0.09 | c2, c3 | so i goes 0, 1, 2 and; so on up to 9 |

#### loop_control, level ways: 19 edges offered
Edges offered:
| edge |
|---|
| lvl:loop_control@L0#0 \| level L0 way everyday_reading: Folk meaning: in mathematics i = 0, i < n and i = i + 1 are equations or constraints that hold at the same time (and i = i + 1 is nonsense). In Java they are three actions run at different moments: init once, test before each pass, update after each pass. |
| lvl:loop_control@L0#3 \| level L0 way inconsistent_trace: Applies the init-test-update rule (LT) unevenly: updates before the body on some passes, skips the test or the update on a pass, or re-runs the init. (here mixing in: "++i in the for-update runs before the body each pass") |
| lvl:loop_control@L1#0 \| level L1 way names_the_element: Loop control is the init / continuation condition / increment scheme on an index variable that decides how many passes a loop makes and with which values. |
| lvl:loop_control@L1#1 \| level L1 way states_the_rule: Initialize an index variable, test a loop-continuation condition on it before each pass, and increment it as the last action of each pass; for (<initialize>; <boolean expression>; <increment>) packages the three. Choosing the loop: for when the passes are counted by an index, while when the loop runs until a condition changes, do-while when the body must run at least once; any one can be rewritten as another, so choose the clearest. |
| lvl:loop_control@L2#0 \| level L2 way line_by_line_trace: init (once) -> test -> body -> update -> test -> body -> update ... -> test false -> exit. |
| lvl:loop_control@L2#1 \| level L2 way output_prediction: The number of passes and the values seen follow from the three parts: for (int i = 0; i <= N; i++) makes N+1 passes with i = 0..N; with i < N it makes N passes; i += 2 visits every second value. |
| lvl:loop_control@L2#2 \| level L2 way one_step_execution: One update changes only the loop variable, by exactly the rule written (i++ adds 1, i = i - 4 subtracts 4); one test reads it and returns true or false without changing it. |
| lvl:loop_control@L3#0 \| level L3 way relation_to_neighbour: All three control parts act on the loop variable: the init sets it, the condition tests it, the update changes it. |
| lvl:loop_control@L3#1 \| level L3 way relation_to_neighbour: The for header is exactly the three control slots, separated by semicolons; the body runs after the test and before the update. |
| lvl:loop_control@L3#2 \| level L3 way relation_to_neighbour: The update i = i + 1 is usually written i++ (or i += k for other steps); as a whole update statement ++i and i++ are equivalent. |
| lvl:loop_control@L3#3 \| level L3 way relation_to_neighbour: A loop is infinite when the update never moves the variable toward making the condition false (e.g. condition i > 3 with update i = i + 1). |
| lvl:loop_control@L3#4 \| level L3 way relation_to_neighbour: The continuation condition fixes the number of iterations, so a sharper bound (i <= n/i instead of i < n) can make a program dramatically faster. |
| lvl:loop_control@L3#5 \| level L3 way relation_to_neighbour: The initialization and the condition of a loop fix how many times it runs; one wrong bound makes it run once too many or too few. |
| lvl:loop_control@L3#6 \| level L3 way purpose_of_the_whole: Plan: counter-controlled loop - the loop variable is a stepper that walks a predictable sequence of values (0..N-1, 1..N, every 2nd value) and fixes the number of passes in advance. |
| lvl:loop_control@L4#0 \| level L4 way predict_a_change: Changing < to <= adds one pass; starting at 1 instead of 0 removes one; doubling the step halves the passes; reversing init and bound with i-- visits the same values in reverse order (and still processes the same set only if both ends are adjusted). |
| lvl:loop_control@L4#1 \| level L4 way diagnose_an_error: rule broken: The number of passes is fixed by the init, the test and the update together. Kind: silent logic error. Trigger class: Wrong start value, < vs <=, a wrong step, or an extra update of the counter in the body (or outside the loop): the loop runs too few or too many passes (off by one, or skips values). |
| lvl:loop_control@L4#2 \| level L4 way transfer_to_a_new_program: Use explicit init/test/update control when the passes are counted or follow a fixed step; when the number of passes depends on data computed in the body, control the loop by that data (a while condition) instead. |
| lvl:loop_control@L4#3 \| level L4 way diagnose_an_error: rule broken: The update must move the loop variable toward making the condition false. Kind: silent logic error. Trigger class: An update in the wrong direction or a condition that the update cannot falsify (e.g. i > 3 with i++, or i != 10 with i += 3): infinite loop. |
| lvl:loop_control@L4#4 \| level L4 way diagnose_an_error: rule broken: Do not control a loop by an equality test on double values. Kind: silent logic error. Trigger class: for (double x = 0.0; x < 1.0; x += 0.1): after ten additions x is 0.9999999999999999, so the loop makes 11 passes instead of the intended 10. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:loop_control@L2#2 (Score: 0.5)}
{lvl:loop_control@L2#1 (Score: 0.3)}
{lvl:loop_control@L3#2 (Score: 0.2)}
```
Kept by pruning: lvl:loop_control@L2#2 (0.50), lvl:loop_control@L2#1 (0.30), lvl:loop_control@L3#2 (0.20)

Label prompt for level way lvl:loop_control@L2#2 (the model saw only the concept, the way's name 'one step execution' and its text; no level):
> One update changes only the loop variable, by exactly the rule written (i++ adds 1, i = i - 4 subtracts 4); one test reads it and returns true or false without changing it.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:loop_control@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> The number of passes and the values seen follow from the three parts: for (int i = 0; i <= N; i++) makes N+1 passes with i = 0..N; with i < N it makes N passes; i += 2 visits every second value.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.8
```

Label prompt for level way lvl:loop_control@L3#2 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> The update i = i + 1 is usually written i++ (or i += k for other steps); as a whole update statement ++i and i++ are equivalent.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:loop_control@L2#2 | not applied |  |  | 0.0 |  |  |
| lvl:loop_control@L2#1 | not applied |  |  | 0.0 |  |  |
| lvl:loop_control@L3#2 | not applied |  |  | 0.0 |  |  |

#### for_loop, misconceptions: 21 edges offered
Edges offered:
| edge |
|---|
| err:for_loop->BracelessMultiStatementBody \| wrong rule: Indenting several statements under an if or for makes them all part of its body, even without braces. \| right rule: Without braces only the first statement belongs to the if/for; the rest run once, after it. |
| err:for_loop->ForCommaSeparators \| wrong rule: Writes for (int i = 0, i < n, i++). \| right rule: The three parts of a for header are separated by semicolons; commas only separate several statements inside the init or the update part. |
| err:for_loop->SemicolonAfterIfHeader \| wrong rule: if (x > 0); System.out.println("positive"); prints only for positive x. \| right rule: The ; ends the if with an empty statement, so the next line always runs. |
| err:for_loop->SemicolonAfterLoopHeader \| wrong rule: Puts a ; right after for (...) or while (...). \| right rule: A ; right after the loop header is a null (empty) loop body, so the statements written after it are not repeated by the loop. |
| err:for_loop->WrongIterationCount \| wrong rule: Updates the loop counter so that the loop runs the wrong number of times. \| right rule: The init, test and update together decide the number of passes; trace them to check the count. |
| mis:for_loop->DoubleLoopIndexCount \| wrong rule: for (double x = 0.0; x <= 1.0; x += 0.1) runs exactly 11 times. \| right rule: Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect. |
| mis:for_loop->FalseLoopRepeatsNextCode \| wrong rule: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. \| right rule: Only the body is repeated; once the condition is false the code after the loop runs once. |
| mis:for_loop->ForInitRepeats \| wrong rule: The initialization of a for loop runs again after a pass of the body. \| right rule: The initialization runs exactly once, before the first condition test. |
| mis:for_loop->ForIsConditional \| wrong rule: The body of a for statement executes at most once. \| right rule: The body of a for statement runs once for every pass on which the condition is true, which can be many times. |
| mis:for_loop->ForLoopPartSkipped \| wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). \| right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start. |
| mis:for_loop->ForUpdateBeforeBody \| wrong rule: The update part of a for header (e.g. i = i - 4) runs before the body on each pass, so the first pass already sees the updated value. \| right rule: The update runs after the body, before the next condition test; the first pass uses the initial value. |
| mis:for_loop->ForWhileNotInterchangeable \| wrong rule: Some loops can only be written with for, others only with while. \| right rule: Any for loop can be rewritten as a while loop and vice versa; for just packages init, test and update. |
| mis:for_loop->IdiomOverridesCode \| wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. |
| mis:for_loop->LoopCountIsStatementCount \| wrong rule: The repeat count of a counted loop says how many of the body statements are executed. \| right rule: The repeat count is how many times the whole body runs; every pass runs all body statements. |
| mis:for_loop->LoopHeaderIsEquations \| wrong rule: The initialization, condition and update of a for header are equations that all hold at the same time. \| right rule: The three header parts are statements run at different moments: init once, then condition test, body, update, repeated. |
| mis:for_loop->LoopImpliedByOneTest \| wrong rule: Testing one case is enough; Java will repeat the test for the other values by itself. \| right rule: A statement runs once each time control reaches it; repeating a test for many values needs a loop. |
| mis:for_loop->LoopStepAlwaysOne \| wrong rule: A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--). \| right rule: The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i *= 2, ...). |
| mis:for_loop->MissingBraces \| wrong rule: Omits braces around a single-statement body of if, for or while. \| right rule: Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later. |
| mis:for_loop->ProgramEndsAfterLoop \| wrong rule: When a loop finishes the program ends, so code after the loop never runs. \| right rule: When the loop condition becomes false, control continues with the first statement after the loop. |
| mis:for_loop->ReturnDoesNotExitLoop \| wrong rule: A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values. \| right rule: When return executes, the method ends at once, so the loop stops on that pass. |
| mis:for_loop->SingleIterationInsteadOfLoop \| wrong rule: A task that must be repeated is written once, without a loop, as if one pass were enough. \| right rule: A step that must happen several times (or an unknown number of times) needs a loop such as while or for; code without a loop runs once. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:for_loop->LoopStepAlwaysOne (0.60), mis:for_loop->IdiomOverridesCode (0.25), err:for_loop->WrongIterationCount (0.15)
```
Kept by pruning: mis:for_loop->LoopStepAlwaysOne (0.60), mis:for_loop->IdiomOverridesCode (0.25), err:for_loop->WrongIterationCount (0.15)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:for_loop->LoopStepAlwaysOne \| wrong rule: A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--). \| right rule: The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i *= 2, ...). |
| mis:for_loop->IdiomOverridesCode \| wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. |
| err:for_loop->WrongIterationCount \| wrong rule: Updates the loop counter so that the loop runs the wrong number of times. \| right rule: The init, test and update together decide the number of passes; trace them to check the count. |
Model's reply:
```
mis:for_loop->LoopStepAlwaysOne | held | clauses: 1, 2, 3 | confidence: 0.95
mis:for_loop->IdiomOverridesCode | not applied | clauses: none | confidence: 0.85
err:for_loop->WrongIterationCount | not applied | clauses: none | confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:for_loop->LoopStepAlwaysOne | held | 0.6 | 0.95 | 0.57 | c1, c2, c3 | A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9 |
| mis:for_loop->IdiomOverridesCode | not applied |  |  | 0.0 |  |  |
| err:for_loop->WrongIterationCount | not applied |  |  | 0.0 |  |  |

#### for_loop, level ways: 24 edges offered
Edges offered:
| edge |
|---|
| lvl:for_loop@L0#0 \| level L0 way everyday_reading: Folk meaning: English 'for each ...' or 'for 10 times' names a whole collection or a count to be handled at once, and a maths reading treats the header as simultaneous conditions. A Java for is a while loop in compact form: one init, then test-body-update repeated, one pass at a time. |
| lvl:for_loop@L0#11 \| level L0 way inconsistent_trace: Applies the for sequencing rule (LT) unevenly: updates before the body on the first pass only, re-runs the init after a pass, or skips the test on some passes. (here mixing in: "The body of a for statement executes at most once") |
| lvl:for_loop@L1#0 \| level L1 way names_the_element: The for statement is a loop that packages an initialization, a loop-continuation condition and an increment in its header around a body. |
| lvl:for_loop@L1#1 \| level L1 way states_the_rule: Syntax: for (<initialize>; <boolean expression>; <increment>) { <statements> }, with the three parts separated by semicolons; it is, with only a few exceptions, equivalent to <initialize>; while (<boolean expression>) { <statements> <increment>; }. |
| lvl:for_loop@L2#0 \| level L2 way line_by_line_trace: Run the initializer once; then repeatedly: test the condition (stop if false), execute the body, run the update. |
| lvl:for_loop@L2#1 \| level L2 way output_prediction: A for statement has no value; the passes it makes are fixed by its header: for (int i = 1; i <= N; i++) sum += i; leaves sum = N(N+1)/2, and for (int i = 2; i <= 8; i += 2) prints 2, 4, 6, 8,. |
| lvl:for_loop@L2#2 \| level L2 way one_step_execution: One pass: the test reads the loop variable; the body applies its changes once; the update then changes the loop variable by its rule; the initializer changes state only once, before the first test. |
| lvl:for_loop@L3#0 \| level L3 way relation_to_neighbour: The for header is exactly the three loop-control slots; the body runs after the test and before the update on each pass. |
| lvl:for_loop@L3#1 \| level L3 way relation_to_neighbour: A for may be the body of another for: the inner for runs its complete set of passes for every single pass of the outer one. |
| lvl:for_loop@L3#2 \| level L3 way relation_to_neighbour: for (int i = 0; i < N; i++) gives i each valid index 0..N-1 exactly once in increasing order, the standard way to process every array element. |
| lvl:for_loop@L3#3 \| level L3 way relation_to_neighbour: A simulation runs a fixed number of trials with an outer for loop (for (int t = 0; t < T; t++)), each trial simulated inside the body. |
| lvl:for_loop@L3#4 \| level L3 way relation_to_neighbour: In a for loop, continue skips the rest of the body and transfers control directly to the increment, then the next test; this is one of the few places where the for/while equivalence fails. |
| lvl:for_loop@L3#5 \| level L3 way relation_to_neighbour: A variable declared in the for header is in scope only in the header and the body, so it cannot be used after the loop. |
| lvl:for_loop@L3#6 \| level L3 way relation_to_neighbour: A fencepost loop is a for loop that handles one item (the first or last) outside the loop so that separators come out n-1 times for n items. |
| lvl:for_loop@L3#7 \| level L3 way relation_to_neighbour: A flag search loop is a for loop that sets a boolean flag when some pass finds the target and leaves it set afterwards; the flag must be declared before the loop. |
| lvl:for_loop@L3#8 \| level L3 way purpose_of_the_whole: Plan: counted loop / counter-controlled repetition - do the body a known number of times, with the loop variable as a stepper (index, term number, trial number). |
| lvl:for_loop@L4#0 \| level L4 way predict_a_change: Rewriting a for as the equivalent while (init before, update at the end of the body) keeps behaviour, except that continue then skips the update and the loop variable stays in scope after the loop. Changing the bound or the step changes the pass count predictably (< to <= adds one pass). |
| lvl:for_loop@L4#1 \| level L4 way diagnose_an_error: rule broken: The three parts of a for header are separated by semicolons; commas only separate several statements inside the init or the update. Kind: compile-time. Trigger class: Writing for (int i = 0, i < n, i++): the compiler parses the commas as more declarators in the init and reports a syntax error. |
| lvl:for_loop@L4#2 \| level L4 way diagnose_an_error: rule broken: A ; right after while (...) or for (...) is an empty statement that is the whole loop body; the block written next is not repeated. Kind: silent logic error. Trigger class: for (...); { body } runs the body once after the loop ends; while (cond); with a cond that the empty body cannot change hangs forever (infinite loop) when cond starts true. |
| lvl:for_loop@L4#3 \| level L4 way transfer_to_a_new_program: Use for when there is an initialization, an increment and a continuation test and the loop variable is not needed after the loop; use while when the loop variable is needed later or the number of passes depends on what happens in the body. |
| lvl:for_loop@L4#4 \| level L4 way diagnose_an_error: rule broken: A ; right after if (...) is an empty statement that forms the whole then branch; the following statement or block is no longer part of the if. Kind: silent logic error. Trigger class: Any if (cond); followed by a statement or block: that statement runs for every input, whatever cond is (it compiles without error). |
| lvl:for_loop@L4#5 \| level L4 way diagnose_an_error: rule broken: The number of passes is fixed by the init, the test and the update together. Kind: silent logic error. Trigger class: Wrong start value, < vs <=, a wrong step, or an extra update of the counter in the body (or outside the loop): the loop runs too few or too many passes (off by one, or skips values). |
| lvl:for_loop@L4#6 \| level L4 way diagnose_an_error: rule broken: Without braces, the body of an if, while or for is exactly one statement; indentation does not add statements to it. Kind: silent logic error. Trigger class: A braceless header followed by two or more indented statements: only the first is controlled, the others run once, after the if/loop, on every input. |
| lvl:for_loop@L4#7 \| level L4 way diagnose_an_error: rule broken: A variable declared in the for initializer exists only inside the for statement. Kind: compile-time. Trigger class: Reading i after for (int i = 0; ...) {...}: 'cannot find symbol'. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:for_loop@L4#5 (Score: 0.5)}
{lvl:for_loop@L2#2 (Score: 0.3)}
{lvl:for_loop@L0#0 (Score: 0.2)}
```
Kept by pruning: lvl:for_loop@L4#5 (0.50), lvl:for_loop@L2#2 (0.30), lvl:for_loop@L0#0 (0.20)

Label prompt for level way lvl:for_loop@L4#5 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: The number of passes is fixed by the init, the test and the update together. Kind: silent logic error. Trigger class: Wrong start value, < vs <=, a wrong step, or an extra update of the counter in the body (or outside the loop): the loop runs too few or too many passes (off by one, or skips values).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:for_loop@L2#2 (the model saw only the concept, the way's name 'one step execution' and its text; no level):
> One pass: the test reads the loop variable; the body applies its changes once; the update then changes the loop variable by its rule; the initializer changes state only once, before the first test.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.8
```

Label prompt for level way lvl:for_loop@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: English 'for each ...' or 'for 10 times' names a whole collection or a count to be handled at once, and a maths reading treats the header as simultaneous conditions. A Java for is a while loop in compact form: one init, then test-body-update repeated, one pass at a time.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.65
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:for_loop@L4#5 | not applied |  |  | 0.0 |  |  |
| lvl:for_loop@L2#2 | not applied |  |  | 0.0 |  |  |
| lvl:for_loop@L0#0 | not applied |  |  | 0.0 |  |  |

#### loop_variable, misconceptions: 7 edges offered
Edges offered:
| edge |
|---|
| mis:loop_variable->BodyChangeIgnoredByCondition \| wrong rule: Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times. \| right rule: The condition is tested with the current value of the variable, including changes made in the body. |
| mis:loop_variable->DoubleLoopIndexCount \| wrong rule: for (double x = 0.0; x <= 1.0; x += 0.1) runs exactly 11 times. \| right rule: Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect. |
| mis:loop_variable->ForInitRepeats \| wrong rule: The initialization of a for loop runs again after a pass of the body. \| right rule: The initialization runs exactly once, before the first condition test. |
| mis:loop_variable->LoopOutputSameEachPass \| wrong rule: A loop prints the same thing on every pass; the changing loop variable does not affect what the body does. \| right rule: The body uses the current value of the loop variable, so its output can differ on each pass. |
| mis:loop_variable->LoopUpdateChangesDirection \| wrong rule: The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same. \| right rule: The update expression is the same on every pass; the loop variable changes by the rule written in the update. |
| mis:loop_variable->LoopVariableLifetimeScope \| wrong rule: The for variable i is a new variable on every pass rather than one variable changed by the update. \| right rule: The for variable i is created once by the init, and the update changes that same variable on every pass. |
| mis:loop_variable->LoopVariableLimitsValues \| wrong rule: The range of the loop variable limits the values that can be read or printed inside the loop. \| right rule: The loop variable only counts passes; other values read or printed in the body are not bounded by it. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:loop_variable->LoopUpdateChangesDirection (0.60), mis:loop_variable->LoopVariableLifetimeScope (0.25), mis:loop_variable->ForInitRepeats (0.15)
```
Kept by pruning: mis:loop_variable->LoopUpdateChangesDirection (0.60), mis:loop_variable->LoopVariableLifetimeScope (0.25), mis:loop_variable->ForInitRepeats (0.15)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:loop_variable->LoopUpdateChangesDirection \| wrong rule: The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same. \| right rule: The update expression is the same on every pass; the loop variable changes by the rule written in the update. |
| mis:loop_variable->LoopVariableLifetimeScope \| wrong rule: The for variable i is a new variable on every pass rather than one variable changed by the update. \| right rule: The for variable i is created once by the init, and the update changes that same variable on every pass. |
| mis:loop_variable->ForInitRepeats \| wrong rule: The initialization of a for loop runs again after a pass of the body. \| right rule: The initialization runs exactly once, before the first condition test. |
Model's reply:
```
mis:loop_variable->LoopUpdateChangesDirection | not applied | clauses: none | confidence: 0.6
mis:loop_variable->LoopVariableLifetimeScope | not applied | clauses: none | confidence: 0.6
mis:loop_variable->ForInitRepeats | correct | clauses: 2, 3 | confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:loop_variable->LoopUpdateChangesDirection | not applied |  |  | 0.0 |  |  |
| mis:loop_variable->LoopVariableLifetimeScope | not applied |  |  | 0.0 |  |  |
| mis:loop_variable->ForInitRepeats | correct | 0.15 | 0.6 | 0.09 | c2, c3 | so i goes 0, 1, 2 and; so on up to 9 |

#### loop_variable, level ways: 13 edges offered
Edges offered:
| edge |
|---|
| lvl:loop_variable@L0#0 \| level L0 way everyday_reading: Folk meaning: in maths a variable like the i in a sum ranges over all its values at once, and 'i from 1 to 10' is a set. A Java loop variable is one storage location holding one value at a time, changed step by step by the update. |
| lvl:loop_variable@L0#5 \| level L0 way inconsistent_trace: Applies the init-test-update rule (LT, loop_control) unevenly to the loop variable: forgets one update, applies a different step on some passes, or re-initializes it mid-loop. (here mixing in: "The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same") |
| lvl:loop_variable@L1#0 \| level L1 way names_the_element: A loop variable (loop-control counter, index) is a variable that is initialized, tested and updated in order to control a loop. |
| lvl:loop_variable@L1#1 \| level L1 way states_the_rule: The loop variable is set once by the initialization, tested by the continuation condition before each pass and updated (usually incremented) at the end of each pass; declared in a for header, it is not available after the loop. |
| lvl:loop_variable@L2#0 \| level L2 way line_by_line_trace: Its value is set by the init, read by the test, read by the body, then changed by the update, and the cycle repeats; the body sees the value set by the previous update. |
| lvl:loop_variable@L2#1 \| level L2 way output_prediction: Across passes the loop variable takes a predictable sequence of values, e.g. 4, 5, ..., 10 in TenHellos, and after a while loop it holds the first value that failed the test (11). |
| lvl:loop_variable@L2#2 \| level L2 way one_step_execution: One update changes only the loop variable (i = i + 1 turns 4 into 5); one test reads it and yields true or false; an assignment to it in the body changes what the next test sees. |
| lvl:loop_variable@L3#0 \| level L3 way relation_to_neighbour: The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |
| lvl:loop_variable@L3#1 \| level L3 way relation_to_neighbour: In a while loop the loop variable is declared and initialized before the loop and updated inside the body, so it remains available after the loop. |
| lvl:loop_variable@L3#2 \| level L3 way purpose_of_the_whole: Role: stepper - a variable stepping through a systematic, predictable succession of values; it counts passes and often serves as an index. |
| lvl:loop_variable@L4#0 \| level L4 way predict_a_change: Shifting the start and the bound by the same amount keeps the number of passes but changes the values the body sees; assigning to the loop variable inside the body changes the pass count. |
| lvl:loop_variable@L4#1 \| level L4 way transfer_to_a_new_program: Use a dedicated loop variable (int) when passes are counted or indexed; do not use a double loop variable, and do not reuse it for other roles inside the body. |
| lvl:loop_variable@L4#2 \| level L4 way diagnose_an_error: rule broken: Update the loop variable only in the update part (or in one place in a while body). Kind: silent logic error. Trigger class: An extra i++ in the body (or modifying i elsewhere): passes are skipped or repeated, and the loop may overshoot an != bound and never end. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:loop_variable@L2#1 (Score: 0.4)}
{lvl:loop_variable@L0#5 (Score: 0.35)}
{lvl:loop_variable@L2#2 (Score: 0.25)}
```
Kept by pruning: lvl:loop_variable@L2#1 (0.40), lvl:loop_variable@L0#5 (0.35), lvl:loop_variable@L2#2 (0.25)

Label prompt for level way lvl:loop_variable@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> Across passes the loop variable takes a predictable sequence of values, e.g. 4, 5, ..., 10 in TenHellos, and after a while loop it holds the first value that failed the test (11).

Model's reply:
```
Label: shown
Clauses: 2, 3
Confidence: 0.7
```

Label prompt for level way lvl:loop_variable@L0#5 (the model saw only the concept, the way's name 'inconsistent trace' and its text; no level):
> Applies the init-test-update rule (LT, loop_control) unevenly to the loop variable: forgets one update, applies a different step on some passes, or re-initializes it mid-loop. (here mixing in: "The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same")

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:loop_variable@L2#2 (the model saw only the concept, the way's name 'one step execution' and its text; no level):
> One update changes only the loop variable (i = i + 1 turns 4 into 5); one test reads it and yields true or false; an assignment to it in the body changes what the next test sees.

Model's reply:
```
Label: shown
Clauses: 1, 2
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:loop_variable@L2#1 | shown | 0.4 | 0.7 | 0.28 | c2, c3 | so i goes 0, 1, 2 and; so on up to 9 |
| lvl:loop_variable@L0#5 | not applied |  |  | 0.0 |  |  |
| lvl:loop_variable@L2#2 | shown | 0.25 | 0.7 | 0.17 | c1, c2 | A for loop moves i on by one each pass; so i goes 0, 1, 2 and |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:loop_control->LoopStepAlwaysOne [held, tier 0, 0.57], mis:for_loop->LoopStepAlwaysOne [held, tier 0, 0.57], err:loop_control->WrongIterationCount [held, tier 1, 0.09]

**Graph check, not yet read (the walk may not stop while these remain):** pre:for_loop->loop_scope, pre:loop_control->for_loop, pre:loop_variable->loop_control

Figure 4 (the graph after depth 1): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY14_figure04.png

### Depth 2: current concepts 'loop_control', 'for_loop', 'loop_variable'

#### loop_control, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| pre:loop_control->for_loop \| rule: The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |
| pre:loop_variable->loop_control \| rule: The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:loop_variable->loop_control (Score: 0.65)}
{pre:loop_control->for_loop (Score: 0.35)}
```
Kept by pruning: pre:loop_variable->loop_control (0.65), pre:loop_control->for_loop (0.35)

Label prompt for concept edge pre:loop_variable->loop_control (loop_variable -> loop_control, prerequisite):
> The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.

Model's reply:
```
Label: broken
Clauses: 1, 2, 3
Confidence: 0.8
```

Label prompt for concept edge pre:loop_control->for_loop (loop_control -> for_loop, prerequisite):
> The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.

Model's reply:
```
Label: broken
Clauses: 1, 2, 3
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:loop_variable->loop_control | broken | 0.65 | 0.8 | 0.52 | c1, c2, c3 | A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9 |
| pre:loop_control->for_loop | broken | 0.35 | 0.8 | 0.28 | c1, c2, c3 | A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9 |

#### for_loop, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:for_loop->loop_scope \| rule: A variable declared in the for header exists only from its declaration to the end of the for statement's block. |
| pre:loop_control->for_loop \| rule: The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:for_loop->loop_scope (Score: 1.0)}
```
Kept by pruning: pre:for_loop->loop_scope (1.00)

Label prompt for concept edge pre:for_loop->loop_scope (for_loop -> loop_scope, prerequisite):
> A variable declared in the for header exists only from its declaration to the end of the for statement's block.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:for_loop->loop_scope | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:loop_variable->loop_control [broken, tier 0, 0.52], pre:loop_control->for_loop [broken, tier 0, 0.28]

Figure 5 (the graph after depth 2): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY14_figure05.png

Held set after the one-fault rules: mis:for_loop->LoopStepAlwaysOne; filed at the dependent concept: mis:loop_control->LoopStepAlwaysOne

## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on ['for_loop'], broken at [] (consequences: pre:loop_variable->loop_control, pre:loop_control->for_loop), prerequisites {'compound_assignment': ['assignment'], 'boolean_expression': ['comparison_operators'], 'comparison_operators': ['expression'], 'loop_scope': ['for_loop'], 'accumulator_pattern': ['loop_body'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable'], 'control_flow': ['statement'], 'println': ['statement']}
- for_loop: L0 via misconception "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9"
- loop_variable: L2 via output_prediction "so i goes 0, 1, 2 and; so on up to 9"

**Stop:** sufficient at depth 2; prompts {'prune': 8, 'label': 15}, fresh model calls 0, cache hits 23

### Held misconceptions
| concept | misconception | kind | quote | score | shares_evidence_with |
|---|---|---|---|---|---|
| for_loop | LoopStepAlwaysOne | misconception | A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9 | 0.57 |  |

### Errors kept as evidence
| concept | error | quote |
|---|---|---|
| loop_control | WrongIterationCount | so i goes 0, 1, 2 and; so on up to 9 |

### Broken concept edges
| edge | quote | score | consequence_of |
|---|---|---|---|
| pre:loop_variable->loop_control | A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9 | 0.52 | mis:loop_control->LoopStepAlwaysOne |
| pre:loop_control->for_loop | A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9 | 0.28 | mis:loop_control->LoopStepAlwaysOne |

### Root cause: for_loop / LoopStepAlwaysOne

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| for_loop | L0 | misconception | LoopStepAlwaysOne | level_mis_links | A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9 | wrong rule: A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--). Right rule: The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i *= 2, ...). |  |  |
| loop_variable | L2 | output_prediction |  | level_way | so i goes 0, 1, 2 and; so on up to 9 |  | L2 one_step_execution |  |

### Overall level: L0

Clause coverage (final):
| clause | covered by |
|---|---|
| A for loop moves i on by one each pass | mis:loop_control->LoopStepAlwaysOne |
| so i goes 0, 1, 2 and | mis:loop_control->LoopStepAlwaysOne |
| so on up to 9 | mis:loop_control->LoopStepAlwaysOne |

Figure 6 (final picture): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY14_figure06.png

## 5. Every labelled edge (the evidence list, kept or not)
| depth | source | edge | kind | label | prune_score | confidence | score | clauses | quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | loop_control | mis:loop_control->LoopStepAlwaysOne | misconception | held | 0.6 | 0.95 | 0.57 | [1, 2, 3] | A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9 |
| 1 | loop_control | err:loop_control->WrongIterationCount | error | held | 0.15 | 0.6 | 0.09 | [2, 3] | so i goes 0, 1, 2 and; so on up to 9 |
| 1 | for_loop | mis:for_loop->LoopStepAlwaysOne | misconception | held | 0.6 | 0.95 | 0.57 | [1, 2, 3] | A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9 |
| 1 | loop_variable | mis:loop_variable->ForInitRepeats | misconception | correct | 0.15 | 0.6 | 0.09 | [2, 3] | so i goes 0, 1, 2 and; so on up to 9 |
| 1 | loop_variable | lvl:loop_variable@L2#1 | level | shown | 0.4 | 0.7 | 0.28 | [2, 3] | so i goes 0, 1, 2 and; so on up to 9 |
| 1 | loop_variable | lvl:loop_variable@L2#2 | level | shown | 0.25 | 0.7 | 0.175 | [1, 2] | A for loop moves i on by one each pass; so i goes 0, 1, 2 and |
| 2 | loop_control | pre:loop_variable->loop_control | prerequisite | broken | 0.65 | 0.8 | 0.52 | [1, 2, 3] | A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9 |
| 2 | loop_control | pre:loop_control->for_loop | prerequisite | broken | 0.35 | 0.8 | 0.28 | [1, 2, 3] | A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9 |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | loop_control | mis:loop_control->LoopStepAlwaysOne | misconception | held | 0.57 | [1, 2, 3] |
| 1 | for_loop | mis:for_loop->LoopStepAlwaysOne | misconception | held | 0.57 | [1, 2, 3] |
| 1 | loop_control | err:loop_control->WrongIterationCount | error | held | 0.09 | [2, 3] |
| 2 | loop_control | pre:loop_variable->loop_control | prerequisite | broken | 0.52 | [1, 2, 3] |
| 2 | loop_control | pre:loop_control->for_loop | prerequisite | broken | 0.28 | [1, 2, 3] |

## 7. Raw traversal log
```
clauses: A for loop moves i on by one each pass | so i goes 0, 1, 2 and | so on up to 9
start: BM25 of the answer against each tagged concept: loop_control 17.91 (hits 1), for_loop 15.17 (hits 1), loop_variable 11.17 (hits 1), loop_scope 8.35 (hits 1), compound_assignment 6.28 (hits 1), loop_body 6.04 (hits 1), accumulator_pattern 5.62 (hits 1), control_flow 5.15 (hits 1), boolean_expression 5.13 (hits 1), println 1.90 (hits 1), comparison_operators 1.52 (hits 1)
start: chosen loop_control, for_loop, loop_variable
start concepts (3): loop_control, for_loop, loop_variable
--- depth 1: current concepts ['loop_control', 'for_loop', 'loop_variable']
  loop_control (misconceptions): 11 candidates -> kept mis:loop_control->LoopStepAlwaysOne (0.60), mis:loop_control->IdiomOverridesCode (0.25), err:loop_control->WrongIterationCount (0.15)
    mis:loop_control->LoopStepAlwaysOne -> held (0.57) "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9"
    mis:loop_control->IdiomOverridesCode -> not applied (0.00) ""
    err:loop_control->WrongIterationCount -> held (0.09) "so i goes 0, 1, 2 and; so on up to 9"
  loop_control (level ways): 19 candidates -> kept lvl:loop_control@L2#2 (0.50), lvl:loop_control@L2#1 (0.30), lvl:loop_control@L3#2 (0.20)
    lvl:loop_control@L2#2 -> not applied (0.00) ""
    lvl:loop_control@L2#1 -> not applied (0.00) ""
    lvl:loop_control@L3#2 -> not applied (0.00) ""
  for_loop (misconceptions): 21 candidates -> kept mis:for_loop->LoopStepAlwaysOne (0.60), mis:for_loop->IdiomOverridesCode (0.25), err:for_loop->WrongIterationCount (0.15)
    mis:for_loop->LoopStepAlwaysOne -> held (0.57) "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9"
    mis:for_loop->IdiomOverridesCode -> not applied (0.00) ""
    err:for_loop->WrongIterationCount -> not applied (0.00) ""
  for_loop (level ways): 24 candidates -> kept lvl:for_loop@L4#5 (0.50), lvl:for_loop@L2#2 (0.30), lvl:for_loop@L0#0 (0.20)
    lvl:for_loop@L4#5 -> not applied (0.00) ""
    lvl:for_loop@L2#2 -> not applied (0.00) ""
    lvl:for_loop@L0#0 -> not applied (0.00) ""
  loop_variable (misconceptions): 7 candidates -> kept mis:loop_variable->LoopUpdateChangesDirection (0.60), mis:loop_variable->LoopVariableLifetimeScope (0.25), mis:loop_variable->ForInitRepeats (0.15)
    mis:loop_variable->LoopUpdateChangesDirection -> not applied (0.00) ""
    mis:loop_variable->LoopVariableLifetimeScope -> not applied (0.00) ""
    mis:loop_variable->ForInitRepeats -> correct (0.09) "so i goes 0, 1, 2 and; so on up to 9"
  loop_variable (level ways): 13 candidates -> kept lvl:loop_variable@L2#1 (0.40), lvl:loop_variable@L0#5 (0.35), lvl:loop_variable@L2#2 (0.25)
    lvl:loop_variable@L2#1 -> shown (0.28) "so i goes 0, 1, 2 and; so on up to 9"
    lvl:loop_variable@L0#5 -> not applied (0.00) ""
    lvl:loop_variable@L2#2 -> shown (0.17) "A for loop moves i on by one each pass; so i goes 0, 1, 2 and"
  kept: mis:loop_control->LoopStepAlwaysOne [held, tier 0, 0.57], mis:for_loop->LoopStepAlwaysOne [held, tier 0, 0.57], err:loop_control->WrongIterationCount [held, tier 1, 0.09]
  clause coverage (rule edges): c1 <- mis:loop_control->LoopStepAlwaysOne; c2 <- mis:loop_control->LoopStepAlwaysOne; c3 <- mis:loop_control->LoopStepAlwaysOne
  not yet read: pre:for_loop->loop_scope, pre:loop_control->for_loop, pre:loop_variable->loop_control
--- depth 2: current concepts ['loop_control', 'for_loop', 'loop_variable']
  loop_control (concept edges): 2 candidates -> kept pre:loop_variable->loop_control (0.65), pre:loop_control->for_loop (0.35)
    pre:loop_variable->loop_control -> broken (0.52) "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9"
    pre:loop_control->for_loop -> broken (0.28) "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9"
  for_loop (concept edges): 1 candidates -> kept pre:for_loop->loop_scope (1.00)
    pre:for_loop->loop_scope -> not applied (0.00) ""
  kept: pre:loop_variable->loop_control [broken, tier 0, 0.52], pre:loop_control->for_loop [broken, tier 0, 0.28]
  clause coverage (rule edges): c1 <- mis:loop_control->LoopStepAlwaysOne; c2 <- mis:loop_control->LoopStepAlwaysOne; c3 <- mis:loop_control->LoopStepAlwaysOne
  held: mis:for_loop->LoopStepAlwaysOne; filed at the dependent concept: mis:loop_control->LoopStepAlwaysOne
  shadows: mis:loop_control->LoopStepAlwaysOne (shadow of mis:for_loop->LoopStepAlwaysOne)
  root-cause walk: held on ['for_loop'], broken at [] (consequences: pre:loop_variable->loop_control, pre:loop_control->for_loop), prerequisites {'compound_assignment': ['assignment'], 'boolean_expression': ['comparison_operators'], 'comparison_operators': ['expression'], 'loop_scope': ['for_loop'], 'accumulator_pattern': ['loop_body'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable'], 'control_flow': ['statement'], 'println': ['statement']}
  level for_loop: L0 via misconception "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9"
  level loop_variable: L2 via output_prediction "so i goes 0, 1, 2 and; so on up to 9"
```

## 8. Full diagnosis JSON
```json
{
 "scenario": "MY14",
 "settings": {
  "width": 3,
  "depth": 3,
  "prune_tools": "llm",
  "model": "claude-opus-5-5",
  "backend": "claude-cli"
 },
 "clauses": [
  "A for loop moves i on by one each pass",
  "so i goes 0, 1, 2 and",
  "so on up to 9"
 ],
 "start_concepts": [
  "loop_control",
  "for_loop",
  "loop_variable"
 ],
 "held_misconceptions": [
  {
   "concept": "for_loop",
   "misconception": "LoopStepAlwaysOne",
   "kind": "misconception",
   "quote": "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9",
   "score": 0.57
  }
 ],
 "error_evidence": [
  {
   "concept": "loop_control",
   "error": "WrongIterationCount",
   "quote": "so i goes 0, 1, 2 and; so on up to 9"
  }
 ],
 "shadowed": [
  {
   "concept": "loop_control",
   "misconception": "LoopStepAlwaysOne",
   "shadow_of": "mis:for_loop->LoopStepAlwaysOne",
   "quote": "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9",
   "score": 0.57
  }
 ],
 "broken_edges": [
  {
   "edge": "pre:loop_variable->loop_control",
   "quote": "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9",
   "score": 0.52,
   "consequence_of": "mis:loop_control->LoopStepAlwaysOne"
  },
  {
   "edge": "pre:loop_control->for_loop",
   "quote": "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9",
   "score": 0.28,
   "consequence_of": "mis:loop_control->LoopStepAlwaysOne"
  }
 ],
 "root_cause": {
  "concept": "for_loop",
  "misconception": "LoopStepAlwaysOne"
 },
 "levels": {
  "for_loop": {
   "level": "L0",
   "way": "misconception",
   "misconception": "LoopStepAlwaysOne",
   "quote": "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9",
   "edge": "mis:for_loop->LoopStepAlwaysOne",
   "rule": "wrong rule: A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--). Right rule: The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i *= 2, ...).",
   "source": "level_mis_links"
  },
  "loop_variable": {
   "level": "L2",
   "way": "output_prediction",
   "quote": "so i goes 0, 1, 2 and; so on up to 9",
   "edge": "lvl:loop_variable@L2#1",
   "source": "level_way",
   "also_shown": [
    "L2 one_step_execution"
   ]
  }
 },
 "overall_level": "L0",
 "paths": [
  {
   "depth": 1,
   "source": "loop_control",
   "edge": "mis:loop_control->LoopStepAlwaysOne",
   "target": "LoopStepAlwaysOne",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9",
   "confidence": 0.95,
   "prune_score": 0.6,
   "score": 0.57,
   "logic": "A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--).",
   "twin_logic": "The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i *= 2, ...)."
  },
  {
   "depth": 1,
   "source": "for_loop",
   "edge": "mis:for_loop->LoopStepAlwaysOne",
   "target": "LoopStepAlwaysOne",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9",
   "confidence": 0.95,
   "prune_score": 0.6,
   "score": 0.57,
   "logic": "A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--).",
   "twin_logic": "The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i *= 2, ...)."
  },
  {
   "depth": 1,
   "source": "loop_control",
   "edge": "err:loop_control->WrongIterationCount",
   "target": "WrongIterationCount",
   "kind": "error",
   "label": "held",
   "clauses": [
    2,
    3
   ],
   "quote": "so i goes 0, 1, 2 and; so on up to 9",
   "confidence": 0.6,
   "prune_score": 0.15,
   "score": 0.09,
   "logic": "Updates the loop counter so that the loop runs the wrong number of times.",
   "twin_logic": "The init, test and update together decide the number of passes; trace them to check the count."
  },
  {
   "depth": 2,
   "source": "loop_control",
   "edge": "pre:loop_variable->loop_control",
   "target": "loop_variable",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9",
   "confidence": 0.8,
   "prune_score": 0.65,
   "score": 0.52,
   "logic": "The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.",
   "twin_logic": null,
   "consequence_of": "mis:loop_control->LoopStepAlwaysOne"
  },
  {
   "depth": 2,
   "source": "loop_control",
   "edge": "pre:loop_control->for_loop",
   "target": "for_loop",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9",
   "confidence": 0.8,
   "prune_score": 0.35,
   "score": 0.28,
   "logic": "The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.",
   "twin_logic": null,
   "consequence_of": "mis:loop_control->LoopStepAlwaysOne"
  }
 ],
 "evidence": [
  {
   "depth": 1,
   "source": "loop_control",
   "edge": "mis:loop_control->LoopStepAlwaysOne",
   "target": "LoopStepAlwaysOne",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9",
   "confidence": 0.95,
   "prune_score": 0.6,
   "score": 0.57,
   "logic": "A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--).",
   "twin_logic": "The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i *= 2, ...)."
  },
  {
   "depth": 1,
   "source": "loop_control",
   "edge": "err:loop_control->WrongIterationCount",
   "target": "WrongIterationCount",
   "kind": "error",
   "label": "held",
   "clauses": [
    2,
    3
   ],
   "quote": "so i goes 0, 1, 2 and; so on up to 9",
   "confidence": 0.6,
   "prune_score": 0.15,
   "score": 0.09,
   "logic": "Updates the loop counter so that the loop runs the wrong number of times.",
   "twin_logic": "The init, test and update together decide the number of passes; trace them to check the count."
  },
  {
   "depth": 1,
   "source": "for_loop",
   "edge": "mis:for_loop->LoopStepAlwaysOne",
   "target": "LoopStepAlwaysOne",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9",
   "confidence": 0.95,
   "prune_score": 0.6,
   "score": 0.57,
   "logic": "A loop variable always goes up or down by 1, whatever the update says (so i = i - 4 is read as i--).",
   "twin_logic": "The loop variable changes exactly as the update expression says (i += 2, i = i - 4, i *= 2, ...)."
  },
  {
   "depth": 1,
   "source": "loop_variable",
   "edge": "mis:loop_variable->ForInitRepeats",
   "target": "ForInitRepeats",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    2,
    3
   ],
   "quote": "so i goes 0, 1, 2 and; so on up to 9",
   "confidence": 0.6,
   "prune_score": 0.15,
   "score": 0.09,
   "logic": "The initialization of a for loop runs again after a pass of the body.",
   "twin_logic": "The initialization runs exactly once, before the first condition test."
  },
  {
   "depth": 1,
   "source": "loop_variable",
   "edge": "lvl:loop_variable@L2#1",
   "target": "loop_variable@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3
   ],
   "quote": "so i goes 0, 1, 2 and; so on up to 9",
   "confidence": 0.7,
   "prune_score": 0.4,
   "score": 0.28,
   "logic": "Across passes the loop variable takes a predictable sequence of values, e.g. 4, 5, ..., 10 in TenHellos, and after a while loop it holds the first value that failed the test (11).",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "loop_variable",
   "edge": "lvl:loop_variable@L2#2",
   "target": "loop_variable@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2
   ],
   "quote": "A for loop moves i on by one each pass; so i goes 0, 1, 2 and",
   "confidence": 0.7,
   "prune_score": 0.25,
   "score": 0.175,
   "logic": "One update changes only the loop variable (i = i + 1 turns 4 into 5); one test reads it and yields true or false; an assignment to it in the body changes what the next test sees.",
   "twin_logic": null,
   "level": "L2",
   "way": "one_step_execution"
  },
  {
   "depth": 2,
   "source": "loop_control",
   "edge": "pre:loop_variable->loop_control",
   "target": "loop_variable",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9",
   "confidence": 0.8,
   "prune_score": 0.65,
   "score": 0.52,
   "logic": "The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.",
   "twin_logic": null,
   "consequence_of": "mis:loop_control->LoopStepAlwaysOne"
  },
  {
   "depth": 2,
   "source": "loop_control",
   "edge": "pre:loop_control->for_loop",
   "target": "for_loop",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "A for loop moves i on by one each pass; so i goes 0, 1, 2 and; so on up to 9",
   "confidence": 0.8,
   "prune_score": 0.35,
   "score": 0.28,
   "logic": "The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.",
   "twin_logic": null,
   "consequence_of": "mis:loop_control->LoopStepAlwaysOne"
  }
 ],
 "clause_coverage": {
  "A for loop moves i on by one each pass": "mis:loop_control->LoopStepAlwaysOne",
  "so i goes 0, 1, 2 and": "mis:loop_control->LoopStepAlwaysOne",
  "so on up to 9": "mis:loop_control->LoopStepAlwaysOne"
 },
 "unexplained_clauses": [],
 "stop_reason": "sufficient",
 "depth_reached": 2,
 "llm_calls": 0,
 "llm_cache_hits": 23,
 "llm_calls_by_step": {
  "prune": 8,
  "label": 15
 }
}
```
