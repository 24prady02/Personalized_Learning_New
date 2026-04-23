"""Test how correctness is determined without training"""

from feature_test_results.enhanced_metrics import SimulatedCodeBERT, SimulatedDINAModel

# Test code examples
correct_code = """
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
"""

buggy_code = """
def factorial(n):
    return n * factorial(n - 1)  # Missing base case
"""

syntax_error_code = """
def factorial(n)
    return n * factorial(n - 1)  # Missing colon
"""

codebert = SimulatedCodeBERT()

print("="*60)
print("HOW CORRECTNESS IS DETERMINED (Without Training)")
print("="*60)

print("\n1. CORRECT CODE:")
result = codebert.analyze_code(correct_code)
print(f"   Errors found: {result['error_count']}")
print(f"   Correctness score: {result['correctness_score']}")
print(f"   Code quality: {result['code_quality']}")
print(f"   Considered 'correct': {result['correctness_score'] > 0.8}")

print("\n2. BUGGY CODE (Logic Error):")
result = codebert.analyze_code(buggy_code)
print(f"   Errors found: {result['error_count']}")
print(f"   Syntax errors: {len(result['syntax_errors'])}")
print(f"   Logic errors: {len(result['logic_errors'])}")
print(f"   Correctness score: {result['correctness_score']}")
print(f"   Code quality: {result['code_quality']}")
print(f"   Considered 'correct': {result['correctness_score'] > 0.8}")

print("\n3. SYNTAX ERROR CODE:")
result = codebert.analyze_code(syntax_error_code)
print(f"   Errors found: {result['error_count']}")
print(f"   Syntax errors: {len(result['syntax_errors'])}")
for err in result['syntax_errors']:
    print(f"     - {err['message']}")
print(f"   Correctness score: {result['correctness_score']}")
print(f"   Code quality: {result['code_quality']}")
print(f"   Considered 'correct': {result['correctness_score'] > 0.8}")

print("\n" + "="*60)
print("KEY INSIGHT:")
print("="*60)
print("""
The system does NOT actually:
  ❌ Run/execute the code
  ❌ Test if it solves the problem
  ❌ Understand semantic correctness
  ❌ Verify against test cases

It ONLY checks for:
  ✅ Obvious syntax errors (missing colons, unmatched parentheses)
  ✅ Obvious logic errors (infinite loops, return outside function)

If NO obvious errors are found:
  → correctness_score = 1.0
  → Code is considered "correct"
  → Mastery increases by +0.15

This is a LIMITATION:
  - Buggy code with no syntax errors → Still considered "correct"
  - Code that doesn't solve the problem → Still considered "correct"
  - Only obvious errors are caught
""")















