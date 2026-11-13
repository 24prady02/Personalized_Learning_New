# primitive_vs_reference (`primitive_vs_reference`)

a primitive variable holds its value; an array (or String) variable holds a reference to the object stored elsewhere

Section 1.4 Arrays, topic 1.4.b Memory representation and bounds checking. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around primitive_vs_reference](primitive_vs_reference.png)

## Concepts associated with primitive\_vs\_reference (11)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **array\_aliasing** | two variables can refer to the same array | same topic (topic1.4.b) |
| **array\_bounds** | valid indices are 0 .. length-1; otherwise throws | same topic (topic1.4.b) |
| **array\_copy** | making a second, independent array with the same elements: create a new array and copy element by element (or Arrays.copyOf) | same topic (topic1.4.b) |
| **array\_reference** | the array variable stores the memory address (pointer) of the array; a[i] is found by adding i to that address | prerequisite of it (it needs this)<br>composition rule (R) with it<br>same topic (topic1.4.b) |
| **comparison\_operators** | == != &lt; &gt; &lt;= &gt;= | shares misconception EqualityOperatorComparesObjectsValues |
| **loop\_guard** | putting the bounds check in the loop condition so the body never makes an out-of-bounds array access | same topic (topic1.4.b) |
| **primitive\_type** | int, double, boolean, char | prerequisite of it (it needs this)<br>composition rule (R) with it<br>shares misconception StringIsPrimitive |
| **printing\_array\_reference** | printing an array variable prints a reference, not the elements | same topic (topic1.4.b) |
| **program\_state** | the information needed to know what a program will do next: the values of its variables and array entries and the next statement | same topic (topic1.4.b) |
| **string\_type** | String -- a reference type, not a primitive | shares misconception StringIsPrimitive<br>shares misconception EqualityOperatorComparesObjectsValues |
| **variable** | a named, typed box that holds a value | shares misconception VariablesHoldObjects |

## Every edge in this view and its full label (23)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **array\_reference** | prerequisite | **primitive\_vs\_reference** | An array variable stores the memory address of the array, not its elements.<br>grounding: book\_passage<br>composition rule (R) of primitive\_vs\_reference with array\_reference: An array variable is the standard example of a reference: its value is the memory address of the array. |
| **primitive\_type** | prerequisite | **primitive\_vs\_reference** | A variable of a primitive type stores the value itself in its own memory.<br>grounding: book\_passage<br>composition rule (R) of primitive\_vs\_reference with primitive\_type: The eight primitive types are the ones whose variables hold the value itself. |
| **comparison\_operators** | misconception | **EqualityOperatorComparesObjectsValues** | **wrong rule:** s == t is true whenever the two Strings contain the same text.<br>**right rule:** s == t is true only when s and t refer to the same object; s.equals(t) compares the text.<br>role: primary |
| **primitive\_type** | misconception | **StringIsPrimitive** | **wrong rule:** String is a primitive type like int.<br>**right rule:** String is not a primitive type; it is a class whose values are objects, although Java gives it some built-in support (literals, +).<br>role: primary |
| **primitive\_vs\_reference** | misconception | **EqualityOperatorComparesObjectsValues** | **wrong rule:** == compares contents (the String == bug)<br>**right rule:** s == t is true only when s and t refer to the same object; s.equals(t) compares the text.<br>role: context |
| **primitive\_vs\_reference** | misconception | **StringIsPrimitive** | **wrong rule:** String is a primitive type like int.<br>**right rule:** String is not a primitive type; it is a class whose values are objects, although Java gives it some built-in support (literals, +).<br>role: context |
| **primitive\_vs\_reference** | misconception | **VariablesHoldObjects** | **wrong rule:** a reference variable holds the whole object, not a reference<br>**right rule:** A reference variable holds only a reference to the object, which is stored separately.<br>role: context |
| **string\_type** | misconception | **EqualityOperatorComparesObjectsValues** | **wrong rule:** s == t is true whenever the two Strings contain the same text.<br>**right rule:** s == t is true only when s and t refer to the same object; s.equals(t) compares the text.<br>role: context |
| **string\_type** | misconception | **StringIsPrimitive** | **wrong rule:** String is a primitive type like int.<br>**right rule:** String is not a primitive type; it is a class whose values are objects, although Java gives it some built-in support (literals, +).<br>role: context |
| **variable** | misconception | **VariablesHoldObjects** | **wrong rule:** A String or array variable contains the whole object inside it.<br>**right rule:** A reference variable holds only a reference to the object, which is stored separately.<br>role: primary |
| **primitive\_vs\_reference** | has\_level | **primitive\_vs\_reference@L0** | primitive vs reference -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).<br>**[0] everyday\_reading** (E): Everyday thinking pictures a variable as a box that holds the thing itself. That is true for int, double, char and boolean; an array variable holds only the address of the array, which is stored elsewhere.<br>**[1] misconception** (M) &rarr; VariablesHoldObjects: wrong rule: A reference variable holds the whole object, not a reference. Right rule: An array variable stores a reference (the memory address) to the array, not the elements.<br>**[2] inconsistent\_trace** (T) &rarr; VariablesHoldObjects: Applies the model unevenly: treats int x = y as copying a value (correct) but also treats b = a for arrays as copying all the elements. (here mixing in: "a reference variable holds the whole object, not a reference")<br>**[3] misconception** (M) &rarr; StringIsPrimitive: wrong rule: String is a primitive type like int. Right rule: Java has eight primitive types; String is not one of them, and a String variable holds a reference. |
| **primitive\_vs\_reference** | has\_level | **primitive\_vs\_reference@L1** | primitive vs reference -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Primitive versus reference variable: the first holds its value, the second holds the address of an object.<br>**[1] states\_the\_rule** (S): When you declare a variable of a primitive type, Java reserves memory that stores its value. An array variable stores a reference to the array: Java treats the array name as a variable whose value is the memory address of the array. |
| **primitive\_vs\_reference** | has\_level | **primitive\_vs\_reference@L2** | primitive vs reference -&gt; L2 (Multistructural): the answer applies the rules of primitive vs reference to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Sequencing: x = y copies the value of y into x; b = a copies the address in a into b. In both cases the right side is evaluated first and its value stored, but the value of an array variable is an address.<br>**[1] output\_prediction** (OP): Result: after int y = x; y++, x is unchanged; after int[] b = a; b[0]++, a[0] has changed too, because a and b refer to the same array.<br>**[2] one\_step\_execution** (OS): State transition: assigning to a primitive variable changes only that variable; assigning to an element through a reference changes the array that every reference to it sees. |
| **primitive\_vs\_reference** | has\_level | **primitive\_vs\_reference@L3** | primitive vs reference -&gt; L3 (Relational): the answer relates the parts (3 ways).<br>**[0] relation\_to\_neighbour** (R): The eight primitive types are the ones whose variables hold the value itself.<br>**[1] relation\_to\_neighbour** (R): An array variable is the standard example of a reference: its value is the memory address of the array.<br>**[2] purpose\_of\_the\_whole** (P): Plan: the model predicts when an assignment shares data (arrays, Strings) and when it copies it (primitives), which decides when a copy is needed. |
| **primitive\_vs\_reference** | has\_level | **primitive\_vs\_reference@L4** | primitive vs reference -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).<br>**[0] predict\_a\_change** (C) &rarr; VariablesHoldObjects: Conservation: changing a primitive copy never affects the original; changing an array through any reference affects every alias.<br>**[1] transfer\_to\_a\_new\_program** (X): Draw a memory diagram (value in a box for primitives, an arrow to the array for references) whenever code assigns or compares arrays.<br>**[2] diagnose\_an\_error** (D): rule broken: == on references compares addresses. Kind: silent logic error. Trigger class: two arrays with the same elements are compared with == and found unequal (or two Strings with the same text) |
| **topic1.4.b** | contains | **array\_aliasing** | topic topic1.4.b contains array\_aliasing |
| **topic1.4.b** | contains | **array\_bounds** | topic topic1.4.b contains array\_bounds |
| **topic1.4.b** | contains | **array\_copy** | topic topic1.4.b contains array\_copy |
| **topic1.4.b** | contains | **array\_reference** | topic topic1.4.b contains array\_reference |
| **topic1.4.b** | contains | **loop\_guard** | topic topic1.4.b contains loop\_guard |
| **topic1.4.b** | contains | **primitive\_vs\_reference** | topic topic1.4.b contains primitive\_vs\_reference |
| **topic1.4.b** | contains | **printing\_array\_reference** | topic topic1.4.b contains printing\_array\_reference |
| **topic1.4.b** | contains | **program\_state** | topic topic1.4.b contains program\_state |
