# div.2 — string_equality

**Student:** I made two strings with the same text so they should be equal

## Diagnostic comparison

| field | v1 | v2 |
|---|---|---|
| wrong_model_id | `SE-A` | `SE-A` |
| match_score | 1.00 | 1.00 |
| progmiscon_id | `-` | `EqualityOperatorComparesObjectsValues` |
| jls_reference | `-` | `JLS21 §15.21` |

## v1 prompt LP-2 block
```
=== LP-1 ===
Student appears at L1; target L2.

=== LP-2: WRONG MENTAL MODEL (IDENTIFIED) ===
Wrong-model ID: SE-A
Student's likely belief: == compares the content of strings. Two strings with the same characters are equal under ==.
Origin: Python: == calls __eq__ which compares content. Mathematics: equality means same value.
Matched signal: the text is the same
Address this belief directly, then correct it.
```

## v2 prompt LP-2 / LP-2.5 block
```
=== LP-1 ===
Student appears at L1; target L2.

=== LP-2: WRONG MENTAL MODEL (IDENTIFIED) ===
Wrong-model ID: SE-A
Student's likely belief: == compares the content of strings. Two strings with the same characters are equal under ==.
Origin: Python: == calls __eq__ which compares content. Mathematics: equality means same value.
Matched signal: the text is the same
Address this belief directly, then correct it.

=== LP-2.5: FORMAL GROUNDING (from ProgMiscon / Java Language Specification) ===
The student's apparent belief contradicts the Java Language Specification. Specifically: o==p compares the references stored in the variables o and p
Reference: JLS21 §15.21
ProgMiscon misconception ID: EqualityOperatorComparesObjectsValues
Use this grounding to explain WHY the belief is wrong, not just THAT it is.
```

## v1 Ollama response  _(ok=True, 14.67s)_

You're on to something! It's great that you think two strings with the same text should be equal. But in Java, equality for strings is a bit more nuanced than just comparing the content.

When we use `==` for strings, it checks if both variables are pointing to the **exact same object** in memory, not just if they have the same characters. Think of it like two different books with the same title - they're not the same book, even if their contents are identical.

To compare the actual content of a string, we use `equals()` instead of `==`. For example: `"hello".equals("hello")` would return true because it's comparing the character sequences directly. Make sense?

## v2 Ollama response  _(ok=True, 17.33s)_

Let's clarify what happens when we use the `==` operator in Java. When you write `string1 == string2`, Java doesn't compare the actual characters stored in both strings, but rather it checks if both variables point to the same memory location where those characters are stored. Think of it like two pointers on a map: just because they're pointing at the same place doesn't mean they're the same map.

According to the Java Language Specification, `==` compares object references, not their contents. So even if two strings have the same text, as long as they were created separately (not assigned from one another), their `==` comparison will be false. Does that make sense?
