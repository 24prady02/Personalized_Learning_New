# div.6 — type_mismatch

**Student:** I thought + would just combine an int and a string into one string

## Diagnostic comparison

| field | v1 | v2 |
|---|---|---|
| wrong_model_id | `TM-B` | `TM-B` |
| match_score | 0.67 | 0.67 |
| progmiscon_id | `-` | `StringPlusStringifiesExpression` |
| jls_reference | `-` | `JLS21 §15.18.1, §5.1.11` |

## v1 prompt LP-2 block
```
=== LP-1 ===
Student appears at L2; target L3.

=== LP-2: WRONG MENTAL MODEL (IDENTIFIED) ===
Wrong-model ID: TM-B
Student's likely belief: The + operator always concatenates. int + String should produce a string automatically the way Python does.
Origin: Python: str(x) is implicit in many contexts
Matched signal: I thought + would just make them into a string
Address this belief directly, then correct it.
```

## v2 prompt LP-2 / LP-2.5 block
```
=== LP-1 ===
Student appears at L2; target L3.

=== LP-2: WRONG MENTAL MODEL (IDENTIFIED) ===
Wrong-model ID: TM-B
Student's likely belief: The + operator always concatenates. int + String should produce a string automatically the way Python does.
Origin: Python: str(x) is implicit in many contexts
Matched signal: I thought + would just make them into a string
Address this belief directly, then correct it.

=== LP-2.5: FORMAL GROUNDING (from ProgMiscon / Java Language Specification) ===
The student's apparent belief contradicts the Java Language Specification. Specifically: String concatenation evaluates non-String operand expressions and casts value to String
Reference: JLS21 §15.18.1, §5.1.11
ProgMiscon misconception ID: StringPlusStringifiesExpression
Use this grounding to explain WHY the belief is wrong, not just THAT it is.
```

## v1 Ollama response  _(ok=True, 14.16s)_

That's a common misunderstanding! In Java, the `+` operator doesn't automatically convert one type to another. When you use `+` with an integer and a string, it will throw an error because they're different data types.

Think of `+` like a math operation in basic arithmetic: when you add two numbers together, you get a number. But in Java, strings are treated as separate entities from numbers, so the `+` operator doesn't know how to combine them automatically.

To fix this, you can use methods like `String.valueOf()` or concatenation using `+` with both operands as strings: `"a" + String.valueOf(b)`. Does that make sense?

## v2 Ollama response  _(ok=True, 19.4s)_

Let's take a closer look at what's going on here. In Python, you're right that `str(x)` converts to a string implicitly in many cases. However, in Java, the rules are a bit different.

According to the Java Language Specification (Section 15.18.1), when you use the `+` operator with a String and a non-String operand, it doesn't automatically convert the other operand to a string like Python does. Instead, the non-String operand expression is evaluated first, and its value is then cast to a String.

Think of it this way: in Java, `int + "Hello"` doesn't try to concatenate an int with a string by making the int into a string automatically. It tries to make sense of adding an int (e.g., 5) with a string ("Hello"), which doesn't make mathematical sense. So, what happens is that the int value gets converted to a String representation of itself as a number.

Does this clarify things?
