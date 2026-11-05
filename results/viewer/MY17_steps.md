# Think on the Graph: every output of the run MY17
## 0. Input
Program:
```java
int[] a = {2, 4, 6};
int sum = 0;
for (int i = 0; i < a.length; i++) {
    sum += a[i];
}
System.out.println("Total: " + sum);
```
Question: Explain how the loop computes the total, and what would change if a fourth element, 8, were added.

Student's answer: The loop visits each index from 0 to a.length - 1 and adds that element to sum, so it prints Total: 12. With 8 added, a.length becomes 4, so the loop runs once more and prints Total: 20, with no other change to the code
Settings: width 3, depth 3, prune llm, backend claude-cli, model claude-opus-5-5
## 1. Stage 1: the subgraph G from the code (no model)
Masked code (string and char literals and comments blanked; this is what the patterns see):
```
int[] a = {2, 4, 6};
int sum = 0;
for (int i = 0; i < a.length; i++) {
    sum += a[i];
}
System.out.println("       " + sum);
```
Which code text tagged which concept (a generic concept fires on almost any Java line; it starts the walk only if the answer repeats its tag):
| concept | generic | channel | matched text | line |
|---|---|---|---|---|
| accumulator_pattern | False | pattern | 'sum += a[i];' | 4 |
| array_bounds | False | pattern | 'i < a.length' | 3 |
| array_declaration | False | pattern | 'int[] a' | 1 |
| array_initializer | False | pattern | '= {' | 1 |
| array_traversal | False | pattern | 'for (int i = 0; i < a.length' | 3 |
| array_traversal | False | pattern | 'for (int i = 0; i < a.length; i++) {\n    sum += a[i]' | 3 |
| assignment | True | pattern | '=' | 1 |
| boolean_expression | False | pattern | 'for (int i = 0; i < a.length;' | 3 |
| comparison_operators | False | pattern | 'for (int i = 0; i <' | 3 |
| compound_assignment | False | pattern | '+=' | 4 |
| control_flow | False | pattern | 'for (' | 3 |
| data_structure | False | pattern | 'int[]' | 1 |
| data_type | True | pattern | 'int' | 1 |
| expression | True | pattern | 'i <' | 3 |
| expression | True | pattern | '= {2, 4, 6};' | 1 |
| for_loop | False | pattern | 'for (' | 3 |
| increment_operators | False | pattern | '++' | 3 |
| indexing | False | pattern | 'a[i]' | 4 |
| length_field | False | pattern | '.length' | 3 |
| loop_body | False | pattern | 'for (' | 3 |
| loop_control | False | signal | 'for (int i = 0; i < a.length; i++)' | 3 |
| loop_scope | False | pattern | 'for (int i' | 3 |
| loop_variable | False | pattern | 'for (int i =' | 3 |
| println | False | pattern | 'System.out.println(' | 6 |
| statement | True | pattern | ';' | 1 |
| string_concatenation | False | pattern | '"Total: " +' | 6 |
| string_conversion | False | pattern | '" + sum' | 6 |
| string_literal | True | pattern | '"Total: "' | 6 |

G: 26 concept nodes (5 generic), 26 concept edges, 162 misconception / error edges, 117 misconception / error nodes, 130 level nodes, 182 level-misconception links, 3 connected piece(s).
Note: concept nodes form 3 pieces (the KG has no edge between them): accumulator_pattern,array_bounds,array_declaration,array_initializer,array_traversal,assignment,boolean_expression,comparison_operators,compound_assignment,data_structure,data_type,expression,for_loop,increment_operators,indexing,length_field,loop_body,loop_control,loop_scope,loop_variable | control_flow,println,statement,string_literal | string_concatenation,string_conversion

Concept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):
| edge | type | rule (logic) |
|---|---|---|
| par:assignment~comparison_operators | parallel | x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands. |
| par:increment_operators~compound_assignment | parallel | i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, *=, /=, %=). |
| pre:array_declaration->array_initializer | prerequisite | int[] a = {1, 2, 3}; declares the array variable and creates and fills the array in one statement. |
| pre:array_initializer->indexing | prerequisite | The values listed in braces are stored at indices 0, 1, 2, ... in order, and a[i] reads the value at index i. |
| pre:array_initializer->length_field | prerequisite | An array made from a literal has as many elements as values listed, and a.length gives that number. |
| pre:assignment->compound_assignment | prerequisite | x op= e is shorthand for the assignment x = x op e. |
| pre:assignment->increment_operators | prerequisite | i++ is shorthand for the assignment i = i + 1. |
| pre:comparison_operators->boolean_expression | prerequisite | A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making. |
| pre:compound_assignment->accumulator_pattern | prerequisite | sum += x is the usual way a running total is updated on each pass. |
| pre:data_structure->array_declaration | prerequisite | An array is a data structure: one name for a sequence of values of the same type, organised by index. |
| pre:data_type->data_structure | prerequisite | A data structure organizes many values of a data type; the array holds a sequence of values of one type. |
| pre:expression->comparison_operators | prerequisite | Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b. |
| pre:for_loop->array_traversal | prerequisite | for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order. |
| pre:for_loop->loop_body | prerequisite | The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop. |
| pre:for_loop->loop_scope | prerequisite | A variable declared in the for header exists only from its declaration to the end of the for statement's block. |
| pre:indexing->array_bounds | prerequisite | Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used. |
| pre:indexing->array_traversal | prerequisite | A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass. |
| pre:length_field->array_traversal | prerequisite | A traversal loop runs its index from 0 while it is below a.length, so it visits every element once. |
| pre:loop_body->accumulator_pattern | prerequisite | The accumulator update sum += x sits inside the body, so it runs once on every pass. |
| pre:loop_control->for_loop | prerequisite | The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |
| pre:loop_control->increment_operators | prerequisite | The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update. |
| pre:loop_variable->loop_control | prerequisite | The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |
| pre:statement->control_flow | prerequisite | Control flow is the order in which statements run. |
| pre:statement->println | prerequisite | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |
| pre:string_concatenation->string_conversion | prerequisite | When one operand of + is a String, Java converts the other operand to a String before concatenating. |
| pre:string_literal->println | prerequisite | println("s") outputs exactly the characters between the quotes and then ends the line. |

Misconception / error edges per concept (count), and level ways per concept (count):
| concept | misconception / error edges | level ways (L1-L4 + L0 non-misconception) |
|---|---|---|
| accumulator_pattern | 4 | 17 |
| array_bounds | 2 | 14 |
| array_declaration | 4 | 13 |
| array_initializer | 2 | 14 |
| array_traversal | 6 | 22 |
| assignment | 15 | 24 |
| boolean_expression | 8 | 19 |
| comparison_operators | 8 | 20 |
| compound_assignment | 2 | 15 |
| control_flow | 11 | 15 |
| data_structure | 0 | 11 |
| data_type | 2 | 14 |
| expression | 8 | 19 |
| for_loop | 21 | 24 |
| increment_operators | 5 | 16 |
| indexing | 8 | 21 |
| length_field | 2 | 15 |
| loop_body | 12 | 14 |
| loop_control | 11 | 19 |
| loop_scope | 5 | 14 |
| loop_variable | 7 | 13 |
| println | 6 | 17 |
| statement | 5 | 19 |
| string_concatenation | 3 | 16 |
| string_conversion | 1 | 13 |
| string_literal | 4 | 16 |

Figure 1: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY17_figure01.png

Figure 2: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY17_figure02.png

## 2. Clauses and start concepts (no model)
The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):
| clause | text |
|---|---|
| c1 | The loop visits each index from 0 to a.length - 1 and adds that element to sum |
| c2 | so it prints Total: 12 |
| c3 | With 8 added, a.length becomes 4 |
| c4 | so the loop runs once more and prints Total: 20, with no other change to the code |

start: BM25 of the answer against each tagged concept: array_traversal 29.50 (hits 2), for_loop 24.84 (hits 1), loop_control 23.43 (hits 1), accumulator_pattern 22.02 (hits 1), loop_body 21.17 (hits 1), indexing 20.63 (hits 1), loop_variable 20.13 (hits 1), control_flow 19.64 (hits 1), compound_assignment 19.24 (hits 1), increment_operators 18.75 (hits 1), length_field 18.23 (hits 1), array_bounds 15.35 (hits 1), loop_scope 14.90 (hits 1), println 13.88 (hits 1), boolean_expression 13.74 (hits 1), string_concatenation 11.41 (hits 1), array_declaration 10.22 (hits 1), array_initializer 8.87 (hits 1), comparison_operators 6.81 (hits 1), string_conversion 4.35 (hits 1), data_structure 2.30 (hits 1)

start: chosen array_traversal, for_loop, loop_control

start concepts (3): array_traversal, for_loop, loop_control

Start concepts: array_traversal, for_loop, loop_control

Figure 3: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY17_figure03.png

## 3. The walk, depth by depth
At each depth, for each current concept: the edges offered (a concept entering as a start concept offers its misconception / error edges and its level ways, as two families; otherwise it offers its concept edges), the prune prompt and the model's reply, then the label prompt(s) and the model's reply, parsed into label / clauses / confidence. Score = prune score x confidence.

### Depth 1: current concepts 'array_traversal', 'for_loop', 'loop_control'

#### array_traversal, misconceptions: 6 edges offered
Edges offered:
| edge |
|---|
| err:array_traversal->EarlyReturnInLoop \| wrong rule: Leaves a traversal loop with return before every element has been processed. \| right rule: A result that depends on all elements is known only after the loop ends. |
| mis:array_traversal->ArrayUseScansAllCells \| wrong rule: Using an array means every cell must be scanned. \| right rule: Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs. |
| mis:array_traversal->ElementBoundToOldIndex \| wrong rule: After i changes, X[i] still refers to the element at the old value of i. \| right rule: a[i] is evaluated with the current value of i each time it is used. |
| mis:array_traversal->IdiomOverridesCode \| wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. |
| mis:array_traversal->OffByOneBound \| wrong rule: < vs <= and 0..n vs 0..n-1 are interchangeable \| right rule: for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n. |
| mis:array_traversal->WholeArrayArithmetic \| wrong rule: a = a + b adds the arrays element by element. \| right rule: Java has no arithmetic on whole arrays; write a loop that adds a[i] + b[i] for each i. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:array_traversal->OffByOneBound (0.45), mis:array_traversal->IdiomOverridesCode (0.30), mis:array_traversal->ElementBoundToOldIndex (0.25)
```
Kept by pruning: mis:array_traversal->OffByOneBound (0.45), mis:array_traversal->IdiomOverridesCode (0.30), mis:array_traversal->ElementBoundToOldIndex (0.25)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:array_traversal->OffByOneBound \| wrong rule: < vs <= and 0..n vs 0..n-1 are interchangeable \| right rule: for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n. |
| mis:array_traversal->IdiomOverridesCode \| wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. |
| mis:array_traversal->ElementBoundToOldIndex \| wrong rule: After i changes, X[i] still refers to the element at the old value of i. \| right rule: a[i] is evaluated with the current value of i each time it is used. |
Model's reply:
```
mis:array_traversal->OffByOneBound | correct | clauses: 1, 3, 4 | confidence: 0.85
mis:array_traversal->IdiomOverridesCode | not applied | clauses: none | confidence: 0.75
mis:array_traversal->ElementBoundToOldIndex | correct | clauses: 1, 2, 4 | confidence: 0.75
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:array_traversal->OffByOneBound | correct | 0.45 | 0.85 | 0.38 | c1, c3, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| mis:array_traversal->IdiomOverridesCode | not applied |  |  | 0.0 |  |  |
| mis:array_traversal->ElementBoundToOldIndex | correct | 0.25 | 0.75 | 0.19 | c1, c2, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |

#### array_traversal, level ways: 22 edges offered
Edges offered:
| edge |
|---|
| lvl:array_traversal@L0#0 \| level L0 way everyday_reading: Folk meaning: 'go through the list' in English means look at every item once, first to last, so an array loop is assumed to process the whole array whatever its code says. Java rule: the loop visits exactly the indices its initialization, guard and update generate, in that order. |
| lvl:array_traversal@L0#4 \| level L0 way inconsistent_trace: Points to LT: initialize i, test, run the body with the current i, update, test again. Inconsistent application: on some passes the update is applied before the body, or a[i] is traced with the previous i. (here mixing in: "a = a + b adds the arrays element by element") |
| lvl:array_traversal@L1#0 \| level L1 way names_the_element: Identity: a traversal is a loop that steps an index through the array and performs the same operation on each element it visits. |
| lvl:array_traversal@L1#1 \| level L1 way states_the_rule: Declarative: the canonical traversal is 'for (int i = 0; i < a.length; i++) { ... a[i] ... }', which gives i every valid index exactly once, in increasing order; the for loop is equivalent to initialize; while (test) { body; increment; }. |
| lvl:array_traversal@L2#0 \| level L2 way line_by_line_trace: Sequencing: i = 0; test i < a.length; body using a[i]; i++; test; ... When i == a.length the test fails and the body is not executed, so a[a.length] is never touched. |
| lvl:array_traversal@L2#1 \| level L2 way output_prediction: Result: the body runs a.length times, and the result depends on the body. Squaring each element of {1, 2, 3, 4, 5} leaves {1, 4, 9, 16, 25}; summing leaves the total in the accumulator. |
| lvl:array_traversal@L2#2 \| level L2 way one_step_execution: State transition: one pass applies the body to element i (reading or writing a[i] and possibly updating an accumulator), then i increases by 1; no other element is touched unless the body indexes it. |
| lvl:array_traversal@L3#0 \| level L3 way relation_to_neighbour: The loop variable is used as the index, so a[i] reaches a different element on each pass. |
| lvl:array_traversal@L3#1 \| level L3 way relation_to_neighbour: for (int x : a) is a traversal that hands the body each value a[i] and hides the index i. |
| lvl:array_traversal@L3#2 \| level L3 way relation_to_neighbour: for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order; the bound must be < a.length, not <=. |
| lvl:array_traversal@L3#3 \| level L3 way relation_to_neighbour: The sieve traverses isPrime[] once to set every flag to true and again at the end to count the flags still true. |
| lvl:array_traversal@L3#4 \| level L3 way relation_to_neighbour: Reversal traverses only the first half (i < N/2), exchanging each a[i] with its mirror a[N-1-i]. |
| lvl:array_traversal@L3#5 \| level L3 way relation_to_neighbour: Sample points are computed into x[] and y[] by one traversal and drawn by another. |
| lvl:array_traversal@L3#6 \| level L3 way relation_to_neighbour: The running maximum is found in one traversal that keeps the largest value seen so far, starting from Double.NEGATIVE_INFINITY. |
| lvl:array_traversal@L3#7 \| level L3 way relation_to_neighbour: The elements are copied one at a time by a loop over every index. |
| lvl:array_traversal@L3#8 \| level L3 way purpose_of_the_whole: Plan/role: the index is a stepper, and the loop carries out a Soloway-style plan (accumulate/sum with a gatherer, count, search, find the extreme, copy) once for each element. |
| lvl:array_traversal@L4#0 \| level L4 way predict_a_change: Conservation: running the index downward (a.length-1 to 0) visits the same set of elements in reverse order, harmless for a sum but not for a shift. Starting at 1 or stopping at a.length-1 drops an element. Invariant: before pass i, elements 0..i-1 have been processed. |
| lvl:array_traversal@L4#1 \| level L4 way diagnose_an_error: rule broken: A result that depends on all elements is known only after the loop ends. Kind: silent logic error. Trigger class: a return (or break) placed inside the loop body fires on the first element, e.g. returning false/-1 in the else branch of a search, or returning the sum inside the loop |
| lvl:array_traversal@L4#2 \| level L4 way transfer_to_a_new_program: Applicability: use an index traversal when every element (or a contiguous range) must be processed and the index matters (writing a[i], comparing neighbours, reporting positions). Use enhanced for when only the values matter, and stop early when one element settles the answer (search). |
| lvl:array_traversal@L4#3 \| level L4 way diagnose_an_error: rule broken: The guard must be i < a.length. Kind: run-time exception. Trigger class: i <= a.length (or a body that reads a[i+1]) makes the last pass index a.length (ArrayIndexOutOfBoundsException) |
| lvl:array_traversal@L4#4 \| level L4 way diagnose_an_error: rule broken: The traversal must cover every element it is meant to process. Kind: silent logic error. Trigger class: the loop starts at 1 or stops at a.length-1, so an end element is skipped |
| lvl:array_traversal@L4#5 \| level L4 way diagnose_an_error: rule broken: Arithmetic operators do not apply to whole arrays. Kind: compile-time. Trigger class: a + b or a * 2 written for arrays (bad operand types for binary operator) |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:array_traversal@L2#1 (Score: 0.45)}
{lvl:array_traversal@L4#0 (Score: 0.3)}
{lvl:array_traversal@L3#2 (Score: 0.25)}
```
Kept by pruning: lvl:array_traversal@L2#1 (0.45), lvl:array_traversal@L4#0 (0.30), lvl:array_traversal@L3#2 (0.25)

Label prompt for level way lvl:array_traversal@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> Result: the body runs a.length times, and the result depends on the body. Squaring each element of {1, 2, 3, 4, 5} leaves {1, 4, 9, 16, 25}; summing leaves the total in the accumulator.

Model's reply:
```
Label: shown
Clauses: 2, 4
Confidence: 0.9
```

Label prompt for level way lvl:array_traversal@L4#0 (the model saw only the concept, the way's name 'predict a change' and its text; no level):
> Conservation: running the index downward (a.length-1 to 0) visits the same set of elements in reverse order, harmless for a sum but not for a shift. Starting at 1 or stopping at a.length-1 drops an element. Invariant: before pass i, elements 0..i-1 have been processed.

Model's reply:
```
Label: shown
Clauses: 3, 4
Confidence: 0.8
```

Label prompt for level way lvl:array_traversal@L3#2 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order; the bound must be < a.length, not <=.

Model's reply:
```
Label: shown
Clauses: 1, 3, 4
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:array_traversal@L2#1 | shown | 0.45 | 0.9 | 0.41 | c2, c4 | so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |
| lvl:array_traversal@L4#0 | shown | 0.3 | 0.8 | 0.24 | c3, c4 | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| lvl:array_traversal@L3#2 | shown | 0.25 | 0.8 | 0.2 | c1, c3, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |

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
err:for_loop->WrongIterationCount (0.45), mis:for_loop->IdiomOverridesCode (0.30), mis:for_loop->ForIsConditional (0.25)
```
Kept by pruning: err:for_loop->WrongIterationCount (0.45), mis:for_loop->IdiomOverridesCode (0.30), mis:for_loop->ForIsConditional (0.25)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| err:for_loop->WrongIterationCount \| wrong rule: Updates the loop counter so that the loop runs the wrong number of times. \| right rule: The init, test and update together decide the number of passes; trace them to check the count. |
| mis:for_loop->IdiomOverridesCode \| wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. |
| mis:for_loop->ForIsConditional \| wrong rule: The body of a for statement executes at most once. \| right rule: The body of a for statement runs once for every pass on which the condition is true, which can be many times. |
Model's reply:
```
err:for_loop->WrongIterationCount | correct | clauses: 1, 2, 3, 4 | confidence: 0.85
mis:for_loop->IdiomOverridesCode | not applied | clauses: none | confidence: 0.75
mis:for_loop->ForIsConditional | correct | clauses: 1, 2, 4 | confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| err:for_loop->WrongIterationCount | correct | 0.45 | 0.85 | 0.38 | c1, c2, c3, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| mis:for_loop->IdiomOverridesCode | not applied |  |  | 0.0 |  |  |
| mis:for_loop->ForIsConditional | correct | 0.25 | 0.85 | 0.21 | c1, c2, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |

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
{lvl:for_loop@L3#2 (Score: 0.4)}
{lvl:for_loop@L4#0 (Score: 0.35)}
{lvl:for_loop@L2#1 (Score: 0.25)}
```
Kept by pruning: lvl:for_loop@L3#2 (0.40), lvl:for_loop@L4#0 (0.35), lvl:for_loop@L2#1 (0.25)

Label prompt for level way lvl:for_loop@L3#2 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> for (int i = 0; i < N; i++) gives i each valid index 0..N-1 exactly once in increasing order, the standard way to process every array element.

Model's reply:
```
Label: shown
Clauses: 1, 3, 4
Confidence: 0.9
```

Label prompt for level way lvl:for_loop@L4#0 (the model saw only the concept, the way's name 'predict a change' and its text; no level):
> Rewriting a for as the equivalent while (init before, update at the end of the body) keeps behaviour, except that continue then skips the update and the loop variable stays in scope after the loop. Changing the bound or the step changes the pass count predictably (< to <= adds one pass).

Model's reply:
```
Label: shown
Clauses: 3, 4
Confidence: 0.75
```

Label prompt for level way lvl:for_loop@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> A for statement has no value; the passes it makes are fixed by its header: for (int i = 1; i <= N; i++) sum += i; leaves sum = N(N+1)/2, and for (int i = 2; i <= 8; i += 2) prints 2, 4, 6, 8,.

Model's reply:
```
Label: shown
Clauses: 1, 2, 3, 4
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:for_loop@L3#2 | shown | 0.4 | 0.9 | 0.36 | c1, c3, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| lvl:for_loop@L4#0 | shown | 0.35 | 0.75 | 0.26 | c3, c4 | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| lvl:for_loop@L2#1 | shown | 0.25 | 0.9 | 0.23 | c1, c2, c3, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |

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
mis:loop_control->OffByOneBound (0.45), err:loop_control->WrongIterationCount (0.35), mis:loop_control->IdiomOverridesCode (0.20)
```
Kept by pruning: mis:loop_control->OffByOneBound (0.45), err:loop_control->WrongIterationCount (0.35), mis:loop_control->IdiomOverridesCode (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:loop_control->OffByOneBound \| wrong rule: i < n and i <= n mean the same, so the loop runs until i equals n and the last pass can use a[n]. \| right rule: for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n. |
| err:loop_control->WrongIterationCount \| wrong rule: Updates the loop counter so that the loop runs the wrong number of times. \| right rule: The init, test and update together decide the number of passes; trace them to check the count. |
| mis:loop_control->IdiomOverridesCode \| wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. |
Model's reply:
```
mis:loop_control->OffByOneBound | correct | clauses: 1, 2, 4 | confidence: 0.85
err:loop_control->WrongIterationCount | correct | clauses: 3, 4 | confidence: 0.8
mis:loop_control->IdiomOverridesCode | not applied | clauses: none | confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:loop_control->OffByOneBound | correct | 0.45 | 0.85 | 0.38 | c1, c2, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |
| err:loop_control->WrongIterationCount | correct | 0.35 | 0.8 | 0.28 | c3, c4 | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
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
{lvl:loop_control@L2#1 (Score: 0.4)}
{lvl:loop_control@L3#5 (Score: 0.35)}
{lvl:loop_control@L4#0 (Score: 0.25)}
```
Kept by pruning: lvl:loop_control@L2#1 (0.40), lvl:loop_control@L3#5 (0.35), lvl:loop_control@L4#0 (0.25)

Label prompt for level way lvl:loop_control@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> The number of passes and the values seen follow from the three parts: for (int i = 0; i <= N; i++) makes N+1 passes with i = 0..N; with i < N it makes N passes; i += 2 visits every second value.

Model's reply:
```
Label: shown
Clauses: 1, 2, 4
Confidence: 0.9
```

Label prompt for level way lvl:loop_control@L3#5 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> The initialization and the condition of a loop fix how many times it runs; one wrong bound makes it run once too many or too few.

Model's reply:
```
Label: shown
Clauses: 1, 3, 4
Confidence: 0.8
```

Label prompt for level way lvl:loop_control@L4#0 (the model saw only the concept, the way's name 'predict a change' and its text; no level):
> Changing < to <= adds one pass; starting at 1 instead of 0 removes one; doubling the step halves the passes; reversing init and bound with i-- visits the same values in reverse order (and still processes the same set only if both ends are adjusted).

Model's reply:
```
Label: shown
Clauses: 3, 4
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:loop_control@L2#1 | shown | 0.4 | 0.9 | 0.36 | c1, c2, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |
| lvl:loop_control@L3#5 | shown | 0.35 | 0.8 | 0.28 | c1, c3, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| lvl:loop_control@L4#0 | shown | 0.25 | 0.7 | 0.17 | c3, c4 | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

lvl:array_traversal@L2#1 [shown, tier 2, 0.41], mis:array_traversal->OffByOneBound [correct, tier 2, 0.38], err:for_loop->WrongIterationCount [correct, tier 2, 0.38]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | The loop visits each index from 0 to a.length - 1 and adds that element to sum | mis:array_traversal->OffByOneBound |
| c2 | so it prints Total: 12 | mis:array_traversal->ElementBoundToOldIndex |
| c3 | With 8 added, a.length becomes 4 | mis:array_traversal->OffByOneBound |
| c4 | so the loop runs once more and prints Total: 20, with no other change to the code | mis:array_traversal->OffByOneBound |

**Graph check, not yet read (the walk may not stop while these remain):** pre:for_loop->array_traversal, pre:for_loop->loop_body, pre:for_loop->loop_scope, pre:indexing->array_traversal, pre:length_field->array_traversal, pre:loop_control->for_loop, pre:loop_control->increment_operators, pre:loop_variable->loop_control

Figure 4 (the graph after depth 1): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY17_figure04.png

### Depth 2: current concepts 'array_traversal', 'for_loop', 'loop_control'

#### array_traversal, concept edges: 3 edges offered
Edges offered:
| edge |
|---|
| pre:for_loop->array_traversal \| rule: for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order. |
| pre:indexing->array_traversal \| rule: A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass. |
| pre:length_field->array_traversal \| rule: A traversal loop runs its index from 0 while it is below a.length, so it visits every element once. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:length_field->array_traversal (Score: 0.45)}
{pre:for_loop->array_traversal (Score: 0.3)}
{pre:indexing->array_traversal (Score: 0.25)}
```
Kept by pruning: pre:length_field->array_traversal (0.45), pre:for_loop->array_traversal (0.30), pre:indexing->array_traversal (0.25)

Label prompt for concept edge pre:length_field->array_traversal (length_field -> array_traversal, prerequisite):
> A traversal loop runs its index from 0 while it is below a.length, so it visits every element once.

Model's reply:
```
Label: confirmed
Clauses: 1, 3, 4
Confidence: 0.95
```

Label prompt for concept edge pre:for_loop->array_traversal (for_loop -> array_traversal, prerequisite):
> for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order.

Model's reply:
```
Label: confirmed
Clauses: 1, 3, 4
Confidence: 0.93
```

Label prompt for concept edge pre:indexing->array_traversal (indexing -> array_traversal, prerequisite):
> A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass.

Model's reply:
```
Label: confirmed
Clauses: 1, 4
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:length_field->array_traversal | confirmed | 0.45 | 0.95 | 0.43 | c1, c3, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| pre:for_loop->array_traversal | confirmed | 0.3 | 0.93 | 0.28 | c1, c3, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| pre:indexing->array_traversal | confirmed | 0.25 | 0.9 | 0.23 | c1, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |

#### for_loop, concept edges: 3 edges offered
Edges offered:
| edge |
|---|
| pre:for_loop->array_traversal \| rule: for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order. |
| pre:for_loop->loop_body \| rule: The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop. |
| pre:for_loop->loop_scope \| rule: A variable declared in the for header exists only from its declaration to the end of the for statement's block. |
| pre:loop_control->for_loop \| rule: The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
pre:loop_control->for_loop (0.50), pre:for_loop->loop_body (0.40), pre:for_loop->loop_scope (0.10)
```
Kept by pruning: pre:loop_control->for_loop (0.50), pre:for_loop->loop_body (0.40), pre:for_loop->loop_scope (0.10)

Label prompt for concept edge pre:loop_control->for_loop (loop_control -> for_loop, prerequisite):
> The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.

Model's reply:
```
Label: confirmed
Clauses: 1, 4
Confidence: 0.6
```

Label prompt for concept edge pre:for_loop->loop_body (for_loop -> loop_body, prerequisite):
> The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop.

Model's reply:
```
Label: confirmed
Clauses: 1, 4
Confidence: 0.85
```

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
| pre:loop_control->for_loop | confirmed | 0.5 | 0.6 | 0.3 | c1, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| pre:for_loop->loop_body | confirmed | 0.4 | 0.85 | 0.34 | c1, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| pre:for_loop->loop_scope | not applied |  |  | 0.0 |  |  |

#### loop_control, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| pre:loop_control->for_loop \| rule: The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |
| pre:loop_control->increment_operators \| rule: The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update. |
| pre:loop_variable->loop_control \| rule: The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:loop_control->for_loop (Score: 0.75)}
{pre:loop_control->increment_operators (Score: 0.25)}
```
Kept by pruning: pre:loop_variable->loop_control (0.80), pre:loop_control->increment_operators (0.20)

Label prompt for concept edge pre:loop_variable->loop_control (loop_variable -> loop_control, prerequisite):
> The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.

Model's reply:
```
Label: confirmed
Clauses: 1, 4
Confidence: 0.75
```

Label prompt for concept edge pre:loop_control->increment_operators (loop_control -> increment_operators, prerequisite):
> The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:loop_variable->loop_control | confirmed | 0.8 | 0.75 | 0.6 | c1, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| pre:loop_control->increment_operators | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:loop_variable->loop_control [confirmed, tier 2, 0.60], pre:length_field->array_traversal [confirmed, tier 2, 0.43], pre:for_loop->loop_body [confirmed, tier 2, 0.34]

reached across pre:loop_variable->loop_control, entered next: loop_variable

reached across pre:length_field->array_traversal, entered next: length_field

reached across pre:for_loop->loop_body, entered next: loop_body

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | The loop visits each index from 0 to a.length - 1 and adds that element to sum | mis:array_traversal->OffByOneBound |
| c2 | so it prints Total: 12 | mis:array_traversal->ElementBoundToOldIndex |
| c3 | With 8 added, a.length becomes 4 | mis:array_traversal->OffByOneBound |
| c4 | so the loop runs once more and prints Total: 20, with no other change to the code | mis:array_traversal->OffByOneBound |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of length_field, own edges of loop_body, own edges of loop_variable

Figure 5 (the graph after depth 2): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY17_figure05.png

### Depth 3: current concepts 'loop_variable', 'loop_control', 'length_field', 'array_traversal', 'loop_body', 'for_loop'

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
mis:loop_variable->LoopOutputSameEachPass (0.50), mis:loop_variable->LoopVariableLimitsValues (0.25), mis:loop_variable->LoopVariableLifetimeScope (0.25)
```
Kept by pruning: mis:loop_variable->LoopOutputSameEachPass (0.50), mis:loop_variable->LoopVariableLimitsValues (0.25), mis:loop_variable->LoopVariableLifetimeScope (0.25)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:loop_variable->LoopOutputSameEachPass \| wrong rule: A loop prints the same thing on every pass; the changing loop variable does not affect what the body does. \| right rule: The body uses the current value of the loop variable, so its output can differ on each pass. |
| mis:loop_variable->LoopVariableLimitsValues \| wrong rule: The range of the loop variable limits the values that can be read or printed inside the loop. \| right rule: The loop variable only counts passes; other values read or printed in the body are not bounded by it. |
| mis:loop_variable->LoopVariableLifetimeScope \| wrong rule: The for variable i is a new variable on every pass rather than one variable changed by the update. \| right rule: The for variable i is created once by the init, and the update changes that same variable on every pass. |
Model's reply:
```
mis:loop_variable->LoopOutputSameEachPass | correct | clauses: 1, 2 | confidence: 0.85
mis:loop_variable->LoopVariableLimitsValues | correct | clauses: 2, 4 | confidence: 0.6
mis:loop_variable->LoopVariableLifetimeScope | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:loop_variable->LoopOutputSameEachPass | correct | 0.5 | 0.85 | 0.42 | c1, c2 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12 |
| mis:loop_variable->LoopVariableLimitsValues | correct | 0.25 | 0.6 | 0.15 | c2, c4 | so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |
| mis:loop_variable->LoopVariableLifetimeScope | not applied |  |  | 0.0 |  |  |

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
{lvl:loop_variable@L3#2 (Score: 0.3)}
{lvl:loop_variable@L4#0 (Score: 0.3)}
```
Kept by pruning: lvl:loop_variable@L2#1 (0.40), lvl:loop_variable@L3#2 (0.30), lvl:loop_variable@L4#0 (0.30)

Label prompt for level way lvl:loop_variable@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> Across passes the loop variable takes a predictable sequence of values, e.g. 4, 5, ..., 10 in TenHellos, and after a while loop it holds the first value that failed the test (11).

Model's reply:
```
Label: shown
Clauses: 1, 4
Confidence: 0.7
```

Label prompt for level way lvl:loop_variable@L3#2 (the model saw only the concept, the way's name 'purpose of the whole' and its text; no level):
> Role: stepper - a variable stepping through a systematic, predictable succession of values; it counts passes and often serves as an index.

Model's reply:
```
Label: shown
Clauses: 1, 4
Confidence: 0.85
```

Label prompt for level way lvl:loop_variable@L4#0 (the model saw only the concept, the way's name 'predict a change' and its text; no level):
> Shifting the start and the bound by the same amount keeps the number of passes but changes the values the body sees; assigning to the loop variable inside the body changes the pass count.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.75
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:loop_variable@L2#1 | shown | 0.4 | 0.7 | 0.28 | c1, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| lvl:loop_variable@L3#2 | shown | 0.3 | 0.85 | 0.26 | c1, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| lvl:loop_variable@L4#0 | not applied |  |  | 0.0 |  |  |

#### loop_control, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| pre:loop_control->for_loop \| rule: The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |
| pre:loop_control->increment_operators \| rule: The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update. |
| pre:loop_variable->loop_control \| rule: The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:loop_control->for_loop (Score: 0.75)}
{pre:loop_control->increment_operators (Score: 0.25)}
```
Kept by pruning: pre:loop_control->for_loop (0.75), pre:loop_control->increment_operators (0.25)

Label prompt for concept edge pre:loop_control->for_loop (loop_control -> for_loop, prerequisite):
> The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.

Model's reply:
```
Label: confirmed
Clauses: 1, 4
Confidence: 0.6
```

Label prompt for concept edge pre:loop_control->increment_operators (loop_control -> increment_operators, prerequisite):
> The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:loop_control->for_loop | confirmed | 0.75 | 0.6 | 0.45 | c1, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| pre:loop_control->increment_operators | not applied |  |  | 0.0 |  |  |

#### length_field, misconceptions: 2 edges offered
Edges offered:
| edge |
|---|
| mis:length_field->ArrayHasLengthMethod \| wrong rule: The size of an array is found by calling a.length(). \| right rule: An array's size is the field a.length, written without parentheses. |
| mis:length_field->ArrayLengthCannotBeZero \| wrong rule: An array cannot have length 0. \| right rule: new int[0] is a legal array of length 0. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:length_field->ArrayHasLengthMethod (Score: 0.9)}
{mis:length_field->ArrayLengthCannotBeZero (Score: 0.1)}
```
Kept by pruning: mis:length_field->ArrayHasLengthMethod (0.90), mis:length_field->ArrayLengthCannotBeZero (0.10)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:length_field->ArrayHasLengthMethod \| wrong rule: The size of an array is found by calling a.length(). \| right rule: An array's size is the field a.length, written without parentheses. |
| mis:length_field->ArrayLengthCannotBeZero \| wrong rule: An array cannot have length 0. \| right rule: new int[0] is a legal array of length 0. |
Model's reply:
```
mis:length_field->ArrayHasLengthMethod | correct | clauses: 1, 3 | confidence: 0.8
mis:length_field->ArrayLengthCannotBeZero | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:length_field->ArrayHasLengthMethod | correct | 0.9 | 0.8 | 0.72 | c1, c3 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4 |
| mis:length_field->ArrayLengthCannotBeZero | not applied |  |  | 0.0 |  |  |

#### length_field, level ways: 15 edges offered
Edges offered:
| edge |
|---|
| lvl:length_field@L0#0 \| level L0 way everyday_reading: Folk meaning: 'length' is something you ask for, like s.length() for a String, and in everyday counting 'length 10' suggests the last item is number 10. Java rule: a.length is a final field written without parentheses, equal to the number of elements, so the last index is a.length-1. |
| lvl:length_field@L0#2 \| level L0 way inconsistent_trace: Points to LT: a.length is read every time the loop test i < a.length runs. Inconsistent application: the trace uses a.length as the last valid index on some passes (as if the test were <=). (here mixing in: "you call length() instead of using the length field") |
| lvl:length_field@L1#0 \| level L1 way names_the_element: Identity: a.length is the public final instance field that every array has, holding its number of elements. |
| lvl:length_field@L1#1 \| level L1 way states_the_rule: Declarative: the length of array a is written a.length (no parentheses); it equals the size given at creation, may be zero, cannot be assigned, and the last element is a[a.length-1]. |
| lvl:length_field@L2#0 \| level L2 way line_by_line_trace: Sequencing: a is evaluated first (a null a throws NullPointerException), then the length field of the array a refers to now is read. In 'for (int i = 0; i < a.length; i++)' it is re-read at each test. |
| lvl:length_field@L2#1 \| level L2 way output_prediction: Result: an int >= 0 equal to the number of elements: new double[8].length is 8, {1, 2, 3}.length is 3, and the last element is a[a.length-1]. |
| lvl:length_field@L2#2 \| level L2 way one_step_execution: State transition: reading a.length changes nothing. Assigning 'a.length = 5' is impossible (a final field), so only making a refer to a different array changes the value later read as a.length. |
| lvl:length_field@L3#0 \| level L3 way relation_to_neighbour: The n given to new becomes a.length and stays fixed for that array object. |
| lvl:length_field@L3#1 \| level L3 way relation_to_neighbour: args is an ordinary String[], so args.length is its length field and counts the command-line arguments (0 when none are typed). |
| lvl:length_field@L3#2 \| level L3 way purpose_of_the_whole: Plan/role: a fixed value (Sajaniemi) that lets code adapt to any array size instead of a hard-coded magic number, e.g. loop bounds and the last element. |
| lvl:length_field@L4#0 \| level L4 way predict_a_change: Conservation: for a given array object a.length never changes, so loops bounded by a.length stay correct when the array is created with a different size. Reassigning a to another array changes a.length. |
| lvl:length_field@L4#1 \| level L4 way transfer_to_a_new_program: Applicability: use a.length wherever code must follow the array's real size (loop bounds, last element, copying); use a[i].length for each row of a possibly ragged 2-D array; use s.length() for Strings. |
| lvl:length_field@L4#2 \| level L4 way diagnose_an_error: rule broken: length is a field, not a method. Kind: compile-time. Trigger class: a.length() is written for an array (cannot find symbol: method length()) |
| lvl:length_field@L4#3 \| level L4 way diagnose_an_error: rule broken: length is final and cannot be assigned. Kind: compile-time. Trigger class: 'a.length = n;' (cannot assign a value to final variable length) |
| lvl:length_field@L4#4 \| level L4 way diagnose_an_error: rule broken: The last valid index is a.length-1. Kind: run-time exception. Trigger class: a[a.length] or a loop with i <= a.length (ArrayIndexOutOfBoundsException) |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:length_field@L4#0 (Score: 0.5)}
{lvl:length_field@L3#2 (Score: 0.3)}
{lvl:length_field@L1#1 (Score: 0.2)}
```
Kept by pruning: lvl:length_field@L4#0 (0.50), lvl:length_field@L3#2 (0.30), lvl:length_field@L1#1 (0.20)

Label prompt for level way lvl:length_field@L4#0 (the model saw only the concept, the way's name 'predict a change' and its text; no level):
> Conservation: for a given array object a.length never changes, so loops bounded by a.length stay correct when the array is created with a different size. Reassigning a to another array changes a.length.

Model's reply:
```
Label: shown
Clauses: 3, 4
Confidence: 0.88
```

Label prompt for level way lvl:length_field@L3#2 (the model saw only the concept, the way's name 'purpose of the whole' and its text; no level):
> Plan/role: a fixed value (Sajaniemi) that lets code adapt to any array size instead of a hard-coded magic number, e.g. loop bounds and the last element.

Model's reply:
```
Label: shown
Clauses: 3, 4
Confidence: 0.85
```

Label prompt for level way lvl:length_field@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> Declarative: the length of array a is written a.length (no parentheses); it equals the size given at creation, may be zero, cannot be assigned, and the last element is a[a.length-1].

Model's reply:
```
Label: shown
Clauses: 1, 3
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:length_field@L4#0 | shown | 0.5 | 0.88 | 0.44 | c3, c4 | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| lvl:length_field@L3#2 | shown | 0.3 | 0.85 | 0.26 | c3, c4 | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| lvl:length_field@L1#1 | shown | 0.2 | 0.8 | 0.16 | c1, c3 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4 |

#### array_traversal, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| pre:for_loop->array_traversal \| rule: for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order. |
| pre:indexing->array_traversal \| rule: A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass. |
| pre:length_field->array_traversal \| rule: A traversal loop runs its index from 0 while it is below a.length, so it visits every element once. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:for_loop->array_traversal (Score: 0.6)}
{pre:indexing->array_traversal (Score: 0.4)}
```
Kept by pruning: pre:for_loop->array_traversal (0.60), pre:indexing->array_traversal (0.40)

Label prompt for concept edge pre:for_loop->array_traversal (for_loop -> array_traversal, prerequisite):
> for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order.

Model's reply:
```
Label: confirmed
Clauses: 1, 3, 4
Confidence: 0.93
```

Label prompt for concept edge pre:indexing->array_traversal (indexing -> array_traversal, prerequisite):
> A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass.

Model's reply:
```
Label: confirmed
Clauses: 1, 4
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:for_loop->array_traversal | confirmed | 0.6 | 0.93 | 0.56 | c1, c3, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| pre:indexing->array_traversal | confirmed | 0.4 | 0.9 | 0.36 | c1, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |

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
mis:loop_body->StateChangeIgnoredAcrossPasses (0.45), mis:loop_body->LoopOutputSameEachPass (0.30), mis:loop_body->StatementAfterLoopInBody (0.25)
```
Kept by pruning: mis:loop_body->StateChangeIgnoredAcrossPasses (0.45), mis:loop_body->LoopOutputSameEachPass (0.30), mis:loop_body->StatementAfterLoopInBody (0.25)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:loop_body->StateChangeIgnoredAcrossPasses \| wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. \| right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones. |
| mis:loop_body->LoopOutputSameEachPass \| wrong rule: A loop prints the same thing on every pass; the changing loop variable does not affect what the body does. \| right rule: The body uses the current value of the loop variable, so its output can differ on each pass. |
| mis:loop_body->StatementAfterLoopInBody \| wrong rule: A statement written after the loop is repeated with the loop body. \| right rule: The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends. |
Model's reply:
```
mis:loop_body->StateChangeIgnoredAcrossPasses | correct | clauses: 1, 2, 4 | confidence: 0.9
mis:loop_body->LoopOutputSameEachPass | correct | clauses: 1 | confidence: 0.6
mis:loop_body->StatementAfterLoopInBody | correct | clauses: 2, 4 | confidence: 0.75
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:loop_body->StateChangeIgnoredAcrossPasses | correct | 0.45 | 0.9 | 0.41 | c1, c2, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |
| mis:loop_body->LoopOutputSameEachPass | correct | 0.3 | 0.6 | 0.18 | c1 | The loop visits each index from 0 to a.length - 1 and adds that element to sum |
| mis:loop_body->StatementAfterLoopInBody | correct | 0.25 | 0.75 | 0.19 | c2, c4 | so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |

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
{lvl:loop_body@L3#0 (Score: 0.4)}
{lvl:loop_body@L4#0 (Score: 0.25)}
{lvl:loop_body@L2#1 (Score: 0.35)}
```
Kept by pruning: lvl:loop_body@L3#0 (0.40), lvl:loop_body@L2#1 (0.35), lvl:loop_body@L4#0 (0.25)

Label prompt for level way lvl:loop_body@L3#0 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> The accumulator update (sum += x) is placed inside the body so it runs once per pass, while the accumulator is declared and initialized before the loop.

Model's reply:
```
Label: shown
Clauses: 1, 4
Confidence: 0.6
```

Label prompt for level way lvl:loop_body@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> The body's output on each pass depends on the current values, so successive passes can print different lines: TenHellos prints '4th Hello', '5th Hello', ...; the number of executions of each body statement equals the number of passes.

Model's reply:
```
Label: shown
Clauses: 1, 4
Confidence: 0.7
```

Label prompt for level way lvl:loop_body@L4#0 (the model saw only the concept, the way's name 'predict a change' and its text; no level):
> Moving a statement from inside the body to after the loop changes it from running once per pass to once in total (and vice versa); reordering two body statements that share a variable changes the results (e.g. increment before vs after use).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:loop_body@L3#0 | shown | 0.4 | 0.6 | 0.24 | c1, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| lvl:loop_body@L2#1 | shown | 0.35 | 0.7 | 0.24 | c1, c4 | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| lvl:loop_body@L4#0 | not applied |  |  | 0.0 |  |  |

#### for_loop, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:for_loop->array_traversal \| rule: for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order. |
| pre:for_loop->loop_body \| rule: The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop. |
| pre:for_loop->loop_scope \| rule: A variable declared in the for header exists only from its declaration to the end of the for statement's block. |
| pre:loop_control->for_loop \| rule: The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
pre:for_loop->loop_scope (1.00)
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

mis:length_field->ArrayHasLengthMethod [correct, tier 2, 0.72], pre:for_loop->array_traversal [confirmed, tier 2, 0.56], pre:loop_control->for_loop [confirmed, tier 2, 0.45]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | The loop visits each index from 0 to a.length - 1 and adds that element to sum | mis:array_traversal->OffByOneBound |
| c2 | so it prints Total: 12 | mis:array_traversal->ElementBoundToOldIndex |
| c3 | With 8 added, a.length becomes 4 | mis:array_traversal->OffByOneBound |
| c4 | so the loop runs once more and prints Total: 20, with no other change to the code | mis:array_traversal->OffByOneBound |

**Graph check, not yet read (the walk may not stop while these remain):** pre:array_initializer->length_field, pre:loop_body->accumulator_pattern

Figure 6 (the graph after depth 3): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY17_figure06.png

## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on [], broken at [], prerequisites {'array_initializer': ['array_declaration'], 'indexing': ['array_initializer'], 'length_field': ['array_initializer'], 'compound_assignment': ['assignment'], 'increment_operators': ['assignment', 'loop_control'], 'boolean_expression': ['comparison_operators'], 'accumulator_pattern': ['compound_assignment', 'loop_body'], 'array_declaration': ['data_structure'], 'data_structure': ['data_type'], 'comparison_operators': ['expression'], 'array_traversal': ['for_loop', 'indexing', 'length_field'], 'loop_body': ['for_loop'], 'loop_scope': ['for_loop'], 'array_bounds': ['indexing'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable'], 'control_flow': ['statement'], 'println': ['statement', 'string_literal'], 'string_conversion': ['string_concatenation']}
- array_traversal: L4 via predict_a_change "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
- for_loop: L4 via predict_a_change "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
- length_field: L4 via predict_a_change "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
- loop_body: L3 via relation_to_neighbour "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code"
- loop_control: L4 via predict_a_change "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
- loop_variable: L3 via purpose_of_the_whole "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code"

**Stop:** max depth at depth 3; prompts {'prune': 18, 'label': 37}, fresh model calls 21, cache hits 34

### Held misconceptions
(none)

### Broken concept edges
(none)

### Root cause: none

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| array_traversal | L4 | predict_a_change |  | level_way | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |  | L3 relation_to_neighbour, L2 output_prediction |  |
| for_loop | L4 | predict_a_change |  | level_way | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |  | L3 relation_to_neighbour, L2 output_prediction |  |
| length_field | L4 | predict_a_change |  | level_way | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |  | L3 purpose_of_the_whole, L1 states_the_rule |  |
| loop_body | L3 | relation_to_neighbour |  | level_way | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |  | L2 output_prediction |  |
| loop_control | L4 | predict_a_change |  | level_way | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |  | L3 relation_to_neighbour, L2 output_prediction |  |
| loop_variable | L3 | purpose_of_the_whole |  | level_way | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |  | L2 output_prediction |  |

### Overall level: L4

Clause coverage (final):
| clause | covered by |
|---|---|
| The loop visits each index from 0 to a.length - 1 and adds that element to sum | mis:array_traversal->OffByOneBound |
| so it prints Total: 12 | mis:array_traversal->ElementBoundToOldIndex |
| With 8 added, a.length becomes 4 | mis:array_traversal->OffByOneBound |
| so the loop runs once more and prints Total: 20, with no other change to the code | mis:array_traversal->OffByOneBound |

Figure 7 (final picture): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY17_figure07.png

## 5. Every labelled edge (the evidence list, kept or not)
| depth | source | edge | kind | label | prune_score | confidence | score | clauses | quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | array_traversal | mis:array_traversal->OffByOneBound | misconception | correct | 0.45 | 0.85 | 0.3825 | [1, 3, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| 1 | array_traversal | mis:array_traversal->ElementBoundToOldIndex | misconception | correct | 0.25 | 0.75 | 0.1875 | [1, 2, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |
| 1 | array_traversal | lvl:array_traversal@L2#1 | level | shown | 0.45 | 0.9 | 0.405 | [2, 4] | so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |
| 1 | array_traversal | lvl:array_traversal@L4#0 | level | shown | 0.3 | 0.8 | 0.24 | [3, 4] | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| 1 | array_traversal | lvl:array_traversal@L3#2 | level | shown | 0.25 | 0.8 | 0.2 | [1, 3, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| 1 | for_loop | err:for_loop->WrongIterationCount | error | correct | 0.45 | 0.85 | 0.3825 | [1, 2, 3, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| 1 | for_loop | mis:for_loop->ForIsConditional | misconception | correct | 0.25 | 0.85 | 0.2125 | [1, 2, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |
| 1 | for_loop | lvl:for_loop@L3#2 | level | shown | 0.4 | 0.9 | 0.36 | [1, 3, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| 1 | for_loop | lvl:for_loop@L4#0 | level | shown | 0.35 | 0.75 | 0.2625 | [3, 4] | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| 1 | for_loop | lvl:for_loop@L2#1 | level | shown | 0.25 | 0.9 | 0.225 | [1, 2, 3, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| 1 | loop_control | mis:loop_control->OffByOneBound | misconception | correct | 0.45 | 0.85 | 0.3825 | [1, 2, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |
| 1 | loop_control | err:loop_control->WrongIterationCount | error | correct | 0.35 | 0.8 | 0.28 | [3, 4] | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| 1 | loop_control | lvl:loop_control@L2#1 | level | shown | 0.4 | 0.9 | 0.36 | [1, 2, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |
| 1 | loop_control | lvl:loop_control@L3#5 | level | shown | 0.35 | 0.8 | 0.28 | [1, 3, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| 1 | loop_control | lvl:loop_control@L4#0 | level | shown | 0.25 | 0.7 | 0.175 | [3, 4] | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| 2 | array_traversal | pre:length_field->array_traversal | prerequisite | confirmed | 0.45 | 0.95 | 0.4275 | [1, 3, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| 2 | array_traversal | pre:for_loop->array_traversal | prerequisite | confirmed | 0.3 | 0.93 | 0.279 | [1, 3, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| 2 | array_traversal | pre:indexing->array_traversal | prerequisite | confirmed | 0.25 | 0.9 | 0.225 | [1, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| 2 | for_loop | pre:loop_control->for_loop | prerequisite | confirmed | 0.5 | 0.6 | 0.3 | [1, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| 2 | for_loop | pre:for_loop->loop_body | prerequisite | confirmed | 0.4 | 0.85 | 0.34 | [1, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| 2 | loop_control | pre:loop_variable->loop_control | prerequisite | confirmed | 0.8 | 0.75 | 0.6 | [1, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| 3 | loop_variable | mis:loop_variable->LoopOutputSameEachPass | misconception | correct | 0.5 | 0.85 | 0.425 | [1, 2] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12 |
| 3 | loop_variable | mis:loop_variable->LoopVariableLimitsValues | misconception | correct | 0.25 | 0.6 | 0.15 | [2, 4] | so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |
| 3 | loop_variable | lvl:loop_variable@L2#1 | level | shown | 0.4 | 0.7 | 0.28 | [1, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| 3 | loop_variable | lvl:loop_variable@L3#2 | level | shown | 0.3 | 0.85 | 0.255 | [1, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| 3 | loop_control | pre:loop_control->for_loop | prerequisite | confirmed | 0.75 | 0.6 | 0.45 | [1, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| 3 | length_field | mis:length_field->ArrayHasLengthMethod | misconception | correct | 0.9 | 0.8 | 0.72 | [1, 3] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4 |
| 3 | length_field | lvl:length_field@L4#0 | level | shown | 0.5 | 0.88 | 0.44 | [3, 4] | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| 3 | length_field | lvl:length_field@L3#2 | level | shown | 0.3 | 0.85 | 0.255 | [3, 4] | With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| 3 | length_field | lvl:length_field@L1#1 | level | shown | 0.2 | 0.8 | 0.16 | [1, 3] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4 |
| 3 | array_traversal | pre:for_loop->array_traversal | prerequisite | confirmed | 0.6 | 0.93 | 0.558 | [1, 3, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code |
| 3 | array_traversal | pre:indexing->array_traversal | prerequisite | confirmed | 0.4 | 0.9 | 0.36 | [1, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| 3 | loop_body | mis:loop_body->StateChangeIgnoredAcrossPasses | misconception | correct | 0.45 | 0.9 | 0.405 | [1, 2, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |
| 3 | loop_body | mis:loop_body->LoopOutputSameEachPass | misconception | correct | 0.3 | 0.6 | 0.18 | [1] | The loop visits each index from 0 to a.length - 1 and adds that element to sum |
| 3 | loop_body | mis:loop_body->StatementAfterLoopInBody | misconception | correct | 0.25 | 0.75 | 0.1875 | [2, 4] | so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code |
| 3 | loop_body | lvl:loop_body@L3#0 | level | shown | 0.4 | 0.6 | 0.24 | [1, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |
| 3 | loop_body | lvl:loop_body@L2#1 | level | shown | 0.35 | 0.7 | 0.245 | [1, 4] | The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | array_traversal | lvl:array_traversal@L2#1 | level | shown | 0.405 | [2, 4] |
| 1 | array_traversal | mis:array_traversal->OffByOneBound | misconception | correct | 0.3825 | [1, 3, 4] |
| 1 | for_loop | err:for_loop->WrongIterationCount | error | correct | 0.3825 | [1, 2, 3, 4] |
| 2 | loop_control | pre:loop_variable->loop_control | prerequisite | confirmed | 0.6 | [1, 4] |
| 2 | array_traversal | pre:length_field->array_traversal | prerequisite | confirmed | 0.4275 | [1, 3, 4] |
| 2 | for_loop | pre:for_loop->loop_body | prerequisite | confirmed | 0.34 | [1, 4] |
| 3 | length_field | mis:length_field->ArrayHasLengthMethod | misconception | correct | 0.72 | [1, 3] |
| 3 | array_traversal | pre:for_loop->array_traversal | prerequisite | confirmed | 0.558 | [1, 3, 4] |
| 3 | loop_control | pre:loop_control->for_loop | prerequisite | confirmed | 0.45 | [1, 4] |

## 7. Raw traversal log
```
clauses: The loop visits each index from 0 to a.length - 1 and adds that element to sum | so it prints Total: 12 | With 8 added, a.length becomes 4 | so the loop runs once more and prints Total: 20, with no other change to the code
start: BM25 of the answer against each tagged concept: array_traversal 29.50 (hits 2), for_loop 24.84 (hits 1), loop_control 23.43 (hits 1), accumulator_pattern 22.02 (hits 1), loop_body 21.17 (hits 1), indexing 20.63 (hits 1), loop_variable 20.13 (hits 1), control_flow 19.64 (hits 1), compound_assignment 19.24 (hits 1), increment_operators 18.75 (hits 1), length_field 18.23 (hits 1), array_bounds 15.35 (hits 1), loop_scope 14.90 (hits 1), println 13.88 (hits 1), boolean_expression 13.74 (hits 1), string_concatenation 11.41 (hits 1), array_declaration 10.22 (hits 1), array_initializer 8.87 (hits 1), comparison_operators 6.81 (hits 1), string_conversion 4.35 (hits 1), data_structure 2.30 (hits 1)
start: chosen array_traversal, for_loop, loop_control
start concepts (3): array_traversal, for_loop, loop_control
--- depth 1: current concepts ['array_traversal', 'for_loop', 'loop_control']
  array_traversal (misconceptions): 6 candidates -> kept mis:array_traversal->OffByOneBound (0.45), mis:array_traversal->IdiomOverridesCode (0.30), mis:array_traversal->ElementBoundToOldIndex (0.25)
    mis:array_traversal->OffByOneBound -> correct (0.38) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
    mis:array_traversal->IdiomOverridesCode -> not applied (0.00) ""
    mis:array_traversal->ElementBoundToOldIndex -> correct (0.19) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code"
  array_traversal (level ways): 22 candidates -> kept lvl:array_traversal@L2#1 (0.45), lvl:array_traversal@L4#0 (0.30), lvl:array_traversal@L3#2 (0.25)
    lvl:array_traversal@L2#1 -> shown (0.41) "so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code"
    lvl:array_traversal@L4#0 -> shown (0.24) "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
    lvl:array_traversal@L3#2 -> shown (0.20) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
  for_loop (misconceptions): 21 candidates -> kept err:for_loop->WrongIterationCount (0.45), mis:for_loop->IdiomOverridesCode (0.30), mis:for_loop->ForIsConditional (0.25)
    err:for_loop->WrongIterationCount -> correct (0.38) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
    mis:for_loop->IdiomOverridesCode -> not applied (0.00) ""
    mis:for_loop->ForIsConditional -> correct (0.21) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code"
  for_loop (level ways): 24 candidates -> kept lvl:for_loop@L3#2 (0.40), lvl:for_loop@L4#0 (0.35), lvl:for_loop@L2#1 (0.25)
    lvl:for_loop@L3#2 -> shown (0.36) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
    lvl:for_loop@L4#0 -> shown (0.26) "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
    lvl:for_loop@L2#1 -> shown (0.23) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
  loop_control (misconceptions): 11 candidates -> kept mis:loop_control->OffByOneBound (0.45), err:loop_control->WrongIterationCount (0.35), mis:loop_control->IdiomOverridesCode (0.20)
    mis:loop_control->OffByOneBound -> correct (0.38) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code"
    err:loop_control->WrongIterationCount -> correct (0.28) "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
    mis:loop_control->IdiomOverridesCode -> not applied (0.00) ""
  loop_control (level ways): 19 candidates -> kept lvl:loop_control@L2#1 (0.40), lvl:loop_control@L3#5 (0.35), lvl:loop_control@L4#0 (0.25)
    lvl:loop_control@L2#1 -> shown (0.36) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code"
    lvl:loop_control@L3#5 -> shown (0.28) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
    lvl:loop_control@L4#0 -> shown (0.17) "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
  kept: lvl:array_traversal@L2#1 [shown, tier 2, 0.41], mis:array_traversal->OffByOneBound [correct, tier 2, 0.38], err:for_loop->WrongIterationCount [correct, tier 2, 0.38]
  clause coverage: c1 <- mis:array_traversal->OffByOneBound; c2 <- mis:array_traversal->ElementBoundToOldIndex; c3 <- mis:array_traversal->OffByOneBound; c4 <- mis:array_traversal->OffByOneBound
  not yet read: pre:for_loop->array_traversal, pre:for_loop->loop_body, pre:for_loop->loop_scope, pre:indexing->array_traversal, pre:length_field->array_traversal, pre:loop_control->for_loop, pre:loop_control->increment_operators, pre:loop_variable->loop_control
--- depth 2: current concepts ['array_traversal', 'for_loop', 'loop_control']
  array_traversal (concept edges): 3 candidates -> kept pre:length_field->array_traversal (0.45), pre:for_loop->array_traversal (0.30), pre:indexing->array_traversal (0.25)
    pre:length_field->array_traversal -> confirmed (0.43) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
    pre:for_loop->array_traversal -> confirmed (0.28) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
    pre:indexing->array_traversal -> confirmed (0.23) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code"
  for_loop (concept edges): 3 candidates -> kept pre:loop_control->for_loop (0.50), pre:for_loop->loop_body (0.40), pre:for_loop->loop_scope (0.10)
    pre:loop_control->for_loop -> confirmed (0.30) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code"
    pre:for_loop->loop_body -> confirmed (0.34) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code"
    pre:for_loop->loop_scope -> not applied (0.00) ""
  loop_control (concept edges): 2 candidates -> kept pre:loop_variable->loop_control (0.80), pre:loop_control->increment_operators (0.20)
    pre:loop_variable->loop_control -> confirmed (0.60) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code"
    pre:loop_control->increment_operators -> not applied (0.00) ""
  kept: pre:loop_variable->loop_control [confirmed, tier 2, 0.60], pre:length_field->array_traversal [confirmed, tier 2, 0.43], pre:for_loop->loop_body [confirmed, tier 2, 0.34]
  reached across pre:loop_variable->loop_control, entered next: loop_variable
  reached across pre:length_field->array_traversal, entered next: length_field
  reached across pre:for_loop->loop_body, entered next: loop_body
  clause coverage: c1 <- mis:array_traversal->OffByOneBound; c2 <- mis:array_traversal->ElementBoundToOldIndex; c3 <- mis:array_traversal->OffByOneBound; c4 <- mis:array_traversal->OffByOneBound
  not yet read: own edges of length_field, own edges of loop_body, own edges of loop_variable
--- depth 3: current concepts ['loop_variable', 'loop_control', 'length_field', 'array_traversal', 'loop_body', 'for_loop']
  loop_variable (misconceptions): 7 candidates -> kept mis:loop_variable->LoopOutputSameEachPass (0.50), mis:loop_variable->LoopVariableLimitsValues (0.25), mis:loop_variable->LoopVariableLifetimeScope (0.25)
    mis:loop_variable->LoopOutputSameEachPass -> correct (0.42) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12"
    mis:loop_variable->LoopVariableLimitsValues -> correct (0.15) "so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code"
    mis:loop_variable->LoopVariableLifetimeScope -> not applied (0.00) ""
  loop_variable (level ways): 13 candidates -> kept lvl:loop_variable@L2#1 (0.40), lvl:loop_variable@L3#2 (0.30), lvl:loop_variable@L4#0 (0.30)
    lvl:loop_variable@L2#1 -> shown (0.28) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code"
    lvl:loop_variable@L3#2 -> shown (0.26) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code"
    lvl:loop_variable@L4#0 -> not applied (0.00) ""
  loop_control (concept edges): 2 candidates -> kept pre:loop_control->for_loop (0.75), pre:loop_control->increment_operators (0.25)
    pre:loop_control->for_loop -> confirmed (0.45) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code"
    pre:loop_control->increment_operators -> not applied (0.00) ""
  length_field (misconceptions): 2 candidates -> kept mis:length_field->ArrayHasLengthMethod (0.90), mis:length_field->ArrayLengthCannotBeZero (0.10)
    mis:length_field->ArrayHasLengthMethod -> correct (0.72) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4"
    mis:length_field->ArrayLengthCannotBeZero -> not applied (0.00) ""
  length_field (level ways): 15 candidates -> kept lvl:length_field@L4#0 (0.50), lvl:length_field@L3#2 (0.30), lvl:length_field@L1#1 (0.20)
    lvl:length_field@L4#0 -> shown (0.44) "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
    lvl:length_field@L3#2 -> shown (0.26) "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
    lvl:length_field@L1#1 -> shown (0.16) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4"
  array_traversal (concept edges): 2 candidates -> kept pre:for_loop->array_traversal (0.60), pre:indexing->array_traversal (0.40)
    pre:for_loop->array_traversal -> confirmed (0.56) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
    pre:indexing->array_traversal -> confirmed (0.36) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code"
  loop_body (misconceptions): 12 candidates -> kept mis:loop_body->StateChangeIgnoredAcrossPasses (0.45), mis:loop_body->LoopOutputSameEachPass (0.30), mis:loop_body->StatementAfterLoopInBody (0.25)
    mis:loop_body->StateChangeIgnoredAcrossPasses -> correct (0.41) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code"
    mis:loop_body->LoopOutputSameEachPass -> correct (0.18) "The loop visits each index from 0 to a.length - 1 and adds that element to sum"
    mis:loop_body->StatementAfterLoopInBody -> correct (0.19) "so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code"
  loop_body (level ways): 14 candidates -> kept lvl:loop_body@L3#0 (0.40), lvl:loop_body@L2#1 (0.35), lvl:loop_body@L4#0 (0.25)
    lvl:loop_body@L3#0 -> shown (0.24) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code"
    lvl:loop_body@L2#1 -> shown (0.24) "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code"
    lvl:loop_body@L4#0 -> not applied (0.00) ""
  for_loop (concept edges): 1 candidates -> kept pre:for_loop->loop_scope (1.00)
    pre:for_loop->loop_scope -> not applied (0.00) ""
  kept: mis:length_field->ArrayHasLengthMethod [correct, tier 2, 0.72], pre:for_loop->array_traversal [confirmed, tier 2, 0.56], pre:loop_control->for_loop [confirmed, tier 2, 0.45]
  clause coverage: c1 <- mis:array_traversal->OffByOneBound; c2 <- mis:array_traversal->ElementBoundToOldIndex; c3 <- mis:array_traversal->OffByOneBound; c4 <- mis:array_traversal->OffByOneBound
  not yet read: pre:array_initializer->length_field, pre:loop_body->accumulator_pattern
  root-cause walk: held on [], broken at [], prerequisites {'array_initializer': ['array_declaration'], 'indexing': ['array_initializer'], 'length_field': ['array_initializer'], 'compound_assignment': ['assignment'], 'increment_operators': ['assignment', 'loop_control'], 'boolean_expression': ['comparison_operators'], 'accumulator_pattern': ['compound_assignment', 'loop_body'], 'array_declaration': ['data_structure'], 'data_structure': ['data_type'], 'comparison_operators': ['expression'], 'array_traversal': ['for_loop', 'indexing', 'length_field'], 'loop_body': ['for_loop'], 'loop_scope': ['for_loop'], 'array_bounds': ['indexing'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable'], 'control_flow': ['statement'], 'println': ['statement', 'string_literal'], 'string_conversion': ['string_concatenation']}
  level array_traversal: L4 via predict_a_change "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
  level for_loop: L4 via predict_a_change "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
  level length_field: L4 via predict_a_change "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
  level loop_body: L3 via relation_to_neighbour "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code"
  level loop_control: L4 via predict_a_change "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code"
  level loop_variable: L3 via purpose_of_the_whole "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code"
```

## 8. Full diagnosis JSON
```json
{
 "scenario": "MY17",
 "settings": {
  "width": 3,
  "depth": 3,
  "prune_tools": "llm",
  "model": "claude-opus-5-5",
  "backend": "claude-cli"
 },
 "clauses": [
  "The loop visits each index from 0 to a.length - 1 and adds that element to sum",
  "so it prints Total: 12",
  "With 8 added, a.length becomes 4",
  "so the loop runs once more and prints Total: 20, with no other change to the code"
 ],
 "start_concepts": [
  "array_traversal",
  "for_loop",
  "loop_control"
 ],
 "held_misconceptions": [],
 "error_evidence": [],
 "shadowed": [],
 "broken_edges": [],
 "root_cause": null,
 "levels": {
  "array_traversal": {
   "level": "L4",
   "way": "predict_a_change",
   "quote": "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "edge": "lvl:array_traversal@L4#0",
   "source": "level_way",
   "also_shown": [
    "L3 relation_to_neighbour",
    "L2 output_prediction"
   ]
  },
  "for_loop": {
   "level": "L4",
   "way": "predict_a_change",
   "quote": "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "edge": "lvl:for_loop@L4#0",
   "source": "level_way",
   "also_shown": [
    "L3 relation_to_neighbour",
    "L2 output_prediction"
   ]
  },
  "length_field": {
   "level": "L4",
   "way": "predict_a_change",
   "quote": "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "edge": "lvl:length_field@L4#0",
   "source": "level_way",
   "also_shown": [
    "L3 purpose_of_the_whole",
    "L1 states_the_rule"
   ]
  },
  "loop_body": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code",
   "edge": "lvl:loop_body@L3#0",
   "source": "level_way",
   "also_shown": [
    "L2 output_prediction"
   ]
  },
  "loop_control": {
   "level": "L4",
   "way": "predict_a_change",
   "quote": "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "edge": "lvl:loop_control@L4#0",
   "source": "level_way",
   "also_shown": [
    "L3 relation_to_neighbour",
    "L2 output_prediction"
   ]
  },
  "loop_variable": {
   "level": "L3",
   "way": "purpose_of_the_whole",
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code",
   "edge": "lvl:loop_variable@L3#2",
   "source": "level_way",
   "also_shown": [
    "L2 output_prediction"
   ]
  }
 },
 "overall_level": "L4",
 "paths": [
  {
   "depth": 1,
   "source": "array_traversal",
   "edge": "lvl:array_traversal@L2#1",
   "target": "array_traversal@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    4
   ],
   "quote": "so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.9,
   "prune_score": 0.45,
   "score": 0.405,
   "logic": "Result: the body runs a.length times, and the result depends on the body. Squaring each element of {1, 2, 3, 4, 5} leaves {1, 4, 9, 16, 25}; summing leaves the total in the accumulator.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "array_traversal",
   "edge": "mis:array_traversal->OffByOneBound",
   "target": "OffByOneBound",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.85,
   "prune_score": 0.45,
   "score": 0.3825,
   "logic": "< vs <= and 0..n vs 0..n-1 are interchangeable",
   "twin_logic": "for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n.",
   "role": "context"
  },
  {
   "depth": 1,
   "source": "for_loop",
   "edge": "err:for_loop->WrongIterationCount",
   "target": "WrongIterationCount",
   "kind": "error",
   "label": "correct",
   "clauses": [
    1,
    2,
    3,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.85,
   "prune_score": 0.45,
   "score": 0.3825,
   "logic": "Updates the loop counter so that the loop runs the wrong number of times.",
   "twin_logic": "The init, test and update together decide the number of passes; trace them to check the count.",
   "role": "primary"
  },
  {
   "depth": 2,
   "source": "loop_control",
   "edge": "pre:loop_variable->loop_control",
   "target": "loop_variable",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.75,
   "prune_score": 0.8,
   "score": 0.6,
   "logic": "The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "array_traversal",
   "edge": "pre:length_field->array_traversal",
   "target": "length_field",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.95,
   "prune_score": 0.45,
   "score": 0.4275,
   "logic": "A traversal loop runs its index from 0 while it is below a.length, so it visits every element once.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "for_loop",
   "edge": "pre:for_loop->loop_body",
   "target": "loop_body",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.85,
   "prune_score": 0.4,
   "score": 0.34,
   "logic": "The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "length_field",
   "edge": "mis:length_field->ArrayHasLengthMethod",
   "target": "ArrayHasLengthMethod",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    3
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4",
   "confidence": 0.8,
   "prune_score": 0.9,
   "score": 0.72,
   "logic": "The size of an array is found by calling a.length().",
   "twin_logic": "An array's size is the field a.length, written without parentheses.",
   "role": "primary"
  },
  {
   "depth": 3,
   "source": "array_traversal",
   "edge": "pre:for_loop->array_traversal",
   "target": "for_loop",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.93,
   "prune_score": 0.6,
   "score": 0.558,
   "logic": "for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "loop_control",
   "edge": "pre:loop_control->for_loop",
   "target": "for_loop",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.6,
   "prune_score": 0.75,
   "score": 0.45,
   "logic": "The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.",
   "twin_logic": null
  }
 ],
 "evidence": [
  {
   "depth": 1,
   "source": "array_traversal",
   "edge": "mis:array_traversal->OffByOneBound",
   "target": "OffByOneBound",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.85,
   "prune_score": 0.45,
   "score": 0.3825,
   "logic": "< vs <= and 0..n vs 0..n-1 are interchangeable",
   "twin_logic": "for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n.",
   "role": "context"
  },
  {
   "depth": 1,
   "source": "array_traversal",
   "edge": "mis:array_traversal->ElementBoundToOldIndex",
   "target": "ElementBoundToOldIndex",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    2,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.75,
   "prune_score": 0.25,
   "score": 0.1875,
   "logic": "After i changes, X[i] still refers to the element at the old value of i.",
   "twin_logic": "a[i] is evaluated with the current value of i each time it is used.",
   "role": "context"
  },
  {
   "depth": 1,
   "source": "array_traversal",
   "edge": "lvl:array_traversal@L2#1",
   "target": "array_traversal@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    4
   ],
   "quote": "so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.9,
   "prune_score": 0.45,
   "score": 0.405,
   "logic": "Result: the body runs a.length times, and the result depends on the body. Squaring each element of {1, 2, 3, 4, 5} leaves {1, 4, 9, 16, 25}; summing leaves the total in the accumulator.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "array_traversal",
   "edge": "lvl:array_traversal@L4#0",
   "target": "array_traversal@L4",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4
   ],
   "quote": "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.8,
   "prune_score": 0.3,
   "score": 0.24,
   "logic": "Conservation: running the index downward (a.length-1 to 0) visits the same set of elements in reverse order, harmless for a sum but not for a shift. Starting at 1 or stopping at a.length-1 drops an element. Invariant: before pass i, elements 0..i-1 have been processed.",
   "twin_logic": null,
   "level": "L4",
   "way": "predict_a_change"
  },
  {
   "depth": 1,
   "source": "array_traversal",
   "edge": "lvl:array_traversal@L3#2",
   "target": "array_traversal@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.8,
   "prune_score": 0.25,
   "score": 0.2,
   "logic": "for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order; the bound must be < a.length, not <=.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 1,
   "source": "for_loop",
   "edge": "err:for_loop->WrongIterationCount",
   "target": "WrongIterationCount",
   "kind": "error",
   "label": "correct",
   "clauses": [
    1,
    2,
    3,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.85,
   "prune_score": 0.45,
   "score": 0.3825,
   "logic": "Updates the loop counter so that the loop runs the wrong number of times.",
   "twin_logic": "The init, test and update together decide the number of passes; trace them to check the count.",
   "role": "primary"
  },
  {
   "depth": 1,
   "source": "for_loop",
   "edge": "mis:for_loop->ForIsConditional",
   "target": "ForIsConditional",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    2,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.85,
   "prune_score": 0.25,
   "score": 0.2125,
   "logic": "The body of a for statement executes at most once.",
   "twin_logic": "The body of a for statement runs once for every pass on which the condition is true, which can be many times.",
   "role": "primary"
  },
  {
   "depth": 1,
   "source": "for_loop",
   "edge": "lvl:for_loop@L3#2",
   "target": "for_loop@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.9,
   "prune_score": 0.4,
   "score": 0.36,
   "logic": "for (int i = 0; i < N; i++) gives i each valid index 0..N-1 exactly once in increasing order, the standard way to process every array element.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 1,
   "source": "for_loop",
   "edge": "lvl:for_loop@L4#0",
   "target": "for_loop@L4",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4
   ],
   "quote": "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.75,
   "prune_score": 0.35,
   "score": 0.2625,
   "logic": "Rewriting a for as the equivalent while (init before, update at the end of the body) keeps behaviour, except that continue then skips the update and the loop variable stays in scope after the loop. Changing the bound or the step changes the pass count predictably (< to <= adds one pass).",
   "twin_logic": null,
   "level": "L4",
   "way": "predict_a_change"
  },
  {
   "depth": 1,
   "source": "for_loop",
   "edge": "lvl:for_loop@L2#1",
   "target": "for_loop@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2,
    3,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.9,
   "prune_score": 0.25,
   "score": 0.225,
   "logic": "A for statement has no value; the passes it makes are fixed by its header: for (int i = 1; i <= N; i++) sum += i; leaves sum = N(N+1)/2, and for (int i = 2; i <= 8; i += 2) prints 2, 4, 6, 8,.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "loop_control",
   "edge": "mis:loop_control->OffByOneBound",
   "target": "OffByOneBound",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    2,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.85,
   "prune_score": 0.45,
   "score": 0.3825,
   "logic": "i < n and i <= n mean the same, so the loop runs until i equals n and the last pass can use a[n].",
   "twin_logic": "for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n.",
   "role": "primary"
  },
  {
   "depth": 1,
   "source": "loop_control",
   "edge": "err:loop_control->WrongIterationCount",
   "target": "WrongIterationCount",
   "kind": "error",
   "label": "correct",
   "clauses": [
    3,
    4
   ],
   "quote": "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.8,
   "prune_score": 0.35,
   "score": 0.28,
   "logic": "Updates the loop counter so that the loop runs the wrong number of times.",
   "twin_logic": "The init, test and update together decide the number of passes; trace them to check the count.",
   "role": "primary"
  },
  {
   "depth": 1,
   "source": "loop_control",
   "edge": "lvl:loop_control@L2#1",
   "target": "loop_control@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.9,
   "prune_score": 0.4,
   "score": 0.36,
   "logic": "The number of passes and the values seen follow from the three parts: for (int i = 0; i <= N; i++) makes N+1 passes with i = 0..N; with i < N it makes N passes; i += 2 visits every second value.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "loop_control",
   "edge": "lvl:loop_control@L3#5",
   "target": "loop_control@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.8,
   "prune_score": 0.35,
   "score": 0.28,
   "logic": "The initialization and the condition of a loop fix how many times it runs; one wrong bound makes it run once too many or too few.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 1,
   "source": "loop_control",
   "edge": "lvl:loop_control@L4#0",
   "target": "loop_control@L4",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4
   ],
   "quote": "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.7,
   "prune_score": 0.25,
   "score": 0.175,
   "logic": "Changing < to <= adds one pass; starting at 1 instead of 0 removes one; doubling the step halves the passes; reversing init and bound with i-- visits the same values in reverse order (and still processes the same set only if both ends are adjusted).",
   "twin_logic": null,
   "level": "L4",
   "way": "predict_a_change"
  },
  {
   "depth": 2,
   "source": "array_traversal",
   "edge": "pre:length_field->array_traversal",
   "target": "length_field",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.95,
   "prune_score": 0.45,
   "score": 0.4275,
   "logic": "A traversal loop runs its index from 0 while it is below a.length, so it visits every element once.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "array_traversal",
   "edge": "pre:for_loop->array_traversal",
   "target": "for_loop",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.93,
   "prune_score": 0.3,
   "score": 0.279,
   "logic": "for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "array_traversal",
   "edge": "pre:indexing->array_traversal",
   "target": "indexing",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.9,
   "prune_score": 0.25,
   "score": 0.225,
   "logic": "A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "for_loop",
   "edge": "pre:loop_control->for_loop",
   "target": "loop_control",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.6,
   "prune_score": 0.5,
   "score": 0.3,
   "logic": "The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "for_loop",
   "edge": "pre:for_loop->loop_body",
   "target": "loop_body",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.85,
   "prune_score": 0.4,
   "score": 0.34,
   "logic": "The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "loop_control",
   "edge": "pre:loop_variable->loop_control",
   "target": "loop_variable",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.75,
   "prune_score": 0.8,
   "score": 0.6,
   "logic": "The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "loop_variable",
   "edge": "mis:loop_variable->LoopOutputSameEachPass",
   "target": "LoopOutputSameEachPass",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    2
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12",
   "confidence": 0.85,
   "prune_score": 0.5,
   "score": 0.425,
   "logic": "A loop prints the same thing on every pass; the changing loop variable does not affect what the body does.",
   "twin_logic": "The body uses the current value of the loop variable, so its output can differ on each pass.",
   "role": "primary"
  },
  {
   "depth": 3,
   "source": "loop_variable",
   "edge": "mis:loop_variable->LoopVariableLimitsValues",
   "target": "LoopVariableLimitsValues",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    2,
    4
   ],
   "quote": "so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.6,
   "prune_score": 0.25,
   "score": 0.15,
   "logic": "The range of the loop variable limits the values that can be read or printed inside the loop.",
   "twin_logic": "The loop variable only counts passes; other values read or printed in the body are not bounded by it.",
   "role": "primary"
  },
  {
   "depth": 3,
   "source": "loop_variable",
   "edge": "lvl:loop_variable@L2#1",
   "target": "loop_variable@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.7,
   "prune_score": 0.4,
   "score": 0.28,
   "logic": "Across passes the loop variable takes a predictable sequence of values, e.g. 4, 5, ..., 10 in TenHellos, and after a while loop it holds the first value that failed the test (11).",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 3,
   "source": "loop_variable",
   "edge": "lvl:loop_variable@L3#2",
   "target": "loop_variable@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.85,
   "prune_score": 0.3,
   "score": 0.255,
   "logic": "Role: stepper - a variable stepping through a systematic, predictable succession of values; it counts passes and often serves as an index.",
   "twin_logic": null,
   "level": "L3",
   "way": "purpose_of_the_whole"
  },
  {
   "depth": 3,
   "source": "loop_control",
   "edge": "pre:loop_control->for_loop",
   "target": "for_loop",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.6,
   "prune_score": 0.75,
   "score": 0.45,
   "logic": "The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "length_field",
   "edge": "mis:length_field->ArrayHasLengthMethod",
   "target": "ArrayHasLengthMethod",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    3
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4",
   "confidence": 0.8,
   "prune_score": 0.9,
   "score": 0.72,
   "logic": "The size of an array is found by calling a.length().",
   "twin_logic": "An array's size is the field a.length, written without parentheses.",
   "role": "primary"
  },
  {
   "depth": 3,
   "source": "length_field",
   "edge": "lvl:length_field@L4#0",
   "target": "length_field@L4",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4
   ],
   "quote": "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.88,
   "prune_score": 0.5,
   "score": 0.44,
   "logic": "Conservation: for a given array object a.length never changes, so loops bounded by a.length stay correct when the array is created with a different size. Reassigning a to another array changes a.length.",
   "twin_logic": null,
   "level": "L4",
   "way": "predict_a_change"
  },
  {
   "depth": 3,
   "source": "length_field",
   "edge": "lvl:length_field@L3#2",
   "target": "length_field@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4
   ],
   "quote": "With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.85,
   "prune_score": 0.3,
   "score": 0.255,
   "logic": "Plan/role: a fixed value (Sajaniemi) that lets code adapt to any array size instead of a hard-coded magic number, e.g. loop bounds and the last element.",
   "twin_logic": null,
   "level": "L3",
   "way": "purpose_of_the_whole"
  },
  {
   "depth": 3,
   "source": "length_field",
   "edge": "lvl:length_field@L1#1",
   "target": "length_field@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    3
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4",
   "confidence": 0.8,
   "prune_score": 0.2,
   "score": 0.16,
   "logic": "Declarative: the length of array a is written a.length (no parentheses); it equals the size given at creation, may be zero, cannot be assigned, and the last element is a[a.length-1].",
   "twin_logic": null,
   "level": "L1",
   "way": "states_the_rule"
  },
  {
   "depth": 3,
   "source": "array_traversal",
   "edge": "pre:for_loop->array_traversal",
   "target": "for_loop",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; With 8 added, a.length becomes 4; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.93,
   "prune_score": 0.6,
   "score": 0.558,
   "logic": "for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "array_traversal",
   "edge": "pre:indexing->array_traversal",
   "target": "indexing",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.9,
   "prune_score": 0.4,
   "score": 0.36,
   "logic": "A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "loop_body",
   "edge": "mis:loop_body->StateChangeIgnoredAcrossPasses",
   "target": "StateChangeIgnoredAcrossPasses",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    2,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.9,
   "prune_score": 0.45,
   "score": 0.405,
   "logic": "Values changed by one pass of a loop (other than the loop variable) do not affect later passes.",
   "twin_logic": "Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.",
   "role": "primary"
  },
  {
   "depth": 3,
   "source": "loop_body",
   "edge": "mis:loop_body->LoopOutputSameEachPass",
   "target": "LoopOutputSameEachPass",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum",
   "confidence": 0.6,
   "prune_score": 0.3,
   "score": 0.18,
   "logic": "A loop prints the same thing on every pass; the changing loop variable does not affect what the body does.",
   "twin_logic": "The body uses the current value of the loop variable, so its output can differ on each pass.",
   "role": "context"
  },
  {
   "depth": 3,
   "source": "loop_body",
   "edge": "mis:loop_body->StatementAfterLoopInBody",
   "target": "StatementAfterLoopInBody",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    2,
    4
   ],
   "quote": "so it prints Total: 12; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.75,
   "prune_score": 0.25,
   "score": 0.1875,
   "logic": "A statement written after the loop is repeated with the loop body.",
   "twin_logic": "The body ends at the closing brace (or after its single statement); code after it runs once, after the loop ends.",
   "role": "primary"
  },
  {
   "depth": 3,
   "source": "loop_body",
   "edge": "lvl:loop_body@L3#0",
   "target": "loop_body@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.6,
   "prune_score": 0.4,
   "score": 0.24,
   "logic": "The accumulator update (sum += x) is placed inside the body so it runs once per pass, while the accumulator is declared and initialized before the loop.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 3,
   "source": "loop_body",
   "edge": "lvl:loop_body@L2#1",
   "target": "loop_body@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    4
   ],
   "quote": "The loop visits each index from 0 to a.length - 1 and adds that element to sum; so the loop runs once more and prints Total: 20, with no other change to the code",
   "confidence": 0.7,
   "prune_score": 0.35,
   "score": 0.245,
   "logic": "The body's output on each pass depends on the current values, so successive passes can print different lines: TenHellos prints '4th Hello', '5th Hello', ...; the number of executions of each body statement equals the number of passes.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  }
 ],
 "clause_coverage": {
  "The loop visits each index from 0 to a.length - 1 and adds that element to sum": "mis:array_traversal->OffByOneBound",
  "so it prints Total: 12": "mis:array_traversal->ElementBoundToOldIndex",
  "With 8 added, a.length becomes 4": "mis:array_traversal->OffByOneBound",
  "so the loop runs once more and prints Total: 20, with no other change to the code": "mis:array_traversal->OffByOneBound"
 },
 "unexplained_clauses": [],
 "stop_reason": "max depth",
 "depth_reached": 3,
 "llm_calls": 21,
 "llm_cache_hits": 34,
 "llm_calls_by_step": {
  "prune": 18,
  "label": 37
 }
}
```
