# div.9 — no_default_constructor

**Student:** cannot find symbol - constructor Foo()

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
Student appears at L3; target L4.
```

## v2 prompt LP-2 / LP-2.5 block
```
=== LP-1 ===
Student appears at L3; target L4.
```

## v1 Ollama response  _(ok=True, 15.29s)_

It looks like we have a minor issue here! The error message "cannot find symbol" usually means that the Java compiler can't find something it's looking for, which in this case is the constructor `Foo()`.

Here are a few possibilities:

1. Did you forget to import the class `Foo` from another package?
2. Is there a typo in the name of the class or method? Make sure it matches exactly how it was defined.
3. Has the `Foo` class been properly declared and implemented?

Let's take a closer look at your code. Can you show me where you've defined the `Foo` class, and what its constructor looks like?

## v2 Ollama response  _(ok=True, 12.85s)_

It looks like we're running into a common issue here!

The error message "cannot find symbol" usually means that Java can't find a specific variable or method. In this case, it's complaining about the constructor `Foo()`.

Here are a few things to check:

1. Make sure you've defined a no-arg constructor in your `Foo` class.
2. Ensure that you're referencing the correct class and constructor.
3. Verify that there aren't any typos or missing imports.

Let's take a closer look at your code together. Can you share the relevant parts of your `Foo.java` file?
