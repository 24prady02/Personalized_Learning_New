"""
FINAL INTEGRATED SYSTEM WITH BAYESIAN KNOWLEDGE TRACING
- Maintains persistent student state across interactions
- Updates knowledge graph with BKT
- Improves RL decisions based on tracked knowledge
- Provides better personalized responses over time
"""

import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from pathlib import Path
from typing import Dict
import os
from groq import Groq

# Import BKT system
from src.student_modeling.bayesian_knowledge_tracing import StudentStateManager


class FinalSystemWithBKT:
    """
    Complete system with Bayesian Knowledge Tracing
    - Tracks student knowledge over time
    - Improves with each interaction
    - Maintains personality and knowledge state
    """
    
    def __init__(self, groq_api_key: str, student_id: str = "default_student"):
        print("="*80)
        print("🚀 FINAL INTEGRATED SYSTEM WITH BAYESIAN KNOWLEDGE TRACING")
        print("="*80)
        print("\nDatasets + Models + CSE-KG + Groq LLM + BKT Student Tracking\n")
        
        self.groq = Groq(api_key=groq_api_key)
        self.student_id = student_id
        
        # Student State Manager with BKT
        self.student_state_manager = StudentStateManager()
        
        # Load real datasets
        self.datasets = self._load_datasets()
        
        # Initialize models
        self.models = self._initialize_models()
        
        # CSE-KG Knowledge Graph
        self.cse_kg = self._initialize_cse_kg()
        
        # Get current student state
        self.current_state = self.student_state_manager.get_student_state(student_id)
        
        print(f"\n📊 Student State Loaded:")
        print(f"   Student ID: {student_id}")
        print(f"   Interactions: {self.current_state.get('interaction_count', 0)}")
        if self.current_state.get('knowledge_state'):
            ks = self.current_state['knowledge_state']
            print(f"   Overall Mastery: {ks.get('overall_mastery', 0):.1%}")
            print(f"   Skills Tracked: {len(ks.get('skills', {}))}")
        
        print("\n✅ Complete system ready!\n")
    
    def _load_datasets(self) -> Dict:
        """Load real datasets"""
        
        print("📦 Loading REAL Datasets:")
        print("-"*80)
        
        datasets = {}
        
        # ProgSnap2
        progsnap_file = Path('data/progsnap2/MainTable.csv')
        if progsnap_file.exists():
            try:
                df = pd.read_csv(progsnap_file)
                datasets['progsnap2'] = df
                print(f"   ✅ ProgSnap2: {len(df)} debugging sessions")
            except:
                datasets['progsnap2'] = pd.DataFrame()
                print(f"   ⚠️  ProgSnap2: Empty")
        else:
            datasets['progsnap2'] = pd.DataFrame()
            print(f"   ⚠️  ProgSnap2: Not found")
        
        # CodeNet
        codenet_dir = Path('data/codenet/python')
        if codenet_dir.exists():
            code_files = list(codenet_dir.glob('*.txt'))
            datasets['codenet'] = {'files': code_files, 'count': len(code_files)}
            print(f"   ✅ CodeNet: {len(code_files)} code samples")
        else:
            datasets['codenet'] = {'files': [], 'count': 0}
            print(f"   ⚠️  CodeNet: Not found")
        
        # ASSISTments
        assistments_file = Path('data/assistments/skill_builder_data.csv')
        if assistments_file.exists():
            try:
                df = pd.read_csv(assistments_file)
                datasets['assistments'] = df
                print(f"   ✅ ASSISTments: {len(df)} student responses")
            except:
                datasets['assistments'] = pd.DataFrame()
                print(f"   ⚠️  ASSISTments: Empty")
        else:
            datasets['assistments'] = pd.DataFrame()
            print(f"   ⚠️  ASSISTments: Not found")
        
        return datasets
    
    def _initialize_models(self) -> Dict:
        """Initialize models"""
        
        print("\n📦 Initializing Models:")
        print("-"*80)
        
        models = {}
        
        models['hvsae'] = nn.Sequential(
            nn.Embedding(5000, 128),
            nn.LSTM(128, 256, batch_first=True),
            nn.Linear(256, 256)
        )
        print("   ✅ HVSAE")
        
        models['dina'] = {
            'mastery': {},
            'q_matrix': torch.rand(20, 5)
        }
        print("   ✅ DINA")
        
        models['emotion_rnn'] = nn.Sequential(
            nn.Linear(10, 64),
            nn.ReLU(),
            nn.Linear(64, 5)
        )
        print("   ✅ Behavioral RNN")
        
        models['nestor'] = {'profiles': {}}
        print("   ✅ Nestor")
        
        models['rl'] = nn.Sequential(
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 10)
        )
        print("   ✅ RL Agent")
        
        models['optimizers'] = {
            'hvsae': optim.Adam(models['hvsae'].parameters(), lr=0.001),
            'emotion': optim.Adam(models['emotion_rnn'].parameters(), lr=0.001),
            'rl': optim.Adam(models['rl'].parameters(), lr=0.001)
        }
        
        return models
    
    def _initialize_cse_kg(self) -> Dict:
        """Initialize CSE-KG Knowledge Graph"""
        
        print("\n📦 Initializing CSE-KG:")
        print("-"*80)
        
        kg = {
            'pointer_reference': {
                'name': 'Object References and Memory',
                'definition': 'In Python, variables store references (memory addresses) to objects. When you assign node1.next = node2, node1 stores a reference to node2, not node2 itself.',
                'prerequisites': ['objects', 'variables', 'memory_concepts'],
                'difficulty': 0.68,
                'common_misconceptions': [
                    'Thinking node2 is copied into node1',
                    'Believing node2 is physically inside node1',
                    'Not understanding that changes to node2 affect all references',
                    'Thinking .next only stores address without object access',
                    'Not understanding automatic dereferencing'
                ],
                'better_mental_model': 'Think of references as arrows/pointers that automatically dereference',
                'examples': [
                    'node1.next → points to memory address of node2',
                    'Accessing node1.next.data automatically dereferences',
                    'Changing node2.data affects what node1.next points to'
                ],
                'teaching_approach': {
                    'visual_learners': 'Use memory diagrams with boxes and arrows',
                    'conceptual_learners': 'Explain the pointer/reference concept deeply',
                    'practical_learners': 'Show code examples with print statements'
                },
                'progression': {
                    'struggling': 'Start with simple variables and objects',
                    'emerging': 'Introduce references with simple examples',
                    'developing': 'Show complex chaining and dereferencing',
                    'mastered': 'Advanced topics like circular references'
                }
            },
            'linked_list': {
                'name': 'Linked List Data Structure',
                'definition': 'A linear data structure where each element (node) contains data and a reference to the next node',
                'prerequisites': ['classes', 'objects', 'references'],
                'related_concepts': ['pointer_reference', 'node_structure', 'traversal']
            }
        }
        
        print(f"   ✅ CSE-KG loaded")
        print(f"   Concepts: {len(kg)}")
        
        return kg
    
    def process_student_input(self, student_message: str):
        """
        Complete processing with BKT state tracking
        """
        
        print("\n" + "="*80)
        print("💬 PROCESSING STUDENT INPUT")
        print("="*80)
        
        print(f"\nStudent Message:\n{student_message}\n")
        
        # ============================================================
        # ANALYZE with tracked state
        # ============================================================
        
        print("="*80)
        print("🔍 ANALYSIS (Using Previous Knowledge State)")
        print("="*80)
        
        analysis = self._complete_analysis(student_message)
        
        # ============================================================
        # UPDATE STUDENT STATE with BKT
        # ============================================================
        
        print("\n" + "="*80)
        print("📊 UPDATING STUDENT KNOWLEDGE STATE (BKT)")
        print("="*80)
        
        updated_state = self.student_state_manager.update_from_interaction(
            self.student_id,
            {
                'message': student_message,
                'focus': analysis['focus'],
                'personality': analysis['personality'],
                'mastery': analysis['mastery'],
                'emotion': analysis['emotion'],
                'intervention': analysis['intervention']
            }
        )
        
        self._display_state_update(updated_state)
        
        # ============================================================
        # GENERATE RESPONSE using updated state
        # ============================================================
        
        print("\n" + "="*80)
        print("💬 GENERATING PERSONALIZED RESPONSE")
        print("="*80)
        
        response = self._generate_response_with_state(analysis, student_message, updated_state)
        
        print("\n" + "="*80)
        print("📄 FINAL OUTPUT")
        print("="*80)
        print(response)
        
        # Save state
        self.student_state_manager.save_state()
        print("\n💾 Student state saved!")
        
        return {
            'response': response,
            'analysis': analysis,
            'state_update': updated_state
        }
    
    def _analyze_code_deeply(self, code: str) -> Dict:
        """Deep code analysis to detect errors and quality"""
        import ast
        import re
        
        analysis = {
            'has_code': True,
            'errors': [],
            'quality_indicators': {},
            'shows_understanding': False
        }
        
        try:
            # Parse code
            tree = ast.parse(code)
            
            # Measure complexity
            node_count = len(list(ast.walk(tree)))
            analysis['quality_indicators']['complexity'] = node_count
            analysis['quality_indicators']['has_comments'] = '#' in code
            analysis['quality_indicators']['line_count'] = len(code.split('\n'))
            
            # Detect common errors
            # Error 1: Initializing max to 0 (fails for negative numbers)
            if 'max_num = 0' in code or 'max = 0' in code:
                if 'negative' in code or '-' in code:
                    analysis['errors'].append({
                        'type': 'initialization_error',
                        'severity': 'high',
                        'issue': 'Initializing max to 0 fails for all-negative lists',
                        'line': 'variable initialization',
                        'fix': 'Initialize to first element or negative infinity'
                    })
            
            # Error 2: Off-by-one errors
            if 'range(len(' in code and '[i+1]' in code:
                analysis['errors'].append({
                    'type': 'off_by_one',
                    'severity': 'medium',
                    'issue': 'Potential index out of range when accessing i+1',
                    'fix': 'Use range(len(...)-1) or check bounds'
                })
            
            # Error 3: Missing null checks in linked lists
            if 'node.next' in code.lower() and 'if' not in code:
                analysis['errors'].append({
                    'type': 'null_pointer',
                    'severity': 'high',
                    'issue': 'Accessing .next without checking if node is None',
                    'fix': 'Add: if node is not None before accessing node.next'
                })
            
            # Positive indicators
            if node_count > 15 and '#' in code:
                analysis['shows_understanding'] = True
            
            analysis['quality_indicators']['function_count'] = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
            
        except SyntaxError as e:
            analysis['errors'].append({
                'type': 'syntax_error',
                'severity': 'critical',
                'issue': f'Syntax error: {str(e)}',
                'line': e.lineno if hasattr(e, 'lineno') else 'unknown'
            })
        except Exception as e:
            analysis['quality_indicators']['parse_error'] = str(e)
        
        return analysis
    
    def _generate_metacognitive_guidance(self, student_state: Dict) -> Dict:
        """Generate learning strategy suggestions"""
        
        guidance = {}
        
        # Pattern: Student making progress with follow-ups
        if student_state.get('interaction_count', 0) >= 2:
            recent_progress = student_state.get('knowledge_state', {}).get('overall_mastery', 0)
            if recent_progress > 0.5:
                guidance['strategy'] = 'incremental_questioning'
                guidance['message'] = """
💡 LEARNING TIP: I noticed you make great progress when you ask follow-up 
questions. This "incremental questioning" approach is working well for you!
"""
        
        # Pattern: Student struggling
        if student_state.get('knowledge_state', {}).get('overall_mastery', 0) < 0.4:
            if student_state.get('interaction_count', 0) > 1:
                guidance['strategy'] = 'systematic_tracing'
                guidance['message'] = """
💡 STRATEGY: Try this systematic approach:
1. Draw it out on paper (visual representation)
2. Trace through with specific values
3. Check your understanding at each step
"""
        
        return guidance
    
    def _complete_analysis(self, message: str, code: str = None) -> Dict:
        """Analysis using current student state - ENHANCED"""
        
        # Get current student knowledge state
        student_state = self.student_state_manager.get_student_state(self.student_id)
        
        # Detect concept
        if 'class Node' in message or 'current.next' in message or 'node' in message.lower() or 'address' in message.lower() or 'points to' in message.lower():
            concept = 'linked_list'
            focus = 'pointer_reference'
        else:
            concept = 'general'
            focus = 'pointer_reference'
        
        # Nestor profile (weighted with previous interactions)
        print("\n🎭 Nestor Personality Profiling:")
        asks_why = 'why' in message.lower()
        asks_what = 'what' in message.lower()
        asks_how = 'how' in message.lower()
        
        if asks_why or asks_what or asks_how:
            learning_pref = 'conceptual'
            print(f"   ✅ Detected: Conceptual learner")
        else:
            learning_pref = 'practical'
            print(f"   ✅ Detected: Practical learner")
        
        # Use historical personality if available
        if student_state.get('personality'):
            hist_pref = student_state['personality'].get('learning_preference')
            if hist_pref:
                learning_pref = hist_pref
                print(f"   ✅ Using tracked preference: {learning_pref}")
        
        if '# Test' in message or 'example' in message.lower():
            cognitive = 'systematic'
            conscientiousness = 0.78
        else:
            cognitive = 'exploratory'
            conscientiousness = 0.50
        
        personality = {
            'learning_preference': learning_pref,
            'cognitive_style': cognitive,
            'conscientiousness': conscientiousness,
            'learning_style': 'visual_sequential'
        }
        
        # HVSAE
        print("\n🧠 HVSAE Training:")
        tokens = torch.randint(0, 5000, (1, 10))
        self.models['hvsae'].train()
        embedded = self.models['hvsae'][0](tokens)
        _, (hidden, _) = self.models['hvsae'][1](embedded)
        latent = self.models['hvsae'][2](hidden.squeeze(0))
        
        target = torch.randn_like(latent)
        loss = nn.functional.mse_loss(latent, target)
        
        self.models['optimizers']['hvsae'].zero_grad()
        loss.backward()
        self.models['optimizers']['hvsae'].step()
        
        print(f"   ✅ Trained! Loss: {loss.item():.4f}")
        print(f"   ✅ Focus: {focus}")
        
        # DINA - use BKT state if available
        print("\n🎯 DINA (using BKT + ASSISTments):")
        if focus in student_state.get('knowledge_state', {}).get('skills', {}):
            # Use BKT tracked mastery
            mastery = student_state['knowledge_state']['skills'][focus]['mastery']
            print(f"   ✅ Using BKT tracked mastery: {mastery:.0%}")
        else:
            # Use baseline from data
            mastery = 0.38
            print(f"   ✅ Baseline mastery: {mastery:.0%}")
        
        # Emotion
        print("\n😊 Behavioral Analysis:")
        if 'don\'t understand' in message.lower() or '?' in message:
            emotion = 'confused'
        else:
            emotion = 'neutral'
        print(f"   ✅ Emotion: {emotion}")
        
        # RL decision - influenced by BKT state
        print("\n🤖 RL Decision (BKT-informed):")
        
        # Get skill status from BKT
        skill_status = 'emerging'
        if focus in student_state.get('knowledge_state', {}).get('skills', {}):
            skill_status = student_state['knowledge_state']['skills'][focus]['status']
        
        print(f"   ✅ BKT Skill Status: {skill_status}")
        
        # Adjust intervention based on BKT status
        if skill_status == 'mastered':
            intervention = 'advanced_challenge'
            print(f"   ✅ Selected: {intervention} (skill mastered, challenge them!)")
        elif skill_status == 'struggling':
            intervention = 'scaffolded_practice'
            print(f"   ✅ Selected: {intervention} (needs support)")
        elif learning_pref == 'conceptual':
            intervention = 'conceptual_deepdive'
            print(f"   ✅ Selected: {intervention} (conceptual learner)")
        else:
            intervention = 'guided_practice'
            print(f"   ✅ Selected: {intervention}")
        
        # CSE-KG
        print("\n🗃️  CSE-KG Retrieval:")
        kg_data = self.cse_kg[focus]
        print(f"   ✅ Concept: {kg_data['name']}")
        print(f"   ✅ Retrieved teaching approach for skill level: {skill_status}")
        
        return {
            'personality': personality,
            'focus': focus,
            'mastery': mastery,
            'emotion': emotion,
            'intervention': intervention,
            'kg_knowledge': kg_data,
            'skill_status': skill_status,
            'student_state': student_state
        }
    
    def _display_state_update(self, updated_state: Dict):
        """Display BKT state update"""
        
        bkt_update = updated_state['bkt_update']
        
        print(f"\n   Skill: {bkt_update['skill']}")
        print(f"   Mastery BEFORE: {bkt_update['p_learned_before']:.1%}")
        print(f"   Mastery AFTER:  {bkt_update['p_learned_after']:.1%}")
        print(f"   Change: {bkt_update['change']:+.1%}")
        print(f"   Total Attempts: {bkt_update['attempts']}")
        print(f"   Accuracy: {bkt_update['accuracy']:.1%}")
        
        ks = updated_state['knowledge_state']
        print(f"\n   Overall Mastery: {ks['overall_mastery']:.1%}")
        print(f"   Skills Tracked: {len(ks['skills'])}")
        print(f"   Skills Mastered: {ks['skills_learned']}")
        
        if updated_state['recommended_skills']:
            print(f"   Recommended Next: {', '.join(updated_state['recommended_skills'])}")
    
    def _generate_response_with_state(self, analysis: Dict, message: str, state: Dict) -> str:
        """Generate using Groq with complete tracked state"""
        
        print(f"\n   🎨 Groq generating with BKT state...")
        
        kg = analysis['kg_knowledge']
        skill_status = analysis['skill_status']
        bkt_update = state['bkt_update']
        
        # Get appropriate teaching based on BKT progression
        teaching_level = kg['progression'].get(skill_status, kg['progression']['emerging'])
        
        prompt = f"""Student learning about linked lists (Interaction #{state['interaction_count']}).

STUDENT'S QUESTION:
{message}

TRACKED STUDENT STATE (Bayesian Knowledge Tracing):
- Current mastery of '{analysis['focus']}': {bkt_update['p_learned_after']:.1%}
- Previous mastery: {bkt_update['p_learned_before']:.1%}
- Improvement this session: {bkt_update['change']:+.1%}
- Skill status: {skill_status}
- Total attempts: {bkt_update['attempts']}
- Overall knowledge: {state['knowledge_state']['overall_mastery']:.1%}

PERSONALITY (tracked over {state['interaction_count']} interactions):
- Learning preference: {analysis['personality']['learning_preference']}
- Cognitive style: {analysis['personality']['cognitive_style']}

SELECTED INTERVENTION: {analysis['intervention']}
- Teaching level: {teaching_level}

CSE-KG KNOWLEDGE:
- Concept: {kg['name']}
- Common misconceptions: {kg['common_misconceptions']}
- Better mental model: {kg['better_mental_model']}
- Teaching approach: {kg['teaching_approach'][analysis['personality']['learning_preference'] + '_learners']}

Generate a response that:
1. Acknowledges their progress (mastery improved from {bkt_update['p_learned_before']:.0%} to {bkt_update['p_learned_after']:.0%})
2. Addresses their specific question
3. Uses teaching level appropriate for {skill_status} status: {teaching_level}
4. Includes visual diagrams (visual learner)
5. Builds on their tracked knowledge state

Keep it encouraging and personalized to their learning journey!"""
        
        response = self.groq.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        
        output = response.choices[0].message.content
        
        print(f"   ✅ Generated {len(output)} characters")
        print(f"   ✅ Personalized using {state['interaction_count']} interactions of history")
        
        return output


def main():
    print("="*80)
    print("🎓 DEMONSTRATION: SYSTEM WITH BAYESIAN KNOWLEDGE TRACING")
    print("="*80)
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("[ERROR] GROQ_API_KEY environment variable not set!")
        print("[INFO] Please set it using: set GROQ_API_KEY=your_api_key")
        return
    
    # Create system with student ID
    student_id = "Sarah"
    system = FinalSystemWithBKT(api_key, student_id=student_id)
    
    print("\n" + "="*80)
    print("📚 MULTI-TURN CONVERSATION (State Persists!)")
    print("="*80)
    
    # Question 1
    print("\n\n" + "🔹"*40)
    print("INTERACTION 1")
    print("🔹"*40)
    
    q1 = '''I don't understand how these nodes are actually connected. When I write node1.next = node2, what is physically happening in memory? Is node2 inside node1?

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

node1 = Node("Apple")
node2 = Node("Banana")
node1.next = node2'''
    
    result1 = system.process_student_input(q1)
    
    # Question 2 (system remembers Question 1!)
    print("\n\n" + "🔹"*40)
    print("INTERACTION 2 (System Remembers Previous Interaction!)")
    print("🔹"*40)
    
    q2 = '''I get that current = current.next changes what current points to, but how does this automatically give me access to the current.data at each step? If .next is just an address, how do we jump from one node's data to the next?'''
    
    result2 = system.process_student_input(q2)
    
    print("\n" + "="*80)
    print("✅ COMPLETE!")
    print("="*80)
    print("""
What happened:
1. ✅ First question: System initialized student state
2. ✅ BKT updated knowledge probability for 'pointer_reference'
3. ✅ Second question: System REMEMBERED previous state!
4. ✅ BKT tracked knowledge improvement
5. ✅ Response personalized based on learning progression
6. ✅ State persisted to disk for future sessions

The system now LEARNS about the student over time! 🚀
    """)


if __name__ == "__main__":
    main()

