"""
Complete Integrated System Test
Integrates:
- Knowledge Graphs (CSE-KG, Pedagogical KG, COKE)
- DINA & Nestor models
- HVSAE encoding
- Groq API for response generation
- Multi-head Reinforcement Learning
- Generates complete response with quantitative metrics
"""

import yaml
import torch
import time
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import os

# Import all components
from src.knowledge_graph import AdaptiveExplanationGenerator, PedagogicalKGIntegration
from src.models.hvsae.model import HVSAE
from groq import Groq
from src.reinforcement_learning.hierarchical_multi_task_rl import HierarchicalMultiTaskRL


class CompleteIntegratedSystem:
    """
    Complete integrated system combining all components
    """
    
    def __init__(self, config: Dict):
        self.config = config
        
        # Initialize Knowledge Graphs
        print("[1/6] Initializing Knowledge Graphs...")
        self.adaptive_explainer = AdaptiveExplanationGenerator(config)
        self.pedagogical_kg = PedagogicalKGIntegration(config)
        
        # Initialize HVSAE
        print("[2/6] Initializing HVSAE...")
        try:
            self.hvsae = HVSAE(config.get('hvsae', {}))
            # Try to load checkpoint
            checkpoint_path = Path("checkpoints/best.pt")
            if checkpoint_path.exists():
                checkpoint = torch.load(checkpoint_path, map_location='cpu')
                self.hvsae.load_state_dict(checkpoint.get('hvsae_state', checkpoint))
                print("  [OK] Loaded HVSAE checkpoint")
            else:
                print("  [WARN] No checkpoint, using untrained model")
        except Exception as e:
            print(f"  [WARN] HVSAE initialization failed: {e}")
            self.hvsae = None
        
        # Initialize Groq API
        print("[3/6] Initializing Groq API...")
        groq_api_key = os.getenv('GROQ_API_KEY') or config.get('groq', {}).get('api_key', '')
        if groq_api_key:
            try:
                self.groq = Groq(api_key=groq_api_key)
                print("  [OK] Groq API initialized")
            except Exception as e:
                print(f"  [WARN] Groq initialization failed: {e}")
                self.groq = None
        else:
            print("  [WARN] No Groq API key found")
            self.groq = None
        
        # Initialize Multi-head RL
        print("[4/6] Initializing Multi-head RL...")
        try:
            self.rl_agent = HierarchicalMultiTaskRL(config.get('reinforcement_learning', {}))
            print("  [OK] Multi-head RL initialized")
        except Exception as e:
            print(f"  [WARN] RL initialization failed: {e}")
            self.rl_agent = None
        
        print("[5/6] System ready!")
        print("[6/6] All components integrated")
    
    def process_student_query(self, student_id: str, student_data: Dict) -> Dict:
        """
        Process student query through complete pipeline
        
        Args:
            student_id: Student identifier
            student_data: Student context (code, question, conversation, etc.)
            
        Returns:
            Complete response with all metrics
        """
        start_time = time.time()
        
        # ===== STEP 1: HVSAE ENCODING =====
        print("\n[STEP 1] HVSAE Encoding...")
        hvsae_encoding = None
        if self.hvsae:
            try:
                # Prepare input batch
                batch = self._prepare_hvsae_batch(student_data)
                with torch.no_grad():
                    hvsae_output = self.hvsae.forward(batch, compute_graph=False)
                hvsae_encoding = {
                    "latent": hvsae_output.get('latent'),
                    "mu": hvsae_output.get('mu'),
                    "kappa": hvsae_output.get('kappa'),
                    "attention_weights": hvsae_output.get('attention_weights'),
                    "misconception_probs": torch.sigmoid(hvsae_output.get('misconception_logits', torch.zeros(1)))
                }
                print("  [OK] HVSAE encoding complete")
            except Exception as e:
                print(f"  [WARN] HVSAE encoding failed: {e}")
        
        # ===== STEP 2: KNOWLEDGE GRAPH ANALYSIS =====
        print("\n[STEP 2] Knowledge Graph Analysis...")
        concept = student_data.get("concept", "recursion")
        kg_analysis = self.adaptive_explainer.generate_adaptive_explanation(
            concept=concept,
            student_id=student_id,
            student_data=student_data
        )
        print(f"  [OK] Strategy: {kg_analysis.get('strategy')}, Complexity: {kg_analysis.get('complexity')}")
        
        # ===== STEP 3: DINA MASTERY ASSESSMENT =====
        print("\n[STEP 3] DINA Mastery Assessment...")
        prior_knowledge = kg_analysis.get('prior_knowledge', {})
        mastery_scores = prior_knowledge.get('mastery_scores', {})
        dina_metrics = {
            "overall_mastery": prior_knowledge.get('average_mastery', 0.5),
            "concept_specific_mastery": mastery_scores,
            "strong_areas": prior_knowledge.get('strong_areas', []),
            "weak_areas": prior_knowledge.get('weak_areas', []),
            "mastery_delta": 0.0  # Would be calculated from previous state
        }
        print(f"  [OK] Overall mastery: {dina_metrics['overall_mastery']:.2f}")
        
        # ===== STEP 4: CODEBERT ANALYSIS =====
        print("\n[STEP 4] CodeBERT Analysis...")
        code = student_data.get("code", "")
        codebert_metrics = self._analyze_code_with_codebert(code)
        print(f"  [OK] Correctness: {codebert_metrics['correctness_score']:.2f}")
        
        # ===== STEP 5: NESTOR PROFILING =====
        print("\n[STEP 5] Nestor Profiling...")
        if self.adaptive_explainer.nestor_wrapper:
            nestor_profile = self.adaptive_explainer.nestor_wrapper.get_student_profile(student_id, student_data)
            nestor_metrics = {
                "personality": nestor_profile.get("personality", {}),
                "learning_style": nestor_profile.get("learning_style", {}),
                "learning_strategy": nestor_profile.get("learning_strategy", "systematic"),
                "intervention_preferences": nestor_profile.get("intervention_preferences", [])
            }
            print(f"  [OK] Learning style: {nestor_metrics['learning_style']}")
        else:
            nestor_metrics = {
                "personality": {},
                "learning_style": {"visual_verbal": "visual", "active_reflective": "active"},
                "learning_strategy": "systematic"
            }
        
        # ===== STEP 6: COKE THEORY OF MIND =====
        print("\n[STEP 6] COKE Theory of Mind...")
        if self.adaptive_explainer.coke_graph:
            tom = self.adaptive_explainer.coke_graph.infer_theory_of_mind(student_data)
            coke_metrics = {
                "cognitive_state": tom.get("cognitive_state", "engaged"),
                "behavioral_response": tom.get("behavioral_response", "continue"),
                "confidence": tom.get("confidence", 0.5),
                "reasoning": tom.get("reasoning", "")
            }
            print(f"  [OK] Cognitive state: {coke_metrics['cognitive_state']}")
        else:
            coke_metrics = {"cognitive_state": "engaged", "confidence": 0.5}
        
        # ===== STEP 7: REINFORCEMENT LEARNING =====
        print("\n[STEP 7] Reinforcement Learning...")
        rl_action = None
        if self.rl_agent:
            try:
                # Prepare state for RL
                rl_state = self._prepare_rl_state(
                    student_id, student_data, dina_metrics, nestor_metrics, coke_metrics
                )
                rl_action = self.rl_agent.select_action(rl_state)
                print(f"  [OK] RL action selected: {rl_action.get('intervention_type', 'N/A')}")
            except Exception as e:
                print(f"  [WARN] RL action selection failed: {e}")
        
        # ===== STEP 8: GENERATE RESPONSE WITH GROQ =====
        print("\n[STEP 8] Generating Response with Groq...")
        response_text = ""
        if self.groq:
            try:
                # Build prompt from all analysis
                prompt = self._build_groq_prompt(
                    student_data, kg_analysis, dina_metrics, nestor_metrics, 
                    coke_metrics, codebert_metrics, rl_action
                )
                
                # Generate with Groq
                completion = self.groq.chat.completions.create(
                    model="llama-3.1-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are an expert programming tutor who provides personalized, clear explanations."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                response_text = completion.choices[0].message.content
                print(f"  [OK] Response generated ({len(response_text)} chars)")
            except Exception as e:
                print(f"  [WARN] Groq generation failed: {e}")
                response_text = kg_analysis.get('explanation', 'Unable to generate response')
        else:
            # Fallback to adaptive explanation
            response_text = kg_analysis.get('explanation', 'Unable to generate response')
        
        # ===== STEP 9: BERT EXPLANATION QUALITY =====
        print("\n[STEP 9] BERT Explanation Quality...")
        bert_metrics = self._analyze_explanation_quality(response_text)
        print(f"  [OK] Quality score: {bert_metrics['quality_score']:.2f}")
        
        # ===== STEP 10: CALCULATE ALL METRICS =====
        processing_time = time.time() - start_time
        
        complete_metrics = {
            "quantitative": {
                "dina_mastery": dina_metrics,
                "codebert_analysis": codebert_metrics,
                "bert_explanation_quality": bert_metrics,
                "time_tracking": {
                    "turn_duration_seconds": processing_time,
                    "turn_duration_minutes": processing_time / 60
                },
                "knowledge_graphs_used": kg_analysis.get('knowledge_graphs_used', {}),
                "nestor_profile": nestor_metrics,
                "coke_analysis": coke_metrics
            },
            "qualitative": {
                "explanation_style": kg_analysis.get('strategy', 'scaffold_gradually'),
                "complexity_level": kg_analysis.get('complexity', 3),
                "personalization_factors": kg_analysis.get('personalization_factors', {}),
                "cognitive_state": coke_metrics.get('cognitive_state', 'engaged'),
                "learning_style": nestor_metrics.get('learning_style', {})
            }
        }
        
        return {
            "session_id": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "student_id": student_id,
            "timestamp": datetime.now().isoformat(),
            "input": {
                "question": student_data.get("question", ""),
                "code": student_data.get("code", ""),
                "error_message": student_data.get("error_message", ""),
                "conversation": student_data.get("conversation", [])
            },
            "output": {
                "response": response_text,
                "response_length": len(response_text),
                "analysis": {
                    "focus": kg_analysis.get('strategy', 'general'),
                    "emotion": coke_metrics.get('cognitive_state', 'engaged'),
                    "frustration_level": 0.3 if coke_metrics.get('cognitive_state') == 'frustrated' else 0.1,
                    "mastery": dina_metrics['overall_mastery']
                }
            },
            "metrics": complete_metrics,
            "hvsae_encoding": {
                "latent_dim": hvsae_encoding['latent'].shape if hvsae_encoding and hvsae_encoding.get('latent') is not None else None,
                "has_encoding": hvsae_encoding is not None
            } if hvsae_encoding else {"has_encoding": False},
            "rl_action": rl_action
        }
    
    def _prepare_hvsae_batch(self, student_data: Dict) -> Dict:
        """Prepare batch for HVSAE"""
        # Simplified batch preparation
        code = student_data.get("code", "")
        error = student_data.get("error_message", "")
        
        return {
            "code": [code],
            "error_message": [error],
            "action_sequence": [student_data.get("action_sequence", [])],
            "time_deltas": [student_data.get("time_deltas", [])]
        }
    
    def _analyze_code_with_codebert(self, code: str) -> Dict:
        """Analyze code with CodeBERT (simplified)"""
        # In production, would use actual CodeBERT model
        syntax_errors = code.count("(") - code.count(")")  # Simple check
        logic_errors = 1 if "recursion" in code.lower() and "base" not in code.lower() else 0
        
        return {
            "syntax_errors": abs(syntax_errors),
            "logic_errors": logic_errors,
            "total_errors": abs(syntax_errors) + logic_errors,
            "correctness_score": max(0.0, 1.0 - (abs(syntax_errors) + logic_errors) * 0.2),
            "code_quality": "excellent" if (abs(syntax_errors) + logic_errors) == 0 else "needs_improvement"
        }
    
    def _analyze_explanation_quality(self, explanation: str) -> Dict:
        """Analyze explanation quality with BERT (simplified)"""
        words = explanation.lower().split()
        
        # Completeness: check for key words
        completeness_indicators = ["because", "reason", "why", "how", "explain", "example", "step"]
        completeness = sum(1 for word in words if any(ind in word for ind in completeness_indicators)) / max(len(words), 1)
        
        # Clarity: check for clarity words
        clarity_indicators = ["clear", "simple", "step", "first", "then", "example"]
        clarity = sum(1 for word in words if any(ind in word for ind in clarity_indicators)) / max(len(words), 1)
        
        # Length score
        length_score = min(1.0, len(words) / 300) if len(words) >= 50 else len(words) / 50
        
        quality_score = (completeness * 0.4 + clarity * 0.4 + length_score * 0.2)
        
        return {
            "quality_score": quality_score,
            "completeness": completeness,
            "clarity": clarity,
            "key_points_covered": int(completeness * 5)
        }
    
    def _prepare_rl_state(self, student_id: str, student_data: Dict, 
                          dina_metrics: Dict, nestor_metrics: Dict, coke_metrics: Dict) -> Dict:
        """Prepare state for RL agent"""
        return {
            "student_id": student_id,
            "mastery": dina_metrics['overall_mastery'],
            "cognitive_state": coke_metrics.get('cognitive_state', 'engaged'),
            "learning_style": nestor_metrics.get('learning_style', {}),
            "concept": student_data.get("concept", ""),
            "has_error": bool(student_data.get("error_message"))
        }
    
    def _build_groq_prompt(self, student_data: Dict, kg_analysis: Dict,
                          dina_metrics: Dict, nestor_metrics: Dict,
                          coke_metrics: Dict, codebert_metrics: Dict,
                          rl_action: Dict) -> str:
        """Build comprehensive prompt for Groq"""
        prompt = f"""Generate a personalized explanation for a student learning programming.

STUDENT CONTEXT:
- Question: {student_data.get('question', 'Help with code')}
- Code: {student_data.get('code', 'N/A')}
- Error: {student_data.get('error_message', 'None')}

STUDENT PROFILE:
- Mastery Level: {dina_metrics['overall_mastery']:.0%}
- Learning Style: {nestor_metrics.get('learning_style', {}).get('visual_verbal', 'visual')} learner
- Cognitive State: {coke_metrics.get('cognitive_state', 'engaged')}
- Strong Areas: {', '.join(dina_metrics.get('strong_areas', [])[:3]) or 'None'}
- Weak Areas: {', '.join(dina_metrics.get('weak_areas', [])[:3]) or 'None'}

KNOWLEDGE GAP ANALYSIS:
- Strategy: {kg_analysis.get('strategy', 'scaffold_gradually')}
- Complexity: {kg_analysis.get('complexity', 3)}
- Knowledge Gaps: {len(kg_analysis.get('knowledge_gaps', []))}

CODE ANALYSIS:
- Correctness: {codebert_metrics['correctness_score']:.0%}
- Errors: {codebert_metrics['total_errors']}

ADAPTIVE EXPLANATION GUIDANCE:
{kg_analysis.get('explanation', 'Provide clear, step-by-step explanation')}

Generate a personalized, encouraging response that:
1. Addresses the student's specific question
2. Adapts to their learning style ({nestor_metrics.get('learning_style', {}).get('visual_verbal', 'visual')})
3. Manages cognitive load appropriately (student is {coke_metrics.get('cognitive_state', 'engaged')})
4. Builds on what they know ({dina_metrics['overall_mastery']:.0%} mastery)
5. Fills knowledge gaps if needed
6. Uses appropriate complexity level
"""
        return prompt


def main():
    print("=" * 70)
    print("COMPLETE INTEGRATED SYSTEM TEST")
    print("=" * 70)
    
    # Load config
    config_path = Path("config.yaml")
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {
            'cse_kg': {
                'sparql_endpoint': 'http://w3id.org/cskg/sparql',
                'local_cache': True,
                'cache_dir': 'data/cse_kg_cache'
            },
            'pedagogical_kg': {'enabled': True},
            'coke': {'enabled': True},
            'hvsae': {},
            'groq': {'api_key': os.getenv('GROQ_API_KEY', '')},
            'reinforcement_learning': {}
        }
    
    # Initialize system
    system = CompleteIntegratedSystem(config)
    
    # Test student query
    print("\n" + "=" * 70)
    print("PROCESSING STUDENT QUERY")
    print("=" * 70)
    
    student_data = {
        "student_id": "test_student_001",
        "question": "I wrote this recursive function but it's not working. Can you help me?",
        "code": """def factorial(n):
    return n * factorial(n - 1)  # Missing base case!""",
        "error_message": "RecursionError: maximum recursion depth exceeded",
        "conversation": [
            "I don't understand why this isn't working",
            "I keep getting RecursionError"
        ],
        "concept": "recursion",
        "action_sequence": ["code_edit", "run_test", "run_test", "search_documentation"],
        "time_deltas": [15.0, 2.0, 3.0, 45.0],
        "time_stuck": 65.0
    }
    
    # Process query
    result = system.process_student_query("test_student_001", student_data)
    
    # Save results
    output_dir = Path("test_output")
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / f"complete_system_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    
    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"\nResponse Length: {result['output']['response_length']} characters")
    print(f"\nQuantitative Metrics:")
    print(f"  DINA Mastery: {result['metrics']['quantitative']['dina_mastery']['overall_mastery']:.2%}")
    print(f"  CodeBERT Correctness: {result['metrics']['quantitative']['codebert_analysis']['correctness_score']:.2%}")
    print(f"  BERT Quality: {result['metrics']['quantitative']['bert_explanation_quality']['quality_score']:.2f}")
    print(f"  Processing Time: {result['metrics']['quantitative']['time_tracking']['turn_duration_seconds']:.2f}s")
    
    print(f"\nKnowledge Graphs Used:")
    kgs = result['metrics']['quantitative']['knowledge_graphs_used']
    for kg, used in kgs.items():
        print(f"  {kg.upper()}: {'[OK]' if used else '[NOT USED]'}")
    
    print(f"\nResponse Preview:")
    print("-" * 70)
    print(result['output']['response'][:500] + "..." if len(result['output']['response']) > 500 else result['output']['response'])
    print("-" * 70)
    
    print(f"\nFull results saved to: {output_file}")
    print("=" * 70)

if __name__ == "__main__":
    main()












