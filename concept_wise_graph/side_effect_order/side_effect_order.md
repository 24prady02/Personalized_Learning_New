# side_effect_order (`side_effect_order`)

i = i++ and other expressions with side effects

Section 1.3 Conditionals and Loops, topic 1.3.d For loops (including i++ and scope). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around side_effect_order](side_effect_order.png)

## Concepts associated with side\_effect\_order (5)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **compound\_assignment** | x += e, x -= e, ... include a hidden cast | same topic (topic1.3.d) |
| **for\_loop** | a while with init/condition/update packaged together | same topic (topic1.3.d) |
| **increment\_operators** | ++ / -- (and +=) | prerequisite of it (it needs this)<br>composition rule (R) with it<br>shares misconception PostIncrementAssignsLater<br>shares misconception PrePostIncrementSameValue<br>same topic (topic1.3.d) |
| **loop\_scope** | lifetime/scope of variables in/around the loop | same topic (topic1.3.d) |
| **loop\_variable** | the counter that drives the loop | same topic (topic1.3.d) |

## Every edge in this view and its full label (16)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **increment\_operators** | prerequisite | **side\_effect\_order** | The result depends on the value an increment expression evaluates to.<br>grounding: book\_passage<br>composition rule (R) of increment\_operators with side\_effect\_order: Inside a larger expression the result depends on which value (old or new) the increment yields and on left-to-right evaluation, e.g. j += j++ in Exercise 1.3.6.<br>composition rule (R) of side\_effect\_order with increment\_operators: The result of an expression with a side effect depends on the value the increment expression evaluates to: old for i++, new for ++i. |
| **increment\_operators** | misconception | **PostIncrementAssignsLater** | **wrong rule:** i = i++ increases i by 1.<br>**right rule:** i++ evaluates to the old value, so i = i++ stores the old value back.<br>role: context |
| **increment\_operators** | misconception | **PrePostIncrementSameValue** | **wrong rule:** x = i++ and x = ++i store the same value in x.<br>**right rule:** Both increment i, but ++i has the value after the increment and i++ the value before.<br>role: primary |
| **side\_effect\_order** | misconception | **PostIncrementAssignsLater** | **wrong rule:** i = i++ increases i by 1.<br>**right rule:** i++ evaluates to the old value, so i = i++ stores the old value back.<br>role: primary |
| **side\_effect\_order** | misconception | **PrePostIncrementSameValue** | **wrong rule:** x = i++ and x = ++i store the same value in x.<br>**right rule:** Both increment i, but ++i has the value after the increment and i++ the value before.<br>role: context |
| **side\_effect\_order** | has\_level | **side\_effect\_order@L0** | side effect order -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).<br>**[0] everyday\_reading** (E): Folk meaning: in maths an expression has no effects, so i = i++ and x = ++i look like statements about equal quantities. In Java ++ changes i as soon as it is evaluated, and the expression's value (old or new) is then used by the rest of the expression.<br>**[1] misconception** (M) &rarr; PostIncrementAssignsLater: wrong rule: i = i++ increases i by 1. Right rule: i++ evaluates to the old value, so i = i++ stores the old value back.<br>**[2] inconsistent\_trace** (T) &rarr; PostIncrementAssignsLater: Applies left-to-right evaluation (LT) unevenly: lets an increment happen 'at the end of the statement' in one place but immediately in another. (here mixing in: "i = i++ increases i by 1")<br>**[3] misconception** (M) &rarr; PrePostIncrementSameValue: wrong rule: x = i++ and x = ++i store the same value in x. Right rule: Both increment i, but ++i has the value after the increment and i++ the value before. |
| **side\_effect\_order** | has\_level | **side\_effect\_order@L1** | side effect order -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): A side effect is a change to a variable's value made while evaluating an expression, e.g. by ++, -- or an assignment used inside a larger expression.<br>**[1] states\_the\_rule** (S): Java evaluates the left operand of a binary operator fully before the right, and all operands (except &amp;&amp;, \|\|, ?:) before the operation; ++i yields the new value and i++ the old one. |
| **side\_effect\_order** | has\_level | **side\_effect\_order@L2** | side effect order -&gt; L2 (Multistructural): the answer applies the rules of side effect order to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Evaluate operands left to right, applying each side effect at the moment its operand is evaluated; then apply the operator; for an assignment, the right side's value is stored last.<br>**[1] output\_prediction** (OP): With i = 5: i = i++ leaves 5 (old value stored back after the increment); x = i++ + i gives 5 + 6 = 11; j += j++ with j = 1 gives 2.<br>**[2] one\_step\_execution** (OS): One evaluation of i++ changes i by 1 and returns the old value; a later assignment in the same statement can overwrite that change. |
| **side\_effect\_order** | has\_level | **side\_effect\_order@L3** | side effect order -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): The result of an expression with a side effect depends on the value the increment expression evaluates to: old for i++, new for ++i.<br>**[1] purpose\_of\_the\_whole** (P): Plan: avoid it - write each change as its own statement (x = i; i++;) so the order of effects is visible; the book avoids statements like x = ++i. |
| **side\_effect\_order** | has\_level | **side\_effect\_order@L4** | side effect order -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C) &rarr; PostIncrementAssignsLater: Splitting x = i++; into x = i; i++; preserves behaviour; splitting it into i++; x = i; changes x by 1. Reordering the operands of an expression that contains a side effect can change the result.<br>**[1] transfer\_to\_a\_new\_program** (X): Rely on side-effect order only when reading other people's code; in your own code keep at most one side effect per statement and never read and modify the same variable in one expression.<br>**[2] diagnose\_an\_error** (D): rule broken: i++ yields the old value; assigning it back undoes the increment. Kind: silent logic error. Trigger class: i = i++ (or j = j++) used as an update: the variable never changes.<br>**[3] diagnose\_an\_error** (D): rule broken: Pre- and post-increment yield different values. Kind: silent logic error. Trigger class: Using x = ++i where x = i++ was meant (or vice versa): x is off by one. |
| **topic1.3.d** | contains | **compound\_assignment** | topic topic1.3.d contains compound\_assignment |
| **topic1.3.d** | contains | **for\_loop** | topic topic1.3.d contains for\_loop |
| **topic1.3.d** | contains | **increment\_operators** | topic topic1.3.d contains increment\_operators |
| **topic1.3.d** | contains | **loop\_scope** | topic topic1.3.d contains loop\_scope |
| **topic1.3.d** | contains | **loop\_variable** | topic topic1.3.d contains loop\_variable |
| **topic1.3.d** | contains | **side\_effect\_order** | topic topic1.3.d contains side\_effect\_order |
