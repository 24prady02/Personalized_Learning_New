"""
Simple Chat Interface for Personalized Learning System
Command-line interface without UI dependencies
"""

import sys
import io
import os
from datetime import datetime
from typing import List, Tuple, Optional, Dict

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from groq import Groq
from src.student_modeling.bayesian_knowledge_tracing import StudentStateManager

# Try to import enhanced generator, fallback to simple generation if not available
try:
    from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator
    HAS_ENHANCED_GENERATOR = True
except ImportError:
    HAS_ENHANCED_GENERATOR = False
    print("⚠️ Enhanced generator not found, using simple generation")


class ChatInterface:
    """
    Simple chat interface for personalized learning (no UI)
    """
    
    def __init__(self, groq_api_key: str):
        try:
            self.groq = Groq(api_key=groq_api_key)
        except Exception as e:
            print(f"❌ Error initializing Groq client: {e}")
            raise
        
        try:
            self.student_state_manager = StudentStateManager()
        except Exception as e:
            print(f"⚠️ Warning: Error initializing StudentStateManager: {e}")
            print("   Continuing with limited functionality...")
            self.student_state_manager = None
        
        # Initialize enhanced generator if available
        if HAS_ENHANCED_GENERATOR:
            try:
                self.generator = EnhancedPersonalizedGenerator(self.groq)
            except Exception as e:
                print(f"⚠️ Warning: Enhanced generator initialization failed: {e}")
                print("   Using simple response generation...")
                self.generator = None
        else:
            self.generator = None
        
        # Conversation history
        self.conversation_history = []
        
        # Current student
        self.current_student_id = "Student"
    
    def initialize_student(self, student_id: str):
        """Initialize or load student"""
        self.current_student_id = student_id if student_id else "Student"
        if self.student_state_manager:
            state = self.student_state_manager.get_student_state(self.current_student_id)
            return state
        else:
            return {
                'interaction_count': 0,
                'knowledge_state': {'overall_mastery': 0.0, 'skills': {}}
            }
    
    def process_message(
        self,
        message: str,
        code: Optional[str] = None
    ) -> Dict:
        """
        Process student message and generate personalized response
        
        Args:
            message: Student's question/message
            code: Optional code input
            
        Returns:
            Dictionary with response and analysis
        """
        
        if not message.strip():
            return {'response': '', 'analysis': {}}
        
        # Get current student state
        if self.student_state_manager:
            student_state = self.student_state_manager.get_student_state(self.current_student_id)
        else:
            # Fallback if BKT manager not available
            student_state = {
                'interaction_count': 0,
                'knowledge_state': {'overall_mastery': 0.3, 'skills': {}}
            }
        
        # Perform analysis (simplified version)
        analysis = self._quick_analysis(message, code, student_state)
        
        # Update BKT state
        if self.student_state_manager:
            updated_state = self.student_state_manager.update_from_interaction(
                self.current_student_id,
                {
                    'message': message,
                    'focus': analysis.get('focus', 'general'),
                    'personality': analysis.get('personality', {}),
                    'mastery': analysis.get('mastery', 0.5),
                    'emotion': analysis.get('emotion', 'neutral'),
                    'intervention': analysis.get('intervention', 'guided_practice')
                }
            )
            # Save state
            self.student_state_manager.save_state()
        else:
            # Fallback if BKT manager not available
            updated_state = student_state
            updated_state['interaction_count'] = updated_state.get('interaction_count', 0) + 1
        
        # Generate personalized response using enhanced generator or fallback
        if self.generator:
            try:
                response = self.generator.generate_personalized_response(
                    student_id=self.current_student_id,
                    student_message=message,
                    student_state=updated_state,
                    analysis=analysis,
                    code=code,
                    code_analysis=analysis.get('code_analysis')
                )
            except Exception as e:
                # Fallback to simple response if enhanced generator fails
                print(f"⚠️ Enhanced generator error: {e}, using fallback")
                response = self._generate_simple_response(message, code, updated_state, analysis)
        else:
            # Use simple response generation
            response = self._generate_simple_response(message, code, updated_state, analysis)
        
        # Update history
        self.conversation_history.append({
            'message': message,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
        return {
            'response': response,
            'analysis': analysis,
            'state': updated_state
        }
    
    def _quick_analysis(self, message: str, code: Optional[str], student_state: Dict) -> Dict:
        """Quick analysis of student input"""
        
        # Detect concept
        concept = 'general'
        if 'recursion' in message.lower() or (code and 'recursion' in code.lower()):
            concept = 'recursion'
        elif 'linked list' in message.lower() or 'node' in message.lower():
            concept = 'linked_list'
        elif 'pointer' in message.lower() or 'reference' in message.lower():
            concept = 'pointer_reference'
        
        # Detect emotion
        emotion = 'neutral'
        frustration = 0.5
        if 'confused' in message.lower() or "don't understand" in message.lower():
            emotion = 'confused'
            frustration = 0.65
        elif 'frustrated' in message.lower() or 'stuck' in message.lower():
            emotion = 'frustrated'
            frustration = 0.75
        elif 'understand' in message.lower() or 'got it' in message.lower():
            emotion = 'engaged'
            frustration = 0.3
        
        # Detect learning preference
        learning_preference = 'visual'
        if 'why' in message.lower() or 'how' in message.lower():
            learning_preference = 'conceptual'
        elif code and len(code) > 50:
            learning_preference = 'practical'
        
        # Get mastery
        knowledge_state = student_state.get('knowledge_state', {})
        mastery = knowledge_state.get('overall_mastery', 0.3)
        
        # Code analysis
        code_analysis = None
        if code:
            code_analysis = self._analyze_code(code)
        
        # BKT update info
        bkt_update = {
            'p_learned_before': mastery,
            'p_learned_after': min(mastery + 0.05, 1.0),  # Simplified
            'change': 0.05,
            'attempts': student_state.get('interaction_count', 0) + 1
        }
        
        return {
            'focus': concept,
            'emotion': emotion,
            'frustration_level': frustration,
            'engagement_score': 0.6 if emotion != 'frustrated' else 0.4,
            'personality': {
                'learning_preference': learning_preference,
                'neuroticism': 0.5,
                'openness': 0.6,
                'conscientiousness': 0.7
            },
            'mastery': mastery,
            'bkt_update': bkt_update,
            'code_analysis': code_analysis,
            'intervention': 'guided_practice',
            'kg_knowledge': {
                'name': concept,
                'common_misconceptions': ['Common misconception about this concept'],
                'better_mental_model': 'Better way to think about this',
                'progression': {
                    'emerging': 'Basic concept',
                    'developing': 'Building understanding',
                    'mastered': 'Advanced application'
                }
            }
        }
    
    def _analyze_code(self, code: str) -> Dict:
        """Quick code analysis"""
        errors = []
        
        # Check for common errors
        if 'max_num = 0' in code or 'max = 0' in code:
            errors.append({
                'type': 'initialization_error',
                'line': 2,
                'severity': 'high',
                'issue': 'Initializing max to 0 fails for negative numbers',
                'fix': 'Use numbers[0] or float("-inf")',
                'present': True
            })
        
        if 'node.next' in code.lower() and 'if' not in code.lower():
            errors.append({
                'type': 'null_pointer',
                'line': 3,
                'severity': 'high',
                'issue': 'Accessing .next without checking if node is None',
                'fix': 'Add: if node is not None before accessing node.next',
                'present': True
            })
        
        return {
            'has_code': True,
            'errors': errors,
            'shows_understanding': len(code) > 50 and '#' in code
        }
    
    def _generate_simple_response(
        self, message: str, code: Optional[str], state: Dict, analysis: Dict
    ) -> str:
        """Fallback simple response generation"""
        
        bkt = analysis.get('bkt_update', {})
        emotion = analysis.get('emotion', 'neutral')
        mastery = state.get('knowledge_state', {}).get('overall_mastery', 0.3)
        
        prompt = f"""You are an AI programming tutor (Interaction #{state.get('interaction_count', 0) + 1}).

STUDENT'S QUESTION:
{message}

{"STUDENT'S CODE:" if code else ""}
{"```python" if code else ""}
{code if code else ""}
{"```" if code else ""}

STUDENT STATE:
- Current mastery: {mastery:.0%}
- Emotion: {emotion}
- Learning preference: {analysis.get('personality', {}).get('learning_preference', 'visual')}

{"CODE ERROR DETECTED:" if analysis.get('code_analysis', {}).get('errors') else ""}
{self._format_errors(analysis.get('code_analysis', {}).get('errors', [])) if analysis.get('code_analysis', {}).get('errors') else ""}

Generate a helpful, personalized response that:
1. Addresses their question clearly
2. Uses appropriate tone for {emotion} emotion
3. {"Addresses the code error first" if analysis.get('code_analysis', {}).get('errors') else "Explains the concept"}
4. Acknowledges their progress (mastery: {mastery:.0%})
5. Provides examples and explanations

Keep it encouraging and personalized!"""
        
        try:
            response = self.groq.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}. Please try again."
    
    def _format_errors(self, errors: List[Dict]) -> str:
        """Format errors for prompt"""
        if not errors:
            return ""
        
        error_text = "\n".join([
            f"- Type: {e.get('type')}, Issue: {e.get('issue')}, Fix: {e.get('fix')}"
            for e in errors[:3]
        ])
        return error_text
    
    def get_student_info(self) -> str:
        """Get formatted student information"""
        if not self.student_state_manager:
            return f"Student ID: {self.current_student_id}\nStatus: Basic mode (BKT not available)"
        
        state = self.student_state_manager.get_student_state(self.current_student_id)
        interaction_count = state.get('interaction_count', 0)
        knowledge_state = state.get('knowledge_state', {})
        mastery = knowledge_state.get('overall_mastery', 0.0)
        
        info = f"""
Student ID: {self.current_student_id}
Total Interactions: {interaction_count}
Overall Mastery: {mastery:.1%}
"""
        
        if knowledge_state.get('skills'):
            info += "\nSkills:\n"
            for skill, data in knowledge_state['skills'].items():
                info += f"- {skill}: {data['mastery']:.0%} ({data['status']})\n"
        
        return info


def main():
    """Main function for command-line interface"""
    import os
    
    # Get API key - check multiple sources
    groq_api_key = os.getenv('GROQ_API_KEY')
    
    # If not in environment, try to load from .env file
    if not groq_api_key:
        try:
            from dotenv import load_dotenv
            load_dotenv()
            groq_api_key = os.getenv('GROQ_API_KEY')
        except ImportError:
            pass
    
    # If still not found, use the API key from other project files
    if not groq_api_key:
        print("[ERROR] GROQ_API_KEY environment variable not set!")
        print("[INFO] Please set it using: set GROQ_API_KEY=your_api_key")
        return
    
    # Verify the key works
    if not groq_api_key or len(groq_api_key) < 10:
        print("❌ Invalid API key. Please check your configuration.")
        return
    
    print("\n" + "="*80)
    print("🚀 Personalized Learning Chat Interface (Simple Mode)")
    print("="*80)
    print("\nInitializing system...")
    
    try:
        # Create chat interface
        chat = ChatInterface(groq_api_key)
        
        print("✅ System initialized!")
        print("\n" + "="*80)
        print("💬 Chat Interface Ready")
        print("="*80)
        print("\nCommands:")
        print("  - Type your question and press Enter")
        print("  - Type 'code:' followed by your code (multi-line, end with 'END')")
        print("  - Type 'info' to see your progress")
        print("  - Type 'student <name>' to change student ID")
        print("  - Type 'quit' or 'exit' to exit")
        print("\n" + "="*80 + "\n")
        
        # Interactive loop
        current_code = None
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Goodbye! Your progress has been saved.")
                    break
                
                if user_input.lower() == 'info':
                    print("\n" + chat.get_student_info() + "\n")
                    continue
                
                if user_input.lower().startswith('student '):
                    new_id = user_input[8:].strip()
                    if new_id:
                        chat.current_student_id = new_id
                        chat.initialize_student(new_id)
                        print(f"✅ Switched to student: {new_id}\n")
                    continue
                
                if user_input.lower().startswith('code:'):
                    print("Enter your code (type 'END' on a new line when finished):")
                    code_lines = []
                    while True:
                        line = input()
                        if line.strip().upper() == 'END':
                            break
                        code_lines.append(line)
                    current_code = '\n'.join(code_lines)
                    print(f"\n✅ Code received ({len(current_code)} characters)")
                    print("Now ask your question about the code:\n")
                    continue
                
                # Process message
                print("\n🤖 Thinking...\n")
                result = chat.process_message(user_input, current_code)
                
                print("="*80)
                print("RESPONSE:")
                print("="*80)
                print(result['response'])
                print("="*80 + "\n")
                
                # Clear code after use
                current_code = None
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Your progress has been saved.")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()
                print()
        
    except Exception as e:
        print(f"\n❌ Error creating interface: {e}")
        print("\n💡 Common issues:")
        print("   1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("   2. Verify your Groq API key is correct")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()














