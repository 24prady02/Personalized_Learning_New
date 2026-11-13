# method_call (`method_call`)

name(arguments) -- invokes a library method and uses its return value

Section 1.2 Built-in Types of Data, topic 1.2.g Library methods and APIs (Math).

![The knowledge graph around method_call](method_call.png)

## At a glance

- **Needs first:** `expression`
- **Leads to:** `api`, `math_library`
- **Learned alongside:** nothing
- **Misconceptions:** `ArgumentOrderInferred`, `ArrayHasLengthMethod`, `EqualsComparesReferences`, `OutsideInMethodNesting`, `ParameterTypesInCall`, `ParenthesesOnlyIfArgument`, `StringMethodChangesString`
- **Errors:** `DiscardedReturnValue`, `MathMethodWithoutClassName`, `WrongArgumentType`
- **Levels:** L0, L1, L2, L3, L4

Everything below comes from the knowledge graph 3.9.8 (`data/raw/chapter1_kg_updated.json`): 36 edges around this concept. The edge logic, the wrong and right rules and the exact rules of the ways are copied word for word from the graph.

## To work on (1)

- misconceptions with no L0 way linked to them: StringMethodChangesString

## What it needs first (1)

A prerequisite edge means the other concept has to be understood before `method_call`.

### `expression` comes before `method_call`

*anything that evaluates to a value*

- **Edge:** `pre:expression->method_call`
- **Exact edge logic:** Method arguments may be expressions, and a method call can be used in expressions in the same way as variables and literals.
- **Grounding:** book\_passage
- **Composition rule (R) of `method_call` with `expression`:** Arguments may be arbitrary expressions of the right type, and the call itself is an expression usable inside larger ones (Math.sin(x) \* Math.cos(y)).
- **Composition rule (R) of `expression` with `method_call`:** A method call is an expression usable wherever a value of its return type is, and its arguments are expressions evaluated before the call.

## What it leads to (2)

These concepts need `method_call` first.

### `method_call` comes before `api`

*Application programming interface (API): a table of library methods giving each method's signature and a short description of what it computes*

- **Edge:** `pre:method_call->api`
- **Exact edge logic:** An API lists, for each library method, the signature you need in order to call it: name, argument types and return type.
- **Grounding:** book\_passage
- **Composition rule (R) of `method_call` with `api`:** The call must match a signature in the API (name, number, order and types of arguments), and the API's return type tells how the value can be used.
- **Composition rule (R) of `api` with `method_call`:** Each call must match one API signature: same name, arguments of the listed types in the listed order, and use of the value consistent with the return type.

### `method_call` comes before `math_library`

*Math.abs, Math.sqrt, Math.max, Math.random, Math.round ...*

- **Edge:** `pre:method_call->math_library`
- **Exact edge logic:** Math.sqrt(x) and other Math methods are used through method calls.
- **Grounding:** book\_passage
- **Composition rule (R) of `method_call` with `math_library`:** Math methods are called through the class name, Math.sqrt(x); without the prefix the compiler looks for the method in the current class and reports cannot find symbol.
- **Composition rule (R) of `math_library` with `method_call`:** Every Math facility is used through a method call with the Math. prefix and parentheses (the constants Math.PI and Math.E are written without parentheses).

## Learned alongside (0)

A parallel edge joins two concepts that sit side by side: neither is needed before the other.

No parallel edge touches this concept.

## Misconceptions (7)

A misconception edge states the wrong rule a student may hold about this concept, and the right rule.

### ArgumentOrderInferred

- **Edge:** `method_call` &rarr; `ArgumentOrderInferred` (misconception)
- **Exact edge logic (the wrong rule):** Java works out from the variable names which argument goes where, so Math.pow(n, 2) and Math.pow(2, n) mean the same.
- **Twin logic (the right rule):** Arguments are written in the order the method's signature lists them; for example, Math.pow(a, b) raises a to the bth power.
- **Wrong belief (on the node):** Java works out from the variable names which argument goes where, so Math.pow(n, 2) and Math.pow(2, n) mean the same.
- **Correct rule (on the node):** Arguments are written in the order the method's signature lists them; for example, Math.pow(a, b) raises a to the bth power.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [3] misconception, exact rule:** wrong rule: Java works out from the variable names which argument goes where, so Math.pow(n, 2) and Math.pow(2, n) mean the same. Right rule: Arguments are matched to parameters by position, in the order the signature lists them; Math.pow(a, b) raises a to the bth power.

### ArrayHasLengthMethod

- **Edge:** `method_call` &rarr; `ArrayHasLengthMethod` (misconception)
- **Exact edge logic (the wrong rule):** you call length() instead of using the length field
- **Twin logic (the right rule):** An array's size is the field a.length, written without parentheses.
- **Wrong belief (on the node):** you call length() instead of using the length field
- **Correct rule (on the node):** An array's size is the field a.length, written without parentheses.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [6] misconception, exact rule:** wrong rule: You call length() instead of using the length field. Right rule: An array's size is the field a.length, written without parentheses (String has the method s.length()).
- **Edge `length_field` &rarr; `ArrayHasLengthMethod`, exact edge logic:** The size of an array is found by calling a.length(). **Twin logic:** An array's size is the field a.length, written without parentheses. (role: primary)

### EqualsComparesReferences

- **Edge:** `method_call` &rarr; `EqualsComparesReferences` (misconception)
- **Exact edge logic (the wrong rule):** .equals() compares references, not contents
- **Twin logic (the right rule):** s.equals(t) checks whether the two Strings contain the same characters.
- **Wrong belief (on the node):** .equals() compares references, not contents
- **Correct rule (on the node):** s.equals(t) checks whether the two Strings contain the same characters.
- **Provenance:** published
- **Role of this concept:** context
- **L0 way linked to it:** yes
- **L0 way [7] misconception, exact rule:** wrong rule: .equals() compares references, not contents. Right rule: s.equals(t) checks whether the two Strings contain the same characters.
- **Edge `comparison_operators` &rarr; `EqualsComparesReferences`, exact edge logic:** .equals() compares references, not contents **Twin logic:** s.equals(t) checks whether the two Strings contain the same characters. (role: context)
- **Edge `string_type` &rarr; `EqualsComparesReferences`, exact edge logic:** s.equals(t) checks whether s and t are the same object. **Twin logic:** s.equals(t) checks whether the two Strings contain the same characters. (role: primary)

### OutsideInMethodNesting

- **Edge:** `method_call` &rarr; `OutsideInMethodNesting` (misconception)
- **Exact edge logic (the wrong rule):** nested calls run outside-in, not arguments-first
- **Twin logic (the right rule):** In f(g(x)), g(x) is evaluated first and its result is passed to f.
- **Wrong belief (on the node):** nested calls run outside-in, not arguments-first
- **Correct rule (on the node):** In f(g(x)), g(x) is evaluated first and its result is passed to f.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [2] misconception, exact rule:** wrong rule: Nested calls run outside-in, not arguments-first. Right rule: In f(g(x)), g(x) is evaluated first and its result is passed to f.
- **Edge `expression` &rarr; `OutsideInMethodNesting`, exact edge logic:** In f(g(x)), f runs first and then g runs. **Twin logic:** In f(g(x)), g(x) is evaluated first and its result is passed to f. (role: context)

### ParameterTypesInCall

- **Edge:** `method_call` &rarr; `ParameterTypesInCall` (misconception)
- **Exact edge logic (the wrong rule):** A method call lists the parameter types, as in Math.pow(double a, double b).
- **Twin logic (the right rule):** A call passes only argument expressions, e.g. Math.pow(a, b); types appear only in the method declaration.
- **Wrong belief (on the node):** A method call lists the parameter types, as in Math.pow(double a, double b).
- **Correct rule (on the node):** A call passes only argument expressions, e.g. Math.pow(a, b); types appear only in the method declaration.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [4] misconception, exact rule:** wrong rule: A method call lists the parameter types, as in Math.pow(double a, double b). Right rule: A call passes only argument expressions, e.g. Math.pow(a, b); types appear only in the signature/declaration.

### ParenthesesOnlyIfArgument

- **Edge:** `method_call` &rarr; `ParenthesesOnlyIfArgument` (misconception)
- **Exact edge logic (the wrong rule):** () are optional on a no-argument call like println
- **Twin logic (the right rule):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Wrong belief (on the node):** () are optional on a no-argument call like println
- **Correct rule (on the node):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Provenance:** published
- **Role of this concept:** primary
- **L0 way linked to it:** yes
- **L0 way [1] misconception, exact rule:** wrong rule: () are optional on a no-argument call like println. Right rule: A method call always needs parentheses, so an empty line is printed with System.out.println(); and a random number is Math.random().
- **L0 way [5] inconsistent\_trace, exact rule:** Points to LT (arguments are evaluated left to right, then the method runs, then its return value replaces the call). Applied unevenly: in f(g(x)) the student calls the outer method before the inner one on some lines, or keeps the argument expression unevaluated in one trace step. (here mixing in: "() are optional on a no-argument call like println")
- **Edge `expression` &rarr; `ParenthesesOnlyIfArgument`, exact edge logic:** () are optional on a no-argument call like println **Twin logic:** A method call always needs parentheses, so an empty line is printed with System.out.println();. (role: context)
- **Edge `print` &rarr; `ParenthesesOnlyIfArgument`, exact edge logic:** println with nothing to print can be written System.out.println; without the parentheses. **Twin logic:** A method call always needs parentheses, so an empty line is printed with System.out.println();. (role: context)
- **Edge `println` &rarr; `ParenthesesOnlyIfArgument`, exact edge logic:** println with nothing to print can be written System.out.println; without the parentheses. **Twin logic:** A method call always needs parentheses, so an empty line is printed with System.out.println();. (role: context)

### StringMethodChangesString

- **Edge:** `method_call` &rarr; `StringMethodChangesString` (misconception)
- **Exact edge logic (the wrong rule):** name.toUpperCase(); changes name.
- **Twin logic (the right rule):** Strings are immutable: String methods return a new String, which must be assigned, e.g. name = name.toUpperCase();
- **Wrong belief (on the node):** name.toUpperCase(); changes name.
- **Correct rule (on the node):** Strings are immutable: String methods return a new String, which must be assigned, e.g. name = name.toUpperCase();
- **Provenance:** textbook
- **Role of this concept:** context
- **L0 way linked to it:** no
- **Edge `string_type` &rarr; `StringMethodChangesString`, exact edge logic:** name.toUpperCase(); changes name. **Twin logic:** Strings are immutable: String methods return a new String, which must be assigned, e.g. name = name.toUpperCase(); (role: primary)

## Errors (3)

An error edge states the rule that gets broken in a program, and the right rule.

### DiscardedReturnValue

- **Edge:** `method_call` &rarr; `DiscardedReturnValue` (error)
- **Exact edge logic (the wrong rule):** Writes Math.round(x); on its own line expecting x to be rounded.
- **Twin logic (the right rule):** Math.round(x) returns a value; that value has to be stored or used (e.g. long r = Math.round(x);), because the call on its own line does nothing with it.
- **Wrong belief (on the node):** Writes Math.round(x); on its own line expecting x to be rounded.
- **Correct rule (on the node):** Math.round(x) returns a value; that value has to be stored or used (e.g. long r = Math.round(x);), because the call on its own line does nothing with it.
- **Provenance:** published
- **Role of this concept:** primary
- **Edge `math_round` &rarr; `DiscardedReturnValue`, exact edge logic:** Writes Math.round(x); on its own line expecting x to be rounded. **Twin logic:** Math.round(x) returns a value; that value has to be stored or used (e.g. long r = Math.round(x);), because the call on its own line does nothing with it. (role: context)

### MathMethodWithoutClassName

- **Edge:** `method_call` &rarr; `MathMethodWithoutClassName` (error)
- **Exact edge logic (the wrong rule):** sqrt(x) calls the square-root method.
- **Twin logic (the right rule):** Library methods are called with the class name, e.g. Math.sqrt(x).
- **Wrong belief (on the node):** sqrt(x) calls the square-root method.
- **Correct rule (on the node):** Library methods are called with the class name, e.g. Math.sqrt(x).
- **Provenance:** published
- **Role of this concept:** primary
- **Edge `compile_time_error` &rarr; `MathMethodWithoutClassName`, exact edge logic:** sqrt(x) calls the square-root method. **Twin logic:** Library methods are called with the class name, e.g. Math.sqrt(x). (role: context)
- **Edge `math_library` &rarr; `MathMethodWithoutClassName`, exact edge logic:** sqrt(x) calls the square-root method. **Twin logic:** Library methods are called with the class name, e.g. Math.sqrt(x). (role: context)

### WrongArgumentType

- **Edge:** `method_call` &rarr; `WrongArgumentType` (error)
- **Exact edge logic (the wrong rule):** Calls a method with arguments of the wrong type, e.g. Math.sqrt("2").
- **Twin logic (the right rule):** Each argument must have the type the method's API lists.
- **Wrong belief (on the node):** Calls a method with arguments of the wrong type, e.g. Math.sqrt("2").
- **Correct rule (on the node):** Each argument must have the type the method's API lists.
- **Provenance:** published
- **Role of this concept:** primary
- **Edge `math_library` &rarr; `WrongArgumentType`, exact edge logic:** Calls a method with arguments of the wrong type, e.g. Math.sqrt("2"). **Twin logic:** Each argument must have the type the method's API lists. (role: context)

## Levels L0 to L4 (5 of 5)

Each level edge lists the ways a student shows that level, each with its exact rule.

### L0: Prestructural / sensorimotor

L0 for method call: the answer holds a rule that contradicts Java.

*Deciding question: Does every rule the answer applies to method call agree with the language rule? If it reads the code with everyday meanings, applies a wrong rule, or switches rules within one trace, it is L0. A slip in an otherwise rule-correct trace is L2 with an error, not L0.*

- **Edge:** `method_call` &rarr; `method_call@L0` (has_level)
- **Exact edge logic:** method call -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (8 ways).

Ways (8), each with its exact rule:

- **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: maths function notation f(x) or sqrt(x), where the name alone suffices, a constant needs no brackets, and the reader infers which argument is which from meaning. Java rule: a library method is called as ClassName.name(arguments) (Math.sqrt(x)), the parentheses are always required, and arguments are matched to parameters by position and type.
- **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ParenthesesOnlyIfArgument`: wrong rule: () are optional on a no-argument call like println. Right rule: A method call always needs parentheses, so an empty line is printed with System.out.println(); and a random number is Math.random().
- **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `OutsideInMethodNesting`: wrong rule: Nested calls run outside-in, not arguments-first. Right rule: In f(g(x)), g(x) is evaluated first and its result is passed to f.
- **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArgumentOrderInferred`: wrong rule: Java works out from the variable names which argument goes where, so Math.pow(n, 2) and Math.pow(2, n) mean the same. Right rule: Arguments are matched to parameters by position, in the order the signature lists them; Math.pow(a, b) raises a to the bth power.
- **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `ParameterTypesInCall`: wrong rule: A method call lists the parameter types, as in Math.pow(double a, double b). Right rule: A call passes only argument expressions, e.g. Math.pow(a, b); types appear only in the signature/declaration.
- **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ParenthesesOnlyIfArgument`: Points to LT (arguments are evaluated left to right, then the method runs, then its return value replaces the call). Applied unevenly: in f(g(x)) the student calls the outer method before the inner one on some lines, or keeps the argument expression unevaluated in one trace step. (here mixing in: "() are optional on a no-argument call like println")
- **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayHasLengthMethod`: wrong rule: You call length() instead of using the length field. Right rule: An array's size is the field a.length, written without parentheses (String has the method s.length()).
- **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `EqualsComparesReferences`: wrong rule: .equals() compares references, not contents. Right rule: s.equals(t) checks whether the two Strings contain the same characters.

### L1: Unistructural / atom x text surface

L1 for method call: the answer states one correct rule without applying it.

*Deciding question: Does the answer cover every part of the code, in order, with the values (L2)? If it covers one part or only states the rule, it is L1.*

- **Edge:** `method_call` &rarr; `method_call@L1` (has_level)
- **Exact edge logic:** method call -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).

Ways (2), each with its exact rule:

- **[0] names\_the\_element** (rule type N, identity rule): A method call is an expression that invokes a (library) method by its name, with arguments in parentheses, and evaluates to the value the method returns.
- **[1] states\_the\_rule** (rule type S, declarative rule): A library method is used by typing its (class-qualified) name followed by arguments of the specified types, in parentheses and separated by commas; the call can be used in expressions like a variable or literal; void methods return no value.

### L2: Multistructural / block x execution / preoperational

L2 for method call: the answer applies these rules to every part of the code, in order.

*Deciding question: Is the answer many segments mapped onto lines (L2), or one segment stating the purpose of the whole (L3)? A correct output with no value-by-value justification is not levelled.*

- **Edge:** `method_call` &rarr; `method_call@L2` (has_level)
- **Exact edge logic:** method call -&gt; L2 (Multistructural): the answer applies the rules of method call to every part of the code, in order (3 ways).

Ways (3), each with its exact rule:

- **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate the argument expressions from left to right (inner calls first), convert each to its parameter type if needed, transfer control to the method, and when it returns substitute the returned value for the call in the enclosing expression.
- **[1] output\_prediction** (rule type OP, evaluation / result rule): The call's value has the method's return type: Math.sqrt(5.0\*5.0 - 4.0\*4.0) is double 3.0, Math.round(3.14159) is long 3, Integer.parseInt("123") is int 123; a void method such as println has no value.
- **[2] one\_step\_execution** (rule type OS, state-transition rule): Calling a Math method changes none of the caller's variables (arguments are passed as values); the program's state changes only if the returned value is stored or used, e.g. double d = Math.sqrt(x);.

### L3: Relational / relations x function (concrete operational begins)

L3 for method call: the answer relates the parts by these rules.

*Deciding question: Was the purpose deduced from the code, or only guessed from traced input/output pairs (then L2)? Does the answer stay within the given code (L3), or reason about changed code, an error class or a new program (L4)?*

- **Edge:** `method_call` &rarr; `method_call@L3` (has_level)
- **Exact edge logic:** method call -&gt; L3 (Relational): the answer relates the parts (4 ways).

Ways (4), each with its exact rule:

- **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Arguments may be arbitrary expressions of the right type, and the call itself is an expression usable inside larger ones (Math.sin(x) \* Math.cos(y)).
- **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Math methods are called through the class name, Math.sqrt(x); without the prefix the compiler looks for the method in the current class and reports cannot find symbol.
- **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The call must match a signature in the API (name, number, order and types of arguments), and the API's return type tells how the value can be used.
- **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Delegates a computation to existing library code used as a black box, and composes computations by passing one call's result into another, e.g. Math.exp(Math.log(10.0)).

### L4: Extended abstract (concrete-operational reversibility and conservation)

L4 for method call: the answer reasons beyond the given code by these rules.

*Deciding question: Does the answer link the code to a broader context: a changed program, a class of inputs, an unseen problem? Re-tracing changed code value by value is L2; fixing one given failing case is L3.*

- **Edge:** `method_call` &rarr; `method_call@L4` (has_level)
- **Exact edge logic:** method call -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).

Ways (6), each with its exact rule:

- **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ParenthesesOnlyIfArgument`: Changing an argument changes only the returned value, never the argument variable; swapping arguments changes the meaning (Math.pow(2, n) vs Math.pow(n, 2)); replacing a call by its value keeps behaviour for mathematical functions but not for Math.random().
- **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Each argument must have (or automatically widen to) the type the method's API lists. Kind: compile-time. Trigger class: An argument whose type cannot be converted to the parameter type, e.g. Math.sqrt("2"), or the wrong number of arguments.
- **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A value-returning call does not change its argument; its result must be stored or used. Kind: silent logic error. Trigger class: A non-void call written as a statement on its own, e.g. Math.round(x); or Math.abs(d); expecting x or d to change.
- **[3] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Call a library method whenever a well-specified computation exists in an API (square roots, powers, conversions); write your own code only when no method fits; store a result in a variable rather than repeating an identical call.
- **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Library methods are called with the class name, e.g. Math.sqrt(x). Kind: compile-time. Trigger class: Calling sqrt(x), pow(a, b) etc. without the Math. prefix from another class (cannot find symbol).
- **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: A call needs parentheses and passes only argument expressions. Kind: compile-time. Trigger class: Omitting () on a call (Math.random) or writing parameter types in the call (Math.pow(double a, double b)).

## Same topic

`method_call` belongs to the topic **Library methods and APIs (Math)** (`topic1.2.g`). The topic also contains: `api`, `math_library`, `math_random`, `math_round`, `trig_functions`.

## Rules of the concept (23)

- **Book** (SW-1e, p. 30 (pdf 40)): "its name followed by arguments of the specified type, enclosed in parentheses and separated by commas"
- **Book** (SW-1.2, ): "You can call a method by typing its name followed by arguments,"
- **E** (folk-meaning rule): Folk meaning: maths function notation f(x) or sqrt(x), where the name alone suffices, a constant needs no brackets, and the reader infers which argument is which from meaning. Java rule: a library method is called as ClassName.name(arguments) (Math.sqrt(x)), the parentheses are always required, and arguments are matched to parameters by position and type.
- **M** (wrong rule / right rule): ArrayHasLengthMethod: wrong: You call length() instead of using the length field. \| right: An array's size is the field a.length, written without parentheses (String has the method s.length()).
- **M** (wrong rule / right rule): EqualsComparesReferences: wrong: .equals() compares references, not contents. \| right: s.equals(t) checks whether the two Strings contain the same characters.
- **M** (wrong rule / right rule): ParenthesesOnlyIfArgument: wrong: () are optional on a no-argument call like println. \| right: A method call always needs parentheses, so an empty line is printed with System.out.println(); and a random number is Math.random().
- **M** (wrong rule / right rule): OutsideInMethodNesting: wrong: Nested calls run outside-in, not arguments-first. \| right: In f(g(x)), g(x) is evaluated first and its result is passed to f.
- **M** (wrong rule / right rule): ArgumentOrderInferred: wrong: Java works out from the variable names which argument goes where, so Math.pow(n, 2) and Math.pow(2, n) mean the same. \| right: Arguments are matched to parameters by position, in the order the signature lists them; Math.pow(a, b) raises a to the bth power.
- **M** (wrong rule / right rule): ParameterTypesInCall: wrong: A method call lists the parameter types, as in Math.pow(double a, double b). \| right: A call passes only argument expressions, e.g. Math.pow(a, b); types appear only in the signature/declaration.
- **T** (uneven-application rule): Points to LT (arguments are evaluated left to right, then the method runs, then its return value replaces the call). Applied unevenly: in f(g(x)) the student calls the outer method before the inner one on some lines, or keeps the argument expression unevaluated in one trace step.
- **N** (identity rule): A method call is an expression that invokes a (library) method by its name, with arguments in parentheses, and evaluates to the value the method returns.
- **S** (declarative rule): A library method is used by typing its (class-qualified) name followed by arguments of the specified types, in parentheses and separated by commas; the call can be used in expressions like a variable or literal; void methods return no value.
- **LT** (operational sequencing rule): Evaluate the argument expressions from left to right (inner calls first), convert each to its parameter type if needed, transfer control to the method, and when it returns substitute the returned value for the call in the enclosing expression.
- **OP** (evaluation / result rule): The call's value has the method's return type: Math.sqrt(5.0\*5.0 - 4.0\*4.0) is double 3.0, Math.round(3.14159) is long 3, Integer.parseInt("123") is int 123; a void method such as println has no value.
- **OS** (state-transition rule): Calling a Math method changes none of the caller's variables (arguments are passed as values); the program's state changes only if the returned value is stored or used, e.g. double d = Math.sqrt(x);.
- **R** (composition rule (with a neighbour)): with expression: Arguments may be arbitrary expressions of the right type, and the call itself is an expression usable inside larger ones (Math.sin(x) \* Math.cos(y)).
- **R** (composition rule (with a neighbour)): with math\_library: Math methods are called through the class name, Math.sqrt(x); without the prefix the compiler looks for the method in the current class and reports cannot find symbol.
- **R** (composition rule (with a neighbour)): with api: The call must match a signature in the API (name, number, order and types of arguments), and the API's return type tells how the value can be used.
- **P** (plan / role rule): Delegates a computation to existing library code used as a black box, and composes computations by passing one call's result into another, e.g. Math.exp(Math.log(10.0)).
- **C** (conservation rule): Changing an argument changes only the returned value, never the argument variable; swapping arguments changes the meaning (Math.pow(2, n) vs Math.pow(n, 2)); replacing a call by its value keeps behaviour for mathematical functions but not for Math.random().
- **D** (error rule): rule broken: Library methods are called with the class name, e.g. Math.sqrt(x). (compile-time)
- **D** (error rule): rule broken: Each argument must have (or automatically widen to) the type the method's API lists. (compile-time)
- **D** (error rule): rule broken: A value-returning call does not change its argument; its result must be stored or used. (silent logic error)
- **D** (error rule): rule broken: A call needs parentheses and passes only argument expressions. (compile-time)
- **X** (applicability rule): Call a library method whenever a well-specified computation exists in an API (square roots, powers, conversions); write your own code only when no method fits; store a result in a variable rather than repeating an identical call.

## How it is found in code and answers (reader block)

- **Aliases:** method call, calls a method
- **Code patterns:** `\b(?!out\b)(?!System\b)(?!StdOut\b)[A-Za-z_]\w*\.[a-z]\w*\s*\(`, `(?:^|[=(,+\-*/\s])(?!if\b|for\b|while\b|switch\b|return\b|new\b)[a-z]\w*\s*\([^)]*\)(?=\s*[;)+\-*/,])`
- **Operator symbols:** none
- **Java types:** none

## The whole prerequisite chain

- **Everything it builds on (7):** `arithmetic_operators`, `data_type`, `expression`, `identifier`, `literal`, `primitive_type`, `variable`
- **Everything that builds on it (19):** `animation`, `api`, `coordinate_scaling`, `drawing_shapes`, `frequency_counting`, `function_plotting`, `math_library`, `math_random`, `math_round`, `monte_carlo_simulation`, `mouse_interaction`, `random_move`, `sampling_without_replacement`, `shuffle`, `simulation_loop`, `standard_audio`, `standard_drawing`, `trig_functions`, `two_models`

## Every edge in this view and its exact edge logic (36)

All the edges drawn in the picture, in the order: prerequisite, parallel, misconception, error, has_level, contains.

**1. `expression` &rarr; `method_call`** (prerequisite)

- **Exact edge logic:** Method arguments may be expressions, and a method call can be used in expressions in the same way as variables and literals.
- **Grounding:** book\_passage
- **Composition rule (R) of `expression` with `method_call`:** A method call is an expression usable wherever a value of its return type is, and its arguments are expressions evaluated before the call.
- **Composition rule (R) of `method_call` with `expression`:** Arguments may be arbitrary expressions of the right type, and the call itself is an expression usable inside larger ones (Math.sin(x) \* Math.cos(y)).

**2. `method_call` &rarr; `api`** (prerequisite)

- **Exact edge logic:** An API lists, for each library method, the signature you need in order to call it: name, argument types and return type.
- **Grounding:** book\_passage
- **Composition rule (R) of `method_call` with `api`:** The call must match a signature in the API (name, number, order and types of arguments), and the API's return type tells how the value can be used.
- **Composition rule (R) of `api` with `method_call`:** Each call must match one API signature: same name, arguments of the listed types in the listed order, and use of the value consistent with the return type.

**3. `method_call` &rarr; `math_library`** (prerequisite)

- **Exact edge logic:** Math.sqrt(x) and other Math methods are used through method calls.
- **Grounding:** book\_passage
- **Composition rule (R) of `method_call` with `math_library`:** Math methods are called through the class name, Math.sqrt(x); without the prefix the compiler looks for the method in the current class and reports cannot find symbol.
- **Composition rule (R) of `math_library` with `method_call`:** Every Math facility is used through a method call with the Math. prefix and parentheses (the constants Math.PI and Math.E are written without parentheses).

**4. `method_call` &rarr; `ArgumentOrderInferred`** (misconception)

- **Exact edge logic (the wrong rule):** Java works out from the variable names which argument goes where, so Math.pow(n, 2) and Math.pow(2, n) mean the same.
- **Twin logic (the right rule):** Arguments are written in the order the method's signature lists them; for example, Math.pow(a, b) raises a to the bth power.
- **Role:** primary

**5. `method_call` &rarr; `ArrayHasLengthMethod`** (misconception)

- **Exact edge logic (the wrong rule):** you call length() instead of using the length field
- **Twin logic (the right rule):** An array's size is the field a.length, written without parentheses.
- **Role:** context

**6. `method_call` &rarr; `EqualsComparesReferences`** (misconception)

- **Exact edge logic (the wrong rule):** .equals() compares references, not contents
- **Twin logic (the right rule):** s.equals(t) checks whether the two Strings contain the same characters.
- **Role:** context

**7. `method_call` &rarr; `OutsideInMethodNesting`** (misconception)

- **Exact edge logic (the wrong rule):** nested calls run outside-in, not arguments-first
- **Twin logic (the right rule):** In f(g(x)), g(x) is evaluated first and its result is passed to f.
- **Role:** primary

**8. `method_call` &rarr; `ParameterTypesInCall`** (misconception)

- **Exact edge logic (the wrong rule):** A method call lists the parameter types, as in Math.pow(double a, double b).
- **Twin logic (the right rule):** A call passes only argument expressions, e.g. Math.pow(a, b); types appear only in the method declaration.
- **Role:** primary

**9. `method_call` &rarr; `ParenthesesOnlyIfArgument`** (misconception)

- **Exact edge logic (the wrong rule):** () are optional on a no-argument call like println
- **Twin logic (the right rule):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Role:** primary

**10. `method_call` &rarr; `StringMethodChangesString`** (misconception)

- **Exact edge logic (the wrong rule):** name.toUpperCase(); changes name.
- **Twin logic (the right rule):** Strings are immutable: String methods return a new String, which must be assigned, e.g. name = name.toUpperCase();
- **Role:** context

**11. `comparison_operators` &rarr; `EqualsComparesReferences`** (misconception)

- **Exact edge logic (the wrong rule):** .equals() compares references, not contents
- **Twin logic (the right rule):** s.equals(t) checks whether the two Strings contain the same characters.
- **Role:** context

**12. `expression` &rarr; `OutsideInMethodNesting`** (misconception)

- **Exact edge logic (the wrong rule):** In f(g(x)), f runs first and then g runs.
- **Twin logic (the right rule):** In f(g(x)), g(x) is evaluated first and its result is passed to f.
- **Role:** context

**13. `expression` &rarr; `ParenthesesOnlyIfArgument`** (misconception)

- **Exact edge logic (the wrong rule):** () are optional on a no-argument call like println
- **Twin logic (the right rule):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Role:** context

**14. `length_field` &rarr; `ArrayHasLengthMethod`** (misconception)

- **Exact edge logic (the wrong rule):** The size of an array is found by calling a.length().
- **Twin logic (the right rule):** An array's size is the field a.length, written without parentheses.
- **Role:** primary

**15. `print` &rarr; `ParenthesesOnlyIfArgument`** (misconception)

- **Exact edge logic (the wrong rule):** println with nothing to print can be written System.out.println; without the parentheses.
- **Twin logic (the right rule):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Role:** context

**16. `println` &rarr; `ParenthesesOnlyIfArgument`** (misconception)

- **Exact edge logic (the wrong rule):** println with nothing to print can be written System.out.println; without the parentheses.
- **Twin logic (the right rule):** A method call always needs parentheses, so an empty line is printed with System.out.println();.
- **Role:** context

**17. `string_type` &rarr; `EqualsComparesReferences`** (misconception)

- **Exact edge logic (the wrong rule):** s.equals(t) checks whether s and t are the same object.
- **Twin logic (the right rule):** s.equals(t) checks whether the two Strings contain the same characters.
- **Role:** primary

**18. `string_type` &rarr; `StringMethodChangesString`** (misconception)

- **Exact edge logic (the wrong rule):** name.toUpperCase(); changes name.
- **Twin logic (the right rule):** Strings are immutable: String methods return a new String, which must be assigned, e.g. name = name.toUpperCase();
- **Role:** primary

**19. `method_call` &rarr; `DiscardedReturnValue`** (error)

- **Exact edge logic (the wrong rule):** Writes Math.round(x); on its own line expecting x to be rounded.
- **Twin logic (the right rule):** Math.round(x) returns a value; that value has to be stored or used (e.g. long r = Math.round(x);), because the call on its own line does nothing with it.
- **Role:** primary

**20. `method_call` &rarr; `MathMethodWithoutClassName`** (error)

- **Exact edge logic (the wrong rule):** sqrt(x) calls the square-root method.
- **Twin logic (the right rule):** Library methods are called with the class name, e.g. Math.sqrt(x).
- **Role:** primary

**21. `method_call` &rarr; `WrongArgumentType`** (error)

- **Exact edge logic (the wrong rule):** Calls a method with arguments of the wrong type, e.g. Math.sqrt("2").
- **Twin logic (the right rule):** Each argument must have the type the method's API lists.
- **Role:** primary

**22. `compile_time_error` &rarr; `MathMethodWithoutClassName`** (error)

- **Exact edge logic (the wrong rule):** sqrt(x) calls the square-root method.
- **Twin logic (the right rule):** Library methods are called with the class name, e.g. Math.sqrt(x).
- **Role:** context

**23. `math_library` &rarr; `MathMethodWithoutClassName`** (error)

- **Exact edge logic (the wrong rule):** sqrt(x) calls the square-root method.
- **Twin logic (the right rule):** Library methods are called with the class name, e.g. Math.sqrt(x).
- **Role:** context

**24. `math_library` &rarr; `WrongArgumentType`** (error)

- **Exact edge logic (the wrong rule):** Calls a method with arguments of the wrong type, e.g. Math.sqrt("2").
- **Twin logic (the right rule):** Each argument must have the type the method's API lists.
- **Role:** context

**25. `math_round` &rarr; `DiscardedReturnValue`** (error)

- **Exact edge logic (the wrong rule):** Writes Math.round(x); on its own line expecting x to be rounded.
- **Twin logic (the right rule):** Math.round(x) returns a value; that value has to be stored or used (e.g. long r = Math.round(x);), because the call on its own line does nothing with it.
- **Role:** context

**26. `method_call` &rarr; `method_call@L0`** (has_level)

- **Exact edge logic:** method call -&gt; L0 (Prestructural): the answer holds a rule that contradicts Java (8 ways).
  - **[0] everyday\_reading** (rule type E, folk-meaning rule): Folk meaning: maths function notation f(x) or sqrt(x), where the name alone suffices, a constant needs no brackets, and the reader infers which argument is which from meaning. Java rule: a library method is called as ClassName.name(arguments) (Math.sqrt(x)), the parentheses are always required, and arguments are matched to parameters by position and type.
  - **[1] misconception** (rule type M, wrong rule / right rule) &rarr; `ParenthesesOnlyIfArgument`: wrong rule: () are optional on a no-argument call like println. Right rule: A method call always needs parentheses, so an empty line is printed with System.out.println(); and a random number is Math.random().
  - **[2] misconception** (rule type M, wrong rule / right rule) &rarr; `OutsideInMethodNesting`: wrong rule: Nested calls run outside-in, not arguments-first. Right rule: In f(g(x)), g(x) is evaluated first and its result is passed to f.
  - **[3] misconception** (rule type M, wrong rule / right rule) &rarr; `ArgumentOrderInferred`: wrong rule: Java works out from the variable names which argument goes where, so Math.pow(n, 2) and Math.pow(2, n) mean the same. Right rule: Arguments are matched to parameters by position, in the order the signature lists them; Math.pow(a, b) raises a to the bth power.
  - **[4] misconception** (rule type M, wrong rule / right rule) &rarr; `ParameterTypesInCall`: wrong rule: A method call lists the parameter types, as in Math.pow(double a, double b). Right rule: A call passes only argument expressions, e.g. Math.pow(a, b); types appear only in the signature/declaration.
  - **[5] inconsistent\_trace** (rule type T, uneven-application rule) &rarr; `ParenthesesOnlyIfArgument`: Points to LT (arguments are evaluated left to right, then the method runs, then its return value replaces the call). Applied unevenly: in f(g(x)) the student calls the outer method before the inner one on some lines, or keeps the argument expression unevaluated in one trace step. (here mixing in: "() are optional on a no-argument call like println")
  - **[6] misconception** (rule type M, wrong rule / right rule) &rarr; `ArrayHasLengthMethod`: wrong rule: You call length() instead of using the length field. Right rule: An array's size is the field a.length, written without parentheses (String has the method s.length()).
  - **[7] misconception** (rule type M, wrong rule / right rule) &rarr; `EqualsComparesReferences`: wrong rule: .equals() compares references, not contents. Right rule: s.equals(t) checks whether the two Strings contain the same characters.

**27. `method_call` &rarr; `method_call@L1`** (has_level)

- **Exact edge logic:** method call -&gt; L1 (Unistructural): the answer states one correct rule without applying it (2 ways).
  - **[0] names\_the\_element** (rule type N, identity rule): A method call is an expression that invokes a (library) method by its name, with arguments in parentheses, and evaluates to the value the method returns.
  - **[1] states\_the\_rule** (rule type S, declarative rule): A library method is used by typing its (class-qualified) name followed by arguments of the specified types, in parentheses and separated by commas; the call can be used in expressions like a variable or literal; void methods return no value.

**28. `method_call` &rarr; `method_call@L2`** (has_level)

- **Exact edge logic:** method call -&gt; L2 (Multistructural): the answer applies the rules of method call to every part of the code, in order (3 ways).
  - **[0] line\_by\_line\_trace** (rule type LT, operational sequencing rule): Evaluate the argument expressions from left to right (inner calls first), convert each to its parameter type if needed, transfer control to the method, and when it returns substitute the returned value for the call in the enclosing expression.
  - **[1] output\_prediction** (rule type OP, evaluation / result rule): The call's value has the method's return type: Math.sqrt(5.0\*5.0 - 4.0\*4.0) is double 3.0, Math.round(3.14159) is long 3, Integer.parseInt("123") is int 123; a void method such as println has no value.
  - **[2] one\_step\_execution** (rule type OS, state-transition rule): Calling a Math method changes none of the caller's variables (arguments are passed as values); the program's state changes only if the returned value is stored or used, e.g. double d = Math.sqrt(x);.

**29. `method_call` &rarr; `method_call@L3`** (has_level)

- **Exact edge logic:** method call -&gt; L3 (Relational): the answer relates the parts (4 ways).
  - **[0] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Arguments may be arbitrary expressions of the right type, and the call itself is an expression usable inside larger ones (Math.sin(x) \* Math.cos(y)).
  - **[1] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): Math methods are called through the class name, Math.sqrt(x); without the prefix the compiler looks for the method in the current class and reports cannot find symbol.
  - **[2] relation\_to\_neighbour** (rule type R, composition rule (with a neighbour)): The call must match a signature in the API (name, number, order and types of arguments), and the API's return type tells how the value can be used.
  - **[3] purpose\_of\_the\_whole** (rule type P, plan / role rule): Delegates a computation to existing library code used as a black box, and composes computations by passing one call's result into another, e.g. Math.exp(Math.log(10.0)).

**30. `method_call` &rarr; `method_call@L4`** (has_level)

- **Exact edge logic:** method call -&gt; L4 (Extended abstract): the answer reasons beyond the given code (6 ways).
  - **[0] predict\_a\_change** (rule type C, conservation rule) &rarr; `ParenthesesOnlyIfArgument`: Changing an argument changes only the returned value, never the argument variable; swapping arguments changes the meaning (Math.pow(2, n) vs Math.pow(n, 2)); replacing a call by its value keeps behaviour for mathematical functions but not for Math.random().
  - **[1] diagnose\_an\_error** (rule type D, error rule): rule broken: Each argument must have (or automatically widen to) the type the method's API lists. Kind: compile-time. Trigger class: An argument whose type cannot be converted to the parameter type, e.g. Math.sqrt("2"), or the wrong number of arguments.
  - **[2] diagnose\_an\_error** (rule type D, error rule): rule broken: A value-returning call does not change its argument; its result must be stored or used. Kind: silent logic error. Trigger class: A non-void call written as a statement on its own, e.g. Math.round(x); or Math.abs(d); expecting x or d to change.
  - **[3] transfer\_to\_a\_new\_program** (rule type X, applicability rule): Call a library method whenever a well-specified computation exists in an API (square roots, powers, conversions); write your own code only when no method fits; store a result in a variable rather than repeating an identical call.
  - **[4] diagnose\_an\_error** (rule type D, error rule): rule broken: Library methods are called with the class name, e.g. Math.sqrt(x). Kind: compile-time. Trigger class: Calling sqrt(x), pow(a, b) etc. without the Math. prefix from another class (cannot find symbol).
  - **[5] diagnose\_an\_error** (rule type D, error rule): rule broken: A call needs parentheses and passes only argument expressions. Kind: compile-time. Trigger class: Omitting () on a call (Math.random) or writing parameter types in the call (Math.pow(double a, double b)).

**31. `topic1.2.g` &rarr; `method_call`** (contains)

- topic `topic1.2.g` contains `method_call`

**32. `topic1.2.g` &rarr; `api`** (contains)

- topic `topic1.2.g` contains `api`

**33. `topic1.2.g` &rarr; `math_library`** (contains)

- topic `topic1.2.g` contains `math_library`

**34. `topic1.2.g` &rarr; `math_random`** (contains)

- topic `topic1.2.g` contains `math_random`

**35. `topic1.2.g` &rarr; `math_round`** (contains)

- topic `topic1.2.g` contains `math_round`

**36. `topic1.2.g` &rarr; `trig_functions`** (contains)

- topic `topic1.2.g` contains `trig_functions`
