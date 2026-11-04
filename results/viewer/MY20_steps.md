# Think on the Graph: every output of the run MY20
## 0. Input
Program:
```java
int n = (int) (Math.random() * 6) + 1;
System.out.println(n);
```
Question: Explain what values n can have

Student's answer: n is a whole number from 1 to 6, for example 4
Settings: width 3, depth 3, prune llm, backend claude-cli, model claude-opus-5-5
## 1. Stage 1: the subgraph G from the code (no model)
Masked code (string and char literals and comments blanked; this is what the patterns see):
```
int n = (int) (Math.random() * 6) + 1;
System.out.println(n);
```
Which code text tagged which concept (a generic concept fires on almost any Java line; it starts the walk only if the answer repeats its tag):
| concept | generic | channel | matched text | line |
|---|---|---|---|---|
| api | False | pattern | 'Math.random(' | 1 |
| arithmetic_operators | False | pattern | ') * 6' | 1 |
| explicit_cast | False | pattern | '(int) (' | 1 |
| expression | True | pattern | ') * 6' | 1 |
| expression | True | pattern | '= (int) (Math.random() * 6) + 1;' | 1 |
| math_library | False | pattern | 'Math.random' | 1 |
| math_random | False | pattern | 'Math.random(' | 1 |
| method_call | False | pattern | 'Math.random(' | 1 |
| primitive_type | True | pattern | 'int' | 1 |
| println | False | pattern | 'System.out.println(' | 2 |
| statement | True | pattern | ';' | 1 |
| type_conversion | False | pattern | '(int) (' | 1 |

G: 11 concept nodes (3 generic), 9 concept edges, 49 misconception / error edges, 42 misconception / error nodes, 55 level nodes, 56 level-misconception links, 2 connected piece(s).
Note: concept nodes form 2 pieces (the KG has no edge between them): api,arithmetic_operators,explicit_cast,expression,math_library,math_random,method_call,primitive_type,type_conversion | println,statement

Concept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):
| edge | type | rule (logic) |
|---|---|---|
| pre:arithmetic_operators->expression | prerequisite | An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones. |
| pre:explicit_cast->math_random | prerequisite | To turn Math.random()'s double in [0, 1) into a random int from 0 to N-1, multiply it by N and cast the result to int. |
| pre:expression->method_call | prerequisite | Method arguments may be expressions, and a method call can be used in expressions in the same way as variables and literals. |
| pre:math_library->math_random | prerequisite | Math.random() is a Math library method; unlike the others it takes no argument and returns a random double in [0, 1). |
| pre:method_call->api | prerequisite | An API lists, for each library method, the signature you need in order to call it: name, argument types and return type. |
| pre:method_call->math_library | prerequisite | Math.sqrt(x) and other Math methods are used through method calls. |
| pre:primitive_type->type_conversion | prerequisite | Conversion moves a value between primitive types: int to double happens automatically, while double to int needs a cast that drops the fraction. |
| pre:statement->println | prerequisite | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |
| pre:type_conversion->explicit_cast | prerequisite | A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2). |

Misconception / error edges per concept (count), and level ways per concept (count):
| concept | misconception / error edges | level ways (L1-L4 + L0 non-misconception) |
|---|---|---|
| api | 0 | 12 |
| arithmetic_operators | 3 | 18 |
| explicit_cast | 6 | 19 |
| expression | 8 | 19 |
| math_library | 4 | 20 |
| math_random | 2 | 16 |
| method_call | 10 | 17 |
| primitive_type | 2 | 21 |
| println | 6 | 17 |
| statement | 5 | 19 |
| type_conversion | 3 | 18 |

Figure 1: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY20_figure01.png

Figure 2: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY20_figure02.png

## 2. Clauses and start concepts (no model)
The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):
| clause | text |
|---|---|
| c1 | n is a whole number from 1 to 6, for example 4 |

start: BM25 of the answer against each tagged concept: arithmetic_operators 9.57 (hits 1), explicit_cast 7.86 (hits 1), math_random 4.79 (hits 1), method_call 4.46 (hits 1), math_library 2.61 (hits 1), api 1.78 (hits 1), type_conversion 1.03 (hits 1), println 0.88 (hits 1)

start: chosen arithmetic_operators, explicit_cast, math_random

start concepts (3): arithmetic_operators, explicit_cast, math_random

Start concepts: arithmetic_operators, explicit_cast, math_random

Figure 3: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY20_figure03.png

## 3. The walk, depth by depth
At each depth, for each current concept: the edges offered (a concept entering as a start concept offers its misconception / error edges and its level ways, as two families; otherwise it offers its concept edges), the prune prompt and the model's reply, then the label prompt(s) and the model's reply, parsed into label / clauses / confidence. Score = prune score x confidence.

### Depth 1: current concepts 'arithmetic_operators', 'explicit_cast', 'math_random'

#### arithmetic_operators, misconceptions: 3 edges offered
Edges offered:
| edge |
|---|
| mis:arithmetic_operators->ArithmeticOnNumericStrings \| wrong rule: "10" - 1 or "6" * "2" works because the strings look like numbers. \| right rule: Arithmetic operators other than + are not defined for Strings; a String of digits must first be converted to a number, e.g. with Integer.parseInt. |
| mis:arithmetic_operators->CaretIsPower \| wrong rule: a^2 computes a squared. \| right rule: Java has no exponent operator; ^ is exclusive or, and a * a or Math.pow(a, 2) computes a squared. |
| mis:arithmetic_operators->RemainderIsSubtraction \| wrong rule: 9 % 5 means 9 minus 5 (a % b subtracts b from a). \| right rule: % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 * 5 + 4, and 17 % 5 is 2, not 12. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:arithmetic_operators->RemainderIsSubtraction (0.40), mis:arithmetic_operators->ArithmeticOnNumericStrings (0.30), mis:arithmetic_operators->CaretIsPower (0.30)
```
Kept by pruning: mis:arithmetic_operators->RemainderIsSubtraction (0.40), mis:arithmetic_operators->ArithmeticOnNumericStrings (0.30), mis:arithmetic_operators->CaretIsPower (0.30)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:arithmetic_operators->RemainderIsSubtraction \| wrong rule: 9 % 5 means 9 minus 5 (a % b subtracts b from a). \| right rule: % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 * 5 + 4, and 17 % 5 is 2, not 12. |
| mis:arithmetic_operators->ArithmeticOnNumericStrings \| wrong rule: "10" - 1 or "6" * "2" works because the strings look like numbers. \| right rule: Arithmetic operators other than + are not defined for Strings; a String of digits must first be converted to a number, e.g. with Integer.parseInt. |
| mis:arithmetic_operators->CaretIsPower \| wrong rule: a^2 computes a squared. \| right rule: Java has no exponent operator; ^ is exclusive or, and a * a or Math.pow(a, 2) computes a squared. |
Model's reply:
```
mis:arithmetic_operators->RemainderIsSubtraction | not applied | clauses: none | confidence: 0.95
mis:arithmetic_operators->ArithmeticOnNumericStrings | not applied | clauses: none | confidence: 0.95
mis:arithmetic_operators->CaretIsPower | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:arithmetic_operators->RemainderIsSubtraction | not applied |  |  | 0.0 |  |  |
| mis:arithmetic_operators->ArithmeticOnNumericStrings | not applied |  |  | 0.0 |  |  |
| mis:arithmetic_operators->CaretIsPower | not applied |  |  | 0.0 |  |  |

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
{lvl:arithmetic_operators@L2#1 (Score: 0.5)}
{lvl:arithmetic_operators@L2#0 (Score: 0.3)}
{lvl:arithmetic_operators@L3#0 (Score: 0.2)}
```
Kept by pruning: lvl:arithmetic_operators@L2#1 (0.50), lvl:arithmetic_operators@L2#0 (0.30), lvl:arithmetic_operators@L3#0 (0.20)

Label prompt for level way lvl:arithmetic_operators@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> With ints, 17 / 3 is 5 and 17 % 3 is 2. With doubles, 5.0 / 3.0 is 1.6666666666666667. With mixed operands, the int is promoted first (10 / 3.0 is 3.333...).

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.6
```

Label prompt for level way lvl:arithmetic_operators@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> The left operand is evaluated fully, then the right operand, and then the operator is applied in the promoted type.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:arithmetic_operators@L3#0 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Operators build larger expressions from smaller ones, and each operand can itself be any expression.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:arithmetic_operators@L2#1 | shown | 0.5 | 0.6 | 0.3 | c1 | n is a whole number from 1 to 6, for example 4 |
| lvl:arithmetic_operators@L2#0 | not applied |  |  | 0.0 |  |  |
| lvl:arithmetic_operators@L3#0 | not applied |  |  | 0.0 |  |  |

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
mis:explicit_cast->CastRounds (0.60), mis:explicit_cast->CastAppliesToWholeExpression (0.30), err:explicit_cast->RoundReturnsInt (0.10)
```
Kept by pruning: mis:explicit_cast->CastRounds (0.60), mis:explicit_cast->CastAppliesToWholeExpression (0.30), err:explicit_cast->RoundReturnsInt (0.10)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:explicit_cast->CastRounds \| wrong rule: (int) 2.7 evaluates to 3. \| right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer. |
| mis:explicit_cast->CastAppliesToWholeExpression \| wrong rule: (int) 2.5 / 0.15 casts the whole quotient to int. \| right rule: The cast applies only to what comes right after it, here 2.5. |
| err:explicit_cast->RoundReturnsInt \| wrong rule: Writes int n = Math.round(x); because Math.round gives an int. \| right rule: Math.round(double) returns a long, so storing it in an int needs a cast: int n = (int) Math.round(x); |
Model's reply:
```
mis:explicit_cast->CastRounds | correct | clauses: 1 | confidence: 0.8
mis:explicit_cast->CastAppliesToWholeExpression | not applied | clauses: none | confidence: 0.85
err:explicit_cast->RoundReturnsInt | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:explicit_cast->CastRounds | correct | 0.6000000000000001 | 0.8 | 0.48 | c1 | n is a whole number from 1 to 6, for example 4 |
| mis:explicit_cast->CastAppliesToWholeExpression | not applied |  |  | 0.0 |  |  |
| err:explicit_cast->RoundReturnsInt | not applied |  |  | 0.0 |  |  |

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
{lvl:explicit_cast@L3#1 (Score: 0.5)}
{lvl:explicit_cast@L3#5 (Score: 0.3)}
{lvl:explicit_cast@L2#1 (Score: 0.2)}
```
Kept by pruning: lvl:explicit_cast@L3#1 (0.50), lvl:explicit_cast@L3#5 (0.30), lvl:explicit_cast@L2#1 (0.20)

Label prompt for level way lvl:explicit_cast@L3#1 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> To turn Math.random()'s double into a random int from 0 to N-1, the cast must enclose the product: (int) (Math.random() * N); casting first gives 0.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Label prompt for level way lvl:explicit_cast@L3#5 (the model saw only the concept, the way's name 'purpose of the whole' and its text; no level):
> Used to discard information on purpose: truncating a scaled random number to an index, taking the integer part, converting between char and int codes ((char) ('a' + k)), or forcing real division with (double) sum / n.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.6
```

Label prompt for level way lvl:explicit_cast@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> (int) 2.71828 is int 2; (int) -2.7 is -2; (int) 11 * 0.3 is double 3.3; (int) (11 * 0.3) is int 3; (double) 3 / 5 is 0.6 but (double) (3 / 5) is 0.0; (char) ('a' + 4) is 'e'.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:explicit_cast@L3#1 | not applied |  |  | 0.0 |  |  |
| lvl:explicit_cast@L3#5 | not applied |  |  | 0.0 |  |  |
| lvl:explicit_cast@L2#1 | shown | 0.2 | 0.6 | 0.12 | c1 | n is a whole number from 1 to 6, for example 4 |

#### math_random, misconceptions: 2 edges offered
Edges offered:
| edge |
|---|
| mis:math_random->ProbabilityIsPrediction \| wrong rule: A probability (e.g. 70%) predicts what the next single trial will do. \| right rule: A probability describes the long-run frequency over many trials, not one outcome. |
| mis:math_random->RandomCanReturnOne \| wrong rule: Math.random() can return exactly 1.0. \| right rule: Math.random() returns a value in [0, 1): 0 is possible, 1 is not. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:math_random->RandomCanReturnOne (Score: 0.85)}
{mis:math_random->ProbabilityIsPrediction (Score: 0.15)}
```
Kept by pruning: mis:math_random->RandomCanReturnOne (0.85), mis:math_random->ProbabilityIsPrediction (0.15)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:math_random->RandomCanReturnOne \| wrong rule: Math.random() can return exactly 1.0. \| right rule: Math.random() returns a value in [0, 1): 0 is possible, 1 is not. |
| mis:math_random->ProbabilityIsPrediction \| wrong rule: A probability (e.g. 70%) predicts what the next single trial will do. \| right rule: A probability describes the long-run frequency over many trials, not one outcome. |
Model's reply:
```
mis:math_random->RandomCanReturnOne | correct | clauses: 1 | confidence: 0.85
mis:math_random->ProbabilityIsPrediction | not applied | clauses: none | confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:math_random->RandomCanReturnOne | correct | 0.85 | 0.85 | 0.72 | c1 | n is a whole number from 1 to 6, for example 4 |
| mis:math_random->ProbabilityIsPrediction | not applied |  |  | 0.0 |  |  |

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
{lvl:math_random@L2#1 (Score: 0.6)}
{lvl:math_random@L4#0 (Score: 0.25)}
{lvl:math_random@L1#1 (Score: 0.15)}
```
Kept by pruning: lvl:math_random@L2#1 (0.60), lvl:math_random@L4#0 (0.25), lvl:math_random@L1#1 (0.15)

Label prompt for level way lvl:math_random@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> A double in [0, 1) that differs from call to call and run to run (e.g. RandomInt 1000 prints 548, then 141); (int) (Math.random() * 6) + 1 is an int from 1 to 6; Math.random() < 0.5 is true about half the time.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.9
```

Label prompt for level way lvl:math_random@L4#0 (the model saw only the concept, the way's name 'predict a change' and its text; no level):
> Changing N in (int) (Math.random() * N) changes the range to 0..N-1, and adding a constant shifts it; the output changes from run to run, so a program using Math.random() cannot be checked by comparing exact outputs, only by statistics over many runs.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:math_random@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> Each call returns a new double r with 0 <= r < 1; multiplying by N gives a value in [0, N), and casting truncates it to an int between 0 and N-1.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:math_random@L2#1 | shown | 0.6 | 0.9 | 0.54 | c1 | n is a whole number from 1 to 6, for example 4 |
| lvl:math_random@L4#0 | not applied |  |  | 0.0 |  |  |
| lvl:math_random@L1#1 | shown | 0.15 | 0.6 | 0.09 | c1 | n is a whole number from 1 to 6, for example 4 |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:math_random->RandomCanReturnOne [correct, tier 2, 0.72], lvl:math_random@L2#1 [shown, tier 2, 0.54], mis:explicit_cast->CastRounds [correct, tier 2, 0.48]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | n is a whole number from 1 to 6, for example 4 | lvl:arithmetic_operators@L2#1 |

**Graph check, not yet read (the walk may not stop while these remain):** pre:arithmetic_operators->expression, pre:explicit_cast->math_random, pre:math_library->math_random, pre:type_conversion->explicit_cast

Figure 4 (the graph after depth 1): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY20_figure04.png

### Depth 2: current concepts 'arithmetic_operators', 'explicit_cast', 'math_random'

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
Label: confirmed
Clauses: 1
Confidence: 0.75
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:arithmetic_operators->expression | confirmed | 1.0 | 0.75 | 0.75 | c1 | n is a whole number from 1 to 6, for example 4 |

#### explicit_cast, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| pre:explicit_cast->math_random \| rule: To turn Math.random()'s double in [0, 1) into a random int from 0 to N-1, multiply it by N and cast the result to int. |
| pre:type_conversion->explicit_cast \| rule: A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:explicit_cast->math_random (Score: 0.6)}
{pre:type_conversion->explicit_cast (Score: 0.4)}
```
Kept by pruning: pre:explicit_cast->math_random (0.60), pre:type_conversion->explicit_cast (0.40)

Label prompt for concept edge pre:explicit_cast->math_random (explicit_cast -> math_random, prerequisite):
> To turn Math.random()'s double in [0, 1) into a random int from 0 to N-1, multiply it by N and cast the result to int.

Model's reply:
```
Label: confirmed
Clauses: 1
Confidence: 0.85
```

Label prompt for concept edge pre:type_conversion->explicit_cast (type_conversion -> explicit_cast, prerequisite):
> A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2).

Model's reply:
```
Label: confirmed
Clauses: 1
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:explicit_cast->math_random | confirmed | 0.6 | 0.85 | 0.51 | c1 | n is a whole number from 1 to 6, for example 4 |
| pre:type_conversion->explicit_cast | confirmed | 0.4 | 0.8 | 0.32 | c1 | n is a whole number from 1 to 6, for example 4 |

#### math_random, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:explicit_cast->math_random \| rule: To turn Math.random()'s double in [0, 1) into a random int from 0 to N-1, multiply it by N and cast the result to int. |
| pre:math_library->math_random \| rule: Math.random() is a Math library method; unlike the others it takes no argument and returns a random double in [0, 1). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
pre:math_library->math_random (1.00)
```
Kept by pruning: pre:math_library->math_random (1.00)

Label prompt for concept edge pre:math_library->math_random (math_library -> math_random, prerequisite):
> Math.random() is a Math library method; unlike the others it takes no argument and returns a random double in [0, 1).

Model's reply:
```
Label: confirmed
Clauses: 1
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:math_library->math_random | confirmed | 1.0 | 0.8 | 0.8 | c1 | n is a whole number from 1 to 6, for example 4 |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:math_library->math_random [confirmed, tier 2, 0.80], pre:arithmetic_operators->expression [confirmed, tier 2, 0.75], pre:explicit_cast->math_random [confirmed, tier 2, 0.51]

reached across pre:math_library->math_random, entered next: math_library

reached across pre:arithmetic_operators->expression, entered next: expression

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | n is a whole number from 1 to 6, for example 4 | lvl:arithmetic_operators@L2#1 |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of expression, own edges of math_library

Figure 5 (the graph after depth 2): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY20_figure05.png

### Depth 3: current concepts 'math_library', 'math_random', 'expression', 'arithmetic_operators', 'explicit_cast'

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
{mis:math_library->CastRounds (Score: 0.9)}
{err:math_library->MathMethodWithoutClassName (Score: 0.05)}
{err:math_library->WrongArgumentType (Score: 0.05)}
```
Kept by pruning: mis:math_library->CastRounds (0.90), err:math_library->MathMethodWithoutClassName (0.05), err:math_library->WrongArgumentType (0.05)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:math_library->CastRounds \| wrong rule: (int) 2.7 evaluates to 3. \| right rule: A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer. |
| err:math_library->MathMethodWithoutClassName \| wrong rule: sqrt(x) calls the square-root method. \| right rule: Library methods are called with the class name, e.g. Math.sqrt(x). |
| err:math_library->WrongArgumentType \| wrong rule: Calls a method with arguments of the wrong type, e.g. Math.sqrt("2"). \| right rule: Each argument must have the type the method's API lists. |
Model's reply:
```
mis:math_library->CastRounds | correct | clauses: 1 | confidence: 0.75
err:math_library->MathMethodWithoutClassName | not applied | clauses: none | confidence: 0.95
err:math_library->WrongArgumentType | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:math_library->CastRounds | correct | 0.9 | 0.75 | 0.68 | c1 | n is a whole number from 1 to 6, for example 4 |
| err:math_library->MathMethodWithoutClassName | not applied |  |  | 0.0 |  |  |
| err:math_library->WrongArgumentType | not applied |  |  | 0.0 |  |  |

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
{lvl:math_library@L3#1 (Score: 0.5)}
{lvl:math_library@L3#3 (Score: 0.3)}
{lvl:math_library@L2#2 (Score: 0.2)}
```
Kept by pruning: lvl:math_library@L3#1 (0.50), lvl:math_library@L3#3 (0.30), lvl:math_library@L2#2 (0.20)

Label prompt for level way lvl:math_library@L3#1 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> In the shuffle, r = i + (int) (Math.random() * (N-i)) scales Math.random() to a uniformly random position between i and N-1, so each remaining card is equally likely.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.8
```

Label prompt for level way lvl:math_library@L3#3 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Math.random() is the one Math method that takes no argument and is not a mathematical function: it returns a random double in [0, 1).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:math_library@L2#2 (the model saw only the concept, the way's name 'one step execution' and its text; no level):
> All the listed Math methods except random() are mathematical functions: they change no variable and return the same result for the same argument; random() takes no argument and returns a different value on each call.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:math_library@L3#1 | not applied |  |  | 0.0 |  |  |
| lvl:math_library@L3#3 | not applied |  |  | 0.0 |  |  |
| lvl:math_library@L2#2 | not applied |  |  | 0.0 |  |  |

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
mis:expression->VariablesHoldExpressions (0.45), mis:expression->TargetTyping (0.35), mis:expression->AssignmentIsEquation (0.20)
```
Kept by pruning: mis:expression->VariablesHoldExpressions (0.45), mis:expression->TargetTyping (0.35), mis:expression->AssignmentIsEquation (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:expression->VariablesHoldExpressions \| wrong rule: = stores the expression itself, not its computed value \| right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y. |
| mis:expression->TargetTyping \| wrong rule: The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction. \| right rule: The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints. |
| mis:expression->AssignmentIsEquation \| wrong rule: An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities. \| right rule: An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable. |
Model's reply:
```
mis:expression->VariablesHoldExpressions | not applied | clauses: none | confidence: 0.85
mis:expression->TargetTyping | not applied | clauses: none | confidence: 0.7
mis:expression->AssignmentIsEquation | not applied | clauses: none | confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:expression->VariablesHoldExpressions | not applied |  |  | 0.0 |  |  |
| mis:expression->TargetTyping | not applied |  |  | 0.0 |  |  |
| mis:expression->AssignmentIsEquation | not applied |  |  | 0.0 |  |  |

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
{lvl:expression@L2#1 (Score: 0.5)}
{lvl:expression@L1#1 (Score: 0.3)}
{lvl:expression@L3#1 (Score: 0.2)}
```
Kept by pruning: lvl:expression@L2#1 (0.50), lvl:expression@L1#1 (0.30), lvl:expression@L3#1 (0.20)

Label prompt for level way lvl:expression@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> An expression produces one value of a type fixed by its operands: hour * 60 + minute with hour = 11 and minute = 59 is the int 719.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.75
```

Label prompt for level way lvl:expression@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> Each operand of an operator can itself be any expression, and a parenthesized expression has the same value as the expression inside. Every expression has a type, determined by its operators and operands.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.6
```

Label prompt for level way lvl:expression@L3#1 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Operators combine operand values into a new value, and the operand types choose the operation (int / truncates, double / does not).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:expression@L2#1 | shown | 0.5 | 0.75 | 0.38 | c1 | n is a whole number from 1 to 6, for example 4 |
| lvl:expression@L1#1 | not applied |  |  | 0.0 |  |  |
| lvl:expression@L3#1 | not applied |  |  | 0.0 |  |  |

#### explicit_cast, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:explicit_cast->math_random \| rule: To turn Math.random()'s double in [0, 1) into a random int from 0 to N-1, multiply it by N and cast the result to int. |
| pre:type_conversion->explicit_cast \| rule: A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
pre:type_conversion->explicit_cast (1.00)
```
Kept by pruning: pre:type_conversion->explicit_cast (1.00)

Label prompt for concept edge pre:type_conversion->explicit_cast (type_conversion -> explicit_cast, prerequisite):
> A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2).

Model's reply:
```
Label: confirmed
Clauses: 1
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:type_conversion->explicit_cast | confirmed | 1.0 | 0.8 | 0.8 | c1 | n is a whole number from 1 to 6, for example 4 |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:type_conversion->explicit_cast [confirmed, tier 2, 0.80], mis:math_library->CastRounds [correct, tier 2, 0.68], lvl:expression@L2#1 [shown, tier 2, 0.38]

reached across pre:type_conversion->explicit_cast, entered next: type_conversion

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | n is a whole number from 1 to 6, for example 4 | lvl:arithmetic_operators@L2#1 |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of type_conversion, pre:expression->method_call, pre:method_call->math_library

Figure 6 (the graph after depth 3): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY20_figure06.png

## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on [], broken at [], prerequisites {'expression': ['arithmetic_operators'], 'math_random': ['explicit_cast', 'math_library'], 'method_call': ['expression'], 'api': ['method_call'], 'math_library': ['method_call'], 'type_conversion': ['primitive_type'], 'println': ['statement'], 'explicit_cast': ['type_conversion']}
- arithmetic_operators: L2 via output_prediction "n is a whole number from 1 to 6, for example 4"
- explicit_cast: L2 via output_prediction "n is a whole number from 1 to 6, for example 4"
- expression: L2 via output_prediction "n is a whole number from 1 to 6, for example 4"
- math_random: L2 via output_prediction "n is a whole number from 1 to 6, for example 4"

**Stop:** max depth at depth 3; prompts {'prune': 14, 'label': 25}, fresh model calls 0, cache hits 39

### Held misconceptions
(none)

### Broken concept edges
(none)

### Root cause: none

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| arithmetic_operators | L2 | output_prediction |  | level_way | n is a whole number from 1 to 6, for example 4 |  |  |  |
| explicit_cast | L2 | output_prediction |  | level_way | n is a whole number from 1 to 6, for example 4 |  |  |  |
| expression | L2 | output_prediction |  | level_way | n is a whole number from 1 to 6, for example 4 |  |  |  |
| math_random | L2 | output_prediction |  | level_way | n is a whole number from 1 to 6, for example 4 |  | L1 states_the_rule |  |

### Overall level: L2

Clause coverage (final):
| clause | covered by |
|---|---|
| n is a whole number from 1 to 6, for example 4 | lvl:arithmetic_operators@L2#1 |

Figure 7 (final picture): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY20_figure07.png

## 5. Every labelled edge (the evidence list, kept or not)
| depth | source | edge | kind | label | prune_score | confidence | score | clauses | quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | arithmetic_operators | lvl:arithmetic_operators@L2#1 | level | shown | 0.5 | 0.6 | 0.3 | [1] | n is a whole number from 1 to 6, for example 4 |
| 1 | explicit_cast | mis:explicit_cast->CastRounds | misconception | correct | 0.6000000000000001 | 0.8 | 0.48 | [1] | n is a whole number from 1 to 6, for example 4 |
| 1 | explicit_cast | lvl:explicit_cast@L2#1 | level | shown | 0.2 | 0.6 | 0.12 | [1] | n is a whole number from 1 to 6, for example 4 |
| 1 | math_random | mis:math_random->RandomCanReturnOne | misconception | correct | 0.85 | 0.85 | 0.7225 | [1] | n is a whole number from 1 to 6, for example 4 |
| 1 | math_random | lvl:math_random@L2#1 | level | shown | 0.6 | 0.9 | 0.54 | [1] | n is a whole number from 1 to 6, for example 4 |
| 1 | math_random | lvl:math_random@L1#1 | level | shown | 0.15 | 0.6 | 0.09 | [1] | n is a whole number from 1 to 6, for example 4 |
| 2 | arithmetic_operators | pre:arithmetic_operators->expression | prerequisite | confirmed | 1.0 | 0.75 | 0.75 | [1] | n is a whole number from 1 to 6, for example 4 |
| 2 | explicit_cast | pre:explicit_cast->math_random | prerequisite | confirmed | 0.6 | 0.85 | 0.51 | [1] | n is a whole number from 1 to 6, for example 4 |
| 2 | explicit_cast | pre:type_conversion->explicit_cast | prerequisite | confirmed | 0.4 | 0.8 | 0.32 | [1] | n is a whole number from 1 to 6, for example 4 |
| 2 | math_random | pre:math_library->math_random | prerequisite | confirmed | 1.0 | 0.8 | 0.8 | [1] | n is a whole number from 1 to 6, for example 4 |
| 3 | math_library | mis:math_library->CastRounds | misconception | correct | 0.9 | 0.75 | 0.675 | [1] | n is a whole number from 1 to 6, for example 4 |
| 3 | expression | lvl:expression@L2#1 | level | shown | 0.5 | 0.75 | 0.375 | [1] | n is a whole number from 1 to 6, for example 4 |
| 3 | explicit_cast | pre:type_conversion->explicit_cast | prerequisite | confirmed | 1.0 | 0.8 | 0.8 | [1] | n is a whole number from 1 to 6, for example 4 |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | math_random | mis:math_random->RandomCanReturnOne | misconception | correct | 0.7225 | [1] |
| 1 | math_random | lvl:math_random@L2#1 | level | shown | 0.54 | [1] |
| 1 | explicit_cast | mis:explicit_cast->CastRounds | misconception | correct | 0.48 | [1] |
| 2 | math_random | pre:math_library->math_random | prerequisite | confirmed | 0.8 | [1] |
| 2 | arithmetic_operators | pre:arithmetic_operators->expression | prerequisite | confirmed | 0.75 | [1] |
| 2 | explicit_cast | pre:explicit_cast->math_random | prerequisite | confirmed | 0.51 | [1] |
| 3 | explicit_cast | pre:type_conversion->explicit_cast | prerequisite | confirmed | 0.8 | [1] |
| 3 | math_library | mis:math_library->CastRounds | misconception | correct | 0.675 | [1] |
| 3 | expression | lvl:expression@L2#1 | level | shown | 0.375 | [1] |

## 7. Raw traversal log
```
clauses: n is a whole number from 1 to 6, for example 4
start: BM25 of the answer against each tagged concept: arithmetic_operators 9.57 (hits 1), explicit_cast 7.86 (hits 1), math_random 4.79 (hits 1), method_call 4.46 (hits 1), math_library 2.61 (hits 1), api 1.78 (hits 1), type_conversion 1.03 (hits 1), println 0.88 (hits 1)
start: chosen arithmetic_operators, explicit_cast, math_random
start concepts (3): arithmetic_operators, explicit_cast, math_random
--- depth 1: current concepts ['arithmetic_operators', 'explicit_cast', 'math_random']
  arithmetic_operators (misconceptions): 3 candidates -> kept mis:arithmetic_operators->RemainderIsSubtraction (0.40), mis:arithmetic_operators->ArithmeticOnNumericStrings (0.30), mis:arithmetic_operators->CaretIsPower (0.30)
    mis:arithmetic_operators->RemainderIsSubtraction -> not applied (0.00) ""
    mis:arithmetic_operators->ArithmeticOnNumericStrings -> not applied (0.00) ""
    mis:arithmetic_operators->CaretIsPower -> not applied (0.00) ""
  arithmetic_operators (level ways): 18 candidates -> kept lvl:arithmetic_operators@L2#1 (0.50), lvl:arithmetic_operators@L2#0 (0.30), lvl:arithmetic_operators@L3#0 (0.20)
    lvl:arithmetic_operators@L2#1 -> shown (0.30) "n is a whole number from 1 to 6, for example 4"
    lvl:arithmetic_operators@L2#0 -> not applied (0.00) ""
    lvl:arithmetic_operators@L3#0 -> not applied (0.00) ""
  explicit_cast (misconceptions): 6 candidates -> kept mis:explicit_cast->CastRounds (0.60), mis:explicit_cast->CastAppliesToWholeExpression (0.30), err:explicit_cast->RoundReturnsInt (0.10)
    mis:explicit_cast->CastRounds -> correct (0.48) "n is a whole number from 1 to 6, for example 4"
    mis:explicit_cast->CastAppliesToWholeExpression -> not applied (0.00) ""
    err:explicit_cast->RoundReturnsInt -> not applied (0.00) ""
  explicit_cast (level ways): 19 candidates -> kept lvl:explicit_cast@L3#1 (0.50), lvl:explicit_cast@L3#5 (0.30), lvl:explicit_cast@L2#1 (0.20)
    lvl:explicit_cast@L3#1 -> not applied (0.00) ""
    lvl:explicit_cast@L3#5 -> not applied (0.00) ""
    lvl:explicit_cast@L2#1 -> shown (0.12) "n is a whole number from 1 to 6, for example 4"
  math_random (misconceptions): 2 candidates -> kept mis:math_random->RandomCanReturnOne (0.85), mis:math_random->ProbabilityIsPrediction (0.15)
    mis:math_random->RandomCanReturnOne -> correct (0.72) "n is a whole number from 1 to 6, for example 4"
    mis:math_random->ProbabilityIsPrediction -> not applied (0.00) ""
  math_random (level ways): 16 candidates -> kept lvl:math_random@L2#1 (0.60), lvl:math_random@L4#0 (0.25), lvl:math_random@L1#1 (0.15)
    lvl:math_random@L2#1 -> shown (0.54) "n is a whole number from 1 to 6, for example 4"
    lvl:math_random@L4#0 -> not applied (0.00) ""
    lvl:math_random@L1#1 -> shown (0.09) "n is a whole number from 1 to 6, for example 4"
  kept: mis:math_random->RandomCanReturnOne [correct, tier 2, 0.72], lvl:math_random@L2#1 [shown, tier 2, 0.54], mis:explicit_cast->CastRounds [correct, tier 2, 0.48]
  clause coverage: c1 <- lvl:arithmetic_operators@L2#1
  not yet read: pre:arithmetic_operators->expression, pre:explicit_cast->math_random, pre:math_library->math_random, pre:type_conversion->explicit_cast
--- depth 2: current concepts ['arithmetic_operators', 'explicit_cast', 'math_random']
  arithmetic_operators (concept edges): 1 candidates -> kept pre:arithmetic_operators->expression (1.00)
    pre:arithmetic_operators->expression -> confirmed (0.75) "n is a whole number from 1 to 6, for example 4"
  explicit_cast (concept edges): 2 candidates -> kept pre:explicit_cast->math_random (0.60), pre:type_conversion->explicit_cast (0.40)
    pre:explicit_cast->math_random -> confirmed (0.51) "n is a whole number from 1 to 6, for example 4"
    pre:type_conversion->explicit_cast -> confirmed (0.32) "n is a whole number from 1 to 6, for example 4"
  math_random (concept edges): 1 candidates -> kept pre:math_library->math_random (1.00)
    pre:math_library->math_random -> confirmed (0.80) "n is a whole number from 1 to 6, for example 4"
  kept: pre:math_library->math_random [confirmed, tier 2, 0.80], pre:arithmetic_operators->expression [confirmed, tier 2, 0.75], pre:explicit_cast->math_random [confirmed, tier 2, 0.51]
  reached across pre:math_library->math_random, entered next: math_library
  reached across pre:arithmetic_operators->expression, entered next: expression
  clause coverage: c1 <- lvl:arithmetic_operators@L2#1
  not yet read: own edges of expression, own edges of math_library
--- depth 3: current concepts ['math_library', 'math_random', 'expression', 'arithmetic_operators', 'explicit_cast']
  math_library (misconceptions): 4 candidates -> kept mis:math_library->CastRounds (0.90), err:math_library->MathMethodWithoutClassName (0.05), err:math_library->WrongArgumentType (0.05)
    mis:math_library->CastRounds -> correct (0.68) "n is a whole number from 1 to 6, for example 4"
    err:math_library->MathMethodWithoutClassName -> not applied (0.00) ""
    err:math_library->WrongArgumentType -> not applied (0.00) ""
  math_library (level ways): 20 candidates -> kept lvl:math_library@L3#1 (0.50), lvl:math_library@L3#3 (0.30), lvl:math_library@L2#2 (0.20)
    lvl:math_library@L3#1 -> not applied (0.00) ""
    lvl:math_library@L3#3 -> not applied (0.00) ""
    lvl:math_library@L2#2 -> not applied (0.00) ""
  expression (misconceptions): 8 candidates -> kept mis:expression->VariablesHoldExpressions (0.45), mis:expression->TargetTyping (0.35), mis:expression->AssignmentIsEquation (0.20)
    mis:expression->VariablesHoldExpressions -> not applied (0.00) ""
    mis:expression->TargetTyping -> not applied (0.00) ""
    mis:expression->AssignmentIsEquation -> not applied (0.00) ""
  expression (level ways): 19 candidates -> kept lvl:expression@L2#1 (0.50), lvl:expression@L1#1 (0.30), lvl:expression@L3#1 (0.20)
    lvl:expression@L2#1 -> shown (0.38) "n is a whole number from 1 to 6, for example 4"
    lvl:expression@L1#1 -> not applied (0.00) ""
    lvl:expression@L3#1 -> not applied (0.00) ""
  explicit_cast (concept edges): 1 candidates -> kept pre:type_conversion->explicit_cast (1.00)
    pre:type_conversion->explicit_cast -> confirmed (0.80) "n is a whole number from 1 to 6, for example 4"
  kept: pre:type_conversion->explicit_cast [confirmed, tier 2, 0.80], mis:math_library->CastRounds [correct, tier 2, 0.68], lvl:expression@L2#1 [shown, tier 2, 0.38]
  reached across pre:type_conversion->explicit_cast, entered next: type_conversion
  clause coverage: c1 <- lvl:arithmetic_operators@L2#1
  not yet read: own edges of type_conversion, pre:expression->method_call, pre:method_call->math_library
  root-cause walk: held on [], broken at [], prerequisites {'expression': ['arithmetic_operators'], 'math_random': ['explicit_cast', 'math_library'], 'method_call': ['expression'], 'api': ['method_call'], 'math_library': ['method_call'], 'type_conversion': ['primitive_type'], 'println': ['statement'], 'explicit_cast': ['type_conversion']}
  level arithmetic_operators: L2 via output_prediction "n is a whole number from 1 to 6, for example 4"
  level explicit_cast: L2 via output_prediction "n is a whole number from 1 to 6, for example 4"
  level expression: L2 via output_prediction "n is a whole number from 1 to 6, for example 4"
  level math_random: L2 via output_prediction "n is a whole number from 1 to 6, for example 4"
```

## 8. Full diagnosis JSON
```json
{
 "scenario": "MY20",
 "settings": {
  "width": 3,
  "depth": 3,
  "prune_tools": "llm",
  "model": "claude-opus-5-5",
  "backend": "claude-cli"
 },
 "clauses": [
  "n is a whole number from 1 to 6, for example 4"
 ],
 "start_concepts": [
  "arithmetic_operators",
  "explicit_cast",
  "math_random"
 ],
 "held_misconceptions": [],
 "error_evidence": [],
 "broken_edges": [],
 "root_cause": null,
 "levels": {
  "arithmetic_operators": {
   "level": "L2",
   "way": "output_prediction",
   "quote": "n is a whole number from 1 to 6, for example 4",
   "edge": "lvl:arithmetic_operators@L2#1",
   "source": "level_way",
   "also_shown": []
  },
  "explicit_cast": {
   "level": "L2",
   "way": "output_prediction",
   "quote": "n is a whole number from 1 to 6, for example 4",
   "edge": "lvl:explicit_cast@L2#1",
   "source": "level_way",
   "also_shown": []
  },
  "expression": {
   "level": "L2",
   "way": "output_prediction",
   "quote": "n is a whole number from 1 to 6, for example 4",
   "edge": "lvl:expression@L2#1",
   "source": "level_way",
   "also_shown": []
  },
  "math_random": {
   "level": "L2",
   "way": "output_prediction",
   "quote": "n is a whole number from 1 to 6, for example 4",
   "edge": "lvl:math_random@L2#1",
   "source": "level_way",
   "also_shown": [
    "L1 states_the_rule"
   ]
  }
 },
 "overall_level": "L2",
 "paths": [
  {
   "depth": 1,
   "source": "math_random",
   "edge": "mis:math_random->RandomCanReturnOne",
   "target": "RandomCanReturnOne",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.85,
   "prune_score": 0.85,
   "score": 0.7225,
   "logic": "Math.random() can return exactly 1.0.",
   "twin_logic": "Math.random() returns a value in [0, 1): 0 is possible, 1 is not."
  },
  {
   "depth": 1,
   "source": "math_random",
   "edge": "lvl:math_random@L2#1",
   "target": "math_random@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.9,
   "prune_score": 0.6,
   "score": 0.54,
   "logic": "A double in [0, 1) that differs from call to call and run to run (e.g. RandomInt 1000 prints 548, then 141); (int) (Math.random() * 6) + 1 is an int from 1 to 6; Math.random() < 0.5 is true about half the time.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "explicit_cast",
   "edge": "mis:explicit_cast->CastRounds",
   "target": "CastRounds",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.8,
   "prune_score": 0.6000000000000001,
   "score": 0.48,
   "logic": "(int) 2.7 evaluates to 3.",
   "twin_logic": "A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer."
  },
  {
   "depth": 2,
   "source": "math_random",
   "edge": "pre:math_library->math_random",
   "target": "math_library",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.8,
   "prune_score": 1.0,
   "score": 0.8,
   "logic": "Math.random() is a Math library method; unlike the others it takes no argument and returns a random double in [0, 1).",
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
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.75,
   "prune_score": 1.0,
   "score": 0.75,
   "logic": "An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "explicit_cast",
   "edge": "pre:explicit_cast->math_random",
   "target": "math_random",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.85,
   "prune_score": 0.6,
   "score": 0.51,
   "logic": "To turn Math.random()'s double in [0, 1) into a random int from 0 to N-1, multiply it by N and cast the result to int.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "explicit_cast",
   "edge": "pre:type_conversion->explicit_cast",
   "target": "type_conversion",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.8,
   "prune_score": 1.0,
   "score": 0.8,
   "logic": "A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2).",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "math_library",
   "edge": "mis:math_library->CastRounds",
   "target": "CastRounds",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.75,
   "prune_score": 0.9,
   "score": 0.675,
   "logic": "(int) 2.7 evaluates to 3.",
   "twin_logic": "A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer."
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "lvl:expression@L2#1",
   "target": "expression@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.75,
   "prune_score": 0.5,
   "score": 0.375,
   "logic": "An expression produces one value of a type fixed by its operands: hour * 60 + minute with hour = 11 and minute = 59 is the int 719.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  }
 ],
 "evidence": [
  {
   "depth": 1,
   "source": "arithmetic_operators",
   "edge": "lvl:arithmetic_operators@L2#1",
   "target": "arithmetic_operators@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.6,
   "prune_score": 0.5,
   "score": 0.3,
   "logic": "With ints, 17 / 3 is 5 and 17 % 3 is 2. With doubles, 5.0 / 3.0 is 1.6666666666666667. With mixed operands, the int is promoted first (10 / 3.0 is 3.333...).",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "explicit_cast",
   "edge": "mis:explicit_cast->CastRounds",
   "target": "CastRounds",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.8,
   "prune_score": 0.6000000000000001,
   "score": 0.48,
   "logic": "(int) 2.7 evaluates to 3.",
   "twin_logic": "A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer."
  },
  {
   "depth": 1,
   "source": "explicit_cast",
   "edge": "lvl:explicit_cast@L2#1",
   "target": "explicit_cast@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "(int) 2.71828 is int 2; (int) -2.7 is -2; (int) 11 * 0.3 is double 3.3; (int) (11 * 0.3) is int 3; (double) 3 / 5 is 0.6 but (double) (3 / 5) is 0.0; (char) ('a' + 4) is 'e'.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "math_random",
   "edge": "mis:math_random->RandomCanReturnOne",
   "target": "RandomCanReturnOne",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.85,
   "prune_score": 0.85,
   "score": 0.7225,
   "logic": "Math.random() can return exactly 1.0.",
   "twin_logic": "Math.random() returns a value in [0, 1): 0 is possible, 1 is not."
  },
  {
   "depth": 1,
   "source": "math_random",
   "edge": "lvl:math_random@L2#1",
   "target": "math_random@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.9,
   "prune_score": 0.6,
   "score": 0.54,
   "logic": "A double in [0, 1) that differs from call to call and run to run (e.g. RandomInt 1000 prints 548, then 141); (int) (Math.random() * 6) + 1 is an int from 1 to 6; Math.random() < 0.5 is true about half the time.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "math_random",
   "edge": "lvl:math_random@L1#1",
   "target": "math_random@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.6,
   "prune_score": 0.15,
   "score": 0.09,
   "logic": "Each call returns a new double r with 0 <= r < 1; multiplying by N gives a value in [0, N), and casting truncates it to an int between 0 and N-1.",
   "twin_logic": null,
   "level": "L1",
   "way": "states_the_rule"
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
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.75,
   "prune_score": 1.0,
   "score": 0.75,
   "logic": "An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "explicit_cast",
   "edge": "pre:explicit_cast->math_random",
   "target": "math_random",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.85,
   "prune_score": 0.6,
   "score": 0.51,
   "logic": "To turn Math.random()'s double in [0, 1) into a random int from 0 to N-1, multiply it by N and cast the result to int.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "explicit_cast",
   "edge": "pre:type_conversion->explicit_cast",
   "target": "type_conversion",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.8,
   "prune_score": 0.4,
   "score": 0.32,
   "logic": "A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2).",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "math_random",
   "edge": "pre:math_library->math_random",
   "target": "math_library",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.8,
   "prune_score": 1.0,
   "score": 0.8,
   "logic": "Math.random() is a Math library method; unlike the others it takes no argument and returns a random double in [0, 1).",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "math_library",
   "edge": "mis:math_library->CastRounds",
   "target": "CastRounds",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.75,
   "prune_score": 0.9,
   "score": 0.675,
   "logic": "(int) 2.7 evaluates to 3.",
   "twin_logic": "A cast to int discards the fractional part (rounds toward zero, so (int) -2.7 is -2); Math.round rounds to the nearest integer."
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "lvl:expression@L2#1",
   "target": "expression@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.75,
   "prune_score": 0.5,
   "score": 0.375,
   "logic": "An expression produces one value of a type fixed by its operands: hour * 60 + minute with hour = 11 and minute = 59 is the int 719.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 3,
   "source": "explicit_cast",
   "edge": "pre:type_conversion->explicit_cast",
   "target": "type_conversion",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "n is a whole number from 1 to 6, for example 4",
   "confidence": 0.8,
   "prune_score": 1.0,
   "score": 0.8,
   "logic": "A cast is the explicit form of type conversion between primitive types, required when the conversion may lose information (e.g. (int) 2.71828 is 2).",
   "twin_logic": null
  }
 ],
 "clause_coverage": {
  "n is a whole number from 1 to 6, for example 4": "lvl:arithmetic_operators@L2#1"
 },
 "unexplained_clauses": [],
 "stop_reason": "max depth",
 "depth_reached": 3,
 "llm_calls": 0,
 "llm_cache_hits": 39,
 "llm_calls_by_step": {
  "prune": 14,
  "label": 25
 }
}
```
