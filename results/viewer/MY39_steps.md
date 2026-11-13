# Think on the Graph: every output of the run MY39
## 0. Input
Program:
```java
int[][] t = {{1, 2, 3}, {4, 5}, {6}};
int sum = 0;
for (int i = 0; i < t.length; i++) {
    for (int j = 0; j < t[0].length; j++) {
        sum += t[i][j];
    }
}
System.out.println(sum);
```
Question: What is printed? Explain how the inner loop decides how many columns to visit.

Student's answer: 21. t[0].length is 3, and every row of a 2D array has the same length, so it visits three columns in every row and adds all six numbers
Settings: width 3, depth 3, prune llm, backend claude-cli, model claude-opus-5-5
## 1. Stage 1: the subgraph G from the code (no model)
Masked code (string and char literals and comments blanked; this is what the patterns see):
```
int[][] t = {{1, 2, 3}, {4, 5}, {6}};
int sum = 0;
for (int i = 0; i < t.length; i++) {
    for (int j = 0; j < t[0].length; j++) {
        sum += t[i][j];
    }
}
System.out.println(sum);
```
Which code text tagged which concept (a generic concept fires on almost any Java line; it starts the walk only if the answer repeats its tag):
| concept | generic | channel | matched text | line |
|---|---|---|---|---|
| accumulator_pattern | False | pattern | 'sum += t[i][j];' | 5 |
| array_bounds | False | pattern | 'i < t.length' | 3 |
| array_initializer | False | pattern | '= {' | 1 |
| array_traversal | False | pattern | 'for (int i = 0; i < t.length' | 3 |
| assignment | True | pattern | '=' | 1 |
| boolean_expression | False | pattern | 'for (int i = 0; i < t.length;' | 3 |
| comparison_operators | False | pattern | 'for (int i = 0; i <' | 3 |
| compound_assignment | False | pattern | '+=' | 5 |
| control_flow | False | pattern | 'for (' | 3 |
| data_structure | False | pattern | 'int[]' | 1 |
| data_type | True | pattern | 'int' | 1 |
| expression | True | pattern | 'i <' | 3 |
| expression | True | pattern | '= {{1, 2, 3}, {4, 5}, {6}};' | 1 |
| for_loop | False | pattern | 'for (' | 3 |
| increment_operators | False | pattern | '++' | 3 |
| indexing | False | pattern | 't[0]' | 4 |
| length_field | False | pattern | '.length' | 3 |
| loop_body | False | pattern | 'for (' | 3 |
| loop_control | False | signal | 'for (int i = 0; i < t.length; i++)' | 3 |
| loop_scope | False | pattern | 'for (int i' | 3 |
| loop_variable | False | pattern | 'for (int i =' | 3 |
| nested_loops | False | signal | 'for (int i = 0; i < t.length; i++) {\n    for (' | 3 |
| println | False | pattern | 'System.out.println(' | 8 |
| ragged_array | False | pattern | 't[0].length' | 4 |
| ragged_array | False | pattern | '= {{1, 2, 3}, {' | 1 |
| row_major_order | False | signal | 'for (int i = 0; i < t.length; i++) {\n    for (int j = 0; j < t[0].length; j++) {\n        sum += t[i][j]' | 3 |
| statement | True | pattern | ';' | 1 |
| two_dimensional_array | False | pattern | '[][]' | 1 |
| two_dimensional_array | False | pattern | 't[i][j]' | 5 |

G: 26 concept nodes (4 generic), 27 concept edges, 167 misconception / error edges, 123 misconception / error nodes, 130 level nodes, 189 level-misconception links, 3 connected piece(s).
Note: concept nodes form 3 pieces (the KG has no edge between them): accumulator_pattern,array_bounds,array_initializer,array_traversal,assignment,boolean_expression,comparison_operators,compound_assignment,expression,for_loop,increment_operators,indexing,length_field,loop_body,loop_control,loop_scope,loop_variable,nested_loops,ragged_array,row_major_order,two_dimensional_array | control_flow,println,statement | data_structure,data_type

Concept edges of G (the links the walk can read; `pre:` = prerequisite A -> B, `par:` = parallel):
| edge | type | rule (logic) |
|---|---|---|
| par:assignment~comparison_operators | parallel | x = y stores the value of y in x (a statement with a side effect); x == y only tests whether the two values are equal and gives a boolean. Writing = where == is meant is a compile error with int operands and a silent bug with boolean operands. |
| par:increment_operators~compound_assignment | parallel | i++, ++i and i += 1 all add 1 to i; ++ and -- change a variable only by one and are normally used for integers, while i += k works for any amount and with any arithmetic operator (-=, *=, /=, %=). |
| pre:array_initializer->indexing | prerequisite | The values listed in braces are stored at indices 0, 1, 2, ... in order, and a[i] reads the value at index i. |
| pre:array_initializer->length_field | prerequisite | An array made from a literal has as many elements as values listed, and a.length gives that number. |
| pre:assignment->compound_assignment | prerequisite | x op= e is shorthand for the assignment x = x op e. |
| pre:assignment->increment_operators | prerequisite | i++ is shorthand for the assignment i = i + 1. |
| pre:comparison_operators->boolean_expression | prerequisite | A comparison such as x < y produces a boolean result; comparisons together with boolean logic provide the basis for decision-making. |
| pre:compound_assignment->accumulator_pattern | prerequisite | sum += x is the usual way a running total is updated on each pass. |
| pre:data_type->data_structure | prerequisite | A data structure organizes many values of a data type; the array holds a sequence of values of one type. |
| pre:expression->comparison_operators | prerequisite | Comparison operators build expressions whose value is a boolean, so one must already know what an expression is to understand a < b. |
| pre:for_loop->array_traversal | prerequisite | for (int i = 0; i < a.length; i++) gives i every valid index exactly once, in increasing order. |
| pre:for_loop->loop_body | prerequisite | The statements in braces after the for header are the loop body; they run once on every pass, between the test and the increment, exactly as in a while loop. |
| pre:for_loop->loop_scope | prerequisite | A variable declared in the for header exists only from its declaration to the end of the for statement's block. |
| pre:for_loop->nested_loops | prerequisite | In nested loops the inner for runs its complete set of passes for every single pass of the outer for. |
| pre:indexing->array_bounds | prerequisite | Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used. |
| pre:indexing->array_traversal | prerequisite | A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass. |
| pre:indexing->two_dimensional_array | prerequisite | A 1-D array uses one index a[i]; a 2-D array uses two, a[i][j], where the first index chooses the row array. |
| pre:length_field->array_traversal | prerequisite | A traversal loop runs its index from 0 while it is below a.length, so it visits every element once. |
| pre:loop_body->accumulator_pattern | prerequisite | The accumulator update sum += x sits inside the body, so it runs once on every pass. |
| pre:loop_control->for_loop | prerequisite | The for header is exactly the three control slots, and the body runs after the test and before the update on each pass. |
| pre:loop_control->increment_operators | prerequisite | The loop update i = i + 1 comes first; ++ (and +=) are then introduced as shorthand for that update. |
| pre:loop_variable->loop_control | prerequisite | The init, condition and update all act on the loop variable: the init sets it, the condition tests it, the update changes it. |
| pre:nested_loops->row_major_order | prerequisite | Which loop is outside decides whether the entries are processed row by row or column by column. |
| pre:statement->control_flow | prerequisite | Control flow is the order in which statements run. |
| pre:statement->println | prerequisite | System.out.println(s); is itself a statement, so its line of output appears at its own place in the sequence. |
| pre:two_dimensional_array->ragged_array | prerequisite | There is no requirement that all rows in a two-dimensional array have the same length; an array with rows of nonuniform length is known as a ragged array. |
| pre:two_dimensional_array->row_major_order | prerequisite | Row-major order visits a[i][j] row by row (outer loop over i); column-major order puts the column loop outside. |

Misconception / error edges per concept (count), and level ways per concept (count):
| concept | misconception / error edges | level ways (L1-L4 + L0 non-misconception) |
|---|---|---|
| accumulator_pattern | 4 | 17 |
| array_bounds | 2 | 14 |
| array_initializer | 2 | 14 |
| array_traversal | 6 | 22 |
| assignment | 15 | 24 |
| boolean_expression | 8 | 19 |
| comparison_operators | 8 | 20 |
| compound_assignment | 2 | 15 |
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
| nested_loops | 8 | 17 |
| println | 6 | 17 |
| ragged_array | 2 | 13 |
| row_major_order | 0 | 13 |
| statement | 5 | 19 |
| two_dimensional_array | 7 | 18 |

Figure 1: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY39_figure01.png

Figure 2: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY39_figure02.png

## 2. Clauses and start concepts (no model)
The answer split into clauses (at sentence ends, ';', and before 'because' / 'so'; quotes removed):
| clause | text |
|---|---|
| c1 | 21 |
| c2 | t[0].length is 3, and every row of a 2D array has the same length |
| c3 | so it visits three columns in every row and adds all six numbers |

start: BM25 of the answer against each tagged concept: two_dimensional_array 28.24 (hits 2), ragged_array 24.31 (hits 2), indexing 20.88 (hits 1), array_traversal 19.88 (hits 1), length_field 16.10 (hits 1), loop_control 14.92 (hits 1), array_initializer 14.01 (hits 1), for_loop 13.06 (hits 1), row_major_order 11.27 (hits 1), increment_operators 10.97 (hits 1), comparison_operators 10.50 (hits 1), compound_assignment 9.75 (hits 1), nested_loops 9.49 (hits 1), array_bounds 9.25 (hits 1), loop_variable 8.67 (hits 1), loop_body 8.59 (hits 1), loop_scope 7.53 (hits 1), accumulator_pattern 6.26 (hits 1), boolean_expression 6.17 (hits 1), println 4.52 (hits 1), control_flow 3.58 (hits 1), data_structure 1.77 (hits 1)

start: chosen two_dimensional_array, ragged_array, indexing

start concepts (3): two_dimensional_array, ragged_array, indexing

Start concepts: two_dimensional_array, ragged_array, indexing

Figure 3: C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY39_figure03.png

## 3. The walk, depth by depth
At each depth, for each current concept: the edges offered (a concept entering as a start concept offers its misconception / error edges and its level ways, as two families; otherwise it offers its concept edges), the prune prompt and the model's reply, then the label prompt(s) and the model's reply, parsed into label / clauses / confidence. Score = prune score x confidence.

### Depth 1: current concepts 'two_dimensional_array', 'ragged_array', 'indexing'

#### two_dimensional_array, misconceptions: 7 edges offered
Edges offered:
| edge |
|---|
| mis:two_dimensional_array->ArrayElementTypeRepeats \| wrong rule: A 2-D int array type is written int[] int[]. \| right rule: It is written int[][]. |
| mis:two_dimensional_array->ArrayRankIsLength \| wrong rule: The number of dimensions of an array is its length. \| right rule: Rank (number of dimensions) and length are different. |
| mis:two_dimensional_array->ColumnLikeRow \| wrong rule: Column j of a 2-D array can be picked out as a 1-D array, just like row a[i]. \| right rule: a[i] is row i (a 1-D array), but there is no expression for a column; loop over i and use a[i][j]. |
| mis:two_dimensional_array->MultidimensionalArray \| wrong rule: int[m][n] is one block of m * n values, so a[i] on its own means nothing. \| right rule: A 2-D array is an array of m row arrays, so a[i] is a 1-D array of length n. |
| mis:two_dimensional_array->NoJaggedArrays \| wrong rule: Every row of a 2-D array must have the same length. \| right rule: Each row a[i] is its own array, so rows can have different lengths a[i].length. |
| mis:two_dimensional_array->OnlyInnermostArrayElements \| wrong rule: Only single elements a[i][j] can be used, not whole rows a[i]. \| right rule: a[i] gives the whole row i, which can be used like any 1-D array. |
| mis:two_dimensional_array->RaggedRowsSameLength \| wrong rule: All rows of a 2-D array have the same length, so one N works for every row. \| right rule: Rows may differ in length; use a[i].length for row i. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:two_dimensional_array->RaggedRowsSameLength (0.50), mis:two_dimensional_array->NoJaggedArrays (0.40), mis:two_dimensional_array->MultidimensionalArray (0.10)
```
Kept by pruning: mis:two_dimensional_array->RaggedRowsSameLength (0.50), mis:two_dimensional_array->NoJaggedArrays (0.40), mis:two_dimensional_array->MultidimensionalArray (0.10)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:two_dimensional_array->RaggedRowsSameLength \| wrong rule: All rows of a 2-D array have the same length, so one N works for every row. \| right rule: Rows may differ in length; use a[i].length for row i. |
| mis:two_dimensional_array->NoJaggedArrays \| wrong rule: Every row of a 2-D array must have the same length. \| right rule: Each row a[i] is its own array, so rows can have different lengths a[i].length. |
| mis:two_dimensional_array->MultidimensionalArray \| wrong rule: int[m][n] is one block of m * n values, so a[i] on its own means nothing. \| right rule: A 2-D array is an array of m row arrays, so a[i] is a 1-D array of length n. |
Model's reply:
```
mis:two_dimensional_array->RaggedRowsSameLength | held | clauses: 2, 3 | confidence: 0.93
mis:two_dimensional_array->NoJaggedArrays | held | clauses: 2 | confidence: 0.7
mis:two_dimensional_array->MultidimensionalArray | correct | clauses: 2 | confidence: 0.6
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:two_dimensional_array->RaggedRowsSameLength | held | 0.5 | 0.93 | 0.47 | c2, c3 | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| mis:two_dimensional_array->NoJaggedArrays | held | 0.4 | 0.7 | 0.28 | c2 | t[0].length is 3, and every row of a 2D array has the same length |
| mis:two_dimensional_array->MultidimensionalArray | correct | 0.1 | 0.6 | 0.06 | c2 | t[0].length is 3, and every row of a 2D array has the same length |

#### two_dimensional_array, level ways: 18 edges offered
Edges offered:
| edge |
|---|
| lvl:two_dimensional_array@L0#0 \| level L0 way everyday_reading: Folk meaning: a table or matrix is one grid in which rows and columns are symmetric, so a column should be as easy to pick out as a row. Java rule: a 2-D array is an array of row arrays; a[i] is row i, a[i][j] an element, and there is no expression for a column. |
| lvl:two_dimensional_array@L0#5 \| level L0 way inconsistent_trace: Points to LT: a[i][j] is evaluated as (a[i])[j], first the row and then the element in it. Inconsistent application: the first index is taken as the row on some steps and as the column on others. (here mixing in: "only the innermost elements are accessible") |
| lvl:two_dimensional_array@L1#0 \| level L1 way names_the_element: Identity: a two-dimensional array, an array of arrays used to represent a table or matrix with M rows and N columns. |
| lvl:two_dimensional_array@L1#1 \| level L1 way states_the_rule: Declarative: declare double[][] a; create with new double[M][N] (rows first, then columns); refer to row i, column j as a[i][j]. Entries start at 0 (numbers) or false (boolean). |
| lvl:two_dimensional_array@L2#0 \| level L2 way line_by_line_trace: Sequencing: new double[M][N] creates an array of M references and then M row arrays of N defaults. a[i][j] evaluates a[i] (checked against a.length = M) and then [j] (checked against a[i].length). |
| lvl:two_dimensional_array@L2#1 \| level L2 way output_prediction: Result: a[i][j] has the element type; a.length is the number of rows M; a[i].length is the length of row i; a[i] is a double[] row. |
| lvl:two_dimensional_array@L2#2 \| level L2 way one_step_execution: State transition: a[i][j] = v changes one element of row i; a[i] = new double[K] replaces the whole row i with a new array; other rows are untouched. |
| lvl:two_dimensional_array@L3#0 \| level L3 way relation_to_neighbour: The transition matrix is a 2-D double array p[i][j] with one row per page; each row holds a probability distribution. |
| lvl:two_dimensional_array@L3#1 \| level L3 way relation_to_neighbour: A 2-D array uses two indices, and the first chooses the row array: a[i][j] is (a[i])[j]. |
| lvl:two_dimensional_array@L3#2 \| level L3 way relation_to_neighbour: Since each row is a separate array, rows may have different lengths; such arrays are ragged. |
| lvl:two_dimensional_array@L3#3 \| level L3 way relation_to_neighbour: Matrix operations index a[i][j] in nested loops (two for addition, three for multiplication). |
| lvl:two_dimensional_array@L3#4 \| level L3 way relation_to_neighbour: The same notation extends to any number of dimensions: a[i][j][k] for double[][][]. |
| lvl:two_dimensional_array@L3#5 \| level L3 way relation_to_neighbour: Row-major order visits a[i][j] with the outer loop over rows i; column-major puts the loop over j outside. |
| lvl:two_dimensional_array@L3#6 \| level L3 way purpose_of_the_whole: Plan/role: store tables, matrices, grids and images indexed by row and column (grades by student and test, lattice intersections, pixels). |
| lvl:two_dimensional_array@L4#0 \| level L4 way predict_a_change: Conservation: swapping the loop order for an element-wise operation keeps the result but changes the processing order. Swapping the indices (a[j][i]) transposes and goes out of bounds when M != N. |
| lvl:two_dimensional_array@L4#1 \| level L4 way transfer_to_a_new_program: Applicability: use a 2-D array for data naturally indexed by two integers (rows by columns). Use a ragged array when rows differ, a 1-D array when one index suffices, and higher dimensions for 3-D models. |
| lvl:two_dimensional_array@L4#2 \| level L4 way diagnose_an_error: rule broken: Indices must be within each dimension (i < a.length, j < a[i].length). Kind: run-time exception. Trigger class: row and column bounds swapped in a non-square M-by-N array, or j bounded by N on a shorter ragged row (ArrayIndexOutOfBoundsException) |
| lvl:two_dimensional_array@L4#3 \| level L4 way diagnose_an_error: rule broken: The type is written with one bracket pair per dimension. Kind: compile-time. Trigger class: int[] int[] a; or assigning an int[] where an int[][] is required (incompatible types) |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:two_dimensional_array@L3#2 (Score: 0.45)}
{lvl:two_dimensional_array@L0#0 (Score: 0.3)}
{lvl:two_dimensional_array@L4#2 (Score: 0.25)}
```
Kept by pruning: lvl:two_dimensional_array@L3#2 (0.45), lvl:two_dimensional_array@L0#0 (0.30), lvl:two_dimensional_array@L4#2 (0.25)

Label prompt for level way lvl:two_dimensional_array@L3#2 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Since each row is a separate array, rows may have different lengths; such arrays are ragged.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Label prompt for level way lvl:two_dimensional_array@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: a table or matrix is one grid in which rows and columns are symmetric, so a column should be as easy to pick out as a row. Java rule: a 2-D array is an array of row arrays; a[i] is row i, a[i][j] an element, and there is no expression for a column.

Model's reply:
```
Label: shown
Clauses: 2, 3
Confidence: 0.7
```

Label prompt for level way lvl:two_dimensional_array@L4#2 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: Indices must be within each dimension (i < a.length, j < a[i].length). Kind: run-time exception. Trigger class: row and column bounds swapped in a non-square M-by-N array, or j bounded by N on a shorter ragged row (ArrayIndexOutOfBoundsException)

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:two_dimensional_array@L3#2 | not applied |  |  | 0.0 |  |  |
| lvl:two_dimensional_array@L0#0 | shown | 0.3 | 0.7 | 0.21 | c2, c3 | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| lvl:two_dimensional_array@L4#2 | not applied |  |  | 0.0 |  |  |

#### ragged_array, misconceptions: 2 edges offered
Edges offered:
| edge |
|---|
| mis:ragged_array->NoJaggedArrays \| wrong rule: multi-dimensional arrays must be rectangular \| right rule: Each row a[i] is its own array, so rows can have different lengths a[i].length. |
| mis:ragged_array->RaggedRowsSameLength \| wrong rule: All rows of a 2-D array have the same length, so one N works for every row. \| right rule: Rows may differ in length; use a[i].length for row i. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{mis:ragged_array->RaggedRowsSameLength (Score: 0.6)}
{mis:ragged_array->NoJaggedArrays (Score: 0.4)}
```
Kept by pruning: mis:ragged_array->RaggedRowsSameLength (0.60), mis:ragged_array->NoJaggedArrays (0.40)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:ragged_array->RaggedRowsSameLength \| wrong rule: All rows of a 2-D array have the same length, so one N works for every row. \| right rule: Rows may differ in length; use a[i].length for row i. |
| mis:ragged_array->NoJaggedArrays \| wrong rule: multi-dimensional arrays must be rectangular \| right rule: Each row a[i] is its own array, so rows can have different lengths a[i].length. |
Model's reply:
```
mis:ragged_array->RaggedRowsSameLength | held | clauses: 2, 3 | confidence: 0.95
mis:ragged_array->NoJaggedArrays | held | clauses: 2 | confidence: 0.55
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:ragged_array->RaggedRowsSameLength | held | 0.6 | 0.95 | 0.57 | c2, c3 | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| mis:ragged_array->NoJaggedArrays | held | 0.4 | 0.55 | 0.22 | c2 | t[0].length is 3, and every row of a 2D array has the same length |

#### ragged_array, level ways: 13 edges offered
Edges offered:
| edge |
|---|
| lvl:ragged_array@L0#0 \| level L0 way everyday_reading: Folk meaning: a 'table' has the same number of columns in every row, so one width N serves all rows. Java rule: each row is a separate array, so rows may have different lengths, and code must use a[i].length for row i. |
| lvl:ragged_array@L0#3 \| level L0 way inconsistent_trace: Points to LT: the inner bound a[i].length is re-evaluated for each row. Inconsistent application: the trace uses row 0's length (or N) for every row, sometimes over-running a short row and sometimes stopping early in a long one. (here mixing in: "All rows of a 2-D array have the same length, so one N works for every row") |
| lvl:ragged_array@L1#0 \| level L1 way names_the_element: Identity: a ragged array is a two-dimensional array whose rows have different (nonuniform) lengths. |
| lvl:ragged_array@L1#1 \| level L1 way states_the_rule: Declarative: there is no requirement that rows have the same length. Process row i up to a[i].length: for (i < a.length) for (j < a[i].length). |
| lvl:ragged_array@L2#0 \| level L2 way line_by_line_trace: Sequencing: the outer loop runs i over 0..a.length-1; for each i the inner loop bound a[i].length is read for that row, and then j runs over 0..a[i].length-1. |
| lvl:ragged_array@L2#1 \| level L2 way output_prediction: Result: rows of different widths, e.g. a Pascal's-triangle array whose row N has N+1 entries; a[i].length differs from row to row. |
| lvl:ragged_array@L2#2 \| level L2 way one_step_execution: State transition: creating a row with a[i] = new double[i+1] sets the length of that row only; element writes change one entry. |
| lvl:ragged_array@L3#0 \| level L3 way relation_to_neighbour: Ragged arrays exist because a 2-D array is an array of arrays: each row is an independent 1-D array with its own length. |
| lvl:ragged_array@L3#1 \| level L3 way purpose_of_the_whole: Plan/role: store triangular or uneven data (binomial coefficients, lists of varying length) without wasting space on unused entries. |
| lvl:ragged_array@L4#0 \| level L4 way predict_a_change: Conservation: code written with a[i].length also works for rectangular arrays, but code written with a fixed N breaks on ragged ones; each later solution should still work for the earlier cases. |
| lvl:ragged_array@L4#1 \| level L4 way transfer_to_a_new_program: Applicability: use a ragged array when rows naturally differ in length. When all rows have equal length, a rectangular array with M and N is simpler, and the book normally uses that. |
| lvl:ragged_array@L4#2 \| level L4 way diagnose_an_error: rule broken: Each row must be processed up to its own length. Kind: run-time exception. Trigger class: the inner loop uses N or a[0].length, and a shorter row is indexed past its end (ArrayIndexOutOfBoundsException) |
| lvl:ragged_array@L4#3 \| level L4 way diagnose_an_error: rule broken: Each row must be processed up to its own length. Kind: silent logic error. Trigger class: the inner bound is shorter than a longer row, so its last entries are silently skipped |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:ragged_array@L0#0 (Score: 0.5)}
{lvl:ragged_array@L0#3 (Score: 0.35)}
{lvl:ragged_array@L4#2 (Score: 0.15)}
```
Kept by pruning: lvl:ragged_array@L0#0 (0.50), lvl:ragged_array@L0#3 (0.35), lvl:ragged_array@L4#2 (0.15)

Label prompt for level way lvl:ragged_array@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: a 'table' has the same number of columns in every row, so one width N serves all rows. Java rule: each row is a separate array, so rows may have different lengths, and code must use a[i].length for row i.

Model's reply:
```
Label: shown
Clauses: 2, 3
Confidence: 0.8
```

Label prompt for level way lvl:ragged_array@L0#3 (the model saw only the concept, the way's name 'inconsistent trace' and its text; no level):
> Points to LT: the inner bound a[i].length is re-evaluated for each row. Inconsistent application: the trace uses row 0's length (or N) for every row, sometimes over-running a short row and sometimes stopping early in a long one. (here mixing in: "All rows of a 2-D array have the same length, so one N works for every row")

Model's reply:
```
Label: shown
Clauses: 2, 3
Confidence: 0.8
```

Label prompt for level way lvl:ragged_array@L4#2 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: Each row must be processed up to its own length. Kind: run-time exception. Trigger class: the inner loop uses N or a[0].length, and a shorter row is indexed past its end (ArrayIndexOutOfBoundsException)

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.93
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:ragged_array@L0#0 | shown | 0.5 | 0.8 | 0.4 | c2, c3 | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| lvl:ragged_array@L0#3 | shown | 0.35 | 0.8 | 0.28 | c2, c3 | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| lvl:ragged_array@L4#2 | not applied |  |  | 0.0 |  |  |

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
mis:indexing->ArrayUseScansAllCells (0.50), mis:indexing->ArrayRangeInclusive (0.30), mis:indexing->IndexIsValue (0.20)
```
Kept by pruning: mis:indexing->ArrayUseScansAllCells (0.50), mis:indexing->ArrayRangeInclusive (0.30), mis:indexing->IndexIsValue (0.20)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:indexing->ArrayUseScansAllCells \| wrong rule: Using an array means every cell must be scanned. \| right rule: Arrays allow random access: a[i] reaches one element directly, and a loop visits only the elements the task needs. |
| mis:indexing->ArrayRangeInclusive \| wrong rule: new int[n] has slots 0 to n, inclusive. \| right rule: The slots are 0 to n - 1. |
| mis:indexing->IndexIsValue \| wrong rule: i and a[i] are the same thing, so the position is the stored value. \| right rule: i is a position; a[i] is the value stored at that position. |
Model's reply:
```
mis:indexing->ArrayUseScansAllCells | not applied | clauses: none | confidence: 0.75
mis:indexing->ArrayRangeInclusive | correct | clauses: 2, 3 | confidence: 0.55
mis:indexing->IndexIsValue | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:indexing->ArrayUseScansAllCells | not applied |  |  | 0.0 |  |  |
| mis:indexing->ArrayRangeInclusive | correct | 0.3 | 0.55 | 0.17 | c2, c3 | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| mis:indexing->IndexIsValue | not applied |  |  | 0.0 |  |  |

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
{lvl:indexing@L3#3 (Score: 0.45)}
{lvl:indexing@L4#2 (Score: 0.35)}
{lvl:indexing@L3#2 (Score: 0.2)}
```
Kept by pruning: lvl:indexing@L3#3 (0.45), lvl:indexing@L4#2 (0.35), lvl:indexing@L3#2 (0.20)

Label prompt for level way lvl:indexing@L3#3 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> a[i] on a 2-D array yields row i (itself a 1-D array), and a[i][j] then indexes into that row.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.6
```

Label prompt for level way lvl:indexing@L4#2 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: The index must be in 0..a.length-1. Kind: run-time exception. Trigger class: index < 0 or >= a.length, e.g. a[a.length], a[i+1] on the last pass, a[i-1] at i = 0, a[0] of an empty array (ArrayIndexOutOfBoundsException)

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.95
```

Label prompt for level way lvl:indexing@L3#2 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Every index value is checked against 0 and a.length at run time; any other value throws.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:indexing@L3#3 | not applied |  |  | 0.0 |  |  |
| lvl:indexing@L4#2 | not applied |  |  | 0.0 |  |  |
| lvl:indexing@L3#2 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

mis:ragged_array->RaggedRowsSameLength [held, tier 0, 0.57], mis:two_dimensional_array->RaggedRowsSameLength [held, tier 0, 0.47], mis:two_dimensional_array->NoJaggedArrays [held, tier 0, 0.28], mis:ragged_array->NoJaggedArrays [held, tier 0, 0.22]

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | 21 | not covered yet |
| c2 | t[0].length is 3, and every row of a 2D array has the same length | mis:two_dimensional_array->RaggedRowsSameLength |
| c3 | so it visits three columns in every row and adds all six numbers | mis:two_dimensional_array->RaggedRowsSameLength |

**Graph check, not yet read (the walk may not stop while these remain):** pre:array_initializer->indexing, pre:indexing->array_bounds, pre:indexing->array_traversal, pre:indexing->two_dimensional_array, pre:two_dimensional_array->ragged_array, pre:two_dimensional_array->row_major_order

Figure 4 (the graph after depth 1): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY39_figure04.png

### Depth 2: current concepts 'ragged_array', 'two_dimensional_array', 'indexing'

#### ragged_array, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:two_dimensional_array->ragged_array \| rule: There is no requirement that all rows in a two-dimensional array have the same length; an array with rows of nonuniform length is known as a ragged array. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:two_dimensional_array->ragged_array (Score: 1.0)}
```
Kept by pruning: pre:two_dimensional_array->ragged_array (1.00)

Label prompt for concept edge pre:two_dimensional_array->ragged_array (two_dimensional_array -> ragged_array, prerequisite):
> There is no requirement that all rows in a two-dimensional array have the same length; an array with rows of nonuniform length is known as a ragged array.

Model's reply:
```
Label: broken
Clauses: 2, 3
Confidence: 0.95
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:two_dimensional_array->ragged_array | broken | 1.0 | 0.95 | 0.95 | c2, c3 | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |

#### two_dimensional_array, concept edges: 2 edges offered
Edges offered:
| edge |
|---|
| pre:indexing->two_dimensional_array \| rule: A 1-D array uses one index a[i]; a 2-D array uses two, a[i][j], where the first index chooses the row array. |
| pre:two_dimensional_array->ragged_array \| rule: There is no requirement that all rows in a two-dimensional array have the same length; an array with rows of nonuniform length is known as a ragged array. |
| pre:two_dimensional_array->row_major_order \| rule: Row-major order visits a[i][j] row by row (outer loop over i); column-major order puts the column loop outside. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
pre:indexing->two_dimensional_array (0.70), pre:two_dimensional_array->row_major_order (0.30)
```
Kept by pruning: pre:indexing->two_dimensional_array (0.70), pre:two_dimensional_array->row_major_order (0.30)

Label prompt for concept edge pre:indexing->two_dimensional_array (indexing -> two_dimensional_array, prerequisite):
> A 1-D array uses one index a[i]; a 2-D array uses two, a[i][j], where the first index chooses the row array.

Model's reply:
```
Label: broken
Clauses: 2, 3
Confidence: 0.7
```

Label prompt for concept edge pre:two_dimensional_array->row_major_order (two_dimensional_array -> row_major_order, prerequisite):
> Row-major order visits a[i][j] row by row (outer loop over i); column-major order puts the column loop outside.

Model's reply:
```
Label: confirmed
Clauses: 3
Confidence: 0.55
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:indexing->two_dimensional_array | broken | 0.7 | 0.7 | 0.49 | c2, c3 | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| pre:two_dimensional_array->row_major_order | confirmed | 0.3 | 0.55 | 0.17 | c3 | so it visits three columns in every row and adds all six numbers |

#### indexing, concept edges: 3 edges offered
Edges offered:
| edge |
|---|
| pre:array_initializer->indexing \| rule: The values listed in braces are stored at indices 0, 1, 2, ... in order, and a[i] reads the value at index i. |
| pre:indexing->array_bounds \| rule: Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used. |
| pre:indexing->array_traversal \| rule: A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass. |
| pre:indexing->two_dimensional_array \| rule: A 1-D array uses one index a[i]; a 2-D array uses two, a[i][j], where the first index chooses the row array. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{pre:indexing->array_bounds (Score: 0.5)}
{pre:array_initializer->indexing (Score: 0.3)}
{pre:indexing->array_traversal (Score: 0.2)}
```
Kept by pruning: pre:indexing->array_bounds (0.50), pre:array_initializer->indexing (0.30), pre:indexing->array_traversal (0.20)

Label prompt for concept edge pre:indexing->array_bounds (indexing -> array_bounds, prerequisite):
> Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used.

Model's reply:
```
Label: broken
Clauses: 1, 3
Confidence: 0.85
```

Label prompt for concept edge pre:array_initializer->indexing (array_initializer -> indexing, prerequisite):
> The values listed in braces are stored at indices 0, 1, 2, ... in order, and a[i] reads the value at index i.

Model's reply:
```
Label: broken
Clauses: 2, 3
Confidence: 0.6
```

Label prompt for concept edge pre:indexing->array_traversal (indexing -> array_traversal, prerequisite):
> A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.55
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:indexing->array_bounds | broken | 0.5 | 0.85 | 0.42 | c1, c3 | 21; so it visits three columns in every row and adds all six numbers |
| pre:array_initializer->indexing | broken | 0.3 | 0.6 | 0.18 | c2, c3 | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| pre:indexing->array_traversal | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:two_dimensional_array->ragged_array [broken, tier 0, 0.95], pre:indexing->two_dimensional_array [broken, tier 0, 0.49], pre:indexing->array_bounds [broken, tier 0, 0.42], pre:array_initializer->indexing [broken, tier 0, 0.18]

reached across pre:indexing->array_bounds, entered next: array_bounds

reached across pre:array_initializer->indexing, entered next: array_initializer

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | 21 | pre:indexing->array_bounds |
| c2 | t[0].length is 3, and every row of a 2D array has the same length | mis:two_dimensional_array->RaggedRowsSameLength |
| c3 | so it visits three columns in every row and adds all six numbers | mis:two_dimensional_array->RaggedRowsSameLength |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of array_bounds, own edges of array_initializer

Figure 5 (the graph after depth 2): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY39_figure05.png

### Depth 3: current concepts 'two_dimensional_array', 'ragged_array', 'indexing', 'array_bounds', 'array_initializer'

#### two_dimensional_array, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:indexing->two_dimensional_array \| rule: A 1-D array uses one index a[i]; a 2-D array uses two, a[i][j], where the first index chooses the row array. |
| pre:two_dimensional_array->ragged_array \| rule: There is no requirement that all rows in a two-dimensional array have the same length; an array with rows of nonuniform length is known as a ragged array. |
| pre:two_dimensional_array->row_major_order \| rule: Row-major order visits a[i][j] row by row (outer loop over i); column-major order puts the column loop outside. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
pre:two_dimensional_array->row_major_order (1.00)
```
Kept by pruning: pre:two_dimensional_array->row_major_order (1.00)

Label prompt for concept edge pre:two_dimensional_array->row_major_order (two_dimensional_array -> row_major_order, prerequisite):
> Row-major order visits a[i][j] row by row (outer loop over i); column-major order puts the column loop outside.

Model's reply:
```
Label: confirmed
Clauses: 3
Confidence: 0.55
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:two_dimensional_array->row_major_order | confirmed | 1.0 | 0.55 | 0.55 | c3 | so it visits three columns in every row and adds all six numbers |

#### indexing, concept edges: 1 edges offered
Edges offered:
| edge |
|---|
| pre:array_initializer->indexing \| rule: The values listed in braces are stored at indices 0, 1, 2, ... in order, and a[i] reads the value at index i. |
| pre:indexing->array_bounds \| rule: Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used. |
| pre:indexing->array_traversal \| rule: A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass. |
| pre:indexing->two_dimensional_array \| rule: A 1-D array uses one index a[i]; a 2-D array uses two, a[i][j], where the first index chooses the row array. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
pre:indexing->array_traversal (1.00)
```
Kept by pruning: pre:indexing->array_traversal (1.00)

Label prompt for concept edge pre:indexing->array_traversal (indexing -> array_traversal, prerequisite):
> A traversal uses the loop variable i as the index, so a[i] reaches a different element on each pass.

Model's reply:
```
Label: not applied
Clauses: none
Confidence: 0.55
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| pre:indexing->array_traversal | not applied |  |  | 0.0 |  |  |

#### array_bounds, misconceptions: 2 edges offered
Edges offered:
| edge |
|---|
| mis:array_bounds->OffByOneBound \| wrong rule: < vs <= and 0..n vs 0..n-1 are interchangeable \| right rule: for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n. |
| mis:array_bounds->OutOfBoundsElementsAreNull \| wrong rule: Reading a[a.length] just gives null or 0. \| right rule: Reading any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:array_bounds->OutOfBoundsElementsAreNull (0.75), mis:array_bounds->OffByOneBound (0.25)
```
Kept by pruning: mis:array_bounds->OutOfBoundsElementsAreNull (0.75), mis:array_bounds->OffByOneBound (0.25)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:array_bounds->OutOfBoundsElementsAreNull \| wrong rule: Reading a[a.length] just gives null or 0. \| right rule: Reading any index outside 0 to a.length - 1 throws ArrayIndexOutOfBoundsException. |
| mis:array_bounds->OffByOneBound \| wrong rule: < vs <= and 0..n vs 0..n-1 are interchangeable \| right rule: for (i = 0; i < n; i++) runs n times with i going up to n - 1; with <= it runs n + 1 times and reaches i = n. |
Model's reply:
```
mis:array_bounds->OutOfBoundsElementsAreNull | not applied | clauses: none | confidence: 0.7
mis:array_bounds->OffByOneBound | not applied | clauses: none | confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:array_bounds->OutOfBoundsElementsAreNull | not applied |  |  | 0.0 |  |  |
| mis:array_bounds->OffByOneBound | not applied |  |  | 0.0 |  |  |

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
{lvl:array_bounds@L0#2 (Score: 0.5)}
{lvl:array_bounds@L0#0 (Score: 0.3)}
{lvl:array_bounds@L3#0 (Score: 0.2)}
```
Kept by pruning: lvl:array_bounds@L0#2 (0.50), lvl:array_bounds@L0#0 (0.30), lvl:array_bounds@L3#0 (0.20)

Label prompt for level way lvl:array_bounds@L0#2 (the model saw only the concept, the way's name 'inconsistent trace' and its text; no level):
> Points to LT: the bounds check runs at every access, at run time. Inconsistent application: the trace accepts an index of a.length on the last pass (or -1 on the first) but rejects it elsewhere, or reads 'some value' there. (here mixing in: "an out-of-bounds read returns null (it throws)")

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.75
```

Label prompt for level way lvl:array_bounds@L0#0 (the model saw only the concept, the way's name 'everyday reading' and its text; no level):
> Folk meaning: in English, 'items 1 to 10' or 'up to n' includes the end point, and reading past the end of a list just gives 'nothing'. Java rule: the legal indices are 0..length-1, and any other index throws ArrayIndexOutOfBoundsException instead of returning a value.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.6
```

Label prompt for level way lvl:array_bounds@L3#0 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Every index value used in a[i] must satisfy 0 <= i <= a.length-1; the last element is a[a.length-1].

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:array_bounds@L0#2 | not applied |  |  | 0.0 |  |  |
| lvl:array_bounds@L0#0 | not applied |  |  | 0.0 |  |  |
| lvl:array_bounds@L3#0 | not applied |  |  | 0.0 |  |  |

#### array_initializer, misconceptions: 2 edges offered
Edges offered:
| edge |
|---|
| mis:array_initializer->ArrayBracketCountIsLength \| wrong rule: The number of brackets in an array type or initializer is the array's length. \| right rule: Brackets give the number of dimensions; the length is set at creation. |
| mis:array_initializer->ArrayInitializerContentsInBrackets \| wrong rule: Starting values go in square brackets, like int[] a = [v0, v1];. \| right rule: Starting values go in braces, like int[] a = {v0, v1};. |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
mis:array_initializer->ArrayBracketCountIsLength (0.85), mis:array_initializer->ArrayInitializerContentsInBrackets (0.15)
```
Kept by pruning: mis:array_initializer->ArrayBracketCountIsLength (0.85), mis:array_initializer->ArrayInitializerContentsInBrackets (0.15)

Label prompt for the misconception / error edges (judged together). The model saw the program, the question, the numbered clauses, and these edges with their wrong rule and right rule:
| edge |
|---|
| mis:array_initializer->ArrayBracketCountIsLength \| wrong rule: The number of brackets in an array type or initializer is the array's length. \| right rule: Brackets give the number of dimensions; the length is set at creation. |
| mis:array_initializer->ArrayInitializerContentsInBrackets \| wrong rule: Starting values go in square brackets, like int[] a = [v0, v1];. \| right rule: Starting values go in braces, like int[] a = {v0, v1};. |
Model's reply:
```
mis:array_initializer->ArrayBracketCountIsLength | not applied | clauses: none | confidence: 0.85
mis:array_initializer->ArrayInitializerContentsInBrackets | not applied | clauses: none | confidence: 0.9
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| mis:array_initializer->ArrayBracketCountIsLength | not applied |  |  | 0.0 |  |  |
| mis:array_initializer->ArrayInitializerContentsInBrackets | not applied |  |  | 0.0 |  |  |

#### array_initializer, level ways: 14 edges offered
Edges offered:
| edge |
|---|
| lvl:array_initializer@L0#0 \| level L0 way everyday_reading: Folk meaning: in maths, braces {1, 2, 3} denote a set (unordered, no repeats) and brackets [1, 2, 3] a list, so novices write int[] a = [1, 2, 3] or expect {1, 1, 2} to have 2 elements. Java rule: braces enclose an ordered, comma-separated list whose count (repeats included) is the length. |
| lvl:array_initializer@L0#2 \| level L0 way inconsistent_trace: Points to LT: an array of length k+1 is created, then v0..vk are stored at indices 0..k in order. Inconsistent application: the trace puts the first value at index 1 for one initializer but at index 0 for another, or counts the length differently. (here mixing in: "initializer values go in [] instead of {}") |
| lvl:array_initializer@L1#0 \| level L1 way names_the_element: Identity: an array initializer is a brace-enclosed, comma-separated list of values that creates and fills an array in one step. |
| lvl:array_initializer@L1#1 \| level L1 way states_the_rule: Declarative: 'T[] a = {v0, ..., vk};' declares, creates (no new needed) and initializes an array of length k+1. For 2-D arrays each row is its own brace list. The bare form is legal only in a declaration; elsewhere write new T[]{...}. |
| lvl:array_initializer@L2#0 \| level L2 way line_by_line_trace: Sequencing: the array of length k+1 is created, the initializer expressions are evaluated left to right and stored in a[0], a[1], ..., a[k], and then the reference is assigned to a. |
| lvl:array_initializer@L2#1 \| level L2 way output_prediction: Result: int[] a = {1, 2, 3}; gives a.length == 3, a[0] == 1, a[2] == 3. String[] suit = {"Clubs", "Diamonds", "Hearts", "Spades"}; gives suit.length == 4. |
| lvl:array_initializer@L2#2 \| level L2 way one_step_execution: State transition: one execution creates one array holding the listed values and sets the variable to its reference. |
| lvl:array_initializer@L3#0 \| level L3 way relation_to_neighbour: An initializer implies array creation: it is shorthand for new T[k+1] followed by k+1 element assignments, so new is not written. |
| lvl:array_initializer@L3#1 \| level L3 way purpose_of_the_whole: Plan/role: build small fixed tables of constants known when the program is written (suits, ranks, month names), usually used as fixed-value lookup tables. |
| lvl:array_initializer@L4#0 \| level L4 way predict_a_change: Conservation: adding or removing a value changes the length. Code that uses a.length (e.g. rank.length) adapts, while code with a hard-coded size breaks. Reordering values changes which index holds which value. |
| lvl:array_initializer@L4#1 \| level L4 way transfer_to_a_new_program: Applicability: use an initializer when all values are known at compile time and the array is small. When the values must be computed at run time, create the array with new and fill it in a loop. |
| lvl:array_initializer@L4#2 \| level L4 way diagnose_an_error: rule broken: Initializer values are enclosed in braces. Kind: compile-time. Trigger class: brackets are used, as in int[] a = [1, 2, 3]; (illegal start of expression) |
| lvl:array_initializer@L4#3 \| level L4 way diagnose_an_error: rule broken: The bare {...} form is allowed only in a declaration. Kind: compile-time. Trigger class: a = {1, 2, 3}; used as a later assignment (array constants can only be used in initializers) |
| lvl:array_initializer@L4#4 \| level L4 way diagnose_an_error: rule broken: Each value must be assignable to the element type. Kind: compile-time. Trigger class: int[] a = {1, 2.5}; (incompatible types: possible lossy conversion from double to int) |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:array_initializer@L1#1 (Score: 0.5)}
{lvl:array_initializer@L0#2 (Score: 0.3)}
{lvl:array_initializer@L2#1 (Score: 0.2)}
```
Kept by pruning: lvl:array_initializer@L1#1 (0.50), lvl:array_initializer@L0#2 (0.30), lvl:array_initializer@L2#1 (0.20)

Label prompt for level way lvl:array_initializer@L1#1 (the model saw only the concept, the way's name 'states the rule' and its text; no level):
> Declarative: 'T[] a = {v0, ..., vk};' declares, creates (no new needed) and initializes an array of length k+1. For 2-D arrays each row is its own brace list. The bare form is legal only in a declaration; elsewhere write new T[]{...}.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:array_initializer@L0#2 (the model saw only the concept, the way's name 'inconsistent trace' and its text; no level):
> Points to LT: an array of length k+1 is created, then v0..vk are stored at indices 0..k in order. Inconsistent application: the trace puts the first value at index 1 for one initializer but at index 0 for another, or counts the length differently. (here mixing in: "initializer values go in [] instead of {}")

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Label prompt for level way lvl:array_initializer@L2#1 (the model saw only the concept, the way's name 'output prediction' and its text; no level):
> Result: int[] a = {1, 2, 3}; gives a.length == 3, a[0] == 1, a[2] == 3. String[] suit = {"Clubs", "Diamonds", "Hearts", "Spades"}; gives suit.length == 4.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.7
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:array_initializer@L1#1 | not applied |  |  | 0.0 |  |  |
| lvl:array_initializer@L0#2 | not applied |  |  | 0.0 |  |  |
| lvl:array_initializer@L2#1 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth** (best N in tiers: held misconception / broken edge, then held error, then correct / confirmed / shown):

pre:two_dimensional_array->row_major_order [confirmed, tier 2, 0.55]

reached across pre:two_dimensional_array->row_major_order, entered next: row_major_order

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | 21 | pre:indexing->array_bounds |
| c2 | t[0].length is 3, and every row of a 2D array has the same length | mis:two_dimensional_array->RaggedRowsSameLength |
| c3 | so it visits three columns in every row and adds all six numbers | mis:two_dimensional_array->RaggedRowsSameLength |

**Graph check, not yet read (the walk may not stop while these remain):** own edges of row_major_order, pre:array_initializer->length_field

Figure 6 (the graph after depth 3): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY39_figure06.png

### Depth 4: current concepts 'row_major_order'

#### row_major_order, level ways: 13 edges offered
Edges offered:
| edge |
|---|
| lvl:row_major_order@L0#0 \| level L0 way everyday_reading: Folk meaning: tables are read left to right, top to bottom, as the only natural order, and 'row' and 'column' are easily swapped. Rule: the loop that is outside decides the order: an outer loop over rows i gives row-major order, an outer loop over columns j gives column-major order. |
| lvl:row_major_order@L1#0 \| level L1 way names_the_element: Identity: row-major order processes a 2-D array row by row; column-major order processes it column by column. |
| lvl:row_major_order@L1#1 \| level L1 way states_the_rule: Declarative: for (i < M) { for (j < N) ... a[i][j] } is row-major; for (j < N) { for (i < M) ... a[i][j] } is column-major. Both keep a[i][j] with i as the row. |
| lvl:row_major_order@L2#0 \| level L2 way line_by_line_trace: Sequencing (row-major print): i = 0, j runs over 0..N-1 printing a[0][j], newline; i = 1, ... So a[0][0], a[0][1], ..., a[1][0], ... in that order. |
| lvl:row_major_order@L2#1 \| level L2 way output_prediction: Result: row-major processing yields per-row results (row averages in column N, rows printed as lines); column-major yields per-column results (column averages in row M). |
| lvl:row_major_order@L2#2 \| level L2 way one_step_execution: State transition: each inner step processes one entry; each outer step completes one whole row (row-major) or column (column-major) and resets the per-row sum. |
| lvl:row_major_order@L3#0 \| level L3 way relation_to_neighbour: Because a[i] is a row array, row-major order walks along each row array in turn; column-major jumps between row arrays at each step. |
| lvl:row_major_order@L3#1 \| level L3 way relation_to_neighbour: Which loop is outside decides whether entries are processed row by row or column by column; the inner loop finishes for each outer value. |
| lvl:row_major_order@L3#2 \| level L3 way purpose_of_the_whole: Plan/role: choose the order that matches the result wanted, row-major for per-row results (and for printing), column-major for per-column results. |
| lvl:row_major_order@L4#0 \| level L4 way predict_a_change: Conservation: swapping the loops of an element-wise operation (copy, add) keeps the result and changes only the visiting order. For printing or per-row sums, swapping changes the output (transposed layout, column results). |
| lvl:row_major_order@L4#1 \| level L4 way transfer_to_a_new_program: Applicability: use row-major by default in Java (rows are arrays; printing goes line by line). Use column-major when the result is per column, and remember that ragged arrays have no full columns. |
| lvl:row_major_order@L4#2 \| level L4 way diagnose_an_error: rule broken: Each loop bound must match the index it controls (i < M rows, j < N columns). Kind: run-time exception. Trigger class: after swapping the loops the bounds are not swapped with them, so in a non-square array a[i][j] gets i up to N-1 (ArrayIndexOutOfBoundsException) |
| lvl:row_major_order@L4#3 \| level L4 way diagnose_an_error: rule broken: Per-row or per-column accumulators must be reset for each outer pass. Kind: silent logic error. Trigger class: sum is declared before the outer loop, so each row average includes all earlier rows |

Prune: the model's reply (edge id and score; the kept edges sum to 1):
```
{lvl:row_major_order@L4#2 (Score: 0.45)}
{lvl:row_major_order@L4#1 (Score: 0.35)}
{lvl:row_major_order@L3#0 (Score: 0.2)}
```
Kept by pruning: lvl:row_major_order@L4#2 (0.45), lvl:row_major_order@L4#1 (0.35), lvl:row_major_order@L3#0 (0.20)

Label prompt for level way lvl:row_major_order@L4#2 (the model saw only the concept, the way's name 'diagnose an error' and its text; no level):
> rule broken: Each loop bound must match the index it controls (i < M rows, j < N columns). Kind: run-time exception. Trigger class: after swapping the loops the bounds are not swapped with them, so in a non-square array a[i][j] gets i up to N-1 (ArrayIndexOutOfBoundsException)

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.9
```

Label prompt for level way lvl:row_major_order@L4#1 (the model saw only the concept, the way's name 'transfer to a new program' and its text; no level):
> Applicability: use row-major by default in Java (rows are arrays; printing goes line by line). Use column-major when the result is per column, and remember that ragged arrays have no full columns.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.85
```

Label prompt for level way lvl:row_major_order@L3#0 (the model saw only the concept, the way's name 'relation to neighbour' and its text; no level):
> Because a[i] is a row array, row-major order walks along each row array in turn; column-major jumps between row arrays at each step.

Model's reply:
```
Label: not shown
Clauses: none
Confidence: 0.8
```

Parsed labels:
| edge | label | prune score | confidence | score | clauses | words |
|---|---|---|---|---|---|---|
| lvl:row_major_order@L4#2 | not applied |  |  | 0.0 |  |  |
| lvl:row_major_order@L4#1 | not applied |  |  | 0.0 |  |  |
| lvl:row_major_order@L3#0 | not applied |  |  | 0.0 |  |  |

**Kept on a path at this depth:** nothing

**Clause coverage after this depth:**
| clause | text | covered by |
|---|---|---|
| c1 | 21 | pre:indexing->array_bounds |
| c2 | t[0].length is 3, and every row of a 2D array has the same length | mis:two_dimensional_array->RaggedRowsSameLength |
| c3 | so it visits three columns in every row and adds all six numbers | mis:two_dimensional_array->RaggedRowsSameLength |

**Graph check, not yet read (the walk may not stop while these remain):** pre:array_initializer->length_field, pre:nested_loops->row_major_order

Figure 7 (the graph after depth 4): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY39_figure07.png

Held set after the one-fault rules: mis:ragged_array->RaggedRowsSameLength, mis:ragged_array->NoJaggedArrays (same words as mis:ragged_array->RaggedRowsSameLength); filed at the dependent concept: mis:two_dimensional_array->RaggedRowsSameLength, mis:two_dimensional_array->NoJaggedArrays

Shadows (a held label on a prerequisite, on a generic concept, or at a concept where the graph attaches the misconception as context, resting on the words of a stronger label at the specific or primary concept, is one wrong sentence read twice; it marks no root cause and sets no level): mis:two_dimensional_array->RaggedRowsSameLength (shadow of mis:ragged_array->RaggedRowsSameLength), mis:two_dimensional_array->NoJaggedArrays (shadow of mis:ragged_array->NoJaggedArrays)

## 4. Diagnosis (rules over the labelled graph, no model)
Root-cause walk: held on ['ragged_array'], broken at [] (consequences: pre:two_dimensional_array->ragged_array, pre:indexing->two_dimensional_array, pre:indexing->array_bounds, pre:array_initializer->indexing), prerequisites {'indexing': ['array_initializer'], 'length_field': ['array_initializer'], 'compound_assignment': ['assignment'], 'increment_operators': ['assignment', 'loop_control'], 'boolean_expression': ['comparison_operators'], 'accumulator_pattern': ['compound_assignment', 'loop_body'], 'data_structure': ['data_type'], 'comparison_operators': ['expression'], 'array_traversal': ['for_loop', 'indexing', 'length_field'], 'loop_body': ['for_loop'], 'loop_scope': ['for_loop'], 'nested_loops': ['for_loop'], 'array_bounds': ['indexing'], 'two_dimensional_array': ['indexing'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable'], 'row_major_order': ['nested_loops', 'two_dimensional_array'], 'control_flow': ['statement'], 'println': ['statement'], 'ragged_array': ['two_dimensional_array']}
- ragged_array: L0 via misconception "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers"
- two_dimensional_array: L0 via everyday_reading "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers"

**Stop:** max depth at depth 4; prompts {'prune': 16, 'label': 31}, fresh model calls 0, cache hits 47

### Held misconceptions
| concept | misconception | kind | quote | score | shares_evidence_with |
|---|---|---|---|---|---|
| ragged_array | RaggedRowsSameLength | misconception | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers | 0.57 |  |
| ragged_array | NoJaggedArrays | misconception | t[0].length is 3, and every row of a 2D array has the same length | 0.22 | mis:ragged_array->RaggedRowsSameLength |

### Shadowed labels (held in the reading, folded into the label they shadow; not faults of their own)
| concept | misconception | shadow_of | quote | score |
|---|---|---|---|---|
| two_dimensional_array | RaggedRowsSameLength | mis:ragged_array->RaggedRowsSameLength | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers | 0.465 |
| two_dimensional_array | NoJaggedArrays | mis:ragged_array->NoJaggedArrays | t[0].length is 3, and every row of a 2D array has the same length | 0.28 |

### Broken concept edges
| edge | quote | score | consequence_of |
|---|---|---|---|
| pre:two_dimensional_array->ragged_array | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers | 0.95 | mis:ragged_array->RaggedRowsSameLength |
| pre:indexing->two_dimensional_array | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers | 0.49 | mis:ragged_array->RaggedRowsSameLength |
| pre:indexing->array_bounds | 21; so it visits three columns in every row and adds all six numbers | 0.425 | mis:ragged_array->RaggedRowsSameLength |
| pre:array_initializer->indexing | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers | 0.18 | mis:ragged_array->RaggedRowsSameLength |

### Root cause: ragged_array / RaggedRowsSameLength

### Level per concept
| concept | level | way | misconception | source | quote | rule | also | note |
|---|---|---|---|---|---|---|---|---|
| ragged_array | L0 | misconception | RaggedRowsSameLength | level_mis_links | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers | wrong rule: All rows of a 2-D array have the same length, so one N works for every row. Right rule: Rows may differ in length; use a[i].length for row i. | NoJaggedArrays |  |
| two_dimensional_array | L0 | everyday_reading |  | level_way | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |  |  |  |

### Overall level: L0

Clause coverage (final):
| clause | covered by |
|---|---|
| 21 | pre:indexing->array_bounds |
| t[0].length is 3, and every row of a 2D array has the same length | mis:two_dimensional_array->RaggedRowsSameLength |
| so it visits three columns in every row and adds all six numbers | mis:two_dimensional_array->RaggedRowsSameLength |

Figure 8 (final picture): C:\Users\magnu\OneDrive\Desktop\ES_VIterbi_Personalized_Learning\results\viewer\MY39_figure08.png

## 5. Every labelled edge (the evidence list, kept or not)
| depth | source | edge | kind | label | prune_score | confidence | score | clauses | quote |
|---|---|---|---|---|---|---|---|---|---|
| 1 | two_dimensional_array | mis:two_dimensional_array->RaggedRowsSameLength | misconception | held | 0.5 | 0.93 | 0.465 | [2, 3] | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| 1 | two_dimensional_array | mis:two_dimensional_array->NoJaggedArrays | misconception | held | 0.4 | 0.7 | 0.28 | [2] | t[0].length is 3, and every row of a 2D array has the same length |
| 1 | two_dimensional_array | mis:two_dimensional_array->MultidimensionalArray | misconception | correct | 0.1 | 0.6 | 0.06 | [2] | t[0].length is 3, and every row of a 2D array has the same length |
| 1 | two_dimensional_array | lvl:two_dimensional_array@L0#0 | level | shown | 0.3 | 0.7 | 0.21 | [2, 3] | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| 1 | ragged_array | mis:ragged_array->RaggedRowsSameLength | misconception | held | 0.6 | 0.95 | 0.57 | [2, 3] | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| 1 | ragged_array | mis:ragged_array->NoJaggedArrays | misconception | held | 0.4 | 0.55 | 0.22 | [2] | t[0].length is 3, and every row of a 2D array has the same length |
| 1 | ragged_array | lvl:ragged_array@L0#0 | level | shown | 0.5 | 0.8 | 0.4 | [2, 3] | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| 1 | ragged_array | lvl:ragged_array@L0#3 | level | shown | 0.35 | 0.8 | 0.28 | [2, 3] | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| 1 | indexing | mis:indexing->ArrayRangeInclusive | misconception | correct | 0.3 | 0.55 | 0.165 | [2, 3] | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| 2 | ragged_array | pre:two_dimensional_array->ragged_array | prerequisite | broken | 1.0 | 0.95 | 0.95 | [2, 3] | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| 2 | two_dimensional_array | pre:indexing->two_dimensional_array | prerequisite | broken | 0.7 | 0.7 | 0.49 | [2, 3] | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| 2 | two_dimensional_array | pre:two_dimensional_array->row_major_order | prerequisite | confirmed | 0.3 | 0.55 | 0.165 | [3] | so it visits three columns in every row and adds all six numbers |
| 2 | indexing | pre:indexing->array_bounds | prerequisite | broken | 0.5 | 0.85 | 0.425 | [1, 3] | 21; so it visits three columns in every row and adds all six numbers |
| 2 | indexing | pre:array_initializer->indexing | prerequisite | broken | 0.3 | 0.6 | 0.18 | [2, 3] | t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers |
| 3 | two_dimensional_array | pre:two_dimensional_array->row_major_order | prerequisite | confirmed | 1.0 | 0.55 | 0.55 | [3] | so it visits three columns in every row and adds all six numbers |

## 6. The paths (what the keep step kept, depth by depth)
| depth | source | edge | kind | label | score | clauses |
|---|---|---|---|---|---|---|
| 1 | ragged_array | mis:ragged_array->RaggedRowsSameLength | misconception | held | 0.57 | [2, 3] |
| 1 | two_dimensional_array | mis:two_dimensional_array->RaggedRowsSameLength | misconception | held | 0.465 | [2, 3] |
| 1 | two_dimensional_array | mis:two_dimensional_array->NoJaggedArrays | misconception | held | 0.28 | [2] |
| 1 | ragged_array | mis:ragged_array->NoJaggedArrays | misconception | held | 0.22 | [2] |
| 2 | ragged_array | pre:two_dimensional_array->ragged_array | prerequisite | broken | 0.95 | [2, 3] |
| 2 | two_dimensional_array | pre:indexing->two_dimensional_array | prerequisite | broken | 0.49 | [2, 3] |
| 2 | indexing | pre:indexing->array_bounds | prerequisite | broken | 0.425 | [1, 3] |
| 2 | indexing | pre:array_initializer->indexing | prerequisite | broken | 0.18 | [2, 3] |
| 3 | two_dimensional_array | pre:two_dimensional_array->row_major_order | prerequisite | confirmed | 0.55 | [3] |

## 7. Raw traversal log
```
clauses: 21 | t[0].length is 3, and every row of a 2D array has the same length | so it visits three columns in every row and adds all six numbers
start: BM25 of the answer against each tagged concept: two_dimensional_array 28.24 (hits 2), ragged_array 24.31 (hits 2), indexing 20.88 (hits 1), array_traversal 19.88 (hits 1), length_field 16.10 (hits 1), loop_control 14.92 (hits 1), array_initializer 14.01 (hits 1), for_loop 13.06 (hits 1), row_major_order 11.27 (hits 1), increment_operators 10.97 (hits 1), comparison_operators 10.50 (hits 1), compound_assignment 9.75 (hits 1), nested_loops 9.49 (hits 1), array_bounds 9.25 (hits 1), loop_variable 8.67 (hits 1), loop_body 8.59 (hits 1), loop_scope 7.53 (hits 1), accumulator_pattern 6.26 (hits 1), boolean_expression 6.17 (hits 1), println 4.52 (hits 1), control_flow 3.58 (hits 1), data_structure 1.77 (hits 1)
start: chosen two_dimensional_array, ragged_array, indexing
start concepts (3): two_dimensional_array, ragged_array, indexing
--- depth 1: current concepts ['two_dimensional_array', 'ragged_array', 'indexing']
  two_dimensional_array (misconceptions): 7 candidates -> kept mis:two_dimensional_array->RaggedRowsSameLength (0.50), mis:two_dimensional_array->NoJaggedArrays (0.40), mis:two_dimensional_array->MultidimensionalArray (0.10)
    mis:two_dimensional_array->RaggedRowsSameLength -> held (0.47) "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers"
    mis:two_dimensional_array->NoJaggedArrays -> held (0.28) "t[0].length is 3, and every row of a 2D array has the same length"
    mis:two_dimensional_array->MultidimensionalArray -> correct (0.06) "t[0].length is 3, and every row of a 2D array has the same length"
  two_dimensional_array (level ways): 18 candidates -> kept lvl:two_dimensional_array@L3#2 (0.45), lvl:two_dimensional_array@L0#0 (0.30), lvl:two_dimensional_array@L4#2 (0.25)
    lvl:two_dimensional_array@L3#2 -> not applied (0.00) ""
    lvl:two_dimensional_array@L0#0 -> shown (0.21) "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers"
    lvl:two_dimensional_array@L4#2 -> not applied (0.00) ""
  ragged_array (misconceptions): 2 candidates -> kept mis:ragged_array->RaggedRowsSameLength (0.60), mis:ragged_array->NoJaggedArrays (0.40)
    mis:ragged_array->RaggedRowsSameLength -> held (0.57) "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers"
    mis:ragged_array->NoJaggedArrays -> held (0.22) "t[0].length is 3, and every row of a 2D array has the same length"
  ragged_array (level ways): 13 candidates -> kept lvl:ragged_array@L0#0 (0.50), lvl:ragged_array@L0#3 (0.35), lvl:ragged_array@L4#2 (0.15)
    lvl:ragged_array@L0#0 -> shown (0.40) "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers"
    lvl:ragged_array@L0#3 -> shown (0.28) "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers"
    lvl:ragged_array@L4#2 -> not applied (0.00) ""
  indexing (misconceptions): 8 candidates -> kept mis:indexing->ArrayUseScansAllCells (0.50), mis:indexing->ArrayRangeInclusive (0.30), mis:indexing->IndexIsValue (0.20)
    mis:indexing->ArrayUseScansAllCells -> not applied (0.00) ""
    mis:indexing->ArrayRangeInclusive -> correct (0.17) "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers"
    mis:indexing->IndexIsValue -> not applied (0.00) ""
  indexing (level ways): 21 candidates -> kept lvl:indexing@L3#3 (0.45), lvl:indexing@L4#2 (0.35), lvl:indexing@L3#2 (0.20)
    lvl:indexing@L3#3 -> not applied (0.00) ""
    lvl:indexing@L4#2 -> not applied (0.00) ""
    lvl:indexing@L3#2 -> not applied (0.00) ""
  kept: mis:ragged_array->RaggedRowsSameLength [held, tier 0, 0.57], mis:two_dimensional_array->RaggedRowsSameLength [held, tier 0, 0.47], mis:two_dimensional_array->NoJaggedArrays [held, tier 0, 0.28], mis:ragged_array->NoJaggedArrays [held, tier 0, 0.22]
  clause coverage: c1 uncovered; c2 <- mis:two_dimensional_array->RaggedRowsSameLength; c3 <- mis:two_dimensional_array->RaggedRowsSameLength
  not yet read: pre:array_initializer->indexing, pre:indexing->array_bounds, pre:indexing->array_traversal, pre:indexing->two_dimensional_array, pre:two_dimensional_array->ragged_array, pre:two_dimensional_array->row_major_order
--- depth 2: current concepts ['ragged_array', 'two_dimensional_array', 'indexing']
  ragged_array (concept edges): 1 candidates -> kept pre:two_dimensional_array->ragged_array (1.00)
    pre:two_dimensional_array->ragged_array -> broken (0.95) "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers"
  two_dimensional_array (concept edges): 2 candidates -> kept pre:indexing->two_dimensional_array (0.70), pre:two_dimensional_array->row_major_order (0.30)
    pre:indexing->two_dimensional_array -> broken (0.49) "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers"
    pre:two_dimensional_array->row_major_order -> confirmed (0.17) "so it visits three columns in every row and adds all six numbers"
  indexing (concept edges): 3 candidates -> kept pre:indexing->array_bounds (0.50), pre:array_initializer->indexing (0.30), pre:indexing->array_traversal (0.20)
    pre:indexing->array_bounds -> broken (0.42) "21; so it visits three columns in every row and adds all six numbers"
    pre:array_initializer->indexing -> broken (0.18) "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers"
    pre:indexing->array_traversal -> not applied (0.00) ""
  kept: pre:two_dimensional_array->ragged_array [broken, tier 0, 0.95], pre:indexing->two_dimensional_array [broken, tier 0, 0.49], pre:indexing->array_bounds [broken, tier 0, 0.42], pre:array_initializer->indexing [broken, tier 0, 0.18]
  reached across pre:indexing->array_bounds, entered next: array_bounds
  reached across pre:array_initializer->indexing, entered next: array_initializer
  clause coverage: c1 <- pre:indexing->array_bounds; c2 <- mis:two_dimensional_array->RaggedRowsSameLength; c3 <- mis:two_dimensional_array->RaggedRowsSameLength
  not yet read: own edges of array_bounds, own edges of array_initializer
--- depth 3: current concepts ['two_dimensional_array', 'ragged_array', 'indexing', 'array_bounds', 'array_initializer']
  two_dimensional_array (concept edges): 1 candidates -> kept pre:two_dimensional_array->row_major_order (1.00)
    pre:two_dimensional_array->row_major_order -> confirmed (0.55) "so it visits three columns in every row and adds all six numbers"
  indexing (concept edges): 1 candidates -> kept pre:indexing->array_traversal (1.00)
    pre:indexing->array_traversal -> not applied (0.00) ""
  array_bounds (misconceptions): 2 candidates -> kept mis:array_bounds->OutOfBoundsElementsAreNull (0.75), mis:array_bounds->OffByOneBound (0.25)
    mis:array_bounds->OutOfBoundsElementsAreNull -> not applied (0.00) ""
    mis:array_bounds->OffByOneBound -> not applied (0.00) ""
  array_bounds (level ways): 14 candidates -> kept lvl:array_bounds@L0#2 (0.50), lvl:array_bounds@L0#0 (0.30), lvl:array_bounds@L3#0 (0.20)
    lvl:array_bounds@L0#2 -> not applied (0.00) ""
    lvl:array_bounds@L0#0 -> not applied (0.00) ""
    lvl:array_bounds@L3#0 -> not applied (0.00) ""
  array_initializer (misconceptions): 2 candidates -> kept mis:array_initializer->ArrayBracketCountIsLength (0.85), mis:array_initializer->ArrayInitializerContentsInBrackets (0.15)
    mis:array_initializer->ArrayBracketCountIsLength -> not applied (0.00) ""
    mis:array_initializer->ArrayInitializerContentsInBrackets -> not applied (0.00) ""
  array_initializer (level ways): 14 candidates -> kept lvl:array_initializer@L1#1 (0.50), lvl:array_initializer@L0#2 (0.30), lvl:array_initializer@L2#1 (0.20)
    lvl:array_initializer@L1#1 -> not applied (0.00) ""
    lvl:array_initializer@L0#2 -> not applied (0.00) ""
    lvl:array_initializer@L2#1 -> not applied (0.00) ""
  kept: pre:two_dimensional_array->row_major_order [confirmed, tier 2, 0.55]
  reached across pre:two_dimensional_array->row_major_order, entered next: row_major_order
  clause coverage: c1 <- pre:indexing->array_bounds; c2 <- mis:two_dimensional_array->RaggedRowsSameLength; c3 <- mis:two_dimensional_array->RaggedRowsSameLength
  not yet read: own edges of row_major_order, pre:array_initializer->length_field
--- depth 4: current concepts ['row_major_order'] (closing round: own edges only)
  row_major_order (level ways): 13 candidates -> kept lvl:row_major_order@L4#2 (0.45), lvl:row_major_order@L4#1 (0.35), lvl:row_major_order@L3#0 (0.20)
    lvl:row_major_order@L4#2 -> not applied (0.00) ""
    lvl:row_major_order@L4#1 -> not applied (0.00) ""
    lvl:row_major_order@L3#0 -> not applied (0.00) ""
  nothing kept at this depth
  clause coverage: c1 <- pre:indexing->array_bounds; c2 <- mis:two_dimensional_array->RaggedRowsSameLength; c3 <- mis:two_dimensional_array->RaggedRowsSameLength
  not yet read: pre:array_initializer->length_field, pre:nested_loops->row_major_order
  held: mis:ragged_array->RaggedRowsSameLength, mis:ragged_array->NoJaggedArrays (same words as mis:ragged_array->RaggedRowsSameLength); filed at the dependent concept: mis:two_dimensional_array->RaggedRowsSameLength, mis:two_dimensional_array->NoJaggedArrays
  shadows: mis:two_dimensional_array->RaggedRowsSameLength (shadow of mis:ragged_array->RaggedRowsSameLength), mis:two_dimensional_array->NoJaggedArrays (shadow of mis:ragged_array->NoJaggedArrays)
  root-cause walk: held on ['ragged_array'], broken at [] (consequences: pre:two_dimensional_array->ragged_array, pre:indexing->two_dimensional_array, pre:indexing->array_bounds, pre:array_initializer->indexing), prerequisites {'indexing': ['array_initializer'], 'length_field': ['array_initializer'], 'compound_assignment': ['assignment'], 'increment_operators': ['assignment', 'loop_control'], 'boolean_expression': ['comparison_operators'], 'accumulator_pattern': ['compound_assignment', 'loop_body'], 'data_structure': ['data_type'], 'comparison_operators': ['expression'], 'array_traversal': ['for_loop', 'indexing', 'length_field'], 'loop_body': ['for_loop'], 'loop_scope': ['for_loop'], 'nested_loops': ['for_loop'], 'array_bounds': ['indexing'], 'two_dimensional_array': ['indexing'], 'for_loop': ['loop_control'], 'loop_control': ['loop_variable'], 'row_major_order': ['nested_loops', 'two_dimensional_array'], 'control_flow': ['statement'], 'println': ['statement'], 'ragged_array': ['two_dimensional_array']}
  level ragged_array: L0 via misconception "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers"
  level two_dimensional_array: L0 via everyday_reading "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers"
```

## 8. Full diagnosis JSON
```json
{
 "scenario": "MY39",
 "settings": {
  "width": 3,
  "depth": 3,
  "prune_tools": "llm",
  "model": "claude-opus-5-5",
  "backend": "claude-cli"
 },
 "clauses": [
  "21",
  "t[0].length is 3, and every row of a 2D array has the same length",
  "so it visits three columns in every row and adds all six numbers"
 ],
 "start_concepts": [
  "two_dimensional_array",
  "ragged_array",
  "indexing"
 ],
 "held_misconceptions": [
  {
   "concept": "ragged_array",
   "misconception": "RaggedRowsSameLength",
   "kind": "misconception",
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "score": 0.57
  },
  {
   "concept": "ragged_array",
   "misconception": "NoJaggedArrays",
   "kind": "misconception",
   "quote": "t[0].length is 3, and every row of a 2D array has the same length",
   "score": 0.22,
   "shares_evidence_with": "mis:ragged_array->RaggedRowsSameLength"
  }
 ],
 "error_evidence": [],
 "shadowed": [
  {
   "concept": "two_dimensional_array",
   "misconception": "RaggedRowsSameLength",
   "shadow_of": "mis:ragged_array->RaggedRowsSameLength",
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "score": 0.465
  },
  {
   "concept": "two_dimensional_array",
   "misconception": "NoJaggedArrays",
   "shadow_of": "mis:ragged_array->NoJaggedArrays",
   "quote": "t[0].length is 3, and every row of a 2D array has the same length",
   "score": 0.28
  }
 ],
 "broken_edges": [
  {
   "edge": "pre:two_dimensional_array->ragged_array",
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "score": 0.95,
   "consequence_of": "mis:ragged_array->RaggedRowsSameLength"
  },
  {
   "edge": "pre:indexing->two_dimensional_array",
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "score": 0.49,
   "consequence_of": "mis:ragged_array->RaggedRowsSameLength"
  },
  {
   "edge": "pre:indexing->array_bounds",
   "quote": "21; so it visits three columns in every row and adds all six numbers",
   "score": 0.425,
   "consequence_of": "mis:ragged_array->RaggedRowsSameLength"
  },
  {
   "edge": "pre:array_initializer->indexing",
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "score": 0.18,
   "consequence_of": "mis:ragged_array->RaggedRowsSameLength"
  }
 ],
 "root_cause": {
  "concept": "ragged_array",
  "misconception": "RaggedRowsSameLength"
 },
 "levels": {
  "ragged_array": {
   "level": "L0",
   "way": "misconception",
   "misconception": "RaggedRowsSameLength",
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "edge": "mis:ragged_array->RaggedRowsSameLength",
   "rule": "wrong rule: All rows of a 2-D array have the same length, so one N works for every row. Right rule: Rows may differ in length; use a[i].length for row i.",
   "source": "level_mis_links",
   "also_held": [
    "NoJaggedArrays"
   ]
  },
  "two_dimensional_array": {
   "level": "L0",
   "way": "everyday_reading",
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "edge": "lvl:two_dimensional_array@L0#0",
   "source": "level_way",
   "also_shown": []
  }
 },
 "overall_level": "L0",
 "paths": [
  {
   "depth": 1,
   "source": "ragged_array",
   "edge": "mis:ragged_array->RaggedRowsSameLength",
   "target": "RaggedRowsSameLength",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2,
    3
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.95,
   "prune_score": 0.6,
   "score": 0.57,
   "logic": "All rows of a 2-D array have the same length, so one N works for every row.",
   "twin_logic": "Rows may differ in length; use a[i].length for row i.",
   "role": "primary"
  },
  {
   "depth": 1,
   "source": "two_dimensional_array",
   "edge": "mis:two_dimensional_array->RaggedRowsSameLength",
   "target": "RaggedRowsSameLength",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2,
    3
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.93,
   "prune_score": 0.5,
   "score": 0.465,
   "logic": "All rows of a 2-D array have the same length, so one N works for every row.",
   "twin_logic": "Rows may differ in length; use a[i].length for row i.",
   "role": "context"
  },
  {
   "depth": 1,
   "source": "two_dimensional_array",
   "edge": "mis:two_dimensional_array->NoJaggedArrays",
   "target": "NoJaggedArrays",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length",
   "confidence": 0.7,
   "prune_score": 0.4,
   "score": 0.28,
   "logic": "Every row of a 2-D array must have the same length.",
   "twin_logic": "Each row a[i] is its own array, so rows can have different lengths a[i].length.",
   "role": "context",
   "shares_evidence_with": "mis:two_dimensional_array->RaggedRowsSameLength"
  },
  {
   "depth": 1,
   "source": "ragged_array",
   "edge": "mis:ragged_array->NoJaggedArrays",
   "target": "NoJaggedArrays",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length",
   "confidence": 0.55,
   "prune_score": 0.4,
   "score": 0.22,
   "logic": "multi-dimensional arrays must be rectangular",
   "twin_logic": "Each row a[i] is its own array, so rows can have different lengths a[i].length.",
   "role": "primary",
   "shares_evidence_with": "mis:ragged_array->RaggedRowsSameLength"
  },
  {
   "depth": 2,
   "source": "ragged_array",
   "edge": "pre:two_dimensional_array->ragged_array",
   "target": "two_dimensional_array",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    2,
    3
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.95,
   "prune_score": 1.0,
   "score": 0.95,
   "logic": "There is no requirement that all rows in a two-dimensional array have the same length; an array with rows of nonuniform length is known as a ragged array.",
   "twin_logic": null,
   "consequence_of": "mis:ragged_array->RaggedRowsSameLength"
  },
  {
   "depth": 2,
   "source": "two_dimensional_array",
   "edge": "pre:indexing->two_dimensional_array",
   "target": "indexing",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    2,
    3
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.7,
   "prune_score": 0.7,
   "score": 0.49,
   "logic": "A 1-D array uses one index a[i]; a 2-D array uses two, a[i][j], where the first index chooses the row array.",
   "twin_logic": null,
   "consequence_of": "mis:ragged_array->RaggedRowsSameLength"
  },
  {
   "depth": 2,
   "source": "indexing",
   "edge": "pre:indexing->array_bounds",
   "target": "array_bounds",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    3
   ],
   "quote": "21; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.85,
   "prune_score": 0.5,
   "score": 0.425,
   "logic": "Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used.",
   "twin_logic": null,
   "consequence_of": "mis:ragged_array->RaggedRowsSameLength"
  },
  {
   "depth": 2,
   "source": "indexing",
   "edge": "pre:array_initializer->indexing",
   "target": "array_initializer",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    2,
    3
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.6,
   "prune_score": 0.3,
   "score": 0.18,
   "logic": "The values listed in braces are stored at indices 0, 1, 2, ... in order, and a[i] reads the value at index i.",
   "twin_logic": null,
   "consequence_of": "mis:ragged_array->RaggedRowsSameLength"
  },
  {
   "depth": 3,
   "source": "two_dimensional_array",
   "edge": "pre:two_dimensional_array->row_major_order",
   "target": "row_major_order",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3
   ],
   "quote": "so it visits three columns in every row and adds all six numbers",
   "confidence": 0.55,
   "prune_score": 1.0,
   "score": 0.55,
   "logic": "Row-major order visits a[i][j] row by row (outer loop over i); column-major order puts the column loop outside.",
   "twin_logic": null
  }
 ],
 "evidence": [
  {
   "depth": 1,
   "source": "two_dimensional_array",
   "edge": "mis:two_dimensional_array->RaggedRowsSameLength",
   "target": "RaggedRowsSameLength",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2,
    3
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.93,
   "prune_score": 0.5,
   "score": 0.465,
   "logic": "All rows of a 2-D array have the same length, so one N works for every row.",
   "twin_logic": "Rows may differ in length; use a[i].length for row i.",
   "role": "context"
  },
  {
   "depth": 1,
   "source": "two_dimensional_array",
   "edge": "mis:two_dimensional_array->NoJaggedArrays",
   "target": "NoJaggedArrays",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length",
   "confidence": 0.7,
   "prune_score": 0.4,
   "score": 0.28,
   "logic": "Every row of a 2-D array must have the same length.",
   "twin_logic": "Each row a[i] is its own array, so rows can have different lengths a[i].length.",
   "role": "context",
   "shares_evidence_with": "mis:two_dimensional_array->RaggedRowsSameLength"
  },
  {
   "depth": 1,
   "source": "two_dimensional_array",
   "edge": "mis:two_dimensional_array->MultidimensionalArray",
   "target": "MultidimensionalArray",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    2
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length",
   "confidence": 0.6,
   "prune_score": 0.1,
   "score": 0.06,
   "logic": "int[m][n] is one block of m * n values, so a[i] on its own means nothing.",
   "twin_logic": "A 2-D array is an array of m row arrays, so a[i] is a 1-D array of length n.",
   "role": "primary"
  },
  {
   "depth": 1,
   "source": "two_dimensional_array",
   "edge": "lvl:two_dimensional_array@L0#0",
   "target": "two_dimensional_array@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.7,
   "prune_score": 0.3,
   "score": 0.21,
   "logic": "Folk meaning: a table or matrix is one grid in which rows and columns are symmetric, so a column should be as easy to pick out as a row. Java rule: a 2-D array is an array of row arrays; a[i] is row i, a[i][j] an element, and there is no expression for a column.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 1,
   "source": "ragged_array",
   "edge": "mis:ragged_array->RaggedRowsSameLength",
   "target": "RaggedRowsSameLength",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2,
    3
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.95,
   "prune_score": 0.6,
   "score": 0.57,
   "logic": "All rows of a 2-D array have the same length, so one N works for every row.",
   "twin_logic": "Rows may differ in length; use a[i].length for row i.",
   "role": "primary"
  },
  {
   "depth": 1,
   "source": "ragged_array",
   "edge": "mis:ragged_array->NoJaggedArrays",
   "target": "NoJaggedArrays",
   "kind": "misconception",
   "label": "held",
   "clauses": [
    2
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length",
   "confidence": 0.55,
   "prune_score": 0.4,
   "score": 0.22,
   "logic": "multi-dimensional arrays must be rectangular",
   "twin_logic": "Each row a[i] is its own array, so rows can have different lengths a[i].length.",
   "role": "primary",
   "shares_evidence_with": "mis:ragged_array->RaggedRowsSameLength"
  },
  {
   "depth": 1,
   "source": "ragged_array",
   "edge": "lvl:ragged_array@L0#0",
   "target": "ragged_array@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.8,
   "prune_score": 0.5,
   "score": 0.4,
   "logic": "Folk meaning: a 'table' has the same number of columns in every row, so one width N serves all rows. Java rule: each row is a separate array, so rows may have different lengths, and code must use a[i].length for row i.",
   "twin_logic": null,
   "level": "L0",
   "way": "everyday_reading"
  },
  {
   "depth": 1,
   "source": "ragged_array",
   "edge": "lvl:ragged_array@L0#3",
   "target": "ragged_array@L0",
   "kind": "level",
   "label": "shown",
   "clauses": [
    2,
    3
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.8,
   "prune_score": 0.35,
   "score": 0.28,
   "logic": "Points to LT: the inner bound a[i].length is re-evaluated for each row. Inconsistent application: the trace uses row 0's length (or N) for every row, sometimes over-running a short row and sometimes stopping early in a long one. (here mixing in: \"All rows of a 2-D array have the same length, so one N works for every row\")",
   "twin_logic": null,
   "level": "L0",
   "way": "inconsistent_trace"
  },
  {
   "depth": 1,
   "source": "indexing",
   "edge": "mis:indexing->ArrayRangeInclusive",
   "target": "ArrayRangeInclusive",
   "kind": "misconception",
   "label": "correct",
   "clauses": [
    2,
    3
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.55,
   "prune_score": 0.3,
   "score": 0.165,
   "logic": "new int[n] has slots 0 to n, inclusive.",
   "twin_logic": "The slots are 0 to n - 1.",
   "role": "primary"
  },
  {
   "depth": 2,
   "source": "ragged_array",
   "edge": "pre:two_dimensional_array->ragged_array",
   "target": "two_dimensional_array",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    2,
    3
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.95,
   "prune_score": 1.0,
   "score": 0.95,
   "logic": "There is no requirement that all rows in a two-dimensional array have the same length; an array with rows of nonuniform length is known as a ragged array.",
   "twin_logic": null,
   "consequence_of": "mis:ragged_array->RaggedRowsSameLength"
  },
  {
   "depth": 2,
   "source": "two_dimensional_array",
   "edge": "pre:indexing->two_dimensional_array",
   "target": "indexing",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    2,
    3
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.7,
   "prune_score": 0.7,
   "score": 0.49,
   "logic": "A 1-D array uses one index a[i]; a 2-D array uses two, a[i][j], where the first index chooses the row array.",
   "twin_logic": null,
   "consequence_of": "mis:ragged_array->RaggedRowsSameLength"
  },
  {
   "depth": 2,
   "source": "two_dimensional_array",
   "edge": "pre:two_dimensional_array->row_major_order",
   "target": "row_major_order",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3
   ],
   "quote": "so it visits three columns in every row and adds all six numbers",
   "confidence": 0.55,
   "prune_score": 0.3,
   "score": 0.165,
   "logic": "Row-major order visits a[i][j] row by row (outer loop over i); column-major order puts the column loop outside.",
   "twin_logic": null
  },
  {
   "depth": 2,
   "source": "indexing",
   "edge": "pre:indexing->array_bounds",
   "target": "array_bounds",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    1,
    3
   ],
   "quote": "21; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.85,
   "prune_score": 0.5,
   "score": 0.425,
   "logic": "Valid indexes run from 0 to a.length - 1; any other index throws an exception when it is used.",
   "twin_logic": null,
   "consequence_of": "mis:ragged_array->RaggedRowsSameLength"
  },
  {
   "depth": 2,
   "source": "indexing",
   "edge": "pre:array_initializer->indexing",
   "target": "array_initializer",
   "kind": "prerequisite",
   "label": "broken",
   "clauses": [
    2,
    3
   ],
   "quote": "t[0].length is 3, and every row of a 2D array has the same length; so it visits three columns in every row and adds all six numbers",
   "confidence": 0.6,
   "prune_score": 0.3,
   "score": 0.18,
   "logic": "The values listed in braces are stored at indices 0, 1, 2, ... in order, and a[i] reads the value at index i.",
   "twin_logic": null,
   "consequence_of": "mis:ragged_array->RaggedRowsSameLength"
  },
  {
   "depth": 3,
   "source": "two_dimensional_array",
   "edge": "pre:two_dimensional_array->row_major_order",
   "target": "row_major_order",
   "kind": "prerequisite",
   "label": "confirmed",
   "clauses": [
    3
   ],
   "quote": "so it visits three columns in every row and adds all six numbers",
   "confidence": 0.55,
   "prune_score": 1.0,
   "score": 0.55,
   "logic": "Row-major order visits a[i][j] row by row (outer loop over i); column-major order puts the column loop outside.",
   "twin_logic": null
  }
 ],
 "clause_coverage": {
  "21": "pre:indexing->array_bounds",
  "t[0].length is 3, and every row of a 2D array has the same length": "mis:two_dimensional_array->RaggedRowsSameLength",
  "so it visits three columns in every row and adds all six numbers": "mis:two_dimensional_array->RaggedRowsSameLength"
 },
 "unexplained_clauses": [],
 "stop_reason": "max depth",
 "depth_reached": 4,
 "llm_calls": 0,
 "llm_cache_hits": 47,
 "llm_calls_by_step": {
  "prune": 16,
  "label": 31
 }
}
```
