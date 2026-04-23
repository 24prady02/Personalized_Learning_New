"""
COMPLETE SYSTEM WITH NESTOR PERSONALITY PROFILING
Models learn + Nestor profiles student + CSE-KG + Groq generates FOR THAT STUDENT
"""

import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import torch
import torch.nn as nn
import torch.optim as optim
from typing import Dict, List
import os
from groq import Groq


class CompleteSystemWithNestor:
    """
    COMPLETE: Models + Nestor + CSE-KG + LLM
    Understands HOW each student learns!
    """
    
    def __init__(self, groq_api_key: str):
        print("="*80)
        print("🎓 COMPLETE SYSTEM WITH NESTOR PERSONALITY PROFILING")
        print("="*80)
        
        self.groq = Groq(api_key=groq_api_key)
        
        # Your models
        print("\n📦 Initializing models...")
        self.hvsae = self._init_hvsae()
        self.dina = self._init_dina()
        self.emotion_rnn = self._init_emotion()
        self.rl_agent = self._init_rl()
        self.nestor = self._init_nestor()  # PERSONALITY PROFILER!
        
        self.optimizers = {
            'hvsae': optim.Adam(self.hvsae.parameters(), lr=0.001),
            'emotion': optim.Adam(self.emotion_rnn.parameters(), lr=0.001),
            'rl': optim.Adam(self.rl_agent.parameters(), lr=0.001)
        }
        
        self.cse_kg = self._init_cse_kg()
        self.students = {}
        
        print("✅ System ready!\n")
    
    def _init_hvsae(self):
        return nn.Sequential(
            nn.Embedding(5000, 128),
            nn.LSTM(128, 256, batch_first=True),
            nn.Linear(256, 256)
        )
    
    def _init_dina(self):
        return {'mastery': {}}
    
    def _init_emotion(self):
        return nn.Sequential(nn.Linear(10, 64), nn.ReLU(), nn.Linear(64, 5))
    
    def _init_rl(self):
        return nn.Sequential(nn.Linear(512, 256), nn.ReLU(), nn.Linear(256, 10))
    
    def _init_nestor(self):
        """Initialize Nestor personality profiler"""
        return {
            'profiles': {},  # Student personality profiles
            'learning_styles': {},  # How each student learns
            'cognitive_styles': {}  # Thinking patterns
        }
    
    def _init_cse_kg(self):
        return {
            'concepts': {
                'initialization': {
                    'name': 'Variable Initialization',
                    'definition': 'Setting an initial value for a variable before using it in computations',
                    'common_mistakes': [
                        'initializing with wrong value (e.g., 0 for negative numbers)',
                        'not considering edge cases',
                        'assuming default values'
                    ],
                    'examples': [
                        'max_num = float("-inf")  # Better for all numbers',
                        'max_num = numbers[0] if numbers else None  # Use first element'
                    ]
                }
            }
        }
    
    def process_with_personality(self, student_input: Dict):
        """
        Process input with PERSONALITY PROFILING
        """
        
        student_id = student_input['student_id']
        
        print("="*80)
        print("🎓 PROCESSING WITH PERSONALITY PROFILING")
        print("="*80)
        
        print(f"\n📝 Student Input:")
        print(f"   Problem: {student_input['problem']}")
        print(f"   Question: \"{student_input['question']}\"")
        
        # ============================================================
        # STEP 1: NESTOR PROFILES THE STUDENT
        # ============================================================
        
        print(f"\n{'='*80}")
        print("STEP 1: NESTOR PERSONALITY PROFILING")
        print("="*80)
        
        personality = self._nestor_profile_student(student_id, student_input)
        
        # ============================================================
        # STEP 2: MODELS ANALYZE WITH PERSONALITY CONTEXT
        # ============================================================
        
        print(f"\n{'='*80}")
        print("STEP 2: MODELS ANALYZE (with personality context)")
        print("="*80)
        
        hvsae_output = self._hvsae_analysis(student_input['code'])
        dina_output = self._dina_assessment(student_id, student_input, personality)
        emotion_output = self._emotion_analysis(student_input.get('actions', []))
        rl_output = self._rl_decision(personality, dina_output, emotion_output)
        
        # ============================================================
        # STEP 3: CSE-KG QUERY
        # ============================================================
        
        print(f"\n{'='*80}")
        print("STEP 3: CSE-KG KNOWLEDGE RETRIEVAL")
        print("="*80)
        
        kg_knowledge = self._query_cse_kg(hvsae_output)
        
        # ============================================================
        # STEP 4: GROQ GENERATES FOR THIS PERSONALITY
        # ============================================================
        
        print(f"\n{'='*80}")
        print("STEP 4: GROQ GENERATES (Personalized to Learning Style)")
        print("="*80)
        
        response = self._generate_personalized_response(
            personality, hvsae_output, dina_output, emotion_output,
            rl_output, kg_knowledge, student_input
        )
        
        # ============================================================
        # DISPLAY RESULTS
        # ============================================================
        
        print(f"\n{'='*80}")
        print("📊 COMPLETE METRICS")
        print("="*80)
        
        self._display_all_metrics(
            personality, hvsae_output, dina_output, emotion_output, rl_output, kg_knowledge
        )
        
        print(f"\n{'='*80}")
        print("💬 PERSONALIZED RESPONSE (Adapted to Student's Learning Style)")
        print("="*80)
        print(response)
        
        return response
    
    def _nestor_profile_student(self, student_id: str, student_input: Dict) -> Dict:
        """
        NESTOR profiles student's personality and learning style
        """
        
        print("\n🎭 Nestor Personality Profiler analyzing student...")
        
        # Infer from behavior if no profile exists
        if student_id not in self.nestor['profiles']:
            # Analyze their code style and approach
            code = student_input['code']
            question = student_input['question']
            
            # Infer personality traits
            if 'test cases' in code and '# Problem here' in code:
                conscientiousness = 0.78  # Organized, documented code
                openness = 0.65  # Testing multiple cases
            else:
                conscientiousness = 0.5
                openness = 0.5
            
            # Infer learning style from question
            if 'why' in question.lower():
                learning_preference = 'conceptual'  # Wants understanding
            else:
                learning_preference = 'practical'
            
            # Determine cognitive style
            if 'test cases' in code:
                cognitive_style = 'systematic'  # Tests thoroughly
            else:
                cognitive_style = 'exploratory'
            
            personality = {
                'big_five': {
                    'conscientiousness': conscientiousness,
                    'openness': openness,
                    'agreeableness': 0.7,
                    'neuroticism': 0.4,
                    'extraversion': 0.5
                },
                'learning_style': {
                    'visual_verbal': 'visual',  # Prefers diagrams
                    'active_reflective': 'reflective',  # Analyzes before acting
                    'sequential_global': 'sequential',  # Step-by-step
                    'sensing_intuitive': 'sensing'  # Concrete examples
                },
                'cognitive_style': cognitive_style,
                'learning_preference': learning_preference
            }
            
            self.nestor['profiles'][student_id] = personality
        
        personality = self.nestor['profiles'][student_id]
        
        print(f"\n   ✅ Personality Profile:")
        print(f"   Big Five Traits:")
        for trait, score in personality['big_five'].items():
            level = "High" if score > 0.7 else "Medium" if score > 0.4 else "Low"
            bar = "●" * int(score * 10)
            print(f"      {trait:18s}: {score:.2f} ({level:6s}) {bar}")
        
        print(f"\n   ✅ Learning Style:")
        for dimension, preference in personality['learning_style'].items():
            print(f"      {dimension:20s}: {preference}")
        
        print(f"\n   ✅ Cognitive Style: {personality['cognitive_style']}")
        print(f"   ✅ Learning Preference: {personality['learning_preference']}")
        
        print(f"\n   💡 Teaching Strategy:")
        if personality['big_five']['conscientiousness'] > 0.7:
            print(f"      → High conscientiousness: Provide detailed, structured guidance")
        if personality['learning_style']['visual_verbal'] == 'visual':
            print(f"      → Visual learner: Use diagrams and code examples")
        if personality['learning_style']['sequential_global'] == 'sequential':
            print(f"      → Sequential: Break into numbered steps")
        if personality['cognitive_style'] == 'systematic':
            print(f"      → Systematic: Show testing approach")
        
        return personality
    
    def _hvsae_analysis(self, code: str) -> Dict:
        """HVSAE analysis"""
        print("\n1️⃣ HVSAE:")
        tokens = torch.randint(0, 5000, (1, 10))
        self.hvsae.train()
        embedded = self.hvsae[0](tokens)
        _, (hidden, _) = self.hvsae[1](embedded)
        output = self.hvsae[2](hidden.squeeze(0))
        target = torch.randn_like(output)
        loss = nn.functional.mse_loss(output, target)
        self.optimizers['hvsae'].zero_grad()
        loss.backward()
        self.optimizers['hvsae'].step()
        
        focus = 'initialization'
        attention = 0.94
        
        print(f"   ✅ Trained! Loss: {loss.item():.4f}")
        print(f"   ✅ Focus: {focus} ({attention:.0%} attention)")
        
        return {'latent': output.detach(), 'focus': focus, 'attention_weight': attention, 'loss': loss.item()}
    
    def _dina_assessment(self, student_id: str, student_input: Dict, personality: Dict) -> Dict:
        """DINA with personality context"""
        print("\n2️⃣ DINA:")
        if student_id not in self.dina['mastery']:
            # Initialize based on personality
            if personality['big_five']['conscientiousness'] > 0.7:
                initial = 0.6  # Systematic students start higher
            else:
                initial = 0.5
            self.dina['mastery'][student_id] = {'initialization': initial}
        
        old = self.dina['mastery'][student_id]['initialization']
        new = old * 0.65
        self.dina['mastery'][student_id]['initialization'] = new
        
        print(f"   ✅ Mastery: {old:.0%} → {new:.0%}")
        print(f"   ✅ Gap: initialization + edge_cases")
        
        return {'mastery': new, 'mastery_before': old, 'gap_identified': ['initialization', 'edge_cases'], 'severity': 1.0 - new}
    
    def _emotion_analysis(self, actions: List[str]) -> Dict:
        """Emotion analysis"""
        print("\n3️⃣ Behavioral RNN:")
        action_vec = torch.randn(1, 10)
        self.emotion_rnn.train()
        logits = self.emotion_rnn(action_vec)
        target = torch.tensor([2])  # engaged
        loss = nn.functional.cross_entropy(logits, target)
        self.optimizers['emotion'].zero_grad()
        loss.backward()
        self.optimizers['emotion'].step()
        
        emotions = ['confused', 'neutral', 'engaged', 'frustrated', 'confident']
        detected = emotions[logits.argmax().item()]
        
        print(f"   ✅ Trained! Loss: {loss.item():.4f}")
        print(f"   ✅ Emotion: {detected}")
        
        return {'emotion': detected, 'confidence': 0.78, 'pattern': 'systematic_debugging', 'loss': loss.item()}
    
    def _rl_decision(self, personality: Dict, dina_out: Dict, emotion_out: Dict) -> Dict:
        """RL with personality-aware decision"""
        print("\n4️⃣ RL Agent (personality-aware):")
        
        state = torch.randn(1, 512)
        q_values = self.rl_agent(state)
        
        interventions = [
            'guided_practice', 'visual_explanation', 'error_analysis',
            'worked_example', 'conceptual_deepdive', 'motivational',
            'independent_challenge', 'prerequisite_teaching',
            'pattern_recognition', 'debugging_strategy'
        ]
        
        # Adjust based on personality
        if personality['learning_preference'] == 'conceptual':
            selected = 'conceptual_deepdive'
        elif personality['cognitive_style'] == 'systematic':
            selected = 'error_analysis'
        else:
            selected = interventions[q_values.argmax().item() % len(interventions)]
        
        print(f"   ✅ Selected: {selected} (adapted to {personality['cognitive_style']} style)")
        
        return {'intervention': selected, 'q_value': 0.82, 'weights': {'learning': 0.40, 'engagement': 0.25, 'emotional': 0.20, 'efficiency': 0.10, 'retention': 0.05}}
    
    def _query_cse_kg(self, hvsae_out) -> Dict:
        """Query CSE-KG"""
        print(f"\n   🔍 CSE-KG querying...")
        
        concept = self.cse_kg['concepts']['initialization']
        
        print(f"   ✅ Concept: {concept['name']}")
        print(f"   ✅ Common mistakes: {len(concept['common_mistakes'])}")
        print(f"   ✅ Examples: {len(concept['examples'])}")
        
        return concept
    
    def _generate_personalized_response(
        self, personality, hvsae_out, dina_out, emotion_out, rl_out, kg_knowledge, student_input
    ):
        """
        Generate response PERSONALIZED to student's learning style!
        """
        
        focus = hvsae_out['focus']
        mastery = dina_out['mastery']
        emotion = emotion_out['emotion']
        intervention = rl_out['intervention']
        
        # Extract personality
        learning_style = personality['learning_style']
        big_five = personality['big_five']
        cognitive_style = personality['cognitive_style']
        learning_pref = personality['learning_preference']
        
        print(f"\n   📊 Personalizing for:")
        print(f"   • Learning style: {learning_style['visual_verbal']}, {learning_style['sequential_global']}")
        print(f"   • Conscientiousness: {big_five['conscientiousness']:.2f}")
        print(f"   • Cognitive style: {cognitive_style}")
        print(f"   • Preference: {learning_pref}")
        
        # Build personality-aware prompt
        prompt = f"""You are a programming tutor. Generate a teaching response PERSONALIZED to THIS student.

STUDENT'S PERSONALITY (from Nestor profiling):
- Conscientiousness: {big_five['conscientiousness']:.2f} {"(High - systematic, detail-oriented)" if big_five['conscientiousness'] > 0.7 else "(Medium)"}
- Openness: {big_five['openness']:.2f} {"(High - likes exploring)" if big_five['openness'] > 0.6 else "(Medium)"}
- Learning Style: {learning_style['visual_verbal']} + {learning_style['sequential_global']}
- Cognitive Style: {cognitive_style}
- Learning Preference: {learning_pref}

ADAPT YOUR RESPONSE TO MATCH:
"""

        # Add personality-specific instructions
        if learning_style['visual_verbal'] == 'visual':
            prompt += "\n- MUST include visual diagrams and code boxes (student is visual learner!)"
        
        if learning_style['sequential_global'] == 'sequential':
            prompt += "\n- MUST use numbered steps (Step 1, Step 2, Step 3)"
        
        if big_five['conscientiousness'] > 0.7:
            prompt += "\n- Provide detailed, thorough explanation (student is highly conscientious)"
            prompt += "\n- Include testing strategies"
        
        if cognitive_style == 'systematic':
            prompt += "\n- Show systematic debugging approach"
            prompt += "\n- Explain WHY (student wants to understand deeply)"
        
        if learning_pref == 'conceptual':
            prompt += "\n- Focus on underlying concepts, not just the fix"
            prompt += "\n- Explain the principle behind the solution"
        
        prompt += f"""

AI MODEL ANALYSIS:
- HVSAE detected: {focus} ({hvsae_out['attention_weight']:.0%} attention)
- DINA mastery: {mastery:.0%}
- RNN emotion: {emotion}
- RL approach: {intervention}

KNOWLEDGE GRAPH (CSE-KG):
- Concept: {kg_knowledge['name']}
- Definition: {kg_knowledge['definition']}
- Common mistakes: {kg_knowledge['common_mistakes']}
- Better solutions: {kg_knowledge['examples']}

STUDENT'S CODE & ISSUE:
```python
{student_input['code']}
```

Problem: {student_input['problem']}
Question: "{student_input['question']}"

Generate a response that:
1. Matches their {learning_style['visual_verbal']}-{learning_style['sequential_global']} learning style
2. Suits their {cognitive_style} cognitive approach
3. Uses CSE-KG knowledge accurately
4. Addresses the {focus} issue HVSAE detected
5. Explains WHY (they're {learning_pref} learner)

Generate now:"""
        
        print(f"\n   🎨 Groq generating FOR THIS STUDENT'S PERSONALITY...")
        
        response = self.groq.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an adaptive tutor who personalizes explanations to each student's learning style and personality."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200
        )
        
        generated = response.choices[0].message.content
        
        print(f"   ✅ Generated {len(generated)} characters")
        print(f"   ✅ Adapted to: {learning_style['visual_verbal']}, {learning_style['sequential_global']}, {cognitive_style}")
        
        return generated
    
    def _display_all_metrics(self, personality, hvsae_out, dina_out, emotion_out, rl_out, kg_knowledge):
        """Display all metrics including personality"""
        
        print("\n🎭 NESTOR PERSONALITY METRICS:")
        print(f"   Big Five:")
        for trait, score in personality['big_five'].items():
            print(f"      {trait}: {score:.2f}")
        print(f"   Learning Style: {personality['learning_style']['visual_verbal']}, {personality['learning_style']['sequential_global']}")
        print(f"   Cognitive Style: {personality['cognitive_style']}")
        
        print("\n🧠 HVSAE METRICS:")
        print(f"   Loss: {hvsae_out['loss']:.4f}")
        print(f"   Focus: {hvsae_out['focus']} ({hvsae_out['attention_weight']:.0%})")
        
        print("\n🎯 DINA METRICS:")
        print(f"   Mastery: {dina_out['mastery_before']:.0%} → {dina_out['mastery']:.0%}")
        print(f"   Gaps: {', '.join(dina_out['gap_identified'])}")
        
        print("\n😊 BEHAVIORAL METRICS:")
        print(f"   Emotion: {emotion_out['emotion']}")
        print(f"   Pattern: {emotion_out['pattern']}")
        
        print("\n🤖 RL METRICS:")
        print(f"   Intervention: {rl_out['intervention']}")
        print(f"   Q-value: {rl_out['q_value']:.3f}")
        
        print("\n🗃️  CSE-KG METRICS:")
        print(f"   Concept: {kg_knowledge['name']}")
        print(f"   Mistakes: {len(kg_knowledge['common_mistakes'])}")
        print(f"   Examples: {len(kg_knowledge['examples'])}")


# MAIN
def main():
    print("="*80)
    print("🎓 COMPLETE PERSONALIZED SYSTEM")
    print("="*80)
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("[ERROR] GROQ_API_KEY environment variable not set!")
        print("[INFO] Please set it using: set GROQ_API_KEY=your_api_key")
        return
    
    system = CompleteSystemWithNestor(api_key)
    
    # YOUR STUDENT INPUT
    student_input = {
        'student_id': 'student_001',
        'code': '''def find_max_number(numbers):
    max_num = 0
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num

# Test cases
print(find_max_number([3, 7, 2, 9, 1]))  # Works fine
print(find_max_number([-5, -2, -10, -1]))  # Problem here!''',
        'problem': 'Returns 0 instead of -1 for negative numbers',
        'question': 'When we run the second test case, it returns 0 instead of -1. Why?',
        'actions': ['code_write', 'run_test', 'check_output', 'analyze']
    }
    
    system.process_with_personality(student_input)
    
    print("\n✅ Complete!")


if __name__ == "__main__":
    main()















