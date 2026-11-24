# Think on the Graph: every output of the run MY40
## 0. Input
Program:
```java
double[] p = {0.2, 0.5, 0.3};
int[] freq = new int[3];
for (int t = 0; t < 10; t++) {
    double r = Math.random();
    double sum = 0.0;
    int j = 0;
    while (r >= sum + p[j]) {
        sum += p[j];
        j++;
    }
    freq[j]++;
}
System.out.println(freq[1]);
```
Question: What does the program print, and why?

Student's answer: 5. Page 1 has probability 0.5, so in 10 steps the surfer goes there exactly 5 times.”
Settings: width 3, depth 3, prune llm, backend claude-cli, model claude-opus-5-5
## 1. Stage 1: the subgraph G from the code (no model)
Masked code (string and char literals and comments blanked; this is what the patterns see):
```
double[] p = {0.2, 0.5, 0.3};
int[] freq = new int[3];
for (int t = 0; t < 10; t++) {
    double r = Math.random();
    double sum = 0.0;
    int j = 0;
    while (r >= sum + p[j]) {
        sum += p[j];
        j++;
    }
    freq[j]++;
}
System.out.println(freq[1]);
```
Which code text tagged which concept (a generic concept fires on almost any Java line; it starts the walk only if the answer repeats its tag):
| concept | generic | channel | matched text | line |
|---|---|---|---|---|
| accumulator_pattern | False | pattern | 'sum += p[j];' | 8 |
| api | False | pattern | 'Math.random(' | 4 |
| arithmetic_operators | False | pattern | 'm + p' | 7 |
| array_creation | False | pattern | 'new int[' | 2 |
| array_declaration | False | pattern | 'double[] p' | 1 |
| array_default_values | False | pattern | 'new int[3];' | 2 |
| array_initializer | False | pattern | '= {' | 1 |
| assignment | True | pattern | '=' | 1 |
| boolean_expression | False | pattern | 'while (' | 7 |
| boolean_expression | False | pattern | 'for (int t = 0; t < 10;' | 3 |
| comparison_operators | False | pattern | 'for (int t = 0; t <' | 3 |
| compound_assignment | False | pattern | '+=' | 8 |
| control_flow | False | pattern | 'for (' | 3 |
| counter_pattern | False | pattern | ']++' | 11 |
| data_structure | False | pattern | 'double[]' | 1 |
| data_type | True | pattern | 'double' | 1 |
| expression | True | pattern | 't <' | 3 |
| expression | True | pattern | '= {0.2, 0.5, 0.3};' | 1 |
| for_loop | False | pattern | 'for (' | 3 |
| frequency_counting | False | pattern | 'freq[j]++' | 11 |
| frequency_counting | False | pattern | 'freq[j]++' | 11 |
| increment_operators | False | pattern | '++' | 3 |
| indexing | False | pattern | 't[3]' | 2 |
| loop_body | False | pattern | 'for (' | 3 |
| loop_control | False | pattern | 'while (r >=' | 7 |
| loop_control | False | signal | 'for (int t = 0; t < 10; t++)' | 3 |
| loop_scope | False | pattern | 'for (int t' | 3 |
| loop_variable | False | pattern | 'for (int t =' | 3 |
| math_library | False | pattern | 'Math.random' | 4 |
| math_random | False | pattern | 'Math.random(' | 4 |
| method_call | False | pattern | 'Math.random(' | 4 |
| nested_loops | False | signal | 'for (int t = 0; t < 10; t++) {\n    double r = Math.random();\n    double sum = 0.0;\n    int j = 0;\n    while (' | 3 |
| println | False | pattern | 'System.out.println(' | 13 |
| statement | True | pattern | ';' | 1 |
| while_loop | False | pattern | '    while (' | 7 |

G: 31 concept nodes (4 generic), 37 concept edges, 205 misconception / error edges, 143 misconception / error nodes, 155 level nodes, 221 level-misconception links, 3 connected piece(s).
Note: concept nodes form 3 pieces (the KG has no edge between them): accumulator_pattern,api,arithmetic_operators,assignment,boolean_expression,comparison_operators,compound_assignment,counter_pattern,expression,for_loop,frequency_counting,increment_operators,loop_body,loop_control,loop_scope,loop_variable,math_library,math_random,method_call,nested_loops,while_loop | array_creation,array_declaration,array_default_values,array_initializer,data_structure,data_type,indexing | control_flow,println,statement

Concept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):
| edge | type | rule (logic) |
|---|---|---|
| par:accumulator_pattern~counter_pattern | parallel | An accumulator adds the current value itself on each pass (sum += x); a counter adds 1 on each pass that matches (count++). |
| par:assignment~comparison_operators | parallel | x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands. |
| par:increment_operators~compound_assignment | parallel | i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, *=, /=, %=). |
| pre:arithmetic_operators->expression | prerequisite | An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones. |
| pre:array_creation->array_default_values | prerequisite | new fills every slot with the type's default value: 0, 0.0, false or null. |
| pre:array_creation->array_initializer | prerequisite | {v0, v1, ..., vk} is a shorthand that creates an array of length k + 1 and fills it in one step. |
| pre:array_creation->indexing | prerequisite | An array must be created with new before any of its elements a[i] can be accessed. |
| pre:array_declaration->array_creation | prerequisite | double[] a; declares the array name and type; a = new double[N]; then creates the array. |
| pre:array_declaration->array_initializer | prerequisite | int[] a = {1, 2, 3}; declares the array variable and creates and fills the array in one statement. |
| pre:array_initializer->indexing | prerequisite | The values listed in braces are stored at indices 0, 1, 2, ... in order, and a[i] reads the value at index i. |
| pre:assignment->compound_assignment | prerequisite | x op= e is shorthand for the assignment x = x op e. |
| pre:assignment->increment_operators | prerequisite | i++ is shorthand for the assignment i = i + 1. |
| pre:boolean_expression->while_loop | prerequisite | A while tests its boolean condition before every pass and stops the first time it evaluates to false. |
| pre:comparison_operators->boolean_expression | prerequisite | A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making. |
| pre:compound_assignment->accumulator_pattern | prerequisite | sum += x is the usual way a running total is updated on each pass. |
| pre:counter_pattern->frequency_counting | prerequisite | Frequency counting keeps one counter per value in an array, freq[page]++. |
| pre:data_structure->array_declaration | prerequisite | An array is a data structure: one name for a sequence of values of the same type, organised by index. |
| pre:data_type->data_structure | prerequisite | A data structure organizes many values of a data type; the array holds a sequence of values of one type. |
| pre:expression->comparison_operators | prerequisite | Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b. |
| pre:expression->method_call | prerequisite | Method arguments may be expressions, and a method call can be used in expressions in the same way as variables and literals. |
| pre:for_loop->loop_body | prerequisite | The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop. |
| pre:for_loop->loop_scope | prerequisite | A variable declared in the for header exists only from its declaration to the end of the for statement's block. |
| pre:for_loop->nested_loops | prerequisite | In nested loops the inner for runs its complete set of passes for every single pass of the outer for. |
| pre:increment_operators->counter_pattern | prerequisite | A counter is updated with count++, adding one on each pass that matches. |
| pre:loop_body->accumulator_pattern | prerequisite | The accumulator update sum += x sits inside the body, so it runs once on every pass. |
| pre:loop_body->counter_pattern | prerequisite | count++ sits inside the body, usually under an if, so it runs once on every pass that matches. |
| pre:loop_control->for_loop | prerequisite | The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |
| pre:loop_control->increment_operators | prerequisite | The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update. |
| pre:loop_variable->loop_control | prerequisite | The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |
| pre:math_library->math_random | prerequisite | Math.random() is a Math library method; unlike the others it takes no argument and returns a random double in [0, 1). |
| pre:method_call->api | prerequisite | An API lists, for each library method, the signature you need in order to call it: name, argument types and return type. |
| pre:method_call->math_library | prerequisite | Math.sqrt(x) and other Math methods are used through method calls. |
| pre:statement->control_flow | prerequisite | Control flow is the order in which statements run. |
| pre:statement->println | prerequisite | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |
| pre:while_loop->loop_body | prerequisite | The loop body is the block of statements that a while (or for) loop repeats on each pass. |
| pre:while_loop->loop_control | prerequisite | A while loop has the same three control parts as a for loop, written in other places: the index set before the loop, the loop-continuation condition in the header, and the update as the last statement of the body. |
| pre:while_loop->loop_variable | prerequisite | A loop variable is a counter that the loop initializes, tests in its condition and increments on each pass. |

Misconception / error edges per concept (count), and level ways per concept (count):
| concept | misconception / error edges | level ways (L1-L4 + L0 non-misconception) |
|---|---|---|
| accumulator_pattern | 4 | 17 |
| api | 0 | 12 |
| arithmetic_operators | 3 | 18 |
| array_creation | 9 | 21 |
| array_declaration | 4 | 13 |
| array_default_values | 2 | 15 |
| array_initializer | 2 | 14 |
| assignment | 15 | 24 |
| boolean_expression | 8 | 19 |
| comparison_operators | 8 | 20 |
| compound_assignment | 2 | 15 |
| control_flow | 11 | 15 |
| counter_pattern | 2 | 16 |
| data_structure | 0 | 11 |
| data_type | 2 | 14 |
| expression | 8 | 19 |
| for_loop | 21 | 24 |
| frequency_counting | 2 | 14 |
| increment_operators | 5 | 16 |
| indexing | 8 | 21 |
| loop_body | 12 | 14 |
| loop_control | 11 | 19 |
| loop_scope | 5 | 14 |
| loop_variable | 7 | 13 |
| math_library | 4 | 20 |
| math_random | 2 | 16 |
| method_call | 10 | 17 |
| nested_loops | 8 | 17 |
| println | 6 | 17 |
| statement | 5 | 19 |
| while_loop | 19 | 24 |

Figure 1: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY40_figure01.png

Figure 2: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY40_figure02.png

## 2. Clauses and start concepts (no model)
The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):
| clause | text |
|---|---|
| c1 | 5 |
| c2 | Page 1 has probability 0.5 |
| c3 | so in 10 steps the surfer goes there exactly 5 times |

start: BM25 of the answer against each tagged concept: arithmetic_operators 19.30 (hits 1), compound_assignment 14.54 (hits 1), println 11.79 (hits 1), math_random 10.79 (hits 1), loop_control 9.63 (hits 2), frequency_counting 8.63 (hits 2), for_loop 8.20 (hits 1), loop_variable 6.98 (hits 1), loop_body 6.45 (hits 1), increment_operators 6.10 (hits 1), while_loop 5.24 (hits 1), array_creation 4.70 (hits 1), counter_pattern 4.52 (hits 1), indexing 4.30 (hits 1), boolean_expression 3.63 (hits 2), nested_loops 3.40 (hits 1), control_flow 3.31 (hits 1), method_call 3.30 (hits 1), array_initializer 2.67 (hits 1), math_library 2.36 (hits 1), loop_scope 2.15 (hits 1), array_default_values 2.12 (hits 1), accumulator_pattern 1.56 (hits 1), array_declaration 1.18 (hits 1), comparison_operators 0.72 (hits 1), api 0.46 (hits 1), data_structure 0.17 (hits 1)

start: chosen arithmetic_operators, compound_assignment, println

start concepts (3): arithmetic_operators, compound_assignment, println

Start concepts: arithmetic_operators, compound_assignment, println

Figure 3: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY40_figure03.png

## 3. The walk, depth by depth
At each depth, for each current concept: the edges offered (a concept entering as a start concept offers its misconception / error edges and its level ways, as two families; otherwise it offers its concept edges), the prune prompt and the model's reply, then the label prompt(s) and the model's reply, parsed into label / clauses / confidence. Score = prune score x confidence.

### Depth 1: current concepts 'arithmetic_operators', 'compound_assignment', 'println'

#### arithmetic_operators, misconceptions: 3 edges offered
Edges offered:
| edge |
|---|
| mis:arithmetic_operators->ArithmeticOnNumericStrings \| wrong rule: "10" - 1 or "6" * "2" works because the strings look like numbers. \| right rule: Arithmetic operators other than + are not defined for Strings; a String of digits must first be converted to a number, e.g. with Integer.parseInt. |
| mis:arithmetic_operators->CaretIsPower \| wrong rule: a^2 computes a squared. \| right rule: Java has no exponent operator; ^ is exclusive or, and a * a or Math.pow(a, 2) computes a squared. |
| mis:arithmetic_operators->RemainderIsSubtraction \| wrong rule: 9 % 5 means 9 minus 5 (a % b subtracts b from a). \| right rule: % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 * 5 + 4, and 17 % 5 is 2, not 12. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:arithmetic_operators->RemainderIsSubtraction (0.34), mis:arithmetic_operators->CaretIsPower (0.33), mis:arithmetic_operators->ArithmeticOnNumericStrings (0.33)
```
Kept by pruning: mis:arithmetic_operators->RemainderIsSubtraction (0.34), mis:arithmetic_operators->CaretIsPower (0.33), mis:arithmetic_operators->ArithmeticOnNumericStrings (0.33)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:arithmetic_operators->RemainderIsSubtraction \| wrong rule: 9 % 5 means 9 minus 5 (a % b subtracts b from a). \| right rule: % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 * 5 + 4, and 17 % 5 is 2, not 12. |
| mis:arithmetic_operators->CaretIsPower \| wrong rule: a^2 computes a squared. \| right rule: Java has no exponent operator; ^ is exclusive or, and a * a or Math.pow(a, 2) computes a squared. |
| mis:arithmetic_operators->ArithmeticOnNumericStrings \| wrong rule: "10" - 1 or "6" * "2" works because the strings look like numbers. \| right rule: Arithmetic operators other than + are not defined for Strings; a String of digits must first be converted to a number, e.g. with Integer.parseInt. |
Model's reply:
```
mis:arithmetic_operators->RemainderIsSubtraction | not applied | clauses: none | confidence: 0.95
mis:arithmetic_operators->CaretIsPower | not applied | clauses: none | confidence: 0.95
mis:arithmetic_operators->ArithmeticOnNumericStrings | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:arithmetic_operators->RemainderIsSubtraction | not applied |  |  | 0.0 |  |  |
| mis:arithmetic_operators->CaretIsPower | not applied |  |  | 0.0 |  |  |
| mis:arithmetic_operators->ArithmeticOnNumericStrings | not applied |  |  | 0.0 |  |  |

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
{lvl:arithmetic_operators@L3#4 (Score: 0.4)}
{lvl:arithmetic_operators@L2#1 (Score: 0.35)}
{lvl:arithmetic_operators@L0#0 (Score: 0.25)}
```
Kept by pruning: lvl:arithmetic_operators@L3#4 (0.40), lvl:arithmetic_operators@L2#1 (0.35), lvl:arithmetic_operators@L0#0 (0.25)

Label prompt for level way lvl:arithmetic_operators@L3#4 (the model saw the concept, the way's name 'purpose of the whole', its text, where the way stops and whether the words must be correct; no level):
> Arithmetic operators turn formulas into code: totals, averages, unit conversions (inch * CM_PER_INCH), and digit extraction (n % 10, n / 10).
>
> Where this way stops: Narrating the lines is L2. A purpose induced from a few traced cases is L2. A wrong purpose is still L3, but with an error.

Model's reply:
```
Label: wrong
Clauses: 2, 3
Confidence: 0.6
```

Label prompt for level way lvl:arithmetic_operators@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> With ints, 17 / 3 is 5 and 17 % 3 is 2. With doubles, 5.0 / 3.0 is 1.6666666666666667. With mixed operands, the int is promoted first (10 / 3.0 is 3.333...).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.8
```

Label prompt for level way lvl:arithmetic_operators@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> In maths notation, multiplication can be implicit (2x), ^ or a superscript means a power, ÷ is exact division, and % means percent. In Java * must be written, / depends on the operand types, % is the remainder, and there is no power operator (^ is exclusive or).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Parsed labels:
(none)

#### compound_assignment, misconceptions: 2 edges offered
Edges offered:
| edge |
|---|
| mis:compound_assignment->CompoundAssignmentNoCast \| wrong rule: x += 0.5 adds one half to an int x. \| right rule: x += 0.5 is x = (int) (x + 0.5), so an int x does not change. |
| mis:compound_assignment->CompoundSubtractIsAssignNegative \| wrong rule: x[i] -= y sets x[i] to -y (reads -= as assignment of a negated value). \| right rule: x[i] -= y means x[i] = x[i] - y: it subtracts y from the current value. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:compound_assignment->CompoundAssignmentNoCast (Score: 0.5)}
{mis:compound_assignment->CompoundSubtractIsAssignNegative (Score: 0.5)}
```
Kept by pruning: mis:compound_assignment->CompoundAssignmentNoCast (0.50), mis:compound_assignment->CompoundSubtractIsAssignNegative (0.50)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:compound_assignment->CompoundAssignmentNoCast \| wrong rule: x += 0.5 adds one half to an int x. \| right rule: x += 0.5 is x = (int) (x + 0.5), so an int x does not change. |
| mis:compound_assignment->CompoundSubtractIsAssignNegative \| wrong rule: x[i] -= y sets x[i] to -y (reads -= as assignment of a negated value). \| right rule: x[i] -= y means x[i] = x[i] - y: it subtracts y from the current value. |
Model's reply:
```
mis:compound_assignment->CompoundAssignmentNoCast | not applied | clauses: none | confidence: 0.9
mis:compound_assignment->CompoundSubtractIsAssignNegative | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:compound_assignment->CompoundAssignmentNoCast | not applied |  |  | 0.0 |  |  |
| mis:compound_assignment->CompoundSubtractIsAssignNegative | not applied |  |  | 0.0 |  |  |

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
{lvl:compound_assignment@L0#0 (Score: 0.4)}
{lvl:compound_assignment@L3#3 (Score: 0.35)}
{lvl:compound_assignment@L2#1 (Score: 0.25)}
```
Kept by pruning: lvl:compound_assignment@L0#0 (0.40), lvl:compound_assignment@L3#3 (0.35), lvl:compound_assignment@L2#1 (0.25)

Label prompt for level way lvl:compound_assignment@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: x -= y reads as 'x equals minus y' and x += 0.5 as 'add a half' in arithmetic. In Java x op= e means x = (T) (x op e): it updates x from its current value and casts the result back to x's type.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:compound_assignment@L3#3 (the model saw the concept, the way's name 'purpose of the whole', its text, where the way stops and whether the words must be correct; no level):
> Plan/role: the update step of a gatherer (sum += a[i], product *= i) or of a stepper with a step other than 1 (i += 2).
>
> Where this way stops: Narrating the lines is L2. A purpose induced from a few traced cases is L2. A wrong purpose is still L3, but with an error.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:compound_assignment@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> The new value of x is (T)(old x op e) and is also the expression's value: each starting from int x = 7: x += 3 gives 10, x /= 2 gives 3, and x += 0.5 gives 7 (7.5 truncated) instead of a compile error.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:compound_assignment@L0#0 | not applied |  |  | 0.0 |  |  |
| lvl:compound_assignment@L3#3 | not applied |  |  | 0.0 |  |  |
| lvl:compound_assignment@L2#1 | not applied |  |  | 0.0 |  |  |

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
mis:println->PrintedTextIsExecuted (0.50), mis:println->PrintNewLineFirst (0.30), err:println->PrintWithoutFinalNewline (0.20)
```
Kept by pruning: mis:println->PrintedTextIsExecuted (0.50), mis:println->PrintNewLineFirst (0.30), err:println->PrintWithoutFinalNewline (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:println->PrintedTextIsExecuted \| wrong rule: System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code). \| right rule: Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x. |
| mis:println->PrintNewLineFirst \| wrong rule: println(s) prints a newline and then s. \| right rule: println(s) prints s and then the newline. |
| err:println->PrintWithoutFinalNewline \| wrong rule: Ends the output with print and expects it to appear right away. \| right rule: Finish a line of print calls with println; some systems hold print output until a newline is printed. |
Model's reply:
```
mis:println->PrintedTextIsExecuted | not applied | clauses: none | confidence: 0.95
mis:println->PrintNewLineFirst | not applied | clauses: none | confidence: 0.95
err:println->PrintWithoutFinalNewline | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:println->PrintedTextIsExecuted | not applied |  |  | 0.0 |  |  |
| mis:println->PrintNewLineFirst | not applied |  |  | 0.0 |  |  |
| err:println->PrintWithoutFinalNewline | not applied |  |  | 0.0 |  |  |

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
{lvl:println@L2#1 (Score: 0.5)}
{lvl:println@L3#4 (Score: 0.25)}
{lvl:println@L1#0 (Score: 0.25)}
```
Kept by pruning: lvl:println@L2#1 (0.50), lvl:println@L3#4 (0.25), lvl:println@L1#0 (0.25)

Label prompt for level way lvl:println@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> Output is the value's characters followed by a line break: println("Hello, "); println("World!"); prints two lines.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.6
```

Label prompt for level way lvl:println@L3#4 (the model saw the concept, the way's name 'purpose of the whole', its text, where the way stops and whether the words must be correct; no level):
> Purpose: produce one complete line of output, e.g. each result on its own line, or end a line built with print.
>
> Where this way stops: Narrating the lines is L2. A purpose induced from a few traced cases is L2. A wrong purpose is still L3, but with an error.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:println@L1#0 (the model saw only the concept, the way's name 'names the element' and its text; no level):
> System.out.println is a library method that prints its argument followed by a line terminator ('print line').

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:println@L2#1 | shown | 0.5 | 0.6 | 0.3 | c1 | 5 |
| lvl:println@L3#4 | not applied |  |  | 0.0 |  |  |
| lvl:println@L1#0 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

lvl:println@L2#1 [shown, tier 2, 0.30]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | 5 | not covered yet |
| c2 | Page 1 has probability 0.5 | not covered yet |
| c3 | so in 10 steps the surfer goes there exactly 5 times | not covered yet |

**Uncovered clauses bring in (BM25 of the uncovered clauses against unvisited concepts):** math_random (10.21), loop_control (9.17), frequency_counting (8.83)

**Graph check, not yet read (the walk may not stop while these remain):** own edges of frequency_counting, own edges of loop_control, own edges of math_random, par:increment_operators~compound_assignment, pre:arithmetic_operators->expression, pre:assignment->compound_assignment, pre:compound_assignment->accumulator_pattern, pre:statement->println

Figure 4 (the graph after depth 1): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY40_figure04.png

### Depth 2: current concepts 'arithmetic_operators', 'compound_assignment', 'println', 'math_random', 'loop_control', 'frequency_counting'

#### arithmetic_operators, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:arithmetic_operators->expression \| rule: An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:arithmetic_operators->expression (Score: 1.0)}
```
Kept by pruning: pre:arithmetic_operators->expression (1.00)

Label prompt for concept edge pre:arithmetic_operators->expression (arithmetic_operators -> expression, prerequisite):
> An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:arithmetic_operators->expression | not applied |  |  | 0.0 |  |  |

#### compound_assignment, concept edges: 3 edges offered
Edges offered:
| edge |
|---|
| par:increment_operators~compound_assignment \| rule: i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, *=, /=, %=). |
| pre:assignment->compound_assignment \| rule: x op= e is shorthand for the assignment x = x op e. |
| pre:compound_assignment->accumulator_pattern \| rule: sum += x is the usual way a running total is updated on each pass. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:compound_assignment->accumulator_pattern (Score: 0.5)}
{pre:assignment->compound_assignment (Score: 0.3)}
{par:increment_operators~compound_assignment (Score: 0.2)}
```
Kept by pruning: pre:compound_assignment->accumulator_pattern (0.50), pre:assignment->compound_assignment (0.30), par:increment_operators~compound_assignment (0.20)

Label prompt for concept edge pre:compound_assignment->accumulator_pattern (compound_assignment -> accumulator_pattern, prerequisite):
> sum += x is the usual way a running total is updated on each pass.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.8
```

Label prompt for concept edge pre:assignment->compound_assignment (assignment -> compound_assignment, prerequisite):
> x op= e is shorthand for the assignment x = x op e.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.85
```

Label prompt for concept edge par:increment_operators~compound_assignment (increment_operators -> compound_assignment, parallel):
> i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, *=, /=, %=).

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:compound_assignment->accumulator_pattern | not applied |  |  | 0.0 |  |  |
| pre:assignment->compound_assignment | not applied |  |  | 0.0 |  |  |
| par:increment_operators~compound_assignment | not applied |  |  | 0.0 |  |  |

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
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:statement->println | not applied |  |  | 0.0 |  |  |

#### math_random, misconceptions: 2 edges offered
Edges offered:
| edge |
|---|
| mis:math_random->ProbabilityIsPrediction \| wrong rule: A probability (e.g. 70%) predicts what the next single trial will do. \| right rule: A probability describes the long-run frequency over many trials, not one outcome. |
| mis:math_random->RandomCanReturnOne \| wrong rule: Math.random() can return exactly 1.0. \| right rule: Math.random() returns a value in [0, 1): 0 is possible, 1 is not. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:math_random->ProbabilityIsPrediction (0.90), mis:math_random->RandomCanReturnOne (0.10)
```
Kept by pruning: mis:math_random->ProbabilityIsPrediction (0.90), mis:math_random->RandomCanReturnOne (0.10)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:math_random->ProbabilityIsPrediction \| wrong rule: A probability (e.g. 70%) predicts what the next single trial will do. \| right rule: A probability describes the long-run frequency over many trials, not one outcome. |
| mis:math_random->RandomCanReturnOne \| wrong rule: Math.random() can return exactly 1.0. \| right rule: Math.random() returns a value in [0, 1): 0 is possible, 1 is not. |
Model's reply:
```
mis:math_random->ProbabilityIsPrediction | held | clauses: 1, 2, 3 | confidence: 0.9
mis:math_random->RandomCanReturnOne | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:math_random->ProbabilityIsPrediction | held | 0.9 | 0.9 | 0.81 | c1, c2, c3 | 5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |
| mis:math_random->RandomCanReturnOne | not applied |  |  | 0.0 |  |  |

#### math_random, level ways: 16 edges offered
Edges offered:
| edge |
|---|
| lvl:math_random@L0#0 \| level L0 way everyday_reading: Folk meaning: 'a random number between 0 and 1' includes both ends, and a 70% chance means the event will happen next time. Java rule: Math.random() returns a double in the half-open interval [0, 1) (0 possible, 1 never), and a probability only describes long-run frequencies over many calls. |
| lvl:math_random@L0#3 \| level L0 way inconsistent_trace: Points to LT (each call produces a fresh value, which is then scaled and cast). Applied unevenly: the student reuses one random value for two separate Math.random() calls on some lines (e.g. assumes the x and y coordinates are equal) or scales without casting on one pass. (here mixing in: "Math.random() can return exactly 1.0") |
| lvl:math_random@L1#0 \| level L1 way names_the_element: Math.random() is a Math library method with no argument that returns a (pseudo-)random double uniformly distributed in [0, 1). |
| lvl:math_random@L1#1 \| level L1 way states_the_rule: Each call returns a new double r with 0 <= r < 1; multiplying by N gives a value in [0, N), and casting truncates it to an int between 0 and N-1. |
| lvl:math_random@L2#0 \| level L2 way line_by_line_trace: In int n = (int) (r * N) with r = Math.random(): the call produces r, the product r * N is computed in double (N promoted), the parenthesized cast truncates it, then n is assigned. |
| lvl:math_random@L2#1 \| level L2 way output_prediction: A double in [0, 1) that differs from call to call and run to run (e.g. RandomInt 1000 prints 548, then 141); (int) (Math.random() * 6) + 1 is an int from 1 to 6; Math.random() < 0.5 is true about half the time. |
| lvl:math_random@L2#2 \| level L2 way one_step_execution: A call changes none of the program's variables, but each call advances the library's hidden generator state, so the next call returns a different value; the drawn value persists only if stored (double r = Math.random();). |
| lvl:math_random@L3#0 \| level L3 way relation_to_neighbour: Math.random() is the Math method that takes no argument and, unlike the others, is not a function of its input: it returns a random double in [0, 1). |
| lvl:math_random@L3#1 \| level L3 way relation_to_neighbour: Converting to a random int requires the cast to apply to the whole product: (int) (Math.random() * N); (int) Math.random() * N casts first and is always 0. |
| lvl:math_random@L3#2 \| level L3 way relation_to_neighbour: Each trial of a Monte Carlo simulation draws fresh values with Math.random(); estimates become reliable only over many trials. |
| lvl:math_random@L3#3 \| level L3 way purpose_of_the_whole: Plans: simulate an event of probability p with if (Math.random() < p); pick a random index with (int) (Math.random() * N); generate random points or samples (Sajaniemi role of the drawn value: most-recent holder, overwritten each trial). |
| lvl:math_random@L4#0 \| level L4 way predict_a_change: Changing N in (int) (Math.random() * N) changes the range to 0..N-1, and adding a constant shifts it; the output changes from run to run, so a program using Math.random() cannot be checked by comparing exact outputs, only by statistics over many runs. |
| lvl:math_random@L4#1 \| level L4 way transfer_to_a_new_program: Use Math.random() for simulations, games, random sampling and shuffling, where 'every value equally likely' in [0, 1) is the model; it is not suitable when results must be reproducible or follow another distribution without further transformation. |
| lvl:math_random@L4#2 \| level L4 way diagnose_an_error: rule broken: The scaled range of (int) (Math.random() * N) is 0..N-1. Kind: silent logic error. Trigger class: Expecting N to be possible, or 1..N, without adding 1; or scaling by (b - a) instead of (b - a + 1) for an inclusive range a..b. |
| lvl:math_random@L4#3 \| level L4 way diagnose_an_error: rule broken: A cast applies only to the value immediately after it. Kind: silent logic error. Trigger class: Writing (int) Math.random() * N, which always gives 0. |
| lvl:math_random@L4#4 \| level L4 way diagnose_an_error: rule broken: A double cannot be assigned to an int without a cast. Kind: compile-time. Trigger class: int n = Math.random() * N; |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:math_random@L0#0 (Score: 0.6)}
{lvl:math_random@L3#2 (Score: 0.25)}
{lvl:math_random@L4#0 (Score: 0.15)}
```
Kept by pruning: lvl:math_random@L0#0 (0.60), lvl:math_random@L3#2 (0.25), lvl:math_random@L4#0 (0.15)

Label prompt for level way lvl:math_random@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: 'a random number between 0 and 1' includes both ends, and a 70% chance means the event will happen next time. Java rule: Math.random() returns a double in the half-open interval [0, 1) (0 possible, 1 never), and a probability only describes long-run frequencies over many calls.

Model's reply:
```
Label: shown
Clauses: 1, 3
Confidence: 0.85
```

Label prompt for level way lvl:math_random@L3#2 (the model saw the concept, the way's name 'relation to neighbour', its text, where the way stops and whether the words must be correct; no level):
> Each trial of a Monte Carlo simulation draws fresh values with Math.random(); estimates become reliable only over many trials.
>
> Where this way stops: Two correct but separate rules are L1. Executing the two in sequence is L2. A relational answer may be correct or a relational error.

Model's reply:
```
Label: wrong
Clauses: 2, 3
Confidence: 0.8
```

Label prompt for level way lvl:math_random@L4#0 (the model saw the concept, the way's name 'predict a change', its text, where the way stops and whether the words must be correct; no level):
> Changing N in (int) (Math.random() * N) changes the range to 0..N-1, and adding a constant shifts it; the output changes from run to run, so a program using Math.random() cannot be checked by comparing exact outputs, only by statistics over many runs.
>
> Where this way stops: Re-tracing the changed code value by value is L2 on the new code. Adapting given code to a familiar variant may be only relational.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.75
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:math_random@L0#0 | shown | 0.6 | 0.85 | 0.51 | c1, c3 | 5; so in 10 steps the surfer goes there exactly 5 times |

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
err:loop_control->WrongIterationCount (0.45), mis:loop_control->OffByOneBound (0.30), mis:loop_control->IdiomOverridesCode (0.25)
```
Kept by pruning: err:loop_control->WrongIterationCount (0.45), mis:loop_control->OffByOneBound (0.30), mis:loop_control->IdiomOverridesCode (0.25)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| err:loop_control->WrongIterationCount \| wrong rule: Updates the loop counter so that the loop runs the wrong number of times. \| right rule: The init, test and update together decide the number of passes; trace them to check the count. |
| mis:loop_control->OffByOneBound \| wrong rule: i < n and i <= n mean the same, so the loop runs until i equals n and the last pass can use a[n]. \| right rule: for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n. |
| mis:loop_control->IdiomOverridesCode \| wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. |
Model's reply:
```
err:loop_control->WrongIterationCount | correct | clauses: 3 | confidence: 0.6
mis:loop_control->OffByOneBound | correct | clauses: 3 | confidence: 0.5
mis:loop_control->IdiomOverridesCode | not applied | clauses: none | confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| err:loop_control->WrongIterationCount | correct | 0.45 | 0.6 | 0.27 | c3 | so in 10 steps the surfer goes there exactly 5 times |
| mis:loop_control->OffByOneBound | correct | 0.3 | 0.5 | 0.15 | c3 | so in 10 steps the surfer goes there exactly 5 times |
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
{lvl:loop_control@L2#1 (Score: 0.45)}
{lvl:loop_control@L3#6 (Score: 0.3)}
{lvl:loop_control@L4#2 (Score: 0.25)}
```
Kept by pruning: lvl:loop_control@L2#1 (0.45), lvl:loop_control@L3#6 (0.30), lvl:loop_control@L4#2 (0.25)

Label prompt for level way lvl:loop_control@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> The number of passes and the values seen follow from the three parts: for (int i = 0; i <= N; i++) makes N+1 passes with i = 0..N; with i < N it makes N passes; i += 2 visits every second value.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.6
```

Label prompt for level way lvl:loop_control@L3#6 (the model saw the concept, the way's name 'purpose of the whole', its text, where the way stops and whether the words must be correct; no level):
> Plan: counter-controlled loop - the loop variable is a stepper that walks a predictable sequence of values (0..N-1, 1..N, every 2nd value) and fixes the number of passes in advance.
>
> Where this way stops: Narrating the lines is L2. A purpose induced from a few traced cases is L2. A wrong purpose is still L3, but with an error.

Model's reply:
```
Label: wrong
Clauses: 2, 3
Confidence: 0.75
```

Label prompt for level way lvl:loop_control@L4#2 (the model saw the concept, the way's name 'transfer to a new program', its text, where the way stops and whether the words must be correct; no level):
> Use explicit init/test/update control when the passes are counted or follow a fixed step; when the number of passes depends on data computed in the body, control the loop by that data (a while condition) instead.
>
> Where this way stops: Reproducing or slightly varying a familiar program is L1 to L3.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:loop_control@L2#1 | not applied |  |  | 0.0 |  |  |

#### frequency_counting, misconceptions: 2 edges offered
Edges offered:
| edge |
|---|
| mis:frequency_counting->FewTrialsAreExact \| wrong rule: A short simulation gives the exact page ranks. \| right rule: A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three). |
| mis:frequency_counting->ManyDigitsMeanAccurate \| wrong rule: A result printed with many decimal places must be accurate to those places. \| right rule: A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:frequency_counting->FewTrialsAreExact (Score: 0.9)}
{mis:frequency_counting->ManyDigitsMeanAccurate (Score: 0.1)}
```
Kept by pruning: mis:frequency_counting->FewTrialsAreExact (0.90), mis:frequency_counting->ManyDigitsMeanAccurate (0.10)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:frequency_counting->FewTrialsAreExact \| wrong rule: A short simulation gives the exact page ranks. \| right rule: A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three). |
| mis:frequency_counting->ManyDigitsMeanAccurate \| wrong rule: A result printed with many decimal places must be accurate to those places. \| right rule: A program does not produce accurate answers simply because it can print numbers to many decimal places of precision; ensuring accuracy is often the most difficult challenge. |
Model's reply:
```
mis:frequency_counting->FewTrialsAreExact | held | clauses: 1, 2, 3 | confidence: 0.92
mis:frequency_counting->ManyDigitsMeanAccurate | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:frequency_counting->FewTrialsAreExact | held | 0.9 | 0.92 | 0.83 | c1, c2, c3 | 5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |
| mis:frequency_counting->ManyDigitsMeanAccurate | not applied |  |  | 0.0 |  |  |

#### frequency_counting, level ways: 14 edges offered
Edges offered:
| edge |
|---|
| lvl:frequency_counting@L0#0 \| level L0 way everyday_reading: Everyday "rank" means a position in a list (1st, 2nd) and "frequency" a rate; here a page's rank is a probability, estimated by the fraction freq[i]/T of moves that land on it. |
| lvl:frequency_counting@L0#3 \| level L0 way inconsistent_trace: Applies LT (increment after each move, divide by T after the loop) unevenly: e.g. incrementing the page before the move on some passes, or dividing inside the loop. (here mixing in: "A short simulation gives the exact page ranks") |
| lvl:frequency_counting@L1#0 \| level L1 way names_the_element: A counting technique: an int array freq[] with one counter per page, incremented each time the surfer lands there; dividing by T gives the visit frequencies. |
| lvl:frequency_counting@L1#1 \| level L1 way states_the_rule: RandomSurfer counts the number of times the surfer visits each page; dividing that count by the number of moves estimates the probability of ending on the page (its rank). |
| lvl:frequency_counting@L2#0 \| level L2 way line_by_line_trace: freq is created (all zeros) before the loop; each pass ends with freq[page]++; after the loop, each (double) freq[i] / T is computed (cast first, then divide) and printed. |
| lvl:frequency_counting@L2#1 \| level L2 way output_prediction: Integer counts summing to T; the printed fractions are doubles in [0, 1] summing to about 1 (e.g. 0.27280 0.26530 0.14820 0.24830 0.06540 after 10000 moves). |
| lvl:frequency_counting@L2#2 \| level L2 way one_step_execution: One count step adds 1 to exactly one element, freq[page]; all other counts are unchanged. |
| lvl:frequency_counting@L3#0 \| level L3 way relation_to_neighbour: The increment is the last statement of each pass, so the counts tally the pages reached by the T moves (sum = T). |
| lvl:frequency_counting@L3#1 \| level L3 way relation_to_neighbour: freq[i]/T converges to the same page ranks the power method computes, but only as an estimate. |
| lvl:frequency_counting@L3#2 \| level L3 way purpose_of_the_whole: Counter plan per bucket (a tally array indexed by outcome): each freq[i] is a gatherer accumulating visits to page i, and the array holds the histogram that stabilises to the ranks. |
| lvl:frequency_counting@L4#0 \| level L4 way predict_a_change: Invariant: the counts sum to T, so the fractions sum to 1; dividing before casting ((double)(freq[i] / T)) or counting outside the loop breaks it. |
| lvl:frequency_counting@L4#1 \| level L4 way transfer_to_a_new_program: Use whenever a probability is estimated from repeated random trials (histograms, Monte Carlo); not when the exact probabilities can be computed, as with the power method. |
| lvl:frequency_counting@L4#2 \| level L4 way diagnose_an_error: rule broken: Casting must apply before the division. Kind: silent logic error. Trigger class: (double) (freq[i] / T) or freq[i] / T: integer division gives 0 for every page that is not visited on every move. |
| lvl:frequency_counting@L4#3 \| level L4 way diagnose_an_error: rule broken: A local array must be created before use. Kind: compile-time. Trigger class: int[] freq; declared without new int[N] and then incremented: compile error, variable might not have been initialized. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:frequency_counting@L0#3 (Score: 0.5)}
{lvl:frequency_counting@L3#1 (Score: 0.3)}
{lvl:frequency_counting@L1#1 (Score: 0.2)}
```
Kept by pruning: lvl:frequency_counting@L0#3 (0.50), lvl:frequency_counting@L3#1 (0.30), lvl:frequency_counting@L1#1 (0.20)

Label prompt for level way lvl:frequency_counting@L0#3 (the model saw only the concept, the way's name 'inconsistent trace' and its text; no level):
> Applies LT (increment after each move, divide by T after the loop) unevenly: e.g. incrementing the page before the move on some passes, or dividing inside the loop. (here mixing in: "A short simulation gives the exact page ranks")

Model's reply:
```
Label: shown
Clauses: 1, 3
Confidence: 0.55
```

Label prompt for level way lvl:frequency_counting@L3#1 (the model saw the concept, the way's name 'relation to neighbour', its text, where the way stops and whether the words must be correct; no level):
> freq[i]/T converges to the same page ranks the power method computes, but only as an estimate.
>
> Where this way stops: Two correct but separate rules are L1. Executing the two in sequence is L2. A relational answer may be correct or a relational error.

Model's reply:
```
Label: wrong
Clauses: 2, 3
Confidence: 0.8
```

Label prompt for level way lvl:frequency_counting@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> RandomSurfer counts the number of times the surfer visits each page; dividing that count by the number of moves estimates the probability of ending on the page (its rank).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:frequency_counting@L0#3 | shown | 0.5 | 0.55 | 0.28 | c1, c3 | 5; so in 10 steps the surfer goes there exactly 5 times |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:frequency_counting->FewTrialsAreExact [held, tier 0, 0.83], mis:math_random->ProbabilityIsPrediction [held, tier 0, 0.81], lvl:math_random@L0#0 [shown, tier 2, 0.51]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | 5 | mis:math_random->ProbabilityIsPrediction |
| c2 | Page 1 has probability 0.5 | mis:math_random->ProbabilityIsPrediction |
| c3 | so in 10 steps the surfer goes there exactly 5 times | mis:math_random->ProbabilityIsPrediction |

**Graph check, not yet read (the walk may not stop while these remain):** pre:counter_pattern->frequency_counting, pre:loop_control->for_loop, pre:loop_control->increment_operators, pre:loop_variable->loop_control, pre:math_library->math_random, pre:while_loop->loop_control

Figure 5 (the graph after depth 2): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY40_figure05.png

### Depth 3: current concepts 'frequency_counting', 'math_random', 'loop_control'

#### frequency_counting, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:counter_pattern->frequency_counting \| rule: Frequency counting keeps one counter per value in an array, freq[page]++. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:counter_pattern->frequency_counting (Score: 1.0)}
```
Kept by pruning: pre:counter_pattern->frequency_counting (1.00)

Label prompt for concept edge pre:counter_pattern->frequency_counting (counter_pattern -> frequency_counting, prerequisite):
> Frequency counting keeps one counter per value in an array, freq[page]++.

Model's reply:
```
Label: confirmed
Clauses: 3
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:counter_pattern->frequency_counting | confirmed | 1.0 | 0.6 | 0.6 | c3 | so in 10 steps the surfer goes there exactly 5 times |

#### math_random, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:math_library->math_random \| rule: Math.random() is a Math library method; unlike the others it takes no argument and returns a random double in [0, 1). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:math_library->math_random (Score: 1.0)}
```
Kept by pruning: pre:math_library->math_random (1.00)

Label prompt for concept edge pre:math_library->math_random (math_library -> math_random, prerequisite):
> Math.random() is a Math library method; unlike the others it takes no argument and returns a random double in [0, 1).

Model's reply:
```
Label: broken
Clauses: 1, 3
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:math_library->math_random | broken | 1.0 | 0.85 | 0.85 | c1, c3 | 5; so in 10 steps the surfer goes there exactly 5 times |

#### loop_control, concept edges: 4 edges offered
Edges offered:
| edge |
|---|
| pre:loop_control->for_loop \| rule: The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |
| pre:loop_control->increment_operators \| rule: The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update. |
| pre:loop_variable->loop_control \| rule: The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |
| pre:while_loop->loop_control \| rule: A while loop has the same three control parts as a for loop, written in other places: the index set before the loop, the loop-continuation condition in the header, and the update as the last statement of the body. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:loop_control->for_loop (Score: 0.5)}
{pre:loop_variable->loop_control (Score: 0.3)}
{pre:while_loop->loop_control (Score: 0.2)}
```
Kept by pruning: pre:loop_control->for_loop (0.50), pre:loop_variable->loop_control (0.30), pre:while_loop->loop_control (0.20)

Label prompt for concept edge pre:loop_control->for_loop (loop_control -> for_loop, prerequisite):
> The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.

Model's reply:
```
Label: confirmed
Clauses: 3
Confidence: 0.55
```

Label prompt for concept edge pre:loop_variable->loop_control (loop_variable -> loop_control, prerequisite):
> The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.

Model's reply:
```
Label: confirmed
Clauses: 3
Confidence: 0.55
```

Label prompt for concept edge pre:while_loop->loop_control (while_loop -> loop_control, prerequisite):
> A while loop has the same three control parts as a for loop, written in other places: the index set before the loop, the loop-continuation condition in the header, and the update as the last statement of the body.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:loop_control->for_loop | confirmed | 0.5 | 0.55 | 0.28 | c3 | so in 10 steps the surfer goes there exactly 5 times |
| pre:loop_variable->loop_control | confirmed | 0.3 | 0.55 | 0.17 | c3 | so in 10 steps the surfer goes there exactly 5 times |
| pre:while_loop->loop_control | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:math_library->math_random [broken, tier 0, 0.85], pre:counter_pattern->frequency_counting [confirmed, tier 2, 0.60], pre:loop_control->for_loop [confirmed, tier 2, 0.28]

reached across pre:math_library->math_random, entered next: math_library

reached across pre:counter_pattern->frequency_counting, entered next: counter_pattern

reached across pre:loop_control->for_loop, entered next: for_loop

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | 5 | mis:math_random->ProbabilityIsPrediction |
| c2 | Page 1 has probability 0.5 | mis:math_random->ProbabilityIsPrediction |
| c3 | so in 10 steps the surfer goes there exactly 5 times | mis:math_random->ProbabilityIsPrediction |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of counter_pattern, own edges of for_loop, own edges of math_library

Figure 6 (the graph after depth 3): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY40_figure06.png

### Depth 4: current concepts 'math_library', 'counter_pattern', 'for_loop'

#### math_library, misconceptions: 4 edges offered
Edges offered:
| edge |
|---|
| err:math_library->MathMethodWithoutClassName \| wrong rule: sqrt(x) calls the square-root method. \| right rule: Library methods are called with the class name, e.g. Math.sqrt(x). |
| err:math_library->WrongArgumentType \| wrong rule: Calls a method with arguments of the wrong type, e.g. Math.sqrt("2"). \| right rule: Each argument must have the type the method's API lists. |
| mis:math_library->AbsAlwaysNonNegative \| wrong rule: Math.abs always returns a non-negative number. \| right rule: Math.abs(Integer.MIN_VALUE) returns Integer.MIN_VALUE, which is negative. |
| mis:math_library->CastRounds \| wrong rule: (int) 2.7 evaluates to 3. \| right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:math_library->CastRounds (0.40), err:math_library->WrongArgumentType (0.30), err:math_library->MathMethodWithoutClassName (0.30)
```
Kept by pruning: mis:math_library->CastRounds (0.40), err:math_library->WrongArgumentType (0.30), err:math_library->MathMethodWithoutClassName (0.30)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:math_library->CastRounds \| wrong rule: (int) 2.7 evaluates to 3. \| right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer. |
| err:math_library->WrongArgumentType \| wrong rule: Calls a method with arguments of the wrong type, e.g. Math.sqrt("2"). \| right rule: Each argument must have the type the method's API lists. |
| err:math_library->MathMethodWithoutClassName \| wrong rule: sqrt(x) calls the square-root method. \| right rule: Library methods are called with the class name, e.g. Math.sqrt(x). |
Model's reply:
```
mis:math_library->CastRounds | not applied | clauses: none | confidence: 0.9
err:math_library->WrongArgumentType | not applied | clauses: none | confidence: 0.95
err:math_library->MathMethodWithoutClassName | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:math_library->CastRounds | not applied |  |  | 0.0 |  |  |
| err:math_library->WrongArgumentType | not applied |  |  | 0.0 |  |  |
| err:math_library->MathMethodWithoutClassName | not applied |  |  | 0.0 |  |  |

#### math_library, level ways: 20 edges offered
Edges offered:
| edge |
|---|
| lvl:math_library@L0#0 \| level L0 way everyday_reading: Folk meaning: the calculator's function buttons, which work in degrees, round 2.7 to 3 when 'converting to a whole number', and always give a non-negative absolute value. Java rule: Math's trigonometric methods take radians, a cast to int truncates (only Math.round rounds, returning a long), and integer overflow makes Math.abs(-2147483648) negative. |
| lvl:math_library@L0#2 \| level L0 way inconsistent_trace: Points to LT (the argument is evaluated, then the method computes from it). Applied unevenly: within one trace the student feeds degrees to Math.sin on one call and radians on another, or rounds the result of one call and truncates another. (here mixing in: "(int) 2.7 evaluates to 3") |
| lvl:math_library@L1#0 \| level L1 way names_the_element: The Math library is Java's class Math (in java.lang, no import needed) of static methods for mathematical functions (abs, max, min, sin, cos, tan, exp, log, pow, sqrt, round, random) and the constants PI and E. |
| lvl:math_library@L1#1 \| level L1 way states_the_rule: Per the API: double abs/max/min (also for int, long, float), double sin/cos/tan(double theta) with theta in radians, double exp, log (natural), pow(a, b), sqrt; long round(double); double random() in [0, 1); constants Math.PI and Math.E. |
| lvl:math_library@L2#0 \| level L2 way line_by_line_trace: For Math.f(arg): evaluate arg (an int argument is widened to double), call the method, use the returned double in the enclosing expression; in nested calls the innermost runs first. |
| lvl:math_library@L2#1 \| level L2 way output_prediction: Math.sqrt(2.0) is 1.4142135623730951, Math.sqrt(-1.0) is NaN, Math.sin(Math.PI/2) is 1.0, Math.log(Math.E) is 1.0, Math.pow(2.0, 10.0) is 1024.0, and Math.abs(-2147483648) is -2147483648. |
| lvl:math_library@L2#2 \| level L2 way one_step_execution: All the listed Math methods except random() are mathematical functions: they change no variable and return the same result for the same argument; random() takes no argument and returns a different value on each call. |
| lvl:math_library@L3#0 \| level L3 way relation_to_neighbour: Every Math facility is used through a method call with the Math. prefix and parentheses (the constants Math.PI and Math.E are written without parentheses). |
| lvl:math_library@L3#1 \| level L3 way relation_to_neighbour: In the shuffle, r = i + (int) (Math.random() * (N-i)) scales Math.random() to a uniformly random position between i and N-1, so each remaining card is equally likely. |
| lvl:math_library@L3#2 \| level L3 way relation_to_neighbour: Each sample a[i] = Math.sin(2*Math.PI * i * hz / sps) is taken at evenly spaced times; the 2*Math.PI factor is needed because Math.sin works in radians, one cycle being 2 pi. |
| lvl:math_library@L3#3 \| level L3 way relation_to_neighbour: Math.random() is the one Math method that takes no argument and is not a mathematical function: it returns a random double in [0, 1). |
| lvl:math_library@L3#4 \| level L3 way relation_to_neighbour: Math.round is the Math method that rounds to the nearest integer, but it returns a long, so storing it in an int needs a cast. |
| lvl:math_library@L3#5 \| level L3 way relation_to_neighbour: The trigonometric functions are Math methods whose angles are in radians; Math.toRadians and Math.toDegrees convert. |
| lvl:math_library@L3#6 \| level L3 way relation_to_neighbour: The random move draws r = Math.random() once per move and compares it with growing cumulative sums of row p[page] to find which interval contains it. |
| lvl:math_library@L3#7 \| level L3 way purpose_of_the_whole: Used as a black box for standard numeric computations so that a program reads like the formula, e.g. Quadratic computes double d = Math.sqrt(discriminant);. |
| lvl:math_library@L4#0 \| level L4 way predict_a_change: Replacing Math.pow(x, 2) by x * x keeps the value (up to rounding) and is cheaper; replacing Math.round(x) by (int) x changes results whenever the fractional part is at least .5 (and for negatives); replacing Math.sin(x)/Math.cos(x) by Math.tan(x) keeps the value. |
| lvl:math_library@L4#1 \| level L4 way diagnose_an_error: rule broken: Library methods are called with the class name, e.g. Math.sqrt(x). Kind: compile-time. Trigger class: Calling sqrt(x) or pow(a, b) without Math. (cannot find symbol). |
| lvl:math_library@L4#2 \| level L4 way transfer_to_a_new_program: Use Math for standard functions (roots, logs, trig, extremes, rounding, randomness); for squaring or small known integer powers multiply instead of calling Math.pow, and write known powers of ten as literals such as 1e6. |
| lvl:math_library@L4#3 \| level L4 way diagnose_an_error: rule broken: Each argument must have the type the method's API lists. Kind: compile-time. Trigger class: Passing a String (Math.sqrt("2")) or a boolean to a Math method; numeric arguments are widened automatically. |
| lvl:math_library@L4#4 \| level L4 way diagnose_an_error: rule broken: Math.sqrt and Math.log are undefined for negative arguments and return NaN. Kind: silent logic error. Trigger class: A negative argument (e.g. a negative discriminant in Quadratic, Math.log(-1)); NaN then propagates to the output. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:math_library@L3#3 (Score: 0.4)}
{lvl:math_library@L2#2 (Score: 0.35)}
{lvl:math_library@L3#6 (Score: 0.25)}
```
Kept by pruning: lvl:math_library@L3#3 (0.40), lvl:math_library@L2#2 (0.35), lvl:math_library@L3#6 (0.25)

Label prompt for level way lvl:math_library@L3#3 (the model saw the concept, the way's name 'relation to neighbour', its text, where the way stops and whether the words must be correct; no level):
> Math.random() is the one Math method that takes no argument and is not a mathematical function: it returns a random double in [0, 1).
>
> Where this way stops: Two correct but separate rules are L1. Executing the two in sequence is L2. A relational answer may be correct or a relational error.

Model's reply:
```
Label: wrong
Clauses: 2, 3
Confidence: 0.6
```

Label prompt for level way lvl:math_library@L2#2 (the model saw only the concept, the way's name 'one step execution' and its text; no level):
> All the listed Math methods except random() are mathematical functions: they change no variable and return the same result for the same argument; random() takes no argument and returns a different value on each call.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:math_library@L3#6 (the model saw the concept, the way's name 'relation to neighbour', its text, where the way stops and whether the words must be correct; no level):
> The random move draws r = Math.random() once per move and compares it with growing cumulative sums of row p[page] to find which interval contains it.
>
> Where this way stops: Two correct but separate rules are L1. Executing the two in sequence is L2. A relational answer may be correct or a relational error.

Model's reply:
```
Label: wrong
Clauses: 2, 3
Confidence: 0.55
```

Parsed labels:
(none)

#### counter_pattern, misconceptions: 2 edges offered
Edges offered:
| edge |
|---|
| err:counter_pattern->AccumulatorDeclaredInLoop \| wrong rule: Declaring sum inside the loop body keeps a running total across passes. \| right rule: The accumulator must be declared and initialised before the loop. |
| mis:counter_pattern->VariableRolesInferred \| wrong rule: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. \| right rule: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:counter_pattern->VariableRolesInferred (Score: 0.6)}
{err:counter_pattern->AccumulatorDeclaredInLoop (Score: 0.4)}
```
Kept by pruning: mis:counter_pattern->VariableRolesInferred (0.60), err:counter_pattern->AccumulatorDeclaredInLoop (0.40)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:counter_pattern->VariableRolesInferred \| wrong rule: The computer recognises that one variable plays two roles, e.g. input value and running total, and keeps the values apart; it knows which variable is the counter and which the sum. \| right rule: A variable holds one value at a time; each role (input, counter, running total) needs its own variable and explicit update. |
| err:counter_pattern->AccumulatorDeclaredInLoop \| wrong rule: Declaring sum inside the loop body keeps a running total across passes. \| right rule: The accumulator must be declared and initialised before the loop. |
Model's reply:
```
mis:counter_pattern->VariableRolesInferred | not applied | clauses: none | confidence: 0.85
err:counter_pattern->AccumulatorDeclaredInLoop | not applied | clauses: none | confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:counter_pattern->VariableRolesInferred | not applied |  |  | 0.0 |  |  |
| err:counter_pattern->AccumulatorDeclaredInLoop | not applied |  |  | 0.0 |  |  |

#### counter_pattern, level ways: 16 edges offered
Edges offered:
| edge |
|---|
| lvl:counter_pattern@L0#0 \| level L0 way everyday_reading: Folk meaning: 'count' in everyday speech is done by looking at the whole collection at once, so a novice expects `count` to 'know' how many items matched. In Java a counter is just an int that changes only when `count++` executes, once per matching pass, starting from the value it was given before the loop. |
| lvl:counter_pattern@L1#0 \| level L1 way names_the_element: Loop plan (Soloway counter plan): an int variable set to 0 before a loop and increased by 1 on each pass that meets a condition, so it ends holding the number of matches. |
| lvl:counter_pattern@L1#1 \| level L1 way states_the_rule: Declare and initialise the counter before the loop (`int wins = 0;`); inside the loop guard `wins++` with the condition being counted (`if (cash == goal) wins++;`); read it after the loop. |
| lvl:counter_pattern@L2#0 \| level L2 way line_by_line_trace: Order: the initialisation `count = 0` runs once before the loop; then on each pass the loop test, the guard (`if (...)`) and, only when the guard is true, `count++`; the counter is read once after the loop ends. |
| lvl:counter_pattern@L2#1 \| level L2 way output_prediction: The result is an int equal to the number of passes on which the guard was true (0 if none); it is between 0 and the number of passes. Turning it into a rate with ints truncates: `100*wins/T` with wins = 503, T = 1000 prints 50. |
| lvl:counter_pattern@L2#2 \| level L2 way one_step_execution: One matching pass changes only the counter, by exactly +1 (`wins++` turns 7 into 8); a non-matching pass leaves it unchanged. `count++` as a statement returns nothing that is used. |
| lvl:counter_pattern@L3#0 \| level L3 way relation_to_neighbour: The `count++` (with its guard) must be inside the loop body, while the declaration `int count = 0;` must be outside and before it. Inside the body it runs once for each matching pass. After the loop it runs only once, so the count is at most 1. |
| lvl:counter_pattern@L3#1 \| level L3 way relation_to_neighbour: Same skeleton (initialise before, update inside, read after); the accumulator adds the current value (`sum += x`), the counter adds the constant 1 on matching passes (`count++`). The two are often combined to compute an average `sum / count`, which needs a guard against `count == 0`. |
| lvl:counter_pattern@L3#2 \| level L3 way relation_to_neighbour: A Monte Carlo estimate is the counter divided by the number of trials (`(double) wins / T`). So the counter has to be initialised once, before the trial loop, and must not be reset inside it. |
| lvl:counter_pattern@L3#3 \| level L3 way purpose_of_the_whole: Plan: counting plan; the counter variable plays a Sajaniemi 'stepper'-like counting role (Soloway's counter variable). Its job is to answer 'how many passes satisfied P?', e.g. wins or number of bets. |
| lvl:counter_pattern@L4#0 \| level L4 way predict_a_change: Invariant: after k passes, count equals the number of matching passes among those k. Moving the guard or the update changes the count. Moving `count++` out of the `if` turns it into a pass counter. Starting at 1 instead of 0 makes every result one too high. Reordering statements that do not touch count leaves it unchanged. |
| lvl:counter_pattern@L4#1 \| level L4 way diagnose_an_error: rule broken: The counter/accumulator must be declared and initialised before the loop. `int count = 0;` inside the body re-creates and resets it on every pass. Kind: silent logic error. Trigger class: Any loop with two or more passes: the count never exceeds 1 (or holds only the last pass). |
| lvl:counter_pattern@L4#2 \| level L4 way transfer_to_a_new_program: Use a counter when the question is 'how many' (wins, bets, primes, distinct values); use an accumulator when it is 'how much in total', and a boolean flag when you only need 'whether any'. When you need a count for each of many values, use an array of counters (a histogram) instead of many separate variables. |
| lvl:counter_pattern@L4#3 \| level L4 way diagnose_an_error: rule broken: A variable declared inside the loop body is out of scope after the loop. Kind: compile-time. Trigger class: Printing or using a counter after the loop when it was declared inside the body (cannot find symbol). |
| lvl:counter_pattern@L4#4 \| level L4 way diagnose_an_error: rule broken: Integer division truncates: a rate computed as `count / total` with ints is 0 whenever count < total. Kind: silent logic error. Trigger class: Converting a count to a fraction or percentage with int operands (e.g. `wins / T`) instead of `(double) wins / T` or `100*wins/T`. |
| lvl:counter_pattern@L4#5 \| level L4 way diagnose_an_error: rule broken: A local counter must be definitely assigned before it is read. Kind: compile-time. Trigger class: Declaring `int count;` without `= 0` and then executing `count++` (variable might not have been initialized). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:counter_pattern@L0#0 (Score: 0.5)}
{lvl:counter_pattern@L2#1 (Score: 0.35)}
{lvl:counter_pattern@L4#2 (Score: 0.15)}
```
Kept by pruning: lvl:counter_pattern@L0#0 (0.50), lvl:counter_pattern@L2#1 (0.35), lvl:counter_pattern@L4#2 (0.15)

Label prompt for level way lvl:counter_pattern@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: 'count' in everyday speech is done by looking at the whole collection at once, so a novice expects `count` to 'know' how many items matched. In Java a counter is just an int that changes only when `count++` executes, once per matching pass, starting from the value it was given before the loop.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.6
```

Label prompt for level way lvl:counter_pattern@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> The result is an int equal to the number of passes on which the guard was true (0 if none); it is between 0 and the number of passes. Turning it into a rate with ints truncates: `100*wins/T` with wins = 503, T = 1000 prints 50.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.8
```

Label prompt for level way lvl:counter_pattern@L4#2 (the model saw the concept, the way's name 'transfer to a new program', its text, where the way stops and whether the words must be correct; no level):
> Use a counter when the question is 'how many' (wins, bets, primes, distinct values); use an accumulator when it is 'how much in total', and a boolean flag when you only need 'whether any'. When you need a count for each of many values, use an array of counters (a histogram) instead of many separate variables.
>
> Where this way stops: Reproducing or slightly varying a familiar program is L1 to L3.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:counter_pattern@L0#0 | not applied |  |  | 0.0 |  |  |
| lvl:counter_pattern@L2#1 | not applied |  |  | 0.0 |  |  |
| lvl:counter_pattern@L4#2 | not applied |  |  | 0.0 |  |  |

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
err:for_loop->WrongIterationCount (0.50), mis:for_loop->LoopCountIsStatementCount (0.30), mis:for_loop->ForIsConditional (0.20)
```
Kept by pruning: err:for_loop->WrongIterationCount (0.50), mis:for_loop->LoopCountIsStatementCount (0.30), mis:for_loop->ForIsConditional (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| err:for_loop->WrongIterationCount \| wrong rule: Updates the loop counter so that the loop runs the wrong number of times. \| right rule: The init, test and update together decide the number of passes; trace them to check the count. |
| mis:for_loop->LoopCountIsStatementCount \| wrong rule: The repeat count of a counted loop says how many of the body statements are executed. \| right rule: The repeat count is how many times the whole body runs; every pass runs all body statements. |
| mis:for_loop->ForIsConditional \| wrong rule: The body of a for statement executes at most once. \| right rule: The body of a for statement runs once for every pass on which the condition is true, which can be many times. |
Model's reply:
```
err:for_loop->WrongIterationCount | correct | clauses: 3 | confidence: 0.75
mis:for_loop->LoopCountIsStatementCount | not applied | clauses: none | confidence: 0.85
mis:for_loop->ForIsConditional | correct | clauses: 3 | confidence: 0.65
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| err:for_loop->WrongIterationCount | correct | 0.5 | 0.75 | 0.38 | c3 | so in 10 steps the surfer goes there exactly 5 times |
| mis:for_loop->LoopCountIsStatementCount | not applied |  |  | 0.0 |  |  |
| mis:for_loop->ForIsConditional | correct | 0.2 | 0.65 | 0.13 | c3 | so in 10 steps the surfer goes there exactly 5 times |

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
{lvl:for_loop@L3#3 (Score: 0.45)}
{lvl:for_loop@L3#8 (Score: 0.35)}
{lvl:for_loop@L2#1 (Score: 0.2)}
```
Kept by pruning: lvl:for_loop@L3#3 (0.45), lvl:for_loop@L3#8 (0.35), lvl:for_loop@L2#1 (0.20)

Label prompt for level way lvl:for_loop@L3#3 (the model saw the concept, the way's name 'relation to neighbour', its text, where the way stops and whether the words must be correct; no level):
> A simulation runs a fixed number of trials with an outer for loop (for (int t = 0; t < T; t++)), each trial simulated inside the body.
>
> Where this way stops: Two correct but separate rules are L1. Executing the two in sequence is L2. A relational answer may be correct or a relational error.

Model's reply:
```
Label: wrong
Clauses: 2, 3
Confidence: 0.6
```

Label prompt for level way lvl:for_loop@L3#8 (the model saw the concept, the way's name 'purpose of the whole', its text, where the way stops and whether the words must be correct; no level):
> Plan: counted loop / counter-controlled repetition - do the body a known number of times, with the loop variable as a stepper (index, term number, trial number).
>
> Where this way stops: Narrating the lines is L2. A purpose induced from a few traced cases is L2. A wrong purpose is still L3, but with an error.

Model's reply:
```
Label: wrong
Clauses: 3
Confidence: 0.6
```

Label prompt for level way lvl:for_loop@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> A for statement has no value; the passes it makes are fixed by its header: for (int i = 1; i <= N; i++) sum += i; leaves sum = N(N+1)/2, and for (int i = 2; i <= 8; i += 2) prints 2, 4, 6, 8,.

Model's reply:
```
Label: shown
Clauses: 1, 3
Confidence: 0.6
```

Parsed labels:
(none)

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

err:for_loop->WrongIterationCount [correct, tier 2, 0.38], mis:for_loop->ForIsConditional [correct, tier 2, 0.13], lvl:for_loop@L2#1 [shown, tier 2, 0.12]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | 5 | mis:math_random->ProbabilityIsPrediction |
| c2 | Page 1 has probability 0.5 | mis:math_random->ProbabilityIsPrediction |
| c3 | so in 10 steps the surfer goes there exactly 5 times | mis:math_random->ProbabilityIsPrediction |

**Graph check, not yet read (the walk may not stop while these remain):** par:accumulator_pattern~counter_pattern, pre:for_loop->loop_body, pre:for_loop->loop_scope, pre:for_loop->nested_loops, pre:increment_operators->counter_pattern, pre:loop_body->counter_pattern, pre:method_call->math_library

Figure 7 (the graph after depth 4): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY40_figure07.png

## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on ['frequency_counting', 'math_random'], broken at [] (consequences: pre:math_library->math_random), prerequisites {'expression': ['arithmetic_operators'], 'array_default_values': ['array_creation'], 'array_initializer': ['array_creation', 'array_declaration'], 'indexing': ['array_creation', 'array_initializer'], 'array_creation': ['array_declaration'], 'compound_assignment': ['assignment'], 'increment_operators': ['assignment', 'loop_control'], 'while_loop': ['boolean_expression'], 'boolean_expression': ['comparison_operators'], 'accumulator_pattern': ['compound_assignment', 'loop_body'], 'frequency_counting': ['counter_pattern'], 'array_declaration': ['data_structure'], 'data_structure': ['data_type'], 'comparison_operators': ['expression'], 'method_call': ['expression'], 'loop_body': ['for_loop', 'while_loop'], 'loop_scope': ['for_loop'], 'nested_loops': ['for_loop'], 'counter_pattern': ['increment_operators', 'loop_body'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable', 'while_loop'], 'math_random': ['math_library'], 'api': ['method_call'], 'math_library': ['method_call'], 'control_flow': ['statement'], 'println': ['statement'], 'loop_variable': ['while_loop']}
- for_loop: L2 via output_prediction "5; so in 10 steps the surfer goes there exactly 5 times"
- frequency_counting: L0 via misconception "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times"
- math_random: L0 via misconception "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times"
- println: L2 via output_prediction "5"

**Stop:** max depth at depth 4; prompts {'prune': 24, 'label': 46}, fresh model calls 0, cache hits 70

### Held misconceptions
| concept | misconception | kind | quote | score | shares_evidence_with |
|---|---|---|---|---|---|
| frequency_counting | FewTrialsAreExact | misconception | 5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times | 0.828 |  |
| math_random | ProbabilityIsPrediction | misconception | 5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times | 0.81 |  |

### Broken concept edges
| edge | quote | score | consequence_of |
|---|---|---|---|
| pre:math_library->math_random | 5; so in 10 steps the surfer goes there exactly 5 times | 0.85 | mis:frequency_counting->FewTrialsAreExact |

### Root cause: frequency_counting / FewTrialsAreExact

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| for_loop | L2 | output_prediction |  | level_way | 5; so in 10 steps the surfer goes there exactly 5 times |  |  |  |
| frequency_counting | L0 | misconception | FewTrialsAreExact | level_mis_links | 5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times | wrong rule: A short simulation gives the exact page ranks. Right rule: freq[i]/T is only an estimate: about 10^n moves for n-digit precision and many more for accuracy. |  |  |
| math_random | L0 | misconception | ProbabilityIsPrediction | level_mis_links | 5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times | wrong rule: A probability (e.g. 70%) predicts what the next single trial will do. Right rule: A probability describes the long-run frequency over many trials, not one outcome; Math.random() < 0.7 is true on about 70% of many calls, and any single call can go either way. |  |  |
| println | L2 | output_prediction |  | level_way | 5 |  |  |  |

Ways above L2 the model answered "wrong" (the kind of thing is done, but what is said contradicts Java; not shown):
| concept | edge | level | way | confidence | clauses | quote |
|---|---|---|---|---|---|---|
| arithmetic_operators | lvl:arithmetic_operators@L3#4 | L3 | purpose_of_the_whole | 0.6 | [2, 3] | Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |
| math_random | lvl:math_random@L3#2 | L3 | relation_to_neighbour | 0.8 | [2, 3] | Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |
| loop_control | lvl:loop_control@L3#6 | L3 | purpose_of_the_whole | 0.75 | [2, 3] | Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |
| frequency_counting | lvl:frequency_counting@L3#1 | L3 | relation_to_neighbour | 0.8 | [2, 3] | Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |
| math_library | lvl:math_library@L3#3 | L3 | relation_to_neighbour | 0.6 | [2, 3] | Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |
| math_library | lvl:math_library@L3#6 | L3 | relation_to_neighbour | 0.55 | [2, 3] | Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |
| for_loop | lvl:for_loop@L3#3 | L3 | relation_to_neighbour | 0.6 | [2, 3] | Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |
| for_loop | lvl:for_loop@L3#8 | L3 | purpose_of_the_whole | 0.6 | [3] | so in 10 steps the surfer goes there exactly 5 times |

### Overall level: L0

Clause coverage (final):
| clause | covered by |
|---|---|
| 5 | lvl:println@L2#1 |
| Page 1 has probability 0.5 | mis:math_random->ProbabilityIsPrediction |
| so in 10 steps the surfer goes there exactly 5 times | mis:math_random->ProbabilityIsPrediction |

Figure 8 (final picture): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY40_figure08.png

## 5. Every labelled edge (the evidence list, kept or not)
| depth | source | edge | kind | label | prune_score | confidence | score | clauses | quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | println | lvl:println@L2#1 | level | shown | 0.5 | 0.6 | 0.3 | [1] | 5 |
| 2 | math_random | mis:math_random->ProbabilityIsPrediction | misconception | held | 0.9 | 0.9 | 0.81 | [1, 2, 3] | 5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |
| 2 | math_random | lvl:math_random@L0#0 | level | shown | 0.6 | 0.85 | 0.51 | [1, 3] | 5; so in 10 steps the surfer goes there exactly 5 times |
| 2 | loop_control | err:loop_control->WrongIterationCount | error | correct | 0.45 | 0.6 | 0.27 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 2 | loop_control | mis:loop_control->OffByOneBound | misconception | correct | 0.3 | 0.5 | 0.15 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 2 | frequency_counting | mis:frequency_counting->FewTrialsAreExact | misconception | held | 0.9 | 0.92 | 0.828 | [1, 2, 3] | 5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |
| 2 | frequency_counting | lvl:frequency_counting@L0#3 | level | shown | 0.5 | 0.55 | 0.275 | [1, 3] | 5; so in 10 steps the surfer goes there exactly 5 times |
| 3 | frequency_counting | pre:counter_pattern->frequency_counting | prerequisite | confirmed | 1.0 | 0.6 | 0.6 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 3 | math_random | pre:math_library->math_random | prerequisite | broken | 1.0 | 0.85 | 0.85 | [1, 3] | 5; so in 10 steps the surfer goes there exactly 5 times |
| 3 | loop_control | pre:loop_control->for_loop | prerequisite | confirmed | 0.5 | 0.55 | 0.275 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 3 | loop_control | pre:loop_variable->loop_control | prerequisite | confirmed | 0.3 | 0.55 | 0.165 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 4 | for_loop | err:for_loop->WrongIterationCount | error | correct | 0.5 | 0.75 | 0.375 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 4 | for_loop | mis:for_loop->ForIsConditional | misconception | correct | 0.2 | 0.65 | 0.13 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 4 | for_loop | lvl:for_loop@L2#1 | level | shown | 0.2 | 0.6 | 0.12 | [1, 3] | 5; so in 10 steps the surfer goes there exactly 5 times |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | println | lvl:println@L2#1 | level | shown | 0.3 | [1] |
| 2 | frequency_counting | mis:frequency_counting->FewTrialsAreExact | misconception | held | 0.828 | [1, 2, 3] |
| 2 | math_random | mis:math_random->ProbabilityIsPrediction | misconception | held | 0.81 | [1, 2, 3] |
| 2 | math_random | lvl:math_random@L0#0 | level | shown | 0.51 | [1, 3] |
| 3 | math_random | pre:math_library->math_random | prerequisite | broken | 0.85 | [1, 3] |
| 3 | frequency_counting | pre:counter_pattern->frequency_counting | prerequisite | confirmed | 0.6 | [3] |
| 3 | loop_control | pre:loop_control->for_loop | prerequisite | confirmed | 0.275 | [3] |
| 4 | for_loop | err:for_loop->WrongIterationCount | error | correct | 0.375 | [3] |
| 4 | for_loop | mis:for_loop->ForIsConditional | misconception | correct | 0.13 | [3] |
| 4 | for_loop | lvl:for_loop@L2#1 | level | shown | 0.12 | [1, 3] |

## 7. Raw traversal log
```
clauses: 5 | Page 1 has probability 0.5 | so in 10 steps the surfer goes there exactly 5 times
start: BM25 of the answer against each tagged concept: arithmetic_operators 19.30 (hits 1), compound_assignment 14.54 (hits 1), println 11.79 (hits 1), math_random 10.79 (hits 1), loop_control 9.63 (hits 2), frequency_counting 8.63 (hits 2), for_loop 8.20 (hits 1), loop_variable 6.98 (hits 1), loop_body 6.45 (hits 1), increment_operators 6.10 (hits 1), while_loop 5.24 (hits 1), array_creation 4.70 (hits 1), counter_pattern 4.52 (hits 1), indexing 4.30 (hits 1), boolean_expression 3.63 (hits 2), nested_loops 3.40 (hits 1), control_flow 3.31 (hits 1), method_call 3.30 (hits 1), array_initializer 2.67 (hits 1), math_library 2.36 (hits 1), loop_scope 2.15 (hits 1), array_default_values 2.12 (hits 1), accumulator_pattern 1.56 (hits 1), array_declaration 1.18 (hits 1), comparison_operators 0.72 (hits 1), api 0.46 (hits 1), data_structure 0.17 (hits 1)
start: chosen arithmetic_operators, compound_assignment, println
start concepts (3): arithmetic_operators, compound_assignment, println
--- depth 1: current concepts ['arithmetic_operators', 'compound_assignment', 'println']
  arithmetic_operators (misconceptions): 3 candidates -> kept mis:arithmetic_operators->RemainderIsSubtraction (0.34), mis:arithmetic_operators->CaretIsPower (0.33), mis:arithmetic_operators->ArithmeticOnNumericStrings (0.33)
    mis:arithmetic_operators->RemainderIsSubtraction -> not applied (0.00) ""
    mis:arithmetic_operators->CaretIsPower -> not applied (0.00) ""
    mis:arithmetic_operators->ArithmeticOnNumericStrings -> not applied (0.00) ""
  arithmetic_operators (level ways): 18 candidates -> kept lvl:arithmetic_operators@L3#4 (0.40), lvl:arithmetic_operators@L2#1 (0.35), lvl:arithmetic_operators@L0#0 (0.25)
    lvl:arithmetic_operators@L3#4: wrong (0.60) -> not applied
    lvl:arithmetic_operators@L3#4 -> not applied (0.00) ""
    lvl:arithmetic_operators@L2#1 -> not applied (0.00) ""
    lvl:arithmetic_operators@L0#0 -> not applied (0.00) ""
  compound_assignment (misconceptions): 2 candidates -> kept mis:compound_assignment->CompoundAssignmentNoCast (0.50), mis:compound_assignment->CompoundSubtractIsAssignNegative (0.50)
    mis:compound_assignment->CompoundAssignmentNoCast -> not applied (0.00) ""
    mis:compound_assignment->CompoundSubtractIsAssignNegative -> not applied (0.00) ""
  compound_assignment (level ways): 15 candidates -> kept lvl:compound_assignment@L0#0 (0.40), lvl:compound_assignment@L3#3 (0.35), lvl:compound_assignment@L2#1 (0.25)
    lvl:compound_assignment@L0#0 -> not applied (0.00) ""
    lvl:compound_assignment@L3#3 -> not applied (0.00) ""
    lvl:compound_assignment@L2#1 -> not applied (0.00) ""
  println (misconceptions): 6 candidates -> kept mis:println->PrintedTextIsExecuted (0.50), mis:println->PrintNewLineFirst (0.30), err:println->PrintWithoutFinalNewline (0.20)
    mis:println->PrintedTextIsExecuted -> not applied (0.00) ""
    mis:println->PrintNewLineFirst -> not applied (0.00) ""
    err:println->PrintWithoutFinalNewline -> not applied (0.00) ""
  println (level ways): 17 candidates -> kept lvl:println@L2#1 (0.50), lvl:println@L3#4 (0.25), lvl:println@L1#0 (0.25)
    lvl:println@L2#1 -> shown (0.30) "5"
    lvl:println@L3#4 -> not applied (0.00) ""
    lvl:println@L1#0 -> not applied (0.00) ""
  kept: lvl:println@L2#1 [shown, tier 2, 0.30]
  clause coverage: c1 uncovered; c2 uncovered; c3 uncovered
  uncovered clauses bring in: math_random (10.21), loop_control (9.17), frequency_counting (8.83)
  not yet read: own edges of frequency_counting, own edges of loop_control, own edges of math_random, par:increment_operators~compound_assignment, pre:arithmetic_operators->expression, pre:assignment->compound_assignment, pre:compound_assignment->accumulator_pattern, pre:statement->println
--- depth 2: current concepts ['arithmetic_operators', 'compound_assignment', 'println', 'math_random', 'loop_control', 'frequency_counting']
  arithmetic_operators (concept edges): 1 candidates -> kept pre:arithmetic_operators->expression (1.00)
    pre:arithmetic_operators->expression -> not applied (0.00) ""
  compound_assignment (concept edges): 3 candidates -> kept pre:compound_assignment->accumulator_pattern (0.50), pre:assignment->compound_assignment (0.30), par:increment_operators~compound_assignment (0.20)
    pre:compound_assignment->accumulator_pattern -> not applied (0.00) ""
    pre:assignment->compound_assignment -> not applied (0.00) ""
    par:increment_operators~compound_assignment -> not applied (0.00) ""
  println (concept edges): 1 candidates -> kept pre:statement->println (1.00)
    pre:statement->println -> not applied (0.00) ""
  math_random (misconceptions): 2 candidates -> kept mis:math_random->ProbabilityIsPrediction (0.90), mis:math_random->RandomCanReturnOne (0.10)
    mis:math_random->ProbabilityIsPrediction -> held (0.81) "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times"
    mis:math_random->RandomCanReturnOne -> not applied (0.00) ""
  math_random (level ways): 16 candidates -> kept lvl:math_random@L0#0 (0.60), lvl:math_random@L3#2 (0.25), lvl:math_random@L4#0 (0.15)
    lvl:math_random@L0#0 -> shown (0.51) "5; so in 10 steps the surfer goes there exactly 5 times"
    lvl:math_random@L3#2: wrong (0.80) -> not applied
    lvl:math_random@L3#2 -> not applied (0.00) ""
    lvl:math_random@L4#0 -> not applied (0.00) ""
  loop_control (misconceptions): 11 candidates -> kept err:loop_control->WrongIterationCount (0.45), mis:loop_control->OffByOneBound (0.30), mis:loop_control->IdiomOverridesCode (0.25)
    err:loop_control->WrongIterationCount -> correct (0.27) "so in 10 steps the surfer goes there exactly 5 times"
    mis:loop_control->OffByOneBound -> correct (0.15) "so in 10 steps the surfer goes there exactly 5 times"
    mis:loop_control->IdiomOverridesCode -> not applied (0.00) ""
  loop_control (level ways): 19 candidates -> kept lvl:loop_control@L2#1 (0.45), lvl:loop_control@L3#6 (0.30), lvl:loop_control@L4#2 (0.25)
    lvl:loop_control@L2#1 -> not applied (0.00) ""
    lvl:loop_control@L3#6: wrong (0.75) -> not applied
    lvl:loop_control@L3#6 -> not applied (0.00) ""
    lvl:loop_control@L4#2 -> not applied (0.00) ""
  frequency_counting (misconceptions): 2 candidates -> kept mis:frequency_counting->FewTrialsAreExact (0.90), mis:frequency_counting->ManyDigitsMeanAccurate (0.10)
    mis:frequency_counting->FewTrialsAreExact -> held (0.83) "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times"
    mis:frequency_counting->ManyDigitsMeanAccurate -> not applied (0.00) ""
  frequency_counting (level ways): 14 candidates -> kept lvl:frequency_counting@L0#3 (0.50), lvl:frequency_counting@L3#1 (0.30), lvl:frequency_counting@L1#1 (0.20)
    lvl:frequency_counting@L0#3 -> shown (0.28) "5; so in 10 steps the surfer goes there exactly 5 times"
    lvl:frequency_counting@L3#1: wrong (0.80) -> not applied
    lvl:frequency_counting@L3#1 -> not applied (0.00) ""
    lvl:frequency_counting@L1#1 -> not applied (0.00) ""
  kept: mis:frequency_counting->FewTrialsAreExact [held, tier 0, 0.83], mis:math_random->ProbabilityIsPrediction [held, tier 0, 0.81], lvl:math_random@L0#0 [shown, tier 2, 0.51]
  clause coverage: c1 <- mis:math_random->ProbabilityIsPrediction; c2 <- mis:math_random->ProbabilityIsPrediction; c3 <- mis:math_random->ProbabilityIsPrediction
  not yet read: pre:counter_pattern->frequency_counting, pre:loop_control->for_loop, pre:loop_control->increment_operators, pre:loop_variable->loop_control, pre:math_library->math_random, pre:while_loop->loop_control
--- depth 3: current concepts ['frequency_counting', 'math_random', 'loop_control']
  frequency_counting (concept edges): 1 candidates -> kept pre:counter_pattern->frequency_counting (1.00)
    pre:counter_pattern->frequency_counting -> confirmed (0.60) "so in 10 steps the surfer goes there exactly 5 times"
  math_random (concept edges): 1 candidates -> kept pre:math_library->math_random (1.00)
    pre:math_library->math_random -> broken (0.85) "5; so in 10 steps the surfer goes there exactly 5 times"
  loop_control (concept edges): 4 candidates -> kept pre:loop_control->for_loop (0.50), pre:loop_variable->loop_control (0.30), pre:while_loop->loop_control (0.20)
    pre:loop_control->for_loop -> confirmed (0.28) "so in 10 steps the surfer goes there exactly 5 times"
    pre:loop_variable->loop_control -> confirmed (0.17) "so in 10 steps the surfer goes there exactly 5 times"
    pre:while_loop->loop_control -> not applied (0.00) ""
  kept: pre:math_library->math_random [broken, tier 0, 0.85], pre:counter_pattern->frequency_counting [confirmed, tier 2, 0.60], pre:loop_control->for_loop [confirmed, tier 2, 0.28]
  reached across pre:math_library->math_random, entered next: math_library
  reached across pre:counter_pattern->frequency_counting, entered next: counter_pattern
  reached across pre:loop_control->for_loop, entered next: for_loop
  clause coverage: c1 <- mis:math_random->ProbabilityIsPrediction; c2 <- mis:math_random->ProbabilityIsPrediction; c3 <- mis:math_random->ProbabilityIsPrediction
  not yet read: own edges of counter_pattern, own edges of for_loop, own edges of math_library
--- depth 4: current concepts ['math_library', 'counter_pattern', 'for_loop'] (closing round: own edges only)
  math_library (misconceptions): 4 candidates -> kept mis:math_library->CastRounds (0.40), err:math_library->WrongArgumentType (0.30), err:math_library->MathMethodWithoutClassName (0.30)
    mis:math_library->CastRounds -> not applied (0.00) ""
    err:math_library->WrongArgumentType -> not applied (0.00) ""
    err:math_library->MathMethodWithoutClassName -> not applied (0.00) ""
  math_library (level ways): 20 candidates -> kept lvl:math_library@L3#3 (0.40), lvl:math_library@L2#2 (0.35), lvl:math_library@L3#6 (0.25)
    lvl:math_library@L3#3: wrong (0.60) -> not applied
    lvl:math_library@L3#3 -> not applied (0.00) ""
    lvl:math_library@L2#2 -> not applied (0.00) ""
    lvl:math_library@L3#6: wrong (0.55) -> not applied
    lvl:math_library@L3#6 -> not applied (0.00) ""
  counter_pattern (misconceptions): 2 candidates -> kept mis:counter_pattern->VariableRolesInferred (0.60), err:counter_pattern->AccumulatorDeclaredInLoop (0.40)
    mis:counter_pattern->VariableRolesInferred -> not applied (0.00) ""
    err:counter_pattern->AccumulatorDeclaredInLoop -> not applied (0.00) ""
  counter_pattern (level ways): 16 candidates -> kept lvl:counter_pattern@L0#0 (0.50), lvl:counter_pattern@L2#1 (0.35), lvl:counter_pattern@L4#2 (0.15)
    lvl:counter_pattern@L0#0 -> not applied (0.00) ""
    lvl:counter_pattern@L2#1 -> not applied (0.00) ""
    lvl:counter_pattern@L4#2 -> not applied (0.00) ""
  for_loop (misconceptions): 21 candidates -> kept err:for_loop->WrongIterationCount (0.50), mis:for_loop->LoopCountIsStatementCount (0.30), mis:for_loop->ForIsConditional (0.20)
    err:for_loop->WrongIterationCount -> correct (0.38) "so in 10 steps the surfer goes there exactly 5 times"
    mis:for_loop->LoopCountIsStatementCount -> not applied (0.00) ""
    mis:for_loop->ForIsConditional -> correct (0.13) "so in 10 steps the surfer goes there exactly 5 times"
  for_loop (level ways): 24 candidates -> kept lvl:for_loop@L3#3 (0.45), lvl:for_loop@L3#8 (0.35), lvl:for_loop@L2#1 (0.20)
    lvl:for_loop@L3#3: wrong (0.60) -> not applied
    lvl:for_loop@L3#3 -> not applied (0.00) ""
    lvl:for_loop@L3#8: wrong (0.60) -> not applied
    lvl:for_loop@L3#8 -> not applied (0.00) ""
    lvl:for_loop@L2#1 -> shown (0.12) "5; so in 10 steps the surfer goes there exactly 5 times"
  kept: err:for_loop->WrongIterationCount [correct, tier 2, 0.38], mis:for_loop->ForIsConditional [correct, tier 2, 0.13], lvl:for_loop@L2#1 [shown, tier 2, 0.12]
  clause coverage: c1 <- mis:math_random->ProbabilityIsPrediction; c2 <- mis:math_random->ProbabilityIsPrediction; c3 <- mis:math_random->ProbabilityIsPrediction
  not yet read: par:accumulator_pattern~counter_pattern, pre:for_loop->loop_body, pre:for_loop->loop_scope, pre:for_loop->nested_loops, pre:increment_operators->counter_pattern, pre:loop_body->counter_pattern, pre:method_call->math_library
  root-cause walk: held on ['frequency_counting', 'math_random'], broken at [] (consequences: pre:math_library->math_random), prerequisites {'expression': ['arithmetic_operators'], 'array_default_values': ['array_creation'], 'array_initializer': ['array_creation', 'array_declaration'], 'indexing': ['array_creation', 'array_initializer'], 'array_creation': ['array_declaration'], 'compound_assignment': ['assignment'], 'increment_operators': ['assignment', 'loop_control'], 'while_loop': ['boolean_expression'], 'boolean_expression': ['comparison_operators'], 'accumulator_pattern': ['compound_assignment', 'loop_body'], 'frequency_counting': ['counter_pattern'], 'array_declaration': ['data_structure'], 'data_structure': ['data_type'], 'comparison_operators': ['expression'], 'method_call': ['expression'], 'loop_body': ['for_loop', 'while_loop'], 'loop_scope': ['for_loop'], 'nested_loops': ['for_loop'], 'counter_pattern': ['increment_operators', 'loop_body'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable', 'while_loop'], 'math_random': ['math_library'], 'api': ['method_call'], 'math_library': ['method_call'], 'control_flow': ['statement'], 'println': ['statement'], 'loop_variable': ['while_loop']}
  level for_loop: L2 via output_prediction "5; so in 10 steps the surfer goes there exactly 5 times"
  level frequency_counting: L0 via misconception "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times"
  level math_random: L0 via misconception "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times"
  level println: L2 via output_prediction "5"
```

## 8. Full diagnosis JSON
```json
{
 "scenario": "MY40",
 "settings": {
  "width": 3,
  "depth": 3,
  "prune_tools": "llm",
  "model": "claude-opus-5-5",
  "backend": "claude-cli",
  "level_v2": true
 },
 "clauses": [
  "5",
  "Page 1 has probability 0.5",
  "so in 10 steps the surfer goes there exactly 5 times"
 ],
 "start_concepts": [
  "arithmetic_operators",
  "compound_assignment",
  "println"
 ],
 "held_misconceptions": [
  {
   "concept": "frequency_counting",
   "misconception": "FewTrialsAreExact",
   "kind": "misconception",
   "quote": "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
   "score": 0.828
  },
  {
   "concept": "math_random",
   "misconception": "ProbabilityIsPrediction",
   "kind": "misconception",
   "quote": "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
   "score": 0.81
  }
 ],
 "error_evidence": [],
 "shadowed": [],
 "broken_edges": [
  {
   "edge": "pre:math_library->math_random",
   "quote": "5; so in 10 steps the surfer goes there exactly 5 times",
   "score": 0.85,
   "consequence_of": "mis:frequency_counting->FewTrialsAreExact"
  }
 ],
 "root_cause": {
  "concept": "frequency_counting",
  "misconception": "FewTrialsAreExact"
 },
 "levels": {
  "for_loop": {
   "level": "L2",
   "way": "output_prediction",
   "quote": "5; so in 10 steps the surfer goes there exactly 5 times",
   "edge": "lvl:for_loop@L2#1",
   "source": "level_way",
   "also_shown": []
  },
  "frequency_counting": {
   "level": "L0",
   "way": "misconception",
   "misconception": "FewTrialsAreExact",
   "quote": "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
   "edge": "mis:frequency_counting->FewTrialsAreExact",
   "rule": "wrong rule: A short simulation gives the exact page ranks. Right rule: freq[i]/T is only an estimate: about 10^n moves for n-digit precision and many more for accuracy.",
   "source": "level_mis_links"
  },
  "math_random": {
   "level": "L0",
   "way": "misconception",
   "misconception": "ProbabilityIsPrediction",
   "quote": "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
   "edge": "mis:math_random->ProbabilityIsPrediction",
   "rule": "wrong rule: A probability (e.g. 70%) predicts what the next single trial will do. Right rule: A probability describes the long-run frequency over many trials, not one outcome; Math.random() < 0.7 is true on about 70% of many calls, and any single call can go either way.",
   "source": "level_mis_links"
  },
  "println": {
   "level": "L2",
   "way": "output_prediction",
   "quote": "5",
   "edge": "lvl:println@L2#1",
   "source": "level_way",
   "also_shown": []
  }
 },
 "overall_level": "L0",
 "paths": [
  {
   "depth": 1,
   "source": "println",
   "edge": "lvl:println@L2#1",
   "target": "println@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "5",
   "confidence": 0.6,
   "prune_score": 0.5,
   "score": 0.3,
   "logic": "Output is the value's characters followed by a line break: println(\"Hello, \"); println(\"World!\"); prints two lines.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 2,
   "source": "frequency_counting",
   "edge": "mis:frequency_counting->FewTrialsAreExact",
   "target": "FewTrialsAreExact",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.92,
   "prune_score": 0.9,
   "score": 0.828,
   "logic": "A short simulation gives the exact page ranks.",
   "twin_logic": "A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).",
   "role": "primary"
  },
  {
   "depth": 2,
   "source": "math_random",
   "edge": "mis:math_random->ProbabilityIsPrediction",
   "target": "ProbabilityIsPrediction",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.9,
   "prune_score": 0.9,
   "score": 0.81,
   "logic": "A probability (e.g. 70%) predicts what the next single trial will do.",
   "twin_logic": "A probability describes the long-run frequency over many trials, not one outcome.",
   "role": "context"
  },
  {
   "depth": 2,
   "source": "math_random",
   "edge": "lvl:math_random@L0#0",
   "target": "math_random@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    3
   ],
   "quote": "5; so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.85,
   "prune_score": 0.6,
   "score": 0.51,
   "logic": "Folk meaning: 'a random number between 0 and 1' includes both ends, and a 70% chance means the event will happen next time. Java rule: Math.random() returns a double in the half-open interval [0, 1) (0 possible, 1 never), and a probability only describes long-run frequencies over many calls.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 3,
   "source": "math_random",
   "edge": "pre:math_library->math_random",
   "target": "math_library",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    3
   ],
   "quote": "5; so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.85,
   "prune_score": 1.0,
   "score": 0.85,
   "logic": "Math.random() is a Math library method; unlike the others it takes no argument and returns a random double in [0, 1).",
   "twin_logic": null,
   "consequence_of": "mis:frequency_counting->FewTrialsAreExact"
  },
  {
   "depth": 3,
   "source": "frequency_counting",
   "edge": "pre:counter_pattern->frequency_counting",
   "target": "counter_pattern",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.6,
   "prune_score": 1.0,
   "score": 0.6,
   "logic": "Frequency counting keeps one counter per value in an array, freq[page]++.",
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
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.55,
   "prune_score": 0.5,
   "score": 0.275,
   "logic": "The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.",
   "twin_logic": null
  },
  {
   "depth": 4,
   "source": "for_loop",
   "edge": "err:for_loop->WrongIterationCount",
   "target": "WrongIterationCount",
   "kind": "error",
   "label": "correct",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.75,
   "prune_score": 0.5,
   "score": 0.375,
   "logic": "Updates the loop counter so that the loop runs the wrong number of times.",
   "twin_logic": "The init, test and update together decide the number of passes; trace them to check the count.",
   "role": "primary"
  },
  {
   "depth": 4,
   "source": "for_loop",
   "edge": "mis:for_loop->ForIsConditional",
   "target": "ForIsConditional",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.65,
   "prune_score": 0.2,
   "score": 0.13,
   "logic": "The body of a for statement executes at most once.",
   "twin_logic": "The body of a for statement runs once for every pass on which the condition is true, which can be many times.",
   "role": "primary"
  },
  {
   "depth": 4,
   "source": "for_loop",
   "edge": "lvl:for_loop@L2#1",
   "target": "for_loop@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    3
   ],
   "quote": "5; so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "A for statement has no value; the passes it makes are fixed by its header: for (int i = 1; i <= N; i++) sum += i; leaves sum = N(N+1)/2, and for (int i = 2; i <= 8; i += 2) prints 2, 4, 6, 8,.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  }
 ],
 "evidence": [
  {
   "depth": 1,
   "source": "println",
   "edge": "lvl:println@L2#1",
   "target": "println@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "5",
   "confidence": 0.6,
   "prune_score": 0.5,
   "score": 0.3,
   "logic": "Output is the value's characters followed by a line break: println(\"Hello, \"); println(\"World!\"); prints two lines.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 2,
   "source": "math_random",
   "edge": "mis:math_random->ProbabilityIsPrediction",
   "target": "ProbabilityIsPrediction",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.9,
   "prune_score": 0.9,
   "score": 0.81,
   "logic": "A probability (e.g. 70%) predicts what the next single trial will do.",
   "twin_logic": "A probability describes the long-run frequency over many trials, not one outcome.",
   "role": "context"
  },
  {
   "depth": 2,
   "source": "math_random",
   "edge": "lvl:math_random@L0#0",
   "target": "math_random@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    3
   ],
   "quote": "5; so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.85,
   "prune_score": 0.6,
   "score": 0.51,
   "logic": "Folk meaning: 'a random number between 0 and 1' includes both ends, and a 70% chance means the event will happen next time. Java rule: Math.random() returns a double in the half-open interval [0, 1) (0 possible, 1 never), and a probability only describes long-run frequencies over many calls.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 2,
   "source": "loop_control",
   "edge": "err:loop_control->WrongIterationCount",
   "target": "WrongIterationCount",
   "kind": "error",
   "label": "correct",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.6,
   "prune_score": 0.45,
   "score": 0.27,
   "logic": "Updates the loop counter so that the loop runs the wrong number of times.",
   "twin_logic": "The init, test and update together decide the number of passes; trace them to check the count.",
   "role": "context"
  },
  {
   "depth": 2,
   "source": "loop_control",
   "edge": "mis:loop_control->OffByOneBound",
   "target": "OffByOneBound",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.5,
   "prune_score": 0.3,
   "score": 0.15,
   "logic": "i < n and i <= n mean the same, so the loop runs until i equals n and the last pass can use a[n].",
   "twin_logic": "for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n.",
   "role": "primary"
  },
  {
   "depth": 2,
   "source": "frequency_counting",
   "edge": "mis:frequency_counting->FewTrialsAreExact",
   "target": "FewTrialsAreExact",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.92,
   "prune_score": 0.9,
   "score": 0.828,
   "logic": "A short simulation gives the exact page ranks.",
   "twin_logic": "A simulation only estimates the page ranks: RandomSurfer needs 10^n moves to get answers precise to n decimal places and many more moves for those answers to become accurate (tens of thousands of moves for two accurate places, millions for three).",
   "role": "primary"
  },
  {
   "depth": 2,
   "source": "frequency_counting",
   "edge": "lvl:frequency_counting@L0#3",
   "target": "frequency_counting@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    3
   ],
   "quote": "5; so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.55,
   "prune_score": 0.5,
   "score": 0.275,
   "logic": "Applies LT (increment after each move, divide by T after the loop) unevenly: e.g. incrementing the page before the move on some passes, or dividing inside the loop. (here mixing in: \"A short simulation gives the exact page ranks\")",
   "twin_logic": null,
   "level": "L0",
   "way": "inconsistent_trace"
  },
  {
   "depth": 3,
   "source": "frequency_counting",
   "edge": "pre:counter_pattern->frequency_counting",
   "target": "counter_pattern",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.6,
   "prune_score": 1.0,
   "score": 0.6,
   "logic": "Frequency counting keeps one counter per value in an array, freq[page]++.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "math_random",
   "edge": "pre:math_library->math_random",
   "target": "math_library",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    3
   ],
   "quote": "5; so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.85,
   "prune_score": 1.0,
   "score": 0.85,
   "logic": "Math.random() is a Math library method; unlike the others it takes no argument and returns a random double in [0, 1).",
   "twin_logic": null,
   "consequence_of": "mis:frequency_counting->FewTrialsAreExact"
  },
  {
   "depth": 3,
   "source": "loop_control",
   "edge": "pre:loop_control->for_loop",
   "target": "for_loop",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.55,
   "prune_score": 0.5,
   "score": 0.275,
   "logic": "The for header is exactly the three control slots, and the body runs after the test and before the update on each pass.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "loop_control",
   "edge": "pre:loop_variable->loop_control",
   "target": "loop_variable",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.55,
   "prune_score": 0.3,
   "score": 0.165,
   "logic": "The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it.",
   "twin_logic": null
  },
  {
   "depth": 4,
   "source": "for_loop",
   "edge": "err:for_loop->WrongIterationCount",
   "target": "WrongIterationCount",
   "kind": "error",
   "label": "correct",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.75,
   "prune_score": 0.5,
   "score": 0.375,
   "logic": "Updates the loop counter so that the loop runs the wrong number of times.",
   "twin_logic": "The init, test and update together decide the number of passes; trace them to check the count.",
   "role": "primary"
  },
  {
   "depth": 4,
   "source": "for_loop",
   "edge": "mis:for_loop->ForIsConditional",
   "target": "ForIsConditional",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.65,
   "prune_score": 0.2,
   "score": 0.13,
   "logic": "The body of a for statement executes at most once.",
   "twin_logic": "The body of a for statement runs once for every pass on which the condition is true, which can be many times.",
   "role": "primary"
  },
  {
   "depth": 4,
   "source": "for_loop",
   "edge": "lvl:for_loop@L2#1",
   "target": "for_loop@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    3
   ],
   "quote": "5; so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "A for statement has no value; the passes it makes are fixed by its header: for (int i = 1; i <= N; i++) sum += i; leaves sum = N(N+1)/2, and for (int i = 2; i <= 8; i += 2) prints 2, 4, 6, 8,.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  }
 ],
 "clause_coverage": {
  "5": "lvl:println@L2#1",
  "Page 1 has probability 0.5": "mis:math_random->ProbabilityIsPrediction",
  "so in 10 steps the surfer goes there exactly 5 times": "mis:math_random->ProbabilityIsPrediction"
 },
 "unexplained_clauses": [],
 "stop_reason": "max depth",
 "depth_reached": 4,
 "llm_calls": 0,
 "llm_cache_hits": 70,
 "llm_calls_by_step": {
  "prune": 24,
  "label": 46
 },
 "level_v2": {
  "wrong_ways": [
   {
    "concept": "arithmetic_operators",
    "edge": "lvl:arithmetic_operators@L3#4",
    "level": "L3",
    "way": "purpose_of_the_whole",
    "clauses": [
     2,
     3
    ],
    "quote": "Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
    "confidence": 0.6
   },
   {
    "concept": "math_random",
    "edge": "lvl:math_random@L3#2",
    "level": "L3",
    "way": "relation_to_neighbour",
    "clauses": [
     2,
     3
    ],
    "quote": "Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
    "confidence": 0.8
   },
   {
    "concept": "loop_control",
    "edge": "lvl:loop_control@L3#6",
    "level": "L3",
    "way": "purpose_of_the_whole",
    "clauses": [
     2,
     3
    ],
    "quote": "Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
    "confidence": 0.75
   },
   {
    "concept": "frequency_counting",
    "edge": "lvl:frequency_counting@L3#1",
    "level": "L3",
    "way": "relation_to_neighbour",
    "clauses": [
     2,
     3
    ],
    "quote": "Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
    "confidence": 0.8
   },
   {
    "concept": "math_library",
    "edge": "lvl:math_library@L3#3",
    "level": "L3",
    "way": "relation_to_neighbour",
    "clauses": [
     2,
     3
    ],
    "quote": "Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
    "confidence": 0.6
   },
   {
    "concept": "math_library",
    "edge": "lvl:math_library@L3#6",
    "level": "L3",
    "way": "relation_to_neighbour",
    "clauses": [
     2,
     3
    ],
    "quote": "Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
    "confidence": 0.55
   },
   {
    "concept": "for_loop",
    "edge": "lvl:for_loop@L3#3",
    "level": "L3",
    "way": "relation_to_neighbour",
    "clauses": [
     2,
     3
    ],
    "quote": "Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
    "confidence": 0.6
   },
   {
    "concept": "for_loop",
    "edge": "lvl:for_loop@L3#8",
    "level": "L3",
    "way": "purpose_of_the_whole",
    "clauses": [
     3
    ],
    "quote": "so in 10 steps the surfer goes there exactly 5 times",
    "confidence": 0.6
   }
  ],
  "not_counted": []
 }
}
```
