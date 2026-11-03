# Think on the Graph: every output of the run MY07
## 0. Input
Program:
```java
int big = 2147483647;
big = big + 1;
System.out.println(big);
```
Question: What does this program print, and why?

Student's answer: It prints 2147483648. Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big, because it makes room for it automatically.
Settings: width 3, depth 3, prune llm, backend claude-cli, model claude-opus-5-5
## 1. Stage 1: the subgraph G from the code (no model)
Masked code (string and char literals and comments blanked; this is what the patterns see):
```
int big = 2147483647;
big = big + 1;
System.out.println(big);
```
Which code text tagged which concept (a generic concept fires on almost any Java line; it starts the walk only if the answer repeats its tag):
| concept | generic | channel | matched text | line |
|---|---|---|---|---|
| arithmetic_operators | False | pattern | 'g + 1' | 2 |
| expression | True | pattern | 'g + 1' | 2 |
| expression | True | pattern | '= 2147483647;' | 1 |
| println | False | pattern | 'System.out.println(' | 3 |
| statement | True | pattern | ';' | 1 |

G: 4 concept nodes (2 generic), 2 concept edges, 22 misconception / error edges, 21 misconception / error nodes, 20 level nodes, 25 level-misconception links, 2 connected piece(s).
Note: concept nodes form 2 pieces (the KG has no edge between them): arithmetic_operators,expression | println,statement

Concept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):
| edge | type | rule (logic) |
|---|---|---|
| pre:arithmetic_operators->expression | prerequisite | An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones. |
| pre:statement->println | prerequisite | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |

Misconception / error edges per concept (count), and level ways per concept (count):
| concept | misconception / error edges | level ways (L1-L4 + L0 non-misconception) |
|---|---|---|
| arithmetic_operators | 3 | 18 |
| expression | 8 | 19 |
| println | 6 | 17 |
| statement | 5 | 19 |

Figure 1: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY07_figure01.png

Figure 2: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY07_figure02.png

## 2. Clauses and start concepts (no model)
The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):
| clause | text |
|---|---|
| c1 | It prints 2147483648 |
| c2 | Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big |
| c3 | because it makes room for it automatically |

start: 2 tagged concepts, all used

start concepts (2): arithmetic_operators, println

Start concepts: arithmetic_operators, println

Figure 3: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY07_figure03.png

## 3. The walk, depth by depth
At each depth, for each current concept: the edges offered (a concept entering as a start concept offers its misconception / error edges and its level ways, as two families; otherwise it offers its concept edges), the prune prompt and the model's reply, then the label prompt(s) and the model's reply, parsed into label / clauses / confidence. Score = prune score x confidence.

### Depth 1: current concepts 'arithmetic_operators', 'println'

#### arithmetic_operators, misconceptions: 3 edges offered
Edges offered:
| edge |
|---|
| mis:arithmetic_operators->ArithmeticOnNumericStrings \| wrong rule: "10" - 1 or "6" * "2" works because the strings look like numbers. \| right rule: Arithmetic operators other than + are not defined for Strings; a String of digits must first be converted to a number, e.g. with Integer.parseInt. |
| mis:arithmetic_operators->CaretIsPower \| wrong rule: a^2 computes a squared. \| right rule: Java has no exponent operator; ^ is exclusive or, and a * a or Math.pow(a, 2) computes a squared. |
| mis:arithmetic_operators->RemainderIsSubtraction \| wrong rule: 9 % 5 means 9 minus 5 (a % b subtracts b from a). \| right rule: % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 * 5 + 4, and 17 % 5 is 2, not 12. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:arithmetic_operators->ArithmeticOnNumericStrings (0.34), mis:arithmetic_operators->RemainderIsSubtraction (0.33), mis:arithmetic_operators->CaretIsPower (0.33)
```
Kept by pruning: mis:arithmetic_operators->ArithmeticOnNumericStrings (0.34), mis:arithmetic_operators->RemainderIsSubtraction (0.33), mis:arithmetic_operators->CaretIsPower (0.33)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:arithmetic_operators->ArithmeticOnNumericStrings \| wrong rule: "10" - 1 or "6" * "2" works because the strings look like numbers. \| right rule: Arithmetic operators other than + are not defined for Strings; a String of digits must first be converted to a number, e.g. with Integer.parseInt. |
| mis:arithmetic_operators->RemainderIsSubtraction \| wrong rule: 9 % 5 means 9 minus 5 (a % b subtracts b from a). \| right rule: % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 * 5 + 4, and 17 % 5 is 2, not 12. |
| mis:arithmetic_operators->CaretIsPower \| wrong rule: a^2 computes a squared. \| right rule: Java has no exponent operator; ^ is exclusive or, and a * a or Math.pow(a, 2) computes a squared. |
Model's reply:
```
mis:arithmetic_operators->ArithmeticOnNumericStrings | not applied | clauses: none | confidence: 0.95
mis:arithmetic_operators->RemainderIsSubtraction | not applied | clauses: none | confidence: 0.97
mis:arithmetic_operators->CaretIsPower | not applied | clauses: none | confidence: 0.97
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:arithmetic_operators->ArithmeticOnNumericStrings | not applied |  |  | 0.0 |  |  |
| mis:arithmetic_operators->RemainderIsSubtraction | not applied |  |  | 0.0 |  |  |
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
{lvl:arithmetic_operators@L4#5 (Score: 0.6)}
{lvl:arithmetic_operators@L1#1 (Score: 0.25)}
{lvl:arithmetic_operators@L2#2 (Score: 0.15)}
```
Kept by pruning: lvl:arithmetic_operators@L4#5 (0.60), lvl:arithmetic_operators@L1#1 (0.25), lvl:arithmetic_operators@L2#2 (0.15)

Label prompt for level way lvl:arithmetic_operators@L4#5 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: int arithmetic wraps silently on overflow. Kind: silent logic error. Trigger class: Results outside the int range.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Label prompt for level way lvl:arithmetic_operators@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> Both operands must be numeric, and the result has the promoted type (int, long or double). * / % bind tighter than + -, all group left to right, and int / or % by zero throws ArithmeticException. Unary minus negates its operand (-x) and unary plus leaves it unchanged; they bind more tightly than * and /, so -a * b is (-a) * b.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:arithmetic_operators@L2#2 (the model saw only the concept, the way's name 'one step execution' and its text; no level):
> An arithmetic operator never changes its operands. Each variable is replaced by its value, and only an assignment (or ++ or op=) stores the result.

Model's reply:
```
Label: shown
Clauses: 2
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:arithmetic_operators@L4#5 | not applied |  |  | 0.0 |  |  |
| lvl:arithmetic_operators@L1#1 | not applied |  |  | 0.0 |  |  |
| lvl:arithmetic_operators@L2#2 | shown | 0.15 | 0.6 | 0.09 | c2 | Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big |

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
mis:println->PrintedTextIsExecuted (0.50), mis:println->PrintNewLineFirst (0.30), mis:println->PrintEqualsPrintln (0.20)
```
Kept by pruning: mis:println->PrintedTextIsExecuted (0.50), mis:println->PrintNewLineFirst (0.30), mis:println->PrintEqualsPrintln (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:println->PrintedTextIsExecuted \| wrong rule: System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code). \| right rule: Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x. |
| mis:println->PrintNewLineFirst \| wrong rule: println(s) prints a newline and then s. \| right rule: println(s) prints s and then the newline. |
| mis:println->PrintEqualsPrintln \| wrong rule: print and println do the same thing, so print(s1); print(s2); puts s1 and s2 on separate lines. \| right rule: println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line. |
Model's reply:
```
mis:println->PrintedTextIsExecuted | not applied | clauses: none | confidence: 0.95
mis:println->PrintNewLineFirst | not applied | clauses: none | confidence: 0.95
mis:println->PrintEqualsPrintln | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:println->PrintedTextIsExecuted | not applied |  |  | 0.0 |  |  |
| mis:println->PrintNewLineFirst | not applied |  |  | 0.0 |  |  |
| mis:println->PrintEqualsPrintln | not applied |  |  | 0.0 |  |  |

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
{lvl:println@L2#1 (Score: 0.45)}
{lvl:println@L3#3 (Score: 0.35)}
{lvl:println@L2#0 (Score: 0.2)}
```
Kept by pruning: lvl:println@L2#1 (0.45), lvl:println@L3#3 (0.35), lvl:println@L2#0 (0.20)

Label prompt for level way lvl:println@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> Output is the value's characters followed by a line break: println("Hello, "); println("World!"); prints two lines.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.6
```

Label prompt for level way lvl:println@L3#3 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> println prints numbers with all their digits and always ends the line; printf formats each value by its conversion code and ends the line only where the format has %n or \n.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:println@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Evaluate the argument, print its characters at the current position, then write the line separator so the cursor moves to the beginning of the next line.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:println@L2#1 | shown | 0.45 | 0.6 | 0.27 | c1 | It prints 2147483648 |
| lvl:println@L3#3 | not applied |  |  | 0.0 |  |  |
| lvl:println@L2#0 | shown | 0.2 | 0.6 | 0.12 | c1 | It prints 2147483648 |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

lvl:println@L2#1 [shown, tier 2, 0.27], lvl:println@L2#0 [shown, tier 2, 0.12], lvl:arithmetic_operators@L2#2 [shown, tier 2, 0.09]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | It prints 2147483648 | lvl:println@L2#1 |
| c2 | Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big | lvl:arithmetic_operators@L2#2 |
| c3 | because it makes room for it automatically | not covered yet |

**Graph check, not yet read (the walk may not stop while these remain):** pre:arithmetic_operators->expression, pre:statement->println

Figure 4 (the graph after depth 1): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY07_figure04.png

### Depth 2: current concepts 'arithmetic_operators', 'println'

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
Clauses: 2
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:arithmetic_operators->expression | confirmed | 1.0 | 0.6 | 0.6 | c2 | Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big |

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
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:statement->println | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:arithmetic_operators->expression [confirmed, tier 2, 0.60]

reached across pre:arithmetic_operators->expression, entered next: expression

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | It prints 2147483648 | lvl:println@L2#1 |
| c2 | Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big | lvl:arithmetic_operators@L2#2 |
| c3 | because it makes room for it automatically | not covered yet |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of expression

Figure 5 (the graph after depth 2): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY07_figure05.png

### Depth 3: current concepts 'expression', 'arithmetic_operators'

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
mis:expression->TargetTyping | not applied | clauses: none | confidence: 0.7
mis:expression->AssignmentIsEquation | correct | clauses: 2 | confidence: 0.6
mis:expression->VariablesHoldExpressions | correct | clauses: 2 | confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:expression->TargetTyping | not applied |  |  | 0.0 |  |  |
| mis:expression->AssignmentIsEquation | correct | 0.2 | 0.6 | 0.12 | c2 | Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big |
| mis:expression->VariablesHoldExpressions | correct | 0.2 | 0.6 | 0.12 | c2 | Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big |

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
{lvl:expression@L0#0 (Score: 0.5)}
{lvl:expression@L2#1 (Score: 0.3)}
{lvl:expression@L3#1 (Score: 0.2)}
```
Kept by pruning: lvl:expression@L0#0 (0.50), lvl:expression@L2#1 (0.30), lvl:expression@L3#1 (0.20)

Label prompt for level way lvl:expression@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> In maths an expression such as 7/2 or x + y names an exact number, and 'expression' means a formula with operators. In Java, any code that evaluates to a typed value is an expression, including a lone literal or variable, and with ints 7/2 evaluates to 3.

Model's reply:
```
Label: shown
Clauses: 1, 2, 3
Confidence: 0.85
```

Label prompt for level way lvl:expression@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> An expression produces one value of a type fixed by its operands: hour * 60 + minute with hour = 11 and minute = 59 is the int 719.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:expression@L3#1 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Operators combine operand values into a new value, and the operand types choose the operation (int / truncates, double / does not).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:expression@L0#0 | shown | 0.5 | 0.85 | 0.42 | c1, c2, c3 | It prints 2147483648; Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big; because it makes room for it automatically |
| lvl:expression@L2#1 | not applied |  |  | 0.0 |  |  |
| lvl:expression@L3#1 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

lvl:expression@L0#0 [shown, tier 2, 0.42], mis:expression->AssignmentIsEquation [correct, tier 2, 0.12], mis:expression->VariablesHoldExpressions [correct, tier 2, 0.12]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | It prints 2147483648 | lvl:println@L2#1 |
| c2 | Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big | lvl:arithmetic_operators@L2#2 |
| c3 | because it makes room for it automatically | lvl:expression@L0#0 |

Figure 6 (the graph after depth 3): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY07_figure06.png

## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on [], broken at [], prerequisites {'expression': ['arithmetic_operators'], 'println': ['statement']}
- arithmetic_operators: L2 via one_step_execution "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big"
- expression: L0 via everyday_reading "It prints 2147483648; Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big; because it makes room for it automatically"
- println: L2 via output_prediction "It prints 2147483648"

**Stop:** sufficient at depth 3; prompts {'prune': 8, 'label': 14}, fresh model calls 0, cache hits 22

### Held misconceptions
(none)

### Broken concept edges
(none)

### Root cause: none

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| arithmetic_operators | L2 | one_step_execution |  | level_way | Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big |  |  |  |
| expression | L0 | everyday_reading |  | level_way | It prints 2147483648; Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big; because it makes room for it automatically |  |  |  |
| println | L2 | output_prediction |  | level_way | It prints 2147483648 |  | L2 line_by_line_trace |  |

### Overall level: L0

Clause coverage (final):
| clause | covered by |
|---|---|
| It prints 2147483648 | lvl:println@L2#1 |
| Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big | lvl:arithmetic_operators@L2#2 |
| because it makes room for it automatically | lvl:expression@L0#0 |

Figure 7 (final picture): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY07_figure07.png

## 5. Every labelled edge (the evidence list, kept or not)
| depth | source | edge | kind | label | prune_score | confidence | score | clauses | quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | arithmetic_operators | lvl:arithmetic_operators@L2#2 | level | shown | 0.15 | 0.6 | 0.09 | [2] | Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big |
| 1 | println | lvl:println@L2#1 | level | shown | 0.45 | 0.6 | 0.27 | [1] | It prints 2147483648 |
| 1 | println | lvl:println@L2#0 | level | shown | 0.2 | 0.6 | 0.12 | [1] | It prints 2147483648 |
| 2 | arithmetic_operators | pre:arithmetic_operators->expression | prerequisite | confirmed | 1.0 | 0.6 | 0.6 | [2] | Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big |
| 3 | expression | mis:expression->AssignmentIsEquation | misconception | correct | 0.2 | 0.6 | 0.12 | [2] | Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big |
| 3 | expression | mis:expression->VariablesHoldExpressions | misconception | correct | 0.2 | 0.6 | 0.12 | [2] | Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big |
| 3 | expression | lvl:expression@L0#0 | level | shown | 0.5 | 0.85 | 0.425 | [1, 2, 3] | It prints 2147483648; Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big; because it makes room for it automatically |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | println | lvl:println@L2#1 | level | shown | 0.27 | [1] |
| 1 | println | lvl:println@L2#0 | level | shown | 0.12 | [1] |
| 1 | arithmetic_operators | lvl:arithmetic_operators@L2#2 | level | shown | 0.09 | [2] |
| 2 | arithmetic_operators | pre:arithmetic_operators->expression | prerequisite | confirmed | 0.6 | [2] |
| 3 | expression | lvl:expression@L0#0 | level | shown | 0.425 | [1, 2, 3] |
| 3 | expression | mis:expression->AssignmentIsEquation | misconception | correct | 0.12 | [2] |
| 3 | expression | mis:expression->VariablesHoldExpressions | misconception | correct | 0.12 | [2] |

## 7. Raw traversal log
```
clauses: It prints 2147483648 | Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big | because it makes room for it automatically
start: 2 tagged concepts, all used
start concepts (2): arithmetic_operators, println
--- depth 1: current concepts ['arithmetic_operators', 'println']
  arithmetic_operators (misconceptions): 3 candidates -> kept mis:arithmetic_operators->ArithmeticOnNumericStrings (0.34), mis:arithmetic_operators->RemainderIsSubtraction (0.33), mis:arithmetic_operators->CaretIsPower (0.33)
    mis:arithmetic_operators->ArithmeticOnNumericStrings -> not applied (0.00) ""
    mis:arithmetic_operators->RemainderIsSubtraction -> not applied (0.00) ""
    mis:arithmetic_operators->CaretIsPower -> not applied (0.00) ""
  arithmetic_operators (level ways): 18 candidates -> kept lvl:arithmetic_operators@L4#5 (0.60), lvl:arithmetic_operators@L1#1 (0.25), lvl:arithmetic_operators@L2#2 (0.15)
    lvl:arithmetic_operators@L4#5 -> not applied (0.00) ""
    lvl:arithmetic_operators@L1#1 -> not applied (0.00) ""
    lvl:arithmetic_operators@L2#2 -> shown (0.09) "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big"
  println (misconceptions): 6 candidates -> kept mis:println->PrintedTextIsExecuted (0.50), mis:println->PrintNewLineFirst (0.30), mis:println->PrintEqualsPrintln (0.20)
    mis:println->PrintedTextIsExecuted -> not applied (0.00) ""
    mis:println->PrintNewLineFirst -> not applied (0.00) ""
    mis:println->PrintEqualsPrintln -> not applied (0.00) ""
  println (level ways): 17 candidates -> kept lvl:println@L2#1 (0.45), lvl:println@L3#3 (0.35), lvl:println@L2#0 (0.20)
    lvl:println@L2#1 -> shown (0.27) "It prints 2147483648"
    lvl:println@L3#3 -> not applied (0.00) ""
    lvl:println@L2#0 -> shown (0.12) "It prints 2147483648"
  kept: lvl:println@L2#1 [shown, tier 2, 0.27], lvl:println@L2#0 [shown, tier 2, 0.12], lvl:arithmetic_operators@L2#2 [shown, tier 2, 0.09]
  clause coverage: c1 <- lvl:println@L2#1; c2 <- lvl:arithmetic_operators@L2#2; c3 uncovered
  not yet read: pre:arithmetic_operators->expression, pre:statement->println
--- depth 2: current concepts ['arithmetic_operators', 'println']
  arithmetic_operators (concept edges): 1 candidates -> kept pre:arithmetic_operators->expression (1.00)
    pre:arithmetic_operators->expression -> confirmed (0.60) "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big"
  println (concept edges): 1 candidates -> kept pre:statement->println (1.00)
    pre:statement->println -> not applied (0.00) ""
  kept: pre:arithmetic_operators->expression [confirmed, tier 2, 0.60]
  reached across pre:arithmetic_operators->expression, entered next: expression
  clause coverage: c1 <- lvl:println@L2#1; c2 <- lvl:arithmetic_operators@L2#2; c3 uncovered
  not yet read: own edges of expression
--- depth 3: current concepts ['expression', 'arithmetic_operators']
  expression (misconceptions): 8 candidates -> kept mis:expression->TargetTyping (0.60), mis:expression->AssignmentIsEquation (0.20), mis:expression->VariablesHoldExpressions (0.20)
    mis:expression->TargetTyping -> not applied (0.00) ""
    mis:expression->AssignmentIsEquation -> correct (0.12) "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big"
    mis:expression->VariablesHoldExpressions -> correct (0.12) "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big"
  expression (level ways): 19 candidates -> kept lvl:expression@L0#0 (0.50), lvl:expression@L2#1 (0.30), lvl:expression@L3#1 (0.20)
    lvl:expression@L0#0 -> shown (0.42) "It prints 2147483648; Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big; because it makes room for it automatically"
    lvl:expression@L2#1 -> not applied (0.00) ""
    lvl:expression@L3#1 -> not applied (0.00) ""
  kept: lvl:expression@L0#0 [shown, tier 2, 0.42], mis:expression->AssignmentIsEquation [correct, tier 2, 0.12], mis:expression->VariablesHoldExpressions [correct, tier 2, 0.12]
  clause coverage: c1 <- lvl:println@L2#1; c2 <- lvl:arithmetic_operators@L2#2; c3 <- lvl:expression@L0#0
  root-cause walk: held on [], broken at [], prerequisites {'expression': ['arithmetic_operators'], 'println': ['statement']}
  level arithmetic_operators: L2 via one_step_execution "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big"
  level expression: L0 via everyday_reading "It prints 2147483648; Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big; because it makes room for it automatically"
  level println: L2 via output_prediction "It prints 2147483648"
```

## 8. Full diagnosis JSON
```json
{
 "scenario": "MY07",
 "settings": {
  "width": 3,
  "depth": 3,
  "prune_tools": "llm",
  "model": "claude-opus-5-5",
  "backend": "claude-cli"
 },
 "clauses": [
  "It prints 2147483648",
  "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big",
  "because it makes room for it automatically"
 ],
 "start_concepts": [
  "arithmetic_operators",
  "println"
 ],
 "held_misconceptions": [],
 "error_evidence": [],
 "broken_edges": [],
 "root_cause": null,
 "levels": {
  "arithmetic_operators": {
   "level": "L2",
   "way": "one_step_execution",
   "quote": "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big",
   "edge": "lvl:arithmetic_operators@L2#2",
   "source": "level_way",
   "also_shown": []
  },
  "expression": {
   "level": "L0",
   "way": "everyday_reading",
   "quote": "It prints 2147483648; Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big; because it makes room for it automatically",
   "edge": "lvl:expression@L0#0",
   "source": "level_way"
  },
  "println": {
   "level": "L2",
   "way": "output_prediction",
   "quote": "It prints 2147483648",
   "edge": "lvl:println@L2#1",
   "source": "level_way",
   "also_shown": [
    "L2 line_by_line_trace"
   ]
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
   "quote": "It prints 2147483648",
   "confidence": 0.6,
   "prune_score": 0.45,
   "score": 0.27,
   "logic": "Output is the value's characters followed by a line break: println(\"Hello, \"); println(\"World!\"); prints two lines.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "println",
   "edge": "lvl:println@L2#0",
   "target": "println@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "It prints 2147483648",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "Evaluate the argument, print its characters at the current position, then write the line separator so the cursor moves to the beginning of the next line.",
   "twin_logic": null,
   "level": "L2",
   "way": "line_by_line_trace"
  },
  {
   "depth": 1,
   "source": "arithmetic_operators",
   "edge": "lvl:arithmetic_operators@L2#2",
   "target": "arithmetic_operators@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big",
   "confidence": 0.6,
   "prune_score": 0.15,
   "score": 0.09,
   "logic": "An arithmetic operator never changes its operands. Each variable is replaced by its value, and only an assignment (or ++ or op=) stores the result.",
   "twin_logic": null,
   "level": "L2",
   "way": "one_step_execution"
  },
  {
   "depth": 2,
   "source": "arithmetic_operators",
   "edge": "pre:arithmetic_operators->expression",
   "target": "expression",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    2
   ],
   "quote": "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big",
   "confidence": 0.6,
   "prune_score": 1.0,
   "score": 0.6,
   "logic": "An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "lvl:expression@L0#0",
   "target": "expression@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "It prints 2147483648; Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big; because it makes room for it automatically",
   "confidence": 0.85,
   "prune_score": 0.5,
   "score": 0.425,
   "logic": "In maths an expression such as 7/2 or x + y names an exact number, and 'expression' means a formula with operators. In Java, any code that evaluates to a typed value is an expression, including a lone literal or variable, and with ints 7/2 evaluates to 3.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "mis:expression->AssignmentIsEquation",
   "target": "AssignmentIsEquation",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    2
   ],
   "quote": "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities.",
   "twin_logic": "An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable."
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "mis:expression->VariablesHoldExpressions",
   "target": "VariablesHoldExpressions",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    2
   ],
   "quote": "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "= stores the expression itself, not its computed value",
   "twin_logic": "y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y."
  }
 ],
 "evidence": [
  {
   "depth": 1,
   "source": "arithmetic_operators",
   "edge": "lvl:arithmetic_operators@L2#2",
   "target": "arithmetic_operators@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2
   ],
   "quote": "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big",
   "confidence": 0.6,
   "prune_score": 0.15,
   "score": 0.09,
   "logic": "An arithmetic operator never changes its operands. Each variable is replaced by its value, and only an assignment (or ++ or op=) stores the result.",
   "twin_logic": null,
   "level": "L2",
   "way": "one_step_execution"
  },
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
   "quote": "It prints 2147483648",
   "confidence": 0.6,
   "prune_score": 0.45,
   "score": 0.27,
   "logic": "Output is the value's characters followed by a line break: println(\"Hello, \"); println(\"World!\"); prints two lines.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "println",
   "edge": "lvl:println@L2#0",
   "target": "println@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "It prints 2147483648",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "Evaluate the argument, print its characters at the current position, then write the line separator so the cursor moves to the beginning of the next line.",
   "twin_logic": null,
   "level": "L2",
   "way": "line_by_line_trace"
  },
  {
   "depth": 2,
   "source": "arithmetic_operators",
   "edge": "pre:arithmetic_operators->expression",
   "target": "expression",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    2
   ],
   "quote": "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big",
   "confidence": 0.6,
   "prune_score": 1.0,
   "score": 0.6,
   "logic": "An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "mis:expression->AssignmentIsEquation",
   "target": "AssignmentIsEquation",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    2
   ],
   "quote": "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "An assignment states a lasting equality between its two sides, so y = x - y can be solved like the equation x = 2y and x = x + 5 relates two equal quantities.",
   "twin_logic": "An assignment is a one-time action: evaluate the right side with current values, then store the result in the left variable."
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "mis:expression->VariablesHoldExpressions",
   "target": "VariablesHoldExpressions",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    2
   ],
   "quote": "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "= stores the expression itself, not its computed value",
   "twin_logic": "y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y."
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "lvl:expression@L0#0",
   "target": "expression@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2,
    3
   ],
   "quote": "It prints 2147483648; Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big; because it makes room for it automatically",
   "confidence": 0.85,
   "prune_score": 0.5,
   "score": 0.425,
   "logic": "In maths an expression such as 7/2 or x + y names an exact number, and 'expression' means a formula with operators. In Java, any code that evaluates to a typed value is an expression, including a lone literal or variable, and with ints 7/2 evaluates to 3.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  }
 ],
 "clause_coverage": {
  "It prints 2147483648": "lvl:println@L2#1",
  "Adding 1 to 2147483647 gives 2147483648, and Java just stores the bigger number in big": "lvl:arithmetic_operators@L2#2",
  "because it makes room for it automatically": "lvl:expression@L0#0"
 },
 "unexplained_clauses": [],
 "stop_reason": "sufficient",
 "depth_reached": 3,
 "llm_calls": 0,
 "llm_cache_hits": 22,
 "llm_calls_by_step": {
  "prune": 8,
  "label": 14
 }
}
```
