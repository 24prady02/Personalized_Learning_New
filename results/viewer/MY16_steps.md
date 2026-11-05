# Think on the Graph: every output of the run MY16
## 0. Input
Program:
```java
int[] a = {4, 7, 2, 9};
int sum = 0, max = a[0];
for (int i = 0; i < a.length; i++) {
    sum += a[i];
    if (a[i] > max) max = a[i];
}
double avg = (double) sum / a.length;
System.out.println(sum + " " + max + " " + avg);
```
Question: Explain how each of sum, max and avg gets its value.

Student's answer: sum adds every element, giving 22. max starts at 4 and keeps the biggest, 9. For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0
Settings: width 3, depth 3, prune llm, backend claude-cli, model claude-opus-5-5
## 1. Stage 1: the subgraph G from the code (no model)
Masked code (string and char literals and comments blanked; this is what the patterns see):
```
int[] a = {4, 7, 2, 9};
int sum = 0, max = a[0];
for (int i = 0; i < a.length; i++) {
    sum += a[i];
    if (a[i] > max) max = a[i];
}
double avg = (double) sum / a.length;
System.out.println(sum + " " + max + " " + avg);
```
Which code text tagged which concept (a generic concept fires on almost any Java line; it starts the walk only if the answer repeats its tag):
| concept | generic | channel | matched text | line |
|---|---|---|---|---|
| accumulator_pattern | False | pattern | 'sum += a[i];' | 4 |
| arithmetic_operators | False | pattern | 'm / a' | 7 |
| array_bounds | False | pattern | 'i < a.length' | 3 |
| array_declaration | False | pattern | 'int[] a' | 1 |
| array_initializer | False | pattern | '= {' | 1 |
| array_traversal | False | pattern | 'for (int i = 0; i < a.length' | 3 |
| array_traversal | False | pattern | 'for (int i = 0; i < a.length; i++) {\n    sum += a[i]' | 3 |
| assignment | True | pattern | '=' | 1 |
| boolean_expression | False | pattern | 'if (' | 5 |
| boolean_expression | False | pattern | 'for (int i = 0; i < a.length;' | 3 |
| comparison_operators | False | pattern | 'for (int i = 0; i <' | 3 |
| compound_assignment | False | pattern | '+=' | 4 |
| control_flow | False | pattern | 'for (' | 3 |
| data_structure | False | pattern | 'int[]' | 1 |
| data_type | True | pattern | 'int' | 1 |
| explicit_cast | False | pattern | '(double)' | 7 |
| expression | True | pattern | 'i <' | 3 |
| expression | True | pattern | '= {4, 7, 2, 9};' | 1 |
| for_loop | False | pattern | 'for (' | 3 |
| if_statement | False | pattern | 'if (' | 5 |
| increment_operators | False | pattern | '++' | 3 |
| indexing | False | pattern | 'a[0]' | 2 |
| length_field | False | pattern | '.length' | 3 |
| loop_body | False | pattern | 'for (' | 3 |
| loop_control | False | signal | 'for (int i = 0; i < a.length; i++)' | 3 |
| loop_scope | False | pattern | 'for (int i' | 3 |
| loop_variable | False | pattern | 'for (int i =' | 3 |
| primitive_type | True | pattern | 'int' | 1 |
| println | False | pattern | 'System.out.println(' | 8 |
| running_extreme | False | pattern | 'if (a[i] > max)' | 5 |
| running_extreme | False | pattern | 'max = a[0];' | 2 |
| statement | True | pattern | ';' | 1 |
| string_concatenation | False | pattern | '+ " "' | 8 |
| string_conversion | False | pattern | '" + max' | 8 |
| string_conversion | False | pattern | 'sum + "' | 8 |
| string_literal | True | pattern | '" "' | 8 |
| type_conversion | False | pattern | '(double)' | 7 |

G: 32 concept nodes (6 generic), 36 concept edges, 199 misconception / error edges, 141 misconception / error nodes, 160 level nodes, 225 level-misconception links, 1 connected piece(s).

Concept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):
| edge | type | rule (logic) |
|---|---|---|
| par:assignment~comparison_operators | parallel | x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands. |
| par:increment_operators~compound_assignment | parallel | i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, *=, /=, %=). |
| par:running_extreme~accumulator_pattern | parallel | Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value. |
| par:string_concatenation~arithmetic_operators | parallel | + adds when both operands are numbers and concatenates when either operand is a String, converting the other operand to a String. It is left-associative, so 1 + 2 + "3" is "33" but "1" + 2 + 3 is "123". |
| pre:arithmetic_operators->expression | prerequisite | An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones. |
| pre:array_declaration->array_initializer | prerequisite | int[] a = {1, 2, 3}; declares the array variable and creates and fills the array in one statement. |
| pre:array_initializer->indexing | prerequisite | The values listed in braces are stored at indices 0, 1, 2, ... in order, and a[i] reads the value at index i. |
| pre:array_initializer->length_field | prerequisite | An array made from a literal has as many elements as values listed, and a.length gives that number. |
| pre:array_traversal->running_extreme | prerequisite | The running maximum is found by traversing the array once, keeping the largest value seen so far (starting from Double.NEGATIVE_INFINITY). |
| pre:assignment->compound_assignment | prerequisite | x op= e is shorthand for the assignment x = x op e. |
| pre:assignment->increment_operators | prerequisite | i++ is shorthand for the assignment i = i + 1. |
| pre:boolean_expression->if_statement | prerequisite | An if runs its block only when its boolean expression evaluates to true. |
| pre:comparison_operators->boolean_expression | prerequisite | A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making. |
| pre:compound_assignment->accumulator_pattern | prerequisite | sum += x is the usual way a running total is updated on each pass. |
| pre:control_flow->if_statement | prerequisite | An if changes the default top-to-bottom flow by running a block only when its condition is true. |
| pre:data_structure->array_declaration | prerequisite | An array is a data structure: one name for a sequence of values of the same type, organised by index. |
| pre:data_type->data_structure | prerequisite | A data structure organizes many values of a data type; the array holds a sequence of values of one type. |
| pre:data_type->primitive_type | prerequisite | Java has eight primitive data types (boolean, char, byte, short, int, long, float, double); each, like any data type, is a set of values and a set of operations on those values. |
| pre:explicit_cast->compound_assignment | prerequisite | x op= e means x = (T)(x op e), where T is the type of x, so the result is cast back to the type of x. |
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
| pre:primitive_type->type_conversion | prerequisite | Conversion moves a value between primitive types: int to double happens automatically, while double to int needs a cast that drops the fraction. |
| pre:statement->control_flow | prerequisite | Control flow is the order in which statements run. |
| pre:statement->println | prerequisite | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |
| pre:string_concatenation->string_conversion | prerequisite | When one operand of + is a String, Java converts the other operand to a String before concatenating. |
| pre:string_literal->println | prerequisite | println("s") outputs exactly the characters between the quotes and then ends the line. |
| pre:type_conversion->explicit_cast | prerequisite | A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2). |

Misconception / error edges per concept (count), and level ways per concept (count):
| concept | misconception / error edges | level ways (L1-L4 + L0 non-misconception) |
|---|---|---|
| accumulator_pattern | 4 | 17 |
| arithmetic_operators | 3 | 18 |
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
| explicit_cast | 6 | 19 |
| expression | 8 | 19 |
| for_loop | 21 | 24 |
| if_statement | 22 | 19 |
| increment_operators | 5 | 16 |
| indexing | 8 | 21 |
| length_field | 2 | 15 |
| loop_body | 12 | 14 |
| loop_control | 11 | 19 |
| loop_scope | 5 | 14 |
| loop_variable | 7 | 13 |
| primitive_type | 2 | 21 |
| println | 6 | 17 |
| running_extreme | 1 | 14 |
| statement | 5 | 19 |
| string_concatenation | 3 | 16 |
| string_conversion | 1 | 13 |
| string_literal | 4 | 16 |
| type_conversion | 3 | 18 |

Figure 1: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY16_figure01.png

Figure 2: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY16_figure02.png

## 2. Clauses and start concepts (no model)
The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):
| clause | text |
|---|---|
| c1 | sum adds every element, giving 22 |
| c2 | max starts at 4 and keeps the biggest, 9 |
| c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |

start: generic concepts whose tagging text occurs in the answer: assignment

start: BM25 of the answer against each tagged concept: accumulator_pattern 24.23 (hits 1), arithmetic_operators 23.06 (hits 1), running_extreme 21.49 (hits 2), loop_body 18.47 (hits 1), for_loop 18.13 (hits 1), compound_assignment 17.90 (hits 1), loop_control 17.72 (hits 1), array_traversal 16.34 (hits 2), assignment 15.20 (hits 1), explicit_cast 15.12 (hits 1), type_conversion 14.88 (hits 1), string_concatenation 14.62 (hits 1), indexing 12.13 (hits 1), if_statement 12.06 (hits 1), println 11.61 (hits 1), array_declaration 11.47 (hits 1), increment_operators 10.82 (hits 1), length_field 10.75 (hits 1), loop_scope 10.70 (hits 1), loop_variable 9.28 (hits 1), control_flow 8.50 (hits 1), boolean_expression 8.24 (hits 2), comparison_operators 6.93 (hits 1), array_initializer 6.81 (hits 1), array_bounds 6.51 (hits 1), string_conversion 5.35 (hits 2), data_structure 1.64 (hits 1)

start: chosen accumulator_pattern, arithmetic_operators, running_extreme

start concepts (3): accumulator_pattern, arithmetic_operators, running_extreme

Start concepts: accumulator_pattern, arithmetic_operators, running_extreme

Figure 3: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY16_figure03.png

## 3. The walk, depth by depth
At each depth, for each current concept: the edges offered (a concept entering as a start concept offers its misconception / error edges and its level ways, as two families; otherwise it offers its concept edges), the prune prompt and the model's reply, then the label prompt(s) and the model's reply, parsed into label / clauses / confidence. Score = prune score x confidence.

### Depth 1: current concepts 'accumulator_pattern', 'arithmetic_operators', 'running_extreme'

#### accumulator_pattern, misconceptions: 4 edges offered
Edges offered:
| edge |
|---|
| err:accumulator_pattern->AccumulatorDeclaredInLoop \| wrong rule: Declaring sum inside the loop body keeps a running total across passes. \| right rule: The accumulator must be declared and initialised before the loop. |
| mis:accumulator_pattern->LoopBodyScopeImpliesLoopLifetime \| wrong rule: a variable declared in the loop body lives across all iterations \| right rule: A variable declared inside the body is created anew on every pass and does not keep the previous pass's value. |
| mis:accumulator_pattern->StateChangeIgnoredAcrossPasses \| wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. \| right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones. |
| mis:accumulator_pattern->VariableRolesInferred \| wrong rule: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. \| right rule: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:accumulator_pattern->StateChangeIgnoredAcrossPasses (Score: 0.5)}
{err:accumulator_pattern->AccumulatorDeclaredInLoop (Score: 0.25)}
{mis:accumulator_pattern->VariableRolesInferred (Score: 0.25)}
```
Kept by pruning: mis:accumulator_pattern->StateChangeIgnoredAcrossPasses (0.50), err:accumulator_pattern->AccumulatorDeclaredInLoop (0.25), mis:accumulator_pattern->VariableRolesInferred (0.25)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:accumulator_pattern->StateChangeIgnoredAcrossPasses \| wrong rule: Values changed by one pass of a loop (other than the loop variable) do not affect later passes. \| right rule: Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones. |
| err:accumulator_pattern->AccumulatorDeclaredInLoop \| wrong rule: Declaring sum inside the loop body keeps a running total across passes. \| right rule: The accumulator must be declared and initialised before the loop. |
| mis:accumulator_pattern->VariableRolesInferred \| wrong rule: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. \| right rule: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update. |
Model's reply:
```
mis:accumulator_pattern->StateChangeIgnoredAcrossPasses | correct | clauses: 1, 2 | confidence: 0.85
err:accumulator_pattern->AccumulatorDeclaredInLoop | not applied | clauses: none | confidence: 0.85
mis:accumulator_pattern->VariableRolesInferred | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:accumulator_pattern->StateChangeIgnoredAcrossPasses | correct | 0.5 | 0.85 | 0.42 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| err:accumulator_pattern->AccumulatorDeclaredInLoop | not applied |  |  | 0.0 |  |  |
| mis:accumulator_pattern->VariableRolesInferred | not applied |  |  | 0.0 |  |  |

#### accumulator_pattern, level ways: 17 edges offered
Edges offered:
| edge |
|---|
| lvl:accumulator_pattern@L0#0 \| level L0 way everyday_reading: Folk meaning: 'the sum' is a single mathematical quantity that simply exists, and a person adding numbers keeps the running total in mind automatically. In Java the total is a variable that must be declared and initialized before the loop and explicitly updated on every pass (sum += x). |
| lvl:accumulator_pattern@L0#2 \| level L0 way inconsistent_trace: Applies the update rule (LT) unevenly: adds the new value to the previous total on some passes but restarts from the initial value (or forgets to add) on others. (here mixing in: "a variable declared in the loop body lives across all iterations") |
| lvl:accumulator_pattern@L1#0 \| level L1 way names_the_element: An accumulator is a variable used to accumulate results during a traversal, e.g. the running total of a sum. |
| lvl:accumulator_pattern@L1#1 \| level L1 way states_the_rule: Initialize the accumulator before the loop (0 for a sum, 1 for a product), update it once per pass in the body (total += array[i]), and use it after the loop. |
| lvl:accumulator_pattern@L2#0 \| level L2 way line_by_line_trace: Before the loop: total = initial value. Each pass: read total, combine with the current item, store back. After the loop: total holds the combination of all items. |
| lvl:accumulator_pattern@L2#1 \| level L2 way output_prediction: After the loop the accumulator holds the reduce result: sum of 1..N is N(N+1)/2; Harmonic(2) = 1.5; the product loop gives N!. |
| lvl:accumulator_pattern@L2#2 \| level L2 way one_step_execution: One pass changes only the accumulator (and the loop variable): sum += x[i] turns sum = 1 into 5 when x[i] = 4. |
| lvl:accumulator_pattern@L3#0 \| level L3 way relation_to_neighbour: The update sum += x sits inside the body so it runs once per pass, while the declaration and initialization stay before the loop. |
| lvl:accumulator_pattern@L3#1 \| level L3 way relation_to_neighbour: A counter is an accumulator that adds 1 on each pass that matches (count++), whereas an accumulator adds the current value itself (sum += x). |
| lvl:accumulator_pattern@L3#2 \| level L3 way relation_to_neighbour: In a sentinel loop the sum and the count of the values read are both accumulators, updated only for values that are not the sentinel. |
| lvl:accumulator_pattern@L3#3 \| level L3 way relation_to_neighbour: Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value. |
| lvl:accumulator_pattern@L3#4 \| level L3 way purpose_of_the_whole: Role: gatherer - a data item accumulating the effect of individual values (running total, product, concatenated string). |
| lvl:accumulator_pattern@L4#0 \| level L4 way predict_a_change: Changing the initial value shifts the result by that amount (sum starts at 1 gives sum + 1); a product starting at 0 stays 0; reordering the items does not change an integer sum (addition is commutative) but may change a floating-point sum slightly. |
| lvl:accumulator_pattern@L4#1 \| level L4 way diagnose_an_error: rule broken: A variable declared in the body is in scope only to the end of the body and is re-declared and re-initialized on every pass. Kind: silent logic error. Trigger class: for (...) { int sum = 0; sum += a[i]; }: sum restarts at 0 each pass, so only the last term survives; printing sum after the loop is a compile-time error (cannot find symbol) because sum is out of scope. |
| lvl:accumulator_pattern@L4#2 \| level L4 way transfer_to_a_new_program: Use an accumulator whenever many values must be reduced to one (sum, product, average, string); for a maximum or minimum use a most-wanted holder updated by an if instead. |
| lvl:accumulator_pattern@L4#3 \| level L4 way diagnose_an_error: rule broken: The accumulator must be initialized before the loop. Kind: compile-time. Trigger class: Declaring int sum; and then sum += x in the loop: 'variable sum might not have been initialized'. |
| lvl:accumulator_pattern@L4#4 \| level L4 way diagnose_an_error: rule broken: A sum must start at 0 and a product at 1. Kind: silent logic error. Trigger class: product initialized to 0 (result always 0) or sum initialized to the first element and then adding it again (first element counted twice). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:accumulator_pattern@L2#1 (Score: 0.45)}
{lvl:accumulator_pattern@L3#3 (Score: 0.35)}
{lvl:accumulator_pattern@L2#0 (Score: 0.2)}
```
Kept by pruning: lvl:accumulator_pattern@L2#1 (0.45), lvl:accumulator_pattern@L3#3 (0.35), lvl:accumulator_pattern@L2#0 (0.20)

Label prompt for level way lvl:accumulator_pattern@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> After the loop the accumulator holds the reduce result: sum of 1..N is N(N+1)/2; Harmonic(2) = 1.5; the product loop gives N!.

Model's reply:
```
Label: shown
Clauses: 1, 2
Confidence: 0.85
```

Label prompt for level way lvl:accumulator_pattern@L3#3 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value.

Model's reply:
```
Label: shown
Clauses: 1, 2
Confidence: 0.6
```

Label prompt for level way lvl:accumulator_pattern@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Before the loop: total = initial value. Each pass: read total, combine with the current item, store back. After the loop: total holds the combination of all items.

Model's reply:
```
Label: shown
Clauses: 1, 2
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:accumulator_pattern@L2#1 | shown | 0.45 | 0.85 | 0.38 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| lvl:accumulator_pattern@L3#3 | shown | 0.35 | 0.6 | 0.21 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| lvl:accumulator_pattern@L2#0 | shown | 0.2 | 0.6 | 0.12 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |

#### arithmetic_operators, misconceptions: 3 edges offered
Edges offered:
| edge |
|---|
| mis:arithmetic_operators->ArithmeticOnNumericStrings \| wrong rule: "10" - 1 or "6" * "2" works because the strings look like numbers. \| right rule: Arithmetic operators other than + are not defined for Strings; a String of digits must first be converted to a number, e.g. with Integer.parseInt. |
| mis:arithmetic_operators->CaretIsPower \| wrong rule: a^2 computes a squared. \| right rule: Java has no exponent operator; ^ is exclusive or, and a * a or Math.pow(a, 2) computes a squared. |
| mis:arithmetic_operators->RemainderIsSubtraction \| wrong rule: 9 % 5 means 9 minus 5 (a % b subtracts b from a). \| right rule: % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 * 5 + 4, and 17 % 5 is 2, not 12. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:arithmetic_operators->RemainderIsSubtraction (1.00)
```
Kept by pruning: mis:arithmetic_operators->RemainderIsSubtraction (1.00)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:arithmetic_operators->RemainderIsSubtraction \| wrong rule: 9 % 5 means 9 minus 5 (a % b subtracts b from a). \| right rule: % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 * 5 + 4, and 17 % 5 is 2, not 12. |
Model's reply:
```
mis:arithmetic_operators->RemainderIsSubtraction | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:arithmetic_operators->RemainderIsSubtraction | not applied |  |  | 0.0 |  |  |

#### arithmetic_operators, level ways: 18 edges offered
Edges offered:
| edge |
|---|
| lvl:arithmetic_operators@L0#0 \| level L0 way everyday_reading: In maths notation, multiplication can be implicit (2x), ^ or a superscript means a power, ÷ is exact division, and % means percent. In Java * must be written, / depends on the operand types, % is the remainder, and there is no power operator (^ is exclusive or). |
| lvl:arithmetic_operators@L0#2 \| level L0 way inconsistent_trace: Points to LT (evaluate operands, then apply the operator in the promoted type). Applied unevenly, a student uses integer division for one / and real division for another / in the same int expression. (here mixing in: "a^2 computes a squared") |
| lvl:arithmetic_operators@L1#0 \| level L1 way names_the_element: Arithmetic operators: the binary operators + - * / % that combine two numeric operands into a numeric result. |
| lvl:arithmetic_operators@L1#1 \| level L1 way states_the_rule: Both operands must be numeric, and the result has the promoted type (int, long or double). * / % bind tighter than + -, all group left to right, and int / or % by zero throws ArithmeticException. Unary minus negates its operand (-x) and unary plus leaves it unchanged; they bind more tightly than * and /, so -a * b is (-a) * b. |
| lvl:arithmetic_operators@L2#0 \| level L2 way line_by_line_trace: The left operand is evaluated fully, then the right operand, and then the operator is applied in the promoted type. |
| lvl:arithmetic_operators@L2#1 \| level L2 way output_prediction: With ints, 17 / 3 is 5 and 17 % 3 is 2. With doubles, 5.0 / 3.0 is 1.6666666666666667. With mixed operands, the int is promoted first (10 / 3.0 is 3.333...). |
| lvl:arithmetic_operators@L2#2 \| level L2 way one_step_execution: An arithmetic operator never changes its operands. Each variable is replaced by its value, and only an assignment (or ++ or op=) stores the result. |
| lvl:arithmetic_operators@L3#0 \| level L3 way relation_to_neighbour: Operators build larger expressions from smaller ones, and each operand can itself be any expression. |
| lvl:arithmetic_operators@L3#1 \| level L3 way relation_to_neighbour: For ints, / gives the truncated quotient and % the remainder, so (a / b) * b + a % b == a. |
| lvl:arithmetic_operators@L3#2 \| level L3 way relation_to_neighbour: int / or % by zero throws a run-time exception, while floating-point division by zero gives Infinity or NaN. |
| lvl:arithmetic_operators@L3#3 \| level L3 way relation_to_neighbour: + adds when both operands are numbers and concatenates when either operand is a String, converting the other operand to a String. It is left-associative, so 1 + 2 + "3" is "33" but "1" + 2 + 3 is "123". |
| lvl:arithmetic_operators@L3#4 \| level L3 way purpose_of_the_whole: Arithmetic operators turn formulas into code: totals, averages, unit conversions (inch * CM_PER_INCH), and digit extraction (n % 10, n / 10). |
| lvl:arithmetic_operators@L4#0 \| level L4 way predict_a_change: Changing an operand's type changes the operator's meaning (int / versus double /). Reordering * and / changes integer results (59 * 100 / 60 is 98, 59 / 60 * 100 is 0). Replacing ^ with Math.pow gives a real power. |
| lvl:arithmetic_operators@L4#1 \| level L4 way transfer_to_a_new_program: Use the operators for arithmetic on numeric types. Use the Math library for powers, roots and absolute values, and parse numeric Strings before computing with them. |
| lvl:arithmetic_operators@L4#2 \| level L4 way diagnose_an_error: rule broken: int / and % by zero are undefined. Kind: run-time exception. Trigger class: A divisor that evaluates to 0 (empty count, zero input): ArithmeticException: / by zero. |
| lvl:arithmetic_operators@L4#3 \| level L4 way diagnose_an_error: rule broken: Arithmetic operators other than + are not defined for Strings. Kind: compile-time. Trigger class: "10" - 1 or "6" * "2": 'bad operand types for binary operator'. |
| lvl:arithmetic_operators@L4#4 \| level L4 way diagnose_an_error: rule broken: ^ is not exponentiation. Kind: silent logic error. Trigger class: Writing x^2 or 10^6 for a power (10^6 is 12). |
| lvl:arithmetic_operators@L4#5 \| level L4 way diagnose_an_error: rule broken: int arithmetic wraps silently on overflow. Kind: silent logic error. Trigger class: Results outside the int range. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:arithmetic_operators@L2#1 (Score: 0.45)}
{lvl:arithmetic_operators@L2#0 (Score: 0.3)}
{lvl:arithmetic_operators@L4#0 (Score: 0.25)}
```
Kept by pruning: lvl:arithmetic_operators@L2#1 (0.45), lvl:arithmetic_operators@L2#0 (0.30), lvl:arithmetic_operators@L4#0 (0.25)

Label prompt for level way lvl:arithmetic_operators@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> With ints, 17 / 3 is 5 and 17 % 3 is 2. With doubles, 5.0 / 3.0 is 1.6666666666666667. With mixed operands, the int is promoted first (10 / 3.0 is 3.333...).

Model's reply:
```
Label: shown
Clauses: 3
Confidence: 0.6
```

Label prompt for level way lvl:arithmetic_operators@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> The left operand is evaluated fully, then the right operand, and then the operator is applied in the promoted type.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Label prompt for level way lvl:arithmetic_operators@L4#0 (the model saw only the concept, the way's name 'predict a change' and its text; no level):
> Changing an operand's type changes the operator's meaning (int / versus double /). Reordering * and / changes integer results (59 * 100 / 60 is 98, 59 / 60 * 100 is 0). Replacing ^ with Math.pow gives a real power.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.75
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:arithmetic_operators@L2#1 | shown | 0.45 | 0.6 | 0.27 | c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| lvl:arithmetic_operators@L2#0 | not applied |  |  | 0.0 |  |  |
| lvl:arithmetic_operators@L4#0 | not applied |  |  | 0.0 |  |  |

#### running_extreme, misconceptions: 1 edges offered
Edges offered:
| edge |
|---|
| mis:running_extreme->ExtremeStartsAtZero \| wrong rule: The running maximum can always start at 0. \| right rule: Start the running maximum at the most negative possible value (Double.NEGATIVE_INFINITY, or the smallest int), so that the first value read replaces it. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:running_extreme->ExtremeStartsAtZero (Score: 1.0)}
```
Kept by pruning: mis:running_extreme->ExtremeStartsAtZero (1.00)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:running_extreme->ExtremeStartsAtZero \| wrong rule: The running maximum can always start at 0. \| right rule: Start the running maximum at the most negative possible value (Double.NEGATIVE_INFINITY, or the smallest int), so that the first value read replaces it. |
Model's reply:
```
mis:running_extreme->ExtremeStartsAtZero | correct | clauses: 2 | confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:running_extreme->ExtremeStartsAtZero | correct | 1.0 | 0.6 | 0.6 | c2 | max starts at 4 and keeps the biggest, 9 |

#### running_extreme, level ways: 14 edges offered
Edges offered:
| edge |
|---|
| lvl:running_extreme@L0#0 \| level L0 way everyday_reading: Folk meaning: 'the biggest so far' starts from nothing, i.e. 0, because everyday quantities are positive. Rule: the running maximum must start at a value no data can be below (Double.NEGATIVE_INFINITY, Integer.MIN_VALUE) or at the first element, so that the first value read replaces it. |
| lvl:running_extreme@L0#2 \| level L0 way inconsistent_trace: Points to LT: on each pass, compare a[i] with max and assign max = a[i] only if a[i] is larger. Inconsistent application: max is overwritten without the comparison on some passes, or compared with a stale value. (here mixing in: "The running maximum can always start at 0") |
| lvl:running_extreme@L1#0 \| level L1 way names_the_element: Identity: a running maximum (or minimum), a variable holding the largest (smallest) value seen so far in a pass over the data; Sajaniemi's most-wanted holder. |
| lvl:running_extreme@L1#1 \| level L1 way states_the_rule: Declarative: double max = Double.NEGATIVE_INFINITY; for (int i = 0; i < N; i++) if (a[i] > max) max = a[i];. |
| lvl:running_extreme@L2#0 \| level L2 way line_by_line_trace: Sequencing: initialize max before the loop; in each pass evaluate a[i] > max, and if it is true assign max = a[i]; read max only after the loop ends. |
| lvl:running_extreme@L2#1 \| level L2 way output_prediction: Result: the largest element (of the element type). For an empty array (or no input) max stays at its start value: NEGATIVE_INFINITY, or MIN_VALUE for int. |
| lvl:running_extreme@L2#2 \| level L2 way one_step_execution: State transition: one pass changes max only when a[i] > max; otherwise nothing changes. |
| lvl:running_extreme@L3#0 \| level L3 way relation_to_neighbour: The maximum is found in one traversal, keeping the largest value seen so far, starting from Double.NEGATIVE_INFINITY. |
| lvl:running_extreme@L3#1 \| level L3 way relation_to_neighbour: Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value. |
| lvl:running_extreme@L3#2 \| level L3 way purpose_of_the_whole: Plan/role: most-wanted holder (Sajaniemi). It finds the extreme in one pass with constant extra memory; the same plan tracks the minimum with <. |
| lvl:running_extreme@L4#0 \| level L4 way predict_a_change: Conservation: replacing > by >= keeps the maximum value but changes which tied position is the last one recorded. Remembering the index of the extreme instead of its value conserves the specification. |
| lvl:running_extreme@L4#1 \| level L4 way transfer_to_a_new_program: Applicability: use a running extreme when only the max or min (or its position) is needed, in a single pass. For further facts such as how many items equal the maximum, keep the data (an array) and make a second pass. |
| lvl:running_extreme@L4#2 \| level L4 way diagnose_an_error: rule broken: The start value must not exceed every possible data value. Kind: silent logic error. Trigger class: max starts at 0 (or Double.MIN_VALUE, which is the smallest positive double) and all data are negative, so the result is the start value |
| lvl:running_extreme@L4#3 \| level L4 way diagnose_an_error: rule broken: Update only when the new value beats the current extreme. Kind: silent logic error. Trigger class: the comparison is reversed (a[i] < max), so the minimum is found, or max = a[i] is unconditional, so the last value is found |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:running_extreme@L2#1 (Score: 0.4)}
{lvl:running_extreme@L2#0 (Score: 0.35)}
{lvl:running_extreme@L1#0 (Score: 0.25)}
```
Kept by pruning: lvl:running_extreme@L2#1 (0.40), lvl:running_extreme@L2#0 (0.35), lvl:running_extreme@L1#0 (0.25)

Label prompt for level way lvl:running_extreme@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> Result: the largest element (of the element type). For an empty array (or no input) max stays at its start value: NEGATIVE_INFINITY, or MIN_VALUE for int.

Model's reply:
```
Label: shown
Clauses: 2
Confidence: 0.85
```

Label prompt for level way lvl:running_extreme@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Sequencing: initialize max before the loop; in each pass evaluate a[i] > max, and if it is true assign max = a[i]; read max only after the loop ends.

Model's reply:
```
Label: shown
Clauses: 2
Confidence: 0.7
```

Label prompt for level way lvl:running_extreme@L1#0 (the model saw only the concept, the way's name 'names the element' and its text; no level):
> Identity: a running maximum (or minimum), a variable holding the largest (smallest) value seen so far in a pass over the data; Sajaniemi's most-wanted holder.

Model's reply:
```
Label: shown
Clauses: 2
Confidence: 0.93
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:running_extreme@L2#1 | shown | 0.4 | 0.85 | 0.34 | c2 | max starts at 4 and keeps the biggest, 9 |
| lvl:running_extreme@L2#0 | shown | 0.35 | 0.7 | 0.24 | c2 | max starts at 4 and keeps the biggest, 9 |
| lvl:running_extreme@L1#0 | shown | 0.25 | 0.93 | 0.23 | c2 | max starts at 4 and keeps the biggest, 9 |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:running_extreme->ExtremeStartsAtZero [correct, tier 2, 0.60], mis:accumulator_pattern->StateChangeIgnoredAcrossPasses [correct, tier 2, 0.42], lvl:accumulator_pattern@L2#1 [shown, tier 2, 0.38]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | sum adds every element, giving 22 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| c2 | max starts at 4 and keeps the biggest, 9 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 | not covered yet |

**Uncovered clauses bring in (BM25 of the uncovered clauses against unvisited concepts):** explicit_cast (15.09), compound_assignment (14.25), for_loop (13.50)

**Graph check, not yet read (the walk may not stop while these remain):** own edges of compound_assignment, own edges of explicit_cast, own edges of for_loop, par:running_extreme~accumulator_pattern, par:string_concatenation~arithmetic_operators, pre:arithmetic_operators->expression, pre:array_traversal->running_extreme, pre:compound_assignment->accumulator_pattern, pre:loop_body->accumulator_pattern

Figure 4 (the graph after depth 1): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY16_figure04.png

### Depth 2: current concepts 'accumulator_pattern', 'arithmetic_operators', 'running_extreme', 'explicit_cast', 'compound_assignment', 'for_loop'

#### accumulator_pattern, concept edges: 3 edges offered
Edges offered:
| edge |
|---|
| par:running_extreme~accumulator_pattern \| rule: Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value. |
| pre:compound_assignment->accumulator_pattern \| rule: sum += x is the usual way a running total is updated on each pass. |
| pre:loop_body->accumulator_pattern \| rule: The accumulator update sum += x sits inside the body, so it runs once on every pass. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{par:running_extreme~accumulator_pattern (Score: 0.5)}
{pre:loop_body->accumulator_pattern (Score: 0.3)}
{pre:compound_assignment->accumulator_pattern (Score: 0.2)}
```
Kept by pruning: par:running_extreme~accumulator_pattern (0.50), pre:loop_body->accumulator_pattern (0.30), pre:compound_assignment->accumulator_pattern (0.20)

Label prompt for concept edge par:running_extreme~accumulator_pattern (running_extreme -> accumulator_pattern, parallel):
> Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value.

Model's reply:
```
Label: confirmed
Clauses: 1, 2
Confidence: 0.85
```

Label prompt for concept edge pre:loop_body->accumulator_pattern (loop_body -> accumulator_pattern, prerequisite):
> The accumulator update sum += x sits inside the body, so it runs once on every pass.

Model's reply:
```
Label: confirmed
Clauses: 1
Confidence: 0.9
```

Label prompt for concept edge pre:compound_assignment->accumulator_pattern (compound_assignment -> accumulator_pattern, prerequisite):
> sum += x is the usual way a running total is updated on each pass.

Model's reply:
```
Label: confirmed
Clauses: 1
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| par:running_extreme~accumulator_pattern | confirmed | 0.5 | 0.85 | 0.42 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| pre:loop_body->accumulator_pattern | confirmed | 0.3 | 0.9 | 0.27 | c1 | sum adds every element, giving 22 |
| pre:compound_assignment->accumulator_pattern | confirmed | 0.2 | 0.85 | 0.17 | c1 | sum adds every element, giving 22 |

#### arithmetic_operators, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| par:string_concatenation~arithmetic_operators \| rule: + adds when both operands are numbers and concatenates when either operand is a String, converting the other operand to a String. It is left-associative, so 1 + 2 + "3" is "33" but "1" + 2 + 3 is "123". |
| pre:arithmetic_operators->expression \| rule: An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:arithmetic_operators->expression (Score: 0.85)}
{par:string_concatenation~arithmetic_operators (Score: 0.15)}
```
Kept by pruning: pre:arithmetic_operators->expression (0.85), par:string_concatenation~arithmetic_operators (0.15)

Label prompt for concept edge pre:arithmetic_operators->expression (arithmetic_operators -> expression, prerequisite):
> An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones.

Model's reply:
```
Label: confirmed
Clauses: 1
Confidence: 0.6
```

Label prompt for concept edge par:string_concatenation~arithmetic_operators (string_concatenation -> arithmetic_operators, parallel):
> + adds when both operands are numbers and concatenates when either operand is a String, converting the other operand to a String. It is left-associative, so 1 + 2 + "3" is "33" but "1" + 2 + 3 is "123".

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:arithmetic_operators->expression | confirmed | 0.85 | 0.6 | 0.51 | c1 | sum adds every element, giving 22 |
| par:string_concatenation~arithmetic_operators | not applied |  |  | 0.0 |  |  |

#### running_extreme, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| par:running_extreme~accumulator_pattern \| rule: Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value. |
| pre:array_traversal->running_extreme \| rule: The running maximum is found by traversing the array once, keeping the largest value seen so far (starting from Double.NEGATIVE_INFINITY). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{par:running_extreme~accumulator_pattern (Score: 1.0)}
```
Kept by pruning: pre:array_traversal->running_extreme (1.00)

Label prompt for concept edge pre:array_traversal->running_extreme (array_traversal -> running_extreme, prerequisite):
> The running maximum is found by traversing the array once, keeping the largest value seen so far (starting from Double.NEGATIVE_INFINITY).

Model's reply:
```
Label: confirmed
Clauses: 2
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:array_traversal->running_extreme | confirmed | 1.0 | 0.85 | 0.85 | c2 | max starts at 4 and keeps the biggest, 9 |

#### explicit_cast, misconceptions: 6 edges offered
Edges offered:
| edge |
|---|
| err:explicit_cast->RoundReturnsInt \| wrong rule: Writes int n = Math.round(x); because Math.round gives an int. \| right rule: Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x); |
| mis:explicit_cast->CastAfterIntDivision \| wrong rule: (double) (3 / 5) is 0.6. \| right rule: The integer division 3 / 5 = 0 happens before the cast, so the result is 0.0. |
| mis:explicit_cast->CastAppliesToWholeExpression \| wrong rule: (int) 2.5 / 0.15 casts the whole quotient to int. \| right rule: The cast applies only to what comes right after it, here 2.5. |
| mis:explicit_cast->CastParsesString \| wrong rule: (int) args[0] converts the text "34" into the number 34. \| right rule: A String argument that represents a number must be converted with a method such as Integer.parseInt. |
| mis:explicit_cast->CastRounds \| wrong rule: (int) 2.7 evaluates to 3. \| right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer. |
| mis:explicit_cast->LaterDoubleLiteralFixesDivision \| wrong rule: Changing a later literal to 100.0 fixes an earlier int division. \| right rule: The int division happens first; the double must be in the division itself. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:explicit_cast->CastAppliesToWholeExpression (0.60), mis:explicit_cast->CastAfterIntDivision (0.30), mis:explicit_cast->LaterDoubleLiteralFixesDivision (0.10)
```
Kept by pruning: mis:explicit_cast->CastAppliesToWholeExpression (0.60), mis:explicit_cast->CastAfterIntDivision (0.30), mis:explicit_cast->LaterDoubleLiteralFixesDivision (0.10)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:explicit_cast->CastAppliesToWholeExpression \| wrong rule: (int) 2.5 / 0.15 casts the whole quotient to int. \| right rule: The cast applies only to what comes right after it, here 2.5. |
| mis:explicit_cast->CastAfterIntDivision \| wrong rule: (double) (3 / 5) is 0.6. \| right rule: The integer division 3 / 5 = 0 happens before the cast, so the result is 0.0. |
| mis:explicit_cast->LaterDoubleLiteralFixesDivision \| wrong rule: Changing a later literal to 100.0 fixes an earlier int division. \| right rule: The int division happens first; the double must be in the division itself. |
Model's reply:
```
mis:explicit_cast->CastAppliesToWholeExpression | held | clauses: 3 | confidence: 0.9
mis:explicit_cast->CastAfterIntDivision | correct | clauses: 3 | confidence: 0.6
mis:explicit_cast->LaterDoubleLiteralFixesDivision | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:explicit_cast->CastAppliesToWholeExpression | held | 0.6000000000000001 | 0.9 | 0.54 | c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| mis:explicit_cast->CastAfterIntDivision | correct | 0.30000000000000004 | 0.6 | 0.18 | c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| mis:explicit_cast->LaterDoubleLiteralFixesDivision | not applied |  |  | 0.0 |  |  |

#### explicit_cast, level ways: 19 edges offered
Edges offered:
| edge |
|---|
| lvl:explicit_cast@L0#0 \| level L0 way everyday_reading: Folk meaning: 'convert 2.7 to a whole number' means round it to 3, and (int) looks like a function label that applies to everything written after it. Java rule: a cast to int truncates toward zero ((int) 2.7 is 2) and, having higher precedence than arithmetic, applies only to the value immediately following it. |
| lvl:explicit_cast@L0#4 \| level L0 way inconsistent_trace: Points to LT (the cast is a unary operator applied to the operand right after it, before * and /). Applied unevenly: in one line the student casts only the first operand, and in another applies the same cast to the whole expression. (here mixing in: "(int) 2.7 evaluates to 3") |
| lvl:explicit_cast@L1#0 \| level L1 way names_the_element: A cast is a unary operator, written (type) expression, that converts a value of one primitive type to another, used when the conversion may lose information. |
| lvl:explicit_cast@L1#1 \| level L1 way states_the_rule: (T) e converts the value of e to type T; a double-to-int cast discards the fraction by rounding toward zero; a cast is required for narrowing conversions; it has higher precedence than arithmetic; casts between boolean and numbers, or from String to int, are not allowed. |
| lvl:explicit_cast@L2#0 \| level L2 way line_by_line_trace: Evaluate the operand immediately to the right of the cast (a parenthesized expression is evaluated completely first), convert that value, then continue with the remaining operators of the expression. |
| lvl:explicit_cast@L2#1 \| level L2 way output_prediction: (int) 2.71828 is int 2; (int) -2.7 is -2; (int) 11 * 0.3 is double 3.3; (int) (11 * 0.3) is int 3; (double) 3 / 5 is 0.6 but (double) (3 / 5) is 0.0; (char) ('a' + 4) is 'e'. |
| lvl:explicit_cast@L2#2 \| level L2 way one_step_execution: A cast yields a new value and changes nothing else: neither the type nor the value of the variable being cast changes (after int x = (int) pi; pi is still 3.14159). |
| lvl:explicit_cast@L3#0 \| level L3 way relation_to_neighbour: A cast is the explicit conversion between primitive types, needed exactly where automatic conversion is refused because information may be lost. |
| lvl:explicit_cast@L3#1 \| level L3 way relation_to_neighbour: To turn Math.random()'s double into a random int from 0 to N-1, the cast must enclose the product: (int) (Math.random() * N); casting first gives 0. |
| lvl:explicit_cast@L3#2 \| level L3 way relation_to_neighbour: x op= e contains an implicit cast back to the type of x, so with int x, x += 0.5 compiles (x = (int) (x + 0.5)) while x = x + 0.5 is a compile-time error. |
| lvl:explicit_cast@L3#3 \| level L3 way relation_to_neighbour: Widening (promotion) happens automatically when a value goes to a type with a larger range (int to double) and loses nothing; a narrowing conversion (double to int) is never automatic and needs an explicit cast, which truncates toward zero. |
| lvl:explicit_cast@L3#4 \| level L3 way relation_to_neighbour: (int) 2.71828 truncates toward zero and gives 2; Math.round(2.71828) rounds to the nearest integer and gives 3, as a long that needs (int) to become an int. |
| lvl:explicit_cast@L3#5 \| level L3 way purpose_of_the_whole: Used to discard information on purpose: truncating a scaled random number to an index, taking the integer part, converting between char and int codes ((char) ('a' + k)), or forcing real division with (double) sum / n. |
| lvl:explicit_cast@L4#0 \| level L4 way predict_a_change: Moving the parentheses changes when truncation happens ((int) (a * b) vs (int) a * b); removing a cast from a narrowing assignment turns it into a compile-time error; int to double to int restores the value, but double to int to double loses the fraction. |
| lvl:explicit_cast@L4#1 \| level L4 way transfer_to_a_new_program: Use a cast when you intend to truncate or narrow (random indices, integer parts, char codes); use Math.round to round, Integer.parseInt for Strings, and put a double into the division itself rather than casting its int result. |
| lvl:explicit_cast@L4#2 \| level L4 way diagnose_an_error: rule broken: Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x);. Kind: compile-time. Trigger class: int n = Math.round(x); with double x. |
| lvl:explicit_cast@L4#3 \| level L4 way diagnose_an_error: rule broken: A cast applies only to the value right after it. Kind: compile-time. Trigger class: int n = (int) 11 * 0.3; the product is still a double (possible loss of precision); in a double context the same mistake is a silent logic error ((int) pi * 20.0 gives 60.0). |
| lvl:explicit_cast@L4#4 \| level L4 way diagnose_an_error: rule broken: Casts require compatible types. Kind: compile-time. Trigger class: (int) "3" or (int) args[0] on a String, or a cast between boolean and a number. |
| lvl:explicit_cast@L4#5 \| level L4 way diagnose_an_error: rule broken: A narrowing cast may lose magnitude, not just the fraction. Kind: silent logic error. Trigger class: Casting a value outside the target range, e.g. (int) of a long above 2147483647 or of a huge double. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:explicit_cast@L0#0 (Score: 0.5)}
{lvl:explicit_cast@L2#1 (Score: 0.3)}
{lvl:explicit_cast@L2#0 (Score: 0.2)}
```
Kept by pruning: lvl:explicit_cast@L0#0 (0.50), lvl:explicit_cast@L2#1 (0.30), lvl:explicit_cast@L2#0 (0.20)

Label prompt for level way lvl:explicit_cast@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: 'convert 2.7 to a whole number' means round it to 3, and (int) looks like a function label that applies to everything written after it. Java rule: a cast to int truncates toward zero ((int) 2.7 is 2) and, having higher precedence than arithmetic, applies only to the value immediately following it.

Model's reply:
```
Label: shown
Clauses: 3
Confidence: 0.85
```

Label prompt for level way lvl:explicit_cast@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> (int) 2.71828 is int 2; (int) -2.7 is -2; (int) 11 * 0.3 is double 3.3; (int) (11 * 0.3) is int 3; (double) 3 / 5 is 0.6 but (double) (3 / 5) is 0.0; (char) ('a' + 4) is 'e'.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:explicit_cast@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Evaluate the operand immediately to the right of the cast (a parenthesized expression is evaluated completely first), convert that value, then continue with the remaining operators of the expression.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:explicit_cast@L0#0 | shown | 0.5 | 0.85 | 0.42 | c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| lvl:explicit_cast@L2#1 | not applied |  |  | 0.0 |  |  |
| lvl:explicit_cast@L2#0 | not applied |  |  | 0.0 |  |  |

#### compound_assignment, misconceptions: 2 edges offered
Edges offered:
| edge |
|---|
| mis:compound_assignment->CompoundAssignmentNoCast \| wrong rule: x += 0.5 adds one half to an int x. \| right rule: x += 0.5 is x = (int) (x + 0.5), so an int x does not change. |
| mis:compound_assignment->CompoundSubtractIsAssignNegative \| wrong rule: x[i] -= y sets x[i] to -y (reads -= as assignment of a negated value). \| right rule: x[i] -= y means x[i] = x[i] - y: it subtracts y from the current value. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:compound_assignment->CompoundSubtractIsAssignNegative (Score: 0.7)}
{mis:compound_assignment->CompoundAssignmentNoCast (Score: 0.3)}
```
Kept by pruning: mis:compound_assignment->CompoundSubtractIsAssignNegative (0.70), mis:compound_assignment->CompoundAssignmentNoCast (0.30)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:compound_assignment->CompoundSubtractIsAssignNegative \| wrong rule: x[i] -= y sets x[i] to -y (reads -= as assignment of a negated value). \| right rule: x[i] -= y means x[i] = x[i] - y: it subtracts y from the current value. |
| mis:compound_assignment->CompoundAssignmentNoCast \| wrong rule: x += 0.5 adds one half to an int x. \| right rule: x += 0.5 is x = (int) (x + 0.5), so an int x does not change. |
Model's reply:
```
mis:compound_assignment->CompoundSubtractIsAssignNegative | not applied | clauses: none | confidence: 0.9
mis:compound_assignment->CompoundAssignmentNoCast | not applied | clauses: none | confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:compound_assignment->CompoundSubtractIsAssignNegative | not applied |  |  | 0.0 |  |  |
| mis:compound_assignment->CompoundAssignmentNoCast | not applied |  |  | 0.0 |  |  |

#### compound_assignment, level ways: 15 edges offered
Edges offered:
| edge |
|---|
| lvl:compound_assignment@L0#0 \| level L0 way everyday_reading: Folk meaning: x -= y reads as 'x equals minus y' and x += 0.5 as 'add a half' in arithmetic. In Java x op= e means x = (T) (x op e): it updates x from its current value and casts the result back to x's type. |
| lvl:compound_assignment@L0#3 \| level L0 way inconsistent_trace: Applies the compound-assignment rule (LT) unevenly: uses the current value of x on some passes but treats x -= y as x = -y on others, or forgets the implicit cast on some lines. (here mixing in: "x += 0.5 adds one half to an int x") |
| lvl:compound_assignment@L1#0 \| level L1 way names_the_element: A compound assignment operator (+=, -=, *=, /=, %=) is an assignment shorthand that combines a binary operation with storing the result back in the left-hand variable. |
| lvl:compound_assignment@L1#1 \| level L1 way states_the_rule: x op= e is equivalent to x = (T) ((x) op (e)) where T is the type of x, with x evaluated only once; it works for any arithmetic operator in any primitive numeric type. x op= e means x = (T)(x op e), with a hidden cast to the type T of x: with int x = 3, x += 0.5 compiles and leaves 3, while x = x + 0.5 does not compile. |
| lvl:compound_assignment@L2#0 \| level L2 way line_by_line_trace: Evaluate x and save its value, then evaluate e, then compute x op e, cast to x's type, and store into x. |
| lvl:compound_assignment@L2#1 \| level L2 way output_prediction: The new value of x is (T)(old x op e) and is also the expression's value: each starting from int x = 7: x += 3 gives 10, x /= 2 gives 3, and x += 0.5 gives 7 (7.5 truncated) instead of a compile error. |
| lvl:compound_assignment@L2#2 \| level L2 way one_step_execution: One execution changes exactly one variable, x, from its old value (sum += x[i] turns sum = 1 into 1 + 4 = 5). |
| lvl:compound_assignment@L3#0 \| level L3 way relation_to_neighbour: x op= e is shorthand for the assignment x = x op e, so the new value depends on the old one (x is read, then written). |
| lvl:compound_assignment@L3#1 \| level L3 way relation_to_neighbour: x op= e includes a hidden narrowing cast to the type of x: with int x = 1, x += 1.7 compiles (as x = (int)(x + 1.7), giving 2) while x = x + 1.7 does not. |
| lvl:compound_assignment@L3#2 \| level L3 way relation_to_neighbour: i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, *=, /=, %=). |
| lvl:compound_assignment@L3#3 \| level L3 way purpose_of_the_whole: Plan/role: the update step of a gatherer (sum += a[i], product *= i) or of a stepper with a step other than 1 (i += 2). |
| lvl:compound_assignment@L4#0 \| level L4 way predict_a_change: For a variable of the same type as the result, replacing x op= e by x = x op e preserves behaviour; when x is narrower (int x, double e), x = x op e no longer compiles, so the two are not always interchangeable. Swapping += and -= reverses the effect of each pass. |
| lvl:compound_assignment@L4#1 \| level L4 way transfer_to_a_new_program: Use op= for in-place updates of accumulators, products and counters with steps other than 1; avoid it when x is int and e is fractional (silent truncation), and use explicit x = x op e when the cast should be visible. |
| lvl:compound_assignment@L4#2 \| level L4 way diagnose_an_error: rule broken: x op= e silently casts the result to the type of x. Kind: silent logic error. Trigger class: int total = 0; total += 0.5 * k; or int avg = 7; avg /= 2.0;: fractional parts are discarded (avg becomes 3) without a compiler error. |
| lvl:compound_assignment@L4#3 \| level L4 way diagnose_an_error: rule broken: =- is assignment of a negated value, not -=. Kind: silent logic error. Trigger class: Typing x =- y for x -= y: compiles as x = -y. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:compound_assignment@L3#3 (Score: 0.5)}
{lvl:compound_assignment@L2#1 (Score: 0.25)}
{lvl:compound_assignment@L3#0 (Score: 0.25)}
```
Kept by pruning: lvl:compound_assignment@L3#3 (0.50), lvl:compound_assignment@L2#1 (0.25), lvl:compound_assignment@L3#0 (0.25)

Label prompt for level way lvl:compound_assignment@L3#3 (the model saw only the concept, the way's name 'purpose of the whole' and its text; no level):
> Plan/role: the update step of a gatherer (sum += a[i], product *= i) or of a stepper with a step other than 1 (i += 2).

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.75
```

Label prompt for level way lvl:compound_assignment@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> The new value of x is (T)(old x op e) and is also the expression's value: each starting from int x = 7: x += 3 gives 10, x /= 2 gives 3, and x += 0.5 gives 7 (7.5 truncated) instead of a compile error.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.55
```

Label prompt for level way lvl:compound_assignment@L3#0 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> x op= e is shorthand for the assignment x = x op e, so the new value depends on the old one (x is read, then written).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:compound_assignment@L3#3 | shown | 0.5 | 0.75 | 0.38 | c1 | sum adds every element, giving 22 |
| lvl:compound_assignment@L2#1 | shown | 0.25 | 0.55 | 0.14 | c1 | sum adds every element, giving 22 |
| lvl:compound_assignment@L3#0 | not applied |  |  | 0.0 |  |  |

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
mis:for_loop->ForIsConditional (0.40), mis:for_loop->LoopCountIsStatementCount (0.30), mis:for_loop->ProgramEndsAfterLoop (0.30)
```
Kept by pruning: mis:for_loop->ForIsConditional (0.40), mis:for_loop->LoopCountIsStatementCount (0.30), mis:for_loop->ProgramEndsAfterLoop (0.30)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:for_loop->ForIsConditional \| wrong rule: The body of a for statement executes at most once. \| right rule: The body of a for statement runs once for every pass on which the condition is true, which can be many times. |
| mis:for_loop->LoopCountIsStatementCount \| wrong rule: The repeat count of a counted loop says how many of the body statements are executed. \| right rule: The repeat count is how many times the whole body runs; every pass runs all body statements. |
| mis:for_loop->ProgramEndsAfterLoop \| wrong rule: When a loop finishes the program ends, so code after the loop never runs. \| right rule: When the loop condition becomes false, control continues with the first statement after the loop. |
Model's reply:
```
mis:for_loop->ForIsConditional | correct | clauses: 1, 2 | confidence: 0.9
mis:for_loop->LoopCountIsStatementCount | correct | clauses: 1, 2 | confidence: 0.7
mis:for_loop->ProgramEndsAfterLoop | correct | clauses: 3 | confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:for_loop->ForIsConditional | correct | 0.4 | 0.9 | 0.36 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| mis:for_loop->LoopCountIsStatementCount | correct | 0.3 | 0.7 | 0.21 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| mis:for_loop->ProgramEndsAfterLoop | correct | 0.3 | 0.8 | 0.24 | c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |

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
{lvl:for_loop@L2#1 (Score: 0.4)}
{lvl:for_loop@L3#2 (Score: 0.35)}
{lvl:for_loop@L2#0 (Score: 0.25)}
```
Kept by pruning: lvl:for_loop@L2#1 (0.40), lvl:for_loop@L3#2 (0.35), lvl:for_loop@L2#0 (0.25)

Label prompt for level way lvl:for_loop@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> A for statement has no value; the passes it makes are fixed by its header: for (int i = 1; i <= N; i++) sum += i; leaves sum = N(N+1)/2, and for (int i = 2; i <= 8; i += 2) prints 2, 4, 6, 8,.

Model's reply:
```
Label: shown
Clauses: 1, 2
Confidence: 0.8
```

Label prompt for level way lvl:for_loop@L3#2 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> for (int i = 0; i < N; i++) gives i each valid index 0..N-1 exactly once in increasing order, the standard way to process every array element.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.6
```

Label prompt for level way lvl:for_loop@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Run the initializer once; then repeatedly: test the condition (stop if false), execute the body, run the update.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:for_loop@L2#1 | shown | 0.4 | 0.8 | 0.32 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| lvl:for_loop@L3#2 | shown | 0.35 | 0.6 | 0.21 | c1 | sum adds every element, giving 22 |
| lvl:for_loop@L2#0 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:explicit_cast->CastAppliesToWholeExpression [held, tier 0, 0.54], pre:array_traversal->running_extreme [confirmed, tier 2, 0.85], pre:arithmetic_operators->expression [confirmed, tier 2, 0.51]

reached across pre:array_traversal->running_extreme, entered next: array_traversal

reached across pre:arithmetic_operators->expression, entered next: expression

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | sum adds every element, giving 22 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| c2 | max starts at 4 and keeps the biggest, 9 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 | mis:explicit_cast->CastAppliesToWholeExpression |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of array_traversal, own edges of expression, par:increment_operators~compound_assignment, pre:assignment->compound_assignment, pre:explicit_cast->compound_assignment, pre:for_loop->array_traversal, pre:for_loop->loop_body, pre:for_loop->loop_scope, pre:loop_control->for_loop, pre:type_conversion->explicit_cast

Figure 5 (the graph after depth 2): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY16_figure05.png

### Depth 3: current concepts 'explicit_cast', 'array_traversal', 'running_extreme', 'expression', 'arithmetic_operators', 'compound_assignment', 'for_loop'

#### explicit_cast, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| pre:explicit_cast->compound_assignment \| rule: x op= e means x = (T)(x op e), where T is the type of x, so the result is cast back to the type of x. |
| pre:type_conversion->explicit_cast \| rule: A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:type_conversion->explicit_cast (Score: 0.85)}
{pre:explicit_cast->compound_assignment (Score: 0.15)}
```
Kept by pruning: pre:type_conversion->explicit_cast (0.85), pre:explicit_cast->compound_assignment (0.15)

Label prompt for concept edge pre:type_conversion->explicit_cast (type_conversion -> explicit_cast, prerequisite):
> A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2).

Model's reply:
```
Label: broken
Clauses: 3
Confidence: 0.75
```

Label prompt for concept edge pre:explicit_cast->compound_assignment (explicit_cast -> compound_assignment, prerequisite):
> x op= e means x = (T)(x op e), where T is the type of x, so the result is cast back to the type of x.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:type_conversion->explicit_cast | broken | 0.85 | 0.75 | 0.64 | c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| pre:explicit_cast->compound_assignment | not applied |  |  | 0.0 |  |  |

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
err:array_traversal->EarlyReturnInLoop (0.40), mis:array_traversal->OffByOneBound (0.30), mis:array_traversal->IdiomOverridesCode (0.30)
```
Kept by pruning: err:array_traversal->EarlyReturnInLoop (0.40), mis:array_traversal->OffByOneBound (0.30), mis:array_traversal->IdiomOverridesCode (0.30)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| err:array_traversal->EarlyReturnInLoop \| wrong rule: Leaves a traversal loop with return before every element has been processed. \| right rule: A result that depends on all elements is known only after the loop ends. |
| mis:array_traversal->OffByOneBound \| wrong rule: < vs <= and 0..n vs 0..n-1 are interchangeable \| right rule: for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n. |
| mis:array_traversal->IdiomOverridesCode \| wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. |
Model's reply:
```
err:array_traversal->EarlyReturnInLoop | not applied | clauses: none | confidence: 0.85
mis:array_traversal->OffByOneBound | correct | clauses: 1, 2 | confidence: 0.6
mis:array_traversal->IdiomOverridesCode | not applied | clauses: none | confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| err:array_traversal->EarlyReturnInLoop | not applied |  |  | 0.0 |  |  |
| mis:array_traversal->OffByOneBound | correct | 0.3 | 0.6 | 0.18 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| mis:array_traversal->IdiomOverridesCode | not applied |  |  | 0.0 |  |  |

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
{lvl:array_traversal@L3#8 (Score: 0.4)}
{lvl:array_traversal@L2#1 (Score: 0.35)}
{lvl:array_traversal@L3#6 (Score: 0.25)}
```
Kept by pruning: lvl:array_traversal@L3#8 (0.40), lvl:array_traversal@L2#1 (0.35), lvl:array_traversal@L3#6 (0.25)

Label prompt for level way lvl:array_traversal@L3#8 (the model saw only the concept, the way's name 'purpose of the whole' and its text; no level):
> Plan/role: the index is a stepper, and the loop carries out a Soloway-style plan (accumulate/sum with a gatherer, count, search, find the extreme, copy) once for each element.

Model's reply:
```
Label: shown
Clauses: 1, 2
Confidence: 0.85
```

Label prompt for level way lvl:array_traversal@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> Result: the body runs a.length times, and the result depends on the body. Squaring each element of {1, 2, 3, 4, 5} leaves {1, 4, 9, 16, 25}; summing leaves the total in the accumulator.

Model's reply:
```
Label: shown
Clauses: 1, 2
Confidence: 0.85
```

Label prompt for level way lvl:array_traversal@L3#6 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> The running maximum is found in one traversal that keeps the largest value seen so far, starting from Double.NEGATIVE_INFINITY.

Model's reply:
```
Label: shown
Clauses: 2
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:array_traversal@L3#8 | shown | 0.4 | 0.85 | 0.34 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| lvl:array_traversal@L2#1 | shown | 0.35 | 0.85 | 0.3 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| lvl:array_traversal@L3#6 | shown | 0.25 | 0.6 | 0.15 | c2 | max starts at 4 and keeps the biggest, 9 |

#### running_extreme, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| par:running_extreme~accumulator_pattern \| rule: Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value. |
| pre:array_traversal->running_extreme \| rule: The running maximum is found by traversing the array once, keeping the largest value seen so far (starting from Double.NEGATIVE_INFINITY). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{par:running_extreme~accumulator_pattern (Score: 1.0)}
```
Kept by pruning: par:running_extreme~accumulator_pattern (1.00)

Label prompt for concept edge par:running_extreme~accumulator_pattern (running_extreme -> accumulator_pattern, parallel):
> Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value.

Model's reply:
```
Label: confirmed
Clauses: 1, 2
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| par:running_extreme~accumulator_pattern | confirmed | 1.0 | 0.85 | 0.85 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |

#### expression, misconceptions: 8 edges offered
Edges offered:
| edge |
|---|
| err:expression->ExpressionOnLeftOfAssignment \| wrong rule: Writes a + b = c; or 7 = a; as if = were a math equation. \| right rule: The left side of an assignment must be a single variable; only the right side can be an expression. |
| mis:expression->AssignmentIsEquation \| wrong rule: An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities. \| right rule: An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable. |
| mis:expression->AssignmentNotExpression \| wrong rule: An assignment cannot be used inside a larger expression, so a condition like (x = read()) != v is not allowed. \| right rule: An assignment is an expression whose value is the value assigned, so (x = v) both stores v in x and gives v. |
| mis:expression->NoAtomicExpression \| wrong rule: A single variable x or a literal on its own is not an expression. \| right rule: A single variable or literal is an expression whose value is just that value. |
| mis:expression->OutsideInMethodNesting \| wrong rule: In f(g(x)), f runs first and then g runs. \| right rule: In f(g(x)), g(x) is evaluated first and its result is passed to f. |
| mis:expression->ParenthesesOnlyIfArgument \| wrong rule: () are optional on a no-argument call like println \| right rule: A method call always needs parentheses, so an empty line is printed with System.out.println();. |
| mis:expression->TargetTyping \| wrong rule: The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction. \| right rule: The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints. |
| mis:expression->VariablesHoldExpressions \| wrong rule: = stores the expression itself, not its computed value \| right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:expression->TargetTyping (0.60), mis:expression->AssignmentIsEquation (0.20), mis:expression->VariablesHoldExpressions (0.20)
```
Kept by pruning: mis:expression->TargetTyping (0.60), mis:expression->AssignmentIsEquation (0.20), mis:expression->VariablesHoldExpressions (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:expression->TargetTyping \| wrong rule: The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction. \| right rule: The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints. |
| mis:expression->AssignmentIsEquation \| wrong rule: An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities. \| right rule: An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable. |
| mis:expression->VariablesHoldExpressions \| wrong rule: = stores the expression itself, not its computed value \| right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y. |
Model's reply:
```
mis:expression->TargetTyping | correct | clauses: 3 | confidence: 0.7
mis:expression->AssignmentIsEquation | not applied | clauses: none | confidence: 0.9
mis:expression->VariablesHoldExpressions | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:expression->TargetTyping | correct | 0.6 | 0.7 | 0.42 | c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| mis:expression->AssignmentIsEquation | not applied |  |  | 0.0 |  |  |
| mis:expression->VariablesHoldExpressions | not applied |  |  | 0.0 |  |  |

#### expression, level ways: 19 edges offered
Edges offered:
| edge |
|---|
| lvl:expression@L0#0 \| level L0 way everyday_reading: In maths an expression such as 7/2 or x + y names an exact number, and 'expression' means a formula with operators. In Java, any code that evaluates to a typed value is an expression, including a lone literal or variable, and with ints 7/2 evaluates to 3. |
| lvl:expression@L0#2 \| level L0 way inconsistent_trace: Points to LT (replace each variable with its current value, then apply operators in precedence order). Applied unevenly, a student substitutes current values for some variables and old or future values for others, or respects precedence in one subexpression only. (here mixing in: "a single literal or variable "isn't an expression"") |
| lvl:expression@L1#0 \| level L1 way names_the_element: Expression: a literal, a variable, or a sequence of operations (operators, method calls) on them that produces one value. |
| lvl:expression@L1#1 \| level L1 way states_the_rule: Each operand of an operator can itself be any expression, and a parenthesized expression has the same value as the expression inside. Every expression has a type, determined by its operators and operands. |
| lvl:expression@L2#0 \| level L2 way line_by_line_trace: Operands are evaluated left to right, each fully before its operator is applied. Precedence and parentheses decide the grouping, and a method's arguments are all evaluated before the method is called. |
| lvl:expression@L2#1 \| level L2 way output_prediction: An expression produces one value of a type fixed by its operands: hour * 60 + minute with hour = 11 and minute = 59 is the int 719. |
| lvl:expression@L2#2 \| level L2 way one_step_execution: Evaluating an expression changes no variable unless it contains an assignment, ++/-- or a method with side effects. The value goes to the enclosing statement, and an expression statement discards it. |
| lvl:expression@L3#0 \| level L3 way relation_to_neighbour: A variable name inside an expression contributes the variable's value at the moment of evaluation. |
| lvl:expression@L3#1 \| level L3 way relation_to_neighbour: Operators combine operand values into a new value, and the operand types choose the operation (int / truncates, double / does not). |
| lvl:expression@L3#2 \| level L3 way relation_to_neighbour: With several operators, precedence and left associativity decide the grouping, and parentheses override both. |
| lvl:expression@L3#3 \| level L3 way relation_to_neighbour: A comparison takes numeric expressions and yields a boolean expression, and it has lower precedence than arithmetic, so a + b < c compares the sum. |
| lvl:expression@L3#4 \| level L3 way relation_to_neighbour: A method call is an expression usable wherever a value of its return type is, and its arguments are expressions evaluated before the call. |
| lvl:expression@L3#5 \| level L3 way purpose_of_the_whole: Expressions compute new values from existing ones. They form the right side of every assignment, every condition, every method argument and every printed value. |
| lvl:expression@L4#0 \| level L4 way predict_a_change: Adding parentheses that match the default grouping keeps the value, and rewriting with an equivalent formula (4 * (x - 3) as 4*x - 12) keeps it for ints. Changing one operand's type (3 to 3.0) can change both the result's type and its value. |
| lvl:expression@L4#1 \| level L4 way transfer_to_a_new_program: Use an expression wherever a value is needed. Split a long or unclear expression into named intermediate variables, and add parentheses wherever the grouping is not obvious. |
| lvl:expression@L4#2 \| level L4 way diagnose_an_error: rule broken: The left-hand side of = must be a single variable; only the right-hand side may be an arbitrary expression. Kind: compile-time. Trigger class: Any assignment whose left side is a literal or compound expression (7 = a; a + b = c;): 'unexpected type, required: variable'. |
| lvl:expression@L4#3 \| level L4 way diagnose_an_error: rule broken: Only assignments, increments, method calls and object creation can stand alone as statements. Kind: compile-time. Trigger class: A bare expression line such as x + 1; or a == b;: 'not a statement'. |
| lvl:expression@L4#4 \| level L4 way diagnose_an_error: rule broken: Operators accept only operands of suitable types. Kind: compile-time. Trigger class: Applying arithmetic to Strings ("Hello" - 1) or comparing booleans with <: 'bad operand types'. |
| lvl:expression@L4#5 \| level L4 way diagnose_an_error: rule broken: An int division or remainder by zero cannot be evaluated. Kind: run-time exception. Trigger class: Any int / or % whose right operand evaluates to 0: ArithmeticException. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:expression@L3#2 (Score: 0.5)}
{lvl:expression@L3#1 (Score: 0.3)}
{lvl:expression@L0#2 (Score: 0.2)}
```
Kept by pruning: lvl:expression@L3#2 (0.50), lvl:expression@L3#1 (0.30), lvl:expression@L0#2 (0.20)

Label prompt for level way lvl:expression@L3#2 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> With several operators, precedence and left associativity decide the grouping, and parentheses override both.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Label prompt for level way lvl:expression@L3#1 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Operators combine operand values into a new value, and the operand types choose the operation (int / truncates, double / does not).

Model's reply:
```
Label: shown
Clauses: 3
Confidence: 0.7
```

Label prompt for level way lvl:expression@L0#2 (the model saw only the concept, the way's name 'inconsistent trace' and its text; no level):
> Points to LT (replace each variable with its current value, then apply operators in precedence order). Applied unevenly, a student substitutes current values for some variables and old or future values for others, or respects precedence in one subexpression only. (here mixing in: "a single literal or variable "isn't an expression"")

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:expression@L3#2 | not applied |  |  | 0.0 |  |  |
| lvl:expression@L3#1 | shown | 0.3 | 0.7 | 0.21 | c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| lvl:expression@L0#2 | not applied |  |  | 0.0 |  |  |

#### arithmetic_operators, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| par:string_concatenation~arithmetic_operators \| rule: + adds when both operands are numbers and concatenates when either operand is a String, converting the other operand to a String. It is left-associative, so 1 + 2 + "3" is "33" but "1" + 2 + 3 is "123". |
| pre:arithmetic_operators->expression \| rule: An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{par:string_concatenation~arithmetic_operators (Score: 1.0)}
```
Kept by pruning: par:string_concatenation~arithmetic_operators (1.00)

Label prompt for concept edge par:string_concatenation~arithmetic_operators (string_concatenation -> arithmetic_operators, parallel):
> + adds when both operands are numbers and concatenates when either operand is a String, converting the other operand to a String. It is left-associative, so 1 + 2 + "3" is "33" but "1" + 2 + 3 is "123".

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| par:string_concatenation~arithmetic_operators | not applied |  |  | 0.0 |  |  |

#### compound_assignment, concept edges: 3 edges offered
Edges offered:
| edge |
|---|
| par:increment_operators~compound_assignment \| rule: i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, *=, /=, %=). |
| pre:assignment->compound_assignment \| rule: x op= e is shorthand for the assignment x = x op e. |
| pre:compound_assignment->accumulator_pattern \| rule: sum += x is the usual way a running total is updated on each pass. |
| pre:explicit_cast->compound_assignment \| rule: x op= e means x = (T)(x op e), where T is the type of x, so the result is cast back to the type of x. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:compound_assignment->accumulator_pattern (Score: 0.6)}
{pre:assignment->compound_assignment (Score: 0.3)}
{par:increment_operators~compound_assignment (Score: 0.1)}
```
Kept by pruning: pre:compound_assignment->accumulator_pattern (0.60), pre:assignment->compound_assignment (0.30), par:increment_operators~compound_assignment (0.10)

Label prompt for concept edge pre:compound_assignment->accumulator_pattern (compound_assignment -> accumulator_pattern, prerequisite):
> sum += x is the usual way a running total is updated on each pass.

Model's reply:
```
Label: confirmed
Clauses: 1
Confidence: 0.85
```

Label prompt for concept edge pre:assignment->compound_assignment (assignment -> compound_assignment, prerequisite):
> x op= e is shorthand for the assignment x = x op e.

Model's reply:
```
Label: confirmed
Clauses: 1
Confidence: 0.7
```

Label prompt for concept edge par:increment_operators~compound_assignment (increment_operators -> compound_assignment, parallel):
> i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, *=, /=, %=).

Model's reply:
```
Label: confirmed
Clauses: 1
Confidence: 0.55
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:compound_assignment->accumulator_pattern | confirmed | 0.6000000000000001 | 0.85 | 0.51 | c1 | sum adds every element, giving 22 |
| pre:assignment->compound_assignment | confirmed | 0.30000000000000004 | 0.7 | 0.21 | c1 | sum adds every element, giving 22 |
| par:increment_operators~compound_assignment | confirmed | 0.10000000000000002 | 0.55 | 0.06 | c1 | sum adds every element, giving 22 |

#### for_loop, concept edges: 4 edges offered
Edges offered:
| edge |
|---|
| pre:for_loop->array_traversal \| rule: for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order. |
| pre:for_loop->loop_body \| rule: The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop. |
| pre:for_loop->loop_scope \| rule: A variable declared in the for header exists only from its declaration to the end of the for statement's block. |
| pre:loop_control->for_loop \| rule: The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:for_loop->array_traversal (Score: 0.5)}
{pre:for_loop->loop_body (Score: 0.35)}
{pre:loop_control->for_loop (Score: 0.15)}
```
Kept by pruning: pre:for_loop->array_traversal (0.50), pre:for_loop->loop_body (0.35), pre:loop_control->for_loop (0.15)

Label prompt for concept edge pre:for_loop->array_traversal (for_loop -> array_traversal, prerequisite):
> for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order.

Model's reply:
```
Label: confirmed
Clauses: 1, 2
Confidence: 0.85
```

Label prompt for concept edge pre:for_loop->loop_body (for_loop -> loop_body, prerequisite):
> The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop.

Model's reply:
```
Label: confirmed
Clauses: 1, 2
Confidence: 0.8
```

Label prompt for concept edge pre:loop_control->for_loop (loop_control -> for_loop, prerequisite):
> The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.

Model's reply:
```
Label: confirmed
Clauses: 1, 2
Confidence: 0.55
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:for_loop->array_traversal | confirmed | 0.5 | 0.85 | 0.42 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| pre:for_loop->loop_body | confirmed | 0.35 | 0.8 | 0.28 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| pre:loop_control->for_loop | confirmed | 0.15 | 0.55 | 0.08 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:type_conversion->explicit_cast [broken, tier 0, 0.64], par:running_extreme~accumulator_pattern [confirmed, tier 2, 0.85], pre:compound_assignment->accumulator_pattern [confirmed, tier 2, 0.51]

reached across pre:type_conversion->explicit_cast, entered next: type_conversion

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | sum adds every element, giving 22 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| c2 | max starts at 4 and keeps the biggest, 9 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 | mis:explicit_cast->CastAppliesToWholeExpression |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of type_conversion, pre:expression->comparison_operators, pre:indexing->array_traversal, pre:length_field->array_traversal

Figure 6 (the graph after depth 3): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY16_figure06.png

### Depth 4: current concepts 'type_conversion'

#### type_conversion, misconceptions: 3 edges offered
Edges offered:
| edge |
|---|
| mis:type_conversion->NarrowingAssignmentAllowed \| wrong rule: A double value can be stored in an int variable like an int in a double. \| right rule: int to double is automatic; double to int needs a cast. |
| mis:type_conversion->NoCastIfSameSize \| wrong rule: If a variable is at least as big as a value, no cast is needed to assign the value. \| right rule: Assigning a double to an int needs a cast even when the value would fit, because a conversion that might involve loss of information leads to a compile-time error. |
| mis:type_conversion->TargetTyping \| wrong rule: The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction. \| right rule: The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:type_conversion->TargetTyping (Score: 0.8)}
{mis:type_conversion->NarrowingAssignmentAllowed (Score: 0.1)}
{mis:type_conversion->NoCastIfSameSize (Score: 0.1)}
```
Kept by pruning: mis:type_conversion->TargetTyping (0.80), mis:type_conversion->NarrowingAssignmentAllowed (0.10), mis:type_conversion->NoCastIfSameSize (0.10)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:type_conversion->TargetTyping \| wrong rule: The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction. \| right rule: The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints. |
| mis:type_conversion->NarrowingAssignmentAllowed \| wrong rule: A double value can be stored in an int variable like an int in a double. \| right rule: int to double is automatic; double to int needs a cast. |
| mis:type_conversion->NoCastIfSameSize \| wrong rule: If a variable is at least as big as a value, no cast is needed to assign the value. \| right rule: Assigning a double to an int needs a cast even when the value would fit, because a conversion that might involve loss of information leads to a compile-time error. |
Model's reply:
```
mis:type_conversion->TargetTyping | correct | clauses: 3 | confidence: 0.6
mis:type_conversion->NarrowingAssignmentAllowed | not applied | clauses: none | confidence: 0.9
mis:type_conversion->NoCastIfSameSize | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:type_conversion->TargetTyping | correct | 0.8 | 0.6 | 0.48 | c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| mis:type_conversion->NarrowingAssignmentAllowed | not applied |  |  | 0.0 |  |  |
| mis:type_conversion->NoCastIfSameSize | not applied |  |  | 0.0 |  |  |

#### type_conversion, level ways: 18 edges offered
Edges offered:
| edge |
|---|
| lvl:type_conversion@L0#0 \| level L0 way everyday_reading: Folk meaning: a number is a number, so 3, 3.0 and "3" are the same value, and a variable will take whatever form the context needs (the result 'becomes' double when stored in a double). Java rule: every value has a fixed type; conversions happen only by automatic promotion to a wider type, by an explicit cast, by conversion methods (Integer.parseInt, Math.round), or by String conversion with +. |
| lvl:type_conversion@L0#3 \| level L0 way inconsistent_trace: Points to LT (each subexpression is computed in its own type, and conversion happens only where the types meet). Applied unevenly: the student promotes before an int division on one line (treating 9/5 as 1.8) but not on another, or casts the whole expression on one pass and only the first operand on the next. (here mixing in: "If a variable is at least as big as a value, no cast is needed to assign the value") |
| lvl:type_conversion@L1#0 \| level L1 way names_the_element: Type conversion is changing a value of one type into a value of another type: automatic promotion (widening), an explicit cast, an explicit conversion method (Integer.parseInt, Double.parseDouble, Math.round), or automatic conversion to String. |
| lvl:type_conversion@L1#1 \| level L1 way states_the_rule: Java converts automatically to a type with a larger range (promotion) because no information is lost; a conversion that might lose information (double to int) requires an explicit cast or is a compile-time error; Strings and numbers convert only via methods or string conversion. |
| lvl:type_conversion@L2#0 \| level L2 way line_by_line_trace: Innermost subexpressions are evaluated in their own types first; at each binary operator the narrower operand is promoted; a cast converts the single value right after it; at an assignment the final value is converted to the variable's type (widening allowed, narrowing rejected at compile time). |
| lvl:type_conversion@L2#1 \| level L2 way output_prediction: Typical results: "1234" + 99 is the String "123499"; Integer.parseInt("123") is int 123; (int) 2.71828 is int 2; Math.round(2.71828) is long 3; 11 * 0.3 is double 3.3; 11 * (int) 0.3 is int 0; (int) (11 * 0.3) is int 3. |
| lvl:type_conversion@L2#2 \| level L2 way one_step_execution: A conversion produces a new value and never changes the source variable or its declared type: after int x = (int) pi; x is 3 and pi still holds 3.14159. |
| lvl:type_conversion@L3#0 \| level L3 way relation_to_neighbour: Conversions between primitive types follow their ranges: int to double happens automatically, double to int needs a cast that drops the fraction, and boolean converts to no numeric type. |
| lvl:type_conversion@L3#1 \| level L3 way relation_to_neighbour: Parsing methods are explicit type conversion from String to a number: a method takes an argument of one type and produces a result of another. |
| lvl:type_conversion@L3#2 \| level L3 way relation_to_neighbour: A cast is the explicit conversion between primitive types, required when information may be lost: (int) 2.71828 is 2. |
| lvl:type_conversion@L3#3 \| level L3 way relation_to_neighbour: Widening (promotion) is the automatic kind of conversion, applied at operators and assignments when the target type has a larger range. |
| lvl:type_conversion@L3#4 \| level L3 way purpose_of_the_whole: Adapts data between parts of a program: command-line text to numbers, int counts to double for an average ((double) sum / n), doubles to int indices or counts. |
| lvl:type_conversion@L4#0 \| level L4 way predict_a_change: Moving the point of conversion changes the result: (double) (a / b) differs from (double) a / b, and (int) 11 * 0.3 differs from (int) (11 * 0.3). Widening int to double and back is reversible for int values; narrowing double to int loses the fraction irreversibly. |
| lvl:type_conversion@L4#1 \| level L4 way transfer_to_a_new_program: Rely on automatic promotion when mixing int with double; write a cast only when you intend to drop information; use parse methods for text input and string conversion for output; paying attention to types avoids subtle bugs. |
| lvl:type_conversion@L4#2 \| level L4 way diagnose_an_error: rule broken: A conversion that may lose information needs an explicit cast. Kind: compile-time. Trigger class: Assigning or passing a double (or long) expression to an int, e.g. int n = 11 * 0.3; (possible loss of precision). |
| lvl:type_conversion@L4#3 \| level L4 way diagnose_an_error: rule broken: Promotion happens per operator, after an int division has already truncated. Kind: silent logic error. Trigger class: All-int division inside a double formula, e.g. double y = 1 / 3; or (9/5) * c + 32. |
| lvl:type_conversion@L4#4 \| level L4 way diagnose_an_error: rule broken: Casts work only between compatible types; a String is converted with a parse method. Kind: compile-time. Trigger class: (int) str with a String str, or (int) flag with a boolean. |
| lvl:type_conversion@L4#5 \| level L4 way diagnose_an_error: rule broken: A parse method accepts only a valid textual representation of the number. Kind: run-time exception. Trigger class: Integer.parseInt of text that is not an integer in digits ("five", "12.2", ""). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:type_conversion@L2#0 (Score: 0.45)}
{lvl:type_conversion@L4#0 (Score: 0.35)}
{lvl:type_conversion@L4#3 (Score: 0.2)}
```
Kept by pruning: lvl:type_conversion@L2#0 (0.45), lvl:type_conversion@L4#0 (0.35), lvl:type_conversion@L4#3 (0.20)

Label prompt for level way lvl:type_conversion@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Innermost subexpressions are evaluated in their own types first; at each binary operator the narrower operand is promoted; a cast converts the single value right after it; at an assignment the final value is converted to the variable's type (widening allowed, narrowing rejected at compile time).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:type_conversion@L4#0 (the model saw only the concept, the way's name 'predict a change' and its text; no level):
> Moving the point of conversion changes the result: (double) (a / b) differs from (double) a / b, and (int) 11 * 0.3 differs from (int) (11 * 0.3). Widening int to double and back is reversible for int values; narrowing double to int loses the fraction irreversibly.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:type_conversion@L4#3 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: Promotion happens per operator, after an int division has already truncated. Kind: silent logic error. Trigger class: All-int division inside a double formula, e.g. double y = 1 / 3; or (9/5) * c + 32.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:type_conversion@L2#0 | not applied |  |  | 0.0 |  |  |
| lvl:type_conversion@L4#0 | not applied |  |  | 0.0 |  |  |
| lvl:type_conversion@L4#3 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:type_conversion->TargetTyping [correct, tier 2, 0.48]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | sum adds every element, giving 22 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| c2 | max starts at 4 and keeps the biggest, 9 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 | mis:explicit_cast->CastAppliesToWholeExpression |

**Graph check, not yet read (the walk may not stop while these remain):** pre:expression->comparison_operators, pre:indexing->array_traversal, pre:length_field->array_traversal, pre:primitive_type->type_conversion

Figure 7 (the graph after depth 4): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY16_figure07.png

## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on ['explicit_cast'], broken at [] (consequences: pre:type_conversion->explicit_cast), prerequisites {'expression': ['arithmetic_operators'], 'array_initializer': ['array_declaration'], 'indexing': ['array_initializer'], 'length_field': ['array_initializer'], 'running_extreme': ['array_traversal'], 'compound_assignment': ['assignment', 'explicit_cast'], 'increment_operators': ['assignment', 'loop_control'], 'if_statement': ['boolean_expression', 'control_flow'], 'boolean_expression': ['comparison_operators'], 'accumulator_pattern': ['compound_assignment', 'loop_body'], 'array_declaration': ['data_structure'], 'data_structure': ['data_type'], 'primitive_type': ['data_type'], 'comparison_operators': ['expression'], 'array_traversal': ['for_loop', 'indexing', 'length_field'], 'loop_body': ['for_loop'], 'loop_scope': ['for_loop'], 'array_bounds': ['indexing'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable'], 'type_conversion': ['primitive_type'], 'control_flow': ['statement'], 'println': ['statement', 'string_literal'], 'string_conversion': ['string_concatenation'], 'explicit_cast': ['type_conversion']}
- accumulator_pattern: L3 via relation_to_neighbour "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
- arithmetic_operators: L2 via output_prediction "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
- array_traversal: L3 via purpose_of_the_whole "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
- compound_assignment: L3 via purpose_of_the_whole "sum adds every element, giving 22"
- explicit_cast: L0 via misconception "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
- expression: L3 via relation_to_neighbour "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
- for_loop: L3 via relation_to_neighbour "sum adds every element, giving 22"
- running_extreme: L2 via output_prediction "max starts at 4 and keeps the biggest, 9"

**Stop:** max depth at depth 4; prompts {'prune': 26, 'label': 52}, fresh model calls 19, cache hits 59

### Held misconceptions
| concept | misconception | kind | quote | score | shares_evidence_with |
|---|---|---|---|---|---|
| explicit_cast | CastAppliesToWholeExpression | misconception | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 | 0.54 |  |

### Broken concept edges
| edge | quote | score | consequence_of |
|---|---|---|---|
| pre:type_conversion->explicit_cast | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 | 0.6375 | mis:explicit_cast->CastAppliesToWholeExpression |

### Root cause: explicit_cast / CastAppliesToWholeExpression

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| accumulator_pattern | L3 | relation_to_neighbour |  | level_way | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |  | L2 output_prediction, L2 line_by_line_trace |  |
| arithmetic_operators | L2 | output_prediction |  | level_way | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |  |  |  |
| array_traversal | L3 | purpose_of_the_whole |  | level_way | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |  | L3 relation_to_neighbour, L2 output_prediction |  |
| compound_assignment | L3 | purpose_of_the_whole |  | level_way | sum adds every element, giving 22 |  | L2 output_prediction |  |
| explicit_cast | L0 | misconception | CastAppliesToWholeExpression | level_mis_links | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 | wrong rule: (int) 2.5 / 0.15 casts the whole quotient to int. Right rule: The cast applies only to what comes right after it, here 2.5, so the expression is 2 / 0.15 (a double); write (int) (2.5 / 0.15) to cast the quotient. |  |  |
| expression | L3 | relation_to_neighbour |  | level_way | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |  |  |  |
| for_loop | L3 | relation_to_neighbour |  | level_way | sum adds every element, giving 22 |  | L2 output_prediction |  |
| running_extreme | L2 | output_prediction |  | level_way | max starts at 4 and keeps the biggest, 9 |  | L2 line_by_line_trace, L1 names_the_element |  |

### Overall level: L0

Clause coverage (final):
| clause | covered by |
|---|---|
| sum adds every element, giving 22 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| max starts at 4 and keeps the biggest, 9 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 | lvl:arithmetic_operators@L2#1 |

Figure 8 (final picture): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY16_figure08.png

## 5. Every labelled edge (the evidence list, kept or not)
| depth | source | edge | kind | label | prune_score | confidence | score | clauses | quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | accumulator_pattern | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses | misconception | correct | 0.5 | 0.85 | 0.425 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 1 | accumulator_pattern | lvl:accumulator_pattern@L2#1 | level | shown | 0.45 | 0.85 | 0.3825 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 1 | accumulator_pattern | lvl:accumulator_pattern@L3#3 | level | shown | 0.35 | 0.6 | 0.21 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 1 | accumulator_pattern | lvl:accumulator_pattern@L2#0 | level | shown | 0.2 | 0.6 | 0.12 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 1 | arithmetic_operators | lvl:arithmetic_operators@L2#1 | level | shown | 0.45 | 0.6 | 0.27 | [3] | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| 1 | running_extreme | mis:running_extreme->ExtremeStartsAtZero | misconception | correct | 1.0 | 0.6 | 0.6 | [2] | max starts at 4 and keeps the biggest, 9 |
| 1 | running_extreme | lvl:running_extreme@L2#1 | level | shown | 0.4 | 0.85 | 0.34 | [2] | max starts at 4 and keeps the biggest, 9 |
| 1 | running_extreme | lvl:running_extreme@L2#0 | level | shown | 0.35 | 0.7 | 0.245 | [2] | max starts at 4 and keeps the biggest, 9 |
| 1 | running_extreme | lvl:running_extreme@L1#0 | level | shown | 0.25 | 0.93 | 0.2325 | [2] | max starts at 4 and keeps the biggest, 9 |
| 2 | accumulator_pattern | par:running_extreme~accumulator_pattern | parallel | confirmed | 0.5 | 0.85 | 0.425 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 2 | accumulator_pattern | pre:loop_body->accumulator_pattern | prerequisite | confirmed | 0.3 | 0.9 | 0.27 | [1] | sum adds every element, giving 22 |
| 2 | accumulator_pattern | pre:compound_assignment->accumulator_pattern | prerequisite | confirmed | 0.2 | 0.85 | 0.17 | [1] | sum adds every element, giving 22 |
| 2 | arithmetic_operators | pre:arithmetic_operators->expression | prerequisite | confirmed | 0.85 | 0.6 | 0.51 | [1] | sum adds every element, giving 22 |
| 2 | running_extreme | pre:array_traversal->running_extreme | prerequisite | confirmed | 1.0 | 0.85 | 0.85 | [2] | max starts at 4 and keeps the biggest, 9 |
| 2 | explicit_cast | mis:explicit_cast->CastAppliesToWholeExpression | misconception | held | 0.6000000000000001 | 0.9 | 0.54 | [3] | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| 2 | explicit_cast | mis:explicit_cast->CastAfterIntDivision | misconception | correct | 0.30000000000000004 | 0.6 | 0.18 | [3] | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| 2 | explicit_cast | lvl:explicit_cast@L0#0 | level | shown | 0.5 | 0.85 | 0.425 | [3] | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| 2 | compound_assignment | lvl:compound_assignment@L3#3 | level | shown | 0.5 | 0.75 | 0.375 | [1] | sum adds every element, giving 22 |
| 2 | compound_assignment | lvl:compound_assignment@L2#1 | level | shown | 0.25 | 0.55 | 0.1375 | [1] | sum adds every element, giving 22 |
| 2 | for_loop | mis:for_loop->ForIsConditional | misconception | correct | 0.4 | 0.9 | 0.36 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 2 | for_loop | mis:for_loop->LoopCountIsStatementCount | misconception | correct | 0.3 | 0.7 | 0.21 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 2 | for_loop | mis:for_loop->ProgramEndsAfterLoop | misconception | correct | 0.3 | 0.8 | 0.24 | [3] | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| 2 | for_loop | lvl:for_loop@L2#1 | level | shown | 0.4 | 0.8 | 0.32 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 2 | for_loop | lvl:for_loop@L3#2 | level | shown | 0.35 | 0.6 | 0.21 | [1] | sum adds every element, giving 22 |
| 3 | explicit_cast | pre:type_conversion->explicit_cast | prerequisite | broken | 0.85 | 0.75 | 0.6375 | [3] | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| 3 | array_traversal | mis:array_traversal->OffByOneBound | misconception | correct | 0.3 | 0.6 | 0.18 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 3 | array_traversal | lvl:array_traversal@L3#8 | level | shown | 0.4 | 0.85 | 0.34 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 3 | array_traversal | lvl:array_traversal@L2#1 | level | shown | 0.35 | 0.85 | 0.2975 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 3 | array_traversal | lvl:array_traversal@L3#6 | level | shown | 0.25 | 0.6 | 0.15 | [2] | max starts at 4 and keeps the biggest, 9 |
| 3 | running_extreme | par:running_extreme~accumulator_pattern | parallel | confirmed | 1.0 | 0.85 | 0.85 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 3 | expression | mis:expression->TargetTyping | misconception | correct | 0.6 | 0.7 | 0.42 | [3] | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| 3 | expression | lvl:expression@L3#1 | level | shown | 0.3 | 0.7 | 0.21 | [3] | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| 3 | compound_assignment | pre:compound_assignment->accumulator_pattern | prerequisite | confirmed | 0.6000000000000001 | 0.85 | 0.51 | [1] | sum adds every element, giving 22 |
| 3 | compound_assignment | pre:assignment->compound_assignment | prerequisite | confirmed | 0.30000000000000004 | 0.7 | 0.21 | [1] | sum adds every element, giving 22 |
| 3 | compound_assignment | par:increment_operators~compound_assignment | parallel | confirmed | 0.10000000000000002 | 0.55 | 0.055 | [1] | sum adds every element, giving 22 |
| 3 | for_loop | pre:for_loop->array_traversal | prerequisite | confirmed | 0.5 | 0.85 | 0.425 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 3 | for_loop | pre:for_loop->loop_body | prerequisite | confirmed | 0.35 | 0.8 | 0.28 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 3 | for_loop | pre:loop_control->for_loop | prerequisite | confirmed | 0.15 | 0.55 | 0.0825 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 4 | type_conversion | mis:type_conversion->TargetTyping | misconception | correct | 0.8 | 0.6 | 0.48 | [3] | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | running_extreme | mis:running_extreme->ExtremeStartsAtZero | misconception | correct | 0.6 | [2] |
| 1 | accumulator_pattern | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses | misconception | correct | 0.425 | [1, 2] |
| 1 | accumulator_pattern | lvl:accumulator_pattern@L2#1 | level | shown | 0.3825 | [1, 2] |
| 2 | explicit_cast | mis:explicit_cast->CastAppliesToWholeExpression | misconception | held | 0.54 | [3] |
| 2 | running_extreme | pre:array_traversal->running_extreme | prerequisite | confirmed | 0.85 | [2] |
| 2 | arithmetic_operators | pre:arithmetic_operators->expression | prerequisite | confirmed | 0.51 | [1] |
| 3 | explicit_cast | pre:type_conversion->explicit_cast | prerequisite | broken | 0.6375 | [3] |
| 3 | running_extreme | par:running_extreme~accumulator_pattern | parallel | confirmed | 0.85 | [1, 2] |
| 3 | compound_assignment | pre:compound_assignment->accumulator_pattern | prerequisite | confirmed | 0.51 | [1] |
| 4 | type_conversion | mis:type_conversion->TargetTyping | misconception | correct | 0.48 | [3] |

## 7. Raw traversal log
```
clauses: sum adds every element, giving 22 | max starts at 4 and keeps the biggest, 9 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0
start: generic concepts whose tagging text occurs in the answer: assignment
start: BM25 of the answer against each tagged concept: accumulator_pattern 24.23 (hits 1), arithmetic_operators 23.06 (hits 1), running_extreme 21.49 (hits 2), loop_body 18.47 (hits 1), for_loop 18.13 (hits 1), compound_assignment 17.90 (hits 1), loop_control 17.72 (hits 1), array_traversal 16.34 (hits 2), assignment 15.20 (hits 1), explicit_cast 15.12 (hits 1), type_conversion 14.88 (hits 1), string_concatenation 14.62 (hits 1), indexing 12.13 (hits 1), if_statement 12.06 (hits 1), println 11.61 (hits 1), array_declaration 11.47 (hits 1), increment_operators 10.82 (hits 1), length_field 10.75 (hits 1), loop_scope 10.70 (hits 1), loop_variable 9.28 (hits 1), control_flow 8.50 (hits 1), boolean_expression 8.24 (hits 2), comparison_operators 6.93 (hits 1), array_initializer 6.81 (hits 1), array_bounds 6.51 (hits 1), string_conversion 5.35 (hits 2), data_structure 1.64 (hits 1)
start: chosen accumulator_pattern, arithmetic_operators, running_extreme
start concepts (3): accumulator_pattern, arithmetic_operators, running_extreme
--- depth 1: current concepts ['accumulator_pattern', 'arithmetic_operators', 'running_extreme']
  accumulator_pattern (misconceptions): 4 candidates -> kept mis:accumulator_pattern->StateChangeIgnoredAcrossPasses (0.50), err:accumulator_pattern->AccumulatorDeclaredInLoop (0.25), mis:accumulator_pattern->VariableRolesInferred (0.25)
    mis:accumulator_pattern->StateChangeIgnoredAcrossPasses -> correct (0.42) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
    err:accumulator_pattern->AccumulatorDeclaredInLoop -> not applied (0.00) ""
    mis:accumulator_pattern->VariableRolesInferred -> not applied (0.00) ""
  accumulator_pattern (level ways): 17 candidates -> kept lvl:accumulator_pattern@L2#1 (0.45), lvl:accumulator_pattern@L3#3 (0.35), lvl:accumulator_pattern@L2#0 (0.20)
    lvl:accumulator_pattern@L2#1 -> shown (0.38) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
    lvl:accumulator_pattern@L3#3 -> shown (0.21) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
    lvl:accumulator_pattern@L2#0 -> shown (0.12) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
  arithmetic_operators (misconceptions): 3 candidates -> kept mis:arithmetic_operators->RemainderIsSubtraction (1.00)
    mis:arithmetic_operators->RemainderIsSubtraction -> not applied (0.00) ""
  arithmetic_operators (level ways): 18 candidates -> kept lvl:arithmetic_operators@L2#1 (0.45), lvl:arithmetic_operators@L2#0 (0.30), lvl:arithmetic_operators@L4#0 (0.25)
    lvl:arithmetic_operators@L2#1 -> shown (0.27) "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
    lvl:arithmetic_operators@L2#0 -> not applied (0.00) ""
    lvl:arithmetic_operators@L4#0 -> not applied (0.00) ""
  running_extreme (misconceptions): 1 candidates -> kept mis:running_extreme->ExtremeStartsAtZero (1.00)
    mis:running_extreme->ExtremeStartsAtZero -> correct (0.60) "max starts at 4 and keeps the biggest, 9"
  running_extreme (level ways): 14 candidates -> kept lvl:running_extreme@L2#1 (0.40), lvl:running_extreme@L2#0 (0.35), lvl:running_extreme@L1#0 (0.25)
    lvl:running_extreme@L2#1 -> shown (0.34) "max starts at 4 and keeps the biggest, 9"
    lvl:running_extreme@L2#0 -> shown (0.24) "max starts at 4 and keeps the biggest, 9"
    lvl:running_extreme@L1#0 -> shown (0.23) "max starts at 4 and keeps the biggest, 9"
  kept: mis:running_extreme->ExtremeStartsAtZero [correct, tier 2, 0.60], mis:accumulator_pattern->StateChangeIgnoredAcrossPasses [correct, tier 2, 0.42], lvl:accumulator_pattern@L2#1 [shown, tier 2, 0.38]
  clause coverage: c1 <- mis:accumulator_pattern->StateChangeIgnoredAcrossPasses; c2 <- mis:accumulator_pattern->StateChangeIgnoredAcrossPasses; c3 uncovered
  uncovered clauses bring in: explicit_cast (15.09), compound_assignment (14.25), for_loop (13.50)
  not yet read: own edges of compound_assignment, own edges of explicit_cast, own edges of for_loop, par:running_extreme~accumulator_pattern, par:string_concatenation~arithmetic_operators, pre:arithmetic_operators->expression, pre:array_traversal->running_extreme, pre:compound_assignment->accumulator_pattern, pre:loop_body->accumulator_pattern
--- depth 2: current concepts ['accumulator_pattern', 'arithmetic_operators', 'running_extreme', 'explicit_cast', 'compound_assignment', 'for_loop']
  accumulator_pattern (concept edges): 3 candidates -> kept par:running_extreme~accumulator_pattern (0.50), pre:loop_body->accumulator_pattern (0.30), pre:compound_assignment->accumulator_pattern (0.20)
    par:running_extreme~accumulator_pattern -> confirmed (0.42) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
    pre:loop_body->accumulator_pattern -> confirmed (0.27) "sum adds every element, giving 22"
    pre:compound_assignment->accumulator_pattern -> confirmed (0.17) "sum adds every element, giving 22"
  arithmetic_operators (concept edges): 2 candidates -> kept pre:arithmetic_operators->expression (0.85), par:string_concatenation~arithmetic_operators (0.15)
    pre:arithmetic_operators->expression -> confirmed (0.51) "sum adds every element, giving 22"
    par:string_concatenation~arithmetic_operators -> not applied (0.00) ""
  running_extreme (concept edges): 1 candidates -> kept pre:array_traversal->running_extreme (1.00)
    pre:array_traversal->running_extreme -> confirmed (0.85) "max starts at 4 and keeps the biggest, 9"
  explicit_cast (misconceptions): 6 candidates -> kept mis:explicit_cast->CastAppliesToWholeExpression (0.60), mis:explicit_cast->CastAfterIntDivision (0.30), mis:explicit_cast->LaterDoubleLiteralFixesDivision (0.10)
    mis:explicit_cast->CastAppliesToWholeExpression -> held (0.54) "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
    mis:explicit_cast->CastAfterIntDivision -> correct (0.18) "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
    mis:explicit_cast->LaterDoubleLiteralFixesDivision -> not applied (0.00) ""
  explicit_cast (level ways): 19 candidates -> kept lvl:explicit_cast@L0#0 (0.50), lvl:explicit_cast@L2#1 (0.30), lvl:explicit_cast@L2#0 (0.20)
    lvl:explicit_cast@L0#0 -> shown (0.42) "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
    lvl:explicit_cast@L2#1 -> not applied (0.00) ""
    lvl:explicit_cast@L2#0 -> not applied (0.00) ""
  compound_assignment (misconceptions): 2 candidates -> kept mis:compound_assignment->CompoundSubtractIsAssignNegative (0.70), mis:compound_assignment->CompoundAssignmentNoCast (0.30)
    mis:compound_assignment->CompoundSubtractIsAssignNegative -> not applied (0.00) ""
    mis:compound_assignment->CompoundAssignmentNoCast -> not applied (0.00) ""
  compound_assignment (level ways): 15 candidates -> kept lvl:compound_assignment@L3#3 (0.50), lvl:compound_assignment@L2#1 (0.25), lvl:compound_assignment@L3#0 (0.25)
    lvl:compound_assignment@L3#3 -> shown (0.38) "sum adds every element, giving 22"
    lvl:compound_assignment@L2#1 -> shown (0.14) "sum adds every element, giving 22"
    lvl:compound_assignment@L3#0 -> not applied (0.00) ""
  for_loop (misconceptions): 21 candidates -> kept mis:for_loop->ForIsConditional (0.40), mis:for_loop->LoopCountIsStatementCount (0.30), mis:for_loop->ProgramEndsAfterLoop (0.30)
    mis:for_loop->ForIsConditional -> correct (0.36) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
    mis:for_loop->LoopCountIsStatementCount -> correct (0.21) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
    mis:for_loop->ProgramEndsAfterLoop -> correct (0.24) "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
  for_loop (level ways): 24 candidates -> kept lvl:for_loop@L2#1 (0.40), lvl:for_loop@L3#2 (0.35), lvl:for_loop@L2#0 (0.25)
    lvl:for_loop@L2#1 -> shown (0.32) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
    lvl:for_loop@L3#2 -> shown (0.21) "sum adds every element, giving 22"
    lvl:for_loop@L2#0 -> not applied (0.00) ""
  kept: mis:explicit_cast->CastAppliesToWholeExpression [held, tier 0, 0.54], pre:array_traversal->running_extreme [confirmed, tier 2, 0.85], pre:arithmetic_operators->expression [confirmed, tier 2, 0.51]
  reached across pre:array_traversal->running_extreme, entered next: array_traversal
  reached across pre:arithmetic_operators->expression, entered next: expression
  clause coverage: c1 <- mis:accumulator_pattern->StateChangeIgnoredAcrossPasses; c2 <- mis:accumulator_pattern->StateChangeIgnoredAcrossPasses; c3 <- mis:explicit_cast->CastAppliesToWholeExpression
  not yet read: own edges of array_traversal, own edges of expression, par:increment_operators~compound_assignment, pre:assignment->compound_assignment, pre:explicit_cast->compound_assignment, pre:for_loop->array_traversal, pre:for_loop->loop_body, pre:for_loop->loop_scope, pre:loop_control->for_loop, pre:type_conversion->explicit_cast
--- depth 3: current concepts ['explicit_cast', 'array_traversal', 'running_extreme', 'expression', 'arithmetic_operators', 'compound_assignment', 'for_loop']
  explicit_cast (concept edges): 2 candidates -> kept pre:type_conversion->explicit_cast (0.85), pre:explicit_cast->compound_assignment (0.15)
    pre:type_conversion->explicit_cast -> broken (0.64) "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
    pre:explicit_cast->compound_assignment -> not applied (0.00) ""
  array_traversal (misconceptions): 6 candidates -> kept err:array_traversal->EarlyReturnInLoop (0.40), mis:array_traversal->OffByOneBound (0.30), mis:array_traversal->IdiomOverridesCode (0.30)
    err:array_traversal->EarlyReturnInLoop -> not applied (0.00) ""
    mis:array_traversal->OffByOneBound -> correct (0.18) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
    mis:array_traversal->IdiomOverridesCode -> not applied (0.00) ""
  array_traversal (level ways): 22 candidates -> kept lvl:array_traversal@L3#8 (0.40), lvl:array_traversal@L2#1 (0.35), lvl:array_traversal@L3#6 (0.25)
    lvl:array_traversal@L3#8 -> shown (0.34) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
    lvl:array_traversal@L2#1 -> shown (0.30) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
    lvl:array_traversal@L3#6 -> shown (0.15) "max starts at 4 and keeps the biggest, 9"
  running_extreme (concept edges): 1 candidates -> kept par:running_extreme~accumulator_pattern (1.00)
    par:running_extreme~accumulator_pattern -> confirmed (0.85) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
  expression (misconceptions): 8 candidates -> kept mis:expression->TargetTyping (0.60), mis:expression->AssignmentIsEquation (0.20), mis:expression->VariablesHoldExpressions (0.20)
    mis:expression->TargetTyping -> correct (0.42) "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
    mis:expression->AssignmentIsEquation -> not applied (0.00) ""
    mis:expression->VariablesHoldExpressions -> not applied (0.00) ""
  expression (level ways): 19 candidates -> kept lvl:expression@L3#2 (0.50), lvl:expression@L3#1 (0.30), lvl:expression@L0#2 (0.20)
    lvl:expression@L3#2 -> not applied (0.00) ""
    lvl:expression@L3#1 -> shown (0.21) "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
    lvl:expression@L0#2 -> not applied (0.00) ""
  arithmetic_operators (concept edges): 1 candidates -> kept par:string_concatenation~arithmetic_operators (1.00)
    par:string_concatenation~arithmetic_operators -> not applied (0.00) ""
  compound_assignment (concept edges): 3 candidates -> kept pre:compound_assignment->accumulator_pattern (0.60), pre:assignment->compound_assignment (0.30), par:increment_operators~compound_assignment (0.10)
    pre:compound_assignment->accumulator_pattern -> confirmed (0.51) "sum adds every element, giving 22"
    pre:assignment->compound_assignment -> confirmed (0.21) "sum adds every element, giving 22"
    par:increment_operators~compound_assignment -> confirmed (0.06) "sum adds every element, giving 22"
  for_loop (concept edges): 4 candidates -> kept pre:for_loop->array_traversal (0.50), pre:for_loop->loop_body (0.35), pre:loop_control->for_loop (0.15)
    pre:for_loop->array_traversal -> confirmed (0.42) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
    pre:for_loop->loop_body -> confirmed (0.28) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
    pre:loop_control->for_loop -> confirmed (0.08) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
  kept: pre:type_conversion->explicit_cast [broken, tier 0, 0.64], par:running_extreme~accumulator_pattern [confirmed, tier 2, 0.85], pre:compound_assignment->accumulator_pattern [confirmed, tier 2, 0.51]
  reached across pre:type_conversion->explicit_cast, entered next: type_conversion
  clause coverage: c1 <- mis:accumulator_pattern->StateChangeIgnoredAcrossPasses; c2 <- mis:accumulator_pattern->StateChangeIgnoredAcrossPasses; c3 <- mis:explicit_cast->CastAppliesToWholeExpression
  not yet read: own edges of type_conversion, pre:expression->comparison_operators, pre:indexing->array_traversal, pre:length_field->array_traversal
--- depth 4: current concepts ['type_conversion'] (closing round: own edges only)
  type_conversion (misconceptions): 3 candidates -> kept mis:type_conversion->TargetTyping (0.80), mis:type_conversion->NarrowingAssignmentAllowed (0.10), mis:type_conversion->NoCastIfSameSize (0.10)
    mis:type_conversion->TargetTyping -> correct (0.48) "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
    mis:type_conversion->NarrowingAssignmentAllowed -> not applied (0.00) ""
    mis:type_conversion->NoCastIfSameSize -> not applied (0.00) ""
  type_conversion (level ways): 18 candidates -> kept lvl:type_conversion@L2#0 (0.45), lvl:type_conversion@L4#0 (0.35), lvl:type_conversion@L4#3 (0.20)
    lvl:type_conversion@L2#0 -> not applied (0.00) ""
    lvl:type_conversion@L4#0 -> not applied (0.00) ""
    lvl:type_conversion@L4#3 -> not applied (0.00) ""
  kept: mis:type_conversion->TargetTyping [correct, tier 2, 0.48]
  clause coverage: c1 <- mis:accumulator_pattern->StateChangeIgnoredAcrossPasses; c2 <- mis:accumulator_pattern->StateChangeIgnoredAcrossPasses; c3 <- mis:explicit_cast->CastAppliesToWholeExpression
  not yet read: pre:expression->comparison_operators, pre:indexing->array_traversal, pre:length_field->array_traversal, pre:primitive_type->type_conversion
  root-cause walk: held on ['explicit_cast'], broken at [] (consequences: pre:type_conversion->explicit_cast), prerequisites {'expression': ['arithmetic_operators'], 'array_initializer': ['array_declaration'], 'indexing': ['array_initializer'], 'length_field': ['array_initializer'], 'running_extreme': ['array_traversal'], 'compound_assignment': ['assignment', 'explicit_cast'], 'increment_operators': ['assignment', 'loop_control'], 'if_statement': ['boolean_expression', 'control_flow'], 'boolean_expression': ['comparison_operators'], 'accumulator_pattern': ['compound_assignment', 'loop_body'], 'array_declaration': ['data_structure'], 'data_structure': ['data_type'], 'primitive_type': ['data_type'], 'comparison_operators': ['expression'], 'array_traversal': ['for_loop', 'indexing', 'length_field'], 'loop_body': ['for_loop'], 'loop_scope': ['for_loop'], 'array_bounds': ['indexing'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable'], 'type_conversion': ['primitive_type'], 'control_flow': ['statement'], 'println': ['statement', 'string_literal'], 'string_conversion': ['string_concatenation'], 'explicit_cast': ['type_conversion']}
  level accumulator_pattern: L3 via relation_to_neighbour "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
  level arithmetic_operators: L2 via output_prediction "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
  level array_traversal: L3 via purpose_of_the_whole "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
  level compound_assignment: L3 via purpose_of_the_whole "sum adds every element, giving 22"
  level explicit_cast: L0 via misconception "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
  level expression: L3 via relation_to_neighbour "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
  level for_loop: L3 via relation_to_neighbour "sum adds every element, giving 22"
  level running_extreme: L2 via output_prediction "max starts at 4 and keeps the biggest, 9"
```

## 8. Full diagnosis JSON
```json
{
 "scenario": "MY16",
 "settings": {
  "width": 3,
  "depth": 3,
  "prune_tools": "llm",
  "model": "claude-opus-5-5",
  "backend": "claude-cli"
 },
 "clauses": [
  "sum adds every element, giving 22",
  "max starts at 4 and keeps the biggest, 9",
  "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
 ],
 "start_concepts": [
  "accumulator_pattern",
  "arithmetic_operators",
  "running_extreme"
 ],
 "held_misconceptions": [
  {
   "concept": "explicit_cast",
   "misconception": "CastAppliesToWholeExpression",
   "kind": "misconception",
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "score": 0.54
  }
 ],
 "error_evidence": [],
 "shadowed": [],
 "broken_edges": [
  {
   "edge": "pre:type_conversion->explicit_cast",
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "score": 0.6375,
   "consequence_of": "mis:explicit_cast->CastAppliesToWholeExpression"
  }
 ],
 "root_cause": {
  "concept": "explicit_cast",
  "misconception": "CastAppliesToWholeExpression"
 },
 "levels": {
  "accumulator_pattern": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "edge": "lvl:accumulator_pattern@L3#3",
   "source": "level_way",
   "also_shown": [
    "L2 output_prediction",
    "L2 line_by_line_trace"
   ]
  },
  "arithmetic_operators": {
   "level": "L2",
   "way": "output_prediction",
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "edge": "lvl:arithmetic_operators@L2#1",
   "source": "level_way",
   "also_shown": []
  },
  "array_traversal": {
   "level": "L3",
   "way": "purpose_of_the_whole",
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "edge": "lvl:array_traversal@L3#8",
   "source": "level_way",
   "also_shown": [
    "L3 relation_to_neighbour",
    "L2 output_prediction"
   ]
  },
  "compound_assignment": {
   "level": "L3",
   "way": "purpose_of_the_whole",
   "quote": "sum adds every element, giving 22",
   "edge": "lvl:compound_assignment@L3#3",
   "source": "level_way",
   "also_shown": [
    "L2 output_prediction"
   ]
  },
  "explicit_cast": {
   "level": "L0",
   "way": "misconception",
   "misconception": "CastAppliesToWholeExpression",
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "edge": "mis:explicit_cast->CastAppliesToWholeExpression",
   "rule": "wrong rule: (int) 2.5 / 0.15 casts the whole quotient to int. Right rule: The cast applies only to what comes right after it, here 2.5, so the expression is 2 / 0.15 (a double); write (int) (2.5 / 0.15) to cast the quotient.",
   "source": "level_mis_links"
  },
  "expression": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "edge": "lvl:expression@L3#1",
   "source": "level_way",
   "also_shown": []
  },
  "for_loop": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "sum adds every element, giving 22",
   "edge": "lvl:for_loop@L3#2",
   "source": "level_way",
   "also_shown": [
    "L2 output_prediction"
   ]
  },
  "running_extreme": {
   "level": "L2",
   "way": "output_prediction",
   "quote": "max starts at 4 and keeps the biggest, 9",
   "edge": "lvl:running_extreme@L2#1",
   "source": "level_way",
   "also_shown": [
    "L2 line_by_line_trace",
    "L1 names_the_element"
   ]
  }
 },
 "overall_level": "L0",
 "paths": [
  {
   "depth": 1,
   "source": "running_extreme",
   "edge": "mis:running_extreme->ExtremeStartsAtZero",
   "target": "ExtremeStartsAtZero",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    2
   ],
   "quote": "max starts at 4 and keeps the biggest, 9",
   "confidence": 0.6,
   "prune_score": 1.0,
   "score": 0.6,
   "logic": "The running maximum can always start at 0.",
   "twin_logic": "Start the running maximum at the most negative possible value (Double.NEGATIVE_INFINITY, or the smallest int), so that the first value read replaces it.",
   "role": "primary"
  },
  {
   "depth": 1,
   "source": "accumulator_pattern",
   "edge": "mis:accumulator_pattern->StateChangeIgnoredAcrossPasses",
   "target": "StateChangeIgnoredAcrossPasses",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.85,
   "prune_score": 0.5,
   "score": 0.425,
   "logic": "Values changed by one pass of a loop (other than the loop variable) do not affect later passes.",
   "twin_logic": "Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.",
   "role": "context"
  },
  {
   "depth": 1,
   "source": "accumulator_pattern",
   "edge": "lvl:accumulator_pattern@L2#1",
   "target": "accumulator_pattern@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.85,
   "prune_score": 0.45,
   "score": 0.3825,
   "logic": "After the loop the accumulator holds the reduce result: sum of 1..N is N(N+1)/2; Harmonic(2) = 1.5; the product loop gives N!.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 2,
   "source": "explicit_cast",
   "edge": "mis:explicit_cast->CastAppliesToWholeExpression",
   "target": "CastAppliesToWholeExpression",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    3
   ],
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "confidence": 0.9,
   "prune_score": 0.6000000000000001,
   "score": 0.54,
   "logic": "(int) 2.5 / 0.15 casts the whole quotient to int.",
   "twin_logic": "The cast applies only to what comes right after it, here 2.5.",
   "role": "primary"
  },
  {
   "depth": 2,
   "source": "running_extreme",
   "edge": "pre:array_traversal->running_extreme",
   "target": "array_traversal",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    2
   ],
   "quote": "max starts at 4 and keeps the biggest, 9",
   "confidence": 0.85,
   "prune_score": 1.0,
   "score": 0.85,
   "logic": "The running maximum is found by traversing the array once, keeping the largest value seen so far (starting from Double.NEGATIVE_INFINITY).",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "arithmetic_operators",
   "edge": "pre:arithmetic_operators->expression",
   "target": "expression",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "sum adds every element, giving 22",
   "confidence": 0.6,
   "prune_score": 0.85,
   "score": 0.51,
   "logic": "An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "explicit_cast",
   "edge": "pre:type_conversion->explicit_cast",
   "target": "type_conversion",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    3
   ],
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "confidence": 0.75,
   "prune_score": 0.85,
   "score": 0.6375,
   "logic": "A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2).",
   "twin_logic": null,
   "consequence_of": "mis:explicit_cast->CastAppliesToWholeExpression"
  },
  {
   "depth": 3,
   "source": "running_extreme",
   "edge": "par:running_extreme~accumulator_pattern",
   "target": "accumulator_pattern",
   "kind": "parallel",
   "label": "confirmed",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.85,
   "prune_score": 1.0,
   "score": 0.85,
   "logic": "Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "compound_assignment",
   "edge": "pre:compound_assignment->accumulator_pattern",
   "target": "accumulator_pattern",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "sum adds every element, giving 22",
   "confidence": 0.85,
   "prune_score": 0.6000000000000001,
   "score": 0.51,
   "logic": "sum += x is the usual way a running total is updated on each pass.",
   "twin_logic": null
  },
  {
   "depth": 4,
   "source": "type_conversion",
   "edge": "mis:type_conversion->TargetTyping",
   "target": "TargetTyping",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3
   ],
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "confidence": 0.6,
   "prune_score": 0.8,
   "score": 0.48,
   "logic": "The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction.",
   "twin_logic": "The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints.",
   "role": "context"
  }
 ],
 "evidence": [
  {
   "depth": 1,
   "source": "accumulator_pattern",
   "edge": "mis:accumulator_pattern->StateChangeIgnoredAcrossPasses",
   "target": "StateChangeIgnoredAcrossPasses",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.85,
   "prune_score": 0.5,
   "score": 0.425,
   "logic": "Values changed by one pass of a loop (other than the loop variable) do not affect later passes.",
   "twin_logic": "Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones.",
   "role": "context"
  },
  {
   "depth": 1,
   "source": "accumulator_pattern",
   "edge": "lvl:accumulator_pattern@L2#1",
   "target": "accumulator_pattern@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.85,
   "prune_score": 0.45,
   "score": 0.3825,
   "logic": "After the loop the accumulator holds the reduce result: sum of 1..N is N(N+1)/2; Harmonic(2) = 1.5; the product loop gives N!.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "accumulator_pattern",
   "edge": "lvl:accumulator_pattern@L3#3",
   "target": "accumulator_pattern@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.6,
   "prune_score": 0.35,
   "score": 0.21,
   "logic": "Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 1,
   "source": "accumulator_pattern",
   "edge": "lvl:accumulator_pattern@L2#0",
   "target": "accumulator_pattern@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "Before the loop: total = initial value. Each pass: read total, combine with the current item, store back. After the loop: total holds the combination of all items.",
   "twin_logic": null,
   "level": "L2",
   "way": "line_by_line_trace"
  },
  {
   "depth": 1,
   "source": "arithmetic_operators",
   "edge": "lvl:arithmetic_operators@L2#1",
   "target": "arithmetic_operators@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3
   ],
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "confidence": 0.6,
   "prune_score": 0.45,
   "score": 0.27,
   "logic": "With ints, 17 / 3 is 5 and 17 % 3 is 2. With doubles, 5.0 / 3.0 is 1.6666666666666667. With mixed operands, the int is promoted first (10 / 3.0 is 3.333...).",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "running_extreme",
   "edge": "mis:running_extreme->ExtremeStartsAtZero",
   "target": "ExtremeStartsAtZero",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    2
   ],
   "quote": "max starts at 4 and keeps the biggest, 9",
   "confidence": 0.6,
   "prune_score": 1.0,
   "score": 0.6,
   "logic": "The running maximum can always start at 0.",
   "twin_logic": "Start the running maximum at the most negative possible value (Double.NEGATIVE_INFINITY, or the smallest int), so that the first value read replaces it.",
   "role": "primary"
  },
  {
   "depth": 1,
   "source": "running_extreme",
   "edge": "lvl:running_extreme@L2#1",
   "target": "running_extreme@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "max starts at 4 and keeps the biggest, 9",
   "confidence": 0.85,
   "prune_score": 0.4,
   "score": 0.34,
   "logic": "Result: the largest element (of the element type). For an empty array (or no input) max stays at its start value: NEGATIVE_INFINITY, or MIN_VALUE for int.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "running_extreme",
   "edge": "lvl:running_extreme@L2#0",
   "target": "running_extreme@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "max starts at 4 and keeps the biggest, 9",
   "confidence": 0.7,
   "prune_score": 0.35,
   "score": 0.245,
   "logic": "Sequencing: initialize max before the loop; in each pass evaluate a[i] > max, and if it is true assign max = a[i]; read max only after the loop ends.",
   "twin_logic": null,
   "level": "L2",
   "way": "line_by_line_trace"
  },
  {
   "depth": 1,
   "source": "running_extreme",
   "edge": "lvl:running_extreme@L1#0",
   "target": "running_extreme@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "max starts at 4 and keeps the biggest, 9",
   "confidence": 0.93,
   "prune_score": 0.25,
   "score": 0.2325,
   "logic": "Identity: a running maximum (or minimum), a variable holding the largest (smallest) value seen so far in a pass over the data; Sajaniemi's most-wanted holder.",
   "twin_logic": null,
   "level": "L1",
   "way": "names_the_element"
  },
  {
   "depth": 2,
   "source": "accumulator_pattern",
   "edge": "par:running_extreme~accumulator_pattern",
   "target": "running_extreme",
   "kind": "parallel",
   "label": "confirmed",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.85,
   "prune_score": 0.5,
   "score": 0.425,
   "logic": "Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "accumulator_pattern",
   "edge": "pre:loop_body->accumulator_pattern",
   "target": "loop_body",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "sum adds every element, giving 22",
   "confidence": 0.9,
   "prune_score": 0.3,
   "score": 0.27,
   "logic": "The accumulator update sum += x sits inside the body, so it runs once on every pass.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "accumulator_pattern",
   "edge": "pre:compound_assignment->accumulator_pattern",
   "target": "compound_assignment",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "sum adds every element, giving 22",
   "confidence": 0.85,
   "prune_score": 0.2,
   "score": 0.17,
   "logic": "sum += x is the usual way a running total is updated on each pass.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "arithmetic_operators",
   "edge": "pre:arithmetic_operators->expression",
   "target": "expression",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "sum adds every element, giving 22",
   "confidence": 0.6,
   "prune_score": 0.85,
   "score": 0.51,
   "logic": "An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "running_extreme",
   "edge": "pre:array_traversal->running_extreme",
   "target": "array_traversal",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    2
   ],
   "quote": "max starts at 4 and keeps the biggest, 9",
   "confidence": 0.85,
   "prune_score": 1.0,
   "score": 0.85,
   "logic": "The running maximum is found by traversing the array once, keeping the largest value seen so far (starting from Double.NEGATIVE_INFINITY).",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "explicit_cast",
   "edge": "mis:explicit_cast->CastAppliesToWholeExpression",
   "target": "CastAppliesToWholeExpression",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    3
   ],
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "confidence": 0.9,
   "prune_score": 0.6000000000000001,
   "score": 0.54,
   "logic": "(int) 2.5 / 0.15 casts the whole quotient to int.",
   "twin_logic": "The cast applies only to what comes right after it, here 2.5.",
   "role": "primary"
  },
  {
   "depth": 2,
   "source": "explicit_cast",
   "edge": "mis:explicit_cast->CastAfterIntDivision",
   "target": "CastAfterIntDivision",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3
   ],
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "confidence": 0.6,
   "prune_score": 0.30000000000000004,
   "score": 0.18,
   "logic": "(double) (3 / 5) is 0.6.",
   "twin_logic": "The integer division 3 / 5 = 0 happens before the cast, so the result is 0.0.",
   "role": "primary"
  },
  {
   "depth": 2,
   "source": "explicit_cast",
   "edge": "lvl:explicit_cast@L0#0",
   "target": "explicit_cast@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3
   ],
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "confidence": 0.85,
   "prune_score": 0.5,
   "score": 0.425,
   "logic": "Folk meaning: 'convert 2.7 to a whole number' means round it to 3, and (int) looks like a function label that applies to everything written after it. Java rule: a cast to int truncates toward zero ((int) 2.7 is 2) and, having higher precedence than arithmetic, applies only to the value immediately following it.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 2,
   "source": "compound_assignment",
   "edge": "lvl:compound_assignment@L3#3",
   "target": "compound_assignment@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "sum adds every element, giving 22",
   "confidence": 0.75,
   "prune_score": 0.5,
   "score": 0.375,
   "logic": "Plan/role: the update step of a gatherer (sum += a[i], product *= i) or of a stepper with a step other than 1 (i += 2).",
   "twin_logic": null,
   "level": "L3",
   "way": "purpose_of_the_whole"
  },
  {
   "depth": 2,
   "source": "compound_assignment",
   "edge": "lvl:compound_assignment@L2#1",
   "target": "compound_assignment@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "sum adds every element, giving 22",
   "confidence": 0.55,
   "prune_score": 0.25,
   "score": 0.1375,
   "logic": "The new value of x is (T)(old x op e) and is also the expression's value: each starting from int x = 7: x += 3 gives 10, x /= 2 gives 3, and x += 0.5 gives 7 (7.5 truncated) instead of a compile error.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 2,
   "source": "for_loop",
   "edge": "mis:for_loop->ForIsConditional",
   "target": "ForIsConditional",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.9,
   "prune_score": 0.4,
   "score": 0.36,
   "logic": "The body of a for statement executes at most once.",
   "twin_logic": "The body of a for statement runs once for every pass on which the condition is true, which can be many times.",
   "role": "primary"
  },
  {
   "depth": 2,
   "source": "for_loop",
   "edge": "mis:for_loop->LoopCountIsStatementCount",
   "target": "LoopCountIsStatementCount",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.7,
   "prune_score": 0.3,
   "score": 0.21,
   "logic": "The repeat count of a counted loop says how many of the body statements are executed.",
   "twin_logic": "The repeat count is how many times the whole body runs; every pass runs all body statements.",
   "role": "primary"
  },
  {
   "depth": 2,
   "source": "for_loop",
   "edge": "mis:for_loop->ProgramEndsAfterLoop",
   "target": "ProgramEndsAfterLoop",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3
   ],
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "confidence": 0.8,
   "prune_score": 0.3,
   "score": 0.24,
   "logic": "When a loop finishes the program ends, so code after the loop never runs.",
   "twin_logic": "When the loop condition becomes false, control continues with the first statement after the loop.",
   "role": "context"
  },
  {
   "depth": 2,
   "source": "for_loop",
   "edge": "lvl:for_loop@L2#1",
   "target": "for_loop@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.8,
   "prune_score": 0.4,
   "score": 0.32,
   "logic": "A for statement has no value; the passes it makes are fixed by its header: for (int i = 1; i <= N; i++) sum += i; leaves sum = N(N+1)/2, and for (int i = 2; i <= 8; i += 2) prints 2, 4, 6, 8,.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 2,
   "source": "for_loop",
   "edge": "lvl:for_loop@L3#2",
   "target": "for_loop@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "sum adds every element, giving 22",
   "confidence": 0.6,
   "prune_score": 0.35,
   "score": 0.21,
   "logic": "for (int i = 0; i < N; i++) gives i each valid index 0..N-1 exactly once in increasing order, the standard way to process every array element.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 3,
   "source": "explicit_cast",
   "edge": "pre:type_conversion->explicit_cast",
   "target": "type_conversion",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    3
   ],
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "confidence": 0.75,
   "prune_score": 0.85,
   "score": 0.6375,
   "logic": "A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2).",
   "twin_logic": null,
   "consequence_of": "mis:explicit_cast->CastAppliesToWholeExpression"
  },
  {
   "depth": 3,
   "source": "array_traversal",
   "edge": "mis:array_traversal->OffByOneBound",
   "target": "OffByOneBound",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.6,
   "prune_score": 0.3,
   "score": 0.18,
   "logic": "< vs <= and 0..n vs 0..n-1 are interchangeable",
   "twin_logic": "for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n.",
   "role": "context"
  },
  {
   "depth": 3,
   "source": "array_traversal",
   "edge": "lvl:array_traversal@L3#8",
   "target": "array_traversal@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.85,
   "prune_score": 0.4,
   "score": 0.34,
   "logic": "Plan/role: the index is a stepper, and the loop carries out a Soloway-style plan (accumulate/sum with a gatherer, count, search, find the extreme, copy) once for each element.",
   "twin_logic": null,
   "level": "L3",
   "way": "purpose_of_the_whole"
  },
  {
   "depth": 3,
   "source": "array_traversal",
   "edge": "lvl:array_traversal@L2#1",
   "target": "array_traversal@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.85,
   "prune_score": 0.35,
   "score": 0.2975,
   "logic": "Result: the body runs a.length times, and the result depends on the body. Squaring each element of {1, 2, 3, 4, 5} leaves {1, 4, 9, 16, 25}; summing leaves the total in the accumulator.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 3,
   "source": "array_traversal",
   "edge": "lvl:array_traversal@L3#6",
   "target": "array_traversal@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "max starts at 4 and keeps the biggest, 9",
   "confidence": 0.6,
   "prune_score": 0.25,
   "score": 0.15,
   "logic": "The running maximum is found in one traversal that keeps the largest value seen so far, starting from Double.NEGATIVE_INFINITY.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 3,
   "source": "running_extreme",
   "edge": "par:running_extreme~accumulator_pattern",
   "target": "accumulator_pattern",
   "kind": "parallel",
   "label": "confirmed",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.85,
   "prune_score": 1.0,
   "score": 0.85,
   "logic": "Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "mis:expression->TargetTyping",
   "target": "TargetTyping",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3
   ],
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "confidence": 0.7,
   "prune_score": 0.6,
   "score": 0.42,
   "logic": "The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction.",
   "twin_logic": "The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints.",
   "role": "context"
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "lvl:expression@L3#1",
   "target": "expression@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3
   ],
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "confidence": 0.7,
   "prune_score": 0.3,
   "score": 0.21,
   "logic": "Operators combine operand values into a new value, and the operand types choose the operation (int / truncates, double / does not).",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 3,
   "source": "compound_assignment",
   "edge": "pre:compound_assignment->accumulator_pattern",
   "target": "accumulator_pattern",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "sum adds every element, giving 22",
   "confidence": 0.85,
   "prune_score": 0.6000000000000001,
   "score": 0.51,
   "logic": "sum += x is the usual way a running total is updated on each pass.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "compound_assignment",
   "edge": "pre:assignment->compound_assignment",
   "target": "assignment",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "sum adds every element, giving 22",
   "confidence": 0.7,
   "prune_score": 0.30000000000000004,
   "score": 0.21,
   "logic": "x op= e is shorthand for the assignment x = x op e.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "compound_assignment",
   "edge": "par:increment_operators~compound_assignment",
   "target": "increment_operators",
   "kind": "parallel",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "sum adds every element, giving 22",
   "confidence": 0.55,
   "prune_score": 0.10000000000000002,
   "score": 0.055,
   "logic": "i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, *=, /=, %=).",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "for_loop",
   "edge": "pre:for_loop->array_traversal",
   "target": "array_traversal",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.85,
   "prune_score": 0.5,
   "score": 0.425,
   "logic": "for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "for_loop",
   "edge": "pre:for_loop->loop_body",
   "target": "loop_body",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.8,
   "prune_score": 0.35,
   "score": 0.28,
   "logic": "The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "for_loop",
   "edge": "pre:loop_control->for_loop",
   "target": "loop_control",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.55,
   "prune_score": 0.15,
   "score": 0.0825,
   "logic": "The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.",
   "twin_logic": null
  },
  {
   "depth": 4,
   "source": "type_conversion",
   "edge": "mis:type_conversion->TargetTyping",
   "target": "TargetTyping",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3
   ],
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "confidence": 0.6,
   "prune_score": 0.8,
   "score": 0.48,
   "logic": "The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction.",
   "twin_logic": "The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints.",
   "role": "context"
  }
 ],
 "clause_coverage": {
  "sum adds every element, giving 22": "mis:accumulator_pattern->StateChangeIgnoredAcrossPasses",
  "max starts at 4 and keeps the biggest, 9": "mis:accumulator_pattern->StateChangeIgnoredAcrossPasses",
  "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0": "lvl:arithmetic_operators@L2#1"
 },
 "unexplained_clauses": [],
 "stop_reason": "max depth",
 "depth_reached": 4,
 "llm_calls": 19,
 "llm_cache_hits": 59,
 "llm_calls_by_step": {
  "prune": 26,
  "label": 52
 }
}
```
