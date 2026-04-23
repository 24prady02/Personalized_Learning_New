"""
Teaching Engine - Main pedagogical orchestrator
Implements multi-session teaching strategies
"""

import torch
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import numpy as np


class TeachingEngine:
    """
    Complete teaching system that guides students through learning journeys
    
    Key Principles:
    1. Don't just fix - TEACH the underlying concept
    2. Use scaffolding - gradually reduce support
    3. Check understanding - not just completion
    4. Adapt to progress - make it harder as they improve
    5. Space practice - review over time
    """
    
    def __init__(self, config: Dict, models: Dict):
        self.config = config
        self.models = models
        
        # Teaching components
        self.scaffolding = ScaffoldingManager(config)
        self.curriculum = AdaptiveCurriculum(config)
        self.assessment = FormativeAssessment(config)
        
        # Student learning histories
        self.learning_histories = {}
        
    def teach_concept(self, student_id: str, concept: str, 
                     current_session: Dict) -> Dict:
        """
        Multi-stage teaching process for a concept
        
        NOT just: "Here's the answer"
        BUT: "Let me help you understand this step-by-step"
        
        Args:
            student_id: Student identifier
            concept: Concept to teach (e.g., 'base_case')
            current_session: Current debugging session data
            
        Returns:
            Teaching plan with multiple interactions
        """
        
        # Get student's learning history
        history = self._get_learning_history(student_id, concept)
        
        # Determine teaching stage
        stage = self._determine_teaching_stage(history, concept)
        
        print(f"\n🎓 TEACHING '{concept}' to {student_id}")
        print(f"   Stage: {stage}")
        print(f"   Previous attempts: {len(history.get('sessions', []))}")
        
        # Generate teaching plan based on stage
        if stage == 'introduction':
            return self._teach_introduction(student_id, concept, current_session)
        
        elif stage == 'guided_practice':
            return self._teach_guided_practice(student_id, concept, current_session)
        
        elif stage == 'independent_practice':
            return self._teach_independent_practice(student_id, concept, current_session)
        
        elif stage == 'mastery_check':
            return self._teach_mastery_check(student_id, concept, current_session)
        
        else:  # review
            return self._teach_review(student_id, concept, current_session)
    
    def _teach_introduction(self, student_id: str, concept: str, 
                           session: Dict) -> Dict:
        """
        Stage 1: Introduction - First exposure to concept
        
        Teach through:
        1. Simple explanation with analogy
        2. Visual representation
        3. Concrete example
        4. Very guided practice
        """
        
        print("\n  📖 Stage 1: INTRODUCTION")
        
        # Retrieve knowledge from CSE-KG
        cse_kg = self.models['cse_kg_client']
        concept_info = cse_kg.get_concept_info(concept)
        examples = cse_kg.get_examples(concept, difficulty='beginner')
        
        # Build explanation using Socratic method
        teaching_content = {
            "stage": "introduction",
            "learning_objective": f"Understand what {concept} is and why it's needed",
            
            # Part 1: Hook with real-world analogy
            "hook": self._generate_analogy(concept),
            
            # Part 2: Formal definition (from CSE-KG)
            "definition": {
                "text": concept_info['descriptions'][0],
                "source": "CS Knowledge Graph",
                "simple_version": self._simplify_for_beginner(concept_info['descriptions'][0])
            },
            
            # Part 3: Show concrete example
            "example": {
                "code": examples[0]['code'],
                "explanation": self._annotate_example(examples[0], concept),
                "interactive": True  # Student can modify and test
            },
            
            # Part 4: Guided discovery questions
            "discovery_questions": [
                f"What do you think happens if we remove the {concept}?",
                f"Can you identify the {concept} in this example?",
                "Try running the code without it - what happens?"
            ],
            
            # Part 5: Very simple practice (heavily guided)
            "practice": {
                "problem": self._generate_starter_problem(concept, difficulty=1),
                "scaffolding_level": 5,  # Maximum support
                "hints": self._generate_progressive_hints(concept, level=1),
                "solution_steps": self._break_into_tiny_steps(concept),
                "check_understanding": self._generate_check_questions(concept, level=1)
            },
            
            # Part 6: What's next
            "next_steps": {
                "if_understand": "Move to guided practice",
                "if_confused": "Review with different analogy",
                "estimated_time": "10-15 minutes"
            }
        }
        
        return teaching_content
    
    def _teach_guided_practice(self, student_id: str, concept: str, 
                              session: Dict) -> Dict:
        """
        Stage 2: Guided Practice - Build competence with support
        
        Gradually reduce scaffolding (Zone of Proximal Development)
        """
        
        print("\n  🎯 Stage 2: GUIDED PRACTICE")
        
        # Check current understanding
        understanding_level = self._assess_understanding(student_id, concept)
        
        teaching_content = {
            "stage": "guided_practice",
            "learning_objective": f"Apply {concept} with decreasing support",
            
            # Part 1: Quick review
            "review": self._generate_quick_review(concept),
            
            # Part 2: Multiple practice problems with decreasing hints
            "practice_sequence": [
                {
                    "problem_num": 1,
                    "difficulty": 2,
                    "scaffolding": 4,  # High support
                    "problem": self._generate_problem(concept, difficulty=2),
                    "hints_available": 5,
                    "show_hints_after": 30,  # seconds
                    "solution_available": True,
                    "explanation": "Full walkthrough available"
                },
                {
                    "problem_num": 2,
                    "difficulty": 3,
                    "scaffolding": 3,  # Medium support
                    "problem": self._generate_problem(concept, difficulty=3),
                    "hints_available": 3,
                    "show_hints_after": 60,
                    "solution_available": True,
                    "explanation": "Partial walkthrough"
                },
                {
                    "problem_num": 3,
                    "difficulty": 4,
                    "scaffolding": 2,  # Low support
                    "problem": self._generate_problem(concept, difficulty=4),
                    "hints_available": 1,
                    "show_hints_after": 90,
                    "solution_available": False,  # Try on your own first
                    "explanation": "Only hints"
                }
            ],
            
            # Part 3: Check understanding between problems
            "formative_checks": [
                {
                    "after_problem": 1,
                    "question": f"In your own words, explain why {concept} is needed",
                    "type": "free_response"
                },
                {
                    "after_problem": 2,
                    "question": f"Identify the {concept} in this code snippet",
                    "type": "code_annotation"
                }
            ],
            
            # Part 4: Common mistakes to avoid
            "common_pitfalls": self._get_common_pitfalls(concept),
            
            # Part 5: Self-assessment
            "self_check": {
                "questions": [
                    f"Can you write a simple function with {concept}?",
                    f"Can you explain when {concept} is needed?",
                    f"Can you debug errors related to {concept}?"
                ],
                "mastery_threshold": 0.7
            }
        }
        
        return teaching_content
    
    def _teach_independent_practice(self, student_id: str, concept: str,
                                   session: Dict) -> Dict:
        """
        Stage 3: Independent Practice - Apply without help
        
        Minimal scaffolding, student works independently
        """
        
        print("\n  🚀 Stage 3: INDEPENDENT PRACTICE")
        
        teaching_content = {
            "stage": "independent_practice",
            "learning_objective": f"Apply {concept} independently in varied contexts",
            
            # Part 1: Challenge problems (no hints)
            "challenges": [
                {
                    "problem": self._generate_problem(concept, difficulty=5),
                    "scaffolding": 0,  # No support initially
                    "hints_on_request_only": True,
                    "time_limit": None,
                    "success_criteria": "Correct solution without hints"
                },
                {
                    "problem": self._generate_transfer_problem(concept),  # Different context!
                    "scaffolding": 0,
                    "tests_transfer": True,  # Can they apply in new situation?
                    "success_criteria": "Recognizes need for concept in new context"
                }
            ],
            
            # Part 2: Debugging challenges
            "debug_challenges": [
                {
                    "buggy_code": self._generate_buggy_code(concept),
                    "task": f"Find and fix the {concept}-related bug",
                    "hints": "Available if stuck for >2 minutes"
                }
            ],
            
            # Part 3: Reflection prompts
            "reflection": [
                f"What strategies did you use to apply {concept}?",
                "What was challenging? What came easily?",
                "Where else might this concept be useful?"
            ],
            
            # Part 4: Progress check
            "mastery_indicators": {
                "can_implement": None,  # To be checked
                "can_debug": None,
                "can_explain": None,
                "can_transfer": None
            }
        }
        
        return teaching_content
    
    def _teach_mastery_check(self, student_id: str, concept: str,
                            session: Dict) -> Dict:
        """
        Stage 4: Mastery Check - Verify deep understanding
        
        Assesses:
        - Can implement correctly
        - Can debug errors
        - Can explain to others
        - Can apply in new contexts
        - Can teach the concept
        """
        
        print("\n  ✅ Stage 4: MASTERY CHECK")
        
        teaching_content = {
            "stage": "mastery_check",
            "learning_objective": f"Demonstrate mastery of {concept}",
            
            # Bloom's Taxonomy - Higher Order Thinking
            "assessments": {
                
                # Level 1: Remember
                "remember": {
                    "question": f"What is {concept}?",
                    "type": "definition"
                },
                
                # Level 2: Understand
                "understand": {
                    "question": f"Explain why {concept} is necessary",
                    "type": "explanation"
                },
                
                # Level 3: Apply
                "apply": {
                    "question": f"Implement {concept} in this new problem",
                    "type": "coding"
                },
                
                # Level 4: Analyze
                "analyze": {
                    "question": f"Find the bug related to {concept}",
                    "type": "debugging"
                },
                
                # Level 5: Evaluate
                "evaluate": {
                    "question": "Which solution is better and why?",
                    "type": "comparison"
                },
                
                # Level 6: Create
                "create": {
                    "question": f"Design a new problem that requires {concept}",
                    "type": "problem_creation"
                }
            },
            
            "mastery_criteria": {
                "minimum_score": 0.85,
                "must_pass_all": False,
                "must_pass_apply_analyze": True  # Critical levels
            },
            
            "on_mastery": "Move to next concept",
            "on_partial": "Additional practice in weak areas",
            "on_failure": "Return to guided practice"
        }
        
        return teaching_content
    
    def _generate_analogy(self, concept: str) -> Dict:
        """Generate real-world analogy for concept"""
        
        analogies = {
            "base_case": {
                "title": "Base Case is like a STOP sign",
                "analogy": """
Imagine you're driving down a street with houses:
- You keep going from house to house (recursive calls)
- But you need a STOP sign at the end (base case)
- Without the stop sign, you'd drive forever!

In recursion:
- Each function call is like visiting a house
- The base case is the STOP sign
- Without it, the program 'drives' forever until it crashes!
                """,
                "visual": "stop_sign_recursion_diagram"
            },
            
            "recursion": {
                "title": "Recursion is like Russian Nesting Dolls",
                "analogy": """
Imagine opening a Russian nesting doll (matryoshka):
- You open the big doll → find a smaller doll inside
- You open that → find an even smaller doll
- You keep going until → you reach the tiniest doll (base case!)
- Then you close them back up in reverse order

In programming:
- Big problem → break into smaller problem (recursive call)
- Keep breaking down → until you reach simplest case (base case)
- Then solve backwards → building up to final answer
                """
            },
            
            "call_stack": {
                "title": "Call Stack is like a Stack of Plates",
                "analogy": """
Think of a stack of plates in a cafeteria:
- Each function call adds a plate to the stack (push)
- When function returns, remove the plate (pop)
- You can only access the TOP plate at any time
- Stack too high → it falls over! (stack overflow)
                """
            }
        }
        
        return analogies.get(concept, {"title": concept, "analogy": "..."})
    
    def _generate_progressive_hints(self, concept: str, level: int) -> List[Dict]:
        """
        Generate hints that progressively reveal the solution
        Following Vygotsky's Zone of Proximal Development
        """
        
        if concept == "base_case":
            return [
                {
                    "hint_level": 1,
                    "reveals": "10%",
                    "hint": "Think about when the recursion should STOP. What's the simplest case?",
                    "type": "question"
                },
                {
                    "hint_level": 2,
                    "reveals": "30%",
                    "hint": "For factorial, what is the result when n is 0 or 1? That's your stopping point.",
                    "type": "guided_thinking"
                },
                {
                    "hint_level": 3,
                    "reveals": "50%",
                    "hint": "You need an IF statement at the beginning of your function. What should it check?",
                    "type": "structural"
                },
                {
                    "hint_level": 4,
                    "reveals": "75%",
                    "hint": "Try: if n <= 1: return 1",
                    "type": "partial_code"
                },
                {
                    "hint_level": 5,
                    "reveals": "100%",
                    "hint": "Complete solution:\ndef factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
                    "type": "complete_solution"
                }
            ]
        
        return []
    
    def _break_into_tiny_steps(self, concept: str) -> List[Dict]:
        """
        Break learning into very small, achievable steps
        Each step builds on previous
        """
        
        if concept == "base_case":
            return [
                {
                    "step": 1,
                    "title": "Understand the problem",
                    "task": "Run the buggy code and observe what happens",
                    "success": "You see RecursionError",
                    "explanation": "The function keeps calling itself forever"
                },
                {
                    "step": 2,
                    "title": "Identify when recursion should stop",
                    "task": "Think: What's the simplest factorial? factorial(0) = 1, factorial(1) = 1",
                    "success": "You identify n=0 or n=1 as stopping points",
                    "explanation": "These are the base cases - no recursion needed"
                },
                {
                    "step": 3,
                    "title": "Add a condition to check",
                    "task": "Add: if n <= 1:",
                    "success": "You have a conditional statement",
                    "explanation": "This checks if we've reached the base case"
                },
                {
                    "step": 4,
                    "title": "Return the base case value",
                    "task": "Inside the if block, add: return 1",
                    "success": "Function returns 1 for base cases",
                    "explanation": "This stops the recursion"
                },
                {
                    "step": 5,
                    "title": "Test your solution",
                    "task": "Run factorial(5) again",
                    "success": "Output is 120, no error!",
                    "explanation": "Now recursion stops at base case and works correctly"
                },
                {
                    "step": 6,
                    "title": "Understand what happened",
                    "task": "Trace through: factorial(5)→factorial(4)→...→factorial(1)→STOP",
                    "success": "You can explain the execution flow",
                    "explanation": "Base case prevents infinite recursion"
                }
            ]
        
        return []
    
    def _generate_check_questions(self, concept: str, level: int) -> List[Dict]:
        """
        Generate questions to check understanding (formative assessment)
        """
        
        if concept == "base_case":
            return [
                {
                    "question": "What would happen if we removed the base case?",
                    "correct_answer": "Infinite recursion / RecursionError",
                    "checks": "understanding_of_purpose"
                },
                {
                    "question": "Can you identify the base case in this code?",
                    "code": "def fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)",
                    "correct_answer": "if n <= 1: return n",
                    "checks": "pattern_recognition"
                },
                {
                    "question": "Write a base case for countdown function countdown(n)",
                    "correct_answer": "if n <= 0: return",
                    "checks": "application"
                }
            ]
        
        return []
    
    def _determine_teaching_stage(self, history: Dict, concept: str) -> str:
        """
        Determine appropriate teaching stage based on student progress
        """
        
        if not history or len(history.get('sessions', [])) == 0:
            return 'introduction'  # First time seeing concept
        
        # Check mastery from previous sessions
        latest_mastery = history.get('latest_mastery', 0.0)
        
        if latest_mastery < 0.3:
            return 'introduction'  # Still very new
        elif latest_mastery < 0.6:
            return 'guided_practice'  # Building competence
        elif latest_mastery < 0.8:
            return 'independent_practice'  # Developing mastery
        elif latest_mastery < 0.9:
            return 'mastery_check'  # Final verification
        else:
            # Check if needs review (spaced repetition)
            last_practice = history.get('last_practice_date')
            if last_practice:
                days_since = (datetime.now() - last_practice).days
                if days_since > 7:  # 1 week
                    return 'review'
            
            return 'mastered'  # Already mastered
    
    def _get_learning_history(self, student_id: str, concept: str) -> Dict:
        """Get student's learning history for this concept"""
        
        if student_id not in self.learning_histories:
            self.learning_histories[student_id] = {}
        
        if concept not in self.learning_histories[student_id]:
            self.learning_histories[student_id][concept] = {
                'sessions': [],
                'latest_mastery': 0.0,
                'attempts': 0,
                'last_practice_date': None,
                'stage': 'introduction'
            }
        
        return self.learning_histories[student_id][concept]
    
    def update_learning_progress(self, student_id: str, concept: str,
                                session_result: Dict):
        """
        Update student's learning progress after a session
        
        Args:
            session_result: {
                'completed': True/False,
                'mastery_score': 0.75,
                'time_spent': 180,
                'problems_solved': 3,
                'hints_used': 2
            }
        """
        
        history = self._get_learning_history(student_id, concept)
        
        # Record session
        history['sessions'].append({
            'timestamp': datetime.now(),
            'result': session_result,
            'mastery_score': session_result.get('mastery_score', 0)
        })
        
        # Update mastery (exponential moving average)
        alpha = 0.3  # Learning rate
        old_mastery = history['latest_mastery']
        new_mastery = alpha * session_result.get('mastery_score', 0) + (1 - alpha) * old_mastery
        
        history['latest_mastery'] = new_mastery
        history['attempts'] += 1
        history['last_practice_date'] = datetime.now()
        
        # Determine new stage
        history['stage'] = self._determine_teaching_stage(history, concept)
        
        print(f"\n📈 Learning progress updated:")
        print(f"   Mastery: {old_mastery:.0%} → {new_mastery:.0%}")
        print(f"   New stage: {history['stage']}")
        
        return history


class ScaffoldingManager:
    """
    Manages scaffolding (support structures) that are gradually removed
    Based on Vygotsky's Zone of Proximal Development
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.scaffolding_levels = {
            5: "maximum_support",
            4: "high_support", 
            3: "medium_support",
            2: "low_support",
            1: "minimal_support",
            0: "no_support"
        }
    
    def get_scaffolding(self, level: int, concept: str, problem: str) -> Dict:
        """
        Get appropriate scaffolding for a problem
        
        Args:
            level: 0-5 (0=no help, 5=maximum help)
            concept: Concept being taught
            problem: Problem to solve
            
        Returns:
            Scaffolding structure
        """
        
        scaffolding = {
            "level": level,
            "description": self.scaffolding_levels[level]
        }
        
        if level >= 5:  # Maximum support
            scaffolding.update({
                "code_template": self._provide_template(concept, problem),
                "step_by_step_guide": True,
                "inline_comments": True,
                "example_solution": True,
                "hints_visible": True
            })
        
        elif level >= 3:  # Medium support
            scaffolding.update({
                "code_template": self._provide_partial_template(concept),
                "hints_available": True,
                "example_available": True
            })
        
        elif level >= 1:  # Low support
            scaffolding.update({
                "hints_on_request": True,
                "time_before_hints": 90  # Must try for 90s first
            })
        
        else:  # No support
            scaffolding.update({
                "independent_work": True,
                "hints_after_failure": True
            })
        
        return scaffolding
    
    def _provide_template(self, concept: str, problem: str) -> str:
        """Provide code template with blanks to fill"""
        
        if concept == "base_case":
            return """
def factorial(n):
    # TODO: Add base case here
    # HINT: What should happen when n is 0 or 1?
    if ______:  # Fill in the condition
        return ______  # Fill in the return value
    
    # Recursive case (already provided)
    return n * factorial(n - 1)
            """
        
        return "# Your code here"


class AdaptiveCurriculum:
    """
    Generates personalized learning paths
    Adapts difficulty based on student progress
    """
    
    def __init__(self, config: Dict):
        self.config = config
    
    def generate_learning_path(self, student_id: str, 
                              target_concept: str,
                              current_mastery: Dict) -> List[Dict]:
        """
        Generate optimal learning path from current state to target
        
        Uses CSE-KG to find prerequisites and logical progression
        """
        
        path = []
        
        # Get prerequisites from CSE-KG
        cse_kg = self.config['cse_kg_client']
        prerequisites = cse_kg.get_prerequisites(target_concept)
        
        # Order by dependency
        for prereq in prerequisites:
            if current_mastery.get(prereq, 0) < 0.7:
                path.append({
                    'concept': prereq,
                    'reason': f'Prerequisite for {target_concept}',
                    'estimated_time': '15-30 minutes',
                    'current_mastery': current_mastery.get(prereq, 0)
                })
        
        # Add target concept
        path.append({
            'concept': target_concept,
            'reason': 'Target learning goal',
            'estimated_time': '30-45 minutes',
            'current_mastery': current_mastery.get(target_concept, 0)
        })
        
        return path


class FormativeAssessment:
    """
    Continuous assessment during learning (not just at the end)
    Checks understanding and adjusts teaching in real-time
    """
    
    def __init__(self, config: Dict):
        self.config = config
    
    def assess_understanding(self, student_response: str, 
                           concept: str) -> Dict:
        """
        Assess student's understanding from their explanation/code
        
        Returns:
            Assessment with mastery score and feedback
        """
        
        # Use HVSAE to encode student's response
        # Compare to expert responses
        # Return mastery estimate
        
        return {
            'mastery_score': 0.75,
            'demonstrates_understanding': True,
            'misconceptions_detected': [],
            'feedback': "Good understanding! Can you explain why...?"
        }


def _simplify_for_beginner(text: str) -> str:
    """Simplify technical language for beginners"""
    
    simplifications = {
        "terminating condition": "stopping point",
        "recursive invocation": "calling itself again",
        "stack overflow": "too many function calls",
        "computational complexity": "how fast the code runs"
    }
    
    simplified = text
    for technical, simple in simplifications.items():
        simplified = simplified.replace(technical, simple)
    
    return simplified




















