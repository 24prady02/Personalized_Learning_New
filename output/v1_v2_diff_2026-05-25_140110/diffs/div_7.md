# div.7 — string_immutability

**Student:** I called s.toUpperCase() but s is still lowercase

## Diagnostic comparison

| field | v1 | v2 |
|---|---|---|
| wrong_model_id | `None` | `None` |
| match_score | 0.00 | 0.00 |
| progmiscon_id | `-` | `-` |
| jls_reference | `-` | `-` |

## v1 prompt LP-2 block
```
=== LP-1 ===
Student appears at L1; target L2.
```

## v2 prompt LP-2 / LP-2.5 block
```
=== LP-1 ===
Student appears at L1; target L2.
```

## v1 Ollama response  _(ok=True, 18.52s)_

So you're getting the expected output in uppercase, but you want to confirm that `s` itself isn't changing to uppercase. In Java, when you call a method like `toUpperCase()` on an object (like a String), it doesn't modify the original object.

Think of it like lending someone your book and asking them to underline a sentence - they can do that with your book without actually modifying it. When you're done "lending" the book back, it's still the same as when you lent it out. Similarly, `toUpperCase()` creates a new String in uppercase form, leaving the original String unchanged.

So, in your case, try printing `s` after calling `toUpperCase()`, and I bet you'll see that it's still in lowercase. To achieve your goal, consider using a different variable to hold the result of `s.toUpperCase()`. What do you think? Want to give it a shot?

## v2 Ollama response  _(ok=True, 13.32s)_

Don't worry, it's an easy mistake! `toUpperCase()` doesn't change the original string. It returns a new string that's all uppercase. So, you need to assign the result back to `s` or use it immediately.

For example:

```java
String s = "hello";
s = s.toUpperCase(); // now s is in uppercase
```

Or:
```java
String s = "hello";
System.out.println(s.toUpperCase()); // prints "HELLO" without changing s
```

Make sense?
