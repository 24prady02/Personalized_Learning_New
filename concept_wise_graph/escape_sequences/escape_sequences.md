# escape_sequences (`escape_sequences`)

backslash codes inside literals: '\t' tab, '\n' newline

Section 1.2 Built-in Types of Data, topic 1.2.b Characters and strings. From the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`).

![The knowledge graph around escape_sequences](escape_sequences.png)

## Concepts associated with escape\_sequences (5)

| Concept | Description | How it is associated |
| --- | --- | --- |
| **char** | 16-bit character primitive | same topic (topic1.2.b) |
| **char\_arithmetic** | a char is a 16-bit number, so 'a' + 1 is an int | same topic (topic1.2.b) |
| **string\_concatenation** | + with a String builds a new string | same topic (topic1.2.b) |
| **string\_literal** | "Hello, World" -- the text being printed | prerequisite of it (it needs this)<br>composition rule (R) with it |
| **string\_type** | String -- a reference type, not a primitive | same topic (topic1.2.b) |

## Every edge in this view and its full label (12)

| From | Edge | To | Full edge label |
| --- | --- | --- | --- |
| **string\_literal** | prerequisite | **escape\_sequences** | Escape sequences are written inside string or char literals.<br>grounding: book\_passage<br>composition rule (R) of string\_literal with escape\_sequences: Escape sequences (\n, \t, \", \\) are written inside string or char literals to stand for one character that cannot be typed directly.<br>composition rule (R) of escape\_sequences with string\_literal: Escapes are written inside "..." or '...'. \" puts a double quote inside a String literal without ending it. |
| **escape\_sequences** | misconception | **EscapeIsTwoCharacters** | **wrong rule:** \t in a string prints a backslash and the letter t.<br>**right rule:** A backslash starts an escape sequence, so \t is a single tab character.<br>role: primary |
| **escape\_sequences** | has\_level | **escape\_sequences@L0** | escape sequences -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (3 ways).<br>**[0] everyday\_reading** (E): In everyday text a backslash is just a character, and a new line is made by pressing Enter. Inside a Java literal a backslash starts an escape: \n is one newline character and \\ is one backslash, and a literal cannot contain a raw line break.<br>**[1] misconception** (M) &rarr; EscapeIsTwoCharacters: wrong rule: \t in a string prints a backslash and the letter t. Right rule: A backslash starts an escape sequence, so \t is a single tab character.<br>**[2] inconsistent\_trace** (T) &rarr; EscapeIsTwoCharacters: Points to LT (the compiler turns each escape into a single character). Applied unevenly, a student prints "\n" as a line break but counts it as two characters in length() or charAt. (here mixing in: "\t in a string prints a backslash and the letter t") |
| **escape\_sequences** | has\_level | **escape\_sequences@L1** | escape sequences -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).<br>**[0] names\_the\_element** (N): Escape sequence: a backslash code inside a char or String literal that stands for one special character (\t, \n, \\, \', \").<br>**[1] states\_the\_rule** (S): Java has eight escape sequences. The common ones are \t (tab), \n (newline), \\ (backslash), \' (single quote) and \" (double quote), and each represents a single character. |
| **escape\_sequences** | has\_level | **escape\_sequences@L2** | escape sequences -&gt; L2 (Multistructural): the answer applies the rules of escape sequences to every part of the code, in order (3 ways).<br>**[0] line\_by\_line\_trace** (LT): The compiler replaces each escape with its single character while reading the literal, so at run time the String already contains that one character.<br>**[1] output\_prediction** (OP): System.out.print("Hello!\nHow are you doing?\n") prints two lines. "a\tb" prints a, a tab, then b. "Hi\n".length() is 3.<br>**[2] one\_step\_execution** (OS): An escape changes no variable. Printing \n moves the output position to the start of a new line. |
| **escape\_sequences** | has\_level | **escape\_sequences@L3** | escape sequences -&gt; L3 (Relational): the answer relates the parts (2 ways).<br>**[0] relation\_to\_neighbour** (R): Escapes are written inside "..." or '...'. \" puts a double quote inside a String literal without ending it.<br>**[1] purpose\_of\_the\_whole** (P): Escapes format output (line breaks, tab-aligned columns) and put quote or backslash characters into text. |
| **escape\_sequences** | has\_level | **escape\_sequences@L4** | escape sequences -&gt; L4 (Extended abstract): the answer reasons beyond the given code (5 ways).<br>**[0] predict\_a\_change** (C) &rarr; EscapeIsTwoCharacters: Removing the backslash turns \n into the letter n. Doubling it (\\n) prints a backslash followed by n. Adding a space after \n puts a space at the start of the next line.<br>**[1] transfer\_to\_a\_new\_program** (X): Use escapes for special characters inside literals. For line ends in formatted output, use println or printf's %n, which gives the platform line separator.<br>**[2] diagnose\_an\_error** (D): rule broken: A double quote inside a String literal must be escaped. Kind: compile-time. Trigger class: An unescaped " inside a String, such as "She said "Hi"": the literal ends early, and the compiler reports an unclosed literal or ')' expected.<br>**[3] diagnose\_an\_error** (D): rule broken: A backslash must be followed by a valid escape character. Kind: compile-time. Trigger class: Backslash plus an undefined letter, e.g. a Windows path "C:\data": 'illegal escape character'.<br>**[4] diagnose\_an\_error** (D): rule broken: A backslash followed by a valid escape letter is replaced by that character. Kind: silent logic error. Trigger class: Paths or text containing \t or \n by accident ("C:\temp" contains a tab). |
| **topic1.2.b** | contains | **char** | topic topic1.2.b contains char |
| **topic1.2.b** | contains | **char\_arithmetic** | topic topic1.2.b contains char\_arithmetic |
| **topic1.2.b** | contains | **escape\_sequences** | topic topic1.2.b contains escape\_sequences |
| **topic1.2.b** | contains | **string\_concatenation** | topic topic1.2.b contains string\_concatenation |
| **topic1.2.b** | contains | **string\_type** | topic topic1.2.b contains string\_type |
