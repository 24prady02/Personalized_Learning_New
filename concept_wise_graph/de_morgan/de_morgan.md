# de_morgan (`de_morgan`)

!(a &amp;&amp; b) == !a \|\| !b and !(a \|\| b) == !a &amp;&amp; !b

Section 1.2 Built-in Types of Data, topic 1.2.e Booleans. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around de_morgan](de_morgan.png)

## Concepts associated with de\_morgan (5)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **boolean** | true/false primitive | same topic (topic1.2.e) |
| **boolean\_expression** | an expression that evaluates to true/false | same topic (topic1.2.e) |
| **exclusive\_or** | ^ on booleans is true when the operands differ | same topic (topic1.2.e) |
| **logical\_operators** | &amp;&amp; \|\| ! | prerequisite of it (it needs this)<br>composition rule (R) with it<br>same topic (topic1.2.e) |
| **short\_circuit** | &amp;&amp;/\|\| stop evaluating once the result is known | same topic (topic1.2.e) |

## Every edge in this view and its full label (13)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **logical\_operators** | prerequisite | **de\_morgan** | De Morgan's laws rewrite expressions built from &amp;&amp; , \|\| and !.<br>grounding: book\_passage<br>composition rule (R) of logical\_operators with de\_morgan: De Morgan's laws rewrite negated &amp;&amp; / \|\| expressions: !(A &amp;&amp; B) is !A \|\| !B and !(A \|\| B) is !A &amp;&amp; !B.<br>composition rule (R) of de\_morgan with logical\_operators: De Morgan's laws relate the three logical operators: a negated &amp;&amp; becomes an \|\| of negations and a negated \|\| becomes an &amp;&amp; of negations. |
| **de\_morgan** | misconception | **NegationDistributesUnchanged** | **wrong rule:** !(a &amp;&amp; b) is the same as !a &amp;&amp; !b.<br>**right rule:** !(a &amp;&amp; b) is !a \|\| !b (De Morgan).<br>role: primary |
| **de\_morgan** | has\_level | **de\_morgan@L0** | de morgan -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): Folk meaning: 'not (A and B)' is read as 'not A and not B', the way a minus sign is distributed over a sum in algebra without changing the operator. Java (Boolean logic) rule: negating a compound condition negates each term and also flips &amp;&amp; to \|\| (and \|\| to &amp;&amp;).<br>**[1] misconception** (M) &rarr; NegationDistributesUnchanged: wrong rule: !(a &amp;&amp; b) is the same as !a &amp;&amp; !b. Right rule: !(a &amp;&amp; b) is !a \|\| !b, and !(a \|\| b) is !a &amp;&amp; !b (De Morgan); !a &amp;&amp; !b differs whenever exactly one of a, b is true.<br>**[2] inconsistent\_trace** (T) &rarr; NegationDistributesUnchanged: Points to LT (push ! into every term, replace each relation by its opposite, and swap &amp;&amp; and \|\|, all together). Applied unevenly: the student negates the terms but keeps the operator, or turns !(x &lt; 5) into x &gt; 5 instead of x &gt;= 5 in one term while handling the other correctly. (here mixing in: "!(a &amp;&amp; b) is the same as !a &amp;&amp; !b") |
| **de\_morgan** | has\_level | **de\_morgan@L1** | de morgan -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): De Morgan's laws are rules of Boolean logic that show how to negate a logical expression.<br>**[1] states\_the\_rule** (S): !(A &amp;&amp; B) is equivalent to !A \|\| !B, and !(A \|\| B) is equivalent to !A &amp;&amp; !B; with comparisons, negating a term uses the opposite relational operator (!(x &lt; 5) is x &gt;= 5). |
| **de\_morgan** | has\_level | **de\_morgan@L2** | de morgan -&gt; L2 (Multistructural): the answer applies the rules of de morgan to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): As a rewrite: move the ! inside the parentheses, negate each term (flipping each comparison), swap &amp;&amp; and \|\|; as evaluation, both forms give the same value on every row of the truth table and short-circuit after the same left operand.<br>**[1] output\_prediction** (OP): The rewritten expression has the same boolean value as the original for all inputs: with x = 1 and y = 0, !(x == 0 \|\| y == 0) and x != 0 &amp;&amp; y != 0 are both false.<br>**[2] one\_step\_execution** (OS): Rewriting changes no program state; both forms evaluate the same terms in the same left-to-right order, so side effects and short-circuit points are unchanged. |
| **de\_morgan** | has\_level | **de\_morgan@L3** | de morgan -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): De Morgan's laws relate the three logical operators: a negated &amp;&amp; becomes an \|\| of negations and a negated \|\| becomes an &amp;&amp; of negations.<br>**[1] purpose\_of\_the\_whole** (P): Used to simplify negated conditions into readable positive ones, e.g. turning a stopping condition ('found or at the end') into a loop-continuation condition while (!found &amp;&amp; i &lt; n), or simplifying (!(a &lt; b) &amp;&amp; !(a &gt; b)) to a == b. |
| **de\_morgan** | has\_level | **de\_morgan@L4** | de morgan -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).<br>**[0] predict\_a\_change** (C) &rarr; NegationDistributesUnchanged: A correct De Morgan rewrite preserves the value for every input (invariant); dropping the operator flip, or using &gt; instead of &gt;= for !(x &lt; 5), breaks it exactly on mixed or boundary inputs.<br>**[1] transfer\_to\_a\_new\_program** (X): Apply De Morgan when a condition is written as !(...) of a compound, or when converting a 'stop when' condition into a 'continue while' condition; leave a condition alone when its positive form is already clear.<br>**[2] diagnose\_an\_error** (D): rule broken: Negation flips &amp;&amp; and \|\| (De Morgan). Kind: silent logic error. Trigger class: Inputs where exactly one term is true (and boundary values of negated comparisons) after a condition was negated term by term without flipping the operator. |
| **topic1.2.e** | contains | **boolean** | topic topic1.2.e contains boolean |
| **topic1.2.e** | contains | **boolean\_expression** | topic topic1.2.e contains boolean\_expression |
| **topic1.2.e** | contains | **de\_morgan** | topic topic1.2.e contains de\_morgan |
| **topic1.2.e** | contains | **exclusive\_or** | topic topic1.2.e contains exclusive\_or |
| **topic1.2.e** | contains | **logical\_operators** | topic topic1.2.e contains logical\_operators |
| **topic1.2.e** | contains | **short\_circuit** | topic topic1.2.e contains short\_circuit |
