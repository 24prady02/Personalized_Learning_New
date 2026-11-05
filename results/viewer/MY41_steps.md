# Think on the Graph: every output of the run MY41
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
Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6.
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

Figure 1: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY41_figure01.png

Figure 2: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY41_figure02.png

## 2. Clauses and start concepts (no model)
The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):
| clause | text |
|---|---|
| c1 | 5 |
| c2 | Page 1 has probability 0.5 |
| c3 | so in 10 steps the surfer goes there exactly 5 times |
| c4 | Actual: it varies from run to run |
| c5 | five runs gave 6, 4, 8, 5 and 6 |

start: generic concepts whose tagging text occurs in the answer: statement

start: BM25 of the answer against each tagged concept: arithmetic_operators 36.94 (hits 1), compound_assignment 21.00 (hits 1), println 19.01 (hits 1), loop_control 17.39 (hits 2), for_loop 16.18 (hits 1), math_random 14.71 (hits 1), loop_body 13.73 (hits 1), statement 11.36 (hits 1), nested_loops 11.05 (hits 1), loop_variable 10.76 (hits 1), frequency_counting 10.00 (hits 2), control_flow 9.42 (hits 1), increment_operators 9.37 (hits 1), while_loop 8.43 (hits 1), array_creation 7.93 (hits 1), method_call 6.96 (hits 1), counter_pattern 6.62 (hits 1), boolean_expression 5.77 (hits 2), indexing 5.64 (hits 1), loop_scope 4.68 (hits 1), accumulator_pattern 4.43 (hits 1), math_library 3.63 (hits 1), array_initializer 3.60 (hits 1), array_default_values 2.81 (hits 1), array_declaration 2.01 (hits 1), comparison_operators 1.63 (hits 1), api 1.50 (hits 1), data_structure 0.53 (hits 1)

start: chosen arithmetic_operators, compound_assignment, println

start concepts (3): arithmetic_operators, compound_assignment, println

Start concepts: arithmetic_operators, compound_assignment, println

Figure 3: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY41_figure03.png

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
mis:arithmetic_operators->CaretIsPower (0.34), mis:arithmetic_operators->ArithmeticOnNumericStrings (0.33), mis:arithmetic_operators->RemainderIsSubtraction (0.33)
```
Kept by pruning: mis:arithmetic_operators->CaretIsPower (0.34), mis:arithmetic_operators->ArithmeticOnNumericStrings (0.33), mis:arithmetic_operators->RemainderIsSubtraction (0.33)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:arithmetic_operators->CaretIsPower \| wrong rule: a^2 computes a squared. \| right rule: Java has no exponent operator; ^ is exclusive or, and a * a or Math.pow(a, 2) computes a squared. |
| mis:arithmetic_operators->ArithmeticOnNumericStrings \| wrong rule: "10" - 1 or "6" * "2" works because the strings look like numbers. \| right rule: Arithmetic operators other than + are not defined for Strings; a String of digits must first be converted to a number, e.g. with Integer.parseInt. |
| mis:arithmetic_operators->RemainderIsSubtraction \| wrong rule: 9 % 5 means 9 minus 5 (a % b subtracts b from a). \| right rule: % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 * 5 + 4, and 17 % 5 is 2, not 12. |
Model's reply:
```
mis:arithmetic_operators->CaretIsPower | not applied | clauses: none | confidence: 0.97
mis:arithmetic_operators->ArithmeticOnNumericStrings | not applied | clauses: none | confidence: 0.97
mis:arithmetic_operators->RemainderIsSubtraction | not applied | clauses: none | confidence: 0.97
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:arithmetic_operators->CaretIsPower | not applied |  |  | 0.0 |  |  |
| mis:arithmetic_operators->ArithmeticOnNumericStrings | not applied |  |  | 0.0 |  |  |
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
{lvl:arithmetic_operators@L2#1 (Score: 0.4)}
{lvl:arithmetic_operators@L3#4 (Score: 0.35)}
{lvl:arithmetic_operators@L0#0 (Score: 0.25)}
```
Kept by pruning: lvl:arithmetic_operators@L2#1 (0.40), lvl:arithmetic_operators@L3#4 (0.35), lvl:arithmetic_operators@L0#0 (0.25)

Label prompt for level way lvl:arithmetic_operators@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> With ints, 17 / 3 is 5 and 17 % 3 is 2. With doubles, 5.0 / 3.0 is 1.6666666666666667. With mixed operands, the int is promoted first (10 / 3.0 is 3.333...).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:arithmetic_operators@L3#4 (the model saw only the concept, the way's name 'purpose of the whole' and its text; no level):
> Arithmetic operators turn formulas into code: totals, averages, unit conversions (inch * CM_PER_INCH), and digit extraction (n % 10, n / 10).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.75
```

Label prompt for level way lvl:arithmetic_operators@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> In maths notation, multiplication can be implicit (2x), ^ or a superscript means a power, ÷ is exact division, and % means percent. In Java * must be written, / depends on the operand types, % is the remainder, and there is no power operator (^ is exclusive or).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:arithmetic_operators@L2#1 | not applied |  |  | 0.0 |  |  |
| lvl:arithmetic_operators@L3#4 | not applied |  |  | 0.0 |  |  |
| lvl:arithmetic_operators@L0#0 | not applied |  |  | 0.0 |  |  |

#### compound_assignment, misconceptions: 2 edges offered
Edges offered:
| edge |
|---|
| mis:compound_assignment->CompoundAssignmentNoCast \| wrong rule: x += 0.5 adds one half to an int x. \| right rule: x += 0.5 is x = (int) (x + 0.5), so an int x does not change. |
| mis:compound_assignment->CompoundSubtractIsAssignNegative \| wrong rule: x[i] -= y sets x[i] to -y (reads -= as assignment of a negated value). \| right rule: x[i] -= y means x[i] = x[i] - y: it subtracts y from the current value. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:compound_assignment->CompoundAssignmentNoCast (Score: 0.6)}
{mis:compound_assignment->CompoundSubtractIsAssignNegative (Score: 0.4)}
```
Kept by pruning: mis:compound_assignment->CompoundAssignmentNoCast (0.60), mis:compound_assignment->CompoundSubtractIsAssignNegative (0.40)

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
{lvl:compound_assignment@L0#0 (Score: 0.5)}
{lvl:compound_assignment@L3#3 (Score: 0.3)}
{lvl:compound_assignment@L2#1 (Score: 0.2)}
```
Kept by pruning: lvl:compound_assignment@L0#0 (0.50), lvl:compound_assignment@L3#3 (0.30), lvl:compound_assignment@L2#1 (0.20)

Label prompt for level way lvl:compound_assignment@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: x -= y reads as 'x equals minus y' and x += 0.5 as 'add a half' in arithmetic. In Java x op= e means x = (T) (x op e): it updates x from its current value and casts the result back to x's type.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.92
```

Label prompt for level way lvl:compound_assignment@L3#3 (the model saw only the concept, the way's name 'purpose of the whole' and its text; no level):
> Plan/role: the update step of a gatherer (sum += a[i], product *= i) or of a stepper with a step other than 1 (i += 2).

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
Confidence: 0.92
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
mis:println->PrintedTextIsExecuted (0.40), mis:println->PrintNewLineFirst (0.35), err:println->PrintWithoutFinalNewline (0.25)
```
Kept by pruning: mis:println->PrintedTextIsExecuted (0.40), mis:println->PrintNewLineFirst (0.35), err:println->PrintWithoutFinalNewline (0.25)

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
{lvl:println@L3#4 (Score: 0.3)}
{lvl:println@L2#0 (Score: 0.2)}
```
Kept by pruning: lvl:println@L2#1 (0.50), lvl:println@L3#4 (0.30), lvl:println@L2#0 (0.20)

Label prompt for level way lvl:println@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> Output is the value's characters followed by a line break: println("Hello, "); println("World!"); prints two lines.

Model's reply:
```
Label: shown
Clauses: 1, 5
Confidence: 0.55
```

Label prompt for level way lvl:println@L3#4 (the model saw only the concept, the way's name 'purpose of the whole' and its text; no level):
> Purpose: produce one complete line of output, e.g. each result on its own line, or end a line built with print.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:println@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Evaluate the argument, print its characters at the current position, then write the line separator so the cursor moves to the beginning of the next line.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:println@L2#1 | shown | 0.5 | 0.55 | 0.28 | c1, c5 | 5; five runs gave 6, 4, 8, 5 and 6 |
| lvl:println@L3#4 | not applied |  |  | 0.0 |  |  |
| lvl:println@L2#0 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

lvl:println@L2#1 [shown, tier 2, 0.28]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | 5 | not covered yet |
| c2 | Page 1 has probability 0.5 | not covered yet |
| c3 | so in 10 steps the surfer goes there exactly 5 times | not covered yet |
| c4 | Actual: it varies from run to run | not covered yet |
| c5 | five runs gave 6, 4, 8, 5 and 6 | not covered yet |

**Uncovered clauses bring in (BM25 of the uncovered clauses against unvisited concepts):** loop_control (16.79), for_loop (15.53), math_random (13.94)

**Graph check, not yet read (the walk may not stop while these remain):** own edges of for_loop, own edges of loop_control, own edges of math_random, par:increment_operators~compound_assignment, pre:arithmetic_operators->expression, pre:assignment->compound_assignment, pre:compound_assignment->accumulator_pattern, pre:statement->println

Figure 4 (the graph after depth 1): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY41_figure04.png

### Depth 2: current concepts 'arithmetic_operators', 'compound_assignment', 'println', 'loop_control', 'for_loop', 'math_random'

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
{pre:compound_assignment->accumulator_pattern (Score: 0.4)}
{par:increment_operators~compound_assignment (Score: 0.35)}
{pre:assignment->compound_assignment (Score: 0.25)}
```
Kept by pruning: pre:compound_assignment->accumulator_pattern (0.40), par:increment_operators~compound_assignment (0.35), pre:assignment->compound_assignment (0.25)

Label prompt for concept edge pre:compound_assignment->accumulator_pattern (compound_assignment -> accumulator_pattern, prerequisite):
> sum += x is the usual way a running total is updated on each pass.

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

Label prompt for concept edge pre:assignment->compound_assignment (assignment -> compound_assignment, prerequisite):
> x op= e is shorthand for the assignment x = x op e.

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
| par:increment_operators~compound_assignment | not applied |  |  | 0.0 |  |  |
| pre:assignment->compound_assignment | not applied |  |  | 0.0 |  |  |

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
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:statement->println | not applied |  |  | 0.0 |  |  |

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
err:loop_control->WrongIterationCount (0.45), mis:loop_control->OffByOneBound (0.35), mis:loop_control->IdiomOverridesCode (0.20)
```
Kept by pruning: err:loop_control->WrongIterationCount (0.45), mis:loop_control->OffByOneBound (0.35), mis:loop_control->IdiomOverridesCode (0.20)

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
| mis:loop_control->OffByOneBound | correct | 0.35 | 0.5 | 0.17 | c3 | so in 10 steps the surfer goes there exactly 5 times |
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
{lvl:loop_control@L2#1 (Score: 0.5)}
{lvl:loop_control@L3#6 (Score: 0.3)}
{lvl:loop_control@L1#0 (Score: 0.2)}
```
Kept by pruning: lvl:loop_control@L2#1 (0.50), lvl:loop_control@L3#6 (0.30), lvl:loop_control@L1#0 (0.20)

Label prompt for level way lvl:loop_control@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> The number of passes and the values seen follow from the three parts: for (int i = 0; i <= N; i++) makes N+1 passes with i = 0..N; with i < N it makes N passes; i += 2 visits every second value.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Label prompt for level way lvl:loop_control@L3#6 (the model saw only the concept, the way's name 'purpose of the whole' and its text; no level):
> Plan: counter-controlled loop - the loop variable is a stepper that walks a predictable sequence of values (0..N-1, 1..N, every 2nd value) and fixes the number of passes in advance.

Model's reply:
```
Label: shown
Clauses: 3
Confidence: 0.55
```

Label prompt for level way lvl:loop_control@L1#0 (the model saw only the concept, the way's name 'names the element' and its text; no level):
> Loop control is the init / continuation condition / increment scheme on an index variable that decides how many passes a loop makes and with which values.

Model's reply:
```
Label: shown
Clauses: 3
Confidence: 0.55
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:loop_control@L2#1 | not applied |  |  | 0.0 |  |  |
| lvl:loop_control@L3#6 | shown | 0.3 | 0.55 | 0.17 | c3 | so in 10 steps the surfer goes there exactly 5 times |
| lvl:loop_control@L1#0 | shown | 0.2 | 0.55 | 0.11 | c3 | so in 10 steps the surfer goes there exactly 5 times |

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
err:for_loop->WrongIterationCount (0.50), mis:for_loop->ForIsConditional (0.30), mis:for_loop->LoopCountIsStatementCount (0.20)
```
Kept by pruning: err:for_loop->WrongIterationCount (0.50), mis:for_loop->ForIsConditional (0.30), mis:for_loop->LoopCountIsStatementCount (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| err:for_loop->WrongIterationCount \| wrong rule: Updates the loop counter so that the loop runs the wrong number of times. \| right rule: The init, test and update together decide the number of passes; trace them to check the count. |
| mis:for_loop->ForIsConditional \| wrong rule: The body of a for statement executes at most once. \| right rule: The body of a for statement runs once for every pass on which the condition is true, which can be many times. |
| mis:for_loop->LoopCountIsStatementCount \| wrong rule: The repeat count of a counted loop says how many of the body statements are executed. \| right rule: The repeat count is how many times the whole body runs; every pass runs all body statements. |
Model's reply:
```
mis:for_loop->ForIsConditional | correct | clauses: 3 | confidence: 0.6
err:for_loop->WrongIterationCount | correct | clauses: 3 | confidence: 0.6
mis:for_loop->LoopCountIsStatementCount | not applied | clauses: none | confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| err:for_loop->WrongIterationCount | correct | 0.5 | 0.6 | 0.3 | c3 | so in 10 steps the surfer goes there exactly 5 times |
| mis:for_loop->ForIsConditional | correct | 0.3 | 0.6 | 0.18 | c3 | so in 10 steps the surfer goes there exactly 5 times |
| mis:for_loop->LoopCountIsStatementCount | not applied |  |  | 0.0 |  |  |

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
{lvl:for_loop@L3#3 (Score: 0.5)}
{lvl:for_loop@L3#8 (Score: 0.3)}
{lvl:for_loop@L0#0 (Score: 0.2)}
```
Kept by pruning: lvl:for_loop@L3#3 (0.50), lvl:for_loop@L3#8 (0.30), lvl:for_loop@L0#0 (0.20)

Label prompt for level way lvl:for_loop@L3#3 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> A simulation runs a fixed number of trials with an outer for loop (for (int t = 0; t < T; t++)), each trial simulated inside the body.

Model's reply:
```
Label: shown
Clauses: 3
Confidence: 0.6
```

Label prompt for level way lvl:for_loop@L3#8 (the model saw only the concept, the way's name 'purpose of the whole' and its text; no level):
> Plan: counted loop / counter-controlled repetition - do the body a known number of times, with the loop variable as a stepper (index, term number, trial number).

Model's reply:
```
Label: shown
Clauses: 3
Confidence: 0.6
```

Label prompt for level way lvl:for_loop@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: English 'for each ...' or 'for 10 times' names a whole collection or a count to be handled at once, and a maths reading treats the header as simultaneous conditions. A Java for is a while loop in compact form: one init, then test-body-update repeated, one pass at a time.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:for_loop@L3#3 | shown | 0.5 | 0.6 | 0.3 | c3 | so in 10 steps the surfer goes there exactly 5 times |
| lvl:for_loop@L3#8 | shown | 0.3 | 0.6 | 0.18 | c3 | so in 10 steps the surfer goes there exactly 5 times |
| lvl:for_loop@L0#0 | not applied |  |  | 0.0 |  |  |

#### math_random, misconceptions: 2 edges offered
Edges offered:
| edge |
|---|
| mis:math_random->ProbabilityIsPrediction \| wrong rule: A probability (e.g. 70%) predicts what the next single trial will do. \| right rule: A probability describes the long-run frequency over many trials, not one outcome. |
| mis:math_random->RandomCanReturnOne \| wrong rule: Math.random() can return exactly 1.0. \| right rule: Math.random() returns a value in [0, 1): 0 is possible, 1 is not. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:math_random->ProbabilityIsPrediction (0.95), mis:math_random->RandomCanReturnOne (0.05)
```
Kept by pruning: mis:math_random->ProbabilityIsPrediction (0.95), mis:math_random->RandomCanReturnOne (0.05)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:math_random->ProbabilityIsPrediction \| wrong rule: A probability (e.g. 70%) predicts what the next single trial will do. \| right rule: A probability describes the long-run frequency over many trials, not one outcome. |
| mis:math_random->RandomCanReturnOne \| wrong rule: Math.random() can return exactly 1.0. \| right rule: Math.random() returns a value in [0, 1): 0 is possible, 1 is not. |
Model's reply:
```
mis:math_random->ProbabilityIsPrediction | held | clauses: 1, 2, 3 | confidence: 0.85
mis:math_random->RandomCanReturnOne | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:math_random->ProbabilityIsPrediction | held | 0.95 | 0.85 | 0.81 | c1, c2, c3 | 5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |
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
{lvl:math_random@L3#2 (Score: 0.2)}
{lvl:math_random@L4#0 (Score: 0.2)}
```
Kept by pruning: lvl:math_random@L0#0 (0.60), lvl:math_random@L3#2 (0.20), lvl:math_random@L4#0 (0.20)

Label prompt for level way lvl:math_random@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: 'a random number between 0 and 1' includes both ends, and a 70% chance means the event will happen next time. Java rule: Math.random() returns a double in the half-open interval [0, 1) (0 possible, 1 never), and a probability only describes long-run frequencies over many calls.

Model's reply:
```
Label: shown
Clauses: 1, 3
Confidence: 0.85
```

Label prompt for level way lvl:math_random@L3#2 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Each trial of a Monte Carlo simulation draws fresh values with Math.random(); estimates become reliable only over many trials.

Model's reply:
```
Label: shown
Clauses: 4, 5
Confidence: 0.6
```

Label prompt for level way lvl:math_random@L4#0 (the model saw only the concept, the way's name 'predict a change' and its text; no level):
> Changing N in (int) (Math.random() * N) changes the range to 0..N-1, and adding a constant shifts it; the output changes from run to run, so a program using Math.random() cannot be checked by comparing exact outputs, only by statistics over many runs.

Model's reply:
```
Label: shown
Clauses: 4, 5
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:math_random@L0#0 | shown | 0.6 | 0.85 | 0.51 | c1, c3 | 5; so in 10 steps the surfer goes there exactly 5 times |
| lvl:math_random@L3#2 | shown | 0.2 | 0.6 | 0.12 | c4, c5 | Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6 |
| lvl:math_random@L4#0 | shown | 0.2 | 0.6 | 0.12 | c4, c5 | Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6 |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:math_random->ProbabilityIsPrediction [held, tier 0, 0.81], lvl:math_random@L0#0 [shown, tier 2, 0.51], err:for_loop->WrongIterationCount [correct, tier 2, 0.30]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | 5 | mis:math_random->ProbabilityIsPrediction |
| c2 | Page 1 has probability 0.5 | mis:math_random->ProbabilityIsPrediction |
| c3 | so in 10 steps the surfer goes there exactly 5 times | err:loop_control->WrongIterationCount |
| c4 | Actual: it varies from run to run | not covered yet |
| c5 | five runs gave 6, 4, 8, 5 and 6 | not covered yet |

**Uncovered clauses bring in (BM25 of the uncovered clauses against unvisited concepts):** statement (8.79), loop_body (8.29), nested_loops (8.27)

**Graph check, not yet read (the walk may not stop while these remain):** own edges of loop_body, own edges of nested_loops, own edges of statement, pre:for_loop->loop_body, pre:for_loop->loop_scope, pre:for_loop->nested_loops, pre:loop_control->for_loop, pre:loop_control->increment_operators, pre:loop_variable->loop_control, pre:math_library->math_random, pre:while_loop->loop_control

Figure 5 (the graph after depth 2): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY41_figure05.png

### Depth 3: current concepts 'math_random', 'loop_control', 'for_loop', 'statement', 'loop_body', 'nested_loops'

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
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:math_library->math_random | broken | 1.0 | 0.8 | 0.8 | c1, c3 | 5; so in 10 steps the surfer goes there exactly 5 times |

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

#### for_loop, concept edges: 3 edges offered
Edges offered:
| edge |
|---|
| pre:for_loop->loop_body \| rule: The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop. |
| pre:for_loop->loop_scope \| rule: A variable declared in the for header exists only from its declaration to the end of the for statement's block. |
| pre:for_loop->nested_loops \| rule: In nested loops the inner for runs its complete set of passes for every single pass of the outer for. |
| pre:loop_control->for_loop \| rule: The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:for_loop->loop_body (Score: 0.7)}
{pre:for_loop->nested_loops (Score: 0.2)}
{pre:for_loop->loop_scope (Score: 0.1)}
```
Kept by pruning: pre:for_loop->loop_body (0.70), pre:for_loop->nested_loops (0.20), pre:for_loop->loop_scope (0.10)

Label prompt for concept edge pre:for_loop->loop_body (for_loop -> loop_body, prerequisite):
> The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop.

Model's reply:
```
Label: confirmed
Clauses: 3, 5
Confidence: 0.7
```

Label prompt for concept edge pre:for_loop->nested_loops (for_loop -> nested_loops, prerequisite):
> In nested loops the inner for runs its complete set of passes for every single pass of the outer for.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.85
```

Label prompt for concept edge pre:for_loop->loop_scope (for_loop -> loop_scope, prerequisite):
> A variable declared in the for header exists only from its declaration to the end of the for statement's block.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.92
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:for_loop->loop_body | confirmed | 0.7000000000000001 | 0.7 | 0.49 | c3, c5 | so in 10 steps the surfer goes there exactly 5 times; five runs gave 6, 4, 8, 5 and 6 |
| pre:for_loop->nested_loops | not applied |  |  | 0.0 |  |  |
| pre:for_loop->loop_scope | not applied |  |  | 0.0 |  |  |

#### statement, misconceptions: 5 edges offered
Edges offered:
| edge |
|---|
| err:statement->StatementNeedsNoTerminator \| wrong rule: A statement still compiles and runs if the semicolon at its end is left out, or if a stray ; is put right after if (c) or for (...). \| right rule: Each statement must end with ;, otherwise javac reports ';' expected. |
| mis:statement->ComputerFillsInIntent \| wrong rule: The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. \| right rule: The computer executes only what the code states; every needed step and value must be written. |
| mis:statement->ProgramLooksAhead \| wrong rule: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. \| right rule: Each statement executes using only the current state; later lines have no effect until control reaches them. |
| mis:statement->StatementsRunInAnyOrder \| wrong rule: Statements in a program can run in any order. \| right rule: Without control statements, statements run once each, top to bottom. |
| mis:statement->WhitespaceIsSignificant \| wrong rule: Line breaks and indentation change what the program does, so each statement must be on its own line. \| right rule: Java compilers consider all whitespace in program text (outside quotation marks) to be equivalent; layout is for human readers. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:statement->ComputerFillsInIntent (Score: 0.55)}
{mis:statement->ProgramLooksAhead (Score: 0.35)}
{mis:statement->StatementsRunInAnyOrder (Score: 0.1)}
```
Kept by pruning: mis:statement->ComputerFillsInIntent (0.55), mis:statement->ProgramLooksAhead (0.35), mis:statement->StatementsRunInAnyOrder (0.10)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:statement->ComputerFillsInIntent \| wrong rule: The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. \| right rule: The computer executes only what the code states; every needed step and value must be written. |
| mis:statement->ProgramLooksAhead \| wrong rule: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. \| right rule: Each statement executes using only the current state; later lines have no effect until control reaches them. |
| mis:statement->StatementsRunInAnyOrder \| wrong rule: Statements in a program can run in any order. \| right rule: Without control statements, statements run once each, top to bottom. |
Model's reply:
```
mis:statement->ComputerFillsInIntent | not applied | clauses: none | confidence: 0.8
mis:statement->ProgramLooksAhead | not applied | clauses: none | confidence: 0.85
mis:statement->StatementsRunInAnyOrder | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:statement->ComputerFillsInIntent | not applied |  |  | 0.0 |  |  |
| mis:statement->ProgramLooksAhead | not applied |  |  | 0.0 |  |  |
| mis:statement->StatementsRunInAnyOrder | not applied |  |  | 0.0 |  |  |

#### statement, level ways: 19 edges offered
Edges offered:
| edge |
|---|
| lvl:statement@L0#0 \| level L0 way everyday_reading: Everyday reading: a program is read like a text or a list of wishes that the computer takes in all at once, so line order, goals of later lines or what the writer meant can matter. Java rule: each statement is one step, ended by ;, executed once, in written order, using only the current state. |
| lvl:statement@L0#2 \| level L0 way inconsistent_trace: Applies the sequencing rule (LT) unevenly: executes the statements in order on some lines but lets a later statement's effect leak into an earlier one, or skips or repeats a statement on one pass. (here mixing in: "The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command") |
| lvl:statement@L1#0 \| level L1 way names_the_element: A statement is one step of a program (a declaration, assignment, method call such as System.out.println(...), or control statement), ended by a semicolon when it is a simple statement. |
| lvl:statement@L1#1 \| level L1 way states_the_rule: A method body is a sequence of statements enclosed in braces and each followed by a semicolon; statements are executed for their effect and have no value; an expression statement evaluates its expression and discards any value. |
| lvl:statement@L2#0 \| level L2 way line_by_line_trace: Statements run one at a time, from first to last; each completes (normally or abruptly) before the next starts. |
| lvl:statement@L2#1 \| level L2 way output_prediction: A statement has no value; its result is its effect: a changed variable, printed output, or a change of control flow. |
| lvl:statement@L2#2 \| level L2 way one_step_execution: Executing one statement applies its single effect to the current state (e.g. prints one string, or stores one value) and then control moves to the next statement. |
| lvl:statement@L3#0 \| level L3 way relation_to_neighbour: Statements live in main's body; running the program executes main's statements in order. |
| lvl:statement@L3#1 \| level L3 way relation_to_neighbour: A block groups a sequence of statements in braces; the body of main() is such a block. |
| lvl:statement@L3#2 \| level L3 way relation_to_neighbour: System.out.print(s); is a statement, so its output appears exactly at its place in the sequence, with no newline. |
| lvl:statement@L3#3 \| level L3 way relation_to_neighbour: System.out.println(s); is a statement, so its line of output appears at its place in the sequence; swapping two println statements swaps the output lines. |
| lvl:statement@L3#4 \| level L3 way relation_to_neighbour: Control flow is the order in which statements run; without control statements it is straight-line, each once in order. |
| lvl:statement@L3#5 \| level L3 way relation_to_neighbour: A lone ; is the empty statement, which does nothing; it can fill a for-loop part or, by accident, end an if or loop header. |
| lvl:statement@L3#6 \| level L3 way relation_to_neighbour: An algorithm becomes a program as a sequence of statements, executed once each in the order given. |
| lvl:statement@L3#7 \| level L3 way purpose_of_the_whole: Purpose: a statement is the unit of action; a program is characterized by its sequence of statements, each doing one step of the algorithm. |
| lvl:statement@L4#0 \| level L4 way predict_a_change: Swapping two statements that touch the same variable or the output generally changes the result; swapping independent statements, or changing only whitespace between them, keeps it. |
| lvl:statement@L4#1 \| level L4 way diagnose_an_error: rule broken: Each simple statement must end with ;. Kind: compile-time. Trigger class: omitting the ; at the end of a statement: javac reports ';' expected (often at the end of that line or the next) |
| lvl:statement@L4#2 \| level L4 way transfer_to_a_new_program: Write one statement per step and order them as the algorithm requires; straight-line sequence suffices when every step runs once, otherwise use conditionals or loops. |
| lvl:statement@L4#3 \| level L4 way diagnose_an_error: rule broken: A ; directly after an if/while/for header is an empty statement. Kind: silent logic error. Trigger class: if (x > 0); or while (cond); followed by the intended body |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:statement@L0#0 (Score: 0.6)}
{lvl:statement@L0#2 (Score: 0.3)}
{lvl:statement@L2#0 (Score: 0.1)}
```
Kept by pruning: lvl:statement@L0#0 (0.60), lvl:statement@L0#2 (0.30), lvl:statement@L2#0 (0.10)

Label prompt for level way lvl:statement@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Everyday reading: a program is read like a text or a list of wishes that the computer takes in all at once, so line order, goals of later lines or what the writer meant can matter. Java rule: each statement is one step, ended by ;, executed once, in written order, using only the current state.

Model's reply:
```
Label: shown
Clauses: 1, 2, 3
Confidence: 0.6
```

Label prompt for level way lvl:statement@L0#2 (the model saw only the concept, the way's name 'inconsistent trace' and its text; no level):
> Applies the sequencing rule (LT) unevenly: executes the statements in order on some lines but lets a later statement's effect leak into an earlier one, or skips or repeats a statement on one pass. (here mixing in: "The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command")

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.75
```

Label prompt for level way lvl:statement@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Statements run one at a time, from first to last; each completes (normally or abruptly) before the next starts.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:statement@L0#0 | shown | 0.6000000000000001 | 0.6 | 0.36 | c1, c2, c3 | 5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |
| lvl:statement@L0#2 | not applied |  |  | 0.0 |  |  |
| lvl:statement@L2#0 | not applied |  |  | 0.0 |  |  |

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
mis:loop_body->ComputerFillsInIntent (0.50), mis:loop_body->LoopOutputSameEachPass (0.30), mis:loop_body->IfInLoopUnchecked (0.20)
```
Kept by pruning: mis:loop_body->ComputerFillsInIntent (0.50), mis:loop_body->LoopOutputSameEachPass (0.30), mis:loop_body->IfInLoopUnchecked (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:loop_body->ComputerFillsInIntent \| wrong rule: The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. \| right rule: The computer executes only what the code states; every needed step and value must be written. |
| mis:loop_body->LoopOutputSameEachPass \| wrong rule: A loop prints the same thing on every pass; the changing loop variable does not affect what the body does. \| right rule: The body uses the current value of the loop variable, so its output can differ on each pass. |
| mis:loop_body->IfInLoopUnchecked \| wrong rule: An if inside a loop body runs its branch on every pass without testing its condition. \| right rule: The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true. |
Model's reply:
```
mis:loop_body->ComputerFillsInIntent | not applied | clauses: none | confidence: 0.7
mis:loop_body->LoopOutputSameEachPass | not applied | clauses: none | confidence: 0.75
mis:loop_body->IfInLoopUnchecked | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:loop_body->ComputerFillsInIntent | not applied |  |  | 0.0 |  |  |
| mis:loop_body->LoopOutputSameEachPass | not applied |  |  | 0.0 |  |  |
| mis:loop_body->IfInLoopUnchecked | not applied |  |  | 0.0 |  |  |

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
{lvl:loop_body@L0#0 (Score: 0.45)}
{lvl:loop_body@L3#3 (Score: 0.35)}
{lvl:loop_body@L2#1 (Score: 0.2)}
```
Kept by pruning: lvl:loop_body@L0#0 (0.45), lvl:loop_body@L3#3 (0.35), lvl:loop_body@L2#1 (0.20)

Label prompt for level way lvl:loop_body@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: an everyday 'repeat this' instruction can be read loosely - a helper fills in missing steps, does each step N times in turn, or stops partway. A Java loop body is exactly the statements inside its braces (or one statement), all executed in order on every pass.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:loop_body@L3#3 (the model saw only the concept, the way's name 'purpose of the whole' and its text; no level):
> Plan: the body is the 'process one item / one step' part of a loop plan: each pass performs the same process on a new value (next element, next bet, next term).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Label prompt for level way lvl:loop_body@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> The body's output on each pass depends on the current values, so successive passes can print different lines: TenHellos prints '4th Hello', '5th Hello', ...; the number of executions of each body statement equals the number of passes.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:loop_body@L0#0 | not applied |  |  | 0.0 |  |  |
| lvl:loop_body@L3#3 | not applied |  |  | 0.0 |  |  |
| lvl:loop_body@L2#1 | not applied |  |  | 0.0 |  |  |

#### nested_loops, misconceptions: 8 edges offered
Edges offered:
| edge |
|---|
| err:nested_loops->BracelessMultiStatementBody \| wrong rule: Indenting several statements under an if or for makes them all part of its body, even without braces. \| right rule: Without braces only the first statement belongs to the if/for; the rest run once, after it. |
| mis:nested_loops->EmptyInnerLoopSkipsRest \| wrong rule: If the inner loop runs zero times, the rest of that outer pass is skipped too. \| right rule: An inner loop that runs zero times just ends; the statements after it in the outer body still run. |
| mis:nested_loops->InconsistentIndentation \| wrong rule: Indents nested blocks inconsistently, so the visual nesting differs from the real nesting. \| right rule: Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation. |
| mis:nested_loops->InnerCounterOverwritesOuter \| wrong rule: The inner loop count replaces the outer loop count, so the nested loops run as one loop. \| right rule: The two counts multiply: the inner body runs (outer passes) x (inner passes) times. |
| mis:nested_loops->InnerOuterSwapped \| wrong rule: The inner loop's variable changes more slowly than the outer loop's. \| right rule: The inner loop runs all its passes for each single pass of the outer loop. |
| mis:nested_loops->NestedLoopsLockstep \| wrong rule: Nested loops run in step as one loop: both variables change together and both conditions are tested together. \| right rule: For each pass of the outer loop the inner loop runs all its passes; the inner variable changes fastest. |
| mis:nested_loops->NestedLoopsSequential \| wrong rule: The outer loop runs completely, then the inner loop runs completely. \| right rule: The inner loop runs all its passes during each single pass of the outer loop. |
| mis:nested_loops->OuterLoopIgnored \| wrong rule: In nested loops only the inner loop repeats; the outer loop runs once. \| right rule: The outer loop repeats as its own condition says, and the inner loop runs fully on each outer pass. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:nested_loops->OuterLoopIgnored (0.50), mis:nested_loops->NestedLoopsSequential (0.30), mis:nested_loops->EmptyInnerLoopSkipsRest (0.20)
```
Kept by pruning: mis:nested_loops->OuterLoopIgnored (0.50), mis:nested_loops->NestedLoopsSequential (0.30), mis:nested_loops->EmptyInnerLoopSkipsRest (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:nested_loops->OuterLoopIgnored \| wrong rule: In nested loops only the inner loop repeats; the outer loop runs once. \| right rule: The outer loop repeats as its own condition says, and the inner loop runs fully on each outer pass. |
| mis:nested_loops->NestedLoopsSequential \| wrong rule: The outer loop runs completely, then the inner loop runs completely. \| right rule: The inner loop runs all its passes during each single pass of the outer loop. |
| mis:nested_loops->EmptyInnerLoopSkipsRest \| wrong rule: If the inner loop runs zero times, the rest of that outer pass is skipped too. \| right rule: An inner loop that runs zero times just ends; the statements after it in the outer body still run. |
Model's reply:
```
mis:nested_loops->OuterLoopIgnored | correct | clauses: 3 | confidence: 0.6
mis:nested_loops->NestedLoopsSequential | not applied | clauses: none | confidence: 0.8
mis:nested_loops->EmptyInnerLoopSkipsRest | not applied | clauses: none | confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:nested_loops->OuterLoopIgnored | correct | 0.5 | 0.6 | 0.3 | c3 | so in 10 steps the surfer goes there exactly 5 times |
| mis:nested_loops->NestedLoopsSequential | not applied |  |  | 0.0 |  |  |
| mis:nested_loops->EmptyInnerLoopSkipsRest | not applied |  |  | 0.0 |  |  |

#### nested_loops, level ways: 17 edges offered
Edges offered:
| edge |
|---|
| lvl:nested_loops@L0#0 \| level L0 way everyday_reading: Folk meaning: 'for each row and each column' sounds like doing two things side by side or one after the other. In Java the inner loop is a statement in the outer body, so it runs all its passes during each single outer pass (like the hands of a clock). |
| lvl:nested_loops@L0#7 \| level L0 way inconsistent_trace: Applies the nested-loop rule (LT) unevenly: resets the inner variable on some outer passes but not others, or advances the outer variable in the middle of the inner loop. (here mixing in: "The outer loop runs completely, then the inner loop runs completely") |
| lvl:nested_loops@L1#0 \| level L1 way names_the_element: Nested loops are a loop inside the body of another loop: the outer loop and the inner loop. |
| lvl:nested_loops@L1#1 \| level L1 way states_the_rule: Because loops are statements, one can be the body of another; the inner loop iterates all the way through for each iteration of the outer loop. |
| lvl:nested_loops@L2#0 \| level L2 way line_by_line_trace: Outer init; outer test; [inner init; inner test; inner body; inner update; ... until the inner test fails]; rest of the outer body; outer update; outer test; ... The inner init runs again on every outer pass. |
| lvl:nested_loops@L2#1 \| level L2 way output_prediction: The inner body runs (outer passes) x (inner passes) times: two loops of 1..10 call printf 100 times; DivisorPattern 3 prints 3 rows of 3 entries, each row ending with its row number. |
| lvl:nested_loops@L2#2 \| level L2 way one_step_execution: One outer pass resets the inner variable, runs the complete inner loop, executes the rest of the outer body once, and then updates the outer variable once. |
| lvl:nested_loops@L3#0 \| level L3 way relation_to_neighbour: Usually both loops are for loops: the inner for runs its complete set of passes for every single pass of the outer for. |
| lvl:nested_loops@L3#1 \| level L3 way relation_to_neighbour: Matrix addition uses two nested loops over i and j; matrix multiplication adds a third, innermost loop over k for each dot product. |
| lvl:nested_loops@L3#2 \| level L3 way relation_to_neighbour: A plain break ends only the innermost loop; a labeled break is needed when the inner loop must end the outer one too. |
| lvl:nested_loops@L3#3 \| level L3 way relation_to_neighbour: Which loop is outside decides the visiting order: row index outside gives row-major order, column index outside gives column-major order. |
| lvl:nested_loops@L3#4 \| level L3 way purpose_of_the_whole: Plan: process every pair (i, j) - two-dimensional tables, every row x column of a matrix, every pair of elements; the outer variable is a slow stepper, the inner a fast stepper. |
| lvl:nested_loops@L4#0 \| level L4 way predict_a_change: Swapping the outer and inner loops visits the same pairs in a different order (rows vs columns), which preserves a sum but changes printed layout; moving a statement between the inner body and the outer body changes its count from (outer x inner) to outer. |
| lvl:nested_loops@L4#1 \| level L4 way transfer_to_a_new_program: Use nested loops when the work ranges over all combinations of two indices (tables, matrices, pairs); expect running time proportional to the product of the pass counts, and prefer a single loop when the second index is a function of the first. |
| lvl:nested_loops@L4#2 \| level L4 way diagnose_an_error: rule broken: Without braces, the body of an if, while or for is exactly one statement; indentation does not add statements to it. Kind: silent logic error. Trigger class: A braceless header followed by two or more indented statements: only the first is controlled, the others run once, after the if/loop, on every input. |
| lvl:nested_loops@L4#3 \| level L4 way diagnose_an_error: rule broken: The inner loop needs its own loop variable. Kind: compile-time. Trigger class: Redeclaring the outer variable in the inner header (for (int i ...) { for (int i ...) }): 'variable i is already defined'. |
| lvl:nested_loops@L4#4 \| level L4 way diagnose_an_error: rule broken: The inner loop must update its own variable. Kind: silent logic error. Trigger class: Writing for (int j = 0; j < N; i++) in the inner loop: j never changes, so the inner loop is infinite (or i runs out of range). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:nested_loops@L2#1 (Score: 0.5)}
{lvl:nested_loops@L1#1 (Score: 0.3)}
{lvl:nested_loops@L2#2 (Score: 0.2)}
```
Kept by pruning: lvl:nested_loops@L2#1 (0.50), lvl:nested_loops@L1#1 (0.30), lvl:nested_loops@L2#2 (0.20)

Label prompt for level way lvl:nested_loops@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> The inner body runs (outer passes) x (inner passes) times: two loops of 1..10 call printf 100 times; DivisorPattern 3 prints 3 rows of 3 entries, each row ending with its row number.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:nested_loops@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> Because loops are statements, one can be the body of another; the inner loop iterates all the way through for each iteration of the outer loop.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:nested_loops@L2#2 (the model saw only the concept, the way's name 'one step execution' and its text; no level):
> One outer pass resets the inner variable, runs the complete inner loop, executes the rest of the outer body once, and then updates the outer variable once.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:nested_loops@L2#1 | not applied |  |  | 0.0 |  |  |
| lvl:nested_loops@L1#1 | not applied |  |  | 0.0 |  |  |
| lvl:nested_loops@L2#2 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:math_library->math_random [broken, tier 0, 0.80], pre:for_loop->loop_body [confirmed, tier 2, 0.49], lvl:statement@L0#0 [shown, tier 2, 0.36]

reached across pre:math_library->math_random, entered next: math_library

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | 5 | mis:math_random->ProbabilityIsPrediction |
| c2 | Page 1 has probability 0.5 | mis:math_random->ProbabilityIsPrediction |
| c3 | so in 10 steps the surfer goes there exactly 5 times | err:loop_control->WrongIterationCount |
| c4 | Actual: it varies from run to run | not covered yet |
| c5 | five runs gave 6, 4, 8, 5 and 6 | pre:for_loop->loop_body |

**Uncovered clauses bring in (BM25 of the uncovered clauses against unvisited concepts):** control_flow (6.08), method_call (4.45), array_creation (3.85)

**Graph check, not yet read (the walk may not stop while these remain):** own edges of array_creation, own edges of control_flow, own edges of math_library, own edges of method_call, pre:loop_body->accumulator_pattern, pre:loop_body->counter_pattern, pre:statement->control_flow, pre:while_loop->loop_body

Figure 6 (the graph after depth 3): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY41_figure06.png

### Depth 4: current concepts 'math_library', 'control_flow', 'method_call', 'array_creation'

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
err:math_library->MathMethodWithoutClassName (0.34), err:math_library->WrongArgumentType (0.33), mis:math_library->CastRounds (0.33)
```
Kept by pruning: err:math_library->MathMethodWithoutClassName (0.34), err:math_library->WrongArgumentType (0.33), mis:math_library->CastRounds (0.33)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| err:math_library->MathMethodWithoutClassName \| wrong rule: sqrt(x) calls the square-root method. \| right rule: Library methods are called with the class name, e.g. Math.sqrt(x). |
| err:math_library->WrongArgumentType \| wrong rule: Calls a method with arguments of the wrong type, e.g. Math.sqrt("2"). \| right rule: Each argument must have the type the method's API lists. |
| mis:math_library->CastRounds \| wrong rule: (int) 2.7 evaluates to 3. \| right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer. |
Model's reply:
```
err:math_library->MathMethodWithoutClassName | not applied | clauses: none | confidence: 0.9
err:math_library->WrongArgumentType | not applied | clauses: none | confidence: 0.9
mis:math_library->CastRounds | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| err:math_library->MathMethodWithoutClassName | not applied |  |  | 0.0 |  |  |
| err:math_library->WrongArgumentType | not applied |  |  | 0.0 |  |  |
| mis:math_library->CastRounds | not applied |  |  | 0.0 |  |  |

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
{lvl:math_library@L2#2 (Score: 0.4)}
{lvl:math_library@L3#3 (Score: 0.35)}
{lvl:math_library@L3#6 (Score: 0.25)}
```
Kept by pruning: lvl:math_library@L2#2 (0.40), lvl:math_library@L3#3 (0.35), lvl:math_library@L3#6 (0.25)

Label prompt for level way lvl:math_library@L2#2 (the model saw only the concept, the way's name 'one step execution' and its text; no level):
> All the listed Math methods except random() are mathematical functions: they change no variable and return the same result for the same argument; random() takes no argument and returns a different value on each call.

Model's reply:
```
Label: shown
Clauses: 4, 5
Confidence: 0.6
```

Label prompt for level way lvl:math_library@L3#3 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Math.random() is the one Math method that takes no argument and is not a mathematical function: it returns a random double in [0, 1).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.75
```

Label prompt for level way lvl:math_library@L3#6 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> The random move draws r = Math.random() once per move and compares it with growing cumulative sums of row p[page] to find which interval contains it.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:math_library@L2#2 | shown | 0.4 | 0.6 | 0.24 | c4, c5 | Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6 |
| lvl:math_library@L3#3 | not applied |  |  | 0.0 |  |  |
| lvl:math_library@L3#6 | not applied |  |  | 0.0 |  |  |

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
mis:control_flow->ProgramLooksAhead (0.60), mis:control_flow->ProgramEndsAfterLoop (0.25), mis:control_flow->FalseLoopRepeatsNextCode (0.15)
```
Kept by pruning: mis:control_flow->ProgramLooksAhead (0.60), mis:control_flow->ProgramEndsAfterLoop (0.25), mis:control_flow->FalseLoopRepeatsNextCode (0.15)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:control_flow->ProgramLooksAhead \| wrong rule: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. \| right rule: Each statement executes using only the current state; later lines have no effect until control reaches them. |
| mis:control_flow->ProgramEndsAfterLoop \| wrong rule: When a loop finishes the program ends, so code after the loop never runs. \| right rule: When the loop condition becomes false, control continues with the first statement after the loop. |
| mis:control_flow->FalseLoopRepeatsNextCode \| wrong rule: A loop is an iterative if-else: while the condition is true the body repeats, and when it is false the code after the loop repeats. \| right rule: Only the body is repeated; once the condition is false the code after the loop runs once. |
Model's reply:
```
mis:control_flow->ProgramLooksAhead | not applied | clauses: none | confidence: 0.85
mis:control_flow->ProgramEndsAfterLoop | correct | clauses: 4, 5 | confidence: 0.6
mis:control_flow->FalseLoopRepeatsNextCode | not applied | clauses: none | confidence: 0.75
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:control_flow->ProgramLooksAhead | not applied |  |  | 0.0 |  |  |
| mis:control_flow->ProgramEndsAfterLoop | correct | 0.25 | 0.6 | 0.15 | c4, c5 | Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6 |
| mis:control_flow->FalseLoopRepeatsNextCode | not applied |  |  | 0.0 |  |  |

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
{lvl:control_flow@L0#0 (Score: 0.6)}
{lvl:control_flow@L2#1 (Score: 0.25)}
{lvl:control_flow@L4#1 (Score: 0.15)}
```
Kept by pruning: lvl:control_flow@L0#0 (0.60), lvl:control_flow@L2#1 (0.25), lvl:control_flow@L4#1 (0.15)

Label prompt for level way lvl:control_flow@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: in everyday instructions a listener reads the whole list at once, does steps in a sensible order and infers what the writer wants. Java instead executes statements one at a time, top to bottom, each only when control reaches it, and nothing later in the program has any effect earlier.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.75
```

Label prompt for level way lvl:control_flow@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> The output is the sequence of print statements that control actually reaches, in the order reached: e.g. TenHellos prints 1st, 2nd, 3rd Hello once each, then 4th to 10th Hello from the loop.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Label prompt for level way lvl:control_flow@L4#1 (the model saw only the concept, the way's name 'transfer to a new program' and its text; no level):
> Reason in terms of control flow whenever you must predict output or find why a statement did or did not run: trace which statement is reached next. Straight-line sequence suffices only when every input needs the same steps exactly once; otherwise add a conditional or a loop.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:control_flow@L0#0 | not applied |  |  | 0.0 |  |  |
| lvl:control_flow@L2#1 | not applied |  |  | 0.0 |  |  |
| lvl:control_flow@L4#1 | not applied |  |  | 0.0 |  |  |

#### method_call, misconceptions: 10 edges offered
Edges offered:
| edge |
|---|
| err:method_call->DiscardedReturnValue \| wrong rule: Writes Math.round(x); on its own line expecting x to be rounded. \| right rule: Math.round(x) returns a value; that value has to be stored or used (e.g. long r = Math.round(x);), because the call on its own line does nothing with it. |
| err:method_call->MathMethodWithoutClassName \| wrong rule: sqrt(x) calls the square-root method. \| right rule: Library methods are called with the class name, e.g. Math.sqrt(x). |
| err:method_call->WrongArgumentType \| wrong rule: Calls a method with arguments of the wrong type, e.g. Math.sqrt("2"). \| right rule: Each argument must have the type the method's API lists. |
| mis:method_call->ArgumentOrderInferred \| wrong rule: Java works out from the variable names which argument goes where, so Math.pow(n, 2) and Math.pow(2, n) mean the same. \| right rule: Arguments are written in the order the method's signature lists them; for example, Math.pow(a, b) raises a to the bth power. |
| mis:method_call->ArrayHasLengthMethod \| wrong rule: you call length() instead of using the length field \| right rule: An array's size is the field a.length, written without parentheses. |
| mis:method_call->EqualsComparesReferences \| wrong rule: .equals() compares references, not contents \| right rule: s.equals(t) checks whether the two Strings contain the same characters. |
| mis:method_call->OutsideInMethodNesting \| wrong rule: nested calls run outside-in, not arguments-first \| right rule: In f(g(x)), g(x) is evaluated first and its result is passed to f. |
| mis:method_call->ParameterTypesInCall \| wrong rule: A method call lists the parameter types, as in Math.pow(double a, double b). \| right rule: A call passes only argument expressions, e.g. Math.pow(a, b); types appear only in the method declaration. |
| mis:method_call->ParenthesesOnlyIfArgument \| wrong rule: () are optional on a no-argument call like println \| right rule: A method call always needs parentheses, so an empty line is printed with System.out.println();. |
| mis:method_call->StringMethodChangesString \| wrong rule: name.toUpperCase(); changes name. \| right rule: Strings are immutable: String methods return a new String, which must be assigned, e.g. name = name.toUpperCase(); |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
err:method_call->DiscardedReturnValue (0.50), err:method_call->MathMethodWithoutClassName (0.30), err:method_call->WrongArgumentType (0.20)
```
Kept by pruning: err:method_call->DiscardedReturnValue (0.50), err:method_call->MathMethodWithoutClassName (0.30), err:method_call->WrongArgumentType (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| err:method_call->DiscardedReturnValue \| wrong rule: Writes Math.round(x); on its own line expecting x to be rounded. \| right rule: Math.round(x) returns a value; that value has to be stored or used (e.g. long r = Math.round(x);), because the call on its own line does nothing with it. |
| err:method_call->MathMethodWithoutClassName \| wrong rule: sqrt(x) calls the square-root method. \| right rule: Library methods are called with the class name, e.g. Math.sqrt(x). |
| err:method_call->WrongArgumentType \| wrong rule: Calls a method with arguments of the wrong type, e.g. Math.sqrt("2"). \| right rule: Each argument must have the type the method's API lists. |
Model's reply:
```
err:method_call->DiscardedReturnValue | not applied | clauses: none | confidence: 0.9
err:method_call->MathMethodWithoutClassName | not applied | clauses: none | confidence: 0.9
err:method_call->WrongArgumentType | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| err:method_call->DiscardedReturnValue | not applied |  |  | 0.0 |  |  |
| err:method_call->MathMethodWithoutClassName | not applied |  |  | 0.0 |  |  |
| err:method_call->WrongArgumentType | not applied |  |  | 0.0 |  |  |

#### method_call, level ways: 17 edges offered
Edges offered:
| edge |
|---|
| lvl:method_call@L0#0 \| level L0 way everyday_reading: Folk meaning: maths function notation f(x) or sqrt(x), where the name alone suffices, a constant needs no brackets, and the reader infers which argument is which from meaning. Java rule: a library method is called as ClassName.name(arguments) (Math.sqrt(x)), the parentheses are always required, and arguments are matched to parameters by position and type. |
| lvl:method_call@L0#5 \| level L0 way inconsistent_trace: Points to LT (arguments are evaluated left to right, then the method runs, then its return value replaces the call). Applied unevenly: in f(g(x)) the student calls the outer method before the inner one on some lines, or keeps the argument expression unevaluated in one trace step. (here mixing in: "() are optional on a no-argument call like println") |
| lvl:method_call@L1#0 \| level L1 way names_the_element: A method call is an expression that invokes a (library) method by its name, with arguments in parentheses, and evaluates to the value the method returns. |
| lvl:method_call@L1#1 \| level L1 way states_the_rule: A library method is used by typing its (class-qualified) name followed by arguments of the specified types, in parentheses and separated by commas; the call can be used in expressions like a variable or literal; void methods return no value. |
| lvl:method_call@L2#0 \| level L2 way line_by_line_trace: Evaluate the argument expressions from left to right (inner calls first), convert each to its parameter type if needed, transfer control to the method, and when it returns substitute the returned value for the call in the enclosing expression. |
| lvl:method_call@L2#1 \| level L2 way output_prediction: The call's value has the method's return type: Math.sqrt(5.0*5.0 - 4.0*4.0) is double 3.0, Math.round(3.14159) is long 3, Integer.parseInt("123") is int 123; a void method such as println has no value. |
| lvl:method_call@L2#2 \| level L2 way one_step_execution: Calling a Math method changes none of the caller's variables (arguments are passed as values); the program's state changes only if the returned value is stored or used, e.g. double d = Math.sqrt(x);. |
| lvl:method_call@L3#0 \| level L3 way relation_to_neighbour: Arguments may be arbitrary expressions of the right type, and the call itself is an expression usable inside larger ones (Math.sin(x) * Math.cos(y)). |
| lvl:method_call@L3#1 \| level L3 way relation_to_neighbour: Math methods are called through the class name, Math.sqrt(x); without the prefix the compiler looks for the method in the current class and reports cannot find symbol. |
| lvl:method_call@L3#2 \| level L3 way relation_to_neighbour: The call must match a signature in the API (name, number, order and types of arguments), and the API's return type tells how the value can be used. |
| lvl:method_call@L3#3 \| level L3 way purpose_of_the_whole: Delegates a computation to existing library code used as a black box, and composes computations by passing one call's result into another, e.g. Math.exp(Math.log(10.0)). |
| lvl:method_call@L4#0 \| level L4 way predict_a_change: Changing an argument changes only the returned value, never the argument variable; swapping arguments changes the meaning (Math.pow(2, n) vs Math.pow(n, 2)); replacing a call by its value keeps behaviour for mathematical functions but not for Math.random(). |
| lvl:method_call@L4#1 \| level L4 way diagnose_an_error: rule broken: Each argument must have (or automatically widen to) the type the method's API lists. Kind: compile-time. Trigger class: An argument whose type cannot be converted to the parameter type, e.g. Math.sqrt("2"), or the wrong number of arguments. |
| lvl:method_call@L4#2 \| level L4 way diagnose_an_error: rule broken: A value-returning call does not change its argument; its result must be stored or used. Kind: silent logic error. Trigger class: A non-void call written as a statement on its own, e.g. Math.round(x); or Math.abs(d); expecting x or d to change. |
| lvl:method_call@L4#3 \| level L4 way transfer_to_a_new_program: Call a library method whenever a well-specified computation exists in an API (square roots, powers, conversions); write your own code only when no method fits; store a result in a variable rather than repeating an identical call. |
| lvl:method_call@L4#4 \| level L4 way diagnose_an_error: rule broken: Library methods are called with the class name, e.g. Math.sqrt(x). Kind: compile-time. Trigger class: Calling sqrt(x), pow(a, b) etc. without the Math. prefix from another class (cannot find symbol). |
| lvl:method_call@L4#5 \| level L4 way diagnose_an_error: rule broken: A call needs parentheses and passes only argument expressions. Kind: compile-time. Trigger class: Omitting () on a call (Math.random) or writing parameter types in the call (Math.pow(double a, double b)). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:method_call@L4#0 (Score: 0.6)}
{lvl:method_call@L0#0 (Score: 0.25)}
{lvl:method_call@L2#1 (Score: 0.15)}
```
Kept by pruning: lvl:method_call@L4#0 (0.60), lvl:method_call@L0#0 (0.25), lvl:method_call@L2#1 (0.15)

Label prompt for level way lvl:method_call@L4#0 (the model saw only the concept, the way's name 'predict a change' and its text; no level):
> Changing an argument changes only the returned value, never the argument variable; swapping arguments changes the meaning (Math.pow(2, n) vs Math.pow(n, 2)); replacing a call by its value keeps behaviour for mathematical functions but not for Math.random().

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.75
```

Label prompt for level way lvl:method_call@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: maths function notation f(x) or sqrt(x), where the name alone suffices, a constant needs no brackets, and the reader infers which argument is which from meaning. Java rule: a library method is called as ClassName.name(arguments) (Math.sqrt(x)), the parentheses are always required, and arguments are matched to parameters by position and type.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:method_call@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> The call's value has the method's return type: Math.sqrt(5.0*5.0 - 4.0*4.0) is double 3.0, Math.round(3.14159) is long 3, Integer.parseInt("123") is int 123; a void method such as println has no value.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:method_call@L4#0 | not applied |  |  | 0.0 |  |  |
| lvl:method_call@L0#0 | not applied |  |  | 0.0 |  |  |
| lvl:method_call@L2#1 | not applied |  |  | 0.0 |  |  |

#### array_creation, misconceptions: 9 edges offered
Edges offered:
| edge |
|---|
| err:array_creation->NegativeArraySize \| wrong rule: new int[n] with a negative n creates an empty array. \| right rule: Creating an array with a negative length throws NegativeArraySizeException at run time. |
| mis:array_creation->ArrayAllocationWithoutNew \| wrong rule: Arrays are created without the new keyword. \| right rule: An array is created with new (or with an initializer list in a declaration). |
| mis:array_creation->ArrayBracketCountIsLength \| wrong rule: The number of brackets in an array type or initializer is the array's length. \| right rule: Brackets give the number of dimensions; the length is set at creation. |
| mis:array_creation->ArrayCreationIsFree \| wrong rule: Creating a big array with new takes no time because the elements are not set yet. \| right rule: Java initializes every element when the array is created, so creation takes time proportional to its length. |
| mis:array_creation->ArrayLengthCannotBeZero \| wrong rule: An array cannot have length 0. \| right rule: new int[0] is a legal array of length 0. |
| mis:array_creation->ArrayListIsArray \| wrong rule: an ArrayList is an array (borderline; beyond Chapter 1 CS1) \| right rule: An array has a fixed length and uses [] and .length; an ArrayList can grow and uses get, set and size(). |
| mis:array_creation->ArrayRangeInclusive \| wrong rule: new int[n] has slots 0 to n, inclusive. \| right rule: The slots are 0 to n - 1. |
| mis:array_creation->ArraysGrow \| wrong rule: Storing a value at a[n] in an array of length n makes the array grow. \| right rule: An array's length is fixed when it is created, so a[n] throws an exception. |
| mis:array_creation->DeclarationCreatesArray \| wrong rule: int[] a; already makes an array that can be indexed. \| right rule: The declaration only names the array; until new (or an initializer) creates it, using a[i] gives a 'variable might not have been initialized' compile-time error. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:array_creation->ArrayRangeInclusive (0.40), mis:array_creation->ArrayCreationIsFree (0.30), mis:array_creation->ArrayAllocationWithoutNew (0.30)
```
Kept by pruning: mis:array_creation->ArrayRangeInclusive (0.40), mis:array_creation->ArrayCreationIsFree (0.30), mis:array_creation->ArrayAllocationWithoutNew (0.30)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:array_creation->ArrayRangeInclusive \| wrong rule: new int[n] has slots 0 to n, inclusive. \| right rule: The slots are 0 to n - 1. |
| mis:array_creation->ArrayCreationIsFree \| wrong rule: Creating a big array with new takes no time because the elements are not set yet. \| right rule: Java initializes every element when the array is created, so creation takes time proportional to its length. |
| mis:array_creation->ArrayAllocationWithoutNew \| wrong rule: Arrays are created without the new keyword. \| right rule: An array is created with new (or with an initializer list in a declaration). |
Model's reply:
```
mis:array_creation->ArrayRangeInclusive | not applied | clauses: none | confidence: 0.9
mis:array_creation->ArrayCreationIsFree | not applied | clauses: none | confidence: 0.95
mis:array_creation->ArrayAllocationWithoutNew | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:array_creation->ArrayRangeInclusive | not applied |  |  | 0.0 |  |  |
| mis:array_creation->ArrayCreationIsFree | not applied |  |  | 0.0 |  |  |
| mis:array_creation->ArrayAllocationWithoutNew | not applied |  |  | 0.0 |  |  |

#### array_creation, level ways: 21 edges offered
Edges offered:
| edge |
|---|
| lvl:array_creation@L0#0 \| level L0 way everyday_reading: Folk meaning: in maths, a[5] or a_5 names element 5, and 'new' means 'fresh, empty, ready to fill', so 'new int[5]' is read as 'element 5' or as an empty list that grows. Java rule: new int[n] allocates exactly n elements, indexed 0 to n-1, each already set to the default value, and the length can never change. |
| lvl:array_creation@L0#5 \| level L0 way inconsistent_trace: Points to LT: evaluate the size, allocate the array, fill it with defaults, return the reference, then assign it. Inconsistent application: the size n is treated as the last index on some lines, or the array is assumed to exist already at its declaration. (here mixing in: "an array grows as you add elements") |
| lvl:array_creation@L1#0 \| level L1 way names_the_element: Identity: an array creation expression; new T[n] makes a new array object with n elements of type T and yields a reference to it. |
| lvl:array_creation@L1#1 \| level L1 way states_the_rule: Declarative: 'new T[expr]', where expr is any int-valued expression evaluated at run time; the resulting length is fixed for the array's lifetime. |
| lvl:array_creation@L2#0 \| level L2 way line_by_line_trace: Sequencing: (1) the dimension expression is evaluated; (2) if it is negative, NegativeArraySizeException is thrown; (3) space for n elements is reserved and every element is set to its default; (4) the expression yields the reference, which an enclosing assignment then stores. |
| lvl:array_creation@L2#1 \| level L2 way output_prediction: Result: a value of type T[], namely a reference to a new array of length n whose elements all hold the default (0, 0.0, false or null). It produces no output; printing it shows an address, not the elements. |
| lvl:array_creation@L2#2 \| level L2 way one_step_execution: State transition: one execution creates one new array object (n new element variables at their defaults) and returns its reference. No existing variable changes until that reference is assigned. |
| lvl:array_creation@L3#0 \| level L3 way relation_to_neighbour: The declared element type must match the created one; in 'double[] a = new double[N];' the left side is the declaration and the right side is the creation. |
| lvl:array_creation@L3#1 \| level L3 way relation_to_neighbour: Elements can be indexed only after creation, and the n given to new fixes the valid index range 0..n-1. |
| lvl:array_creation@L3#2 \| level L3 way relation_to_neighbour: Creation is what puts the default value (0, 0.0, false, null) in every slot; each execution of new gives fresh defaults. |
| lvl:array_creation@L3#3 \| level L3 way relation_to_neighbour: The size n given to new becomes a.length and never changes for that array object. |
| lvl:array_creation@L3#4 \| level L3 way relation_to_neighbour: An initializer {v0, ..., vk} implies creation of an array of length k+1, so new is not written. |
| lvl:array_creation@L3#5 \| level L3 way relation_to_neighbour: Only new makes a distinct array. Assignment copies the reference, so a separate copy needs new plus an element-by-element copy. |
| lvl:array_creation@L3#6 \| level L3 way relation_to_neighbour: new yields the reference (address) of the array, and the array variable stores that reference, not the elements. |
| lvl:array_creation@L3#7 \| level L3 way purpose_of_the_whole: Plan/role: reserve storage for a number of values that may be known only at run time (e.g. N from the command line), before any value is stored. |
| lvl:array_creation@L4#0 \| level L4 way predict_a_change: Conservation: changing n changes a.length and the valid index range but not the element type. Moving 'new' inside a loop gives a fresh array of defaults on every pass (SelfAvoidingWalk relies on this). Re-creating an array never changes arrays that other variables already refer to. |
| lvl:array_creation@L4#1 \| level L4 way diagnose_an_error: rule broken: The dimension expression of new must be >= 0. Kind: run-time exception. Trigger class: the size evaluates to a negative int, e.g. a negative command-line value, or int overflow such as new int[N*N*N*N] with N = 1000 (NegativeArraySizeException) |
| lvl:array_creation@L4#2 \| level L4 way transfer_to_a_new_program: Applicability: use new T[n] when the number of values is known (at least at run time) before they are stored and stays fixed. Use an initializer when the values are compile-time constants, and a resizing structure when the count is unknown in advance. |
| lvl:array_creation@L4#3 \| level L4 way diagnose_an_error: rule broken: An array must be allocated with new before its elements are accessed. Kind: compile-time. Trigger class: 'int[] a;' followed by a[i] = ... with no creation (variable a might not have been initialized) |
| lvl:array_creation@L4#4 \| level L4 way diagnose_an_error: rule broken: The dimension expression must have an integral type (int after promotion). Kind: compile-time. Trigger class: a double or long size such as new int[2.5] or new int[n] with long n (incompatible types: possible lossy conversion) |
| lvl:array_creation@L4#5 \| level L4 way diagnose_an_error: rule broken: The requested array must fit in the memory available to Java. Kind: run-time exception. Trigger class: a very large n such as new boolean[N+1] for huge N in PrimeSieve (OutOfMemoryError) |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:array_creation@L3#2 (Score: 0.4)}
{lvl:array_creation@L3#1 (Score: 0.35)}
{lvl:array_creation@L3#4 (Score: 0.25)}
```
Kept by pruning: lvl:array_creation@L3#2 (0.40), lvl:array_creation@L3#1 (0.35), lvl:array_creation@L3#4 (0.25)

Label prompt for level way lvl:array_creation@L3#2 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Creation is what puts the default value (0, 0.0, false, null) in every slot; each execution of new gives fresh defaults.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:array_creation@L3#1 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Elements can be indexed only after creation, and the n given to new fixes the valid index range 0..n-1.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:array_creation@L3#4 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> An initializer {v0, ..., vk} implies creation of an array of length k+1, so new is not written.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:array_creation@L3#2 | not applied |  |  | 0.0 |  |  |
| lvl:array_creation@L3#1 | not applied |  |  | 0.0 |  |  |
| lvl:array_creation@L3#4 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

lvl:math_library@L2#2 [shown, tier 2, 0.24], mis:control_flow->ProgramEndsAfterLoop [correct, tier 2, 0.15]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | 5 | mis:math_random->ProbabilityIsPrediction |
| c2 | Page 1 has probability 0.5 | mis:math_random->ProbabilityIsPrediction |
| c3 | so in 10 steps the surfer goes there exactly 5 times | err:loop_control->WrongIterationCount |
| c4 | Actual: it varies from run to run | mis:control_flow->ProgramEndsAfterLoop |
| c5 | five runs gave 6, 4, 8, 5 and 6 | pre:for_loop->loop_body |

**Graph check, not yet read (the walk may not stop while these remain):** pre:array_creation->array_default_values, pre:array_creation->array_initializer, pre:array_creation->indexing, pre:array_declaration->array_creation, pre:expression->method_call, pre:loop_body->accumulator_pattern, pre:loop_body->counter_pattern, pre:method_call->api, pre:method_call->math_library, pre:statement->control_flow, pre:while_loop->loop_body

Figure 7 (the graph after depth 4): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY41_figure07.png

## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on ['math_random'], broken at [] (consequences: pre:math_library->math_random), prerequisites {'expression': ['arithmetic_operators'], 'array_default_values': ['array_creation'], 'array_initializer': ['array_creation', 'array_declaration'], 'indexing': ['array_creation', 'array_initializer'], 'array_creation': ['array_declaration'], 'compound_assignment': ['assignment'], 'increment_operators': ['assignment', 'loop_control'], 'while_loop': ['boolean_expression'], 'boolean_expression': ['comparison_operators'], 'accumulator_pattern': ['compound_assignment', 'loop_body'], 'frequency_counting': ['counter_pattern'], 'array_declaration': ['data_structure'], 'data_structure': ['data_type'], 'comparison_operators': ['expression'], 'method_call': ['expression'], 'loop_body': ['for_loop', 'while_loop'], 'loop_scope': ['for_loop'], 'nested_loops': ['for_loop'], 'counter_pattern': ['increment_operators', 'loop_body'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable', 'while_loop'], 'math_random': ['math_library'], 'api': ['method_call'], 'math_library': ['method_call'], 'control_flow': ['statement'], 'println': ['statement'], 'loop_variable': ['while_loop']}
- for_loop: L3 via relation_to_neighbour "so in 10 steps the surfer goes there exactly 5 times"
- loop_control: L3 via purpose_of_the_whole "so in 10 steps the surfer goes there exactly 5 times"
- math_library: L2 via one_step_execution "Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6"
- math_random: L0 via misconception "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times"
- println: L2 via output_prediction "5; five runs gave 6, 4, 8, 5 and 6"
- statement: L0 via everyday_reading "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times"

**Stop:** max depth at depth 4; prompts {'prune': 32, 'label': 64}, fresh model calls 0, cache hits 96

### Held misconceptions
| concept | misconception | kind | quote | score | shares_evidence_with |
|---|---|---|---|---|---|
| math_random | ProbabilityIsPrediction | misconception | 5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times | 0.8075 |  |

### Broken concept edges
| edge | quote | score | consequence_of |
|---|---|---|---|
| pre:math_library->math_random | 5; so in 10 steps the surfer goes there exactly 5 times | 0.8 | mis:math_random->ProbabilityIsPrediction |

### Root cause: math_random / ProbabilityIsPrediction

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| for_loop | L3 | relation_to_neighbour |  | level_way | so in 10 steps the surfer goes there exactly 5 times |  | L3 purpose_of_the_whole |  |
| loop_control | L3 | purpose_of_the_whole |  | level_way | so in 10 steps the surfer goes there exactly 5 times |  | L1 names_the_element |  |
| math_library | L2 | one_step_execution |  | level_way | Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6 |  |  |  |
| math_random | L0 | misconception | ProbabilityIsPrediction | level_mis_links | 5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times | wrong rule: A probability (e.g. 70%) predicts what the next single trial will do. Right rule: A probability describes the long-run frequency over many trials, not one outcome; Math.random() < 0.7 is true on about 70% of many calls, and any single call can go either way. |  |  |
| println | L2 | output_prediction |  | level_way | 5; five runs gave 6, 4, 8, 5 and 6 |  |  |  |
| statement | L0 | everyday_reading |  | level_way | 5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |  |  |  |

### Overall level: L0

Clause coverage (final):
| clause | covered by |
|---|---|
| 5 | lvl:println@L2#1 |
| Page 1 has probability 0.5 | mis:math_random->ProbabilityIsPrediction |
| so in 10 steps the surfer goes there exactly 5 times | err:loop_control->WrongIterationCount |
| Actual: it varies from run to run | lvl:math_random@L3#2 |
| five runs gave 6, 4, 8, 5 and 6 | lvl:println@L2#1 |

Figure 8 (final picture): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY41_figure08.png

## 5. Every labelled edge (the evidence list, kept or not)
| depth | source | edge | kind | label | prune_score | confidence | score | clauses | quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | println | lvl:println@L2#1 | level | shown | 0.5 | 0.55 | 0.275 | [1, 5] | 5; five runs gave 6, 4, 8, 5 and 6 |
| 2 | loop_control | err:loop_control->WrongIterationCount | error | correct | 0.45 | 0.6 | 0.27 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 2 | loop_control | mis:loop_control->OffByOneBound | misconception | correct | 0.35 | 0.5 | 0.175 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 2 | loop_control | lvl:loop_control@L3#6 | level | shown | 0.3 | 0.55 | 0.165 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 2 | loop_control | lvl:loop_control@L1#0 | level | shown | 0.2 | 0.55 | 0.11 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 2 | for_loop | err:for_loop->WrongIterationCount | error | correct | 0.5 | 0.6 | 0.3 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 2 | for_loop | mis:for_loop->ForIsConditional | misconception | correct | 0.3 | 0.6 | 0.18 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 2 | for_loop | lvl:for_loop@L3#3 | level | shown | 0.5 | 0.6 | 0.3 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 2 | for_loop | lvl:for_loop@L3#8 | level | shown | 0.3 | 0.6 | 0.18 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 2 | math_random | mis:math_random->ProbabilityIsPrediction | misconception | held | 0.95 | 0.85 | 0.8075 | [1, 2, 3] | 5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |
| 2 | math_random | lvl:math_random@L0#0 | level | shown | 0.6 | 0.85 | 0.51 | [1, 3] | 5; so in 10 steps the surfer goes there exactly 5 times |
| 2 | math_random | lvl:math_random@L3#2 | level | shown | 0.2 | 0.6 | 0.12 | [4, 5] | Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6 |
| 2 | math_random | lvl:math_random@L4#0 | level | shown | 0.2 | 0.6 | 0.12 | [4, 5] | Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6 |
| 3 | math_random | pre:math_library->math_random | prerequisite | broken | 1.0 | 0.8 | 0.8 | [1, 3] | 5; so in 10 steps the surfer goes there exactly 5 times |
| 3 | loop_control | pre:loop_control->for_loop | prerequisite | confirmed | 0.5 | 0.55 | 0.275 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 3 | loop_control | pre:loop_variable->loop_control | prerequisite | confirmed | 0.3 | 0.55 | 0.165 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 3 | for_loop | pre:for_loop->loop_body | prerequisite | confirmed | 0.7000000000000001 | 0.7 | 0.49 | [3, 5] | so in 10 steps the surfer goes there exactly 5 times; five runs gave 6, 4, 8, 5 and 6 |
| 3 | statement | lvl:statement@L0#0 | level | shown | 0.6000000000000001 | 0.6 | 0.36 | [1, 2, 3] | 5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times |
| 3 | nested_loops | mis:nested_loops->OuterLoopIgnored | misconception | correct | 0.5 | 0.6 | 0.3 | [3] | so in 10 steps the surfer goes there exactly 5 times |
| 4 | math_library | lvl:math_library@L2#2 | level | shown | 0.4 | 0.6 | 0.24 | [4, 5] | Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6 |
| 4 | control_flow | mis:control_flow->ProgramEndsAfterLoop | misconception | correct | 0.25 | 0.6 | 0.15 | [4, 5] | Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6 |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | println | lvl:println@L2#1 | level | shown | 0.275 | [1, 5] |
| 2 | math_random | mis:math_random->ProbabilityIsPrediction | misconception | held | 0.8075 | [1, 2, 3] |
| 2 | math_random | lvl:math_random@L0#0 | level | shown | 0.51 | [1, 3] |
| 2 | for_loop | err:for_loop->WrongIterationCount | error | correct | 0.3 | [3] |
| 3 | math_random | pre:math_library->math_random | prerequisite | broken | 0.8 | [1, 3] |
| 3 | for_loop | pre:for_loop->loop_body | prerequisite | confirmed | 0.49 | [3, 5] |
| 3 | statement | lvl:statement@L0#0 | level | shown | 0.36 | [1, 2, 3] |
| 4 | math_library | lvl:math_library@L2#2 | level | shown | 0.24 | [4, 5] |
| 4 | control_flow | mis:control_flow->ProgramEndsAfterLoop | misconception | correct | 0.15 | [4, 5] |

## 7. Raw traversal log
```
clauses: 5 | Page 1 has probability 0.5 | so in 10 steps the surfer goes there exactly 5 times | Actual: it varies from run to run | five runs gave 6, 4, 8, 5 and 6
start: generic concepts whose tagging text occurs in the answer: statement
start: BM25 of the answer against each tagged concept: arithmetic_operators 36.94 (hits 1), compound_assignment 21.00 (hits 1), println 19.01 (hits 1), loop_control 17.39 (hits 2), for_loop 16.18 (hits 1), math_random 14.71 (hits 1), loop_body 13.73 (hits 1), statement 11.36 (hits 1), nested_loops 11.05 (hits 1), loop_variable 10.76 (hits 1), frequency_counting 10.00 (hits 2), control_flow 9.42 (hits 1), increment_operators 9.37 (hits 1), while_loop 8.43 (hits 1), array_creation 7.93 (hits 1), method_call 6.96 (hits 1), counter_pattern 6.62 (hits 1), boolean_expression 5.77 (hits 2), indexing 5.64 (hits 1), loop_scope 4.68 (hits 1), accumulator_pattern 4.43 (hits 1), math_library 3.63 (hits 1), array_initializer 3.60 (hits 1), array_default_values 2.81 (hits 1), array_declaration 2.01 (hits 1), comparison_operators 1.63 (hits 1), api 1.50 (hits 1), data_structure 0.53 (hits 1)
start: chosen arithmetic_operators, compound_assignment, println
start concepts (3): arithmetic_operators, compound_assignment, println
--- depth 1: current concepts ['arithmetic_operators', 'compound_assignment', 'println']
  arithmetic_operators (misconceptions): 3 candidates -> kept mis:arithmetic_operators->CaretIsPower (0.34), mis:arithmetic_operators->ArithmeticOnNumericStrings (0.33), mis:arithmetic_operators->RemainderIsSubtraction (0.33)
    mis:arithmetic_operators->CaretIsPower -> not applied (0.00) ""
    mis:arithmetic_operators->ArithmeticOnNumericStrings -> not applied (0.00) ""
    mis:arithmetic_operators->RemainderIsSubtraction -> not applied (0.00) ""
  arithmetic_operators (level ways): 18 candidates -> kept lvl:arithmetic_operators@L2#1 (0.40), lvl:arithmetic_operators@L3#4 (0.35), lvl:arithmetic_operators@L0#0 (0.25)
    lvl:arithmetic_operators@L2#1 -> not applied (0.00) ""
    lvl:arithmetic_operators@L3#4 -> not applied (0.00) ""
    lvl:arithmetic_operators@L0#0 -> not applied (0.00) ""
  compound_assignment (misconceptions): 2 candidates -> kept mis:compound_assignment->CompoundAssignmentNoCast (0.60), mis:compound_assignment->CompoundSubtractIsAssignNegative (0.40)
    mis:compound_assignment->CompoundAssignmentNoCast -> not applied (0.00) ""
    mis:compound_assignment->CompoundSubtractIsAssignNegative -> not applied (0.00) ""
  compound_assignment (level ways): 15 candidates -> kept lvl:compound_assignment@L0#0 (0.50), lvl:compound_assignment@L3#3 (0.30), lvl:compound_assignment@L2#1 (0.20)
    lvl:compound_assignment@L0#0 -> not applied (0.00) ""
    lvl:compound_assignment@L3#3 -> not applied (0.00) ""
    lvl:compound_assignment@L2#1 -> not applied (0.00) ""
  println (misconceptions): 6 candidates -> kept mis:println->PrintedTextIsExecuted (0.40), mis:println->PrintNewLineFirst (0.35), err:println->PrintWithoutFinalNewline (0.25)
    mis:println->PrintedTextIsExecuted -> not applied (0.00) ""
    mis:println->PrintNewLineFirst -> not applied (0.00) ""
    err:println->PrintWithoutFinalNewline -> not applied (0.00) ""
  println (level ways): 17 candidates -> kept lvl:println@L2#1 (0.50), lvl:println@L3#4 (0.30), lvl:println@L2#0 (0.20)
    lvl:println@L2#1 -> shown (0.28) "5; five runs gave 6, 4, 8, 5 and 6"
    lvl:println@L3#4 -> not applied (0.00) ""
    lvl:println@L2#0 -> not applied (0.00) ""
  kept: lvl:println@L2#1 [shown, tier 2, 0.28]
  clause coverage: c1 uncovered; c2 uncovered; c3 uncovered; c4 uncovered; c5 uncovered
  uncovered clauses bring in: loop_control (16.79), for_loop (15.53), math_random (13.94)
  not yet read: own edges of for_loop, own edges of loop_control, own edges of math_random, par:increment_operators~compound_assignment, pre:arithmetic_operators->expression, pre:assignment->compound_assignment, pre:compound_assignment->accumulator_pattern, pre:statement->println
--- depth 2: current concepts ['arithmetic_operators', 'compound_assignment', 'println', 'loop_control', 'for_loop', 'math_random']
  arithmetic_operators (concept edges): 1 candidates -> kept pre:arithmetic_operators->expression (1.00)
    pre:arithmetic_operators->expression -> not applied (0.00) ""
  compound_assignment (concept edges): 3 candidates -> kept pre:compound_assignment->accumulator_pattern (0.40), par:increment_operators~compound_assignment (0.35), pre:assignment->compound_assignment (0.25)
    pre:compound_assignment->accumulator_pattern -> not applied (0.00) ""
    par:increment_operators~compound_assignment -> not applied (0.00) ""
    pre:assignment->compound_assignment -> not applied (0.00) ""
  println (concept edges): 1 candidates -> kept pre:statement->println (1.00)
    pre:statement->println -> not applied (0.00) ""
  loop_control (misconceptions): 11 candidates -> kept err:loop_control->WrongIterationCount (0.45), mis:loop_control->OffByOneBound (0.35), mis:loop_control->IdiomOverridesCode (0.20)
    err:loop_control->WrongIterationCount -> correct (0.27) "so in 10 steps the surfer goes there exactly 5 times"
    mis:loop_control->OffByOneBound -> correct (0.17) "so in 10 steps the surfer goes there exactly 5 times"
    mis:loop_control->IdiomOverridesCode -> not applied (0.00) ""
  loop_control (level ways): 19 candidates -> kept lvl:loop_control@L2#1 (0.50), lvl:loop_control@L3#6 (0.30), lvl:loop_control@L1#0 (0.20)
    lvl:loop_control@L2#1 -> not applied (0.00) ""
    lvl:loop_control@L3#6 -> shown (0.17) "so in 10 steps the surfer goes there exactly 5 times"
    lvl:loop_control@L1#0 -> shown (0.11) "so in 10 steps the surfer goes there exactly 5 times"
  for_loop (misconceptions): 21 candidates -> kept err:for_loop->WrongIterationCount (0.50), mis:for_loop->ForIsConditional (0.30), mis:for_loop->LoopCountIsStatementCount (0.20)
    err:for_loop->WrongIterationCount -> correct (0.30) "so in 10 steps the surfer goes there exactly 5 times"
    mis:for_loop->ForIsConditional -> correct (0.18) "so in 10 steps the surfer goes there exactly 5 times"
    mis:for_loop->LoopCountIsStatementCount -> not applied (0.00) ""
  for_loop (level ways): 24 candidates -> kept lvl:for_loop@L3#3 (0.50), lvl:for_loop@L3#8 (0.30), lvl:for_loop@L0#0 (0.20)
    lvl:for_loop@L3#3 -> shown (0.30) "so in 10 steps the surfer goes there exactly 5 times"
    lvl:for_loop@L3#8 -> shown (0.18) "so in 10 steps the surfer goes there exactly 5 times"
    lvl:for_loop@L0#0 -> not applied (0.00) ""
  math_random (misconceptions): 2 candidates -> kept mis:math_random->ProbabilityIsPrediction (0.95), mis:math_random->RandomCanReturnOne (0.05)
    mis:math_random->ProbabilityIsPrediction -> held (0.81) "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times"
    mis:math_random->RandomCanReturnOne -> not applied (0.00) ""
  math_random (level ways): 16 candidates -> kept lvl:math_random@L0#0 (0.60), lvl:math_random@L3#2 (0.20), lvl:math_random@L4#0 (0.20)
    lvl:math_random@L0#0 -> shown (0.51) "5; so in 10 steps the surfer goes there exactly 5 times"
    lvl:math_random@L3#2 -> shown (0.12) "Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6"
    lvl:math_random@L4#0 -> shown (0.12) "Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6"
  kept: mis:math_random->ProbabilityIsPrediction [held, tier 0, 0.81], lvl:math_random@L0#0 [shown, tier 2, 0.51], err:for_loop->WrongIterationCount [correct, tier 2, 0.30]
  clause coverage: c1 <- mis:math_random->ProbabilityIsPrediction; c2 <- mis:math_random->ProbabilityIsPrediction; c3 <- err:loop_control->WrongIterationCount; c4 uncovered; c5 uncovered
  uncovered clauses bring in: statement (8.79), loop_body (8.29), nested_loops (8.27)
  not yet read: own edges of loop_body, own edges of nested_loops, own edges of statement, pre:for_loop->loop_body, pre:for_loop->loop_scope, pre:for_loop->nested_loops, pre:loop_control->for_loop, pre:loop_control->increment_operators, pre:loop_variable->loop_control, pre:math_library->math_random, pre:while_loop->loop_control
--- depth 3: current concepts ['math_random', 'loop_control', 'for_loop', 'statement', 'loop_body', 'nested_loops']
  math_random (concept edges): 1 candidates -> kept pre:math_library->math_random (1.00)
    pre:math_library->math_random -> broken (0.80) "5; so in 10 steps the surfer goes there exactly 5 times"
  loop_control (concept edges): 4 candidates -> kept pre:loop_control->for_loop (0.50), pre:loop_variable->loop_control (0.30), pre:while_loop->loop_control (0.20)
    pre:loop_control->for_loop -> confirmed (0.28) "so in 10 steps the surfer goes there exactly 5 times"
    pre:loop_variable->loop_control -> confirmed (0.17) "so in 10 steps the surfer goes there exactly 5 times"
    pre:while_loop->loop_control -> not applied (0.00) ""
  for_loop (concept edges): 3 candidates -> kept pre:for_loop->loop_body (0.70), pre:for_loop->nested_loops (0.20), pre:for_loop->loop_scope (0.10)
    pre:for_loop->loop_body -> confirmed (0.49) "so in 10 steps the surfer goes there exactly 5 times; five runs gave 6, 4, 8, 5 and 6"
    pre:for_loop->nested_loops -> not applied (0.00) ""
    pre:for_loop->loop_scope -> not applied (0.00) ""
  statement (misconceptions): 5 candidates -> kept mis:statement->ComputerFillsInIntent (0.55), mis:statement->ProgramLooksAhead (0.35), mis:statement->StatementsRunInAnyOrder (0.10)
    mis:statement->ComputerFillsInIntent -> not applied (0.00) ""
    mis:statement->ProgramLooksAhead -> not applied (0.00) ""
    mis:statement->StatementsRunInAnyOrder -> not applied (0.00) ""
  statement (level ways): 19 candidates -> kept lvl:statement@L0#0 (0.60), lvl:statement@L0#2 (0.30), lvl:statement@L2#0 (0.10)
    lvl:statement@L0#0 -> shown (0.36) "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times"
    lvl:statement@L0#2 -> not applied (0.00) ""
    lvl:statement@L2#0 -> not applied (0.00) ""
  loop_body (misconceptions): 12 candidates -> kept mis:loop_body->ComputerFillsInIntent (0.50), mis:loop_body->LoopOutputSameEachPass (0.30), mis:loop_body->IfInLoopUnchecked (0.20)
    mis:loop_body->ComputerFillsInIntent -> not applied (0.00) ""
    mis:loop_body->LoopOutputSameEachPass -> not applied (0.00) ""
    mis:loop_body->IfInLoopUnchecked -> not applied (0.00) ""
  loop_body (level ways): 14 candidates -> kept lvl:loop_body@L0#0 (0.45), lvl:loop_body@L3#3 (0.35), lvl:loop_body@L2#1 (0.20)
    lvl:loop_body@L0#0 -> not applied (0.00) ""
    lvl:loop_body@L3#3 -> not applied (0.00) ""
    lvl:loop_body@L2#1 -> not applied (0.00) ""
  nested_loops (misconceptions): 8 candidates -> kept mis:nested_loops->OuterLoopIgnored (0.50), mis:nested_loops->NestedLoopsSequential (0.30), mis:nested_loops->EmptyInnerLoopSkipsRest (0.20)
    mis:nested_loops->OuterLoopIgnored -> correct (0.30) "so in 10 steps the surfer goes there exactly 5 times"
    mis:nested_loops->NestedLoopsSequential -> not applied (0.00) ""
    mis:nested_loops->EmptyInnerLoopSkipsRest -> not applied (0.00) ""
  nested_loops (level ways): 17 candidates -> kept lvl:nested_loops@L2#1 (0.50), lvl:nested_loops@L1#1 (0.30), lvl:nested_loops@L2#2 (0.20)
    lvl:nested_loops@L2#1 -> not applied (0.00) ""
    lvl:nested_loops@L1#1 -> not applied (0.00) ""
    lvl:nested_loops@L2#2 -> not applied (0.00) ""
  kept: pre:math_library->math_random [broken, tier 0, 0.80], pre:for_loop->loop_body [confirmed, tier 2, 0.49], lvl:statement@L0#0 [shown, tier 2, 0.36]
  reached across pre:math_library->math_random, entered next: math_library
  clause coverage: c1 <- mis:math_random->ProbabilityIsPrediction; c2 <- mis:math_random->ProbabilityIsPrediction; c3 <- err:loop_control->WrongIterationCount; c4 uncovered; c5 <- pre:for_loop->loop_body
  uncovered clauses bring in: control_flow (6.08), method_call (4.45), array_creation (3.85)
  not yet read: own edges of array_creation, own edges of control_flow, own edges of math_library, own edges of method_call, pre:loop_body->accumulator_pattern, pre:loop_body->counter_pattern, pre:statement->control_flow, pre:while_loop->loop_body
--- depth 4: current concepts ['math_library', 'control_flow', 'method_call', 'array_creation'] (closing round: own edges only)
  math_library (misconceptions): 4 candidates -> kept err:math_library->MathMethodWithoutClassName (0.34), err:math_library->WrongArgumentType (0.33), mis:math_library->CastRounds (0.33)
    err:math_library->MathMethodWithoutClassName -> not applied (0.00) ""
    err:math_library->WrongArgumentType -> not applied (0.00) ""
    mis:math_library->CastRounds -> not applied (0.00) ""
  math_library (level ways): 20 candidates -> kept lvl:math_library@L2#2 (0.40), lvl:math_library@L3#3 (0.35), lvl:math_library@L3#6 (0.25)
    lvl:math_library@L2#2 -> shown (0.24) "Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6"
    lvl:math_library@L3#3 -> not applied (0.00) ""
    lvl:math_library@L3#6 -> not applied (0.00) ""
  control_flow (misconceptions): 11 candidates -> kept mis:control_flow->ProgramLooksAhead (0.60), mis:control_flow->ProgramEndsAfterLoop (0.25), mis:control_flow->FalseLoopRepeatsNextCode (0.15)
    mis:control_flow->ProgramLooksAhead -> not applied (0.00) ""
    mis:control_flow->ProgramEndsAfterLoop -> correct (0.15) "Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6"
    mis:control_flow->FalseLoopRepeatsNextCode -> not applied (0.00) ""
  control_flow (level ways): 15 candidates -> kept lvl:control_flow@L0#0 (0.60), lvl:control_flow@L2#1 (0.25), lvl:control_flow@L4#1 (0.15)
    lvl:control_flow@L0#0 -> not applied (0.00) ""
    lvl:control_flow@L2#1 -> not applied (0.00) ""
    lvl:control_flow@L4#1 -> not applied (0.00) ""
  method_call (misconceptions): 10 candidates -> kept err:method_call->DiscardedReturnValue (0.50), err:method_call->MathMethodWithoutClassName (0.30), err:method_call->WrongArgumentType (0.20)
    err:method_call->DiscardedReturnValue -> not applied (0.00) ""
    err:method_call->MathMethodWithoutClassName -> not applied (0.00) ""
    err:method_call->WrongArgumentType -> not applied (0.00) ""
  method_call (level ways): 17 candidates -> kept lvl:method_call@L4#0 (0.60), lvl:method_call@L0#0 (0.25), lvl:method_call@L2#1 (0.15)
    lvl:method_call@L4#0 -> not applied (0.00) ""
    lvl:method_call@L0#0 -> not applied (0.00) ""
    lvl:method_call@L2#1 -> not applied (0.00) ""
  array_creation (misconceptions): 9 candidates -> kept mis:array_creation->ArrayRangeInclusive (0.40), mis:array_creation->ArrayCreationIsFree (0.30), mis:array_creation->ArrayAllocationWithoutNew (0.30)
    mis:array_creation->ArrayRangeInclusive -> not applied (0.00) ""
    mis:array_creation->ArrayCreationIsFree -> not applied (0.00) ""
    mis:array_creation->ArrayAllocationWithoutNew -> not applied (0.00) ""
  array_creation (level ways): 21 candidates -> kept lvl:array_creation@L3#2 (0.40), lvl:array_creation@L3#1 (0.35), lvl:array_creation@L3#4 (0.25)
    lvl:array_creation@L3#2 -> not applied (0.00) ""
    lvl:array_creation@L3#1 -> not applied (0.00) ""
    lvl:array_creation@L3#4 -> not applied (0.00) ""
  kept: lvl:math_library@L2#2 [shown, tier 2, 0.24], mis:control_flow->ProgramEndsAfterLoop [correct, tier 2, 0.15]
  clause coverage: c1 <- mis:math_random->ProbabilityIsPrediction; c2 <- mis:math_random->ProbabilityIsPrediction; c3 <- err:loop_control->WrongIterationCount; c4 <- mis:control_flow->ProgramEndsAfterLoop; c5 <- pre:for_loop->loop_body
  not yet read: pre:array_creation->array_default_values, pre:array_creation->array_initializer, pre:array_creation->indexing, pre:array_declaration->array_creation, pre:expression->method_call, pre:loop_body->accumulator_pattern, pre:loop_body->counter_pattern, pre:method_call->api, pre:method_call->math_library, pre:statement->control_flow, pre:while_loop->loop_body
  root-cause walk: held on ['math_random'], broken at [] (consequences: pre:math_library->math_random), prerequisites {'expression': ['arithmetic_operators'], 'array_default_values': ['array_creation'], 'array_initializer': ['array_creation', 'array_declaration'], 'indexing': ['array_creation', 'array_initializer'], 'array_creation': ['array_declaration'], 'compound_assignment': ['assignment'], 'increment_operators': ['assignment', 'loop_control'], 'while_loop': ['boolean_expression'], 'boolean_expression': ['comparison_operators'], 'accumulator_pattern': ['compound_assignment', 'loop_body'], 'frequency_counting': ['counter_pattern'], 'array_declaration': ['data_structure'], 'data_structure': ['data_type'], 'comparison_operators': ['expression'], 'method_call': ['expression'], 'loop_body': ['for_loop', 'while_loop'], 'loop_scope': ['for_loop'], 'nested_loops': ['for_loop'], 'counter_pattern': ['increment_operators', 'loop_body'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable', 'while_loop'], 'math_random': ['math_library'], 'api': ['method_call'], 'math_library': ['method_call'], 'control_flow': ['statement'], 'println': ['statement'], 'loop_variable': ['while_loop']}
  level for_loop: L3 via relation_to_neighbour "so in 10 steps the surfer goes there exactly 5 times"
  level loop_control: L3 via purpose_of_the_whole "so in 10 steps the surfer goes there exactly 5 times"
  level math_library: L2 via one_step_execution "Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6"
  level math_random: L0 via misconception "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times"
  level println: L2 via output_prediction "5; five runs gave 6, 4, 8, 5 and 6"
  level statement: L0 via everyday_reading "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times"
```

## 8. Full diagnosis JSON
```json
{
 "scenario": "MY41",
 "settings": {
  "width": 3,
  "depth": 3,
  "prune_tools": "llm",
  "model": "claude-opus-5-5",
  "backend": "claude-cli"
 },
 "clauses": [
  "5",
  "Page 1 has probability 0.5",
  "so in 10 steps the surfer goes there exactly 5 times",
  "Actual: it varies from run to run",
  "five runs gave 6, 4, 8, 5 and 6"
 ],
 "start_concepts": [
  "arithmetic_operators",
  "compound_assignment",
  "println"
 ],
 "held_misconceptions": [
  {
   "concept": "math_random",
   "misconception": "ProbabilityIsPrediction",
   "kind": "misconception",
   "quote": "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
   "score": 0.8075
  }
 ],
 "error_evidence": [],
 "shadowed": [],
 "broken_edges": [
  {
   "edge": "pre:math_library->math_random",
   "quote": "5; so in 10 steps the surfer goes there exactly 5 times",
   "score": 0.8,
   "consequence_of": "mis:math_random->ProbabilityIsPrediction"
  }
 ],
 "root_cause": {
  "concept": "math_random",
  "misconception": "ProbabilityIsPrediction"
 },
 "levels": {
  "for_loop": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "edge": "lvl:for_loop@L3#3",
   "source": "level_way",
   "also_shown": [
    "L3 purpose_of_the_whole"
   ]
  },
  "loop_control": {
   "level": "L3",
   "way": "purpose_of_the_whole",
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "edge": "lvl:loop_control@L3#6",
   "source": "level_way",
   "also_shown": [
    "L1 names_the_element"
   ]
  },
  "math_library": {
   "level": "L2",
   "way": "one_step_execution",
   "quote": "Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6",
   "edge": "lvl:math_library@L2#2",
   "source": "level_way",
   "also_shown": []
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
   "quote": "5; five runs gave 6, 4, 8, 5 and 6",
   "edge": "lvl:println@L2#1",
   "source": "level_way",
   "also_shown": []
  },
  "statement": {
   "level": "L0",
   "way": "everyday_reading",
   "quote": "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
   "edge": "lvl:statement@L0#0",
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
    1,
    5
   ],
   "quote": "5; five runs gave 6, 4, 8, 5 and 6",
   "confidence": 0.55,
   "prune_score": 0.5,
   "score": 0.275,
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
   "confidence": 0.85,
   "prune_score": 0.95,
   "score": 0.8075,
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
   "source": "for_loop",
   "edge": "err:for_loop->WrongIterationCount",
   "target": "WrongIterationCount",
   "kind": "error",
   "label": "correct",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.6,
   "prune_score": 0.5,
   "score": 0.3,
   "logic": "Updates the loop counter so that the loop runs the wrong number of times.",
   "twin_logic": "The init, test and update together decide the number of passes; trace them to check the count.",
   "role": "primary"
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
   "confidence": 0.8,
   "prune_score": 1.0,
   "score": 0.8,
   "logic": "Math.random() is a Math library method; unlike the others it takes no argument and returns a random double in [0, 1).",
   "twin_logic": null,
   "consequence_of": "mis:math_random->ProbabilityIsPrediction"
  },
  {
   "depth": 3,
   "source": "for_loop",
   "edge": "pre:for_loop->loop_body",
   "target": "loop_body",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    5
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times; five runs gave 6, 4, 8, 5 and 6",
   "confidence": 0.7,
   "prune_score": 0.7000000000000001,
   "score": 0.49,
   "logic": "The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "statement",
   "edge": "lvl:statement@L0#0",
   "target": "statement@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.6,
   "prune_score": 0.6000000000000001,
   "score": 0.36,
   "logic": "Everyday reading: a program is read like a text or a list of wishes that the computer takes in all at once, so line order, goals of later lines or what the writer meant can matter. Java rule: each statement is one step, ended by ;, executed once, in written order, using only the current state.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 4,
   "source": "math_library",
   "edge": "lvl:math_library@L2#2",
   "target": "math_library@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    4,
    5
   ],
   "quote": "Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6",
   "confidence": 0.6,
   "prune_score": 0.4,
   "score": 0.24,
   "logic": "All the listed Math methods except random() are mathematical functions: they change no variable and return the same result for the same argument; random() takes no argument and returns a different value on each call.",
   "twin_logic": null,
   "level": "L2",
   "way": "one_step_execution"
  },
  {
   "depth": 4,
   "source": "control_flow",
   "edge": "mis:control_flow->ProgramEndsAfterLoop",
   "target": "ProgramEndsAfterLoop",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    4,
    5
   ],
   "quote": "Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6",
   "confidence": 0.6,
   "prune_score": 0.25,
   "score": 0.15,
   "logic": "When a loop finishes the program ends, so code after the loop never runs.",
   "twin_logic": "When the loop condition becomes false, control continues with the first statement after the loop.",
   "role": "context"
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
    1,
    5
   ],
   "quote": "5; five runs gave 6, 4, 8, 5 and 6",
   "confidence": 0.55,
   "prune_score": 0.5,
   "score": 0.275,
   "logic": "Output is the value's characters followed by a line break: println(\"Hello, \"); println(\"World!\"); prints two lines.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
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
   "prune_score": 0.35,
   "score": 0.175,
   "logic": "i < n and i <= n mean the same, so the loop runs until i equals n and the last pass can use a[n].",
   "twin_logic": "for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n.",
   "role": "primary"
  },
  {
   "depth": 2,
   "source": "loop_control",
   "edge": "lvl:loop_control@L3#6",
   "target": "loop_control@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.55,
   "prune_score": 0.3,
   "score": 0.165,
   "logic": "Plan: counter-controlled loop - the loop variable is a stepper that walks a predictable sequence of values (0..N-1, 1..N, every 2nd value) and fixes the number of passes in advance.",
   "twin_logic": null,
   "level": "L3",
   "way": "purpose_of_the_whole"
  },
  {
   "depth": 2,
   "source": "loop_control",
   "edge": "lvl:loop_control@L1#0",
   "target": "loop_control@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.55,
   "prune_score": 0.2,
   "score": 0.11,
   "logic": "Loop control is the init / continuation condition / increment scheme on an index variable that decides how many passes a loop makes and with which values.",
   "twin_logic": null,
   "level": "L1",
   "way": "names_the_element"
  },
  {
   "depth": 2,
   "source": "for_loop",
   "edge": "err:for_loop->WrongIterationCount",
   "target": "WrongIterationCount",
   "kind": "error",
   "label": "correct",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.6,
   "prune_score": 0.5,
   "score": 0.3,
   "logic": "Updates the loop counter so that the loop runs the wrong number of times.",
   "twin_logic": "The init, test and update together decide the number of passes; trace them to check the count.",
   "role": "primary"
  },
  {
   "depth": 2,
   "source": "for_loop",
   "edge": "mis:for_loop->ForIsConditional",
   "target": "ForIsConditional",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.6,
   "prune_score": 0.3,
   "score": 0.18,
   "logic": "The body of a for statement executes at most once.",
   "twin_logic": "The body of a for statement runs once for every pass on which the condition is true, which can be many times.",
   "role": "primary"
  },
  {
   "depth": 2,
   "source": "for_loop",
   "edge": "lvl:for_loop@L3#3",
   "target": "for_loop@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.6,
   "prune_score": 0.5,
   "score": 0.3,
   "logic": "A simulation runs a fixed number of trials with an outer for loop (for (int t = 0; t < T; t++)), each trial simulated inside the body.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 2,
   "source": "for_loop",
   "edge": "lvl:for_loop@L3#8",
   "target": "for_loop@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.6,
   "prune_score": 0.3,
   "score": 0.18,
   "logic": "Plan: counted loop / counter-controlled repetition - do the body a known number of times, with the loop variable as a stepper (index, term number, trial number).",
   "twin_logic": null,
   "level": "L3",
   "way": "purpose_of_the_whole"
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
   "confidence": 0.85,
   "prune_score": 0.95,
   "score": 0.8075,
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
   "source": "math_random",
   "edge": "lvl:math_random@L3#2",
   "target": "math_random@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    4,
    5
   ],
   "quote": "Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "Each trial of a Monte Carlo simulation draws fresh values with Math.random(); estimates become reliable only over many trials.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 2,
   "source": "math_random",
   "edge": "lvl:math_random@L4#0",
   "target": "math_random@L4",
   "kind": "level",
   "label": "shown",
   "clauses": [
    4,
    5
   ],
   "quote": "Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "Changing N in (int) (Math.random() * N) changes the range to 0..N-1, and adding a constant shifts it; the output changes from run to run, so a program using Math.random() cannot be checked by comparing exact outputs, only by statistics over many runs.",
   "twin_logic": null,
   "level": "L4",
   "way": "predict_a_change"
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
   "confidence": 0.8,
   "prune_score": 1.0,
   "score": 0.8,
   "logic": "Math.random() is a Math library method; unlike the others it takes no argument and returns a random double in [0, 1).",
   "twin_logic": null,
   "consequence_of": "mis:math_random->ProbabilityIsPrediction"
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
   "depth": 3,
   "source": "for_loop",
   "edge": "pre:for_loop->loop_body",
   "target": "loop_body",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    5
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times; five runs gave 6, 4, 8, 5 and 6",
   "confidence": 0.7,
   "prune_score": 0.7000000000000001,
   "score": 0.49,
   "logic": "The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "statement",
   "edge": "lvl:statement@L0#0",
   "target": "statement@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "5; Page 1 has probability 0.5; so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.6,
   "prune_score": 0.6000000000000001,
   "score": 0.36,
   "logic": "Everyday reading: a program is read like a text or a list of wishes that the computer takes in all at once, so line order, goals of later lines or what the writer meant can matter. Java rule: each statement is one step, ended by ;, executed once, in written order, using only the current state.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 3,
   "source": "nested_loops",
   "edge": "mis:nested_loops->OuterLoopIgnored",
   "target": "OuterLoopIgnored",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3
   ],
   "quote": "so in 10 steps the surfer goes there exactly 5 times",
   "confidence": 0.6,
   "prune_score": 0.5,
   "score": 0.3,
   "logic": "In nested loops only the inner loop repeats; the outer loop runs once.",
   "twin_logic": "The outer loop repeats as its own condition says, and the inner loop runs fully on each outer pass.",
   "role": "primary"
  },
  {
   "depth": 4,
   "source": "math_library",
   "edge": "lvl:math_library@L2#2",
   "target": "math_library@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    4,
    5
   ],
   "quote": "Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6",
   "confidence": 0.6,
   "prune_score": 0.4,
   "score": 0.24,
   "logic": "All the listed Math methods except random() are mathematical functions: they change no variable and return the same result for the same argument; random() takes no argument and returns a different value on each call.",
   "twin_logic": null,
   "level": "L2",
   "way": "one_step_execution"
  },
  {
   "depth": 4,
   "source": "control_flow",
   "edge": "mis:control_flow->ProgramEndsAfterLoop",
   "target": "ProgramEndsAfterLoop",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    4,
    5
   ],
   "quote": "Actual: it varies from run to run; five runs gave 6, 4, 8, 5 and 6",
   "confidence": 0.6,
   "prune_score": 0.25,
   "score": 0.15,
   "logic": "When a loop finishes the program ends, so code after the loop never runs.",
   "twin_logic": "When the loop condition becomes false, control continues with the first statement after the loop.",
   "role": "context"
  }
 ],
 "clause_coverage": {
  "5": "lvl:println@L2#1",
  "Page 1 has probability 0.5": "mis:math_random->ProbabilityIsPrediction",
  "so in 10 steps the surfer goes there exactly 5 times": "err:loop_control->WrongIterationCount",
  "Actual: it varies from run to run": "lvl:math_random@L3#2",
  "five runs gave 6, 4, 8, 5 and 6": "lvl:println@L2#1"
 },
 "unexplained_clauses": [],
 "stop_reason": "max depth",
 "depth_reached": 4,
 "llm_calls": 0,
 "llm_cache_hits": 96,
 "llm_calls_by_step": {
  "prune": 32,
  "label": 64
 }
}
```
