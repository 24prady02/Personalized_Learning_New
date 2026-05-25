# div.5 — assignment_vs_compare

**Student:** I wrote if (x = 5) but it's not comparing

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

## v1 Ollama response  _(ok=True, 13.91s)_

I think I see where you're coming from! In Java, when you want to check if a variable is equal to a certain value, you should use the `==` operator, like this:

```java
if (x == 5) {
    // do something if x is indeed 5
}
```

Notice the double equals sign (`==`) instead of a single one. The single equals sign (`=`) is used for assignment, not comparison. So in your code, `x = 5` actually sets the value of `x` to 5, but it doesn't check if `x` already has that value.

Does this make sense?

## v2 Ollama response  _(ok=True, 10.75s)_

One small tweak can make a big difference! In Java, when you want to check if a variable equals something, you need to use the "double equals" sign ==. So instead of `if (x = 5)`, try using `if (x == 5)`.

Think about it like this: the single equals sign = is for assigning values, whereas the double equals sign == is for comparing them. Make sense? Give it a shot and see if that fixes your code!
