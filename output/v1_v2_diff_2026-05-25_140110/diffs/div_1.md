# div.1 — string_equality

**Student:** why does == not work for comparing strings?

## Diagnostic comparison

| field | v1 | v2 |
|---|---|---|
| wrong_model_id | `SE-C` | `SE-C` |
| match_score | 0.70 | 0.70 |
| progmiscon_id | `-` | `StringLiteralNoObject` |
| jls_reference | `-` | `JLS21 §3.10.5` |

## v1 prompt LP-2 block
```
=== LP-1 ===
Student appears at L2; target L3.

=== LP-2: WRONG MENTAL MODEL (IDENTIFIED) ===
Wrong-model ID: SE-C
Student's likely belief: == and .equals() are interchangeable syntax variants. One is shorthand for the other.
Origin: Syntactic variants in other languages (== and .equals() in some frameworks behave identically)
Matched signal: [st-wm-head match p=0.70]
Address this belief directly, then correct it.
```

## v2 prompt LP-2 / LP-2.5 block
```
=== LP-1 ===
Student appears at L2; target L3.

=== LP-2: WRONG MENTAL MODEL (IDENTIFIED) ===
Wrong-model ID: SE-C
Student's likely belief: == and .equals() are interchangeable syntax variants. One is shorthand for the other.
Origin: Syntactic variants in other languages (== and .equals() in some frameworks behave identically)
Matched signal: [st-wm-head match p=0.70]
Address this belief directly, then correct it.

=== LP-2.5: FORMAL GROUNDING (from ProgMiscon / Java Language Specification) ===
The student's apparent belief contradicts the Java Language Specification. Specifically: A String literal represents a String object and can be treated as such
Reference: JLS21 §3.10.5
ProgMiscon misconception ID: StringLiteralNoObject
Use this grounding to explain WHY the belief is wrong, not just THAT it is.
```

## v1 Ollama response  _(ok=True, 27.57s)_

I see what might be going on here! In Java, `==` checks if two variables point to the same memory location, whereas `.equals()` checks if their values are equal. So when you use `==` to compare strings, it's not looking at the actual characters in the string, but rather where they're stored in memory.

To see this in action, let's try a simple example:
```java
String s1 = "hello";
String s2 = "hello";

System.out.println(s1 == s2); // prints false (even though they have the same value)
System.out.println(s1.equals(s2)); // prints true (because their values are equal)
```
Does that make sense?

## v2 Ollama response  _(ok=True, 21.35s)_

"Great question! So, in Java, when you compare two objects using `==`, it checks if they are the same object in memory, not just equal. This is because `==` checks for reference equality, not value equality.

Let's take an example: if you have two strings `a = "hello"` and `b = "hello"`, even though their values are the same, `a == b` would return false because they are two separate objects in memory.

On the other hand, when you compare strings using `.equals()`, it checks for value equality. So, `a.equals(b)` would return true because they have the same value.

Think of it like comparing two books: `==` is like checking if they're the same physical book on your shelf, while `.equals()` is like checking if their contents are the same, regardless of where you find them."

(Note: I'm responding in a way that directly addresses the student's belief and provides a clear explanation grounded in formal concepts from the Java Language Specification.)
