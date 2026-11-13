# array_copy (`array_copy`)

making a second, independent array with the same elements: create a new array and copy element by element (or Arrays.copyOf)

Section 1.4 Arrays, topic 1.4.b Memory representation and bounds checking. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around array_copy](array_copy.png)

## Concepts associated with array\_copy (9)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **array\_aliasing** | two variables can refer to the same array | parallel concept<br>composition rule (R) with it<br>shares misconception ArrayEqualityComparesValues<br>shares misconception AssignmentCopiesObject<br>same topic (topic1.4.b) |
| **array\_bounds** | valid indices are 0 .. length-1; otherwise throws | same topic (topic1.4.b) |
| **array\_reference** | the array variable stores the memory address (pointer) of the array; a[i] is found by adding i to that address | same topic (topic1.4.b) |
| **array\_traversal** | walking the array with an index loop | prerequisite of it (it needs this)<br>composition rule (R) with it |
| **assignment** | = stores the computed value of the right side | shares misconception AssignmentCopiesObject |
| **loop\_guard** | putting the bounds check in the loop condition so the body never makes an out-of-bounds array access | same topic (topic1.4.b) |
| **primitive\_vs\_reference** | a primitive variable holds its value; an array (or String) variable holds a reference to the object stored elsewhere | same topic (topic1.4.b) |
| **printing\_array\_reference** | printing an array variable prints a reference, not the elements | same topic (topic1.4.b) |
| **program\_state** | the information needed to know what a program will do next: the values of its variables and array entries and the next statement | same topic (topic1.4.b) |

## Every edge in this view and its full label (20)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **array\_traversal** | prerequisite | **array\_copy** | The elements are copied one at a time by a loop over every index.<br>grounding: book\_passage<br>composition rule (R) of array\_copy with array\_traversal: The copy is a traversal of every index of the original. |
| **array\_copy** | parallel | **array\_aliasing** | b = a makes a second name for the same array (an alias); copying makes a second array: after a copy, changing b[i] leaves a[i] unchanged.<br>grounding: book\_passage<br>composition rule (R) of array\_copy with array\_aliasing: b = a makes an alias of the same array; a copy is a different array: changes through one are not seen through the other. |
| **array\_aliasing** | misconception | **ArrayEqualityComparesValues** | **wrong rule:** a == b is true when a and b hold the same values.<br>**right rule:** == compares whether the two arrays are the same array, not whether their values are equal.<br>role: primary |
| **array\_aliasing** | misconception | **AssignmentCopiesObject** | **wrong rule:** assigning a reference copies the object<br>**right rule:** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].<br>role: primary |
| **array\_copy** | misconception | **ArrayEqualityComparesValues** | **wrong rule:** a == b is true when a and b hold the same values.<br>**right rule:** == compares whether the two arrays are the same array, not whether their values are equal.<br>role: context |
| **array\_copy** | misconception | **AssignmentCopiesObject** | **wrong rule:** assigning a reference copies the object<br>**right rule:** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].<br>role: context |
| **assignment** | misconception | **AssignmentCopiesObject** | **wrong rule:** b = a; for an array makes b a separate copy, so changing b[i] leaves a[i] unchanged.<br>**right rule:** b = a; copies only the reference, so a and b refer to the same array and b[i] = v also changes a[i].<br>role: context |
| **array\_copy** | has\_level | **array\_copy@L0** | array copy -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (4 ways).<br>**[0] everyday\_reading** (E): Everyday 'copy' (b = a, like copying a value onto paper) suggests a second, separate thing. For arrays, b = a only copies the reference; a separate copy needs a new array with each element copied.<br>**[1] misconception** (M) &rarr; AssignmentCopiesObject: wrong rule: Assigning an array reference copies the array. Right rule: b = a copies only the reference, so a and b refer to the same array; to copy, create a new array and copy each element.<br>**[2] inconsistent\_trace** (T) &rarr; AssignmentCopiesObject: Applies the copy rule unevenly: copies element by element in one place but writes b = a in another and expects b to be independent. (here mixing in: "assigning a reference copies the object")<br>**[3] misconception** (M) &rarr; ArrayEqualityComparesValues: wrong rule: a == b is true when a and b hold the same values. Right rule: == compares whether a and b are the same array, so a copy and its original are not ==, even with equal elements. |
| **array\_copy** | has\_level | **array\_copy@L1** | array copy -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Array copy: a second, independent array holding the same elements as the first.<br>**[1] states\_the\_rule** (S): To copy an array, create a new array of the same length and copy the elements one by one: double[] b = new double[N]; for (int i = 0; i &lt; N; i++) b[i] = a[i]; (java.util.Arrays.copyOf does the same). |
| **array\_copy** | has\_level | **array\_copy@L2** | array copy -&gt; L2 (Multistructural): the answer applies the rules of array copy to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Sequencing: new creates the second array first, then the loop copies a[0], a[1], ... in order into b[0], b[1], ...; after the loop, a and b are separate arrays with equal elements.<br>**[1] output\_prediction** (OP): Result: after copying, b[i] == a[i] for every i, but a == b is false; after b[0] = 9, a[0] is unchanged.<br>**[2] one\_step\_execution** (OS): State transition: each pass of the copy loop sets one element of the new array and leaves the original unchanged. |
| **array\_copy** | has\_level | **array\_copy@L3** | array copy -&gt; L3 (Relational): the answer relates the parts (3 ways).<br>**[0] relation\_to\_neighbour** (R): The copy is a traversal of every index of the original.<br>**[1] relation\_to\_neighbour** (R): b = a makes an alias of the same array; a copy is a different array: changes through one are not seen through the other.<br>**[2] purpose\_of\_the\_whole** (P): Plan: copy an array when the original must stay unchanged while the copy is modified (for example shuffling or sorting a copy). |
| **array\_copy** | has\_level | **array\_copy@L4** | array copy -&gt; L4 (Extended abstract): the answer reasons beyond the given code (3 ways).<br>**[0] predict\_a\_change** (C) &rarr; AssignmentCopiesObject: Conservation: changing the copy never changes the original, and the reverse; with an alias every change is shared.<br>**[1] transfer\_to\_a\_new\_program** (X): When an algorithm must change an array but the original is still needed, work on a copy made with new and a loop (or Arrays.copyOf).<br>**[2] diagnose\_an\_error** (D): rule broken: Assignment copies the reference, not the elements. Kind: silent logic error. Trigger class: b = a is used as a copy and then b is modified while a is expected to stay unchanged |
| **topic1.4.b** | contains | **array\_aliasing** | topic topic1.4.b contains array\_aliasing |
| **topic1.4.b** | contains | **array\_bounds** | topic topic1.4.b contains array\_bounds |
| **topic1.4.b** | contains | **array\_copy** | topic topic1.4.b contains array\_copy |
| **topic1.4.b** | contains | **array\_reference** | topic topic1.4.b contains array\_reference |
| **topic1.4.b** | contains | **loop\_guard** | topic topic1.4.b contains loop\_guard |
| **topic1.4.b** | contains | **primitive\_vs\_reference** | topic topic1.4.b contains primitive\_vs\_reference |
| **topic1.4.b** | contains | **printing\_array\_reference** | topic topic1.4.b contains printing\_array\_reference |
| **topic1.4.b** | contains | **program\_state** | topic topic1.4.b contains program\_state |
