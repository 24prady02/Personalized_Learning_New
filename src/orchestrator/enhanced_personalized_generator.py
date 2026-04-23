"""
Enhanced Personalized Content Generator
Implements 10 key personalization features for student responses:
1. Conversation Memory & Context
2. Emotional Intelligence & Tone Adaptation
3. Learning Style Deep Personalization
4. Personality-Based Communication
5. Progress-Aware Responses
6. Interest & Context Personalization
7. Response Format Preferences
8. Error-Specific & Diagnostic Feedback
9. Metacognitive & Learning Strategy Support
10. Adaptive Difficulty & Pacing
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json


class EnhancedPersonalizedGenerator:
    """
    Generates highly personalized student responses using 10 personalization dimensions
    """
    
    def __init__(self, client=None):
        # Ollama: client param kept for API compatibility but unused —
        # all calls go to local Ollama HTTP endpoint.
        self.conversation_history = {}  # Track conversation context per student
        # Optional token-streaming callback; if set, fires once per chunk.
        # Set via generator._stream_callback = fn  (fn takes one str arg).
        self._stream_callback = None
        self._ollama_url = "http://localhost:11434/api/generate"
        # Auto-detect an available model on the local Ollama server.
        # Falls back to llama3.2 which is the most common lightweight default.
        self._ollama_model = self._detect_ollama_model() or "llama3.2"

    def _detect_ollama_model(self):
        """Query the Ollama /api/tags endpoint and pick the best installed model.

        Preference order (best for programming-pedagogy task first):
          1. qwen2.5-coder / codellama / deepseek-coder — code-specialized
          2. llama3.1:8b or larger llama3 variants
          3. any llama3.x (e.g. 3b)
          4. any installed model
        Returns tag like "qwen2.5-coder:7b" (keeps the tag so we pick the
        exact installed variant, not just the family name).
        """
        try:
            import requests as _req
            r = _req.get("http://localhost:11434/api/tags", timeout=2)
            names = [m.get("name") for m in r.json().get("models", [])
                     if m.get("name")]
            if not names:
                return None
            preferences = [
                lambda n: "qwen" in n.lower() and "coder" in n.lower(),
                lambda n: "deepseek" in n.lower() and "coder" in n.lower(),
                lambda n: "codellama" in n.lower(),
                lambda n: "llama3.1" in n.lower() or "llama3.3" in n.lower(),
                lambda n: "llama3" in n.lower(),
                lambda n: True,
            ]
            for pred in preferences:
                for n in names:
                    if pred(n):
                        return n  # return full tag, not family stub
            return names[0]
        except Exception:
            return None

    def generate_personalized_response(
        self,
        student_id: str,
        student_message: str,
        student_state: Dict,
        analysis: Dict,
        code: Optional[str] = None,
        code_analysis: Optional[Dict] = None,
        adaptive_analysis: Optional[Dict] = None
    ) -> str:
        """
        Generate fully personalized response using all 10 features
        
        Args:
            student_id: Unique student identifier
            student_message: Current student question/message
            student_state: Complete student state (BKT, personality, history)
            analysis: System analysis (emotion, knowledge gaps, etc.)
            code: Optional student code
            code_analysis: Optional code analysis results
            
        Returns:
            Personalized response string
        """
        
        # Feature 1: Conversation Memory & Context
        conversation_context = self._build_conversation_context(
            student_id, student_state, analysis
        )
        
        # Feature 2: Emotional Intelligence & Tone Adaptation
        emotional_context = self._adapt_emotional_tone(
            analysis, student_state
        )
        
        # Feature 3: Learning Style Deep Personalization
        learning_style_adaptation = self._adapt_to_learning_style(
            student_state, analysis
        )
        
        # Feature 4: Personality-Based Communication
        personality_adaptation = self._adapt_to_personality(
            student_state
        )
        
        # Feature 5: Progress-Aware Responses
        progress_context = self._build_progress_context(
            student_state, analysis
        )
        
        # Feature 6: Interest & Context Personalization
        interest_context = self._build_interest_context(
            student_state
        )
        
        # Feature 7: Response Format Preferences
        format_preferences = self._get_format_preferences(
            student_state
        )
        
        # Feature 8: Error-Specific & Diagnostic Feedback
        error_feedback = self._build_error_feedback(
            code, code_analysis, analysis
        )
        
        # Feature 9: Metacognitive & Learning Strategy Support
        metacognitive_guidance = self._generate_metacognitive_guidance(
            student_state, analysis
        )
        
        # Feature 10: Adaptive Difficulty & Pacing
        difficulty_adaptation = self._adapt_difficulty_and_pacing(
            student_state, analysis
        )
        
        # Build comprehensive prompt (include adaptive_analysis for knowledge graphs)
        prompt = self._build_enhanced_prompt(
            student_message=student_message,
            code=code,
            student_state=student_state,
            analysis=analysis,
            conversation_context=conversation_context,
            emotional_context=emotional_context,
            learning_style_adaptation=learning_style_adaptation,
            personality_adaptation=personality_adaptation,
            progress_context=progress_context,
            interest_context=interest_context,
            format_preferences=format_preferences,
            error_feedback=error_feedback,
            metacognitive_guidance=metacognitive_guidance,
            difficulty_adaptation=difficulty_adaptation,
            adaptive_analysis=adaptive_analysis
        )
        
        # Ollama local inference — streaming so first tokens appear in ~8-10s
        # instead of buffering the full 40s response. Same quality either way.
        import json as _json
        import time as _time
        import requests as _req
        try:
            resp = _req.post(
                self._ollama_url,
                json={"model": self._ollama_model, "prompt": prompt, "stream": True},
                timeout=300,
                stream=True,
            )
            resp.raise_for_status()
            chunks = []
            first_token_time = None
            t_start = _time.time()
            for line in resp.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    obj = _json.loads(line)
                except _json.JSONDecodeError:
                    continue
                piece = obj.get("response", "")
                if piece:
                    if first_token_time is None:
                        first_token_time = _time.time() - t_start
                    chunks.append(piece)
                    if self._stream_callback is not None:
                        try:
                            self._stream_callback(piece)
                        except Exception:
                            pass
                if obj.get("done"):
                    break
            output = "".join(chunks).strip()
            if first_token_time is not None:
                total = _time.time() - t_start
                print(f"[Ollama] TTFT={first_token_time:.1f}s  total={total:.1f}s  "
                      f"chunks={len(chunks)}  model={self._ollama_model}")
            if not output:
                raise ValueError("Empty response from Ollama")
        except Exception as _e:
            print(f"[WARN] Ollama call failed: {_e}")
            output = (
                "I am sorry, the local model is not responding right now. "
                "Please make sure Ollama is running: ollama serve"
            )
        
        # Store conversation context
        self._update_conversation_history(student_id, student_message, output)
        
        return output
    
    # ========== FEATURE 1: Conversation Memory & Context ==========
    
    def _build_conversation_context(
        self, student_id: str, student_state: Dict, analysis: Dict
    ) -> Dict:
        """Build context from previous conversations"""
        
        interaction_count = student_state.get('interaction_count', 0)
        history = self.conversation_history.get(student_id, [])
        
        context = {
            'interaction_number': interaction_count,
            'previous_topics': [],
            'what_worked_before': [],
            'confusion_patterns': [],
            'learning_trajectory': []
        }
        
        if interaction_count > 1:
            # Get recent conversation history
            recent_history = history[-3:] if len(history) > 3 else history
            
            # Extract previous topics
            context['previous_topics'] = [
                h.get('topic', 'unknown') for h in recent_history
            ]
            
            # Identify what worked before
            for h in recent_history:
                if h.get('student_feedback', {}).get('helpful', False):
                    context['what_worked_before'].append(
                        h.get('intervention_type', 'unknown')
                    )
            
            # Track confusion patterns
            confusion_count = sum(
                1 for h in history 
                if h.get('emotion') in ['confused', 'frustrated']
            )
            if confusion_count > 2:
                context['confusion_patterns'] = [
                    "Student has asked about this concept multiple times",
                    "May need alternative explanation approach"
                ]
        
        # Learning trajectory
        if interaction_count >= 3:
            mastery_history = student_state.get('knowledge_state', {}).get(
                'mastery_history', []
            )
            if len(mastery_history) >= 2:
                trend = "improving" if mastery_history[-1] > mastery_history[-2] else "stable"
                context['learning_trajectory'] = f"Mastery is {trend}"
        
        return context
    
    # ========== FEATURE 2: Emotional Intelligence & Tone Adaptation ==========
    
    def _adapt_emotional_tone(self, analysis: Dict, student_state: Dict) -> Dict:
        """Adapt tone based on emotional state"""
        
        emotion = analysis.get('emotion', 'neutral')
        frustration = analysis.get('frustration_level', 0.5)
        engagement = analysis.get('engagement_score', 0.5)
        mastery = student_state.get('knowledge_state', {}).get('overall_mastery', 0.5)
        
        tone_guidance = {
            'tone': 'neutral',
            'encouragement_level': 'moderate',
            'step_size': 'normal',
            'reassurance_needed': False,
            'celebration_needed': False
        }
        
        # High frustration → Softer, more supportive
        if frustration > 0.7:
            tone_guidance.update({
                'tone': 'gentle_supportive',
                'encouragement_level': 'high',
                'step_size': 'small',
                'reassurance_needed': True,
                'message': "Student is frustrated. Use gentle, encouraging tone. Break into smaller steps. Normalize the struggle."
            })
        
        # Low engagement → More engaging, enthusiastic
        elif engagement < 0.4:
            tone_guidance.update({
                'tone': 'enthusiastic_engaging',
                'encouragement_level': 'high',
                'message': "Student engagement is low. Be more enthusiastic. Use interesting examples. Make it exciting!"
            })
        
        # High mastery + improving → Celebrate!
        elif mastery > 0.7 and analysis.get('mastery_change', 0) > 0.1:
            tone_guidance.update({
                'tone': 'celebratory',
                'celebration_needed': True,
                'message': "Student is doing great! Celebrate their progress. Acknowledge improvement."
            })
        
        # Confused but trying → Supportive with clarity
        elif emotion == 'confused' and engagement > 0.5:
            tone_guidance.update({
                'tone': 'supportive_clarifying',
                'step_size': 'small',
                'message': "Student is confused but engaged. Be supportive. Provide clear, step-by-step explanation."
            })
        
        return tone_guidance
    
    # ========== FEATURE 3: Learning Style Deep Personalization ==========
    
    def _adapt_to_learning_style(self, student_state: Dict, analysis: Dict) -> Dict:
        """Deep personalization based on learning style"""
        
        learning_style = student_state.get('personality', {}).get(
            'learning_style', 'visual'
        )
        learning_preference = student_state.get('personality', {}).get(
            'learning_preference', 'visual'
        )
        
        adaptation = {
            'style': learning_style,
            'content_format': [],
            'explanation_approach': '',
            'examples_type': '',
            'visual_elements': False
        }
        
        # Visual learners
        if learning_preference in ['visual', 'visual_sequential']:
            adaptation.update({
                'content_format': ['diagrams', 'visual_metaphors', 'step_by_step_visual'],
                'explanation_approach': 'Use visual analogies and diagrams. "Imagine it like..."',
                'examples_type': 'visual_metaphors',
                'visual_elements': True,
                'instructions': "Include ASCII diagrams, flowcharts, or visual representations. Use visual metaphors."
            })
        
        # Conceptual learners
        elif learning_preference == 'conceptual':
            adaptation.update({
                'content_format': ['why_explanations', 'connections', 'mental_models'],
                'explanation_approach': 'Explain WHY, not just HOW. Connect to other concepts.',
                'examples_type': 'conceptual_connections',
                'instructions': "Focus on 'why' questions. Explain underlying principles. Connect to related concepts."
            })
        
        # Practical/Active learners
        elif learning_preference in ['practical', 'active']:
            adaptation.update({
                'content_format': ['hands_on_examples', 'interactive_exercises', 'try_it_now'],
                'explanation_approach': 'Provide hands-on examples. "Try this now..."',
                'examples_type': 'practical_applications',
                'instructions': "Include hands-on examples. Provide 'try it now' prompts. Show real-world applications."
            })
        
        # Sequential learners
        elif 'sequential' in str(learning_style):
            adaptation.update({
                'content_format': ['numbered_steps', 'linear_progression', 'clear_sequence'],
                'explanation_approach': 'Use numbered steps. "First... then... finally..."',
                'instructions': "Use numbered steps. Clear linear progression. 'First, then, finally' structure."
            })
        
        return adaptation
    
    # ========== FEATURE 4: Personality-Based Communication ==========
    
    def _adapt_to_personality(self, student_state: Dict) -> Dict:
        """
        Adapt communication style to personality traits
        Uses personality profile to customize response
        """
        
        personality = student_state.get('personality', {})
        neuroticism = personality.get('neuroticism', 0.5)
        openness = personality.get('openness', 0.5)
        conscientiousness = personality.get('conscientiousness', 0.5)
        extraversion = personality.get('extraversion', 0.5)
        agreeableness = personality.get('agreeableness', 0.5)
        
        adaptation = {
            'communication_style': 'balanced',
            'reassurance_level': 'moderate',
            'structure_level': 'moderate',
            'engagement_style': 'moderate',
            'tone': 'professional',
            'detail_level': 'moderate',
            'encouragement_style': 'moderate'
        }
        
        # High neuroticism → Extra reassurance, gentle tone
        if neuroticism > 0.6:
            adaptation.update({
                'reassurance_level': 'high',
                'communication_style': 'supportive_reassuring',
                'tone': 'gentle',
                'encouragement_style': 'frequent',
                'instructions': "Provide extra reassurance. Normalize struggles. Break into smaller steps. Frequent check-ins. Use phrases like 'That's okay', 'Many students find this challenging', 'You're making progress'."
            })
        
        # High openness → Explore connections, creative examples
        if openness > 0.7:
            adaptation.update({
                'communication_style': 'exploratory',
                'detail_level': 'high',
                'instructions': "Explore connections to other concepts. Mention advanced topics. Use creative examples. Ask 'what if' questions. Encourage experimentation."
            })
        
        # Low openness → Stick to basics, concrete examples
        elif openness < 0.4:
            adaptation.update({
                'communication_style': 'concrete_practical',
                'detail_level': 'low',
                'instructions': "Stick to concrete, practical examples. Avoid abstract concepts. Use real-world applications. Keep it simple and straightforward."
            })
        
        # High conscientiousness → Structured format, detailed
        if conscientiousness > 0.7:
            adaptation.update({
                'structure_level': 'high',
                'communication_style': 'structured_organized',
                'detail_level': 'high',
                'instructions': "Use structured format. Clear organization. Detailed notes. Numbered sections. Step-by-step breakdown. Provide checklists."
            })
        
        # Low conscientiousness → Flexible, less structure
        elif conscientiousness < 0.4:
            adaptation.update({
                'structure_level': 'low',
                'communication_style': 'flexible',
                'instructions': "Use flexible format. Less rigid structure. Allow exploration. Don't overwhelm with too many steps."
            })
        
        # High extraversion → Engaging, conversational, enthusiastic
        if extraversion > 0.6:
            adaptation.update({
                'engagement_style': 'high',
                'communication_style': 'conversational_engaging',
                'tone': 'enthusiastic',
                'instructions': "Use conversational tone. Engaging questions. Interactive elements. More enthusiasm. Use exclamation marks. Ask 'What do you think?' 'Want to try this?'"
            })
        
        # Low extraversion → Respectful, less chatty, more direct
        elif extraversion < 0.4:
            adaptation.update({
                'engagement_style': 'low',
                'communication_style': 'direct_respectful',
                'tone': 'professional',
                'instructions': "Be direct and respectful. Less chatty. Focus on information. Avoid excessive enthusiasm. Give space for independent work."
            })
        
        # High agreeableness → Collaborative language, supportive
        if agreeableness > 0.7:
            adaptation.update({
                'communication_style': 'collaborative',
                'tone': 'friendly',
                'instructions': "Use collaborative language. 'Let's work together...' 'We can...' 'How about we...' Be supportive and encouraging."
            })
        
        # Low agreeableness → More direct, less collaborative
        elif agreeableness < 0.4:
            adaptation.update({
                'communication_style': 'direct',
                'instructions': "Be direct and factual. Less collaborative language. Focus on the solution. Avoid being overly friendly."
            })
        
        return adaptation
    
    # ========== FEATURE 5: Progress-Aware Responses ==========
    
    def _build_progress_context(self, student_state: Dict, analysis: Dict) -> Dict:
        """Build context about student progress"""
        
        knowledge_state = student_state.get('knowledge_state', {})
        current_mastery = knowledge_state.get('overall_mastery', 0.0)
        interaction_count = student_state.get('interaction_count', 0)
        
        # Get mastery change
        mastery_history = knowledge_state.get('mastery_history', [])
        mastery_change = 0.0
        if len(mastery_history) >= 2:
            mastery_change = mastery_history[-1] - mastery_history[-2]
        
        # Get BKT update if available
        bkt_update = analysis.get('bkt_update', {})
        skill_mastery_before = bkt_update.get('p_learned_before', current_mastery)
        skill_mastery_after = bkt_update.get('p_learned_after', current_mastery)
        skill_change = skill_mastery_after - skill_mastery_before
        
        progress_context = {
            'current_mastery': current_mastery,
            'mastery_change': mastery_change,
            'skill_mastery_before': skill_mastery_before,
            'skill_mastery_after': skill_mastery_after,
            'skill_change': skill_change,
            'interaction_count': interaction_count,
            'acknowledgment_needed': False,
            'challenge_level': 'appropriate'
        }
        
        # Significant improvement → Acknowledge!
        if skill_change > 0.15:
            progress_context.update({
                'acknowledgment_needed': True,
                'acknowledgment': f"Great progress! Your mastery improved from {skill_mastery_before:.0%} to {skill_mastery_after:.0%}!"
            })
        
        # Determine challenge level
        if current_mastery < 0.3:
            progress_context['challenge_level'] = 'foundational'
        elif current_mastery < 0.6:
            progress_context['challenge_level'] = 'building'
        elif current_mastery < 0.8:
            progress_context['challenge_level'] = 'reinforcing'
        else:
            progress_context['challenge_level'] = 'mastery'
        
        return progress_context
    
    # ========== FEATURE 6: Interest & Context Personalization ==========
    
    def _build_interest_context(self, student_state: Dict) -> Dict:
        """Build context from student interests"""
        
        # Get interests from student profile (if available)
        interests = student_state.get('interests', [])
        hobbies = student_state.get('hobbies', [])
        career_goals = student_state.get('career_goals', [])
        age_group = student_state.get('age_group', 'college')
        
        # Default interests if not specified
        if not interests:
            interests = ['programming', 'technology']
        
        interest_context = {
            'interests': interests,
            'hobbies': hobbies,
            'career_goals': career_goals,
            'age_group': age_group,
            'example_domains': []
        }
        
        # Map interests to example domains
        interest_mapping = {
            'gaming': 'game development, game mechanics, player interactions',
            'sports': 'sports statistics, team management, performance tracking',
            'music': 'audio processing, music theory, sound synthesis',
            'art': 'graphics programming, visual design, creative coding',
            'science': 'scientific computing, data analysis, simulations',
            'business': 'business applications, data management, automation'
        }
        
        for interest in interests:
            if interest.lower() in interest_mapping:
                interest_context['example_domains'].append(
                    interest_mapping[interest.lower()]
                )
        
        return interest_context
    
    # ========== FEATURE 7: Response Format Preferences ==========
    
    def _get_format_preferences(self, student_state: Dict) -> Dict:
        """Get student's preferred response format"""
        
        # Infer from interaction history
        history = self.conversation_history.get(
            student_state.get('student_id', 'default'), []
        )
        
        preferences = {
            'length': 'moderate',  # concise, moderate, detailed
            'code_style': 'commented',  # minimal, commented, verbose
            'visual_density': 'moderate',  # low, moderate, high
            'structure': 'structured'  # narrative, structured, step_by_step
        }
        
        # Analyze what worked before
        if history:
            # Check engagement with different formats
            detailed_responses = [h for h in history if h.get('response_length', 0) > 1000]
            if detailed_responses:
                avg_engagement = sum(
                    h.get('engagement', 0.5) for h in detailed_responses
                ) / len(detailed_responses)
                if avg_engagement > 0.7:
                    preferences['length'] = 'detailed'
            
            # Check visual preference
            visual_responses = [h for h in history if h.get('has_diagrams', False)]
            if visual_responses:
                preferences['visual_density'] = 'high'
        
        # Adjust based on personality
        personality = student_state.get('personality', {})
        if personality.get('conscientiousness', 0.5) > 0.7:
            preferences['structure'] = 'structured'
        if personality.get('openness', 0.5) > 0.7:
            preferences['length'] = 'detailed'
        
        return preferences
    
    # ========== FEATURE 8: Error-Specific & Diagnostic Feedback ==========
    
    def _build_error_feedback(
        self, code: Optional[str], code_analysis: Optional[Dict], analysis: Dict
    ) -> Dict:
        """Build specific error feedback"""
        
        if not code or not code_analysis:
            return {'has_errors': False}
        
        errors = code_analysis.get('errors', [])
        if not errors:
            return {'has_errors': False}
        
        # Get most critical error
        primary_error = errors[0]
        
        error_feedback = {
            'has_errors': True,
            'error_type': primary_error.get('type', 'unknown'),
            'error_location': primary_error.get('line', 'unknown'),
            'error_issue': primary_error.get('issue', ''),
            'error_fix': primary_error.get('fix', ''),
            'severity': primary_error.get('severity', 'medium'),
            'hint_level': 'moderate'  # subtle, moderate, explicit
        }
        
        # Determine hint level based on frustration
        frustration = analysis.get('frustration_level', 0.5)
        if frustration > 0.7:
            error_feedback['hint_level'] = 'explicit'  # More direct help
        elif frustration < 0.3:
            error_feedback['hint_level'] = 'subtle'  # Let them discover
        
        return error_feedback
    
    # ========== FEATURE 9: Metacognitive & Learning Strategy Support ==========
    
    def _generate_metacognitive_guidance(
        self, student_state: Dict, analysis: Dict
    ) -> Dict:
        """Generate learning strategy guidance"""
        
        interaction_count = student_state.get('interaction_count', 0)
        mastery = student_state.get('knowledge_state', {}).get('overall_mastery', 0.5)
        emotion = analysis.get('emotion', 'neutral')
        
        guidance = {
            'has_guidance': False,
            'strategy_type': '',
            'message': '',
            'tips': []
        }
        
        # Pattern: Making progress with follow-ups
        if interaction_count >= 2:
            mastery_history = student_state.get('knowledge_state', {}).get(
                'mastery_history', []
            )
            if len(mastery_history) >= 2 and mastery_history[-1] > mastery_history[-2]:
                guidance.update({
                    'has_guidance': True,
                    'strategy_type': 'incremental_questioning',
                    'message': "Your incremental questioning approach is working great! Keep asking follow-up questions.",
                    'tips': [
                        "Break complex topics into smaller questions",
                        "Ask 'why' and 'how' to deepen understanding"
                    ]
                })
        
        # Pattern: Struggling with concept
        if mastery < 0.4 and interaction_count > 1:
            guidance.update({
                'has_guidance': True,
                'strategy_type': 'systematic_tracing',
                'message': "Try this systematic approach:",
                'tips': [
                    "Draw it out on paper (visual representation)",
                    "Trace through with specific values",
                    "Check understanding at each step"
                ]
            })
        
        # Pattern: Frustrated
        if emotion == 'frustrated':
            guidance.update({
                'has_guidance': True,
                'strategy_type': 'self_regulation',
                'message': "When stuck, try:",
                'tips': [
                    "Take a short break, then return with fresh eyes",
                    "Explain the problem to someone (or yourself) out loud",
                    "Start with a simpler version of the problem"
                ]
            })
        
        return guidance
    
    # ========== FEATURE 10: Adaptive Difficulty & Pacing ==========
    
    def _adapt_difficulty_and_pacing(
        self, student_state: Dict, analysis: Dict
    ) -> Dict:
        """Adapt difficulty and pacing to student level"""
        
        mastery = student_state.get('knowledge_state', {}).get('overall_mastery', 0.5)
        emotion = analysis.get('emotion', 'neutral')
        engagement = analysis.get('engagement_score', 0.5)
        frustration = analysis.get('frustration_level', 0.5)
        
        adaptation = {
            'difficulty_level': 'appropriate',
            'pacing': 'moderate',
            'scaffolding_level': 3,  # 1-5 scale
            'challenge_type': 'just_right'
        }
        
        # Determine difficulty based on mastery
        if mastery < 0.3:
            adaptation.update({
                'difficulty_level': 'foundational',
                'scaffolding_level': 5,  # High support
                'challenge_type': 'building_foundation',
                'instructions': "Use foundational concepts. High scaffolding. Small steps."
            })
        elif mastery < 0.6:
            adaptation.update({
                'difficulty_level': 'building',
                'scaffolding_level': 3,
                'challenge_type': 'just_right',
                'instructions': "Build on existing knowledge. Moderate scaffolding."
            })
        elif mastery < 0.8:
            adaptation.update({
                'difficulty_level': 'reinforcing',
                'scaffolding_level': 2,
                'challenge_type': 'reinforcement',
                'instructions': "Reinforce understanding. Lower scaffolding. More independence."
            })
        else:
            adaptation.update({
                'difficulty_level': 'mastery',
                'scaffolding_level': 1,
                'challenge_type': 'extension',
                'instructions': "Extend to advanced concepts. Minimal scaffolding. Challenge them."
            })
        
        # Adjust pacing based on emotion and engagement
        if frustration > 0.7:
            adaptation['pacing'] = 'slower'
        elif engagement < 0.4:
            adaptation['pacing'] = 'faster'  # Speed up to maintain interest
        elif emotion == 'engaged' and mastery > 0.6:
            adaptation['pacing'] = 'faster'
        
        return adaptation
    
    # ========== PROMPT BUILDING ==========
    
    def _build_enhanced_prompt(
        self,
        student_message: str,
        code: Optional[str],
        student_state: Dict,
        analysis: Dict,
        conversation_context: Dict,
        emotional_context: Dict,
        learning_style_adaptation: Dict,
        personality_adaptation: Dict,
        progress_context: Dict,
        interest_context: Dict,
        format_preferences: Dict,
        error_feedback: Dict,
        metacognitive_guidance: Dict,
        difficulty_adaptation: Dict,
        adaptive_analysis: Optional[Dict] = None
    ) -> str:
        """Build comprehensive personalized prompt"""
        
        prompt_parts = []
        
        # Header
        prompt_parts.append(
            f"You are an AI tutor having conversation #{conversation_context['interaction_number']} "
            f"with a student learning programming."
        )

        # ===== LP ENFORCEMENT GATE =====
        # If the learning progression says the student is not yet ready for the
        # concept they asked about, we hard-redirect the lesson to the next
        # concept they CAN learn. This runs before everything else so the LLM
        # sees the override first; small models (e.g. llama3.2 3B) obey it more
        # reliably than a deeply-nested MUST clause inside the pedagogical-KG
        # section.
        lp_path = (analysis.get('pedagogical_kg') or {}).get('learning_path')
        lp_redirect = None
        if lp_path and not lp_path.get('on_track', True):
            target = lp_path.get('target_concept')
            nxt    = lp_path.get('next_concept')
            if target and nxt and target != nxt:
                # find the next-step entry to surface its mastery numbers
                next_step = next(
                    (s for s in lp_path.get('path', []) if s['concept'] == nxt),
                    None,
                )
                cur_m = next_step['current_mastery'] if next_step else 0.0
                req_m = next_step['required_mastery'] if next_step else 0.7
                prereqs = next_step['prerequisites'] if next_step else []
                lp_redirect = {
                    'target': target,
                    'next':   nxt,
                    'current_mastery':  cur_m,
                    'required_mastery': req_m,
                    'prerequisites':    prereqs,
                }
                prompt_parts.append(
                    "\n=== PROGRESSION ENFORCEMENT (HARD OVERRIDE) ===\n"
                    f"The student asked about '{target}', but the learning progression "
                    f"says they are NOT READY for it yet. They must first master '{nxt}' "
                    f"(current mastery {cur_m:.2f} / required {req_m:.2f}).\n"
                    "\n"
                    f"YOU MUST DO THE FOLLOWING — these rules override every other "
                    f"instruction in this prompt:\n"
                    f"  1. Do NOT teach '{target}' in this response.\n"
                    f"  2. Do NOT show any '{target}' code, syntax, or worked examples.\n"
                    f"  3. Acknowledge the student's question about '{target}' briefly — say "
                    f"     you can see why they are stuck, but explain that '{nxt}' is a "
                    f"     prerequisite they need to master first.\n"
                    f"  4. Then teach '{nxt}' — only '{nxt}' — with a short, concrete "
                    f"     explanation appropriate for a beginner (this student's mastery "
                    f"     on '{nxt}' is only {cur_m:.2f}).\n"
                    f"  5. End by saying you will return to '{target}' once '{nxt}' is solid.\n"
                    "\n"
                    f"Rationale shown to the student: '{nxt}' is on the path to '{target}' "
                    f"with prereqs {prereqs or '[none]'}. The full progression is in the "
                    f"[LP Progression] block below."
                )

        # Student's question
        prompt_parts.append(f"\nSTUDENT'S QUESTION:\n{student_message}")

        # Code if provided — suppress when we are redirecting off-topic so the
        # LLM doesn't get re-primed to discuss the target concept's code.
        if code and lp_redirect is None:
            prompt_parts.append(f"\nSTUDENT'S CODE:\n```python\n{code}\n```")
        elif code:
            prompt_parts.append(
                f"\n(The student's code for '{lp_redirect['target']}' is intentionally "
                f"OMITTED from this prompt per the ENFORCEMENT gate — do not reconstruct it.)"
            )
        
        # Feature 1: Conversation Memory
        if conversation_context['interaction_number'] > 1:
            prompt_parts.append("\n=== CONVERSATION CONTEXT ===")
            if conversation_context['previous_topics']:
                prompt_parts.append(
                    f"Previous topics discussed: {', '.join(conversation_context['previous_topics'][-2:])}"
                )
            if conversation_context['what_worked_before']:
                prompt_parts.append(
                    f"What worked before: {', '.join(set(conversation_context['what_worked_before']))}"
                )
            if conversation_context['confusion_patterns']:
                prompt_parts.append(
                    f"Note: {conversation_context['confusion_patterns'][0]}"
                )
        
        # Feature 2: Emotional Intelligence
        prompt_parts.append("\n=== EMOTIONAL CONTEXT ===")
        prompt_parts.append(f"Tone: {emotional_context['tone']}")
        prompt_parts.append(f"Encouragement level: {emotional_context['encouragement_level']}")
        if 'message' in emotional_context:
            prompt_parts.append(f"Guidance: {emotional_context['message']}")
        
        # Feature 3: Learning Style
        prompt_parts.append("\n=== LEARNING STYLE ADAPTATION ===")
        prompt_parts.append(f"Student is a {learning_style_adaptation['style']} learner")
        if 'instructions' in learning_style_adaptation:
            prompt_parts.append(f"Adaptation: {learning_style_adaptation['instructions']}")
        
        # Feature 4: Personality
        prompt_parts.append("\n=== PERSONALITY ADAPTATION ===")
        prompt_parts.append(f"Communication style: {personality_adaptation['communication_style']}")
        if 'instructions' in personality_adaptation:
            prompt_parts.append(f"Guidance: {personality_adaptation['instructions']}")
        
        # Feature 5: Progress
        prompt_parts.append("\n=== PROGRESS CONTEXT ===")
        prompt_parts.append(
            f"Current mastery: {progress_context['current_mastery']:.0%} "
            f"(Change: {progress_context['skill_change']:+.1%})"
        )
        if progress_context['acknowledgment_needed']:
            prompt_parts.append(f"MUST acknowledge: {progress_context['acknowledgment']}")
        prompt_parts.append(f"Challenge level: {progress_context['challenge_level']}")
        
        # Feature 6: Interests
        if interest_context['example_domains']:
            prompt_parts.append("\n=== INTEREST-BASED EXAMPLES ===")
            prompt_parts.append(
                f"Use examples from: {', '.join(interest_context['example_domains'])}"
            )
        
        # Feature 7: Format Preferences
        prompt_parts.append("\n=== RESPONSE FORMAT ===")
        prompt_parts.append(f"Length: {format_preferences['length']}")
        prompt_parts.append(f"Structure: {format_preferences['structure']}")
        prompt_parts.append(f"Visual density: {format_preferences['visual_density']}")
        
        # Feature 8: Error Feedback
        if error_feedback.get('has_errors'):
            prompt_parts.append("\n=== ERROR FEEDBACK (CRITICAL) ===")
            prompt_parts.append(f"Error type: {error_feedback['error_type']}")
            prompt_parts.append(f"Location: {error_feedback['error_location']}")
            prompt_parts.append(f"Issue: {error_feedback['error_issue']}")
            prompt_parts.append(f"Fix: {error_feedback['error_fix']}")
            prompt_parts.append(
                f"MUST: Point to this error first, explain WHY it occurs, show HOW to fix it"
            )
        
        # Feature 9: Metacognitive Guidance
        if metacognitive_guidance.get('has_guidance'):
            prompt_parts.append("\n=== LEARNING STRATEGY ===")
            prompt_parts.append(f"Strategy: {metacognitive_guidance['strategy_type']}")
            prompt_parts.append(f"Message: {metacognitive_guidance['message']}")
            if metacognitive_guidance.get('tips'):
                prompt_parts.append(f"Tips to include: {', '.join(metacognitive_guidance['tips'])}")
        
        # Feature 10: Difficulty & Pacing
        prompt_parts.append("\n=== DIFFICULTY & PACING ===")
        prompt_parts.append(f"Difficulty: {difficulty_adaptation['difficulty_level']}")
        prompt_parts.append(f"Pacing: {difficulty_adaptation['pacing']}")
        prompt_parts.append(f"Scaffolding: {difficulty_adaptation['scaffolding_level']}/5")
        if 'instructions' in difficulty_adaptation:
            prompt_parts.append(f"Guidance: {difficulty_adaptation['instructions']}")
        
        # ===== FIX 1+2: PSYCHOLOGICAL STATE from three-channel analysis ==========
        pg  = student_state.get('psychological_graph', {})
        prg = student_state.get('progression_graph', {})
        cc  = student_state.get('content_channel', {})
        lg  = student_state.get('language_channel', {})
        ri  = student_state.get('recommended_intervention', {})

        if pg or prg or cc:
            prompt_parts.append("\n=== PSYCHOLOGICAL STATE (from three-channel analysis) ===")
            if pg:
                prompt_parts.append(f"Attribution style: {pg.get('attribution', 'neutral')}")
                prompt_parts.append(f"Self-efficacy: {pg.get('self_efficacy', 'neutral')}")
                prompt_parts.append(f"SRL phase: {pg.get('srl_phase', 'unknown')}")
                prompt_parts.append(f"Imposter flag: {pg.get('imposter_flag', False)}")
                prompt_parts.append(f"High anxiety: {pg.get('high_anxiety', False)}")
                prompt_parts.append(f"Flow state: {pg.get('flow_state', False)}")
            if prg:
                prompt_parts.append(f"Developmental stage: {prg.get('stage', 1)} / 5 (ZPD: {prg.get('zpd_status', 'unknown')})")
                prompt_parts.append(f"Scaffold level needed: {prg.get('scaffold_level', 3)} / 5")
                prompt_parts.append(f"Student has made an attempt: {prg.get('has_attempt', False)}")
            if cc:
                prompt_parts.append(f"Encoding depth: {cc.get('encoding_strength', 'surface')}")
                prompt_parts.append(f"Dual coding: {cc.get('dual_coding', 'verbal_only')}")
                prompt_parts.append(f"Elaboration present: {cc.get('elaboration', False)}")

        # ===== FIX 2: INTERVENTION INSTRUCTION — translate type to Groq instructions
        intervention_map = {
            'attribution_reframe': (
                "CRITICAL — this student believes they are fundamentally bad at programming. "
                "Do NOT advance the concept yet. First: acknowledge that this specific error trips up "
                "almost every Java learner. Reframe the difficulty as a normal learning step, not a "
                "sign of inability. Use phrases like 'this confuses nearly everyone at first' and "
                "'the fact that you spotted it means you are making progress'. Only after reframing "
                "should you gently begin explaining the concept."
            ),
            'reduce_challenge':    (
                "Student is overwhelmed. Drastically simplify. Use the smallest possible code example "
                "(3-5 lines max). Do not introduce new terms. Focus on one single idea only. "
                "Be warm and reassuring throughout."
            ),
            'mastery_surface':     (
                "Student has solid understanding but low confidence. Your primary job is to surface "
                "evidence of their competence before teaching anything new. Start by pointing out what "
                "they already got right in their code or reasoning. Then build from there."
            ),
            'worked_example':      (
                "Student needs a complete worked example. Provide a short Java snippet (5-10 lines) "
                "that demonstrates exactly the concept they are struggling with. Walk through it line "
                "by line. Use dual coding — annotate the code AND explain in prose. Do not ask them "
                "to figure it out themselves yet."
            ),
            'socratic_prompt':     (
                "Do NOT explain the answer. Instead ask ONE targeted question that leads the student "
                "to discover the issue themselves. The question should point at the exact line or "
                "concept causing confusion without giving it away. Wait for their response."
            ),
            'transfer_task':       (
                "Student has deep understanding. Do not re-explain what they already know. "
                "Extend their learning with a novel real-world Java application of this concept. "
                "Frame it as a challenge: 'Now that you understand this, how would you apply it to...'"
            ),
            'validate_and_advance': (
                "Confirm mastery first — explicitly tell the student what they got right and why it "
                "shows real understanding. Then advance to the next concept in the progression. "
                "Be specific about what they demonstrated."
            ),
            'increase_challenge':  (
                "Student is ready for a harder problem. Acknowledge their success briefly, then "
                "present a more complex variant of the same concept. Increase complexity by adding "
                "one layer only — do not introduce multiple new ideas at once."
            ),
        }
        if ri:
            i_type = ri.get('type', '')
            instruction = intervention_map.get(i_type, '')
            if instruction:
                prompt_parts.append(f"\n=== INTERVENTION INSTRUCTION [{i_type.upper()}] ===")
                prompt_parts.append(instruction)
                if ri.get('rationale'):
                    prompt_parts.append(f"Why this was selected: {ri['rationale']}")

        # ===== KNOWLEDGE GRAPHS CONTEXT (CRITICAL - MUST USE THESE) =====
        prompt_parts.append("\n=== KNOWLEDGE GRAPHS (MUST REFERENCE IN RESPONSE) ===")
        
        # CSE-KG 2.0 (Computer Science Knowledge Graph)
        cse_kg_info = analysis.get('cse_kg', {})
        if cse_kg_info:
            prompt_parts.append("\n[CSE-KG 2.0 - Computer Science Domain Knowledge]")
            prompt_parts.append(f"  - Concept: {cse_kg_info.get('concept', 'N/A')}")
            prompt_parts.append(f"  - Prerequisites: {', '.join(cse_kg_info.get('prerequisites', []))}")
            prompt_parts.append(f"  - Related Concepts: {', '.join(cse_kg_info.get('related_concepts', []))}")
            prompt_parts.append(f"  - Definition: {cse_kg_info.get('definition', 'N/A')}")
            prompt_parts.append("  - MUST: Use CSE-KG information to explain concepts accurately and reference prerequisites")
        
        # Pedagogical KG (Learning Progressions, Misconceptions)
        pedagogical_kg_info = analysis.get('pedagogical_kg', {})
        if pedagogical_kg_info:
            prompt_parts.append("\n[Pedagogical Knowledge Graph - Learning Science]")
            prompt_parts.append(f"  - Learning Progression: {pedagogical_kg_info.get('progression', 'N/A')}")
            misconceptions = pedagogical_kg_info.get('misconceptions', [])
            if misconceptions:
                prompt_parts.append(f"  - Common Misconceptions: {', '.join(misconceptions[:3])}")
            prompt_parts.append(f"  - Cognitive Load Level: {pedagogical_kg_info.get('cognitive_load', 'N/A')}")
            prompt_parts.append(f"  - Recommended Interventions: {', '.join(pedagogical_kg_info.get('interventions', []))}")
            prompt_parts.append("  - MUST: Address misconceptions explicitly and follow learning progression")

            # Structured learning-progression path from data/pedagogical_kg/learning_progressions.json
            # Inserted by orchestrator / end-to-end pipeline via LPIndex.get_path().
            lp_path = pedagogical_kg_info.get('learning_path')
            if lp_path:
                prompt_parts.append("\n[LP Progression (from learning_progressions.json)]")
                try:
                    from src.knowledge_graph.lp_index import LPIndex
                    # Use a module-level singleton to avoid reloading JSON each call
                    if not hasattr(EnhancedPersonalizedGenerator, "_lp_index_singleton"):
                        EnhancedPersonalizedGenerator._lp_index_singleton = LPIndex()
                    prompt_parts.append(
                        EnhancedPersonalizedGenerator._lp_index_singleton
                        .render_prompt_block(lp_path)
                    )
                except Exception as _e:
                    # fall back to a minimal render if LPIndex can't be imported
                    prompt_parts.append(
                        f"Progression: {lp_path.get('progression_id', 'unknown')}\n"
                        f"Target: {lp_path.get('target_concept')}  "
                        f"next step: {lp_path.get('next_concept')}\n"
                        f"On track: {lp_path.get('on_track')}"
                    )
        
        # COKE (Cognitive Knowledge Graph - Theory of Mind)
        coke_info = analysis.get('coke', {})
        if coke_info:
            prompt_parts.append("\n[COKE - Cognitive Knowledge Graph for Theory of Mind]")
            prompt_parts.append(f"  - Cognitive State: {coke_info.get('cognitive_state', 'N/A')}")
            prompt_parts.append(f"  - Mental Activity: {coke_info.get('mental_activity', 'N/A')}")
            prompt_parts.append(f"  - Behavioral Response: {coke_info.get('behavioral_response', 'N/A')}")
            prompt_parts.append(f"  - Confidence: {coke_info.get('confidence', 0.5):.2f}")
            cognitive_chain = coke_info.get('cognitive_chain', {})
            if cognitive_chain:
                prompt_parts.append(f"  - Cognitive Chain: {cognitive_chain.get('description', 'N/A')}")
            prompt_parts.append("  - MUST: Use COKE cognitive state to understand student's mental state and adapt explanation accordingly")
        
        # Fix 9: Fallback uses Java KG defaults from setup_java_knowledge.py
        kg = analysis.get('kg_knowledge', {})
        if kg and not (cse_kg_info or pedagogical_kg_info or coke_info):
            prompt_parts.append("\n=== JAVA DOMAIN KNOWLEDGE ===")
            prompt_parts.append(f"Concept: {kg.get('name', 'N/A')}")
            prompt_parts.append(f"Java-specific misconceptions: {kg.get('common_misconceptions', 'N/A')}")
            prompt_parts.append(f"Better mental model for Java: {kg.get('better_mental_model', 'N/A')}")
            prompt_parts.append(f"Week in CSCI 1301: {kg.get('week', 'N/A')}")
            prompt_parts.append(f"Error type: {kg.get('error_type', 'N/A')}")
        
        # Emphasize knowledge graph usage
        prompt_parts.append("\n=== CRITICAL INSTRUCTION: KNOWLEDGE GRAPH INTEGRATION ===")
        prompt_parts.append("Your response MUST be grounded in and reference the knowledge graphs above:")
        prompt_parts.append("")
        prompt_parts.append("1. CSE-KG 2.0 (Computer Science Knowledge Graph):")
        prompt_parts.append("   - Use the concept definition and prerequisites from CSE-KG")
        prompt_parts.append("   - Reference related concepts when explaining connections")
        prompt_parts.append("   - Ensure technical accuracy based on CSE-KG domain knowledge")
        prompt_parts.append("")
        prompt_parts.append("2. Pedagogical Knowledge Graph (Learning Science):")
        prompt_parts.append("   - Explicitly address the common misconceptions listed above")
        prompt_parts.append("   - Follow the learning progression to structure your explanation")
        prompt_parts.append("   - Manage cognitive load according to the level indicated")
        prompt_parts.append("   - Consider the recommended interventions when choosing your approach")
        prompt_parts.append("")
        prompt_parts.append("3. COKE (Cognitive Knowledge Graph - Theory of Mind):")
        prompt_parts.append("   - Adapt your explanation tone and complexity based on the cognitive state")
        prompt_parts.append("   - If student is 'confused', use simpler language and more examples")
        prompt_parts.append("   - If student is 'frustrated', provide extra reassurance and break into smaller steps")
        prompt_parts.append("   - If student is 'understanding', you can use more advanced concepts")
        prompt_parts.append("   - Consider the behavioral response prediction when framing your explanation")
        prompt_parts.append("")
        prompt_parts.append("4. INTEGRATION REQUIREMENT:")
        prompt_parts.append("   - Your explanation must show evidence of using all three knowledge graphs")
        prompt_parts.append("   - Reference specific insights (e.g., 'Based on common misconceptions about recursion...')")
        prompt_parts.append("   - Use CSE-KG prerequisites to build understanding step-by-step")
        prompt_parts.append("   - Adapt to COKE cognitive state in your language and approach")
        
        # Final instructions
        prompt_parts.append("\n=== YOUR RESPONSE MUST ===")
        prompt_parts.append("1. Follow the INTERVENTION INSTRUCTION above exactly — it overrides general advice")
        prompt_parts.append("2. Address the student's specific Java question")
        prompt_parts.append("3. Use tone and style matching the PSYCHOLOGICAL STATE above")
        prompt_parts.append("4. Include Java-specific examples grounded in the knowledge graphs")
        prompt_parts.append("5. Acknowledge progress if there is evidence of improvement")
        prompt_parts.append("6. Match difficulty and scaffolding to the DEVELOPMENTAL STAGE above")
        prompt_parts.append("7. Be encouraging — adapt warmth to the emotional state detected")
        prompt_parts.append("8. CRITICAL: Ground explanation in the knowledge graphs provided")
        prompt_parts.append("   - Reference CSE-KG Java concepts and prerequisites explicitly")
        prompt_parts.append("   - Address Pedagogical KG Java misconceptions directly")
        prompt_parts.append("   - Adapt to COKE cognitive state")
        prompt_parts.append("   - Use knowledge graph information to build accurate mental models")
        prompt_parts.append("9. NEVER just output a code solution — always explain the WHY behind it")
        prompt_parts.append("10. Respond in Java (not Python) unless the student's code is in another language")
        
        # Add adaptive analysis knowledge graph info if available
        if adaptive_analysis:
            # Extract additional KG info from adaptive analysis
            if adaptive_analysis.get('prerequisites'):
                if not analysis.get('cse_kg', {}).get('prerequisites'):
                    if 'cse_kg' not in analysis:
                        analysis['cse_kg'] = {}
                    analysis['cse_kg']['prerequisites'] = [p.get('concept', '') if isinstance(p, dict) else str(p) for p in adaptive_analysis['prerequisites']]
            
            if adaptive_analysis.get('knowledge_gaps'):
                if not analysis.get('pedagogical_kg', {}).get('misconceptions'):
                    if 'pedagogical_kg' not in analysis:
                        analysis['pedagogical_kg'] = {}
                    analysis['pedagogical_kg']['misconceptions'] = [g.get('concept', '') for g in adaptive_analysis['knowledge_gaps']]
        
        return "\n".join(prompt_parts)
    
    def _update_conversation_history(
        self, student_id: str, message: str, response: str
    ):
        """Update conversation history"""
        if student_id not in self.conversation_history:
            self.conversation_history[student_id] = []
        
        self.conversation_history[student_id].append({
            'message': message,
            'response': response,
            'timestamp': datetime.now().isoformat(),
            'response_length': len(response)
        })
        
        # Keep only last 10 conversations
        if len(self.conversation_history[student_id]) > 10:
            self.conversation_history[student_id] = self.conversation_history[student_id][-10:]






