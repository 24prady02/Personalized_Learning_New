# de_morgan (`de_morgan`)

!(a &amp;&amp; b) == !a \|\| !b and !(a \|\| b) == !a &amp;&amp; !b

Section 1.2 Built-in Types of Data, topic 1.2.e Booleans.

![The knowledge graph around de_morgan](de_morgan.png)

## At a glance

- **Needs first:** `logical_operators`
- **Leads to:** nothing
- **Learned alongside:** nothing
- **Misconceptions:** `NegationDistributesUnchanged`
- **Errors:** none
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 13 edges around this concept, each explained in the graph's own words.

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `de_morgan`.

### `logical_operators` comes before `de_morgan`

*&amp;&amp; \|\| !*

De Morgan's laws rewrite expressions built from &amp;&amp; , \|\| and !.

- **Grounding:** book passage
- **How `de_morgan` combines with `logical_operators`:** De Morgan's laws relate the three logical operators: a negated &amp;&amp; becomes an \|\| of negations and a negated \|\| becomes an &amp;&amp; of negations.
- **How `logical_operators` combines with `de_morgan`:** De Morgan's laws rewrite negated &amp;&amp; / \|\| expressions: !(A &amp;&amp; B) is !A \|\| !B and !(A \|\| B) is !A &amp;&amp; !B.

## What it leads to (0)

These concepts need `de_morgan` first.

No concept has this one as a prerequisite.

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (1)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### NegationDistributesUnchanged

- **Wrong rule:** !(a &amp;&amp; b) is the same as !a &amp;&amp; !b.
- **Right rule:** !(a &amp;&amp; b) is !a \|\| !b (De Morgan).
- **Role of this concept:** primary
- **Shows at level L0 as:** misconception: wrong rule: !(a &amp;&amp; b) is the same as !a &amp;&amp; !b. Right rule: !(a &amp;&amp; b) is !a \|\| !b, and !(a \|\| b) is !a &amp;&amp; !b (De Morgan); !a &amp;&amp; !b differs whenever exactly one of a, b is true.
- **Shows at level L0 as:** inconsistent trace: Points to LT (push ! into every term, replace each relation by its opposite, and swap &amp;&amp; and \|\|, all together). Applied unevenly: the student negates the terms but keeps the operator, or turns !(x &lt; 5) into x &gt; 5 instead of x &gt;= 5 in one term while handling the other correctly. (here mixing in: "!(a &amp;&amp; b) is the same as !a &amp;&amp; !b")

## Errors (0)

An error edge states the rule that gets broken in a program, and the right rule.

The graph has no error edge from this concept.

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for de morgan: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to de morgan agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

de morgan -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).

- **everyday reading** (folk-meaning rule): Folk meaning: 'not (A and B)' is read as 'not A and not B', the way a minus sign is distributed over a sum in algebra without changing the operator. Java (Boolean logic) rule: negating a compound condition negates each term and also flips &amp;&amp; to \|\| (and \|\| to &amp;&amp;).
- **misconception** (wrong rule / right rule; shows `NegationDistributesUnchanged`): wrong rule: !(a &amp;&amp; b) is the same as !a &amp;&amp; !b. Right rule: !(a &amp;&amp; b) is !a \|\| !b, and !(a \|\| b) is !a &amp;&amp; !b (De Morgan); !a &amp;&amp; !b differs whenever exactly one of a, b is true.
- **inconsistent trace** (uneven-application rule; shows `NegationDistributesUnchanged`): Points to LT (push ! into every term, replace each relation by its opposite, and swap &amp;&amp; and \|\|, all together). Applied unevenly: the student negates the terms but keeps the operator, or turns !(x &lt; 5) into x &gt; 5 instead of x &gt;= 5 in one term while handling the other correctly. (here mixing in: "!(a &amp;&amp; b) is the same as !a &amp;&amp; !b")

### L1: Unistructural / atom x text surface

L1 for de morgan: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

de morgan -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

- **names the element** (identity rule): De Morgan's laws are rules of Boolean logic that show how to negate a logical expression.
- **states the rule** (declarative rule): !(A &amp;&amp; B) is equivalent to !A \|\| !B, and !(A \|\| B) is equivalent to !A &amp;&amp; !B; with comparisons, negating a term uses the opposite relational operator (!(x &lt; 5) is x &gt;= 5).

### L2: Multistructural / block x execution / preoperational

L2 for de morgan: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

de morgan -&gt; L2 (Multistructural): the answer applies the rules of de morgan to every part of the code, in order (3 ways).

- **line by line trace** (operational sequencing rule): As a rewrite: move the ! inside the parentheses, negate each term (flipping each comparison), swap &amp;&amp; and \|\|; as evaluation, both forms give the same value on every row of the truth table and short-circuit after the same left operand.
- **output prediction** (evaluation / result rule): The rewritten expression has the same boolean value as the original for all inputs: with x = 1 and y = 0, !(x == 0 \|\| y == 0) and x != 0 &amp;&amp; y != 0 are both false.
- **one step execution** (state-transition rule): Rewriting changes no program state; both forms evaluate the same terms in the same left-to-right order, so side effects and short-circuit points are unchanged.

### L3: Relational / relations x function (concrete operational begins)

L3 for de morgan: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

de morgan -&gt; L3 (Relational): the answer relates the parts (2 ways).

- **relation to neighbour** (composition rule (with a neighbour)): De Morgan's laws relate the three logical operators: a negated &amp;&amp; becomes an \|\| of negations and a negated \|\| becomes an &amp;&amp; of negations.
- **purpose of the whole** (plan / role rule): Used to simplify negated conditions into readable positive ones, e.g. turning a stopping condition ('found or at the end') into a loop-continuation condition while (!found &amp;&amp; i &lt; n), or simplifying (!(a &lt; b) &amp;&amp; !(a &gt; b)) to a == b.

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for de morgan: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

de morgan -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).

- **predict a change** (conservation rule; shows `NegationDistributesUnchanged`): A correct De Morgan rewrite preserves the value for every input (invariant); dropping the operator flip, or using &gt; instead of &gt;= for !(x &lt; 5), breaks it exactly on mixed or boundary inputs.
- **transfer to a new program** (applicability rule): Apply De Morgan when a condition is written as !(...) of a compound, or when converting a 'stop when' condition into a 'continue while' condition; leave a condition alone when its positive form is already clear.
- **diagnose an error** (error rule): rule broken: Negation flips &amp;&amp; and \|\| (De Morgan). Kind: silent logic error. Trigger class: Inputs where exactly one term is true (and boundary values of negated comparisons) after a condition was negated term by term without flipping the operator.

## Same topic

`de_morgan` belongs to the topic **Booleans** (`topic1.2.e`). The topic also contains: `boolean`, `boolean_expression`, `exclusive_or`, `logical_operators`, `short_circuit`.

## Rules of the concept (13)

- **folk-meaning rule:** Folk meaning: 'not (A and B)' is read as 'not A and not B', the way a minus sign is distributed over a sum in algebra without changing the operator. Java (Boolean logic) rule: negating a compound condition negates each term and also flips &amp;&amp; to \|\| (and \|\| to &amp;&amp;).
- **wrong rule / right rule:** NegationDistributesUnchanged: wrong: !(a &amp;&amp; b) is the same as !a &amp;&amp; !b. \| right: !(a &amp;&amp; b) is !a \|\| !b, and !(a \|\| b) is !a &amp;&amp; !b (De Morgan); !a &amp;&amp; !b differs whenever exactly one of a, b is true.
- **uneven-application rule:** Points to LT (push ! into every term, replace each relation by its opposite, and swap &amp;&amp; and \|\|, all together). Applied unevenly: the student negates the terms but keeps the operator, or turns !(x &lt; 5) into x &gt; 5 instead of x &gt;= 5 in one term while handling the other correctly.
- **identity rule:** De Morgan's laws are rules of Boolean logic that show how to negate a logical expression.
- **declarative rule:** !(A &amp;&amp; B) is equivalent to !A \|\| !B, and !(A \|\| B) is equivalent to !A &amp;&amp; !B; with comparisons, negating a term uses the opposite relational operator (!(x &lt; 5) is x &gt;= 5).
- **operational sequencing rule:** As a rewrite: move the ! inside the parentheses, negate each term (flipping each comparison), swap &amp;&amp; and \|\|; as evaluation, both forms give the same value on every row of the truth table and short-circuit after the same left operand.
- **evaluation / result rule:** The rewritten expression has the same boolean value as the original for all inputs: with x = 1 and y = 0, !(x == 0 \|\| y == 0) and x != 0 &amp;&amp; y != 0 are both false.
- **state-transition rule:** Rewriting changes no program state; both forms evaluate the same terms in the same left-to-right order, so side effects and short-circuit points are unchanged.
- **composition rule (with a neighbour):** with logical\_operators: De Morgan's laws relate the three logical operators: a negated &amp;&amp; becomes an \|\| of negations and a negated \|\| becomes an &amp;&amp; of negations.
- **plan / role rule:** Used to simplify negated conditions into readable positive ones, e.g. turning a stopping condition ('found or at the end') into a loop-continuation condition while (!found &amp;&amp; i &lt; n), or simplifying (!(a &lt; b) &amp;&amp; !(a &gt; b)) to a == b.
- **conservation rule:** A correct De Morgan rewrite preserves the value for every input (invariant); dropping the operator flip, or using &gt; instead of &gt;= for !(x &lt; 5), breaks it exactly on mixed or boundary inputs.
- **error rule:** rule broken: Negation flips &amp;&amp; and \|\| (De Morgan). (silent logic error)
- **applicability rule:** Apply De Morgan when a condition is written as !(...) of a compound, or when converting a 'stop when' condition into a 'continue while' condition; leave a condition alone when its positive form is already clear.

## The whole prerequisite chain

- **Everything it builds on (4):** `boolean`, `data_type`, `logical_operators`, `primitive_type`
- **Everything that builds on it (0):** nothing
