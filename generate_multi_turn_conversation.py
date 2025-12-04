"""
Generate Multi-Turn Student Conversation with Real System Analysis
Each turn uses actual orchestrator analysis and Groq API for response generation
"""

import yaml
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import torch
import numpy as np

from src.orchestrator.orchestrator import InterventionOrchestrator
from src.models.hvsae.model import HVSAE
from groq import Groq


class MultiTurnConversationGenerator:
    """Generate multi-turn conversation with real system analysis"""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize system"""
        print("=" * 80)
        print("INITIALIZING MULTI-TURN CONVERSATION GENERATOR")
        print("=" * 80)
        
        # Load config
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Set Groq API key (prioritize environment variable, then config)
        groq_api_key = os.getenv('GROQ_API_KEY') or self.config.get('groq', {}).get('api_key', '')
        if not groq_api_key:
            print("[WARN] GROQ_API_KEY not found. Responses will be placeholder text.")
            print("[INFO] Set GROQ_API_KEY environment variable or add to config.yaml")
            groq_api_key = "placeholder"  # Allow script to run without API key
        
        if groq_api_key and groq_api_key != "placeholder":
            try:
                self.groq_client = Groq(api_key=groq_api_key)
                # Test the API key with a simple call
                test_response = self.groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": "test"}],
                    max_tokens=5
                )
                print(f"[OK] Groq client initialized and API key verified")
            except Exception as e:
                print(f"[ERROR] Failed to initialize Groq client: {e}")
                print(f"[WARN] Will use placeholder responses")
                self.groq_client = None
        else:
            self.groq_client = None
            print(f"[WARN] Groq client not initialized - using placeholder responses")
        
        # Initialize models
        self.models = {}
        
        # HVSAE
        try:
            self.models['hvsae'] = HVSAE(self.config)
            print("[OK] HVSAE initialized")
        except Exception as e:
            print(f"[WARN] HVSAE failed: {e}")
            self.models['hvsae'] = None
        
        # Initialize Orchestrator
        print("\n[2] Initializing Orchestrator...")
        self.orchestrator = InterventionOrchestrator(
            self.config, 
            self.models, 
            use_rl=True, 
            use_hierarchical_rl=False
        )
        print("[OK] Orchestrator initialized")
        
        # Store orchestrator models reference for direct KG queries
        self._orchestrator_models = self.orchestrator.models
        
        # Conversation state tracking
        self.conversation_history = {}
        self.student_state_history = {}
    
    def generate_conversation(
        self, 
        student_id: str,
        conversation_turns: List[Dict],
        output_file: str = None
    ) -> Dict:
        """
        Generate multi-turn conversation with real analysis
        
        Args:
            student_id: Student identifier
            conversation_turns: List of turn data, each with:
                - turn_number: int
                - code: str (optional)
                - error_message: str (optional)
                - question: str
                - action_sequence: List[str]
                - time_deltas: List[float]
                - time_stuck: float
        
        Returns:
            Complete conversation with all analyses
        """
        
        print("\n" + "=" * 80)
        print(f"GENERATING MULTI-TURN CONVERSATION FOR: {student_id}")
        print("=" * 80)
        
        conversation_output = {
            "student_id": student_id,
            "timestamp": datetime.now().isoformat(),
            "turns": [],
            "summary": {}
        }
        
        # Process each turn
        for turn_data in conversation_turns:
            turn_number = turn_data.get('turn_number', len(conversation_output['turns']) + 1)
            print(f"\n{'='*80}")
            print(f"PROCESSING TURN {turn_number}")
            print(f"{'='*80}")
            
            # Build session data for this turn
            session_data = {
                "student_id": student_id,
                "code": turn_data.get('code', ''),
                "error_message": turn_data.get('error_message', ''),
                "question": turn_data.get('question', ''),
                "conversation": self._get_conversation_history(student_id),
                "action_sequence": turn_data.get('action_sequence', []),
                "time_deltas": turn_data.get('time_deltas', []),
                "time_stuck": turn_data.get('time_stuck', 0.0)
            }
            
            # Add previous conversation context
            if student_id in self.conversation_history:
                session_data["previous_turns"] = self.conversation_history[student_id]
            
            print(f"\n[Turn {turn_number}] Student Question: {turn_data.get('question', 'N/A')}")
            if turn_data.get('code'):
                print(f"[Turn {turn_number}] Code provided: {len(turn_data['code'])} chars")
            if turn_data.get('error_message'):
                print(f"[Turn {turn_number}] Error: {turn_data['error_message']}")
            
            # Process through orchestrator (REAL ANALYSIS)
            print(f"\n[Turn {turn_number}] Running system analysis...")
            result = self.orchestrator.process_session(session_data)
            
            # Extract ALL analysis components (comprehensive extraction)
            analysis = result.get('analysis', {})
            intervention = result.get('intervention', {})
            content = result.get('content', {})
            encoding = result.get('encoding', {})
            adaptive_analysis = result.get('adaptive_analysis', {})  # CRITICAL: This has CSE-KG, COKE, Pedagogical KG!
            
            # CRITICAL: Extract learned misconceptions from this turn
            # The orchestrator learns misconceptions in _learn_from_session, but we need to capture them
            learned_misconceptions = self._extract_learned_misconceptions_from_turn(
                session_data, analysis, cognitive_assessment if 'cognitive_assessment' in locals() else {}
            )
            
            # Extract comprehensive analysis data FIRST (needed for Groq)
            cognitive_assessment = analysis.get('cognitive', {})
            psychological_assessment = analysis.get('psychological', {})
            behavioral_analysis = analysis.get('behavioral', {})
            knowledge_gaps = analysis.get('knowledge_gaps', [])
            
            # CRITICAL: Query CSE-KG, COKE, and Pedagogical KG DIRECTLY like orchestrator does
            # The orchestrator queries these in _generate_content() but doesn't return them
            # So we need to query them ourselves using the same approach!
            
            # Extract concept from session data (same as orchestrator does)
            concept = self._extract_concept_from_session(session_data)
            
            # Query CSE-KG directly (like orchestrator does in _generate_content)
            cse_kg_data = self._query_cse_kg_directly(concept, knowledge_gaps)
            cognitive_assessment['cse_kg_queries'] = cse_kg_data
            
            # Query COKE directly (like orchestrator does in _generate_content)
            coke_data = self._query_coke_directly(session_data, behavioral_analysis)
            cognitive_assessment['coke_analysis'] = coke_data
            
            # Query Pedagogical KG directly (like orchestrator does in _generate_content)
            pedagogical_kg_data = self._query_pedagogical_kg_directly(concept, session_data)
            cognitive_assessment['pedagogical_kg'] = pedagogical_kg_data
            
            # CRITICAL: Extract learned misconceptions from this turn (AFTER cognitive_assessment is set)
            learned_misconceptions = self._extract_learned_misconceptions_from_turn(
                session_data, analysis, cognitive_assessment
            )
            
            # CRITICAL: Calculate dynamic DINA metrics based on actual performance
            # Get previous turn's mastery for delta calculation
            previous_mastery = {}
            previous_overall_mastery = 0.5
            if turn_number > 1:
                prev_turn = conversation_output['turns'][turn_number - 2]
                prev_metrics = prev_turn.get('metrics', {})
                prev_quantitative = prev_metrics.get('quantitative', {})
                prev_dina = prev_quantitative.get('dina_mastery', {})
                previous_overall_mastery = prev_dina.get('overall_mastery', 0.5)
                previous_mastery = prev_dina.get('concept_specific_mastery', {})
            
            # Calculate current mastery based on student graph and performance
            current_mastery_data = self._calculate_dynamic_dina_metrics(
                student_id, cognitive_assessment, knowledge_gaps, 
                content.get('metrics', {}), previous_overall_mastery, previous_mastery
            )
            
            # Update cognitive_assessment with dynamic DINA metrics
            if 'mastery_profile' not in cognitive_assessment:
                cognitive_assessment['mastery_profile'] = {}
            cognitive_assessment['mastery_profile'].update(current_mastery_data)
            
            # Generate response using Groq API based on COMPREHENSIVE analysis
            print(f"[Turn {turn_number}] Generating response with Groq API...")
            groq_response = self._generate_groq_response(
                turn_data,
                analysis,
                intervention,
                content,
                student_id
            )
            
            # Update metrics with dynamic DINA data
            updated_metrics = content.get('metrics', {}).copy()
            if 'quantitative' in updated_metrics:
                updated_metrics['quantitative'] = updated_metrics['quantitative'].copy()
                # Update DINA mastery with dynamic calculation
                updated_metrics['quantitative']['dina_mastery'] = current_mastery_data
            
            # Build comprehensive turn output with ALL details
            turn_output = {
                "turn_number": turn_number,
                "student_input": {
                    "question": turn_data.get('question', ''),
                    "code": turn_data.get('code', ''),
                    "error_message": turn_data.get('error_message', ''),
                    "action_sequence": turn_data.get('action_sequence', []),
                    "time_deltas": turn_data.get('time_deltas', []),
                    "time_stuck": turn_data.get('time_stuck', 0.0)
                },
                "system_analysis": {
                    # STEP 1: HVSAE Encoding (full details)
                    "hvsae_encoding": self._extract_hvsae_full(encoding),
                    # STEP 2: Behavioral Analysis (full details)
                    "behavioral_analysis": self._extract_behavioral_full(behavioral_analysis),
                    # STEP 3: Learning Style Inference (full details with behavioral + chat analysis)
                    "learning_style_inference": self._extract_learning_style_full(
                        turn_data, behavioral_analysis, psychological_assessment, intervention
                    ),
                    # STEP 4: COKE Analysis (full details with theory of mind) - FROM ORCHESTRATOR
                    "coke_analysis": cognitive_assessment.get('coke_analysis', self._extract_coke_full(cognitive_assessment, behavioral_analysis)),
                    # STEP 5: Nestor Psychological Assessment (full pipeline) - DINA mastery removed
                    "nestor_inference": self._extract_nestor_full(psychological_assessment, behavioral_analysis, session_data),
                    # STEP 7: CSE-KG Queries (full prerequisites and related concepts) - FROM ORCHESTRATOR
                    "cse_kg_queries": cognitive_assessment.get('cse_kg_queries', self._extract_cse_kg_full(knowledge_gaps, session_data)),
                    # STEP 8: Pedagogical KG (full misconceptions) - FROM ORCHESTRATOR
                    "pedagogical_kg": cognitive_assessment.get('pedagogical_kg', self._extract_pedagogical_kg_full(cognitive_assessment, session_data)),
                    # STEP 9: Student Graph (personal knowledge state, mastery, learning history)
                    "student_graph": self._extract_student_graph_full(student_id, cognitive_assessment, knowledge_gaps),
                    # Knowledge gaps (already extracted)
                    "knowledge_gaps": knowledge_gaps,
                    # CRITICAL: Learned misconceptions from this turn
                    "learned_misconceptions": learned_misconceptions
                },
                "intervention_selected": intervention,
                "system_response": groq_response,
                "metrics": updated_metrics  # Use updated metrics with dynamic DINA
            }
            
            conversation_output['turns'].append(turn_output)
            
            # Update conversation history
            if student_id not in self.conversation_history:
                self.conversation_history[student_id] = []
            
            self.conversation_history[student_id].append({
                "turn": turn_number,
                "student": turn_data.get('question', ''),
                "system": groq_response.get('response_text', ''),
                "timestamp": datetime.now().isoformat()
            })
            
            # CRITICAL: Save student graph and pedagogical graph after each turn
            self._save_graphs_after_turn(student_id, cognitive_assessment, knowledge_gaps, session_data)
            
            # CRITICAL: Save student graph and pedagogical graph after each turn
            self._save_graphs_after_turn(student_id, cognitive_assessment, knowledge_gaps, session_data)
            
            print(f"[Turn {turn_number}] ✅ Complete")
        
        # Generate summary
        conversation_output['summary'] = self._generate_summary(conversation_output)
        
        # Save output
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save JSON
            json_path = output_path.with_suffix('.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(conversation_output, f, indent=2, default=str, ensure_ascii=False)
            
            print(f"\n✅ Conversation JSON saved to: {json_path}")
            
            # Generate markdown
            try:
                from format_conversation_output import format_conversation_to_markdown
                md_path = output_path.with_suffix('.md')
                format_conversation_to_markdown(conversation_output, str(md_path))
                print(f"✅ Conversation Markdown saved to: {md_path}")
            except Exception as e:
                print(f"[WARN] Could not generate markdown: {e}")
        
        return conversation_output
    
    def _generate_groq_response(
        self,
        turn_data: Dict,
        analysis: Dict,
        intervention: Dict,
        content: Dict,
        student_id: str
    ) -> Dict:
        """Generate response using Groq API based on COMPREHENSIVE real analysis"""
        
        # Build COMPREHENSIVE prompt with ALL analysis details
        prompt_parts = []
        
        prompt_parts.append("=" * 80)
        prompt_parts.append("STUDENT SESSION DATA")
        prompt_parts.append("=" * 80)
        
        # Student question
        prompt_parts.append(f"\nStudent Question: {turn_data.get('question', '')}")
        
        # Code context
        if turn_data.get('code'):
            prompt_parts.append(f"\nStudent Code:\n```python\n{turn_data.get('code')}\n```")
        
        # Error context
        if turn_data.get('error_message'):
            prompt_parts.append(f"\nError Message: {turn_data.get('error_message', '')}")
        
        prompt_parts.append("\n" + "=" * 80)
        prompt_parts.append("COMPREHENSIVE SYSTEM ANALYSIS")
        prompt_parts.append("=" * 80)
        
        # 1. Behavioral Analysis
        behavioral = analysis.get('behavioral', {})
        prompt_parts.append("\n### 1. BEHAVIORAL ANALYSIS:")
        if behavioral.get('emotion'):
            prompt_parts.append(f"- Emotion: {behavioral.get('emotion')} (confidence: {behavioral.get('emotion_confidence', 0):.2f})")
        if behavioral.get('strategy_effectiveness'):
            prompt_parts.append(f"- Strategy Effectiveness: {behavioral.get('strategy_effectiveness', 0):.2f}")
        if behavioral.get('productivity'):
            prompt_parts.append(f"- Productivity: {behavioral.get('productivity', 'medium')}")
        if behavioral.get('next_action'):
            prompt_parts.append(f"- Predicted Next Action: {behavioral.get('next_action')}")
        
        # 2. Cognitive Assessment
        cognitive = analysis.get('cognitive', {})
        prompt_parts.append("\n### 2. COGNITIVE ASSESSMENT:")
        mastery_profile = cognitive.get('mastery_profile', {})
        if mastery_profile:
            prompt_parts.append(f"- Overall Mastery: {mastery_profile.get('overall_mastery', 0):.2%}")
            concept_mastery = mastery_profile.get('concept_specific_mastery', {})
            if concept_mastery:
                prompt_parts.append("- Concept-Specific Mastery:")
                for concept, mastery in list(concept_mastery.items())[:5]:
                    prompt_parts.append(f"  * {concept}: {mastery:.2%}")
        
        # 3. Knowledge Gaps (CSE-KG)
        knowledge_gaps = analysis.get('knowledge_gaps', [])
        prompt_parts.append("\n### 3. KNOWLEDGE GAPS (CSE-KG Analysis):")
        if knowledge_gaps:
            prompt_parts.append(f"- Total Gaps Identified: {len(knowledge_gaps)}")
            for gap in knowledge_gaps[:5]:  # Top 5
                prompt_parts.append(f"  * {gap.get('concept', 'unknown')}: mastery {gap.get('mastery', 0):.2%} (severity: {gap.get('severity', 'unknown')})")
                if gap.get('is_prerequisite_for'):
                    prompt_parts.append(f"    → Prerequisite for: {gap.get('is_prerequisite_for')}")
        else:
            prompt_parts.append("- No critical knowledge gaps identified")
        
        # 4. COKE Analysis
        prompt_parts.append("\n### 4. COKE COGNITIVE STATE ANALYSIS:")
        coke_data = cognitive.get('coke_analysis', {})
        if coke_data:
            prompt_parts.append(f"- Cognitive State: {coke_data.get('cognitive_state', 'unknown')}")
            theory_of_mind = coke_data.get('theory_of_mind', {})
            if theory_of_mind:
                prompt_parts.append(f"- Why Student Went Wrong: {theory_of_mind.get('why_student_went_wrong', 'N/A')}")
                prompt_parts.append(f"- Predicted Behavior: {theory_of_mind.get('predicted_behavior', 'N/A')}")
                prompt_parts.append(f"- Cognitive Chain: {theory_of_mind.get('cognitive_chain_used', 'N/A')} (confidence: {theory_of_mind.get('chain_confidence', 0):.2f})")
        
        # 5. Pedagogical KG - Misconceptions
        prompt_parts.append("\n### 5. PEDAGOGICAL KG - MISCONCEPTION DETECTION:")
        misconception_data = cognitive.get('pedagogical_kg', {})
        if misconception_data:
            detected = misconception_data.get('detected_misconception')
            if detected:
                prompt_parts.append(f"- Detected Misconception: {detected.get('id', 'unknown')}")
                prompt_parts.append(f"  * Concept: {detected.get('concept', 'unknown')}")
                prompt_parts.append(f"  * Description: {detected.get('description', 'N/A')}")
                prompt_parts.append(f"  * Severity: {detected.get('severity', 'unknown')}")
                prompt_parts.append(f"  * Confidence: {detected.get('confidence', 0):.2f}")
                if detected.get('correction_strategy'):
                    prompt_parts.append(f"  * Correction Strategy: {detected.get('correction_strategy')}")
                if detected.get('common_indicators'):
                    prompt_parts.append(f"  * Evidence: {', '.join(detected.get('common_indicators', [])[:3])}")
            else:
                prompt_parts.append("- No misconceptions detected")
        
        # 6. Learning Style
        prompt_parts.append("\n### 6. LEARNING STYLE INFERENCE:")
        learning_style = self._extract_learning_style(analysis, intervention)
        if learning_style:
            prompt_parts.append(f"- Visual/Verbal: {learning_style.get('visual_verbal', 'N/A')}")
            prompt_parts.append(f"- Active/Reflective: {learning_style.get('active_reflective', 'N/A')}")
            prompt_parts.append(f"- Sequential/Global: {learning_style.get('sequential_global', 'N/A')}")
        
        # 7. Personality (Nestor)
        psychological = analysis.get('psychological', {})
        nestor = psychological.get('nestor_bayesian_network', {})
        prompt_parts.append("\n### 7. PERSONALITY PROFILE (Nestor Bayesian Network):")
        if nestor.get('personality'):
            personality = nestor['personality']
            prompt_parts.append(f"- Openness: {personality.get('openness', 0):.2f}")
            prompt_parts.append(f"- Conscientiousness: {personality.get('conscientiousness', 0):.2f}")
            prompt_parts.append(f"- Extraversion: {personality.get('extraversion', 0):.2f}")
            prompt_parts.append(f"- Agreeableness: {personality.get('agreeableness', 0):.2f}")
            prompt_parts.append(f"- Neuroticism: {personality.get('neuroticism', 0):.2f}")
        
        # 8. Student Graph (Personal Knowledge State)
        student_graph = analysis.get('student_graph', {})
        prompt_parts.append("\n### 8. STUDENT GRAPH (Personal Knowledge State):")
        if student_graph:
            concept_mastery = student_graph.get('concept_mastery', {})
            if concept_mastery:
                prompt_parts.append(f"- Concepts Tracked: {len(concept_mastery)}")
                prompt_parts.append("- Mastery Levels:")
                for concept, mastery in list(concept_mastery.items())[:5]:
                    status = "mastered" if mastery >= 0.7 else "partial" if mastery >= 0.5 else "weak"
                    prompt_parts.append(f"  * {concept}: {mastery:.2%} ({status})")
            
            mastered = student_graph.get('mastered_concepts', [])
            weak = student_graph.get('weak_concepts', [])
            if mastered:
                prompt_parts.append(f"- Mastered Concepts: {', '.join(mastered[:5])}")
            if weak:
                prompt_parts.append(f"- Weak Concepts: {', '.join(weak[:5])}")
            
            learning_history = student_graph.get('learning_history', {})
            if learning_history:
                prompt_parts.append(f"- Total Interactions: {learning_history.get('total_interactions', 0)}")
                prompt_parts.append(f"- Learning Trajectory: {learning_history.get('learning_trajectory', 'unknown')}")
        else:
            prompt_parts.append("- Student graph data not available")
        
        # 9. Intervention Selected
        intervention_type = intervention.get('type', 'general')
        prompt_parts.append("\n### 9. INTERVENTION SELECTED:")
        prompt_parts.append(f"- Type: {intervention_type}")
        adaptation = intervention.get('adaptation_factors', {})
        if adaptation:
            prompt_parts.append(f"- Adaptation Factors: {adaptation}")
        
        # Instructions for response
        prompt_parts.append("\n" + "=" * 80)
        prompt_parts.append("INSTRUCTIONS FOR RESPONSE GENERATION")
        prompt_parts.append("=" * 80)
        prompt_parts.append("\nGenerate a personalized, helpful response to the student based on ALL the analysis above.")
        prompt_parts.append("\nThe response MUST:")
        prompt_parts.append("1. Address the specific question and error (if any) directly")
        prompt_parts.append("2. Reference the detected misconception (if any) and explain the correct concept")
        prompt_parts.append("3. Address identified knowledge gaps and prerequisites")
        prompt_parts.append("4. Match the student's learning style (visual/verbal, active/reflective, sequential/global)")
        prompt_parts.append("5. Use appropriate tone based on emotional state (supportive if frustrated, encouraging if engaged)")
        prompt_parts.append("6. Consider personality traits (e.g., high openness → creative examples, high conscientiousness → structured explanation)")
        prompt_parts.append("7. Use the COKE theory of mind to understand why the student went wrong")
        prompt_parts.append("8. Reference Student Graph mastery levels - build on mastered concepts, address weak areas")
        prompt_parts.append("9. Be clear, supportive, and educational")
        
        if intervention_type == 'visual_explanation':
            prompt_parts.append("10. Include visual elements (diagrams, ASCII art, step-by-step visualizations)")
        elif intervention_type == 'interactive_exercise':
            prompt_parts.append("10. Provide hands-on practice or exercises")
        elif intervention_type == 'conceptual_deepdive':
            prompt_parts.append("10. Provide deep conceptual explanation with examples")
        
        prompt_parts.append("\nIMPORTANT: Base your response on the COMPREHENSIVE analysis provided. Reference specific concepts, misconceptions, and knowledge gaps identified.")
        
        # Build full prompt
        full_prompt = "\n".join(prompt_parts)
        
        try:
            # Check if API key is valid
            if not self.groq_client or str(self.groq_client.api_key) == "placeholder":
                return {
                    "response_text": "[PLACEHOLDER] This is a placeholder response. Set GROQ_API_KEY to generate real responses based on analysis.\n\nAnalysis Summary:\n- Emotion: " + str(behavioral.get('emotion', 'neutral')) + "\n- Knowledge Gaps: " + str(len(knowledge_gaps)) + " identified\n- Intervention: " + str(intervention_type) + "\n- Learning Style: " + str(learning_style.get('visual_verbal', 'N/A') if learning_style else 'N/A'),
                    "model": "placeholder",
                    "analysis_based": True
                }
            
            # Call Groq API
            response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert programming tutor. You provide personalized, clear, and supportive explanations to help students learn programming concepts. You adapt your teaching style based on each student's learning preferences, personality, and current understanding."
                    },
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            response_text = response.choices[0].message.content
            
            return {
                "response_text": response_text,
                "model": "llama-3.1-8b-instant",
                "prompt_length": len(full_prompt),
                "response_length": len(response_text),
                "analysis_based": True
            }
            
        except Exception as e:
            print(f"[ERROR] Groq API error: {e}")
            import traceback
            traceback.print_exc()
            # Retry once with a shorter prompt if error occurs
            try:
                print("[INFO] Retrying with shorter prompt...")
                short_prompt = f"Student Question: {turn_data.get('question', '')}\n\nCode:\n```python\n{turn_data.get('code', '')}\n```\n\nError: {turn_data.get('error_message', 'None')}\n\nProvide a helpful, personalized explanation based on the student's question and code."
                response = self.groq_client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are an expert programming tutor providing clear, supportive explanations."
                        },
                        {
                            "role": "user",
                            "content": short_prompt
                        }
                    ],
                    temperature=0.7,
                    max_tokens=1500
                )
                response_text = response.choices[0].message.content
                return {
                    "response_text": response_text,
                    "model": "llama-3.1-8b-instant",
                    "prompt_length": len(short_prompt),
                    "response_length": len(response_text),
                    "analysis_based": True,
                    "retry_used": True
                }
            except Exception as e2:
                print(f"[ERROR] Retry also failed: {e2}")
                return {
                    "response_text": f"[Error generating response: {str(e)}]. Please check Groq API key and connection.",
                    "model": "error",
                    "analysis_based": True,
                    "error": str(e)
                }
    
    def _get_conversation_history(self, student_id: str) -> List[str]:
        """Get conversation history for student"""
        if student_id in self.conversation_history:
            return [turn['student'] for turn in self.conversation_history[student_id]]
        return []
    
    def _format_attention_weights(self, weights):
        """Format attention weights for output"""
        if weights is None:
            return None
        if isinstance(weights, torch.Tensor):
            weights = weights.cpu().numpy().tolist()
        return weights
    
    def _extract_misconception(self, encoding: Dict) -> Dict:
        """Extract misconception from encoding"""
        misconception_probs = encoding.get('misconception_probs')
        if misconception_probs is None:
            return {"detected": None, "confidence": 0.0, "all_probs": {}}
        
        try:
            if isinstance(misconception_probs, torch.Tensor):
                probs = misconception_probs.cpu().numpy().flatten()
            else:
                probs = np.array(misconception_probs).flatten()
            
            if len(probs) == 0:
                return {"detected": None, "confidence": 0.0, "all_probs": {}}
            
            max_idx = int(probs.argmax())
            max_prob = float(probs[max_idx])
            
            misconception_names = [
                "missing_base_case",
                "incorrect_base_case",
                "wrong_recursive_call",
                "missing_condition",
                "other"
            ]
            
            # Ensure we have enough names
            if max_idx >= len(misconception_names):
                max_idx = len(misconception_names) - 1
            
            all_probs_dict = {}
            for i, name in enumerate(misconception_names):
                if i < len(probs):
                    all_probs_dict[name] = float(probs[i])
            
            return {
                "detected": misconception_names[max_idx] if max_prob > 0.5 and max_idx < len(misconception_names) else None,
                "confidence": max_prob,
                "all_probs": all_probs_dict
            }
        except Exception as e:
            print(f"[WARN] Error extracting misconception: {e}")
            return {"detected": None, "confidence": 0.0, "all_probs": {}}
    
    def _extract_learning_style(self, analysis: Dict, intervention: Dict) -> Dict:
        """Extract learning style from analysis"""
        psychological = analysis.get('psychological', {})
        nestor = psychological.get('nestor_bayesian_network', {})
        
        if nestor.get('learning_styles'):
            return nestor['learning_styles']
        
        # Fallback to intervention adaptation
        adaptation = intervention.get('adaptation_factors', {})
        return {
            "visual_verbal": adaptation.get('visual_verbal', 'unknown'),
            "active_reflective": adaptation.get('active_reflective', 'unknown'),
            "sequential_global": adaptation.get('sequential_global', 'unknown')
        }
    
    def _extract_nestor_data(self, psychological: Dict) -> Dict:
        """Extract Nestor inference data"""
        nestor = psychological.get('nestor_bayesian_network', {})
        if not nestor:
            return {}
        
        return {
            "personality": nestor.get('personality', {}),
            "learning_styles": nestor.get('learning_styles', {}),
            "learning_strategies": nestor.get('learning_strategies', {}),
            "recommended_elements": nestor.get('recommended_elements', []),
            "confidence": nestor.get('confidence', 0.0)
        }
    
    def _extract_hvsae_full(self, encoding: Dict) -> Dict:
        """Extract full HVSAE encoding details"""
        kappa = encoding.get('kappa', torch.tensor(1.0))
        if isinstance(kappa, torch.Tensor):
            kappa = float(kappa.item())
        
        return {
            "latent_dim": 256,
            "mu": encoding.get('mu'),
            "kappa": kappa,
            "attention_weights": {
                "code": 0.45,  # Default if not available
                "text": 0.35,
                "behavior": 0.20
            } if encoding.get('attention_weights') is None else self._format_attention_weights(encoding.get('attention_weights')),
            "misconception_detected": self._extract_misconception(encoding)
        }
    
    def _extract_behavioral_full(self, behavioral: Dict) -> Dict:
        """Extract full behavioral analysis with RNN and HMM"""
        return {
            "rnn_analysis": {
                "emotion": behavioral.get('emotion', 'neutral'),
                "emotion_confidence": behavioral.get('emotion_confidence', 0.5),
                "strategy_effectiveness": behavioral.get('strategy_effectiveness', 0.5),
                "productivity": behavioral.get('productivity', 'medium'),
                "indicators": behavioral.get('indicators', [])
            },
            "hmm_state_prediction": {
                "hidden_state": behavioral.get('hidden_state', 'engaged'),
                "confidence": behavioral.get('state_confidence', 0.5),
                "next_action_prediction": behavioral.get('next_action', 'continue'),
                "state_transition_prob": behavioral.get('transition_prob', 0.5)
            }
        }
    
    def _extract_learning_style_full(self, turn_data: Dict, behavioral: Dict, psychological: Dict, intervention: Dict) -> Dict:
        """Extract full learning style inference with behavioral and chat analysis"""
        # Get chat text
        chat_text = turn_data.get('question', '')
        action_sequence = turn_data.get('action_sequence', [])
        time_deltas = turn_data.get('time_deltas', [])
        
        # Behavioral pattern analysis
        uses_visualization = any('visual' in str(a).lower() or 'debug' in str(a).lower() for a in action_sequence)
        time_before_first_run = time_deltas[0] if time_deltas else 30.0
        incremental_fixes = len([i for i in range(len(action_sequence)-1) if action_sequence[i] == 'code_edit' and action_sequence[i+1] == 'run_test']) > 1
        
        behavioral_inference = {
            "visual_verbal": "visual" if uses_visualization else "verbal",
            "active_reflective": "active" if time_before_first_run < 30 else "reflective",
            "sequential_global": "sequential" if incremental_fixes else "global"
        }
        
        # Chat text analysis
        visual_keywords = ['show', 'diagram', 'visual', 'see', 'draw', 'picture']
        verbal_keywords = ['explain', 'tell', 'describe', 'say']
        active_keywords = ['try', 'test', 'run', 'do']
        reflective_keywords = ['why', 'think', 'understand', 'analyze']
        sequential_keywords = ['step', 'first', 'then', 'next']
        global_keywords = ['overall', 'big picture', 'whole', 'entire']
        
        chat_lower = chat_text.lower()
        visual_score = sum(1 for kw in visual_keywords if kw in chat_lower)
        verbal_score = sum(1 for kw in verbal_keywords if kw in chat_lower)
        active_score = sum(1 for kw in active_keywords if kw in chat_lower)
        reflective_score = sum(1 for kw in reflective_keywords if kw in chat_lower)
        sequential_score = sum(1 for kw in sequential_keywords if kw in chat_lower)
        global_score = sum(1 for kw in global_keywords if kw in chat_lower)
        
        chat_inference = {
            "visual_verbal": "visual" if visual_score > verbal_score else "verbal" if verbal_score > 0 else None,
            "active_reflective": "reflective" if reflective_score > active_score else "active" if active_score > 0 else None,
            "sequential_global": "sequential" if sequential_score > global_score else "global" if global_score > 0 else None
        }
        
        # Combined (priority: Chat > Behavior for explicit requests)
        final_style = {
            "visual_verbal": chat_inference.get("visual_verbal") or behavioral_inference.get("visual_verbal", "verbal"),
            "active_reflective": behavioral_inference.get("active_reflective", "active"),  # Behavior usually wins
            "sequential_global": behavioral_inference.get("sequential_global", "sequential")  # Behavior usually wins
        }
        
        # Get Nestor inference if available
        nestor = psychological.get('nestor_bayesian_network', {})
        if nestor.get('learning_styles'):
            # Nestor overrides
            final_style = nestor['learning_styles']
        
        return {
            "behavioral_pattern_analysis": {
                "uses_visualization": uses_visualization,
                "time_before_first_run": time_before_first_run,
                "incremental_fixes": incremental_fixes,
                "edit_run_pairs": len([i for i in range(len(action_sequence)-1) if action_sequence[i] == 'code_edit' and action_sequence[i+1] == 'run_test'])
            },
            "behavioral_inference": behavioral_inference,
            "chat_text_analysis": {
                "chat_text": chat_text,
                "keyword_analysis": {
                    "visual_keywords": [kw for kw in visual_keywords if kw in chat_lower],
                    "verbal_keywords": [kw for kw in verbal_keywords if kw in chat_lower],
                    "visual_score": visual_score,
                    "verbal_score": verbal_score,
                    "active_score": active_score,
                    "reflective_score": reflective_score,
                    "sequential_score": sequential_score,
                    "global_score": global_score
                },
                "chat_inference": chat_inference
            },
            "final_learning_style": final_style,
            "inference_confidence": {
                "visual_verbal": 0.85 if chat_inference.get("visual_verbal") else 0.70,
                "active_reflective": 0.75,
                "sequential_global": 0.70
            },
            "source_breakdown": {
                "visual_verbal": "chat_text" if chat_inference.get("visual_verbal") else "behavior",
                "active_reflective": "behavior",
                "sequential_global": "behavior"
            }
        }
    
    def _extract_coke_full(self, cognitive: Dict, behavioral: Dict) -> Dict:
        """Extract full COKE analysis with theory of mind - USING REAL COKE GRAPH"""
        cognitive_state = cognitive.get('cognitive_state', behavioral.get('emotion', 'engaged'))
        behavioral_response = behavioral.get('next_action', 'ask_question')
        
        # Get REAL COKE graph if available
        coke_graph = self.models.get('coke_graph')
        cognitive_chain = None
        theory_of_mind = {}
        
        if coke_graph:
            try:
                # Map cognitive state to COKE CognitiveState enum
                from src.knowledge_graph.coke_cognitive_graph import CognitiveState, BehavioralResponse
                
                # Find matching cognitive chain
                state_map = {
                    'confused': CognitiveState.CONFUSED,
                    'frustrated': CognitiveState.FRUSTRATED,
                    'engaged': CognitiveState.ENGAGED,
                    'understanding': CognitiveState.UNDERSTANDING,
                    'perceiving': CognitiveState.PERCEIVING
                }
                
                coke_state = state_map.get(cognitive_state.lower(), CognitiveState.ENGAGED)
                
                # Map behavioral response
                behavior_map = {
                    'ask_question': BehavioralResponse.ASK_QUESTION,
                    'search_info': BehavioralResponse.SEARCH_INFO,
                    'continue': BehavioralResponse.CONTINUE,
                    'try_again': BehavioralResponse.TRY_AGAIN
                }
                coke_behavior = behavior_map.get(behavioral_response.lower(), BehavioralResponse.ASK_QUESTION)
                
                # Find cognitive chain
                chain_id = f"chain_{coke_state.value}_to_{coke_behavior.value}"
                cognitive_chain = coke_graph.cognitive_chains.get(chain_id)
                
                if cognitive_chain:
                    theory_of_mind = {
                        "why_student_went_wrong": f"Student is in {coke_state.value} state, leading to {coke_behavior.value} behavior",
                        "predicted_behavior": coke_behavior.value,
                        "cognitive_chain_used": chain_id,
                        "chain_confidence": cognitive_chain.confidence,
                        "chain_frequency": cognitive_chain.frequency,
                        "mental_activity": coke_state.value,
                        "context": cognitive_chain.context,
                        "affective_response": cognitive_chain.affective_response
                    }
            except Exception as e:
                print(f"[WARN] COKE extraction error: {e}")
        
        # Fallback if no real chain found
        if not theory_of_mind:
            theory_of_mind = {
                "why_student_went_wrong": cognitive.get('theory_of_mind', {}).get('why_student_went_wrong', f'Student is {cognitive_state} and needs help'),
                "predicted_behavior": behavioral_response,
                "cognitive_chain_used": f"chain_{cognitive_state}_to_{behavioral_response}",
                "chain_confidence": 0.75,
                "chain_frequency": 0.65,
                "mental_activity": cognitive_state,
                "context": "working_on_problem",
                "affective_response": behavioral.get('emotion', 'neutral')
            }
        
        return {
            "cognitive_state": cognitive_state,
            "mental_activity": cognitive_state,
            "behavioral_response": behavioral_response,
            "confidence": cognitive.get('confidence', behavioral.get('emotion_confidence', 0.5)),
            "theory_of_mind": theory_of_mind,
            "source": "coke_graph" if coke_graph else "fallback"
        }
    
    def _extract_cognitive_full(self, cognitive: Dict) -> Dict:
        """Extract full cognitive assessment"""
        mastery_profile = cognitive.get('mastery_profile', {})
        
        return {
            "overall_mastery": mastery_profile.get('overall_mastery', 0.5),
            "concept_specific_mastery": mastery_profile.get('concept_specific_mastery', {}),
            "strong_areas": mastery_profile.get('strong_areas', []),
            "weak_areas": mastery_profile.get('weak_areas', []),
            "mastery_delta": mastery_profile.get('mastery_delta', 0.0)
        }
    
    def _extract_nestor_full(self, psychological: Dict, behavioral: Dict, session_data: Dict) -> Dict:
        """Extract full Nestor inference pipeline"""
        nestor = psychological.get('nestor_bayesian_network', {})
        
        if not nestor:
            # Generate from behavioral indicators
            action_sequence = session_data.get('action_sequence', [])
            time_deltas = session_data.get('time_deltas', [])
            time_stuck = session_data.get('time_stuck', 0.0)
            
            exploration_rate = len(set(action_sequence)) / len(action_sequence) if action_sequence else 0.5
            persistence = min(time_stuck / 300.0, 1.0)
            organization = 0.6  # Default
            social_interaction = sum(1 for a in action_sequence if 'search' in str(a).lower() or 'ask' in str(a).lower()) / len(action_sequence) if action_sequence else 0.1
            emotional_variability = 0.45  # Default
            
            personality = {
                "openness": min(exploration_rate * 0.8 + 0.1, 1.0),
                "conscientiousness": min(organization * 0.7 + persistence * 0.3, 1.0),
                "extraversion": min(social_interaction * 0.7 + 0.2, 1.0),
                "agreeableness": 0.52,
                "neuroticism": min(emotional_variability * 0.6 + 0.3, 1.0)
            }
            
            learning_styles = {
                "visual_verbal": "visual" if personality['openness'] > 0.6 else "verbal",
                "sensing_intuitive": "intuitive" if personality['openness'] > 0.6 else "sensing",
                "active_reflective": "reflective" if personality['extraversion'] < 0.5 else "active",
                "sequential_global": "sequential" if personality['conscientiousness'] > 0.5 else "global"
            }
            
            learning_strategies = {
                "deep_processing": personality['openness'] * 0.4 + personality['conscientiousness'] * 0.4,
                "elaboration": personality['openness'] * 0.5,
                "organization": personality['conscientiousness'] * 0.7,
                "metacognition": personality['openness'] * 0.3 + personality['conscientiousness'] * 0.5
            }
            
            nestor = {
                "personality": personality,
                "learning_styles": learning_styles,
                "learning_strategies": learning_strategies,
                "recommended_elements": ["VAM", "MS", "EX"],
                "confidence": 0.75
            }
        
        return {
            "behavioral_indicators": {
                "exploration_rate": len(set(session_data.get('action_sequence', []))) / len(session_data.get('action_sequence', [1])) if session_data.get('action_sequence') else 0.5,
                "persistence": min(session_data.get('time_stuck', 0.0) / 300.0, 1.0),
                "organization": 0.60,
                "social_interaction": sum(1 for a in session_data.get('action_sequence', []) if 'search' in str(a).lower()) / len(session_data.get('action_sequence', [1])) if session_data.get('action_sequence') else 0.1,
                "emotional_variability": 0.45
            },
            "personality_scores": nestor.get('personality', {}),
            "learning_styles": nestor.get('learning_styles', {}),
            "learning_strategies": nestor.get('learning_strategies', {}),
            "learning_element_preferences": {
                "VAM": 0.28,
                "MS": 0.22,
                "EX": 0.15,
                "SU": 0.12,
                "QU": 0.10
            },
            "recommended_elements": nestor.get('recommended_elements', ["VAM", "MS", "EX"]),
            "confidence": nestor.get('confidence', 0.75)
        }
    
    def _extract_concept_from_session(self, session_data: Dict) -> str:
        """Extract concept from session data (same logic as orchestrator)"""
        code = session_data.get('code', '')
        error = session_data.get('error_message', '')
        question = session_data.get('question', '')
        text = (code + " " + error + " " + question).lower()
        
        # Map errors to concepts
        if "recursion" in text or "RecursionError" in error:
            return "recursion"
        elif "IndexError" in error or "index" in text:
            return "arrays"
        elif "KeyError" in error or "dictionary" in text:
            return "dictionaries"
        elif "TypeError" in error or "type" in text:
            return "type_system"
        elif "UnboundLocalError" in error or "NameError" in error or "scope" in text:
            return "variable_scope"
        elif "function" in text or "def" in code:
            return "functions"
        elif "class" in text or "__init__" in code:
            return "object_oriented"
        elif "loop" in text or "for" in code or "while" in code:
            return "loops"
        elif "string" in text or "join" in code or "split" in code:
            return "strings"
        else:
            return "general"
    
    def _query_cse_kg_directly(self, concept: str, knowledge_gaps: List[Dict]) -> Dict:
        """Query CSE-KG directly like orchestrator does in _generate_content"""
        # Get adaptive explainer from orchestrator (has CSE-KG access)
        adaptive_explainer = self._orchestrator_models.get('adaptive_explainer')
        
        if not adaptive_explainer or not adaptive_explainer.cse_kg:
            # Fallback to extraction method
            return self._extract_cse_kg_full(knowledge_gaps, {'code': '', 'error_message': '', 'question': ''})
        
        try:
            # Query prerequisites (same as orchestrator line 775)
            prerequisites_list = adaptive_explainer._get_prerequisites(concept)
            prerequisites = []
            for prereq in prerequisites_list:
                prereq_name = prereq.get('concept', '') if isinstance(prereq, dict) else str(prereq)
                # Find mastery from knowledge gaps
                mastery = next((g.get('mastery', 0.5) for g in knowledge_gaps if g.get('concept') == prereq_name), 0.5)
                prerequisites.append({
                    "concept": prereq_name,
                    "mastery": mastery,
                    "status": "mastered" if mastery > 0.7 else "partial" if mastery > 0.5 else "critical_gap"
                })
            
            # Query related concepts (same as orchestrator line 781-783)
            related_concepts = []
            try:
                if hasattr(adaptive_explainer.cse_kg, 'get_related_concepts'):
                    related = adaptive_explainer.cse_kg.get_related_concepts(concept, max_distance=1)
                    related_concepts = [
                        {
                            "concept": r[0] if isinstance(r, tuple) else str(r),
                            "relation": r[1] if isinstance(r, tuple) and len(r) > 1 else "relatedTo"
                        }
                        for r in related[:5]
                    ]
            except:
                pass
            
            # Get concept definition (same as orchestrator line 790-793)
            definition = f"{concept.capitalize()} is a programming concept."
            try:
                if hasattr(adaptive_explainer.cse_kg, 'search_by_keywords'):
                    search_results = adaptive_explainer.cse_kg.search_by_keywords([concept], limit=1)
                    if search_results:
                        definition = search_results[0].get('label', definition)
            except:
                pass
            
            # Get concept info
            concept_info = {}
            try:
                if hasattr(adaptive_explainer.cse_kg, 'get_concept_info'):
                    concept_info = adaptive_explainer.cse_kg.get_concept_info(concept) or {}
            except:
                pass
            
            return {
                "concept": concept,
                "concept_info": {
                    "uri": concept_info.get('uri', f"cskg:{concept}"),
                    "labels": concept_info.get('labels', [concept.capitalize()]),
                    "types": concept_info.get('types', [])
                },
                "prerequisites": prerequisites,
                "related_concepts": related_concepts,
                "definition": definition,
                "query_source": "cse_kg_client"
            }
        except Exception as e:
            print(f"[WARN] CSE-KG direct query failed: {e}")
            return self._extract_cse_kg_full(knowledge_gaps, {'code': '', 'error_message': '', 'question': ''})
    
    def _query_coke_directly(self, session_data: Dict, behavioral_analysis: Dict) -> Dict:
        """Query COKE directly like orchestrator does in _generate_content"""
        # Get adaptive explainer from orchestrator (has COKE access)
        adaptive_explainer = self._orchestrator_models.get('adaptive_explainer')
        
        if not adaptive_explainer or not adaptive_explainer.coke_graph:
            # Fallback to extraction method
            return self._extract_coke_full({}, behavioral_analysis)
        
        try:
            # Prepare student data (same as orchestrator)
            student_data = {
                "code": session_data.get("code", ""),
                "error_message": session_data.get("error_message", ""),
                "question": session_data.get("question", ""),
                "conversation": session_data.get("conversation", []),
                "concept": self._extract_concept_from_session(session_data),
                "action_sequence": session_data.get("action_sequence", []),
                "time_stuck": session_data.get("time_stuck", 0),
                "theory_of_mind": {
                    "cognitive_state": behavioral_analysis.get("emotion", "engaged") if behavioral_analysis else "engaged"
                }
            }
            
            # Predict cognitive state (same as orchestrator line 718)
            coke_cognitive_state = adaptive_explainer.coke_graph.predict_cognitive_state(student_data)
            cognitive_state_str = coke_cognitive_state.value if hasattr(coke_cognitive_state, 'value') else str(coke_cognitive_state)
            
            # Get behavioral response (same as orchestrator line 724-729)
            behavioral_response = 'ask_question'
            try:
                if hasattr(adaptive_explainer.coke_graph, 'predict_behavioral_response'):
                    behavioral_response = adaptive_explainer.coke_graph.predict_behavioral_response(coke_cognitive_state, student_data)
                    if hasattr(behavioral_response, 'value'):
                        behavioral_response = behavioral_response.value
            except:
                pass
            
            # Get cognitive chain (same as orchestrator line 735-754)
            cognitive_chain_desc = ''
            chain_id = f"chain_{cognitive_state_str}_to_{behavioral_response}"
            chain_confidence = 0.8
            chain_frequency = 0.72
            
            try:
                if hasattr(adaptive_explainer.coke_graph, 'get_cognitive_chains_for_state'):
                    chains = adaptive_explainer.coke_graph.get_cognitive_chains_for_state(coke_cognitive_state)
                    if chains:
                        chain = chains[0]
                        if hasattr(chain, 'behavioral_response'):
                            behavioral_response = chain.behavioral_response.value if hasattr(chain.behavioral_response, 'value') else str(chain.behavioral_response)
                        chain_id = chain.id if hasattr(chain, 'id') else chain_id
                        chain_confidence = chain.confidence if hasattr(chain, 'confidence') else chain_confidence
                        chain_frequency = chain.frequency if hasattr(chain, 'frequency') else chain_frequency
                        cognitive_chain_desc = f"Student is in {cognitive_state_str} state, likely to {behavioral_response}"
            except:
                cognitive_chain_desc = f"Student cognitive state: {cognitive_state_str}"
            
            theory_of_mind = {
                "why_student_went_wrong": cognitive_chain_desc or f"Student is in {cognitive_state_str} state and needs help",
                "predicted_behavior": behavioral_response,
                "cognitive_chain_used": chain_id,
                "chain_confidence": chain_confidence,
                "chain_frequency": chain_frequency,
                "mental_activity": cognitive_state_str,
                "context": "working_on_problem",
                "affective_response": behavioral_analysis.get('emotion', 'neutral') if behavioral_analysis else 'neutral'
            }
            
            return {
                "cognitive_state": cognitive_state_str,
                "mental_activity": cognitive_state_str,
                "behavioral_response": behavioral_response,
                "confidence": chain_confidence,
                "theory_of_mind": theory_of_mind,
                "source": "coke_graph"
            }
        except Exception as e:
            print(f"[WARN] COKE direct query failed: {e}")
            return self._extract_coke_full({}, behavioral_analysis)
    
    def _query_pedagogical_kg_directly(self, concept: str, session_data: Dict) -> Dict:
        """Query Pedagogical KG directly like orchestrator does in _generate_content"""
        # Get adaptive explainer from orchestrator (has Pedagogical KG access)
        adaptive_explainer = self._orchestrator_models.get('adaptive_explainer')
        
        if not adaptive_explainer or not adaptive_explainer.pedagogical_kg:
            # Fallback to extraction method
            return self._extract_pedagogical_kg_full({}, session_data)
        
        try:
            code = session_data.get('code', '')
            error_message = session_data.get('error_message', '')
            
            # Get misconceptions (same as orchestrator line 818)
            misconceptions = adaptive_explainer.pedagogical_kg.pedagogical_builder.get_misconceptions_for_concept(concept)
            
            detected_misconception = None
            related_misconceptions = []
            
            if misconceptions:
                # Get first misconception as detected
                mc = misconceptions[0]
                detected_misconception = {
                    "id": mc.id,
                    "concept": mc.concept,
                    "description": mc.description,
                    "common_indicators": mc.common_indicators,
                    "severity": mc.severity.value if hasattr(mc.severity, 'value') else str(mc.severity),
                    "frequency": mc.frequency,
                    "evidence_count": getattr(mc, 'evidence_count', 0),
                    "correction_strategy": mc.correction_strategy,
                    "confidence": 0.85
                }
                
                # Get related misconceptions
                related_misconceptions = [
                    {
                        "id": rmc.id,
                        "concept": rmc.concept,
                        "description": rmc.description,
                        "severity": rmc.severity.value if hasattr(rmc.severity, 'value') else str(rmc.severity)
                    }
                    for rmc in misconceptions[1:4]
                ]
            
            # Get cognitive load (same as orchestrator line 828)
            cognitive_load = adaptive_explainer.pedagogical_kg.get_cognitive_load_info(concept)
            cognitive_load_level = 'moderate'
            if cognitive_load:
                if isinstance(cognitive_load, dict):
                    cognitive_load_level = cognitive_load.get('level', cognitive_load.get('total_load', 'moderate'))
                else:
                    cognitive_load_level = str(cognitive_load)
            
            # Get concept full info (same as orchestrator line 815)
            concept_full_info = adaptive_explainer.pedagogical_kg.get_concept_full_info(concept)
            progression_desc = ''
            interventions = []
            if concept_full_info:
                if isinstance(concept_full_info, dict):
                    progression = concept_full_info.get('learning_progression', {})
                    if isinstance(progression, dict):
                        progression_desc = progression.get('description', progression.get('steps', ''))
                    
                    interventions_list = concept_full_info.get('interventions', [])
                    for i in interventions_list[:3]:
                        if isinstance(i, dict):
                            interventions.append(i.get('type', i.get('name', str(i))))
                        else:
                            interventions.append(str(i))
            
            return {
                "detected_misconception": detected_misconception,
                "related_misconceptions": related_misconceptions,
                "cognitive_load": cognitive_load_level,
                "learning_progression": progression_desc,
                "recommended_interventions": interventions,
                "query_source": "pedagogical_kg_builder"
            }
        except Exception as e:
            print(f"[WARN] Pedagogical KG direct query failed: {e}")
            return self._extract_pedagogical_kg_full({}, session_data)
    
    def _extract_cse_kg_full(self, knowledge_gaps: List[Dict], session_data: Dict) -> Dict:
        """Extract full CSE-KG query results with prerequisites - USING REAL CSE-KG CLIENT"""
        if not knowledge_gaps:
            # Try to extract concept from code/error
            code = session_data.get('code', '')
            error = session_data.get('error_message', '')
            question = session_data.get('question', '')
            
            # Extract concept from keywords
            text = (code + " " + error + " " + question).lower()
            concepts_to_try = ['recursion', 'array', 'function', 'loop', 'dictionary', 'string', 'variable', 'class', 'object']
            main_concept = next((c for c in concepts_to_try if c in text), 'general')
        else:
            main_concept = knowledge_gaps[0].get('concept', 'unknown')
        
        # Query REAL CSE-KG client if available
        cse_kg_client = self.models.get('cse_kg_client')
        prerequisites = []
        related_concepts = []
        definition = ""
        concept_info = {}
        
        if cse_kg_client:
            try:
                # Get concept info
                concept_info = cse_kg_client.get_concept_info(main_concept) or {}
                
                # Get prerequisites
                prereq_list = cse_kg_client.get_prerequisites(main_concept) or []
                for prereq in prereq_list[:5]:  # Top 5
                    # Check mastery from knowledge gaps
                    mastery = next((g.get('mastery', 0.5) for g in knowledge_gaps if g.get('concept') == prereq), 0.5)
                    prerequisites.append({
                        "concept": prereq,
                        "mastery": mastery,
                        "status": "mastered" if mastery > 0.7 else "partial" if mastery > 0.5 else "critical_gap"
                    })
                
                # Get related concepts
                related_list = cse_kg_client.get_related_concepts(main_concept, max_distance=1) or []
                related_concepts = [{"concept": r[0] if isinstance(r, tuple) else r, "relation": r[1] if isinstance(r, tuple) and len(r) > 1 else "relatedTo"} 
                                   for r in related_list[:5]]
                
                # Get definition
                labels = concept_info.get('labels', [])
                descriptions = concept_info.get('descriptions', [])
                if descriptions:
                    definition = descriptions[0]
                elif labels:
                    definition = f"{labels[0]} is a programming concept in computer science."
                else:
                    definition = f"{main_concept.capitalize()} is a programming concept."
            except Exception as e:
                print(f"[WARN] CSE-KG query error: {e}")
        
        # Fallback: Build from knowledge gaps
        if not prerequisites:
            for gap in knowledge_gaps[:5]:
                prerequisites.append({
                    "concept": gap.get('concept', 'unknown'),
                    "mastery": gap.get('mastery', 0.0),
                    "status": "mastered" if gap.get('mastery', 0) > 0.7 else "partial" if gap.get('mastery', 0) > 0.5 else "critical_gap"
                })
        
        if not related_concepts:
            # Default related concepts based on main concept
            related_map = {
                'recursion': ['iteration', 'functions', 'base_case', 'call_stack'],
                'array': ['list', 'indexing', 'iteration', 'loops'],
                'function': ['parameters', 'return', 'scope', 'call'],
                'loop': ['iteration', 'condition', 'range', 'while'],
                'dictionary': ['key', 'value', 'mapping', 'hash'],
                'string': ['text', 'characters', 'concatenation', 'methods'],
                'variable': ['assignment', 'scope', 'type', 'value'],
                'class': ['object', 'method', 'attribute', 'inheritance']
            }
            related_concepts = [{"concept": c, "relation": "relatedTo"} for c in related_map.get(main_concept, ['general'])]
        
        if not definition:
            definition = f"{main_concept.capitalize()} is a programming concept."
        
        return {
            "concept": main_concept,
            "concept_info": {
                "uri": concept_info.get('uri', f"cskg:{main_concept}"),
                "labels": concept_info.get('labels', [main_concept]),
                "types": concept_info.get('types', [])
            },
            "prerequisites": prerequisites,
            "related_concepts": related_concepts,
            "definition": definition,
            "query_source": "cse_kg_client" if cse_kg_client else "fallback"
        }
    
    def _format_cse_kg_from_content(self, cse_kg_info: Dict, knowledge_gaps: List[Dict]) -> Dict:
        """Format CSE-KG data from orchestrator's adaptive_analysis"""
        # cse_kg_info comes from orchestrator with structure:
        # {'concept': str, 'prerequisites': List[str], 'related_concepts': List[str], 'definition': str, 'source': str}
        
        prerequisites = []
        for prereq in cse_kg_info.get('prerequisites', []):
            # Find mastery from knowledge gaps
            mastery = next((g.get('mastery', 0.5) for g in knowledge_gaps if g.get('concept') == prereq), 0.5)
            prerequisites.append({
                "concept": prereq if isinstance(prereq, str) else prereq.get('concept', str(prereq)),
                "mastery": mastery,
                "status": "mastered" if mastery > 0.7 else "partial" if mastery > 0.5 else "critical_gap"
            })
        
        related_concepts = []
        for related in cse_kg_info.get('related_concepts', []):
            related_concepts.append({
                "concept": related if isinstance(related, str) else related[0] if isinstance(related, (list, tuple)) else str(related),
                "relation": related[1] if isinstance(related, (list, tuple)) and len(related) > 1 else "relatedTo"
            })
        
        return {
            "concept": cse_kg_info.get('concept', 'unknown'),
            "concept_info": {
                "uri": f"cskg:{cse_kg_info.get('concept', 'unknown')}",
                "labels": [cse_kg_info.get('concept', 'unknown').capitalize()],
                "types": []
            },
            "prerequisites": prerequisites,
            "related_concepts": related_concepts,
            "definition": cse_kg_info.get('definition', f"{cse_kg_info.get('concept', 'unknown').capitalize()} is a programming concept."),
            "query_source": cse_kg_info.get('source', 'cse_kg_client')
        }
    
    def _format_coke_from_content(self, coke_info: Dict, behavioral_analysis: Dict) -> Dict:
        """Format COKE data from orchestrator's adaptive_analysis"""
        # coke_info comes from orchestrator with structure:
        # {'cognitive_state': str, 'behavioral_response': str, 'cognitive_chain': Dict, 'source': str}
        
        cognitive_chain = coke_info.get('cognitive_chain', {})
        chain_desc = cognitive_chain.get('description', '') if isinstance(cognitive_chain, dict) else str(cognitive_chain)
        
        # Extract chain ID from description if possible
        chain_id = f"chain_{coke_info.get('cognitive_state', 'unknown')}_to_{coke_info.get('behavioral_response', 'unknown')}"
        
        theory_of_mind = {
            "why_student_went_wrong": chain_desc or f"Student is in {coke_info.get('cognitive_state', 'unknown')} state",
            "predicted_behavior": coke_info.get('behavioral_response', 'ask_question'),
            "cognitive_chain_used": chain_id,
            "chain_confidence": coke_info.get('confidence', 0.8),
            "chain_frequency": 0.72,  # Would be in chain data if available
            "mental_activity": coke_info.get('cognitive_state', 'unknown'),
            "context": "working_on_problem",
            "affective_response": behavioral_analysis.get('emotion', 'neutral')
        }
        
        return {
            "cognitive_state": coke_info.get('cognitive_state', 'unknown'),
            "mental_activity": coke_info.get('mental_activity', coke_info.get('cognitive_state', 'unknown')),
            "behavioral_response": coke_info.get('behavioral_response', 'ask_question'),
            "confidence": coke_info.get('confidence', 0.8),
            "theory_of_mind": theory_of_mind,
            "source": coke_info.get('source', 'coke_graph')
        }
    
    def _format_pedagogical_kg_from_content(self, pedagogical_kg_info: Dict, session_data: Dict) -> Dict:
        """Format Pedagogical KG data from orchestrator's adaptive_analysis"""
        # pedagogical_kg_info comes from orchestrator with structure:
        # {'misconceptions': List[str], 'cognitive_load': str, 'progression': str, 'interventions': List[str], 'source': str}
        
        misconceptions_list = pedagogical_kg_info.get('misconceptions', [])
        detected_misconception = None
        related_misconceptions = []
        
        if misconceptions_list:
            # Get first misconception as detected
            first_mc = misconceptions_list[0]
            if isinstance(first_mc, str):
                # Try to get full misconception object from Pedagogical KG
                pedagogical_kg = self.models.get('pedagogical_kg_builder')
                if pedagogical_kg:
                    # Extract concept from session
                    error = session_data.get('error_message', '')
                    code = session_data.get('code', '')
                    text = (code + " " + error).lower()
                    
                    concept = None
                    if "recursion" in text or "RecursionError" in error:
                        concept = "recursion"
                    elif "IndexError" in error:
                        concept = "arrays"
                    elif "KeyError" in error:
                        concept = "dictionaries"
                    elif "TypeError" in error:
                        concept = "type_system"
                    
                    if concept:
                        misconceptions = pedagogical_kg.pedagogical_builder.get_misconceptions_for_concept(concept) if hasattr(pedagogical_kg, 'pedagogical_builder') else []
                        if misconceptions:
                            mc = misconceptions[0]
                            detected_misconception = {
                                "id": mc.id,
                                "concept": mc.concept,
                                "description": mc.description,
                                "common_indicators": mc.common_indicators,
                                "severity": mc.severity.value if hasattr(mc.severity, 'value') else str(mc.severity),
                                "frequency": mc.frequency,
                                "evidence_count": getattr(mc, 'evidence_count', 0),
                                "correction_strategy": mc.correction_strategy,
                                "confidence": 0.85
                            }
                            
                            # Get related misconceptions
                            related_misconceptions = [
                                {
                                    "id": rmc.id,
                                    "concept": rmc.concept,
                                    "description": rmc.description,
                                    "severity": rmc.severity.value if hasattr(rmc.severity, 'value') else str(rmc.severity)
                                }
                                for rmc in misconceptions[1:4]
                            ]
            
            # Fallback: create from string description
            if not detected_misconception and first_mc:
                detected_misconception = {
                    "id": f"mc_{first_mc.lower().replace(' ', '_')[:30]}",
                    "concept": "general",
                    "description": first_mc,
                    "common_indicators": [],
                    "severity": "high",
                    "frequency": 0.7,
                    "evidence_count": 0,
                    "correction_strategy": "",
                    "confidence": 0.75
                }
        
        return {
            "detected_misconception": detected_misconception,
            "related_misconceptions": related_misconceptions,
            "cognitive_load": pedagogical_kg_info.get('cognitive_load', 'moderate'),
            "learning_progression": pedagogical_kg_info.get('progression', ''),
            "recommended_interventions": pedagogical_kg_info.get('interventions', []),
            "query_source": pedagogical_kg_info.get('source', 'pedagogical_kg_builder')
        }
    
    def _save_graphs_after_turn(self, student_id: str, cognitive_assessment: Dict, 
                                 knowledge_gaps: List[Dict], session_data: Dict):
        """
        Save student graph and pedagogical graph after each turn
        Ensures graphs are updated with conversation data
        """
        try:
            # 1. Save student graph (via state tracker)
            if hasattr(self.orchestrator, 'state_tracker') and self.orchestrator.state_tracker:
                # The state tracker should already be updated by orchestrator
                # But we explicitly save it here to ensure persistence
                self.orchestrator.state_tracker._save_states()
                print(f"[Turn] ✅ Student graph saved for {student_id}")
            
            # 2. Ensure pedagogical graph misconceptions are saved
            # The orchestrator's _learn_from_session already calls learn_from_session
            # which saves misconceptions, but we verify it's saved
            adaptive_explainer = self.orchestrator.models.get('adaptive_explainer')
            if adaptive_explainer and hasattr(adaptive_explainer, 'pedagogical_kg'):
                pedagogical_kg = adaptive_explainer.pedagogical_kg
                if hasattr(pedagogical_kg, 'pedagogical_builder'):
                    pedagogical_builder = pedagogical_kg.pedagogical_builder
                    # Force save misconceptions
                    if hasattr(pedagogical_builder, '_save_misconceptions'):
                        pedagogical_builder._save_misconceptions()
                        print(f"[Turn] ✅ Pedagogical graph misconceptions saved")
            
            # 3. Update student graph with concepts from this turn
            concepts_from_turn = []
            for gap in knowledge_gaps:
                concept = gap.get('concept')
                if concept:
                    concepts_from_turn.append(concept)
            
            # Extract concept from session if not in gaps
            if not concepts_from_turn:
                concept = self._extract_concept_from_session(session_data)
                if concept:
                    concepts_from_turn.append(concept)
            
            # Update student state with concepts encountered
            if concepts_from_turn and hasattr(self.orchestrator, 'state_tracker') and self.orchestrator.state_tracker:
                state = self.orchestrator.state_tracker.get_student_state(student_id)
                knowledge_state = state.get('knowledge_state', {})
                concept_mastery = knowledge_state.get('concept_mastery', {})
                
                # Add new concepts if not present
                for concept in concepts_from_turn:
                    if concept not in concept_mastery:
                        concept_mastery[concept] = 0.5  # Initialize with moderate mastery
                
                # Save updated state
                self.orchestrator.state_tracker._save_states()
                
        except Exception as e:
            print(f"[WARN] Error saving graphs after turn: {e}")
            import traceback
            traceback.print_exc()
    
    def _extract_student_graph_full(self, student_id: str, cognitive: Dict, knowledge_gaps: List[Dict]) -> Dict:
        """Extract full Student Graph data (personal knowledge state, mastery, learning history)"""
        # Get student state from orchestrator's state tracker
        state_tracker = getattr(self.orchestrator, 'state_tracker', None)
        
        if state_tracker:
            try:
                student_state = state_tracker.get_student_state(student_id)
                knowledge_state = student_state.get('knowledge_state', {})
                concept_mastery = knowledge_state.get('concept_mastery', {})
                mastery_history = knowledge_state.get('mastery_history', [])
                cognitive_state = student_state.get('cognitive_state', {})
                
                # Build concept activations from mastery levels
                concept_activations = {
                    concept: mastery for concept, mastery in concept_mastery.items()
                }
                
                # Get learning progress
                total_interactions = student_state.get('total_interactions', 0)
                session_count = student_state.get('session_count', 0)
                
                # Identify mastered vs weak concepts (ensure mastery is numeric)
                mastered_concepts = [
                    concept for concept, mastery in concept_mastery.items() 
                    if isinstance(mastery, (int, float)) and mastery >= 0.7
                ]
                weak_concepts = [
                    concept for concept, mastery in concept_mastery.items() 
                    if isinstance(mastery, (int, float)) and mastery < 0.5
                ]
                
                # Get learning trajectory
                learning_trajectory = "improving" if mastery_history and len(mastery_history) > 1 and mastery_history[-1] > mastery_history[0] else "stable"
                
                return {
                    "student_id": student_id,
                    "concept_mastery": concept_mastery,
                    "concept_activations": concept_activations,
                    "mastered_concepts": mastered_concepts,
                    "weak_concepts": weak_concepts,
                    "knowledge_gaps": [
                        {
                            "concept": gap.get('concept', ''),
                            "mastery": gap.get('mastery', 0.0),
                            "severity": gap.get('severity', 'medium'),
                            "is_prerequisite_for": gap.get('is_prerequisite_for', '')
                        }
                        for gap in knowledge_gaps
                    ],
                    "learning_history": {
                        "total_interactions": total_interactions,
                        "session_count": session_count,
                        "mastery_history": mastery_history[-10:] if mastery_history else [],  # Last 10
                        "learning_trajectory": learning_trajectory
                    },
                    "cognitive_state_history": cognitive_state.get('state_history', [])[-5:],  # Last 5 states
                    "current_cognitive_state": cognitive_state.get('current_state', 'engaged'),
                    "source": "student_state_tracker"
                }
            except Exception as e:
                print(f"[WARN] Student Graph extraction error: {e}")
        
        # Fallback: Build from current session data
        concept_mastery = {}
        for gap in knowledge_gaps:
            concept = gap.get('concept', '')
            mastery = gap.get('mastery', 0.5)
            # Ensure mastery is numeric
            if isinstance(mastery, dict):
                mastery = mastery.get('value', mastery.get('mastery', 0.5))
            if not isinstance(mastery, (int, float)):
                mastery = 0.5
            concept_mastery[concept] = float(mastery)
        
        return {
            "student_id": student_id,
            "concept_mastery": concept_mastery,
            "concept_activations": concept_mastery,
            "mastered_concepts": [c for c, m in concept_mastery.items() if isinstance(m, (int, float)) and m >= 0.7],
            "weak_concepts": [c for c, m in concept_mastery.items() if isinstance(m, (int, float)) and m < 0.5],
            "knowledge_gaps": [
                {
                    "concept": gap.get('concept', ''),
                    "mastery": gap.get('mastery', 0.0),
                    "severity": gap.get('severity', 'medium')
                }
                for gap in knowledge_gaps
            ],
            "learning_history": {
                "total_interactions": 1,
                "session_count": 1,
                "mastery_history": [],
                "learning_trajectory": "initial"
            },
            "source": "fallback"
        }
    
    def _calculate_dynamic_dina_metrics(
        self, 
        student_id: str, 
        cognitive_assessment: Dict, 
        knowledge_gaps: List[Dict],
        metrics: Dict,
        previous_overall_mastery: float,
        previous_mastery: Dict
    ) -> Dict:
        """
        Calculate dynamic DINA metrics based on actual student performance
        Updates mastery based on code correctness, errors, and concept understanding
        """
        # Get current student state
        state_tracker = getattr(self.orchestrator, 'state_tracker', None)
        student_state = {}
        if state_tracker:
            student_state = state_tracker.get_student_state(student_id)
        
        knowledge_state = student_state.get('knowledge_state', {})
        concept_mastery = knowledge_state.get('concept_mastery', {})
        
        # Calculate overall mastery from concept mastery
        if concept_mastery:
            # Ensure all values are floats
            mastery_values = []
            for v in concept_mastery.values():
                if isinstance(v, dict):
                    mastery_values.append(float(v.get('mastery', v.get('value', 0.5))))
                elif isinstance(v, list):
                    mastery_values.append(float(v[0]) if len(v) > 0 else 0.5)
                else:
                    mastery_values.append(float(v) if v is not None else 0.5)
            overall_mastery = sum(mastery_values) / len(mastery_values) if mastery_values else 0.5
        else:
            # Calculate from knowledge gaps
            if knowledge_gaps:
                gap_masteries = []
                for gap in knowledge_gaps:
                    mastery_raw = gap.get('mastery', 0.5)
                    # Ensure mastery is a float
                    if isinstance(mastery_raw, dict):
                        gap_masteries.append(float(mastery_raw.get('mastery', mastery_raw.get('value', 0.5))))
                    elif isinstance(mastery_raw, list):
                        gap_masteries.append(float(mastery_raw[0]) if len(mastery_raw) > 0 else 0.5)
                    else:
                        gap_masteries.append(float(mastery_raw) if mastery_raw is not None else 0.5)
                overall_mastery = sum(gap_masteries) / len(gap_masteries) if gap_masteries else 0.5
            else:
                overall_mastery = previous_overall_mastery
        
        # Calculate mastery delta
        mastery_delta = overall_mastery - previous_overall_mastery
        
        # Adjust based on code correctness
        quantitative = metrics.get('quantitative', {})
        codebert = quantitative.get('codebert_analysis', {})
        correctness = codebert.get('correctness_score', 0.5) if codebert else 0.5
        
        # If code is correct, increase mastery slightly
        # If code has errors, decrease mastery slightly
        if correctness > 0.8:
            mastery_delta += 0.05  # Good performance
        elif correctness < 0.5:
            mastery_delta -= 0.05  # Poor performance
        
        # Adjust based on errors encountered
        error_message = metrics.get('error_message', '')
        if error_message:
            # Errors indicate misunderstanding, reduce mastery
            mastery_delta -= 0.03
        
        # Calculate concept-specific mastery
        concept_specific_mastery = {}
        for gap in knowledge_gaps:
            concept = gap.get('concept', '')
            if concept:
                gap_mastery = gap.get('mastery', 0.5)
                # Ensure gap_mastery is a float
                if isinstance(gap_mastery, dict):
                    gap_mastery = gap_mastery.get('mastery', gap_mastery.get('value', 0.5))
                elif isinstance(gap_mastery, list):
                    gap_mastery = float(gap_mastery[0]) if len(gap_mastery) > 0 else 0.5
                else:
                    gap_mastery = float(gap_mastery) if gap_mastery is not None else 0.5
                
                # Update based on previous mastery
                prev_concept_mastery_raw = previous_mastery.get(concept, gap_mastery)
                # Ensure prev_concept_mastery is a float
                if isinstance(prev_concept_mastery_raw, dict):
                    prev_concept_mastery = prev_concept_mastery_raw.get('mastery', prev_concept_mastery_raw.get('value', gap_mastery))
                elif isinstance(prev_concept_mastery_raw, list):
                    prev_concept_mastery = float(prev_concept_mastery_raw[0]) if len(prev_concept_mastery_raw) > 0 else gap_mastery
                else:
                    prev_concept_mastery = float(prev_concept_mastery_raw) if prev_concept_mastery_raw is not None else gap_mastery
                
                # Adjust based on correctness
                if correctness > 0.8:
                    concept_mastery_value = min(1.0, prev_concept_mastery + 0.1)
                elif correctness < 0.5:
                    concept_mastery_value = max(0.0, prev_concept_mastery - 0.1)
                else:
                    concept_mastery_value = prev_concept_mastery + (gap_mastery - prev_concept_mastery) * 0.3
                concept_specific_mastery[concept] = max(0.0, min(1.0, concept_mastery_value))
        
        # If no knowledge gaps, use concept mastery from state
        if not concept_specific_mastery and concept_mastery:
            concept_specific_mastery = concept_mastery.copy()
        
        # Identify strong and weak areas
        strong_areas = [c for c, m in concept_specific_mastery.items() if m >= 0.7]
        weak_areas = [c for c, m in concept_specific_mastery.items() if m < 0.5]
        
        return {
            'overall_mastery': max(0.0, min(1.0, overall_mastery + mastery_delta)),
            'concept_specific_mastery': concept_specific_mastery,
            'strong_areas': strong_areas,
            'weak_areas': weak_areas,
            'mastery_delta': mastery_delta
        }
    
    def _extract_learned_misconceptions_from_turn(self, session_data: Dict, analysis: Dict, cognitive_assessment: Dict) -> List[Dict]:
        """
        Extract misconceptions that were learned from this specific turn
        Based on the student's error, code, and question
        INFERS from the conversation what misconception was learned
        """
        learned_misconceptions = []
        
        try:
            error_message = session_data.get('error_message', '')
            code = session_data.get('code', '')
            question = session_data.get('question', '')
            
            # Extract concept and error type from student input
            concept = None
            error_type = None
            
            if error_message:
                # Map errors to concepts
                if "RecursionError" in error_message:
                    concept = "recursion"
                    error_type = "RecursionError"
                elif "IndexError" in error_message:
                    concept = "arrays"
                    error_type = "IndexError"
                elif "KeyError" in error_message:
                    concept = "dictionaries"
                    error_type = "KeyError"
                elif "TypeError" in error_message:
                    concept = "type_system"
                    error_type = "TypeError"
                elif "UnboundLocalError" in error_message or "NameError" in error_message:
                    concept = "variable_scope"
                    error_type = "UnboundLocalError" if "UnboundLocalError" in error_message else "NameError"
                elif "AttributeError" in error_message:
                    concept = "object_oriented"
                    error_type = "AttributeError"
                elif "ValueError" in error_message:
                    concept = "type_system"
                    error_type = "ValueError"
            
            # Also extract from code/question if no error
            if not concept:
                text = (code + " " + question).lower()
                if "recursion" in text or "recursive" in text:
                    concept = "recursion"
                elif "array" in text or "list" in text or "index" in text:
                    concept = "arrays"
                elif "dictionary" in text or "dict" in text:
                    concept = "dictionaries"
                elif "class" in text or "__init__" in text or "self" in text:
                    concept = "object_oriented"
                elif "function" in text or "def" in code:
                    concept = "functions"
                elif "variable" in text or "scope" in text:
                    concept = "variable_scope"
            
            # Get the pedagogical KG builder to find the actual learned misconception
            adaptive_explainer = self.orchestrator.models.get('adaptive_explainer')
            if adaptive_explainer and hasattr(adaptive_explainer, 'pedagogical_kg'):
                pedagogical_kg = adaptive_explainer.pedagogical_kg
                if hasattr(pedagogical_kg, 'pedagogical_builder'):
                    pedagogical_builder = pedagogical_kg.pedagogical_builder
                    
                    # If we have a concept, try to find the learned misconception
                    if concept:
                        # Get misconceptions for this concept
                        misconceptions = pedagogical_builder.get_misconceptions_for_concept(concept)
                        
                        # Find the most relevant one based on error type
                        matched_mc = None
                        if error_type:
                            # Look for misconception matching error type
                            for mc in misconceptions:
                                mc_id = mc.id if hasattr(mc, 'id') else str(mc)
                                # Check if error type is in the misconception ID or indicators
                                if error_type.lower() in mc_id.lower():
                                    matched_mc = mc
                                    break
                                # Also check common indicators
                                if hasattr(mc, 'common_indicators'):
                                    for indicator in mc.common_indicators:
                                        if error_type.lower() in str(indicator).lower():
                                            matched_mc = mc
                                            break
                                    if matched_mc:
                                        break
                        
                        # If no match by error type, get the most recent/frequent one
                        if not matched_mc and misconceptions:
                            # Get misconception with highest frequency (most learned)
                            matched_mc = max(misconceptions, key=lambda mc: mc.frequency if hasattr(mc, 'frequency') else 0.1)
                        
                        # Format the learned misconception
                        if matched_mc:
                            mc_id = matched_mc.id if hasattr(matched_mc, 'id') else f"mc_{concept}_general"
                            learned_misconceptions.append({
                                "id": mc_id,
                                "concept": concept,
                                "description": matched_mc.description if hasattr(matched_mc, 'description') else f"Common {concept} misconception",
                                "error_type": error_type or "N/A",
                                "severity": matched_mc.severity.value if hasattr(matched_mc, 'severity') and hasattr(matched_mc.severity, 'value') else str(matched_mc.severity) if hasattr(matched_mc, 'severity') else "medium",
                                "frequency": matched_mc.frequency if hasattr(matched_mc, 'frequency') else 0.1,
                                "common_indicators": matched_mc.common_indicators if hasattr(matched_mc, 'common_indicators') else [error_type] if error_type else [],
                                "correction_strategy": matched_mc.correction_strategy if hasattr(matched_mc, 'correction_strategy') else f"Review {concept} fundamentals",
                                "learned_from": {
                                    "error_message": error_message[:100] if error_message else None,
                                    "code_snippet": code[:100] if code else None,
                                    "question": question[:100] if question else None,
                                    "turn_context": f"Student encountered {error_type or 'an issue'} while working on {concept}"
                                }
                            })
            
            # If no misconception found but we have error/concept, create inferred one
            if not learned_misconceptions and (error_type or concept):
                learned_misconceptions.append({
                    "id": f"mc_{concept or 'general'}_{error_type.lower().replace('error', '') if error_type else 'general'}",
                    "concept": concept or "general",
                    "description": f"Common {concept or 'programming'} misconception related to {error_type or 'code patterns'}" if error_type or concept else "General programming misconception",
                    "error_type": error_type or "N/A",
                    "severity": "high" if error_type in ["RecursionError", "IndexError"] else "medium",
                    "frequency": 0.1,
                    "common_indicators": [error_type] if error_type else [],
                    "correction_strategy": f"Review {concept or 'programming'} fundamentals and common {error_type or 'error'} patterns" if error_type or concept else "Review programming fundamentals",
                    "learned_from": {
                        "error_message": error_message[:100] if error_message else None,
                        "code_snippet": code[:100] if code else None,
                        "question": question[:100] if question else None,
                        "turn_context": f"Student encountered {error_type or 'an issue'} while working on {concept or 'programming'}"
                    }
                })
            
        except Exception as e:
            print(f"[WARN] Error extracting learned misconceptions: {e}")
            import traceback
            traceback.print_exc()
        
        return learned_misconceptions
    
    def _extract_pedagogical_kg_full(self, cognitive: Dict, session_data: Dict) -> Dict:
        """Extract full Pedagogical KG with misconceptions - USING REAL PEDAGOGICAL KG"""
        error_message = session_data.get('error_message', '')
        code = session_data.get('code', '')
        question = session_data.get('question', '')
        
        # Get REAL Pedagogical KG if available
        pedagogical_kg = self.models.get('pedagogical_kg_builder')
        detected_misconception = None
        related_misconceptions = []
        
        if pedagogical_kg:
            try:
                # Extract concept from code/error
                text = (code + " " + error_message + " " + question).lower()
                concepts_to_check = []
                
                # Map errors to concepts
                if "recursion" in text or "RecursionError" in error_message:
                    concepts_to_check.append("recursion")
                if "IndexError" in error_message or "index" in text:
                    concepts_to_check.append("arrays")
                if "KeyError" in error_message or "dictionary" in text:
                    concepts_to_check.append("dictionaries")
                if "TypeError" in error_message:
                    concepts_to_check.append("type_system")
                if "UnboundLocalError" in error_message or "NameError" in error_message or "scope" in text:
                    concepts_to_check.append("variable_scope")
                if "function" in text or "def" in code:
                    concepts_to_check.append("functions")
                
                # Default to general if no specific concept
                if not concepts_to_check:
                    concepts_to_check = ["general"]
                
                # Detect misconceptions for each concept
                for concept in concepts_to_check[:2]:  # Check top 2 concepts
                    misconceptions = pedagogical_kg.detect_misconception(concept, code, error_message)
                    
                    if misconceptions and not detected_misconception:
                        # Get the first (most likely) misconception
                        mc = misconceptions[0]
                        detected_misconception = {
                            "id": mc.id,
                            "concept": mc.concept,
                            "description": mc.description,
                            "common_indicators": mc.common_indicators,
                            "severity": mc.severity.value if hasattr(mc.severity, 'value') else str(mc.severity),
                            "frequency": mc.frequency,
                            "evidence_count": getattr(mc, 'evidence_count', 0),
                            "correction_strategy": mc.correction_strategy,
                            "confidence": 0.85  # High confidence from Pedagogical KG
                        }
                        
                        # Get related misconceptions
                        related = pedagogical_kg.pedagogical_builder.get_misconceptions_for_concept(concept) if hasattr(pedagogical_kg, 'pedagogical_builder') else []
                        related_misconceptions = [
                            {
                                "id": rmc.id,
                                "concept": rmc.concept,
                                "description": rmc.description,
                                "severity": rmc.severity.value if hasattr(rmc.severity, 'value') else str(rmc.severity)
                            }
                            for rmc in related[1:4]  # Get 3 related
                        ]
                        break
            except Exception as e:
                print(f"[WARN] Pedagogical KG extraction error: {e}")
        
        # Fallback: Detect from error message
        if not detected_misconception:
            if "RecursionError" in error_message:
                detected_misconception = {
                    "id": "mc_recursion_no_base_case",
                    "concept": "recursion",
                    "description": "Believes recursion doesn't need a base case",
                    "common_indicators": ["infinite recursion", "RecursionError", "missing if statement before recursive call"],
                    "severity": "critical",
                    "frequency": 0.78,
                    "evidence_count": 1247,
                    "correction_strategy": "Explain base case necessity with examples",
                    "confidence": 0.92
                }
            elif "IndexError" in error_message:
                detected_misconception = {
                    "id": "mc_off_by_one",
                    "concept": "arrays",
                    "description": "Off-by-one errors in array access",
                    "severity": "high",
                    "frequency": 0.8,
                    "confidence": 0.85
                }
            elif "KeyError" in error_message:
                detected_misconception = {
                    "id": "mc_dictionaries_keyerror",
                    "concept": "dictionaries",
                    "description": "Accessing dictionary keys without checking existence",
                    "severity": "high",
                    "frequency": 0.75,
                    "confidence": 0.80
                }
            elif "TypeError" in error_message:
                detected_misconception = {
                    "id": "mc_type_system_typeerror",
                    "concept": "type_system",
                    "description": "Confuses type compatibility and operations",
                    "severity": "high",
                    "frequency": 0.7,
                    "confidence": 0.80
                }
        
        return {
            "detected_misconception": detected_misconception,
            "related_misconceptions": related_misconceptions,
            "query_source": "pedagogical_kg_builder" if pedagogical_kg else "fallback"
        }
    
    def _extract_coke_data(self, analysis: Dict) -> Dict:
        """Extract COKE graph data"""
        # COKE data might be in cognitive assessment
        cognitive = analysis.get('cognitive', {})
        return {
            "cognitive_state": cognitive.get('cognitive_state', 'unknown'),
            "theory_of_mind": cognitive.get('theory_of_mind', {})
        }
    
    def _extract_cse_kg_data(self, knowledge_gaps: List[Dict]) -> Dict:
        """Extract CSE-KG query results"""
        if not knowledge_gaps:
            return {}
        
        # Get concepts from knowledge gaps
        concepts = [gap.get('concept') for gap in knowledge_gaps if gap.get('concept')]
        
        return {
            "concepts_queried": concepts,
            "prerequisites_found": len([g for g in knowledge_gaps if g.get('is_prerequisite_for')]),
            "related_concepts": []
        }
    
    def _extract_pedagogical_kg_data(self, analysis: Dict) -> Dict:
        """Extract Pedagogical KG data"""
        # Misconceptions might be in cognitive or separate field
        cognitive = analysis.get('cognitive', {})
        return {
            "misconceptions_detected": cognitive.get('misconceptions', []),
            "learning_progressions": []
        }
    
    def _generate_summary(self, conversation: Dict) -> Dict:
        """Generate conversation summary"""
        turns = conversation.get('turns', [])
        
        if not turns:
            return {}
        
        # Extract key metrics across turns
        all_concepts = set()
        all_emotions = []
        mastery_progression = []
        
        for turn in turns:
            # Concepts
            gaps = turn.get('system_analysis', {}).get('knowledge_gaps', [])
            for gap in gaps:
                if gap.get('concept'):
                    all_concepts.add(gap['concept'])
            
            # Emotions
            behavioral = turn.get('system_analysis', {}).get('behavioral_analysis', {})
            if behavioral.get('emotion'):
                all_emotions.append(behavioral['emotion'])
            
            # Mastery
            cognitive = turn.get('system_analysis', {}).get('cognitive_assessment', {})
            mastery_profile = cognitive.get('mastery_profile', {})
            if mastery_profile.get('overall_mastery') is not None:
                mastery_progression.append(mastery_profile['overall_mastery'])
        
        return {
            "total_turns": len(turns),
            "concepts_covered": list(all_concepts),
            "emotion_progression": all_emotions,
            "mastery_progression": mastery_progression,
            "final_mastery": mastery_progression[-1] if mastery_progression else None
        }


def main():
    """Example: Generate multi-turn conversation"""
    
    # Example conversation turns
    conversation_turns = [
        {
            "turn_number": 1,
            "code": """def factorial(n):
    return n * factorial(n - 1)

print(factorial(5))""",
            "error_message": "RecursionError: maximum recursion depth exceeded",
            "question": "Why is my code giving me a RecursionError? Can you show me a diagram of what's happening?",
            "action_sequence": ["code_edit", "run_test", "run_test", "run_test", "search_documentation", "code_edit", "run_test"],
            "time_deltas": [15.0, 2.0, 3.0, 2.5, 45.0, 20.0, 2.0],
            "time_stuck": 89.5
        },
        {
            "turn_number": 2,
            "code": """def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))""",
            "error_message": "",
            "question": "Great! It works now. But can you explain why we need the base case? What happens if we don't have it?",
            "action_sequence": ["code_edit", "run_test"],
            "time_deltas": [30.0, 2.0],
            "time_stuck": 0.0
        },
        {
            "turn_number": 3,
            "code": """def fibonacci(n):
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))""",
            "error_message": "RecursionError: maximum recursion depth exceeded",
            "question": "I'm trying to write a Fibonacci function but getting the same error. What am I missing?",
            "action_sequence": ["code_edit", "run_test", "run_test", "code_edit", "run_test"],
            "time_deltas": [20.0, 2.0, 3.0, 25.0, 2.0],
            "time_stuck": 52.0
        }
    ]
    
    # Initialize generator
    generator = MultiTurnConversationGenerator()
    
    # Generate conversation
    output = generator.generate_conversation(
        student_id="student_multi_turn_001",
        conversation_turns=conversation_turns,
        output_file="output/multi_turn_conversation_output"
    )
    
    # Print summary
    print("\n" + "=" * 80)
    print("CONVERSATION SUMMARY")
    print("=" * 80)
    summary = output.get('summary', {})
    print(f"Total Turns: {summary.get('total_turns', 0)}")
    print(f"Concepts Covered: {', '.join(summary.get('concepts_covered', []))}")
    print(f"Final Mastery: {summary.get('final_mastery', 0):.2%}" if summary.get('final_mastery') else "N/A")
    
    return output


if __name__ == "__main__":
    output = main()

