# Think on the Graph: every output of the run LP08

Files of this scenario: `input.json` (program, question, answer), `diagnosis.json`, `subgraph.json`, `traverse_log.txt`, `report.html` (this report as one full-page file, with the interactive graph `LP08_G.html`), `LP08.ipynb` (this report as a notebook).

## Level classification

This scenario tests **L1: names the element**. How the overall level is decided is explained in the [folder README](../../README.md).

- **Overall level: L1** (decided by: largest share)
- **Shares of the components:** L1 1.00; coherent
- **Mistake held (root cause):** none
- **Expected by design:** overall L1; components `for_loop` L1; held none; root none
- **Overall level matches the expected one:** yes

### How the overall level of this run was calculated

1. **Find the parts of the answer.** The answer touches 5 concepts (the components in the table below). Each one got its own level from what the student wrote about it.
2. **Is a real mistake held?** No wrong rule is held.
3. **Count the parts at each level:** 5 at L1.
4. **Result.** Most parts (5 of 5) are at L1, so the overall level is **L1**.
5. **Check.** The levels of the parts are next to each other, so the answer is coherent.

| Component | Level | Decided by | Student's words |
|---|---|---|---|
| `control_flow` | L1 | way: names the element | The program has two System.out.println statements and one for loop; The for loop has a header with a start, a condition and an update, and a body |
| `for_loop` | L1 | way: names the element | The for loop has a header with a start, a condition and an update, and a body |
| `loop_body` | L1 | way: names the element | The for loop has a header with a start, a condition and an update, and a body |
| `loop_control` | L1 | way: names the element | The for loop has a header with a start, a condition and an update, and a body |
| `println` | L1 | way: names the element | The program has two System.out.println statements and one for loop |

## 0. Input
Program:
```java
int i, n = 5;
for (i = 1; i < n; i++)
    i++;
    System.out.println(i);
System.out.println(i);
```
Question: How many times is System.out.println executed? Explain your reasoning.

Student's answer: The program has two System.out.println statements and one for loop. The for loop has a header with a start, a condition and an update, and a body.
Settings: width 3, depth 3, prune llm, backend claude-cli, model claude-opus-5-5
## 1. Stage 1: the subgraph G from the code (no model)
Masked code (string and char literals and comments blanked; this is what the patterns see):
```
int i, n = 5;
for (i = 1; i < n; i++)
    i++;
    System.out.println(i);
System.out.println(i);
```
Which code text tagged which concept (a generic concept fires on almost any Java line; it starts the walk only if the answer repeats its tag):
| concept | generic | channel | matched text | line |
|---|---|---|---|---|
| assignment | True | pattern | '=' | 1 |
| boolean_expression | False | pattern | 'for (i = 1; i < n;' | 2 |
| comparison_operators | False | pattern | 'for (i = 1; i <' | 2 |
| control_flow | False | pattern | 'for (' | 2 |
| expression | True | pattern | 'i <' | 2 |
| expression | True | pattern | '= 5;' | 1 |
| for_loop | False | pattern | 'for (' | 2 |
| increment_operators | False | pattern | '++' | 2 |
| loop_body | False | pattern | 'for (' | 2 |
| loop_control | False | signal | 'for (i = 1; i < n; i++)' | 2 |
| loop_variable | False | pattern | 'for (i =' | 2 |
| println | False | pattern | 'System.out.println(' | 4 |
| statement | True | pattern | ';' | 1 |

G: 12 concept nodes (3 generic), 10 concept edges, 116 misconception / error edges, 84 misconception / error nodes, 60 level nodes, 120 level-misconception links, 2 connected piece(s).
Note: concept nodes form 2 pieces (the KG has no edge between them): assignment,boolean_expression,comparison_operators,expression,for_loop,increment_operators,loop_body,loop_control,loop_variable | control_flow,println,statement

Concept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):
| edge | type | rule (logic) |
|---|---|---|
| par:assignment~comparison_operators | parallel | x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands. |
| pre:assignment->increment_operators | prerequisite | i++ is shorthand for the assignment i = i + 1. |
| pre:comparison_operators->boolean_expression | prerequisite | A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making. |
| pre:expression->comparison_operators | prerequisite | Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b. |
| pre:for_loop->loop_body | prerequisite | The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop. |
| pre:loop_control->for_loop | prerequisite | The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |
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
| expression | 8 | 19 |
| for_loop | 20 | 24 |
| increment_operators | 5 | 16 |
| loop_body | 12 | 14 |
| loop_control | 11 | 19 |
| loop_variable | 7 | 13 |
| println | 6 | 17 |
| statement | 5 | 19 |

**Figure 1**

![Figure 1](figure01.png)
**Figure 2**

![Figure 2](figure02.png)
## 2. Clauses and start concepts (no model)
The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):
| clause | text |
|---|---|
| c1 | The program has two System.out.println statements and one for loop |
| c2 | The for loop has a header with a start, a condition and an update, and a body |

start: BM25 of the answer against each tagged concept: for_loop 15.43 (hits 1), loop_control 11.85 (hits 1), loop_body 11.75 (hits 1), control_flow 10.92 (hits 1), println 10.77 (hits 1), increment_operators 9.27 (hits 1), boolean_expression 9.14 (hits 1), loop_variable 8.05 (hits 1), comparison_operators 7.48 (hits 1)

start: chosen for_loop, loop_control, loop_body

start concepts (3): for_loop, loop_control, loop_body

Start concepts: for_loop, loop_control, loop_body

**Figure 3**

![Figure 3](figure03.png)
## 3. The walk, depth by depth
At each depth, for each current concept: the edges offered (a concept entering as a start concept offers its misconception / error edges and its level ways, as two families; otherwise it offers its concept edges), the prune prompt and the model's reply, then the label prompt(s) and the model's reply, parsed into label / clauses / confidence. Score = prune score x confidence.

### Depth 1: current concepts 'for_loop', 'loop_control', 'loop_body'

#### for_loop, misconceptions: 20 edges offered
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
| mis:for_loop->ProgramEndsAfterLoop \| wrong rule: When a loop finishes the program ends, so code after the loop never runs. \| right rule: When the loop condition becomes false, control continues with the first statement after the loop. |
| mis:for_loop->ReturnDoesNotExitLoop \| wrong rule: A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values. \| right rule: When return executes, the method ends at once, so the loop stops on that pass. |
| mis:for_loop->SingleIterationInsteadOfLoop \| wrong rule: A task that must be repeated is written once, without a loop, as if one pass were enough. \| right rule: A step that must happen several times (or an unknown number of times) needs a loop such as while or for; code without a loop runs once. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:for_loop->ForLoopPartSkipped (0.40), mis:for_loop->LoopHeaderIsEquations (0.35), err:for_loop->BracelessMultiStatementBody (0.25)
```
Kept by pruning: mis:for_loop->ForLoopPartSkipped (0.40), mis:for_loop->LoopHeaderIsEquations (0.35), err:for_loop->BracelessMultiStatementBody (0.25)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:for_loop->ForLoopPartSkipped \| wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). \| right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start. |
| mis:for_loop->LoopHeaderIsEquations \| wrong rule: The initialization, condition and update of a for header are equations that all hold at the same time. \| right rule: The three header parts are statements run at different moments: init once, then condition test, body, update, repeated. |
| err:for_loop->BracelessMultiStatementBody \| wrong rule: Indenting several statements under an if or for makes them all part of its body, even without braces. \| right rule: Without braces only the first statement belongs to the if/for; the rest run once, after it. |
Model's reply:
```
mis:for_loop->ForLoopPartSkipped | not applied | clauses: none | confidence: 0.85
mis:for_loop->LoopHeaderIsEquations | not applied | clauses: none | confidence: 0.8
err:for_loop->BracelessMultiStatementBody | not applied | clauses: none | confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:for_loop->ForLoopPartSkipped | not applied |  |  | 0.0 |  |  |
| mis:for_loop->LoopHeaderIsEquations | not applied |  |  | 0.0 |  |  |
| err:for_loop->BracelessMultiStatementBody | not applied |  |  | 0.0 |  |  |

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
{lvl:for_loop@L1#0 (Score: 0.6)}
{lvl:for_loop@L1#1 (Score: 0.25)}
{lvl:for_loop@L3#0 (Score: 0.15)}
```
Kept by pruning: lvl:for_loop@L1#0 (0.60), lvl:for_loop@L1#1 (0.25), lvl:for_loop@L3#0 (0.15)

Label prompt for level way lvl:for_loop@L1#0 (the model saw only the concept, the way's name 'names the element' and its text; no level):
> The for statement is a loop that packages an initialization, a loop-continuation condition and an increment in its header around a body.

Model's reply:
```
Label: shown
Clauses: 2
Confidence: 0.85
```

Label prompt for level way lvl:for_loop@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> Syntax: for (<initialize>; <boolean expression>; <increment>) { <statements> }, with the three parts separated by semicolons; it is, with only a few exceptions, equivalent to <initialize>; while (<boolean expression>) { <statements> <increment>; }.

Model's reply:
```
Label: shown
Clauses: 2
Confidence: 0.65
```

Label prompt for level way lvl:for_loop@L3#0 (the model saw the concept, the way's name 'relation to neighbour', its text, where the way stops and whether the words must be correct; no level):
> The for header is exactly the three loop-control slots; the body runs after the test and before the update on each pass.
>
> Where this way stops: Two correct but separate rules are L1. Executing the two in sequence is L2. A relational answer may be correct or a relational error.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:for_loop@L1#0 | shown | 0.6 | 0.85 | 0.51 | c2 | The for loop has a header with a start, a condition and an update, and a body |
| lvl:for_loop@L1#1 | shown | 0.25 | 0.65 | 0.16 | c2 | The for loop has a header with a start, a condition and an update, and a body |
| lvl:for_loop@L3#0 | not applied |  |  | 0.0 |  |  |

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
mis:loop_control->ForLoopPartSkipped (0.40), mis:loop_control->LoopHeaderIsEquations (0.35), err:loop_control->WrongIterationCount (0.25)
```
Kept by pruning: mis:loop_control->ForLoopPartSkipped (0.40), mis:loop_control->LoopHeaderIsEquations (0.35), err:loop_control->WrongIterationCount (0.25)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:loop_control->ForLoopPartSkipped \| wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). \| right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start. |
| mis:loop_control->LoopHeaderIsEquations \| wrong rule: The initialization, condition and update of a for header are equations that all hold at the same time. \| right rule: The three header parts are statements run at different moments: init once, then condition test, body, update, repeated. |
| err:loop_control->WrongIterationCount \| wrong rule: Updates the loop counter so that the loop runs the wrong number of times. \| right rule: The init, test and update together decide the number of passes; trace them to check the count. |
Model's reply:
```
mis:loop_control->ForLoopPartSkipped | not applied | clauses: none | confidence: 0.85
mis:loop_control->LoopHeaderIsEquations | not applied | clauses: none | confidence: 0.75
err:loop_control->WrongIterationCount | not applied | clauses: none | confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:loop_control->ForLoopPartSkipped | not applied |  |  | 0.0 |  |  |
| mis:loop_control->LoopHeaderIsEquations | not applied |  |  | 0.0 |  |  |
| err:loop_control->WrongIterationCount | not applied |  |  | 0.0 |  |  |

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
{lvl:loop_control@L1#0 (Score: 0.5)}
{lvl:loop_control@L3#1 (Score: 0.3)}
{lvl:loop_control@L1#1 (Score: 0.2)}
```
Kept by pruning: lvl:loop_control@L1#0 (0.50), lvl:loop_control@L3#1 (0.30), lvl:loop_control@L1#1 (0.20)

Label prompt for level way lvl:loop_control@L1#0 (the model saw only the concept, the way's name 'names the element' and its text; no level):
> Loop control is the init / continuation condition / increment scheme on an index variable that decides how many passes a loop makes and with which values.

Model's reply:
```
Label: shown
Clauses: 2
Confidence: 0.7
```

Label prompt for level way lvl:loop_control@L3#1 (the model saw the concept, the way's name 'relation to neighbour', its text, where the way stops and whether the words must be correct; no level):
> The for header is exactly the three control slots, separated by semicolons; the body runs after the test and before the update.
>
> Where this way stops: Two correct but separate rules are L1. Executing the two in sequence is L2. A relational answer may be correct or a relational error.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Label prompt for level way lvl:loop_control@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> Initialize an index variable, test a loop-continuation condition on it before each pass, and increment it as the last action of each pass; for (<initialize>; <boolean expression>; <increment>) packages the three. Choosing the loop: for when the passes are counted by an index, while when the loop runs until a condition changes, do-while when the body must run at least once; any one can be rewritten as another, so choose the clearest.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:loop_control@L1#0 | shown | 0.5 | 0.7 | 0.35 | c2 | The for loop has a header with a start, a condition and an update, and a body |
| lvl:loop_control@L3#1 | not applied |  |  | 0.0 |  |  |
| lvl:loop_control@L1#1 | not applied |  |  | 0.0 |  |  |

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
mis:loop_body->ForLoopPartSkipped (0.50), err:loop_body->BracelessMultiStatementBody (0.30), mis:loop_body->StatementAfterLoopInBody (0.20)
```
Kept by pruning: mis:loop_body->ForLoopPartSkipped (0.50), err:loop_body->BracelessMultiStatementBody (0.30), mis:loop_body->StatementAfterLoopInBody (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:loop_body->ForLoopPartSkipped \| wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). \| right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start. |
| err:loop_body->BracelessMultiStatementBody \| wrong rule: Indenting several statements under an if or for makes them all part of its body, even without braces. \| right rule: Without braces only the first statement belongs to the if/for; the rest run once, after it. |
| mis:loop_body->StatementAfterLoopInBody \| wrong rule: A statement written after the loop is repeated with the loop body. \| right rule: The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends. |
Model's reply:
```
mis:loop_body->ForLoopPartSkipped | not applied | clauses: none | confidence: 0.8
err:loop_body->BracelessMultiStatementBody | not applied | clauses: none | confidence: 0.8
mis:loop_body->StatementAfterLoopInBody | not applied | clauses: none | confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:loop_body->ForLoopPartSkipped | not applied |  |  | 0.0 |  |  |
| err:loop_body->BracelessMultiStatementBody | not applied |  |  | 0.0 |  |  |
| mis:loop_body->StatementAfterLoopInBody | not applied |  |  | 0.0 |  |  |

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
{lvl:loop_body@L1#0 (Score: 0.6)}
{lvl:loop_body@L1#1 (Score: 0.3)}
{lvl:loop_body@L0#0 (Score: 0.1)}
```
Kept by pruning: lvl:loop_body@L1#0 (0.60), lvl:loop_body@L1#1 (0.30), lvl:loop_body@L0#0 (0.10)

Label prompt for level way lvl:loop_body@L1#0 (the model saw only the concept, the way's name 'names the element' and its text; no level):
> The loop body is the statement block that a loop repeats on each pass.

Model's reply:
```
Label: shown
Clauses: 2
Confidence: 0.6
```

Label prompt for level way lvl:loop_body@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> The body is the block after the loop header; braces are optional only if it is a single statement, in which case only that one statement is repeated.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:loop_body@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: an everyday 'repeat this' instruction can be read loosely - a helper fills in missing steps, does each step N times in turn, or stops partway. A Java loop body is exactly the statements inside its braces (or one statement), all executed in order on every pass.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:loop_body@L1#0 | shown | 0.6000000000000001 | 0.6 | 0.36 | c2 | The for loop has a header with a start, a condition and an update, and a body |
| lvl:loop_body@L1#1 | not applied |  |  | 0.0 |  |  |
| lvl:loop_body@L0#0 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

lvl:for_loop@L1#0 [shown, tier 2, 0.51], lvl:loop_body@L1#0 [shown, tier 2, 0.36], lvl:loop_control@L1#0 [shown, tier 2, 0.35]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | The program has two System.out.println statements and one for loop | not covered yet |
| c2 | The for loop has a header with a start, a condition and an update, and a body | not covered yet |

**Uncovered clauses bring in (BM25 of the uncovered clauses against unvisited concepts):** control_flow (14.56), println (13.60), loop_variable (11.67)

**Graph check, not yet read (the walk may not stop while these remain):** own edges of control_flow, own edges of loop_variable, own edges of println, pre:for_loop->loop_body, pre:loop_control->for_loop, pre:loop_control->increment_operators, pre:loop_variable->loop_control

**Figure 4 (the graph after depth 1)**

![Figure 4](figure04.png)
### Depth 2: current concepts 'for_loop', 'loop_control', 'loop_body', 'control_flow', 'println', 'loop_variable'

#### for_loop, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| pre:for_loop->loop_body \| rule: The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop. |
| pre:loop_control->for_loop \| rule: The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:loop_control->for_loop (Score: 0.6)}
{pre:for_loop->loop_body (Score: 0.4)}
```
Kept by pruning: pre:loop_control->for_loop (0.60), pre:for_loop->loop_body (0.40)

Label prompt for concept edge pre:loop_control->for_loop (loop_control -> for_loop, prerequisite):
> The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.

Model's reply:
```
Label: confirmed
Clauses: 2
Confidence: 0.6
```

Label prompt for concept edge pre:for_loop->loop_body (for_loop -> loop_body, prerequisite):
> The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:loop_control->for_loop | confirmed | 0.6 | 0.6 | 0.36 | c2 | The for loop has a header with a start, a condition and an update, and a body |
| pre:for_loop->loop_body | not applied |  |  | 0.0 |  |  |

#### loop_control, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| pre:loop_control->for_loop \| rule: The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |
| pre:loop_control->increment_operators \| rule: The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update. |
| pre:loop_variable->loop_control \| rule: The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
pre:loop_variable->loop_control (0.80), pre:loop_control->increment_operators (0.20)
```
Kept by pruning: pre:loop_variable->loop_control (0.80), pre:loop_control->increment_operators (0.20)

Label prompt for concept edge pre:loop_variable->loop_control (loop_variable -> loop_control, prerequisite):
> The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.

Model's reply:
```
Label: not applied
Clauses: none
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
| pre:loop_variable->loop_control | not applied |  |  | 0.0 |  |  |
| pre:loop_control->increment_operators | not applied |  |  | 0.0 |  |  |

#### control_flow, misconceptions: 11 edges offered
Edges offered:
| edge |
|---|
| mis:control_flow->CodeAfterIfSkipped \| wrong rule: When the then branch runs, the code after the if is skipped. \| right rule: After the if finishes, execution continues with the next statement either way. |
| mis:control_flow->FalseConditionRestartsProgram \| wrong rule: When an if condition is false (and there is no else), control jumps back to the start of the program. \| right rule: A false condition skips the then branch and execution continues with the statement after the if statement. |
| mis:control_flow->FalseLoopRepeatsNextCode \| wrong rule: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. \| right rule: Only the body is repeated; once the condition is false the code after the loop runs once. |
| mis:control_flow->IfConditionWatched \| wrong rule: An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever). \| right rule: An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch. |
| mis:control_flow->IfWaitsForCondition \| wrong rule: An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true. \| right rule: An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it. |
| mis:control_flow->LoopImpliedByOneTest \| wrong rule: Testing one case is enough; Java will repeat the test for the other values by itself. \| right rule: A statement runs once each time control reaches it; repeating a test for many values needs a loop. |
| mis:control_flow->NoShortCircuit \| wrong rule: logical AND/OR always evaluate both sides (Java short-circuits them) \| right rule: In p && q, q is evaluated only when p is true; in p \|\| q, q is evaluated only when p is false. |
| mis:control_flow->ProgramEndsAfterLoop \| wrong rule: When a loop finishes the program ends, so code after the loop never runs. \| right rule: When the loop condition becomes false, control continues with the first statement after the loop. |
| mis:control_flow->ProgramLooksAhead \| wrong rule: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. \| right rule: Each statement executes using only the current state; later lines have no effect until control reaches them. |
| mis:control_flow->ReturnDoesNotExitLoop \| wrong rule: A return inside a loop does not end the loop; it sets a value each pass (the last one is returned) or returns several values. \| right rule: When return executes, the method ends at once, so the loop stops on that pass. |
| mis:control_flow->StatementsRunInAnyOrder \| wrong rule: Statements in a program can run in any order. \| right rule: Without control statements, statements run once each, top to bottom. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:control_flow->FalseLoopRepeatsNextCode (0.40), mis:control_flow->ProgramEndsAfterLoop (0.35), mis:control_flow->StatementsRunInAnyOrder (0.25)
```
Kept by pruning: mis:control_flow->FalseLoopRepeatsNextCode (0.40), mis:control_flow->ProgramEndsAfterLoop (0.35), mis:control_flow->StatementsRunInAnyOrder (0.25)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:control_flow->FalseLoopRepeatsNextCode \| wrong rule: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. \| right rule: Only the body is repeated; once the condition is false the code after the loop runs once. |
| mis:control_flow->ProgramEndsAfterLoop \| wrong rule: When a loop finishes the program ends, so code after the loop never runs. \| right rule: When the loop condition becomes false, control continues with the first statement after the loop. |
| mis:control_flow->StatementsRunInAnyOrder \| wrong rule: Statements in a program can run in any order. \| right rule: Without control statements, statements run once each, top to bottom. |
Model's reply:
```
mis:control_flow->FalseLoopRepeatsNextCode | not applied | clauses: none | confidence: 0.9
mis:control_flow->ProgramEndsAfterLoop | not applied | clauses: none | confidence: 0.9
mis:control_flow->StatementsRunInAnyOrder | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:control_flow->FalseLoopRepeatsNextCode | not applied |  |  | 0.0 |  |  |
| mis:control_flow->ProgramEndsAfterLoop | not applied |  |  | 0.0 |  |  |
| mis:control_flow->StatementsRunInAnyOrder | not applied |  |  | 0.0 |  |  |

#### control_flow, level ways: 15 edges offered
Edges offered:
| edge |
|---|
| lvl:control_flow@L0#0 \| level L0 way everyday_reading: Folk meaning: in everyday instructions a listener reads the whole list at once, does steps in a sensible order and infers what the writer wants. Java instead executes statements one at a time, top to bottom, each only when control reaches it, and nothing later in the program has any effect earlier. |
| lvl:control_flow@L0#3 \| level L0 way inconsistent_trace: Applies the sequencing rule (LT) unevenly: e.g. runs a later line before an earlier one, lets an if that was already passed fire again later, or ends the program when a loop or a false if ends instead of continuing with the next statement. (here mixing in: "Statements in a program can run in any order") |
| lvl:control_flow@L1#0 \| level L1 way names_the_element: Control flow is the order in which a program's statements are executed (statement sequencing); conditionals and loops are the statements that change it. |
| lvl:control_flow@L1#1 \| level L1 way states_the_rule: Without control statements every statement executes once, in the order given; a block executes its statements in order from first to last; if/if-else choose between one or two alternatives and loops repeat statements depending on a condition. |
| lvl:control_flow@L2#0 \| level L2 way line_by_line_trace: Execute the statement at the current point; when it completes normally, control passes to the next statement in the block. An if evaluates its condition once and then runs at most one branch; a loop evaluates its condition before each pass; after an if or a loop finishes, control continues with the statement after it. |
| lvl:control_flow@L2#1 \| level L2 way output_prediction: The output is the sequence of print statements that control actually reaches, in the order reached: e.g. TenHellos prints 1st, 2nd, 3rd Hello once each, then 4th to 10th Hello from the loop. |
| lvl:control_flow@L2#2 \| level L2 way one_step_execution: One step executes the single statement at the current control point using the current values, updates at most the variables it assigns, and moves the control point to the next statement (or, for an if/loop test, to the chosen branch, back to the test, or past the statement). |
| lvl:control_flow@L3#0 \| level L3 way relation_to_neighbour: Control flow is defined over statements: statements are executed for their effect, and if/while/for are themselves statements that may be used wherever a statement is allowed, so they can nest. |
| lvl:control_flow@L3#1 \| level L3 way relation_to_neighbour: An if changes the default top-to-bottom flow: its condition is tested once when control reaches it, its block runs only if true, and in both cases control then continues with the next statement. |
| lvl:control_flow@L3#2 \| level L3 way relation_to_neighbour: A flowchart draws control flow: each path through the diagram is a possible path of execution, with a decision box for each if or loop test. |
| lvl:control_flow@L3#3 \| level L3 way purpose_of_the_whole: Plan: control flow lets one program do different things for different inputs (selection) and do a thing many times (repetition), so a short program can specify a potentially unlimited number of executed statements. |
| lvl:control_flow@L4#0 \| level L4 way predict_a_change: Reordering two statements generally changes the result whenever one reads a variable that the other writes (e.g. swapping x = x + 1 and print(x)); reordering is safe only for statements that touch disjoint variables. Moving a statement into or out of a branch or loop body changes how many times it runs (0, 1 or n). |
| lvl:control_flow@L4#1 \| level L4 way transfer_to_a_new_program: Reason in terms of control flow whenever you must predict output or find why a statement did or did not run: trace which statement is reached next. Straight-line sequence suffices only when every input needs the same steps exactly once; otherwise add a conditional or a loop. |
| lvl:control_flow@L4#2 \| level L4 way diagnose_an_error: rule broken: A local variable must be definitely assigned on every control-flow path before it is read. Kind: compile-time. Trigger class: A variable assigned only inside an if branch (or only in a loop body) and read after it: the compiler reports 'variable might not have been initialized'. |
| lvl:control_flow@L4#3 \| level L4 way diagnose_an_error: rule broken: Statements run in the order written, so an update must come before the statement that needs the new value. Kind: silent logic error. Trigger class: Swapping two dependent statements (e.g. printing before updating, or incrementing the index before using it): output is shifted or off by one pass, with no error. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:control_flow@L1#0 (Score: 0.6)}
{lvl:control_flow@L1#1 (Score: 0.25)}
{lvl:control_flow@L3#0 (Score: 0.15)}
```
Kept by pruning: lvl:control_flow@L1#0 (0.60), lvl:control_flow@L1#1 (0.25), lvl:control_flow@L3#0 (0.15)

Label prompt for level way lvl:control_flow@L1#0 (the model saw only the concept, the way's name 'names the element' and its text; no level):
> Control flow is the order in which a program's statements are executed (statement sequencing); conditionals and loops are the statements that change it.

Model's reply:
```
Label: shown
Clauses: 1, 2
Confidence: 0.6
```

Label prompt for level way lvl:control_flow@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> Without control statements every statement executes once, in the order given; a block executes its statements in order from first to last; if/if-else choose between one or two alternatives and loops repeat statements depending on a condition.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:control_flow@L3#0 (the model saw the concept, the way's name 'relation to neighbour', its text, where the way stops and whether the words must be correct; no level):
> Control flow is defined over statements: statements are executed for their effect, and if/while/for are themselves statements that may be used wherever a statement is allowed, so they can nest.
>
> Where this way stops: Two correct but separate rules are L1. Executing the two in sequence is L2. A relational answer may be correct or a relational error.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:control_flow@L1#0 | shown | 0.6 | 0.6 | 0.36 | c1, c2 | The program has two System.out.println statements and one for loop; The for loop has a header with a start, a condition and an update, and a body |
| lvl:control_flow@L1#1 | not applied |  |  | 0.0 |  |  |
| lvl:control_flow@L3#0 | not applied |  |  | 0.0 |  |  |

#### println, misconceptions: 6 edges offered
Edges offered:
| edge |
|---|
| err:println->PrintWithoutFinalNewline \| wrong rule: Ends the output with print and expects it to appear right away. \| right rule: Finish a line of print calls with println; some systems hold print output until a newline is printed. |
| mis:println->IdentifierCaseInsensitive \| wrong rule: System.out.Println and System.out.println name the same method. \| right rule: Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names. |
| mis:println->ParenthesesOnlyIfArgument \| wrong rule: println with nothing to print can be written System.out.println; without the parentheses. \| right rule: A method call always needs parentheses, so an empty line is printed with System.out.println();. |
| mis:println->PrintEqualsPrintln \| wrong rule: print and println do the same thing, so print(s1); print(s2); puts s1 and s2 on separate lines. \| right rule: println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line. |
| mis:println->PrintNewLineFirst \| wrong rule: println(s) prints a newline and then s. \| right rule: println(s) prints s and then the newline. |
| mis:println->PrintedTextIsExecuted \| wrong rule: System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code). \| right rule: Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:println->IdentifierCaseInsensitive (0.40), mis:println->ParenthesesOnlyIfArgument (0.35), mis:println->PrintedTextIsExecuted (0.25)
```
Kept by pruning: mis:println->IdentifierCaseInsensitive (0.40), mis:println->ParenthesesOnlyIfArgument (0.35), mis:println->PrintedTextIsExecuted (0.25)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:println->IdentifierCaseInsensitive \| wrong rule: System.out.Println and System.out.println name the same method. \| right rule: Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names. |
| mis:println->ParenthesesOnlyIfArgument \| wrong rule: println with nothing to print can be written System.out.println; without the parentheses. \| right rule: A method call always needs parentheses, so an empty line is printed with System.out.println();. |
| mis:println->PrintedTextIsExecuted \| wrong rule: System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code). \| right rule: Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x. |
Model's reply:
```
mis:println->IdentifierCaseInsensitive | not applied | clauses: none | confidence: 0.95
mis:println->ParenthesesOnlyIfArgument | not applied | clauses: none | confidence: 0.95
mis:println->PrintedTextIsExecuted | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:println->IdentifierCaseInsensitive | not applied |  |  | 0.0 |  |  |
| mis:println->ParenthesesOnlyIfArgument | not applied |  |  | 0.0 |  |  |
| mis:println->PrintedTextIsExecuted | not applied |  |  | 0.0 |  |  |

#### println, level ways: 17 edges offered
Edges offered:
| edge |
|---|
| lvl:println@L0#0 \| level L0 way everyday_reading: Everyday reading: 'println' is just 'print', and 'new line' is something you do before writing. Java rule: println(x) prints x and then ends the line; println() alone just ends the line. |
| lvl:println@L0#3 \| level L0 way inconsistent_trace: Applies the println rule (print, then end line) unevenly: puts the newline before the text on one call and after it on another, or forgets that the next output starts on a new line. (here mixing in: "print and println behave the same (no newline difference)") |
| lvl:println@L1#0 \| level L1 way names_the_element: System.out.println is a library method that prints its argument followed by a line terminator ('print line'). |
| lvl:println@L1#1 \| level L1 way states_the_rule: println(String x) behaves as though it calls print(x) and then println(); println() terminates the current line by writing the line separator string. |
| lvl:println@L2#0 \| level L2 way line_by_line_trace: Evaluate the argument, print its characters at the current position, then write the line separator so the cursor moves to the beginning of the next line. |
| lvl:println@L2#1 \| level L2 way output_prediction: Output is the value's characters followed by a line break: println("Hello, "); println("World!"); prints two lines. |
| lvl:println@L2#2 \| level L2 way one_step_execution: One call appends the text and a line separator to the output; the cursor ends at the start of the next line; no variable changes and nothing is returned. |
| lvl:println@L3#0 \| level L3 way relation_to_neighbour: System.out.println(s); is a statement, so its line of output appears at its own place in the sequence. |
| lvl:println@L3#1 \| level L3 way relation_to_neighbour: println("s") outputs exactly the characters between the quotes and then ends the line. |
| lvl:println@L3#2 \| level L3 way relation_to_neighbour: print leaves the cursor on the line; println ends it; several prints followed by one println make one line. |
| lvl:println@L3#3 \| level L3 way relation_to_neighbour: println prints numbers with all their digits and always ends the line; printf formats each value by its conversion code and ends the line only where the format has %n or \n. |
| lvl:println@L3#4 \| level L3 way purpose_of_the_whole: Purpose: produce one complete line of output, e.g. each result on its own line, or end a line built with print. |
| lvl:println@L4#0 \| level L4 way predict_a_change: Replacing println with print joins the next output onto the same line (a typical logic error); the characters printed stay the same. |
| lvl:println@L4#1 \| level L4 way transfer_to_a_new_program: Use println when each output item belongs on its own line or to end a line; use print to continue a line and printf to control number formatting. |
| lvl:println@L4#2 \| level L4 way diagnose_an_error: rule broken: Finish a line of print calls with println. Kind: silent logic error. Trigger class: output ends with print, so the last line may not be shown or runs into the shell prompt |
| lvl:println@L4#3 \| level L4 way diagnose_an_error: rule broken: Method names are case-sensitive. Kind: compile-time. Trigger class: System.out.Println or system.out.println: cannot find symbol |
| lvl:println@L4#4 \| level L4 way diagnose_an_error: rule broken: Calls need parentheses. Kind: compile-time. Trigger class: System.out.println; without () |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:println@L1#0 (Score: 0.6)}
{lvl:println@L3#0 (Score: 0.3)}
{lvl:println@L1#1 (Score: 0.1)}
```
Kept by pruning: lvl:println@L1#0 (0.60), lvl:println@L3#0 (0.30), lvl:println@L1#1 (0.10)

Label prompt for level way lvl:println@L1#0 (the model saw only the concept, the way's name 'names the element' and its text; no level):
> System.out.println is a library method that prints its argument followed by a line terminator ('print line').

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.6
```

Label prompt for level way lvl:println@L3#0 (the model saw the concept, the way's name 'relation to neighbour', its text, where the way stops and whether the words must be correct; no level):
> System.out.println(s); is a statement, so its line of output appears at its own place in the sequence.
>
> Where this way stops: Two correct but separate rules are L1. Executing the two in sequence is L2. A relational answer may be correct or a relational error.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:println@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> println(String x) behaves as though it calls print(x) and then println(); println() terminates the current line by writing the line separator string.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.93
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:println@L1#0 | shown | 0.6000000000000001 | 0.6 | 0.36 | c1 | The program has two System.out.println statements and one for loop |
| lvl:println@L3#0 | not applied |  |  | 0.0 |  |  |
| lvl:println@L1#1 | not applied |  |  | 0.0 |  |  |

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
mis:loop_variable->ForInitRepeats (0.40), mis:loop_variable->BodyChangeIgnoredByCondition (0.35), mis:loop_variable->LoopUpdateChangesDirection (0.25)
```
Kept by pruning: mis:loop_variable->ForInitRepeats (0.40), mis:loop_variable->BodyChangeIgnoredByCondition (0.35), mis:loop_variable->LoopUpdateChangesDirection (0.25)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:loop_variable->ForInitRepeats \| wrong rule: The initialization of a for loop runs again after a pass of the body. \| right rule: The initialization runs exactly once, before the first condition test. |
| mis:loop_variable->BodyChangeIgnoredByCondition \| wrong rule: Changing the loop variable inside the body does not affect the loop condition; the loop still runs its planned number of times. \| right rule: The condition is tested with the current value of the variable, including changes made in the body. |
| mis:loop_variable->LoopUpdateChangesDirection \| wrong rule: The update of the loop variable can change from pass to pass (e.g. switch direction) although the code is the same. \| right rule: The update expression is the same on every pass; the loop variable changes by the rule written in the update. |
Model's reply:
```
mis:loop_variable->ForInitRepeats | not applied | clauses: none | confidence: 0.9
mis:loop_variable->BodyChangeIgnoredByCondition | not applied | clauses: none | confidence: 0.9
mis:loop_variable->LoopUpdateChangesDirection | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:loop_variable->ForInitRepeats | not applied |  |  | 0.0 |  |  |
| mis:loop_variable->BodyChangeIgnoredByCondition | not applied |  |  | 0.0 |  |  |
| mis:loop_variable->LoopUpdateChangesDirection | not applied |  |  | 0.0 |  |  |

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
{lvl:loop_variable@L1#0 (Score: 0.5)}
{lvl:loop_variable@L1#1 (Score: 0.3)}
{lvl:loop_variable@L3#0 (Score: 0.2)}
```
Kept by pruning: lvl:loop_variable@L1#0 (0.50), lvl:loop_variable@L1#1 (0.30), lvl:loop_variable@L3#0 (0.20)

Label prompt for level way lvl:loop_variable@L1#0 (the model saw only the concept, the way's name 'names the element' and its text; no level):
> A loop variable (loop-control counter, index) is a variable that is initialized, tested and updated in order to control a loop.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Label prompt for level way lvl:loop_variable@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> The loop variable is set once by the initialization, tested by the continuation condition before each pass and updated (usually incremented) at the end of each pass; declared in a for header, it is not available after the loop.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.8
```

Label prompt for level way lvl:loop_variable@L3#0 (the model saw the concept, the way's name 'relation to neighbour', its text, where the way stops and whether the words must be correct; no level):
> The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.
>
> Where this way stops: Two correct but separate rules are L1. Executing the two in sequence is L2. A relational answer may be correct or a relational error.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:loop_variable@L1#0 | not applied |  |  | 0.0 |  |  |
| lvl:loop_variable@L1#1 | not applied |  |  | 0.0 |  |  |
| lvl:loop_variable@L3#0 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:loop_control->for_loop [confirmed, tier 2, 0.36], lvl:control_flow@L1#0 [shown, tier 2, 0.36], lvl:println@L1#0 [shown, tier 2, 0.36]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | The program has two System.out.println statements and one for loop | not covered yet |
| c2 | The for loop has a header with a start, a condition and an update, and a body | pre:loop_control->for_loop |

**Uncovered clauses bring in (BM25 of the uncovered clauses against unvisited concepts):** comparison_operators (3.62), boolean_expression (3.48), increment_operators (3.32)

**Graph check, not yet read (the walk may not stop while these remain):** own edges of boolean_expression, own edges of comparison_operators, own edges of increment_operators, pre:statement->control_flow, pre:statement->println

**Figure 5 (the graph after depth 2)**

![Figure 5](figure05.png)
### Depth 3: current concepts 'loop_control', 'for_loop', 'control_flow', 'println', 'comparison_operators', 'boolean_expression', 'increment_operators'

#### loop_control, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| pre:loop_control->for_loop \| rule: The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |
| pre:loop_control->increment_operators \| rule: The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update. |
| pre:loop_variable->loop_control \| rule: The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
pre:loop_variable->loop_control (0.80), pre:loop_control->increment_operators (0.20)
```
Kept by pruning: pre:loop_variable->loop_control (0.80), pre:loop_control->increment_operators (0.20)

Label prompt for concept edge pre:loop_variable->loop_control (loop_variable -> loop_control, prerequisite):
> The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.

Model's reply:
```
Label: not applied
Clauses: none
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
| pre:loop_variable->loop_control | not applied |  |  | 0.0 |  |  |
| pre:loop_control->increment_operators | not applied |  |  | 0.0 |  |  |

#### for_loop, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:for_loop->loop_body \| rule: The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop. |
| pre:loop_control->for_loop \| rule: The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:for_loop->loop_body (Score: 1.0)}
```
Kept by pruning: pre:for_loop->loop_body (1.00)

Label prompt for concept edge pre:for_loop->loop_body (for_loop -> loop_body, prerequisite):
> The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:for_loop->loop_body | not applied |  |  | 0.0 |  |  |

#### control_flow, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:statement->control_flow \| rule: Control flow is the order in which statements run. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:statement->control_flow (Score: 1.0)}
```
Kept by pruning: pre:statement->control_flow (1.00)

Label prompt for concept edge pre:statement->control_flow (statement -> control_flow, prerequisite):
> Control flow is the order in which statements run.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.75
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:statement->control_flow | not applied |  |  | 0.0 |  |  |

#### println, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:statement->println \| rule: System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:statement->println (Score: 1.0)}
```
Kept by pruning: pre:statement->println (1.00)

Label prompt for concept edge pre:statement->println (statement -> println, prerequisite):
> System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:statement->println | not applied |  |  | 0.0 |  |  |

#### comparison_operators, misconceptions: 8 edges offered
Edges offered:
| edge |
|---|
| err:comparison_operators->ReversedRelationalOperator \| wrong rule: Writes =< or => instead of <= and >=. \| right rule: The operators are written <= and >=. |
| mis:comparison_operators->AssignCompares \| wrong rule: = compares two values instead of assigning \| right rule: x = y copies the value of y into x; x == y is what compares them. |
| mis:comparison_operators->ChainedComparison \| wrong rule: 90 <= grade <= 100 tests whether grade is between 90 and 100. \| right rule: a < b < c does not compile (a < b is a boolean); a range test is written 90 <= grade && grade <= 100. |
| mis:comparison_operators->ComparisonWithBooleanLiteral \| wrong rule: you must write == true / == false to test a boolean \| right rule: if (b) already tests b, so writing == true adds nothing. |
| mis:comparison_operators->EqualityOperatorComparesObjectsValues \| wrong rule: s == t is true whenever the two Strings contain the same text. \| right rule: s == t is true only when s and t refer to the same object; s.equals(t) compares the text. |
| mis:comparison_operators->EqualsComparesReferences \| wrong rule: .equals() compares references, not contents \| right rule: s.equals(t) checks whether the two Strings contain the same characters. |
| mis:comparison_operators->LessGreaterSwapped \| wrong rule: < and > mean the same thing (or a < b means a is greater than b). \| right rule: a < b is true when a is smaller than b; a > b when a is larger. |
| mis:comparison_operators->StringRelationalComparison \| wrong rule: s < t compares two Strings alphabetically. \| right rule: < and > are defined only for primitive types; comparing Strings with them does not compile. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:comparison_operators->LessGreaterSwapped (0.50), err:comparison_operators->ReversedRelationalOperator (0.30), mis:comparison_operators->AssignCompares (0.20)
```
Kept by pruning: mis:comparison_operators->LessGreaterSwapped (0.50), err:comparison_operators->ReversedRelationalOperator (0.30), mis:comparison_operators->AssignCompares (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:comparison_operators->LessGreaterSwapped \| wrong rule: < and > mean the same thing (or a < b means a is greater than b). \| right rule: a < b is true when a is smaller than b; a > b when a is larger. |
| err:comparison_operators->ReversedRelationalOperator \| wrong rule: Writes =< or => instead of <= and >=. \| right rule: The operators are written <= and >=. |
| mis:comparison_operators->AssignCompares \| wrong rule: = compares two values instead of assigning \| right rule: x = y copies the value of y into x; x == y is what compares them. |
Model's reply:
```
mis:comparison_operators->LessGreaterSwapped | not applied | clauses: none | confidence: 0.9
err:comparison_operators->ReversedRelationalOperator | not applied | clauses: none | confidence: 0.95
mis:comparison_operators->AssignCompares | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:comparison_operators->LessGreaterSwapped | not applied |  |  | 0.0 |  |  |
| err:comparison_operators->ReversedRelationalOperator | not applied |  |  | 0.0 |  |  |
| mis:comparison_operators->AssignCompares | not applied |  |  | 0.0 |  |  |

#### comparison_operators, level ways: 20 edges offered
Edges offered:
| edge |
|---|
| lvl:comparison_operators@L0#0 \| level L0 way everyday_reading: Folk meaning: in maths = states that two things are equal, and inequalities can be chained (a < b < c) or spoken as 'equal or less than' (=<). Java rule: = assigns while == compares; the operators are spelled <= and >= only; a < b < c does not compile; and on Strings == compares references. |
| lvl:comparison_operators@L0#5 \| level L0 way inconsistent_trace: Points to LT (evaluate both operands, promote to a common type, then compare). Applied unevenly: the student treats < as <= on the boundary pass of a loop, or compares an int with a double as ints on one line and as doubles on another. (here mixing in: "90 <= grade <= 100 tests whether grade is between 90 and 100") |
| lvl:comparison_operators@L1#0 \| level L1 way names_the_element: Comparison (relational) operators ==, !=, <, <=, >, >= are mixed-type operators: they take two operands of a numeric type and produce a boolean. |
| lvl:comparison_operators@L1#1 \| level L1 way states_the_rule: ==, !=, <, <=, >, >= are defined for each primitive numeric type and produce a boolean; they have lower precedence than arithmetic and higher than boolean operators; < and > are not defined for Strings, and == on non-primitive types compares identity. |
| lvl:comparison_operators@L2#0 \| level L2 way line_by_line_trace: Evaluate the left operand (including its arithmetic), then the right operand; if their types differ, promote the narrower one (int to double); then compare and produce true or false. |
| lvl:comparison_operators@L2#1 \| level L2 way output_prediction: The result is a boolean: (2 <= 2) is true, 2 < 2 is false, (x < 3.1) is true for int x = 3; any comparison involving NaN, even NaN == NaN, is false. |
| lvl:comparison_operators@L2#2 \| level L2 way one_step_execution: A comparison changes no variable and only returns a boolean, unlike =, which changes the value of the variable on its left. |
| lvl:comparison_operators@L3#0 \| level L3 way relation_to_neighbour: A comparison is itself an expression whose value is a boolean, so it can appear anywhere a boolean is needed, including on the right of an assignment (boolean ok = x > y;). |
| lvl:comparison_operators@L3#1 \| level L3 way relation_to_neighbour: Comparisons are the building blocks of conditions: together with boolean logic they provide the basis for decision-making. |
| lvl:comparison_operators@L3#2 \| level L3 way relation_to_neighbour: Comparisons bind tighter than && and \|\|, so they are evaluated first and logical operators combine their boolean results. |
| lvl:comparison_operators@L3#3 \| level L3 way relation_to_neighbour: Comparisons take numbers and produce a boolean; boolean values themselves can be compared only with == and != (not <), and testing them against true is unnecessary. |
| lvl:comparison_operators@L3#4 \| level L3 way relation_to_neighbour: x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands. |
| lvl:comparison_operators@L3#5 \| level L3 way purpose_of_the_whole: Used to test a numeric condition: thresholds and sign checks, range tests, divisibility (n % k == 0), loop continuation (i < N), sentinel checks, and running-extreme updates (if (x > max) max = x). |
| lvl:comparison_operators@L4#0 \| level L4 way predict_a_change: Changing < to <= (or > to >=) changes the result only at the boundary value, which in a loop guard means one more or one fewer iteration (off-by-one); mirroring the comparison (a < b to b > a) preserves the value; negating it gives the complementary operator (!(a < b) is a >= b). |
| lvl:comparison_operators@L4#1 \| level L4 way diagnose_an_error: rule broken: The operators are written <= and >=. Kind: compile-time. Trigger class: Writing =< or => (e.g. if (x => 0)). |
| lvl:comparison_operators@L4#2 \| level L4 way transfer_to_a_new_program: Use comparison operators for numeric and char tests; for Strings use equals (or compareTo); for computed doubles use a tolerance; for booleans use the variable itself instead of == true. |
| lvl:comparison_operators@L4#3 \| level L4 way diagnose_an_error: rule broken: == compares, = assigns. Kind: compile-time. Trigger class: if (a = b) with int operands (with boolean operands it compiles and silently assigns). |
| lvl:comparison_operators@L4#4 \| level L4 way diagnose_an_error: rule broken: == on Strings compares references, not text. Kind: silent logic error. Trigger class: Comparing a String built at run time (input, concatenation) with a literal using ==. |
| lvl:comparison_operators@L4#5 \| level L4 way diagnose_an_error: rule broken: < and > are defined only for primitive types; comparisons cannot be chained; both operands must be compatible. Kind: compile-time. Trigger class: s < t on Strings, a < b < c, or 5 < "6". |
| lvl:comparison_operators@L4#6 \| level L4 way diagnose_an_error: rule broken: Computed doubles should not be compared with ==. Kind: silent logic error. Trigger class: == between doubles produced by arithmetic, e.g. (0.1 + 0.1 + 0.1 == 0.3). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:comparison_operators@L1#0 (Score: 0.5)}
{lvl:comparison_operators@L3#5 (Score: 0.3)}
{lvl:comparison_operators@L3#1 (Score: 0.2)}
```
Kept by pruning: lvl:comparison_operators@L1#0 (0.50), lvl:comparison_operators@L3#5 (0.30), lvl:comparison_operators@L3#1 (0.20)

Label prompt for level way lvl:comparison_operators@L1#0 (the model saw only the concept, the way's name 'names the element' and its text; no level):
> Comparison (relational) operators ==, !=, <, <=, >, >= are mixed-type operators: they take two operands of a numeric type and produce a boolean.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Label prompt for level way lvl:comparison_operators@L3#5 (the model saw the concept, the way's name 'purpose of the whole', its text, where the way stops and whether the words must be correct; no level):
> Used to test a numeric condition: thresholds and sign checks, range tests, divisibility (n % k == 0), loop continuation (i < N), sentinel checks, and running-extreme updates (if (x > max) max = x).
>
> Where this way stops: Narrating the lines is L2. A purpose induced from a few traced cases is L2. A wrong purpose is still L3, but with an error.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.93
```

Label prompt for level way lvl:comparison_operators@L3#1 (the model saw the concept, the way's name 'relation to neighbour', its text, where the way stops and whether the words must be correct; no level):
> Comparisons are the building blocks of conditions: together with boolean logic they provide the basis for decision-making.
>
> Where this way stops: Two correct but separate rules are L1. Executing the two in sequence is L2. A relational answer may be correct or a relational error.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:comparison_operators@L1#0 | not applied |  |  | 0.0 |  |  |
| lvl:comparison_operators@L3#5 | not applied |  |  | 0.0 |  |  |
| lvl:comparison_operators@L3#1 | not applied |  |  | 0.0 |  |  |

#### boolean_expression, misconceptions: 8 edges offered
Edges offered:
| edge |
|---|
| err:boolean_expression->ElseWithCondition \| wrong rule: Writes else (x > 0) with a condition but no if. \| right rule: else takes no condition; use else if (x > 0). |
| mis:boolean_expression->ArithmeticInsteadOfBoolean \| wrong rule: A true/false question is answered with arithmetic (e.g. 1 for true). \| right rule: A logic question is written as a boolean expression whose value is true or false. |
| mis:boolean_expression->ChainedComparison \| wrong rule: 90 <= grade <= 100 tests whether grade is between 90 and 100. \| right rule: a < b < c does not compile (a < b is a boolean); a range test is written 90 <= grade && grade <= 100. |
| mis:boolean_expression->ComparisonWithBooleanLiteral \| wrong rule: To test a boolean b you must write if (b == true). \| right rule: if (b) already tests b, so writing == true adds nothing. |
| mis:boolean_expression->LoopForOneTimeTest \| wrong rule: Uses a loop where a condition needs to be tested only once. \| right rule: A test made once is an if; a loop repeats. |
| mis:boolean_expression->MapToBooleanWithConditionalOperator \| wrong rule: To get a boolean from x > y you need ok = (x > y) ? true : false;. \| right rule: ok = (x > y); already gives the boolean, so the ? : is unnecessary. |
| mis:boolean_expression->MapToBooleanWithIf \| wrong rule: To store whether x > y in a boolean you need if (x > y) ok = true; else ok = false;. \| right rule: ok = (x > y); stores the result of the comparison directly. |
| mis:boolean_expression->NestedIfsInsteadOfLogicalOperators \| wrong rule: A condition on several values has to be written as nested if statements, one value per if. \| right rule: Several conditions combine into one boolean expression with && and \|\|, e.g. if (x == 0 && y == 0). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:boolean_expression->LoopForOneTimeTest (0.50), mis:boolean_expression->ArithmeticInsteadOfBoolean (0.30), mis:boolean_expression->ChainedComparison (0.20)
```
Kept by pruning: mis:boolean_expression->LoopForOneTimeTest (0.50), mis:boolean_expression->ArithmeticInsteadOfBoolean (0.30), mis:boolean_expression->ChainedComparison (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:boolean_expression->LoopForOneTimeTest \| wrong rule: Uses a loop where a condition needs to be tested only once. \| right rule: A test made once is an if; a loop repeats. |
| mis:boolean_expression->ArithmeticInsteadOfBoolean \| wrong rule: A true/false question is answered with arithmetic (e.g. 1 for true). \| right rule: A logic question is written as a boolean expression whose value is true or false. |
| mis:boolean_expression->ChainedComparison \| wrong rule: 90 <= grade <= 100 tests whether grade is between 90 and 100. \| right rule: a < b < c does not compile (a < b is a boolean); a range test is written 90 <= grade && grade <= 100. |
Model's reply:
```
mis:boolean_expression->LoopForOneTimeTest | not applied | clauses: none | confidence: 0.9
mis:boolean_expression->ArithmeticInsteadOfBoolean | not applied | clauses: none | confidence: 0.95
mis:boolean_expression->ChainedComparison | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:boolean_expression->LoopForOneTimeTest | not applied |  |  | 0.0 |  |  |
| mis:boolean_expression->ArithmeticInsteadOfBoolean | not applied |  |  | 0.0 |  |  |
| mis:boolean_expression->ChainedComparison | not applied |  |  | 0.0 |  |  |

#### boolean_expression, level ways: 19 edges offered
Edges offered:
| edge |
|---|
| lvl:boolean_expression@L0#0 \| level L0 way everyday_reading: Folk meaning: maths writes a range as 90 <= grade <= 100 and English says 'if x is 1 or 2'. Java rule: each comparison is a separate boolean expression and they must be joined explicitly: 90 <= grade && grade <= 100, x == 1 \|\| x == 2; 90 <= grade <= 100 does not compile because 90 <= grade is already a boolean. |
| lvl:boolean_expression@L0#5 \| level L0 way inconsistent_trace: Points to LT (arithmetic first, then comparisons, then !, &&, \|\|, left to right, with short-circuit). Applied unevenly: the student evaluates && before a comparison in one sub-expression, or evaluates the right operand of && on a pass where the left was already false. (here mixing in: "you must write == true / == false to test a boolean") |
| lvl:boolean_expression@L1#0 \| level L1 way names_the_element: A boolean expression is any expression whose type is boolean: a boolean literal or variable, a comparison, or such parts combined with &&, \|\| and !. |
| lvl:boolean_expression@L1#1 \| level L1 way states_the_rule: A boolean expression has value true or false; it is built from comparisons (lower precedence than arithmetic, higher than boolean operators) and boolean operators; the condition of if, while and for must be one. |
| lvl:boolean_expression@L2#0 \| level L2 way line_by_line_trace: Operands are evaluated left to right; arithmetic sub-expressions first, then comparisons, then !, then &&, then \|\|; && and \|\| evaluate their right operand only when the left has not decided the result. |
| lvl:boolean_expression@L2#1 \| level L2 way output_prediction: The value is true or false: with year = 1900, (year % 4 == 0) && (year % 100 != 0) \|\| (year % 400 == 0) is false, so LeapYear prints false. |
| lvl:boolean_expression@L2#2 \| level L2 way one_step_execution: Evaluating a boolean expression changes no variable (unless it contains an assignment, ++ or a method with side effects); state changes only when its value is stored, as in isLeapYear = isLeapYear && (year % 100 != 0);. |
| lvl:boolean_expression@L3#0 \| level L3 way relation_to_neighbour: Comparisons are the atoms of boolean expressions; because they bind tighter than && and \|\|, month >= 1 && month <= 12 groups as (month >= 1) && (month <= 12) without parentheses. |
| lvl:boolean_expression@L3#1 \| level L3 way relation_to_neighbour: &&, \|\| and ! combine boolean sub-expressions into a larger one; ! binds tighter than comparisons, so negating a comparison needs parentheses: !(x > 0). |
| lvl:boolean_expression@L3#2 \| level L3 way relation_to_neighbour: The if statement evaluates its boolean expression once and runs its block only when the value is true; the expression must have type boolean, so if (x = 5) with int x does not compile. |
| lvl:boolean_expression@L3#3 \| level L3 way relation_to_neighbour: The while loop re-evaluates its boolean expression before every pass and stops the first time it is false, so some variable in the expression must change in the body or the loop never ends. |
| lvl:boolean_expression@L3#4 \| level L3 way relation_to_neighbour: In RandomSurfer the boolean expression r < sum is evaluated for each candidate page j in turn, as sum grows; the first j for which it is true is the chosen page. |
| lvl:boolean_expression@L3#5 \| level L3 way relation_to_neighbour: In the template if (<boolean expression>) { <statements> } the placeholder may be filled by any boolean-typed expression: a literal, a boolean variable, a comparison or a combination with logical operators. |
| lvl:boolean_expression@L3#6 \| level L3 way purpose_of_the_whole: Expresses a decision condition or guard (which branch runs, whether a loop continues) or computes a flag; common plans: range test lo <= x && x <= hi, divisibility test n % k == 0, combined rule as in LeapYear. |
| lvl:boolean_expression@L4#0 \| level L4 way predict_a_change: Rewriting with De Morgan (!(a && b) as !a \|\| !b) keeps the value for every input; swapping the operands of && keeps the truth value but can change whether the right operand is evaluated (and whether a guard still protects it); changing < to <= changes the result only at the boundary value. |
| lvl:boolean_expression@L4#1 \| level L4 way diagnose_an_error: rule broken: else takes no condition; a second condition needs else if (...). Kind: compile-time. Trigger class: Writing else (x > 0) { ... } after an if block (the compiler reports e.g. 'not a statement' or '; expected'). |
| lvl:boolean_expression@L4#2 \| level L4 way transfer_to_a_new_program: Use a boolean expression wherever code must decide or record a yes/no condition, and store it directly (ok = x > y) rather than via if or ? :; when different outcomes are needed for several cases use an if-else chain of such expressions. |
| lvl:boolean_expression@L4#3 \| level L4 way diagnose_an_error: rule broken: The condition must be a boolean expression; = assigns, == compares. Kind: compile-time. Trigger class: if (a = b) with int a and b (with boolean variables it compiles and silently assigns). |
| lvl:boolean_expression@L4#4 \| level L4 way diagnose_an_error: rule broken: Comparisons cannot be chained; each must be joined with && or \|\|. Kind: compile-time. Trigger class: Range written as a < b < c or 90 <= grade <= 100. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:boolean_expression@L1#1 (Score: 0.5)}
{lvl:boolean_expression@L1#0 (Score: 0.3)}
{lvl:boolean_expression@L3#5 (Score: 0.2)}
```
Kept by pruning: lvl:boolean_expression@L1#1 (0.50), lvl:boolean_expression@L1#0 (0.30), lvl:boolean_expression@L3#5 (0.20)

Label prompt for level way lvl:boolean_expression@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> A boolean expression has value true or false; it is built from comparisons (lower precedence than arithmetic, higher than boolean operators) and boolean operators; the condition of if, while and for must be one.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:boolean_expression@L1#0 (the model saw only the concept, the way's name 'names the element' and its text; no level):
> A boolean expression is any expression whose type is boolean: a boolean literal or variable, a comparison, or such parts combined with &&, || and !.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Label prompt for level way lvl:boolean_expression@L3#5 (the model saw the concept, the way's name 'relation to neighbour', its text, where the way stops and whether the words must be correct; no level):
> In the template if (<boolean expression>) { <statements> } the placeholder may be filled by any boolean-typed expression: a literal, a boolean variable, a comparison or a combination with logical operators.
>
> Where this way stops: Two correct but separate rules are L1. Executing the two in sequence is L2. A relational answer may be correct or a relational error.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:boolean_expression@L1#1 | not applied |  |  | 0.0 |  |  |
| lvl:boolean_expression@L1#0 | not applied |  |  | 0.0 |  |  |
| lvl:boolean_expression@L3#5 | not applied |  |  | 0.0 |  |  |

#### increment_operators, misconceptions: 5 edges offered
Edges offered:
| edge |
|---|
| mis:increment_operators->IdiomOverridesCode \| wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. |
| mis:increment_operators->IncrementByTwo \| wrong rule: i++ increases i by 2. \| right rule: i++ (and ++i) increases i by exactly 1. |
| mis:increment_operators->PostIncrementAssignsLater \| wrong rule: i = i++ increases i by 1. \| right rule: i++ evaluates to the old value, so i = i++ stores the old value back. |
| mis:increment_operators->PreIncrementBeforeLoop \| wrong rule: ++i in the for-update runs before the body each pass \| right rule: The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s. |
| mis:increment_operators->PrePostIncrementSameValue \| wrong rule: x = i++ and x = ++i store the same value in x. \| right rule: Both increment i, but ++i has the value after the increment and i++ the value before. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:increment_operators->IdiomOverridesCode (0.50), mis:increment_operators->PreIncrementBeforeLoop (0.30), mis:increment_operators->IncrementByTwo (0.20)
```
Kept by pruning: mis:increment_operators->IdiomOverridesCode (0.50), mis:increment_operators->PreIncrementBeforeLoop (0.30), mis:increment_operators->IncrementByTwo (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:increment_operators->IdiomOverridesCode \| wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. |
| mis:increment_operators->PreIncrementBeforeLoop \| wrong rule: ++i in the for-update runs before the body each pass \| right rule: The update runs after each pass of the body, so with either ++i or i++ the first pass uses i = s. |
| mis:increment_operators->IncrementByTwo \| wrong rule: i++ increases i by 2. \| right rule: i++ (and ++i) increases i by exactly 1. |
Model's reply:
```
mis:increment_operators->IdiomOverridesCode | not applied | clauses: none | confidence: 0.9
mis:increment_operators->PreIncrementBeforeLoop | not applied | clauses: none | confidence: 0.9
mis:increment_operators->IncrementByTwo | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:increment_operators->IdiomOverridesCode | not applied |  |  | 0.0 |  |  |
| mis:increment_operators->PreIncrementBeforeLoop | not applied |  |  | 0.0 |  |  |
| mis:increment_operators->IncrementByTwo | not applied |  |  | 0.0 |  |  |

#### increment_operators, level ways: 16 edges offered
Edges offered:
| edge |
|---|
| lvl:increment_operators@L0#0 \| level L0 way everyday_reading: Folk meaning: '++' reads as 'plus plus' (add twice) or as a maths symbol with no effect, and i++ inside an expression is read as 'add 1 at some later time'. In Java i++ and ++i each add exactly 1 to i immediately when evaluated; they differ only in the value the expression yields. |
| lvl:increment_operators@L0#3 \| level L0 way inconsistent_trace: Applies the increment rule (LT) unevenly: uses the old value in one expression and the new value in another for the same i++, or performs the increment at the end of the loop body instead of where it is written. (here mixing in: "x = i++ and x = ++i store the same value in x") |
| lvl:increment_operators@L1#0 \| level L1 way names_the_element: ++ and -- are the increment and decrement operators: shorthand that adds 1 to (or subtracts 1 from) a numeric variable. |
| lvl:increment_operators@L1#1 \| level L1 way states_the_rule: ++ has the same effect as i = i + 1 and -- the same as i = i - 1; as statements i++ and ++i are the same, but in expressions ++i has the value after the increment and i++ the value before. |
| lvl:increment_operators@L2#0 \| level L2 way line_by_line_trace: i++: fetch the value of i (that is the expression's value), then store i + 1 into i. ++i: store i + 1 into i, and the new value is the expression's value. Both happen before the rest of the enclosing expression continues. |
| lvl:increment_operators@L2#1 \| level L2 way output_prediction: With i = 5: x = i++ gives x = 5, i = 6; x = ++i gives x = 6, i = 6; i = i++ leaves i = 5. |
| lvl:increment_operators@L2#2 \| level L2 way one_step_execution: One execution changes exactly one variable (i) by exactly 1 and returns its old (i++) or new (++i) value. |
| lvl:increment_operators@L3#0 \| level L3 way relation_to_neighbour: The usual for-loop update is i++ (shorthand for i = i + 1); as a stand-alone update statement ++i and i++ give the same loop. |
| lvl:increment_operators@L3#1 \| level L3 way relation_to_neighbour: Inside a larger expression the result depends on which value (old or new) the increment yields and on left-to-right evaluation, e.g. j += j++ in Exercise 1.3.6. |
| lvl:increment_operators@L3#2 \| level L3 way relation_to_neighbour: i++ is shorthand for the assignment i = i + 1 (and i += k for i = i + k), so it changes the variable's stored value. |
| lvl:increment_operators@L3#3 \| level L3 way relation_to_neighbour: i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, *=, /=, %=). |
| lvl:increment_operators@L3#4 \| level L3 way purpose_of_the_whole: Plan/role: the update of a stepper or counter (count++ in a counter, i++ in a counted loop). |
| lvl:increment_operators@L4#0 \| level L4 way predict_a_change: As a stand-alone statement, replacing i++ by ++i, i += 1 or i = i + 1 preserves behaviour; inside an expression (x = i++ vs x = ++i) the swap changes the value used by 1. |
| lvl:increment_operators@L4#1 \| level L4 way transfer_to_a_new_program: Use i++ / i-- as stand-alone statements and in for-loop updates; avoid them inside larger expressions (x = ++i), as the book does, and use += for steps other than 1. |
| lvl:increment_operators@L4#2 \| level L4 way diagnose_an_error: rule broken: i = i++ stores the old value back. Kind: silent logic error. Trigger class: Writing i = i++ to increment: i never changes, so a loop driven by it is infinite. |
| lvl:increment_operators@L4#3 \| level L4 way diagnose_an_error: rule broken: ++ and -- apply only to a variable. Kind: compile-time. Trigger class: Applying ++ to a value that is not a variable, e.g. 5++ or (i + 1)++: compile-time error. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:increment_operators@L3#0 (Score: 0.4)}
{lvl:increment_operators@L3#4 (Score: 0.35)}
{lvl:increment_operators@L1#0 (Score: 0.25)}
```
Kept by pruning: lvl:increment_operators@L3#0 (0.40), lvl:increment_operators@L3#4 (0.35), lvl:increment_operators@L1#0 (0.25)

Label prompt for level way lvl:increment_operators@L3#0 (the model saw the concept, the way's name 'relation to neighbour', its text, where the way stops and whether the words must be correct; no level):
> The usual for-loop update is i++ (shorthand for i = i + 1); as a stand-alone update statement ++i and i++ give the same loop.
>
> Where this way stops: Two correct but separate rules are L1. Executing the two in sequence is L2. A relational answer may be correct or a relational error.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.93
```

Label prompt for level way lvl:increment_operators@L3#4 (the model saw the concept, the way's name 'purpose of the whole', its text, where the way stops and whether the words must be correct; no level):
> Plan/role: the update of a stepper or counter (count++ in a counter, i++ in a counted loop).
>
> Where this way stops: Narrating the lines is L2. A purpose induced from a few traced cases is L2. A wrong purpose is still L3, but with an error.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.92
```

Label prompt for level way lvl:increment_operators@L1#0 (the model saw only the concept, the way's name 'names the element' and its text; no level):
> ++ and -- are the increment and decrement operators: shorthand that adds 1 to (or subtracts 1 from) a numeric variable.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.92
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:increment_operators@L3#0 | not applied |  |  | 0.0 |  |  |
| lvl:increment_operators@L3#4 | not applied |  |  | 0.0 |  |  |
| lvl:increment_operators@L1#0 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth:** nothing

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | The program has two System.out.println statements and one for loop | not covered yet |
| c2 | The for loop has a header with a start, a condition and an update, and a body | pre:loop_control->for_loop |

**Graph check, not yet read (the walk may not stop while these remain):** par:assignment~comparison_operators, pre:assignment->increment_operators, pre:comparison_operators->boolean_expression, pre:expression->comparison_operators

**Figure 6 (the graph after depth 3)**

![Figure 6](figure06.png)
## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on [], broken at [], prerequisites {'increment_operators': ['assignment', 'loop_control'], 'boolean_expression': ['comparison_operators'], 'comparison_operators': ['expression'], 'loop_body': ['for_loop'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable'], 'control_flow': ['statement'], 'println': ['statement']}
- control_flow: L1 via names_the_element "The program has two System.out.println statements and one for loop; The for loop has a header with a start, a condition and an update, and a body"
- for_loop: L1 via names_the_element "The for loop has a header with a start, a condition and an update, and a body"
- loop_body: L1 via names_the_element "The for loop has a header with a start, a condition and an update, and a body"
- loop_control: L1 via names_the_element "The for loop has a header with a start, a condition and an update, and a body"
- println: L1 via names_the_element "The program has two System.out.println statements and one for loop"

**Stop:** max depth at depth 3; prompts {'prune': 24, 'label': 45}, fresh model calls 0, cache hits 69

### Held misconceptions
(none)

### Broken concept edges
(none)

### Root cause: none

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| control_flow | L1 | names_the_element |  | level_way | The program has two System.out.println statements and one for loop; The for loop has a header with a start, a condition and an update, and a body |  |  |  |
| for_loop | L1 | names_the_element |  | level_way | The for loop has a header with a start, a condition and an update, and a body |  | L1 states_the_rule |  |
| loop_body | L1 | names_the_element |  | level_way | The for loop has a header with a start, a condition and an update, and a body |  |  |  |
| loop_control | L1 | names_the_element |  | level_way | The for loop has a header with a start, a condition and an update, and a body |  |  |  |
| println | L1 | names_the_element |  | level_way | The program has two System.out.println statements and one for loop |  |  |  |

### Overall level: L1

Clause coverage (final):
| clause | covered by |
|---|---|
| The program has two System.out.println statements and one for loop | lvl:control_flow@L1#0 |
| The for loop has a header with a start, a condition and an update, and a body | lvl:for_loop@L1#0 |

**Figure 7 (final picture)**

![Figure 7](figure07.png)
## 5. Every labelled edge (the evidence list, kept or not)
| depth | source | edge | kind | label | prune_score | confidence | score | clauses | quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | for_loop | lvl:for_loop@L1#0 | level | shown | 0.6 | 0.85 | 0.51 | [2] | The for loop has a header with a start, a condition and an update, and a body |
| 1 | for_loop | lvl:for_loop@L1#1 | level | shown | 0.25 | 0.65 | 0.1625 | [2] | The for loop has a header with a start, a condition and an update, and a body |
| 1 | loop_control | lvl:loop_control@L1#0 | level | shown | 0.5 | 0.7 | 0.35 | [2] | The for loop has a header with a start, a condition and an update, and a body |
| 1 | loop_body | lvl:loop_body@L1#0 | level | shown | 0.6000000000000001 | 0.6 | 0.36 | [2] | The for loop has a header with a start, a condition and an update, and a body |
| 2 | for_loop | pre:loop_control->for_loop | prerequisite | confirmed | 0.6 | 0.6 | 0.36 | [2] | The for loop has a header with a start, a condition and an update, and a body |
| 2 | control_flow | lvl:control_flow@L1#0 | level | shown | 0.6 | 0.6 | 0.36 | [1, 2] | The program has two System.out.println statements and one for loop; The for loop has a header with a start, a condition and an update, and a body |
| 2 | println | lvl:println@L1#0 | level | shown | 0.6000000000000001 | 0.6 | 0.36 | [1] | The program has two System.out.println statements and one for loop |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | for_loop | lvl:for_loop@L1#0 | level | shown | 0.51 | [2] |
| 1 | loop_body | lvl:loop_body@L1#0 | level | shown | 0.36 | [2] |
| 1 | loop_control | lvl:loop_control@L1#0 | level | shown | 0.35 | [2] |
| 2 | for_loop | pre:loop_control->for_loop | prerequisite | confirmed | 0.36 | [2] |
| 2 | control_flow | lvl:control_flow@L1#0 | level | shown | 0.36 | [1, 2] |
| 2 | println | lvl:println@L1#0 | level | shown | 0.36 | [1] |

## 7. Raw traversal log
```
clauses: The program has two System.out.println statements and one for loop | The for loop has a header with a start, a condition and an update, and a body
start: BM25 of the answer against each tagged concept: for_loop 15.43 (hits 1), loop_control 11.85 (hits 1), loop_body 11.75 (hits 1), control_flow 10.92 (hits 1), println 10.77 (hits 1), increment_operators 9.27 (hits 1), boolean_expression 9.14 (hits 1), loop_variable 8.05 (hits 1), comparison_operators 7.48 (hits 1)
start: chosen for_loop, loop_control, loop_body
start concepts (3): for_loop, loop_control, loop_body
--- depth 1: current concepts ['for_loop', 'loop_control', 'loop_body']
  for_loop (misconceptions): 20 candidates -> kept mis:for_loop->ForLoopPartSkipped (0.40), mis:for_loop->LoopHeaderIsEquations (0.35), err:for_loop->BracelessMultiStatementBody (0.25)
    mis:for_loop->ForLoopPartSkipped -> not applied (0.00) ""
    mis:for_loop->LoopHeaderIsEquations -> not applied (0.00) ""
    err:for_loop->BracelessMultiStatementBody -> not applied (0.00) ""
  for_loop (level ways): 24 candidates -> kept lvl:for_loop@L1#0 (0.60), lvl:for_loop@L1#1 (0.25), lvl:for_loop@L3#0 (0.15)
    lvl:for_loop@L1#0 -> shown (0.51) "The for loop has a header with a start, a condition and an update, and a body"
    lvl:for_loop@L1#1 -> shown (0.16) "The for loop has a header with a start, a condition and an update, and a body"
    lvl:for_loop@L3#0 -> not applied (0.00) ""
  loop_control (misconceptions): 11 candidates -> kept mis:loop_control->ForLoopPartSkipped (0.40), mis:loop_control->LoopHeaderIsEquations (0.35), err:loop_control->WrongIterationCount (0.25)
    mis:loop_control->ForLoopPartSkipped -> not applied (0.00) ""
    mis:loop_control->LoopHeaderIsEquations -> not applied (0.00) ""
    err:loop_control->WrongIterationCount -> not applied (0.00) ""
  loop_control (level ways): 19 candidates -> kept lvl:loop_control@L1#0 (0.50), lvl:loop_control@L3#1 (0.30), lvl:loop_control@L1#1 (0.20)
    lvl:loop_control@L1#0 -> shown (0.35) "The for loop has a header with a start, a condition and an update, and a body"
    lvl:loop_control@L3#1 -> not applied (0.00) ""
    lvl:loop_control@L1#1 -> not applied (0.00) ""
  loop_body (misconceptions): 12 candidates -> kept mis:loop_body->ForLoopPartSkipped (0.50), err:loop_body->BracelessMultiStatementBody (0.30), mis:loop_body->StatementAfterLoopInBody (0.20)
    mis:loop_body->ForLoopPartSkipped -> not applied (0.00) ""
    err:loop_body->BracelessMultiStatementBody -> not applied (0.00) ""
    mis:loop_body->StatementAfterLoopInBody -> not applied (0.00) ""
  loop_body (level ways): 14 candidates -> kept lvl:loop_body@L1#0 (0.60), lvl:loop_body@L1#1 (0.30), lvl:loop_body@L0#0 (0.10)
    lvl:loop_body@L1#0 -> shown (0.36) "The for loop has a header with a start, a condition and an update, and a body"
    lvl:loop_body@L1#1 -> not applied (0.00) ""
    lvl:loop_body@L0#0 -> not applied (0.00) ""
  kept: lvl:for_loop@L1#0 [shown, tier 2, 0.51], lvl:loop_body@L1#0 [shown, tier 2, 0.36], lvl:loop_control@L1#0 [shown, tier 2, 0.35]
  clause coverage: c1 uncovered; c2 uncovered
  uncovered clauses bring in: control_flow (14.56), println (13.60), loop_variable (11.67)
  not yet read: own edges of control_flow, own edges of loop_variable, own edges of println, pre:for_loop->loop_body, pre:loop_control->for_loop, pre:loop_control->increment_operators, pre:loop_variable->loop_control
--- depth 2: current concepts ['for_loop', 'loop_control', 'loop_body', 'control_flow', 'println', 'loop_variable']
  for_loop (concept edges): 2 candidates -> kept pre:loop_control->for_loop (0.60), pre:for_loop->loop_body (0.40)
    pre:loop_control->for_loop -> confirmed (0.36) "The for loop has a header with a start, a condition and an update, and a body"
    pre:for_loop->loop_body -> not applied (0.00) ""
  loop_control (concept edges): 2 candidates -> kept pre:loop_variable->loop_control (0.80), pre:loop_control->increment_operators (0.20)
    pre:loop_variable->loop_control -> not applied (0.00) ""
    pre:loop_control->increment_operators -> not applied (0.00) ""
  control_flow (misconceptions): 11 candidates -> kept mis:control_flow->FalseLoopRepeatsNextCode (0.40), mis:control_flow->ProgramEndsAfterLoop (0.35), mis:control_flow->StatementsRunInAnyOrder (0.25)
    mis:control_flow->FalseLoopRepeatsNextCode -> not applied (0.00) ""
    mis:control_flow->ProgramEndsAfterLoop -> not applied (0.00) ""
    mis:control_flow->StatementsRunInAnyOrder -> not applied (0.00) ""
  control_flow (level ways): 15 candidates -> kept lvl:control_flow@L1#0 (0.60), lvl:control_flow@L1#1 (0.25), lvl:control_flow@L3#0 (0.15)
    lvl:control_flow@L1#0 -> shown (0.36) "The program has two System.out.println statements and one for loop; The for loop has a header with a start, a condition and an update, and a body"
    lvl:control_flow@L1#1 -> not applied (0.00) ""
    lvl:control_flow@L3#0 -> not applied (0.00) ""
  println (misconceptions): 6 candidates -> kept mis:println->IdentifierCaseInsensitive (0.40), mis:println->ParenthesesOnlyIfArgument (0.35), mis:println->PrintedTextIsExecuted (0.25)
    mis:println->IdentifierCaseInsensitive -> not applied (0.00) ""
    mis:println->ParenthesesOnlyIfArgument -> not applied (0.00) ""
    mis:println->PrintedTextIsExecuted -> not applied (0.00) ""
  println (level ways): 17 candidates -> kept lvl:println@L1#0 (0.60), lvl:println@L3#0 (0.30), lvl:println@L1#1 (0.10)
    lvl:println@L1#0 -> shown (0.36) "The program has two System.out.println statements and one for loop"
    lvl:println@L3#0 -> not applied (0.00) ""
    lvl:println@L1#1 -> not applied (0.00) ""
  loop_variable (misconceptions): 7 candidates -> kept mis:loop_variable->ForInitRepeats (0.40), mis:loop_variable->BodyChangeIgnoredByCondition (0.35), mis:loop_variable->LoopUpdateChangesDirection (0.25)
    mis:loop_variable->ForInitRepeats -> not applied (0.00) ""
    mis:loop_variable->BodyChangeIgnoredByCondition -> not applied (0.00) ""
    mis:loop_variable->LoopUpdateChangesDirection -> not applied (0.00) ""
  loop_variable (level ways): 13 candidates -> kept lvl:loop_variable@L1#0 (0.50), lvl:loop_variable@L1#1 (0.30), lvl:loop_variable@L3#0 (0.20)
    lvl:loop_variable@L1#0 -> not applied (0.00) ""
    lvl:loop_variable@L1#1 -> not applied (0.00) ""
    lvl:loop_variable@L3#0 -> not applied (0.00) ""
  kept: pre:loop_control->for_loop [confirmed, tier 2, 0.36], lvl:control_flow@L1#0 [shown, tier 2, 0.36], lvl:println@L1#0 [shown, tier 2, 0.36]
  clause coverage: c1 uncovered; c2 <- pre:loop_control->for_loop
  uncovered clauses bring in: comparison_operators (3.62), boolean_expression (3.48), increment_operators (3.32)
  not yet read: own edges of boolean_expression, own edges of comparison_operators, own edges of increment_operators, pre:statement->control_flow, pre:statement->println
--- depth 3: current concepts ['loop_control', 'for_loop', 'control_flow', 'println', 'comparison_operators', 'boolean_expression', 'increment_operators']
  loop_control (concept edges): 2 candidates -> kept pre:loop_variable->loop_control (0.80), pre:loop_control->increment_operators (0.20)
    pre:loop_variable->loop_control -> not applied (0.00) ""
    pre:loop_control->increment_operators -> not applied (0.00) ""
  for_loop (concept edges): 1 candidates -> kept pre:for_loop->loop_body (1.00)
    pre:for_loop->loop_body -> not applied (0.00) ""
  control_flow (concept edges): 1 candidates -> kept pre:statement->control_flow (1.00)
    pre:statement->control_flow -> not applied (0.00) ""
  println (concept edges): 1 candidates -> kept pre:statement->println (1.00)
    pre:statement->println -> not applied (0.00) ""
  comparison_operators (misconceptions): 8 candidates -> kept mis:comparison_operators->LessGreaterSwapped (0.50), err:comparison_operators->ReversedRelationalOperator (0.30), mis:comparison_operators->AssignCompares (0.20)
    mis:comparison_operators->LessGreaterSwapped -> not applied (0.00) ""
    err:comparison_operators->ReversedRelationalOperator -> not applied (0.00) ""
    mis:comparison_operators->AssignCompares -> not applied (0.00) ""
  comparison_operators (level ways): 20 candidates -> kept lvl:comparison_operators@L1#0 (0.50), lvl:comparison_operators@L3#5 (0.30), lvl:comparison_operators@L3#1 (0.20)
    lvl:comparison_operators@L1#0 -> not applied (0.00) ""
    lvl:comparison_operators@L3#5 -> not applied (0.00) ""
    lvl:comparison_operators@L3#1 -> not applied (0.00) ""
  boolean_expression (misconceptions): 8 candidates -> kept mis:boolean_expression->LoopForOneTimeTest (0.50), mis:boolean_expression->ArithmeticInsteadOfBoolean (0.30), mis:boolean_expression->ChainedComparison (0.20)
    mis:boolean_expression->LoopForOneTimeTest -> not applied (0.00) ""
    mis:boolean_expression->ArithmeticInsteadOfBoolean -> not applied (0.00) ""
    mis:boolean_expression->ChainedComparison -> not applied (0.00) ""
  boolean_expression (level ways): 19 candidates -> kept lvl:boolean_expression@L1#1 (0.50), lvl:boolean_expression@L1#0 (0.30), lvl:boolean_expression@L3#5 (0.20)
    lvl:boolean_expression@L1#1 -> not applied (0.00) ""
    lvl:boolean_expression@L1#0 -> not applied (0.00) ""
    lvl:boolean_expression@L3#5 -> not applied (0.00) ""
  increment_operators (misconceptions): 5 candidates -> kept mis:increment_operators->IdiomOverridesCode (0.50), mis:increment_operators->PreIncrementBeforeLoop (0.30), mis:increment_operators->IncrementByTwo (0.20)
    mis:increment_operators->IdiomOverridesCode -> not applied (0.00) ""
    mis:increment_operators->PreIncrementBeforeLoop -> not applied (0.00) ""
    mis:increment_operators->IncrementByTwo -> not applied (0.00) ""
  increment_operators (level ways): 16 candidates -> kept lvl:increment_operators@L3#0 (0.40), lvl:increment_operators@L3#4 (0.35), lvl:increment_operators@L1#0 (0.25)
    lvl:increment_operators@L3#0 -> not applied (0.00) ""
    lvl:increment_operators@L3#4 -> not applied (0.00) ""
    lvl:increment_operators@L1#0 -> not applied (0.00) ""
  nothing kept at this depth
  clause coverage: c1 uncovered; c2 <- pre:loop_control->for_loop
  not yet read: par:assignment~comparison_operators, pre:assignment->increment_operators, pre:comparison_operators->boolean_expression, pre:expression->comparison_operators
  root-cause walk: held on [], broken at [], prerequisites {'increment_operators': ['assignment', 'loop_control'], 'boolean_expression': ['comparison_operators'], 'comparison_operators': ['expression'], 'loop_body': ['for_loop'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable'], 'control_flow': ['statement'], 'println': ['statement']}
  level control_flow: L1 via names_the_element "The program has two System.out.println statements and one for loop; The for loop has a header with a start, a condition and an update, and a body"
  level for_loop: L1 via names_the_element "The for loop has a header with a start, a condition and an update, and a body"
  level loop_body: L1 via names_the_element "The for loop has a header with a start, a condition and an update, and a body"
  level loop_control: L1 via names_the_element "The for loop has a header with a start, a condition and an update, and a body"
  level println: L1 via names_the_element "The program has two System.out.println statements and one for loop"
```

## 8. Full diagnosis JSON
```json
{
 "scenario": "LP08",
 "settings": {
  "width": 3,
  "depth": 3,
  "prune_tools": "llm",
  "model": "claude-opus-5-5",
  "backend": "claude-cli",
  "rule_fixes": true,
  "level_v2": true
 },
 "clauses": [
  "The program has two System.out.println statements and one for loop",
  "The for loop has a header with a start, a condition and an update, and a body"
 ],
 "start_concepts": [
  "for_loop",
  "loop_control",
  "loop_body"
 ],
 "held_misconceptions": [],
 "error_evidence": [],
 "shadowed": [],
 "broken_edges": [],
 "root_cause": null,
 "levels": {
  "control_flow": {
   "level": "L1",
   "way": "names_the_element",
   "quote": "The program has two System.out.println statements and one for loop; The for loop has a header with a start, a condition and an update, and a body",
   "edge": "lvl:control_flow@L1#0",
   "source": "level_way",
   "also_shown": []
  },
  "for_loop": {
   "level": "L1",
   "way": "names_the_element",
   "quote": "The for loop has a header with a start, a condition and an update, and a body",
   "edge": "lvl:for_loop@L1#0",
   "source": "level_way",
   "also_shown": [
    "L1 states_the_rule"
   ]
  },
  "loop_body": {
   "level": "L1",
   "way": "names_the_element",
   "quote": "The for loop has a header with a start, a condition and an update, and a body",
   "edge": "lvl:loop_body@L1#0",
   "source": "level_way",
   "also_shown": []
  },
  "loop_control": {
   "level": "L1",
   "way": "names_the_element",
   "quote": "The for loop has a header with a start, a condition and an update, and a body",
   "edge": "lvl:loop_control@L1#0",
   "source": "level_way",
   "also_shown": []
  },
  "println": {
   "level": "L1",
   "way": "names_the_element",
   "quote": "The program has two System.out.println statements and one for loop",
   "edge": "lvl:println@L1#0",
   "source": "level_way",
   "also_shown": []
  }
 },
 "overall_level": "L1",
 "paths": [
  {
   "depth": 1,
   "source": "for_loop",
   "edge": "lvl:for_loop@L1#0",
   "target": "for_loop@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "The for loop has a header with a start, a condition and an update, and a body",
   "confidence": 0.85,
   "prune_score": 0.6,
   "score": 0.51,
   "logic": "The for statement is a loop that packages an initialization, a loop-continuation condition and an increment in its header around a body.",
   "twin_logic": null,
   "level": "L1",
   "way": "names_the_element"
  },
  {
   "depth": 1,
   "source": "loop_body",
   "edge": "lvl:loop_body@L1#0",
   "target": "loop_body@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "The for loop has a header with a start, a condition and an update, and a body",
   "confidence": 0.6,
   "prune_score": 0.6000000000000001,
   "score": 0.36,
   "logic": "The loop body is the statement block that a loop repeats on each pass.",
   "twin_logic": null,
   "level": "L1",
   "way": "names_the_element"
  },
  {
   "depth": 1,
   "source": "loop_control",
   "edge": "lvl:loop_control@L1#0",
   "target": "loop_control@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "The for loop has a header with a start, a condition and an update, and a body",
   "confidence": 0.7,
   "prune_score": 0.5,
   "score": 0.35,
   "logic": "Loop control is the init / continuation condition / increment scheme on an index variable that decides how many passes a loop makes and with which values.",
   "twin_logic": null,
   "level": "L1",
   "way": "names_the_element"
  },
  {
   "depth": 2,
   "source": "for_loop",
   "edge": "pre:loop_control->for_loop",
   "target": "loop_control",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    2
   ],
   "quote": "The for loop has a header with a start, a condition and an update, and a body",
   "confidence": 0.6,
   "prune_score": 0.6,
   "score": 0.36,
   "logic": "The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "control_flow",
   "edge": "lvl:control_flow@L1#0",
   "target": "control_flow@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2
   ],
   "quote": "The program has two System.out.println statements and one for loop; The for loop has a header with a start, a condition and an update, and a body",
   "confidence": 0.6,
   "prune_score": 0.6,
   "score": 0.36,
   "logic": "Control flow is the order in which a program's statements are executed (statement sequencing); conditionals and loops are the statements that change it.",
   "twin_logic": null,
   "level": "L1",
   "way": "names_the_element"
  },
  {
   "depth": 2,
   "source": "println",
   "edge": "lvl:println@L1#0",
   "target": "println@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "The program has two System.out.println statements and one for loop",
   "confidence": 0.6,
   "prune_score": 0.6000000000000001,
   "score": 0.36,
   "logic": "System.out.println is a library method that prints its argument followed by a line terminator ('print line').",
   "twin_logic": null,
   "level": "L1",
   "way": "names_the_element"
  }
 ],
 "evidence": [
  {
   "depth": 1,
   "source": "for_loop",
   "edge": "lvl:for_loop@L1#0",
   "target": "for_loop@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "The for loop has a header with a start, a condition and an update, and a body",
   "confidence": 0.85,
   "prune_score": 0.6,
   "score": 0.51,
   "logic": "The for statement is a loop that packages an initialization, a loop-continuation condition and an increment in its header around a body.",
   "twin_logic": null,
   "level": "L1",
   "way": "names_the_element"
  },
  {
   "depth": 1,
   "source": "for_loop",
   "edge": "lvl:for_loop@L1#1",
   "target": "for_loop@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "The for loop has a header with a start, a condition and an update, and a body",
   "confidence": 0.65,
   "prune_score": 0.25,
   "score": 0.1625,
   "logic": "Syntax: for (<initialize>; <boolean expression>; <increment>) { <statements> }, with the three parts separated by semicolons; it is, with only a few exceptions, equivalent to <initialize>; while (<boolean expression>) { <statements> <increment>; }.",
   "twin_logic": null,
   "level": "L1",
   "way": "states_the_rule"
  },
  {
   "depth": 1,
   "source": "loop_control",
   "edge": "lvl:loop_control@L1#0",
   "target": "loop_control@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "The for loop has a header with a start, a condition and an update, and a body",
   "confidence": 0.7,
   "prune_score": 0.5,
   "score": 0.35,
   "logic": "Loop control is the init / continuation condition / increment scheme on an index variable that decides how many passes a loop makes and with which values.",
   "twin_logic": null,
   "level": "L1",
   "way": "names_the_element"
  },
  {
   "depth": 1,
   "source": "loop_body",
   "edge": "lvl:loop_body@L1#0",
   "target": "loop_body@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "The for loop has a header with a start, a condition and an update, and a body",
   "confidence": 0.6,
   "prune_score": 0.6000000000000001,
   "score": 0.36,
   "logic": "The loop body is the statement block that a loop repeats on each pass.",
   "twin_logic": null,
   "level": "L1",
   "way": "names_the_element"
  },
  {
   "depth": 2,
   "source": "for_loop",
   "edge": "pre:loop_control->for_loop",
   "target": "loop_control",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    2
   ],
   "quote": "The for loop has a header with a start, a condition and an update, and a body",
   "confidence": 0.6,
   "prune_score": 0.6,
   "score": 0.36,
   "logic": "The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "control_flow",
   "edge": "lvl:control_flow@L1#0",
   "target": "control_flow@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2
   ],
   "quote": "The program has two System.out.println statements and one for loop; The for loop has a header with a start, a condition and an update, and a body",
   "confidence": 0.6,
   "prune_score": 0.6,
   "score": 0.36,
   "logic": "Control flow is the order in which a program's statements are executed (statement sequencing); conditionals and loops are the statements that change it.",
   "twin_logic": null,
   "level": "L1",
   "way": "names_the_element"
  },
  {
   "depth": 2,
   "source": "println",
   "edge": "lvl:println@L1#0",
   "target": "println@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "The program has two System.out.println statements and one for loop",
   "confidence": 0.6,
   "prune_score": 0.6000000000000001,
   "score": 0.36,
   "logic": "System.out.println is a library method that prints its argument followed by a line terminator ('print line').",
   "twin_logic": null,
   "level": "L1",
   "way": "names_the_element"
  }
 ],
 "clause_coverage": {
  "The program has two System.out.println statements and one for loop": "lvl:control_flow@L1#0",
  "The for loop has a header with a start, a condition and an update, and a body": "lvl:for_loop@L1#0"
 },
 "unexplained_clauses": [],
 "stop_reason": "max depth",
 "depth_reached": 3,
 "llm_calls": 0,
 "llm_cache_hits": 69,
 "llm_calls_by_step": {
  "prune": 24,
  "label": 45
 },
 "level_v2": {
  "wrong_ways": [],
  "not_counted": []
 }
}
```
