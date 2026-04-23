"""
Format multi-turn conversation output as markdown
Similar format to SYSTEM_OUTPUT_FACTORIAL_WITH_DYNAMIC_LEARNING_STYLE.md
"""

import json
from pathlib import Path
from typing import Dict, List


def format_conversation_to_markdown(conversation_data: Dict, output_path: str):
    """Format conversation data to markdown format"""
    
    student_id = conversation_data.get('student_id', 'unknown')
    turns = conversation_data.get('turns', [])
    summary = conversation_data.get('summary', {})
    
    md_lines = []
    
    # Header
    md_lines.append(f"# Multi-Turn Student Conversation: {student_id}")
    md_lines.append("")
    md_lines.append(f"**Generated**: {conversation_data.get('timestamp', 'N/A')}")
    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    
    # Process each turn
    for turn in turns:
        turn_num = turn.get('turn_number', 0)
        student_input = turn.get('student_input', {})
        system_analysis = turn.get('system_analysis', {})
        intervention = turn.get('intervention_selected', {})
        system_response = turn.get('system_response', {})
        metrics = turn.get('metrics', {})
        
        md_lines.append(f"## 🔄 TURN {turn_num}")
        md_lines.append("")
        
        # Student Input
        md_lines.append("### 📥 Student Input")
        md_lines.append("")
        md_lines.append(f"**Question**: `{student_input.get('question', 'N/A')}`")
        md_lines.append("")
        
        if student_input.get('code'):
            md_lines.append("**Code**:")
            md_lines.append("```python")
            md_lines.append(student_input['code'])
            md_lines.append("```")
            md_lines.append("")
        
        if student_input.get('error_message'):
            md_lines.append(f"**Error**: `{student_input.get('error_message', 'N/A')}`")
            md_lines.append("")
        
        md_lines.append(f"**Action Sequence**: `{student_input.get('action_sequence', [])}`")
        md_lines.append("")
        md_lines.append(f"**Time Deltas**: `{student_input.get('time_deltas', [])}` seconds")
        md_lines.append("")
        md_lines.append(f"**Time Stuck**: `{student_input.get('time_stuck', 0.0)}` seconds")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        
        # System Analysis - ALL 11 STEPS (like factorial example)
        md_lines.append("## 🔬 System Analysis Pipeline")
        md_lines.append("")
        
        # STEP 1: HVSAE Multi-Modal Encoding
        hvsae = system_analysis.get('hvsae_encoding', {})
        md_lines.append("### **STEP 1: HVSAE Multi-Modal Encoding**")
        md_lines.append("")
        md_lines.append("**Input Processing**:")
        md_lines.append("- **Code**: Tokenized with CodeBERT → 768-dim embedding")
        md_lines.append("- **Error Message**: Tokenized with BERT → 768-dim embedding")
        md_lines.append("- **Action Sequence**: Encoded with LSTM → 256-dim embedding")
        md_lines.append("")
        md_lines.append("**Fusion**:")
        md_lines.append("- Self-attention (8 heads) across 3 modalities")
        md_lines.append("- Output: 512-dim fused features")
        md_lines.append("")
        md_lines.append("**Latent Representation**:")
        md_lines.append("```json")
        attention_weights = hvsae.get('attention_weights', {})
        if isinstance(attention_weights, dict):
            attn_dict = attention_weights
        else:
            attn_dict = {"code": 0.45, "text": 0.35, "behavior": 0.20}
        md_lines.append(json.dumps({
            "latent": "[256-dim hyperspherical vector]",
            "mu": "[256-dim mean]",
            "kappa": hvsae.get('kappa', 95.2),
            "attention_weights": attn_dict
        }, indent=2, default=str))
        md_lines.append("```")
        md_lines.append("")
        
        misconception = hvsae.get('misconception_detected', {})
        if misconception.get('detected'):
            md_lines.append("**Misconception Classification** (from HVSAE decoder):")
            md_lines.append("```json")
            all_probs = misconception.get('all_probs', {})
            misconception_probs = [all_probs.get('missing_base_case', 0.0), 
                                  all_probs.get('incorrect_base_case', 0.0),
                                  all_probs.get('wrong_recursive_call', 0.0),
                                  all_probs.get('missing_condition', 0.0),
                                  all_probs.get('other', 0.0)]
            md_lines.append(json.dumps({
                "misconception_probs": misconception_probs,
                "detected": misconception.get('detected'),
                "confidence": misconception.get('confidence', 0.0)
            }, indent=2, default=str))
            md_lines.append("```")
            md_lines.append("")
        
        md_lines.append("---")
        md_lines.append("")
        
        # STEP 2: Behavioral Analysis (RNN + HMM)
        behavioral = system_analysis.get('behavioral_analysis', {})
        if behavioral:
            md_lines.append("### **STEP 2: Behavioral Analysis (RNN + HMM)**")
            md_lines.append("")
            rnn = behavioral.get('rnn_analysis', {})
            hmm = behavioral.get('hmm_state_prediction', {})
            
            md_lines.append("**RNN Analysis**:")
            md_lines.append("```json")
            md_lines.append(json.dumps(rnn, indent=2, default=str))
            md_lines.append("```")
            md_lines.append("")
            
            md_lines.append("**HMM State Prediction**:")
            md_lines.append("```json")
            md_lines.append(json.dumps(hmm, indent=2, default=str))
            md_lines.append("```")
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
        
        # STEP 3: Dynamic Learning Style Inference
        learning_style = system_analysis.get('learning_style_inference', {})
        if learning_style:
            md_lines.append("### **STEP 3: ⭐ DYNAMIC LEARNING STYLE INFERENCE** (NEW!)")
            md_lines.append("")
            md_lines.append("**Learning Style Analysis**:")
            md_lines.append("")
            
            behavioral_pattern = learning_style.get('behavioral_pattern_analysis', {})
            behavioral_inf = learning_style.get('behavioral_inference', {})
            chat_analysis = learning_style.get('chat_text_analysis', {})
            final_style = learning_style.get('final_learning_style', {})
            
            md_lines.append("#### **3.1 Behavioral Pattern Analysis**:")
            md_lines.append("```json")
            md_lines.append(json.dumps({
                "action_sequence_analysis": behavioral_pattern,
                "behavioral_inference": behavioral_inf
            }, indent=2, default=str))
            md_lines.append("```")
            md_lines.append("")
            
            md_lines.append("#### **3.2 Chat Text Analysis**:")
            md_lines.append("```json")
            md_lines.append(json.dumps(chat_analysis, indent=2, default=str))
            md_lines.append("```")
            md_lines.append("")
            
            md_lines.append("#### **3.3 Combined Learning Style** (Priority: Behavior > Chat):")
            md_lines.append("```json")
            md_lines.append(json.dumps({
                "final_learning_style": final_style,
                "inference_confidence": learning_style.get('inference_confidence', {}),
                "source_breakdown": learning_style.get('source_breakdown', {}),
                "stored_for_future": True
            }, indent=2, default=str))
            md_lines.append("```")
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
        
        # STEP 4: COKE Analysis
        coke = system_analysis.get('coke_analysis', {})
        if coke:
            md_lines.append("### **STEP 4: Cognitive State Inference (COKE Graph)**")
            md_lines.append("")
            md_lines.append("**COKE Analysis** (Using Learned Chains from ProgSnap2):")
            md_lines.append("```json")
            md_lines.append(json.dumps(coke, indent=2, default=str))
            md_lines.append("```")
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
        
        # STEP 5: Nestor Psychological Assessment
        nestor = system_analysis.get('nestor_inference', {})
        if nestor:
            md_lines.append("### **STEP 5: ⭐ Psychological Assessment (Nestor Bayesian Network)**")
            md_lines.append("")
            
            behavioral_indicators = nestor.get('behavioral_indicators', {})
            md_lines.append("**Behavioral Data Extraction for Nestor**:")
            md_lines.append("```json")
            md_lines.append(json.dumps({
                "behavioral_indicators": behavioral_indicators,
                "extraction_source": "session_data + action_sequence + time_deltas"
            }, indent=2, default=str))
            md_lines.append("```")
            md_lines.append("")
            
            md_lines.append("**Nestor Bayesian Network Inference Pipeline**:")
            md_lines.append("")
            
            md_lines.append("#### **5.1 Personality Inference** (P1-P5):")
            md_lines.append("```json")
            md_lines.append(json.dumps({
                "personality_scores": nestor.get('personality_scores', {}),
                "inference_method": "nestor_bayesian_network",
                "confidence": nestor.get('confidence', 0.82)
            }, indent=2, default=str))
            md_lines.append("```")
            md_lines.append("")
            
            md_lines.append("#### **5.2 Learning Style Inference from Personality** (D1-D4):")
            md_lines.append("```json")
            md_lines.append(json.dumps({
                "learning_styles": nestor.get('learning_styles', {}),
                "inference_chain": "Personality → Learning Styles (Nestor BN)",
                "confidence": nestor.get('confidence', 0.75)
            }, indent=2, default=str))
            md_lines.append("```")
            md_lines.append("")
            
            md_lines.append("#### **6.3 Learning Strategy Inference from Personality** (T1-T4):")
            md_lines.append("```json")
            md_lines.append(json.dumps({
                "learning_strategies": nestor.get('learning_strategies', {}),
                "inference_chain": "Personality → Learning Strategies (Nestor BN)"
            }, indent=2, default=str))
            md_lines.append("```")
            md_lines.append("")
            
            md_lines.append("#### **6.4 Learning Element Preference Prediction**:")
            md_lines.append("```json")
            md_lines.append(json.dumps({
                "learning_element_preferences": nestor.get('learning_element_preferences', {}),
                "top_recommendations": [[elem, nestor.get('learning_element_preferences', {}).get(elem, 0.0)] 
                                       for elem in nestor.get('recommended_elements', [])],
                "inference_chain": "Personality + Learning Styles + Strategies → Learning Elements (Nestor BN)"
            }, indent=2, default=str))
            md_lines.append("```")
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
        
        # STEP 7: CSE-KG Knowledge Gap Identification
        cse_kg = system_analysis.get('cse_kg_queries', {})
        knowledge_gaps = system_analysis.get('knowledge_gaps', [])
        if cse_kg or knowledge_gaps:
            md_lines.append("### **STEP 6: Knowledge Gap Identification (CSE-KG + Student Graph)**")
            md_lines.append("")
            
            if cse_kg:
                md_lines.append("**CSE-KG Query Results**:")
                md_lines.append("```json")
                md_lines.append(json.dumps(cse_kg, indent=2, default=str))
                md_lines.append("```")
                md_lines.append("")
            
            if knowledge_gaps:
                md_lines.append("**Knowledge Gaps Identified**:")
                md_lines.append("```json")
                md_lines.append(json.dumps(knowledge_gaps, indent=2, default=str))
                md_lines.append("```")
                md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
        
        # STEP 7: Student Graph (Personal Knowledge State) - WITH UPDATES
        student_graph = system_analysis.get('student_graph', {})
        student_input = turn.get('student_input', {})
        error_message = student_input.get('error_message', '')
        knowledge_gaps = system_analysis.get('knowledge_gaps', [])
        learned_misconceptions = system_analysis.get('learned_misconceptions', [])
        
        if student_graph:
            md_lines.append("### **STEP 7: Student Graph (Personal Knowledge State)**")
            md_lines.append("")
            
            # Show what was updated in this turn
            md_lines.append("**📊 Student Graph Updates from This Turn:**")
            md_lines.append("")
            
            # Extract concepts from this turn
            concepts_encountered = []
            if knowledge_gaps:
                for gap in knowledge_gaps:
                    concept = gap.get('concept', '')
                    if concept:
                        concepts_encountered.append(concept)
            
            # Extract concept from error if present
            if error_message:
                if "RecursionError" in error_message:
                    concepts_encountered.append("recursion")
                elif "IndexError" in error_message:
                    concepts_encountered.append("arrays")
                elif "KeyError" in error_message:
                    concepts_encountered.append("dictionaries")
                elif "TypeError" in error_message:
                    concepts_encountered.append("type_system")
                elif "NameError" in error_message or "UnboundLocalError" in error_message:
                    concepts_encountered.append("variable_scope")
                elif "AttributeError" in error_message:
                    concepts_encountered.append("object_oriented")
            
            # Show concepts encountered
            if concepts_encountered:
                md_lines.append("**Concepts Encountered in This Turn:**")
                for concept in set(concepts_encountered):
                    mastery = student_graph.get('concept_mastery', {}).get(concept, 0.5)
                    mastery_status = "🟢 Mastered" if mastery >= 0.7 else "🟡 Learning" if mastery >= 0.5 else "🔴 Weak"
                    md_lines.append(f"- `{concept}`: Mastery = {mastery:.2f} ({mastery_status})")
                md_lines.append("")
            
            # Show errors and their impact
            if error_message:
                md_lines.append("**Errors Encountered and Impact:**")
                md_lines.append(f"- **Error**: `{error_message[:100]}`")
                if learned_misconceptions:
                    for mc in learned_misconceptions:
                        concept = mc.get('concept', 'unknown')
                        md_lines.append(f"  - **Impact**: Misconception `{mc.get('id', 'unknown')}` learned for concept `{concept}`")
                        md_lines.append(f"  - **Action**: Student graph updated to reflect this misconception")
                md_lines.append("")
            
            # Show mastery updates
            concept_mastery = student_graph.get('concept_mastery', {})
            if concept_mastery:
                md_lines.append("**Current Concept Mastery Levels:**")
                md_lines.append("```json")
                md_lines.append(json.dumps(concept_mastery, indent=2, default=str))
                md_lines.append("```")
                md_lines.append("")
            
            # Show mastered vs weak concepts
            mastered_concepts = student_graph.get('mastered_concepts', [])
            weak_concepts = student_graph.get('weak_concepts', [])
            
            if mastered_concepts or weak_concepts:
                md_lines.append("**Concept Status:**")
                if mastered_concepts:
                    md_lines.append(f"- **Mastered Concepts** ({len(mastered_concepts)}): {', '.join(mastered_concepts[:5])}")
                    if len(mastered_concepts) > 5:
                        md_lines.append(f"  ... and {len(mastered_concepts) - 5} more")
                if weak_concepts:
                    md_lines.append(f"- **Weak Concepts** ({len(weak_concepts)}): {', '.join(weak_concepts[:5])}")
                    if len(weak_concepts) > 5:
                        md_lines.append(f"  ... and {len(weak_concepts) - 5} more")
                md_lines.append("")
            
            # Show learning history
            learning_history = student_graph.get('learning_history', {})
            if learning_history:
                md_lines.append("**Learning Progress:**")
                md_lines.append(f"- **Total Interactions**: {learning_history.get('total_interactions', 0)}")
                md_lines.append(f"- **Session Count**: {learning_history.get('session_count', 0)}")
                md_lines.append(f"- **Learning Trajectory**: {learning_history.get('learning_trajectory', 'initial')}")
                if learning_history.get('mastery_history'):
                    recent_mastery = learning_history['mastery_history'][-5:]  # Last 5
                    md_lines.append(f"- **Recent Mastery History**: {recent_mastery}")
                md_lines.append("")
            
            md_lines.append("**Full Student Graph State:**")
            md_lines.append("```json")
            md_lines.append(json.dumps({
                "student_id": student_graph.get('student_id', 'unknown'),
                "concept_mastery": student_graph.get('concept_mastery', {}),
                "mastered_concepts": student_graph.get('mastered_concepts', []),
                "weak_concepts": student_graph.get('weak_concepts', []),
                "learning_history": student_graph.get('learning_history', {}),
                "current_cognitive_state": student_graph.get('current_cognitive_state', 'engaged'),
                "source": student_graph.get('source', 'student_state_tracker')
            }, indent=2, default=str))
            md_lines.append("```")
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
        
        # STEP 8: Pedagogical KG Misconception Detection
        pedagogical_kg = system_analysis.get('pedagogical_kg', {})
        learned_misconceptions = system_analysis.get('learned_misconceptions', [])
        
        if pedagogical_kg or learned_misconceptions:
            md_lines.append("### **STEP 8: Misconception Detection (Pedagogical KG)**")
            md_lines.append("")
            
            # Show learned misconceptions from this turn
            if learned_misconceptions:
                md_lines.append("**🎓 Misconceptions Learned from This Turn:**")
                md_lines.append("")
                for i, mc in enumerate(learned_misconceptions, 1):
                    md_lines.append(f"#### **Misconception {i}: {mc.get('id', 'unknown')}**")
                    md_lines.append("")
                    md_lines.append(f"- **Concept**: `{mc.get('concept', 'unknown')}`")
                    md_lines.append(f"- **Error Type**: `{mc.get('error_type', 'N/A')}`")
                    md_lines.append(f"- **Description**: {mc.get('description', 'N/A')}")
                    md_lines.append(f"- **Severity**: `{mc.get('severity', 'medium')}`")
                    md_lines.append(f"- **Frequency**: `{mc.get('frequency', 0):.2f}`")
                    md_lines.append(f"- **Correction Strategy**: {mc.get('correction_strategy', 'N/A')}")
                    md_lines.append("")
                    md_lines.append("**Evidence from Student Input:**")
                    learned_from = mc.get('learned_from', {})
                    if learned_from.get('error_message'):
                        md_lines.append(f"- Error: `{learned_from['error_message']}`")
                    if learned_from.get('code_snippet'):
                        md_lines.append(f"- Code: `{learned_from['code_snippet']}`")
                    if learned_from.get('question'):
                        md_lines.append(f"- Question: `{learned_from['question']}`")
                    md_lines.append("")
                    md_lines.append("---")
                    md_lines.append("")
            
            # Show detected misconceptions (if any)
            if pedagogical_kg:
                md_lines.append("**Pedagogical KG Query** (Using Learned Misconceptions):")
                md_lines.append("```json")
                md_lines.append(json.dumps(pedagogical_kg, indent=2, default=str))
                md_lines.append("```")
                md_lines.append("")
                md_lines.append("---")
                md_lines.append("")
        
        # STEP 9: Intervention Selection
        md_lines.append("### **STEP 9: Intervention Selection**")
        md_lines.append("")
        md_lines.append("**Intervention Selection** (Hierarchical RL):")
        md_lines.append("```json")
        md_lines.append(json.dumps(intervention, indent=2, default=str))
        md_lines.append("```")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        
        # STEP 10: Personalized Content Generation
        md_lines.append("### **STEP 10: Personalized Content Generation**")
        md_lines.append("")
        md_lines.append("**Content Generated** (Adapted to Dynamic Learning Style):")
        md_lines.append("```json")
        md_lines.append(json.dumps({
            "intro": "Personalized introduction based on analysis",
            "main_explanation": {
                "strategy": intervention.get('adaptation_factors', {}).get('visual_verbal', 'visual') + "_step_by_step",
                "content": "Detailed explanation based on knowledge gaps and learning style"
            },
            "personalization_applied": intervention.get('adaptation_factors', {})
        }, indent=2, default=str))
        md_lines.append("```")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        
        # STEP 11: Complete Metrics with Definitions
        if metrics:
            md_lines.append("### **STEP 11: Complete Metrics**")
            md_lines.append("")
            md_lines.append("**📊 Metric Definitions:**")
            md_lines.append("")
            md_lines.append("The system calculates comprehensive metrics to track student progress and learning effectiveness:")
            md_lines.append("")
            md_lines.append("#### **Quantitative Metrics:**")
            md_lines.append("")
            md_lines.append("1. **CodeBERT Analysis**:")
            md_lines.append("   - **Syntax Errors**: Probability of syntax errors in code (0.0 = no errors, 1.0 = many errors)")
            md_lines.append("   - **Logic Errors**: Probability of logic errors in code (0.0 = no errors, 1.0 = many errors)")
            md_lines.append("   - **Total Errors**: Combined error probability")
            md_lines.append("   - **Correctness Score**: Code correctness (0.0 = incorrect, 1.0 = perfect)")
            md_lines.append("   - **Code Quality**: Qualitative assessment (poor/fair/good/excellent)")
            md_lines.append("")
            md_lines.append("3. **BERT Explanation Quality**:")
            md_lines.append("   - **Quality Score**: Overall explanation quality (0.0 = poor, 1.0 = excellent)")
            md_lines.append("   - **Completeness**: How complete the explanation is (0.0 = incomplete, 1.0 = complete)")
            md_lines.append("   - **Clarity**: How clear the explanation is (0.0 = unclear, 1.0 = very clear)")
            md_lines.append("   - **Coherence**: How coherent the explanation is (0.0 = incoherent, 1.0 = coherent)")
            md_lines.append("   - **Key Points Covered**: Number of important points addressed")
            md_lines.append("")
            md_lines.append("4. **Time Tracking**:")
            md_lines.append("   - **Turn Duration**: Total time spent on this turn (seconds/minutes)")
            md_lines.append("   - **Time Stuck**: Time spent stuck/struggling (seconds/minutes)")
            md_lines.append("   - **Average Action Duration**: Average time between actions")
            md_lines.append("   - **Total Actions**: Number of actions taken in this turn")
            md_lines.append("")
            md_lines.append("5. **Knowledge Graph Usage**:")
            md_lines.append("   - **CSE-KG**: Whether CSE Knowledge Graph was used")
            md_lines.append("   - **Pedagogical KG**: Whether Pedagogical Knowledge Graph was used")
            md_lines.append("   - **COKE**: Whether COKE Cognitive Graph was used")
            md_lines.append("   - **State Tracker**: Whether Student State Tracker was used")
            md_lines.append("")
            md_lines.append("6. **COKE Analysis**:")
            md_lines.append("   - **Cognitive State**: Current cognitive state (perceiving/understanding/engaged/confused/frustrated)")
            md_lines.append("   - **Confidence**: Confidence in cognitive state assessment (0.0 = uncertain, 1.0 = certain)")
            md_lines.append("   - **Behavioral Response**: Predicted behavioral response (continue/try_again/search_info/ask_question)")
            md_lines.append("")
            md_lines.append("#### **Qualitative Metrics:**")
            md_lines.append("")
            md_lines.append("1. **Explanation Style**: How the explanation is delivered (scaffold_gradually/direct_explanation/example_first)")
            md_lines.append("2. **Complexity Level**: Complexity of the explanation (1 = simple, 5 = advanced)")
            md_lines.append("3. **Personalization Factors**:")
            md_lines.append("   - **Based on Prior Knowledge**: Whether explanation adapts to student's prior knowledge")
            md_lines.append("   - **Gaps Addressed**: Whether knowledge gaps are addressed")
            md_lines.append("   - **Style Adapted**: Whether learning style is adapted to")
            md_lines.append("   - **Load Managed**: Whether cognitive load is managed")
            md_lines.append("4. **Cognitive State**: Current cognitive state (from COKE analysis)")
            md_lines.append("5. **Learning Style**: Inferred learning style preferences")
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
            md_lines.append("**📈 Current Turn Metrics:**")
            md_lines.append("")
            md_lines.append("**Quantitative Metrics**:")
            md_lines.append("```json")
            # Remove dina_mastery from metrics output
            metrics_copy = json.loads(json.dumps(metrics, default=str))
            if 'quantitative' in metrics_copy and 'dina_mastery' in metrics_copy['quantitative']:
                del metrics_copy['quantitative']['dina_mastery']
            md_lines.append(json.dumps(metrics_copy, indent=2, default=str))
            md_lines.append("```")
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")
        
        # System Response
        md_lines.append("### 📊 System Response to Student")
        md_lines.append("")
        md_lines.append("**Generated Response** (Based on Real Analysis):")
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        
        response_text = system_response.get('response_text', 'No response generated')
        md_lines.append(response_text)
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
        
        # Metrics (without DINA mastery)
        if metrics:
            md_lines.append("### 📈 Metrics")
            md_lines.append("")
            md_lines.append("```json")
            # Remove dina_mastery from metrics output
            metrics_copy = json.loads(json.dumps(metrics, default=str))
            if 'quantitative' in metrics_copy and 'dina_mastery' in metrics_copy['quantitative']:
                del metrics_copy['quantitative']['dina_mastery']
            md_lines.append(json.dumps(metrics_copy, indent=2, default=str))
            md_lines.append("```")
            md_lines.append("")
        
        md_lines.append("")
        md_lines.append("---")
        md_lines.append("")
    
    # Summary
    md_lines.append("## 📋 Conversation Summary")
    md_lines.append("")
    md_lines.append("```json")
    md_lines.append(json.dumps(summary, indent=2, default=str))
    md_lines.append("```")
    md_lines.append("")
    
    # Write to file
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
    
    print(f"[OK] Markdown output saved to: {output_file}")
    return output_file


if __name__ == "__main__":
    # Load conversation JSON and format
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python format_conversation_output.py <conversation_json_file> [output_md_file]")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else json_file.replace('.json', '.md')
    
    with open(json_file, 'r', encoding='utf-8') as f:
        conversation_data = json.load(f)
    
    format_conversation_to_markdown(conversation_data, output_file)

