# 05_array_index_AI-A — array_index (expected AI-A)

## Student message
I have an array with 5 numbers: 10, 20, 30, 40, 50. When I try arr[5] to get the fifth element I get ArrayIndexOutOfBoundsException. The fifth slot holds 50, why isn't arr[5] giving me 50?

## Student code
```java
int[] arr = {10, 20, 30, 40, 50};
int fifth = arr[5];   // crashes
```

## Diagnosis
- LP: L3 -> L4
- Classifier WM: AI-C (score=0.46619606018066406)
- RAG hybrid WM: AI-B  (flipped=True)
- BKT mastery: 0.30 -> 0.24

## LLM response

Let's start by confirming the mechanism you just articulated:

When you access an array element using `arr[5]`, you are trying to access index 5. However, arrays in Java are **zero-indexed**, which means they start counting from 0. Therefore, a 5-element array has valid indices ranging from 0 to 4.

Let's break it down step-by-step:

1. `arr.length` is 5.
2. The valid indices for the array are: 0, 1, 2, 3, and 4.
3. Trying to access index 5 results in an **ArrayIndexOutOfBoundsException** because there is no element at index 5.

Now, let's look at a worked example:

```java
int[] arr = {10, 20, 30, 40, 50};
for (int i = 0; i <= arr.length - 1; i++) {
    System.out.println("arr[" + i + "] = " + arr[i]);
}
```

This loop will correctly print:

```
arr[0] = 10
arr[1] = 20
arr[2] = 30
arr[3] = 40
arr[4] = 50
```

Notice that `i` goes from 0 to `arr.length - 1`. This ensures that we always access valid indices within the array.

Now, let's connect this example to your code:

```java
int[] arr = {10, 20, 30, 40, 50};
int fifth = arr[5];   // crashes
```

In this case, `arr.length` is 5, so the valid indices are 0 through 4. Accessing `arr[5]` goes one past the last valid index and results in an **ArrayIndexOutOfBoundsException**.

### What's the shared mechanism between these two cases?

1. Both involve accessing an array.
2. In both cases, you are trying to access an index that is one beyond the last valid index.
3. Both result in an **ArrayIndexOutOfBoundsException** because the accessed index is out of bounds.

### General Principle:

The principle being abstracted here is that when working with arrays in Java:
- Arrays are zero-indexed.
- The last valid index for an array of length `n` is `n - 1`.
- Accessing any index greater than or equal to `arr.length` will result in an **ArrayIndexOutOfBoundsException**.

### Transfer Challenge:

Now, let's try a harder variant that requires the same mechanism applied in an unfamiliar setting. Consider this code:

```java
int[] numbers = {100, 200, 300};
for (int i = 0; i <= numbers.length; i++) {
    System.out.println("numbers[" + i + "] = " + numbers[i]);
}
```

What will happen when you run this code? Why?

Take a moment to think about it before moving on.