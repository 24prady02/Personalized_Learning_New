"""Add the sixteen concepts that chapter-1 student code can contain but KG v3.9.5 lacked.

    PYTHONPATH=src python -m lp_graph.kg_extend [--kg data/raw/chapter1_kg.json]

Idempotent: a concept that already exists is skipped. For every concept it writes the concept record
(rules of all 13 types), five learning-level nodes, five has_level edges with ways, prerequisite and
parallel edges, misconception and error nodes and edges (and links to existing misconceptions that
fit), a contains edge from its topic, and the reader block with code patterns. Every rule is marked
author-added and unverified: these constructs are not covered by the SW-1e chapter-1 text, so no
book quote exists for them. All additions are listed in kg["reader"]["concepts_added_reader4"].
"""
from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path

AUTH = {"type": "author", "note": "added 2026-10-30 (reader4 extension); construct not covered in SW-1e chapter 1, no book quote", "check": "unverified"}
STAMP = "3.9.5-reader4-ext"

# ----------------------------------------------------------------------------- sections and topics

SECTION = {"id": "sec.ext", "layer": 1, "type": "section", "section": "ext",
           "label": "Ext. Constructs beyond Chapter 1 that appear in student code", "source": "reader4",
           "topics": ["topic.ext.a", "topic.ext.b", "topic.ext.c", "topic.ext.d"]}
TOPICS = {
    "topic1.2.b": None,  # existing: Characters and strings
    "topic.ext.a": "Methods",
    "topic.ext.b": "Program structure",
    "topic.ext.c": "Objects and references",
    "topic.ext.d": "Operators and literals",
}

# ----------------------------------------------------------------------------- concepts

def mis(id_, wrong, right, role="primary", kind="misconception"):
    return {"id": id_, "wrong": wrong, "right": right, "role": role, "kind": kind}


def err(id_, wrong, right, ekind, trigger):
    return {"id": id_, "wrong": wrong, "right": right, "role": "primary", "kind": "error", "error_kind": ekind, "trigger": trigger}


CONCEPTS = [
 dict(id="string_methods", section="1.2", topic="topic1.2.b",
      description="s.length(), s.charAt(i), s.substring(a, b), s.indexOf(t), s.toUpperCase(): methods called on a String value; each returns a new value and leaves s unchanged",
      aliases=["string method", "string methods", "charAt", "substring", "indexOf", "toUpperCase", "toLowerCase", "length()", "trim", "split"],
      patterns=[r"\b\w+\.(?:length|charAt|substring|indexOf|lastIndexOf|toUpperCase|toLowerCase|trim|split|contains|startsWith|endsWith|replace|isEmpty|concat|equals|equalsIgnoreCase|compareTo)\s*\("],
      signals=[],
      prereqs=[("string_type", "A String value has methods; s.method(...) is called on the value that s holds, and that value never changes."),
               ("method_call", "A String method is a method call: it returns a value that must be stored or used, and a call on its own line does nothing."),
               ("indexing", "Positions in a String count from 0 like array indices: charAt(0) is the first character and charAt(length() - 1) the last.")],
      parallels=[],
      miscs=[mis("StringIndexStartsAtOne", "charAt(1) is the first character of the string.", "Positions count from 0: charAt(0) is the first character and charAt(s.length() - 1) the last."),
             mis("SubstringEndInclusive", "substring(a, b) includes the character at position b.", "substring(a, b) takes the characters at positions a to b - 1, so its length is b - a."),
             err("StringLengthIsField", "s.length without parentheses gives the number of characters.", "A String's length is the method call s.length(); only arrays have the field a.length.", "compile-time error", "s.length on a String: cannot find symbol (or a comparison of a method reference)"),
             err("StringIndexOutOfRange", "charAt(s.length()) reads the last character.", "Valid positions are 0 to s.length() - 1; charAt(s.length()) throws StringIndexOutOfBoundsException.", "run-time exception", "a loop to i <= s.length() with s.charAt(i), or charAt(s.length())")],
      link=[("StringMethodChangesString", "primary"), ("ArrayHasLengthMethod", "context")],
      E="In everyday reading 'the first letter' is letter 1 and 'up to position b' includes b. In Java, String positions start at 0 and the end position of substring is excluded.",
      T="Counts from 0 at charAt(0) but then treats substring(0, 3) as four characters, or applies s.toUpperCase() and later reads s as still lower case within the same trace.",
      N="String methods: operations such as length(), charAt(i), substring(a, b), indexOf(t) and toUpperCase() invoked on a String with dot notation.",
      S="A String method is called as s.name(arguments) and returns a value: length() the number of characters, charAt(i) the character at position i counting from 0, substring(a, b) the characters at positions a to b - 1, indexOf(t) the first position of t or -1. The String s itself never changes.",
      LT="Evaluate the receiver, then the arguments, then apply the method, and use the result where the call stands. Chained calls such as s.trim().toUpperCase() are applied left to right.",
      OP="\"hello\".length() is 5, \"hello\".charAt(1) is 'e', \"hello\".substring(1, 3) is \"el\", \"hello\".indexOf(\"l\") is 2, \"hello\".toUpperCase() is \"HELLO\".",
      OS="After t = s.toUpperCase(); t holds the upper-case copy and s is unchanged; after s = s.toUpperCase(); s holds the new String and the old value is gone.",
      P="String methods take text apart and rebuild it: a loop over i from 0 to s.length() - 1 with s.charAt(i) examines each character; indexOf finds a position and substring cuts the string there.",
      C="Changing substring(1, 3) to substring(1, 4) adds one character. Changing a loop bound from i < s.length() to i <= s.length() reads past the end on the last pass. Dropping the assignment in s = s.trim() leaves s unchanged.",
      X="Use charAt in a counted loop to examine characters, substring with an exclusive end to cut text, indexOf to search; assign the result of any String method whose effect should persist."),

 dict(id="string_comparison", section="1.2", topic="topic1.2.b",
      description="s.equals(t) compares the characters of two Strings; s == t asks whether they are the same object",
      aliases=["equals", "equalsIgnoreCase", "compareTo", "same string", "string comparison", "compare strings"],
      patterns=[r"\.equals(?:IgnoreCase)?\s*\(", r"\.compareTo(?:IgnoreCase)?\s*\("],
      signals=[{"name": "string_double_equals", "scope": "program", "decisive": True,
                "regex": r"\bString\s+(\w+)\s*(?:=[^;]*)?;[\s\S]{0,800}?\b\1\s*(?:==|!=)\s*(?:\w+|\")|(?:==|!=)\s*\"",
                "note": "a String variable or a string literal compared with == or !="}],
      prereqs=[("string_type", "A String variable holds a reference to a String object; two variables can refer to different objects that spell the same text."),
               ("comparison_operators", "== and != on Strings compare references, not characters; the characters are compared with equals."),
               ("primitive_vs_reference", "For primitives == compares values; for String references it compares identity, which is why equals exists.")],
      parallels=[],
      miscs=[mis("StringEqualsOperator", "s == t is true whenever s and t spell the same text.", "== asks whether s and t refer to the same String object; s.equals(t) asks whether they contain the same characters."),
             mis("CompareToIsBoolean", "compareTo returns true or false.", "compareTo returns an int: negative, zero or positive according to dictionary order of the two strings."),
             mis("EqualsIgnoresCase", "equals ignores the case of letters.", "equals compares the exact characters; equalsIgnoreCase is the method that ignores case."),
             err("InputStringComparedWithOperator", "Comparing a String read from StdIn or args with == works.", "A string read at run time is a new object, so == is false even when the text matches; use equals.", "silent logic error", "if (answer == \"yes\") with answer read from input never matches")],
      link=[("EqualsComparesReferences", "primary")],
      E="In everyday language two words 'are equal' when they are spelled the same, and the = sign means that. In Java, == on two Strings asks whether they are the very same object; spelling is compared with equals.",
      T="Uses equals for one comparison and == for the next in the same program, or treats == as working for literals but not for input without saying why.",
      N="String comparison: s.equals(t) and s.equalsIgnoreCase(t) test the characters, s.compareTo(t) orders two strings, and s == t tests whether both names refer to one object.",
      S="s.equals(t) is true exactly when the two Strings have the same length and the same character at every position. s == t is true only when both refer to the same object. s.compareTo(t) is negative, zero or positive as s comes before, equals or comes after t.",
      LT="Evaluate both operands to String values, then apply the comparison: for equals compare characters position by position; for == compare the references.",
      OP="\"abc\".equals(\"abc\") is true; \"abc\".equalsIgnoreCase(\"ABC\") is true; \"abc\".compareTo(\"abd\") is negative; s == t is true for two names of one literal and usually false for a string read from input.",
      OS="A comparison changes no variable; its boolean result selects a branch or is stored.",
      P="A String comparison decides a branch: if (cmd.equals(\"quit\")) ends a read loop; compareTo sorts or finds the alphabetically smallest word.",
      C="Replacing equals with == makes a comparison with input text false; adding IgnoreCase accepts \"Yes\" and \"YES\" as well; swapping the operands of compareTo flips the sign.",
      X="Compare Strings with equals or equalsIgnoreCase, order them with compareTo, and reserve == for primitives."),

 dict(id="character_methods", section="1.2", topic="topic1.2.b",
      description="Character.isDigit(c), Character.isLetter(c), Character.toUpperCase(c): static methods that test or convert a single char and return a new value",
      aliases=["Character class", "isDigit", "isLetter", "Character.toUpperCase", "character method"],
      patterns=[r"\bCharacter\.\w+\s*\("],
      signals=[],
      prereqs=[("char", "The argument of a Character method is a single char value."),
               ("method_call", "Character.isDigit(c) is a static method call whose boolean or char result must be used.")],
      parallels=[],
      miscs=[mis("CharacterMethodMutates", "Character.toUpperCase(c) changes c.", "It returns a new char; c changes only if the result is assigned: c = Character.toUpperCase(c);"),
             mis("IsDigitTakesString", "Character.isDigit(s) tests whether a whole String is a number.", "It tests one char; test each character with s.charAt(i) in a loop, or parse the string."),
             err("CharacterClassLowerCase", "character.isDigit(c) calls the library method.", "The class is Character with a capital C: Character.isDigit(c).", "compile-time error", "character.isDigit(c): cannot find symbol")],
      link=[("MathMethodWithoutClassName", "context")],
      E="In everyday reading 'make it upper case' changes the letter in place and 'is it a digit' can be asked of any text. In Java the Character methods take one char and return a new value.",
      T="Assigns the result of Character.toUpperCase in one line and in the next expects an unassigned call to have changed the variable.",
      N="Character methods: static methods of the Character class, called as Character.name(c), that test (isDigit, isLetter, isWhitespace) or convert (toUpperCase, toLowerCase, getNumericValue) one char.",
      S="Character.isDigit(c) is true when c is '0' to '9'; Character.isLetter(c) when c is a letter; Character.toUpperCase(c) returns the upper-case char and leaves c unchanged; Character.getNumericValue('7') is 7.",
      LT="Evaluate the char argument, apply the static method, use the returned boolean or char where the call stands.",
      OP="Character.isDigit('7') is true, Character.isLetter('7') is false, Character.toUpperCase('a') is 'A', Character.getNumericValue('7') is 7.",
      OS="After c = Character.toUpperCase(c); c holds the upper-case character; after Character.toUpperCase(c); alone c is unchanged.",
      P="Character methods classify the characters of a String one by one: counting digits in a loop with charAt, or normalising case before comparing.",
      C="Replacing isDigit with isLetter counts letters instead of digits; dropping the assignment leaves the character unchanged; the result of getNumericValue is an int, so adding it sums digits rather than joining them.",
      X="Use Character methods on single chars obtained from charAt, and assign their result when the change should persist."),

 dict(id="method_definition", section="ext", topic="topic.ext.a",
      description="static type name(parameters) { body }: a named block of code that runs when it is called; void when it returns nothing",
      aliases=["method", "methods", "function", "functions", "define a method", "helper method", "static method", "method header", "method signature"],
      patterns=[r"^\s*(?:public|private|protected)?\s*static\s+(?!void\s+main\b)[\w\[\]<>]+\s+\w+\s*\([^)]*\)\s*\{",
                r"^\s*(?:public|private|protected)?\s*(?:static\s+)?(?:int|double|boolean|char|long|String|void|float|short|byte)(?:\[\])*\s+(?!main\b)\w+\s*\([^)]*\)\s*\{"],
      signals=[],
      prereqs=[("main_method", "main is itself a static method; other methods are declared beside it in the class and called from it."),
               ("block", "The body of a method is a block with its own scope; variables declared inside it do not exist outside."),
               ("data_type", "The return type and each parameter have a declared type; void means no value comes back.")],
      parallels=[],
      miscs=[mis("MethodRunsWhereDefined", "A method's body runs at the place in the file where it is written.", "A method body runs only when the method is called; definitions may appear in any order in the class."),
             mis("VoidMethodReturnsValue", "A void method can hand back a value with return x;", "void means no value is returned; return; alone may be used to leave the method early."),
             err("MethodInsideMethod", "A helper method can be defined inside main.", "Methods are defined directly in the class, never inside another method.", "compile-time error", "a method header inside main: illegal start of expression"),
             err("MissingReturnInNonVoid", "A non-void method may end without returning on some path.", "Every path through a non-void method must reach a return with a value.", "compile-time error", "missing return statement")],
      link=[("ParameterTypesInCall", "context")],
      E="In everyday reading a recipe written on a page is carried out as one reads it. In Java a method is a named recipe that runs only when called, and the call can come from anywhere in the class.",
      T="Traces the first call into the method correctly, but on the second call continues with the variables of the first call or skips the body as if it had already run.",
      N="Method definition: a header static type name(parameters) followed by a block, defining a reusable piece of code that is run by calling name(arguments).",
      S="A method is declared as static returnType name(type param, ...) { body }. Calling name(args) copies the arguments into the parameters, runs the body, and hands back the value of return (none when the type is void).",
      LT="At a call, evaluate the arguments, jump into the body with the parameters set, run the body until return or its end, then continue in the caller with the returned value in place of the call.",
      OP="static int square(int x) { return x * x; } makes square(3) evaluate to 9 and square(square(2)) to 16; a void method call is a statement and produces no value.",
      OS="Calling a method creates fresh parameters and local variables; when it returns they vanish, and the caller's variables are unchanged unless the method changed an array they share.",
      P="A method names a step so main reads as a plan: isPrime(n), average(a), printRow(i). The same code is written once and called from several places.",
      C="Changing a parameter type changes which arguments compile; making the return type void removes the value from the caller's expression; moving a method below main changes nothing.",
      X="Put repeated or self-contained work into a static method with a clear name, a parameter for every varying input, and a return type for the single result."),

 dict(id="return_statement", section="ext", topic="topic.ext.a",
      description="return value; ends the method at once and hands the value to the caller",
      aliases=["return", "returns", "return value", "return statement"],
      patterns=[r"\breturn\b"],
      signals=[],
      prereqs=[("method_definition", "return belongs to a method body; its value becomes the value of the call in the caller."),
               ("control_flow", "return is a transfer of control: the method ends immediately, whatever loop or branch it is in.")],
      parallels=[],
      miscs=[mis("ReturnPrintsValue", "return x; prints x.", "return hands x back to the caller; nothing is shown unless the caller prints it."),
             mis("CodeAfterReturnRuns", "Statements after return in the same block still run.", "return ends the method at once; code after it in the same block never runs (and is a compile error when it directly follows)."),
             err("UnreachableAfterReturn", "A statement may follow return in the same block.", "The compiler rejects an unreachable statement after return.", "compile-time error", "unreachable statement")],
      link=[("ReturnDoesNotExitLoop", "primary"), ("DiscardedReturnValue", "context"), ("EarlyReturnInLoop", "context")],
      E="In everyday reading 'return the answer' means announce or write it down. In Java return hands a value to the caller silently and ends the method.",
      T="Treats return as exiting the method in one trace and as 'setting the answer and continuing the loop' in the next.",
      N="return statement: return expression; inside a method, which evaluates the expression, ends the method and makes that value the result of the call.",
      S="return expr; evaluates expr, ends the method immediately, skipping any remaining statements and loop passes, and the call expression takes that value. In a void method return; ends the method without a value.",
      LT="Evaluate the expression after return, leave the method, resume the caller at the call with that value.",
      OP="for a method that returns i inside a loop over i from 0 when a[i] == k, the call yields the first matching index and the loop stops there; the call never yields the later matches.",
      OS="After return the method's locals are gone; the caller's variables are unchanged except where the returned value is stored.",
      P="return delivers the one result a method computes: the sum after a loop, the found index as soon as it is seen, or a boolean verdict.",
      C="Moving return inside the loop ends the search at the first hit; moving it after the loop returns only after all elements; returning -1 after the loop marks 'not found'.",
      X="Return the result once it is known, return a sentinel such as -1 when there is none, and let the caller print or store it."),

 dict(id="parameters_and_arguments", section="ext", topic="topic.ext.a",
      description="parameters are the variables in a method header; arguments are the values a call passes, copied into them",
      aliases=["parameter", "parameters", "argument", "arguments", "pass by value", "passing", "passed to the method"],
      patterns=[],
      signals=[{"name": "typed_parameter_list", "scope": "program", "decisive": True,
                "regex": r"\b(?:int|double|boolean|char|long|String|void|float|short|byte)(?:\[\])*\s+(?!main\b)\w+\s*\(\s*(?:final\s+)?(?:int|double|boolean|char|long|String|float|short|byte)(?:\[\])*\s+\w+(?:\s*,\s*(?:final\s+)?[\w\[\]<>]+\s+\w+)*\s*\)\s*\{",
                "note": "a method header with at least one typed parameter"}],
      prereqs=[("method_definition", "Parameters are declared in the method header and exist only while the method runs."),
               ("variable", "A parameter is a variable of the method, initialised from the argument at each call."),
               ("assignment", "Passing an argument is an assignment of its value to the parameter; assigning to the parameter later changes only the parameter.")],
      parallels=[],
      miscs=[mis("ArgumentChangeAffectsCaller", "Assigning to a parameter inside the method changes the caller's variable.", "Java passes a copy of the value; assigning to the parameter changes only the copy. Only through a shared array reference can a method change the caller's data."),
             mis("ParameterNamesMustMatch", "The argument variable must have the same name as the parameter.", "Names are independent; the argument's value is copied into the parameter whatever it is called."),
             err("ArgumentCountMismatch", "A method can be called with fewer or more arguments than it has parameters.", "A call must supply exactly one argument of a compatible type for every parameter.", "compile-time error", "method f cannot be applied to given types")],
      link=[("ParameterTypesInCall", "primary")],
      E="In everyday reading 'giving someone the box' lets them change what is inside it. In Java an argument of primitive type is copied, so the method gets its own value; an array argument shares the elements.",
      T="Copies a primitive argument correctly in one call and then expects a later call to have changed the caller's variable.",
      N="Parameters and arguments: the typed names in a method header are parameters; the expressions in a call are arguments whose values are copied into them.",
      S="At a call each argument is evaluated and its value is copied into the corresponding parameter, matched by position, with a compatible type. The parameter is a local variable of the method; changing it does not change the argument.",
      LT="Evaluate the arguments left to right, bind them to the parameters by position, run the body; on return the parameters disappear.",
      OP="With static void inc(int x) { x = x + 1; } the call inc(a) leaves a unchanged; with static void zero(int[] a) { a[0] = 0; } the caller's array element becomes 0.",
      OS="During the call the parameter holds the copied value; after the call the caller's primitive variable is as before, and a shared array shows any element changes.",
      P="Parameters make a method general: the same body serves every value passed; an array parameter lets a method process or fill the caller's data.",
      C="Swapping two arguments swaps which parameter gets which value; changing a parameter from int to int[] lets the method change the caller's data; renaming a parameter changes nothing.",
      X="Pass what the method needs as arguments, return the single result, and use an array parameter when the method must change several values."),

 dict(id="recursion", section="ext", topic="topic.ext.a",
      description="a method that calls itself on a smaller input, with a base case that returns without calling",
      aliases=["recursion", "recursive", "calls itself", "base case", "recursive call"],
      patterns=[],
      signals=[{"name": "recursive_call", "scope": "program", "decisive": True,
                "regex": r"\b(?:static\s+)?(?:int|double|boolean|char|long|String|void|float|short|byte)(?:\[\])*\s+(?P<m>\w+)\s*\([^)]*\)\s*\{(?:[^{}]|\{[^{}]*\})*?\b(?P=m)\s*\(",
                "note": "a method whose body calls itself"}],
      prereqs=[("method_definition", "A recursive method is an ordinary method whose body contains a call to itself."),
               ("return_statement", "Each call returns its result to the call that made it; the first call returns last."),
               ("if_statement", "The base case is an if that returns directly for the smallest input.")],
      parallels=[],
      miscs=[mis("RecursionNeedsNoBaseCase", "A recursive method stops by itself when the argument gets small.", "It stops only when a base case returns without calling again; without one the calls never end and the program dies with StackOverflowError."),
             mis("RecursionReusesVariables", "The recursive call jumps back to the start of the method and reuses the same variables, like a loop.", "Each call has its own parameters and local variables; when it returns, the caller resumes where it left off with its own values."),
             mis("RecursiveCallsRunAtOnce", "All the recursive calls run at the same time.", "Each call waits for the inner call to return; the deepest call finishes first and the results are combined on the way back."),
             err("MissingBaseCase", "The recursion will stop when n reaches 0 even without a test.", "Without an if that returns for the smallest case the method calls itself for ever.", "run-time exception", "StackOverflowError")],
      link=[],
      E="In everyday reading a definition that uses itself is circular and meaningless. In Java a method may call itself on a smaller input, and the base case keeps the definition well founded.",
      T="Unwinds the first two calls correctly and then combines the results of deeper calls in the wrong order or forgets the pending work in the outer calls.",
      N="Recursion: a method that calls itself with a smaller argument, together with a base case that returns a direct answer.",
      S="A recursive method has a base case, an if that returns the answer for the smallest input, and a recursive case that calls the method on a smaller input and combines the result. Each call has its own parameters; the inner call completes before the outer one continues.",
      LT="Enter the call; if the base case holds, return its value; otherwise evaluate the recursive call fully (recursively), then combine and return.",
      OP="static int fact(int n) { if (n <= 1) return 1; return n * fact(n - 1); } gives fact(4) = 4 * fact(3) = 4 * 3 * fact(2) = 4 * 3 * 2 * 1 = 24.",
      OS="Each pending call keeps its own n; after the deepest return the values are multiplied on the way back up and the outer call returns 24.",
      P="Recursion expresses a problem in terms of a smaller copy of itself: factorial, sum of digits, power, or printing a ruler; the base case is the smallest instance.",
      C="Changing the base case from n <= 1 to n == 1 makes fact(0) recurse without end; changing n - 1 to n never reaches the base case; swapping the print and the recursive call reverses the output order.",
      X="Write a base case first, make sure every recursive call moves toward it, and combine the returned value rather than relying on shared variables."),

 dict(id="import_statement", section="ext", topic="topic.ext.b",
      description="import java.util.Scanner; before the class makes a library class usable by its simple name; java.lang needs no import",
      aliases=["import", "imports", "import statement", "java.util", "package"],
      patterns=[r"^\s*import\s+(?:static\s+)?[\w.]+\s*(?:\.\*)?\s*;", r"^\s*package\s+[\w.]+\s*;"],
      signals=[{"name": "scanner_without_import", "scope": "program", "decisive": True,
                "regex": r"\A(?![\s\S]*\bimport\s+java\.util\b)[\s\S]*\bnew\s+Scanner\s*\(",
                "note": "Scanner used in a program with no import java.util line"}],
      prereqs=[("program_text", "import lines belong to the program text before the class declaration, after any package line.")],
      parallels=[],
      miscs=[mis("ImportCopiesCode", "import pastes the library's code into the program.", "import only lets the simple name Scanner stand for java.util.Scanner; nothing is copied and the program size does not change."),
             mis("JavaLangNeedsImport", "System, Math and String need an import line.", "Everything in java.lang is available without import; only other packages such as java.util need one."),
             err("ImportInsideClass", "import can be written inside the class body.", "import lines come before the class declaration, after any package line.", "compile-time error", "import inside the class: illegal start of type"),
             err("MissingImport", "Scanner can be used without an import.", "Using java.util.Scanner by its simple name requires import java.util.Scanner; (or java.util.*).", "compile-time error", "new Scanner(System.in) with no import: cannot find symbol")],
      link=[],
      E="In everyday reading 'import' brings goods in, so novices expect code to be copied into the file. In Java import only makes a name known to the compiler.",
      T="Writes import java.util.Scanner; in one program and in the next expects Scanner to work without it, or adds an import for Math.",
      N="import statement: import package.Class; (or package.*) at the top of the file, telling the compiler which library class a simple name refers to.",
      S="An import line appears before the class, after any package line, and makes the named class usable by its simple name. Classes in java.lang (System, Math, String, Integer) need no import. A class from another package used without import does not compile.",
      LT="The compiler reads the import lines first and resolves every simple class name in the file against them and java.lang.",
      OP="With import java.util.Scanner; the declaration Scanner in = new Scanner(System.in); compiles; without it javac reports cannot find symbol: class Scanner.",
      OS="import changes no run-time state; it affects only whether the program compiles.",
      P="Imports declare which libraries a program relies on: java.util for Scanner and ArrayList, java.io for files; the StdIn and StdOut classes are in the default package and need none.",
      C="Removing the import of Scanner breaks compilation; replacing it with import java.util.*; still compiles; adding import java.lang.Math; is allowed but unnecessary.",
      X="Import exactly the classes from other packages that the program uses, placed before the class declaration."),

 dict(id="null_reference", section="ext", topic="topic.ext.c",
      description="null: the value of a reference variable that refers to no object; using it as an object throws NullPointerException",
      aliases=["null", "null pointer", "NullPointerException", "refers to nothing", "no object"],
      patterns=[r"\bnull\b"],
      signals=[],
      prereqs=[("primitive_vs_reference", "Only reference variables (String, arrays, objects) can be null; a primitive always holds a value."),
               ("string_type", "A String variable declared without a value as a field, or assigned null, refers to no String.")],
      parallels=[],
      miscs=[mis("NullIsEmptyString", "null and \"\" are the same thing.", "\"\" is a real String with no characters, on which methods work; null is no object at all, and any method call on it throws."),
             mis("NullIsZero", "A variable set to null holds 0.", "null means the variable refers to no object; only numeric primitives hold 0."),
             mis("MethodOnNullReturnsNull", "Calling a method on a null variable returns null.", "It throws NullPointerException and the program stops unless the exception is caught."),
             err("NullPointerDereference", "s.length() is safe when s may be null.", "Test s != null before calling a method on s, or make sure s was assigned.", "run-time exception", "NullPointerException on a method call or array access through a null reference")],
      link=[("NullIsObject", "primary"), ("OutOfBoundsElementsAreNull", "context")],
      E="In everyday reading 'nothing' is like zero or an empty box. In Java null is the absence of an object: a reference pointing nowhere, distinct from 0 and from \"\".",
      T="Tests one variable for null before use but calls a method on another possibly-null variable in the same trace, or treats null as \"\" in one line and as an error in the next.",
      N="null reference: the literal null, which a reference variable holds when it refers to no object; the default value of object elements in a new array.",
      S="A reference variable holds either a reference to an object or null. Comparing with == null is allowed and tells whether an object is present. Calling a method or reading a field through a null reference throws NullPointerException.",
      LT="Evaluate the reference; if it is null, any dot operation on it throws at that point and the rest of the statement is not executed.",
      OP="String s = null; s.length() throws NullPointerException; String t = \"\"; t.length() is 0; new String[3] holds three nulls.",
      OS="After s = null; the variable refers to nothing; after s = \"\"; it refers to an empty String; array elements of object type start as null.",
      P="null marks 'no value yet' or 'not found' for references: a search method returns null when nothing matches, and the caller tests for it before using the result.",
      C="Initialising the String array elements removes the NullPointerException; replacing == null with equals(null) throws instead of testing; a primitive int cannot be null.",
      X="Give every reference a value before using it, test for null where absence is possible, and never use null where \"\" or 0 is meant."),

 dict(id="unary_operators", section="ext", topic="topic.ext.d",
      description="-x, +x and !b: operators with one operand that produce a new value and change nothing",
      aliases=["unary minus", "negation", "negate", "unary operator", "unary"],
      patterns=[r"(?:^|[=(,;+*/%<>!&|?:])\s*-(?!-)\s*[A-Za-z_(]", r"[=(,]\s*\+(?!\+)\s*[A-Za-z_(]", r"!(?!=)\s*[A-Za-z_(]"],
      signals=[],
      prereqs=[("arithmetic_operators", "Unary minus is the one-operand form of -, applied before the binary operators."),
               ("logical_operators", "! is the unary boolean operator; it inverts a truth value.")],
      parallels=[("increment_operators", "++ and -- are also unary, but they change the variable; -x and !b produce a value and change nothing.")],
      miscs=[mis("NegationMutatesVariable", "Writing -x changes x to its negative.", "-x is a new value; x is unchanged unless the result is assigned, as in x = -x;"),
             mis("MinusMinusIsDoubleNegative", "x = --y is the same as x = -(-y).", "-- is the decrement operator, so --y decreases y by 1 first; - -y with a space is double negation.")],
      link=[],
      E="In everyday arithmetic writing a minus in front of a number changes the number. In Java -x computes a new value and x stays as it was.",
      T="Negates a value correctly in an expression and then also treats the variable as negated afterwards.",
      N="Unary operators: -x (negation), +x (identity) and !b (logical not), each taking one operand and yielding a new value.",
      S="Unary -, + and ! bind tighter than the binary arithmetic and comparison operators: -a * b is (-a) * b and !a && b is (!a) && b. They evaluate their operand and produce a new value without changing it.",
      LT="Evaluate the operand, apply the unary operator, use the result; the operand variable is untouched.",
      OP="With x = 5, -x is -5 and x is still 5; -x * 2 is -10; with b = true, !b is false; - -x is 5.",
      OS="A unary operator changes no variable; x = -x; stores the negated value back into x.",
      P="Unary minus flips a sign or reverses a direction (dx = -dx on a bounce); ! inverts a flag in a condition.",
      C="Inserting a space in --x turns a decrement into double negation; parenthesising -(a * b) gives the same value as -a * b for integers; removing ! inverts the branch taken.",
      X="Use -x for a new negated value and x = -x to store it; use ! to invert a boolean and ++/-- only when the variable itself should change."),

 dict(id="bitwise_operators", section="ext", topic="topic.ext.d",
      description="&, |, ^, ~, <<, >>, >>> operate on the bits of integers; & and | on booleans evaluate both sides",
      aliases=["bitwise", "bit operator", "shift", "left shift", "right shift", "bitwise and", "bitwise or"],
      patterns=[r"^(?![ \t]*(?:[%$]|javac?\b))[^\n]*?[\w)\]]\s*(?:&|\|)(?![&|=])\s*[\w(]", r"[\w)\]]\s*(?:<<|>>>?)(?!=)\s*[\w(]", r"~\s*[\w(]"],
      signals=[],
      prereqs=[("int", "Bitwise operators act on the binary representation of int and long values."),
               ("logical_operators", "&& and || are the short-circuit boolean operators; & and | are their non-short-circuit, bitwise counterparts."),
               ("boolean", "On boolean operands & and | give the same truth table as && and || but always evaluate both sides.")],
      parallels=[("exclusive_or", "^ is exclusive or on booleans and on bits; it is not exponentiation.")],
      miscs=[mis("SingleAmpersandIsAnd", "& and && do the same thing.", "On booleans & evaluates both sides even when the left is false, so a guard like i < a.length & a[i] > 0 can still index out of bounds; on ints & works bit by bit."),
             mis("ShiftIsMultiplyAlways", "x << 1 always equals x * 2.", "Only while no significant bit is shifted out; shifting past the 31-bit range overflows, and >> keeps the sign while >>> does not.")],
      link=[("CaretIsPower", "primary")],
      E="In everyday reading & means 'and' and ^ looks like 'to the power of'. In Java & is the bitwise or non-short-circuit and, and ^ is exclusive or.",
      T="Uses && for one guard and & for the next, or treats ^ as a power in one line and as xor in another.",
      N="Bitwise operators: & (and), | (or), ^ (xor), ~ (not), << (shift left), >> (arithmetic shift right) and >>> (logical shift right), acting on the bits of int and long values.",
      S="& | ^ combine corresponding bits of two integers; ~ flips every bit; x << n multiplies by 2^n within the width; x >> n divides by 2^n keeping the sign; on booleans & | ^ evaluate both operands.",
      LT="Convert the operands to binary, apply the operation bit by bit (or shift the bit pattern), and read the result back as an integer.",
      OP="6 & 3 is 2, 6 | 3 is 7, 6 ^ 3 is 5, 1 << 3 is 8, -8 >> 1 is -4, 2 ^ 3 is 1 (not 8).",
      OS="Bitwise operators change no variable unless assigned (x <<= 1 doubles x in place).",
      P="Bit operations test and set flags, extract digits in binary, and compute fast powers of two; in chapter-1 code they appear mostly by mistake for && or Math.pow.",
      C="Replacing & by && in a guard stops the out-of-bounds access; replacing ^ by Math.pow gives the intended power; shifting by 32 wraps the shift count.",
      X="Use && and || for conditions, Math.pow or repeated multiplication for powers, and bitwise operators only when working on bits deliberately."),

 dict(id="numeric_literals_radix", section="ext", topic="topic.ext.d",
      description="0x1F (hexadecimal), 0b101 (binary), 010 (octal) and 1_000_000 (underscores) are alternative spellings of int literals",
      aliases=["hexadecimal", "hex literal", "binary literal", "octal", "leading zero", "underscore in number"],
      patterns=[r"\b0[xX][0-9A-Fa-f_]+\b", r"\b0[bB][01_]+\b", r"(?<![\d.])\b0[0-7]+\b(?![.\deE])", r"\b\d+(?:_\d+)+\b"],
      signals=[],
      prereqs=[("literal", "A radix literal is just another spelling of an int literal; its value is fixed at compile time."),
               ("int", "The value is an ordinary int (or long with L); the base is only a way of writing it.")],
      parallels=[],
      miscs=[mis("LeadingZeroIsDecimal", "010 is ten.", "A leading 0 makes an octal literal: 010 is eight, and 08 does not compile."),
             mis("HexLiteralIsText", "0x1F is a String of characters.", "0x1F is an int literal with value 31; it prints as 31."),
             mis("UnderscoresPrintInOutput", "1_000_000 prints as 1_000_000.", "Underscores exist only in the source; the value is 1000000 and prints as such.")],
      link=[],
      E="In everyday reading 010 is 'ten with a leading zero' and 1,000,000 is written with separators. In Java a leading 0 means octal and underscores are allowed only as visual separators in the source.",
      T="Reads 0x10 as 16 and then 010 as 10 in the same trace.",
      N="Radix literals: 0x or 0X prefix for hexadecimal, 0b or 0B for binary, a leading 0 for octal, and underscores between digits for readability; all denote int values.",
      S="0x1F is 31, 0b101 is 5, 010 is 8, 1_000_000 is 1000000. The literal's base does not affect the value stored or printed; System.out.println(0x1F) prints 31.",
      LT="Convert the literal from its base to a value at compile time, then use the value like any int.",
      OP="System.out.println(0x10 + 010 + 0b10) prints 26 (16 + 8 + 2).",
      OS="The variable holds the numeric value; the spelling of the literal is not kept.",
      P="Hex and binary literals show bit patterns (0xFF, 0b1010) and underscores group long constants (1_000_000); octal appears mostly by accident from a leading zero.",
      C="Removing the leading zero from 010 changes the value from 8 to 10; changing 0x to 0b changes the base; printing with Integer.toHexString shows the hex spelling again.",
      X="Write decimal unless a bit pattern is meant; never pad a number with a leading zero; use Integer.toBinaryString or toHexString to display other bases."),

 dict(id="string_builder", section="ext", topic="topic.ext.c",
      description="StringBuilder sb = new StringBuilder(); sb.append(x); builds text in place; sb.toString() gives the String",
      aliases=["StringBuilder", "append", "string builder"],
      patterns=[r"\bStringBuilder\b", r"\.append\s*\("],
      signals=[],
      prereqs=[("string_type", "A StringBuilder is a mutable companion of String; toString() converts it back to a String."),
               ("string_methods", "StringBuilder has methods of its own (append, insert, reverse, toString) that change the builder, unlike String methods."),
               ("method_call", "sb.append(x) is a method call on the builder object.")],
      parallels=[],
      miscs=[mis("StringBuilderIsImmutable", "sb.append(x) returns a new builder and leaves sb unchanged.", "append changes sb in place and returns the same builder, so sb.append(x); alone is enough."),
             mis("StringBuilderIsString", "A StringBuilder can be used wherever a String is needed.", "Call sb.toString() to get a String; a StringBuilder is a different type.")],
      link=[("StringMethodChangesString", "context")],
      E="By analogy with String methods, which return new values, novices expect append to return a new builder. StringBuilder is the mutable exception: its methods change the object itself.",
      T="Appends in place on one line and on the next assigns sb = sb.append(x) as if the old builder were unchanged.",
      N="StringBuilder: a mutable sequence of characters built with append, insert and reverse, converted to a String with toString().",
      S="new StringBuilder() creates an empty builder; sb.append(x) adds the text form of x to its end and changes sb; sb.length() is the current length; sb.toString() returns the accumulated String.",
      LT="Each append changes the builder's contents in order; toString at the end produces the String.",
      OP="StringBuilder sb = new StringBuilder(); sb.append(\"a\"); sb.append(1); sb.append('b'); sb.toString() is \"a1b\".",
      OS="After sb.append(x); sb holds the longer text; the builder object is the same one, so every name for it sees the change.",
      P="A StringBuilder gathers text in a loop efficiently where repeated s = s + piece would copy the whole string each time.",
      C="Replacing s += piece in a loop by sb.append(piece) changes the speed, not the result; forgetting toString() passes a builder where a String is expected.",
      X="Use StringBuilder when text is built in a loop, append in place, and convert once with toString()."),

 dict(id="exception_handling", section="ext", topic="topic.ext.c",
      description="try { } catch (Type e) { }: run code and, if it throws an exception of that type, run the catch block instead of stopping",
      aliases=["exception", "exceptions", "try", "catch", "throw", "throws", "finally", "try-catch"],
      patterns=[r"\btry\s*\{", r"\bcatch\s*\(", r"\bthrow\s+new\b", r"\bthrows\s+\w+", r"\bfinally\s*\{"],
      signals=[],
      prereqs=[("run_time_error", "An exception is the object a run-time error throws; catch intercepts it."),
               ("control_flow", "A thrown exception transfers control out of the try block to the matching catch."),
               ("block", "try, catch and finally each take a block with its own scope.")],
      parallels=[],
      miscs=[mis("CatchAlwaysRuns", "The catch block runs after every try block.", "catch runs only when an exception of its type is thrown inside the try block; otherwise it is skipped."),
             mis("TryResumesAfterCatch", "After the catch block, execution continues with the statement in try that failed.", "The rest of the try block is skipped; after catch, execution continues after the whole try-catch."),
             mis("ExceptionIsCompileError", "An exception is an error the compiler reports.", "An exception is thrown while the program runs; the compiler only checks that checked exceptions are caught or declared."),
             err("UncaughtException", "A thrown exception with no matching catch is ignored.", "It propagates to the caller; if nothing catches it the program prints a stack trace and stops.", "run-time exception", "Exception in thread \"main\" ... with a stack trace")],
      link=[],
      E="In everyday reading 'catch the error' sounds like fixing it and carrying on where one was. In Java catch receives the exception object and runs its own block; the failed statement is not retried.",
      T="Skips the rest of the try block in one trace and resumes it in the next, or runs the catch block when nothing was thrown.",
      N="Exception handling: try { statements } catch (ExceptionType e) { handler } with optional finally, plus throw new ExceptionType(...) to raise one.",
      S="The statements in try run in order; if one throws an exception, the remaining try statements are skipped and the first catch whose type matches runs; then execution continues after the try-catch. finally runs in every case. An uncaught exception ends the method and propagates to the caller.",
      LT="Run the try block statement by statement; on a throw jump to the matching catch, bind e, run it, then continue after the construct; without a throw skip every catch.",
      OP="try { int x = Integer.parseInt(\"abc\"); System.out.println(x); } catch (NumberFormatException e) { System.out.println(\"bad\"); } prints bad and never prints x.",
      OS="Variables assigned before the throwing statement keep their values; those assigned after it inside try are not assigned; e exists only inside catch.",
      P="try-catch guards input parsing and file access, turning a crash into a message or a retry; throw reports an invalid argument to the caller.",
      C="Moving the println inside try after the parse skips it on failure; catching Exception instead of NumberFormatException also catches other errors; removing the catch makes the program stop with a stack trace.",
      X="Catch the specific exception you can handle, keep the try block small, and let other exceptions propagate."),

 dict(id="wrapper_types", section="ext", topic="topic.ext.c",
      description="Integer, Double, Boolean, Character: object versions of the primitive types, converted automatically (boxing) and holding parse and constant methods",
      aliases=["Integer", "Double", "wrapper", "wrapper class", "boxing", "autoboxing", "unboxing"],
      patterns=[r"\b(?:Integer|Double|Boolean|Character|Long)\s+\w+\s*[=;]", r"\bnew\s+(?:Integer|Double|Boolean|Character|Long)\s*\(", r"\.(?:intValue|doubleValue|booleanValue|charValue|longValue)\s*\(", r"\b(?:Integer|Double|Long|Boolean)\.valueOf\s*\("],
      signals=[],
      prereqs=[("int", "Integer wraps an int value in an object."),
               ("double", "Double wraps a double value in an object."),
               ("primitive_vs_reference", "A wrapper variable is a reference that can be null and is compared with equals, unlike the primitive."),
               ("parsing", "Integer.parseInt and Double.parseDouble are static methods of the wrapper classes.")],
      parallels=[],
      miscs=[mis("WrapperEqualsOperator", "Two Integer variables with the same value are always ==.", "== compares references; equals compares values. Small values are cached so == may seem to work, then fails above 127."),
             mis("WrapperIsPrimitive", "Integer and int are the same type.", "Integer is an object type that can be null and can be stored in collections; int is a primitive. Java converts between them automatically, which is called boxing and unboxing."),
             err("UnboxingNull", "A null Integer used in arithmetic gives 0.", "Unboxing null throws NullPointerException.", "run-time exception", "int x = nullInteger; or arithmetic on a null Integer")],
      link=[],
      E="Since Integer prints like an int, novices treat it as the same type. It is an object: == compares identity, it may be null, and collections hold it where they cannot hold int.",
      T="Compares two Integer values with == in one place and with equals in another, or treats a wrapper as nullable in one line and as a number in the next.",
      N="Wrapper types: the classes Integer, Double, Boolean, Character and Long, each holding one primitive value as an object, with parse methods and MAX_VALUE/MIN_VALUE constants.",
      S="Integer n = 5; boxes the int into an object; int m = n; unboxes it. Integer.parseInt(s) and Integer.MAX_VALUE are static members. Two Integer objects are compared with equals; == compares references and is reliable only for the cached range -128 to 127.",
      LT="At an assignment or arithmetic between int and Integer the compiler inserts the conversion; a null Integer throws when unboxed.",
      OP="Integer a = 127, b = 127; a == b is true; Integer c = 128, d = 128; c == d is false but c.equals(d) is true; Integer.parseInt(\"42\") is 42.",
      OS="Boxing creates or reuses an object; unboxing copies the value out; a wrapper variable may hold null.",
      P="Wrappers let primitive values live in collections (ArrayList<Integer>) and carry the parse and constant methods used with command-line arguments.",
      C="Changing int to Integer lets the variable be null and changes what == means; changing == to equals makes the comparison correct for all values.",
      X="Use primitives for arithmetic, wrappers only where objects are required, and equals to compare wrapper values."),

 dict(id="collections", section="ext", topic="topic.ext.c",
      description="ArrayList<Integer> list = new ArrayList<>(); list.add(x); list.get(i); list.size(): a growable list of objects with methods instead of [] and length",
      aliases=["ArrayList", "list", "collection", "collections", "add", "size()", "get(i)"],
      patterns=[r"\b(?:ArrayList|LinkedList|HashMap|HashSet|TreeMap|List|Map|Set)\s*<", r"\.size\s*\(\s*\)", r"\bnew\s+(?:ArrayList|LinkedList|HashMap|HashSet)\b"],
      signals=[],
      prereqs=[("array_declaration", "A list plays the role of an array whose length can change; the two use different syntax."),
               ("method_call", "Every list operation is a method call: add, get, set, remove, size."),
               ("wrapper_types", "A list holds objects, so int values are stored as Integer."),
               ("import_statement", "ArrayList lives in java.util and needs an import.")],
      parallels=[],
      miscs=[mis("ListLengthIsField", "list.length gives the number of elements.", "size() is a method of a list; only arrays have the field length."),
             mis("ListIndexWithBrackets", "list[i] reads an element of an ArrayList.", "list.get(i) reads and list.set(i, v) writes; brackets are only for arrays."),
             mis("RemoveLeavesGap", "list.remove(i) leaves an empty slot at i.", "remove shifts the later elements down and size() decreases by one."),
             err("PrimitiveTypeArgument", "ArrayList<int> is allowed.", "Type arguments must be object types: ArrayList<Integer>.", "compile-time error", "unexpected type: int in a type argument")],
      link=[("ArrayListIsArray", "primary")],
      E="In everyday reading a list is like a row of boxes, so novices use the array syntax a[i] and length. An ArrayList is an object with methods: get, set, add, remove and size().",
      T="Calls size() in one line and .length in the next, or uses get(i) for reading but brackets for writing.",
      N="Collections: library classes such as ArrayList that hold a growing sequence of objects, used through methods add, get, set, remove and size.",
      S="new ArrayList<Integer>() is empty; add(x) appends and size() grows by one; get(i) returns the element at i (0 to size() - 1); set(i, v) replaces it; remove(i) deletes it and shifts the rest down. Elements are objects, so int is boxed to Integer.",
      LT="Apply each call in order to the same list object; indices are valid from 0 to size() - 1 at that moment.",
      OP="list.add(5); list.add(7); list.add(9); list.remove(1); gives size() 2 and get(1) is 9.",
      OS="Each add, set or remove changes the list in place; every variable referring to it sees the change.",
      P="A list collects values whose count is unknown in advance: reading all inputs until end of input, then processing them.",
      C="Replacing the ArrayList by an array fixes the length at creation; replacing remove(i) with set(i, null) keeps the size; iterating to size() while removing skips elements.",
      X="Use an ArrayList when the number of items grows while reading; use an array when the length is known."),
]

# ----------------------------------------------------------------------------- builders

def load_templates(kg):
    """Templated way fields and level-node texts, taken from an existing concept."""
    tpl = {}
    for e in kg["edges"]:
        if e["type"] != "has_level":
            continue
        for w in e["ways"]:
            k = (w["way"], w["rule_type"])
            if k not in tpl:
                tpl[k] = {f: w[f] for f in ("rule_type_name", "boundary", "correctness", "filled_from", "framework", "check_correct", "check_unambiguous", "check_high_level") if f in w}
    lv = {l["level"]: l for l in kg["learning_levels"] if l["concept"] == "string_concatenation"}
    return tpl, lv


def way(tpl, name, rt, rule, **extra):
    w = {"way": name, "rule_type": rt, "rule_type_name": tpl[(name, rt)]["rule_type_name"],
         "edge_logic": rule, "exact_rule": rule}
    for f in ("boundary", "correctness", "filled_from", "framework"):
        if f in tpl[(name, rt)]:
            w[f] = tpl[(name, rt)][f]
    w.update(extra)
    w["book_source"] = []
    w["rule_sources"] = [AUTH]
    w["rule_source_status"] = "unverified (author-added)"
    for f in ("check_correct", "check_unambiguous", "check_high_level"):
        w[f] = tpl[(name, rt)][f]
    return w


def src(rule):
    return {"rule": rule, "sources": [AUTH], "source_status": "unverified", "note": "author-added 2026-10-30"}


def build_concept(c, kg, tpl, lv, mis_by_id):
    cid = c["id"]
    words = cid.replace("_", " ")
    label = cid
    topic_title = TOPICS.get(c["topic"]) or next(t["label"] for t in kg["topics"] if t["id"] == c["topic"])
    section_title = "Built-in Types of Data" if c["section"] == "1.2" else SECTION["label"]
    new_miscs = [m for m in c["miscs"] if m["kind"] == "misconception"]
    new_errs = [m for m in c["miscs"] if m["kind"] == "error"]
    linked = [(mid, role) for mid, role in c["link"] if mid in mis_by_id]
    prereq_rules = [(s, r) for s, r in c["prereqs"]] + [(s, r) for s, r in c["parallels"]]

    rules_by_type = {
        "E": src(c["E"]),
        "M": [{"node": m["id"], "wrong": m["wrong"], "right": m["right"], "sources": [AUTH], "source_status": "unverified", "note": None} for m in new_miscs]
             + [{"node": mid, "wrong": mis_by_id[mid]["wrong_belief"], "right": mis_by_id[mid]["correct_rule"], "sources": [{"type": "kg", "note": "existing misconception node linked to this concept", "check": "existing"}], "source_status": "existing", "note": None} for mid, _ in linked if mis_by_id[mid]["kind"] == "misconception"],
        "T": src(c["T"]), "N": src(c["N"]), "S": src(c["S"]), "LT": src(c["LT"]), "OP": src(c["OP"]), "OS": src(c["OS"]),
        "R": [{"neighbour": s, "rule": r, "sources": [AUTH], "source_status": "unverified", "note": None} for s, r in prereq_rules],
        "P": src(c["P"]), "C": src(c["C"]),
        "D": [{"node": e["id"], "rule_broken": e["right"], "kind": e["error_kind"], "trigger": e["trigger"], "sources": [AUTH], "source_status": "unverified", "note": None} for e in new_errs]
             + [{"node": mid, "rule_broken": mis_by_id[mid]["correct_rule"], "kind": "error", "trigger": mis_by_id[mid]["wrong_belief"], "sources": [{"type": "kg", "check": "existing"}], "source_status": "existing", "note": None} for mid, _ in linked if mis_by_id[mid]["kind"] == "error"],
        "X": src(c["X"]),
    }
    concept = {
        "id": cid, "type": "concept", "section": c["section"], "section_title": section_title, "topic": c["topic"].replace("topic", "").lstrip("."),
        "topic_title": topic_title, "label": label, "description": c["description"],
        "rules": [{"id": f"{cid}.R1", "source": "reader4", "quote": c["S"], "quote_status": "author-added", "role": "supplementary"}],
        "misconceptions": [m["id"] for m in new_miscs] + [mid for mid, _ in linked if mis_by_id[mid]["kind"] == "misconception"],
        "errors": [e["id"] for e in new_errs] + [mid for mid, _ in linked if mis_by_id[mid]["kind"] == "error"],
        "book_status": "not taught in SW-1e chapter 1; added for code coverage (reader4 extension, 2026-10-30)",
        "book_location": None, "rules_by_type": rules_by_type, "previous_id": None,
        "reader": {"aliases": c["aliases"], "code_patterns": c["patterns"], "code_text": "masked", "command_patterns": [], "operator_symbols": [], "java_types": [],
                   "generic": False, "shown_by_declaration": False, "signals": c["signals"], "patterns_added_in": STAMP},
    }

    # level nodes
    levels = []
    for L, t in lv.items():
        n = copy.deepcopy(t)
        n["id"] = f"{cid}@{L}"
        n["concept"] = cid
        for f in ("criterion", "criterion_general", "deciding_question"):
            n[f] = n[f].replace("string concatenation", words)
        levels.append(n)

    # has_level edges with ways
    ways = {
        "L0": [way(tpl, "everyday_reading", "E", c["E"], boundary=f"Any correct, programming-specific statement about {words} makes the answer L1 or higher.")]
              + [way(tpl, "misconception", "M", f"wrong rule: {m['wrong']} Right rule: {m['right']}", linked_misconception=[m["node"]], scope="language",
                     literature_disagreement="Jimoyiannis 2011 codes some answers driven by a misconception as unistructural or multistructural, not prestructural.") for m in rules_by_type["M"]]
              + [way(tpl, "inconsistent_trace", "T", c["T"], linked_misconception=[m["node"] for m in rules_by_type["M"]], scope="language",
                     literature_disagreement="Teague & Lister 2014 treat an inconsistent trace as preoperational, not as a stable misconception.")],
        "L1": [way(tpl, "names_the_element", "N", c["N"]), way(tpl, "states_the_rule", "S", c["S"])],
        "L2": [way(tpl, "line_by_line_trace", "LT", c["LT"]), way(tpl, "output_prediction", "OP", c["OP"],
                   literature_disagreement="Lister 2004 and Fowler 2021 treat output prediction as a trace-level task; a bare correct output is not levelled here."),
               way(tpl, "one_step_execution", "OS", c["OS"])],
        "L3": [way(tpl, "relation_to_neighbour", "R", r, requires_concept=[s], edge=f"{s} -{'parallel' if (s, r) in c['parallels'] else 'prerequisite'}-> {cid}") for s, r in prereq_rules]
              + [way(tpl, "purpose_of_the_whole", "P", c["P"])],
        "L4": [way(tpl, "predict_a_change", "C", c["C"], linked_misconception=[m["node"] for m in rules_by_type["M"]],
                   literature_disagreement="Jimoyiannis 2011 and Vrachnos & Jimoyiannis 2017 code modification of given code as relational, not extended abstract.")]
              + [way(tpl, "diagnose_an_error", "D", f"{d['rule_broken']} Trigger: {d['trigger']}", linked_error=[d["node"]], error_kind=d["kind"], trigger_class=d["trigger"],
                     literature_disagreement="Lister 2011 places hypothesis-driven debugging at formal operational. Ahadi 2014 places patch-and-repatch at preoperational.") for d in rules_by_type["D"]]
              + [way(tpl, "transfer_to_a_new_program", "X", c["X"],
                     literature_disagreement="Jimoyiannis 2011 codes solving an unseen problem as extended abstract only when the student generalises the rule.")],
    }
    names = {"L0": "Prestructural", "L1": "Unistructural", "L2": "Multistructural", "L3": "Relational", "L4": "Extended abstract"}
    descr = {"L0": "the answer holds a rule that contradicts Java", "L1": "the answer states one correct rule without applying it",
             "L2": f"the answer applies the rules of {words} to every part of the code, in order", "L3": "the answer relates the parts", "L4": "the answer reasons beyond the given code"}
    rts = {"L0": ["E", "M", "T"], "L1": ["N", "S"], "L2": ["LT", "OP", "OS"], "L3": ["R", "P"], "L4": ["C", "D", "X"]}
    level_edges = [{"source": cid, "target": f"{cid}@{L}", "type": "has_level", "level": L, "rule_types": rts[L],
                    "logic": f"{words} -> {L} ({names[L]}): {descr[L]} ({len(ways[L])} ways).", "ways": ways[L]} for L in ("L0", "L1", "L2", "L3", "L4")]

    # relation edges
    rel_edges = []
    for s, r in c["prereqs"]:
        rel_edges.append({"source": s, "target": cid, "type": "prerequisite", "logic": r, "sources": ["reader4"], "evidence_type": "author-added; unverified",
                          "grounding": "none", "book_support": [], "final_check": {"verdict": "unverified", "action": "added", "passage_kind": None, "note": "reader4 extension 2026-10-30"}})
    for s, r in c["parallels"]:
        rel_edges.append({"source": cid, "target": s, "type": "parallel", "logic": r, "sources": ["reader4"], "evidence_type": "author-added; unverified",
                          "grounding": "none", "book_support": [], "final_check": {"verdict": "unverified", "action": "added", "passage_kind": None, "note": "reader4 extension 2026-10-30"}})

    # misconception / error nodes and edges
    mis_nodes, mis_edges = [], []
    for m in c["miscs"]:
        mis_nodes.append({"id": m["id"], "kind": m["kind"], "label": m["id"], "wrong_belief": m["wrong"], "correct_rule": m["right"],
                          "violates_rule": {"source": "reader4", "concept": cid, "rule_ids": [f"{cid}.R1"]}, "provenance": "author-added",
                          "literature_sources": [], "note": "reader4 extension 2026-10-30; unverified", "book_verdict": "not_in_book", "book_support": [],
                          "final_check": {"verdict": "unverified", "action": "added", "note": ""}, "type": m["kind"], "concepts": [cid]})
        mis_edges.append({"source": cid, "target": m["id"], "type": m["kind"], "logic": m["wrong"], "twin_logic": m["right"], "violates_rule": [f"{cid}.R1"],
                          "role": m["role"], "provenance": "author-added", "sources": ["reader4"], "evidence_type": "author knowledge of Java; unverified"})
    for mid, role in linked:
        rec = mis_by_id[mid]
        mis_edges.append({"source": cid, "target": mid, "type": rec["kind"], "logic": rec["wrong_belief"], "twin_logic": rec["correct_rule"],
                          "violates_rule": [f"{cid}.R1"], "role": role, "provenance": "author-added link to existing node", "sources": ["reader4"],
                          "evidence_type": "existing misconception node; link unverified"})
        rec.setdefault("concepts", [])
        if cid not in rec["concepts"]:
            rec["concepts"].append(cid)

    contains = {"source": c["topic"], "target": cid, "type": "contains", "logic": f"The topic '{topic_title}' introduces {cid}.", "sources": ["reader4"]}
    return concept, levels, level_edges, rel_edges, mis_nodes, mis_edges, contains


def extend(kg):
    tpl, lv = load_templates(kg)
    existing = {c["id"] for c in kg["concepts"]}
    mis_by_id = {m["id"]: m for m in kg["misconceptions_and_errors"]}
    added = []

    if not any(s["id"] == SECTION["id"] for s in kg["sections"]):
        kg["sections"].append(copy.deepcopy(SECTION))
    for tid, title in TOPICS.items():
        if title and not any(t["id"] == tid for t in kg["topics"]):
            kg["topics"].append({"id": tid, "layer": 1.5, "type": "topic", "section": "ext", "label": title, "book_quote": None,
                                 "book_quote_status": "none (construct beyond chapter 1)", "concepts": []})

    for c in CONCEPTS:
        if c["id"] in existing:
            continue
        for p in c["patterns"]:
            re.compile(p)
        for s in c["signals"]:
            re.compile(s["regex"])
        concept, levels, level_edges, rel_edges, mis_nodes, mis_edges, contains = build_concept(c, kg, tpl, lv, mis_by_id)
        kg["concepts"].append(concept)
        kg["learning_levels"].extend(levels)
        kg["edges"].extend(level_edges + rel_edges + mis_edges + [contains])
        for m in mis_nodes:
            if m["id"] not in mis_by_id:
                kg["misconceptions_and_errors"].append(m)
                mis_by_id[m["id"]] = m
        topic = next(t for t in kg["topics"] if t["id"] == c["topic"])
        topic["concepts"].append(c["id"])
        existing.add(c["id"])
        added.append({"concept": c["id"], "topic": c["topic"], "prerequisites": [s for s, _ in c["prereqs"]], "parallels": [s for s, _ in c["parallels"]],
                      "new_misconceptions": [m["id"] for m in mis_nodes if m["kind"] == "misconception"], "new_errors": [m["id"] for m in mis_nodes if m["kind"] == "error"],
                      "linked_existing": [mid for mid, _ in c["link"]]})

    # dependency order check: every edge endpoint must exist
    ids = {c["id"] for c in kg["concepts"]} | {l["id"] for l in kg["learning_levels"]} | set(mis_by_id) | {t["id"] for t in kg["topics"]} | {s["id"] for s in kg["sections"]}
    for e in kg["edges"]:
        assert e["source"] in ids, e
        assert e["target"] in ids, e

    kg["counts"] = {
        "concepts": len(kg["concepts"]),
        "misconception_nodes": sum(1 for m in kg["misconceptions_and_errors"] if m["kind"] == "misconception"),
        "error_nodes": sum(1 for m in kg["misconceptions_and_errors"] if m["kind"] == "error"),
        "prerequisite": sum(1 for e in kg["edges"] if e["type"] == "prerequisite"),
        "parallel": sum(1 for e in kg["edges"] if e["type"] == "parallel"),
        "misconception": sum(1 for e in kg["edges"] if e["type"] == "misconception"),
        "error": sum(1 for e in kg["edges"] if e["type"] == "error"),
        "has_level": sum(1 for e in kg["edges"] if e["type"] == "has_level"),
        "learning_level_nodes": len(kg["learning_levels"]),
        "ways_in_has_level_edge_logic": sum(len(e["ways"]) for e in kg["edges"] if e["type"] == "has_level"),
    }
    if added:
        kg["reader"].setdefault("concepts_added_reader4", []).extend(added)
        kg["version"] = f"3.9.5-reader4-ext ({len(kg['concepts'])} concepts: reader4 + {len(kg['reader']['concepts_added_reader4'])} concepts for constructs beyond chapter 1 seen in student code, 2026-10-30)"
    return added


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--kg", default="data/raw/chapter1_kg.json")
    a = ap.parse_args(argv)
    p = Path(a.kg)
    kg = json.loads(p.read_text(encoding="utf-8"))
    added = extend(kg)
    p.write_text(json.dumps(kg, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"added {len(added)} concepts; now {kg['counts']}")
    for a_ in added:
        print(" ", a_["concept"], "<-", a_["prerequisites"], "| new:", a_["new_misconceptions"] + a_["new_errors"], "| linked:", a_["linked_existing"])


if __name__ == "__main__":
    main()
