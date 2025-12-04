"""
Personalized Content Generator
Generates explanations, exercises, and learning materials tailored to student
"""

import torch
from typing import Dict, List, Optional
from transformers import AutoTokenizer


class PersonalizedContentGenerator:
    """
    Generates personalized learning content based on:
    - Student's latent representation (from HVSAE)
    - Intervention type
    - Learning style preferences
    - Knowledge gaps
    - Emotional state
    """
    
    def __init__(self, config: Dict, hvsae_model):
        self.config = config
        self.hvsae = hvsae_model
        
        # Tokenizer for text generation
        self.tokenizer = AutoTokenizer.from_pretrained(
            config['hvsae']['text_encoder']['model_name']
        )
        
        # Content templates
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict:
        """Load content templates for different intervention types"""
        return {
            'visual_explanation': {
                'intro': "Let me show you a visual representation to help clarify this concept:",
                'structure': ['diagram', 'explanation', 'example']
            },
            'interactive_exercise': {
                'intro': "Let's practice this concept with a hands-on exercise:",
                'structure': ['problem', 'hints', 'solution']
            },
            'guided_practice': {
                'intro': "I'll walk you through this step-by-step:",
                'structure': ['step1', 'step2', 'step3', 'verification']
            },
            'conceptual_deepdive': {
                'intro': "Let's explore the underlying concepts in depth:",
                'structure': ['fundamentals', 'connections', 'applications']
            },
            'motivational_support': {
                'intro': "You're doing great! Let's break this down together:",
                'structure': ['encouragement', 'simplification', 'next_step']
            }
        }
    
    def generate(self, latent: torch.Tensor,
                intervention_type: str,
                student_profile: Dict,
                knowledge_gaps: List[Dict]) -> Dict:
        """
        Generate personalized content
        
        Args:
            latent: Student's latent representation from HVSAE
            intervention_type: Type of intervention
            student_profile: Student's personality and learning style
            knowledge_gaps: Identified knowledge gaps
            
        Returns:
            Dictionary with generated content
        """
        # Get template for intervention type
        template = self.templates.get(intervention_type, self.templates['visual_explanation'])
        
        # Generate main explanation
        explanation = self._generate_explanation(
            latent, 
            intervention_type,
            student_profile,
            knowledge_gaps
        )
        
        # Adapt tone and language based on profile
        explanation = self._adapt_tone(explanation, student_profile)
        
        # Generate supporting materials
        materials = self._generate_materials(
            intervention_type,
            student_profile,
            knowledge_gaps
        )
        
        return {
            'type': intervention_type,
            'intro': template['intro'],
            'explanation': explanation,
            'materials': materials,
            'structure': template['structure']
        }
    
    def _generate_explanation(self, latent: torch.Tensor,
                            intervention_type: str,
                            student_profile: Dict,
                            knowledge_gaps: List[Dict]) -> str:
        """Generate explanation using HVSAE decoder"""
        # Use HVSAE explanation decoder
        with torch.no_grad():
            generated_tokens = self.hvsae.generate_explanation(
                latent,
                max_length=256,
                temperature=0.8
            )
        
        # Decode tokens to text
        explanation = self.tokenizer.decode(
            generated_tokens[0],
            skip_special_tokens=True
        )
        
        # Add context about knowledge gaps
        if knowledge_gaps:
            gap_context = self._format_gap_context(knowledge_gaps)
            explanation = f"{gap_context}\n\n{explanation}"
        
        return explanation
    
    def _format_gap_context(self, gaps: List[Dict]) -> str:
        """Format knowledge gaps into context"""
        if not gaps:
            return ""
        
        context = "Let's address some foundational concepts first:\n"
        for gap in gaps[:3]:  # Top 3 gaps
            concept = gap.get('concept', 'unknown')
            mastery = gap.get('mastery', 0)
            context += f"- {concept} (current understanding: {mastery:.0%})\n"
        
        return context
    
    def _adapt_tone(self, text: str, profile: Dict) -> str:
        """
        Adapt tone and language based on student profile
        
        Args:
            text: Original text
            profile: Student profile with personality and learning style
            
        Returns:
            Adapted text
        """
        personality = profile.get('personality', {})
        
        # Add encouragement for high neuroticism students
        if personality.get('neuroticism', 0.5) > 0.6:
            text = "Don't worry, this is a common challenge! " + text
            text += "\n\nRemember, everyone learns at their own pace."
        
        # More detailed explanations for high openness
        if personality.get('openness', 0.5) > 0.7:
            text += "\n\nInteresting note: This concept connects to many advanced topics you might explore later."
        
        # Structured, clear language for high conscientiousness
        if personality.get('conscientiousness', 0.5) > 0.7:
            text = self._add_structure(text)
        
        return text
    
    def _add_structure(self, text: str) -> str:
        """Add structural elements to text"""
        # Add numbered steps if not already present
        lines = text.split('\n')
        if len(lines) > 2 and not any(line.strip().startswith(('1.', '2.', '3.')) for line in lines):
            # Add section headers
            text = "**Key Points:**\n\n" + text
        
        return text
    
    def _generate_materials(self, intervention_type: str,
                          student_profile: Dict,
                          knowledge_gaps: List[Dict]) -> Dict:
        """Generate supporting learning materials"""
        materials = {}
        
        learning_style = student_profile.get('learning_style', {})
        
        # Visual learners get diagrams
        if learning_style.get('visual_verbal') == 'visual':
            materials['diagram'] = self._generate_diagram_placeholder(knowledge_gaps)
        
        # Active learners get exercises
        if learning_style.get('active_reflective') == 'active':
            materials['exercise'] = self._generate_exercise(knowledge_gaps)
        
        # Code examples
        materials['code_example'] = self._generate_code_example(knowledge_gaps)
        
        return materials
    
    def _generate_diagram_placeholder(self, gaps: List[Dict]) -> Dict:
        """Generate diagram metadata (actual rendering would be done client-side)"""
        if not gaps:
            return {'type': 'flowchart', 'description': 'General concept overview'}
        
        gap = gaps[0]
        concept = gap.get('concept', 'unknown')
        
        return {
            'type': 'concept_map',
            'central_concept': concept,
            'description': f'Visual representation of {concept} and related concepts',
            'nodes': [concept] + gap.get('prerequisites', [])
        }
    
    def _generate_exercise(self, gaps: List[Dict]) -> Dict:
        """Generate practice exercise"""
        if not gaps:
            return {
                'problem': 'Practice the concept you just learned.',
                'hints': [],
                'solution': ''
            }
        
        gap = gaps[0]
        concept = gap.get('concept', 'unknown')
        
        return {
            'problem': f'Write a simple program that demonstrates {concept}.',
            'hints': [
                'Start by setting up the basic structure',
                f'Focus on applying {concept} correctly',
                'Test your code with different inputs'
            ],
            'solution': f'// Solution code for {concept} would go here'
        }
    
    def _generate_code_example(self, gaps: List[Dict]) -> Dict:
        """Generate code example"""
        if not gaps:
            return {'code': '// Example code', 'explanation': 'Code explanation'}
        
        gap = gaps[0]
        concept = gap.get('concept', 'unknown')
        
        # Placeholder code generation
        # In production, this would use a code generation model
        code_examples = {
            'recursion': '''
def factorial(n):
    # Base case
    if n == 0 or n == 1:
        return 1
    # Recursive case
    return n * factorial(n - 1)

# Example usage
print(factorial(5))  # Output: 120
''',
            'loops': '''
# Using a for loop
for i in range(5):
    print(f"Iteration {i}")

# Using a while loop
count = 0
while count < 5:
    print(f"Count: {count}")
    count += 1
''',
            'arrays': '''
# Creating and manipulating arrays
numbers = [1, 2, 3, 4, 5]

# Accessing elements
print(numbers[0])  # First element

# Iterating
for num in numbers:
    print(num)

# Common operations
numbers.append(6)
numbers.remove(3)
'''
        }
        
        code = code_examples.get(concept, f'// Example code for {concept}')
        
        return {
            'code': code,
            'explanation': f'This example demonstrates {concept} in action.',
            'language': 'python'
        }


class ProgressTracker:
    """
    Tracks student progress and adaptation effectiveness
    """
    
    def __init__(self):
        self.student_progress = {}
        
    def record_interaction(self, student_id: str, interaction: Dict):
        """Record a learning interaction"""
        if student_id not in self.student_progress:
            self.student_progress[student_id] = {
                'interactions': [],
                'concept_mastery': {},
                'intervention_history': []
            }
        
        self.student_progress[student_id]['interactions'].append(interaction)
        
    def update_mastery(self, student_id: str, concept: str, 
                      mastery_delta: float):
        """Update mastery level for a concept"""
        if student_id not in self.student_progress:
            self.student_progress[student_id] = {'concept_mastery': {}}
        
        current = self.student_progress[student_id]['concept_mastery'].get(concept, 0.0)
        new_mastery = max(0.0, min(1.0, current + mastery_delta))
        self.student_progress[student_id]['concept_mastery'][concept] = new_mastery
        
    def get_progress_report(self, student_id: str) -> Dict:
        """Generate progress report for student"""
        if student_id not in self.student_progress:
            return {'status': 'No data'}
        
        data = self.student_progress[student_id]
        
        return {
            'total_interactions': len(data.get('interactions', [])),
            'concepts_mastered': sum(
                1 for m in data.get('concept_mastery', {}).values() if m > 0.7
            ),
            'average_mastery': sum(data.get('concept_mastery', {}).values()) / 
                             max(len(data.get('concept_mastery', {})), 1),
            'interventions_received': len(data.get('intervention_history', []))
        }




















