"""
Generate 10 Sample Multi-Turn Conversations
Each conversation has 5-6 turns with random student inputs
Uses real system analysis and Groq API for responses
"""

import yaml
import os
import json
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import torch

from src.orchestrator.orchestrator import InterventionOrchestrator
from src.models.hvsae.model import HVSAE
from groq import Groq
from generate_multi_turn_conversation import MultiTurnConversationGenerator


# Sample student scenarios with different programming problems
STUDENT_SCENARIOS = [
    {
        "problem_type": "recursion_base_case",
        "turns": [
            {
                "code": """def factorial(n):
    return n * factorial(n - 1)

print(factorial(5))""",
                "error_message": "RecursionError: maximum recursion depth exceeded",
                "question": "Why is my code giving me a RecursionError? Can you show me a diagram?",
                "action_sequence": ["code_edit", "run_test", "run_test", "run_test", "search_documentation"],
                "time_deltas": [15.0, 2.0, 3.0, 2.5, 45.0],
                "time_stuck": 67.5
            },
            {
                "code": """def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))""",
                "error_message": "",
                "question": "Great! It works now. But can you explain why we need the base case?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [30.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """def fibonacci(n):
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))""",
                "error_message": "RecursionError: maximum recursion depth exceeded",
                "question": "I'm trying to write Fibonacci but getting the same error. What am I missing?",
                "action_sequence": ["code_edit", "run_test", "run_test", "code_edit"],
                "time_deltas": [20.0, 2.0, 3.0, 25.0],
                "time_stuck": 50.0
            },
            {
                "code": """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))""",
                "error_message": "",
                "question": "It works! But it's very slow. Is there a better way?",
                "action_sequence": ["code_edit", "run_test", "search_documentation"],
                "time_deltas": [25.0, 2.0, 30.0],
                "time_stuck": 0.0
            },
            {
                "code": """def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))""",
                "error_message": "",
                "question": "Can you explain memoization? I heard it can make recursion faster.",
                "action_sequence": ["search_documentation", "code_edit"],
                "time_deltas": [40.0, 35.0],
                "time_stuck": 0.0
            }
        ]
    },
    {
        "problem_type": "array_index_error",
        "turns": [
            {
                "code": """arr = [1, 2, 3, 4, 5]
for i in range(len(arr) + 1):
    print(arr[i])""",
                "error_message": "IndexError: list index out of range",
                "question": "Why am I getting an IndexError? The array has 5 elements.",
                "action_sequence": ["code_edit", "run_test", "run_test", "code_edit"],
                "time_deltas": [10.0, 2.0, 3.0, 15.0],
                "time_stuck": 30.0
            },
            {
                "code": """arr = [1, 2, 3, 4, 5]
for i in range(len(arr)):
    print(arr[i])""",
                "error_message": "",
                "question": "Thanks! But why does range(len(arr)) work but range(len(arr) + 1) doesn't?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [20.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """def get_middle(arr):
    return arr[len(arr) // 2]

print(get_middle([1, 2, 3]))""",
                "error_message": "",
                "question": "I wrote a function to get the middle element. Is this correct?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [15.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """def get_middle(arr):
    return arr[len(arr) // 2]

print(get_middle([1, 2]))""",
                "error_message": "",
                "question": "What happens if the array has an even number of elements?",
                "action_sequence": ["code_edit", "run_test", "code_edit"],
                "time_deltas": [12.0, 2.0, 18.0],
                "time_stuck": 0.0
            },
            {
                "code": """def get_middle(arr):
    if len(arr) == 0:
        return None
    return arr[len(arr) // 2]

print(get_middle([]))""",
                "error_message": "",
                "question": "I added a check for empty arrays. Is this good practice?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [20.0, 2.0],
                "time_stuck": 0.0
            }
        ]
    },
    {
        "problem_type": "variable_scope",
        "turns": [
            {
                "code": """x = 10

def change_x():
    x = 20
    print(x)

change_x()
print(x)""",
                "error_message": "",
                "question": "Why does x still print 10 after calling change_x()? I set it to 20 inside the function.",
                "action_sequence": ["code_edit", "run_test", "run_test", "search_documentation"],
                "time_deltas": [12.0, 2.0, 3.0, 40.0],
                "time_stuck": 57.0
            },
            {
                "code": """x = 10

def change_x():
    global x
    x = 20
    print(x)

change_x()
print(x)""",
                "error_message": "",
                "question": "I added 'global x' and now it works! Can you explain what 'global' does?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [25.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """def counter():
    count = 0
    count += 1
    return count

print(counter())
print(counter())""",
                "error_message": "",
                "question": "I want to create a counter that remembers its value. Why does this always return 1?",
                "action_sequence": ["code_edit", "run_test", "code_edit"],
                "time_deltas": [15.0, 2.0, 20.0],
                "time_stuck": 37.0
            },
            {
                "code": """def counter():
    if not hasattr(counter, 'count'):
        counter.count = 0
    counter.count += 1
    return counter.count

print(counter())
print(counter())""",
                "error_message": "",
                "question": "I used a function attribute. Is this the right way to do it?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [30.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

c = make_counter()
print(c())
print(c())""",
                "error_message": "",
                "question": "I learned about closures! Can you explain how this works?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [35.0, 2.0],
                "time_stuck": 0.0
            }
        ]
    },
    {
        "problem_type": "type_error",
        "turns": [
            {
                "code": """def add(a, b):
    return a + b

result = add("5", 3)
print(result)""",
                "error_message": "TypeError: can only concatenate str (not \"int\") to str",
                "question": "Why can't I add a string and an integer? In math, 5 + 3 = 8.",
                "action_sequence": ["code_edit", "run_test", "run_test", "search_documentation"],
                "time_deltas": [8.0, 2.0, 3.0, 35.0],
                "time_stuck": 48.0
            },
            {
                "code": """def add(a, b):
    return int(a) + b

result = add("5", 3)
print(result)""",
                "error_message": "",
                "question": "I converted the string to int. But what if the string isn't a number?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [20.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """def add(a, b):
    try:
        return int(a) + b
    except ValueError:
        return "Error: Cannot convert to number"

print(add("5", 3))
print(add("hello", 3))""",
                "error_message": "",
                "question": "I added error handling. Is this the right approach?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [25.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """def add(a, b):
    if isinstance(a, str):
        a = int(a)
    if isinstance(b, str):
        b = int(b)
    return a + b

print(add("5", "3"))""",
                "error_message": "",
                "question": "I made it handle both strings. Can you review this code?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [18.0, 2.0],
                "time_stuck": 0.0
            }
        ]
    },
    {
        "problem_type": "list_comprehension",
        "turns": [
            {
                "code": """numbers = [1, 2, 3, 4, 5]
squares = []
for num in numbers:
    squares.append(num * num)
print(squares)""",
                "error_message": "",
                "question": "I want to square all numbers. Is there a shorter way to do this?",
                "action_sequence": ["code_edit", "run_test", "search_documentation"],
                "time_deltas": [10.0, 2.0, 30.0],
                "time_stuck": 0.0
            },
            {
                "code": """numbers = [1, 2, 3, 4, 5]
squares = [num * num for num in numbers]
print(squares)""",
                "error_message": "",
                "question": "I learned about list comprehensions! Can you explain the syntax?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [20.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """numbers = [1, 2, 3, 4, 5]
even_squares = [num * num for num in numbers if num % 2 == 0]
print(even_squares)""",
                "error_message": "",
                "question": "I added a condition to only square even numbers. Is this correct?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [15.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """matrix = [[1, 2], [3, 4], [5, 6]]
flattened = [num for row in matrix for num in row]
print(flattened)""",
                "error_message": "",
                "question": "I'm trying to flatten a 2D list. Does this nested comprehension work?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [22.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """words = ["hello", "world", "python"]
lengths = {word: len(word) for word in words}
print(lengths)""",
                "error_message": "",
                "question": "I made a dictionary comprehension! Can you explain how this differs from list comprehension?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [18.0, 2.0],
                "time_stuck": 0.0
            }
        ]
    },
    {
        "problem_type": "dictionary_key_error",
        "turns": [
            {
                "code": """student = {"name": "Alice", "age": 20}
print(student["grade"])""",
                "error_message": "KeyError: 'grade'",
                "question": "Why am I getting a KeyError? The dictionary exists.",
                "action_sequence": ["code_edit", "run_test", "run_test", "search_documentation"],
                "time_deltas": [8.0, 2.0, 3.0, 35.0],
                "time_stuck": 48.0
            },
            {
                "code": """student = {"name": "Alice", "age": 20}
if "grade" in student:
    print(student["grade"])
else:
    print("Grade not found")""",
                "error_message": "",
                "question": "I added a check. But is there a simpler way?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [15.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """student = {"name": "Alice", "age": 20}
grade = student.get("grade", "N/A")
print(grade)""",
                "error_message": "",
                "question": "I used .get() method. Can you explain how it works?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [12.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """students = [
    {"name": "Alice", "age": 20},
    {"name": "Bob", "age": 22},
    {"name": "Charlie"}
]

for student in students:
    age = student.get("age", "Unknown")
    print(f"{student['name']}: {age}")""",
                "error_message": "",
                "question": "I'm iterating through a list of dictionaries. Is this the right way to handle missing keys?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [25.0, 2.0],
                "time_stuck": 0.0
            }
        ]
    },
    {
        "problem_type": "function_arguments",
        "turns": [
            {
                "code": """def greet(name, message):
    return f"{message}, {name}!"

print(greet("Alice"))""",
                "error_message": "TypeError: greet() missing 1 required positional argument: 'message'",
                "question": "Why do I need to provide both arguments? Can I make message optional?",
                "action_sequence": ["code_edit", "run_test", "search_documentation"],
                "time_deltas": [10.0, 2.0, 30.0],
                "time_stuck": 42.0
            },
            {
                "code": """def greet(name, message="Hello"):
    return f"{message}, {name}!"

print(greet("Alice"))
print(greet("Bob", "Hi"))""",
                "error_message": "",
                "question": "I added a default value. Can you explain default parameters?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [20.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """def calculate(a, b, operation="add"):
    if operation == "add":
        return a + b
    elif operation == "multiply":
        return a * b
    return a - b

print(calculate(5, 3))
print(calculate(5, 3, "multiply"))""",
                "error_message": "",
                "question": "I made a calculator function with a default operation. Is this good design?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [25.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """def process_data(*args):
    return sum(args)

print(process_data(1, 2, 3, 4, 5))""",
                "error_message": "",
                "question": "I learned about *args! Can you explain how it works?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [18.0, 2.0],
                "time_stuck": 0.0
            }
        ]
    },
    {
        "problem_type": "loop_logic",
        "turns": [
            {
                "code": """numbers = [1, 2, 3, 4, 5]
for i in range(len(numbers)):
    if numbers[i] % 2 == 0:
        numbers.remove(numbers[i])
print(numbers)""",
                "error_message": "IndexError: list index out of range",
                "question": "I'm trying to remove even numbers but getting an error. What's wrong?",
                "action_sequence": ["code_edit", "run_test", "run_test", "code_edit"],
                "time_deltas": [12.0, 2.0, 3.0, 20.0],
                "time_stuck": 37.0
            },
            {
                "code": """numbers = [1, 2, 3, 4, 5]
result = []
for num in numbers:
    if num % 2 != 0:
        result.append(num)
print(result)""",
                "error_message": "",
                "question": "I created a new list instead. Is this better?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [20.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """numbers = [1, 2, 3, 4, 5]
result = [num for num in numbers if num % 2 != 0]
print(result)""",
                "error_message": "",
                "question": "I converted it to a list comprehension. Is this the Pythonic way?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [15.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """numbers = [1, 2, 3, 4, 5]
numbers = [num for num in numbers if num % 2 != 0]
print(numbers)""",
                "error_message": "",
                "question": "Can I modify the original list this way?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [10.0, 2.0],
                "time_stuck": 0.0
            }
        ]
    },
    {
        "problem_type": "string_manipulation",
        "turns": [
            {
                "code": """text = "hello world"
words = text.split()
result = ""
for word in words:
    result += word.capitalize() + " "
print(result)""",
                "error_message": "",
                "question": "I want to capitalize each word. Is there a better way?",
                "action_sequence": ["code_edit", "run_test", "search_documentation"],
                "time_deltas": [10.0, 2.0, 25.0],
                "time_stuck": 0.0
            },
            {
                "code": """text = "hello world"
words = text.split()
result = " ".join([word.capitalize() for word in words])
print(result)""",
                "error_message": "",
                "question": "I used join() and a list comprehension. Can you explain join()?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [18.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """text = "hello world"
result = text.title()
print(result)""",
                "error_message": "",
                "question": "I found the title() method! Is this simpler?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [12.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """text = "hello world"
result = " ".join(word.capitalize() for word in text.split())
print(result)""",
                "error_message": "",
                "question": "I used a generator expression. What's the difference from a list comprehension?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [20.0, 2.0],
                "time_stuck": 0.0
            }
        ]
    },
    {
        "problem_type": "object_oriented",
        "turns": [
            {
                "code": """class Dog:
    def __init__(self, name):
        self.name = name
    
    def bark(self):
        return f"{self.name} says woof!"

dog = Dog("Buddy")
print(dog.bark())""",
                "error_message": "",
                "question": "I created my first class! Can you explain what __init__ does?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [15.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """class Dog:
    def __init__(self, name, age=0):
        self.name = name
        self.age = age
    
    def bark(self):
        return f"{self.name} says woof!"
    
    def get_info(self):
        return f"{self.name} is {self.age} years old"

dog = Dog("Buddy", 3)
print(dog.get_info())""",
                "error_message": "",
                "question": "I added an age attribute. Is self always needed?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [18.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return "Some sound"

class Dog(Animal):
    def speak(self):
        return f"{self.name} says woof!"

dog = Dog("Buddy")
print(dog.speak())""",
                "error_message": "",
                "question": "I learned about inheritance! Can you explain how it works?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [25.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        raise NotImplementedError("Subclass must implement")

class Dog(Animal):
    def speak(self):
        return f"{self.name} says woof!"

dog = Dog("Buddy")
print(dog.speak())""",
                "error_message": "",
                "question": "I used NotImplementedError. Is this a good pattern?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [20.0, 2.0],
                "time_stuck": 0.0
            },
            {
                "code": """class Animal:
    def __init__(self, name):
        self._name = name  # Protected attribute
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

dog = Animal("Buddy")
print(dog.name)""",
                "error_message": "",
                "question": "I learned about properties and setters! Can you explain @property?",
                "action_sequence": ["code_edit", "run_test"],
                "time_deltas": [30.0, 2.0],
                "time_stuck": 0.0
            }
        ]
    }
]


def generate_10_conversations():
    """Generate 10 sample conversations"""
    
    print("=" * 80)
    print("GENERATING 10 SAMPLE MULTI-TURN CONVERSATIONS")
    print("=" * 80)
    
    # Initialize generator
    generator = MultiTurnConversationGenerator()
    
    # Select 10 scenarios (some may be repeated with variations)
    selected_scenarios = random.sample(STUDENT_SCENARIOS, min(10, len(STUDENT_SCENARIOS)))
    
    # If we need more, repeat some
    while len(selected_scenarios) < 10:
        selected_scenarios.append(random.choice(STUDENT_SCENARIOS))
    
    conversations = []
    
    for i, scenario in enumerate(selected_scenarios[:10], 1):
        print(f"\n{'='*80}")
        print(f"GENERATING CONVERSATION {i}/10: {scenario['problem_type']}")
        print(f"{'='*80}")
        
        # Prepare turns
        turns = []
        for j, turn_data in enumerate(scenario['turns'], 1):
            turns.append({
                "turn_number": j,
                **turn_data
            })
        
        # Generate conversation
        student_id = f"student_sample_{i:02d}"
        output_file = f"output/sample_conversation_{i:02d}"
        
        try:
            conversation = generator.generate_conversation(
                student_id=student_id,
                conversation_turns=turns,
                output_file=output_file
            )
            conversations.append(conversation)
            print(f"[OK] Conversation {i} completed")
        except Exception as e:
            print(f"[ERROR] Error generating conversation {i}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    # Generate summary
    print("\n" + "=" * 80)
    print("GENERATION SUMMARY")
    print("=" * 80)
    print(f"Total conversations generated: {len(conversations)}/10")
    
    # Save master index
    index_file = Path("output/sample_conversations_index.json")
    index_file.parent.mkdir(parents=True, exist_ok=True)
    
    index_data = {
        "generated_at": datetime.now().isoformat(),
        "total_conversations": len(conversations),
        "conversations": [
            {
                "conversation_number": i + 1,
                "student_id": conv.get('student_id'),
                "turns": len(conv.get('turns', [])),
                "json_file": f"sample_conversation_{i+1:02d}.json",
                "markdown_file": f"sample_conversation_{i+1:02d}.md",
                "summary": conv.get('summary', {})
            }
            for i, conv in enumerate(conversations)
        ]
    }
    
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, default=str, ensure_ascii=False)
    
    print(f"[OK] Index saved to: {index_file}")
    
    return conversations


if __name__ == "__main__":
    # Set UTF-8 encoding for Windows console
    import sys
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    
    conversations = generate_10_conversations()
    print("\n[OK] All conversations generated!")
    print(f"Check the 'output/' directory for all conversation files.")
    print(f"Files saved to: {Path('output').absolute()}")

