"""
Student-Friendly Explanation Generator
Converts complex analysis into clear, understandable explanations for students

Takes:
- Theory of Mind analysis
- Misconception detection
- Root cause analysis
- Error patterns

Generates:
- Clear, simple explanations
- Personalized to student's level
- Uses appropriate analogies/examples
- Adapts to cognitive state
"""

from typing import Dict, List, Optional
from enum import Enum
import re


class ExplanationStyle(Enum):
    """Explanation styles adapted to student needs"""
    SIMPLE_ANALOGY = "simple_analogy"  # Use everyday analogies
    STEP_BY_STEP = "step_by_step"  # Break into small steps
    VISUAL = "visual"  # Use diagrams/examples
    CONVERSATIONAL = "conversational"  # Friendly, supportive
    TECHNICAL = "technical"  # More detailed for advanced students


class StudentFriendlyExplainer:
    """
    Converts complex analysis into student-friendly explanations
    
    Adapts:
    - Language complexity
    - Explanation style
    - Examples and analogies
    - Tone and pacing
    """
    
    def __init__(self, config: Dict):
        """
        Args:
            config: Configuration dictionary
        """
        self.config = config
        
        # Explanation templates and strategies
        self.analogy_bank = self._initialize_analogies()
        self.explanation_templates = self._initialize_templates()
    
    def _initialize_analogies(self) -> Dict[str, List[str]]:
        """Initialize analogy bank for different concepts"""
        return {
            "recursion": [
                "Like climbing stairs - you need to know when to stop (base case) or you'll fall forever",
                "Like a Russian doll - each one opens to reveal a smaller one, until you reach the smallest",
                "Like a countdown timer - it counts down until it reaches zero, then stops"
            ],
            "base_case": [
                "Like a light switch - it turns the recursion OFF",
                "Like a stop sign - tells the function when to stop",
                "Like reaching the ground floor - you stop there, don't go further"
            ],
            "variable_scope": [
                "Like rooms in a house - local variables stay in their room, global variables are in the hallway",
                "Like personal belongings vs shared items - local is yours, global is everyone's",
                "Like your locker vs school supplies - locker is local, school supplies are global"
            ],
            "loops": [
                "Like counting on your fingers - you count 1, 2, 3... until you reach the end",
                "Like reading a book page by page - you read each page until you finish",
                "Like walking through a hallway - you check each door until you find the right one"
            ],
            "off_by_one": [
                "Like counting floors in a building - if there are 5 floors, they're numbered 0-4, not 1-5",
                "Like counting items in a list - if you have 5 items, the last one is at position 4, not 5",
                "Like measuring with a ruler - if something is 5 units long, it goes from 0 to 4, not 1 to 5"
            ]
        }
    
    def _initialize_templates(self) -> Dict[str, str]:
        """Initialize explanation templates"""
        return {
            "confused_simple": "I see you're working on {concept}. Let me explain it simply: {explanation}",
            "frustrated_supportive": "I understand this can be frustrating. Let's break it down step by step: {explanation}",
            "understanding_encourage": "Great progress! You're on the right track. Here's what's happening: {explanation}",
            "misconception_correct": "I see the issue - you're thinking {misconception}. Actually, {correction}",
            "root_cause_explain": "The reason this happened is {root_cause}. Here's why: {explanation}"
        }
    
    def generate_student_friendly_explanation(self, analysis: Dict) -> Dict:
        """
        Generate student-friendly explanation from complex analysis
        
        Args:
            analysis: Dictionary with:
                - theory_of_mind: Cognitive state and reasoning
                - misconception: What student believes wrong
                - error_analysis: Error and root cause
                - unified_explanation: Combined analysis
                - code: Student's code (optional)
                
        Returns:
            Student-friendly explanation with:
                - Clear main explanation
                - Simple analogies
                - Step-by-step guidance
                - Encouraging tone
        """
        """
        Generate student-friendly explanation from complex analysis
        
        Args:
            analysis: Dictionary with:
                - theory_of_mind: Cognitive state and reasoning
                - misconception: What student believes wrong
                - error_analysis: Error and root cause
                - unified_explanation: Combined analysis
                
        Returns:
            Student-friendly explanation with:
                - Clear main explanation
                - Simple analogies
                - Step-by-step guidance
                - Encouraging tone
        """
        result = {
            "greeting": "",
            "main_explanation": "",
            "analogy": "",
            "step_by_step": [],
            "example": "",
            "encouragement": "",
            "next_steps": []
        }
        
        # Get cognitive state
        tom = analysis.get("theory_of_mind", {})
        cognitive_state = tom.get("cognitive_state", "confused")
        
        # Get misconception
        misconception = analysis.get("misconception", {})
        has_misconception = misconception.get("detected", False)
        
        # Get error analysis
        error_analysis = analysis.get("error_analysis", {})
        root_cause = error_analysis.get("root_cause", {})
        
        # Get unified explanation
        unified = analysis.get("unified_explanation", {})
        
        # Get code if available (for better examples)
        code = analysis.get("code", "")
        
        # ===== 1. GREETING (Adapt to cognitive state) =====
        greetings = {
            "confused": "I see you're working on this - let me help clarify!",
            "frustrated": "I understand this can be challenging. Let's work through it together!",
            "understanding": "Great! You're making progress. Let me explain what's happening:",
            "engaged": "Awesome that you're exploring this! Here's what's going on:",
            "insight": "Excellent! You're getting it. Let me confirm your understanding:"
        }
        result["greeting"] = greetings.get(cognitive_state, "Let me help you understand this!")
        
        # ===== 2. MAIN EXPLANATION (Simplify complex analysis) =====
        # Get the core issue
        explanation_parts = []
        
        if has_misconception:
            misconception_desc = misconception.get("what_student_believes_wrong", "")
            if misconception_desc:
                explanation_parts.append(f"I see you're thinking: {misconception_desc}.")
            
            # Get correction from intervention
            intervention = misconception.get("best_intervention", {})
            if intervention:
                correction = intervention.get("content_template", "") or intervention.get("description", "")
                # Replace template placeholders
                correction = correction.replace("{example}", "an example")
                correction = correction.replace("{concept}", "this concept")
                if correction:
                    explanation_parts.append(f"Actually, {correction}")
        
        # Add root cause explanation
        if root_cause.get("cognitive_reason"):
            reason = root_cause.get("cognitive_reason", "")
            if reason and reason not in str(explanation_parts):
                explanation_parts.append(reason)
        
        # Add unified explanation
        if unified.get("best_way_to_help_understand"):
            help_text = unified["best_way_to_help_understand"]
            # Clean up template placeholders
            help_text = help_text.replace("{example}", "an example")
            help_text = help_text.replace("{concept}", "this concept")
            if help_text and help_text not in str(explanation_parts):
                explanation_parts.append(help_text)
        
        if explanation_parts:
            result["main_explanation"] = self._simplify_explanation(
                " ".join(explanation_parts),
                cognitive_state
            )
        else:
            result["main_explanation"] = "Let me help you understand what's happening here."
        
        # ===== 3. ANALOGY (Make it relatable) =====
        # Get concept from error or misconception
        concept = error_analysis.get("error", {}).get("concept", "")
        if not concept:
            # Try to infer from code
            if code:
                code_lower = code.lower()
                if "recursion" in code_lower or "factorial" in code_lower:
                    concept = "recursion"
                elif "for" in code_lower or "while" in code_lower:
                    concept = "loops"
                elif "global" in code_lower or "scope" in code_lower:
                    concept = "variable_scope"
        
        if not concept:
            concept = "programming"
        
        # Normalize concept name
        concept_key = concept.lower().replace(" ", "_")
        
        # Check if concept matches any key in analogy bank
        matched_key = None
        for key in self.analogy_bank.keys():
            if key in concept_key or concept_key in key:
                matched_key = key
                break
        
        if matched_key:
            analogies = self.analogy_bank[matched_key]
            # Choose analogy based on cognitive state
            if cognitive_state == "confused":
                result["analogy"] = analogies[0]  # Simplest
            elif cognitive_state == "frustrated":
                result["analogy"] = analogies[1] if len(analogies) > 1 else analogies[0]
            else:
                result["analogy"] = analogies[0]
        
        # ===== 4. STEP-BY-STEP (Break it down) =====
        result["step_by_step"] = self._create_steps(
            analysis, cognitive_state
        )
        
        # ===== 5. EXAMPLE (Concrete example) =====
        example_analysis = analysis.copy()
        if code:
            example_analysis["code"] = code
        result["example"] = self._create_example(example_analysis)
        
        # ===== 6. ENCOURAGEMENT (Supportive message) =====
        encouragements = {
            "confused": "Don't worry - this is a common challenge. You'll get it!",
            "frustrated": "You're doing great by asking for help. Let's solve this together!",
            "understanding": "You're on the right track! Keep going!",
            "engaged": "Your curiosity is great! This will help you learn.",
            "insight": "Excellent thinking! You're really understanding this now!"
        }
        result["encouragement"] = encouragements.get(cognitive_state, "Keep up the great work!")
        
        # ===== 7. NEXT STEPS (What to do next) =====
        result["next_steps"] = self._suggest_next_steps(analysis)
        
        # ===== 8. FULL EXPLANATION (Combined) =====
        result["full_explanation"] = self._combine_into_full_explanation(result)
        
        return result
    
    def _simplify_explanation(self, explanation: str, cognitive_state: str) -> str:
        """Simplify complex explanation based on cognitive state"""
        # Remove technical jargon for confused/frustrated students
        if cognitive_state in ["confused", "frustrated"]:
            # Replace technical terms
            replacements = {
                "recursive function": "function that calls itself",
                "base case": "stopping condition",
                "infinite recursion": "function that never stops",
                "stack overflow": "too many function calls",
                "variable scope": "where a variable can be used",
                "cognitive load": "how hard something is to understand"
            }
            
            for tech_term, simple_term in replacements.items():
                explanation = explanation.replace(tech_term, simple_term)
        
        # Make sentences shorter
        sentences = explanation.split(". ")
        if cognitive_state in ["confused", "frustrated"] and len(sentences) > 3:
            explanation = ". ".join(sentences[:3]) + "."
        
        return explanation
    
    def _create_steps(self, analysis: Dict, cognitive_state: str) -> List[str]:
        """Create step-by-step guidance"""
        steps = []
        
        error_analysis = analysis.get("error_analysis", {})
        error = error_analysis.get("error", {})
        
        if error.get("type") == "runtime_error" and "recursion" in error.get("concept", ""):
            steps = [
                "Step 1: Every recursive function needs a 'stopping point' (called a base case)",
                "Step 2: Without it, the function calls itself forever",
                "Step 3: Add an 'if' statement that checks when to stop",
                "Step 4: For factorial, stop when n is 0 or 1"
            ]
        elif "scope" in error.get("concept", ""):
            steps = [
                "Step 1: Variables inside a function are 'local' - they only exist there",
                "Step 2: Variables outside are 'global' - everyone can use them",
                "Step 3: To change a global variable inside a function, use 'global variable_name'",
                "Step 4: Or better - pass it as a parameter and return the new value"
            ]
        else:
            steps = [
                "Step 1: Let's identify what's happening",
                "Step 2: Understand why it's not working",
                "Step 3: Fix it step by step",
                "Step 4: Test to make sure it works"
            ]
        
        # Simplify steps for confused/frustrated students
        if cognitive_state in ["confused", "frustrated"]:
            steps = steps[:3]  # Fewer steps
        
        return steps
    
    def _create_example(self, analysis: Dict) -> str:
        """Create concrete example"""
        error_analysis = analysis.get("error_analysis", {})
        error = error_analysis.get("error", {})
        error_type = error.get("type", "")
        concept = error.get("concept", "").lower()
        
        # Get code from analysis if available
        code = analysis.get("code", "")
        
        # Infer concept from code if not in error
        if not concept and code:
            code_lower = code.lower()
            if "factorial" in code_lower or ("def" in code_lower and "(" in code_lower and ")" in code_lower and "return" in code_lower):
                # Check if it's recursive
                if any(func in code_lower for func in ["factorial", "fibonacci", "recursive"]):
                    concept = "recursion"
        
        # Create example based on error type and concept
        if "recursion" in concept or "recursive" in concept or "base case" in concept.lower() or "factorial" in str(code).lower():
            if code and "factorial" in code.lower():
                return """
Here's the corrected version:

def factorial(n):
    if n <= 1:        # <-- This is the base case (stopping point)
        return 1      # <-- Stop here when n is 0 or 1!
    return n * factorial(n - 1)  # <-- Keep going if n > 1

The key is the 'if n <= 1' part - that's what stops the recursion!
"""
            else:
                return """
Example of recursion with base case:

def factorial(n):
    if n <= 1:        # <-- Base case: stop when n is 0 or 1
        return 1      # <-- Return 1 (factorial of 0 or 1 is 1)
    return n * factorial(n - 1)  # <-- Recursive case: call itself

Without the base case, the function calls itself forever!
"""
        elif "scope" in concept or "variable" in concept:
            return """
Example of variable scope:

x = 10  # Global variable (everyone can see it)

def add_five():
    global x  # <-- Tell Python you want to use the global x
    x = x + 5
    return x

# Or better - pass it as parameter:
def add_five(x):
    return x + 5  # <-- x is a parameter, not global
"""
        elif "loop" in concept or "iteration" in concept:
            return """
Example of a loop:

for i in range(5):  # ← Loop 5 times (0, 1, 2, 3, 4)
    print(i)        # ← Do this each time

# This prints: 0, 1, 2, 3, 4
"""
        elif "syntax" in error_type.lower():
            return """
Example of correct syntax:

def my_function():  # ← Don't forget the colon!
    return "Hello"  # ← Indent the code inside

# Common mistakes:
# - Missing colon after def/if/for/while
# - Wrong indentation
# - Missing parentheses
"""
        else:
            return "Let me show you an example of how this works."
    
    def _suggest_next_steps(self, analysis: Dict) -> List[str]:
        """Suggest what student should do next"""
        steps = []
        
        tom = analysis.get("theory_of_mind", {})
        cognitive_state = tom.get("cognitive_state", "confused")
        
        if cognitive_state == "confused":
            steps = [
                "Try the example I provided",
                "Read through the steps one more time",
                "Ask me if anything is still unclear"
            ]
        elif cognitive_state == "frustrated":
            steps = [
                "Take a deep breath - you're doing great!",
                "Let's try a simpler example first",
                "We'll work through this together"
            ]
        elif cognitive_state == "understanding":
            steps = [
                "Try applying this to your code",
                "Test it and see if it works",
                "Let me know if you need more help"
            ]
        else:
            steps = [
                "Try implementing the solution",
                "Test it to make sure it works",
                "Come back if you have questions"
            ]
        
        return steps
    
    def _combine_into_full_explanation(self, parts: Dict) -> str:
        """Combine all parts into one coherent explanation"""
        explanation_parts = []
        
        # Greeting
        if parts.get("greeting"):
            explanation_parts.append(parts["greeting"])
        
        # Main explanation
        if parts.get("main_explanation"):
            explanation_parts.append(parts["main_explanation"])
        
        # Analogy
        if parts.get("analogy"):
            explanation_parts.append(f"Think of it like this: {parts['analogy']}")
        
        # Steps
        if parts.get("step_by_step"):
            explanation_parts.append("\nHere's how to fix it:")
            for i, step in enumerate(parts["step_by_step"], 1):
                explanation_parts.append(f"{step}")
        
        # Example
        if parts.get("example"):
            explanation_parts.append(f"\nHere's an example:\n{parts['example']}")
        
        # Encouragement
        if parts.get("encouragement"):
            explanation_parts.append(f"\n{parts['encouragement']}")
        
        # Next steps
        if parts.get("next_steps"):
            explanation_parts.append("\nWhat to do next:")
            for step in parts["next_steps"]:
                explanation_parts.append(f"• {step}")
        
        return "\n\n".join(explanation_parts)

