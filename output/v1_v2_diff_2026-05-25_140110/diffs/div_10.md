# div.10 — static_vs_instance

**Student:** cannot make a static reference to non-static field

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

## v1 Ollama response  _(ok=True, 13.4s)_

You're getting close to solving this one!

This error is because you're trying to access an instance variable (a field) from a static method. When you call a static method, it's not associated with any specific instance of the class, so you can't use non-static fields.

Think about it: if every time you run your program, you want to reuse the same values for those variables, then they should be part of the class itself, not dependent on instances. You probably need to declare them as static!

Try changing the field declaration to `static` and see what happens!

## v2 Ollama response  _(ok=True, 25.38s)_

This error usually occurs when you're trying to access an instance variable (a variable inside a method) using the class name, instead of an object. Think of it like trying to reach into your pocket from outside.

For example:
```java
public class MyClass {
    public static void main(String[] args) {
        int x = myObject.y; // error!
    }

    private int y;
}
```
To fix this, you need to create an instance of the class (myObject in this case). You can do that by changing the code to:
```java
public class MyClass {
    public static void main(String[] args) {
        MyClass myObject = new MyClass();
        int x = myObject.y; // now it works!
    }

    private int y;
}
```
Or, if you meant to have a static variable (something that belongs to the class itself), you can make `y` static by adding the keyword `static` before its declaration:
```java
public class MyClass {
    public static void main(String[] args) {
        int x = myObject.y; // now it works!
    }

    private static int y;
}
```
Which one do you think applies to your code?
