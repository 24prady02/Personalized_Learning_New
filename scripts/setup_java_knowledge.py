"""
setup_java_knowledge.py
=======================
Fix 9+10: Populates the Pedagogical KG with Java CSCI 1301 specific data
for all 20 concepts. Run this ONCE before starting the system.

Replaces the four Python-oriented default misconceptions/progressions with
real Java curriculum content grounded in your 20-concept bank.

Usage:
    python scripts/setup_java_knowledge.py
"""

import json
from pathlib import Path

DATA_DIR = Path("data/pedagogical_kg")
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ─── 20 Java Concept Misconceptions ──────────────────────────────────────────
JAVA_MISCONCEPTIONS = [
    {
        "id": "mc_type_mismatch",
        "concept": "type_mismatch",
        "week": 1,
        "error_type": "compile",
        "description": "Student believes int + String concatenation auto-converts the int",
        "common_indicators": [
            "can't you just add them", "int becomes string", "converts automatically",
            "why doesn't + work", "type mismatch"
        ],
        "l1_pattern": "just use + to join them",
        "l2_pattern": "you need to convert somehow",
        "l3_pattern": "Java doesn't automatically cast int to String, you need String.valueOf or casting",
        "l4_pattern": "Java is strongly typed — the + operator is overloaded for String but requires one operand to already be a String; int is a primitive with no implicit toString",
        "severity": "high",
        "frequency": 0.75,
        "correction_strategy": "Show String.valueOf(n) and explicit casting; contrast with Python"
    },
    {
        "id": "mc_infinite_loop",
        "concept": "infinite_loop",
        "week": 1,
        "error_type": "logic",
        "description": "Student forgets to update loop variable, causing infinite loop",
        "common_indicators": [
            "never stops", "hangs", "freezes", "loop variable", "increment", "update"
        ],
        "l1_pattern": "the loop just keeps going",
        "l2_pattern": "something in the loop isn't changing",
        "l3_pattern": "the loop variable is never incremented so the condition stays true forever",
        "l4_pattern": "loop termination requires the loop variable to progress toward making the boolean condition false; without i++ the condition i < n never becomes false",
        "severity": "high",
        "frequency": 0.70,
        "correction_strategy": "Trace through loop by hand; show i++ in the update clause"
    },
    {
        "id": "mc_null_pointer",
        "concept": "null_pointer",
        "week": 2,
        "error_type": "runtime",
        "description": "Student declares a reference variable but never instantiates the object",
        "common_indicators": [
            "NullPointerException", "NPE", "null", "not initialized", "reference"
        ],
        "l1_pattern": "I declared it but it doesn't work",
        "l2_pattern": "something about the object not being created",
        "l3_pattern": "the variable holds null because new was never called; calling a method on null throws NPE",
        "l4_pattern": "in Java, declaring a reference variable (String s) gives you a reference slot initialized to null; the object only exists on the heap after new; invoking any method on a null reference causes NullPointerException at runtime",
        "severity": "critical",
        "frequency": 0.85,
        "correction_strategy": "Show reference vs object with memory diagram; always initialize with new"
    },
    {
        "id": "mc_string_equality",
        "concept": "string_equality",
        "week": 2,
        "error_type": "logic",
        "description": "Student uses == to compare String content instead of .equals()",
        "common_indicators": [
            "== doesn't work", "use equals", "same string", "comparison", "reference"
        ],
        "l1_pattern": "I think == doesn't work on Strings",
        "l2_pattern": "== compares something different for Strings",
        "l3_pattern": "== compares object references not content; .equals() checks the character sequence",
        "l4_pattern": "== performs reference comparison via memory addresses; two String literals may be interned to the same object but new String() always creates a new heap object; .equals() overrides Object.equals to compare character-by-character content",
        "severity": "critical",
        "frequency": 0.90,
        "correction_strategy": "Memory diagram showing two String objects; == vs .equals() side by side"
    },
    {
        "id": "mc_variable_scope",
        "concept": "variable_scope",
        "week": 2,
        "error_type": "compile",
        "description": "Student tries to use a variable outside the block where it was declared",
        "common_indicators": [
            "cannot find symbol", "not defined", "scope", "local", "block", "braces"
        ],
        "l1_pattern": "I defined it so it should work",
        "l2_pattern": "the variable isn't accessible outside where I put it",
        "l3_pattern": "variables in Java are scoped to the block they are declared in; outside the braces they no longer exist",
        "l4_pattern": "Java uses lexical block scoping; a variable declared inside {} only exists on the stack frame for that block; once the closing brace is reached the variable is out of scope and any reference to it is a compile-time cannot-find-symbol error",
        "severity": "high",
        "frequency": 0.65,
        "correction_strategy": "Highlight the braces; show variable declared before the block"
    },
    {
        "id": "mc_assignment_vs_compare",
        "concept": "assignment_vs_compare",
        "week": 2,
        "error_type": "compile",
        "description": "Student uses = (assignment) where == (comparison) is needed in a condition",
        "common_indicators": [
            "= vs ==", "assign in if", "condition", "always true", "incompatible types"
        ],
        "l1_pattern": "I used = to check",
        "l2_pattern": "= and == do different things in a condition",
        "l3_pattern": "= assigns a value and returns it; in Java a non-boolean result in an if condition is a compile error",
        "l4_pattern": "= is the assignment operator and evaluates to the assigned value; Java's if requires a boolean expression; assigning an int produces an int not a boolean causing incompatible types at compile time",
        "severity": "medium",
        "frequency": 0.60,
        "correction_strategy": "Show the compiler error; contrast with C where this silently passes"
    },
    {
        "id": "mc_integer_division",
        "concept": "integer_division",
        "week": 2,
        "error_type": "logic",
        "description": "Student expects decimal result from int / int but gets truncated integer",
        "common_indicators": [
            "division", "wrong answer", "truncates", "decimal", "cast", "double"
        ],
        "l1_pattern": "the division gives the wrong number",
        "l2_pattern": "int division cuts off the decimal part",
        "l3_pattern": "when both operands are int, Java performs integer division and discards the remainder",
        "l4_pattern": "Java's / operator performs integer division when both operands are int type; the fractional part is truncated not rounded; to get a double result at least one operand must be cast to double or declared as double",
        "severity": "medium",
        "frequency": 0.70,
        "correction_strategy": "Show (double) cast; contrast 5/2=2 vs 5.0/2=2.5"
    },
    {
        "id": "mc_scanner_buffer",
        "concept": "scanner_buffer",
        "week": 2,
        "error_type": "logic",
        "description": "Student mixes nextInt() with nextLine() causing the newline to be consumed unexpectedly",
        "common_indicators": [
            "nextLine", "nextInt", "skips", "empty string", "buffer", "newline"
        ],
        "l1_pattern": "nextLine skips my input",
        "l2_pattern": "something about the newline being left in the buffer",
        "l3_pattern": "nextInt() reads the number but leaves the newline in the buffer; the next nextLine() consumes that newline and returns empty string",
        "l4_pattern": "nextInt() consumes only the integer token, leaving the newline character \\n in the input stream; the subsequent nextLine() call reads until the next \\n and immediately returns an empty string because the newline is already there; fix by calling nextLine() to consume the leftover newline before reading the next string",
        "severity": "high",
        "frequency": 0.75,
        "correction_strategy": "Add extra sc.nextLine() after nextInt(); or use Integer.parseInt(sc.nextLine())"
    },
    {
        "id": "mc_array_index",
        "concept": "array_index",
        "week": 3,
        "error_type": "runtime",
        "description": "Student uses 1-based indexing or accesses index equal to array length",
        "common_indicators": [
            "ArrayIndexOutOfBounds", "index", "length", "off by one", "zero"
        ],
        "l1_pattern": "the index is out of bounds",
        "l2_pattern": "arrays start at 0 so the last index is different from the length",
        "l3_pattern": "valid indices are 0 to length-1; accessing arr[arr.length] throws ArrayIndexOutOfBoundsException",
        "l4_pattern": "Java arrays are zero-indexed; for an array of length n the valid indices are 0 through n-1; index n does not exist; the JVM throws ArrayIndexOutOfBoundsException at runtime with the offending index in the message",
        "severity": "high",
        "frequency": 0.80,
        "correction_strategy": "Use arr.length-1 as upper bound; trace through with small array"
    },
    {
        "id": "mc_missing_return",
        "concept": "missing_return",
        "week": 3,
        "error_type": "compile",
        "description": "Student forgets return statement on one branch of control flow",
        "common_indicators": [
            "missing return", "not all paths", "return statement", "void", "method"
        ],
        "l1_pattern": "I have a return but it still complains",
        "l2_pattern": "not all branches have a return",
        "l3_pattern": "Java requires every code path in a non-void method to return a value; if the compiler sees a branch that could exit without returning it gives missing return",
        "l4_pattern": "Java performs static control-flow analysis at compile time; every possible execution path through a non-void method must end with a return statement; an if without else, or a return only inside one branch, leaves an implicit fall-through path with no return value which is a compile-time error",
        "severity": "medium",
        "frequency": 0.65,
        "correction_strategy": "Add else return or a final return after the if block"
    },
    {
        "id": "mc_array_not_allocated",
        "concept": "array_not_allocated",
        "week": 3,
        "error_type": "runtime",
        "description": "Student declares array variable but forgets to allocate with new",
        "common_indicators": [
            "new", "array", "null", "not initialized", "allocate", "[]"
        ],
        "l1_pattern": "I declared the array but it's null",
        "l2_pattern": "the array needs to be created with new",
        "l3_pattern": "int[] arr just creates a reference initialized to null; you need arr = new int[size] to allocate the actual array on the heap",
        "l4_pattern": "declaring int[] arr creates a reference variable on the stack holding null; no array object exists yet; new int[n] allocates n contiguous int slots on the heap and returns a reference to the first slot; without new any attempt to access arr[i] dereferences null and throws NullPointerException",
        "severity": "high",
        "frequency": 0.70,
        "correction_strategy": "Memory diagram: stack has reference, heap has array; always new"
    },
    {
        "id": "mc_boolean_operators",
        "concept": "boolean_operators",
        "week": 3,
        "error_type": "logic",
        "description": "Student confuses && (AND) with || (OR) in conditions",
        "common_indicators": [
            "AND", "OR", "&&", "||", "both conditions", "either condition", "logic"
        ],
        "l1_pattern": "the condition doesn't work right",
        "l2_pattern": "AND and OR do different things",
        "l3_pattern": "&& requires both conditions to be true; || requires at least one to be true",
        "l4_pattern": "&& is short-circuit AND: evaluates left, if false stops and returns false; || is short-circuit OR: evaluates left, if true stops and returns true; choosing wrong operator inverts the logic of the entire condition",
        "severity": "medium",
        "frequency": 0.60,
        "correction_strategy": "Truth table with concrete Java examples; highlight short-circuit behavior"
    },
    {
        "id": "mc_sentinel_loop",
        "concept": "sentinel_loop",
        "week": 3,
        "error_type": "logic",
        "description": "Student forgets the priming read before a sentinel-controlled while loop",
        "common_indicators": [
            "sentinel", "priming read", "while loop", "first iteration", "never reads"
        ],
        "l1_pattern": "the loop doesn't process the first input",
        "l2_pattern": "you need to read before the loop",
        "l3_pattern": "a sentinel while loop checks the condition before each iteration; without a priming read the first check has no value to test",
        "l4_pattern": "sentinel-controlled while loops require a priming read before the loop to initialize the condition variable; the pattern is: read once, while(value != sentinel) { process; read again }; without the priming read the while condition tests an uninitialized value",
        "severity": "medium",
        "frequency": 0.55,
        "correction_strategy": "Show the read-process-read pattern; trace through by hand"
    },
    {
        "id": "mc_unreachable_code",
        "concept": "unreachable_code",
        "week": 3,
        "error_type": "compile",
        "description": "Student writes code after a return statement in the same block",
        "common_indicators": [
            "unreachable", "dead code", "after return", "never executes", "statement"
        ],
        "l1_pattern": "I have code after return",
        "l2_pattern": "nothing after return can run",
        "l3_pattern": "return exits the method immediately; any statements after it in the same block are unreachable and Java reports a compile error",
        "l4_pattern": "Java's static analysis detects statements that can never be executed; a return, break, continue, or throw makes all subsequent statements in that block unreachable; the compiler emits an unreachable statement error to prevent dead code",
        "severity": "low",
        "frequency": 0.50,
        "correction_strategy": "Remove or move the code to before the return statement"
    },
    {
        "id": "mc_string_immutability",
        "concept": "string_immutability",
        "week": 3,
        "error_type": "logic",
        "description": "Student assigns result of string operation but ignores the return value",
        "common_indicators": [
            "immutable", "replace", "concat", "toUpperCase", "unchanged", "same value"
        ],
        "l1_pattern": "the string doesn't change after I call replace",
        "l2_pattern": "String methods don't modify the original",
        "l3_pattern": "String objects in Java are immutable; methods like replace and toUpperCase return a new String; the original is unchanged",
        "l4_pattern": "java.lang.String is immutable by design for safety and string pool efficiency; every String method returns a new String object; the original reference is unmodified; to keep the result you must assign it back: s = s.toUpperCase()",
        "severity": "high",
        "frequency": 0.75,
        "correction_strategy": "Show s = s.replace(); contrast with StringBuilder"
    },
    {
        "id": "mc_no_default_constructor",
        "concept": "no_default_constructor",
        "week": 4,
        "error_type": "compile",
        "description": "Student defines a parameterized constructor and then tries to use no-arg constructor",
        "common_indicators": [
            "no default constructor", "constructor", "no args", "class", "OOP"
        ],
        "l1_pattern": "it says no default constructor",
        "l2_pattern": "once you add a constructor you lose the default one",
        "l3_pattern": "Java provides a default no-arg constructor only when no constructor is defined; adding any constructor removes the default",
        "l4_pattern": "the Java compiler auto-generates a no-arg constructor only if the class declares no constructors at all; as soon as you write any constructor the auto-generation is suppressed; if you need both a no-arg and a parameterized constructor you must write both explicitly",
        "severity": "medium",
        "frequency": 0.65,
        "correction_strategy": "Add explicit no-arg constructor; explain the Java compiler rule"
    },
    {
        "id": "mc_static_vs_instance",
        "concept": "static_vs_instance",
        "week": 4,
        "error_type": "compile",
        "description": "Student tries to access instance variables or methods from a static context",
        "common_indicators": [
            "static", "non-static", "instance", "this", "cannot be referenced", "static context"
        ],
        "l1_pattern": "it says non-static variable in static context",
        "l2_pattern": "static methods can't use instance things",
        "l3_pattern": "static methods belong to the class not any object; they cannot access instance variables or call instance methods because there is no this",
        "l4_pattern": "static methods are class-level and execute without an instance; instance variables and methods exist per-object and require a specific object reference (this) to access; from a static method there is no implicit this so any direct access to instance members is a compile-time error",
        "severity": "high",
        "frequency": 0.80,
        "correction_strategy": "Explain static belongs to class, instance belongs to object; show this"
    },
    {
        "id": "mc_foreach_no_modify",
        "concept": "foreach_no_modify",
        "week": 4,
        "error_type": "logic",
        "description": "Student expects for-each loop variable assignment to modify the original array",
        "common_indicators": [
            "for each", "doesn't change", "loop variable", "copy", "array unchanged"
        ],
        "l1_pattern": "changing the loop variable doesn't change the array",
        "l2_pattern": "the for-each variable is a copy",
        "l3_pattern": "the enhanced for loop variable is a copy of the element value; assigning to it does not modify the original array",
        "l4_pattern": "Java is pass-by-value; the enhanced for-each loop variable holds a copy of each primitive element (or a copy of the object reference for objects); assigning to the loop variable changes only the local copy; to modify array elements you must use a traditional indexed for loop",
        "severity": "medium",
        "frequency": 0.60,
        "correction_strategy": "Show indexed for loop; demonstrate with small array trace"
    },
    {
        "id": "mc_overloading",
        "concept": "overloading",
        "week": 4,
        "error_type": "logic",
        "description": "Student confused about which overloaded method gets called",
        "common_indicators": [
            "overload", "same name", "which method", "parameter", "signature"
        ],
        "l1_pattern": "I'm not sure which version runs",
        "l2_pattern": "Java picks based on the parameter types",
        "l3_pattern": "Java selects the overloaded method at compile time by matching the argument types to the parameter signature",
        "l4_pattern": "method overloading resolution occurs at compile time based on the static types of the arguments; Java selects the most specific applicable overload; if types are ambiguous or no match exists the compiler reports an error; runtime polymorphism applies to overriding not overloading",
        "severity": "medium",
        "frequency": 0.55,
        "correction_strategy": "Show method signatures side by side; trace which gets called for each call"
    },
    {
        "id": "mc_generics_primitives",
        "concept": "generics_primitives",
        "week": 5,
        "error_type": "compile",
        "description": "Student tries ArrayList<int> instead of ArrayList<Integer>",
        "common_indicators": [
            "ArrayList<int>", "primitive", "Integer", "wrapper", "generic", "type argument"
        ],
        "l1_pattern": "ArrayList<int> doesn't work",
        "l2_pattern": "you have to use Integer not int",
        "l3_pattern": "Java generics only work with reference types; int is a primitive so you must use the wrapper class Integer",
        "l4_pattern": "Java generics are implemented via type erasure and work only with reference types (objects on the heap); primitives like int are not objects and cannot be used as type parameters; each primitive has a corresponding wrapper class (int→Integer, double→Double etc.) that boxes the value into an object; Java autoboxing automatically converts between int and Integer in most contexts",
        "severity": "high",
        "frequency": 0.75,
        "correction_strategy": "Show ArrayList<Integer>; explain boxing/unboxing and autoboxing"
    },
]

# ─── Learning Progressions for 20 Java concepts ──────────────────────────────
JAVA_PROGRESSIONS = [
    {
        "id": "prog_java_week1",
        "concept_sequence": ["type_mismatch", "infinite_loop"],
        "difficulty_levels": [1, 1],
        "prerequisites": {
            "type_mismatch": [],
            "infinite_loop": ["type_mismatch"],
        },
        "mastery_thresholds": {"type_mismatch": 0.70, "infinite_loop": 0.70},
    },
    {
        "id": "prog_java_week2",
        "concept_sequence": [
            "null_pointer", "string_equality", "variable_scope",
            "assignment_vs_compare", "integer_division", "scanner_buffer"
        ],
        "difficulty_levels": [2, 2, 2, 1, 2, 3],
        "prerequisites": {
            "null_pointer":          ["type_mismatch"],
            "string_equality":       ["null_pointer"],
            "variable_scope":        ["type_mismatch"],
            "assignment_vs_compare": ["variable_scope"],
            "integer_division":      ["type_mismatch"],
            "scanner_buffer":        ["integer_division"],
        },
        "mastery_thresholds": {
            "null_pointer": 0.75, "string_equality": 0.80,
            "variable_scope": 0.70, "assignment_vs_compare": 0.70,
            "integer_division": 0.70, "scanner_buffer": 0.70,
        },
    },
    {
        "id": "prog_java_week3",
        "concept_sequence": [
            "array_index", "missing_return", "array_not_allocated",
            "boolean_operators", "sentinel_loop", "unreachable_code", "string_immutability"
        ],
        "difficulty_levels": [2, 2, 2, 2, 3, 1, 2],
        "prerequisites": {
            "array_index":        ["variable_scope"],
            "missing_return":     ["variable_scope"],
            "array_not_allocated":["null_pointer"],
            "boolean_operators":  ["assignment_vs_compare"],
            "sentinel_loop":      ["infinite_loop", "boolean_operators"],
            "unreachable_code":   ["missing_return"],
            "string_immutability":["string_equality", "null_pointer"],
        },
        "mastery_thresholds": {
            "array_index": 0.75, "missing_return": 0.70, "array_not_allocated": 0.75,
            "boolean_operators": 0.70, "sentinel_loop": 0.70,
            "unreachable_code": 0.65, "string_immutability": 0.75,
        },
    },
    {
        "id": "prog_java_week4",
        "concept_sequence": [
            "no_default_constructor", "static_vs_instance",
            "foreach_no_modify", "overloading"
        ],
        "difficulty_levels": [3, 3, 3, 3],
        "prerequisites": {
            "no_default_constructor": ["null_pointer", "variable_scope"],
            "static_vs_instance":     ["no_default_constructor"],
            "foreach_no_modify":      ["array_index"],
            "overloading":            ["missing_return", "static_vs_instance"],
        },
        "mastery_thresholds": {
            "no_default_constructor": 0.75, "static_vs_instance": 0.80,
            "foreach_no_modify": 0.70, "overloading": 0.70,
        },
    },
    {
        "id": "prog_java_week5",
        "concept_sequence": ["generics_primitives"],
        "difficulty_levels": [4],
        "prerequisites": {
            "generics_primitives": ["null_pointer", "no_default_constructor", "foreach_no_modify"],
        },
        "mastery_thresholds": {"generics_primitives": 0.80},
    },
]

# ─── Cognitive loads for 20 Java concepts ────────────────────────────────────
JAVA_COGNITIVE_LOADS = [
    {"concept": "type_mismatch",          "intrinsic": 2, "extraneous": 1, "germane": 2, "total": 2, "factors": ["type_system", "primitive_vs_reference"]},
    {"concept": "infinite_loop",          "intrinsic": 2, "extraneous": 2, "germane": 3, "total": 3, "factors": ["loop_mechanics", "update_step"]},
    {"concept": "null_pointer",           "intrinsic": 3, "extraneous": 2, "germane": 4, "total": 4, "factors": ["reference_semantics", "heap_vs_stack", "object_creation"]},
    {"concept": "string_equality",        "intrinsic": 3, "extraneous": 2, "germane": 4, "total": 4, "factors": ["reference_vs_value", "string_pool", "overriding_equals"]},
    {"concept": "variable_scope",         "intrinsic": 2, "extraneous": 1, "germane": 2, "total": 2, "factors": ["block_scoping", "lexical_scope"]},
    {"concept": "assignment_vs_compare",  "intrinsic": 1, "extraneous": 1, "germane": 2, "total": 1, "factors": ["operator_meaning"]},
    {"concept": "integer_division",       "intrinsic": 2, "extraneous": 1, "germane": 2, "total": 2, "factors": ["type_promotion", "truncation"]},
    {"concept": "scanner_buffer",         "intrinsic": 3, "extraneous": 3, "germane": 3, "total": 4, "factors": ["stream_model", "newline_token"]},
    {"concept": "array_index",            "intrinsic": 2, "extraneous": 1, "germane": 3, "total": 3, "factors": ["zero_indexing", "bounds_checking"]},
    {"concept": "missing_return",         "intrinsic": 2, "extraneous": 1, "germane": 2, "total": 2, "factors": ["control_flow_analysis", "all_paths"]},
    {"concept": "array_not_allocated",    "intrinsic": 3, "extraneous": 2, "germane": 3, "total": 3, "factors": ["reference_semantics", "heap_allocation"]},
    {"concept": "boolean_operators",      "intrinsic": 2, "extraneous": 1, "germane": 2, "total": 2, "factors": ["truth_tables", "short_circuit"]},
    {"concept": "sentinel_loop",          "intrinsic": 3, "extraneous": 2, "germane": 3, "total": 3, "factors": ["loop_pattern", "priming_read"]},
    {"concept": "unreachable_code",       "intrinsic": 1, "extraneous": 1, "germane": 2, "total": 1, "factors": ["static_analysis", "control_flow"]},
    {"concept": "string_immutability",    "intrinsic": 3, "extraneous": 2, "germane": 3, "total": 3, "factors": ["immutability", "return_value", "string_pool"]},
    {"concept": "no_default_constructor", "intrinsic": 3, "extraneous": 2, "germane": 3, "total": 3, "factors": ["oop", "constructor_rules"]},
    {"concept": "static_vs_instance",     "intrinsic": 4, "extraneous": 2, "germane": 4, "total": 4, "factors": ["class_vs_object", "this_reference", "static_context"]},
    {"concept": "foreach_no_modify",      "intrinsic": 3, "extraneous": 2, "germane": 3, "total": 3, "factors": ["pass_by_value", "loop_variable_copy"]},
    {"concept": "overloading",            "intrinsic": 3, "extraneous": 2, "germane": 3, "total": 3, "factors": ["compile_time_resolution", "signature_matching"]},
    {"concept": "generics_primitives",    "intrinsic": 4, "extraneous": 3, "germane": 4, "total": 5, "factors": ["type_erasure", "wrapper_classes", "autoboxing"]},
]

# ─── Interventions for Java concepts ─────────────────────────────────────────
JAVA_INTERVENTIONS = [
    {"id": "int_reference_diagram",      "name": "Reference vs Object Diagram",
     "type": "visualization", "target_concepts": ["null_pointer", "string_equality", "array_not_allocated"],
     "description": "Draw stack (reference) and heap (object) side by side",
     "content_template": "Let's draw memory: stack has the variable name, heap has the object. {example}",
     "effectiveness_score": 0.88, "usage_count": 0},
    {"id": "int_memory_trace",           "name": "Line-by-line Memory Trace",
     "type": "worked_example", "target_concepts": ["string_equality", "static_vs_instance", "foreach_no_modify"],
     "description": "Trace each line showing what each variable holds in memory",
     "content_template": "Let's trace through line by line: {trace}",
     "effectiveness_score": 0.85, "usage_count": 0},
    {"id": "int_loop_trace",             "name": "Loop Variable Trace",
     "type": "worked_example", "target_concepts": ["infinite_loop", "sentinel_loop", "array_index"],
     "description": "Trace loop iterations showing variable values each pass",
     "content_template": "Let's trace the loop: iteration 1: {i}={v1}, iteration 2: {i}={v2}...",
     "effectiveness_score": 0.82, "usage_count": 0},
    {"id": "int_java_vs_python",         "name": "Java vs Python Contrast",
     "type": "analogy", "target_concepts": ["type_mismatch", "integer_division", "string_immutability"],
     "description": "Contrast Java behavior with Python to leverage prior knowledge",
     "content_template": "In Python this works automatically, but in Java: {difference}",
     "effectiveness_score": 0.78, "usage_count": 0},
    {"id": "int_minimal_example",        "name": "Minimal Java Snippet",
     "type": "example", "target_concepts": ["scanner_buffer", "variable_scope", "missing_return"],
     "description": "5-10 line Java snippet isolating exactly the concept",
     "content_template": "Here is the smallest Java program that shows this: {snippet}",
     "effectiveness_score": 0.80, "usage_count": 0},
    {"id": "int_socratic_java",          "name": "Socratic Question — Java specific",
     "type": "socratic", "target_concepts": ["boolean_operators", "overloading", "assignment_vs_compare"],
     "description": "One targeted question pointing at the exact mechanism",
     "content_template": "Before I explain — what do you think happens when Java sees {expression}?",
     "effectiveness_score": 0.75, "usage_count": 0},
    {"id": "int_wrapper_autobox",        "name": "Wrapper + Autoboxing Explanation",
     "type": "explanation", "target_concepts": ["generics_primitives"],
     "description": "Explain primitive vs wrapper class with autoboxing",
     "content_template": "Java generics need objects, not primitives. Integer is the object version of int. {example}",
     "effectiveness_score": 0.80, "usage_count": 0},
    {"id": "int_oop_diagram",            "name": "Class vs Object Diagram",
     "type": "visualization", "target_concepts": ["no_default_constructor", "static_vs_instance"],
     "description": "Show class as blueprint and objects as instances",
     "content_template": "Think of the class as a blueprint. Each new creates a separate object. {diagram}",
     "effectiveness_score": 0.82, "usage_count": 0},
]


def save_json(path: Path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[OK] Saved {path} ({len(data)} items)")


def main():
    print("=" * 60)
    print("Setting up Java CSCI 1301 Pedagogical Knowledge Graph")
    print("=" * 60)

    # Save misconceptions
    save_json(DATA_DIR / "misconceptions.json",
              {m["id"]: m for m in JAVA_MISCONCEPTIONS})

    # Save progressions
    save_json(DATA_DIR / "learning_progressions.json",
              {p["id"]: p for p in JAVA_PROGRESSIONS})

    # Save cognitive loads
    save_json(DATA_DIR / "cognitive_loads.json",
              {c["concept"]: c for c in JAVA_COGNITIVE_LOADS})

    # Save interventions
    save_json(DATA_DIR / "interventions.json",
              {i["id"]: i for i in JAVA_INTERVENTIONS})

    # Save LP rubric definitions — L1 through L4 per concept
    lp_rubric = {}
    for m in JAVA_MISCONCEPTIONS:
        lp_rubric[m["concept"]] = {
            "concept":     m["concept"],
            "java_concept": m.get("java_concept", m["concept"]),
            "week":        m["week"],
            "error_type":  m["error_type"],
            "L1": {"name": "Heuristic",    "description": m["l1_pattern"],
                   "what_it_means": "Rule-based with no mechanism understanding"},
            "L2": {"name": "Qualitative",  "description": m["l2_pattern"],
                   "what_it_means": "Recognises a distinction but cannot explain the mechanism"},
            "L3": {"name": "Measurable",   "description": m["l3_pattern"],
                   "what_it_means": "Understands the actual mechanism; can name what is happening"},
            "L4": {"name": "Scientific",   "description": m["l4_pattern"],
                   "what_it_means": "Full principled explanation; can generalize to new situations"},
        }
    save_json(DATA_DIR / "lp_rubric.json", lp_rubric)

    print("\n[DONE] Java Pedagogical KG ready.")
    print(f"  Misconceptions:      {len(JAVA_MISCONCEPTIONS)}")
    print(f"  Progressions:        {len(JAVA_PROGRESSIONS)}")
    print(f"  Cognitive loads:     {len(JAVA_COGNITIVE_LOADS)}")
    print(f"  Interventions:       {len(JAVA_INTERVENTIONS)}")
    print(f"  LP rubric entries:   {len(lp_rubric)}")


if __name__ == "__main__":
    main()
