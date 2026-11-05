# Think on the Graph: every output of the run MY33
## 0. Input
Program:
```java
int n = 10;
do {
    System.out.println(n);
    n++;
} while (n < 5);
```
Question: How many times does the body run? Explain your reasoning.

Student's answer: Zero times. 10 < 5 is false, so the loop never starts.
Settings: width 3, depth 3, prune llm, backend claude-cli, model claude-opus-5-5
## 1. Stage 1: the subgraph G from the code (no model)
Masked code (string and char literals and comments blanked; this is what the patterns see):
```
int n = 10;
do {
    System.out.println(n);
    n++;
} while (n < 5);
```
Which code text tagged which concept (a generic concept fires on almost any Java line; it starts the walk only if the answer repeats its tag):
| concept | generic | channel | matched text | line |
|---|---|---|---|---|
| assignment | True | pattern | '=' | 1 |
| boolean_expression | False | pattern | 'while (' | 5 |
| comparison_operators | False | pattern | '} while (n <' | 5 |
| control_flow | False | pattern | 'while (' | 5 |
| control_flow | False | pattern | 'do {' | 2 |
| do_while_loop | False | pattern | 'do {' | 2 |
| do_while_loop | False | pattern | 'do' | 2 |
| do_while_loop | False | signal | 'do {' | 2 |
| expression | True | pattern | 'n <' | 5 |
| expression | True | pattern | '= 10;' | 1 |
| increment_operators | False | pattern | '++' | 4 |
| loop_body | False | pattern | 'while (' | 5 |
| loop_body | False | pattern | 'do {' | 2 |
| loop_control | False | pattern | 'while (n <' | 5 |
| loop_variable | False | pattern | 'do {\n    System.out.println(n);\n    n++;\n} while (n' | 2 |
| println | False | pattern | 'System.out.println(' | 3 |
| statement | True | pattern | ';' | 1 |

G: 12 concept nodes (3 generic), 10 concept edges, 97 misconception / error edges, 79 misconception / error nodes, 60 level nodes, 108 level-misconception links, 2 connected piece(s).
Note: concept nodes form 2 pieces (the KG has no edge between them): assignment,boolean_expression,comparison_operators,do_while_loop,expression,increment_operators,loop_body,loop_control,loop_variable | control_flow,println,statement

Concept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):
| edge | type | rule (logic) |
|---|---|---|
| par:assignment~comparison_operators | parallel | x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands. |
| pre:assignment->increment_operators | prerequisite | i++ is shorthand for the assignment i = i + 1. |
| pre:comparison_operators->boolean_expression | prerequisite | A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making. |
| pre:do_while_loop->loop_body | prerequisite | The block between do and while is the loop body; it runs first and is repeated while the condition holds. |
| pre:do_while_loop->loop_control | prerequisite | A do-while loop has the same control parts as a while loop (the variable set before, the condition, the update in the body); only the test is moved after the body. |
| pre:expression->comparison_operators | prerequisite | Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b. |
| pre:loop_control->increment_operators | prerequisite | The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update. |
| pre:loop_variable->loop_control | prerequisite | The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |
| pre:statement->control_flow | prerequisite | Control flow is the order in which statements run. |
| pre:statement->println | prerequisite | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |

Misconception / error edges per concept (count), and level ways per concept (count):
| concept | misconception / error edges | level ways (L1-L4 + L0 non-misconception) |
|---|---|---|
| assignment | 15 | 24 |
| boolean_expression | 8 | 19 |
| comparison_operators | 8 | 20 |
| control_flow | 11 | 15 |
| do_while_loop | 1 | 14 |
| expression | 8 | 19 |
| increment_operators | 5 | 16 |
| loop_body | 12 | 14 |
| loop_control | 11 | 19 |
| loop_variable | 7 | 13 |
| println | 6 | 17 |
| statement | 5 | 19 |

Figure 1: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY33_figure01.png

Figure 2: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY33_figure02.png

## 2. Clauses and start concepts (no model)
The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):
| clause | text |
|---|---|
| c1 | Zero times |
| c2 | 10 < 5 is false |
| c3 | so the loop never starts |

start: BM25 of the answer against each tagged concept: do_while_loop 7.21 (hits 3), loop_body 5.84 (hits 2), loop_control 5.71 (hits 1), println 4.25 (hits 1), boolean_expression 3.70 (hits 1), control_flow 3.49 (hits 2), loop_variable 3.42 (hits 1), comparison_operators 3.04 (hits 1), increment_operators 1.31 (hits 1)

start: chosen do_while_loop, loop_body, loop_control

start concepts (3): do_while_loop, loop_body, loop_control

Start concepts: do_while_loop, loop_body, loop_control

Figure 3: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY33_figure03.png

## 3. The walk, depth by depth
At each depth, for each current concept: the edges offered (a concept entering as a start concept offers its misconception / error edges and its level ways, as two families; otherwise it offers its concept edges), the prune prompt and the model's reply, then the label prompt(s) and the model's reply, parsed into label / clauses / confidence. Score = prune score x confidence.

### Depth 1: current concepts 'do_while_loop', 'loop_body', 'loop_control'

#### do_while_loop, misconceptions: 1 edges offered
Edges offered:
| edge |
|---|
| mis:do_while_loop->DoWhileTestsFirst \| wrong rule: A do-while whose condition starts false runs its body zero times. \| right rule: The statements within the do block are always executed at least once. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:do_while_loop->DoWhileTestsFirst (Score: 1.0)}
```
Kept by pruning: mis:do_while_loop->DoWhileTestsFirst (1.00)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:do_while_loop->DoWhileTestsFirst \| wrong rule: A do-while whose condition starts false runs its body zero times. \| right rule: The statements within the do block are always executed at least once. |
Model's reply:
```
mis:do_while_loop->DoWhileTestsFirst | held | clauses: 1, 2, 3 | confidence: 0.97
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:do_while_loop->DoWhileTestsFirst | held | 1.0 | 0.97 | 0.97 | c1, c2, c3 | Zero times; 10 < 5 is false; so the loop never starts |

#### do_while_loop, level ways: 14 edges offered
Edges offered:
| edge |
|---|
| lvl:do_while_loop@L0#0 \| level L0 way everyday_reading: Folk meaning: in English 'do X while Y' means do X during the time that Y holds, with Y watched continuously, as in the 'while demon'. In Java the condition is tested only at the bottom, after each complete pass of the body, and the first pass always runs. |
| lvl:do_while_loop@L0#2 \| level L0 way inconsistent_trace: Applies the LT rule unevenly: on a trace, the condition is tested before the first pass on some runs (as for while) and after it on others, or one more pass is run after the condition becomes false. The traced number of passes is off by one. (here mixing in: "A do-while whose condition starts false runs its body zero times") |
| lvl:do_while_loop@L1#0 \| level L1 way names_the_element: Loop statement: `do { body } while (cond);` is a loop whose test comes after the body, so the body runs one or more times. |
| lvl:do_while_loop@L1#1 \| level L1 way states_the_rule: `do { <statements> } while (<boolean expression>);` (note the final semicolon) means the same as the corresponding while loop except that the first test of the condition is omitted. (Spec: JLS §14.13.) |
| lvl:do_while_loop@L2#0 \| level L2 way line_by_line_trace: Order: execute the body; evaluate the condition; if true, execute the body again and re-test; stop the first time the condition is false at the bottom test. |
| lvl:do_while_loop@L2#1 \| level L2 way output_prediction: do-while produces no value. Its result is the state after the last pass. In the unit-disk example, x and y end inside the disk after about 4/π ≈ 1.27 passes on average. |
| lvl:do_while_loop@L2#2 \| level L2 way one_step_execution: One pass runs every statement of the body once (e.g. new random x and y) and then evaluates the condition, a boolean that decides whether another pass follows. The test changes nothing unless it has side effects. |
| lvl:do_while_loop@L3#0 \| level L3 way relation_to_neighbour: do { S } while (c); equals `S; while (c) { S }`. If c is initially true it behaves exactly like `while (c) { S }`; if c is initially false it still runs S once where the while runs it zero times. |
| lvl:do_while_loop@L3#1 \| level L3 way purpose_of_the_whole: Plan: generate-and-test (rejection sampling) or read-then-validate. Produce a candidate, test it, and repeat until it is acceptable, e.g. a random point in the unit disk. |
| lvl:do_while_loop@L4#0 \| level L4 way predict_a_change: Converting do-while to while keeps behaviour whenever the condition is true before the first pass, and breaks it (0 passes vs 1) when it is false. Moving the body's variables out of the block doesn't change the passes, but it is needed for the condition to see them. |
| lvl:do_while_loop@L4#1 \| level L4 way transfer_to_a_new_program: Use do-while when the body must run at least once before the test makes sense: generate-and-reject, prompt-and-validate, or a menu loop. Use while when zero passes must be possible, and for when there is an index with initialise/test/increment. |
| lvl:do_while_loop@L4#2 \| level L4 way diagnose_an_error: rule broken: A variable declared inside the do block is out of scope in the while condition. Kind: compile-time. Trigger class: `do { double x = ...; } while (x > 1.0);` (cannot find symbol x): declare x before the do. |
| lvl:do_while_loop@L4#3 \| level L4 way diagnose_an_error: rule broken: The do-while statement ends with a semicolon after the condition. Kind: compile-time. Trigger class: Omitting the `;` after `while (cond)` (';' expected). |
| lvl:do_while_loop@L4#4 \| level L4 way diagnose_an_error: rule broken: The body runs at least once even if the condition is false. Kind: silent logic error. Trigger class: Using do-while for a task that must allow zero passes (e.g. processing an empty input or N = 0): one spurious pass runs. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:do_while_loop@L0#2 (Score: 0.5)}
{lvl:do_while_loop@L0#0 (Score: 0.3)}
{lvl:do_while_loop@L3#0 (Score: 0.2)}
```
Kept by pruning: lvl:do_while_loop@L0#2 (0.50), lvl:do_while_loop@L0#0 (0.30), lvl:do_while_loop@L3#0 (0.20)

Label prompt for level way lvl:do_while_loop@L0#2 (the model saw only the concept, the way's name 'inconsistent trace' and its text; no level):
> Applies the LT rule unevenly: on a trace, the condition is tested before the first pass on some runs (as for while) and after it on others, or one more pass is run after the condition becomes false. The traced number of passes is off by one. (here mixing in: "A do-while whose condition starts false runs its body zero times")

Model's reply:
```
Label: shown
Clauses: 1, 2, 3
Confidence: 0.75
```

Label prompt for level way lvl:do_while_loop@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: in English 'do X while Y' means do X during the time that Y holds, with Y watched continuously, as in the 'while demon'. In Java the condition is tested only at the bottom, after each complete pass of the body, and the first pass always runs.

Model's reply:
```
Label: shown
Clauses: 1, 2, 3
Confidence: 0.85
```

Label prompt for level way lvl:do_while_loop@L3#0 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> do { S } while (c); equals `S; while (c) { S }`. If c is initially true it behaves exactly like `while (c) { S }`; if c is initially false it still runs S once where the while runs it zero times.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:do_while_loop@L0#2 | shown | 0.5 | 0.75 | 0.38 | c1, c2, c3 | Zero times; 10 < 5 is false; so the loop never starts |
| lvl:do_while_loop@L0#0 | shown | 0.3 | 0.85 | 0.26 | c1, c2, c3 | Zero times; 10 < 5 is false; so the loop never starts |
| lvl:do_while_loop@L3#0 | not applied |  |  | 0.0 |  |  |

#### loop_body, misconceptions: 12 edges offered
Edges offered:
| edge |
|---|
| err:loop_body->BracelessMultiStatementBody \| wrong rule: Indenting several statements under an if or for makes them all part of its body, even without braces. \| right rule: Without braces only the first statement belongs to the if/for; the rest run once, after it. |
| mis:loop_body->ComputerFillsInIntent \| wrong rule: The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. \| right rule: The computer executes only what the code states; every needed step and value must be written. |
| mis:loop_body->ForLoopPartSkipped \| wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). \| right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start. |
| mis:loop_body->IfInLoopUnchecked \| wrong rule: An if inside a loop body runs its branch on every pass without testing its condition. \| right rule: The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true. |
| mis:loop_body->LoopBodyAlwaysOnce \| wrong rule: The loop body always runs at least once, even if the condition is false at the start. \| right rule: A while or for body runs zero times when the condition is false at the start. |
| mis:loop_body->LoopBodyStatementOutsideLoop \| wrong rule: Some statements inside the braces of a loop body are not repeated; they run once, before or after the loop. \| right rule: Every statement inside the loop braces is part of the body and runs on every pass. |
| mis:loop_body->LoopCountIsStatementCount \| wrong rule: The repeat count of a counted loop says how many of the body statements are executed. \| right rule: The repeat count is how many times the whole body runs; every pass runs all body statements. |
| mis:loop_body->LoopOutputSameEachPass \| wrong rule: A loop prints the same thing on every pass; the changing loop variable does not affect what the body does. \| right rule: The body uses the current value of the loop variable, so its output can differ on each pass. |
| mis:loop_body->LoopRunsStatementsSeparately \| wrong rule: A loop runs its first body statement all N times, then its second body statement all N times. \| right rule: Each pass runs the whole body in order, so the body statements interleave: S1, S2, S1, S2, ... |
| mis:loop_body->StateChangeIgnoredAcrossPasses \| wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. \| right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones. |
| mis:loop_body->StatementAfterLoopInBody \| wrong rule: A statement written after the loop is repeated with the loop body. \| right rule: The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends. |
| mis:loop_body->WhileStopsMidBody \| wrong rule: The loop stops the moment the condition becomes false, even in the middle of the body. \| right rule: The condition is tested only before each pass, so the whole body finishes before the loop can stop. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:loop_body->LoopBodyAlwaysOnce (0.70), mis:loop_body->ForLoopPartSkipped (0.15), mis:loop_body->WhileStopsMidBody (0.15)
```
Kept by pruning: mis:loop_body->LoopBodyAlwaysOnce (0.70), mis:loop_body->ForLoopPartSkipped (0.15), mis:loop_body->WhileStopsMidBody (0.15)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:loop_body->LoopBodyAlwaysOnce \| wrong rule: The loop body always runs at least once, even if the condition is false at the start. \| right rule: A while or for body runs zero times when the condition is false at the start. |
| mis:loop_body->ForLoopPartSkipped \| wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). \| right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start. |
| mis:loop_body->WhileStopsMidBody \| wrong rule: The loop stops the moment the condition becomes false, even in the middle of the body. \| right rule: The condition is tested only before each pass, so the whole body finishes before the loop can stop. |
Model's reply:
```
mis:loop_body->LoopBodyAlwaysOnce | correct | clauses: 1, 2, 3 | confidence: 0.6
mis:loop_body->ForLoopPartSkipped | not applied | clauses: none | confidence: 0.8
mis:loop_body->WhileStopsMidBody | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:loop_body->LoopBodyAlwaysOnce | correct | 0.7 | 0.6 | 0.42 | c1, c2, c3 | Zero times; 10 < 5 is false; so the loop never starts |
| mis:loop_body->ForLoopPartSkipped | not applied |  |  | 0.0 |  |  |
| mis:loop_body->WhileStopsMidBody | not applied |  |  | 0.0 |  |  |

#### loop_body, level ways: 14 edges offered
Edges offered:
| edge |
|---|
| lvl:loop_body@L0#0 \| level L0 way everyday_reading: Folk meaning: an everyday 'repeat this' instruction can be read loosely - a helper fills in missing steps, does each step N times in turn, or stops partway. A Java loop body is exactly the statements inside its braces (or one statement), all executed in order on every pass. |
| lvl:loop_body@L0#6 \| level L0 way inconsistent_trace: Applies the body rule (LT) unevenly: runs all body statements on some passes but only some on others, includes the statement after the loop on some passes, or uses stale values from the first pass later. (here mixing in: "The loop body always runs at least once, even if the condition is false at the start") |
| lvl:loop_body@L1#0 \| level L1 way names_the_element: The loop body is the statement block that a loop repeats on each pass. |
| lvl:loop_body@L1#1 \| level L1 way states_the_rule: The body is the block after the loop header; braces are optional only if it is a single statement, in which case only that one statement is repeated. |
| lvl:loop_body@L2#0 \| level L2 way line_by_line_trace: On each pass the body's statements run in order, first to last, after a true test (and, in a for loop, before the update); the next pass starts from the state left by this one. |
| lvl:loop_body@L2#1 \| level L2 way output_prediction: The body's output on each pass depends on the current values, so successive passes can print different lines: TenHellos prints '4th Hello', '5th Hello', ...; the number of executions of each body statement equals the number of passes. |
| lvl:loop_body@L2#2 \| level L2 way one_step_execution: One pass of the body changes exactly the variables it assigns (e.g. print i and v, double v, increment i) and these changes carry into the next test and pass. |
| lvl:loop_body@L3#0 \| level L3 way relation_to_neighbour: The accumulator update (sum += x) is placed inside the body so it runs once per pass, while the accumulator is declared and initialized before the loop. |
| lvl:loop_body@L3#1 \| level L3 way relation_to_neighbour: count++ sits inside the body, often under an if, so it runs once on each pass that matches; the counter is declared before the loop. |
| lvl:loop_body@L3#2 \| level L3 way relation_to_neighbour: The body is what the while repeats; the condition is tested only between complete executions of it. |
| lvl:loop_body@L3#3 \| level L3 way purpose_of_the_whole: Plan: the body is the 'process one item / one step' part of a loop plan: each pass performs the same process on a new value (next element, next bet, next term). |
| lvl:loop_body@L4#0 \| level L4 way predict_a_change: Moving a statement from inside the body to after the loop changes it from running once per pass to once in total (and vice versa); reordering two body statements that share a variable changes the results (e.g. increment before vs after use). |
| lvl:loop_body@L4#1 \| level L4 way diagnose_an_error: rule broken: Without braces, the body of an if, while or for is exactly one statement; indentation does not add statements to it. Kind: silent logic error. Trigger class: A braceless header followed by two or more indented statements: only the first is controlled, the others run once, after the if/loop, on every input. |
| lvl:loop_body@L4#2 \| level L4 way transfer_to_a_new_program: Put inside the body exactly what must happen once per pass; put set-up before the loop and final reporting after it. Always brace a multi-statement body. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:loop_body@L3#2 (Score: 0.5)}
{lvl:loop_body@L0#6 (Score: 0.3)}
{lvl:loop_body@L2#0 (Score: 0.2)}
```
Kept by pruning: lvl:loop_body@L3#2 (0.50), lvl:loop_body@L0#6 (0.30), lvl:loop_body@L2#0 (0.20)

Label prompt for level way lvl:loop_body@L3#2 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> The body is what the while repeats; the condition is tested only between complete executions of it.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.92
```

Label prompt for level way lvl:loop_body@L0#6 (the model saw only the concept, the way's name 'inconsistent trace' and its text; no level):
> Applies the body rule (LT) unevenly: runs all body statements on some passes but only some on others, includes the statement after the loop on some passes, or uses stale values from the first pass later. (here mixing in: "The loop body always runs at least once, even if the condition is false at the start")

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:loop_body@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> On each pass the body's statements run in order, first to last, after a true test (and, in a for loop, before the update); the next pass starts from the state left by this one.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:loop_body@L3#2 | not applied |  |  | 0.0 |  |  |
| lvl:loop_body@L0#6 | not applied |  |  | 0.0 |  |  |
| lvl:loop_body@L2#0 | not applied |  |  | 0.0 |  |  |

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
err:loop_control->WrongIterationCount (0.45), mis:loop_control->ForLoopPartSkipped (0.30), mis:loop_control->IdiomOverridesCode (0.25)
```
Kept by pruning: err:loop_control->WrongIterationCount (0.45), mis:loop_control->ForLoopPartSkipped (0.30), mis:loop_control->IdiomOverridesCode (0.25)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| err:loop_control->WrongIterationCount \| wrong rule: Updates the loop counter so that the loop runs the wrong number of times. \| right rule: The init, test and update together decide the number of passes; trace them to check the count. |
| mis:loop_control->ForLoopPartSkipped \| wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). \| right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start. |
| mis:loop_control->IdiomOverridesCode \| wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. |
Model's reply:
```
err:loop_control->WrongIterationCount | not applied | clauses: none | confidence: 0.6
mis:loop_control->ForLoopPartSkipped | not applied | clauses: none | confidence: 0.55
mis:loop_control->IdiomOverridesCode | not applied | clauses: none | confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| err:loop_control->WrongIterationCount | not applied |  |  | 0.0 |  |  |
| mis:loop_control->ForLoopPartSkipped | not applied |  |  | 0.0 |  |  |
| mis:loop_control->IdiomOverridesCode | not applied |  |  | 0.0 |  |  |

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
{lvl:loop_control@L1#1 (Score: 0.5)}
{lvl:loop_control@L0#3 (Score: 0.3)}
{lvl:loop_control@L2#0 (Score: 0.2)}
```
Kept by pruning: lvl:loop_control@L1#1 (0.50), lvl:loop_control@L0#3 (0.30), lvl:loop_control@L2#0 (0.20)

Label prompt for level way lvl:loop_control@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> Initialize an index variable, test a loop-continuation condition on it before each pass, and increment it as the last action of each pass; for (<initialize>; <boolean expression>; <increment>) packages the three. Choosing the loop: for when the passes are counted by an index, while when the loop runs until a condition changes, do-while when the body must run at least once; any one can be rewritten as another, so choose the clearest.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:loop_control@L0#3 (the model saw only the concept, the way's name 'inconsistent trace' and its text; no level):
> Applies the init-test-update rule (LT) unevenly: updates before the body on some passes, skips the test or the update on a pass, or re-runs the init. (here mixing in: "++i in the for-update runs before the body each pass")

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.8
```

Label prompt for level way lvl:loop_control@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> init (once) -> test -> body -> update -> test -> body -> update ... -> test false -> exit.

Model's reply:
```
Label: shown
Clauses: 2, 3
Confidence: 0.75
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:loop_control@L1#1 | not applied |  |  | 0.0 |  |  |
| lvl:loop_control@L0#3 | not applied |  |  | 0.0 |  |  |
| lvl:loop_control@L2#0 | shown | 0.2 | 0.75 | 0.15 | c2, c3 | 10 < 5 is false; so the loop never starts |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:do_while_loop->DoWhileTestsFirst [held, tier 0, 0.97], mis:loop_body->LoopBodyAlwaysOnce [correct, tier 2, 0.42], lvl:do_while_loop@L0#2 [shown, tier 2, 0.38]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | Zero times | mis:do_while_loop->DoWhileTestsFirst |
| c2 | 10 < 5 is false | mis:do_while_loop->DoWhileTestsFirst |
| c3 | so the loop never starts | mis:do_while_loop->DoWhileTestsFirst |

**Graph check, not yet read (the walk may not stop while these remain):** pre:do_while_loop->loop_body, pre:do_while_loop->loop_control, pre:loop_control->increment_operators, pre:loop_variable->loop_control

Figure 4 (the graph after depth 1): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY33_figure04.png

### Depth 2: current concepts 'do_while_loop', 'loop_body', 'loop_control'

#### do_while_loop, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| pre:do_while_loop->loop_body \| rule: The block between do and while is the loop body; it runs first and is repeated while the condition holds. |
| pre:do_while_loop->loop_control \| rule: A do-while loop has the same control parts as a while loop (the variable set before, the condition, the update in the body); only the test is moved after the body. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:do_while_loop->loop_control (Score: 0.55)}
{pre:do_while_loop->loop_body (Score: 0.45)}
```
Kept by pruning: pre:do_while_loop->loop_control (0.55), pre:do_while_loop->loop_body (0.45)

Label prompt for concept edge pre:do_while_loop->loop_control (do_while_loop -> loop_control, prerequisite):
> A do-while loop has the same control parts as a while loop (the variable set before, the condition, the update in the body); only the test is moved after the body.

Model's reply:
```
Label: broken
Clauses: 1, 2, 3
Confidence: 0.9
```

Label prompt for concept edge pre:do_while_loop->loop_body (do_while_loop -> loop_body, prerequisite):
> The block between do and while is the loop body; it runs first and is repeated while the condition holds.

Model's reply:
```
Label: broken
Clauses: 1, 3
Confidence: 0.93
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:do_while_loop->loop_control | broken | 0.55 | 0.9 | 0.5 | c1, c2, c3 | Zero times; 10 < 5 is false; so the loop never starts |
| pre:do_while_loop->loop_body | broken | 0.45 | 0.93 | 0.42 | c1, c3 | Zero times; so the loop never starts |

#### loop_control, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| pre:do_while_loop->loop_control \| rule: A do-while loop has the same control parts as a while loop (the variable set before, the condition, the update in the body); only the test is moved after the body. |
| pre:loop_control->increment_operators \| rule: The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update. |
| pre:loop_variable->loop_control \| rule: The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
pre:loop_variable->loop_control (0.85), pre:loop_control->increment_operators (0.15)
```
Kept by pruning: pre:loop_variable->loop_control (0.85), pre:loop_control->increment_operators (0.15)

Label prompt for concept edge pre:loop_variable->loop_control (loop_variable -> loop_control, prerequisite):
> The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.

Model's reply:
```
Label: confirmed
Clauses: 2
Confidence: 0.6
```

Label prompt for concept edge pre:loop_control->increment_operators (loop_control -> increment_operators, prerequisite):
> The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:loop_variable->loop_control | confirmed | 0.85 | 0.6 | 0.51 | c2 | 10 < 5 is false |
| pre:loop_control->increment_operators | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:do_while_loop->loop_control [broken, tier 0, 0.49], pre:do_while_loop->loop_body [broken, tier 0, 0.42], pre:loop_variable->loop_control [confirmed, tier 2, 0.51]

reached across pre:loop_variable->loop_control, entered next: loop_variable

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | Zero times | mis:do_while_loop->DoWhileTestsFirst |
| c2 | 10 < 5 is false | mis:do_while_loop->DoWhileTestsFirst |
| c3 | so the loop never starts | mis:do_while_loop->DoWhileTestsFirst |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of loop_variable

Figure 5 (the graph after depth 2): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY33_figure05.png

### Depth 3: current concepts 'loop_control', 'do_while_loop', 'loop_body', 'loop_variable'

#### loop_control, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:do_while_loop->loop_control \| rule: A do-while loop has the same control parts as a while loop (the variable set before, the condition, the update in the body); only the test is moved after the body. |
| pre:loop_control->increment_operators \| rule: The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update. |
| pre:loop_variable->loop_control \| rule: The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
pre:loop_control->increment_operators (1.00)
```
Kept by pruning: pre:loop_control->increment_operators (1.00)

Label prompt for concept edge pre:loop_control->increment_operators (loop_control -> increment_operators, prerequisite):
> The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:loop_control->increment_operators | not applied |  |  | 0.0 |  |  |

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
mis:loop_variable->BodyChangeIgnoredByCondition (0.50), mis:loop_variable->ForInitRepeats (0.30), mis:loop_variable->LoopVariableLimitsValues (0.20)
```
Kept by pruning: mis:loop_variable->BodyChangeIgnoredByCondition (0.50), mis:loop_variable->ForInitRepeats (0.30), mis:loop_variable->LoopVariableLimitsValues (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:loop_variable->BodyChangeIgnoredByCondition \| wrong rule: Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times. \| right rule: The condition is tested with the current value of the variable, including changes made in the body. |
| mis:loop_variable->ForInitRepeats \| wrong rule: The initialization of a for loop runs again after a pass of the body. \| right rule: The initialization runs exactly once, before the first condition test. |
| mis:loop_variable->LoopVariableLimitsValues \| wrong rule: The range of the loop variable limits the values that can be read or printed inside the loop. \| right rule: The loop variable only counts passes; other values read or printed in the body are not bounded by it. |
Model's reply:
```
mis:loop_variable->BodyChangeIgnoredByCondition | not applied | clauses: none | confidence: 0.85
mis:loop_variable->ForInitRepeats | not applied | clauses: none | confidence: 0.95
mis:loop_variable->LoopVariableLimitsValues | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:loop_variable->BodyChangeIgnoredByCondition | not applied |  |  | 0.0 |  |  |
| mis:loop_variable->ForInitRepeats | not applied |  |  | 0.0 |  |  |
| mis:loop_variable->LoopVariableLimitsValues | not applied |  |  | 0.0 |  |  |

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
{lvl:loop_variable@L1#1 (Score: 0.5)}
{lvl:loop_variable@L2#2 (Score: 0.3)}
{lvl:loop_variable@L3#0 (Score: 0.2)}
```
Kept by pruning: lvl:loop_variable@L1#1 (0.50), lvl:loop_variable@L2#2 (0.30), lvl:loop_variable@L3#0 (0.20)

Label prompt for level way lvl:loop_variable@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> The loop variable is set once by the initialization, tested by the continuation condition before each pass and updated (usually incremented) at the end of each pass; declared in a for header, it is not available after the loop.

Model's reply:
```
Label: shown
Clauses: 2, 3
Confidence: 0.6
```

Label prompt for level way lvl:loop_variable@L2#2 (the model saw only the concept, the way's name 'one step execution' and its text; no level):
> One update changes only the loop variable (i = i + 1 turns 4 into 5); one test reads it and yields true or false; an assignment to it in the body changes what the next test sees.

Model's reply:
```
Label: shown
Clauses: 2
Confidence: 0.7
```

Label prompt for level way lvl:loop_variable@L3#0 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.

Model's reply:
```
Label: shown
Clauses: 2
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:loop_variable@L1#1 | shown | 0.5 | 0.6 | 0.3 | c2, c3 | 10 < 5 is false; so the loop never starts |
| lvl:loop_variable@L2#2 | shown | 0.3 | 0.7 | 0.21 | c2 | 10 < 5 is false |
| lvl:loop_variable@L3#0 | shown | 0.2 | 0.6 | 0.12 | c2 | 10 < 5 is false |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

lvl:loop_variable@L1#1 [shown, tier 2, 0.30], lvl:loop_variable@L2#2 [shown, tier 2, 0.21], lvl:loop_variable@L3#0 [shown, tier 2, 0.12]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | Zero times | mis:do_while_loop->DoWhileTestsFirst |
| c2 | 10 < 5 is false | mis:do_while_loop->DoWhileTestsFirst |
| c3 | so the loop never starts | mis:do_while_loop->DoWhileTestsFirst |

Figure 6 (the graph after depth 3): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY33_figure06.png

## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on ['do_while_loop'], broken at [] (consequences: pre:do_while_loop->loop_control, pre:do_while_loop->loop_body), prerequisites {'increment_operators': ['assignment', 'loop_control'], 'boolean_expression': ['comparison_operators'], 'loop_body': ['do_while_loop'], 'loop_control': ['do_while_loop', 'loop_variable'], 'comparison_operators': ['expression'], 'control_flow': ['statement'], 'println': ['statement']}
- do_while_loop: L0 via misconception "Zero times; 10 < 5 is false; so the loop never starts"
- loop_control: L2 via line_by_line_trace "10 < 5 is false; so the loop never starts"
- loop_variable: L3 via relation_to_neighbour "10 < 5 is false"

**Stop:** sufficient at depth 3; prompts {'prune': 11, 'label': 21}, fresh model calls 0, cache hits 32

### Held misconceptions
| concept | misconception | kind | quote | score | shares_evidence_with |
|---|---|---|---|---|---|
| do_while_loop | DoWhileTestsFirst | misconception | Zero times; 10 < 5 is false; so the loop never starts | 0.97 |  |

### Broken concept edges
| edge | quote | score | consequence_of |
|---|---|---|---|
| pre:do_while_loop->loop_control | Zero times; 10 < 5 is false; so the loop never starts | 0.495 | mis:do_while_loop->DoWhileTestsFirst |
| pre:do_while_loop->loop_body | Zero times; so the loop never starts | 0.4185 | mis:do_while_loop->DoWhileTestsFirst |

### Root cause: do_while_loop / DoWhileTestsFirst

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| do_while_loop | L0 | misconception | DoWhileTestsFirst | level_mis_links | Zero times; 10 < 5 is false; so the loop never starts | wrong rule: A do-while whose condition starts false runs its body zero times. Right rule: The first test is omitted: the body always runs at least once, and the condition is checked only after each pass. |  |  |
| loop_control | L2 | line_by_line_trace |  | level_way | 10 < 5 is false; so the loop never starts |  |  |  |
| loop_variable | L3 | relation_to_neighbour |  | level_way | 10 < 5 is false |  | L2 one_step_execution, L1 states_the_rule |  |

### Overall level: L0

Clause coverage (final):
| clause | covered by |
|---|---|
| Zero times | mis:do_while_loop->DoWhileTestsFirst |
| 10 < 5 is false | mis:do_while_loop->DoWhileTestsFirst |
| so the loop never starts | mis:do_while_loop->DoWhileTestsFirst |

Figure 7 (final picture): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY33_figure07.png

## 5. Every labelled edge (the evidence list, kept or not)
| depth | source | edge | kind | label | prune_score | confidence | score | clauses | quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | do_while_loop | mis:do_while_loop->DoWhileTestsFirst | misconception | held | 1.0 | 0.97 | 0.97 | [1, 2, 3] | Zero times; 10 < 5 is false; so the loop never starts |
| 1 | do_while_loop | lvl:do_while_loop@L0#2 | level | shown | 0.5 | 0.75 | 0.375 | [1, 2, 3] | Zero times; 10 < 5 is false; so the loop never starts |
| 1 | do_while_loop | lvl:do_while_loop@L0#0 | level | shown | 0.3 | 0.85 | 0.255 | [1, 2, 3] | Zero times; 10 < 5 is false; so the loop never starts |
| 1 | loop_body | mis:loop_body->LoopBodyAlwaysOnce | misconception | correct | 0.7 | 0.6 | 0.42 | [1, 2, 3] | Zero times; 10 < 5 is false; so the loop never starts |
| 1 | loop_control | lvl:loop_control@L2#0 | level | shown | 0.2 | 0.75 | 0.15 | [2, 3] | 10 < 5 is false; so the loop never starts |
| 2 | do_while_loop | pre:do_while_loop->loop_control | prerequisite | broken | 0.55 | 0.9 | 0.495 | [1, 2, 3] | Zero times; 10 < 5 is false; so the loop never starts |
| 2 | do_while_loop | pre:do_while_loop->loop_body | prerequisite | broken | 0.45 | 0.93 | 0.4185 | [1, 3] | Zero times; so the loop never starts |
| 2 | loop_control | pre:loop_variable->loop_control | prerequisite | confirmed | 0.85 | 0.6 | 0.51 | [2] | 10 < 5 is false |
| 3 | loop_variable | lvl:loop_variable@L1#1 | level | shown | 0.5 | 0.6 | 0.3 | [2, 3] | 10 < 5 is false; so the loop never starts |
| 3 | loop_variable | lvl:loop_variable@L2#2 | level | shown | 0.3 | 0.7 | 0.21 | [2] | 10 < 5 is false |
| 3 | loop_variable | lvl:loop_variable@L3#0 | level | shown | 0.2 | 0.6 | 0.12 | [2] | 10 < 5 is false |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | do_while_loop | mis:do_while_loop->DoWhileTestsFirst | misconception | held | 0.97 | [1, 2, 3] |
| 1 | loop_body | mis:loop_body->LoopBodyAlwaysOnce | misconception | correct | 0.42 | [1, 2, 3] |
| 1 | do_while_loop | lvl:do_while_loop@L0#2 | level | shown | 0.375 | [1, 2, 3] |
| 2 | do_while_loop | pre:do_while_loop->loop_control | prerequisite | broken | 0.495 | [1, 2, 3] |
| 2 | do_while_loop | pre:do_while_loop->loop_body | prerequisite | broken | 0.4185 | [1, 3] |
| 2 | loop_control | pre:loop_variable->loop_control | prerequisite | confirmed | 0.51 | [2] |
| 3 | loop_variable | lvl:loop_variable@L1#1 | level | shown | 0.3 | [2, 3] |
| 3 | loop_variable | lvl:loop_variable@L2#2 | level | shown | 0.21 | [2] |
| 3 | loop_variable | lvl:loop_variable@L3#0 | level | shown | 0.12 | [2] |

## 7. Raw traversal log
```
clauses: Zero times | 10 < 5 is false | so the loop never starts
start: BM25 of the answer against each tagged concept: do_while_loop 7.21 (hits 3), loop_body 5.84 (hits 2), loop_control 5.71 (hits 1), println 4.25 (hits 1), boolean_expression 3.70 (hits 1), control_flow 3.49 (hits 2), loop_variable 3.42 (hits 1), comparison_operators 3.04 (hits 1), increment_operators 1.31 (hits 1)
start: chosen do_while_loop, loop_body, loop_control
start concepts (3): do_while_loop, loop_body, loop_control
--- depth 1: current concepts ['do_while_loop', 'loop_body', 'loop_control']
  do_while_loop (misconceptions): 1 candidates -> kept mis:do_while_loop->DoWhileTestsFirst (1.00)
    mis:do_while_loop->DoWhileTestsFirst -> held (0.97) "Zero times; 10 < 5 is false; so the loop never starts"
  do_while_loop (level ways): 14 candidates -> kept lvl:do_while_loop@L0#2 (0.50), lvl:do_while_loop@L0#0 (0.30), lvl:do_while_loop@L3#0 (0.20)
    lvl:do_while_loop@L0#2 -> shown (0.38) "Zero times; 10 < 5 is false; so the loop never starts"
    lvl:do_while_loop@L0#0 -> shown (0.26) "Zero times; 10 < 5 is false; so the loop never starts"
    lvl:do_while_loop@L3#0 -> not applied (0.00) ""
  loop_body (misconceptions): 12 candidates -> kept mis:loop_body->LoopBodyAlwaysOnce (0.70), mis:loop_body->ForLoopPartSkipped (0.15), mis:loop_body->WhileStopsMidBody (0.15)
    mis:loop_body->LoopBodyAlwaysOnce -> correct (0.42) "Zero times; 10 < 5 is false; so the loop never starts"
    mis:loop_body->ForLoopPartSkipped -> not applied (0.00) ""
    mis:loop_body->WhileStopsMidBody -> not applied (0.00) ""
  loop_body (level ways): 14 candidates -> kept lvl:loop_body@L3#2 (0.50), lvl:loop_body@L0#6 (0.30), lvl:loop_body@L2#0 (0.20)
    lvl:loop_body@L3#2 -> not applied (0.00) ""
    lvl:loop_body@L0#6 -> not applied (0.00) ""
    lvl:loop_body@L2#0 -> not applied (0.00) ""
  loop_control (misconceptions): 11 candidates -> kept err:loop_control->WrongIterationCount (0.45), mis:loop_control->ForLoopPartSkipped (0.30), mis:loop_control->IdiomOverridesCode (0.25)
    err:loop_control->WrongIterationCount -> not applied (0.00) ""
    mis:loop_control->ForLoopPartSkipped -> not applied (0.00) ""
    mis:loop_control->IdiomOverridesCode -> not applied (0.00) ""
  loop_control (level ways): 19 candidates -> kept lvl:loop_control@L1#1 (0.50), lvl:loop_control@L0#3 (0.30), lvl:loop_control@L2#0 (0.20)
    lvl:loop_control@L1#1 -> not applied (0.00) ""
    lvl:loop_control@L0#3 -> not applied (0.00) ""
    lvl:loop_control@L2#0 -> shown (0.15) "10 < 5 is false; so the loop never starts"
  kept: mis:do_while_loop->DoWhileTestsFirst [held, tier 0, 0.97], mis:loop_body->LoopBodyAlwaysOnce [correct, tier 2, 0.42], lvl:do_while_loop@L0#2 [shown, tier 2, 0.38]
  clause coverage: c1 <- mis:do_while_loop->DoWhileTestsFirst; c2 <- mis:do_while_loop->DoWhileTestsFirst; c3 <- mis:do_while_loop->DoWhileTestsFirst
  not yet read: pre:do_while_loop->loop_body, pre:do_while_loop->loop_control, pre:loop_control->increment_operators, pre:loop_variable->loop_control
--- depth 2: current concepts ['do_while_loop', 'loop_body', 'loop_control']
  do_while_loop (concept edges): 2 candidates -> kept pre:do_while_loop->loop_control (0.55), pre:do_while_loop->loop_body (0.45)
    pre:do_while_loop->loop_control -> broken (0.50) "Zero times; 10 < 5 is false; so the loop never starts"
    pre:do_while_loop->loop_body -> broken (0.42) "Zero times; so the loop never starts"
  loop_control (concept edges): 2 candidates -> kept pre:loop_variable->loop_control (0.85), pre:loop_control->increment_operators (0.15)
    pre:loop_variable->loop_control -> confirmed (0.51) "10 < 5 is false"
    pre:loop_control->increment_operators -> not applied (0.00) ""
  kept: pre:do_while_loop->loop_control [broken, tier 0, 0.49], pre:do_while_loop->loop_body [broken, tier 0, 0.42], pre:loop_variable->loop_control [confirmed, tier 2, 0.51]
  reached across pre:loop_variable->loop_control, entered next: loop_variable
  clause coverage: c1 <- mis:do_while_loop->DoWhileTestsFirst; c2 <- mis:do_while_loop->DoWhileTestsFirst; c3 <- mis:do_while_loop->DoWhileTestsFirst
  not yet read: own edges of loop_variable
--- depth 3: current concepts ['loop_control', 'do_while_loop', 'loop_body', 'loop_variable']
  loop_control (concept edges): 1 candidates -> kept pre:loop_control->increment_operators (1.00)
    pre:loop_control->increment_operators -> not applied (0.00) ""
  loop_variable (misconceptions): 7 candidates -> kept mis:loop_variable->BodyChangeIgnoredByCondition (0.50), mis:loop_variable->ForInitRepeats (0.30), mis:loop_variable->LoopVariableLimitsValues (0.20)
    mis:loop_variable->BodyChangeIgnoredByCondition -> not applied (0.00) ""
    mis:loop_variable->ForInitRepeats -> not applied (0.00) ""
    mis:loop_variable->LoopVariableLimitsValues -> not applied (0.00) ""
  loop_variable (level ways): 13 candidates -> kept lvl:loop_variable@L1#1 (0.50), lvl:loop_variable@L2#2 (0.30), lvl:loop_variable@L3#0 (0.20)
    lvl:loop_variable@L1#1 -> shown (0.30) "10 < 5 is false; so the loop never starts"
    lvl:loop_variable@L2#2 -> shown (0.21) "10 < 5 is false"
    lvl:loop_variable@L3#0 -> shown (0.12) "10 < 5 is false"
  kept: lvl:loop_variable@L1#1 [shown, tier 2, 0.30], lvl:loop_variable@L2#2 [shown, tier 2, 0.21], lvl:loop_variable@L3#0 [shown, tier 2, 0.12]
  clause coverage: c1 <- mis:do_while_loop->DoWhileTestsFirst; c2 <- mis:do_while_loop->DoWhileTestsFirst; c3 <- mis:do_while_loop->DoWhileTestsFirst
  root-cause walk: held on ['do_while_loop'], broken at [] (consequences: pre:do_while_loop->loop_control, pre:do_while_loop->loop_body), prerequisites {'increment_operators': ['assignment', 'loop_control'], 'boolean_expression': ['comparison_operators'], 'loop_body': ['do_while_loop'], 'loop_control': ['do_while_loop', 'loop_variable'], 'comparison_operators': ['expression'], 'control_flow': ['statement'], 'println': ['statement']}
  level do_while_loop: L0 via misconception "Zero times; 10 < 5 is false; so the loop never starts"
  level loop_control: L2 via line_by_line_trace "10 < 5 is false; so the loop never starts"
  level loop_variable: L3 via relation_to_neighbour "10 < 5 is false"
```

## 8. Full diagnosis JSON
```json
{
 "scenario": "MY33",
 "settings": {
  "width": 3,
  "depth": 3,
  "prune_tools": "llm",
  "model": "claude-opus-5-5",
  "backend": "claude-cli"
 },
 "clauses": [
  "Zero times",
  "10 < 5 is false",
  "so the loop never starts"
 ],
 "start_concepts": [
  "do_while_loop",
  "loop_body",
  "loop_control"
 ],
 "held_misconceptions": [
  {
   "concept": "do_while_loop",
   "misconception": "DoWhileTestsFirst",
   "kind": "misconception",
   "quote": "Zero times; 10 < 5 is false; so the loop never starts",
   "score": 0.97
  }
 ],
 "error_evidence": [],
 "shadowed": [],
 "broken_edges": [
  {
   "edge": "pre:do_while_loop->loop_control",
   "quote": "Zero times; 10 < 5 is false; so the loop never starts",
   "score": 0.495,
   "consequence_of": "mis:do_while_loop->DoWhileTestsFirst"
  },
  {
   "edge": "pre:do_while_loop->loop_body",
   "quote": "Zero times; so the loop never starts",
   "score": 0.4185,
   "consequence_of": "mis:do_while_loop->DoWhileTestsFirst"
  }
 ],
 "root_cause": {
  "concept": "do_while_loop",
  "misconception": "DoWhileTestsFirst"
 },
 "levels": {
  "do_while_loop": {
   "level": "L0",
   "way": "misconception",
   "misconception": "DoWhileTestsFirst",
   "quote": "Zero times; 10 < 5 is false; so the loop never starts",
   "edge": "mis:do_while_loop->DoWhileTestsFirst",
   "rule": "wrong rule: A do-while whose condition starts false runs its body zero times. Right rule: The first test is omitted: the body always runs at least once, and the condition is checked only after each pass.",
   "source": "level_mis_links"
  },
  "loop_control": {
   "level": "L2",
   "way": "line_by_line_trace",
   "quote": "10 < 5 is false; so the loop never starts",
   "edge": "lvl:loop_control@L2#0",
   "source": "level_way",
   "also_shown": []
  },
  "loop_variable": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "10 < 5 is false",
   "edge": "lvl:loop_variable@L3#0",
   "source": "level_way",
   "also_shown": [
    "L2 one_step_execution",
    "L1 states_the_rule"
   ]
  }
 },
 "overall_level": "L0",
 "paths": [
  {
   "depth": 1,
   "source": "do_while_loop",
   "edge": "mis:do_while_loop->DoWhileTestsFirst",
   "target": "DoWhileTestsFirst",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "Zero times; 10 < 5 is false; so the loop never starts",
   "confidence": 0.97,
   "prune_score": 1.0,
   "score": 0.97,
   "logic": "A do-while whose condition starts false runs its body zero times.",
   "twin_logic": "The statements within the do block are always executed at least once.",
   "role": "primary"
  },
  {
   "depth": 1,
   "source": "loop_body",
   "edge": "mis:loop_body->LoopBodyAlwaysOnce",
   "target": "LoopBodyAlwaysOnce",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "Zero times; 10 < 5 is false; so the loop never starts",
   "confidence": 0.6,
   "prune_score": 0.7,
   "score": 0.42,
   "logic": "The loop body always runs at least once, even if the condition is false at the start.",
   "twin_logic": "A while or for body runs zero times when the condition is false at the start.",
   "role": "context"
  },
  {
   "depth": 1,
   "source": "do_while_loop",
   "edge": "lvl:do_while_loop@L0#2",
   "target": "do_while_loop@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "Zero times; 10 < 5 is false; so the loop never starts",
   "confidence": 0.75,
   "prune_score": 0.5,
   "score": 0.375,
   "logic": "Applies the LT rule unevenly: on a trace, the condition is tested before the first pass on some runs (as for while) and after it on others, or one more pass is run after the condition becomes false. The traced number of passes is off by one. (here mixing in: \"A do-while whose condition starts false runs its body zero times\")",
   "twin_logic": null,
   "level": "L0",
   "way": "inconsistent_trace"
  },
  {
   "depth": 2,
   "source": "do_while_loop",
   "edge": "pre:do_while_loop->loop_control",
   "target": "loop_control",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "Zero times; 10 < 5 is false; so the loop never starts",
   "confidence": 0.9,
   "prune_score": 0.55,
   "score": 0.495,
   "logic": "A do-while loop has the same control parts as a while loop (the variable set before, the condition, the update in the body); only the test is moved after the body.",
   "twin_logic": null,
   "consequence_of": "mis:do_while_loop->DoWhileTestsFirst"
  },
  {
   "depth": 2,
   "source": "do_while_loop",
   "edge": "pre:do_while_loop->loop_body",
   "target": "loop_body",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    3
   ],
   "quote": "Zero times; so the loop never starts",
   "confidence": 0.93,
   "prune_score": 0.45,
   "score": 0.4185,
   "logic": "The block between do and while is the loop body; it runs first and is repeated while the condition holds.",
   "twin_logic": null,
   "consequence_of": "mis:do_while_loop->DoWhileTestsFirst"
  },
  {
   "depth": 2,
   "source": "loop_control",
   "edge": "pre:loop_variable->loop_control",
   "target": "loop_variable",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    2
   ],
   "quote": "10 < 5 is false",
   "confidence": 0.6,
   "prune_score": 0.85,
   "score": 0.51,
   "logic": "The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "loop_variable",
   "edge": "lvl:loop_variable@L1#1",
   "target": "loop_variable@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3
   ],
   "quote": "10 < 5 is false; so the loop never starts",
   "confidence": 0.6,
   "prune_score": 0.5,
   "score": 0.3,
   "logic": "The loop variable is set once by the initialization, tested by the continuation condition before each pass and updated (usually incremented) at the end of each pass; declared in a for header, it is not available after the loop.",
   "twin_logic": null,
   "level": "L1",
   "way": "states_the_rule"
  },
  {
   "depth": 3,
   "source": "loop_variable",
   "edge": "lvl:loop_variable@L2#2",
   "target": "loop_variable@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "10 < 5 is false",
   "confidence": 0.7,
   "prune_score": 0.3,
   "score": 0.21,
   "logic": "One update changes only the loop variable (i = i + 1 turns 4 into 5); one test reads it and yields true or false; an assignment to it in the body changes what the next test sees.",
   "twin_logic": null,
   "level": "L2",
   "way": "one_step_execution"
  },
  {
   "depth": 3,
   "source": "loop_variable",
   "edge": "lvl:loop_variable@L3#0",
   "target": "loop_variable@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "10 < 5 is false",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  }
 ],
 "evidence": [
  {
   "depth": 1,
   "source": "do_while_loop",
   "edge": "mis:do_while_loop->DoWhileTestsFirst",
   "target": "DoWhileTestsFirst",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "Zero times; 10 < 5 is false; so the loop never starts",
   "confidence": 0.97,
   "prune_score": 1.0,
   "score": 0.97,
   "logic": "A do-while whose condition starts false runs its body zero times.",
   "twin_logic": "The statements within the do block are always executed at least once.",
   "role": "primary"
  },
  {
   "depth": 1,
   "source": "do_while_loop",
   "edge": "lvl:do_while_loop@L0#2",
   "target": "do_while_loop@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "Zero times; 10 < 5 is false; so the loop never starts",
   "confidence": 0.75,
   "prune_score": 0.5,
   "score": 0.375,
   "logic": "Applies the LT rule unevenly: on a trace, the condition is tested before the first pass on some runs (as for while) and after it on others, or one more pass is run after the condition becomes false. The traced number of passes is off by one. (here mixing in: \"A do-while whose condition starts false runs its body zero times\")",
   "twin_logic": null,
   "level": "L0",
   "way": "inconsistent_trace"
  },
  {
   "depth": 1,
   "source": "do_while_loop",
   "edge": "lvl:do_while_loop@L0#0",
   "target": "do_while_loop@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "Zero times; 10 < 5 is false; so the loop never starts",
   "confidence": 0.85,
   "prune_score": 0.3,
   "score": 0.255,
   "logic": "Folk meaning: in English 'do X while Y' means do X during the time that Y holds, with Y watched continuously, as in the 'while demon'. In Java the condition is tested only at the bottom, after each complete pass of the body, and the first pass always runs.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 1,
   "source": "loop_body",
   "edge": "mis:loop_body->LoopBodyAlwaysOnce",
   "target": "LoopBodyAlwaysOnce",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "Zero times; 10 < 5 is false; so the loop never starts",
   "confidence": 0.6,
   "prune_score": 0.7,
   "score": 0.42,
   "logic": "The loop body always runs at least once, even if the condition is false at the start.",
   "twin_logic": "A while or for body runs zero times when the condition is false at the start.",
   "role": "context"
  },
  {
   "depth": 1,
   "source": "loop_control",
   "edge": "lvl:loop_control@L2#0",
   "target": "loop_control@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3
   ],
   "quote": "10 < 5 is false; so the loop never starts",
   "confidence": 0.75,
   "prune_score": 0.2,
   "score": 0.15,
   "logic": "init (once) -> test -> body -> update -> test -> body -> update ... -> test false -> exit.",
   "twin_logic": null,
   "level": "L2",
   "way": "line_by_line_trace"
  },
  {
   "depth": 2,
   "source": "do_while_loop",
   "edge": "pre:do_while_loop->loop_control",
   "target": "loop_control",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "Zero times; 10 < 5 is false; so the loop never starts",
   "confidence": 0.9,
   "prune_score": 0.55,
   "score": 0.495,
   "logic": "A do-while loop has the same control parts as a while loop (the variable set before, the condition, the update in the body); only the test is moved after the body.",
   "twin_logic": null,
   "consequence_of": "mis:do_while_loop->DoWhileTestsFirst"
  },
  {
   "depth": 2,
   "source": "do_while_loop",
   "edge": "pre:do_while_loop->loop_body",
   "target": "loop_body",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    3
   ],
   "quote": "Zero times; so the loop never starts",
   "confidence": 0.93,
   "prune_score": 0.45,
   "score": 0.4185,
   "logic": "The block between do and while is the loop body; it runs first and is repeated while the condition holds.",
   "twin_logic": null,
   "consequence_of": "mis:do_while_loop->DoWhileTestsFirst"
  },
  {
   "depth": 2,
   "source": "loop_control",
   "edge": "pre:loop_variable->loop_control",
   "target": "loop_variable",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    2
   ],
   "quote": "10 < 5 is false",
   "confidence": 0.6,
   "prune_score": 0.85,
   "score": 0.51,
   "logic": "The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "loop_variable",
   "edge": "lvl:loop_variable@L1#1",
   "target": "loop_variable@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3
   ],
   "quote": "10 < 5 is false; so the loop never starts",
   "confidence": 0.6,
   "prune_score": 0.5,
   "score": 0.3,
   "logic": "The loop variable is set once by the initialization, tested by the continuation condition before each pass and updated (usually incremented) at the end of each pass; declared in a for header, it is not available after the loop.",
   "twin_logic": null,
   "level": "L1",
   "way": "states_the_rule"
  },
  {
   "depth": 3,
   "source": "loop_variable",
   "edge": "lvl:loop_variable@L2#2",
   "target": "loop_variable@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "10 < 5 is false",
   "confidence": 0.7,
   "prune_score": 0.3,
   "score": 0.21,
   "logic": "One update changes only the loop variable (i = i + 1 turns 4 into 5); one test reads it and yields true or false; an assignment to it in the body changes what the next test sees.",
   "twin_logic": null,
   "level": "L2",
   "way": "one_step_execution"
  },
  {
   "depth": 3,
   "source": "loop_variable",
   "edge": "lvl:loop_variable@L3#0",
   "target": "loop_variable@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "10 < 5 is false",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  }
 ],
 "clause_coverage": {
  "Zero times": "mis:do_while_loop->DoWhileTestsFirst",
  "10 < 5 is false": "mis:do_while_loop->DoWhileTestsFirst",
  "so the loop never starts": "mis:do_while_loop->DoWhileTestsFirst"
 },
 "unexplained_clauses": [],
 "stop_reason": "sufficient",
 "depth_reached": 3,
 "llm_calls": 0,
 "llm_cache_hits": 32,
 "llm_calls_by_step": {
  "prune": 11,
  "label": 21
 }
}
```
