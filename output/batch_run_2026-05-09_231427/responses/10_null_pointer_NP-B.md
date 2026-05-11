# 10_null_pointer_NP-B — null_pointer (expected NP-B)

## Student message
I have a Widget with a label field. When I call describe() before setting label, it crashes. Can't null just mean "nothing" and return an empty string? Why does calling a method on null have to blow up?

## Student code
```java
public class Widget {
    String label;
    public String describe() { return label.toUpperCase(); }
}
// Widget w = new Widget(); w.describe();  // NullPointerException
```

## Diagnosis
- LP: L4 -> L4
- Classifier WM: NP-B (score=0.5275176167488098)
- RAG hybrid WM: NP-B  (flipped=False)
- BKT mastery: 0.30 -> 0.24

## LLM response

It seems there's been a mix-up. The student is asking about Java, but their provided code snippet is written in Python. Let's correct this and proceed with the Java version.

The student's question:
"I have a Widget with a label field. When I call describe() before setting label, it crashes. Can't null just mean 'nothing' and return an empty string? Why does calling a method on null have to blow up?"

Student's code (Java version):
```java
public class Widget {
    String label;
    public String describe() { return label.toUpperCase(); }
}
// Widget w = new Widget(); w.describe();  // NullPointerException
```

Let's address the misconceptions and provide a visual explanation before moving on to a transfer task.

### Misconception: null means empty or zero. Calling a method on null should return empty/default result, not crash.
**Corrected Mechanism:**  
- When you declare a reference (like `String label;`), it is initially set to `null`. This indicates that the reference does **not** point to any object in memory.
- To use an object's methods or access its fields, you need to first create an object and get its address. For example: `label = new String("Hello");`.
- If you call a method on a `null` reference, Java has no way of knowing what object it should refer to because the reference is empty (it holds no value). This leads to a **NullPointerException**.

### Transfer Task
Now that you understand why calling methods on null results in a crash, let's apply this understanding to a new scenario involving database connections. 

Imagine you have a `DatabaseConnection` class:

```java
public class DatabaseConnection {
    private Connection conn;

    public void connect() {
        // Simulate connection logic
        conn = DriverManager.getConnection("jdbc:mysql://localhost/db", "user", "password");
    }

    public boolean isConnected() {
        return conn != null;  // Check if the connection is established
    }

    public void close() throws SQLException {
        if (conn != null) {
            conn.close();
        }
    }
}
```

**Task:**  
1. Implement a method `executeQuery(String query)` in the `DatabaseConnection` class.
2. The method should execute the given SQL query only if the connection is established (`isConnected()` returns true).
3. If the connection is not established, it should return an empty string.

Here's how you can do it:

```java
public String executeQuery(String query) {
    if (isConnected()) {
        try {
            // Simulate executing a query
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery(query);
            StringBuilder result = new StringBuilder();
            while (rs.next()) {
                result.append(rs.getString(1)).append("\n");
            }
            return result.toString();
        } catch (SQLException e) {
            e.printStackTrace();
            return "";
        }
    } else {
        return "";  // Return an empty string if not connected
    }
}
```

### Challenge
Think about edge cases for this method. What happens if the query itself throws a `SQLException`? How can you handle it gracefully?

**Design Question:**
Why do you think Java's designers made this choice to throw a `NullPointerException` when calling methods on null references? What are some pros and cons of this design choice?

### Consolidation
By addressing this task, you've reinforced the principle that calling methods on null references can lead to crashes. Understanding this is crucial for writing robust and error-free Java code.

**Mastered Design Principle:**
The design principle you’ve mastered here is **Null Safety**, which involves ensuring that your code handles `null` values gracefully to avoid runtime exceptions like `NullPointerException`.

Good job so far! Keep up the good work, and I'm sure you'll get this right.