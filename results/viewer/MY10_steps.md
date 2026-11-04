# Think on the Graph: every output of the run MY10
## 0. Input
Program:
```java
int[] a = {5, 10, 15};
for (int i = 0; i <= a.length; i++) {
    System.out.println(a[i]);
}
```
Question: What does this program print, and why?

Student's answer: It prints 0, then 5, 10 and 15. Arrays start at a[1], so a[0] is before the first element and just gives 0. Then a[1], a[2] and a[3] are 5, 10 and 15.
Settings: width 3, depth 3, prune llm, backend claude-cli, model claude-opus-5-5
## 1. Stage 1: the subgraph G from the code (no model)
Masked code (string and char literals and comments blanked; this is what the patterns see):
```
int[] a = {5, 10, 15};
for (int i = 0; i <= a.length; i++) {
    System.out.println(a[i]);
}
```
Which code text tagged which concept (a generic concept fires on almost any Java line; it starts the walk only if the answer repeats its tag):
| concept | generic | channel | matched text | line |
|---|---|---|---|---|
| array_bounds | False | pattern | '<= a.length' | 2 |
| array_declaration | False | pattern | 'int[] a' | 1 |
| array_initializer | False | pattern | '= {' | 1 |
| array_traversal | False | pattern | 'for (int i = 0; i <= a.length' | 2 |
| array_traversal | False | pattern | 'for (int i = 0; i <= a.length; i++) {\n    System.out.println(a[i]' | 2 |
| assignment | True | pattern | '=' | 1 |
| boolean_expression | False | pattern | 'for (int i = 0; i <= a.length;' | 2 |
| comparison_operators | False | pattern | 'for (int i = 0; i <=' | 2 |
| control_flow | False | pattern | 'for (' | 2 |
| data_structure | False | pattern | 'int[]' | 1 |
| data_type | True | pattern | 'int' | 1 |
| expression | True | pattern | 'i <= a' | 2 |
| expression | True | pattern | '= {5, 10, 15};' | 1 |
| for_loop | False | pattern | 'for (' | 2 |
| increment_operators | False | pattern | '++' | 2 |
| indexing | False | pattern | 'a[i]' | 3 |
| length_field | False | pattern | '.length' | 2 |
| loop_body | False | pattern | 'for (' | 2 |
| loop_control | False | signal | 'for (int i = 0; i <= a.length; i++)' | 2 |
| loop_scope | False | pattern | 'for (int i' | 2 |
| loop_variable | False | pattern | 'for (int i =' | 2 |
| off_by_one_error | False | signal | 'for (int i = 0; i <= a.length' | 2 |
| println | False | pattern | 'System.out.println(' | 3 |
| run_time_error | False | pattern | '<= a.length' | 2 |
| statement | True | pattern | ';' | 1 |

G: 23 concept nodes (4 generic), 16 concept edges, 159 misconception / error edges, 116 misconception / error nodes, 115 level nodes, 173 level-misconception links, 8 connected piece(s).
Note: concept nodes form 8 pieces (the KG has no edge between them): array_bounds,array_traversal,assignment,boolean_expression,comparison_operators,expression,for_loop,increment_operators,indexing,loop_control,loop_scope,loop_variable,off_by_one_error | array_declaration | array_initializer | control_flow,println,statement | data_structure,data_type | length_field | loop_body | run_time_error

Concept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):
| edge | type | rule (logic) |
|---|---|---|
| par:assignment~comparison_operators | parallel | x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands. |
| pre:assignment->increment_operators | prerequisite | i++ is shorthand for the assignment i = i + 1. |
| pre:comparison_operators->boolean_expression | prerequisite | A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making. |
| pre:data_type->data_structure | prerequisite | A data structure organizes many values of a data type; the array holds a sequence of values of one type. |
| pre:expression->comparison_operators | prerequisite | Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b. |
| pre:for_loop->array_traversal | prerequisite | for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order. |
| pre:for_loop->loop_scope | prerequisite | A variable declared in the for header exists only from its declaration to the end of the for statement's block. |
| pre:indexing->array_bounds | prerequisite | Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used. |
| pre:indexing->array_traversal | prerequisite | A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass. |
| pre:indexing->off_by_one_error | prerequisite | Indices start at 0, so the last element is a[N-1]; misreading this convention is the usual source of off-by-one errors. |
| pre:loop_control->for_loop | prerequisite | The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |
| pre:loop_control->increment_operators | prerequisite | The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update. |
| pre:loop_control->off_by_one_error | prerequisite | The initialization and the condition of a loop fix how many times it runs; one wrong bound makes it run once too many or too few. |
| pre:loop_variable->loop_control | prerequisite | The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |
| pre:statement->control_flow | prerequisite | Control flow is the order in which statements run. |
| pre:statement->println | prerequisite | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |

Misconception / error edges per concept (count), and level ways per concept (count):
| concept | misconception / error edges | level ways (L1-L4 + L0 non-misconception) |
|---|---|---|
| array_bounds | 2 | 14 |
| array_declaration | 4 | 13 |
| array_initializer | 2 | 14 |
| array_traversal | 6 | 22 |
| assignment | 15 | 24 |
| boolean_expression | 8 | 19 |
| comparison_operators | 8 | 20 |
| control_flow | 11 | 15 |
| data_structure | 0 | 11 |
| data_type | 2 | 14 |
| expression | 8 | 19 |
| for_loop | 21 | 24 |
| increment_operators | 5 | 16 |
| indexing | 8 | 21 |
| length_field | 2 | 15 |
| loop_body | 12 | 14 |
| loop_control | 11 | 19 |
| loop_scope | 5 | 14 |
| loop_variable | 7 | 13 |
| off_by_one_error | 4 | 16 |
| println | 6 | 17 |
| run_time_error | 7 | 19 |
| statement | 5 | 19 |

Figure 1: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY10_figure01.png

Figure 2: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY10_figure02.png

## 2. Clauses and start concepts (no model)
The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):
| clause | text |
|---|---|
| c1 | It prints 0, then 5, 10 and 15 |
| c2 | Arrays start at a[1] |
| c3 | so a[0] is before the first element and just gives 0 |
| c4 | Then a[1], a[2] and a[3] are 5, 10 and 15 |

start: BM25 of the answer against each tagged concept: indexing 35.54 (hits 1), array_traversal 34.58 (hits 2), run_time_error 28.43 (hits 1), loop_control 26.24 (hits 1), off_by_one_error 25.47 (hits 1), array_bounds 24.89 (hits 1), array_declaration 21.43 (hits 1), for_loop 21.24 (hits 1), loop_body 20.32 (hits 1), println 19.62 (hits 1), increment_operators 17.90 (hits 1), array_initializer 16.65 (hits 1), length_field 15.96 (hits 1), loop_variable 13.95 (hits 1), control_flow 11.28 (hits 1), boolean_expression 10.07 (hits 1), comparison_operators 6.88 (hits 1), loop_scope 6.53 (hits 1), data_structure 1.11 (hits 1)

start: chosen indexing, array_traversal, run_time_error

start concepts (3): indexing, array_traversal, run_time_error

Start concepts: indexing, array_traversal, run_time_error

Figure 3: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY10_figure03.png

## 3. The walk, depth by depth
At each depth, for each current concept: the edges offered (a concept entering as a start concept offers its misconception / error edges and its level ways, as two families; otherwise it offers its concept edges), the prune prompt and the model's reply, then the label prompt(s) and the model's reply, parsed into label / clauses / confidence. Score = prune score x confidence.

### Depth 1: current concepts 'indexing', 'array_traversal', 'run_time_error'

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
mis:indexing->ArrayIndexStartsAtOne (0.65), mis:indexing->ArrayRangeInclusive (0.25), mis:indexing->ElementBoundToOldIndex (0.10)
```
Kept by pruning: mis:indexing->ArrayIndexStartsAtOne (0.65), mis:indexing->ArrayRangeInclusive (0.25), mis:indexing->ElementBoundToOldIndex (0.10)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:indexing->ArrayIndexStartsAtOne \| wrong rule: The first element of a is a[1]. \| right rule: Numbering begins with 0; the first element is a[0]. |
| mis:indexing->ArrayRangeInclusive \| wrong rule: new int[n] has slots 0 to n, inclusive. \| right rule: The slots are 0 to n - 1. |
| mis:indexing->ElementBoundToOldIndex \| wrong rule: After i changes, X[i] still refers to the element at the old value of i. \| right rule: a[i] is evaluated with the current value of i each time it is used. |
Model's reply:
```
mis:indexing->ArrayIndexStartsAtOne | held | clauses: 2, 3, 4 | confidence: 0.95
mis:indexing->ArrayRangeInclusive | not applied | clauses: none | confidence: 0.6
mis:indexing->ElementBoundToOldIndex | correct | clauses: 1, 4 | confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:indexing->ArrayIndexStartsAtOne | held | 0.65 | 0.95 | 0.62 | c2, c3, c4 | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| mis:indexing->ArrayRangeInclusive | not applied |  |  | 0.0 |  |  |
| mis:indexing->ElementBoundToOldIndex | correct | 0.1 | 0.6 | 0.06 | c1, c4 | It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15 |

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
{lvl:indexing@L0#0 (Score: 0.6)}
{lvl:indexing@L3#6 (Score: 0.25)}
{lvl:indexing@L4#2 (Score: 0.15)}
```
Kept by pruning: lvl:indexing@L0#0 (0.60), lvl:indexing@L3#6 (0.25), lvl:indexing@L4#2 (0.15)

Label prompt for level way lvl:indexing@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: everyday counting starts at 1 (first = number 1), maths subscripts a_1..a_n run from 1, and f(i) with parentheses means 'apply to i'. Java rule: a[i] uses square brackets and is 0-origin, so the first element is a[0] and the last is a[a.length-1].

Model's reply:
```
Label: shown
Clauses: 2, 3, 4
Confidence: 0.9
```

Label prompt for level way lvl:indexing@L3#6 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Indices start at 0, so the last element is a[N-1]; misreading this convention is the usual source of off-by-one errors.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:indexing@L4#2 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: The index must be in 0..a.length-1. Kind: run-time exception. Trigger class: index < 0 or >= a.length, e.g. a[a.length], a[i+1] on the last pass, a[i-1] at i = 0, a[0] of an empty array (ArrayIndexOutOfBoundsException)

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:indexing@L0#0 | shown | 0.6 | 0.9 | 0.54 | c2, c3, c4 | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| lvl:indexing@L3#6 | not applied |  |  | 0.0 |  |  |
| lvl:indexing@L4#2 | not applied |  |  | 0.0 |  |  |

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
mis:array_traversal->OffByOneBound (0.60), mis:array_traversal->IdiomOverridesCode (0.25), mis:array_traversal->ElementBoundToOldIndex (0.15)
```
Kept by pruning: mis:array_traversal->OffByOneBound (0.60), mis:array_traversal->IdiomOverridesCode (0.25), mis:array_traversal->ElementBoundToOldIndex (0.15)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:array_traversal->OffByOneBound \| wrong rule: < vs <= and 0..n vs 0..n-1 are interchangeable \| right rule: for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n. |
| mis:array_traversal->IdiomOverridesCode \| wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. |
| mis:array_traversal->ElementBoundToOldIndex \| wrong rule: After i changes, X[i] still refers to the element at the old value of i. \| right rule: a[i] is evaluated with the current value of i each time it is used. |
Model's reply:
```
mis:array_traversal->OffByOneBound | correct | clauses: 1, 3, 4 | confidence: 0.75
mis:array_traversal->IdiomOverridesCode | correct | clauses: 1, 3, 4 | confidence: 0.7
mis:array_traversal->ElementBoundToOldIndex | correct | clauses: 4 | confidence: 0.55
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:array_traversal->OffByOneBound | correct | 0.6 | 0.75 | 0.45 | c1, c3, c4 | It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| mis:array_traversal->IdiomOverridesCode | correct | 0.25 | 0.7 | 0.17 | c1, c3, c4 | It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| mis:array_traversal->ElementBoundToOldIndex | correct | 0.15 | 0.55 | 0.08 | c4 | Then a[1], a[2] and a[3] are 5, 10 and 15 |

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
{lvl:array_traversal@L4#3 (Score: 0.55)}
{lvl:array_traversal@L2#0 (Score: 0.25)}
{lvl:array_traversal@L3#0 (Score: 0.2)}
```
Kept by pruning: lvl:array_traversal@L4#3 (0.55), lvl:array_traversal@L2#0 (0.25), lvl:array_traversal@L3#0 (0.20)

Label prompt for level way lvl:array_traversal@L4#3 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: The guard must be i < a.length. Kind: run-time exception. Trigger class: i <= a.length (or a body that reads a[i+1]) makes the last pass index a.length (ArrayIndexOutOfBoundsException)

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Label prompt for level way lvl:array_traversal@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Sequencing: i = 0; test i < a.length; body using a[i]; i++; test; ... When i == a.length the test fails and the body is not executed, so a[a.length] is never touched.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.88
```

Label prompt for level way lvl:array_traversal@L3#0 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> The loop variable is used as the index, so a[i] reaches a different element on each pass.

Model's reply:
```
Label: shown
Clauses: 3, 4
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:array_traversal@L4#3 | not applied |  |  | 0.0 |  |  |
| lvl:array_traversal@L2#0 | not applied |  |  | 0.0 |  |  |
| lvl:array_traversal@L3#0 | shown | 0.2 | 0.7 | 0.14 | c3, c4 | so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |

#### run_time_error, misconceptions: 7 edges offered
Edges offered:
| edge |
|---|
| err:run_time_error->ArgsAlwaysPresent \| wrong rule: args[0] can always be read. \| right rule: If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0. |
| err:run_time_error->InputTypeMismatch \| wrong rule: StdIn.readInt() accepts any typed text such as abc or 12.2. \| right rule: If the next token is not an int (e.g. abc, 12.2, true), StdIn.readInt() throws a NumberFormatException at run time (Scanner.nextInt throws InputMismatchException). |
| err:run_time_error->MainWithoutStringArgs \| wrong rule: public static void main() is an acceptable entry point. \| right rule: main is written public static void main(String[] args); these keywords and the args parameter are required. |
| err:run_time_error->NegativeArraySize \| wrong rule: new int[n] with a negative n creates an empty array. \| right rule: Creating an array with a negative length throws NegativeArraySizeException at run time. |
| mis:run_time_error->CompilesMeansWorks \| wrong rule: Code that compiles is code that works. \| right rule: Code that compiles can still have run-time and logical errors. |
| mis:run_time_error->DivisionByZeroIsCompileError \| wrong rule: System.out.println(5 / 0); is rejected by the compiler. \| right rule: It compiles; the ArithmeticException happens when the program runs. |
| mis:run_time_error->ParseAnyString \| wrong rule: Integer.parseInt works on any text, e.g. "five" or "12.2". \| right rule: Integer.parseInt throws a NumberFormatException at run time when the string is not an integer written in digits. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:run_time_error->CompilesMeansWorks (0.50), err:run_time_error->ArgsAlwaysPresent (0.35), err:run_time_error->NegativeArraySize (0.15)
```
Kept by pruning: mis:run_time_error->CompilesMeansWorks (0.50), err:run_time_error->ArgsAlwaysPresent (0.35), err:run_time_error->NegativeArraySize (0.15)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:run_time_error->CompilesMeansWorks \| wrong rule: Code that compiles is code that works. \| right rule: Code that compiles can still have run-time and logical errors. |
| err:run_time_error->ArgsAlwaysPresent \| wrong rule: args[0] can always be read. \| right rule: If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0. |
| err:run_time_error->NegativeArraySize \| wrong rule: new int[n] with a negative n creates an empty array. \| right rule: Creating an array with a negative length throws NegativeArraySizeException at run time. |
Model's reply:
```
mis:run_time_error->CompilesMeansWorks | not applied | clauses: none | confidence: 0.6
err:run_time_error->ArgsAlwaysPresent | not applied | clauses: none | confidence: 0.95
err:run_time_error->NegativeArraySize | not applied | clauses: none | confidence: 0.97
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:run_time_error->CompilesMeansWorks | not applied |  |  | 0.0 |  |  |
| err:run_time_error->ArgsAlwaysPresent | not applied |  |  | 0.0 |  |  |
| err:run_time_error->NegativeArraySize | not applied |  |  | 0.0 |  |  |

#### run_time_error, level ways: 19 edges offered
Edges offered:
| edge |
|---|
| lvl:run_time_error@L0#0 \| level L0 way everyday_reading: Everyday reading: if the program compiled, the computer has accepted it, so any problem would have been reported then. Java rule: run-time errors are detected only while the program executes, on particular data (e.g. no argument, a divisor of 0), and stop it with an exception. |
| lvl:run_time_error@L0#3 \| level L0 way inconsistent_trace: Applies the exception rule (LT: execution stops at the faulty statement) unevenly: lets the program keep printing after the failing statement on one trace, or reports the error before any earlier output on another. (here mixing in: "Code that compiles is code that works") |
| lvl:run_time_error@L1#0 \| level L1 way names_the_element: A run-time error (exception) is an error that does not show up until the program is executed and makes it impossible to run to completion. |
| lvl:run_time_error@L1#1 \| level L1 way states_the_rule: When a run-time error occurs, the program 'crashes' (terminates) and the JVM prints the exception name, a message, and the method, file and line where it happened. |
| lvl:run_time_error@L2#0 \| level L2 way line_by_line_trace: Statements before the faulty one run normally (their output appears); the faulty statement throws; no later statement runs. |
| lvl:run_time_error@L2#1 \| level L2 way output_prediction: Output: any earlier output, then Exception in thread "main" java.lang.<Name>: <detail> at Class.main(Class.java:<line>). |
| lvl:run_time_error@L2#2 \| level L2 way one_step_execution: The throwing step changes no variable it was meant to set (the operation does not complete) and transfers control out of main, ending the program. |
| lvl:run_time_error@L3#0 \| level L3 way relation_to_neighbour: A run-time error appears only while java Name executes, after compiling has succeeded. |
| lvl:run_time_error@L3#1 \| level L3 way relation_to_neighbour: javac cannot detect it because it depends on run-time values (the argument typed, the divisor's value). |
| lvl:run_time_error@L3#2 \| level L3 way relation_to_neighbour: A run-time error stops the program with an exception message; a logic error lets it finish with wrong output and no message. |
| lvl:run_time_error@L3#3 \| level L3 way purpose_of_the_whole: Purpose (of exceptions): stop the program at the point where something impossible was asked, instead of continuing with an undefined value, and report what and where. |
| lvl:run_time_error@L4#0 \| level L4 way predict_a_change: The same compiled program may run fine on one input and throw on another (UseArgument with and without an argument); adding a guard such as checking args.length removes the trigger without changing correct runs. |
| lvl:run_time_error@L4#1 \| level L4 way diagnose_an_error: rule broken: main is written public static void main(String[] args). Kind: launch error. Trigger class: header public static void main(): compiles, but java Name cannot find the main method |
| lvl:run_time_error@L4#2 \| level L4 way diagnose_an_error: rule broken: Array length must be >= 0. Kind: run-time exception. Trigger class: new int[n] with n < 0: NegativeArraySizeException |
| lvl:run_time_error@L4#3 \| level L4 way diagnose_an_error: rule broken: args[k] exists only if at least k+1 arguments were typed. Kind: run-time exception. Trigger class: running without the expected argument: java.lang.ArrayIndexOutOfBoundsException: 0 |
| lvl:run_time_error@L4#4 \| level L4 way transfer_to_a_new_program: Expect a run-time error when correctness depends on data (array indices, divisors, parsed input, presence of arguments); validate such data before use. Errors that depend only on the text are compile-time; wrong-but-legal results are logic errors. |
| lvl:run_time_error@L4#5 \| level L4 way diagnose_an_error: rule broken: StdIn.readInt() needs the next token to be an int. Kind: run-time exception. Trigger class: next token abc, 12.2 or true (StdIn: InputMismatchException/NumberFormatException depending on version; Scanner.nextInt: InputMismatchException) |
| lvl:run_time_error@L4#6 \| level L4 way diagnose_an_error: rule broken: Integer division and remainder by zero are undefined. Kind: run-time exception. Trigger class: a / b or a % b with int b == 0: ArithmeticException: / by zero |
| lvl:run_time_error@L4#7 \| level L4 way diagnose_an_error: rule broken: Integer.parseInt needs an integer written in digits. Kind: run-time exception. Trigger class: parsing "five" or "12.2": NumberFormatException |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:run_time_error@L2#1 (Score: 0.4)}
{lvl:run_time_error@L0#0 (Score: 0.35)}
{lvl:run_time_error@L4#4 (Score: 0.25)}
```
Kept by pruning: lvl:run_time_error@L2#1 (0.40), lvl:run_time_error@L0#0 (0.35), lvl:run_time_error@L4#4 (0.25)

Label prompt for level way lvl:run_time_error@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> Output: any earlier output, then Exception in thread "main" java.lang.<Name>: <detail> at Class.main(Class.java:<line>).

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Label prompt for level way lvl:run_time_error@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Everyday reading: if the program compiled, the computer has accepted it, so any problem would have been reported then. Java rule: run-time errors are detected only while the program executes, on particular data (e.g. no argument, a divisor of 0), and stop it with an exception.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.75
```

Label prompt for level way lvl:run_time_error@L4#4 (the model saw only the concept, the way's name 'transfer to a new program' and its text; no level):
> Expect a run-time error when correctness depends on data (array indices, divisors, parsed input, presence of arguments); validate such data before use. Errors that depend only on the text are compile-time; wrong-but-legal results are logic errors.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:run_time_error@L2#1 | not applied |  |  | 0.0 |  |  |
| lvl:run_time_error@L0#0 | not applied |  |  | 0.0 |  |  |
| lvl:run_time_error@L4#4 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:indexing->ArrayIndexStartsAtOne [held, tier 0, 0.62], lvl:indexing@L0#0 [shown, tier 2, 0.54], mis:array_traversal->OffByOneBound [correct, tier 2, 0.45]

**Graph check, not yet read (the walk may not stop while these remain):** pre:for_loop->array_traversal, pre:indexing->array_bounds, pre:indexing->array_traversal, pre:indexing->off_by_one_error

Figure 4 (the graph after depth 1): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY10_figure04.png

### Depth 2: current concepts 'indexing', 'array_traversal'

#### indexing, concept edges: 3 edges offered
Edges offered:
| edge |
|---|
| pre:indexing->array_bounds \| rule: Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used. |
| pre:indexing->array_traversal \| rule: A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass. |
| pre:indexing->off_by_one_error \| rule: Indices start at 0, so the last element is a[N-1]; misreading this convention is the usual source of off-by-one errors. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:indexing->off_by_one_error (Score: 0.45)}
{pre:indexing->array_bounds (Score: 0.35)}
{pre:indexing->array_traversal (Score: 0.2)}
```
Kept by pruning: pre:indexing->off_by_one_error (0.45), pre:indexing->array_bounds (0.35), pre:indexing->array_traversal (0.20)

Label prompt for concept edge pre:indexing->off_by_one_error (indexing -> off_by_one_error, prerequisite):
> Indices start at 0, so the last element is a[N-1]; misreading this convention is the usual source of off-by-one errors.

Model's reply:
```
Label: broken
Clauses: 2, 3, 4
Confidence: 0.93
```

Label prompt for concept edge pre:indexing->array_bounds (indexing -> array_bounds, prerequisite):
> Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used.

Model's reply:
```
Label: broken
Clauses: 2, 3, 4
Confidence: 0.9
```

Label prompt for concept edge pre:indexing->array_traversal (indexing -> array_traversal, prerequisite):
> A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass.

Model's reply:
```
Label: confirmed
Clauses: 3, 4
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:indexing->off_by_one_error | broken | 0.45 | 0.93 | 0.42 | c2, c3, c4 | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| pre:indexing->array_bounds | broken | 0.35 | 0.9 | 0.32 | c2, c3, c4 | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| pre:indexing->array_traversal | confirmed | 0.2 | 0.6 | 0.12 | c3, c4 | so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |

#### array_traversal, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:for_loop->array_traversal \| rule: for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order. |
| pre:indexing->array_traversal \| rule: A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:for_loop->array_traversal (Score: 1.0)}
```
Kept by pruning: pre:for_loop->array_traversal (1.00)

Label prompt for concept edge pre:for_loop->array_traversal (for_loop -> array_traversal, prerequisite):
> for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order.

Model's reply:
```
Label: broken
Clauses: 1, 2, 3, 4
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:for_loop->array_traversal | broken | 1.0 | 0.85 | 0.85 | c1, c2, c3, c4 | It prints 0, then 5, 10 and 15; Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:for_loop->array_traversal [broken, tier 0, 0.85], pre:indexing->off_by_one_error [broken, tier 0, 0.42], pre:indexing->array_bounds [broken, tier 0, 0.32]

reached across pre:for_loop->array_traversal, entered next: for_loop

reached across pre:indexing->off_by_one_error, entered next: off_by_one_error

reached across pre:indexing->array_bounds, entered next: array_bounds

**Graph check, not yet read (the walk may not stop while these remain):** own edges of array_bounds, own edges of for_loop, own edges of off_by_one_error

Figure 5 (the graph after depth 2): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY10_figure05.png

### Depth 3: current concepts 'for_loop', 'array_traversal', 'off_by_one_error', 'indexing', 'array_bounds'

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
mis:for_loop->IdiomOverridesCode (0.45), err:for_loop->WrongIterationCount (0.35), mis:for_loop->ForLoopPartSkipped (0.20)
```
Kept by pruning: mis:for_loop->IdiomOverridesCode (0.45), err:for_loop->WrongIterationCount (0.35), mis:for_loop->ForLoopPartSkipped (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:for_loop->IdiomOverridesCode \| wrong rule: An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says. \| right rule: The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written. |
| err:for_loop->WrongIterationCount \| wrong rule: Updates the loop counter so that the loop runs the wrong number of times. \| right rule: The init, test and update together decide the number of passes; trace them to check the count. |
| mis:for_loop->ForLoopPartSkipped \| wrong rule: A pass of a loop may leave out one of its parts (the condition test, the body, the update, or the initialization). \| right rule: Each pass of a for loop runs test, then body, then update, every time; the initialization runs once, at the start. |
Model's reply:
```
mis:for_loop->IdiomOverridesCode | correct | clauses: 1, 3, 4 | confidence: 0.7
err:for_loop->WrongIterationCount | correct | clauses: 1, 4 | confidence: 0.6
mis:for_loop->ForLoopPartSkipped | not applied | clauses: none | confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:for_loop->IdiomOverridesCode | correct | 0.45 | 0.7 | 0.32 | c1, c3, c4 | It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| err:for_loop->WrongIterationCount | correct | 0.35 | 0.6 | 0.21 | c1, c4 | It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| mis:for_loop->ForLoopPartSkipped | not applied |  |  | 0.0 |  |  |

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
Clauses: 1, 3, 4
Confidence: 0.6
```

Label prompt for level way lvl:for_loop@L3#2 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> for (int i = 0; i < N; i++) gives i each valid index 0..N-1 exactly once in increasing order, the standard way to process every array element.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Label prompt for level way lvl:for_loop@L2#0 (the model saw only the concept, the way's name 'line by line trace' and its text; no level):
> Run the initializer once; then repeatedly: test the condition (stop if false), execute the body, run the update.

Model's reply:
```
Label: shown
Clauses: 1, 3, 4
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:for_loop@L2#1 | shown | 0.4 | 0.6 | 0.24 | c1, c3, c4 | It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| lvl:for_loop@L3#2 | not applied |  |  | 0.0 |  |  |
| lvl:for_loop@L2#0 | shown | 0.25 | 0.6 | 0.15 | c1, c3, c4 | It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |

#### array_traversal, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:for_loop->array_traversal \| rule: for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order. |
| pre:indexing->array_traversal \| rule: A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:for_loop->array_traversal (Score: 1.0)}
```
Kept by pruning: pre:indexing->array_traversal (1.00)

Label prompt for concept edge pre:indexing->array_traversal (indexing -> array_traversal, prerequisite):
> A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass.

Model's reply:
```
Label: confirmed
Clauses: 3, 4
Confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:indexing->array_traversal | confirmed | 1.0 | 0.6 | 0.6 | c3, c4 | so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |

#### off_by_one_error, misconceptions: 4 edges offered
Edges offered:
| edge |
|---|
| err:off_by_one_error->FencepostExtraSeparator \| wrong rule: Prints item and separator together in the loop, leaving an extra separator at the end. \| right rule: Handle one item outside the loop so n items get n - 1 separators. |
| err:off_by_one_error->WrongIterationCount \| wrong rule: Updates the loop counter so that the loop runs the wrong number of times. \| right rule: The init, test and update together decide the number of passes; trace them to check the count. |
| mis:off_by_one_error->DoubleLoopIndexCount \| wrong rule: for (double x = 0.0; x <= 1.0; x += 0.1) runs exactly 11 times. \| right rule: Using a double as a for-loop index is legal but bad practice: the number of iterations depends on an equality test between double values, which may not give the result you expect. |
| mis:off_by_one_error->OffByOneBound \| wrong rule: < vs <= and 0..n vs 0..n-1 are interchangeable \| right rule: for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:off_by_one_error->OffByOneBound (0.60), err:off_by_one_error->WrongIterationCount (0.35), err:off_by_one_error->FencepostExtraSeparator (0.05)
```
Kept by pruning: mis:off_by_one_error->OffByOneBound (0.60), err:off_by_one_error->WrongIterationCount (0.35), err:off_by_one_error->FencepostExtraSeparator (0.05)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:off_by_one_error->OffByOneBound \| wrong rule: < vs <= and 0..n vs 0..n-1 are interchangeable \| right rule: for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n. |
| err:off_by_one_error->WrongIterationCount \| wrong rule: Updates the loop counter so that the loop runs the wrong number of times. \| right rule: The init, test and update together decide the number of passes; trace them to check the count. |
| err:off_by_one_error->FencepostExtraSeparator \| wrong rule: Prints item and separator together in the loop, leaving an extra separator at the end. \| right rule: Handle one item outside the loop so n items get n - 1 separators. |
Model's reply:
```
mis:off_by_one_error->OffByOneBound | correct | clauses: 1, 4 | confidence: 0.6
err:off_by_one_error->WrongIterationCount | correct | clauses: 1, 4 | confidence: 0.55
err:off_by_one_error->FencepostExtraSeparator | not applied | clauses: none | confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:off_by_one_error->OffByOneBound | correct | 0.6 | 0.6 | 0.36 | c1, c4 | It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| err:off_by_one_error->WrongIterationCount | correct | 0.35 | 0.55 | 0.19 | c1, c4 | It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| err:off_by_one_error->FencepostExtraSeparator | not applied |  |  | 0.0 |  |  |

#### off_by_one_error, level ways: 16 edges offered
Edges offered:
| edge |
|---|
| lvl:off_by_one_error@L0#0 \| level L0 way everyday_reading: Everyday counting starts at 1 and 'up to N' includes N. Java arrays start at index 0 and end at N-1, and a loop with i < N runs N times while i <= N runs N+1 times. |
| lvl:off_by_one_error@L0#2 \| level L0 way inconsistent_trace: Applies the bound rule unevenly: writes i < a.length in one loop and i <= a.length in the next one over the same array. (here mixing in: "< vs <= and 0..n vs 0..n-1 are interchangeable") |
| lvl:off_by_one_error@L1#0 \| level L1 way names_the_element: Off-by-one error: a loop or index that is one step too far or too short. |
| lvl:off_by_one_error@L1#1 \| level L1 way states_the_rule: Indices run from 0 to N-1; a loop for (int i = 0; i < N; i++) runs exactly N times. Misunderstanding the 0-based convention leads to off-by-one errors, which are hard to avoid and debug. |
| lvl:off_by_one_error@L2#0 \| level L2 way line_by_line_trace: Sequencing: to check a bound, trace the first pass (the start value) and the last pass (the value that makes the condition false), not only a middle pass. |
| lvl:off_by_one_error@L2#1 \| level L2 way output_prediction: Result: for (i = 0; i < 5; i++) gives i = 0..4, five passes; i <= 5 gives six passes, and a[5] on an array of length 5 throws ArrayIndexOutOfBoundsException. |
| lvl:off_by_one_error@L2#2 \| level L2 way one_step_execution: State transition: one extra pass reads or writes one element past the end (an exception) or adds one term too many; one missing pass leaves the last element unprocessed. |
| lvl:off_by_one_error@L3#0 \| level L3 way relation_to_neighbour: Because indexing starts at 0, the last valid index is length-1, and that is the bound most often missed by one. |
| lvl:off_by_one_error@L3#1 \| level L3 way relation_to_neighbour: The start value and the condition together fix the number of passes; changing either by one changes the count by one. |
| lvl:off_by_one_error@L3#2 \| level L3 way relation_to_neighbour: When one action must happen once more (or less) than the other, the fencepost plan handles the extra case explicitly instead of risking an off-by-one. |
| lvl:off_by_one_error@L3#3 \| level L3 way purpose_of_the_whole: Plan: choose the bounds from the meaning (count N things, valid indices 0..N-1) and check the first and last pass, rather than guessing. |
| lvl:off_by_one_error@L4#0 \| level L4 way predict_a_change: Conservation: changing < to <= adds exactly one pass; starting at 1 instead of 0 removes exactly one; both keep the loop otherwise the same. |
| lvl:off_by_one_error@L4#1 \| level L4 way diagnose_an_error: rule broken: The init, test and update together decide the number of passes; trace them to check the count. Kind: see node. Trigger class: see node |
| lvl:off_by_one_error@L4#2 \| level L4 way transfer_to_a_new_program: Whenever writing a loop over a range or an array, write the bound from the count (i < N for N passes from 0) and check the first and last values of the index by hand. |
| lvl:off_by_one_error@L4#3 \| level L4 way diagnose_an_error: rule broken: A traversal of an array of length N must use indices 0..N-1. Kind: run-time exception. Trigger class: i <= a.length, a[i+1] on the last pass, or a[i-1] at i = 0 (ArrayIndexOutOfBoundsException) |
| lvl:off_by_one_error@L4#4 \| level L4 way diagnose_an_error: rule broken: A loop meant to run N times must run exactly N times. Kind: silent logic error. Trigger class: the loop stops one short or goes one too far, so the last element is skipped or one term too many is added |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:off_by_one_error@L0#0 (Score: 0.6)}
{lvl:off_by_one_error@L4#3 (Score: 0.25)}
{lvl:off_by_one_error@L3#0 (Score: 0.15)}
```
Kept by pruning: lvl:off_by_one_error@L0#0 (0.60), lvl:off_by_one_error@L4#3 (0.25), lvl:off_by_one_error@L3#0 (0.15)

Label prompt for level way lvl:off_by_one_error@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Everyday counting starts at 1 and 'up to N' includes N. Java arrays start at index 0 and end at N-1, and a loop with i < N runs N times while i <= N runs N+1 times.

Model's reply:
```
Label: shown
Clauses: 2, 3, 4
Confidence: 0.7
```

Label prompt for level way lvl:off_by_one_error@L4#3 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: A traversal of an array of length N must use indices 0..N-1. Kind: run-time exception. Trigger class: i <= a.length, a[i+1] on the last pass, or a[i-1] at i = 0 (ArrayIndexOutOfBoundsException)

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Label prompt for level way lvl:off_by_one_error@L3#0 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Because indexing starts at 0, the last valid index is length-1, and that is the bound most often missed by one.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:off_by_one_error@L0#0 | shown | 0.6 | 0.7 | 0.42 | c2, c3, c4 | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| lvl:off_by_one_error@L4#3 | not applied |  |  | 0.0 |  |  |
| lvl:off_by_one_error@L3#0 | not applied |  |  | 0.0 |  |  |

#### array_bounds, misconceptions: 2 edges offered
Edges offered:
| edge |
|---|
| mis:array_bounds->OffByOneBound \| wrong rule: < vs <= and 0..n vs 0..n-1 are interchangeable \| right rule: for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n. |
| mis:array_bounds->OutOfBoundsElementsAreNull \| wrong rule: Reading a[a.length] just gives null or 0. \| right rule: Reading any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:array_bounds->OutOfBoundsElementsAreNull (Score: 0.65)}
{mis:array_bounds->OffByOneBound (Score: 0.35)}
```
Kept by pruning: mis:array_bounds->OutOfBoundsElementsAreNull (0.65), mis:array_bounds->OffByOneBound (0.35)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:array_bounds->OutOfBoundsElementsAreNull \| wrong rule: Reading a[a.length] just gives null or 0. \| right rule: Reading any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException. |
| mis:array_bounds->OffByOneBound \| wrong rule: < vs <= and 0..n vs 0..n-1 are interchangeable \| right rule: for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n. |
Model's reply:
```
mis:array_bounds->OutOfBoundsElementsAreNull | held | clauses: 2, 3 | confidence: 0.7
mis:array_bounds->OffByOneBound | correct | clauses: 1, 4 | confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:array_bounds->OutOfBoundsElementsAreNull | held | 0.65 | 0.7 | 0.45 | c2, c3 | Arrays start at a[1]; so a[0] is before the first element and just gives 0 |
| mis:array_bounds->OffByOneBound | correct | 0.35 | 0.7 | 0.24 | c1, c4 | It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15 |

#### array_bounds, level ways: 14 edges offered
Edges offered:
| edge |
|---|
| lvl:array_bounds@L0#0 \| level L0 way everyday_reading: Folk meaning: in English, 'items 1 to 10' or 'up to n' includes the end point, and reading past the end of a list just gives 'nothing'. Java rule: the legal indices are 0..length-1, and any other index throws ArrayIndexOutOfBoundsException instead of returning a value. |
| lvl:array_bounds@L0#2 \| level L0 way inconsistent_trace: Points to LT: the bounds check runs at every access, at run time. Inconsistent application: the trace accepts an index of a.length on the last pass (or -1 on the first) but rejects it elsewhere, or reads 'some value' there. (here mixing in: "an out-of-bounds read returns null (it throws)") |
| lvl:array_bounds@L1#0 \| level L1 way names_the_element: Identity: the bounds of an array are its legal index range, 0 to length-1. |
| lvl:array_bounds@L1#1 \| level L1 way states_the_rule: Declarative: an index less than 0 or greater than length-1 makes the program terminate with an ArrayIndexOutOfBoundsException; it is the programmer's responsibility to use legal indices. |
| lvl:array_bounds@L2#0 \| level L2 way line_by_line_trace: Sequencing: at each access the index expression is evaluated first and then compared with 0 and a.length. Only if it is in range is the element read or written; otherwise the exception is thrown before any element changes. |
| lvl:array_bounds@L2#1 \| level L2 way output_prediction: Result: a legal access yields the element. An illegal one yields no value; the program stops with ArrayIndexOutOfBoundsException naming the bad index (old JVMs print ': 10', current ones 'Index 10 out of bounds for length 10'). |
| lvl:array_bounds@L2#2 \| level L2 way one_step_execution: State transition: an out-of-bounds write changes no element, because the exception is raised before the store. Control leaves the statement, and main terminates unless the exception is caught. |
| lvl:array_bounds@L3#0 \| level L3 way relation_to_neighbour: Every index value used in a[i] must satisfy 0 <= i <= a.length-1; the last element is a[a.length-1]. |
| lvl:array_bounds@L3#1 \| level L3 way relation_to_neighbour: Because an out-of-bounds index stops the program, the loop test checks the bounds before the body uses the index (e.g. x > 0 && x < N-1 before a[x-1], a[x+1]). |
| lvl:array_bounds@L3#2 \| level L3 way purpose_of_the_whole: Plan/role: run-time bounds checking makes an indexing mistake a visible error instead of silent memory corruption (buffer overflow). |
| lvl:array_bounds@L4#0 \| level L4 way predict_a_change: Conservation: a loop bounded by i < a.length stays within bounds when the array size changes. Changing < to <= adds one pass that throws, and starting at 1 or ending at a.length-1 silently skips an element. |
| lvl:array_bounds@L4#1 \| level L4 way transfer_to_a_new_program: Applicability: check indices explicitly (or restrict the loop range) whenever an index is computed from data, a random number or a neighbour (i-1, i+1). A plain i < a.length traversal or an enhanced for loop needs no extra check. |
| lvl:array_bounds@L4#2 \| level L4 way diagnose_an_error: rule broken: Indices must be in 0..a.length-1. Kind: run-time exception. Trigger class: index >= a.length or < 0: i <= a.length, a[i+1] on the last pass, a[i-1] at i = 0, a[0] on an empty array, or the Sample program run with M > N (ArrayIndexOutOfBoundsException) |
| lvl:array_bounds@L4#3 \| level L4 way diagnose_an_error: rule broken: A traversal must reach the last valid index a.length-1. Kind: silent logic error. Trigger class: the loop stops one short (i < a.length-1) or starts at 1, so the last or first element is never processed |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:array_bounds@L0#0 (Score: 0.5)}
{lvl:array_bounds@L0#2 (Score: 0.3)}
{lvl:array_bounds@L3#0 (Score: 0.2)}
```
Kept by pruning: lvl:array_bounds@L0#0 (0.50), lvl:array_bounds@L0#2 (0.30), lvl:array_bounds@L3#0 (0.20)

Label prompt for level way lvl:array_bounds@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: in English, 'items 1 to 10' or 'up to n' includes the end point, and reading past the end of a list just gives 'nothing'. Java rule: the legal indices are 0..length-1, and any other index throws ArrayIndexOutOfBoundsException instead of returning a value.

Model's reply:
```
Label: shown
Clauses: 2, 3, 4
Confidence: 0.8
```

Label prompt for level way lvl:array_bounds@L0#2 (the model saw only the concept, the way's name 'inconsistent trace' and its text; no level):
> Points to LT: the bounds check runs at every access, at run time. Inconsistent application: the trace accepts an index of a.length on the last pass (or -1 on the first) but rejects it elsewhere, or reads 'some value' there. (here mixing in: "an out-of-bounds read returns null (it throws)")

Model's reply:
```
Label: shown
Clauses: 1, 3, 4
Confidence: 0.6
```

Label prompt for level way lvl:array_bounds@L3#0 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Every index value used in a[i] must satisfy 0 <= i <= a.length-1; the last element is a[a.length-1].

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.93
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:array_bounds@L0#0 | shown | 0.5 | 0.8 | 0.4 | c2, c3, c4 | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| lvl:array_bounds@L0#2 | shown | 0.3 | 0.6 | 0.18 | c1, c3, c4 | It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| lvl:array_bounds@L3#0 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:array_bounds->OutOfBoundsElementsAreNull [held, tier 0, 0.46], pre:indexing->array_traversal [confirmed, tier 2, 0.60], lvl:off_by_one_error@L0#0 [shown, tier 2, 0.42]

**Graph check, not yet read (the walk may not stop while these remain):** pre:for_loop->loop_scope, pre:loop_control->for_loop, pre:loop_control->off_by_one_error

Figure 6 (the graph after depth 3): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY10_figure06.png

## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on ['array_bounds', 'indexing'], broken at [] (consequences: pre:for_loop->array_traversal, pre:indexing->off_by_one_error, pre:indexing->array_bounds), prerequisites {'increment_operators': ['assignment', 'loop_control'], 'boolean_expression': ['comparison_operators'], 'data_structure': ['data_type'], 'comparison_operators': ['expression'], 'array_traversal': ['for_loop', 'indexing'], 'loop_scope': ['for_loop'], 'array_bounds': ['indexing'], 'off_by_one_error': ['indexing', 'loop_control'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable'], 'control_flow': ['statement'], 'println': ['statement']}
- array_bounds: L0 via misconception "Arrays start at a[1]; so a[0] is before the first element and just gives 0"
- array_traversal: L3 via relation_to_neighbour "so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
- for_loop: L2 via output_prediction "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
- indexing: L0 via misconception "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
- off_by_one_error: L0 via everyday_reading "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"

**Stop:** max depth at depth 3; prompts {'prune': 15, 'label': 29}, fresh model calls 0, cache hits 44

### Held misconceptions
| concept | misconception | kind | quote | score | shares_evidence_with |
|---|---|---|---|---|---|
| indexing | ArrayIndexStartsAtOne | misconception | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 | 0.6175 |  |
| array_bounds | OutOfBoundsElementsAreNull | misconception | Arrays start at a[1]; so a[0] is before the first element and just gives 0 | 0.455 |  |

### Broken concept edges
| edge | quote | score | consequence_of |
|---|---|---|---|
| pre:for_loop->array_traversal | It prints 0, then 5, 10 and 15; Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 | 0.85 | mis:indexing->ArrayIndexStartsAtOne |
| pre:indexing->off_by_one_error | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 | 0.4185 | mis:indexing->ArrayIndexStartsAtOne |
| pre:indexing->array_bounds | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 | 0.315 | mis:indexing->ArrayIndexStartsAtOne |

### Root cause: indexing / ArrayIndexStartsAtOne

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| array_bounds | L0 | misconception | OutOfBoundsElementsAreNull | level_mis_links | Arrays start at a[1]; so a[0] is before the first element and just gives 0 | wrong rule: An out-of-bounds read returns null (or 0). Right rule: Reading or writing any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException and returns no value. |  |  |
| array_traversal | L3 | relation_to_neighbour |  | level_way | so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |  |  |  |
| for_loop | L2 | output_prediction |  | level_way | It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |  | L2 line_by_line_trace |  |
| indexing | L0 | misconception | ArrayIndexStartsAtOne | level_mis_links | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 | wrong rule: The first element of a is a[1]. Right rule: Numbering begins with 0; the first element is a[0]. |  |  |
| off_by_one_error | L0 | everyday_reading |  | level_way | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |  |  |  |

### Overall level: L0

Clause coverage (final):
| clause | covered by |
|---|---|
| It prints 0, then 5, 10 and 15 | mis:indexing->ElementBoundToOldIndex |
| Arrays start at a[1] | mis:indexing->ArrayIndexStartsAtOne |
| so a[0] is before the first element and just gives 0 | mis:indexing->ArrayIndexStartsAtOne |
| Then a[1], a[2] and a[3] are 5, 10 and 15 | mis:indexing->ArrayIndexStartsAtOne |

Figure 7 (final picture): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY10_figure07.png

## 5. Every labelled edge (the evidence list, kept or not)
| depth | source | edge | kind | label | prune_score | confidence | score | clauses | quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | indexing | mis:indexing->ArrayIndexStartsAtOne | misconception | held | 0.65 | 0.95 | 0.6175 | [2, 3, 4] | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 1 | indexing | mis:indexing->ElementBoundToOldIndex | misconception | correct | 0.1 | 0.6 | 0.06 | [1, 4] | It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 1 | indexing | lvl:indexing@L0#0 | level | shown | 0.6 | 0.9 | 0.54 | [2, 3, 4] | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 1 | array_traversal | mis:array_traversal->OffByOneBound | misconception | correct | 0.6 | 0.75 | 0.45 | [1, 3, 4] | It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 1 | array_traversal | mis:array_traversal->IdiomOverridesCode | misconception | correct | 0.25 | 0.7 | 0.175 | [1, 3, 4] | It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 1 | array_traversal | mis:array_traversal->ElementBoundToOldIndex | misconception | correct | 0.15 | 0.55 | 0.0825 | [4] | Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 1 | array_traversal | lvl:array_traversal@L3#0 | level | shown | 0.2 | 0.7 | 0.14 | [3, 4] | so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 2 | indexing | pre:indexing->off_by_one_error | prerequisite | broken | 0.45 | 0.93 | 0.4185 | [2, 3, 4] | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 2 | indexing | pre:indexing->array_bounds | prerequisite | broken | 0.35 | 0.9 | 0.315 | [2, 3, 4] | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 2 | indexing | pre:indexing->array_traversal | prerequisite | confirmed | 0.2 | 0.6 | 0.12 | [3, 4] | so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 2 | array_traversal | pre:for_loop->array_traversal | prerequisite | broken | 1.0 | 0.85 | 0.85 | [1, 2, 3, 4] | It prints 0, then 5, 10 and 15; Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 3 | for_loop | mis:for_loop->IdiomOverridesCode | misconception | correct | 0.45 | 0.7 | 0.315 | [1, 3, 4] | It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 3 | for_loop | err:for_loop->WrongIterationCount | error | correct | 0.35 | 0.6 | 0.21 | [1, 4] | It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 3 | for_loop | lvl:for_loop@L2#1 | level | shown | 0.4 | 0.6 | 0.24 | [1, 3, 4] | It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 3 | for_loop | lvl:for_loop@L2#0 | level | shown | 0.25 | 0.6 | 0.15 | [1, 3, 4] | It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 3 | array_traversal | pre:indexing->array_traversal | prerequisite | confirmed | 1.0 | 0.6 | 0.6 | [3, 4] | so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 3 | off_by_one_error | mis:off_by_one_error->OffByOneBound | misconception | correct | 0.6 | 0.6 | 0.36 | [1, 4] | It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 3 | off_by_one_error | err:off_by_one_error->WrongIterationCount | error | correct | 0.35 | 0.55 | 0.1925 | [1, 4] | It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 3 | off_by_one_error | lvl:off_by_one_error@L0#0 | level | shown | 0.6 | 0.7 | 0.42 | [2, 3, 4] | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 3 | array_bounds | mis:array_bounds->OutOfBoundsElementsAreNull | misconception | held | 0.65 | 0.7 | 0.455 | [2, 3] | Arrays start at a[1]; so a[0] is before the first element and just gives 0 |
| 3 | array_bounds | mis:array_bounds->OffByOneBound | misconception | correct | 0.35 | 0.7 | 0.245 | [1, 4] | It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 3 | array_bounds | lvl:array_bounds@L0#0 | level | shown | 0.5 | 0.8 | 0.4 | [2, 3, 4] | Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |
| 3 | array_bounds | lvl:array_bounds@L0#2 | level | shown | 0.3 | 0.6 | 0.18 | [1, 3, 4] | It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15 |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | indexing | mis:indexing->ArrayIndexStartsAtOne | misconception | held | 0.6175 | [2, 3, 4] |
| 1 | indexing | lvl:indexing@L0#0 | level | shown | 0.54 | [2, 3, 4] |
| 1 | array_traversal | mis:array_traversal->OffByOneBound | misconception | correct | 0.45 | [1, 3, 4] |
| 2 | array_traversal | pre:for_loop->array_traversal | prerequisite | broken | 0.85 | [1, 2, 3, 4] |
| 2 | indexing | pre:indexing->off_by_one_error | prerequisite | broken | 0.4185 | [2, 3, 4] |
| 2 | indexing | pre:indexing->array_bounds | prerequisite | broken | 0.315 | [2, 3, 4] |
| 3 | array_bounds | mis:array_bounds->OutOfBoundsElementsAreNull | misconception | held | 0.455 | [2, 3] |
| 3 | array_traversal | pre:indexing->array_traversal | prerequisite | confirmed | 0.6 | [3, 4] |
| 3 | off_by_one_error | lvl:off_by_one_error@L0#0 | level | shown | 0.42 | [2, 3, 4] |

## 7. Raw traversal log
```
clauses: It prints 0, then 5, 10 and 15 | Arrays start at a[1] | so a[0] is before the first element and just gives 0 | Then a[1], a[2] and a[3] are 5, 10 and 15
start: BM25 of the answer against each tagged concept: indexing 35.54 (hits 1), array_traversal 34.58 (hits 2), run_time_error 28.43 (hits 1), loop_control 26.24 (hits 1), off_by_one_error 25.47 (hits 1), array_bounds 24.89 (hits 1), array_declaration 21.43 (hits 1), for_loop 21.24 (hits 1), loop_body 20.32 (hits 1), println 19.62 (hits 1), increment_operators 17.90 (hits 1), array_initializer 16.65 (hits 1), length_field 15.96 (hits 1), loop_variable 13.95 (hits 1), control_flow 11.28 (hits 1), boolean_expression 10.07 (hits 1), comparison_operators 6.88 (hits 1), loop_scope 6.53 (hits 1), data_structure 1.11 (hits 1)
start: chosen indexing, array_traversal, run_time_error
start concepts (3): indexing, array_traversal, run_time_error
--- depth 1: current concepts ['indexing', 'array_traversal', 'run_time_error']
  indexing (misconceptions): 8 candidates -> kept mis:indexing->ArrayIndexStartsAtOne (0.65), mis:indexing->ArrayRangeInclusive (0.25), mis:indexing->ElementBoundToOldIndex (0.10)
    mis:indexing->ArrayIndexStartsAtOne -> held (0.62) "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
    mis:indexing->ArrayRangeInclusive -> not applied (0.00) ""
    mis:indexing->ElementBoundToOldIndex -> correct (0.06) "It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15"
  indexing (level ways): 21 candidates -> kept lvl:indexing@L0#0 (0.60), lvl:indexing@L3#6 (0.25), lvl:indexing@L4#2 (0.15)
    lvl:indexing@L0#0 -> shown (0.54) "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
    lvl:indexing@L3#6 -> not applied (0.00) ""
    lvl:indexing@L4#2 -> not applied (0.00) ""
  array_traversal (misconceptions): 6 candidates -> kept mis:array_traversal->OffByOneBound (0.60), mis:array_traversal->IdiomOverridesCode (0.25), mis:array_traversal->ElementBoundToOldIndex (0.15)
    mis:array_traversal->OffByOneBound -> correct (0.45) "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
    mis:array_traversal->IdiomOverridesCode -> correct (0.17) "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
    mis:array_traversal->ElementBoundToOldIndex -> correct (0.08) "Then a[1], a[2] and a[3] are 5, 10 and 15"
  array_traversal (level ways): 22 candidates -> kept lvl:array_traversal@L4#3 (0.55), lvl:array_traversal@L2#0 (0.25), lvl:array_traversal@L3#0 (0.20)
    lvl:array_traversal@L4#3 -> not applied (0.00) ""
    lvl:array_traversal@L2#0 -> not applied (0.00) ""
    lvl:array_traversal@L3#0 -> shown (0.14) "so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
  run_time_error (misconceptions): 7 candidates -> kept mis:run_time_error->CompilesMeansWorks (0.50), err:run_time_error->ArgsAlwaysPresent (0.35), err:run_time_error->NegativeArraySize (0.15)
    mis:run_time_error->CompilesMeansWorks -> not applied (0.00) ""
    err:run_time_error->ArgsAlwaysPresent -> not applied (0.00) ""
    err:run_time_error->NegativeArraySize -> not applied (0.00) ""
  run_time_error (level ways): 19 candidates -> kept lvl:run_time_error@L2#1 (0.40), lvl:run_time_error@L0#0 (0.35), lvl:run_time_error@L4#4 (0.25)
    lvl:run_time_error@L2#1 -> not applied (0.00) ""
    lvl:run_time_error@L0#0 -> not applied (0.00) ""
    lvl:run_time_error@L4#4 -> not applied (0.00) ""
  kept: mis:indexing->ArrayIndexStartsAtOne [held, tier 0, 0.62], lvl:indexing@L0#0 [shown, tier 2, 0.54], mis:array_traversal->OffByOneBound [correct, tier 2, 0.45]
  clause coverage (rule edges): c1 <- mis:indexing->ElementBoundToOldIndex; c2 <- mis:indexing->ArrayIndexStartsAtOne; c3 <- mis:indexing->ArrayIndexStartsAtOne; c4 <- mis:indexing->ArrayIndexStartsAtOne
  not yet read: pre:for_loop->array_traversal, pre:indexing->array_bounds, pre:indexing->array_traversal, pre:indexing->off_by_one_error
--- depth 2: current concepts ['indexing', 'array_traversal']
  indexing (concept edges): 3 candidates -> kept pre:indexing->off_by_one_error (0.45), pre:indexing->array_bounds (0.35), pre:indexing->array_traversal (0.20)
    pre:indexing->off_by_one_error -> broken (0.42) "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
    pre:indexing->array_bounds -> broken (0.32) "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
    pre:indexing->array_traversal -> confirmed (0.12) "so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
  array_traversal (concept edges): 1 candidates -> kept pre:for_loop->array_traversal (1.00)
    pre:for_loop->array_traversal -> broken (0.85) "It prints 0, then 5, 10 and 15; Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
  kept: pre:for_loop->array_traversal [broken, tier 0, 0.85], pre:indexing->off_by_one_error [broken, tier 0, 0.42], pre:indexing->array_bounds [broken, tier 0, 0.32]
  reached across pre:for_loop->array_traversal, entered next: for_loop
  reached across pre:indexing->off_by_one_error, entered next: off_by_one_error
  reached across pre:indexing->array_bounds, entered next: array_bounds
  clause coverage (rule edges): c1 <- mis:indexing->ElementBoundToOldIndex; c2 <- mis:indexing->ArrayIndexStartsAtOne; c3 <- mis:indexing->ArrayIndexStartsAtOne; c4 <- mis:indexing->ArrayIndexStartsAtOne
  not yet read: own edges of array_bounds, own edges of for_loop, own edges of off_by_one_error
--- depth 3: current concepts ['for_loop', 'array_traversal', 'off_by_one_error', 'indexing', 'array_bounds']
  for_loop (misconceptions): 21 candidates -> kept mis:for_loop->IdiomOverridesCode (0.45), err:for_loop->WrongIterationCount (0.35), mis:for_loop->ForLoopPartSkipped (0.20)
    mis:for_loop->IdiomOverridesCode -> correct (0.32) "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
    err:for_loop->WrongIterationCount -> correct (0.21) "It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15"
    mis:for_loop->ForLoopPartSkipped -> not applied (0.00) ""
  for_loop (level ways): 24 candidates -> kept lvl:for_loop@L2#1 (0.40), lvl:for_loop@L3#2 (0.35), lvl:for_loop@L2#0 (0.25)
    lvl:for_loop@L2#1 -> shown (0.24) "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
    lvl:for_loop@L3#2 -> not applied (0.00) ""
    lvl:for_loop@L2#0 -> shown (0.15) "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
  array_traversal (concept edges): 1 candidates -> kept pre:indexing->array_traversal (1.00)
    pre:indexing->array_traversal -> confirmed (0.60) "so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
  off_by_one_error (misconceptions): 4 candidates -> kept mis:off_by_one_error->OffByOneBound (0.60), err:off_by_one_error->WrongIterationCount (0.35), err:off_by_one_error->FencepostExtraSeparator (0.05)
    mis:off_by_one_error->OffByOneBound -> correct (0.36) "It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15"
    err:off_by_one_error->WrongIterationCount -> correct (0.19) "It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15"
    err:off_by_one_error->FencepostExtraSeparator -> not applied (0.00) ""
  off_by_one_error (level ways): 16 candidates -> kept lvl:off_by_one_error@L0#0 (0.60), lvl:off_by_one_error@L4#3 (0.25), lvl:off_by_one_error@L3#0 (0.15)
    lvl:off_by_one_error@L0#0 -> shown (0.42) "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
    lvl:off_by_one_error@L4#3 -> not applied (0.00) ""
    lvl:off_by_one_error@L3#0 -> not applied (0.00) ""
  array_bounds (misconceptions): 2 candidates -> kept mis:array_bounds->OutOfBoundsElementsAreNull (0.65), mis:array_bounds->OffByOneBound (0.35)
    mis:array_bounds->OutOfBoundsElementsAreNull -> held (0.45) "Arrays start at a[1]; so a[0] is before the first element and just gives 0"
    mis:array_bounds->OffByOneBound -> correct (0.24) "It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15"
  array_bounds (level ways): 14 candidates -> kept lvl:array_bounds@L0#0 (0.50), lvl:array_bounds@L0#2 (0.30), lvl:array_bounds@L3#0 (0.20)
    lvl:array_bounds@L0#0 -> shown (0.40) "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
    lvl:array_bounds@L0#2 -> shown (0.18) "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
    lvl:array_bounds@L3#0 -> not applied (0.00) ""
  kept: mis:array_bounds->OutOfBoundsElementsAreNull [held, tier 0, 0.46], pre:indexing->array_traversal [confirmed, tier 2, 0.60], lvl:off_by_one_error@L0#0 [shown, tier 2, 0.42]
  clause coverage (rule edges): c1 <- mis:indexing->ElementBoundToOldIndex; c2 <- mis:indexing->ArrayIndexStartsAtOne; c3 <- mis:indexing->ArrayIndexStartsAtOne; c4 <- mis:indexing->ArrayIndexStartsAtOne
  not yet read: pre:for_loop->loop_scope, pre:loop_control->for_loop, pre:loop_control->off_by_one_error
  root-cause walk: held on ['array_bounds', 'indexing'], broken at [] (consequences: pre:for_loop->array_traversal, pre:indexing->off_by_one_error, pre:indexing->array_bounds), prerequisites {'increment_operators': ['assignment', 'loop_control'], 'boolean_expression': ['comparison_operators'], 'data_structure': ['data_type'], 'comparison_operators': ['expression'], 'array_traversal': ['for_loop', 'indexing'], 'loop_scope': ['for_loop'], 'array_bounds': ['indexing'], 'off_by_one_error': ['indexing', 'loop_control'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable'], 'control_flow': ['statement'], 'println': ['statement']}
  level array_bounds: L0 via misconception "Arrays start at a[1]; so a[0] is before the first element and just gives 0"
  level array_traversal: L3 via relation_to_neighbour "so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
  level for_loop: L2 via output_prediction "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
  level indexing: L0 via misconception "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
  level off_by_one_error: L0 via everyday_reading "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15"
```

## 8. Full diagnosis JSON
```json
{
 "scenario": "MY10",
 "settings": {
  "width": 3,
  "depth": 3,
  "prune_tools": "llm",
  "model": "claude-opus-5-5",
  "backend": "claude-cli"
 },
 "clauses": [
  "It prints 0, then 5, 10 and 15",
  "Arrays start at a[1]",
  "so a[0] is before the first element and just gives 0",
  "Then a[1], a[2] and a[3] are 5, 10 and 15"
 ],
 "start_concepts": [
  "indexing",
  "array_traversal",
  "run_time_error"
 ],
 "held_misconceptions": [
  {
   "concept": "indexing",
   "misconception": "ArrayIndexStartsAtOne",
   "kind": "misconception",
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "score": 0.6175
  },
  {
   "concept": "array_bounds",
   "misconception": "OutOfBoundsElementsAreNull",
   "kind": "misconception",
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0",
   "score": 0.455
  }
 ],
 "error_evidence": [],
 "shadowed": [],
 "broken_edges": [
  {
   "edge": "pre:for_loop->array_traversal",
   "quote": "It prints 0, then 5, 10 and 15; Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "score": 0.85,
   "consequence_of": "mis:indexing->ArrayIndexStartsAtOne"
  },
  {
   "edge": "pre:indexing->off_by_one_error",
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "score": 0.4185,
   "consequence_of": "mis:indexing->ArrayIndexStartsAtOne"
  },
  {
   "edge": "pre:indexing->array_bounds",
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "score": 0.315,
   "consequence_of": "mis:indexing->ArrayIndexStartsAtOne"
  }
 ],
 "root_cause": {
  "concept": "indexing",
  "misconception": "ArrayIndexStartsAtOne"
 },
 "levels": {
  "array_bounds": {
   "level": "L0",
   "way": "misconception",
   "misconception": "OutOfBoundsElementsAreNull",
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0",
   "edge": "mis:array_bounds->OutOfBoundsElementsAreNull",
   "rule": "wrong rule: An out-of-bounds read returns null (or 0). Right rule: Reading or writing any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException and returns no value.",
   "source": "level_mis_links"
  },
  "array_traversal": {
   "level": "L3",
   "way": "relation_to_neighbour",
   "quote": "so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "edge": "lvl:array_traversal@L3#0",
   "source": "level_way",
   "also_shown": []
  },
  "for_loop": {
   "level": "L2",
   "way": "output_prediction",
   "quote": "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "edge": "lvl:for_loop@L2#1",
   "source": "level_way",
   "also_shown": [
    "L2 line_by_line_trace"
   ]
  },
  "indexing": {
   "level": "L0",
   "way": "misconception",
   "misconception": "ArrayIndexStartsAtOne",
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "edge": "mis:indexing->ArrayIndexStartsAtOne",
   "rule": "wrong rule: The first element of a is a[1]. Right rule: Numbering begins with 0; the first element is a[0].",
   "source": "level_mis_links"
  },
  "off_by_one_error": {
   "level": "L0",
   "way": "everyday_reading",
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "edge": "lvl:off_by_one_error@L0#0",
   "source": "level_way",
   "also_shown": []
  }
 },
 "overall_level": "L0",
 "paths": [
  {
   "depth": 1,
   "source": "indexing",
   "edge": "mis:indexing->ArrayIndexStartsAtOne",
   "target": "ArrayIndexStartsAtOne",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.95,
   "prune_score": 0.65,
   "score": 0.6175,
   "logic": "The first element of a is a[1].",
   "twin_logic": "Numbering begins with 0; the first element is a[0]."
  },
  {
   "depth": 1,
   "source": "indexing",
   "edge": "lvl:indexing@L0#0",
   "target": "indexing@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.9,
   "prune_score": 0.6,
   "score": 0.54,
   "logic": "Folk meaning: everyday counting starts at 1 (first = number 1), maths subscripts a_1..a_n run from 1, and f(i) with parentheses means 'apply to i'. Java rule: a[i] uses square brackets and is 0-origin, so the first element is a[0] and the last is a[a.length-1].",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 1,
   "source": "array_traversal",
   "edge": "mis:array_traversal->OffByOneBound",
   "target": "OffByOneBound",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.75,
   "prune_score": 0.6,
   "score": 0.45,
   "logic": "< vs <= and 0..n vs 0..n-1 are interchangeable",
   "twin_logic": "for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n."
  },
  {
   "depth": 2,
   "source": "array_traversal",
   "edge": "pre:for_loop->array_traversal",
   "target": "for_loop",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    2,
    3,
    4
   ],
   "quote": "It prints 0, then 5, 10 and 15; Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.85,
   "prune_score": 1.0,
   "score": 0.85,
   "logic": "for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order.",
   "twin_logic": null,
   "consequence_of": "mis:indexing->ArrayIndexStartsAtOne"
  },
  {
   "depth": 2,
   "source": "indexing",
   "edge": "pre:indexing->off_by_one_error",
   "target": "off_by_one_error",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.93,
   "prune_score": 0.45,
   "score": 0.4185,
   "logic": "Indices start at 0, so the last element is a[N-1]; misreading this convention is the usual source of off-by-one errors.",
   "twin_logic": null,
   "consequence_of": "mis:indexing->ArrayIndexStartsAtOne"
  },
  {
   "depth": 2,
   "source": "indexing",
   "edge": "pre:indexing->array_bounds",
   "target": "array_bounds",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.9,
   "prune_score": 0.35,
   "score": 0.315,
   "logic": "Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used.",
   "twin_logic": null,
   "consequence_of": "mis:indexing->ArrayIndexStartsAtOne"
  },
  {
   "depth": 3,
   "source": "array_bounds",
   "edge": "mis:array_bounds->OutOfBoundsElementsAreNull",
   "target": "OutOfBoundsElementsAreNull",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2,
    3
   ],
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0",
   "confidence": 0.7,
   "prune_score": 0.65,
   "score": 0.455,
   "logic": "Reading a[a.length] just gives null or 0.",
   "twin_logic": "Reading any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException."
  },
  {
   "depth": 3,
   "source": "array_traversal",
   "edge": "pre:indexing->array_traversal",
   "target": "indexing",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    4
   ],
   "quote": "so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.6,
   "prune_score": 1.0,
   "score": 0.6,
   "logic": "A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "off_by_one_error",
   "edge": "lvl:off_by_one_error@L0#0",
   "target": "off_by_one_error@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.7,
   "prune_score": 0.6,
   "score": 0.42,
   "logic": "Everyday counting starts at 1 and 'up to N' includes N. Java arrays start at index 0 and end at N-1, and a loop with i < N runs N times while i <= N runs N+1 times.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  }
 ],
 "evidence": [
  {
   "depth": 1,
   "source": "indexing",
   "edge": "mis:indexing->ArrayIndexStartsAtOne",
   "target": "ArrayIndexStartsAtOne",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.95,
   "prune_score": 0.65,
   "score": 0.6175,
   "logic": "The first element of a is a[1].",
   "twin_logic": "Numbering begins with 0; the first element is a[0]."
  },
  {
   "depth": 1,
   "source": "indexing",
   "edge": "mis:indexing->ElementBoundToOldIndex",
   "target": "ElementBoundToOldIndex",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    4
   ],
   "quote": "It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.6,
   "prune_score": 0.1,
   "score": 0.06,
   "logic": "After i changes, X[i] still refers to the element at the old value of i.",
   "twin_logic": "a[i] is evaluated with the current value of i each time it is used."
  },
  {
   "depth": 1,
   "source": "indexing",
   "edge": "lvl:indexing@L0#0",
   "target": "indexing@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.9,
   "prune_score": 0.6,
   "score": 0.54,
   "logic": "Folk meaning: everyday counting starts at 1 (first = number 1), maths subscripts a_1..a_n run from 1, and f(i) with parentheses means 'apply to i'. Java rule: a[i] uses square brackets and is 0-origin, so the first element is a[0] and the last is a[a.length-1].",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 1,
   "source": "array_traversal",
   "edge": "mis:array_traversal->OffByOneBound",
   "target": "OffByOneBound",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.75,
   "prune_score": 0.6,
   "score": 0.45,
   "logic": "< vs <= and 0..n vs 0..n-1 are interchangeable",
   "twin_logic": "for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n."
  },
  {
   "depth": 1,
   "source": "array_traversal",
   "edge": "mis:array_traversal->IdiomOverridesCode",
   "target": "IdiomOverridesCode",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.7,
   "prune_score": 0.25,
   "score": 0.175,
   "logic": "An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.",
   "twin_logic": "The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written."
  },
  {
   "depth": 1,
   "source": "array_traversal",
   "edge": "mis:array_traversal->ElementBoundToOldIndex",
   "target": "ElementBoundToOldIndex",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    4
   ],
   "quote": "Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.55,
   "prune_score": 0.15,
   "score": 0.0825,
   "logic": "After i changes, X[i] still refers to the element at the old value of i.",
   "twin_logic": "a[i] is evaluated with the current value of i each time it is used."
  },
  {
   "depth": 1,
   "source": "array_traversal",
   "edge": "lvl:array_traversal@L3#0",
   "target": "array_traversal@L3",
   "kind": "level",
   "label": "shown",
   "clauses": [
    3,
    4
   ],
   "quote": "so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.7,
   "prune_score": 0.2,
   "score": 0.14,
   "logic": "The loop variable is used as the index, so a[i] reaches a different element on each pass.",
   "twin_logic": null,
   "level": "L3",
   "way": "relation_to_neighbour"
  },
  {
   "depth": 2,
   "source": "indexing",
   "edge": "pre:indexing->off_by_one_error",
   "target": "off_by_one_error",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.93,
   "prune_score": 0.45,
   "score": 0.4185,
   "logic": "Indices start at 0, so the last element is a[N-1]; misreading this convention is the usual source of off-by-one errors.",
   "twin_logic": null,
   "consequence_of": "mis:indexing->ArrayIndexStartsAtOne"
  },
  {
   "depth": 2,
   "source": "indexing",
   "edge": "pre:indexing->array_bounds",
   "target": "array_bounds",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.9,
   "prune_score": 0.35,
   "score": 0.315,
   "logic": "Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used.",
   "twin_logic": null,
   "consequence_of": "mis:indexing->ArrayIndexStartsAtOne"
  },
  {
   "depth": 2,
   "source": "indexing",
   "edge": "pre:indexing->array_traversal",
   "target": "array_traversal",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    4
   ],
   "quote": "so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.6,
   "prune_score": 0.2,
   "score": 0.12,
   "logic": "A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "array_traversal",
   "edge": "pre:for_loop->array_traversal",
   "target": "for_loop",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    2,
    3,
    4
   ],
   "quote": "It prints 0, then 5, 10 and 15; Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.85,
   "prune_score": 1.0,
   "score": 0.85,
   "logic": "for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order.",
   "twin_logic": null,
   "consequence_of": "mis:indexing->ArrayIndexStartsAtOne"
  },
  {
   "depth": 3,
   "source": "for_loop",
   "edge": "mis:for_loop->IdiomOverridesCode",
   "target": "IdiomOverridesCode",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.7,
   "prune_score": 0.45,
   "score": 0.315,
   "logic": "An array loop processes the whole array from index 0 to length-1 and increments its index at the end of the body, whatever the code says.",
   "twin_logic": "The loop visits exactly the indices that its initialisation, guard and update produce, in the order in which its statements are written."
  },
  {
   "depth": 3,
   "source": "for_loop",
   "edge": "err:for_loop->WrongIterationCount",
   "target": "WrongIterationCount",
   "kind": "error",
   "label": "correct",
   "clauses": [
    1,
    4
   ],
   "quote": "It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.6,
   "prune_score": 0.35,
   "score": 0.21,
   "logic": "Updates the loop counter so that the loop runs the wrong number of times.",
   "twin_logic": "The init, test and update together decide the number of passes; trace them to check the count."
  },
  {
   "depth": 3,
   "source": "for_loop",
   "edge": "lvl:for_loop@L2#1",
   "target": "for_loop@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.6,
   "prune_score": 0.4,
   "score": 0.24,
   "logic": "A for statement has no value; the passes it makes are fixed by its header: for (int i = 1; i <= N; i++) sum += i; leaves sum = N(N+1)/2, and for (int i = 2; i <= 8; i += 2) prints 2, 4, 6, 8,.",
   "twin_logic": null,
   "level": "L2",
   "way": "output_prediction"
  },
  {
   "depth": 3,
   "source": "for_loop",
   "edge": "lvl:for_loop@L2#0",
   "target": "for_loop@L2",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.6,
   "prune_score": 0.25,
   "score": 0.15,
   "logic": "Run the initializer once; then repeatedly: test the condition (stop if false), execute the body, run the update.",
   "twin_logic": null,
   "level": "L2",
   "way": "line_by_line_trace"
  },
  {
   "depth": 3,
   "source": "array_traversal",
   "edge": "pre:indexing->array_traversal",
   "target": "indexing",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3,
    4
   ],
   "quote": "so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.6,
   "prune_score": 1.0,
   "score": 0.6,
   "logic": "A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass.",
   "twin_logic": null
  },
  {
   "depth": 3,
   "source": "off_by_one_error",
   "edge": "mis:off_by_one_error->OffByOneBound",
   "target": "OffByOneBound",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    4
   ],
   "quote": "It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.6,
   "prune_score": 0.6,
   "score": 0.36,
   "logic": "< vs <= and 0..n vs 0..n-1 are interchangeable",
   "twin_logic": "for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n."
  },
  {
   "depth": 3,
   "source": "off_by_one_error",
   "edge": "err:off_by_one_error->WrongIterationCount",
   "target": "WrongIterationCount",
   "kind": "error",
   "label": "correct",
   "clauses": [
    1,
    4
   ],
   "quote": "It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.55,
   "prune_score": 0.35,
   "score": 0.1925,
   "logic": "Updates the loop counter so that the loop runs the wrong number of times.",
   "twin_logic": "The init, test and update together decide the number of passes; trace them to check the count."
  },
  {
   "depth": 3,
   "source": "off_by_one_error",
   "edge": "lvl:off_by_one_error@L0#0",
   "target": "off_by_one_error@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.7,
   "prune_score": 0.6,
   "score": 0.42,
   "logic": "Everyday counting starts at 1 and 'up to N' includes N. Java arrays start at index 0 and end at N-1, and a loop with i < N runs N times while i <= N runs N+1 times.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 3,
   "source": "array_bounds",
   "edge": "mis:array_bounds->OutOfBoundsElementsAreNull",
   "target": "OutOfBoundsElementsAreNull",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2,
    3
   ],
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0",
   "confidence": 0.7,
   "prune_score": 0.65,
   "score": 0.455,
   "logic": "Reading a[a.length] just gives null or 0.",
   "twin_logic": "Reading any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException."
  },
  {
   "depth": 3,
   "source": "array_bounds",
   "edge": "mis:array_bounds->OffByOneBound",
   "target": "OffByOneBound",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    1,
    4
   ],
   "quote": "It prints 0, then 5, 10 and 15; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.7,
   "prune_score": 0.35,
   "score": 0.245,
   "logic": "< vs <= and 0..n vs 0..n-1 are interchangeable",
   "twin_logic": "for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n."
  },
  {
   "depth": 3,
   "source": "array_bounds",
   "edge": "lvl:array_bounds@L0#0",
   "target": "array_bounds@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3,
    4
   ],
   "quote": "Arrays start at a[1]; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.8,
   "prune_score": 0.5,
   "score": 0.4,
   "logic": "Folk meaning: in English, 'items 1 to 10' or 'up to n' includes the end point, and reading past the end of a list just gives 'nothing'. Java rule: the legal indices are 0..length-1, and any other index throws ArrayIndexOutOfBoundsException instead of returning a value.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 3,
   "source": "array_bounds",
   "edge": "lvl:array_bounds@L0#2",
   "target": "array_bounds@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    1,
    3,
    4
   ],
   "quote": "It prints 0, then 5, 10 and 15; so a[0] is before the first element and just gives 0; Then a[1], a[2] and a[3] are 5, 10 and 15",
   "confidence": 0.6,
   "prune_score": 0.3,
   "score": 0.18,
   "logic": "Points to LT: the bounds check runs at every access, at run time. Inconsistent application: the trace accepts an index of a.length on the last pass (or -1 on the first) but rejects it elsewhere, or reads 'some value' there. (here mixing in: \"an out-of-bounds read returns null (it throws)\")",
   "twin_logic": null,
   "level": "L0",
   "way": "inconsistent_trace"
  }
 ],
 "clause_coverage": {
  "It prints 0, then 5, 10 and 15": "mis:indexing->ElementBoundToOldIndex",
  "Arrays start at a[1]": "mis:indexing->ArrayIndexStartsAtOne",
  "so a[0] is before the first element and just gives 0": "mis:indexing->ArrayIndexStartsAtOne",
  "Then a[1], a[2] and a[3] are 5, 10 and 15": "mis:indexing->ArrayIndexStartsAtOne"
 },
 "unexplained_clauses": [],
 "stop_reason": "max depth",
 "depth_reached": 3,
 "llm_calls": 0,
 "llm_cache_hits": 44,
 "llm_calls_by_step": {
  "prune": 15,
  "label": 29
 }
}
```
