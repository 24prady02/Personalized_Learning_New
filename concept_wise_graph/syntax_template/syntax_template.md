# Template notation (`syntax_template`)

the book's notation for a construct: a name in angle brackets, such as &lt;boolean expression&gt;, stands for any instance of that construct

Section 1.3 1.3 Conditionals and Loops, topic 1.3.b If statements.

![The knowledge graph around syntax_template](syntax_template.png)

## At a glance

- **Needs first:** `boolean_expression`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** none
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 10 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (2)

- no misconception or error edge
- no aliases: a student's words cannot name this concept

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `syntax_template`.

### `boolean_expression` comes before `syntax_template`

*an expression that evaluates to true/false*

- **Edge:** `pre:boolean_expression->syntax_template`
- **Exact edge logic:** In the template if (&lt;boolean expression&gt;) { &lt;statements&gt; }, &lt;boolean expression&gt; stands for any expression of type boolean.
- **Grounding:** book\_passage
- **Composition rule (R) of `syntax_template` with `boolean_expression`:** The \`&lt;boolean expression&gt;\` slot accepts only expressions of type boolean (\`x &gt; y\`, \`found\`, \`a &amp;&amp; b\`). An int expression or an assignment such as \`x = y\` with int x is a compile error in that slot.
- **Composition rule (R) of `boolean_expression` with `syntax_template`:** In the template if (&lt;boolean expression&gt;) { &lt;statements&gt; } the placeholder may be filled by any boolean-typed expression: a literal, a boolean variable, a comparison or a combination with logical operators.

## What it leads to (0)

These concepts need `syntax_template` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (0)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

The graph has no misconception edge from this concept.

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for Template notation: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to Template notation agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `syntax_template` &rarr; `syntax_template@L0` (has_level)
- **Exact edge logic:** Template notation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).

Ways (1), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: angle brackets read as the less-than and greater-than signs, or as text to be typed. In a template, \`&lt;boolean expression&gt;\` is a placeholder that is replaced by any instance of that construct; only the other tokens (if, parentheses, braces) are typed literally.

### L1: Unistructural / atom x text surface

L1 for Template notation: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `syntax_template` &rarr; `syntax_template@L1` (has_level)
- **Exact edge logic:** Template notation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): Notation (metalanguage): a template is S&amp;W's pattern for the form of a Java construct. Fixed tokens are written literally, and a name in angle brackets stands for any instance of a previously defined construct.
- **[1] states\_the\_rule** (rule type S, declarative rule): In \`if (&lt;boolean expression&gt;) { &lt;statements&gt; }\`, \`if\`, \`(\`, \`)\`, \`{\`, \`}\` must appear as written. \`&lt;boolean expression&gt;\` may be any expression of type boolean, and \`&lt;statements&gt;\` any statement block. The braces are optional for a single statement. Syntax is the form a statement must have, checked by the compiler (syntax errors); semantics is what the statement means when it runs, which the compiler does not check.

### L2: Multistructural / block x execution / preoperational

L2 for Template notation: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `syntax_template` &rarr; `syntax_template@L2` (has_level)
- **Exact edge logic:** Template notation -&gt; L2 (Multistructural): the answer applies the rules of Template notation to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Reading order: match the template's fixed tokens left to right against the code, then for each placeholder check that the code in that position is an instance of the named construct, recursively (a boolean expression may itself contain sub-expressions).
- **[1] output\_prediction** (rule type OP, evaluation / result rule): Filling a template produces one concrete, legal Java construct. For example, if (&lt;boolean expression&gt;) &lt;statements&gt; becomes \`if (x &lt; 0) x = -x;\`.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): One substitution step replaces one placeholder with one instance of its construct and leaves the rest of the template unchanged.

### L3: Relational / relations x function (concrete operational begins)

L3 for Template notation: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `syntax_template` &rarr; `syntax_template@L3` (has_level)
- **Exact edge logic:** Template notation -&gt; L3 (Relational): the answer relates the parts (2 ways).

Ways (2), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The \`&lt;boolean expression&gt;\` slot accepts only expressions of type boolean (\`x &gt; y\`, \`found\`, \`a &amp;&amp; b\`). An int expression or an assignment such as \`x = y\` with int x is a compile error in that slot.
- **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: to describe compactly what every instance of a construct looks like (if, while, for, do-while), so that you can write new instances and check existing code against the form.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for Template notation: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `syntax_template` &rarr; `syntax_template@L4` (has_level)
- **Exact edge logic:** Template notation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).

Ways (5), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule): Changing what fills a placeholder (any other boolean expression) keeps the code legal. Changing or omitting a fixed token (dropping the parentheses, adding \`then\`) breaks it.
- **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use templates to learn or check the form of a new construct. They show syntax, not meaning (the meaning of while vs if is not in the template), and they leave out details such as optional braces, so read them together with the semantic rule.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Fixed tokens of the template must appear exactly. Kind: compile-time. Trigger class: Dropping the parentheses (\`if a &gt; b { c = 0; }\`) or adding a word (\`if (a &gt; b) then c = 0;\`).
- **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A placeholder must be filled by an instance of the named construct. Kind: compile-time. Trigger class: Putting an int expression in a \`&lt;boolean expression&gt;\` slot (\`if (x)\` with int x, \`if (t = goal)\`): incompatible types.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Angle brackets are notation, not code. Kind: compile-time. Trigger class: Typing the template text literally (\`if (&lt;boolean expression&gt;)\`).

## Same topic

`syntax_template` belongs to the topic **If statements** (`topic1.3.b`). The topic also contains: `empty_statement`, `if_else_statement`, `if_statement`.

## Rules of the concept (14)

- **Book** (SW-1e, p. 46 (pdf 56)): "This description introduces a formal notation known as a template"
- **E** (folk-meaning rule): Folk meaning: angle brackets read as the less-than and greater-than signs, or as text to be typed. In a template, \`&lt;boolean expression&gt;\` is a placeholder that is replaced by any instance of that construct; only the other tokens (if, parentheses, braces) are typed literally.
- **T** (uneven-application rule): Applies the substitution rule unevenly: some placeholders are filled with the right kind of construct and others with the wrong kind (a statement for an expression), or fixed tokens like the parentheses are dropped in some instances.
- **N** (identity rule): Notation (metalanguage): a template is S&amp;W's pattern for the form of a Java construct. Fixed tokens are written literally, and a name in angle brackets stands for any instance of a previously defined construct.
- **S** (declarative rule): In \`if (&lt;boolean expression&gt;) { &lt;statements&gt; }\`, \`if\`, \`(\`, \`)\`, \`{\`, \`}\` must appear as written. \`&lt;boolean expression&gt;\` may be any expression of type boolean, and \`&lt;statements&gt;\` any statement block. The braces are optional for a single statement. Syntax is the form a statement must have, checked by the compiler (syntax errors); semantics is what the statement means when it runs, which the compiler does not check.
- **LT** (operational sequencing rule): Reading order: match the template's fixed tokens left to right against the code, then for each placeholder check that the code in that position is an instance of the named construct, recursively (a boolean expression may itself contain sub-expressions).
- **OP** (evaluation / result rule): Filling a template produces one concrete, legal Java construct. For example, if (&lt;boolean expression&gt;) &lt;statements&gt; becomes \`if (x &lt; 0) x = -x;\`.
- **OS** (state-transition rule): One substitution step replaces one placeholder with one instance of its construct and leaves the rest of the template unchanged.
- **R** (composition rule (with a neighbour)): with boolean\_expression: The \`&lt;boolean expression&gt;\` slot accepts only expressions of type boolean (\`x &gt; y\`, \`found\`, \`a &amp;&amp; b\`). An int expression or an assignment such as \`x = y\` with int x is a compile error in that slot.
- **P** (plan / role rule): Purpose: to describe compactly what every instance of a construct looks like (if, while, for, do-while), so that you can write new instances and check existing code against the form.
- **C** (conservation rule): Changing what fills a placeholder (any other boolean expression) keeps the code legal. Changing or omitting a fixed token (dropping the parentheses, adding \`then\`) breaks it.
- **D** (error rule): rule broken: Fixed tokens of the template must appear exactly. (compile-time)
- **D** (error rule): rule broken: A placeholder must be filled by an instance of the named construct. (compile-time)
- **D** (error rule): rule broken: Angle brackets are notation, not code. (compile-time)
- **X** (applicability rule): Use templates to learn or check the form of a new construct. They show syntax, not meaning (the meaning of while vs if is not in the template), and they leave out details such as optional braces, so read them together with the semantic rule.

## How it is found in code and answers (reader block)

- **Aliases:** none
- **Code patterns:** `<\s*[a-z]+(?:[ \-][a-z]+)*\s*>`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (11):** `arithmetic_operators`, `boolean`, `boolean_expression`, `comparison_operators`, `data_type`, `expression`, `identifier`, `literal`, `logical_operators`, `primitive_type`, `variable`
- **Everything that builds on it (0):** nothing

## Every edge in this view and its exact edge logic (10)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `boolean_expression` &rarr; `syntax_template`** (prerequisite)

- **Exact edge logic:** In the template if (&lt;boolean expression&gt;) { &lt;statements&gt; }, &lt;boolean expression&gt; stands for any expression of type boolean.
- **Grounding:** book\_passage
- **Composition rule (R) of `boolean_expression` with `syntax_template`:** In the template if (&lt;boolean expression&gt;) { &lt;statements&gt; } the placeholder may be filled by any boolean-typed expression: a literal, a boolean variable, a comparison or a combination with logical operators.
- **Composition rule (R) of `syntax_template` with `boolean_expression`:** The \`&lt;boolean expression&gt;\` slot accepts only expressions of type boolean (\`x &gt; y\`, \`found\`, \`a &amp;&amp; b\`). An int expression or an assignment such as \`x = y\` with int x is a compile error in that slot.

**2. `syntax_template` &rarr; `syntax_template@L0`** (has_level)

- **Exact edge logic:** Template notation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: angle brackets read as the less-than and greater-than signs, or as text to be typed. In a template, \`&lt;boolean expression&gt;\` is a placeholder that is replaced by any instance of that construct; only the other tokens (if, parentheses, braces) are typed literally.

**3. `syntax_template` &rarr; `syntax_template@L1`** (has_level)

- **Exact edge logic:** Template notation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): Notation (metalanguage): a template is S&amp;W's pattern for the form of a Java construct. Fixed tokens are written literally, and a name in angle brackets stands for any instance of a previously defined construct.
  - **[1] states\_the\_rule** (rule type S, declarative rule): In \`if (&lt;boolean expression&gt;) { &lt;statements&gt; }\`, \`if\`, \`(\`, \`)\`, \`{\`, \`}\` must appear as written. \`&lt;boolean expression&gt;\` may be any expression of type boolean, and \`&lt;statements&gt;\` any statement block. The braces are optional for a single statement. Syntax is the form a statement must have, checked by the compiler (syntax errors); semantics is what the statement means when it runs, which the compiler does not check.

**4. `syntax_template` &rarr; `syntax_template@L2`** (has_level)

- **Exact edge logic:** Template notation -&gt; L2 (Multistructural): the answer applies the rules of Template notation to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Reading order: match the template's fixed tokens left to right against the code, then for each placeholder check that the code in that position is an instance of the named construct, recursively (a boolean expression may itself contain sub-expressions).
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): Filling a template produces one concrete, legal Java construct. For example, if (&lt;boolean expression&gt;) &lt;statements&gt; becomes \`if (x &lt; 0) x = -x;\`.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): One substitution step replaces one placeholder with one instance of its construct and leaves the rest of the template unchanged.

**5. `syntax_template` &rarr; `syntax_template@L3`** (has_level)

- **Exact edge logic:** Template notation -&gt; L3 (Relational): the answer relates the parts (2 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The \`&lt;boolean expression&gt;\` slot accepts only expressions of type boolean (\`x &gt; y\`, \`found\`, \`a &amp;&amp; b\`). An int expression or an assignment such as \`x = y\` with int x is a compile error in that slot.
  - **[1] purpose\_of\_the\_whole** (rule type P, plan / role rule): Purpose: to describe compactly what every instance of a construct looks like (if, while, for, do-while), so that you can write new instances and check existing code against the form.

**6. `syntax_template` &rarr; `syntax_template@L4`** (has_level)

- **Exact edge logic:** Template notation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule): Changing what fills a placeholder (any other boolean expression) keeps the code legal. Changing or omitting a fixed token (dropping the parentheses, adding \`then\`) breaks it.
  - **[1] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Use templates to learn or check the form of a new construct. They show syntax, not meaning (the meaning of while vs if is not in the template), and they leave out details such as optional braces, so read them together with the semantic rule.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: Fixed tokens of the template must appear exactly. Kind: compile-time. Trigger class: Dropping the parentheses (\`if a &gt; b { c = 0; }\`) or adding a word (\`if (a &gt; b) then c = 0;\`).
  - **[3] diagnose\_an\_error** (rule type D, error rule): rule broken: A placeholder must be filled by an instance of the named construct. Kind: compile-time. Trigger class: Putting an int expression in a \`&lt;boolean expression&gt;\` slot (\`if (x)\` with int x, \`if (t = goal)\`): incompatible types.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Angle brackets are notation, not code. Kind: compile-time. Trigger class: Typing the template text literally (\`if (&lt;boolean expression&gt;)\`).

**7. `topic1.3.b` &rarr; `syntax_template`** (contains)

- topic `topic1.3.b` contains `syntax_template`

**8. `topic1.3.b` &rarr; `empty_statement`** (contains)

- topic `topic1.3.b` contains `empty_statement`

**9. `topic1.3.b` &rarr; `if_else_statement`** (contains)

- topic `topic1.3.b` contains `if_else_statement`

**10. `topic1.3.b` &rarr; `if_statement`** (contains)

- topic `topic1.3.b` contains `if_statement`
