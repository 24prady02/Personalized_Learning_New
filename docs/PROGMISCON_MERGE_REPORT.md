# ProgMiscon → CPAL catalogue merge report

- ProgMiscon snapshot: 2026-04-14T15:48:03.718Z
- Java entries considered: 55 (public only)
- Enriched existing wrong models: **29**
- Pushed to progmiscon_only (no room in main): **5**
- New concepts created: **6** (recursion, method_chaining, this_semantics, access_modifiers, numeric_literals, object_instantiation)
- Unmapped ProgMiscon entries (consider adding mappings): **0**

## Per-concept enrichment table

| ProgMiscon ID | → concept | wm slot | refutation snippet |
|---|---|---|---|
| `ArithmeticPlusPrecedes` | `type_mismatch` | `TM-A` | Addition and string concatenation have same precedence |
| `ArrayHasLengthMethod` | `array_index` | `AI-A` | To get the length of an array, one needs to read its length field |
| `ArrayListIsArray` | `array_index` | `AI-B` | ArrayLists and arrays are different things |
| `ArraysGrow` | `array_not_allocated` | `ANA-A` | The length of an array is fixed and is determined at allocation |
| `AssignCompares` | `assignment_vs_compare` | `AC-A` | = assigns a value to a variable |
| `AssignmentCopiesObject` | `null_pointer` | `NP-A` | Assignment copies the reference pointing to the object |
| `AssignmentNotExpression` | `assignment_vs_compare` | `AC-B` | An assignment a=b is an expression and thus produces a value |
| `ComparisonWithBooleanLiteral` | `boolean_operators` | `BO-A` | To test whether an expression is true or false, one can just use it |
| `ConditionalIsSequence` | `boolean_operators` | `BO-B` | If-else can behave differently from sequence of two ifs |
| `ConstructorAllocates` | `no_default_constructor` | `NDC-A` | The constructor does not allocate the object, it just initializes it |
| `ConstructorReturnsObject` | `no_default_constructor` | `NDC-B` | Constructors cannot return anything |
| `DeferredReturn` | `missing_return` | `MR-A` | A return statement immediately returns from the method |
| `EqualityOperatorComparesObjectsValues` | `string_equality` | `SE-A` | o==p compares the references stored in the variables o and p |
| `EqualsComparesReferences` | `string_equality` | `SE-B` | o.equals(p) compares the objects referred to by variables o and p |
| `FinalReferenceImpliesImmutability` | `string_immutability` | `SI-A` | An object referred to by a final variable can be a mutable object |
| `IfIsLoop` | `boolean_operators` | `BO-C` | The body of an if statement executes at most once |
| `LocalVariablesAutoInitialized` | `variable_scope` | `VS-A` | Local variables must be initialized explicitly |
| `MustInitializeFieldInConstructor` | `no_default_constructor` | `NDC-C` | Constructors do not need to assign values to all fields |
| `NullIsObject` | `null_pointer` | `NP-B` | null is a reference pointing to no object |
| `PrivateFromOtherInstance` | `static_vs_instance` | `SVI-A` | An object can access private members of all other objects of the same class |
| `PrivateFromStatic` | `static_vs_instance` | `SVI-B` | Static methods can access private members of instances of same class |
| `ReturnCall` | `missing_return` | `MR-B` | Return statements do not need () around the return value |
| `ReturnUnwindsMultipleFrames` | `missing_return` | `MR-C` | A return statement pops exactly one call stack frame |
| `ReferenceToVariable` | `variable_scope` | `VS-B` | References can only point to heap objects |
| `StringLiteralNoObject` | `string_equality` | `SE-C` | A String literal represents a String object and can be treated as such |
| `StringPlusStringifiesExpression` | `type_mismatch` | `TM-B` | String concatenation evaluates non-String operand expressions and casts value to |
| `ThisExistsInStaticMethod` | `static_vs_instance` | `SVI-C` | this does not exist in static methods |
| `VariablesHoldExpressions` | `assignment_vs_compare` | `AC-C` | = evaluates an expression and stores its value in a variable |
| `VariablesHoldObjects` | `null_pointer` | `NP-C` | A variable of a reference type contains a reference to an object |

## Pushed to `progmiscon_only` (concept's main slots full)

| ProgMiscon ID | → concept |
|---|---|
| `MapToBooleanWithConditionalOperator` | `boolean_operators` |
| `MapToBooleanWithIf` | `boolean_operators` |
| `NoEmptyConstructor` | `no_default_constructor` |
| `NoShortCircuit` | `boolean_operators` |
| `NoSingleLogicAnd` | `boolean_operators` |

## New concepts seeded (rubric_status=draft_needs_review)

### `recursion` (3 PM entries)
- `RecursiveActivationsShareFrame`: Recursive calls of a method share a stack frame
- `RecursiveMethodImpliesRecursiveType`: A class with a recursive method represents part of a recursive data structure
- `RecursiveMethodNeedsIfElse`: A recursive method needs to contain an if-else statement

  - **L1**: Recognises that a method calling itself is 'recursion' but can't predict what happens at runtime.
  - **L2**: Names the rule that every recursive method needs a base case or it will infinitely recurse.
  - **L3**: Traces a small recursive call by hand, showing each activation has its own local variables / parameters on the call stack, and that returns unwind one frame at a time.
  - **L4**: Generalises to mutual recursion, tail-call optimisation (JVM doesn't do it), and the relationship between recursion depth and StackOverflowError.

### `method_chaining` (5 PM entries)
- `CannotChainMemberAccesses`: Member accesses cannot be chained together
- `CannotChainMemberToConstructor`: Method calls or field accesses cannot be chained to a constructor invocation
- `OutsideInMethodNesting`: Nested method calls are invoked outside in
- `RightToLeftChaining`: Chained accesses are invoked from right to left
- `ParenthesesOnlyIfArgument`: () are optional for method calls without arguments

  - **L1**: Recognises a.foo().bar() syntactically as 'a dot foo dot bar'.
  - **L2**: Names that chained calls happen left-to-right and that the return type of foo() determines what bar() can be.
  - **L3**: Traces a chain step-by-step, showing the intermediate receiver objects/values and what would happen if any step returns null or the wrong type.
  - **L4**: Generalises to fluent interfaces, builder pattern, and when chaining hurts readability vs helps it.

### `this_semantics` (3 PM entries)
- `ThisAssignable`: One can assign to this
- `ThisCanBeNull`: this can be null
- `ThisNoExpression`: The name this is not an expression

  - **L1**: Recognises `this` as 'the current object' but uses it interchangeably with the variable name.
  - **L2**: Names the rule that `this` is implicit and refers to the object the method was called on.
  - **L3**: Explains why `this = something` is a compile error (implicit final), why `this` is unavailable in static methods (no instance), and how `this.field` disambiguates field from local.
  - **L4**: Generalises to qualified `this` in inner classes (Outer.this), `this(...)` constructor delegation, and the JLS guarantee that `this` is non-null in normal instance contexts.

### `access_modifiers` (1 PM entries)
- `ControlledLocalAccess`: One can control access to local variables using access modifiers

  - **L1**: Knows the words public/private but treats them as labels.
  - **L2**: Names the four levels and which is the default; knows private can't be reached from outside the class.
  - **L3**: Explains the package vs subclass distinction for protected, and why local variables can't be modified with public/private (scope is already the smallest possible).
  - **L4**: Generalises to module system (Java 9+), reflection-based access, and the difference between compile-time and runtime access checks.

### `numeric_literals` (4 PM entries)
- `LargeIntegerLong`: Large integer numbers have type long
- `NoFloatLiterals`: There are no float literals
- `NoLongLiterals`: There are no long literals
- `CharNotNumeric`: Char is not a numeric type

  - **L1**: Writes numbers without thinking about type; surprised when 3000000000 doesn't compile.
  - **L2**: Names the rule that int literals max out at ~2.1 billion and that L makes it long; that 3.14 is double; that 3.14f is float; that 'A' is a char (integer 65), not a String.
  - **L3**: Explains the implicit widening conversions and why (double)5/2 differs from 5/2; the exact-vs-approximation distinction between long and double.
  - **L4**: Generalises to underscores in literals (Java 7+), binary/hex/oct prefixes, and the IEEE 754 reasons for double vs float precision differences.

### `object_instantiation` (5 PM entries)
- `ObjectsMustBeNamed`: A variable is needed to instantiate an object
- `AddMemberAtRuntime`: Set of class members can change at runtime
- `CallNotStaticallyChecked`: A method invocation on a reference of a type that does not have that method won't compile
- `NoReservedWords`: Every sequence of letters and digits starting with a letter can be used as an identifier
- `NoAtomicExpression`: Expressions must consist of more than one piece

  - **L1**: Knows `new Foo()` makes a Foo but can't say what the expression evaluates to or where the object lives.
  - **L2**: Names that `new` returns a reference, that the constructor runs once, and that you usually store the reference in a variable.
  - **L3**: Explains heap allocation, that `new Foo()` is an expression (can be used inline as an argument), why you can't add new fields at runtime, and why method calls are statically checked.
  - **L4**: Generalises to anonymous inner classes, lambda vs object instantiation, escape analysis (JVM optimisation), and why dynamic-language idioms (monkey patching, duck typing) don't translate.
