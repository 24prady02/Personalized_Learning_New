# Application programming interface (API) (`api`)

a table of library methods giving each method's signature and a short description of what it computes

Section 1.2 1.2 Built-in Types of Data, topic 1.2.g Library methods and APIs (Math). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around api](api.png)

## Concepts associated with api (7)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **math\_library** | Math.abs, Math.sqrt, Math.max, Math.random, Math.round ... | same topic (topic1.2.g) |
| **math\_random** | Math.random() and scaling to an int range | same topic (topic1.2.g) |
| **math\_round** | Math.round rounds to the nearest integer and returns a long | same topic (topic1.2.g) |
| **method\_call** | name(arguments) -- invokes a library method and uses its return value | prerequisite of it (it needs this)<br>composition rule (R) with it<br>same topic (topic1.2.g) |
| **standard\_audio** | StdAudio: sound as an array of samples | builds on it (needs it) |
| **standard\_drawing** | StdDraw -- graphical output (book-specific) | builds on it (needs it) |
| **trig\_functions** | Math.sin, Math.cos, Math.atan2 work in radians | same topic (topic1.2.g) |

## Every edge in this view and its full label (14)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **api** | prerequisite | **standard\_audio** | StdAudio is a library used through its API of static methods.<br>grounding: book\_passage |
| **api** | prerequisite | **standard\_drawing** | StdDraw is a library used through its API of static methods.<br>grounding: book\_passage |
| **method\_call** | prerequisite | **api** | An API lists, for each library method, the signature you need in order to call it: name, argument types and return type.<br>grounding: book\_passage<br>composition rule (R) of method\_call with api: The call must match a signature in the API (name, number, order and types of arguments), and the API's return type tells how the value can be used.<br>composition rule (R) of api with method\_call: Each call must match one API signature: same name, arguments of the listed types in the listed order, and use of the value consistent with the return type. |
| **api** | has\_level | **api@L0** | Application programming interface (API) -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).<br>**[0] everyday\_reading** (E): Folk meaning: an 'interface' is a screen you click on, and documentation shows the code you type. SW rule: an API is a table of library methods, each line giving the method's signature (return type, name, argument types) and what it computes; the signature is not the code you type to call it. |
| **api** | has\_level | **api@L1** | Application programming interface (API) -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): An API (application programming interface) is a table of library methods giving, for each, its signature and a short description of what it computes.<br>**[1] states\_the\_rule** (S): Each API line specifies the return type, the method name and the types of its arguments (the signature), plus a description; it provides the information needed to write a program that uses the method. |
| **api** | has\_level | **api@L2** | Application programming interface (API) -&gt; L2 (Multistructural): the answer applies the rules of Application programming interface (API) to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): To use an entry: find the method, read its signature left to right (return type, name, parameter types in order), write a call with the name and argument expressions of those types in that order, and use the returned value according to the return type (none for void).<br>**[1] output\_prediction** (OP): From the API alone one predicts the type of a call's value: Math.sqrt returns a double, Math.round a long, Integer.parseInt an int, println nothing (void).<br>**[2] one\_step\_execution** (OS): Reading the API changes nothing in the program; it states what each call returns, and (for void methods such as println) what effect the call has instead of a value. |
| **api** | has\_level | **api@L3** | Application programming interface (API) -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): Each call must match one API signature: same name, arguments of the listed types in the listed order, and use of the value consistent with the return type.<br>**[1] purpose\_of\_the\_whole** (P): An API is a contract that separates the client, who needs only the signatures and descriptions, from the implementation; it lets programmers use large libraries without reading their code, and later to design their own libraries. |
| **api** | has\_level | **api@L4** | Application programming interface (API) -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C): Client code keeps working when a method's implementation changes but its signature and behaviour stay the same; changing a signature (name, parameter types, return type) breaks every call that relies on it. Choosing which methods an API includes is a trade-off between convenience and size.<br>**[1] transfer\_to\_a\_new\_program** (X): Consult the API whenever you use a library method (to get name, argument order and return type right); if no listed method fits, combine listed ones (e.g. secant from Math.cos) or write your own.<br>**[2] diagnose\_an\_error** (D): rule broken: A call must match the API signature (argument types/number/order and return type). Kind: compile-time. Trigger class: Wrong argument types or count (Math.sqrt("2")), or a return value stored in an incompatible variable (int n = Math.round(x)).<br>**[3] diagnose\_an\_error** (D): rule broken: The API describes what the method returns; a value-returning call does not change its arguments. Kind: silent logic error. Trigger class: Using a non-void method as a statement and expecting its argument to change (Math.round(x);). |
| **topic1.2.g** | contains | **api** | topic topic1.2.g contains api |
| **topic1.2.g** | contains | **math\_library** | topic topic1.2.g contains math\_library |
| **topic1.2.g** | contains | **math\_random** | topic topic1.2.g contains math\_random |
| **topic1.2.g** | contains | **math\_round** | topic topic1.2.g contains math\_round |
| **topic1.2.g** | contains | **method\_call** | topic topic1.2.g contains method\_call |
| **topic1.2.g** | contains | **trig\_functions** | topic topic1.2.g contains trig\_functions |
