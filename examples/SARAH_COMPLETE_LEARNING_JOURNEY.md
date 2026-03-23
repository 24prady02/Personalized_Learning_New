# 🎓 Sarah's Complete Learning Journey - Multi-Session Teaching Example

This shows **exactly how the system teaches Sarah** across multiple sessions, not just giving her answers!

---

## 👩‍💻 Meet Sarah

- **Background**: 19-year-old CS freshman
- **Starting Level**: Knows functions and loops, new to recursion
- **Learning Style**: Systematic, high conscientiousness
- **Personality**: Organized, persistent, stays calm under pressure

---

## 📅 **SESSION 1: First Encounter (Monday, 2:30 PM)**

### Sarah's Code:
```python
def factorial(n):
    return n * factorial(n - 1)

print(factorial(5))
```

### Error:
```
RecursionError: maximum recursion depth exceeded
```

### Sarah's Actions:
```python
["code_edit", "run_test", "run_test", "run_test", "search_documentation"]
# Stuck for 2 minutes, confused
```

---

### 🤖 System Analysis:

```python
ANALYSIS = {
    "code_understanding": {
        "intent": "factorial_using_recursion",
        "missing": "base_case",
        "error_type": "infinite_recursion"
    },
    
    "knowledge_state": {
        "functions": 0.85,        # Knows functions ✓
        "recursion": 0.35,        # Learning
        "base_case": 0.18,        # ❌ CRITICAL GAP!
        "conditionals": 0.78      # Knows if statements ✓
    },
    
    "emotional_state": "confused_but_persistent",
    
    "personality_inferred": {
        "conscientiousness": 0.82,  # Very organized
        "openness": 0.55,           # Moderate
        "neuroticism": 0.32         # Calm
    },
    
    "teaching_stage": "INTRODUCTION",  # First time seeing this
    "scaffolding_needed": 5,           # Maximum support
    
    "decision": "Don't just give answer - TEACH the concept!"
}
```

---

### 📚 System's Teaching Response (Session 1):

```
════════════════════════════════════════════════════════
🎓 LEARNING: Base Case in Recursion
Stage: Introduction (Step 1 of 4)
════════════════════════════════════════════════════════

Hi Sarah! 👋

I see you're learning recursion - that's exciting! Let me help you 
understand a critical concept you're missing: the BASE CASE.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌟 Real-World Analogy:

Think of recursion like Russian nesting dolls:
- You open the big doll → find a smaller doll inside
- You open that → find an even smaller one
- You keep going until → you reach the TINIEST doll

That tiniest doll is the BASE CASE - it's when you STOP opening!

Without that final small doll, you'd be trying to open dolls forever!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 What is a Base Case? (From CS Knowledge Graph)

A base case is a terminating condition that stops recursive calls.
It's the simplest version of the problem that can be solved directly
without recursion.

Every recursive function MUST have:
1. BASE CASE - when to stop (you're missing this!)
2. RECURSIVE CASE - calling itself (you have this!)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 Let's Look at Your Code:

Your code:
```python
def factorial(n):
    return n * factorial(n - 1)  ← Always calls itself!
```

What happens:
factorial(5) → calls factorial(4)
factorial(4) → calls factorial(3)
factorial(3) → calls factorial(2)
factorial(2) → calls factorial(1)
factorial(1) → calls factorial(0)
factorial(0) → calls factorial(-1)
factorial(-1) → calls factorial(-2)
... keeps going FOREVER! 💥

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Here's How to Fix It:

I'll show you step-by-step, then you'll practice:

```python
def factorial(n):
    # BASE CASE - This is what you need to add!
    if n <= 1:          # ← Check: are we at the smallest case?
        return 1        # ← Yes! Return 1 (factorial of 0 or 1 is 1)
    
    # RECURSIVE CASE - You already have this part!
    return n * factorial(n - 1)
```

Now it works:
factorial(5) → 5 * factorial(4)
factorial(4) → 4 * factorial(3)
factorial(3) → 3 * factorial(2)
factorial(2) → 2 * factorial(1)
factorial(1) → **STOPS HERE** (base case!) returns 1
Then multiplies back: 2×1=2, 3×2=6, 4×6=24, 5×24=120 ✓

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 YOUR TURN - Guided Practice:

I've started a fibonacci function for you. Can you add the base case?

```python
def fibonacci(n):
    # TODO: Add base case here
    # HINT: fibonacci(0) = 0 and fibonacci(1) = 1
    if ____________:  # What should the condition be?
        return ____________  # What should it return?
    
    # Recursive case
    return fibonacci(n-1) + fibonacci(n-2)
```

[Fill in the blanks] [Need a hint?] [See solution]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❓ Check Your Understanding:

Before we continue, answer these quick questions:

1. What does a base case do?
   [Your answer here]

2. What happens without a base case?
   [Your answer here]

3. For factorial, what is the base case?
   [Your answer here]

[Submit Answers]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Your Learning Progress:

Concept: Base Case
├─ Understanding: 40% → 60% (improving! 📈)
├─ Current Stage: Introduction (1 of 4)
├─ Next Stage: Guided Practice
└─ Estimated time to mastery: 2-3 more sessions

Keep going - you're making great progress! 🚀

[Continue Learning] [Take a Break] [Ask Question]

════════════════════════════════════════════════════════
```

---

### 📝 Sarah's Response (Session 1):

```python
# Sarah completes the fibonacci exercise:
sarah_answer = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

# She answers understanding questions:
sarah_answers = {
    "q1": "A base case tells the function when to stop calling itself",
    "q2": "Without it, the function keeps calling forever and crashes",
    "q3": "if n <= 1: return 1"
}

# System assesses her understanding
assessment = formative_assessment.assess(sarah_answers, "base_case")
# Result: 75% understanding - Good! Can move forward
```

### ✅ Session 1 Outcome:

```python
learning_update = {
    "concept": "base_case",
    "mastery": 0.18 → 0.65,  # Big jump! 📈
    "completed": True,
    "time_spent": "18 minutes",
    "next_session": "Guided practice with less support",
    "ready_for_next_stage": True
}

print("✓ Session 1 complete!")
print("  Mastery improved: 18% → 65%")
print("  Sarah now understands BASE CASE concept!")
print("  Next: Practice with decreasing scaffolding")
```

---

## 📅 **SESSION 2: Guided Practice (Wednesday, 3:15 PM - 2 days later)**

### Sarah Returns:

She's working on a new problem and encounters recursion again.

```python
# New problem: Sum of array using recursion
sarah_code = """
def sum_array(arr):
    return arr[0] + sum_array(arr[1:])

print(sum_array([1, 2, 3, 4, 5]))
```

### Error:
```
IndexError: list index out of range
```

---

### 🤖 System Analysis (Session 2):

```python
ANALYSIS = {
    "code_understanding": {
        "intent": "sum_array_recursive",
        "missing": "base_case_for_empty_array",
        "same_concept_as_before": True  # Still base case!
    },
    
    "knowledge_state": {
        "base_case": 0.65,  # From last session
        "recursion": 0.55,  # Improved
        "array_operations": 0.82
    },
    
    "learning_history": {
        "learned_base_case": "2 days ago",
        "previous_mastery": 0.65,
        "current_stage": "GUIDED_PRACTICE",
        "scaffolding_level": 3  # Medium support
    },
    
    "decision": "She remembers the concept but needs practice applying it!"
}
```

---

### 📚 System's Teaching Response (Session 2):

```
════════════════════════════════════════════════════════
🎓 PRACTICING: Base Case (Session 2)
Stage: Guided Practice (Step 2 of 4)
Scaffolding: Medium Support
════════════════════════════════════════════════════════

Great to see you again, Sarah! 👋

I notice you're applying recursion to a new problem - excellent!

You learned about base cases 2 days ago. Let's see if you can
identify what's needed here!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤔 Guided Discovery Questions:

Before I tell you the answer, let's think through this together:

Question 1: Your function gets an array and recursively sums it.
What's the SIMPLEST array you could get?

    [Think about it...] [Show hint]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[After Sarah thinks/clicks hint]

💡 Hint: The simplest array is an EMPTY array []

Question 2: What should sum_array([]) return?

    [Your answer: _____] [Show hint]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[After Sarah answers]

✓ Correct! sum_array([]) should return 0 (sum of nothing is 0)

That's your BASE CASE! 🎯

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Now You Try:

Add the base case to your function:

```python
def sum_array(arr):
    # Add base case here
    # What should you check? What should you return?
    
    return arr[0] + sum_array(arr[1:])
```

[Your code editor]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Hints Available (click if stuck):
[Hint 1: 30% revealed] [Hint 2: 60% revealed] [Hint 3: 90% revealed]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Your Progress:

Base Case Mastery: 65% → Working towards 80%
Sessions completed: 2
Practice problems: 1 of 3

[Continue] [Review Previous Lesson] [Ask Question]

════════════════════════════════════════════════════════
```

---

### 📝 Sarah's Response (Session 2):

```python
# Sarah writes (with minimal hints):
sarah_solution = """
def sum_array(arr):
    if len(arr) == 0:
        return 0
    return arr[0] + sum_array(arr[1:])
"""

# Tests it
result = sarah_solution.sum_array([1, 2, 3, 4, 5])
# Output: 15 ✓ Correct!

# System assesses
assessment = {
    "correct": True,
    "hints_used": 1,  # Used 1 hint
    "time_taken": 240,  # 4 minutes
    "demonstrates_understanding": True
}
```

### ✅ Session 2 Outcome:

```python
learning_update = {
    "mastery": 0.65 → 0.78,  # Improved! 📈
    "applied_concept_in_new_context": True,  # ⭐ Transfer learning!
    "hints_used": 1,  # Less support needed
    "ready_for_less_scaffolding": True
}

print("✓ Session 2 complete!")
print("  Sarah successfully applied base case to NEW problem!")
print("  Mastery: 65% → 78%")
print("  Transfer learning demonstrated! ⭐")
print("  Next: Independent practice")
```

---

## 📅 **SESSION 3: Independent Practice (Friday, 4:00 PM - 2 days later)**

### New Challenge:

```python
# System gives Sarah harder problem with NO hints shown initially
problem = """
Write a recursive function to reverse a string.

Example:
reverse('hello') should return 'olleh'
reverse('a') should return 'a'

Starter code:
def reverse(s):
    # Your code here
    pass
"""
```

---

### 🤖 System Analysis (Session 3):

```python
ANALYSIS = {
    "learning_history": {
        "previous_mastery": 0.78,
        "sessions_completed": 2,
        "last_session": "2 days ago",
        "concept_retention": 0.85,  # Still remembers!
        "stage": "INDEPENDENT_PRACTICE",
        "scaffolding_level": 1  # Minimal support
    },
    
    "decision": "Let her try independently - only help if stuck > 2 minutes"
}
```

---

### 📚 System's Teaching Response (Session 3):

```
════════════════════════════════════════════════════════
🎓 CHALLENGE: Apply Your Knowledge
Stage: Independent Practice (Step 3 of 4)
Scaffolding: Minimal (try on your own first!)
════════════════════════════════════════════════════════

Hi Sarah! Ready for a challenge? 💪

You've learned about base cases in factorial and sum_array.
Now apply that knowledge to a NEW problem!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Challenge: Reverse a String Recursively

reverse('hello') → 'olleh'
reverse('abc') → 'cba'

Your task: Write it using recursion (with a base case!)

[Code Editor - Sarah works independently]

```python
def reverse(s):
    # Your code here




```

[Run Tests] [Submit Solution]

⏱️ Try for at least 2 minutes before asking for hints!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[After 2 minutes 30 seconds - Sarah hasn't submitted]

💭 Thinking through the problem? That's good!

Quick reminder (not a full hint):
- What's the simplest string? 
- What should reverse('') return?

[Continue working] [Request hint]

════════════════════════════════════════════════════════
```

---

### 📝 Sarah's Response (Session 3):

```python
# After 3 minutes 45 seconds:
sarah_solution = """
def reverse(s):
    if len(s) == 0:  # BASE CASE!
        return ''
    return reverse(s[1:]) + s[0]
"""

# Tests:
reverse('hello')  # Output: 'olleh' ✓
reverse('')       # Output: '' ✓
reverse('a')      # Output: 'a' ✓

# ALL CORRECT! And she did it mostly independently!
```

### ✅ System's Response:

```
════════════════════════════════════════════════════════
🎉 EXCELLENT WORK, SARAH!
════════════════════════════════════════════════════════

✓ Solution is correct!
✓ You identified the base case correctly (empty string)
✓ You applied the concept to a NEW problem
✓ You did it with minimal hints!

This shows you really UNDERSTAND base cases! 🌟

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Your Learning Progress:

Base Case Mastery: 78% → 88% 📈
- ✓ Can explain the concept
- ✓ Can identify in examples  
- ✓ Can apply to new problems ⭐

Recursion Understanding: 55% → 72%

Overall Progress:
████████████████░░░░ 88% mastered!

You're almost ready for the mastery check! Keep it up! 🚀

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎓 What You've Learned:

Session 1: Introduction to base case (factorial)
Session 2: Applied to different problem (sum_array)
Session 3: Independent application (reverse string)

Next Session: Mastery check + move to next concept!

[View Learning Path] [Practice More] [Next Concept]

════════════════════════════════════════════════════════
```

---

## 📅 **SESSION 4: Mastery Check (Monday, 2:00 PM - 3 days later)**

### Spaced Repetition:

System waits 3 days to check if Sarah retained the knowledge.

---

### 📚 System's Teaching Response (Session 4):

```
════════════════════════════════════════════════════════
✅ MASTERY CHECK: Base Case
Stage: Final Assessment (Step 4 of 4)
════════════════════════════════════════════════════════

Welcome back, Sarah! 🎓

You've done great work learning about base cases. 
Let's verify you've truly mastered it!

This assessment checks if you can:
✓ Remember the concept (even after 3 days)
✓ Apply it independently
✓ Debug errors related to it
✓ Explain it clearly

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 Assessment (4 parts):

Part 1: Explain (in your own words)
❓ What is a base case and why is it needed in recursion?

[Text box for explanation]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Part 2: Identify
❓ Find the base case in this code:

```python
def power(x, n):
    if n == 0:
        return 1
    return x * power(x, n-1)
```

[Highlight the base case]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Part 3: Debug
❓ Fix this buggy recursive function:

```python
def countdown(n):
    print(n)
    countdown(n - 1)  # Bug: missing base case!
```

[Fix the code]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Part 4: Create
❓ Write a recursive function to calculate the sum of digits.
   sum_digits(123) should return 6 (1+2+3)

[Code editor - completely blank]

No hints available - show me what you've learned!

[Submit for grading]

════════════════════════════════════════════════════════
```

---

### 📝 Sarah's Mastery Check Response:

```python
sarah_mastery_responses = {
    "part1": """
    A base case is the stopping condition in recursion. It tells the 
    function when to stop calling itself. Without it, the function 
    would call itself forever and crash with a RecursionError.
    """,
    # ✓ Excellent explanation!
    
    "part2": """
    if n == 0:
        return 1
    """,
    # ✓ Correctly identified!
    
    "part3": """
    def countdown(n):
        if n <= 0:  # BASE CASE added
            return
        print(n)
        countdown(n - 1)
    """,
    # ✓ Correctly fixed!
    
    "part4": """
    def sum_digits(n):
        if n == 0:  # BASE CASE
            return 0
        return (n % 10) + sum_digits(n // 10)
    """,
    # ✓ Correctly implemented in completely new context!
}
```

---

### ✅ System's Assessment:

```python
mastery_assessment = {
    "part1_score": 1.0,  # Perfect explanation
    "part2_score": 1.0,  # Correct identification
    "part3_score": 1.0,  # Correct debugging
    "part4_score": 0.95, # Excellent creation (minor style point)
    
    "overall_score": 0.98,  # 98%!
    
    "mastery_achieved": True,  # ✓ MASTERED!
    
    "demonstrates": {
        "remembers": True,      # After 3 days
        "understands": True,    # Can explain clearly
        "applies": True,        # Can use in practice
        "analyzes": True,       # Can debug
        "creates": True,        # Can create new solutions
        "transfers": True       # Can apply to new contexts
    }
}
```

---

### 🎉 System's Congratulations:

```
════════════════════════════════════════════════════════
🎉 CONGRATULATIONS, SARAH!
════════════════════════════════════════════════════════

You've MASTERED the concept of base case! 🌟

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Your Achievement:

Concept: Base Case in Recursion
Final Mastery: 98% ✅

Your learning journey:
Session 1 (Mon): Introduction → 18% to 65%
Session 2 (Wed): Guided Practice → 65% to 78%
Session 3 (Fri): Independent Practice → 78% to 88%
Session 4 (Mon): Mastery Check → 88% to 98% ✓

Total time: 4 sessions over 1 week
Total practice time: 52 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌟 What You Can Now Do:

✓ Explain what base cases are
✓ Identify base cases in code
✓ Write base cases for recursive functions
✓ Debug missing base case errors
✓ Apply concept to new problems
✓ Create your own recursive solutions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎓 Certificate Earned:

╔═══════════════════════════════════════════════╗
║                                               ║
║      Base Case Mastery Certificate           ║
║                                               ║
║      Awarded to: Sarah                        ║
║      Mastery Level: 98%                       ║
║      Date: November 4, 2024                   ║
║                                               ║
╚═══════════════════════════════════════════════╝

[Download Certificate] [Share Achievement]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 What's Next?

Now that you understand base cases, you're ready for:

1. Advanced Recursion (tail recursion, memoization)
2. Recursive Data Structures (trees, linked lists)
3. Divide and Conquer Algorithms

Recommended next lesson: "Understanding Call Stack"
Estimated time: 45 minutes

[Start Next Lesson] [Practice More Recursion] [View Learning Path]

════════════════════════════════════════════════════════
```

---

## 📈 **SARAH'S LEARNING PROGRESSION**

```
Mastery Over Time:

100% |                                          ✓ (98%)
     |                                      ✓ (88%)
 80% |                             ✓ (78%)
     |                    ✓ (65%)
 60% |                                          
     |                                          
 40% |                                          
     |                                          
 20% | ✗ (18%)                                  
     |                                          
  0% |_____|_____|_____|_____|_____|_____|_____|
     Mon   Tue   Wed   Thu   Fri   Sat   Sun   Mon
     
     Session 1  Session 2     Session 3  Session 4
     (Intro)    (Guided)      (Indep.)   (Mastery)


Learning Characteristics:
- Scaffolding: 5 → 3 → 1 → 0 (gradually removed)
- Hints used: Many → Some → Few → None
- Time to solve: 18min → 12min → 8min → 6min
- Transfer ability: 0% → 50% → 85% → 95%
```

---

## 🎯 **Key Teaching Mechanisms Used**

### 1. **Scaffolding (Gradual Support Removal)**

| Session | Support Level | What System Provided |
|---------|---------------|---------------------|
| 1 | Maximum (5) | Full explanation, templates, step-by-step |
| 2 | Medium (3) | Guided questions, hints available |
| 3 | Low (1) | Independent work, hints only if stuck |
| 4 | None (0) | Assessment, no help |

### 2. **Formative Assessment (Check Understanding)**

After EACH session:
```python
# Not just "did you complete it?"
# But "do you UNDERSTAND it?"

checks = [
    "Explain in your own words",
    "Identify in new examples",
    "Apply to different problem",
    "Debug related errors"
]
```

### 3. **Spaced Repetition**

```python
Session 1 → Wait 2 days → Session 2 → Wait 2 days → Session 3 → Wait 3 days → Session 4

# System uses spaced repetition algorithm:
review_intervals = [2 days, 2 days, 3 days, 1 week, 2 weeks, 1 month]

# Helps move knowledge to long-term memory
```

### 4. **Adaptive Difficulty**

```python
# Problems get harder as Sarah improves:

Session 1: factorial (easiest - given example)
Session 2: sum_array (moderate - similar pattern)
Session 3: reverse_string (harder - different pattern)
Session 4: sum_digits (hardest - completely novel)
```

### 5. **Transfer Learning Assessment**

```python
# System doesn't just teach ONE example
# It ensures Sarah can TRANSFER to new contexts:

factorial → sum_array → reverse_string → sum_digits
   ↓            ↓             ↓              ↓
 (intro)    (similar)    (different)    (novel)

# Tests: Can she recognize base case need in any recursive problem?
```

---

## 💡 **Why This Works (Pedagogical Research)**

### Based on Proven Learning Science:

1. **Bloom's Taxonomy** - Progress from remember → understand → apply → analyze → create

2. **Zone of Proximal Development** (Vygotsky) - Teach just beyond current ability with support

3. **Cognitive Load Theory** - Don't overwhelm; break into manageable chunks

4. **Spaced Repetition** - Review over increasing intervals for retention

5. **Mastery Learning** - Don't move forward until concept is solid

6. **Formative Assessment** - Continuous feedback, not just final test

---

## 🎯 **Summary: How System TEACHES Sarah**

| What Normal Tutors Do | What This System Does |
|-----------------------|----------------------|
| Give answer once | Multi-session teaching progression |
| Same for everyone | Personalized to Sarah's learning style |
| Static hints | Progressive hints (10% → 100%) |
| One example | Multiple problems with increasing difficulty |
| Hope they understand | Formative assessment at each step |
| Move on quickly | Wait until mastery (>85%) before advancing |
| Forget to review | Spaced repetition over days/weeks |

---

## 📚 **Complete Code Flow**

```python
# src/teaching/teaching_engine.py

# Session 1: Introduction
teaching_engine.teach_concept(
    student_id="sarah",
    concept="base_case",
    stage="introduction"
)
# → Full explanation, analogy, guided practice
# → Sarah's mastery: 18% → 65%

# Session 2: Guided Practice
teaching_engine.teach_concept(
    student_id="sarah",
    concept="base_case",
    stage="guided_practice"
)
# → Less support, Sarah applies to new problem
# → Sarah's mastery: 65% → 78%

# Session 3: Independent
teaching_engine.teach_concept(
    student_id="sarah",
    concept="base_case",
    stage="independent_practice"
)
# → Minimal support, Sarah works alone
# → Sarah's mastery: 78% → 88%

# Session 4: Mastery Check
teaching_engine.teach_concept(
    student_id="sarah",
    concept="base_case",
    stage="mastery_check"
)
# → No support, comprehensive assessment
# → Sarah's mastery: 88% → 98% ✓ MASTERED!

# System automatically plans next concept
next_lesson = curriculum.generate_next_lesson(
    student_id="sarah",
    completed_concepts=["base_case"],
    target="advanced_recursion"
)
```

---

## 🎉 **Result**

**Sarah didn't just get the answer** - she **learned the concept deeply** through:

✅ Multiple sessions with decreasing support
✅ Spaced practice over 1 week
✅ Transfer to new problems
✅ Continuous understanding checks
✅ Personalized to her learning style
✅ Adaptive difficulty
✅ Real mastery (98% vs just "completed")

**Now Sarah can:**
- ✅ Solve ANY recursion problem with base cases
- ✅ Debug base case errors independently
- ✅ Teach the concept to others
- ✅ Apply it in new contexts

**That's REAL teaching!** 🎓🚀
