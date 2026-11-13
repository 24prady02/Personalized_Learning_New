# teleportation (`teleportation`)

the 90-10 rule: follow a link or jump to a random page

Section 1.6 Case Study: Random Web Surfer, topic 1.6.a Input format and transition matrix. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around teleportation](teleportation.png)

## Concepts associated with teleportation (4)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **dangling\_pages** | pages with no outgoing links | same topic (topic1.6.a) |
| **input\_graph** | read the page links from input | same topic (topic1.6.a) |
| **normalization** | scaling a row so its probabilities sum to 1 | same topic (topic1.6.a) |
| **transition\_matrix** | a 2-D array of move probabilities (rows sum to 1) | builds on it (needs it)<br>composition rule (R) with it<br>same topic (topic1.6.a) |

## Every edge in this view and its full label (12)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **teleportation** | prerequisite | **transition\_matrix** | The 90-10 rule says the surfer follows a random link 90 percent of the time and jumps to a random page 10 percent of the time, and each transition-matrix entry is computed from it.<br>grounding: questionable<br>composition rule (R) of teleportation with transition\_matrix: Every entry is built as link part plus leap part; the .90 and .10 weights must sum to 1 for each row to remain a distribution.<br>composition rule (R) of transition\_matrix with teleportation: The .10/N term, added to every entry, is the teleport (random-page) part of each row; the .90 factor scales the link part so the two parts sum to 1. |
| **teleportation** | misconception | **TeleportUnneeded** | **wrong rule:** Without teleporting, the surfer still visits every page.<br>**right rule:** Without the random leap the surfer can get stuck (e.g. in a spider trap with no outgoing links); the 90-10 rule guarantees mixing.<br>role: primary |
| **teleportation** | has\_level | **teleportation@L0** | teleportation -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): Everyday "90 percent of the time" reads as a quota (exactly 9 of every 10 moves follow links); in the model it is a probability applied independently on every move, folded into each matrix entry as .90\*(link share) + .10/N.<br>**[1] misconception** (M) &rarr; TeleportUnneeded: wrong rule: Without teleporting, the surfer still visits every page. Right rule: Without the random leap the surfer can get stuck (e.g. in a spider trap with no outgoing links); the 90-10 rule guarantees mixing.<br>**[2] inconsistent\_trace** (T) &rarr; TeleportUnneeded: Applies LT (add .10/N to every entry of every row, after the link term) unevenly: e.g. adds it only to entries that have links, or only to the diagonal, so rows sum to less than 1. (here mixing in: "Without teleporting, the surfer still visits every page") |
| **teleportation** | has\_level | **teleportation@L1** | teleportation -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): A model rule: the random leap of the 90-10 rule, a jump to a page chosen uniformly from all N pages with probability .10.<br>**[1] states\_the\_rule** (S): 90 percent of the time the surfer clicks a random link on the current page (each link equally likely) and 10 percent of the time goes directly to a random page (all pages equally likely); in the matrix this adds .10/N to each entry. |
| **teleportation** | has\_level | **teleportation@L2** | teleportation -&gt; L2 (Multistructural): the answer applies the rules of teleportation to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Per entry, the link term .90\*counts[i][j]/outDegree[i] is computed first and the leap term .10/N is then added to every entry, including entries with no link and the diagonal.<br>**[1] output\_prediction** (OP): The leap contributes .10/N to each entry: .02 for tiny.txt (N = 5), so an entry with no link is .02 and the single link of page 0 gives .92.<br>**[2] one\_step\_execution** (OS): Adding the leap term raises one entry p by .10/N; summed across a row it adds exactly .10. |
| **teleportation** | has\_level | **teleportation@L3** | teleportation -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): Every entry is built as link part plus leap part; the .90 and .10 weights must sum to 1 for each row to remain a distribution.<br>**[1] purpose\_of\_the\_whole** (P): Guarantee mixing: the leap makes every page reachable from every page, so the chain has a unique long-run distribution and spider traps cannot capture the surfer. |
| **teleportation** | has\_level | **teleportation@L4** | teleportation -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C) &rarr; TeleportUnneeded: Changing the split to 80-20 or 95-5 keeps rows stochastic and mixing but changes the ranks; removing the leap (100-0) can break mixing.<br>**[1] transfer\_to\_a\_new\_program** (X): Use whenever the link graph may not be strongly connected (any real web model) to make the chain mix; the particular 90-10 split is a guess, so it is a modelling parameter, not a fact.<br>**[2] diagnose\_an\_error** (D): rule broken: The leap is needed for mixing. Kind: silent logic error. Trigger class: Leap term removed and graph has a spider trap or unreachable part: ranks pile up in the trap and depend on the starting page.<br>**[3] diagnose\_an\_error** (D): rule broken: Leap and link weights must sum to 1. Kind: silent logic error. Trigger class: Leap changed (e.g. .20/N) without changing .90: rows sum to 1.1 and the random move misbehaves. |
| **topic1.6.a** | contains | **dangling\_pages** | topic topic1.6.a contains dangling\_pages |
| **topic1.6.a** | contains | **input\_graph** | topic topic1.6.a contains input\_graph |
| **topic1.6.a** | contains | **normalization** | topic topic1.6.a contains normalization |
| **topic1.6.a** | contains | **teleportation** | topic topic1.6.a contains teleportation |
| **topic1.6.a** | contains | **transition\_matrix** | topic topic1.6.a contains transition\_matrix |
