# args_length (`args_length`)

args.length gives the number of command-line arguments

Section 1.4 Arrays, topic 1.4.a Arrays in Java (declare, create, initialize; indexing; length; default values). From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around args_length](args_length.png)

## Concepts associated with args\_length (9)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **array\_creation** | new int[n] -- allocates n slots | same topic (topic1.4.a) |
| **array\_declaration** | int[] a; -- declares an array variable | same topic (topic1.4.a) |
| **array\_default\_values** | new slots start at 0 / false / null | same topic (topic1.4.a) |
| **command\_line\_args** | args[] -- strings passed at launch | prerequisite of it (it needs this)<br>composition rule (R) with it<br>shares error ArgsAlwaysPresent |
| **data\_structure** | a method for organizing data; the one-dimensional array is the first example | same topic (topic1.4.a) |
| **indexing** | a[i] -- 0-based access | same topic (topic1.4.a) |
| **length\_field** | a.length is a field, not a method | prerequisite of it (it needs this)<br>composition rule (R) with it<br>same topic (topic1.4.a) |
| **off\_by\_one\_error** | a loop or index that runs one time too many or too few (&lt; vs &lt;=, 0..n vs 1..n, length vs length-1) | same topic (topic1.4.a) |
| **run\_time\_error** | an error raised while the program executes (e.g. ArrayIndexOutOfBounds, NumberFormatException) | shares error ArgsAlwaysPresent |

## Every edge in this view and its full label (18)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **command\_line\_args** | prerequisite | **args\_length** | args is the array of command-line arguments.<br>grounding: book\_passage<br>composition rule (R) of command\_line\_args with args\_length: args.length is the number of arguments typed (0 if none), so valid indices are 0 to args.length-1.<br>composition rule (R) of args\_length with command\_line\_args: args[i] may be read only for i &lt; args.length; with no arguments even args[0] is out of bounds. |
| **length\_field** | prerequisite | **args\_length** | args is an ordinary String array, so args.length is its length field and counts the command-line arguments.<br>grounding: order\_only<br>composition rule (R) of length\_field with args\_length: args is an ordinary String[], so args.length is its length field and counts the command-line arguments (0 when none are typed).<br>composition rule (R) of args\_length with length\_field: args.length is the ordinary array length field applied to the String[] args. |
| **args\_length** | error | **ArgsAlwaysPresent** | **wrong rule:** args[0] can always be read.<br>**right rule:** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0.<br>role: primary |
| **command\_line\_args** | error | **ArgsAlwaysPresent** | **wrong rule:** args[0] can always be read.<br>**right rule:** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0.<br>role: context |
| **run\_time\_error** | error | **ArgsAlwaysPresent** | **wrong rule:** args[0] can always be read.<br>**right rule:** If you run the program without typing the command-line argument it expects, reading args[0] fails with java.lang.ArrayIndexOutOfBoundsException: 0.<br>role: context |
| **args\_length** | has\_level | **args\_length@L0** | args length -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (1 way).<br>**[0] everyday\_reading** (E): Folk meaning: like a conversation partner, the program is thought to 'get' the input it expects; arguments are always there. Java rule: args holds exactly the strings typed after the class name, so args.length can be 0 and args[0] exists only when args.length &gt;= 1. |
| **args\_length** | has\_level | **args\_length@L1** | args length -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Identity: args.length is the length field of main's String[] parameter args; it counts the command-line arguments.<br>**[1] states\_the\_rule** (S): Declarative: args is a String[] whose elements args[0] .. args[args.length-1] are the typed arguments, as strings; numbers must be converted with Integer.parseInt or Double.parseDouble. |
| **args\_length** | has\_level | **args\_length@L2** | args length -&gt; L2 (Multistructural): the answer applies the rules of args length to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Sequencing: the command line is split at whitespace, and the pieces are stored in order in args before main's first statement runs. Reading args.length then behaves like any length field.<br>**[1] output\_prediction** (OP): Result: an int equal to the number of typed arguments: 'java Max' gives 0, and 'java Max 10 -3 55 0 14' gives 5.<br>**[2] one\_step\_execution** (OS): State transition: reading args.length changes nothing; args itself is fixed for the whole run. |
| **args\_length** | has\_level | **args\_length@L3** | args length -&gt; L3 (Relational): the answer relates the parts (3 ways).<br>**[0] relation\_to\_neighbour** (R): args[i] may be read only for i &lt; args.length; with no arguments even args[0] is out of bounds.<br>**[1] relation\_to\_neighbour** (R): args.length is the ordinary array length field applied to the String[] args.<br>**[2] purpose\_of\_the\_whole** (P): Plan/role: validate input before use (print a usage message and return when args.length is too small), or loop over a variable number of arguments. |
| **args\_length** | has\_level | **args\_length@L4** | args length -&gt; L4 (Extended abstract): the answer reasons beyond the given code (4 ways).<br>**[0] predict\_a\_change** (C): Conservation: extra arguments do not break code that reads args[0]; fewer arguments than the code reads break it at run time. Adding an args.length check keeps behaviour for correct input and only changes what happens for bad input.<br>**[1] diagnose\_an\_error** (D): rule broken: args[i] exists only if i &lt; args.length. Kind: run-time exception. Trigger class: the program is run with fewer command-line arguments than it reads, e.g. none at all (java.lang.ArrayIndexOutOfBoundsException: 0)<br>**[2] transfer\_to\_a\_new\_program** (X): Applicability: use args.length to validate or iterate over a small, variable number of command-line values. For large or open-ended input, read standard input instead.<br>**[3] diagnose\_an\_error** (D): rule broken: An argument is a String and must be a valid numeral to be parsed. Kind: run-time exception. Trigger class: a non-numeric argument is passed to Integer.parseInt, e.g. 'five' (NumberFormatException) |
| **topic1.4.a** | contains | **args\_length** | topic topic1.4.a contains args\_length |
| **topic1.4.a** | contains | **array\_creation** | topic topic1.4.a contains array\_creation |
| **topic1.4.a** | contains | **array\_declaration** | topic topic1.4.a contains array\_declaration |
| **topic1.4.a** | contains | **array\_default\_values** | topic topic1.4.a contains array\_default\_values |
| **topic1.4.a** | contains | **data\_structure** | topic topic1.4.a contains data\_structure |
| **topic1.4.a** | contains | **indexing** | topic topic1.4.a contains indexing |
| **topic1.4.a** | contains | **length\_field** | topic topic1.4.a contains length\_field |
| **topic1.4.a** | contains | **off\_by\_one\_error** | topic topic1.4.a contains off\_by\_one\_error |
