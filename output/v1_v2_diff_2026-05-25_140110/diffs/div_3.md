# div.3 — null_pointer

**Student:** I declared String s so it should be empty string by default

## Diagnostic comparison

| field | v1 | v2 |
|---|---|---|
| wrong_model_id | `NP-A` | `NP-A` |
| match_score | 0.93 | 0.93 |
| progmiscon_id | `-` | `AssignmentCopiesObject` |
| jls_reference | `-` | `JLS21 §4.3.1, §15.26` |

## v1 prompt LP-2 block
```
=== LP-1 ===
Student appears at L1; target L2.

=== LP-2: WRONG MENTAL MODEL (IDENTIFIED) ===
Wrong-model ID: NP-A
Student's likely belief: Declaring a variable creates the object. String s; creates a String object named s. The name and the thing are the same act.
Origin: Python/scripting: name = thing is one act. Natural language: naming implies existence.
Matched signal: [st-wm-head match p=0.93]
Address this belief directly, then correct it.
```

## v2 prompt LP-2 / LP-2.5 block
```
=== LP-1 ===
Student appears at L1; target L2.

=== LP-2: WRONG MENTAL MODEL (IDENTIFIED) ===
Wrong-model ID: NP-A
Student's likely belief: Declaring a variable creates the object. String s; creates a String object named s. The name and the thing are the same act.
Origin: Python/scripting: name = thing is one act. Natural language: naming implies existence.
Matched signal: [st-wm-head match p=0.93]
Address this belief directly, then correct it.

=== LP-2.5: FORMAL GROUNDING (from ProgMiscon / Java Language Specification) ===
The student's apparent belief contradicts the Java Language Specification. Specifically: Assignment copies the reference pointing to the object
Reference: JLS21 §4.3.1, §15.26
ProgMiscon misconception ID: AssignmentCopiesObject
Use this grounding to explain WHY the belief is wrong, not just THAT it is.
```

## v1 Ollama response  _(ok=True, 22.28s)_

It sounds like you think declaring a variable creates the object itself. In Java, when we declare `String s;`, we're only creating a reference to a String object, not the object itself. The actual object is created later, when we assign a value to it.

Let's take a look at what happens in this code snippet:

```java
String s;
```

We declare `s` as a reference type variable. It doesn't create an empty string by default; instead, it creates a "null" reference. Think of it like a bookmark or a pointer: we're assigning a name (`s`) to point to the location where the String object will be created.

We can verify this with `System.out.println(s == null);`, which would output `true`. To create an empty string, we need to assign `" "` (a string literal) like this: `s = "";`.

Does that clarify things?

## v2 Ollama response  _(ok=True, 12.33s)_

Let's clarify what happens when we declare a variable in Java. When you write `String s;`, you're creating an empty string object and assigning its reference to the name "s". Think of it like giving a bookshelf a name - the name doesn't create the books, but rather labels the shelf where they'll be stored.

In Java, declaring a variable creates a new reference, but it doesn't automatically create the object. You need to use a constructor or assignment (like `s = "";`) to "put" something into that reference.

Does this make sense?
