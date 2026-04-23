"""
Scaffolding Manager - Implements graduated support
Based on Vygotsky's Zone of Proximal Development
"""

from typing import Dict, List, Optional
import random


class ScaffoldingManager:
    """
    Manages scaffolding (support) that is gradually removed as student learns
    
    Scaffolding Levels:
    5 - Maximum: Code templates, step-by-step, full solutions
    4 - High: Partial templates, detailed hints, examples
    3 - Medium: Structure guidance, hints on request
    2 - Low: Minimal hints, must attempt first
    1 - Minimal: Only if stuck for extended time
    0 - None: Independent work
    """
    
    def __init__(self, config: Dict):
        self.config = config
    
    def generate_scaffolded_problem(self, concept: str, level: int,
                                   difficulty: int) -> Dict:
        """
        Generate problem with appropriate scaffolding
        
        Args:
            concept: Concept being taught
            level: Scaffolding level (0-5)
            difficulty: Problem difficulty (1-10)
            
        Returns:
            Problem with scaffolding materials
        """
        
        if concept == "base_case" and level == 5:
            # Maximum scaffolding - almost fill-in-the-blank
            return {
                "problem": "Complete this factorial function:",
                "template": """
def factorial(n):
    # Step 1: Check if we've reached the base case
    if ____________:  # What condition stops recursion?
        return ____________  # What value to return?
    
    # Step 2: Recursive case (provided for you)
    return n * factorial(n - 1)
                """,
                "guidance": [
                    "Base case for factorial is when n is 0 or 1",
                    "Both factorial(0) and factorial(1) equal 1",
                    "Use: if n <= 1:",
                    "Then: return 1"
                ],
                "test_cases": [
                    "factorial(0) should return 1",
                    "factorial(1) should return 1",
                    "factorial(5) should return 120"
                ],
                "solution_visible": True,
                "can_run_anytime": True
            }
        
        elif concept == "base_case" and level == 3:
            # Medium scaffolding - some structure
            return {
                "problem": "Write a recursive fibonacci function",
                "starter_code": """
def fibonacci(n):
    # Add your base case here
    
    # Add your recursive case here
    pass
                """,
                "hints": [
                    "Fibonacci has TWO base cases: n=0 and n=1",
                    "fib(0)=0 and fib(1)=1",
                    "Recursive: fib(n) = fib(n-1) + fib(n-2)"
                ],
                "hints_available_after": 60,  # Must try for 1 minute first
                "example_similar": "factorial",
                "test_cases": ["fib(0)=0", "fib(5)=5", "fib(10)=55"]
            }
        
        elif concept == "base_case" and level == 1:
            # Minimal scaffolding - must work independently
            return {
                "problem": "Write a recursive function to reverse a string",
                "description": "reverse('hello') should return 'olleh'",
                "starter_code": "# Your code here",
                "hints": ["Available if stuck > 3 minutes"],
                "must_attempt_first": True,
                "test_cases": [
                    "reverse('hello') == 'olleh'",
                    "reverse('a') == 'a'",
                    "reverse('') == ''"
                ]
            }
        
        else:
            # No scaffolding - completely independent
            return {
                "problem": "Solve this challenge using recursion",
                "description": "Your choice of approach",
                "independent": True
            }
    
    def fade_scaffolding(self, current_level: int, 
                        performance: float) -> int:
        """
        Decide whether to reduce scaffolding based on performance
        
        Args:
            current_level: Current scaffolding level
            performance: Score on recent task (0-1)
            
        Returns:
            New scaffolding level
        """
        
        if performance >= 0.9:
            # Excellent - reduce by 2 levels
            return max(0, current_level - 2)
        elif performance >= 0.75:
            # Good - reduce by 1 level
            return max(0, current_level - 1)
        elif performance >= 0.5:
            # Okay - maintain current level
            return current_level
        else:
            # Struggling - increase support
            return min(5, current_level + 1)
    
    def provide_just_in_time_hint(self, student_code: str,
                                  time_stuck: int,
                                  concept: str) -> Optional[str]:
        """
        Provide hint at the right moment
        Not too early (prevent learning) or too late (frustration)
        """
        
        # No hint if not stuck long enough
        if time_stuck < 30:
            return None
        
        # Gentle hint after 30s
        if time_stuck < 60:
            return "💡 Think about: What's the simplest input?"
        
        # More specific hint after 1 minute
        if time_stuck < 120:
            return "💡 For recursion, you need a condition that stops the calls. What condition?"
        
        # Direct hint after 2 minutes
        if time_stuck < 180:
            return "💡 Try adding: if n <= 1: return 1"
        
        # Show solution after 3 minutes
        return "Let me show you the solution and explain why it works..."


import random




















