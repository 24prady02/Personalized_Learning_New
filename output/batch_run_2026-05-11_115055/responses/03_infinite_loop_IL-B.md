# 03_infinite_loop_IL-B — infinite_loop (expected IL-B)

## Student message
My while loop keeps running forever. I use i in the condition so I thought i would automatically increase each iteration. Doesn't i update on its own when it's used in the loop?

## Student code
```java
int i = 0;
while (i < 10) {
    System.out.println(i);
    // I thought i would increase here automatically
}
```

## Diagnosis
- LP: L3 -> L4
- Classifier WM: IL-B (score=0.8142681121826172)
- RAG hybrid WM: IL-B  (flipped=False)
- BKT mastery: 0.15 -> 0.22

## LLM response

You can see why you're stuck, but let's first make sure you understand how to handle `type_mismatch` errors before we tackle infinite loops.

In Java, a `type_mismatch` error occurs when there's a mismatch between the expected type and the actual type used. For example, if you try to assign an integer value to a variable that was declared as a string, you'll get a `type_mismatch` error.

Here’s a simple example:

```java
String myNumber = "123";
int convertedNumber = myNumber; // This will cause a type_mismatch error
```

In the code above, Java expects an integer value, but it gets a string instead. To fix this, you need to convert the string to an integer:

```java
String myNumber = "123";
int convertedNumber = Integer.parseInt(myNumber); // Correct conversion
```

Now `convertedNumber` will hold the value `123`.

### Practice Exercise

Let's try a practice exercise. Write a program that reads two numbers from the user and adds them together. Make sure you handle any potential `type_mismatch` errors.

```java
import java.util.Scanner;

public class SumOfNumbers {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.println("Enter the first number:");
        String input1 = scanner.nextLine();

        System.out.println("Enter the second number:");
        String input2 = scanner.nextLine();

        try {
            int num1 = Integer.parseInt(input1);
            int num2 = Integer.parseInt(input2);
            int sum = num1 + num2;
            System.out.println("The sum is: " + sum);
        } catch (NumberFormatException e) {
            System.out.println("Invalid input. Please enter valid numbers.");
        }
    }
}
```

### Explanation

- We use `Scanner` to read user input.
- We convert the string input to integers using `Integer.parseInt()`.
- If the conversion fails because the input is not a number, a `NumberFormatException` is thrown, and we handle it in the catch block.

Once you feel confident with handling `type_mismatch` errors, we can return to infinite loops. Let me know when you're ready!