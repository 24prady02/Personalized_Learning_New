"""
ChatGPT-like UI Interface for Personalized Learning System
Interactive chat interface with code input support

NOTE: UI integration removed - use chat_interface_simple.py for command-line version
This file is kept for future UI integration.
"""

import sys
import io
import os
from datetime import datetime
from typing import List, Tuple, Optional, Dict
import gradio as gr

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
    ChatGPT-like interface for personalized learning
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
        
        # Conversation history for Gradio
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
        code: Optional[str],
        history: List[Tuple[str, str]]
    ) -> Tuple[List[Tuple[str, str]], str, str]:
        """
        Process student message and generate personalized response
        
        Args:
            message: Student's question/message
            code: Optional code input
            history: Conversation history (Gradio format)
            
        Returns:
            Updated history, empty message, updated code
        """
        
        if not message.strip():
            return history, "", code or ""
        
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
        history.append((message, response))
        
        return history, "", code or ""
    
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
            return f"**Student ID:** {self.current_student_id}\n**Status:** Basic mode (BKT not available)"
        
        state = self.student_state_manager.get_student_state(self.current_student_id)
        interaction_count = state.get('interaction_count', 0)
        knowledge_state = state.get('knowledge_state', {})
        mastery = knowledge_state.get('overall_mastery', 0.0)
        
        info = f"""
**Student ID:** {self.current_student_id}
**Total Interactions:** {interaction_count}
**Overall Mastery:** {mastery:.1%}
"""
        
        if knowledge_state.get('skills'):
            info += "\n**Skills:**\n"
            for skill, data in knowledge_state['skills'].items():
                info += f"- {skill}: {data['mastery']:.0%} ({data['status']})\n"
        
        return info
    
    def clear_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
        return [], ""


def create_interface(groq_api_key: str):
    """Create Gradio interface"""
    
    try:
        chat_interface = ChatInterface(groq_api_key)
    except Exception as e:
        print(f"❌ Error initializing ChatInterface: {e}")
        print("💡 Make sure all dependencies are installed and Groq API key is valid")
        raise
    
    # Custom CSS for better styling
    css = """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .chat-message {
        padding: 10px;
        margin: 5px 0;
        border-radius: 10px;
    }
    .user-message {
        background-color: #e3f2fd;
    }
    .bot-message {
        background-color: #f5f5f5;
    }
    """
    
    with gr.Blocks(css=css, title="Personalized Learning Chat") as demo:
        gr.Markdown("""
        # 🎓 Personalized Learning System
        ### AI-Powered Programming Tutor with 10 Personalization Features
        
        Ask questions, share code, and get personalized explanations tailored to your learning style!
        """)
        
        with gr.Row():
            with gr.Column(scale=3):
                # Chat interface
                chatbot = gr.Chatbot(
                    label="Chat",
                    height=500,
                    show_label=True,
                    avatar_images=(None, "🤖")  # User, Bot
                )
                
                with gr.Row():
                    msg = gr.Textbox(
                        label="Your Question",
                        placeholder="Type your question here... (e.g., 'Why does my code fail?')",
                        lines=2,
                        scale=4
                    )
                    submit_btn = gr.Button("Send", variant="primary", scale=1)
                
                with gr.Row():
                    code_input = gr.Textbox(
                        label="Your Code (Optional)",
                        placeholder="Paste your code here if you have any...",
                        lines=5,
                        language="python"
                    )
                
                with gr.Row():
                    clear_btn = gr.Button("Clear Conversation", variant="secondary")
            
            with gr.Column(scale=1):
                # Student info panel
                gr.Markdown("### 📊 Your Progress")
                student_info = gr.Markdown(chat_interface.get_student_info())
                
                # Student ID input
                student_id_input = gr.Textbox(
                    label="Student ID",
                    value="Student",
                    placeholder="Enter your name/ID"
                )
                update_student_btn = gr.Button("Update Student", variant="secondary")
                
                # Refresh info
                refresh_btn = gr.Button("Refresh Progress", variant="secondary")
        
        # Event handlers
        def respond(message, code, history, student_id):
            """Handle message submission"""
            if not message.strip():
                return history, "", code, student_info.value
            
            # Update student if changed
            if student_id and student_id != chat_interface.current_student_id:
                chat_interface.current_student_id = student_id
                chat_interface.initialize_student(student_id)
            
            # Process message
            history, empty_msg, code_out = chat_interface.process_message(
                message, code, history
            )
            
            # Update student info
            info = chat_interface.get_student_info()
            
            return history, empty_msg, code_out, info
        
        def update_student(student_id):
            """Update student ID"""
            if student_id:
                chat_interface.current_student_id = student_id
                chat_interface.initialize_student(student_id)
                return chat_interface.get_student_info()
            return student_info.value
        
        def refresh_info():
            """Refresh student info"""
            return chat_interface.get_student_info()
        
        def clear_chat():
            """Clear chat"""
            history, _ = chat_interface.clear_conversation()
            return history, "", ""
        
        # Bind events
        submit_btn.click(
            respond,
            inputs=[msg, code_input, chatbot, student_id_input],
            outputs=[chatbot, msg, code_input, student_info]
        )
        
        msg.submit(
            respond,
            inputs=[msg, code_input, chatbot, student_id_input],
            outputs=[chatbot, msg, code_input, student_info]
        )
        
        update_student_btn.click(
            update_student,
            inputs=[student_id_input],
            outputs=[student_info]
        )
        
        refresh_btn.click(
            refresh_info,
            outputs=[student_info]
        )
        
        clear_btn.click(
            clear_chat,
            outputs=[chatbot, msg, code_input]
        )
        
        gr.Markdown("""
        ---
        ### 💡 Tips:
        - Ask questions about programming concepts
        - Share your code to get error-specific feedback
        - The system learns your learning style and adapts
        - Your progress is tracked across sessions
        """)
    
    return demo


def main():
    """Main function - UI integration removed"""
    print("\n" + "="*80)
    print("⚠️  UI Integration Removed")
    print("="*80)
    print("\nThe Gradio UI integration has been removed.")
    print("Please use chat_interface_simple.py for the command-line interface.")
    print("\nTo use the simple interface, run:")
    print("  python chat_interface_simple.py")
    print("\n" + "="*80)


if __name__ == "__main__":
    main()

