# div.4 — null_pointer

**Student:** I set s = null then called .length(), why does it crash?

## Diagnostic comparison

| field | v1 | v2 |
|---|---|---|
| wrong_model_id | `NP-B` | `NP-B` |
| match_score | 0.61 | 0.61 |
| progmiscon_id | `-` | `NullIsObject` |
| jls_reference | `-` | `JLS21 §3.10.8, §4.3.1` |

## v1 prompt LP-2 block
```
=== LP-1 ===
Student appears at L1; target L2.

=== LP-2: WRONG MENTAL MODEL (IDENTIFIED) ===
Wrong-model ID: NP-B
Student's likely belief: null means empty or zero. Calling a method on null should return empty/default result, not crash.
Origin: null is like 0 for numbers or empty string for strings - a valid default value
Matched signal: [st-wm-head match p=0.61]
Address this belief directly, then correct it.
```

## v2 prompt LP-2 / LP-2.5 block
```
=== LP-1 ===
Student appears at L1; target L2.

=== LP-2: WRONG MENTAL MODEL (IDENTIFIED) ===
Wrong-model ID: NP-B
Student's likely belief: null means empty or zero. Calling a method on null should return empty/default result, not crash.
Origin: null is like 0 for numbers or empty string for strings - a valid default value
Matched signal: [st-wm-head match p=0.61]
Address this belief directly, then correct it.

=== LP-2.5: FORMAL GROUNDING (from ProgMiscon / Java Language Specification) ===
The student's apparent belief contradicts the Java Language Specification. Specifically: null is a reference pointing to no object
Reference: JLS21 §3.10.8, §4.3.1
ProgMiscon misconception ID: NullIsObject
Use this grounding to explain WHY the belief is wrong, not just THAT it is.
```

## v1 Ollama response  _(ok=True, 16.01s)_

The .length() method doesn't return 0 or an empty string because null is not a valid object that has length. It's like trying to ask for the height of a non-existent building - there's no property to retrieve. 

In Java, calling a method on null will indeed crash with a NullPointerException (which is why we see that error message). That's because you're essentially asking the compiler to operate on something that doesn't exist.

Think about it like this: if s were an empty string, then .length() would return 0. But since s is null, there's no property called "length" for Java to work with. We need to initialize s before using it or check if it's null first. Does that make sense?

## v2 Ollama response  _(ok=True, 20.19s)_

Let's take a closer look at what's going on. You're thinking that calling methods on `null` should be like working with an empty string or zero - you should get some kind of default result, but not crash the program.

That makes sense in a way, because `null` is used to represent "no value" or "nothing". But what's actually happening when you call `.length()` on `null`?

According to the Java Language Specification, `null` isn't really like an empty string or zero. It's not an object at all - it's just a reference that points to nothing. When you try to call a method on `null`, Java can't figure out what code to run because there is no actual object to work with.

Think of it like trying to get the length of a book when you haven't even picked one up yet. You can't get its length if you don't have it! That's basically what's happening when you try to call `.length()` on `null`.

Does that make sense?
