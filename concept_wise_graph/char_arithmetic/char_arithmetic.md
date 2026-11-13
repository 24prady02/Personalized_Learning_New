# char_arithmetic (`char_arithmetic`)

a char is a 16-bit number, so 'a' + 1 is an int

Section 1.2 Built-in Types of Data, topic 1.2.b Characters and strings. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around char_arithmetic](char_arithmetic.png)

## Concepts associated with char\_arithmetic (4)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **char** | 16-bit character primitive | prerequisite of it (it needs this)<br>composition rule (R) with it<br>shares misconception CharNotNumeric<br>same topic (topic1.2.b) |
| **escape\_sequences** | backslash codes inside literals: '\t' tab, '\n' newline | same topic (topic1.2.b) |
| **string\_concatenation** | + with a String builds a new string | same topic (topic1.2.b) |
| **string\_type** | String -- a reference type, not a primitive | same topic (topic1.2.b) |

## Every edge in this view and its full label (13)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **char** | prerequisite | **char\_arithmetic** | Char arithmetic uses the numeric code stored for each char.<br>grounding: book\_passage<br>composition rule (R) of char with char\_arithmetic: Char arithmetic works on each char's numeric code and yields an int. A cast turns the result back into a character.<br>composition rule (R) of char\_arithmetic with char: Char arithmetic uses each char's numeric code, so the result is an int, not a char, unless it is cast back. |
| **char** | misconception | **CharNotNumeric** | **wrong rule:** A char is only a letter, so c + k is an error.<br>**right rule:** A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.<br>role: primary |
| **char\_arithmetic** | misconception | **CharNotNumeric** | **wrong rule:** char is not a numeric type<br>**right rule:** A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.<br>role: context |
| **char\_arithmetic** | has\_level | **char\_arithmetic@L0** | char arithmetic -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): In everyday use letters are not numbers, so 'a' + 1 seems meaningless or should give "a1". Java promotes each char to its int code, so 'a' + 1 is 98.<br>**[1] misconception** (M) &rarr; CharNotNumeric: wrong rule: char is not a numeric type. Right rule: A char is encoded as a 16-bit integer, so arithmetic such as 'b' + 'c' or 'a' + 4 works on the character codes.<br>**[2] inconsistent\_trace** (T) &rarr; CharNotNumeric: Points to LT (chars become int codes before the operator is applied). Applied unevenly, a student converts to codes in one step but keeps letters in another, e.g. printing 'b' + 'c' as "bc". (here mixing in: "char is not a numeric type") |
| **char\_arithmetic** | has\_level | **char\_arithmetic@L1** | char arithmetic -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Char arithmetic: applying arithmetic or comparison operators to char values, which act on their Unicode codes.<br>**[1] states\_the\_rule** (S): char operands of arithmetic are promoted to int, so the result is an int. Casting an int to char gives the character with that code. ++, -- and comparisons work directly on chars. |
| **char\_arithmetic** | has\_level | **char\_arithmetic@L2** | char arithmetic -&gt; L2 (Multistructural): the answer applies the rules of char arithmetic to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): Each char operand is replaced by its code (promoted to int) and the operation runs in int. A cast written outside the parentheses, as in (char) ('a' + 4), is applied last.<br>**[1] output\_prediction** (OP): 'b' + 'c' is the int 197. 'a' + 4 is 101. (char) ('a' + 4) is 'e'. 'A' &lt; 'a' is true.<br>**[2] one\_step\_execution** (OS): For char c = 'A', c++ sets c to 'B'. c = c + 1; is rejected, because the right side is an int. |
| **char\_arithmetic** | has\_level | **char\_arithmetic@L3** | char arithmetic -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): Char arithmetic uses each char's numeric code, so the result is an int, not a char, unless it is cast back.<br>**[1] purpose\_of\_the\_whole** (P): Plans: shifting letters (Caesar cipher), turning a digit char into its value (c - '0'), looping over 'A'..'Z', and testing whether a char is in a range. |
| **char\_arithmetic** | has\_level | **char\_arithmetic@L4** | char arithmetic -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).<br>**[0] predict\_a\_change** (C) &rarr; CharNotNumeric: Adding or removing the (char) cast changes the output from a number to a letter. Changing 'a' + 4 to "a" + 4 makes it concatenation ("a4").<br>**[1] transfer\_to\_a\_new\_program** (X): Use char arithmetic when the computation depends on character order or codes (alphabet loops, ciphers, digit values). To join characters into text, use String + or a String instead.<br>**[2] diagnose\_an\_error** (D): rule broken: Arithmetic on chars yields an int, which needs a cast to go back into a char. Kind: compile-time. Trigger class: char next = c + 1; or char d = 'a' + k;: 'possible lossy conversion from int to char'.<br>**[3] diagnose\_an\_error** (D): rule broken: Without a cast the int code is printed, not the letter. Kind: silent logic error. Trigger class: Printing c + 1 or 'a' + i when a letter was expected.<br>**[4] diagnose\_an\_error** (D): rule broken: A char compares by its code, not by the digit it shows. Kind: silent logic error. Trigger class: Comparing a char with an int as if it were a digit (seat &lt;= 3 for seat = 'A'). |
| **topic1.2.b** | contains | **char** | topic topic1.2.b contains char |
| **topic1.2.b** | contains | **char\_arithmetic** | topic topic1.2.b contains char\_arithmetic |
| **topic1.2.b** | contains | **escape\_sequences** | topic topic1.2.b contains escape\_sequences |
| **topic1.2.b** | contains | **string\_concatenation** | topic topic1.2.b contains string\_concatenation |
| **topic1.2.b** | contains | **string\_type** | topic topic1.2.b contains string\_type |
