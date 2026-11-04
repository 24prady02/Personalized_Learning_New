# Think on the Graph: every output of the run MY05
## 0. Input
Program:
```java
char c = 'A';
int n = c + 1;
System.out.println(n);
```
Question: What does this program print, and why?

Student's answer: It does not compile. c is a letter, not a number, so you cannot add 1 to it. Java will give an error that a char and an int cannot be added.
Settings: width 3, depth 3, prune llm, backend claude-cli, model claude-opus-5-5
## 1. Stage 1: the subgraph G from the code (no model)
Masked code (string and char literals and comments blanked; this is what the patterns see):
```
char c = ' ';
int n = c + 1;
System.out.println(n);
```
Which code text tagged which concept (a generic concept fires on almost any Java line; it starts the walk only if the answer repeats its tag):
| concept | generic | channel | matched text | line |
|---|---|---|---|---|
| arithmetic_operators | False | pattern | 'c + 1' | 2 |
| char | True | pattern | 'char' | 1 |
| char | True | pattern | "'A'" | 1 |
| char | True | type | 'char' | 1 |
| char_arithmetic | False | signal | "char c = 'A';\nint n = c + 1" | 1 |
| expression | True | pattern | 'c + 1' | 2 |
| expression | True | pattern | "= ' ';" | 1 |
| println | False | pattern | 'System.out.println(' | 3 |
| statement | True | pattern | ';' | 1 |

G: 6 concept nodes (3 generic), 3 concept edges, 24 misconception / error edges, 22 misconception / error nodes, 30 level nodes, 31 level-misconception links, 3 connected piece(s).
Note: concept nodes form 3 pieces (the KG has no edge between them): arithmetic_operators,expression | char,char_arithmetic | println,statement

Concept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):
| edge | type | rule (logic) |
|---|---|---|
| pre:arithmetic_operators->expression | prerequisite | An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones. |
| pre:char->char_arithmetic | prerequisite | Char arithmetic uses the numeric code stored for each char. |
| pre:statement->println | prerequisite | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |

Misconception / error edges per concept (count), and level ways per concept (count):
| concept | misconception / error edges | level ways (L1-L4 + L0 non-misconception) |
|---|---|---|
| arithmetic_operators | 3 | 18 |
| char | 1 | 19 |
| char_arithmetic | 1 | 14 |
| expression | 8 | 19 |
| println | 6 | 17 |
| statement | 5 | 19 |

Figure 1: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY05_figure01.png

Figure 2: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY05_figure02.png

## 2. Clauses and start concepts (no model)
The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):
| clause | text |
|---|---|
| c1 | It does not compile |
| c2 | c is a letter, not a number |
| c3 | so you cannot add 1 to it |
| c4 | Java will give an error that a char and an int cannot be added |

start: generic concepts whose tagging text occurs in the answer: char

start: BM25 of the answer against each tagged concept: println 9.77 (hits 1), arithmetic_operators 9.56 (hits 1), char 8.92 (hits 3), char_arithmetic 5.26 (hits 1)

start: chosen println, arithmetic_operators, char

start concepts (3): println, arithmetic_operators, char

Start concepts: println, arithmetic_operators, char

Figure 3: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY05_figure03.png

## 3. The walk, depth by depth
At each depth, for each current concept: the edges offered (a concept entering as a start concept offers its misconception / error edges and its level ways, as two families; otherwise it offers its concept edges), the prune prompt and the model's reply, then the label prompt(s) and the model's reply, parsed into label / clauses / confidence. Score = prune score x confidence.

### Depth 1: current concepts 'println', 'arithmetic_operators', 'char'

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
mis:println->PrintedTextIsExecuted (0.40), mis:println->ParenthesesOnlyIfArgument (0.30), mis:println->IdentifierCaseInsensitive (0.30)
```
Kept by pruning: mis:println->PrintedTextIsExecuted (0.40), mis:println->ParenthesesOnlyIfArgument (0.30), mis:println->IdentifierCaseInsensitive (0.30)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:println->PrintedTextIsExecuted \| wrong rule: System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code). \| right rule: Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x. |
| mis:println->ParenthesesOnlyIfArgument \| wrong rule: println with nothing to print can be written System.out.println; without the parentheses. \| right rule: A method call always needs parentheses, so an empty line is printed with System.out.println();. |
| mis:println->IdentifierCaseInsensitive \| wrong rule: System.out.Println and System.out.println name the same method. \| right rule: Java is case-sensitive: names of variables, methods and classes that differ only in capitalization are different names. |
Model's reply:
```
mis:println->PrintedTextIsExecuted | not applied | clauses: none | confidence: 0.95
mis:println->ParenthesesOnlyIfArgument | not applied | clauses: none | confidence: 0.97
mis:println->IdentifierCaseInsensitive | not applied | clauses: none | confidence: 0.97
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:println->PrintedTextIsExecuted | not applied |  |  | 0.0 |  |  |
| mis:println->ParenthesesOnlyIfArgument | not applied |  |  | 0.0 |  |  |
| mis:println->IdentifierCaseInsensitive | not applied |  |  | 0.0 |  |  |

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
{lvl:println@L2#0 (Score: 0.3)}
{lvl:println@L2#2 (Score: 0.2)}
```
Kept by pruning: lvl:println@L2#1 (0.50), lvl:println@L2#0 (0.30), lvl:println@L2#2 (0.20)

Label prompt for level way lvl:println@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> Output is the value's characters followed by a line break: println("Hello, "); println("World!"); prints two lines.

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
Label: not shown
Clauses: none
Confidence: 0.95
```

Label prompt for level way lvl:println@L2#2 (the model saw only the concept, the way's name 'one step execution' and its text; no level):
> One call appends the text and a line separator to the output; the cursor ends at the start of the next line; no variable changes and nothing is returned.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:println@L2#1 | not applied |  |  | 0.0 |  |  |
| lvl:println@L2#0 | not applied |  |  | 0.0 |  |  |
| lvl:println@L2#2 | not applied |  |  | 0.0 |  |  |

#### arithmetic_operators, misconceptions: 3 edges offered
Edges offered:
| edge |
|---|
| mis:arithmetic_operators->ArithmeticOnNumericStrings \| wrong rule: "10" - 1 or "6" * "2" works because the strings look like numbers. \| right rule: Arithmetic operators other than + are not defined for Strings; a String of digits must first be converted to a number, e.g. with Integer.parseInt. |
| mis:arithmetic_operators->CaretIsPower \| wrong rule: a^2 computes a squared. \| right rule: Java has no exponent operator; ^ is exclusive or, and a * a or Math.pow(a, 2) computes a squared. |
| mis:arithmetic_operators->RemainderIsSubtraction \| wrong rule: 9 % 5 means 9 minus 5 (a % b subtracts b from a). \| right rule: % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 * 5 + 4, and 17 % 5 is 2, not 12. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:arithmetic_operators->ArithmeticOnNumericStrings (0.80), mis:arithmetic_operators->CaretIsPower (0.10), mis:arithmetic_operators->RemainderIsSubtraction (0.10)
```
Kept by pruning: mis:arithmetic_operators->ArithmeticOnNumericStrings (0.80), mis:arithmetic_operators->CaretIsPower (0.10), mis:arithmetic_operators->RemainderIsSubtraction (0.10)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:arithmetic_operators->ArithmeticOnNumericStrings \| wrong rule: "10" - 1 or "6" * "2" works because the strings look like numbers. \| right rule: Arithmetic operators other than + are not defined for Strings; a String of digits must first be converted to a number, e.g. with Integer.parseInt. |
| mis:arithmetic_operators->CaretIsPower \| wrong rule: a^2 computes a squared. \| right rule: Java has no exponent operator; ^ is exclusive or, and a * a or Math.pow(a, 2) computes a squared. |
| mis:arithmetic_operators->RemainderIsSubtraction \| wrong rule: 9 % 5 means 9 minus 5 (a % b subtracts b from a). \| right rule: % gives the remainder after integer division: 9 % 5 is 4 because 9 = 1 * 5 + 4, and 17 % 5 is 2, not 12. |
Model's reply:
```
mis:arithmetic_operators->ArithmeticOnNumericStrings | not applied | clauses: none | confidence: 0.85
mis:arithmetic_operators->CaretIsPower | not applied | clauses: none | confidence: 0.97
mis:arithmetic_operators->RemainderIsSubtraction | not applied | clauses: none | confidence: 0.97
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:arithmetic_operators->ArithmeticOnNumericStrings | not applied |  |  | 0.0 |  |  |
| mis:arithmetic_operators->CaretIsPower | not applied |  |  | 0.0 |  |  |
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
{lvl:arithmetic_operators@L1#1 (Score: 0.45)}
{lvl:arithmetic_operators@L4#3 (Score: 0.35)}
{lvl:arithmetic_operators@L2#1 (Score: 0.2)}
```
Kept by pruning: lvl:arithmetic_operators@L1#1 (0.45), lvl:arithmetic_operators@L4#3 (0.35), lvl:arithmetic_operators@L2#1 (0.20)

Label prompt for level way lvl:arithmetic_operators@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> Both operands must be numeric, and the result has the promoted type (int, long or double). * / % bind tighter than + -, all group left to right, and int / or % by zero throws ArithmeticException. Unary minus negates its operand (-x) and unary plus leaves it unchanged; they bind more tightly than * and /, so -a * b is (-a) * b.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:arithmetic_operators@L4#3 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: Arithmetic operators other than + are not defined for Strings. Kind: compile-time. Trigger class: "10" - 1 or "6" * "2": 'bad operand types for binary operator'.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:arithmetic_operators@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> With ints, 17 / 3 is 5 and 17 % 3 is 2. With doubles, 5.0 / 3.0 is 1.6666666666666667. With mixed operands, the int is promoted first (10 / 3.0 is 3.333...).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:arithmetic_operators@L1#1 | not applied |  |  | 0.0 |  |  |
| lvl:arithmetic_operators@L4#3 | not applied |  |  | 0.0 |  |  |
| lvl:arithmetic_operators@L2#1 | not applied |  |  | 0.0 |  |  |

#### char, misconceptions: 1 edges offered
Edges offered:
| edge |
|---|
| mis:char->CharNotNumeric \| wrong rule: A char is only a letter, so c + k is an error. \| right rule: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:char->CharNotNumeric (Score: 1.0)}
```
Kept by pruning: mis:char->CharNotNumeric (1.00)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:char->CharNotNumeric \| wrong rule: A char is only a letter, so c + k is an error. \| right rule: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes. |
Model's reply:
```
mis:char->CharNotNumeric | held | clauses: 1, 2, 3, 4 | confidence: 0.97
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:char->CharNotNumeric | held | 1.0 | 0.97 | 0.97 | c1, c2, c3, c4 | It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |

#### char, level ways: 19 edges offered
Edges offered:
| edge |
|---|
| lvl:char@L0#0 \| level L0 way everyday_reading: In everyday life '7' and 7 are the same thing, and a character is a letter, not a number. A Java char is a 16-bit numeric code: '7' has code 55, and 'a' + 1 is the int 98. |
| lvl:char@L0#2 \| level L0 way inconsistent_trace: Points to LT (a char in arithmetic becomes its int code). Applied unevenly, a student treats 'b' + 'c' as 197 in one exercise but prints it as "bc" in another. (here mixing in: "char is not a numeric type") |
| lvl:char@L1#0 \| level L1 way names_the_element: char: the primitive type for a single 16-bit Unicode character, such as 'a', '%' or '\n'. |
| lvl:char@L1#1 \| level L1 way states_the_rule: A char literal is exactly one character (or one escape sequence) in single quotes. Values range from '\u0000' to '\uffff' (0 to 65535), and char is an integral type. A char literal is one character in single quotes ('a'); a String literal is any sequence in double quotes ("a"), so 'a' and "a" have different types and 'ab' does not compile. |
| lvl:char@L2#0 \| level L2 way line_by_line_trace: When a char meets an arithmetic operator, it is first promoted to int (its code) and the operation runs in int. Storing the result back in a char needs an explicit cast. |
| lvl:char@L2#1 \| level L2 way output_prediction: System.out.println('b') prints b. 'b' + 'c' is the int 197. (char) ('a' + 4) is 'e'. |
| lvl:char@L2#2 \| level L2 way one_step_execution: c++ on char c = 'A' makes c 'B', because increment works on chars directly. c = c + 1; does not compile, because the right side is an int. |
| lvl:char@L3#0 \| level L3 way relation_to_neighbour: A char is stored as an unsigned 16-bit code, so in arithmetic it acts as an int ('a' + 1 is 98). Going from int to char needs a cast. |
| lvl:char@L3#1 \| level L3 way relation_to_neighbour: A char widens automatically to double (its code), but a double needs a cast to become a char. A char never holds a fractional part. |
| lvl:char@L3#2 \| level L3 way relation_to_neighbour: char and boolean are unrelated: there is no conversion or cast between them, and 'c' is never true or false. |
| lvl:char@L3#3 \| level L3 way relation_to_neighbour: Char arithmetic works on each char's numeric code and yields an int. A cast turns the result back into a character. |
| lvl:char@L3#4 \| level L3 way relation_to_neighbour: char is one of the eight primitive types: the unsigned 16-bit integral one, used for single characters. |
| lvl:char@L3#5 \| level L3 way relation_to_neighbour: 'a' is a char (one 16-bit character code, a primitive); "a" is a String (a sequence of characters, an object). 'a' + 'b' is the int 195, while "a" + "b" is "ab". |
| lvl:char@L3#6 \| level L3 way purpose_of_the_whole: A char holds one character: processing text one character at a time (charAt), looping over 'A'..'Z', or shifting letters in a cipher. |
| lvl:char@L4#0 \| level L4 way predict_a_change: Changing 'A' to "A" changes the type to String, so + concatenates instead of adding. Changing a char variable to int keeps the arithmetic, but println then prints numbers instead of letters. |
| lvl:char@L4#1 \| level L4 way transfer_to_a_new_program: Use char for one character from a literal or from charAt, especially when the character's code matters (alphabet loops, ciphers). Use String for text of any length. |
| lvl:char@L4#2 \| level L4 way diagnose_an_error: rule broken: A char literal holds exactly one character. Kind: compile-time. Trigger class: Several characters in single quotes ('ab') or a word in single quotes: 'unclosed character literal'. |
| lvl:char@L4#3 \| level L4 way diagnose_an_error: rule broken: int arithmetic on chars yields an int, which cannot go into a char without a cast. Kind: compile-time. Trigger class: char c = 'a' + i; or c = c + 1; with variable i: 'possible lossy conversion from int to char'. |
| lvl:char@L4#4 \| level L4 way diagnose_an_error: rule broken: A char compares by its code, not by the digit or letter it shows. Kind: silent logic error. Trigger class: Comparing a char with an int as if it were a digit (seat <= 3 for seat = 'A'), or printing c + 1 expecting a letter. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:char@L0#0 (Score: 0.6)}
{lvl:char@L3#0 (Score: 0.2)}
{lvl:char@L2#0 (Score: 0.2)}
```
Kept by pruning: lvl:char@L0#0 (0.60), lvl:char@L3#0 (0.20), lvl:char@L2#0 (0.20)

Label prompt for level way lvl:char@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> In everyday life '7' and 7 are the same thing, and a character is a letter, not a number. A Java char is a 16-bit numeric code: '7' has code 55, and 'a' + 1 is the int 98.

Model's reply:
```
Label: shown
Clauses: 2, 3, 4
Confidence: 0.9
```

Label prompt for level way lvl:char@L3#0 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> A char is stored as an unsigned 16-bit code, so in arithmetic it acts as an int ('a' + 1 is 98). Going from int to char needs a cast.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Label prompt for level way lvl:char@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> When a char meets an arithmetic operator, it is first promoted to int (its code) and the operation runs in int. Storing the result back in a char needs an explicit cast.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:char@L0#0 | shown | 0.6 | 0.9 | 0.54 | c2, c3, c4 | c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |
| lvl:char@L3#0 | not applied |  |  | 0.0 |  |  |
| lvl:char@L2#0 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:char->CharNotNumeric [held, tier 0, 0.97], lvl:char@L0#0 [shown, tier 2, 0.54]

**Graph check, not yet read (the walk may not stop while these remain):** pre:arithmetic_operators->expression, pre:char->char_arithmetic, pre:statement->println

Figure 4 (the graph after depth 1): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY05_figure04.png

### Depth 2: current concepts 'char', 'println', 'arithmetic_operators'

#### char, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:char->char_arithmetic \| rule: Char arithmetic uses the numeric code stored for each char. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:char->char_arithmetic (Score: 1.0)}
```
Kept by pruning: pre:char->char_arithmetic (1.00)

Label prompt for concept edge pre:char->char_arithmetic (char -> char_arithmetic, prerequisite):
> Char arithmetic uses the numeric code stored for each char.

Model's reply:
```
Label: broken
Clauses: 2, 3, 4
Confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:char->char_arithmetic | broken | 1.0 | 0.95 | 0.95 | c2, c3, c4 | c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |

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
Label: broken
Clauses: 3, 4
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:arithmetic_operators->expression | broken | 1.0 | 0.7 | 0.7 | c3, c4 | so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:char->char_arithmetic [broken, tier 0, 0.95], pre:arithmetic_operators->expression [broken, tier 0, 0.70]

reached across pre:char->char_arithmetic, entered next: char_arithmetic

reached across pre:arithmetic_operators->expression, entered next: expression

**Graph check, not yet read (the walk may not stop while these remain):** own edges of char_arithmetic, own edges of expression

Figure 5 (the graph after depth 2): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY05_figure05.png

### Depth 3: current concepts 'char_arithmetic', 'char', 'expression', 'arithmetic_operators'

#### char_arithmetic, misconceptions: 1 edges offered
Edges offered:
| edge |
|---|
| mis:char_arithmetic->CharNotNumeric \| wrong rule: char is not a numeric type \| right rule: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:char_arithmetic->CharNotNumeric (Score: 1.0)}
```
Kept by pruning: mis:char_arithmetic->CharNotNumeric (1.00)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:char_arithmetic->CharNotNumeric \| wrong rule: char is not a numeric type \| right rule: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes. |
Model's reply:
```
mis:char_arithmetic->CharNotNumeric | held | clauses: 1, 2, 3, 4 | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:char_arithmetic->CharNotNumeric | held | 1.0 | 0.95 | 0.95 | c1, c2, c3, c4 | It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |

#### char_arithmetic, level ways: 14 edges offered
Edges offered:
| edge |
|---|
| lvl:char_arithmetic@L0#0 \| level L0 way everyday_reading: In everyday use letters are not numbers, so 'a' + 1 seems meaningless or should give "a1". Java promotes each char to its int code, so 'a' + 1 is 98. |
| lvl:char_arithmetic@L0#2 \| level L0 way inconsistent_trace: Points to LT (chars become int codes before the operator is applied). Applied unevenly, a student converts to codes in one step but keeps letters in another, e.g. printing 'b' + 'c' as "bc". (here mixing in: "char is not a numeric type") |
| lvl:char_arithmetic@L1#0 \| level L1 way names_the_element: Char arithmetic: applying arithmetic or comparison operators to char values, which act on their Unicode codes. |
| lvl:char_arithmetic@L1#1 \| level L1 way states_the_rule: char operands of arithmetic are promoted to int, so the result is an int. Casting an int to char gives the character with that code. ++, -- and comparisons work directly on chars. |
| lvl:char_arithmetic@L2#0 \| level L2 way line_by_line_trace: Each char operand is replaced by its code (promoted to int) and the operation runs in int. A cast written outside the parentheses, as in (char) ('a' + 4), is applied last. |
| lvl:char_arithmetic@L2#1 \| level L2 way output_prediction: 'b' + 'c' is the int 197. 'a' + 4 is 101. (char) ('a' + 4) is 'e'. 'A' < 'a' is true. |
| lvl:char_arithmetic@L2#2 \| level L2 way one_step_execution: For char c = 'A', c++ sets c to 'B'. c = c + 1; is rejected, because the right side is an int. |
| lvl:char_arithmetic@L3#0 \| level L3 way relation_to_neighbour: Char arithmetic uses each char's numeric code, so the result is an int, not a char, unless it is cast back. |
| lvl:char_arithmetic@L3#1 \| level L3 way purpose_of_the_whole: Plans: shifting letters (Caesar cipher), turning a digit char into its value (c - '0'), looping over 'A'..'Z', and testing whether a char is in a range. |
| lvl:char_arithmetic@L4#0 \| level L4 way predict_a_change: Adding or removing the (char) cast changes the output from a number to a letter. Changing 'a' + 4 to "a" + 4 makes it concatenation ("a4"). |
| lvl:char_arithmetic@L4#1 \| level L4 way transfer_to_a_new_program: Use char arithmetic when the computation depends on character order or codes (alphabet loops, ciphers, digit values). To join characters into text, use String + or a String instead. |
| lvl:char_arithmetic@L4#2 \| level L4 way diagnose_an_error: rule broken: Arithmetic on chars yields an int, which needs a cast to go back into a char. Kind: compile-time. Trigger class: char next = c + 1; or char d = 'a' + k;: 'possible lossy conversion from int to char'. |
| lvl:char_arithmetic@L4#3 \| level L4 way diagnose_an_error: rule broken: Without a cast the int code is printed, not the letter. Kind: silent logic error. Trigger class: Printing c + 1 or 'a' + i when a letter was expected. |
| lvl:char_arithmetic@L4#4 \| level L4 way diagnose_an_error: rule broken: A char compares by its code, not by the digit it shows. Kind: silent logic error. Trigger class: Comparing a char with an int as if it were a digit (seat <= 3 for seat = 'A'). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:char_arithmetic@L0#0 (Score: 0.6)}
{lvl:char_arithmetic@L0#2 (Score: 0.25)}
{lvl:char_arithmetic@L4#2 (Score: 0.15)}
```
Kept by pruning: lvl:char_arithmetic@L0#0 (0.60), lvl:char_arithmetic@L0#2 (0.25), lvl:char_arithmetic@L4#2 (0.15)

Label prompt for level way lvl:char_arithmetic@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> In everyday use letters are not numbers, so 'a' + 1 seems meaningless or should give "a1". Java promotes each char to its int code, so 'a' + 1 is 98.

Model's reply:
```
Label: shown
Clauses: 2, 3, 4
Confidence: 0.9
```

Label prompt for level way lvl:char_arithmetic@L0#2 (the model saw only the concept, the way's name 'inconsistent trace' and its text; no level):
> Points to LT (chars become int codes before the operator is applied). Applied unevenly, a student converts to codes in one step but keeps letters in another, e.g. printing 'b' + 'c' as "bc". (here mixing in: "char is not a numeric type")

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Label prompt for level way lvl:char_arithmetic@L4#2 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: Arithmetic on chars yields an int, which needs a cast to go back into a char. Kind: compile-time. Trigger class: char next = c + 1; or char d = 'a' + k;: 'possible lossy conversion from int to char'.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:char_arithmetic@L0#0 | shown | 0.6 | 0.9 | 0.54 | c2, c3, c4 | c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |
| lvl:char_arithmetic@L0#2 | not applied |  |  | 0.0 |  |  |
| lvl:char_arithmetic@L4#2 | not applied |  |  | 0.0 |  |  |

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
mis:expression->TargetTyping (0.50), mis:expression->NoAtomicExpression (0.35), mis:expression->VariablesHoldExpressions (0.15)
```
Kept by pruning: mis:expression->TargetTyping (0.50), mis:expression->NoAtomicExpression (0.35), mis:expression->VariablesHoldExpressions (0.15)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:expression->TargetTyping \| wrong rule: The type of a numerical expression depends on the type expected by the surrounding context, so double d = a / b; keeps the fraction. \| right rule: The type of a numerical expression is determined by the expression, so double d = a / b; with int a and b still divides as ints. |
| mis:expression->NoAtomicExpression \| wrong rule: A single variable x or a literal on its own is not an expression. \| right rule: A single variable or literal is an expression whose value is just that value. |
| mis:expression->VariablesHoldExpressions \| wrong rule: = stores the expression itself, not its computed value \| right rule: y = x + k; stores the value that x + k has at that moment, so later changes to x do not change y. |
Model's reply:
```
mis:expression->TargetTyping | not applied | clauses: none | confidence: 0.85
mis:expression->NoAtomicExpression | not applied | clauses: none | confidence: 0.85
mis:expression->VariablesHoldExpressions | not applied | clauses: none | confidence: 0.9
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
{lvl:expression@L4#4 (Score: 0.5)}
{lvl:expression@L3#1 (Score: 0.3)}
{lvl:expression@L0#0 (Score: 0.2)}
```
Kept by pruning: lvl:expression@L4#4 (0.50), lvl:expression@L3#1 (0.30), lvl:expression@L0#0 (0.20)

Label prompt for level way lvl:expression@L4#4 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: Operators accept only operands of suitable types. Kind: compile-time. Trigger class: Applying arithmetic to Strings ("Hello" - 1) or comparing booleans with <: 'bad operand types'.

Model's reply:
```
Label: shown
Clauses: 1, 2, 3, 4
Confidence: 0.8
```

Label prompt for level way lvl:expression@L3#1 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Operators combine operand values into a new value, and the operand types choose the operation (int / truncates, double / does not).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Label prompt for level way lvl:expression@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> In maths an expression such as 7/2 or x + y names an exact number, and 'expression' means a formula with operators. In Java, any code that evaluates to a typed value is an expression, including a lone literal or variable, and with ints 7/2 evaluates to 3.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:expression@L4#4 | shown | 0.5 | 0.8 | 0.4 | c1, c2, c3, c4 | It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |
| lvl:expression@L3#1 | not applied |  |  | 0.0 |  |  |
| lvl:expression@L0#0 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:char_arithmetic->CharNotNumeric [held, tier 0, 0.95], lvl:char_arithmetic@L0#0 [shown, tier 2, 0.54], lvl:expression@L4#4 [shown, tier 2, 0.40]

Figure 6 (the graph after depth 3): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY05_figure06.png

Held set after the one-fault rules: mis:char_arithmetic->CharNotNumeric; filed at the dependent concept: mis:char->CharNotNumeric

## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on ['char_arithmetic'], broken at [] (consequences: pre:char->char_arithmetic, pre:arithmetic_operators->expression), prerequisites {'expression': ['arithmetic_operators'], 'char_arithmetic': ['char'], 'println': ['statement']}
- char: L0 via everyday_reading "c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added"
- char_arithmetic: L0 via misconception "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added"
- expression: L4 via diagnose_an_error "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added"

**Stop:** sufficient at depth 3; prompts {'prune': 13, 'label': 23}, fresh model calls 0, cache hits 36

### Held misconceptions
| concept | misconception | kind | quote | score | shares_evidence_with |
|---|---|---|---|---|---|
| char_arithmetic | CharNotNumeric | misconception | It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added | 0.95 |  |

### Broken concept edges
| edge | quote | score | consequence_of |
|---|---|---|---|
| pre:char->char_arithmetic | c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added | 0.95 | mis:char->CharNotNumeric |
| pre:arithmetic_operators->expression | so you cannot add 1 to it; Java will give an error that a char and an int cannot be added | 0.7 | mis:char->CharNotNumeric |

### Root cause: char_arithmetic / CharNotNumeric

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| char | L0 | everyday_reading |  | level_way | c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |  |  |  |
| char_arithmetic | L0 | misconception | CharNotNumeric | level_mis_links | It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added | wrong rule: char is not a numeric type. Right rule: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes. |  |  |
| expression | L4 | diagnose_an_error |  | level_way | It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |  |  |  |

### Overall level: L0

Clause coverage (final):
| clause | covered by |
|---|---|
| It does not compile | mis:char->CharNotNumeric |
| c is a letter, not a number | mis:char->CharNotNumeric |
| so you cannot add 1 to it | mis:char->CharNotNumeric |
| Java will give an error that a char and an int cannot be added | mis:char->CharNotNumeric |

Figure 7 (final picture): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY05_figure07.png

## 5. Every labelled edge (the evidence list, kept or not)
| depth | source | edge | kind | label | prune_score | confidence | score | clauses | quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | char | mis:char->CharNotNumeric | misconception | held | 1.0 | 0.97 | 0.97 | [1, 2, 3, 4] | It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |
| 1 | char | lvl:char@L0#0 | level | shown | 0.6 | 0.9 | 0.54 | [2, 3, 4] | c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |
| 2 | char | pre:char->char_arithmetic | prerequisite | broken | 1.0 | 0.95 | 0.95 | [2, 3, 4] | c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |
| 2 | arithmetic_operators | pre:arithmetic_operators->expression | prerequisite | broken | 1.0 | 0.7 | 0.7 | [3, 4] | so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |
| 3 | char_arithmetic | mis:char_arithmetic->CharNotNumeric | misconception | held | 1.0 | 0.95 | 0.95 | [1, 2, 3, 4] | It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |
| 3 | char_arithmetic | lvl:char_arithmetic@L0#0 | level | shown | 0.6 | 0.9 | 0.54 | [2, 3, 4] | c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |
| 3 | expression | lvl:expression@L4#4 | level | shown | 0.5 | 0.8 | 0.4 | [1, 2, 3, 4] | It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | char | mis:char->CharNotNumeric | misconception | held | 0.97 | [1, 2, 3, 4] |
| 1 | char | lvl:char@L0#0 | level | shown | 0.54 | [2, 3, 4] |
| 2 | char | pre:char->char_arithmetic | prerequisite | broken | 0.95 | [2, 3, 4] |
| 2 | arithmetic_operators | pre:arithmetic_operators->expression | prerequisite | broken | 0.7 | [3, 4] |
| 3 | char_arithmetic | mis:char_arithmetic->CharNotNumeric | misconception | held | 0.95 | [1, 2, 3, 4] |
| 3 | char_arithmetic | lvl:char_arithmetic@L0#0 | level | shown | 0.54 | [2, 3, 4] |
| 3 | expression | lvl:expression@L4#4 | level | shown | 0.4 | [1, 2, 3, 4] |

## 7. Raw traversal log
```
clauses: It does not compile | c is a letter, not a number | so you cannot add 1 to it | Java will give an error that a char and an int cannot be added
start: generic concepts whose tagging text occurs in the answer: char
start: BM25 of the answer against each tagged concept: println 9.77 (hits 1), arithmetic_operators 9.56 (hits 1), char 8.92 (hits 3), char_arithmetic 5.26 (hits 1)
start: chosen println, arithmetic_operators, char
start concepts (3): println, arithmetic_operators, char
--- depth 1: current concepts ['println', 'arithmetic_operators', 'char']
  println (misconceptions): 6 candidates -> kept mis:println->PrintedTextIsExecuted (0.40), mis:println->ParenthesesOnlyIfArgument (0.30), mis:println->IdentifierCaseInsensitive (0.30)
    mis:println->PrintedTextIsExecuted -> not applied (0.00) ""
    mis:println->ParenthesesOnlyIfArgument -> not applied (0.00) ""
    mis:println->IdentifierCaseInsensitive -> not applied (0.00) ""
  println (level ways): 17 candidates -> kept lvl:println@L2#1 (0.50), lvl:println@L2#0 (0.30), lvl:println@L2#2 (0.20)
    lvl:println@L2#1 -> not applied (0.00) ""
    lvl:println@L2#0 -> not applied (0.00) ""
    lvl:println@L2#2 -> not applied (0.00) ""
  arithmetic_operators (misconceptions): 3 candidates -> kept mis:arithmetic_operators->ArithmeticOnNumericStrings (0.80), mis:arithmetic_operators->CaretIsPower (0.10), mis:arithmetic_operators->RemainderIsSubtraction (0.10)
    mis:arithmetic_operators->ArithmeticOnNumericStrings -> not applied (0.00) ""
    mis:arithmetic_operators->CaretIsPower -> not applied (0.00) ""
    mis:arithmetic_operators->RemainderIsSubtraction -> not applied (0.00) ""
  arithmetic_operators (level ways): 18 candidates -> kept lvl:arithmetic_operators@L1#1 (0.45), lvl:arithmetic_operators@L4#3 (0.35), lvl:arithmetic_operators@L2#1 (0.20)
    lvl:arithmetic_operators@L1#1 -> not applied (0.00) ""
    lvl:arithmetic_operators@L4#3 -> not applied (0.00) ""
    lvl:arithmetic_operators@L2#1 -> not applied (0.00) ""
  char (misconceptions): 1 candidates -> kept mis:char->CharNotNumeric (1.00)
    mis:char->CharNotNumeric -> held (0.97) "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added"
  char (level ways): 19 candidates -> kept lvl:char@L0#0 (0.60), lvl:char@L3#0 (0.20), lvl:char@L2#0 (0.20)
    lvl:char@L0#0 -> shown (0.54) "c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added"
    lvl:char@L3#0 -> not applied (0.00) ""
    lvl:char@L2#0 -> not applied (0.00) ""
  kept: mis:char->CharNotNumeric [held, tier 0, 0.97], lvl:char@L0#0 [shown, tier 2, 0.54]
  clause coverage (rule edges): c1 <- mis:char->CharNotNumeric; c2 <- mis:char->CharNotNumeric; c3 <- mis:char->CharNotNumeric; c4 <- mis:char->CharNotNumeric
  not yet read: pre:arithmetic_operators->expression, pre:char->char_arithmetic, pre:statement->println
--- depth 2: current concepts ['char', 'println', 'arithmetic_operators']
  char (concept edges): 1 candidates -> kept pre:char->char_arithmetic (1.00)
    pre:char->char_arithmetic -> broken (0.95) "c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added"
  println (concept edges): 1 candidates -> kept pre:statement->println (1.00)
    pre:statement->println -> not applied (0.00) ""
  arithmetic_operators (concept edges): 1 candidates -> kept pre:arithmetic_operators->expression (1.00)
    pre:arithmetic_operators->expression -> broken (0.70) "so you cannot add 1 to it; Java will give an error that a char and an int cannot be added"
  kept: pre:char->char_arithmetic [broken, tier 0, 0.95], pre:arithmetic_operators->expression [broken, tier 0, 0.70]
  reached across pre:char->char_arithmetic, entered next: char_arithmetic
  reached across pre:arithmetic_operators->expression, entered next: expression
  clause coverage (rule edges): c1 <- mis:char->CharNotNumeric; c2 <- mis:char->CharNotNumeric; c3 <- mis:char->CharNotNumeric; c4 <- mis:char->CharNotNumeric
  not yet read: own edges of char_arithmetic, own edges of expression
--- depth 3: current concepts ['char_arithmetic', 'char', 'expression', 'arithmetic_operators']
  char_arithmetic (misconceptions): 1 candidates -> kept mis:char_arithmetic->CharNotNumeric (1.00)
    mis:char_arithmetic->CharNotNumeric -> held (0.95) "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added"
  char_arithmetic (level ways): 14 candidates -> kept lvl:char_arithmetic@L0#0 (0.60), lvl:char_arithmetic@L0#2 (0.25), lvl:char_arithmetic@L4#2 (0.15)
    lvl:char_arithmetic@L0#0 -> shown (0.54) "c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added"
    lvl:char_arithmetic@L0#2 -> not applied (0.00) ""
    lvl:char_arithmetic@L4#2 -> not applied (0.00) ""
  expression (misconceptions): 8 candidates -> kept mis:expression->TargetTyping (0.50), mis:expression->NoAtomicExpression (0.35), mis:expression->VariablesHoldExpressions (0.15)
    mis:expression->TargetTyping -> not applied (0.00) ""
    mis:expression->NoAtomicExpression -> not applied (0.00) ""
    mis:expression->VariablesHoldExpressions -> not applied (0.00) ""
  expression (level ways): 19 candidates -> kept lvl:expression@L4#4 (0.50), lvl:expression@L3#1 (0.30), lvl:expression@L0#0 (0.20)
    lvl:expression@L4#4 -> shown (0.40) "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added"
    lvl:expression@L3#1 -> not applied (0.00) ""
    lvl:expression@L0#0 -> not applied (0.00) ""
  kept: mis:char_arithmetic->CharNotNumeric [held, tier 0, 0.95], lvl:char_arithmetic@L0#0 [shown, tier 2, 0.54], lvl:expression@L4#4 [shown, tier 2, 0.40]
  clause coverage (rule edges): c1 <- mis:char->CharNotNumeric; c2 <- mis:char->CharNotNumeric; c3 <- mis:char->CharNotNumeric; c4 <- mis:char->CharNotNumeric
  held: mis:char_arithmetic->CharNotNumeric; filed at the dependent concept: mis:char->CharNotNumeric
  shadows: mis:char->CharNotNumeric (shadow of mis:char_arithmetic->CharNotNumeric)
  root-cause walk: held on ['char_arithmetic'], broken at [] (consequences: pre:char->char_arithmetic, pre:arithmetic_operators->expression), prerequisites {'expression': ['arithmetic_operators'], 'char_arithmetic': ['char'], 'println': ['statement']}
  level char: L0 via everyday_reading "c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added"
  level char_arithmetic: L0 via misconception "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added"
  level expression: L4 via diagnose_an_error "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added"
```

## 8. Full diagnosis JSON
```json
{
 "scenario": "MY05",
 "settings": {
  "width": 3,
  "depth": 3,
  "prune_tools": "llm",
  "model": "claude-opus-5-5",
  "backend": "claude-cli"
 },
 "clauses": [
  "It does not compile",
  "c is a letter, not a number",
  "so you cannot add 1 to it",
  "Java will give an error that a char and an int cannot be added"
 ],
 "start_concepts": [
  "println",
  "arithmetic_operators",
  "char"
 ],
 "held_misconceptions": [
  {
   "concept": "char_arithmetic",
   "misconception": "CharNotNumeric",
   "kind": "misconception",
   "quote": "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "score": 0.95
  }
 ],
 "error_evidence": [],
 "shadowed": [
  {
   "concept": "char",
   "misconception": "CharNotNumeric",
   "shadow_of": "mis:char_arithmetic->CharNotNumeric",
   "quote": "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "score": 0.97
  }
 ],
 "broken_edges": [
  {
   "edge": "pre:char->char_arithmetic",
   "quote": "c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "score": 0.95,
   "consequence_of": "mis:char->CharNotNumeric"
  },
  {
   "edge": "pre:arithmetic_operators->expression",
   "quote": "so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "score": 0.7,
   "consequence_of": "mis:char->CharNotNumeric"
  }
 ],
 "root_cause": {
  "concept": "char_arithmetic",
  "misconception": "CharNotNumeric"
 },
 "levels": {
  "char": {
   "level": "L0",
   "way": "everyday_reading",
   "quote": "c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "edge": "lvl:char@L0#0",
   "source": "level_way",
   "also_shown": []
  },
  "char_arithmetic": {
   "level": "L0",
   "way": "misconception",
   "misconception": "CharNotNumeric",
   "quote": "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "edge": "mis:char_arithmetic->CharNotNumeric",
   "rule": "wrong rule: char is not a numeric type. Right rule: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.",
   "source": "level_mis_links"
  },
  "expression": {
   "level": "L4",
   "way": "diagnose_an_error",
   "quote": "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "edge": "lvl:expression@L4#4",
   "source": "level_way",
   "also_shown": []
  }
 },
 "overall_level": "L0",
 "paths": [
  {
   "depth": 1,
   "source": "char",
   "edge": "mis:char->CharNotNumeric",
   "target": "CharNotNumeric",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3,
    4
   ],
   "quote": "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "confidence": 0.97,
   "prune_score": 1.0,
   "score": 0.97,
   "logic": "A char is only a letter, so c + k is an error.",
   "twin_logic": "A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes."
  },
  {
   "depth": 1,
   "source": "char",
   "edge": "lvl:char@L0#0",
   "target": "char@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "confidence": 0.9,
   "prune_score": 0.6,
   "score": 0.54,
   "logic": "In everyday life '7' and 7 are the same thing, and a character is a letter, not a number. A Java char is a 16-bit numeric code: '7' has code 55, and 'a' + 1 is the int 98.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 2,
   "source": "char",
   "edge": "pre:char->char_arithmetic",
   "target": "char_arithmetic",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "confidence": 0.95,
   "prune_score": 1.0,
   "score": 0.95,
   "logic": "Char arithmetic uses the numeric code stored for each char.",
   "twin_logic": null,
   "consequence_of": "mis:char->CharNotNumeric"
  },
  {
   "depth": 2,
   "source": "arithmetic_operators",
   "edge": "pre:arithmetic_operators->expression",
   "target": "expression",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    3,
    4
   ],
   "quote": "so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "confidence": 0.7,
   "prune_score": 1.0,
   "score": 0.7,
   "logic": "An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones.",
   "twin_logic": null,
   "consequence_of": "mis:char->CharNotNumeric"
  },
  {
   "depth": 3,
   "source": "char_arithmetic",
   "edge": "mis:char_arithmetic->CharNotNumeric",
   "target": "CharNotNumeric",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3,
    4
   ],
   "quote": "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "confidence": 0.95,
   "prune_score": 1.0,
   "score": 0.95,
   "logic": "char is not a numeric type",
   "twin_logic": "A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes."
  },
  {
   "depth": 3,
   "source": "char_arithmetic",
   "edge": "lvl:char_arithmetic@L0#0",
   "target": "char_arithmetic@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "confidence": 0.9,
   "prune_score": 0.6,
   "score": 0.54,
   "logic": "In everyday use letters are not numbers, so 'a' + 1 seems meaningless or should give \"a1\". Java promotes each char to its int code, so 'a' + 1 is 98.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "lvl:expression@L4#4",
   "target": "expression@L4",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2,
    3,
    4
   ],
   "quote": "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "confidence": 0.8,
   "prune_score": 0.5,
   "score": 0.4,
   "logic": "rule broken: Operators accept only operands of suitable types. Kind: compile-time. Trigger class: Applying arithmetic to Strings (\"Hello\" - 1) or comparing booleans with <: 'bad operand types'.",
   "twin_logic": null,
   "level": "L4",
   "way": "diagnose_an_error"
  }
 ],
 "evidence": [
  {
   "depth": 1,
   "source": "char",
   "edge": "mis:char->CharNotNumeric",
   "target": "CharNotNumeric",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3,
    4
   ],
   "quote": "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "confidence": 0.97,
   "prune_score": 1.0,
   "score": 0.97,
   "logic": "A char is only a letter, so c + k is an error.",
   "twin_logic": "A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes."
  },
  {
   "depth": 1,
   "source": "char",
   "edge": "lvl:char@L0#0",
   "target": "char@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "confidence": 0.9,
   "prune_score": 0.6,
   "score": 0.54,
   "logic": "In everyday life '7' and 7 are the same thing, and a character is a letter, not a number. A Java char is a 16-bit numeric code: '7' has code 55, and 'a' + 1 is the int 98.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 2,
   "source": "char",
   "edge": "pre:char->char_arithmetic",
   "target": "char_arithmetic",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "confidence": 0.95,
   "prune_score": 1.0,
   "score": 0.95,
   "logic": "Char arithmetic uses the numeric code stored for each char.",
   "twin_logic": null,
   "consequence_of": "mis:char->CharNotNumeric"
  },
  {
   "depth": 2,
   "source": "arithmetic_operators",
   "edge": "pre:arithmetic_operators->expression",
   "target": "expression",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    3,
    4
   ],
   "quote": "so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "confidence": 0.7,
   "prune_score": 1.0,
   "score": 0.7,
   "logic": "An operator combines operand values a and b into a new value, so operators build larger expressions from smaller ones.",
   "twin_logic": null,
   "consequence_of": "mis:char->CharNotNumeric"
  },
  {
   "depth": 3,
   "source": "char_arithmetic",
   "edge": "mis:char_arithmetic->CharNotNumeric",
   "target": "CharNotNumeric",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3,
    4
   ],
   "quote": "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "confidence": 0.95,
   "prune_score": 1.0,
   "score": 0.95,
   "logic": "char is not a numeric type",
   "twin_logic": "A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes."
  },
  {
   "depth": 3,
   "source": "char_arithmetic",
   "edge": "lvl:char_arithmetic@L0#0",
   "target": "char_arithmetic@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "confidence": 0.9,
   "prune_score": 0.6,
   "score": 0.54,
   "logic": "In everyday use letters are not numbers, so 'a' + 1 seems meaningless or should give \"a1\". Java promotes each char to its int code, so 'a' + 1 is 98.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 3,
   "source": "expression",
   "edge": "lvl:expression@L4#4",
   "target": "expression@L4",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2,
    3,
    4
   ],
   "quote": "It does not compile; c is a letter, not a number; so you cannot add 1 to it; Java will give an error that a char and an int cannot be added",
   "confidence": 0.8,
   "prune_score": 0.5,
   "score": 0.4,
   "logic": "rule broken: Operators accept only operands of suitable types. Kind: compile-time. Trigger class: Applying arithmetic to Strings (\"Hello\" - 1) or comparing booleans with <: 'bad operand types'.",
   "twin_logic": null,
   "level": "L4",
   "way": "diagnose_an_error"
  }
 ],
 "clause_coverage": {
  "It does not compile": "mis:char->CharNotNumeric",
  "c is a letter, not a number": "mis:char->CharNotNumeric",
  "so you cannot add 1 to it": "mis:char->CharNotNumeric",
  "Java will give an error that a char and an int cannot be added": "mis:char->CharNotNumeric"
 },
 "unexplained_clauses": [],
 "stop_reason": "sufficient",
 "depth_reached": 3,
 "llm_calls": 0,
 "llm_cache_hits": 36,
 "llm_calls_by_step": {
  "prune": 13,
  "label": 23
 }
}
```
