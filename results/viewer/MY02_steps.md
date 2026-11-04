# Think on the Graph: every output of the run MY02
## 0. Input
Program:
```java
int a = -7;
int b = 2;
System.out.println(a / b);
System.out.println(a % b);
```
Question: What does this program print, and why?

Student's answer: It prints -4 and then 1. -7 / 2 is -3.5, and integer division rounds down, so it becomes -4. A remainder is never negative, so -7 % 2 is 1, because -4 * 2 + 1 = -7.
Settings: width 3, depth 3, prune llm, backend claude-cli, model claude-opus-5-5
## 1. Stage 1: the subgraph G from the code (no model)
Masked code (string and char literals and comments blanked; this is what the patterns see):
```
int a = -7;
int b = 2;
System.out.println(a / b);
System.out.println(a % b);
```
Which code text tagged which concept (a generic concept fires on almost any Java line; it starts the walk only if the answer repeats its tag):
| concept | generic | channel | matched text | line |
|---|---|---|---|---|
| arithmetic_operators | False | pattern | 'a / b' | 3 |
| expression | True | pattern | 'a / b' | 3 |
| expression | True | pattern | '= -7;' | 1 |
| integer_division | False | signal | 'int a = -7;\nint b = 2;\nSystem.out.println(a / b' | 1 |
| println | False | pattern | 'System.out.println(' | 3 |
| remainder_operator | False | pattern | 'a % b' | 4 |
| statement | True | pattern | ';' | 1 |

G: 6 concept nodes (2 generic), 4 concept edges, 31 misconception / error edges, 27 misconception / error nodes, 30 level nodes, 37 level-misconception links, 2 connected piece(s).
Note: concept nodes form 2 pieces (the KG has no edge between them): arithmetic_operators,expression,integer_division,remainder_operator | println,statement

Concept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):
| edge | type | rule (logic) |
|---|---|---|
| pre:arithmetic_operators->expression | prerequisite | An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones. |
| pre:arithmetic_operators->integer_division | prerequisite | For ints a and b, / gives the whole quotient q and % gives the remainder r, so that a = b * q + r. |
| pre:integer_division->remainder_operator | prerequisite | % is the companion of integer division: a = (a / b) * b + a % b. |
| pre:statement->println | prerequisite | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |

Misconception / error edges per concept (count), and level ways per concept (count):
| concept | misconception / error edges | level ways (L1-L4 + L0 non-misconception) |
|---|---|---|
| arithmetic_operators | 3 | 18 |
| expression | 8 | 19 |
| integer_division | 6 | 16 |
| println | 6 | 17 |
| remainder_operator | 3 | 14 |
| statement | 5 | 19 |

Figure 1: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY02_figure01.png

Figure 2: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY02_figure02.png

## 2. Clauses and start concepts (no model)
The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):
| clause | text |
|---|---|
| c1 | It prints -4 and then 1 |
| c2 | -7 / 2 is -3.5, and integer division rounds down |
| c3 | so it becomes -4 |
| c4 | A remainder is never negative |
| c5 | so -7 % 2 is 1 |
| c6 | because -4 * 2 + 1 = -7 |

start: BM25 of the answer against each tagged concept: remainder_operator 22.32 (hits 1), arithmetic_operators 16.99 (hits 1), integer_division 15.68 (hits 1), println 10.56 (hits 1)

start: chosen remainder_operator, arithmetic_operators, integer_division

start concepts (3): remainder_operator, arithmetic_operators, integer_division

Start concepts: remainder_operator, arithmetic_operators, integer_division

Figure 3: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY02_figure03.png

## 3. The walk, depth by depth
At each depth, for each current concept: the edges offered (a concept entering as a start concept offers its misconception / error edges and its level ways, as two families; otherwise it offers its concept edges), the prune prompt and the model's reply, then the label prompt(s) and the model's reply, parsed into label / clauses / confidence. Score = prune score x confidence.

### Depth 1: current concepts 'remainder_operator', 'arithmetic_operators', 'integer_division'

#### remainder_operator, misconceptions: 3 edges offered
Edges offered:
| edge |
|---|
| mis:remainder_operator->NegativeRemainderSign \| wrong rule: a % b is never negative, and integer division of a negative number rounds down. \| right rule: a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2. |
| mis:remainder_operator->RemainderIsQuotient \| wrong rule: 17 % 5 is 3 (the quotient). \| right rule: % returns the remainder, so 17 % 5 is 2. |
| mis:remainder_operator->RemainderIsSubtraction \| wrong rule: 9 % 5 means 9 minus 5 (a % b subtracts b from a). \| right rule: % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 * 5 + 4, and 17 % 5 is 2, not 12. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:remainder_operator->NegativeRemainderSign (Score: 0.9)}
{mis:remainder_operator->RemainderIsSubtraction (Score: 0.05)}
{mis:remainder_operator->RemainderIsQuotient (Score: 0.05)}
```
Kept by pruning: mis:remainder_operator->NegativeRemainderSign (0.90), mis:remainder_operator->RemainderIsSubtraction (0.05), mis:remainder_operator->RemainderIsQuotient (0.05)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:remainder_operator->NegativeRemainderSign \| wrong rule: a % b is never negative, and integer division of a negative number rounds down. \| right rule: a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2. |
| mis:remainder_operator->RemainderIsSubtraction \| wrong rule: 9 % 5 means 9 minus 5 (a % b subtracts b from a). \| right rule: % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 * 5 + 4, and 17 % 5 is 2, not 12. |
| mis:remainder_operator->RemainderIsQuotient \| wrong rule: 17 % 5 is 3 (the quotient). \| right rule: % returns the remainder, so 17 % 5 is 2. |
Model's reply:
```
mis:remainder_operator->NegativeRemainderSign | held | clauses: 2, 3, 4, 5 | confidence: 0.97
mis:remainder_operator->RemainderIsSubtraction | not applied | clauses: none | confidence: 0.85
mis:remainder_operator->RemainderIsQuotient | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:remainder_operator->NegativeRemainderSign | held | 0.9 | 0.97 | 0.87 | c2, c3, c4, c5 | -7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1 |
| mis:remainder_operator->RemainderIsSubtraction | not applied |  |  | 0.0 |  |  |
| mis:remainder_operator->RemainderIsQuotient | not applied |  |  | 0.0 |  |  |

#### remainder_operator, level ways: 14 edges offered
Edges offered:
| edge |
|---|
| lvl:remainder_operator@L0#0 \| level L0 way everyday_reading: In everyday use % means percent (50% of x), and in maths 'mod' always gives a non-negative result. In Java % is the remainder of truncating division, and its sign follows the left operand (-14 % 3 is -2). |
| lvl:remainder_operator@L0#3 \| level L0 way inconsistent_trace: Points to LT (compute the truncated quotient, then the remainder). Applied unevenly, a student gives the remainder for positive operands but the mathematical mod for negatives, or swaps quotient and remainder (17 % 5 as 3). (here mixing in: "17 % 5 is 3 (the quotient)") |
| lvl:remainder_operator@L1#0 \| level L1 way names_the_element: Remainder operator %: the binary operator that gives the remainder after dividing a by b. |
| lvl:remainder_operator@L1#1 \| level L1 way states_the_rule: For ints, a % b is defined so that (a / b) * b + a % b equals a. The result takes the sign of a, % by zero throws ArithmeticException, and % also works on doubles. |
| lvl:remainder_operator@L2#0 \| level L2 way line_by_line_trace: Evaluate a, then b, take the quotient rounded toward 0, and give what is left over. % has the same precedence as * and /, and they group left to right. |
| lvl:remainder_operator@L2#1 \| level L2 way output_prediction: 17 % 3 is 2, 76 % 12 is 4, 1234 % 99 is 46, -14 % 3 is -2, and 14 % -3 is 2. |
| lvl:remainder_operator@L2#2 \| level L2 way one_step_execution: r = a % b stores a remainder smaller in size than b and leaves a and b unchanged. If b is 0, ArithmeticException is thrown before anything is stored. |
| lvl:remainder_operator@L3#0 \| level L3 way relation_to_neighbour: % is the companion of integer division, since a == (a / b) * b + a % b. Both use the same quotient rounded toward 0. |
| lvl:remainder_operator@L3#1 \| level L3 way purpose_of_the_whole: Plans: divisibility and parity tests (x % 2 == 0), digit extraction (x % 10), cyclic wrap-around ((i + 1) % n), leap-year rules, and splitting units (76 % 12 inches). |
| lvl:remainder_operator@L4#0 \| level L4 way predict_a_change: Negating a flips the remainder's sign, so n % 2 == 1 fails for negative odd n while n % 2 != 0 still works. Changing the divisor changes the cycle length. Swapping % with / swaps the remainder for the quotient. |
| lvl:remainder_operator@L4#1 \| level L4 way transfer_to_a_new_program: Use % for divisibility, parity, digits, cyclic indices and unit splitting. Do not use it for percentages (use * / 100.0), and do not use it where a non-negative mathematical mod is needed for negative values (adjust the result or use Math.floorMod). |
| lvl:remainder_operator@L4#2 \| level L4 way diagnose_an_error: rule broken: int remainder by zero is undefined. Kind: run-time exception. Trigger class: x % 0, or a divisor variable that is 0: ArithmeticException: / by zero. |
| lvl:remainder_operator@L4#3 \| level L4 way diagnose_an_error: rule broken: The remainder takes the sign of the dividend. Kind: silent logic error. Trigger class: Negative inputs in an odd test written as x % 2 == 1, or in a wrap-around index computed as (i - 1) % n. |
| lvl:remainder_operator@L4#4 \| level L4 way diagnose_an_error: rule broken: % is the remainder, not a percentage. Kind: silent logic error. Trigger class: Writing price % 15 for 15 percent of price. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:remainder_operator@L0#0 (Score: 0.4)}
{lvl:remainder_operator@L0#3 (Score: 0.35)}
{lvl:remainder_operator@L3#0 (Score: 0.25)}
```
Kept by pruning: lvl:remainder_operator@L0#0 (0.40), lvl:remainder_operator@L0#3 (0.35), lvl:remainder_operator@L3#0 (0.25)

Label prompt for level way lvl:remainder_operator@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> In everyday use % means percent (50% of x), and in maths 'mod' always gives a non-negative result. In Java % is the remainder of truncating division, and its sign follows the left operand (-14 % 3 is -2).

Model's reply:
```
Label: shown
Clauses: 4, 5, 6
Confidence: 0.9
```

Label prompt for level way lvl:remainder_operator@L0#3 (the model saw only the concept, the way's name 'inconsistent trace' and its text; no level):
> Points to LT (compute the truncated quotient, then the remainder). Applied unevenly, a student gives the remainder for positive operands but the mathematical mod for negatives, or swaps quotient and remainder (17 % 5 as 3). (here mixing in: "17 % 5 is 3 (the quotient)")

Model's reply:
```
Label: shown
Clauses: 4, 5
Confidence: 0.55
```

Label prompt for level way lvl:remainder_operator@L3#0 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> % is the companion of integer division, since a == (a / b) * b + a % b. Both use the same quotient rounded toward 0.

Model's reply:
```
Label: shown
Clauses: 6
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:remainder_operator@L0#0 | shown | 0.4 | 0.9 | 0.36 | c4, c5, c6 | A remainder is never negative; so -7 % 2 is 1; because -4 * 2 + 1 = -7 |
| lvl:remainder_operator@L0#3 | shown | 0.35 | 0.55 | 0.19 | c4, c5 | A remainder is never negative; so -7 % 2 is 1 |
| lvl:remainder_operator@L3#0 | shown | 0.25 | 0.6 | 0.15 | c6 | because -4 * 2 + 1 = -7 |

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
mis:arithmetic_operators->RemainderIsSubtraction | correct | clauses: 5, 6 | confidence: 0.75
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:arithmetic_operators->RemainderIsSubtraction | correct | 1.0 | 0.75 | 0.75 | c5, c6 | so -7 % 2 is 1; because -4 * 2 + 1 = -7 |

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
{lvl:arithmetic_operators@L3#1 (Score: 0.5)}
{lvl:arithmetic_operators@L2#1 (Score: 0.35)}
{lvl:arithmetic_operators@L2#0 (Score: 0.15)}
```
Kept by pruning: lvl:arithmetic_operators@L3#1 (0.50), lvl:arithmetic_operators@L2#1 (0.35), lvl:arithmetic_operators@L2#0 (0.15)

Label prompt for level way lvl:arithmetic_operators@L3#1 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> For ints, / gives the truncated quotient and % the remainder, so (a / b) * b + a % b == a.

Model's reply:
```
Label: shown
Clauses: 6
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

Label prompt for level way lvl:arithmetic_operators@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> The left operand is evaluated fully, then the right operand, and then the operator is applied in the promoted type.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:arithmetic_operators@L3#1 | shown | 0.5 | 0.6 | 0.3 | c6 | because -4 * 2 + 1 = -7 |
| lvl:arithmetic_operators@L2#1 | not applied |  |  | 0.0 |  |  |
| lvl:arithmetic_operators@L2#0 | not applied |  |  | 0.0 |  |  |

#### integer_division, misconceptions: 6 edges offered
Edges offered:
| edge |
|---|
| mis:integer_division->AllDoublesToAvoidDivision \| wrong rule: Making every variable a double is the right fix for integer division. \| right rule: Use int for countable things and double for measured ones; where a fraction is needed, make one operand of the division a double (or cast) instead of changing every type. |
| mis:integer_division->CastAfterIntDivision \| wrong rule: (double) (3 / 5) is 0.6. \| right rule: The integer division 3 / 5 = 0 happens before the cast, so the result is 0.0. |
| mis:integer_division->IntegerDivisionGivesFraction \| wrong rule: 10 / 3 evaluates to 3.333.... \| right rule: Dividing two ints gives an int: the fractional part is discarded. |
| mis:integer_division->LaterDoubleLiteralFixesDivision \| wrong rule: Changing a later literal to 100.0 fixes an earlier int division. \| right rule: The int division happens first; the double must be in the division itself. |
| mis:integer_division->NegativeRemainderSign \| wrong rule: a % b is never negative, and integer division of a negative number rounds down. \| right rule: a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2. |
| mis:integer_division->TargetTyping \| wrong rule: The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction. \| right rule: The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:integer_division->NegativeRemainderSign (0.75), mis:integer_division->IntegerDivisionGivesFraction (0.20), mis:integer_division->TargetTyping (0.05)
```
Kept by pruning: mis:integer_division->NegativeRemainderSign (0.75), mis:integer_division->IntegerDivisionGivesFraction (0.20), mis:integer_division->TargetTyping (0.05)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:integer_division->NegativeRemainderSign \| wrong rule: a % b is never negative, and integer division of a negative number rounds down. \| right rule: a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2. |
| mis:integer_division->IntegerDivisionGivesFraction \| wrong rule: 10 / 3 evaluates to 3.333.... \| right rule: Dividing two ints gives an int: the fractional part is discarded. |
| mis:integer_division->TargetTyping \| wrong rule: The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction. \| right rule: The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints. |
Model's reply:
```
mis:integer_division->NegativeRemainderSign | held | clauses: 2, 3, 4, 5 | confidence: 0.97
mis:integer_division->IntegerDivisionGivesFraction | correct | clauses: 2, 3 | confidence: 0.75
mis:integer_division->TargetTyping | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:integer_division->NegativeRemainderSign | held | 0.75 | 0.97 | 0.73 | c2, c3, c4, c5 | -7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1 |
| mis:integer_division->IntegerDivisionGivesFraction | correct | 0.2 | 0.75 | 0.15 | c2, c3 | -7 / 2 is -3.5, and integer division rounds down; so it becomes -4 |
| mis:integer_division->TargetTyping | not applied |  |  | 0.0 |  |  |

#### integer_division, level ways: 16 edges offered
Edges offered:
| edge |
|---|
| lvl:integer_division@L0#0 \| level L0 way everyday_reading: In everyday and school arithmetic, 'divide' gives an exact answer or a fraction (10 ÷ 3 = 3 1/3), and rounding goes to the nearest whole number. In Java, / with two int operands discards the fraction, rounding toward zero (59 / 60 is 0). |
| lvl:integer_division@L0#4 \| level L0 way inconsistent_trace: Points to LT (each / looks at its own two operand types when it is evaluated). Applied unevenly, a student evaluates 9/5 as 1.8 in f = (9/5)*c + 32 but as 1 elsewhere, or assumes a later double operand rescues an earlier int division. (here mixing in: "The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction") |
| lvl:integer_division@L1#0 \| level L1 way names_the_element: Integer division: / applied to two integer operands, giving the whole-number quotient with the fractional part discarded. |
| lvl:integer_division@L1#1 \| level L1 way states_the_rule: If both operands of / are integral types, the result is an integer that rounds toward 0 (-14 / 3 is -4). If either operand is a double, the division is floating point. |
| lvl:integer_division@L2#0 \| level L2 way line_by_line_trace: Each / is evaluated when its turn comes (precedence, then left to right), using the types of its own two operands. Promoting the result to double, by a cast or by assignment, happens only afterwards and cannot restore the lost fraction. |
| lvl:integer_division@L2#1 \| level L2 way output_prediction: 10 / 3 is 3, 59 / 60 is 0, 1234 / 99 is 12, -14 / 3 is -4, and (double) (3 / 5) is 0.0. |
| lvl:integer_division@L2#2 \| level L2 way one_step_execution: q = a / b stores the truncated quotient in q and leaves a and b unchanged. If b is 0, an ArithmeticException stops execution before anything is stored. |
| lvl:integer_division@L3#0 \| level L3 way relation_to_neighbour: / and % on ints are paired: q = a / b and r = a % b always satisfy a = b * q + r. |
| lvl:integer_division@L3#1 \| level L3 way relation_to_neighbour: Normalizing counts must divide as doubles. With two ints, counts / total truncates to 0 whenever counts < total. |
| lvl:integer_division@L3#2 \| level L3 way relation_to_neighbour: % gives the remainder of the same truncating division: (a / b) * b + a % b == a. |
| lvl:integer_division@L3#3 \| level L3 way purpose_of_the_whole: Quotient plans: unit conversion (76 / 12 feet), dropping a digit (n / 10), finding a midpoint ((lo + hi) / 2), and computing a bucket or row index (i / cols). |
| lvl:integer_division@L4#0 \| level L4 way predict_a_change: Making one operand a double (10.0 / 3) keeps the fraction (3.333...). Casting after the division does not. Multiplying before dividing preserves precision (59 * 100 / 60 is 98). Changing an operand's sign changes only the quotient's sign, since rounding is toward zero. |
| lvl:integer_division@L4#1 \| level L4 way transfer_to_a_new_program: Use integer division when you want the whole quotient (units, digits, indices, half a size). When a fraction is needed, make one operand a double (10.0 / 3 or (double) a / b) rather than turning every variable into a double. |
| lvl:integer_division@L4#2 \| level L4 way diagnose_an_error: rule broken: With two int operands, / discards the fraction. Kind: silent logic error. Trigger class: Two int operands where a fraction is intended: 9/5 in a temperature formula, count / total, 1 / n, sum / n for an average. |
| lvl:integer_division@L4#3 \| level L4 way diagnose_an_error: rule broken: int division by zero is undefined. Kind: run-time exception. Trigger class: A divisor that evaluates to 0: ArithmeticException: / by zero. |
| lvl:integer_division@L4#4 \| level L4 way diagnose_an_error: rule broken: Integer division rounds toward zero, not down. Kind: silent logic error. Trigger class: Negative operands where floor was expected (-7 / 2 is -3, not -4). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:integer_division@L4#4 (Score: 0.5)}
{lvl:integer_division@L3#0 (Score: 0.3)}
{lvl:integer_division@L1#1 (Score: 0.2)}
```
Kept by pruning: lvl:integer_division@L4#4 (0.50), lvl:integer_division@L3#0 (0.30), lvl:integer_division@L1#1 (0.20)

Label prompt for level way lvl:integer_division@L4#4 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: Integer division rounds toward zero, not down. Kind: silent logic error. Trigger class: Negative operands where floor was expected (-7 / 2 is -3, not -4).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:integer_division@L3#0 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> / and % on ints are paired: q = a / b and r = a % b always satisfy a = b * q + r.

Model's reply:
```
Label: shown
Clauses: 6
Confidence: 0.85
```

Label prompt for level way lvl:integer_division@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> If both operands of / are integral types, the result is an integer that rounds toward 0 (-14 / 3 is -4). If either operand is a double, the division is floating point.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:integer_division@L4#4 | not applied |  |  | 0.0 |  |  |
| lvl:integer_division@L3#0 | shown | 0.3 | 0.85 | 0.26 | c6 | because -4 * 2 + 1 = -7 |
| lvl:integer_division@L1#1 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:remainder_operator->NegativeRemainderSign [held, tier 0, 0.87], mis:integer_division->NegativeRemainderSign [held, tier 0, 0.73], mis:arithmetic_operators->RemainderIsSubtraction [correct, tier 2, 0.75]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | It prints -4 and then 1 | not covered yet |
| c2 | -7 / 2 is -3.5, and integer division rounds down | mis:remainder_operator->NegativeRemainderSign |
| c3 | so it becomes -4 | mis:remainder_operator->NegativeRemainderSign |
| c4 | A remainder is never negative | mis:remainder_operator->NegativeRemainderSign |
| c5 | so -7 % 2 is 1 | mis:remainder_operator->NegativeRemainderSign |
| c6 | because -4 * 2 + 1 = -7 | mis:arithmetic_operators->RemainderIsSubtraction |

**Uncovered clauses bring in (BM25 of the uncovered clauses against unvisited concepts):** println (2.34)

**Graph check, not yet read (the walk may not stop while these remain):** own edges of println, pre:arithmetic_operators->expression, pre:arithmetic_operators->integer_division, pre:integer_division->remainder_operator

Figure 4 (the graph after depth 1): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY02_figure04.png

### Depth 2: current concepts 'remainder_operator', 'integer_division', 'arithmetic_operators', 'println'

#### remainder_operator, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:integer_division->remainder_operator \| rule: % is the companion of integer division: a = (a / b) * b + a % b. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:integer_division->remainder_operator (Score: 1.0)}
```
Kept by pruning: pre:integer_division->remainder_operator (1.00)

Label prompt for concept edge pre:integer_division->remainder_operator (integer_division -> remainder_operator, prerequisite):
> % is the companion of integer division: a = (a / b) * b + a % b.

Model's reply:
```
Label: confirmed
Clauses: 6
Confidence: 0.75
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:integer_division->remainder_operator | confirmed | 1.0 | 0.75 | 0.75 | c6 | because -4 * 2 + 1 = -7 |

#### integer_division, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:arithmetic_operators->integer_division \| rule: For ints a and b, / gives the whole quotient q and % gives the remainder r, so that a = b * q + r. |
| pre:integer_division->remainder_operator \| rule: % is the companion of integer division: a = (a / b) * b + a % b. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:arithmetic_operators->integer_division (Score: 1.0)}
```
Kept by pruning: pre:arithmetic_operators->integer_division (1.00)

Label prompt for concept edge pre:arithmetic_operators->integer_division (arithmetic_operators -> integer_division, prerequisite):
> For ints a and b, / gives the whole quotient q and % gives the remainder r, so that a = b * q + r.

Model's reply:
```
Label: confirmed
Clauses: 3, 5, 6
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:arithmetic_operators->integer_division | confirmed | 1.0 | 0.6 | 0.6 | c3, c5, c6 | so it becomes -4; so -7 % 2 is 1; because -4 * 2 + 1 = -7 |

#### arithmetic_operators, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:arithmetic_operators->expression \| rule: An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones. |
| pre:arithmetic_operators->integer_division \| rule: For ints a and b, / gives the whole quotient q and % gives the remainder r, so that a = b * q + r. |

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
Clauses: 2, 5, 6
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:arithmetic_operators->expression | confirmed | 1.0 | 0.7 | 0.7 | c2, c5, c6 | -7 / 2 is -3.5, and integer division rounds down; so -7 % 2 is 1; because -4 * 2 + 1 = -7 |

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
mis:println->PrintEqualsPrintln (0.50), mis:println->PrintNewLineFirst (0.30), err:println->PrintWithoutFinalNewline (0.20)
```
Kept by pruning: mis:println->PrintEqualsPrintln (0.50), mis:println->PrintNewLineFirst (0.30), err:println->PrintWithoutFinalNewline (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:println->PrintEqualsPrintln \| wrong rule: print and println do the same thing, so print(s1); print(s2); puts s1 and s2 on separate lines. \| right rule: println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line. |
| mis:println->PrintNewLineFirst \| wrong rule: println(s) prints a newline and then s. \| right rule: println(s) prints s and then the newline. |
| err:println->PrintWithoutFinalNewline \| wrong rule: Ends the output with print and expects it to appear right away. \| right rule: Finish a line of print calls with println; some systems hold print output until a newline is printed. |
Model's reply:
```
mis:println->PrintEqualsPrintln | not applied | clauses: none | confidence: 0.9
mis:println->PrintNewLineFirst | not applied | clauses: none | confidence: 0.9
err:println->PrintWithoutFinalNewline | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:println->PrintEqualsPrintln | not applied |  |  | 0.0 |  |  |
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
{lvl:println@L2#1 (Score: 0.4)}
{lvl:println@L3#0 (Score: 0.35)}
{lvl:println@L3#4 (Score: 0.25)}
```
Kept by pruning: lvl:println@L2#1 (0.40), lvl:println@L3#0 (0.35), lvl:println@L3#4 (0.25)

Label prompt for level way lvl:println@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> Output is the value's characters followed by a line break: println("Hello, "); println("World!"); prints two lines.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.6
```

Label prompt for level way lvl:println@L3#0 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> System.out.println(s); is a statement, so its line of output appears at its own place in the sequence.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.7
```

Label prompt for level way lvl:println@L3#4 (the model saw only the concept, the way's name 'purpose of the whole' and its text; no level):
> Purpose: produce one complete line of output, e.g. each result on its own line, or end a line built with print.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.65
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:println@L2#1 | shown | 0.4 | 0.6 | 0.24 | c1 | It prints -4 and then 1 |
| lvl:println@L3#0 | shown | 0.35 | 0.7 | 0.24 | c1 | It prints -4 and then 1 |
| lvl:println@L3#4 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:integer_division->remainder_operator [confirmed, tier 2, 0.75], pre:arithmetic_operators->expression [confirmed, tier 2, 0.70], pre:arithmetic_operators->integer_division [confirmed, tier 2, 0.60]

reached across pre:arithmetic_operators->expression, entered next: expression

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | It prints -4 and then 1 | not covered yet |
| c2 | -7 / 2 is -3.5, and integer division rounds down | mis:remainder_operator->NegativeRemainderSign |
| c3 | so it becomes -4 | mis:remainder_operator->NegativeRemainderSign |
| c4 | A remainder is never negative | mis:remainder_operator->NegativeRemainderSign |
| c5 | so -7 % 2 is 1 | mis:remainder_operator->NegativeRemainderSign |
| c6 | because -4 * 2 + 1 = -7 | mis:arithmetic_operators->RemainderIsSubtraction |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of expression, pre:statement->println

Figure 5 (the graph after depth 2): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY02_figure05.png

### Depth 3: current concepts 'integer_division', 'remainder_operator', 'expression', 'arithmetic_operators', 'println'

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
mis:expression->TargetTyping (0.60), mis:expression->NoAtomicExpression (0.20), mis:expression->VariablesHoldExpressions (0.20)
```
Kept by pruning: mis:expression->TargetTyping (0.60), mis:expression->NoAtomicExpression (0.20), mis:expression->VariablesHoldExpressions (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:expression->TargetTyping \| wrong rule: The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction. \| right rule: The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints. |
| mis:expression->NoAtomicExpression \| wrong rule: A single variable x or a literal on its own is not an expression. \| right rule: A single variable or literal is an expression whose value is just that value. |
| mis:expression->VariablesHoldExpressions \| wrong rule: = stores the expression itself, not its computed value \| right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y. |
Model's reply:
```
mis:expression->TargetTyping | not applied | clauses: none | confidence: 0.85
mis:expression->NoAtomicExpression | not applied | clauses: none | confidence: 0.95
mis:expression->VariablesHoldExpressions | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:expression->TargetTyping | not applied |  |  | 0.0 |  |  |
| mis:expression->NoAtomicExpression | not applied |  |  | 0.0 |  |  |
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
{lvl:expression@L3#1 (Score: 0.45)}
{lvl:expression@L0#0 (Score: 0.3)}
{lvl:expression@L2#1 (Score: 0.25)}
```
Kept by pruning: lvl:expression@L3#1 (0.45), lvl:expression@L0#0 (0.30), lvl:expression@L2#1 (0.25)

Label prompt for level way lvl:expression@L3#1 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Operators combine operand values into a new value, and the operand types choose the operation (int / truncates, double / does not).

Model's reply:
```
Label: shown
Clauses: 2, 3
Confidence: 0.6
```

Label prompt for level way lvl:expression@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> In maths an expression such as 7/2 or x + y names an exact number, and 'expression' means a formula with operators. In Java, any code that evaluates to a typed value is an expression, including a lone literal or variable, and with ints 7/2 evaluates to 3.

Model's reply:
```
Label: shown
Clauses: 2
Confidence: 0.65
```

Label prompt for level way lvl:expression@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> An expression produces one value of a type fixed by its operands: hour * 60 + minute with hour = 11 and minute = 59 is the int 719.

Model's reply:
```
Label: shown
Clauses: 1, 2, 3, 5
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:expression@L3#1 | shown | 0.45 | 0.6 | 0.27 | c2, c3 | -7 / 2 is -3.5, and integer division rounds down; so it becomes -4 |
| lvl:expression@L0#0 | shown | 0.3 | 0.65 | 0.2 | c2 | -7 / 2 is -3.5, and integer division rounds down |
| lvl:expression@L2#1 | shown | 0.25 | 0.7 | 0.17 | c1, c2, c3, c5 | It prints -4 and then 1; -7 / 2 is -3.5, and integer division rounds down; so it becomes -4; so -7 % 2 is 1 |

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
Label: confirmed
Clauses: 1
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:statement->println | confirmed | 1.0 | 0.7 | 0.7 | c1 | It prints -4 and then 1 |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:statement->println [confirmed, tier 2, 0.70], lvl:expression@L3#1 [shown, tier 2, 0.27], lvl:expression@L0#0 [shown, tier 2, 0.20]

reached across pre:statement->println, entered next: statement

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | It prints -4 and then 1 | pre:statement->println |
| c2 | -7 / 2 is -3.5, and integer division rounds down | mis:remainder_operator->NegativeRemainderSign |
| c3 | so it becomes -4 | mis:remainder_operator->NegativeRemainderSign |
| c4 | A remainder is never negative | mis:remainder_operator->NegativeRemainderSign |
| c5 | so -7 % 2 is 1 | mis:remainder_operator->NegativeRemainderSign |
| c6 | because -4 * 2 + 1 = -7 | mis:arithmetic_operators->RemainderIsSubtraction |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of statement

Figure 6 (the graph after depth 3): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY02_figure06.png

### Depth 4: current concepts 'statement'

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
mis:statement->StatementsRunInAnyOrder (0.60), mis:statement->ComputerFillsInIntent (0.20), mis:statement->ProgramLooksAhead (0.20)
```
Kept by pruning: mis:statement->StatementsRunInAnyOrder (0.60), mis:statement->ComputerFillsInIntent (0.20), mis:statement->ProgramLooksAhead (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:statement->StatementsRunInAnyOrder \| wrong rule: Statements in a program can run in any order. \| right rule: Without control statements, statements run once each, top to bottom. |
| mis:statement->ComputerFillsInIntent \| wrong rule: The computer fills in omitted steps or values that the programmer meant, e.g. REPEAT 4 [FORWARD 30] draws a square without a turn command. \| right rule: The computer executes only what the code states; every needed step and value must be written. |
| mis:statement->ProgramLooksAhead \| wrong rule: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. \| right rule: Each statement executes using only the current state; later lines have no effect until control reaches them. |
Model's reply:
```
mis:statement->StatementsRunInAnyOrder | correct | clauses: 1 | confidence: 0.6
mis:statement->ComputerFillsInIntent | not applied | clauses: none | confidence: 0.9
mis:statement->ProgramLooksAhead | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:statement->StatementsRunInAnyOrder | correct | 0.6 | 0.6 | 0.36 | c1 | It prints -4 and then 1 |
| mis:statement->ComputerFillsInIntent | not applied |  |  | 0.0 |  |  |
| mis:statement->ProgramLooksAhead | not applied |  |  | 0.0 |  |  |

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
{lvl:statement@L3#3 (Score: 0.4)}
{lvl:statement@L2#0 (Score: 0.3)}
{lvl:statement@L2#2 (Score: 0.3)}
```
Kept by pruning: lvl:statement@L3#3 (0.40), lvl:statement@L2#0 (0.30), lvl:statement@L2#2 (0.30)

Label prompt for level way lvl:statement@L3#3 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> System.out.println(s); is a statement, so its line of output appears at its place in the sequence; swapping two println statements swaps the output lines.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.55
```

Label prompt for level way lvl:statement@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Statements run one at a time, from first to last; each completes (normally or abruptly) before the next starts.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.55
```

Label prompt for level way lvl:statement@L2#2 (the model saw only the concept, the way's name 'one step execution' and its text; no level):
> Executing one statement applies its single effect to the current state (e.g. prints one string, or stores one value) and then control moves to the next statement.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:statement@L3#3 | shown | 0.4 | 0.55 | 0.22 | c1 | It prints -4 and then 1 |
| lvl:statement@L2#0 | shown | 0.3 | 0.55 | 0.17 | c1 | It prints -4 and then 1 |
| lvl:statement@L2#2 | shown | 0.3 | 0.6 | 0.18 | c1 | It prints -4 and then 1 |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:statement->StatementsRunInAnyOrder [correct, tier 2, 0.36], lvl:statement@L3#3 [shown, tier 2, 0.22], lvl:statement@L2#2 [shown, tier 2, 0.18]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | It prints -4 and then 1 | pre:statement->println |
| c2 | -7 / 2 is -3.5, and integer division rounds down | mis:remainder_operator->NegativeRemainderSign |
| c3 | so it becomes -4 | mis:remainder_operator->NegativeRemainderSign |
| c4 | A remainder is never negative | mis:remainder_operator->NegativeRemainderSign |
| c5 | so -7 % 2 is 1 | mis:remainder_operator->NegativeRemainderSign |
| c6 | because -4 * 2 + 1 = -7 | mis:arithmetic_operators->RemainderIsSubtraction |

Figure 7 (the graph after depth 4): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY02_figure07.png

Held set after the one-fault rules: mis:remainder_operator->NegativeRemainderSign; filed at the dependent concept: mis:integer_division->NegativeRemainderSign

Shadows (a held label on a prerequisite or a generic concept that rests on the words of a stronger label at the specific concept is one wrong sentence read twice; it marks no root cause and sets no level): mis:integer_division->NegativeRemainderSign (shadow of mis:remainder_operator->NegativeRemainderSign)

## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on ['remainder_operator'], broken at [], prerequisites {'expression': ['arithmetic_operators'], 'integer_division': ['arithmetic_operators'], 'remainder_operator': ['integer_division'], 'println': ['statement']}
- arithmetic_operators: L3 via relation_to_neighbour "because -4 * 2 + 1 = -7"
- expression: L3 via relation_to_neighbour "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4"
- integer_division: L3 via relation_to_neighbour "because -4 * 2 + 1 = -7"
- println: L3 via relation_to_neighbour "It prints -4 and then 1"
- remainder_operator: L0 via misconception "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1"
- statement: L3 via relation_to_neighbour "It prints -4 and then 1"

**Stop:** sufficient at depth 4; prompts {'prune': 16, 'label': 28}, fresh model calls 0, cache hits 44

### Held misconceptions
| concept | misconception | kind | quote | score | shares_evidence_with |
|---|---|---|---|---|---|
| remainder_operator | NegativeRemainderSign | misconception | -7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1 | 0.873 |  |

### Shadowed labels (held in the reading, folded into the label they shadow; not faults of their own)
| concept | misconception | shadow_of | quote | score |
|---|---|---|---|---|
| integer_division | NegativeRemainderSign | mis:remainder_operator->NegativeRemainderSign | -7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1 | 0.7275 |

### Broken concept edges
(none)

### Root cause: remainder_operator / NegativeRemainderSign

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| arithmetic_operators | L3 | relation_to_neighbour |  | level_way | because -4 * 2 + 1 = -7 |  |  |  |
| expression | L3 | relation_to_neighbour |  | level_way | -7 / 2 is -3.5, and integer division rounds down; so it becomes -4 |  | L2 output_prediction, L0 everyday_reading |  |
| integer_division | L3 | relation_to_neighbour |  | level_way | because -4 * 2 + 1 = -7 |  |  |  |
| println | L3 | relation_to_neighbour |  | level_way | It prints -4 and then 1 |  | L2 output_prediction |  |
| remainder_operator | L0 | misconception | NegativeRemainderSign | level_mis_links | -7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1 | wrong rule: a % b is never negative, and integer division of a negative number rounds down. Right rule: a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2. |  |  |
| statement | L3 | relation_to_neighbour |  | level_way | It prints -4 and then 1 |  | L2 one_step_execution, L2 line_by_line_trace |  |

### Overall level: L0

Clause coverage (final):
| clause | covered by |
|---|---|
| It prints -4 and then 1 | lvl:println@L2#1 |
| -7 / 2 is -3.5, and integer division rounds down | mis:remainder_operator->NegativeRemainderSign |
| so it becomes -4 | mis:remainder_operator->NegativeRemainderSign |
| A remainder is never negative | mis:remainder_operator->NegativeRemainderSign |
| so -7 % 2 is 1 | mis:remainder_operator->NegativeRemainderSign |
| because -4 * 2 + 1 = -7 | lvl:remainder_operator@L0#0 |

Figure 8 (final picture): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY02_figure08.png

## 5. Every labelled edge (the evidence list, kept or not)
| depth | source | edge | kind | label | prune_score | confidence | score | clauses | quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | remainder_operator | mis:remainder_operator->NegativeRemainderSign | misconception | held | 0.9 | 0.97 | 0.873 | [2, 3, 4, 5] | -7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1 |
| 1 | remainder_operator | lvl:remainder_operator@L0#0 | level | shown | 0.4 | 0.9 | 0.36 | [4, 5, 6] | A remainder is never negative; so -7 % 2 is 1; because -4 * 2 + 1 = -7 |
| 1 | remainder_operator | lvl:remainder_operator@L0#3 | level | shown | 0.35 | 0.55 | 0.1925 | [4, 5] | A remainder is never negative; so -7 % 2 is 1 |
| 1 | remainder_operator | lvl:remainder_operator@L3#0 | level | shown | 0.25 | 0.6 | 0.15 | [6] | because -4 * 2 + 1 = -7 |
| 1 | arithmetic_operators | mis:arithmetic_operators->RemainderIsSubtraction | misconception | correct | 1.0 | 0.75 | 0.75 | [5, 6] | so -7 % 2 is 1; because -4 * 2 + 1 = -7 |
| 1 | arithmetic_operators | lvl:arithmetic_operators@L3#1 | level | shown | 0.5 | 0.6 | 0.3 | [6] | because -4 * 2 + 1 = -7 |
| 1 | integer_division | mis:integer_division->NegativeRemainderSign | misconception | held | 0.75 | 0.97 | 0.7275 | [2, 3, 4, 5] | -7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1 |
| 1 | integer_division | mis:integer_division->IntegerDivisionGivesFraction | misconception | correct | 0.2 | 0.75 | 0.15 | [2, 3] | -7 / 2 is -3.5, and integer division rounds down; so it becomes -4 |
| 1 | integer_division | lvl:integer_division@L3#0 | level | shown | 0.3 | 0.85 | 0.255 | [6] | because -4 * 2 + 1 = -7 |
| 2 | remainder_operator | pre:integer_division->remainder_operator | prerequisite | confirmed | 1.0 | 0.75 | 0.75 | [6] | because -4 * 2 + 1 = -7 |
| 2 | integer_division | pre:arithmetic_operators->integer_division | prerequisite | confirmed | 1.0 | 0.6 | 0.6 | [3, 5, 6] | so it becomes -4; so -7 % 2 is 1; because -4 * 2 + 1 = -7 |
| 2 | arithmetic_operators | pre:arithmetic_operators->expression | prerequisite | confirmed | 1.0 | 0.7 | 0.7 | [2, 5, 6] | -7 / 2 is -3.5, and integer division rounds down; so -7 % 2 is 1; because -4 * 2 + 1 = -7 |
| 2 | println | lvl:println@L2#1 | level | shown | 0.4 | 0.6 | 0.24 | [1] | It prints -4 and then 1 |
| 2 | println | lvl:println@L3#0 | level | shown | 0.35 | 0.7 | 0.245 | [1] | It prints -4 and then 1 |
| 3 | expression | lvl:expression@L3#1 | level | shown | 0.45 | 0.6 | 0.27 | [2, 3] | -7 / 2 is -3.5, and integer division rounds down; so it becomes -4 |
| 3 | expression | lvl:expression@L0#0 | level | shown | 0.3 | 0.65 | 0.195 | [2] | -7 / 2 is -3.5, and integer division rounds down |
| 3 | expression | lvl:expression@L2#1 | level | shown | 0.25 | 0.7 | 0.175 | [1, 2, 3, 5] | It prints -4 and then 1; -7 / 2 is -3.5, and integer division rounds down; so it becomes -4; so -7 % 2 is 1 |
| 3 | println | pre:statement->println | prerequisite | confirmed | 1.0 | 0.7 | 0.7 | [1] | It prints -4 and then 1 |
| 4 | statement | mis:statement->StatementsRunInAnyOrder | misconception | correct | 0.6 | 0.6 | 0.36 | [1] | It prints -4 and then 1 |
| 4 | statement | lvl:statement@L3#3 | level | shown | 0.4 | 0.55 | 0.22 | [1] | It prints -4 and then 1 |
| 4 | statement | lvl:statement@L2#0 | level | shown | 0.3 | 0.55 | 0.165 | [1] | It prints -4 and then 1 |
| 4 | statement | lvl:statement@L2#2 | level | shown | 0.3 | 0.6 | 0.18 | [1] | It prints -4 and then 1 |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | remainder_operator | mis:remainder_operator->NegativeRemainderSign | misconception | held | 0.873 | [2, 3, 4, 5] |
| 1 | integer_division | mis:integer_division->NegativeRemainderSign | misconception | held | 0.7275 | [2, 3, 4, 5] |
| 1 | arithmetic_operators | mis:arithmetic_operators->RemainderIsSubtraction | misconception | correct | 0.75 | [5, 6] |
| 2 | remainder_operator | pre:integer_division->remainder_operator | prerequisite | confirmed | 0.75 | [6] |
| 2 | arithmetic_operators | pre:arithmetic_operators->expression | prerequisite | confirmed | 0.7 | [2, 5, 6] |
| 2 | integer_division | pre:arithmetic_operators->integer_division | prerequisite | confirmed | 0.6 | [3, 5, 6] |
| 3 | println | pre:statement->println | prerequisite | confirmed | 0.7 | [1] |
| 3 | expression | lvl:expression@L3#1 | level | shown | 0.27 | [2, 3] |
| 3 | expression | lvl:expression@L0#0 | level | shown | 0.195 | [2] |
| 4 | statement | mis:statement->StatementsRunInAnyOrder | misconception | correct | 0.36 | [1] |
| 4 | statement | lvl:statement@L3#3 | level | shown | 0.22 | [1] |
| 4 | statement | lvl:statement@L2#2 | level | shown | 0.18 | [1] |

## 7. Raw traversal log
```
clauses: It prints -4 and then 1 | -7 / 2 is -3.5, and integer division rounds down | so it becomes -4 | A remainder is never negative | so -7 % 2 is 1 | because -4 * 2 + 1 = -7
start: BM25 of the answer against each tagged concept: remainder_operator 22.32 (hits 1), arithmetic_operators 16.99 (hits 1), integer_division 15.68 (hits 1), println 10.56 (hits 1)
start: chosen remainder_operator, arithmetic_operators, integer_division
start concepts (3): remainder_operator, arithmetic_operators, integer_division
--- depth 1: current concepts ['remainder_operator', 'arithmetic_operators', 'integer_division']
  remainder_operator (misconceptions): 3 candidates -> kept mis:remainder_operator->NegativeRemainderSign (0.90), mis:remainder_operator->RemainderIsSubtraction (0.05), mis:remainder_operator->RemainderIsQuotient (0.05)
    mis:remainder_operator->NegativeRemainderSign -> held (0.87) "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1"
    mis:remainder_operator->RemainderIsSubtraction -> not applied (0.00) ""
    mis:remainder_operator->RemainderIsQuotient -> not applied (0.00) ""
  remainder_operator (level ways): 14 candidates -> kept lvl:remainder_operator@L0#0 (0.40), lvl:remainder_operator@L0#3 (0.35), lvl:remainder_operator@L3#0 (0.25)
    lvl:remainder_operator@L0#0 -> shown (0.36) "A remainder is never negative; so -7 % 2 is 1; because -4 * 2 + 1 = -7"
    lvl:remainder_operator@L0#3 -> shown (0.19) "A remainder is never negative; so -7 % 2 is 1"
    lvl:remainder_operator@L3#0 -> shown (0.15) "because -4 * 2 + 1 = -7"
  arithmetic_operators (misconceptions): 3 candidates -> kept mis:arithmetic_operators->RemainderIsSubtraction (1.00)
    mis:arithmetic_operators->RemainderIsSubtraction -> correct (0.75) "so -7 % 2 is 1; because -4 * 2 + 1 = -7"
  arithmetic_operators (level ways): 18 candidates -> kept lvl:arithmetic_operators@L3#1 (0.50), lvl:arithmetic_operators@L2#1 (0.35), lvl:arithmetic_operators@L2#0 (0.15)
    lvl:arithmetic_operators@L3#1 -> shown (0.30) "because -4 * 2 + 1 = -7"
    lvl:arithmetic_operators@L2#1 -> not applied (0.00) ""
    lvl:arithmetic_operators@L2#0 -> not applied (0.00) ""
  integer_division (misconceptions): 6 candidates -> kept mis:integer_division->NegativeRemainderSign (0.75), mis:integer_division->IntegerDivisionGivesFraction (0.20), mis:integer_division->TargetTyping (0.05)
    mis:integer_division->NegativeRemainderSign -> held (0.73) "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1"
    mis:integer_division->IntegerDivisionGivesFraction -> correct (0.15) "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4"
    mis:integer_division->TargetTyping -> not applied (0.00) ""
  integer_division (level ways): 16 candidates -> kept lvl:integer_division@L4#4 (0.50), lvl:integer_division@L3#0 (0.30), lvl:integer_division@L1#1 (0.20)
    lvl:integer_division@L4#4 -> not applied (0.00) ""
    lvl:integer_division@L3#0 -> shown (0.26) "because -4 * 2 + 1 = -7"
    lvl:integer_division@L1#1 -> not applied (0.00) ""
  kept: mis:remainder_operator->NegativeRemainderSign [held, tier 0, 0.87], mis:integer_division->NegativeRemainderSign [held, tier 0, 0.73], mis:arithmetic_operators->RemainderIsSubtraction [correct, tier 2, 0.75]
  clause coverage: c1 uncovered; c2 <- mis:remainder_operator->NegativeRemainderSign; c3 <- mis:remainder_operator->NegativeRemainderSign; c4 <- mis:remainder_operator->NegativeRemainderSign; c5 <- mis:remainder_operator->NegativeRemainderSign; c6 <- mis:arithmetic_operators->RemainderIsSubtraction
  uncovered clauses bring in: println (2.34)
  not yet read: own edges of println, pre:arithmetic_operators->expression, pre:arithmetic_operators->integer_division, pre:integer_division->remainder_operator
--- depth 2: current concepts ['remainder_operator', 'integer_division', 'arithmetic_operators', 'println']
  remainder_operator (concept edges): 1 candidates -> kept pre:integer_division->remainder_operator (1.00)
    pre:integer_division->remainder_operator -> confirmed (0.75) "because -4 * 2 + 1 = -7"
  integer_division (concept edges): 1 candidates -> kept pre:arithmetic_operators->integer_division (1.00)
    pre:arithmetic_operators->integer_division -> confirmed (0.60) "so it becomes -4; so -7 % 2 is 1; because -4 * 2 + 1 = -7"
  arithmetic_operators (concept edges): 1 candidates -> kept pre:arithmetic_operators->expression (1.00)
    pre:arithmetic_operators->expression -> confirmed (0.70) "-7 / 2 is -3.5, and integer division rounds down; so -7 % 2 is 1; because -4 * 2 + 1 = -7"
  println (misconceptions): 6 candidates -> kept mis:println->PrintEqualsPrintln (0.50), mis:println->PrintNewLineFirst (0.30), err:println->PrintWithoutFinalNewline (0.20)
    mis:println->PrintEqualsPrintln -> not applied (0.00) ""
    mis:println->PrintNewLineFirst -> not applied (0.00) ""
    err:println->PrintWithoutFinalNewline -> not applied (0.00) ""
  println (level ways): 17 candidates -> kept lvl:println@L2#1 (0.40), lvl:println@L3#0 (0.35), lvl:println@L3#4 (0.25)
    lvl:println@L2#1 -> shown (0.24) "It prints -4 and then 1"
    lvl:println@L3#0 -> shown (0.24) "It prints -4 and then 1"
    lvl:println@L3#4 -> not applied (0.00) ""
  kept: pre:integer_division->remainder_operator [confirmed, tier 2, 0.75], pre:arithmetic_operators->expression [confirmed, tier 2, 0.70], pre:arithmetic_operators->integer_division [confirmed, tier 2, 0.60]
  reached across pre:arithmetic_operators->expression, entered next: expression
  clause coverage: c1 uncovered; c2 <- mis:remainder_operator->NegativeRemainderSign; c3 <- mis:remainder_operator->NegativeRemainderSign; c4 <- mis:remainder_operator->NegativeRemainderSign; c5 <- mis:remainder_operator->NegativeRemainderSign; c6 <- mis:arithmetic_operators->RemainderIsSubtraction
  not yet read: own edges of expression, pre:statement->println
--- depth 3: current concepts ['integer_division', 'remainder_operator', 'expression', 'arithmetic_operators', 'println']
  expression (misconceptions): 8 candidates -> kept mis:expression->TargetTyping (0.60), mis:expression->NoAtomicExpression (0.20), mis:expression->VariablesHoldExpressions (0.20)
    mis:expression->TargetTyping -> not applied (0.00) ""
    mis:expression->NoAtomicExpression -> not applied (0.00) ""
    mis:expression->VariablesHoldExpressions -> not applied (0.00) ""
  expression (level ways): 19 candidates -> kept lvl:expression@L3#1 (0.45), lvl:expression@L0#0 (0.30), lvl:expression@L2#1 (0.25)
    lvl:expression@L3#1 -> shown (0.27) "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4"
    lvl:expression@L0#0 -> shown (0.20) "-7 / 2 is -3.5, and integer division rounds down"
    lvl:expression@L2#1 -> shown (0.17) "It prints -4 and then 1; -7 / 2 is -3.5, and integer division rounds down; so it becomes -4; so -7 % 2 is 1"
  println (concept edges): 1 candidates -> kept pre:statement->println (1.00)
    pre:statement->println -> confirmed (0.70) "It prints -4 and then 1"
  kept: pre:statement->println [confirmed, tier 2, 0.70], lvl:expression@L3#1 [shown, tier 2, 0.27], lvl:expression@L0#0 [shown, tier 2, 0.20]
  reached across pre:statement->println, entered next: statement
  clause coverage: c1 <- pre:statement->println; c2 <- mis:remainder_operator->NegativeRemainderSign; c3 <- mis:remainder_operator->NegativeRemainderSign; c4 <- mis:remainder_operator->NegativeRemainderSign; c5 <- mis:remainder_operator->NegativeRemainderSign; c6 <- mis:arithmetic_operators->RemainderIsSubtraction
  not yet read: own edges of statement
--- depth 4: current concepts ['statement'] (closing round: own edges only)
  statement (misconceptions): 5 candidates -> kept mis:statement->StatementsRunInAnyOrder (0.60), mis:statement->ComputerFillsInIntent (0.20), mis:statement->ProgramLooksAhead (0.20)
    mis:statement->StatementsRunInAnyOrder -> correct (0.36) "It prints -4 and then 1"
    mis:statement->ComputerFillsInIntent -> not applied (0.00) ""
    mis:statement->ProgramLooksAhead -> not applied (0.00) ""
  statement (level ways): 19 candidates -> kept lvl:statement@L3#3 (0.40), lvl:statement@L2#0 (0.30), lvl:statement@L2#2 (0.30)
    lvl:statement@L3#3 -> shown (0.22) "It prints -4 and then 1"
    lvl:statement@L2#0 -> shown (0.17) "It prints -4 and then 1"
    lvl:statement@L2#2 -> shown (0.18) "It prints -4 and then 1"
  kept: mis:statement->StatementsRunInAnyOrder [correct, tier 2, 0.36], lvl:statement@L3#3 [shown, tier 2, 0.22], lvl:statement@L2#2 [shown, tier 2, 0.18]
  clause coverage: c1 <- pre:statement->println; c2 <- mis:remainder_operator->NegativeRemainderSign; c3 <- mis:remainder_operator->NegativeRemainderSign; c4 <- mis:remainder_operator->NegativeRemainderSign; c5 <- mis:remainder_operator->NegativeRemainderSign; c6 <- mis:arithmetic_operators->RemainderIsSubtraction
  held: mis:remainder_operator->NegativeRemainderSign; filed at the dependent concept: mis:integer_division->NegativeRemainderSign
  shadows: mis:integer_division->NegativeRemainderSign (shadow of mis:remainder_operator->NegativeRemainderSign)
  root-cause walk: held on ['remainder_operator'], broken at [], prerequisites {'expression': ['arithmetic_operators'], 'integer_division': ['arithmetic_operators'], 'remainder_operator': ['integer_division'], 'println': ['statement']}
  level arithmetic_operators: L3 via relation_to_neighbour "because -4 * 2 + 1 = -7"
  level expression: L3 via relation_to_neighbour "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4"
  level integer_division: L3 via relation_to_neighbour "because -4 * 2 + 1 = -7"
  level println: L3 via relation_to_neighbour "It prints -4 and then 1"
  level remainder_operator: L0 via misconception "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1"
  level statement: L3 via relation_to_neighbour "It prints -4 and then 1"
```

## 8. Full diagnosis JSON
```json
{
 "scenario": "MY02",
 "settings": {
  "width": 3,
  "depth": 3,
  "prune_tools": "llm",
  "model": "claude-opus-5-5",
  "backend": "claude-cli"
 },
 "clauses": [
  "It prints -4 and then 1",
  "-7 / 2 is -3.5, and integer division rounds down",
  "so it becomes -4",
  "A remainder is never negative",
  "so -7 % 2 is 1",
  "because -4 * 2 + 1 = -7"
 ],
 "start_concepts": [
  "remainder_operator",
  "arithmetic_operators",
  "integer_division"
 ],
 "held_misconceptions": [
  {
   "concept": "remainder_operator",
   "misconception": "NegativeRemainderSign",
   "kind": "misconception",
   "quote": "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1",
   "score": 0.873
  }
 ],
 "error_evidence": [],
 "shadowed": [
  {
   "concept": "integer_division",
   "misconception": "NegativeRemainderSign",
   "shadow_of": "mis:remainder_operator->NegativeRemainderSign",
   "quote": "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1",
   "score": 0.7275
  }
 ],
 "broken_edges": [],
 "root_cause": {
  "concept": "remainder_operator",
  "misconception": "NegativeRemainderSign"
 },
 "levels": {
  "arithmetic_operators": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "because -4 * 2 + 1 = -7",
   "edge": "lvl:arithmetic_operators@L3#1",
   "source": "level_way",
   "also_shown": []
  },
  "expression": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4",
   "edge": "lvl:expression@L3#1",
   "source": "level_way",
   "also_shown": [
    "L2 output_prediction",
    "L0 everyday_reading"
   ]
  },
  "integer_division": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "because -4 * 2 + 1 = -7",
   "edge": "lvl:integer_division@L3#0",
   "source": "level_way",
   "also_shown": []
  },
  "println": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "It prints -4 and then 1",
   "edge": "lvl:println@L3#0",
   "source": "level_way",
   "also_shown": [
    "L2 output_prediction"
   ]
  },
  "remainder_operator": {
   "level": "L0",
   "way": "misconception",
   "misconception": "NegativeRemainderSign",
   "quote": "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1",
   "edge": "mis:remainder_operator->NegativeRemainderSign",
   "rule": "wrong rule: a % b is never negative, and integer division of a negative number rounds down. Right rule: a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2.",
   "source": "level_mis_links"
  },
  "statement": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "It prints -4 and then 1",
   "edge": "lvl:statement@L3#3",
   "source": "level_way",
   "also_shown": [
    "L2 one_step_execution",
    "L2 line_by_line_trace"
   ]
  }
 },
 "overall_level": "L0",
 "paths": [
  {
   "depth": 1,
   "source": "remainder_operator",
   "edge": "mis:remainder_operator->NegativeRemainderSign",
   "target": "NegativeRemainderSign",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2,
    3,
    4,
    5
   ],
   "quote": "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1",
   "confidence": 0.97,
   "prune_score": 0.9,
   "score": 0.873,
   "logic": "a % b is never negative, and integer division of a negative number rounds down.",
   "twin_logic": "a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2."
  },
  {
   "depth": 1,
   "source": "integer_division",
   "edge": "mis:integer_division->NegativeRemainderSign",
   "target": "NegativeRemainderSign",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2,
    3,
    4,
    5
   ],
   "quote": "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1",
   "confidence": 0.97,
   "prune_score": 0.75,
   "score": 0.7275,
   "logic": "a % b is never negative, and integer division of a negative number rounds down.",
   "twin_logic": "a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2."
  },
  {
   "depth": 1,
   "source": "arithmetic_operators",
   "edge": "mis:arithmetic_operators->RemainderIsSubtraction",
   "target": "RemainderIsSubtraction",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    5,
    6
   ],
   "quote": "so -7 % 2 is 1; because -4 * 2 + 1 = -7",
   "confidence": 0.75,
   "prune_score": 1.0,
   "score": 0.75,
   "logic": "9 % 5 means 9 minus 5 (a % b subtracts b from a).",
   "twin_logic": "% gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 * 5 + 4, and 17 % 5 is 2, not 12."
  },
  {
   "depth": 2,
   "source": "remainder_operator",
   "edge": "pre:integer_division->remainder_operator",
   "target": "integer_division",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    6
   ],
   "quote": "because -4 * 2 + 1 = -7",
   "confidence": 0.75,
   "prune_score": 1.0,
   "score": 0.75,
   "logic": "% is the companion of integer division: a = (a / b) * b + a % b.",
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
    2,
    5,
    6
   ],
   "quote": "-7 / 2 is -3.5, and integer division rounds down; so -7 % 2 is 1; because -4 * 2 + 1 = -7",
   "confidence": 0.7,
   "prune_score": 1.0,
   "score": 0.7,
   "logic": "An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "integer_division",
   "edge": "pre:arithmetic_operators->integer_division",
   "target": "arithmetic_operators",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    5,
    6
   ],
   "quote": "so it becomes -4; so -7 % 2 is 1; because -4 * 2 + 1 = -7",
   "confidence": 0.6,
   "prune_score": 1.0,
   "score": 0.6,
   "logic": "For ints a and b, / gives the whole quotient q and % gives the remainder r, so that a = b * q + r.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "println",
   "edge": "pre:statement->println",
   "target": "statement",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "It prints -4 and then 1",
   "confidence": 0.7,
   "prune_score": 1.0,
   "score": 0.7,
   "logic": "System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "lvl:expression@L3#1",
   "target": "expression@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3
   ],
   "quote": "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4",
   "confidence": 0.6,
   "prune_score": 0.45,
   "score": 0.27,
   "logic": "Operators combine operand values into a new value, and the operand types choose the operation (int / truncates, double / does not).",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "lvl:expression@L0#0",
   "target": "expression@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "-7 / 2 is -3.5, and integer division rounds down",
   "confidence": 0.65,
   "prune_score": 0.3,
   "score": 0.195,
   "logic": "In maths an expression such as 7/2 or x + y names an exact number, and 'expression' means a formula with operators. In Java, any code that evaluates to a typed value is an expression, including a lone literal or variable, and with ints 7/2 evaluates to 3.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 4,
   "source": "statement",
   "edge": "mis:statement->StatementsRunInAnyOrder",
   "target": "StatementsRunInAnyOrder",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1
   ],
   "quote": "It prints -4 and then 1",
   "confidence": 0.6,
   "prune_score": 0.6,
   "score": 0.36,
   "logic": "Statements in a program can run in any order.",
   "twin_logic": "Without control statements, statements run once each, top to bottom."
  },
  {
   "depth": 4,
   "source": "statement",
   "edge": "lvl:statement@L3#3",
   "target": "statement@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "It prints -4 and then 1",
   "confidence": 0.55,
   "prune_score": 0.4,
   "score": 0.22,
   "logic": "System.out.println(s); is a statement, so its line of output appears at its place in the sequence; swapping two println statements swaps the output lines.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 4,
   "source": "statement",
   "edge": "lvl:statement@L2#2",
   "target": "statement@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "It prints -4 and then 1",
   "confidence": 0.6,
   "prune_score": 0.3,
   "score": 0.18,
   "logic": "Executing one statement applies its single effect to the current state (e.g. prints one string, or stores one value) and then control moves to the next statement.",
   "twin_logic": null,
   "level": "L2",
   "way": "one_step_execution"
  }
 ],
 "evidence": [
  {
   "depth": 1,
   "source": "remainder_operator",
   "edge": "mis:remainder_operator->NegativeRemainderSign",
   "target": "NegativeRemainderSign",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2,
    3,
    4,
    5
   ],
   "quote": "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1",
   "confidence": 0.97,
   "prune_score": 0.9,
   "score": 0.873,
   "logic": "a % b is never negative, and integer division of a negative number rounds down.",
   "twin_logic": "a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2."
  },
  {
   "depth": 1,
   "source": "remainder_operator",
   "edge": "lvl:remainder_operator@L0#0",
   "target": "remainder_operator@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    4,
    5,
    6
   ],
   "quote": "A remainder is never negative; so -7 % 2 is 1; because -4 * 2 + 1 = -7",
   "confidence": 0.9,
   "prune_score": 0.4,
   "score": 0.36,
   "logic": "In everyday use % means percent (50% of x), and in maths 'mod' always gives a non-negative result. In Java % is the remainder of truncating division, and its sign follows the left operand (-14 % 3 is -2).",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 1,
   "source": "remainder_operator",
   "edge": "lvl:remainder_operator@L0#3",
   "target": "remainder_operator@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    4,
    5
   ],
   "quote": "A remainder is never negative; so -7 % 2 is 1",
   "confidence": 0.55,
   "prune_score": 0.35,
   "score": 0.1925,
   "logic": "Points to LT (compute the truncated quotient, then the remainder). Applied unevenly, a student gives the remainder for positive operands but the mathematical mod for negatives, or swaps quotient and remainder (17 % 5 as 3). (here mixing in: \"17 % 5 is 3 (the quotient)\")",
   "twin_logic": null,
   "level": "L0",
   "way": "inconsistent_trace"
  },
  {
   "depth": 1,
   "source": "remainder_operator",
   "edge": "lvl:remainder_operator@L3#0",
   "target": "remainder_operator@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    6
   ],
   "quote": "because -4 * 2 + 1 = -7",
   "confidence": 0.6,
   "prune_score": 0.25,
   "score": 0.15,
   "logic": "% is the companion of integer division, since a == (a / b) * b + a % b. Both use the same quotient rounded toward 0.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 1,
   "source": "arithmetic_operators",
   "edge": "mis:arithmetic_operators->RemainderIsSubtraction",
   "target": "RemainderIsSubtraction",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    5,
    6
   ],
   "quote": "so -7 % 2 is 1; because -4 * 2 + 1 = -7",
   "confidence": 0.75,
   "prune_score": 1.0,
   "score": 0.75,
   "logic": "9 % 5 means 9 minus 5 (a % b subtracts b from a).",
   "twin_logic": "% gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 * 5 + 4, and 17 % 5 is 2, not 12."
  },
  {
   "depth": 1,
   "source": "arithmetic_operators",
   "edge": "lvl:arithmetic_operators@L3#1",
   "target": "arithmetic_operators@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    6
   ],
   "quote": "because -4 * 2 + 1 = -7",
   "confidence": 0.6,
   "prune_score": 0.5,
   "score": 0.3,
   "logic": "For ints, / gives the truncated quotient and % the remainder, so (a / b) * b + a % b == a.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 1,
   "source": "integer_division",
   "edge": "mis:integer_division->NegativeRemainderSign",
   "target": "NegativeRemainderSign",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2,
    3,
    4,
    5
   ],
   "quote": "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4; A remainder is never negative; so -7 % 2 is 1",
   "confidence": 0.97,
   "prune_score": 0.75,
   "score": 0.7275,
   "logic": "a % b is never negative, and integer division of a negative number rounds down.",
   "twin_logic": "a / b rounds toward 0 and a % b takes the sign of a: -14 / 3 is -4 and -14 % 3 is -2."
  },
  {
   "depth": 1,
   "source": "integer_division",
   "edge": "mis:integer_division->IntegerDivisionGivesFraction",
   "target": "IntegerDivisionGivesFraction",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    2,
    3
   ],
   "quote": "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4",
   "confidence": 0.75,
   "prune_score": 0.2,
   "score": 0.15,
   "logic": "10 / 3 evaluates to 3.333....",
   "twin_logic": "Dividing two ints gives an int: the fractional part is discarded."
  },
  {
   "depth": 1,
   "source": "integer_division",
   "edge": "lvl:integer_division@L3#0",
   "target": "integer_division@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    6
   ],
   "quote": "because -4 * 2 + 1 = -7",
   "confidence": 0.85,
   "prune_score": 0.3,
   "score": 0.255,
   "logic": "/ and % on ints are paired: q = a / b and r = a % b always satisfy a = b * q + r.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 2,
   "source": "remainder_operator",
   "edge": "pre:integer_division->remainder_operator",
   "target": "integer_division",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    6
   ],
   "quote": "because -4 * 2 + 1 = -7",
   "confidence": 0.75,
   "prune_score": 1.0,
   "score": 0.75,
   "logic": "% is the companion of integer division: a = (a / b) * b + a % b.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "integer_division",
   "edge": "pre:arithmetic_operators->integer_division",
   "target": "arithmetic_operators",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    5,
    6
   ],
   "quote": "so it becomes -4; so -7 % 2 is 1; because -4 * 2 + 1 = -7",
   "confidence": 0.6,
   "prune_score": 1.0,
   "score": 0.6,
   "logic": "For ints a and b, / gives the whole quotient q and % gives the remainder r, so that a = b * q + r.",
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
    2,
    5,
    6
   ],
   "quote": "-7 / 2 is -3.5, and integer division rounds down; so -7 % 2 is 1; because -4 * 2 + 1 = -7",
   "confidence": 0.7,
   "prune_score": 1.0,
   "score": 0.7,
   "logic": "An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "println",
   "edge": "lvl:println@L2#1",
   "target": "println@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "It prints -4 and then 1",
   "confidence": 0.6,
   "prune_score": 0.4,
   "score": 0.24,
   "logic": "Output is the value's characters followed by a line break: println(\"Hello, \"); println(\"World!\"); prints two lines.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 2,
   "source": "println",
   "edge": "lvl:println@L3#0",
   "target": "println@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "It prints -4 and then 1",
   "confidence": 0.7,
   "prune_score": 0.35,
   "score": 0.245,
   "logic": "System.out.println(s); is a statement, so its line of output appears at its own place in the sequence.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "lvl:expression@L3#1",
   "target": "expression@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3
   ],
   "quote": "-7 / 2 is -3.5, and integer division rounds down; so it becomes -4",
   "confidence": 0.6,
   "prune_score": 0.45,
   "score": 0.27,
   "logic": "Operators combine operand values into a new value, and the operand types choose the operation (int / truncates, double / does not).",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "lvl:expression@L0#0",
   "target": "expression@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "-7 / 2 is -3.5, and integer division rounds down",
   "confidence": 0.65,
   "prune_score": 0.3,
   "score": 0.195,
   "logic": "In maths an expression such as 7/2 or x + y names an exact number, and 'expression' means a formula with operators. In Java, any code that evaluates to a typed value is an expression, including a lone literal or variable, and with ints 7/2 evaluates to 3.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "lvl:expression@L2#1",
   "target": "expression@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2,
    3,
    5
   ],
   "quote": "It prints -4 and then 1; -7 / 2 is -3.5, and integer division rounds down; so it becomes -4; so -7 % 2 is 1",
   "confidence": 0.7,
   "prune_score": 0.25,
   "score": 0.175,
   "logic": "An expression produces one value of a type fixed by its operands: hour * 60 + minute with hour = 11 and minute = 59 is the int 719.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 3,
   "source": "println",
   "edge": "pre:statement->println",
   "target": "statement",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "It prints -4 and then 1",
   "confidence": 0.7,
   "prune_score": 1.0,
   "score": 0.7,
   "logic": "System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence.",
   "twin_logic": null
  },
  {
   "depth": 4,
   "source": "statement",
   "edge": "mis:statement->StatementsRunInAnyOrder",
   "target": "StatementsRunInAnyOrder",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1
   ],
   "quote": "It prints -4 and then 1",
   "confidence": 0.6,
   "prune_score": 0.6,
   "score": 0.36,
   "logic": "Statements in a program can run in any order.",
   "twin_logic": "Without control statements, statements run once each, top to bottom."
  },
  {
   "depth": 4,
   "source": "statement",
   "edge": "lvl:statement@L3#3",
   "target": "statement@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "It prints -4 and then 1",
   "confidence": 0.55,
   "prune_score": 0.4,
   "score": 0.22,
   "logic": "System.out.println(s); is a statement, so its line of output appears at its place in the sequence; swapping two println statements swaps the output lines.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 4,
   "source": "statement",
   "edge": "lvl:statement@L2#0",
   "target": "statement@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "It prints -4 and then 1",
   "confidence": 0.55,
   "prune_score": 0.3,
   "score": 0.165,
   "logic": "Statements run one at a time, from first to last; each completes (normally or abruptly) before the next starts.",
   "twin_logic": null,
   "level": "L2",
   "way": "line_by_line_trace"
  },
  {
   "depth": 4,
   "source": "statement",
   "edge": "lvl:statement@L2#2",
   "target": "statement@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "It prints -4 and then 1",
   "confidence": 0.6,
   "prune_score": 0.3,
   "score": 0.18,
   "logic": "Executing one statement applies its single effect to the current state (e.g. prints one string, or stores one value) and then control moves to the next statement.",
   "twin_logic": null,
   "level": "L2",
   "way": "one_step_execution"
  }
 ],
 "clause_coverage": {
  "It prints -4 and then 1": "lvl:println@L2#1",
  "-7 / 2 is -3.5, and integer division rounds down": "mis:remainder_operator->NegativeRemainderSign",
  "so it becomes -4": "mis:remainder_operator->NegativeRemainderSign",
  "A remainder is never negative": "mis:remainder_operator->NegativeRemainderSign",
  "so -7 % 2 is 1": "mis:remainder_operator->NegativeRemainderSign",
  "because -4 * 2 + 1 = -7": "lvl:remainder_operator@L0#0"
 },
 "unexplained_clauses": [],
 "stop_reason": "sufficient",
 "depth_reached": 4,
 "llm_calls": 0,
 "llm_cache_hits": 44,
 "llm_calls_by_step": {
  "prune": 16,
  "label": 28
 }
}
```
