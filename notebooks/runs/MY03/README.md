# Think on the Graph: every output of the run MY03

Files of this scenario: `input.json` (program, question, answer), `diagnosis.json`, `subgraph.json`, `traverse_log.txt`, `report.html` (this report as one full-page file, with the interactive graph `MY03_G.html`), `MY03.ipynb` (this report as a notebook).

## 0. Input
Program:
```java
int[] a = {1, 2, 3};
int[] b = a;
b[0] = 9;
System.out.println(a[0] + " " + b[0]);
```
Question: What does this program print, and why?

Student's answer: It prints 1 9. The line b = a makes b a copy of a, so b is a separate array. Changing b[0] to 9 only changes b, and a[0] is still 1.
Settings: width 3, depth 3, prune llm, backend claude-cli, model claude-opus-5-5
## 1. Stage 1: the subgraph G from the code (no model)
Masked code (string and char literals and comments blanked; this is what the patterns see):
```
int[] a = {1, 2, 3};
int[] b = a;
b[0] = 9;
System.out.println(a[0] + " " + b[0]);
```
Which code text tagged which concept (a generic concept fires on almost any Java line; it starts the walk only if the answer repeats its tag):
| concept | generic | channel | matched text | line |
|---|---|---|---|---|
| array_aliasing | False | pattern | 'int[] b = a;' | 2 |
| array_declaration | False | pattern | 'int[] a' | 1 |
| array_initializer | False | pattern | '= {' | 1 |
| array_reference | False | pattern | 'int[] b = a;' | 2 |
| data_structure | False | pattern | 'int[]' | 1 |
| data_type | True | pattern | 'int' | 1 |
| indexing | False | pattern | 'b[0]' | 3 |
| primitive_type | True | pattern | 'int' | 1 |
| primitive_vs_reference | False | pattern | 'int[] b = a;' | 2 |
| println | False | pattern | 'System.out.println(' | 4 |
| statement | True | pattern | ';' | 1 |
| string_concatenation | False | pattern | '+ " "' | 4 |
| string_conversion | False | pattern | '" + b' | 4 |
| string_literal | True | pattern | '" "' | 4 |

G: 14 concept nodes (4 generic), 7 concept edges, 43 misconception / error edges, 38 misconception / error nodes, 70 level nodes, 56 level-misconception links, 7 connected piece(s).
Note: concept nodes form 7 pieces (the KG has no edge between them): array_aliasing | array_declaration | array_initializer | array_reference,data_structure,data_type,primitive_type,primitive_vs_reference | indexing | println,statement,string_literal | string_concatenation,string_conversion

Concept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):
| edge | type | rule (logic) |
|---|---|---|
| pre:array_reference->primitive_vs_reference | prerequisite | An array variable stores the memory address of the array, not its elements. |
| pre:data_type->data_structure | prerequisite | A data structure organizes many values of a data type; the array holds a sequence of values of one type. |
| pre:data_type->primitive_type | prerequisite | Java has eight primitive data types (boolean, char, byte, short, int, long, float, double); each, like any data type, is a set of values and a set of operations on those values. |
| pre:primitive_type->primitive_vs_reference | prerequisite | A variable of a primitive type stores the value itself in its own memory. |
| pre:statement->println | prerequisite | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |
| pre:string_concatenation->string_conversion | prerequisite | When one operand of + is a String, Java converts the other operand to a String before concatenating. |
| pre:string_literal->println | prerequisite | println("s") outputs exactly the characters between the quotes and then ends the line. |

Misconception / error edges per concept (count), and level ways per concept (count):
| concept | misconception / error edges | level ways (L1-L4 + L0 non-misconception) |
|---|---|---|
| array_aliasing | 3 | 15 |
| array_declaration | 4 | 13 |
| array_initializer | 2 | 14 |
| array_reference | 0 | 12 |
| data_structure | 0 | 11 |
| data_type | 2 | 14 |
| indexing | 8 | 21 |
| primitive_type | 2 | 21 |
| primitive_vs_reference | 3 | 13 |
| println | 6 | 17 |
| statement | 5 | 19 |
| string_concatenation | 3 | 16 |
| string_conversion | 1 | 13 |
| string_literal | 4 | 16 |

**Figure 1**

![Figure 1](figure01.png)
**Figure 2**

![Figure 2](figure02.png)
## 2. Clauses and start concepts (no model)
The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):
| clause | text |
|---|---|
| c1 | It prints 1 9 |
| c2 | The line b = a makes b a copy of a |
| c3 | so b is a separate array |
| c4 | Changing b[0] to 9 only changes b, and a[0] is still 1 |

start: BM25 of the answer against each tagged concept: array_aliasing 32.58 (hits 1), indexing 27.65 (hits 1), string_concatenation 22.00 (hits 1), println 15.38 (hits 1), array_declaration 13.84 (hits 1), array_initializer 12.24 (hits 1), primitive_vs_reference 8.93 (hits 1), string_conversion 4.73 (hits 1), data_structure 2.75 (hits 1), array_reference 1.85 (hits 1)

start: chosen array_aliasing, indexing, string_concatenation

start concepts (3): array_aliasing, indexing, string_concatenation

Start concepts: array_aliasing, indexing, string_concatenation

**Figure 3**

![Figure 3](figure03.png)
## 3. The walk, depth by depth
At each depth, for each current concept: the edges offered (a concept entering as a start concept offers its misconception / error edges and its level ways, as two families; otherwise it offers its concept edges), the prune prompt and the model's reply, then the label prompt(s) and the model's reply, parsed into label / clauses / confidence. Score = prune score x confidence.

### Depth 1: current concepts 'array_aliasing', 'indexing', 'string_concatenation'

#### array_aliasing, misconceptions: 3 edges offered
Edges offered:
| edge |
|---|
| mis:array_aliasing->ArrayEqualityComparesValues \| wrong rule: a == b is true when a and b hold the same values. \| right rule: == compares whether the two arrays are the same array, not whether their values are equal. |
| mis:array_aliasing->ArrayListIsArray \| wrong rule: An ArrayList is just an array, so it has a fixed length and is indexed with []. \| right rule: An array has a fixed length and uses [] and .length; an ArrayList can grow and uses get, set and size(). |
| mis:array_aliasing->AssignmentCopiesObject \| wrong rule: assigning a reference copies the object \| right rule: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i]. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:array_aliasing->AssignmentCopiesObject (1.00)
```
Kept by pruning: mis:array_aliasing->AssignmentCopiesObject (1.00)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:array_aliasing->AssignmentCopiesObject \| wrong rule: assigning a reference copies the object \| right rule: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i]. |
Model's reply:
```
mis:array_aliasing->AssignmentCopiesObject | held | clauses: 1, 2, 3, 4 | confidence: 0.97
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:array_aliasing->AssignmentCopiesObject | held | 1.0 | 0.97 | 0.97 | c1, c2, c3, c4 | It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1 |

#### array_aliasing, level ways: 15 edges offered
Edges offered:
| edge |
|---|
| lvl:array_aliasing@L0#0 \| level L0 way everyday_reading: Folk meaning: in maths and English, 'b = a' means b becomes an equal but independent copy, and 'a == b' means 'have the same values'. Java rule: for arrays, b = a copies only the reference, so both names denote one array, and == tests whether two names refer to the same array. |
| lvl:array_aliasing@L0#3 \| level L0 way inconsistent_trace: Points to LT: b = a copies the reference, so every later write through b is a write to the shared array. Inconsistent application: after b = a the trace changes b[0] but leaves a[0] unchanged in its table, keeping two copies on some steps and one array on others. (here mixing in: "a == b is true when a and b hold the same values") |
| lvl:array_aliasing@L1#0 \| level L1 way names_the_element: Identity: aliasing is the situation in which two or more array variables refer to the same array object. |
| lvl:array_aliasing@L1#1 \| level L1 way states_the_rule: Declarative: an assignment makes the names a and b refer to the same array; an equality test a == b checks whether the two names refer to the same array. |
| lvl:array_aliasing@L2#0 \| level L2 way line_by_line_trace: Sequencing: in b = a, a is evaluated to its reference value, which is then stored in b; no element is read or copied. In a == b both reference values are evaluated and compared. |
| lvl:array_aliasing@L2#1 \| level L2 way output_prediction: Result: for int[] a = {1, 2, 3}; int[] b = {1, 2, 3};, the test a == b is false; after b = a it is true. A read through either name gives the same element. |
| lvl:array_aliasing@L2#2 \| level L2 way one_step_execution: State transition: b = a changes only the variable b (it now holds a's reference). A later b[0] = 17 changes the one shared array, so a[0] then reads 17 too. |
| lvl:array_aliasing@L3#0 \| level L3 way relation_to_neighbour: Only new creates a distinct array; to copy, create a new array and copy each element (or use Arrays.copyOf). |
| lvl:array_aliasing@L3#1 \| level L3 way relation_to_neighbour: Assignment, == and println(a) all act on the reference value: two aliases print the same address, while two equal-content arrays print different ones. |
| lvl:array_aliasing@L3#2 \| level L3 way relation_to_neighbour: b = a makes a second name for the same array (an alias); copying makes a second array: after a copy, changing b[i] leaves a[i] unchanged. |
| lvl:array_aliasing@L3#3 \| level L3 way purpose_of_the_whole: Plan/role: aliasing lets two names work on one array without copying (as when an array is passed to a method), but in Chapter 1 code it is mostly a source of subtle bugs. |
| lvl:array_aliasing@L4#0 \| level L4 way predict_a_change: Conservation: replacing b = a with an element-copy loop keeps b's initial contents but breaks the link, so later changes to a no longer show in b. Reassigning a = new int[n] after b = a leaves b on the old array. |
| lvl:array_aliasing@L4#1 \| level L4 way transfer_to_a_new_program: Applicability: assign an array variable when you want a second name for the same data. Use a copy loop or Arrays.copyOf for an independent copy, and an element loop or Arrays.equals to compare contents. |
| lvl:array_aliasing@L4#2 \| level L4 way diagnose_an_error: rule broken: Assignment copies the reference, not the elements. Kind: silent logic error. Trigger class: b = a is used as a 'copy', and then b is modified while a is expected to stay unchanged (or the reverse) |
| lvl:array_aliasing@L4#3 \| level L4 way diagnose_an_error: rule broken: == on arrays compares references, not contents. Kind: silent logic error. Trigger class: two separately created arrays with equal elements are compared with == (always false) |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:array_aliasing@L0#0 (Score: 0.5)}
{lvl:array_aliasing@L4#2 (Score: 0.3)}
{lvl:array_aliasing@L2#2 (Score: 0.2)}
```
Kept by pruning: lvl:array_aliasing@L0#0 (0.50), lvl:array_aliasing@L4#2 (0.30), lvl:array_aliasing@L2#2 (0.20)

Label prompt for level way lvl:array_aliasing@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: in maths and English, 'b = a' means b becomes an equal but independent copy, and 'a == b' means 'have the same values'. Java rule: for arrays, b = a copies only the reference, so both names denote one array, and == tests whether two names refer to the same array.

Model's reply:
```
Label: shown
Clauses: 1, 2, 3, 4
Confidence: 0.9
```

Label prompt for level way lvl:array_aliasing@L4#2 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: Assignment copies the reference, not the elements. Kind: silent logic error. Trigger class: b = a is used as a 'copy', and then b is modified while a is expected to stay unchanged (or the reverse)

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:array_aliasing@L2#2 (the model saw only the concept, the way's name 'one step execution' and its text; no level):
> State transition: b = a changes only the variable b (it now holds a's reference). A later b[0] = 17 changes the one shared array, so a[0] then reads 17 too.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:array_aliasing@L0#0 | shown | 0.5 | 0.9 | 0.45 | c1, c2, c3, c4 | It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1 |
| lvl:array_aliasing@L4#2 | not applied |  |  | 0.0 |  |  |
| lvl:array_aliasing@L2#2 | not applied |  |  | 0.0 |  |  |

#### indexing, misconceptions: 8 edges offered
Edges offered:
| edge |
|---|
| mis:indexing->ArrayAccessWithParentheses \| wrong rule: a(i) accesses element i of an array. \| right rule: Array elements are accessed with square brackets, a[i]. |
| mis:indexing->ArrayElementNotVariable \| wrong rule: An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]]. \| right rule: Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index. |
| mis:indexing->ArrayIndexStartsAtOne \| wrong rule: The first element of a is a[1]. \| right rule: Numbering begins with 0; the first element is a[0]. |
| mis:indexing->ArrayRangeInclusive \| wrong rule: new int[n] has slots 0 to n, inclusive. \| right rule: The slots are 0 to n - 1. |
| mis:indexing->ArrayUseScansAllCells \| wrong rule: Using an array means every cell must be scanned. \| right rule: Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs. |
| mis:indexing->ElementBoundToOldIndex \| wrong rule: After i changes, X[i] still refers to the element at the old value of i. \| right rule: a[i] is evaluated with the current value of i each time it is used. |
| mis:indexing->ElementNameIsWholeArray \| wrong rule: X[i] names the whole array, not one element. \| right rule: The array is a; a[i] is the single element at index i. |
| mis:indexing->IndexIsValue \| wrong rule: i and a[i] are the same thing, so the position is the stored value. \| right rule: i is a position; a[i] is the value stored at that position. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:indexing->ArrayIndexStartsAtOne (0.40), mis:indexing->ElementNameIsWholeArray (0.35), mis:indexing->ArrayElementNotVariable (0.25)
```
Kept by pruning: mis:indexing->ArrayIndexStartsAtOne (0.40), mis:indexing->ElementNameIsWholeArray (0.35), mis:indexing->ArrayElementNotVariable (0.25)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:indexing->ArrayIndexStartsAtOne \| wrong rule: The first element of a is a[1]. \| right rule: Numbering begins with 0; the first element is a[0]. |
| mis:indexing->ElementNameIsWholeArray \| wrong rule: X[i] names the whole array, not one element. \| right rule: The array is a; a[i] is the single element at index i. |
| mis:indexing->ArrayElementNotVariable \| wrong rule: An array element a[i] is not a variable, so it cannot be read into directly or used inside another index, as in a[a[i]]. \| right rule: Each element a[i] is a variable of the element type and can be used anywhere a variable of that type can, including as an index. |
Model's reply:
```
mis:indexing->ArrayIndexStartsAtOne | correct | clauses: 1, 4 | confidence: 0.75
mis:indexing->ElementNameIsWholeArray | correct | clauses: 4 | confidence: 0.55
mis:indexing->ArrayElementNotVariable | not applied | clauses: none | confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:indexing->ArrayIndexStartsAtOne | correct | 0.4 | 0.75 | 0.3 | c1, c4 | It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1 |
| mis:indexing->ElementNameIsWholeArray | correct | 0.35 | 0.55 | 0.19 | c4 | Changing b[0] to 9 only changes b, and a[0] is still 1 |
| mis:indexing->ArrayElementNotVariable | not applied |  |  | 0.0 |  |  |

#### indexing, level ways: 21 edges offered
Edges offered:
| edge |
|---|
| lvl:indexing@L0#0 \| level L0 way everyday_reading: Folk meaning: everyday counting starts at 1 (first = number 1), maths subscripts a_1..a_n run from 1, and f(i) with parentheses means 'apply to i'. Java rule: a[i] uses square brackets and is 0-origin, so the first element is a[0] and the last is a[a.length-1]. |
| lvl:indexing@L0#8 \| level L0 way inconsistent_trace: Points to LT: in a[i], a is evaluated, then i with its current value, then the bounds check, then the element is read or written. Inconsistent application: i is updated on one line, but a later a[i] is traced with the old i. (here mixing in: "i and a[i] are the same thing, so the position is the stored value") |
| lvl:indexing@L1#0 \| level L1 way names_the_element: Identity: an array access expression; a[i] names the single element variable at position i of the array a refers to. |
| lvl:indexing@L1#1 \| level L1 way states_the_rule: Declarative: the index is any int-valued expression in square brackets; the valid indices of an array of length n are 0 to n-1, and an access outside that range throws ArrayIndexOutOfBoundsException. |
| lvl:indexing@L2#0 \| level L2 way line_by_line_trace: Sequencing: the array reference is evaluated before the index; the index expression is fully evaluated with current variable values; the bounds are checked; then the element is fetched or, on the left of =, becomes the target. In a[i] = a[j], the target a[i] is located before a[j] is read. |
| lvl:indexing@L2#1 \| level L2 way output_prediction: Result: a[i] has the element type and the value currently stored at position i. For int[] a = {5, 7, 9}, a[1] is 7 and a[0] + a[2] is 14. |
| lvl:indexing@L2#2 \| level L2 way one_step_execution: State transition: reading a[i] changes nothing. a[i] = v changes only element i (i, a and all other elements are unchanged), and a[i]++ adds 1 to that one element. |
| lvl:indexing@L3#0 \| level L3 way relation_to_neighbour: An element can be indexed only after the array is created, and the n given to new sets the valid indices 0..n-1. |
| lvl:indexing@L3#1 \| level L3 way relation_to_neighbour: A traversal uses the loop variable as the index, so the same expression a[i] reaches a different element on each pass. |
| lvl:indexing@L3#2 \| level L3 way relation_to_neighbour: Every index value is checked against 0 and a.length at run time; any other value throws. |
| lvl:indexing@L3#3 \| level L3 way relation_to_neighbour: a[i] on a 2-D array yields row i (itself a 1-D array), and a[i][j] then indexes into that row. |
| lvl:indexing@L3#4 \| level L3 way relation_to_neighbour: The exchange reads and writes elements only through their indices: t = a[i]; a[i] = a[j]; a[j] = t. |
| lvl:indexing@L3#5 \| level L3 way relation_to_neighbour: A lookup table uses a data value as the index (months[m]), so the data must lie in 0..length-1. |
| lvl:indexing@L3#6 \| level L3 way relation_to_neighbour: Indices start at 0, so the last element is a[N-1]; misreading this convention is the usual source of off-by-one errors. |
| lvl:indexing@L3#7 \| level L3 way purpose_of_the_whole: Plan/role: random access, reaching any element directly by its position in constant time (address plus index), so code touches only the elements it needs. |
| lvl:indexing@L4#0 \| level L4 way predict_a_change: Conservation: changing the index expression (i to i+1 or i-1) shifts which element is touched and can leave the bounds at the ends. Writing a[a[i]] instead of a[i] uses an element value as the index, a different access entirely. Changing what is stored never changes the positions. |
| lvl:indexing@L4#1 \| level L4 way transfer_to_a_new_program: Applicability: index when you need a particular element by position, or when the position is computed from data (counts[score]++, months[m]). When every value is processed in order and the position is never needed, an enhanced for loop is simpler. |
| lvl:indexing@L4#2 \| level L4 way diagnose_an_error: rule broken: The index must be in 0..a.length-1. Kind: run-time exception. Trigger class: index < 0 or >= a.length, e.g. a[a.length], a[i+1] on the last pass, a[i-1] at i = 0, a[0] of an empty array (ArrayIndexOutOfBoundsException) |
| lvl:indexing@L4#3 \| level L4 way diagnose_an_error: rule broken: The index must have type int (after promotion); long or double indices are rejected. Kind: compile-time. Trigger class: a[1.5], a[x] with double x, or a[n] with long n (incompatible types: possible lossy conversion) |
| lvl:indexing@L4#4 \| level L4 way diagnose_an_error: rule broken: Elements are selected with brackets, not parentheses. Kind: compile-time. Trigger class: a(i) is written for a[i] (cannot find symbol: method a) |
| lvl:indexing@L4#5 \| level L4 way diagnose_an_error: rule broken: An index is a position, not the stored value. Kind: silent logic error. Trigger class: code uses i where a[i] is meant (or a[i] where i is meant), e.g. returning i as the maximum value or comparing positions instead of contents |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:indexing@L2#2 (Score: 0.45)}
{lvl:indexing@L1#0 (Score: 0.35)}
{lvl:indexing@L2#1 (Score: 0.2)}
```
Kept by pruning: lvl:indexing@L2#2 (0.45), lvl:indexing@L1#0 (0.35), lvl:indexing@L2#1 (0.20)

Label prompt for level way lvl:indexing@L2#2 (the model saw only the concept, the way's name 'one step execution' and its text; no level):
> State transition: reading a[i] changes nothing. a[i] = v changes only element i (i, a and all other elements are unchanged), and a[i]++ adds 1 to that one element.

Model's reply:
```
Label: shown
Clauses: 1, 4
Confidence: 0.6
```

Label prompt for level way lvl:indexing@L1#0 (the model saw only the concept, the way's name 'names the element' and its text; no level):
> Identity: an array access expression; a[i] names the single element variable at position i of the array a refers to.

Model's reply:
```
Label: shown
Clauses: 4
Confidence: 0.6
```

Label prompt for level way lvl:indexing@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> Result: a[i] has the element type and the value currently stored at position i. For int[] a = {5, 7, 9}, a[1] is 7 and a[0] + a[2] is 14.

Model's reply:
```
Label: shown
Clauses: 1, 4
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:indexing@L2#2 | shown | 0.45 | 0.6 | 0.27 | c1, c4 | It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1 |
| lvl:indexing@L1#0 | shown | 0.35 | 0.6 | 0.21 | c4 | Changing b[0] to 9 only changes b, and a[0] is still 1 |
| lvl:indexing@L2#1 | shown | 0.2 | 0.6 | 0.12 | c1, c4 | It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1 |

#### string_concatenation, misconceptions: 3 edges offered
Edges offered:
| edge |
|---|
| mis:string_concatenation->ArithmeticPlusPrecedes \| wrong rule: In "s" + a + b, the numbers a and b are added first and their sum is joined to s. \| right rule: Both uses of + have the same precedence and are evaluated left to right, so "s" + a + b joins a and then b as text; only "s" + (a + b) adds them first. |
| mis:string_concatenation->StringPlusLeftToRight \| wrong rule: 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. \| right rule: + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23". |
| mis:string_concatenation->StringPlusStringifiesExpression \| wrong rule: In "s" + (a + b), the text a + b is joined to s instead of its value. \| right rule: The expression (a + b) is evaluated first, and its value is then turned into text and joined to s. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:string_concatenation->ArithmeticPlusPrecedes (Score: 0.5)}
{mis:string_concatenation->StringPlusLeftToRight (Score: 0.35)}
{mis:string_concatenation->StringPlusStringifiesExpression (Score: 0.15)}
```
Kept by pruning: mis:string_concatenation->ArithmeticPlusPrecedes (0.50), mis:string_concatenation->StringPlusLeftToRight (0.35), mis:string_concatenation->StringPlusStringifiesExpression (0.15)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:string_concatenation->ArithmeticPlusPrecedes \| wrong rule: In "s" + a + b, the numbers a and b are added first and their sum is joined to s. \| right rule: Both uses of + have the same precedence and are evaluated left to right, so "s" + a + b joins a and then b as text; only "s" + (a + b) adds them first. |
| mis:string_concatenation->StringPlusLeftToRight \| wrong rule: 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. \| right rule: + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23". |
| mis:string_concatenation->StringPlusStringifiesExpression \| wrong rule: In "s" + (a + b), the text a + b is joined to s instead of its value. \| right rule: The expression (a + b) is evaluated first, and its value is then turned into text and joined to s. |
Model's reply:
```
mis:string_concatenation->ArithmeticPlusPrecedes | not applied | clauses: none | confidence: 0.85
mis:string_concatenation->StringPlusLeftToRight | not applied | clauses: none | confidence: 0.85
mis:string_concatenation->StringPlusStringifiesExpression | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:string_concatenation->ArithmeticPlusPrecedes | not applied |  |  | 0.0 |  |  |
| mis:string_concatenation->StringPlusLeftToRight | not applied |  |  | 0.0 |  |  |
| mis:string_concatenation->StringPlusStringifiesExpression | not applied |  |  | 0.0 |  |  |

#### string_concatenation, level ways: 16 edges offered
Edges offered:
| edge |
|---|
| lvl:string_concatenation@L0#0 \| level L0 way everyday_reading: In arithmetic, + always means 'add', and 'plus' combines quantities, so novices expect "1" + 2 to be 3. In Java, + with a String operand joins text end to end, and a chain of + is processed left to right, one operator at a time. |
| lvl:string_concatenation@L0#3 \| level L0 way inconsistent_trace: Points to LT (left to right, and each + adds or concatenates according to its operands at that moment). Applied unevenly, a student keeps adding numbers after a String has appeared, or concatenates before any String appears (1 + 2 + "x" as "12x"). (here mixing in: "+ with a String turns the whole other side into a string first") |
| lvl:string_concatenation@L1#0 \| level L1 way names_the_element: String concatenation: the + operator with a String operand, which joins two values end to end into a new String. |
| lvl:string_concatenation@L1#1 \| level L1 way states_the_rule: If either operand of + is a String, the other is converted to a String, and the result is a new String made of the first operand's characters followed by the second's. |
| lvl:string_concatenation@L2#0 \| level L2 way line_by_line_trace: A chain of + is evaluated left to right, after any parenthesized parts. At each + the current operand types decide: two numbers are added, otherwise the values are concatenated. |
| lvl:string_concatenation@L2#1 \| level L2 way output_prediction: The result is a String: 2 + "bc" is "2bc", 2 + 3 + "bc" is "5bc", "bc" + 2 + 3 is "bc23", and "bc" + (2+3) is "bc5". |
| lvl:string_concatenation@L2#2 \| level L2 way one_step_execution: Concatenation creates a new String and changes no operand. A variable changes only if the result is assigned, as in ruler = ruler + i + ruler;. |
| lvl:string_concatenation@L3#0 \| level L3 way relation_to_neighbour: Concatenation always yields a String, even when one operand is a number, so its result cannot be used in arithmetic without parsing. |
| lvl:string_concatenation@L3#1 \| level L3 way relation_to_neighbour: The non-String operand is converted to its printed form (int 99 to "99", double 1.0 to "1.0", char 'a' to "a") before joining. |
| lvl:string_concatenation@L3#2 \| level L3 way relation_to_neighbour: + adds when both operands are numbers and concatenates when either operand is a String, converting the other operand to a String. It is left-associative, so 1 + 2 + "3" is "33" but "1" + 2 + 3 is "123". |
| lvl:string_concatenation@L3#3 \| level L3 way purpose_of_the_whole: Concatenation builds output lines and labels from computed values (a + " + " + b + " = " + c). Repeated s = s + piece makes s a gatherer of text. |
| lvl:string_concatenation@L4#0 \| level L4 way predict_a_change: Parenthesizing numeric parts changes the result ("sum " + (a + b) adds before joining). Moving numbers before or after the first String changes whether they are added. Concatenating into a printf format string removes the separate argument printf needs. |
| lvl:string_concatenation@L4#1 \| level L4 way transfer_to_a_new_program: Use + concatenation for simple output and labels, putting parentheses around any arithmetic inside. Use printf when numbers need formatting, and parse Strings before using them as numbers. |
| lvl:string_concatenation@L4#2 \| level L4 way diagnose_an_error: rule broken: Once a String appears in a + chain, every later + concatenates. Kind: silent logic error. Trigger class: "Sum: " + a + b with numbers a and b prints both digit strings side by side (e.g. Sum: 23). |
| lvl:string_concatenation@L4#3 \| level L4 way diagnose_an_error: rule broken: char + char is numeric addition, not concatenation. Kind: silent logic error. Trigger class: Joining two chars with + when no String is involved ('b' + 'c' prints 197). |
| lvl:string_concatenation@L4#4 \| level L4 way diagnose_an_error: rule broken: printf needs its values as separate arguments matching the format specifiers. Kind: run-time exception. Trigger class: Concatenating the value into the format (printf("inches = %d" + inch)): MissingFormatArgumentException. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:string_concatenation@L2#1 (Score: 0.5)}
{lvl:string_concatenation@L2#0 (Score: 0.3)}
{lvl:string_concatenation@L3#1 (Score: 0.2)}
```
Kept by pruning: lvl:string_concatenation@L2#1 (0.50), lvl:string_concatenation@L2#0 (0.30), lvl:string_concatenation@L3#1 (0.20)

Label prompt for level way lvl:string_concatenation@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> The result is a String: 2 + "bc" is "2bc", 2 + 3 + "bc" is "5bc", "bc" + 2 + 3 is "bc23", and "bc" + (2+3) is "bc5".

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.75
```

Label prompt for level way lvl:string_concatenation@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> A chain of + is evaluated left to right, after any parenthesized parts. At each + the current operand types decide: two numbers are added, otherwise the values are concatenated.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.75
```

Label prompt for level way lvl:string_concatenation@L3#1 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> The non-String operand is converted to its printed form (int 99 to "99", double 1.0 to "1.0", char 'a' to "a") before joining.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.55
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:string_concatenation@L2#1 | not applied |  |  | 0.0 |  |  |
| lvl:string_concatenation@L2#0 | not applied |  |  | 0.0 |  |  |
| lvl:string_concatenation@L3#1 | shown | 0.2 | 0.55 | 0.11 | c1 | It prints 1 9 |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:array_aliasing->AssignmentCopiesObject [held, tier 0, 0.97], lvl:array_aliasing@L0#0 [shown, tier 2, 0.45], mis:indexing->ArrayIndexStartsAtOne [correct, tier 2, 0.30]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | It prints 1 9 | mis:array_aliasing->AssignmentCopiesObject |
| c2 | The line b = a makes b a copy of a | mis:array_aliasing->AssignmentCopiesObject |
| c3 | so b is a separate array | mis:array_aliasing->AssignmentCopiesObject |
| c4 | Changing b[0] to 9 only changes b, and a[0] is still 1 | mis:array_aliasing->AssignmentCopiesObject |

**Graph check, not yet read (the walk may not stop while these remain):** pre:string_concatenation->string_conversion

**Figure 4 (the graph after depth 1)**

![Figure 4](figure04.png)
### Depth 2: current concepts 'array_aliasing', 'string_concatenation'

#### string_concatenation, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:string_concatenation->string_conversion \| rule: When one operand of + is a String, Java converts the other operand to a String before concatenating. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:string_concatenation->string_conversion (Score: 1.0)}
```
Kept by pruning: pre:string_concatenation->string_conversion (1.00)

Label prompt for concept edge pre:string_concatenation->string_conversion (string_concatenation -> string_conversion, prerequisite):
> When one operand of + is a String, Java converts the other operand to a String before concatenating.

Model's reply:
```
Label: confirmed
Clauses: 1
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:string_concatenation->string_conversion | confirmed | 1.0 | 0.6 | 0.6 | c1 | It prints 1 9 |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:string_concatenation->string_conversion [confirmed, tier 2, 0.60]

reached across pre:string_concatenation->string_conversion, entered next: string_conversion

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | It prints 1 9 | mis:array_aliasing->AssignmentCopiesObject |
| c2 | The line b = a makes b a copy of a | mis:array_aliasing->AssignmentCopiesObject |
| c3 | so b is a separate array | mis:array_aliasing->AssignmentCopiesObject |
| c4 | Changing b[0] to 9 only changes b, and a[0] is still 1 | mis:array_aliasing->AssignmentCopiesObject |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of string_conversion

**Figure 5 (the graph after depth 2)**

![Figure 5](figure05.png)
### Depth 3: current concepts 'string_conversion', 'string_concatenation'

#### string_conversion, misconceptions: 1 edges offered
Edges offered:
| edge |
|---|
| mis:string_conversion->StringPlusLeftToRight \| wrong rule: 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. \| right rule: + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23". |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:string_conversion->StringPlusLeftToRight (Score: 1.0)}
```
Kept by pruning: mis:string_conversion->StringPlusLeftToRight (1.00)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:string_conversion->StringPlusLeftToRight \| wrong rule: 2 + 3 + "bc" and "bc" + 2 + 3 give the same text. \| right rule: + is evaluated left to right: 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23". |
Model's reply:
```
mis:string_conversion->StringPlusLeftToRight | not applied | clauses: none | confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:string_conversion->StringPlusLeftToRight | not applied |  |  | 0.0 |  |  |

#### string_conversion, level ways: 13 edges offered
Edges offered:
| edge |
|---|
| lvl:string_conversion@L0#0 \| level L0 way everyday_reading: Folk meaning: + is addition, which is commutative and associative, so 2 + 3 + "bc" and "bc" + 2 + 3 must give the same thing. Java rule: when one operand of + is a String the other is converted to a String and concatenated, and + is evaluated left to right, so 2 + 3 + "bc" is "5bc" but "bc" + 2 + 3 is "bc23". |
| lvl:string_conversion@L0#2 \| level L0 way inconsistent_trace: Points to LT (+ is applied left to right, each + deciding between addition and concatenation from its two operands at that moment). Applied unevenly: once a String has appeared the student goes back to numeric addition for later terms, or concatenates two numbers that come before any String. (here mixing in: "2 + 3 + "bc" and "bc" + 2 + 3 give the same text") |
| lvl:string_conversion@L1#0 \| level L1 way names_the_element: String conversion is the automatic conversion of a non-String operand of + into its String form when the other operand is a String (also done for print/println arguments). |
| lvl:string_conversion@L1#1 \| level L1 way states_the_rule: When either operand of + is a String, the other operand is converted to a String and the result is the characters of the first followed by those of the second; System.out.print and println also convert any argument to a String. |
| lvl:string_conversion@L2#0 \| level L2 way line_by_line_trace: Evaluate + operators left to right (same precedence, left-associative): at each +, if either current operand is a String, convert the other and concatenate; otherwise add numerically. Parenthesized parts are evaluated first. |
| lvl:string_conversion@L2#1 \| level L2 way output_prediction: A String: 2 + "bc" is "2bc", 2 + 3 + "bc" is "5bc", "bc" + (2+3) is "bc5", "bc" + 2 + 3 is "bc23", "1234" + 99 is "123499". |
| lvl:string_conversion@L2#2 \| level L2 way one_step_execution: Concatenation creates a new String and changes no variable; state changes only by assignment, e.g. String c = a + b; with a = "1234" and int b = 99 gives c the value "123499". |
| lvl:string_conversion@L3#0 \| level L3 way relation_to_neighbour: Conversion happens first, then concatenation: the non-String operand is turned into its characters before the two Strings are joined. |
| lvl:string_conversion@L3#1 \| level L3 way purpose_of_the_whole: Used to build output messages and labels from computed values, e.g. System.out.println(a + " + " + b + " = " + c);. |
| lvl:string_conversion@L4#0 \| level L4 way predict_a_change: Adding parentheses around the numeric part changes "bc23" into "bc5"; moving a String operand earlier turns every later + into concatenation; the order of operands matters, unlike numeric addition. |
| lvl:string_conversion@L4#1 \| level L4 way transfer_to_a_new_program: Use string conversion with + to produce output and labels; do not use it to do arithmetic on numeric text (parse first), and parenthesize numeric parts that must be added before concatenation. |
| lvl:string_conversion@L4#2 \| level L4 way diagnose_an_error: rule broken: + is left-associative, so terms after a String are concatenated, not added. Kind: silent logic error. Trigger class: A numeric sum written after a String without parentheses, e.g. "Sum: " + a + b printing "Sum: 34" for a = 3, b = 4. |
| lvl:string_conversion@L4#3 \| level L4 way diagnose_an_error: rule broken: Only + converts to String; other arithmetic operators are not defined on Strings. Kind: compile-time. Trigger class: Using -, *, / with a String operand, e.g. "Hello" - 1 or "12" * 2. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:string_conversion@L2#1 (Score: 0.5)}
{lvl:string_conversion@L3#1 (Score: 0.3)}
{lvl:string_conversion@L2#0 (Score: 0.2)}
```
Kept by pruning: lvl:string_conversion@L2#1 (0.50), lvl:string_conversion@L3#1 (0.30), lvl:string_conversion@L2#0 (0.20)

Label prompt for level way lvl:string_conversion@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> A String: 2 + "bc" is "2bc", 2 + 3 + "bc" is "5bc", "bc" + (2+3) is "bc5", "bc" + 2 + 3 is "bc23", "1234" + 99 is "123499".

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.97
```

Label prompt for level way lvl:string_conversion@L3#1 (the model saw only the concept, the way's name 'purpose of the whole' and its text; no level):
> Used to build output messages and labels from computed values, e.g. System.out.println(a + " + " + b + " = " + c);.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.75
```

Label prompt for level way lvl:string_conversion@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Evaluate + operators left to right (same precedence, left-associative): at each +, if either current operand is a String, convert the other and concatenate; otherwise add numerically. Parenthesized parts are evaluated first.

Model's reply:
```
Label: shown
Clauses: 1
Confidence: 0.55
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:string_conversion@L2#1 | not applied |  |  | 0.0 |  |  |
| lvl:string_conversion@L3#1 | not applied |  |  | 0.0 |  |  |
| lvl:string_conversion@L2#0 | shown | 0.2 | 0.55 | 0.11 | c1 | It prints 1 9 |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

lvl:string_conversion@L2#0 [shown, tier 2, 0.11]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | It prints 1 9 | mis:array_aliasing->AssignmentCopiesObject |
| c2 | The line b = a makes b a copy of a | mis:array_aliasing->AssignmentCopiesObject |
| c3 | so b is a separate array | mis:array_aliasing->AssignmentCopiesObject |
| c4 | Changing b[0] to 9 only changes b, and a[0] is still 1 | mis:array_aliasing->AssignmentCopiesObject |

**Figure 6 (the graph after depth 3)**

![Figure 6](figure06.png)
## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on ['array_aliasing'], broken at [], prerequisites {'primitive_vs_reference': ['array_reference', 'primitive_type'], 'data_structure': ['data_type'], 'primitive_type': ['data_type'], 'println': ['statement', 'string_literal'], 'string_conversion': ['string_concatenation']}
- array_aliasing: L0 via misconception "It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1"
- indexing: L2 via one_step_execution "It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1"
- string_concatenation: L3 via relation_to_neighbour "It prints 1 9"
- string_conversion: L2 via line_by_line_trace "It prints 1 9"

**Stop:** sufficient at depth 3; prompts {'prune': 9, 'label': 17}, fresh model calls 0, cache hits 26

### Held misconceptions
| concept | misconception | kind | quote | score | shares_evidence_with |
|---|---|---|---|---|---|
| array_aliasing | AssignmentCopiesObject | misconception | It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1 | 0.97 |  |

### Broken concept edges
(none)

### Root cause: array_aliasing / AssignmentCopiesObject

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| array_aliasing | L0 | misconception | AssignmentCopiesObject | level_mis_links | It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1 | wrong rule: Assigning an array reference copies the array. Right rule: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i]. |  |  |
| indexing | L2 | one_step_execution |  | level_way | It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1 |  | L2 output_prediction, L1 names_the_element |  |
| string_concatenation | L3 | relation_to_neighbour |  | level_way | It prints 1 9 |  |  |  |
| string_conversion | L2 | line_by_line_trace |  | level_way | It prints 1 9 |  |  |  |

### Overall level: L0

Clause coverage (final):
| clause | covered by |
|---|---|
| It prints 1 9 | mis:array_aliasing->AssignmentCopiesObject |
| The line b = a makes b a copy of a | mis:array_aliasing->AssignmentCopiesObject |
| so b is a separate array | mis:array_aliasing->AssignmentCopiesObject |
| Changing b[0] to 9 only changes b, and a[0] is still 1 | mis:array_aliasing->AssignmentCopiesObject |

**Figure 7 (final picture)**

![Figure 7](figure07.png)
## 5. Every labelled edge (the evidence list, kept or not)
| depth | source | edge | kind | label | prune_score | confidence | score | clauses | quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | array_aliasing | mis:array_aliasing->AssignmentCopiesObject | misconception | held | 1.0 | 0.97 | 0.97 | [1, 2, 3, 4] | It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1 |
| 1 | array_aliasing | lvl:array_aliasing@L0#0 | level | shown | 0.5 | 0.9 | 0.45 | [1, 2, 3, 4] | It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1 |
| 1 | indexing | mis:indexing->ArrayIndexStartsAtOne | misconception | correct | 0.4 | 0.75 | 0.3 | [1, 4] | It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1 |
| 1 | indexing | mis:indexing->ElementNameIsWholeArray | misconception | correct | 0.35 | 0.55 | 0.1925 | [4] | Changing b[0] to 9 only changes b, and a[0] is still 1 |
| 1 | indexing | lvl:indexing@L2#2 | level | shown | 0.45 | 0.6 | 0.27 | [1, 4] | It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1 |
| 1 | indexing | lvl:indexing@L1#0 | level | shown | 0.35 | 0.6 | 0.21 | [4] | Changing b[0] to 9 only changes b, and a[0] is still 1 |
| 1 | indexing | lvl:indexing@L2#1 | level | shown | 0.2 | 0.6 | 0.12 | [1, 4] | It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1 |
| 1 | string_concatenation | lvl:string_concatenation@L3#1 | level | shown | 0.2 | 0.55 | 0.11 | [1] | It prints 1 9 |
| 2 | string_concatenation | pre:string_concatenation->string_conversion | prerequisite | confirmed | 1.0 | 0.6 | 0.6 | [1] | It prints 1 9 |
| 3 | string_conversion | lvl:string_conversion@L2#0 | level | shown | 0.2 | 0.55 | 0.11 | [1] | It prints 1 9 |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | array_aliasing | mis:array_aliasing->AssignmentCopiesObject | misconception | held | 0.97 | [1, 2, 3, 4] |
| 1 | array_aliasing | lvl:array_aliasing@L0#0 | level | shown | 0.45 | [1, 2, 3, 4] |
| 1 | indexing | mis:indexing->ArrayIndexStartsAtOne | misconception | correct | 0.3 | [1, 4] |
| 2 | string_concatenation | pre:string_concatenation->string_conversion | prerequisite | confirmed | 0.6 | [1] |
| 3 | string_conversion | lvl:string_conversion@L2#0 | level | shown | 0.11 | [1] |

## 7. Raw traversal log
```
clauses: It prints 1 9 | The line b = a makes b a copy of a | so b is a separate array | Changing b[0] to 9 only changes b, and a[0] is still 1
start: BM25 of the answer against each tagged concept: array_aliasing 32.58 (hits 1), indexing 27.65 (hits 1), string_concatenation 22.00 (hits 1), println 15.38 (hits 1), array_declaration 13.84 (hits 1), array_initializer 12.24 (hits 1), primitive_vs_reference 8.93 (hits 1), string_conversion 4.73 (hits 1), data_structure 2.75 (hits 1), array_reference 1.85 (hits 1)
start: chosen array_aliasing, indexing, string_concatenation
start concepts (3): array_aliasing, indexing, string_concatenation
--- depth 1: current concepts ['array_aliasing', 'indexing', 'string_concatenation']
  array_aliasing (misconceptions): 3 candidates -> kept mis:array_aliasing->AssignmentCopiesObject (1.00)
    mis:array_aliasing->AssignmentCopiesObject -> held (0.97) "It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1"
  array_aliasing (level ways): 15 candidates -> kept lvl:array_aliasing@L0#0 (0.50), lvl:array_aliasing@L4#2 (0.30), lvl:array_aliasing@L2#2 (0.20)
    lvl:array_aliasing@L0#0 -> shown (0.45) "It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1"
    lvl:array_aliasing@L4#2 -> not applied (0.00) ""
    lvl:array_aliasing@L2#2 -> not applied (0.00) ""
  indexing (misconceptions): 8 candidates -> kept mis:indexing->ArrayIndexStartsAtOne (0.40), mis:indexing->ElementNameIsWholeArray (0.35), mis:indexing->ArrayElementNotVariable (0.25)
    mis:indexing->ArrayIndexStartsAtOne -> correct (0.30) "It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1"
    mis:indexing->ElementNameIsWholeArray -> correct (0.19) "Changing b[0] to 9 only changes b, and a[0] is still 1"
    mis:indexing->ArrayElementNotVariable -> not applied (0.00) ""
  indexing (level ways): 21 candidates -> kept lvl:indexing@L2#2 (0.45), lvl:indexing@L1#0 (0.35), lvl:indexing@L2#1 (0.20)
    lvl:indexing@L2#2 -> shown (0.27) "It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1"
    lvl:indexing@L1#0 -> shown (0.21) "Changing b[0] to 9 only changes b, and a[0] is still 1"
    lvl:indexing@L2#1 -> shown (0.12) "It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1"
  string_concatenation (misconceptions): 3 candidates -> kept mis:string_concatenation->ArithmeticPlusPrecedes (0.50), mis:string_concatenation->StringPlusLeftToRight (0.35), mis:string_concatenation->StringPlusStringifiesExpression (0.15)
    mis:string_concatenation->ArithmeticPlusPrecedes -> not applied (0.00) ""
    mis:string_concatenation->StringPlusLeftToRight -> not applied (0.00) ""
    mis:string_concatenation->StringPlusStringifiesExpression -> not applied (0.00) ""
  string_concatenation (level ways): 16 candidates -> kept lvl:string_concatenation@L2#1 (0.50), lvl:string_concatenation@L2#0 (0.30), lvl:string_concatenation@L3#1 (0.20)
    lvl:string_concatenation@L2#1 -> not applied (0.00) ""
    lvl:string_concatenation@L2#0 -> not applied (0.00) ""
    lvl:string_concatenation@L3#1 -> shown (0.11) "It prints 1 9"
  kept: mis:array_aliasing->AssignmentCopiesObject [held, tier 0, 0.97], lvl:array_aliasing@L0#0 [shown, tier 2, 0.45], mis:indexing->ArrayIndexStartsAtOne [correct, tier 2, 0.30]
  clause coverage: c1 <- mis:array_aliasing->AssignmentCopiesObject; c2 <- mis:array_aliasing->AssignmentCopiesObject; c3 <- mis:array_aliasing->AssignmentCopiesObject; c4 <- mis:array_aliasing->AssignmentCopiesObject
  not yet read: pre:string_concatenation->string_conversion
--- depth 2: current concepts ['array_aliasing', 'string_concatenation']
  string_concatenation (concept edges): 1 candidates -> kept pre:string_concatenation->string_conversion (1.00)
    pre:string_concatenation->string_conversion -> confirmed (0.60) "It prints 1 9"
  kept: pre:string_concatenation->string_conversion [confirmed, tier 2, 0.60]
  reached across pre:string_concatenation->string_conversion, entered next: string_conversion
  clause coverage: c1 <- mis:array_aliasing->AssignmentCopiesObject; c2 <- mis:array_aliasing->AssignmentCopiesObject; c3 <- mis:array_aliasing->AssignmentCopiesObject; c4 <- mis:array_aliasing->AssignmentCopiesObject
  not yet read: own edges of string_conversion
--- depth 3: current concepts ['string_conversion', 'string_concatenation']
  string_conversion (misconceptions): 1 candidates -> kept mis:string_conversion->StringPlusLeftToRight (1.00)
    mis:string_conversion->StringPlusLeftToRight -> not applied (0.00) ""
  string_conversion (level ways): 13 candidates -> kept lvl:string_conversion@L2#1 (0.50), lvl:string_conversion@L3#1 (0.30), lvl:string_conversion@L2#0 (0.20)
    lvl:string_conversion@L2#1 -> not applied (0.00) ""
    lvl:string_conversion@L3#1 -> not applied (0.00) ""
    lvl:string_conversion@L2#0 -> shown (0.11) "It prints 1 9"
  kept: lvl:string_conversion@L2#0 [shown, tier 2, 0.11]
  clause coverage: c1 <- mis:array_aliasing->AssignmentCopiesObject; c2 <- mis:array_aliasing->AssignmentCopiesObject; c3 <- mis:array_aliasing->AssignmentCopiesObject; c4 <- mis:array_aliasing->AssignmentCopiesObject
  root-cause walk: held on ['array_aliasing'], broken at [], prerequisites {'primitive_vs_reference': ['array_reference', 'primitive_type'], 'data_structure': ['data_type'], 'primitive_type': ['data_type'], 'println': ['statement', 'string_literal'], 'string_conversion': ['string_concatenation']}
  level array_aliasing: L0 via misconception "It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1"
  level indexing: L2 via one_step_execution "It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1"
  level string_concatenation: L3 via relation_to_neighbour "It prints 1 9"
  level string_conversion: L2 via line_by_line_trace "It prints 1 9"
```

## 8. Full diagnosis JSON
```json
{
 "scenario": "MY03",
 "settings": {
  "width": 3,
  "depth": 3,
  "prune_tools": "llm",
  "model": "claude-opus-5-5",
  "backend": "claude-cli"
 },
 "clauses": [
  "It prints 1 9",
  "The line b = a makes b a copy of a",
  "so b is a separate array",
  "Changing b[0] to 9 only changes b, and a[0] is still 1"
 ],
 "start_concepts": [
  "array_aliasing",
  "indexing",
  "string_concatenation"
 ],
 "held_misconceptions": [
  {
   "concept": "array_aliasing",
   "misconception": "AssignmentCopiesObject",
   "kind": "misconception",
   "quote": "It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1",
   "score": 0.97
  }
 ],
 "error_evidence": [],
 "broken_edges": [],
 "root_cause": {
  "concept": "array_aliasing",
  "misconception": "AssignmentCopiesObject"
 },
 "levels": {
  "array_aliasing": {
   "level": "L0",
   "way": "misconception",
   "misconception": "AssignmentCopiesObject",
   "quote": "It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1",
   "edge": "mis:array_aliasing->AssignmentCopiesObject",
   "rule": "wrong rule: Assigning an array reference copies the array. Right rule: b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].",
   "source": "level_mis_links"
  },
  "indexing": {
   "level": "L2",
   "way": "one_step_execution",
   "quote": "It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1",
   "edge": "lvl:indexing@L2#2",
   "source": "level_way",
   "also_shown": [
    "L2 output_prediction",
    "L1 names_the_element"
   ]
  },
  "string_concatenation": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "It prints 1 9",
   "edge": "lvl:string_concatenation@L3#1",
   "source": "level_way",
   "also_shown": []
  },
  "string_conversion": {
   "level": "L2",
   "way": "line_by_line_trace",
   "quote": "It prints 1 9",
   "edge": "lvl:string_conversion@L2#0",
   "source": "level_way",
   "also_shown": []
  }
 },
 "overall_level": "L0",
 "paths": [
  {
   "depth": 1,
   "source": "array_aliasing",
   "edge": "mis:array_aliasing->AssignmentCopiesObject",
   "target": "AssignmentCopiesObject",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3,
    4
   ],
   "quote": "It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1",
   "confidence": 0.97,
   "prune_score": 1.0,
   "score": 0.97,
   "logic": "assigning a reference copies the object",
   "twin_logic": "b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i]."
  },
  {
   "depth": 1,
   "source": "array_aliasing",
   "edge": "lvl:array_aliasing@L0#0",
   "target": "array_aliasing@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2,
    3,
    4
   ],
   "quote": "It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1",
   "confidence": 0.9,
   "prune_score": 0.5,
   "score": 0.45,
   "logic": "Folk meaning: in maths and English, 'b = a' means b becomes an equal but independent copy, and 'a == b' means 'have the same values'. Java rule: for arrays, b = a copies only the reference, so both names denote one array, and == tests whether two names refer to the same array.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 1,
   "source": "indexing",
   "edge": "mis:indexing->ArrayIndexStartsAtOne",
   "target": "ArrayIndexStartsAtOne",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    4
   ],
   "quote": "It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1",
   "confidence": 0.75,
   "prune_score": 0.4,
   "score": 0.3,
   "logic": "The first element of a is a[1].",
   "twin_logic": "Numbering begins with 0; the first element is a[0]."
  },
  {
   "depth": 2,
   "source": "string_concatenation",
   "edge": "pre:string_concatenation->string_conversion",
   "target": "string_conversion",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "It prints 1 9",
   "confidence": 0.6,
   "prune_score": 1.0,
   "score": 0.6,
   "logic": "When one operand of + is a String, Java converts the other operand to a String before concatenating.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "string_conversion",
   "edge": "lvl:string_conversion@L2#0",
   "target": "string_conversion@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "It prints 1 9",
   "confidence": 0.55,
   "prune_score": 0.2,
   "score": 0.11,
   "logic": "Evaluate + operators left to right (same precedence, left-associative): at each +, if either current operand is a String, convert the other and concatenate; otherwise add numerically. Parenthesized parts are evaluated first.",
   "twin_logic": null,
   "level": "L2",
   "way": "line_by_line_trace"
  }
 ],
 "evidence": [
  {
   "depth": 1,
   "source": "array_aliasing",
   "edge": "mis:array_aliasing->AssignmentCopiesObject",
   "target": "AssignmentCopiesObject",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    1,
    2,
    3,
    4
   ],
   "quote": "It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1",
   "confidence": 0.97,
   "prune_score": 1.0,
   "score": 0.97,
   "logic": "assigning a reference copies the object",
   "twin_logic": "b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i]."
  },
  {
   "depth": 1,
   "source": "array_aliasing",
   "edge": "lvl:array_aliasing@L0#0",
   "target": "array_aliasing@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    2,
    3,
    4
   ],
   "quote": "It prints 1 9; The line b = a makes b a copy of a; so b is a separate array; Changing b[0] to 9 only changes b, and a[0] is still 1",
   "confidence": 0.9,
   "prune_score": 0.5,
   "score": 0.45,
   "logic": "Folk meaning: in maths and English, 'b = a' means b becomes an equal but independent copy, and 'a == b' means 'have the same values'. Java rule: for arrays, b = a copies only the reference, so both names denote one array, and == tests whether two names refer to the same array.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 1,
   "source": "indexing",
   "edge": "mis:indexing->ArrayIndexStartsAtOne",
   "target": "ArrayIndexStartsAtOne",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    4
   ],
   "quote": "It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1",
   "confidence": 0.75,
   "prune_score": 0.4,
   "score": 0.3,
   "logic": "The first element of a is a[1].",
   "twin_logic": "Numbering begins with 0; the first element is a[0]."
  },
  {
   "depth": 1,
   "source": "indexing",
   "edge": "mis:indexing->ElementNameIsWholeArray",
   "target": "ElementNameIsWholeArray",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    4
   ],
   "quote": "Changing b[0] to 9 only changes b, and a[0] is still 1",
   "confidence": 0.55,
   "prune_score": 0.35,
   "score": 0.1925,
   "logic": "X[i] names the whole array, not one element.",
   "twin_logic": "The array is a; a[i] is the single element at index i."
  },
  {
   "depth": 1,
   "source": "indexing",
   "edge": "lvl:indexing@L2#2",
   "target": "indexing@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    4
   ],
   "quote": "It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1",
   "confidence": 0.6,
   "prune_score": 0.45,
   "score": 0.27,
   "logic": "State transition: reading a[i] changes nothing. a[i] = v changes only element i (i, a and all other elements are unchanged), and a[i]++ adds 1 to that one element.",
   "twin_logic": null,
   "level": "L2",
   "way": "one_step_execution"
  },
  {
   "depth": 1,
   "source": "indexing",
   "edge": "lvl:indexing@L1#0",
   "target": "indexing@L1",
   "kind": "level",
   "label": "shown",
   "clauses": [
    4
   ],
   "quote": "Changing b[0] to 9 only changes b, and a[0] is still 1",
   "confidence": 0.6,
   "prune_score": 0.35,
   "score": 0.21,
   "logic": "Identity: an array access expression; a[i] names the single element variable at position i of the array a refers to.",
   "twin_logic": null,
   "level": "L1",
   "way": "names_the_element"
  },
  {
   "depth": 1,
   "source": "indexing",
   "edge": "lvl:indexing@L2#1",
   "target": "indexing@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    4
   ],
   "quote": "It prints 1 9; Changing b[0] to 9 only changes b, and a[0] is still 1",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "Result: a[i] has the element type and the value currently stored at position i. For int[] a = {5, 7, 9}, a[1] is 7 and a[0] + a[2] is 14.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 1,
   "source": "string_concatenation",
   "edge": "lvl:string_concatenation@L3#1",
   "target": "string_concatenation@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "It prints 1 9",
   "confidence": 0.55,
   "prune_score": 0.2,
   "score": 0.11,
   "logic": "The non-String operand is converted to its printed form (int 99 to \"99\", double 1.0 to \"1.0\", char 'a' to \"a\") before joining.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 2,
   "source": "string_concatenation",
   "edge": "pre:string_concatenation->string_conversion",
   "target": "string_conversion",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    1
   ],
   "quote": "It prints 1 9",
   "confidence": 0.6,
   "prune_score": 1.0,
   "score": 0.6,
   "logic": "When one operand of + is a String, Java converts the other operand to a String before concatenating.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "string_conversion",
   "edge": "lvl:string_conversion@L2#0",
   "target": "string_conversion@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1
   ],
   "quote": "It prints 1 9",
   "confidence": 0.55,
   "prune_score": 0.2,
   "score": 0.11,
   "logic": "Evaluate + operators left to right (same precedence, left-associative): at each +, if either current operand is a String, convert the other and concatenate; otherwise add numerically. Parenthesized parts are evaluated first.",
   "twin_logic": null,
   "level": "L2",
   "way": "line_by_line_trace"
  }
 ],
 "clause_coverage": {
  "It prints 1 9": "mis:array_aliasing->AssignmentCopiesObject",
  "The line b = a makes b a copy of a": "mis:array_aliasing->AssignmentCopiesObject",
  "so b is a separate array": "mis:array_aliasing->AssignmentCopiesObject",
  "Changing b[0] to 9 only changes b, and a[0] is still 1": "mis:array_aliasing->AssignmentCopiesObject"
 },
 "unexplained_clauses": [],
 "stop_reason": "sufficient",
 "depth_reached": 3,
 "llm_calls": 0,
 "llm_cache_hits": 26,
 "llm_calls_by_step": {
  "prune": 9,
  "label": 17
 }
}
```
