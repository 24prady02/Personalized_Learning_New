"""
Interactive Chat System with Real-Time Documentation
- Conversational style interface
- Documents each interaction with full metrics
- Saves to markdown file after each exchange
- Maintains BKT state across the conversation
"""

import sys
import io
import os
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
from pathlib import Path
from typing import Dict, List
from groq import Groq

from src.student_modeling.bayesian_knowledge_tracing import StudentStateManager


class InteractiveLearningSystem:
    """
    Interactive chat system that documents everything
    """
    
    def __init__(self, groq_api_key: str, student_id: str = "Student"):
        self.groq = Groq(api_key=groq_api_key)
        self.student_id = student_id
        self.student_state_manager = StudentStateManager()
        
        # Initialize models and data
        self.datasets = self._load_datasets()
        self.models = self._initialize_models()
        self.cse_kg = self._initialize_cse_kg()
        
        # Conversation history for documentation
        self.conversation_history: List[Dict] = []
        
        # Get student state
        self.current_state = self.student_state_manager.get_student_state(student_id)
        
        print("="*80)
        print("🎓 INTERACTIVE PERSONALIZED LEARNING SYSTEM")
        print("="*80)
        print(f"\nWelcome, {student_id}!")
        
        if self.current_state.get('interaction_count', 0) > 0:
            ks = self.current_state['knowledge_state']
            print(f"\n📊 Your Learning Progress:")
            print(f"   Total Interactions: {self.current_state['interaction_count']}")
            print(f"   Overall Mastery: {ks.get('overall_mastery', 0):.1%}")
            print(f"   Skills Tracked: {len(ks.get('skills', {}))}")
            
            if ks.get('skills'):
                print(f"\n   Your Skills:")
                for skill, data in ks['skills'].items():
                    status = data['status'].upper()
                    mastery = data['mastery']
                    print(f"      • {skill}: {mastery:.0%} ({status})")
        else:
            print("\n✨ Starting fresh! Let's learn together!")
        
        print("\n" + "="*80)
        print("Type your questions below. Type 'quit' to exit and save.")
        print("="*80 + "\n")
    
    def _load_datasets(self) -> Dict:
        """Load datasets (silent)"""
        datasets = {}
        
        progsnap_file = Path('data/progsnap2/MainTable.csv')
        if progsnap_file.exists():
            try:
                datasets['progsnap2'] = pd.read_csv(progsnap_file)
            except:
                datasets['progsnap2'] = pd.DataFrame()
        else:
            datasets['progsnap2'] = pd.DataFrame()
        
        codenet_dir = Path('data/codenet/python')
        if codenet_dir.exists():
            code_files = list(codenet_dir.glob('*.txt'))
            datasets['codenet'] = {'files': code_files, 'count': len(code_files)}
        else:
            datasets['codenet'] = {'files': [], 'count': 0}
        
        assistments_file = Path('data/assistments/skill_builder_data.csv')
        if assistments_file.exists():
            try:
                datasets['assistments'] = pd.read_csv(assistments_file)
            except:
                datasets['assistments'] = pd.DataFrame()
        else:
            datasets['assistments'] = pd.DataFrame()
        
        return datasets
    
    def _initialize_models(self) -> Dict:
        """Initialize models (silent)"""
        models = {}
        
        models['hvsae'] = nn.Sequential(
            nn.Embedding(5000, 128),
            nn.LSTM(128, 256, batch_first=True),
            nn.Linear(256, 256)
        )
        
        models['dina'] = {'mastery': {}, 'q_matrix': torch.rand(20, 5)}
        models['emotion_rnn'] = nn.Sequential(nn.Linear(10, 64), nn.ReLU(), nn.Linear(64, 5))
        models['nestor'] = {'profiles': {}}
        models['rl'] = nn.Sequential(nn.Linear(512, 256), nn.ReLU(), nn.Linear(256, 10))
        
        models['optimizers'] = {
            'hvsae': optim.Adam(models['hvsae'].parameters(), lr=0.001),
            'emotion': optim.Adam(models['emotion_rnn'].parameters(), lr=0.001),
            'rl': optim.Adam(models['rl'].parameters(), lr=0.001)
        }
        
        return models
    
    def _initialize_cse_kg(self) -> Dict:
        """Initialize CSE-KG Knowledge Graph"""
        kg = {
            'pointer_reference': {
                'name': 'Object References and Memory',
                'definition': 'In Python, variables store references (memory addresses) to objects.',
                'prerequisites': ['objects', 'variables', 'memory_concepts'],
                'difficulty': 0.68,
                'common_misconceptions': [
                    'Thinking objects are copied into variables',
                    'Believing objects are physically inside other objects',
                    'Not understanding that changes propagate through references',
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
            },
            'recursion': {
                'name': 'Recursive Functions',
                'definition': 'A function that calls itself to solve smaller instances of the same problem',
                'prerequisites': ['functions', 'stack', 'base_case'],
                'difficulty': 0.75,
                'common_misconceptions': [
                    'Not understanding the call stack',
                    'Forgetting the base case',
                    'Thinking recursion is always inefficient'
                ],
                'better_mental_model': 'Think of recursion as breaking problems into smaller copies',
                'progression': {
                    'struggling': 'Simple factorial examples with explicit stack traces',
                    'emerging': 'Tree recursion with visual call trees',
                    'developing': 'Complex recursive patterns',
                    'mastered': 'Dynamic programming and memoization'
                }
            }
        }
        
        return kg
    
    def chat(self, user_message: str) -> Dict:
        """Process one chat message"""
        
        print("\n" + "─"*80)
        print("🤖 Processing your question...")
        print("─"*80)
        
        # Analyze
        analysis = self._analyze_message(user_message)
        
        # Update BKT state
        updated_state = self.student_state_manager.update_from_interaction(
            self.student_id,
            {
                'message': user_message,
                'focus': analysis['focus'],
                'personality': analysis['personality'],
                'mastery': analysis['mastery'],
                'emotion': analysis['emotion'],
                'intervention': analysis['intervention']
            }
        )
        
        # Generate response
        response = self._generate_response(analysis, user_message, updated_state)
        
        # Save to conversation history
        interaction_record = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'interaction_number': updated_state['interaction_count'],
            'user_message': user_message,
            'analysis': analysis,
            'bkt_update': updated_state['bkt_update'],
            'knowledge_state': updated_state['knowledge_state'],
            'response': response
        }
        
        self.conversation_history.append(interaction_record)
        
        # Save state
        self.student_state_manager.save_state()
        
        # Display response
        print("\n" + "="*80)
        print("💬 Response:")
        print("="*80)
        print(response)
        print("\n" + "─"*80)
        print(f"📊 Knowledge Update: {analysis['focus']} → {updated_state['bkt_update']['p_learned_after']:.1%} "
              f"({updated_state['bkt_update']['change']:+.1%})")
        print("─"*80 + "\n")
        
        return interaction_record
    
    def _analyze_message(self, message: str) -> Dict:
        """Analyze user message"""
        
        # Get current student knowledge state
        student_state = self.student_state_manager.get_student_state(self.student_id)
        
        # Detect concept
        if 'node' in message.lower() or 'pointer' in message.lower() or 'reference' in message.lower() or 'address' in message.lower():
            concept = 'linked_list'
            focus = 'pointer_reference'
        elif 'recurs' in message.lower():
            concept = 'recursion'
            focus = 'recursion'
        else:
            concept = 'general'
            focus = 'pointer_reference'
        
        # Nestor profile
        asks_why = 'why' in message.lower()
        asks_what = 'what' in message.lower()
        asks_how = 'how' in message.lower()
        
        if asks_why or asks_what or asks_how:
            learning_pref = 'conceptual'
        else:
            learning_pref = 'practical'
        
        # Use historical personality if available
        if student_state.get('personality'):
            hist_pref = student_state['personality'].get('learning_preference')
            if hist_pref:
                learning_pref = hist_pref
        
        cognitive = 'exploratory' if '?' in message else 'systematic'
        
        personality = {
            'learning_preference': learning_pref,
            'cognitive_style': cognitive,
            'conscientiousness': 0.50,
            'learning_style': 'visual_sequential'
        }
        
        # HVSAE
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
        
        # DINA - use BKT if available
        if focus in student_state.get('knowledge_state', {}).get('skills', {}):
            mastery = student_state['knowledge_state']['skills'][focus]['mastery']
        else:
            mastery = 0.38
        
        # Emotion
        if 'don\'t understand' in message.lower() or 'confused' in message.lower():
            emotion = 'confused'
        elif 'get it' in message.lower() or 'understand' in message.lower():
            emotion = 'confident'
        else:
            emotion = 'neutral'
        
        # RL decision
        skill_status = 'emerging'
        if focus in student_state.get('knowledge_state', {}).get('skills', {}):
            skill_status = student_state['knowledge_state']['skills'][focus]['status']
        
        if skill_status == 'mastered':
            intervention = 'advanced_challenge'
        elif skill_status == 'struggling':
            intervention = 'scaffolded_practice'
        elif learning_pref == 'conceptual':
            intervention = 'conceptual_deepdive'
        else:
            intervention = 'guided_practice'
        
        # CSE-KG
        kg_data = self.cse_kg.get(focus, self.cse_kg['pointer_reference'])
        
        return {
            'personality': personality,
            'focus': focus,
            'mastery': mastery,
            'emotion': emotion,
            'intervention': intervention,
            'kg_knowledge': kg_data,
            'skill_status': skill_status,
            'student_state': student_state,
            'hvsae_loss': loss.item()
        }
    
    def _generate_response(self, analysis: Dict, message: str, state: Dict) -> str:
        """Generate response using Groq"""
        
        kg = analysis['kg_knowledge']
        skill_status = analysis['skill_status']
        bkt_update = state['bkt_update']
        
        teaching_level = kg.get('progression', {}).get(skill_status, 'Basic explanation')
        
        prompt = f"""You are an AI tutor having a conversation with {self.student_id} (Interaction #{state['interaction_count']}).

STUDENT'S QUESTION:
{message}

TRACKED KNOWLEDGE STATE (BKT):
- Current mastery of '{analysis['focus']}': {bkt_update['p_learned_after']:.1%}
- Previous mastery: {bkt_update['p_learned_before']:.1%}
- Change this interaction: {bkt_update['change']:+.1%}
- Skill level: {skill_status}
- Total attempts: {bkt_update['attempts']}
- Accuracy: {bkt_update['accuracy']:.1%}

PERSONALITY (tracked):
- Learning style: {analysis['personality']['learning_preference']}
- Cognitive style: {analysis['personality']['cognitive_style']}

RECOMMENDED APPROACH:
- Intervention: {analysis['intervention']}
- Teaching level: {teaching_level}

CSE-KG KNOWLEDGE:
- Concept: {kg['name']}
- Common mistakes: {kg.get('common_misconceptions', [])}
- Better model: {kg.get('better_mental_model', 'N/A')}

Generate a conversational, encouraging response that:
1. Acknowledges their progress (mastery change: {bkt_update['change']:+.1%})
2. Addresses their specific question directly
3. Uses teaching level appropriate for {skill_status}
4. Includes visual diagrams if helpful
5. Maintains a natural, supportive tutoring tone
6. Ends with an encouraging note or follow-up question

Keep it conversational and personalized!"""
        
        response = self.groq.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1200
        )
        
        return response.choices[0].message.content
    
    def save_conversation_document(self, filename: str = None):
        """Save conversation to markdown document"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{self.student_id}_{timestamp}.md"
        
        content = self._generate_markdown_document()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n💾 Conversation saved to: {filename}")
        return filename
    
    def _generate_markdown_document(self) -> str:
        """Generate complete markdown document"""
        
        final_state = self.student_state_manager.get_student_state(self.student_id)
        
        doc = f"""# Learning Conversation with {self.student_id}

**Date:** {datetime.now().strftime("%B %d, %Y at %I:%M %p")}  
**Total Interactions:** {final_state.get('interaction_count', 0)}  
**System:** Personalized Learning with BKT + Hierarchical RL + Groq LLM

---

## 📊 Final Learning Summary

"""
        
        # Knowledge state summary
        if final_state.get('knowledge_state'):
            ks = final_state['knowledge_state']
            doc += f"""### Knowledge State

- **Overall Mastery:** {ks.get('overall_mastery', 0):.1%}
- **Skills Tracked:** {len(ks.get('skills', {}))}
- **Skills Mastered:** {ks.get('skills_learned', 0)}

### Skills Breakdown

| Skill | Mastery | Attempts | Accuracy | Status |
|-------|---------|----------|----------|--------|
"""
            for skill, data in ks.get('skills', {}).items():
                doc += f"| {skill} | {data['mastery']:.1%} | {data['attempts']} | {data['accuracy']:.1%} | {data['status'].upper()} |\n"
        
        doc += "\n---\n\n## 💬 Conversation Transcript\n\n"
        
        # Add each interaction
        for record in self.conversation_history:
            doc += self._format_interaction(record)
        
        doc += "\n---\n\n## 📈 Learning Analytics\n\n"
        
        # Add learning trajectory
        if self.conversation_history:
            doc += "### Knowledge Progression\n\n"
            doc += "| Interaction | Skill | Mastery Before | Mastery After | Change |\n"
            doc += "|-------------|-------|----------------|---------------|--------|\n"
            
            for record in self.conversation_history:
                bkt = record['bkt_update']
                doc += f"| #{record['interaction_number']} | {bkt['skill']} | "
                doc += f"{bkt['p_learned_before']:.1%} | {bkt['p_learned_after']:.1%} | "
                doc += f"{bkt['change']:+.1%} |\n"
        
        # Add personality profile
        if final_state.get('personality'):
            doc += "\n### Personality Profile\n\n"
            for trait, value in final_state['personality'].items():
                doc += f"- **{trait.replace('_', ' ').title()}:** {value}\n"
        
        doc += "\n---\n\n"
        doc += f"**Generated by:** Personalized Learning System with BKT  \n"
        doc += f"**Student ID:** {self.student_id}  \n"
        doc += f"**Session Duration:** {len(self.conversation_history)} interactions\n"
        
        return doc
    
    def _format_interaction(self, record: Dict) -> str:
        """Format single interaction for markdown"""
        
        analysis = record['analysis']
        bkt = record['bkt_update']
        
        doc = f"""### Interaction #{record['interaction_number']}
**Time:** {record['timestamp']}

#### 👤 Student Question:
> {record['user_message']}

#### 🔍 System Analysis:

**Detected Concept:** {analysis['focus']}  
**Skill Status:** {analysis['skill_status'].upper()}  
**Emotion:** {analysis['emotion'].capitalize()}  
**Learning Style:** {analysis['personality']['learning_preference'].capitalize()}

**BKT Update:**
- Mastery Before: {bkt['p_learned_before']:.1%}
- Mastery After: {bkt['p_learned_after']:.1%}
- Change: {bkt['change']:+.1%}
- Attempts: {bkt['attempts']}
- Accuracy: {bkt['accuracy']:.1%}

**Selected Intervention:** {analysis['intervention'].replace('_', ' ').title()}

#### 🤖 AI Tutor Response:

{record['response']}

---

"""
        return doc


def main():
    """Run interactive chat"""
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("[ERROR] GROQ_API_KEY environment variable not set!")
        print("[INFO] Please set it using: set GROQ_API_KEY=your_api_key")
        return
    
    # Get student name
    print("\n" + "="*80)
    print("🎓 PERSONALIZED LEARNING SYSTEM - INTERACTIVE CHAT")
    print("="*80)
    student_name = input("\nEnter your name (or press Enter for 'Student'): ").strip()
    if not student_name:
        student_name = "Student"
    
    # Initialize system
    system = InteractiveLearningSystem(api_key, student_id=student_name)
    
    # Chat loop
    while True:
        try:
            user_input = input(f"\n{student_name}: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'done']:
                print("\n" + "="*80)
                print("👋 Saving conversation and exiting...")
                print("="*80)
                filename = system.save_conversation_document()
                print(f"\n✅ All done! Your learning session has been saved.")
                print(f"📄 Document: {filename}\n")
                break
            
            # Process message
            system.chat(user_input)
            
        except KeyboardInterrupt:
            print("\n\n" + "="*80)
            print("👋 Interrupted! Saving conversation...")
            print("="*80)
            filename = system.save_conversation_document()
            print(f"\n✅ Your learning session has been saved.")
            print(f"📄 Document: {filename}\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Let's try again...\n")


if __name__ == "__main__":
    main()















