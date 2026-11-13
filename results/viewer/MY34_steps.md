# Think on the Graph: every output of the run MY34
## 0. Input
Program:
```java
int x = 5;
if (x > 0)
    if (x > 10)
        System.out.println("big");
else
    System.out.println("small");
```
Question: What is printed? Explain which if the else belongs to.

Student's answer: Nothing. The else lines up with if (x > 0), and that’s true, so the else is skipped. x > 10 is false, so big isn’t printed either
Settings: width 3, depth 3, prune llm, backend claude-cli, model claude-opus-5-5
## 1. Stage 1: the subgraph G from the code (no model)
Masked code (string and char literals and comments blanked; this is what the patterns see):
```
int x = 5;
if (x > 0)
    if (x > 10)
        System.out.println("   ");
else
    System.out.println("     ");
```
Which code text tagged which concept (a generic concept fires on almost any Java line; it starts the walk only if the answer repeats its tag):
| concept | generic | channel | matched text | line |
|---|---|---|---|---|
| assignment | True | pattern | '=' | 1 |
| boolean_expression | False | pattern | 'if (' | 2 |
| comparison_operators | False | pattern | 'if (x >' | 2 |
| control_flow | False | pattern | 'if (' | 2 |
| dangling_else | False | signal | 'if (x > 0)\n    if (x > 10)\n        System.out.println("   ");\nelse' | 2 |
| expression | True | pattern | 'x >' | 2 |
| expression | True | pattern | '= 5;' | 1 |
| fencepost_loop | False | pattern | 'if (x > 0)\n    if (x > 10)\n        System.out.print' | 2 |
| if_else_statement | False | pattern | 'else' | 5 |
| if_statement | False | pattern | 'if (' | 2 |
| nested_conditionals | False | signal | 'if (x > 0)\n    if (' | 2 |
| println | False | pattern | 'System.out.println(' | 4 |
| statement | True | pattern | ';' | 1 |
| string_literal | True | pattern | '"big"' | 4 |

G: 13 concept nodes (4 generic), 12 concept edges, 101 misconception / error edges, 76 misconception / error nodes, 65 level nodes, 101 level-misconception links, 2 connected piece(s).
Note: concept nodes form 2 pieces (the KG has no edge between them): assignment,boolean_expression,comparison_operators,control_flow,dangling_else,expression,if_else_statement,if_statement,nested_conditionals,println,statement,string_literal | fencepost_loop

Concept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):
| edge | type | rule (logic) |
|---|---|---|
| par:assignment~comparison_operators | parallel | x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands. |
| pre:boolean_expression->if_statement | prerequisite | An if runs its block only when its boolean expression evaluates to true. |
| pre:comparison_operators->boolean_expression | prerequisite | A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making. |
| pre:control_flow->if_statement | prerequisite | An if changes the default top-to-bottom flow by running a block only when its condition is true. |
| pre:expression->comparison_operators | prerequisite | Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b. |
| pre:if_else_statement->nested_conditionals | prerequisite | Nesting puts an if or if-else inside a branch of another if-else; an else-if chain is the common case where the else branch is itself an if. |
| pre:if_statement->if_else_statement | prerequisite | if-else extends if with a second block that runs exactly when the condition is false. |
| pre:if_statement->nested_conditionals | prerequisite | An if statement can sit inside the body of another if; the inner one is tested only when the outer condition is true. |
| pre:nested_conditionals->dangling_else | prerequisite | The dangling else arises when ifs are nested without braces. |
| pre:statement->control_flow | prerequisite | Control flow is the order in which statements run. |
| pre:statement->println | prerequisite | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |
| pre:string_literal->println | prerequisite | println("s") outputs exactly the characters between the quotes and then ends the line. |

Misconception / error edges per concept (count), and level ways per concept (count):
| concept | misconception / error edges | level ways (L1-L4 + L0 non-misconception) |
|---|---|---|
| assignment | 15 | 24 |
| boolean_expression | 8 | 19 |
| comparison_operators | 8 | 20 |
| control_flow | 11 | 15 |
| dangling_else | 1 | 12 |
| expression | 8 | 19 |
| fencepost_loop | 1 | 13 |
| if_else_statement | 6 | 17 |
| if_statement | 22 | 19 |
| nested_conditionals | 6 | 14 |
| println | 6 | 17 |
| statement | 5 | 19 |
| string_literal | 4 | 16 |

Figure 1: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY34_figure01.png

Figure 2: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY34_figure02.png

## 2. Clauses and start concepts (no model)
The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):
| clause | text |
|---|---|
| c1 | Nothing |
| c2 | The else lines up with if |
| c3 | x > 0 |
| c4 | and thats true |
| c5 | so the else is skipped |
| c6 | x > 10 is false |
| c7 | so big isnt printed either |

start: generic concepts whose tagging text occurs in the answer: expression

start: BM25 of the answer against each tagged concept: comparison_operators 15.12 (hits 1), println 14.44 (hits 1), if_statement 13.10 (hits 1), boolean_expression 12.75 (hits 1), control_flow 11.94 (hits 1), nested_conditionals 11.56 (hits 1), if_else_statement 11.37 (hits 1), expression 8.80 (hits 2), dangling_else 6.81 (hits 1), fencepost_loop 1.89 (hits 1)

start: chosen comparison_operators, println, if_statement

start concepts (3): comparison_operators, println, if_statement

Start concepts: comparison_operators, println, if_statement

Figure 3: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY34_figure03.png

## 3. The walk, depth by depth
At each depth, for each current concept: the edges offered (a concept entering as a start concept offers its misconception / error edges and its level ways, as two families; otherwise it offers its concept edges), the prune prompt and the model's reply, then the label prompt(s) and the model's reply, parsed into label / clauses / confidence. Score = prune score x confidence.

### Depth 1: current concepts 'comparison_operators', 'println', 'if_statement'

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
mis:comparison_operators->LessGreaterSwapped (0.80), mis:comparison_operators->ChainedComparison (0.10), mis:comparison_operators->ComparisonWithBooleanLiteral (0.10)
```
Kept by pruning: mis:comparison_operators->LessGreaterSwapped (0.80), mis:comparison_operators->ChainedComparison (0.10), mis:comparison_operators->ComparisonWithBooleanLiteral (0.10)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:comparison_operators->LessGreaterSwapped \| wrong rule: < and > mean the same thing (or a < b means a is greater than b). \| right rule: a < b is true when a is smaller than b; a > b when a is larger. |
| mis:comparison_operators->ChainedComparison \| wrong rule: 90 <= grade <= 100 tests whether grade is between 90 and 100. \| right rule: a < b < c does not compile (a < b is a boolean); a range test is written 90 <= grade && grade <= 100. |
| mis:comparison_operators->ComparisonWithBooleanLiteral \| wrong rule: you must write == true / == false to test a boolean \| right rule: if (b) already tests b, so writing == true adds nothing. |
Model's reply:
```
mis:comparison_operators->LessGreaterSwapped | correct | clauses: 3, 4, 6 | confidence: 0.85
mis:comparison_operators->ChainedComparison | not applied | clauses: none | confidence: 0.95
mis:comparison_operators->ComparisonWithBooleanLiteral | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:comparison_operators->LessGreaterSwapped | correct | 0.8 | 0.85 | 0.68 | c3, c4, c6 | x > 0; and thats true; x > 10 is false |
| mis:comparison_operators->ChainedComparison | not applied |  |  | 0.0 |  |  |
| mis:comparison_operators->ComparisonWithBooleanLiteral | not applied |  |  | 0.0 |  |  |

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
{lvl:comparison_operators@L2#1 (Score: 0.4)}
{lvl:comparison_operators@L3#1 (Score: 0.35)}
{lvl:comparison_operators@L2#0 (Score: 0.25)}
```
Kept by pruning: lvl:comparison_operators@L2#1 (0.40), lvl:comparison_operators@L3#1 (0.35), lvl:comparison_operators@L2#0 (0.25)

Label prompt for level way lvl:comparison_operators@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> The result is a boolean: (2 <= 2) is true, 2 < 2 is false, (x < 3.1) is true for int x = 3; any comparison involving NaN, even NaN == NaN, is false.

Model's reply:
```
Label: shown
Clauses: 3, 4, 6
Confidence: 0.8
```

Label prompt for level way lvl:comparison_operators@L3#1 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Comparisons are the building blocks of conditions: together with boolean logic they provide the basis for decision-making.

Model's reply:
```
Label: shown
Clauses: 3, 4, 5, 6, 7
Confidence: 0.7
```

Label prompt for level way lvl:comparison_operators@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Evaluate the left operand (including its arithmetic), then the right operand; if their types differ, promote the narrower one (int to double); then compare and produce true or false.

Model's reply:
```
Label: shown
Clauses: 3, 4, 6
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:comparison_operators@L2#1 | shown | 0.4 | 0.8 | 0.32 | c3, c4, c6 | x > 0; and thats true; x > 10 is false |
| lvl:comparison_operators@L3#1 | shown | 0.35 | 0.7 | 0.24 | c3, c4, c5, c6, c7 | x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |
| lvl:comparison_operators@L2#0 | shown | 0.25 | 0.7 | 0.17 | c3, c4, c6 | x > 0; and thats true; x > 10 is false |

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
mis:println->PrintedTextIsExecuted (0.60), mis:println->PrintEqualsPrintln (0.20), mis:println->PrintNewLineFirst (0.20)
```
Kept by pruning: mis:println->PrintedTextIsExecuted (0.60), mis:println->PrintEqualsPrintln (0.20), mis:println->PrintNewLineFirst (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:println->PrintedTextIsExecuted \| wrong rule: System.out.println("x is 5"); sets x to 5 (text inside the quotes is run as code). \| right rule: Characters inside double quotes are printed literally; println only displays them and changes no variable. Only an assignment such as x = 5; sets x. |
| mis:println->PrintEqualsPrintln \| wrong rule: print and println do the same thing, so print(s1); print(s2); puts s1 and s2 on separate lines. \| right rule: println ends the line after printing and print does not, so print(s1); print(s2); puts s1 and s2 on the same line. |
| mis:println->PrintNewLineFirst \| wrong rule: println(s) prints a newline and then s. \| right rule: println(s) prints s and then the newline. |
Model's reply:
```
mis:println->PrintedTextIsExecuted | not applied | clauses: none | confidence: 0.9
mis:println->PrintEqualsPrintln | not applied | clauses: none | confidence: 0.95
mis:println->PrintNewLineFirst | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:println->PrintedTextIsExecuted | not applied |  |  | 0.0 |  |  |
| mis:println->PrintEqualsPrintln | not applied |  |  | 0.0 |  |  |
| mis:println->PrintNewLineFirst | not applied |  |  | 0.0 |  |  |

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
{lvl:println@L3#0 (Score: 0.45)}
{lvl:println@L2#1 (Score: 0.35)}
{lvl:println@L2#0 (Score: 0.2)}
```
Kept by pruning: lvl:println@L3#0 (0.45), lvl:println@L2#1 (0.35), lvl:println@L2#0 (0.20)

Label prompt for level way lvl:println@L3#0 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> System.out.println(s); is a statement, so its line of output appears at its own place in the sequence.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Label prompt for level way lvl:println@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> Output is the value's characters followed by a line break: println("Hello, "); println("World!"); prints two lines.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Label prompt for level way lvl:println@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Evaluate the argument, print its characters at the current position, then write the line separator so the cursor moves to the beginning of the next line.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:println@L3#0 | not applied |  |  | 0.0 |  |  |
| lvl:println@L2#1 | not applied |  |  | 0.0 |  |  |
| lvl:println@L2#0 | not applied |  |  | 0.0 |  |  |

#### if_statement, misconceptions: 22 edges offered
Edges offered:
| edge |
|---|
| err:if_statement->BracelessMultiStatementBody \| wrong rule: Indenting several statements under an if or for makes them all part of its body, even without braces. \| right rule: Without braces only the first statement belongs to the if/for; the rest run once, after it. |
| err:if_statement->CurlyIfCondition \| wrong rule: Writes the if condition inside { } instead of ( ). \| right rule: The condition of an if is written in parentheses. |
| err:if_statement->SemicolonAfterIfHeader \| wrong rule: if (x > 0); System.out.println("positive"); prints only for positive x. \| right rule: The ; ends the if with an empty statement, so the next line always runs. |
| mis:if_statement->AssignCompares \| wrong rule: = compares two values instead of assigning \| right rule: x = y copies the value of y into x; x == y is what compares them. |
| mis:if_statement->BranchChosenByIntent \| wrong rule: Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true. \| right rule: The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs. |
| mis:if_statement->CodeAfterIfSkipped \| wrong rule: When the then branch runs, the code after the if is skipped. \| right rule: After the if finishes, execution continues with the next statement either way. |
| mis:if_statement->FalseConditionEndsProgram \| wrong rule: A false condition with no else ends the program. \| right rule: When an if condition is false and there is no else, execution continues with the statement after the if. |
| mis:if_statement->FalseConditionRestartsProgram \| wrong rule: When an if condition is false (and there is no else), control jumps back to the start of the program. \| right rule: A false condition skips the then branch and execution continues with the statement after the if statement. |
| mis:if_statement->IfConditionCheckedInHindsight \| wrong rule: Whether the branch runs is decided by the condition after the branch, or from the point inside the body where the condition becomes true. \| right rule: The condition is tested once, before the branch; the whole branch runs if it was true at that moment and none of it runs otherwise. |
| mis:if_statement->IfConditionWatched \| wrong rule: An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever). \| right rule: An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch. |
| mis:if_statement->IfInLoopUnchecked \| wrong rule: An if inside a loop body runs its branch on every pass without testing its condition. \| right rule: The if condition is tested again on every pass, with the current values, so the branch runs only on passes where it is true. |
| mis:if_statement->IfIsLoop \| wrong rule: The if body keeps repeating as long as its condition stays true. \| right rule: An if body runs at most once; only a loop repeats its body. |
| mis:if_statement->IfRequiresElse \| wrong rule: Every if statement requires an else. \| right rule: An if statement may stand alone; the else part is optional. |
| mis:if_statement->IfWaitsForCondition \| wrong rule: An IF statement earlier in the program stays active and fires later, e.g. inside a later loop, when its condition becomes true. \| right rule: An if is evaluated once when control reaches it; afterwards it is inactive unless control returns to it. |
| mis:if_statement->LoopForOneTimeTest \| wrong rule: Uses a loop where a condition needs to be tested only once. \| right rule: A test made once is an if; a loop repeats. |
| mis:if_statement->MapToBooleanWithIf \| wrong rule: you need an if to turn a boolean expression into a boolean \| right rule: ok = (x > y); stores the result of the comparison directly. |
| mis:if_statement->MissingBraces \| wrong rule: Omits braces around a single-statement body of if, for or while. \| right rule: Braces are optional for a single-statement body, but using them anyway avoids bugs when statements are added later. |
| mis:if_statement->NextStatementIsElse \| wrong rule: In if (c) A; B; the statement B runs only when c is false. \| right rule: B is not part of the if; it runs every time. |
| mis:if_statement->ProgramLooksAhead \| wrong rule: The program knows or sees what later lines will do and acts on those goals at the current line, e.g. it stops 'at ten' because it wants to draw a box. \| right rule: Each statement executes using only the current state; later lines have no effect until control reaches them. |
| mis:if_statement->SequentialIfsAreNested \| wrong rule: Of two if statements one after the other, the second runs its body only if both conditions are true. \| right rule: Two ifs in sequence are independent: each tests only its own condition. |
| mis:if_statement->StatementAfterIfInBranch \| wrong rule: A statement placed after the if statement belongs to its branch, so it runs only when the condition is true. \| right rule: The branch ends at its closing brace (or after its single statement); the next statement runs whatever the condition was. |
| mis:if_statement->ThenAlwaysExecutes \| wrong rule: The then branch always runs. \| right rule: The then branch runs only when the condition is true. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
err:if_statement->BracelessMultiStatementBody (0.50), mis:if_statement->BranchChosenByIntent (0.30), mis:if_statement->ThenAlwaysExecutes (0.20)
```
Kept by pruning: err:if_statement->BracelessMultiStatementBody (0.50), mis:if_statement->BranchChosenByIntent (0.30), mis:if_statement->ThenAlwaysExecutes (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| err:if_statement->BracelessMultiStatementBody \| wrong rule: Indenting several statements under an if or for makes them all part of its body, even without braces. \| right rule: Without braces only the first statement belongs to the if/for; the rest run once, after it. |
| mis:if_statement->BranchChosenByIntent \| wrong rule: Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true. \| right rule: The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs. |
| mis:if_statement->ThenAlwaysExecutes \| wrong rule: The then branch always runs. \| right rule: The then branch runs only when the condition is true. |
Model's reply:
```
err:if_statement->BracelessMultiStatementBody | not applied | clauses: none | confidence: 0.6
mis:if_statement->BranchChosenByIntent | correct | clauses: 3, 4, 6, 7 | confidence: 0.55
mis:if_statement->ThenAlwaysExecutes | correct | clauses: 6, 7 | confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| err:if_statement->BracelessMultiStatementBody | not applied |  |  | 0.0 |  |  |
| mis:if_statement->BranchChosenByIntent | correct | 0.3 | 0.55 | 0.17 | c3, c4, c6, c7 | x > 0; and thats true; x > 10 is false; so big isnt printed either |
| mis:if_statement->ThenAlwaysExecutes | correct | 0.2 | 0.85 | 0.17 | c6, c7 | x > 10 is false; so big isnt printed either |

#### if_statement, level ways: 19 edges offered
Edges offered:
| edge |
|---|
| lvl:if_statement@L0#0 \| level L0 way everyday_reading: Folk meaning: English 'if' (and 'whenever') states a standing rule that stays in force and fires whenever its condition becomes true. A Java if is evaluated once, when control reaches it, and then is 'taken off the books'; changing the variables later does not re-trigger it. |
| lvl:if_statement@L0#14 \| level L0 way inconsistent_trace: Applies the if rule (LT) unevenly: tests the condition on some visits but not others (e.g. runs the branch on every loop pass without testing), runs the branch after a false test, or re-checks the condition after the branch has run. (here mixing in: "an if body repeats while its condition holds") |
| lvl:if_statement@L1#0 \| level L1 way names_the_element: The if statement is a conditional (selection) statement: it runs a statement or block only when a boolean condition is true. |
| lvl:if_statement@L1#1 \| level L1 way states_the_rule: Syntax: if (<boolean expression>) <statement or { block }>; the braces are optional when the body is a single statement. The expression must have type boolean (or Boolean), and the body is executed if and only if the expression is true. |
| lvl:if_statement@L2#0 \| level L2 way line_by_line_trace: Evaluate the condition once; if true, execute the body; then, in either case, continue with the statement after the if. |
| lvl:if_statement@L2#1 \| level L2 way output_prediction: An if produces no value; its observable result is that the body's effects (assignments, output) happen exactly once when the condition is true and not at all when it is false; e.g. if (x < 0) x = -x; leaves x = 5 for 5 and gives 5 for -5. |
| lvl:if_statement@L2#2 \| level L2 way one_step_execution: One execution reads the variables in the condition, changes nothing by the test itself (unless the condition has a side effect), and, when true, applies the body's changes once; control then moves to the next statement. |
| lvl:if_statement@L3#0 \| level L3 way relation_to_neighbour: The condition must be a boolean expression; a non-boolean condition such as if (t = goal) with int t is a compile-time error, while if (b = false) with boolean b compiles and assigns. |
| lvl:if_statement@L3#1 \| level L3 way relation_to_neighbour: if-else extends if with a second branch that runs exactly when the condition is false; a lone if has an implicit empty else-case. |
| lvl:if_statement@L3#2 \| level L3 way relation_to_neighbour: An if is a fork in the control flow: one path through the body, one around it, both rejoining at the next statement. |
| lvl:if_statement@L3#3 \| level L3 way relation_to_neighbour: if and while have the same form, but if tests its condition once and runs the block at most once, while while tests again after every pass and repeats the block as long as the condition is true. |
| lvl:if_statement@L3#4 \| level L3 way purpose_of_the_whole: Plan: guard / conditional action - do something only for the inputs that need it (absolute value, put two values in order, error check before dividing). |
| lvl:if_statement@L4#0 \| level L4 way predict_a_change: Negating the condition swaps which inputs run the body; changing < to <= changes only the boundary value. Adding a statement under a braceless if does not put it in the body. Whatever the condition, code after the if still runs exactly once. |
| lvl:if_statement@L4#1 \| level L4 way diagnose_an_error: rule broken: A ; right after if (...) is an empty statement that forms the whole then branch; the following statement or block is no longer part of the if. Kind: silent logic error. Trigger class: Any if (cond); followed by a statement or block: that statement runs for every input, whatever cond is (it compiles without error). |
| lvl:if_statement@L4#2 \| level L4 way diagnose_an_error: rule broken: The if template is if (<boolean expression>) <statement>: the condition must be enclosed in parentheses. Kind: compile-time. Trigger class: Any if whose condition is written in { } or without ( ), e.g. if {x > 0} ... or if a > b { c = 0; }. |
| lvl:if_statement@L4#3 \| level L4 way transfer_to_a_new_program: Use an if when an action is needed for some inputs only and the test happens once at that point; use a loop if the action must repeat while the condition holds, and assign a boolean directly (ok = x > y;) when you only need the truth value. |
| lvl:if_statement@L4#4 \| level L4 way diagnose_an_error: rule broken: Without braces, the body of an if, while or for is exactly one statement; indentation does not add statements to it. Kind: silent logic error. Trigger class: A braceless header followed by two or more indented statements: only the first is controlled, the others run once, after the if/loop, on every input. |
| lvl:if_statement@L4#5 \| level L4 way diagnose_an_error: rule broken: The condition of an if must have type boolean. Kind: compile-time. Trigger class: Using = instead of == with int operands, e.g. if (t = goal): 'incompatible types: int cannot be converted to boolean'. |
| lvl:if_statement@L4#6 \| level L4 way diagnose_an_error: rule broken: With boolean operands, = is assignment, not comparison. Kind: silent logic error. Trigger class: if (isPrime = false) with boolean isPrime: compiles, sets isPrime to false and the branch never runs. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:if_statement@L4#4 (Score: 0.5)}
{lvl:if_statement@L3#1 (Score: 0.3)}
{lvl:if_statement@L2#0 (Score: 0.2)}
```
Kept by pruning: lvl:if_statement@L4#4 (0.50), lvl:if_statement@L3#1 (0.30), lvl:if_statement@L2#0 (0.20)

Label prompt for level way lvl:if_statement@L4#4 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: Without braces, the body of an if, while or for is exactly one statement; indentation does not add statements to it. Kind: silent logic error. Trigger class: A braceless header followed by two or more indented statements: only the first is controlled, the others run once, after the if/loop, on every input.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:if_statement@L3#1 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> if-else extends if with a second branch that runs exactly when the condition is false; a lone if has an implicit empty else-case.

Model's reply:
```
Label: shown
Clauses: 3, 4, 5, 6, 7
Confidence: 0.7
```

Label prompt for level way lvl:if_statement@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Evaluate the condition once; if true, execute the body; then, in either case, continue with the statement after the if.

Model's reply:
```
Label: shown
Clauses: 3, 4, 5, 6, 7
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:if_statement@L4#4 | not applied |  |  | 0.0 |  |  |
| lvl:if_statement@L3#1 | shown | 0.3 | 0.7 | 0.21 | c3, c4, c5, c6, c7 | x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |
| lvl:if_statement@L2#0 | shown | 0.2 | 0.8 | 0.16 | c3, c4, c5, c6, c7 | x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:comparison_operators->LessGreaterSwapped [correct, tier 2, 0.68], lvl:comparison_operators@L2#1 [shown, tier 2, 0.32], lvl:comparison_operators@L3#1 [shown, tier 2, 0.24]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | Nothing | not covered yet |
| c2 | The else lines up with if | not covered yet |
| c3 | x > 0 | mis:comparison_operators->LessGreaterSwapped |
| c4 | and thats true | mis:comparison_operators->LessGreaterSwapped |
| c5 | so the else is skipped | not covered yet |
| c6 | x > 10 is false | mis:comparison_operators->LessGreaterSwapped |
| c7 | so big isnt printed either | mis:if_statement->BranchChosenByIntent |

**Uncovered clauses bring in (BM25 of the uncovered clauses against unvisited concepts):** control_flow (5.84), dangling_else (4.86), nested_conditionals (4.69)

**Graph check, not yet read (the walk may not stop while these remain):** own edges of control_flow, own edges of dangling_else, own edges of nested_conditionals, par:assignment~comparison_operators, pre:boolean_expression->if_statement, pre:comparison_operators->boolean_expression, pre:control_flow->if_statement, pre:expression->comparison_operators, pre:if_statement->if_else_statement, pre:if_statement->nested_conditionals, pre:statement->println, pre:string_literal->println

Figure 4 (the graph after depth 1): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY34_figure04.png

### Depth 2: current concepts 'comparison_operators', 'println', 'if_statement', 'control_flow', 'dangling_else', 'nested_conditionals'

#### comparison_operators, concept edges: 3 edges offered
Edges offered:
| edge |
|---|
| par:assignment~comparison_operators \| rule: x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands. |
| pre:comparison_operators->boolean_expression \| rule: A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making. |
| pre:expression->comparison_operators \| rule: Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:comparison_operators->boolean_expression (Score: 0.6)}
{pre:expression->comparison_operators (Score: 0.3)}
{par:assignment~comparison_operators (Score: 0.1)}
```
Kept by pruning: pre:comparison_operators->boolean_expression (0.60), pre:expression->comparison_operators (0.30), par:assignment~comparison_operators (0.10)

Label prompt for concept edge pre:comparison_operators->boolean_expression (comparison_operators -> boolean_expression, prerequisite):
> A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making.

Model's reply:
```
Label: confirmed
Clauses: 3, 4, 6, 7
Confidence: 0.8
```

Label prompt for concept edge pre:expression->comparison_operators (expression -> comparison_operators, prerequisite):
> Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b.

Model's reply:
```
Label: confirmed
Clauses: 3, 4, 6
Confidence: 0.8
```

Label prompt for concept edge par:assignment~comparison_operators (assignment -> comparison_operators, parallel):
> x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:comparison_operators->boolean_expression | confirmed | 0.6000000000000001 | 0.8 | 0.48 | c3, c4, c6, c7 | x > 0; and thats true; x > 10 is false; so big isnt printed either |
| pre:expression->comparison_operators | confirmed | 0.30000000000000004 | 0.8 | 0.24 | c3, c4, c6 | x > 0; and thats true; x > 10 is false |
| par:assignment~comparison_operators | not applied |  |  | 0.0 |  |  |

#### println, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| pre:statement->println \| rule: System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |
| pre:string_literal->println \| rule: println("s") outputs exactly the characters between the quotes and then ends the line. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:statement->println (Score: 0.7)}
{pre:string_literal->println (Score: 0.3)}
```
Kept by pruning: pre:statement->println (0.70), pre:string_literal->println (0.30)

Label prompt for concept edge pre:statement->println (statement -> println, prerequisite):
> System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence.

Model's reply:
```
Label: confirmed
Clauses: 7
Confidence: 0.55
```

Label prompt for concept edge pre:string_literal->println (string_literal -> println, prerequisite):
> println("s") outputs exactly the characters between the quotes and then ends the line.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:statement->println | confirmed | 0.7 | 0.55 | 0.39 | c7 | so big isnt printed either |
| pre:string_literal->println | not applied |  |  | 0.0 |  |  |

#### if_statement, concept edges: 4 edges offered
Edges offered:
| edge |
|---|
| pre:boolean_expression->if_statement \| rule: An if runs its block only when its boolean expression evaluates to true. |
| pre:control_flow->if_statement \| rule: An if changes the default top-to-bottom flow by running a block only when its condition is true. |
| pre:if_statement->if_else_statement \| rule: if-else extends if with a second block that runs exactly when the condition is false. |
| pre:if_statement->nested_conditionals \| rule: An if statement can sit inside the body of another if; the inner one is tested only when the outer condition is true. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:if_statement->nested_conditionals (Score: 0.4)}
{pre:if_statement->if_else_statement (Score: 0.35)}
{pre:boolean_expression->if_statement (Score: 0.25)}
```
Kept by pruning: pre:if_statement->nested_conditionals (0.40), pre:if_statement->if_else_statement (0.35), pre:boolean_expression->if_statement (0.25)

Label prompt for concept edge pre:if_statement->nested_conditionals (if_statement -> nested_conditionals, prerequisite):
> An if statement can sit inside the body of another if; the inner one is tested only when the outer condition is true.

Model's reply:
```
Label: confirmed
Clauses: 3, 4, 6, 7
Confidence: 0.8
```

Label prompt for concept edge pre:if_statement->if_else_statement (if_statement -> if_else_statement, prerequisite):
> if-else extends if with a second block that runs exactly when the condition is false.

Model's reply:
```
Label: confirmed
Clauses: 3, 4, 5
Confidence: 0.6
```

Label prompt for concept edge pre:boolean_expression->if_statement (boolean_expression -> if_statement, prerequisite):
> An if runs its block only when its boolean expression evaluates to true.

Model's reply:
```
Label: confirmed
Clauses: 3, 4, 6, 7
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:if_statement->nested_conditionals | confirmed | 0.4 | 0.8 | 0.32 | c3, c4, c6, c7 | x > 0; and thats true; x > 10 is false; so big isnt printed either |
| pre:if_statement->if_else_statement | confirmed | 0.35 | 0.6 | 0.21 | c3, c4, c5 | x > 0; and thats true; so the else is skipped |
| pre:boolean_expression->if_statement | confirmed | 0.25 | 0.8 | 0.2 | c3, c4, c6, c7 | x > 0; and thats true; x > 10 is false; so big isnt printed either |

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
mis:control_flow->FalseConditionRestartsProgram (0.40), mis:control_flow->IfConditionWatched (0.30), mis:control_flow->StatementsRunInAnyOrder (0.30)
```
Kept by pruning: mis:control_flow->FalseConditionRestartsProgram (0.40), mis:control_flow->IfConditionWatched (0.30), mis:control_flow->StatementsRunInAnyOrder (0.30)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:control_flow->FalseConditionRestartsProgram \| wrong rule: When an if condition is false (and there is no else), control jumps back to the start of the program. \| right rule: A false condition skips the then branch and execution continues with the statement after the if statement. |
| mis:control_flow->IfConditionWatched \| wrong rule: An if statement watches its condition while the program runs and fires as soon as the condition becomes true (if = whenever). \| right rule: An if condition is tested once, when control reaches the if statement; later changes to the variables do not trigger the branch. |
| mis:control_flow->StatementsRunInAnyOrder \| wrong rule: Statements in a program can run in any order. \| right rule: Without control statements, statements run once each, top to bottom. |
Model's reply:
```
mis:control_flow->FalseConditionRestartsProgram | correct | clauses: 6, 7 | confidence: 0.6
mis:control_flow->IfConditionWatched | not applied | clauses: none | confidence: 0.9
mis:control_flow->StatementsRunInAnyOrder | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:control_flow->FalseConditionRestartsProgram | correct | 0.4 | 0.6 | 0.24 | c6, c7 | x > 10 is false; so big isnt printed either |
| mis:control_flow->IfConditionWatched | not applied |  |  | 0.0 |  |  |
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
{lvl:control_flow@L2#0 (Score: 0.45)}
{lvl:control_flow@L0#0 (Score: 0.3)}
{lvl:control_flow@L2#1 (Score: 0.25)}
```
Kept by pruning: lvl:control_flow@L2#0 (0.45), lvl:control_flow@L0#0 (0.30), lvl:control_flow@L2#1 (0.25)

Label prompt for level way lvl:control_flow@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Execute the statement at the current point; when it completes normally, control passes to the next statement in the block. An if evaluates its condition once and then runs at most one branch; a loop evaluates its condition before each pass; after an if or a loop finishes, control continues with the statement after it.

Model's reply:
```
Label: shown
Clauses: 3, 4, 5, 6, 7
Confidence: 0.8
```

Label prompt for level way lvl:control_flow@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: in everyday instructions a listener reads the whole list at once, does steps in a sensible order and infers what the writer wants. Java instead executes statements one at a time, top to bottom, each only when control reaches it, and nothing later in the program has any effect earlier.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.6
```

Label prompt for level way lvl:control_flow@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> The output is the sequence of print statements that control actually reaches, in the order reached: e.g. TenHellos prints 1st, 2nd, 3rd Hello once each, then 4th to 10th Hello from the loop.

Model's reply:
```
Label: shown
Clauses: 1, 3, 4, 5, 6, 7
Confidence: 0.75
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:control_flow@L2#0 | shown | 0.45 | 0.8 | 0.36 | c3, c4, c5, c6, c7 | x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |
| lvl:control_flow@L0#0 | not applied |  |  | 0.0 |  |  |
| lvl:control_flow@L2#1 | shown | 0.25 | 0.75 | 0.19 | c1, c3, c4, c5, c6, c7 | Nothing; x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |

#### dangling_else, misconceptions: 1 edges offered
Edges offered:
| edge |
|---|
| mis:dangling_else->ElseMatchesIndentation \| wrong rule: The else belongs to the if it is lined up with. \| right rule: The else belongs to the most recent unmatched if, whatever the indentation. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:dangling_else->ElseMatchesIndentation (Score: 1.0)}
```
Kept by pruning: mis:dangling_else->ElseMatchesIndentation (1.00)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:dangling_else->ElseMatchesIndentation \| wrong rule: The else belongs to the if it is lined up with. \| right rule: The else belongs to the most recent unmatched if, whatever the indentation. |
Model's reply:
```
mis:dangling_else->ElseMatchesIndentation | held | clauses: 1, 2, 3, 4, 5 | confidence: 0.93
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:dangling_else->ElseMatchesIndentation | held | 1.0 | 0.93 | 0.93 | c1, c2, c3, c4, c5 | Nothing; The else lines up with if; x > 0; and thats true; so the else is skipped |

#### dangling_else, level ways: 12 edges offered
Edges offered:
| edge |
|---|
| lvl:dangling_else@L0#0 \| level L0 way everyday_reading: Folk meaning: on paper the layout shows which 'if' an 'otherwise' answers, so an else lined up with the outer if is read as belonging to it. Java ignores indentation and attaches each else to the innermost if to which it might possibly belong. |
| lvl:dangling_else@L0#2 \| level L0 way inconsistent_trace: Applies the matching rule (LT) unevenly: attaches the else to the inner if in one fragment but to the outer if in a similarly indented one. (here mixing in: "The else belongs to the if it is lined up with") |
| lvl:dangling_else@L1#0 \| level L1 way names_the_element: The dangling else is the ambiguity of an else after two nested ifs without braces: it could belong to either if. |
| lvl:dangling_else@L1#1 \| level L1 way states_the_rule: Java decrees that an else clause belongs to the innermost if to which it might possibly belong: if <e1> if <e2> A else B means if <e1> { if <e2> A else B }. |
| lvl:dangling_else@L2#0 \| level L2 way line_by_line_trace: Parse first: match each else with the nearest preceding unmatched if; then execute: test e1; only if true test e2, running A if e2 is true and B if e2 is false; if e1 is false nothing runs. |
| lvl:dangling_else@L2#1 \| level L2 way output_prediction: For if (x > 0) if (y > 0) A; else B;: x > 0, y > 0 runs A; x > 0, y <= 0 runs B; x <= 0 runs neither, even if the else was indented under the outer if. |
| lvl:dangling_else@L2#2 \| level L2 way one_step_execution: One execution tests e1 and, only if it is true, e2; it runs at most one of A and B. |
| lvl:dangling_else@L3#0 \| level L3 way relation_to_neighbour: The dangling else arises only when ifs are nested without braces; adding braces around the inner if lets the else belong to the outer if. |
| lvl:dangling_else@L3#1 \| level L3 way purpose_of_the_whole: Purpose: not a technique but a pitfall to recognise; braces state the intended pairing explicitly. |
| lvl:dangling_else@L4#0 \| level L4 way predict_a_change: Adding braces { if (e2) A } before the else moves the else to the outer if and changes the behaviour for e1 false; re-indenting the code changes nothing. |
| lvl:dangling_else@L4#1 \| level L4 way transfer_to_a_new_program: Whenever an if without braces contains another if and an else follows, add braces to state which if the else belongs to; coding standards require brackets for this reason. |
| lvl:dangling_else@L4#2 \| level L4 way diagnose_an_error: rule broken: An else belongs to the innermost unmatched if. Kind: silent logic error. Trigger class: Nested braceless ifs with the else indented under the outer if: the else case runs for inner-false inputs and never for outer-false inputs. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:dangling_else@L0#0 (Score: 0.7)}
{lvl:dangling_else@L2#1 (Score: 0.15)}
{lvl:dangling_else@L4#2 (Score: 0.15)}
```
Kept by pruning: lvl:dangling_else@L0#0 (0.70), lvl:dangling_else@L2#1 (0.15), lvl:dangling_else@L4#2 (0.15)

Label prompt for level way lvl:dangling_else@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: on paper the layout shows which 'if' an 'otherwise' answers, so an else lined up with the outer if is read as belonging to it. Java ignores indentation and attaches each else to the innermost if to which it might possibly belong.

Model's reply:
```
Label: shown
Clauses: 2, 3, 4, 5
Confidence: 0.85
```

Label prompt for level way lvl:dangling_else@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> For if (x > 0) if (y > 0) A; else B;: x > 0, y > 0 runs A; x > 0, y <= 0 runs B; x <= 0 runs neither, even if the else was indented under the outer if.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.93
```

Label prompt for level way lvl:dangling_else@L4#2 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: An else belongs to the innermost unmatched if. Kind: silent logic error. Trigger class: Nested braceless ifs with the else indented under the outer if: the else case runs for inner-false inputs and never for outer-false inputs.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.92
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:dangling_else@L0#0 | shown | 0.7 | 0.85 | 0.59 | c2, c3, c4, c5 | The else lines up with if; x > 0; and thats true; so the else is skipped |
| lvl:dangling_else@L2#1 | not applied |  |  | 0.0 |  |  |
| lvl:dangling_else@L4#2 | not applied |  |  | 0.0 |  |  |

#### nested_conditionals, misconceptions: 6 edges offered
Edges offered:
| edge |
|---|
| mis:nested_conditionals->ElseMatchesIndentation \| wrong rule: The else belongs to the if it is lined up with. \| right rule: The else belongs to the most recent unmatched if, whatever the indentation. |
| mis:nested_conditionals->InconsistentIndentation \| wrong rule: Indents nested blocks inconsistently, so the visual nesting differs from the real nesting. \| right rule: Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation. |
| mis:nested_conditionals->InnerIfIgnoresOuter \| wrong rule: An inner if runs its body whenever its own condition is true, even if the outer if condition is false. \| right rule: The inner if is part of the outer branch: it is reached, and its condition tested, only when the outer condition is true. |
| mis:nested_conditionals->MultipleElseIfBranchesRun \| wrong rule: Every true branch of an else-if chain runs. \| right rule: Only the first branch whose condition is true runs. |
| mis:nested_conditionals->NestedIfsInsteadOfLogicalOperators \| wrong rule: A condition on several values has to be written as nested if statements, one value per if. \| right rule: Several conditions combine into one boolean expression with && and \|\|, e.g. if (x == 0 && y == 0). |
| mis:nested_conditionals->SequentialIfsAreNested \| wrong rule: Of two if statements one after the other, the second runs its body only if both conditions are true. \| right rule: Two ifs in sequence are independent: each tests only its own condition. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:nested_conditionals->ElseMatchesIndentation (0.70), mis:nested_conditionals->InconsistentIndentation (0.15), mis:nested_conditionals->InnerIfIgnoresOuter (0.15)
```
Kept by pruning: mis:nested_conditionals->ElseMatchesIndentation (0.70), mis:nested_conditionals->InconsistentIndentation (0.15), mis:nested_conditionals->InnerIfIgnoresOuter (0.15)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:nested_conditionals->ElseMatchesIndentation \| wrong rule: The else belongs to the if it is lined up with. \| right rule: The else belongs to the most recent unmatched if, whatever the indentation. |
| mis:nested_conditionals->InconsistentIndentation \| wrong rule: Indents nested blocks inconsistently, so the visual nesting differs from the real nesting. \| right rule: Indent consistently, one level deeper for each nested block, so the layout shows the real nesting; the compiler ignores indentation. |
| mis:nested_conditionals->InnerIfIgnoresOuter \| wrong rule: An inner if runs its body whenever its own condition is true, even if the outer if condition is false. \| right rule: The inner if is part of the outer branch: it is reached, and its condition tested, only when the outer condition is true. |
Model's reply:
```
mis:nested_conditionals->ElseMatchesIndentation | held | clauses: 2, 3, 4, 5 | confidence: 0.93
mis:nested_conditionals->InconsistentIndentation | not applied | clauses: none | confidence: 0.85
mis:nested_conditionals->InnerIfIgnoresOuter | not applied | clauses: none | confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:nested_conditionals->ElseMatchesIndentation | held | 0.7 | 0.93 | 0.65 | c2, c3, c4, c5 | The else lines up with if; x > 0; and thats true; so the else is skipped |
| mis:nested_conditionals->InconsistentIndentation | not applied |  |  | 0.0 |  |  |
| mis:nested_conditionals->InnerIfIgnoresOuter | not applied |  |  | 0.0 |  |  |

#### nested_conditionals, level ways: 14 edges offered
Edges offered:
| edge |
|---|
| lvl:nested_conditionals@L0#0 \| level L0 way everyday_reading: Folk meaning: in prose, indentation and line layout show what belongs to what, and two consecutive 'if' sentences can be heard as one combined condition. The Java compiler ignores indentation: an inner if belongs to the branch that syntactically contains it, and an else pairs with the innermost unmatched if. |
| lvl:nested_conditionals@L0#3 \| level L0 way inconsistent_trace: Applies the nesting rule (LT) unevenly: on some inputs tests the inner condition even though the outer one was false, or matches an else to the if it is lined up with. (here mixing in: "An inner if runs its body whenever its own condition is true, even if the outer if condition is false") |
| lvl:nested_conditionals@L1#0 \| level L1 way names_the_element: Nested conditionals are if or if-else statements placed inside a branch of another conditional; an else-if chain is the common special case. |
| lvl:nested_conditionals@L1#1 \| level L1 way states_the_rule: An if/if-else is a statement, so it can be the body (branch) of another conditional; without braces an else belongs to the innermost if to which it might belong, so braces should be used to resolve ambiguities. |
| lvl:nested_conditionals@L2#0 \| level L2 way line_by_line_trace: Test the outer condition; only if control enters the branch that contains the inner if is the inner condition tested; after the inner statement, control leaves the outer statement too. |
| lvl:nested_conditionals@L2#1 \| level L2 way output_prediction: The output is the action of the single path whose conditions all hold along the way: if (a > b) { if (b > c) X; else Y; } else Z; runs X when a > b > c, Y when a > b and b <= c, and Z otherwise. |
| lvl:nested_conditionals@L2#2 \| level L2 way one_step_execution: One execution evaluates the conditions along one path only (outer, then possibly inner) and applies one leaf action; conditions on other paths are never evaluated. |
| lvl:nested_conditionals@L3#0 \| level L3 way relation_to_neighbour: Nesting puts an if or if-else inside a branch of another if-else; when the inner statement fills the else branch it forms an else-if chain. |
| lvl:nested_conditionals@L3#1 \| level L3 way relation_to_neighbour: The dangling-else ambiguity arises when ifs are nested without braces: if <e1> if <e2> A else B attaches else to the inner if. |
| lvl:nested_conditionals@L3#2 \| level L3 way relation_to_neighbour: For more than two mutually exclusive alternatives a chain of if-else statements works, but a switch tests one expression against many values directly. |
| lvl:nested_conditionals@L3#3 \| level L3 way purpose_of_the_whole: Plan: decision tree - refine a case analysis step by step (e.g. find the smallest of three values, classify a value into ranges). |
| lvl:nested_conditionals@L4#0 \| level L4 way predict_a_change: Combining if (c1) { if (c2) S; } into if (c1 && c2) S; preserves behaviour when there are no else parts; adding or removing braces around an inner if can move an else to a different if. Swapping some branches can keep the specification only on certain inputs. |
| lvl:nested_conditionals@L4#1 \| level L4 way transfer_to_a_new_program: Nest conditionals when a second test only makes sense once the first has succeeded or when cases form a tree; use && for a simple conjunction, an else-if chain for mutually exclusive ranges, and a switch for many discrete values; one or two levels usually suffice. |
| lvl:nested_conditionals@L4#2 \| level L4 way diagnose_an_error: rule broken: Without braces an else pairs with the innermost if, whatever the indentation. Kind: silent logic error. Trigger class: if (a) if (b) X; else Y; written with else under the outer if: Y runs when a is true and b false, not when a is false. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:nested_conditionals@L0#3 (Score: 0.45)}
{lvl:nested_conditionals@L0#0 (Score: 0.35)}
{lvl:nested_conditionals@L4#2 (Score: 0.2)}
```
Kept by pruning: lvl:nested_conditionals@L0#3 (0.45), lvl:nested_conditionals@L0#0 (0.35), lvl:nested_conditionals@L4#2 (0.20)

Label prompt for level way lvl:nested_conditionals@L0#3 (the model saw only the concept, the way's name 'inconsistent trace' and its text; no level):
> Applies the nesting rule (LT) unevenly: on some inputs tests the inner condition even though the outer one was false, or matches an else to the if it is lined up with. (here mixing in: "An inner if runs its body whenever its own condition is true, even if the outer if condition is false")

Model's reply:
```
Label: shown
Clauses: 2, 5
Confidence: 0.85
```

Label prompt for level way lvl:nested_conditionals@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: in prose, indentation and line layout show what belongs to what, and two consecutive 'if' sentences can be heard as one combined condition. The Java compiler ignores indentation: an inner if belongs to the branch that syntactically contains it, and an else pairs with the innermost unmatched if.

Model's reply:
```
Label: shown
Clauses: 1, 2, 5
Confidence: 0.85
```

Label prompt for level way lvl:nested_conditionals@L4#2 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: Without braces an else pairs with the innermost if, whatever the indentation. Kind: silent logic error. Trigger class: if (a) if (b) X; else Y; written with else under the outer if: Y runs when a is true and b false, not when a is false.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:nested_conditionals@L0#3 | shown | 0.45 | 0.85 | 0.38 | c2, c5 | The else lines up with if; so the else is skipped |
| lvl:nested_conditionals@L0#0 | shown | 0.35 | 0.85 | 0.3 | c1, c2, c5 | Nothing; The else lines up with if; so the else is skipped |
| lvl:nested_conditionals@L4#2 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:dangling_else->ElseMatchesIndentation [held, tier 0, 0.93], mis:nested_conditionals->ElseMatchesIndentation [held, tier 0, 0.65], lvl:dangling_else@L0#0 [shown, tier 2, 0.59]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | Nothing | mis:dangling_else->ElseMatchesIndentation |
| c2 | The else lines up with if | mis:dangling_else->ElseMatchesIndentation |
| c3 | x > 0 | mis:comparison_operators->LessGreaterSwapped |
| c4 | and thats true | mis:comparison_operators->LessGreaterSwapped |
| c5 | so the else is skipped | pre:if_statement->if_else_statement |
| c6 | x > 10 is false | mis:comparison_operators->LessGreaterSwapped |
| c7 | so big isnt printed either | mis:if_statement->BranchChosenByIntent |

**Graph check, not yet read (the walk may not stop while these remain):** pre:if_else_statement->nested_conditionals, pre:nested_conditionals->dangling_else, pre:statement->control_flow

Figure 5 (the graph after depth 2): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY34_figure05.png

### Depth 3: current concepts 'dangling_else', 'nested_conditionals', 'control_flow'

#### dangling_else, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:nested_conditionals->dangling_else \| rule: The dangling else arises when ifs are nested without braces. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:nested_conditionals->dangling_else (Score: 1.0)}
```
Kept by pruning: pre:nested_conditionals->dangling_else (1.00)

Label prompt for concept edge pre:nested_conditionals->dangling_else (nested_conditionals -> dangling_else, prerequisite):
> The dangling else arises when ifs are nested without braces.

Model's reply:
```
Label: broken
Clauses: 2, 5, 7
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:nested_conditionals->dangling_else | broken | 1.0 | 0.8 | 0.8 | c2, c5, c7 | The else lines up with if; so the else is skipped; so big isnt printed either |

#### nested_conditionals, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| pre:if_else_statement->nested_conditionals \| rule: Nesting puts an if or if-else inside a branch of another if-else; an else-if chain is the common case where the else branch is itself an if. |
| pre:if_statement->nested_conditionals \| rule: An if statement can sit inside the body of another if; the inner one is tested only when the outer condition is true. |
| pre:nested_conditionals->dangling_else \| rule: The dangling else arises when ifs are nested without braces. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:if_else_statement->nested_conditionals (Score: 0.6)}
{pre:if_statement->nested_conditionals (Score: 0.4)}
```
Kept by pruning: pre:if_else_statement->nested_conditionals (0.60), pre:if_statement->nested_conditionals (0.40)

Label prompt for concept edge pre:if_else_statement->nested_conditionals (if_else_statement -> nested_conditionals, prerequisite):
> Nesting puts an if or if-else inside a branch of another if-else; an else-if chain is the common case where the else branch is itself an if.

Model's reply:
```
Label: broken
Clauses: 1, 2, 5
Confidence: 0.85
```

Label prompt for concept edge pre:if_statement->nested_conditionals (if_statement -> nested_conditionals, prerequisite):
> An if statement can sit inside the body of another if; the inner one is tested only when the outer condition is true.

Model's reply:
```
Label: confirmed
Clauses: 3, 4, 6, 7
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:if_else_statement->nested_conditionals | broken | 0.6 | 0.85 | 0.51 | c1, c2, c5 | Nothing; The else lines up with if; so the else is skipped |
| pre:if_statement->nested_conditionals | confirmed | 0.4 | 0.8 | 0.32 | c3, c4, c6, c7 | x > 0; and thats true; x > 10 is false; so big isnt printed either |

#### control_flow, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| pre:control_flow->if_statement \| rule: An if changes the default top-to-bottom flow by running a block only when its condition is true. |
| pre:statement->control_flow \| rule: Control flow is the order in which statements run. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:control_flow->if_statement (Score: 0.8)}
{pre:statement->control_flow (Score: 0.2)}
```
Kept by pruning: pre:control_flow->if_statement (0.80), pre:statement->control_flow (0.20)

Label prompt for concept edge pre:control_flow->if_statement (control_flow -> if_statement, prerequisite):
> An if changes the default top-to-bottom flow by running a block only when its condition is true.

Model's reply:
```
Label: confirmed
Clauses: 3, 4, 6, 7
Confidence: 0.8
```

Label prompt for concept edge pre:statement->control_flow (statement -> control_flow, prerequisite):
> Control flow is the order in which statements run.

Model's reply:
```
Label: confirmed
Clauses: 3, 4, 6, 7
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:control_flow->if_statement | confirmed | 0.8 | 0.8 | 0.64 | c3, c4, c6, c7 | x > 0; and thats true; x > 10 is false; so big isnt printed either |
| pre:statement->control_flow | confirmed | 0.2 | 0.6 | 0.12 | c3, c4, c6, c7 | x > 0; and thats true; x > 10 is false; so big isnt printed either |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:nested_conditionals->dangling_else [broken, tier 0, 0.80], pre:if_else_statement->nested_conditionals [broken, tier 0, 0.51], pre:control_flow->if_statement [confirmed, tier 2, 0.64]

reached across pre:if_else_statement->nested_conditionals, entered next: if_else_statement

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | Nothing | mis:dangling_else->ElseMatchesIndentation |
| c2 | The else lines up with if | mis:dangling_else->ElseMatchesIndentation |
| c3 | x > 0 | mis:comparison_operators->LessGreaterSwapped |
| c4 | and thats true | mis:comparison_operators->LessGreaterSwapped |
| c5 | so the else is skipped | pre:if_statement->if_else_statement |
| c6 | x > 10 is false | mis:comparison_operators->LessGreaterSwapped |
| c7 | so big isnt printed either | mis:if_statement->BranchChosenByIntent |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of if_else_statement

Figure 6 (the graph after depth 3): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY34_figure06.png

### Depth 4: current concepts 'if_else_statement'

#### if_else_statement, misconceptions: 6 edges offered
Edges offered:
| edge |
|---|
| err:if_else_statement->ElseWithCondition \| wrong rule: Writes else (x > 0) with a condition but no if. \| right rule: else takes no condition; use else if (x > 0). |
| mis:if_else_statement->BothBranchesExecute \| wrong rule: Both the then branch and the else branch run. \| right rule: Exactly one of the two branches runs. |
| mis:if_else_statement->BranchChosenByIntent \| wrong rule: Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true. \| right rule: The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs. |
| mis:if_else_statement->ConditionalIsSequence \| wrong rule: if (c) A else B is the same as if (c) A followed by if (!c) B. \| right rule: In if-else, c is tested once and exactly one of A or B runs, even if A changes the variables that c uses. |
| mis:if_else_statement->DuplicateCodeInBranches \| wrong rule: Writes the same statements in both branches of an if-else. \| right rule: Code common to both branches belongs before or after the if-else. |
| mis:if_else_statement->ElseAlwaysExecutes \| wrong rule: The else branch of an if-else statement always executes. \| right rule: The else branch runs only when the if condition is false. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:if_else_statement->BranchChosenByIntent (0.40), mis:if_else_statement->ElseAlwaysExecutes (0.40), mis:if_else_statement->BothBranchesExecute (0.20)
```
Kept by pruning: mis:if_else_statement->BranchChosenByIntent (0.40), mis:if_else_statement->ElseAlwaysExecutes (0.40), mis:if_else_statement->BothBranchesExecute (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:if_else_statement->BranchChosenByIntent \| wrong rule: Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true. \| right rule: The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs. |
| mis:if_else_statement->ElseAlwaysExecutes \| wrong rule: The else branch of an if-else statement always executes. \| right rule: The else branch runs only when the if condition is false. |
| mis:if_else_statement->BothBranchesExecute \| wrong rule: Both the then branch and the else branch run. \| right rule: Exactly one of the two branches runs. |
Model's reply:
```
mis:if_else_statement->BranchChosenByIntent | correct | clauses: 3, 4, 5 | confidence: 0.7
mis:if_else_statement->ElseAlwaysExecutes | correct | clauses: 3, 4, 5 | confidence: 0.85
mis:if_else_statement->BothBranchesExecute | correct | clauses: 4, 5 | confidence: 0.75
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:if_else_statement->BranchChosenByIntent | correct | 0.4 | 0.7 | 0.28 | c3, c4, c5 | x > 0; and thats true; so the else is skipped |
| mis:if_else_statement->ElseAlwaysExecutes | correct | 0.4 | 0.85 | 0.34 | c3, c4, c5 | x > 0; and thats true; so the else is skipped |
| mis:if_else_statement->BothBranchesExecute | correct | 0.2 | 0.75 | 0.15 | c4, c5 | and thats true; so the else is skipped |

#### if_else_statement, level ways: 17 edges offered
Edges offered:
| edge |
|---|
| lvl:if_else_statement@L0#0 \| level L0 way everyday_reading: Folk meaning: in English 'otherwise' can be heard as 'and then also', and 'if ... else ...' as two separate rules that are each checked. In Java the condition is tested once and exactly one of the two branches runs. |
| lvl:if_else_statement@L0#5 \| level L0 way inconsistent_trace: Applies the if-else rule (LT) unevenly: on some traces runs both branches, re-tests the condition after the then branch to decide whether to run the else branch, or runs the else branch whatever the condition. (here mixing in: "if-else is the same as two separate ifs") |
| lvl:if_else_statement@L1#0 \| level L1 way names_the_element: The if-else statement is a two-way conditional: it executes one of two statements (or blocks) depending on a boolean condition. |
| lvl:if_else_statement@L1#1 \| level L1 way states_the_rule: Syntax: if (<boolean expression>) <statements T> else <statements F>; it executes one or the other, but not both: T if the condition is true, F otherwise. |
| lvl:if_else_statement@L2#0 \| level L2 way line_by_line_trace: Evaluate the condition once; if true execute the then branch, otherwise execute the else branch; then continue with the statement after the whole if-else (the condition is not re-tested). |
| lvl:if_else_statement@L2#1 \| level L2 way output_prediction: Exactly one branch's effects occur; e.g. if (x > y) max = x; else max = y; leaves max equal to the larger value, and the coin flip prints either Heads or Tails, never both. |
| lvl:if_else_statement@L2#2 \| level L2 way one_step_execution: One execution reads the condition's variables and applies the effects of exactly one branch; a change made by the then branch to the condition's variables cannot cause the else branch to run. |
| lvl:if_else_statement@L3#0 \| level L3 way relation_to_neighbour: if-else is an if with a second branch for the false case; dropping the else gives a plain if in which the false case does nothing. |
| lvl:if_else_statement@L3#1 \| level L3 way relation_to_neighbour: Either branch may itself be an if or if-else, which nests conditionals; without braces an inner else pairs with the innermost if. |
| lvl:if_else_statement@L3#2 \| level L3 way relation_to_neighbour: c ? a : b is the expression form of if (c) v = a; else v = b;: it yields a value of one branch, evaluating only the selected operand. |
| lvl:if_else_statement@L3#3 \| level L3 way relation_to_neighbour: An else-if chain is an if-else whose else part is another if-else, repeated; the final else catches all remaining cases. |
| lvl:if_else_statement@L3#4 \| level L3 way purpose_of_the_whole: Plan: two-way choice / alternative action - compute one of two results (max of two values, heads or tails, error message or quotient). |
| lvl:if_else_statement@L4#0 \| level L4 way predict_a_change: Swapping the two branches and negating the condition preserves behaviour; swapping the branches alone inverts it. Replacing if-else with two separate ifs is not equivalent when the then branch changes a variable used in the condition. |
| lvl:if_else_statement@L4#1 \| level L4 way diagnose_an_error: rule broken: else takes no condition: it is the branch for the false case of the preceding if; a further test needs else if (...). Kind: compile-time. Trigger class: Writing else (x > 0) stmt; the compiler reads (x > 0) as the start of an expression statement, which is not a valid statement, and reports an error. |
| lvl:if_else_statement@L4#2 \| level L4 way transfer_to_a_new_program: Use if-else when exactly one of two actions must happen; use a plain if when nothing happens in the false case, an else-if chain or switch for more than two mutually exclusive cases, and c ? a : b when you only need to choose a value. |
| lvl:if_else_statement@L4#3 \| level L4 way diagnose_an_error: rule broken: Code common to both branches belongs before or after the if-else. Kind: silent logic error. Trigger class: A statement duplicated in both branches and later edited in only one: the two cases silently diverge. |
| lvl:if_else_statement@L4#4 \| level L4 way diagnose_an_error: rule broken: An else must directly follow the then statement of an if. Kind: compile-time. Trigger class: if (c) x = 1; y = 2; else x = 0;: the else has no matching if ('else without if'). |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:if_else_statement@L3#1 (Score: 0.6)}
{lvl:if_else_statement@L2#0 (Score: 0.25)}
{lvl:if_else_statement@L2#1 (Score: 0.15)}
```
Kept by pruning: lvl:if_else_statement@L3#1 (0.60), lvl:if_else_statement@L2#0 (0.25), lvl:if_else_statement@L2#1 (0.15)

Label prompt for level way lvl:if_else_statement@L3#1 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Either branch may itself be an if or if-else, which nests conditionals; without braces an inner else pairs with the innermost if.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:if_else_statement@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Evaluate the condition once; if true execute the then branch, otherwise execute the else branch; then continue with the statement after the whole if-else (the condition is not re-tested).

Model's reply:
```
Label: shown
Clauses: 3, 4, 5, 6, 7
Confidence: 0.8
```

Label prompt for level way lvl:if_else_statement@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> Exactly one branch's effects occur; e.g. if (x > y) max = x; else max = y; leaves max equal to the larger value, and the coin flip prints either Heads or Tails, never both.

Model's reply:
```
Label: shown
Clauses: 3, 4, 5
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:if_else_statement@L3#1 | not applied |  |  | 0.0 |  |  |
| lvl:if_else_statement@L2#0 | shown | 0.25 | 0.8 | 0.2 | c3, c4, c5, c6, c7 | x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |
| lvl:if_else_statement@L2#1 | shown | 0.15 | 0.6 | 0.09 | c3, c4, c5 | x > 0; and thats true; so the else is skipped |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:if_else_statement->ElseAlwaysExecutes [correct, tier 2, 0.34], mis:if_else_statement->BranchChosenByIntent [correct, tier 2, 0.28], lvl:if_else_statement@L2#0 [shown, tier 2, 0.20]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | Nothing | mis:dangling_else->ElseMatchesIndentation |
| c2 | The else lines up with if | mis:dangling_else->ElseMatchesIndentation |
| c3 | x > 0 | mis:comparison_operators->LessGreaterSwapped |
| c4 | and thats true | mis:comparison_operators->LessGreaterSwapped |
| c5 | so the else is skipped | pre:if_statement->if_else_statement |
| c6 | x > 10 is false | mis:comparison_operators->LessGreaterSwapped |
| c7 | so big isnt printed either | mis:if_statement->BranchChosenByIntent |

Figure 7 (the graph after depth 4): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY34_figure07.png

Held set after the one-fault rules: mis:dangling_else->ElseMatchesIndentation; filed at the dependent concept: mis:nested_conditionals->ElseMatchesIndentation

Shadows (a held label on a prerequisite, on a generic concept, or at a concept where the graph attaches the misconception as context, resting on the words of a stronger label at the specific or primary concept, is one wrong sentence read twice; it marks no root cause and sets no level): mis:nested_conditionals->ElseMatchesIndentation (shadow of mis:dangling_else->ElseMatchesIndentation)

## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on ['dangling_else'], broken at [] (consequences: pre:nested_conditionals->dangling_else, pre:if_else_statement->nested_conditionals), prerequisites {'if_statement': ['boolean_expression', 'control_flow'], 'boolean_expression': ['comparison_operators'], 'comparison_operators': ['expression'], 'nested_conditionals': ['if_else_statement', 'if_statement'], 'if_else_statement': ['if_statement'], 'dangling_else': ['nested_conditionals'], 'control_flow': ['statement'], 'println': ['statement', 'string_literal']}
- comparison_operators: L3 via relation_to_neighbour "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either"
- control_flow: L2 via line_by_line_trace "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either"
- dangling_else: L0 via misconception "Nothing; The else lines up with if; x > 0; and thats true; so the else is skipped"
- if_else_statement: L2 via line_by_line_trace "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either"
- if_statement: L3 via relation_to_neighbour "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either"
- nested_conditionals: L0 via inconsistent_trace "The else lines up with if; so the else is skipped"

**Stop:** sufficient at depth 4; prompts {'prune': 20, 'label': 41}, fresh model calls 0, cache hits 61

### Held misconceptions
| concept | misconception | kind | quote | score | shares_evidence_with |
|---|---|---|---|---|---|
| dangling_else | ElseMatchesIndentation | misconception | Nothing; The else lines up with if; x > 0; and thats true; so the else is skipped | 0.93 |  |

### Shadowed labels (held in the reading, folded into the label they shadow; not faults of their own)
| concept | misconception | shadow_of | quote | score |
|---|---|---|---|---|
| nested_conditionals | ElseMatchesIndentation | mis:dangling_else->ElseMatchesIndentation | The else lines up with if; x > 0; and thats true; so the else is skipped | 0.651 |

### Broken concept edges
| edge | quote | score | consequence_of |
|---|---|---|---|
| pre:nested_conditionals->dangling_else | The else lines up with if; so the else is skipped; so big isnt printed either | 0.8 | mis:dangling_else->ElseMatchesIndentation |
| pre:if_else_statement->nested_conditionals | Nothing; The else lines up with if; so the else is skipped | 0.51 | mis:dangling_else->ElseMatchesIndentation |

### Root cause: dangling_else / ElseMatchesIndentation

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| comparison_operators | L3 | relation_to_neighbour |  | level_way | x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |  | L2 output_prediction, L2 line_by_line_trace |  |
| control_flow | L2 | line_by_line_trace |  | level_way | x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |  | L2 output_prediction |  |
| dangling_else | L0 | misconception | ElseMatchesIndentation | level_mis_links | Nothing; The else lines up with if; x > 0; and thats true; so the else is skipped | wrong rule: The else belongs to the if it is lined up with. Right rule: The else belongs to the most recent unmatched if, whatever the indentation. |  |  |
| if_else_statement | L2 | line_by_line_trace |  | level_way | x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |  | L2 output_prediction |  |
| if_statement | L3 | relation_to_neighbour |  | level_way | x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |  | L2 line_by_line_trace |  |
| nested_conditionals | L0 | inconsistent_trace |  | level_way | The else lines up with if; so the else is skipped |  | L0 everyday_reading |  |

### Overall level: L0

Clause coverage (final):
| clause | covered by |
|---|---|
| Nothing | lvl:control_flow@L2#1 |
| The else lines up with if | mis:dangling_else->ElseMatchesIndentation |
| x > 0 | mis:comparison_operators->LessGreaterSwapped |
| and thats true | mis:comparison_operators->LessGreaterSwapped |
| so the else is skipped | lvl:comparison_operators@L3#1 |
| x > 10 is false | mis:comparison_operators->LessGreaterSwapped |
| so big isnt printed either | lvl:comparison_operators@L3#1 |

Figure 8 (final picture): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY34_figure08.png

## 5. Every labelled edge (the evidence list, kept or not)
| depth | source | edge | kind | label | prune_score | confidence | score | clauses | quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | comparison_operators | mis:comparison_operators->LessGreaterSwapped | misconception | correct | 0.8 | 0.85 | 0.68 | [3, 4, 6] | x > 0; and thats true; x > 10 is false |
| 1 | comparison_operators | lvl:comparison_operators@L2#1 | level | shown | 0.4 | 0.8 | 0.32 | [3, 4, 6] | x > 0; and thats true; x > 10 is false |
| 1 | comparison_operators | lvl:comparison_operators@L3#1 | level | shown | 0.35 | 0.7 | 0.245 | [3, 4, 5, 6, 7] | x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |
| 1 | comparison_operators | lvl:comparison_operators@L2#0 | level | shown | 0.25 | 0.7 | 0.175 | [3, 4, 6] | x > 0; and thats true; x > 10 is false |
| 1 | if_statement | mis:if_statement->BranchChosenByIntent | misconception | correct | 0.3 | 0.55 | 0.165 | [3, 4, 6, 7] | x > 0; and thats true; x > 10 is false; so big isnt printed either |
| 1 | if_statement | mis:if_statement->ThenAlwaysExecutes | misconception | correct | 0.2 | 0.85 | 0.17 | [6, 7] | x > 10 is false; so big isnt printed either |
| 1 | if_statement | lvl:if_statement@L3#1 | level | shown | 0.3 | 0.7 | 0.21 | [3, 4, 5, 6, 7] | x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |
| 1 | if_statement | lvl:if_statement@L2#0 | level | shown | 0.2 | 0.8 | 0.16 | [3, 4, 5, 6, 7] | x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |
| 2 | comparison_operators | pre:comparison_operators->boolean_expression | prerequisite | confirmed | 0.6000000000000001 | 0.8 | 0.48 | [3, 4, 6, 7] | x > 0; and thats true; x > 10 is false; so big isnt printed either |
| 2 | comparison_operators | pre:expression->comparison_operators | prerequisite | confirmed | 0.30000000000000004 | 0.8 | 0.24 | [3, 4, 6] | x > 0; and thats true; x > 10 is false |
| 2 | println | pre:statement->println | prerequisite | confirmed | 0.7 | 0.55 | 0.385 | [7] | so big isnt printed either |
| 2 | if_statement | pre:if_statement->nested_conditionals | prerequisite | confirmed | 0.4 | 0.8 | 0.32 | [3, 4, 6, 7] | x > 0; and thats true; x > 10 is false; so big isnt printed either |
| 2 | if_statement | pre:if_statement->if_else_statement | prerequisite | confirmed | 0.35 | 0.6 | 0.21 | [3, 4, 5] | x > 0; and thats true; so the else is skipped |
| 2 | if_statement | pre:boolean_expression->if_statement | prerequisite | confirmed | 0.25 | 0.8 | 0.2 | [3, 4, 6, 7] | x > 0; and thats true; x > 10 is false; so big isnt printed either |
| 2 | control_flow | mis:control_flow->FalseConditionRestartsProgram | misconception | correct | 0.4 | 0.6 | 0.24 | [6, 7] | x > 10 is false; so big isnt printed either |
| 2 | control_flow | lvl:control_flow@L2#0 | level | shown | 0.45 | 0.8 | 0.36 | [3, 4, 5, 6, 7] | x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |
| 2 | control_flow | lvl:control_flow@L2#1 | level | shown | 0.25 | 0.75 | 0.1875 | [1, 3, 4, 5, 6, 7] | Nothing; x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |
| 2 | dangling_else | mis:dangling_else->ElseMatchesIndentation | misconception | held | 1.0 | 0.93 | 0.93 | [1, 2, 3, 4, 5] | Nothing; The else lines up with if; x > 0; and thats true; so the else is skipped |
| 2 | dangling_else | lvl:dangling_else@L0#0 | level | shown | 0.7 | 0.85 | 0.595 | [2, 3, 4, 5] | The else lines up with if; x > 0; and thats true; so the else is skipped |
| 2 | nested_conditionals | mis:nested_conditionals->ElseMatchesIndentation | misconception | held | 0.7 | 0.93 | 0.651 | [2, 3, 4, 5] | The else lines up with if; x > 0; and thats true; so the else is skipped |
| 2 | nested_conditionals | lvl:nested_conditionals@L0#3 | level | shown | 0.45 | 0.85 | 0.3825 | [2, 5] | The else lines up with if; so the else is skipped |
| 2 | nested_conditionals | lvl:nested_conditionals@L0#0 | level | shown | 0.35 | 0.85 | 0.2975 | [1, 2, 5] | Nothing; The else lines up with if; so the else is skipped |
| 3 | dangling_else | pre:nested_conditionals->dangling_else | prerequisite | broken | 1.0 | 0.8 | 0.8 | [2, 5, 7] | The else lines up with if; so the else is skipped; so big isnt printed either |
| 3 | nested_conditionals | pre:if_else_statement->nested_conditionals | prerequisite | broken | 0.6 | 0.85 | 0.51 | [1, 2, 5] | Nothing; The else lines up with if; so the else is skipped |
| 3 | nested_conditionals | pre:if_statement->nested_conditionals | prerequisite | confirmed | 0.4 | 0.8 | 0.32 | [3, 4, 6, 7] | x > 0; and thats true; x > 10 is false; so big isnt printed either |
| 3 | control_flow | pre:control_flow->if_statement | prerequisite | confirmed | 0.8 | 0.8 | 0.64 | [3, 4, 6, 7] | x > 0; and thats true; x > 10 is false; so big isnt printed either |
| 3 | control_flow | pre:statement->control_flow | prerequisite | confirmed | 0.2 | 0.6 | 0.12 | [3, 4, 6, 7] | x > 0; and thats true; x > 10 is false; so big isnt printed either |
| 4 | if_else_statement | mis:if_else_statement->BranchChosenByIntent | misconception | correct | 0.4 | 0.7 | 0.28 | [3, 4, 5] | x > 0; and thats true; so the else is skipped |
| 4 | if_else_statement | mis:if_else_statement->ElseAlwaysExecutes | misconception | correct | 0.4 | 0.85 | 0.34 | [3, 4, 5] | x > 0; and thats true; so the else is skipped |
| 4 | if_else_statement | mis:if_else_statement->BothBranchesExecute | misconception | correct | 0.2 | 0.75 | 0.15 | [4, 5] | and thats true; so the else is skipped |
| 4 | if_else_statement | lvl:if_else_statement@L2#0 | level | shown | 0.25 | 0.8 | 0.2 | [3, 4, 5, 6, 7] | x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either |
| 4 | if_else_statement | lvl:if_else_statement@L2#1 | level | shown | 0.15 | 0.6 | 0.09 | [3, 4, 5] | x > 0; and thats true; so the else is skipped |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | comparison_operators | mis:comparison_operators->LessGreaterSwapped | misconception | correct | 0.68 | [3, 4, 6] |
| 1 | comparison_operators | lvl:comparison_operators@L2#1 | level | shown | 0.32 | [3, 4, 6] |
| 1 | comparison_operators | lvl:comparison_operators@L3#1 | level | shown | 0.245 | [3, 4, 5, 6, 7] |
| 2 | dangling_else | mis:dangling_else->ElseMatchesIndentation | misconception | held | 0.93 | [1, 2, 3, 4, 5] |
| 2 | nested_conditionals | mis:nested_conditionals->ElseMatchesIndentation | misconception | held | 0.651 | [2, 3, 4, 5] |
| 2 | dangling_else | lvl:dangling_else@L0#0 | level | shown | 0.595 | [2, 3, 4, 5] |
| 3 | dangling_else | pre:nested_conditionals->dangling_else | prerequisite | broken | 0.8 | [2, 5, 7] |
| 3 | nested_conditionals | pre:if_else_statement->nested_conditionals | prerequisite | broken | 0.51 | [1, 2, 5] |
| 3 | control_flow | pre:control_flow->if_statement | prerequisite | confirmed | 0.64 | [3, 4, 6, 7] |
| 4 | if_else_statement | mis:if_else_statement->ElseAlwaysExecutes | misconception | correct | 0.34 | [3, 4, 5] |
| 4 | if_else_statement | mis:if_else_statement->BranchChosenByIntent | misconception | correct | 0.28 | [3, 4, 5] |
| 4 | if_else_statement | lvl:if_else_statement@L2#0 | level | shown | 0.2 | [3, 4, 5, 6, 7] |

## 7. Raw traversal log
```
clauses: Nothing | The else lines up with if | x > 0 | and thats true | so the else is skipped | x > 10 is false | so big isnt printed either
start: generic concepts whose tagging text occurs in the answer: expression
start: BM25 of the answer against each tagged concept: comparison_operators 15.12 (hits 1), println 14.44 (hits 1), if_statement 13.10 (hits 1), boolean_expression 12.75 (hits 1), control_flow 11.94 (hits 1), nested_conditionals 11.56 (hits 1), if_else_statement 11.37 (hits 1), expression 8.80 (hits 2), dangling_else 6.81 (hits 1), fencepost_loop 1.89 (hits 1)
start: chosen comparison_operators, println, if_statement
start concepts (3): comparison_operators, println, if_statement
--- depth 1: current concepts ['comparison_operators', 'println', 'if_statement']
  comparison_operators (misconceptions): 8 candidates -> kept mis:comparison_operators->LessGreaterSwapped (0.80), mis:comparison_operators->ChainedComparison (0.10), mis:comparison_operators->ComparisonWithBooleanLiteral (0.10)
    mis:comparison_operators->LessGreaterSwapped -> correct (0.68) "x > 0; and thats true; x > 10 is false"
    mis:comparison_operators->ChainedComparison -> not applied (0.00) ""
    mis:comparison_operators->ComparisonWithBooleanLiteral -> not applied (0.00) ""
  comparison_operators (level ways): 20 candidates -> kept lvl:comparison_operators@L2#1 (0.40), lvl:comparison_operators@L3#1 (0.35), lvl:comparison_operators@L2#0 (0.25)
    lvl:comparison_operators@L2#1 -> shown (0.32) "x > 0; and thats true; x > 10 is false"
    lvl:comparison_operators@L3#1 -> shown (0.24) "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either"
    lvl:comparison_operators@L2#0 -> shown (0.17) "x > 0; and thats true; x > 10 is false"
  println (misconceptions): 6 candidates -> kept mis:println->PrintedTextIsExecuted (0.60), mis:println->PrintEqualsPrintln (0.20), mis:println->PrintNewLineFirst (0.20)
    mis:println->PrintedTextIsExecuted -> not applied (0.00) ""
    mis:println->PrintEqualsPrintln -> not applied (0.00) ""
    mis:println->PrintNewLineFirst -> not applied (0.00) ""
  println (level ways): 17 candidates -> kept lvl:println@L3#0 (0.45), lvl:println@L2#1 (0.35), lvl:println@L2#0 (0.20)
    lvl:println@L3#0 -> not applied (0.00) ""
    lvl:println@L2#1 -> not applied (0.00) ""
    lvl:println@L2#0 -> not applied (0.00) ""
  if_statement (misconceptions): 22 candidates -> kept err:if_statement->BracelessMultiStatementBody (0.50), mis:if_statement->BranchChosenByIntent (0.30), mis:if_statement->ThenAlwaysExecutes (0.20)
    err:if_statement->BracelessMultiStatementBody -> not applied (0.00) ""
    mis:if_statement->BranchChosenByIntent -> correct (0.17) "x > 0; and thats true; x > 10 is false; so big isnt printed either"
    mis:if_statement->ThenAlwaysExecutes -> correct (0.17) "x > 10 is false; so big isnt printed either"
  if_statement (level ways): 19 candidates -> kept lvl:if_statement@L4#4 (0.50), lvl:if_statement@L3#1 (0.30), lvl:if_statement@L2#0 (0.20)
    lvl:if_statement@L4#4 -> not applied (0.00) ""
    lvl:if_statement@L3#1 -> shown (0.21) "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either"
    lvl:if_statement@L2#0 -> shown (0.16) "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either"
  kept: mis:comparison_operators->LessGreaterSwapped [correct, tier 2, 0.68], lvl:comparison_operators@L2#1 [shown, tier 2, 0.32], lvl:comparison_operators@L3#1 [shown, tier 2, 0.24]
  clause coverage: c1 uncovered; c2 uncovered; c3 <- mis:comparison_operators->LessGreaterSwapped; c4 <- mis:comparison_operators->LessGreaterSwapped; c5 uncovered; c6 <- mis:comparison_operators->LessGreaterSwapped; c7 <- mis:if_statement->BranchChosenByIntent
  uncovered clauses bring in: control_flow (5.84), dangling_else (4.86), nested_conditionals (4.69)
  not yet read: own edges of control_flow, own edges of dangling_else, own edges of nested_conditionals, par:assignment~comparison_operators, pre:boolean_expression->if_statement, pre:comparison_operators->boolean_expression, pre:control_flow->if_statement, pre:expression->comparison_operators, pre:if_statement->if_else_statement, pre:if_statement->nested_conditionals, pre:statement->println, pre:string_literal->println
--- depth 2: current concepts ['comparison_operators', 'println', 'if_statement', 'control_flow', 'dangling_else', 'nested_conditionals']
  comparison_operators (concept edges): 3 candidates -> kept pre:comparison_operators->boolean_expression (0.60), pre:expression->comparison_operators (0.30), par:assignment~comparison_operators (0.10)
    pre:comparison_operators->boolean_expression -> confirmed (0.48) "x > 0; and thats true; x > 10 is false; so big isnt printed either"
    pre:expression->comparison_operators -> confirmed (0.24) "x > 0; and thats true; x > 10 is false"
    par:assignment~comparison_operators -> not applied (0.00) ""
  println (concept edges): 2 candidates -> kept pre:statement->println (0.70), pre:string_literal->println (0.30)
    pre:statement->println -> confirmed (0.39) "so big isnt printed either"
    pre:string_literal->println -> not applied (0.00) ""
  if_statement (concept edges): 4 candidates -> kept pre:if_statement->nested_conditionals (0.40), pre:if_statement->if_else_statement (0.35), pre:boolean_expression->if_statement (0.25)
    pre:if_statement->nested_conditionals -> confirmed (0.32) "x > 0; and thats true; x > 10 is false; so big isnt printed either"
    pre:if_statement->if_else_statement -> confirmed (0.21) "x > 0; and thats true; so the else is skipped"
    pre:boolean_expression->if_statement -> confirmed (0.20) "x > 0; and thats true; x > 10 is false; so big isnt printed either"
  control_flow (misconceptions): 11 candidates -> kept mis:control_flow->FalseConditionRestartsProgram (0.40), mis:control_flow->IfConditionWatched (0.30), mis:control_flow->StatementsRunInAnyOrder (0.30)
    mis:control_flow->FalseConditionRestartsProgram -> correct (0.24) "x > 10 is false; so big isnt printed either"
    mis:control_flow->IfConditionWatched -> not applied (0.00) ""
    mis:control_flow->StatementsRunInAnyOrder -> not applied (0.00) ""
  control_flow (level ways): 15 candidates -> kept lvl:control_flow@L2#0 (0.45), lvl:control_flow@L0#0 (0.30), lvl:control_flow@L2#1 (0.25)
    lvl:control_flow@L2#0 -> shown (0.36) "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either"
    lvl:control_flow@L0#0 -> not applied (0.00) ""
    lvl:control_flow@L2#1 -> shown (0.19) "Nothing; x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either"
  dangling_else (misconceptions): 1 candidates -> kept mis:dangling_else->ElseMatchesIndentation (1.00)
    mis:dangling_else->ElseMatchesIndentation -> held (0.93) "Nothing; The else lines up with if; x > 0; and thats true; so the else is skipped"
  dangling_else (level ways): 12 candidates -> kept lvl:dangling_else@L0#0 (0.70), lvl:dangling_else@L2#1 (0.15), lvl:dangling_else@L4#2 (0.15)
    lvl:dangling_else@L0#0 -> shown (0.59) "The else lines up with if; x > 0; and thats true; so the else is skipped"
    lvl:dangling_else@L2#1 -> not applied (0.00) ""
    lvl:dangling_else@L4#2 -> not applied (0.00) ""
  nested_conditionals (misconceptions): 6 candidates -> kept mis:nested_conditionals->ElseMatchesIndentation (0.70), mis:nested_conditionals->InconsistentIndentation (0.15), mis:nested_conditionals->InnerIfIgnoresOuter (0.15)
    mis:nested_conditionals->ElseMatchesIndentation -> held (0.65) "The else lines up with if; x > 0; and thats true; so the else is skipped"
    mis:nested_conditionals->InconsistentIndentation -> not applied (0.00) ""
    mis:nested_conditionals->InnerIfIgnoresOuter -> not applied (0.00) ""
  nested_conditionals (level ways): 14 candidates -> kept lvl:nested_conditionals@L0#3 (0.45), lvl:nested_conditionals@L0#0 (0.35), lvl:nested_conditionals@L4#2 (0.20)
    lvl:nested_conditionals@L0#3 -> shown (0.38) "The else lines up with if; so the else is skipped"
    lvl:nested_conditionals@L0#0 -> shown (0.30) "Nothing; The else lines up with if; so the else is skipped"
    lvl:nested_conditionals@L4#2 -> not applied (0.00) ""
  kept: mis:dangling_else->ElseMatchesIndentation [held, tier 0, 0.93], mis:nested_conditionals->ElseMatchesIndentation [held, tier 0, 0.65], lvl:dangling_else@L0#0 [shown, tier 2, 0.59]
  clause coverage: c1 <- mis:dangling_else->ElseMatchesIndentation; c2 <- mis:dangling_else->ElseMatchesIndentation; c3 <- mis:comparison_operators->LessGreaterSwapped; c4 <- mis:comparison_operators->LessGreaterSwapped; c5 <- pre:if_statement->if_else_statement; c6 <- mis:comparison_operators->LessGreaterSwapped; c7 <- mis:if_statement->BranchChosenByIntent
  not yet read: pre:if_else_statement->nested_conditionals, pre:nested_conditionals->dangling_else, pre:statement->control_flow
--- depth 3: current concepts ['dangling_else', 'nested_conditionals', 'control_flow']
  dangling_else (concept edges): 1 candidates -> kept pre:nested_conditionals->dangling_else (1.00)
    pre:nested_conditionals->dangling_else -> broken (0.80) "The else lines up with if; so the else is skipped; so big isnt printed either"
  nested_conditionals (concept edges): 2 candidates -> kept pre:if_else_statement->nested_conditionals (0.60), pre:if_statement->nested_conditionals (0.40)
    pre:if_else_statement->nested_conditionals -> broken (0.51) "Nothing; The else lines up with if; so the else is skipped"
    pre:if_statement->nested_conditionals -> confirmed (0.32) "x > 0; and thats true; x > 10 is false; so big isnt printed either"
  control_flow (concept edges): 2 candidates -> kept pre:control_flow->if_statement (0.80), pre:statement->control_flow (0.20)
    pre:control_flow->if_statement -> confirmed (0.64) "x > 0; and thats true; x > 10 is false; so big isnt printed either"
    pre:statement->control_flow -> confirmed (0.12) "x > 0; and thats true; x > 10 is false; so big isnt printed either"
  kept: pre:nested_conditionals->dangling_else [broken, tier 0, 0.80], pre:if_else_statement->nested_conditionals [broken, tier 0, 0.51], pre:control_flow->if_statement [confirmed, tier 2, 0.64]
  reached across pre:if_else_statement->nested_conditionals, entered next: if_else_statement
  clause coverage: c1 <- mis:dangling_else->ElseMatchesIndentation; c2 <- mis:dangling_else->ElseMatchesIndentation; c3 <- mis:comparison_operators->LessGreaterSwapped; c4 <- mis:comparison_operators->LessGreaterSwapped; c5 <- pre:if_statement->if_else_statement; c6 <- mis:comparison_operators->LessGreaterSwapped; c7 <- mis:if_statement->BranchChosenByIntent
  not yet read: own edges of if_else_statement
--- depth 4: current concepts ['if_else_statement'] (closing round: own edges only)
  if_else_statement (misconceptions): 6 candidates -> kept mis:if_else_statement->BranchChosenByIntent (0.40), mis:if_else_statement->ElseAlwaysExecutes (0.40), mis:if_else_statement->BothBranchesExecute (0.20)
    mis:if_else_statement->BranchChosenByIntent -> correct (0.28) "x > 0; and thats true; so the else is skipped"
    mis:if_else_statement->ElseAlwaysExecutes -> correct (0.34) "x > 0; and thats true; so the else is skipped"
    mis:if_else_statement->BothBranchesExecute -> correct (0.15) "and thats true; so the else is skipped"
  if_else_statement (level ways): 17 candidates -> kept lvl:if_else_statement@L3#1 (0.60), lvl:if_else_statement@L2#0 (0.25), lvl:if_else_statement@L2#1 (0.15)
    lvl:if_else_statement@L3#1 -> not applied (0.00) ""
    lvl:if_else_statement@L2#0 -> shown (0.20) "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either"
    lvl:if_else_statement@L2#1 -> shown (0.09) "x > 0; and thats true; so the else is skipped"
  kept: mis:if_else_statement->ElseAlwaysExecutes [correct, tier 2, 0.34], mis:if_else_statement->BranchChosenByIntent [correct, tier 2, 0.28], lvl:if_else_statement@L2#0 [shown, tier 2, 0.20]
  clause coverage: c1 <- mis:dangling_else->ElseMatchesIndentation; c2 <- mis:dangling_else->ElseMatchesIndentation; c3 <- mis:comparison_operators->LessGreaterSwapped; c4 <- mis:comparison_operators->LessGreaterSwapped; c5 <- pre:if_statement->if_else_statement; c6 <- mis:comparison_operators->LessGreaterSwapped; c7 <- mis:if_statement->BranchChosenByIntent
  held: mis:dangling_else->ElseMatchesIndentation; filed at the dependent concept: mis:nested_conditionals->ElseMatchesIndentation
  shadows: mis:nested_conditionals->ElseMatchesIndentation (shadow of mis:dangling_else->ElseMatchesIndentation)
  root-cause walk: held on ['dangling_else'], broken at [] (consequences: pre:nested_conditionals->dangling_else, pre:if_else_statement->nested_conditionals), prerequisites {'if_statement': ['boolean_expression', 'control_flow'], 'boolean_expression': ['comparison_operators'], 'comparison_operators': ['expression'], 'nested_conditionals': ['if_else_statement', 'if_statement'], 'if_else_statement': ['if_statement'], 'dangling_else': ['nested_conditionals'], 'control_flow': ['statement'], 'println': ['statement', 'string_literal']}
  level comparison_operators: L3 via relation_to_neighbour "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either"
  level control_flow: L2 via line_by_line_trace "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either"
  level dangling_else: L0 via misconception "Nothing; The else lines up with if; x > 0; and thats true; so the else is skipped"
  level if_else_statement: L2 via line_by_line_trace "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either"
  level if_statement: L3 via relation_to_neighbour "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either"
  level nested_conditionals: L0 via inconsistent_trace "The else lines up with if; so the else is skipped"
```

## 8. Full diagnosis JSON
```json
{
 "scenario": "MY34",
 "settings": {
  "width": 3,
  "depth": 3,
  "prune_tools": "llm",
  "model": "claude-opus-5-5",
  "backend": "claude-cli"
 },
 "clauses": [
  "Nothing",
  "The else lines up with if",
  "x > 0",
  "and thats true",
  "so the else is skipped",
  "x > 10 is false",
  "so big isnt printed either"
 ],
 "start_concepts": [
  "comparison_operators",
  "println",
  "if_statement"
 ],
 "held_misconceptions": [
  {
   "concept": "dangling_else",
   "misconception": "ElseMatchesIndentation",
   "kind": "misconception",
   "quote": "Nothing; The else lines up with if; x > 0; and thats true; so the else is skipped",
   "score": 0.93
  }
 ],
 "error_evidence": [],
 "shadowed": [
  {
   "concept": "nested_conditionals",
   "misconception": "ElseMatchesIndentation",
   "shadow_of": "mis:dangling_else->ElseMatchesIndentation",
   "quote": "The else lines up with if; x > 0; and thats true; so the else is skipped",
   "score": 0.651
  }
 ],
 "broken_edges": [
  {
   "edge": "pre:nested_conditionals->dangling_else",
   "quote": "The else lines up with if; so the else is skipped; so big isnt printed either",
   "score": 0.8,
   "consequence_of": "mis:dangling_else->ElseMatchesIndentation"
  },
  {
   "edge": "pre:if_else_statement->nested_conditionals",
   "quote": "Nothing; The else lines up with if; so the else is skipped",
   "score": 0.51,
   "consequence_of": "mis:dangling_else->ElseMatchesIndentation"
  }
 ],
 "root_cause": {
  "concept": "dangling_else",
  "misconception": "ElseMatchesIndentation"
 },
 "levels": {
  "comparison_operators": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either",
   "edge": "lvl:comparison_operators@L3#1",
   "source": "level_way",
   "also_shown": [
    "L2 output_prediction",
    "L2 line_by_line_trace"
   ]
  },
  "control_flow": {
   "level": "L2",
   "way": "line_by_line_trace",
   "quote": "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either",
   "edge": "lvl:control_flow@L2#0",
   "source": "level_way",
   "also_shown": [
    "L2 output_prediction"
   ]
  },
  "dangling_else": {
   "level": "L0",
   "way": "misconception",
   "misconception": "ElseMatchesIndentation",
   "quote": "Nothing; The else lines up with if; x > 0; and thats true; so the else is skipped",
   "edge": "mis:dangling_else->ElseMatchesIndentation",
   "rule": "wrong rule: The else belongs to the if it is lined up with. Right rule: The else belongs to the most recent unmatched if, whatever the indentation.",
   "source": "level_mis_links"
  },
  "if_else_statement": {
   "level": "L2",
   "way": "line_by_line_trace",
   "quote": "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either",
   "edge": "lvl:if_else_statement@L2#0",
   "source": "level_way",
   "also_shown": [
    "L2 output_prediction"
   ]
  },
  "if_statement": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either",
   "edge": "lvl:if_statement@L3#1",
   "source": "level_way",
   "also_shown": [
    "L2 line_by_line_trace"
   ]
  },
  "nested_conditionals": {
   "level": "L0",
   "way": "inconsistent_trace",
   "quote": "The else lines up with if; so the else is skipped",
   "edge": "lvl:nested_conditionals@L0#3",
   "source": "level_way",
   "also_shown": [
    "L0 everyday_reading"
   ]
  }
 },
 "overall_level": "L0",
 "paths": [
  {
   "depth": 1,
   "source": "comparison_operators",
   "edge": "mis:comparison_operators->LessGreaterSwapped",
   "target": "LessGreaterSwapped",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3,
    4,
    6
   ],
   "quote": "x > 0; and thats true; x > 10 is false",
   "confidence": 0.85,
   "prune_score": 0.8,
   "score": 0.68,
   "logic": "< and > mean the same thing (or a < b means a is greater than b).",
   "twin_logic": "a < b is true when a is smaller than b; a > b when a is larger.",
   "role": "primary"
  },
  {
   "depth": 1,
   "source": "comparison_operators",
   "edge": "lvl:comparison_operators@L2#1",
   "target": "comparison_operators@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4,
    6
   ],
   "quote": "x > 0; and thats true; x > 10 is false",
   "confidence": 0.8,
   "prune_score": 0.4,
   "score": 0.32,
   "logic": "The result is a boolean: (2 <= 2) is true, 2 < 2 is false, (x < 3.1) is true for int x = 3; any comparison involving NaN, even NaN == NaN, is false.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "comparison_operators",
   "edge": "lvl:comparison_operators@L3#1",
   "target": "comparison_operators@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4,
    5,
    6,
    7
   ],
   "quote": "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either",
   "confidence": 0.7,
   "prune_score": 0.35,
   "score": 0.245,
   "logic": "Comparisons are the building blocks of conditions: together with boolean logic they provide the basis for decision-making.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 2,
   "source": "dangling_else",
   "edge": "mis:dangling_else->ElseMatchesIndentation",
   "target": "ElseMatchesIndentation",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3,
    4,
    5
   ],
   "quote": "Nothing; The else lines up with if; x > 0; and thats true; so the else is skipped",
   "confidence": 0.93,
   "prune_score": 1.0,
   "score": 0.93,
   "logic": "The else belongs to the if it is lined up with.",
   "twin_logic": "The else belongs to the most recent unmatched if, whatever the indentation.",
   "role": "primary"
  },
  {
   "depth": 2,
   "source": "nested_conditionals",
   "edge": "mis:nested_conditionals->ElseMatchesIndentation",
   "target": "ElseMatchesIndentation",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2,
    3,
    4,
    5
   ],
   "quote": "The else lines up with if; x > 0; and thats true; so the else is skipped",
   "confidence": 0.93,
   "prune_score": 0.7,
   "score": 0.651,
   "logic": "The else belongs to the if it is lined up with.",
   "twin_logic": "The else belongs to the most recent unmatched if, whatever the indentation.",
   "role": "context"
  },
  {
   "depth": 2,
   "source": "dangling_else",
   "edge": "lvl:dangling_else@L0#0",
   "target": "dangling_else@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3,
    4,
    5
   ],
   "quote": "The else lines up with if; x > 0; and thats true; so the else is skipped",
   "confidence": 0.85,
   "prune_score": 0.7,
   "score": 0.595,
   "logic": "Folk meaning: on paper the layout shows which 'if' an 'otherwise' answers, so an else lined up with the outer if is read as belonging to it. Java ignores indentation and attaches each else to the innermost if to which it might possibly belong.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 3,
   "source": "dangling_else",
   "edge": "pre:nested_conditionals->dangling_else",
   "target": "nested_conditionals",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    2,
    5,
    7
   ],
   "quote": "The else lines up with if; so the else is skipped; so big isnt printed either",
   "confidence": 0.8,
   "prune_score": 1.0,
   "score": 0.8,
   "logic": "The dangling else arises when ifs are nested without braces.",
   "twin_logic": null,
   "consequence_of": "mis:dangling_else->ElseMatchesIndentation"
  },
  {
   "depth": 3,
   "source": "nested_conditionals",
   "edge": "pre:if_else_statement->nested_conditionals",
   "target": "if_else_statement",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    2,
    5
   ],
   "quote": "Nothing; The else lines up with if; so the else is skipped",
   "confidence": 0.85,
   "prune_score": 0.6,
   "score": 0.51,
   "logic": "Nesting puts an if or if-else inside a branch of another if-else; an else-if chain is the common case where the else branch is itself an if.",
   "twin_logic": null,
   "consequence_of": "mis:dangling_else->ElseMatchesIndentation"
  },
  {
   "depth": 3,
   "source": "control_flow",
   "edge": "pre:control_flow->if_statement",
   "target": "if_statement",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    4,
    6,
    7
   ],
   "quote": "x > 0; and thats true; x > 10 is false; so big isnt printed either",
   "confidence": 0.8,
   "prune_score": 0.8,
   "score": 0.64,
   "logic": "An if changes the default top-to-bottom flow by running a block only when its condition is true.",
   "twin_logic": null
  },
  {
   "depth": 4,
   "source": "if_else_statement",
   "edge": "mis:if_else_statement->ElseAlwaysExecutes",
   "target": "ElseAlwaysExecutes",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3,
    4,
    5
   ],
   "quote": "x > 0; and thats true; so the else is skipped",
   "confidence": 0.85,
   "prune_score": 0.4,
   "score": 0.34,
   "logic": "The else branch of an if-else statement always executes.",
   "twin_logic": "The else branch runs only when the if condition is false.",
   "role": "primary"
  },
  {
   "depth": 4,
   "source": "if_else_statement",
   "edge": "mis:if_else_statement->BranchChosenByIntent",
   "target": "BranchChosenByIntent",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3,
    4,
    5
   ],
   "quote": "x > 0; and thats true; so the else is skipped",
   "confidence": 0.7,
   "prune_score": 0.4,
   "score": 0.28,
   "logic": "Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true.",
   "twin_logic": "The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs.",
   "role": "context"
  },
  {
   "depth": 4,
   "source": "if_else_statement",
   "edge": "lvl:if_else_statement@L2#0",
   "target": "if_else_statement@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4,
    5,
    6,
    7
   ],
   "quote": "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either",
   "confidence": 0.8,
   "prune_score": 0.25,
   "score": 0.2,
   "logic": "Evaluate the condition once; if true execute the then branch, otherwise execute the else branch; then continue with the statement after the whole if-else (the condition is not re-tested).",
   "twin_logic": null,
   "level": "L2",
   "way": "line_by_line_trace"
  }
 ],
 "evidence": [
  {
   "depth": 1,
   "source": "comparison_operators",
   "edge": "mis:comparison_operators->LessGreaterSwapped",
   "target": "LessGreaterSwapped",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3,
    4,
    6
   ],
   "quote": "x > 0; and thats true; x > 10 is false",
   "confidence": 0.85,
   "prune_score": 0.8,
   "score": 0.68,
   "logic": "< and > mean the same thing (or a < b means a is greater than b).",
   "twin_logic": "a < b is true when a is smaller than b; a > b when a is larger.",
   "role": "primary"
  },
  {
   "depth": 1,
   "source": "comparison_operators",
   "edge": "lvl:comparison_operators@L2#1",
   "target": "comparison_operators@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4,
    6
   ],
   "quote": "x > 0; and thats true; x > 10 is false",
   "confidence": 0.8,
   "prune_score": 0.4,
   "score": 0.32,
   "logic": "The result is a boolean: (2 <= 2) is true, 2 < 2 is false, (x < 3.1) is true for int x = 3; any comparison involving NaN, even NaN == NaN, is false.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "comparison_operators",
   "edge": "lvl:comparison_operators@L3#1",
   "target": "comparison_operators@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4,
    5,
    6,
    7
   ],
   "quote": "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either",
   "confidence": 0.7,
   "prune_score": 0.35,
   "score": 0.245,
   "logic": "Comparisons are the building blocks of conditions: together with boolean logic they provide the basis for decision-making.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 1,
   "source": "comparison_operators",
   "edge": "lvl:comparison_operators@L2#0",
   "target": "comparison_operators@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4,
    6
   ],
   "quote": "x > 0; and thats true; x > 10 is false",
   "confidence": 0.7,
   "prune_score": 0.25,
   "score": 0.175,
   "logic": "Evaluate the left operand (including its arithmetic), then the right operand; if their types differ, promote the narrower one (int to double); then compare and produce true or false.",
   "twin_logic": null,
   "level": "L2",
   "way": "line_by_line_trace"
  },
  {
   "depth": 1,
   "source": "if_statement",
   "edge": "mis:if_statement->BranchChosenByIntent",
   "target": "BranchChosenByIntent",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3,
    4,
    6,
    7
   ],
   "quote": "x > 0; and thats true; x > 10 is false; so big isnt printed either",
   "confidence": 0.55,
   "prune_score": 0.3,
   "score": 0.165,
   "logic": "Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true.",
   "twin_logic": "The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs.",
   "role": "primary"
  },
  {
   "depth": 1,
   "source": "if_statement",
   "edge": "mis:if_statement->ThenAlwaysExecutes",
   "target": "ThenAlwaysExecutes",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    6,
    7
   ],
   "quote": "x > 10 is false; so big isnt printed either",
   "confidence": 0.85,
   "prune_score": 0.2,
   "score": 0.17,
   "logic": "The then branch always runs.",
   "twin_logic": "The then branch runs only when the condition is true.",
   "role": "primary"
  },
  {
   "depth": 1,
   "source": "if_statement",
   "edge": "lvl:if_statement@L3#1",
   "target": "if_statement@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4,
    5,
    6,
    7
   ],
   "quote": "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either",
   "confidence": 0.7,
   "prune_score": 0.3,
   "score": 0.21,
   "logic": "if-else extends if with a second branch that runs exactly when the condition is false; a lone if has an implicit empty else-case.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 1,
   "source": "if_statement",
   "edge": "lvl:if_statement@L2#0",
   "target": "if_statement@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4,
    5,
    6,
    7
   ],
   "quote": "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either",
   "confidence": 0.8,
   "prune_score": 0.2,
   "score": 0.16,
   "logic": "Evaluate the condition once; if true, execute the body; then, in either case, continue with the statement after the if.",
   "twin_logic": null,
   "level": "L2",
   "way": "line_by_line_trace"
  },
  {
   "depth": 2,
   "source": "comparison_operators",
   "edge": "pre:comparison_operators->boolean_expression",
   "target": "boolean_expression",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    4,
    6,
    7
   ],
   "quote": "x > 0; and thats true; x > 10 is false; so big isnt printed either",
   "confidence": 0.8,
   "prune_score": 0.6000000000000001,
   "score": 0.48,
   "logic": "A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "comparison_operators",
   "edge": "pre:expression->comparison_operators",
   "target": "expression",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    4,
    6
   ],
   "quote": "x > 0; and thats true; x > 10 is false",
   "confidence": 0.8,
   "prune_score": 0.30000000000000004,
   "score": 0.24,
   "logic": "Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "println",
   "edge": "pre:statement->println",
   "target": "statement",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    7
   ],
   "quote": "so big isnt printed either",
   "confidence": 0.55,
   "prune_score": 0.7,
   "score": 0.385,
   "logic": "System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "if_statement",
   "edge": "pre:if_statement->nested_conditionals",
   "target": "nested_conditionals",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    4,
    6,
    7
   ],
   "quote": "x > 0; and thats true; x > 10 is false; so big isnt printed either",
   "confidence": 0.8,
   "prune_score": 0.4,
   "score": 0.32,
   "logic": "An if statement can sit inside the body of another if; the inner one is tested only when the outer condition is true.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "if_statement",
   "edge": "pre:if_statement->if_else_statement",
   "target": "if_else_statement",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    4,
    5
   ],
   "quote": "x > 0; and thats true; so the else is skipped",
   "confidence": 0.6,
   "prune_score": 0.35,
   "score": 0.21,
   "logic": "if-else extends if with a second block that runs exactly when the condition is false.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "if_statement",
   "edge": "pre:boolean_expression->if_statement",
   "target": "boolean_expression",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    4,
    6,
    7
   ],
   "quote": "x > 0; and thats true; x > 10 is false; so big isnt printed either",
   "confidence": 0.8,
   "prune_score": 0.25,
   "score": 0.2,
   "logic": "An if runs its block only when its boolean expression evaluates to true.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "control_flow",
   "edge": "mis:control_flow->FalseConditionRestartsProgram",
   "target": "FalseConditionRestartsProgram",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    6,
    7
   ],
   "quote": "x > 10 is false; so big isnt printed either",
   "confidence": 0.6,
   "prune_score": 0.4,
   "score": 0.24,
   "logic": "When an if condition is false (and there is no else), control jumps back to the start of the program.",
   "twin_logic": "A false condition skips the then branch and execution continues with the statement after the if statement.",
   "role": "context"
  },
  {
   "depth": 2,
   "source": "control_flow",
   "edge": "lvl:control_flow@L2#0",
   "target": "control_flow@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4,
    5,
    6,
    7
   ],
   "quote": "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either",
   "confidence": 0.8,
   "prune_score": 0.45,
   "score": 0.36,
   "logic": "Execute the statement at the current point; when it completes normally, control passes to the next statement in the block. An if evaluates its condition once and then runs at most one branch; a loop evaluates its condition before each pass; after an if or a loop finishes, control continues with the statement after it.",
   "twin_logic": null,
   "level": "L2",
   "way": "line_by_line_trace"
  },
  {
   "depth": 2,
   "source": "control_flow",
   "edge": "lvl:control_flow@L2#1",
   "target": "control_flow@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    3,
    4,
    5,
    6,
    7
   ],
   "quote": "Nothing; x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either",
   "confidence": 0.75,
   "prune_score": 0.25,
   "score": 0.1875,
   "logic": "The output is the sequence of print statements that control actually reaches, in the order reached: e.g. TenHellos prints 1st, 2nd, 3rd Hello once each, then 4th to 10th Hello from the loop.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 2,
   "source": "dangling_else",
   "edge": "mis:dangling_else->ElseMatchesIndentation",
   "target": "ElseMatchesIndentation",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3,
    4,
    5
   ],
   "quote": "Nothing; The else lines up with if; x > 0; and thats true; so the else is skipped",
   "confidence": 0.93,
   "prune_score": 1.0,
   "score": 0.93,
   "logic": "The else belongs to the if it is lined up with.",
   "twin_logic": "The else belongs to the most recent unmatched if, whatever the indentation.",
   "role": "primary"
  },
  {
   "depth": 2,
   "source": "dangling_else",
   "edge": "lvl:dangling_else@L0#0",
   "target": "dangling_else@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3,
    4,
    5
   ],
   "quote": "The else lines up with if; x > 0; and thats true; so the else is skipped",
   "confidence": 0.85,
   "prune_score": 0.7,
   "score": 0.595,
   "logic": "Folk meaning: on paper the layout shows which 'if' an 'otherwise' answers, so an else lined up with the outer if is read as belonging to it. Java ignores indentation and attaches each else to the innermost if to which it might possibly belong.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 2,
   "source": "nested_conditionals",
   "edge": "mis:nested_conditionals->ElseMatchesIndentation",
   "target": "ElseMatchesIndentation",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2,
    3,
    4,
    5
   ],
   "quote": "The else lines up with if; x > 0; and thats true; so the else is skipped",
   "confidence": 0.93,
   "prune_score": 0.7,
   "score": 0.651,
   "logic": "The else belongs to the if it is lined up with.",
   "twin_logic": "The else belongs to the most recent unmatched if, whatever the indentation.",
   "role": "context"
  },
  {
   "depth": 2,
   "source": "nested_conditionals",
   "edge": "lvl:nested_conditionals@L0#3",
   "target": "nested_conditionals@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    5
   ],
   "quote": "The else lines up with if; so the else is skipped",
   "confidence": 0.85,
   "prune_score": 0.45,
   "score": 0.3825,
   "logic": "Applies the nesting rule (LT) unevenly: on some inputs tests the inner condition even though the outer one was false, or matches an else to the if it is lined up with. (here mixing in: \"An inner if runs its body whenever its own condition is true, even if the outer if condition is false\")",
   "twin_logic": null,
   "level": "L0",
   "way": "inconsistent_trace"
  },
  {
   "depth": 2,
   "source": "nested_conditionals",
   "edge": "lvl:nested_conditionals@L0#0",
   "target": "nested_conditionals@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2,
    5
   ],
   "quote": "Nothing; The else lines up with if; so the else is skipped",
   "confidence": 0.85,
   "prune_score": 0.35,
   "score": 0.2975,
   "logic": "Folk meaning: in prose, indentation and line layout show what belongs to what, and two consecutive 'if' sentences can be heard as one combined condition. The Java compiler ignores indentation: an inner if belongs to the branch that syntactically contains it, and an else pairs with the innermost unmatched if.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 3,
   "source": "dangling_else",
   "edge": "pre:nested_conditionals->dangling_else",
   "target": "nested_conditionals",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    2,
    5,
    7
   ],
   "quote": "The else lines up with if; so the else is skipped; so big isnt printed either",
   "confidence": 0.8,
   "prune_score": 1.0,
   "score": 0.8,
   "logic": "The dangling else arises when ifs are nested without braces.",
   "twin_logic": null,
   "consequence_of": "mis:dangling_else->ElseMatchesIndentation"
  },
  {
   "depth": 3,
   "source": "nested_conditionals",
   "edge": "pre:if_else_statement->nested_conditionals",
   "target": "if_else_statement",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    2,
    5
   ],
   "quote": "Nothing; The else lines up with if; so the else is skipped",
   "confidence": 0.85,
   "prune_score": 0.6,
   "score": 0.51,
   "logic": "Nesting puts an if or if-else inside a branch of another if-else; an else-if chain is the common case where the else branch is itself an if.",
   "twin_logic": null,
   "consequence_of": "mis:dangling_else->ElseMatchesIndentation"
  },
  {
   "depth": 3,
   "source": "nested_conditionals",
   "edge": "pre:if_statement->nested_conditionals",
   "target": "if_statement",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    4,
    6,
    7
   ],
   "quote": "x > 0; and thats true; x > 10 is false; so big isnt printed either",
   "confidence": 0.8,
   "prune_score": 0.4,
   "score": 0.32,
   "logic": "An if statement can sit inside the body of another if; the inner one is tested only when the outer condition is true.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "control_flow",
   "edge": "pre:control_flow->if_statement",
   "target": "if_statement",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    4,
    6,
    7
   ],
   "quote": "x > 0; and thats true; x > 10 is false; so big isnt printed either",
   "confidence": 0.8,
   "prune_score": 0.8,
   "score": 0.64,
   "logic": "An if changes the default top-to-bottom flow by running a block only when its condition is true.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "control_flow",
   "edge": "pre:statement->control_flow",
   "target": "statement",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    4,
    6,
    7
   ],
   "quote": "x > 0; and thats true; x > 10 is false; so big isnt printed either",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "Control flow is the order in which statements run.",
   "twin_logic": null
  },
  {
   "depth": 4,
   "source": "if_else_statement",
   "edge": "mis:if_else_statement->BranchChosenByIntent",
   "target": "BranchChosenByIntent",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3,
    4,
    5
   ],
   "quote": "x > 0; and thats true; so the else is skipped",
   "confidence": 0.7,
   "prune_score": 0.4,
   "score": 0.28,
   "logic": "Which branch runs is decided by what the programmer meant or by code outside the if, not by whether the condition is true.",
   "twin_logic": "The then branch runs exactly when the condition evaluates to true at the moment it is tested; otherwise the else branch (if any) runs.",
   "role": "context"
  },
  {
   "depth": 4,
   "source": "if_else_statement",
   "edge": "mis:if_else_statement->ElseAlwaysExecutes",
   "target": "ElseAlwaysExecutes",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    3,
    4,
    5
   ],
   "quote": "x > 0; and thats true; so the else is skipped",
   "confidence": 0.85,
   "prune_score": 0.4,
   "score": 0.34,
   "logic": "The else branch of an if-else statement always executes.",
   "twin_logic": "The else branch runs only when the if condition is false.",
   "role": "primary"
  },
  {
   "depth": 4,
   "source": "if_else_statement",
   "edge": "mis:if_else_statement->BothBranchesExecute",
   "target": "BothBranchesExecute",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    4,
    5
   ],
   "quote": "and thats true; so the else is skipped",
   "confidence": 0.75,
   "prune_score": 0.2,
   "score": 0.15,
   "logic": "Both the then branch and the else branch run.",
   "twin_logic": "Exactly one of the two branches runs.",
   "role": "primary"
  },
  {
   "depth": 4,
   "source": "if_else_statement",
   "edge": "lvl:if_else_statement@L2#0",
   "target": "if_else_statement@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4,
    5,
    6,
    7
   ],
   "quote": "x > 0; and thats true; so the else is skipped; x > 10 is false; so big isnt printed either",
   "confidence": 0.8,
   "prune_score": 0.25,
   "score": 0.2,
   "logic": "Evaluate the condition once; if true execute the then branch, otherwise execute the else branch; then continue with the statement after the whole if-else (the condition is not re-tested).",
   "twin_logic": null,
   "level": "L2",
   "way": "line_by_line_trace"
  },
  {
   "depth": 4,
   "source": "if_else_statement",
   "edge": "lvl:if_else_statement@L2#1",
   "target": "if_else_statement@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4,
    5
   ],
   "quote": "x > 0; and thats true; so the else is skipped",
   "confidence": 0.6,
   "prune_score": 0.15,
   "score": 0.09,
   "logic": "Exactly one branch's effects occur; e.g. if (x > y) max = x; else max = y; leaves max equal to the larger value, and the coin flip prints either Heads or Tails, never both.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  }
 ],
 "clause_coverage": {
  "Nothing": "lvl:control_flow@L2#1",
  "The else lines up with if": "mis:dangling_else->ElseMatchesIndentation",
  "x > 0": "mis:comparison_operators->LessGreaterSwapped",
  "and thats true": "mis:comparison_operators->LessGreaterSwapped",
  "so the else is skipped": "lvl:comparison_operators@L3#1",
  "x > 10 is false": "mis:comparison_operators->LessGreaterSwapped",
  "so big isnt printed either": "lvl:comparison_operators@L3#1"
 },
 "unexplained_clauses": [],
 "stop_reason": "sufficient",
 "depth_reached": 4,
 "llm_calls": 0,
 "llm_cache_hits": 61,
 "llm_calls_by_step": {
  "prune": 20,
  "label": 41
 }
}
```
