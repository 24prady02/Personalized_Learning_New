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
| explicit_cast | False | pattern | '(double) s' | 7 |
| expression | True | pattern | 'i < a' | 3 |
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
| type_conversion | False | pattern | '(double) s' | 7 |

G: 32 concept nodes (6 generic), 29 concept edges, 199 misconception / error edges, 141 misconception / error nodes, 160 level nodes, 225 level-misconception links, 4 connected piece(s).
Note: concept nodes form 4 pieces (the KG has no edge between them): accumulator_pattern,arithmetic_operators,array_bounds,array_traversal,assignment,boolean_expression,comparison_operators,compound_assignment,control_flow,data_structure,data_type,explicit_cast,expression,for_loop,if_statement,increment_operators,indexing,loop_body,loop_control,loop_scope,loop_variable,primitive_type,println,running_extreme,statement,string_concatenation,string_conversion,string_literal,type_conversion | array_declaration | array_initializer | length_field

Concept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):
| edge | type | rule (logic) |
|---|---|---|
| par:assignment~comparison_operators | parallel | x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands. |
| par:increment_operators~compound_assignment | parallel | i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, *=, /=, %=). |
| par:running_extreme~accumulator_pattern | parallel | Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value. |
| par:string_concatenation~arithmetic_operators | parallel | + adds when both operands are numbers and concatenates when either operand is a String, converting the other operand to a String. It is left-associative, so 1 + 2 + "3" is "33" but "1" + 2 + 3 is "123". |
| pre:arithmetic_operators->expression | prerequisite | An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones. |
| pre:array_traversal->running_extreme | prerequisite | The running maximum is found by traversing the array once, keeping the largest value seen so far (starting from Double.NEGATIVE_INFINITY). |
| pre:assignment->compound_assignment | prerequisite | x op= e is shorthand for the assignment x = x op e. |
| pre:assignment->increment_operators | prerequisite | i++ is shorthand for the assignment i = i + 1. |
| pre:boolean_expression->if_statement | prerequisite | An if runs its block only when its boolean expression evaluates to true. |
| pre:comparison_operators->boolean_expression | prerequisite | A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making. |
| pre:control_flow->if_statement | prerequisite | An if changes the default top-to-bottom flow by running a block only when its condition is true. |
| pre:data_type->data_structure | prerequisite | A data structure organizes many values of a data type; the array holds a sequence of values of one type. |
| pre:data_type->primitive_type | prerequisite | Java has eight primitive data types (boolean, char, byte, short, int, long, float, double); each, like any data type, is a set of values and a set of operations on those values. |
| pre:explicit_cast->compound_assignment | prerequisite | x op= e means x = (T)(x op e), where T is the type of x, so the result is cast back to the type of x. |
| pre:expression->comparison_operators | prerequisite | Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b. |
| pre:for_loop->array_traversal | prerequisite | for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order. |
| pre:for_loop->loop_scope | prerequisite | A variable declared in the for header exists only from its declaration to the end of the for statement's block. |
| pre:indexing->array_bounds | prerequisite | Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used. |
| pre:indexing->array_traversal | prerequisite | A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass. |
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

start: BM25 of the answer against each tagged concept: accumulator_pattern 26.16 (hits 1), arithmetic_operators 24.17 (hits 1), running_extreme 22.71 (hits 2), for_loop 19.78 (hits 1), loop_body 19.75 (hits 1), loop_control 19.42 (hits 1), array_traversal 18.05 (hits 2), assignment 16.54 (hits 1), compound_assignment 16.31 (hits 1), string_concatenation 16.16 (hits 1), explicit_cast 15.95 (hits 1), type_conversion 15.94 (hits 1), indexing 14.05 (hits 1), if_statement 13.54 (hits 1), println 12.88 (hits 1), loop_scope 12.38 (hits 1), increment_operators 12.32 (hits 1), array_declaration 11.48 (hits 1), loop_variable 10.90 (hits 1), control_flow 9.88 (hits 1), boolean_expression 9.59 (hits 2), comparison_operators 8.20 (hits 1), array_bounds 7.52 (hits 1), string_conversion 6.10 (hits 2), length_field 5.62 (hits 1), array_initializer 5.09 (hits 1), data_structure 0.35 (hits 1)

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
| c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 | lvl:arithmetic_operators@L2#1 |

**Graph check, not yet read (the walk may not stop while these remain):** par:running_extreme~accumulator_pattern, par:string_concatenation~arithmetic_operators, pre:arithmetic_operators->expression, pre:array_traversal->running_extreme, pre:loop_body->accumulator_pattern

Figure 4 (the graph after depth 1): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY16_figure04.png

### Depth 2: current concepts 'accumulator_pattern', 'arithmetic_operators', 'running_extreme'

#### accumulator_pattern, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| par:running_extreme~accumulator_pattern \| rule: Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value. |
| pre:loop_body->accumulator_pattern \| rule: The accumulator update sum += x sits inside the body, so it runs once on every pass. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{par:running_extreme~accumulator_pattern (Score: 0.6)}
{pre:loop_body->accumulator_pattern (Score: 0.4)}
```
Kept by pruning: par:running_extreme~accumulator_pattern (0.60), pre:loop_body->accumulator_pattern (0.40)

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

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| par:running_extreme~accumulator_pattern | confirmed | 0.6 | 0.85 | 0.51 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| pre:loop_body->accumulator_pattern | confirmed | 0.4 | 0.9 | 0.36 | c1 | sum adds every element, giving 22 |

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
pre:array_traversal->running_extreme (1.00)
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

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:array_traversal->running_extreme [confirmed, tier 2, 0.85], par:running_extreme~accumulator_pattern [confirmed, tier 2, 0.51], pre:arithmetic_operators->expression [confirmed, tier 2, 0.51]

reached across pre:array_traversal->running_extreme, entered next: array_traversal

reached across pre:arithmetic_operators->expression, entered next: expression

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | sum adds every element, giving 22 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| c2 | max starts at 4 and keeps the biggest, 9 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 | lvl:arithmetic_operators@L2#1 |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of array_traversal, own edges of expression

Figure 5 (the graph after depth 2): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY16_figure05.png

### Depth 3: current concepts 'array_traversal', 'running_extreme', 'accumulator_pattern', 'expression', 'arithmetic_operators'

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
err:array_traversal->EarlyReturnInLoop (0.40), mis:array_traversal->OffByOneBound (0.30), mis:array_traversal->ElementBoundToOldIndex (0.30)
```
Kept by pruning: err:array_traversal->EarlyReturnInLoop (0.40), mis:array_traversal->OffByOneBound (0.30), mis:array_traversal->ElementBoundToOldIndex (0.30)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| err:array_traversal->EarlyReturnInLoop \| wrong rule: Leaves a traversal loop with return before every element has been processed. \| right rule: A result that depends on all elements is known only after the loop ends. |
| mis:array_traversal->OffByOneBound \| wrong rule: < vs <= and 0..n vs 0..n-1 are interchangeable \| right rule: for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n. |
| mis:array_traversal->ElementBoundToOldIndex \| wrong rule: After i changes, X[i] still refers to the element at the old value of i. \| right rule: a[i] is evaluated with the current value of i each time it is used. |
Model's reply:
```
mis:array_traversal->OffByOneBound | correct | clauses: 1 | confidence: 0.6
mis:array_traversal->ElementBoundToOldIndex | correct | clauses: 1, 2 | confidence: 0.55
err:array_traversal->EarlyReturnInLoop | not applied | clauses: none | confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| err:array_traversal->EarlyReturnInLoop | not applied |  |  | 0.0 |  |  |
| mis:array_traversal->OffByOneBound | correct | 0.3 | 0.6 | 0.18 | c1 | sum adds every element, giving 22 |
| mis:array_traversal->ElementBoundToOldIndex | correct | 0.3 | 0.55 | 0.17 | c1, c2 | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |

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

#### accumulator_pattern, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| par:running_extreme~accumulator_pattern \| rule: Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value. |
| pre:loop_body->accumulator_pattern \| rule: The accumulator update sum += x sits inside the body, so it runs once on every pass. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
pre:loop_body->accumulator_pattern (1.00)
```
Kept by pruning: pre:loop_body->accumulator_pattern (1.00)

Label prompt for concept edge pre:loop_body->accumulator_pattern (loop_body -> accumulator_pattern, prerequisite):
> The accumulator update sum += x sits inside the body, so it runs once on every pass.

Model's reply:
```
Label: confirmed
Clauses: 1
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:loop_body->accumulator_pattern | confirmed | 1.0 | 0.9 | 0.9 | c1 | sum adds every element, giving 22 |

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
mis:expression->TargetTyping (0.50), mis:expression->AssignmentIsEquation (0.30), mis:expression->VariablesHoldExpressions (0.20)
```
Kept by pruning: mis:expression->TargetTyping (0.50), mis:expression->AssignmentIsEquation (0.30), mis:expression->VariablesHoldExpressions (0.20)

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
| mis:expression->TargetTyping | correct | 0.5 | 0.7 | 0.35 | c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
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

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:loop_body->accumulator_pattern [confirmed, tier 2, 0.90], mis:expression->TargetTyping [correct, tier 2, 0.35], lvl:array_traversal@L3#8 [shown, tier 2, 0.34]

reached across pre:loop_body->accumulator_pattern, entered next: loop_body

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | sum adds every element, giving 22 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| c2 | max starts at 4 and keeps the biggest, 9 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| c3 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 | lvl:arithmetic_operators@L2#1 |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of loop_body, pre:expression->comparison_operators, pre:for_loop->array_traversal, pre:indexing->array_traversal

Figure 6 (the graph after depth 3): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY16_figure06.png

## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on [], broken at [], prerequisites {'expression': ['arithmetic_operators'], 'running_extreme': ['array_traversal'], 'compound_assignment': ['assignment', 'explicit_cast'], 'increment_operators': ['assignment', 'loop_control'], 'if_statement': ['boolean_expression', 'control_flow'], 'boolean_expression': ['comparison_operators'], 'data_structure': ['data_type'], 'primitive_type': ['data_type'], 'comparison_operators': ['expression'], 'array_traversal': ['for_loop', 'indexing'], 'loop_scope': ['for_loop'], 'array_bounds': ['indexing'], 'accumulator_pattern': ['loop_body'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable'], 'type_conversion': ['primitive_type'], 'control_flow': ['statement'], 'println': ['statement', 'string_literal'], 'string_conversion': ['string_concatenation'], 'explicit_cast': ['type_conversion']}
- accumulator_pattern: L3 via relation_to_neighbour "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
- arithmetic_operators: L2 via output_prediction "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
- array_traversal: L3 via purpose_of_the_whole "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
- expression: L3 via relation_to_neighbour "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
- running_extreme: L2 via output_prediction "max starts at 4 and keeps the biggest, 9"

**Stop:** max depth at depth 3; prompts {'prune': 15, 'label': 27}, fresh model calls 0, cache hits 42

### Held misconceptions
(none)

### Broken concept edges
(none)

### Root cause: none

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| accumulator_pattern | L3 | relation_to_neighbour |  | level_way | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |  | L2 output_prediction, L2 line_by_line_trace |  |
| arithmetic_operators | L2 | output_prediction |  | level_way | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |  |  |  |
| array_traversal | L3 | purpose_of_the_whole |  | level_way | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |  | L3 relation_to_neighbour, L2 output_prediction |  |
| expression | L3 | relation_to_neighbour |  | level_way | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |  |  |  |
| running_extreme | L2 | output_prediction |  | level_way | max starts at 4 and keeps the biggest, 9 |  | L2 line_by_line_trace, L1 names_the_element |  |

### Overall level: L2

Clause coverage (final):
| clause | covered by |
|---|---|
| sum adds every element, giving 22 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| max starts at 4 and keeps the biggest, 9 | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses |
| For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 | lvl:arithmetic_operators@L2#1 |

Figure 7 (final picture): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY16_figure07.png

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
| 2 | accumulator_pattern | par:running_extreme~accumulator_pattern | parallel | confirmed | 0.6 | 0.85 | 0.51 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 2 | accumulator_pattern | pre:loop_body->accumulator_pattern | prerequisite | confirmed | 0.4 | 0.9 | 0.36 | [1] | sum adds every element, giving 22 |
| 2 | arithmetic_operators | pre:arithmetic_operators->expression | prerequisite | confirmed | 0.85 | 0.6 | 0.51 | [1] | sum adds every element, giving 22 |
| 2 | running_extreme | pre:array_traversal->running_extreme | prerequisite | confirmed | 1.0 | 0.85 | 0.85 | [2] | max starts at 4 and keeps the biggest, 9 |
| 3 | array_traversal | mis:array_traversal->OffByOneBound | misconception | correct | 0.3 | 0.6 | 0.18 | [1] | sum adds every element, giving 22 |
| 3 | array_traversal | mis:array_traversal->ElementBoundToOldIndex | misconception | correct | 0.3 | 0.55 | 0.165 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 3 | array_traversal | lvl:array_traversal@L3#8 | level | shown | 0.4 | 0.85 | 0.34 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 3 | array_traversal | lvl:array_traversal@L2#1 | level | shown | 0.35 | 0.85 | 0.2975 | [1, 2] | sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9 |
| 3 | array_traversal | lvl:array_traversal@L3#6 | level | shown | 0.25 | 0.6 | 0.15 | [2] | max starts at 4 and keeps the biggest, 9 |
| 3 | accumulator_pattern | pre:loop_body->accumulator_pattern | prerequisite | confirmed | 1.0 | 0.9 | 0.9 | [1] | sum adds every element, giving 22 |
| 3 | expression | mis:expression->TargetTyping | misconception | correct | 0.5 | 0.7 | 0.35 | [3] | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |
| 3 | expression | lvl:expression@L3#1 | level | shown | 0.3 | 0.7 | 0.21 | [3] | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0 |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | running_extreme | mis:running_extreme->ExtremeStartsAtZero | misconception | correct | 0.6 | [2] |
| 1 | accumulator_pattern | mis:accumulator_pattern->StateChangeIgnoredAcrossPasses | misconception | correct | 0.425 | [1, 2] |
| 1 | accumulator_pattern | lvl:accumulator_pattern@L2#1 | level | shown | 0.3825 | [1, 2] |
| 2 | running_extreme | pre:array_traversal->running_extreme | prerequisite | confirmed | 0.85 | [2] |
| 2 | accumulator_pattern | par:running_extreme~accumulator_pattern | parallel | confirmed | 0.51 | [1, 2] |
| 2 | arithmetic_operators | pre:arithmetic_operators->expression | prerequisite | confirmed | 0.51 | [1] |
| 3 | accumulator_pattern | pre:loop_body->accumulator_pattern | prerequisite | confirmed | 0.9 | [1] |
| 3 | expression | mis:expression->TargetTyping | misconception | correct | 0.35 | [3] |
| 3 | array_traversal | lvl:array_traversal@L3#8 | level | shown | 0.34 | [1, 2] |

## 7. Raw traversal log
```
clauses: sum adds every element, giving 22 | max starts at 4 and keeps the biggest, 9 | For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0
start: generic concepts whose tagging text occurs in the answer: assignment
start: BM25 of the answer against each tagged concept: accumulator_pattern 26.16 (hits 1), arithmetic_operators 24.17 (hits 1), running_extreme 22.71 (hits 2), for_loop 19.78 (hits 1), loop_body 19.75 (hits 1), loop_control 19.42 (hits 1), array_traversal 18.05 (hits 2), assignment 16.54 (hits 1), compound_assignment 16.31 (hits 1), string_concatenation 16.16 (hits 1), explicit_cast 15.95 (hits 1), type_conversion 15.94 (hits 1), indexing 14.05 (hits 1), if_statement 13.54 (hits 1), println 12.88 (hits 1), loop_scope 12.38 (hits 1), increment_operators 12.32 (hits 1), array_declaration 11.48 (hits 1), loop_variable 10.90 (hits 1), control_flow 9.88 (hits 1), boolean_expression 9.59 (hits 2), comparison_operators 8.20 (hits 1), array_bounds 7.52 (hits 1), string_conversion 6.10 (hits 2), length_field 5.62 (hits 1), array_initializer 5.09 (hits 1), data_structure 0.35 (hits 1)
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
  clause coverage: c1 <- mis:accumulator_pattern->StateChangeIgnoredAcrossPasses; c2 <- mis:accumulator_pattern->StateChangeIgnoredAcrossPasses; c3 <- lvl:arithmetic_operators@L2#1
  not yet read: par:running_extreme~accumulator_pattern, par:string_concatenation~arithmetic_operators, pre:arithmetic_operators->expression, pre:array_traversal->running_extreme, pre:loop_body->accumulator_pattern
--- depth 2: current concepts ['accumulator_pattern', 'arithmetic_operators', 'running_extreme']
  accumulator_pattern (concept edges): 2 candidates -> kept par:running_extreme~accumulator_pattern (0.60), pre:loop_body->accumulator_pattern (0.40)
    par:running_extreme~accumulator_pattern -> confirmed (0.51) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
    pre:loop_body->accumulator_pattern -> confirmed (0.36) "sum adds every element, giving 22"
  arithmetic_operators (concept edges): 2 candidates -> kept pre:arithmetic_operators->expression (0.85), par:string_concatenation~arithmetic_operators (0.15)
    pre:arithmetic_operators->expression -> confirmed (0.51) "sum adds every element, giving 22"
    par:string_concatenation~arithmetic_operators -> not applied (0.00) ""
  running_extreme (concept edges): 1 candidates -> kept pre:array_traversal->running_extreme (1.00)
    pre:array_traversal->running_extreme -> confirmed (0.85) "max starts at 4 and keeps the biggest, 9"
  kept: pre:array_traversal->running_extreme [confirmed, tier 2, 0.85], par:running_extreme~accumulator_pattern [confirmed, tier 2, 0.51], pre:arithmetic_operators->expression [confirmed, tier 2, 0.51]
  reached across pre:array_traversal->running_extreme, entered next: array_traversal
  reached across pre:arithmetic_operators->expression, entered next: expression
  clause coverage: c1 <- mis:accumulator_pattern->StateChangeIgnoredAcrossPasses; c2 <- mis:accumulator_pattern->StateChangeIgnoredAcrossPasses; c3 <- lvl:arithmetic_operators@L2#1
  not yet read: own edges of array_traversal, own edges of expression
--- depth 3: current concepts ['array_traversal', 'running_extreme', 'accumulator_pattern', 'expression', 'arithmetic_operators']
  array_traversal (misconceptions): 6 candidates -> kept err:array_traversal->EarlyReturnInLoop (0.40), mis:array_traversal->OffByOneBound (0.30), mis:array_traversal->ElementBoundToOldIndex (0.30)
    err:array_traversal->EarlyReturnInLoop -> not applied (0.00) ""
    mis:array_traversal->OffByOneBound -> correct (0.18) "sum adds every element, giving 22"
    mis:array_traversal->ElementBoundToOldIndex -> correct (0.17) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
  array_traversal (level ways): 22 candidates -> kept lvl:array_traversal@L3#8 (0.40), lvl:array_traversal@L2#1 (0.35), lvl:array_traversal@L3#6 (0.25)
    lvl:array_traversal@L3#8 -> shown (0.34) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
    lvl:array_traversal@L2#1 -> shown (0.30) "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
    lvl:array_traversal@L3#6 -> shown (0.15) "max starts at 4 and keeps the biggest, 9"
  accumulator_pattern (concept edges): 1 candidates -> kept pre:loop_body->accumulator_pattern (1.00)
    pre:loop_body->accumulator_pattern -> confirmed (0.90) "sum adds every element, giving 22"
  expression (misconceptions): 8 candidates -> kept mis:expression->TargetTyping (0.50), mis:expression->AssignmentIsEquation (0.30), mis:expression->VariablesHoldExpressions (0.20)
    mis:expression->TargetTyping -> correct (0.35) "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
    mis:expression->AssignmentIsEquation -> not applied (0.00) ""
    mis:expression->VariablesHoldExpressions -> not applied (0.00) ""
  expression (level ways): 19 candidates -> kept lvl:expression@L3#2 (0.50), lvl:expression@L3#1 (0.30), lvl:expression@L0#2 (0.20)
    lvl:expression@L3#2 -> not applied (0.00) ""
    lvl:expression@L3#1 -> shown (0.21) "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
    lvl:expression@L0#2 -> not applied (0.00) ""
  arithmetic_operators (concept edges): 1 candidates -> kept par:string_concatenation~arithmetic_operators (1.00)
    par:string_concatenation~arithmetic_operators -> not applied (0.00) ""
  kept: pre:loop_body->accumulator_pattern [confirmed, tier 2, 0.90], mis:expression->TargetTyping [correct, tier 2, 0.35], lvl:array_traversal@L3#8 [shown, tier 2, 0.34]
  reached across pre:loop_body->accumulator_pattern, entered next: loop_body
  clause coverage: c1 <- mis:accumulator_pattern->StateChangeIgnoredAcrossPasses; c2 <- mis:accumulator_pattern->StateChangeIgnoredAcrossPasses; c3 <- lvl:arithmetic_operators@L2#1
  not yet read: own edges of loop_body, pre:expression->comparison_operators, pre:for_loop->array_traversal, pre:indexing->array_traversal
  root-cause walk: held on [], broken at [], prerequisites {'expression': ['arithmetic_operators'], 'running_extreme': ['array_traversal'], 'compound_assignment': ['assignment', 'explicit_cast'], 'increment_operators': ['assignment', 'loop_control'], 'if_statement': ['boolean_expression', 'control_flow'], 'boolean_expression': ['comparison_operators'], 'data_structure': ['data_type'], 'primitive_type': ['data_type'], 'comparison_operators': ['expression'], 'array_traversal': ['for_loop', 'indexing'], 'loop_scope': ['for_loop'], 'array_bounds': ['indexing'], 'accumulator_pattern': ['loop_body'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable'], 'type_conversion': ['primitive_type'], 'control_flow': ['statement'], 'println': ['statement', 'string_literal'], 'string_conversion': ['string_concatenation'], 'explicit_cast': ['type_conversion']}
  level accumulator_pattern: L3 via relation_to_neighbour "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
  level arithmetic_operators: L2 via output_prediction "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
  level array_traversal: L3 via purpose_of_the_whole "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9"
  level expression: L3 via relation_to_neighbour "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0"
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
 "held_misconceptions": [],
 "error_evidence": [],
 "broken_edges": [],
 "root_cause": null,
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
  "expression": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0",
   "edge": "lvl:expression@L3#1",
   "source": "level_way",
   "also_shown": []
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
 "overall_level": "L2",
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
   "twin_logic": "Start the running maximum at the most negative possible value (Double.NEGATIVE_INFINITY, or the smallest int), so that the first value read replaces it."
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
   "twin_logic": "Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones."
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
   "prune_score": 0.6,
   "score": 0.51,
   "logic": "Both make one pass over the values with one variable kept across passes. An accumulator (gatherer role) combines every value into it (sum += a[i]), so it starts at the identity 0.0; a running extreme (most-wanted holder) replaces it only when a better value is found (if (a[i] > max) max = a[i]), so it starts at Double.NEGATIVE_INFINITY or the first value.",
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
   "prune_score": 1.0,
   "score": 0.9,
   "logic": "The accumulator update sum += x sits inside the body, so it runs once on every pass.",
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
   "prune_score": 0.5,
   "score": 0.35,
   "logic": "The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction.",
   "twin_logic": "The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints."
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
   "twin_logic": "Each pass starts from the state left by the previous pass, so a change in one pass carries into the next ones."
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
   "twin_logic": "Start the running maximum at the most negative possible value (Double.NEGATIVE_INFINITY, or the smallest int), so that the first value read replaces it."
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
   "prune_score": 0.6,
   "score": 0.51,
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
   "prune_score": 0.4,
   "score": 0.36,
   "logic": "The accumulator update sum += x sits inside the body, so it runs once on every pass.",
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
   "depth": 3,
   "source": "array_traversal",
   "edge": "mis:array_traversal->OffByOneBound",
   "target": "OffByOneBound",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1
   ],
   "quote": "sum adds every element, giving 22",
   "confidence": 0.6,
   "prune_score": 0.3,
   "score": 0.18,
   "logic": "< vs <= and 0..n vs 0..n-1 are interchangeable",
   "twin_logic": "for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n."
  },
  {
   "depth": 3,
   "source": "array_traversal",
   "edge": "mis:array_traversal->ElementBoundToOldIndex",
   "target": "ElementBoundToOldIndex",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    2
   ],
   "quote": "sum adds every element, giving 22; max starts at 4 and keeps the biggest, 9",
   "confidence": 0.55,
   "prune_score": 0.3,
   "score": 0.165,
   "logic": "After i changes, X[i] still refers to the element at the old value of i.",
   "twin_logic": "a[i] is evaluated with the current value of i each time it is used."
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
   "prune_score": 1.0,
   "score": 0.9,
   "logic": "The accumulator update sum += x sits inside the body, so it runs once on every pass.",
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
   "prune_score": 0.5,
   "score": 0.35,
   "logic": "The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction.",
   "twin_logic": "The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints."
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
  }
 ],
 "clause_coverage": {
  "sum adds every element, giving 22": "mis:accumulator_pattern->StateChangeIgnoredAcrossPasses",
  "max starts at 4 and keeps the biggest, 9": "mis:accumulator_pattern->StateChangeIgnoredAcrossPasses",
  "For avg, sum / a.length is divided first as ints, 22 / 4 = 5, and then the (double) makes it 5.0": "lvl:arithmetic_operators@L2#1"
 },
 "unexplained_clauses": [],
 "stop_reason": "max depth",
 "depth_reached": 3,
 "llm_calls": 0,
 "llm_cache_hits": 42,
 "llm_calls_by_step": {
  "prune": 15,
  "label": 27
 }
}
```
