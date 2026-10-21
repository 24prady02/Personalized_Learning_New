"""
Main Orchestrator
Coordinates all models to select and deliver personalized interventions
Now includes Reinforcement Learning for continuous improvement!
"""

# Force UTF-8 on stdout/stderr so arrow/checkmark characters in log lines
# don't crash on Windows consoles that default to cp1252.
import sys as _sys
for _stream in (_sys.stdout, _sys.stderr):
    try:
        _stream.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import torch
from typing import Dict, List, Optional, Tuple
import numpy as np
from datetime import datetime
import time


class InterventionOrchestrator:
    """
    Central orchestrator that coordinates:
    - HVSAE for encoding student state
    - Student State Tracker for cognitive diagnosis and mastery tracking
    - Behavioral models for strategy analysis
    - CSE-KG for domain knowledge
    - Intervention recommender for selection
    - Content generator for personalized delivery
    """
    
    def __init__(self, config: Dict, models: Dict, use_rl: bool = True, use_hierarchical_rl: bool = False):
        """
        Args:
            config: System configuration
            models: Dictionary with all model instances:
                - hvsae: HVSAE model
                - behavioral_rnn: Behavioral RNN
                - behavioral_hmm: Behavioral HMM
                - cse_kg_client: CSE-KG client
                - intervention_recommender: Intervention recommender
                - content_generator: Content generator
            use_rl: Whether to use RL agent for continuous improvement
            use_hierarchical_rl: Whether to use hierarchical multi-task RL
        """
        self.config = config
        self.models = models
        self.use_rl = use_rl
        self.use_hierarchical_rl = use_hierarchical_rl
        
        # Priority factors for intervention selection
        self.priority_factors = config['orchestrator']['priority_factors']
        self.intervention_threshold = config['orchestrator']['intervention_threshold']
        
        # Session history
        self.session_history = {}
        
        # Real metrics calculator (using actual CodeBERT and BERT models)
        try:
            from src.utils.real_metrics_calculator import RealMetricsCalculator
            self.metrics_calculator = RealMetricsCalculator(config)
            print("[OK] Real Metrics Calculator initialized (CodeBERT + BERT)")
        except Exception as e:
            print(f"[WARN] Real Metrics Calculator failed: {e}")
            self.metrics_calculator = None
        
        # Track session start times for time calculation
        self.session_start_times = {}
        
        # Student state tracker (for dynamic state updates)
        try:
            from src.orchestrator.student_state_tracker import StudentStateTracker
            self.state_tracker = StudentStateTracker(config)
            print("[OK] Student State Tracker initialized")
        except Exception as e:
            print(f"[WARN] Student State Tracker failed: {e}")
            self.state_tracker = None

        # ⭐ CPAL Stage 1 — LP Diagnostic + 20-concept wrong-models catalogue.
        # See mental_models_cpal_methodology.docx Part 3. This layer runs
        # on every session BEFORE intervention selection to identify the
        # student's wrong model and classify their LP level.
        try:
            from src.knowledge_graph.mental_models import MentalModelsCatalogue
            from src.orchestrator.lp_diagnostic   import LPDiagnostician
            catalogue_path = config.get("mental_models", {}).get(
                "catalogue_path",
                "data/mental_models/wrong_models_catalogue.json",
            )
            self.mental_models_catalogue = MentalModelsCatalogue(catalogue_path)
            # LPDiagnostician is the Stage 1 orchestrator; it holds the
            # catalogue and exposes .diagnose() for pre-session scoring.
            self.lp_diagnostician = LPDiagnostician(self.mental_models_catalogue)
            print("[OK] LP Diagnostician + Mental Models Catalogue initialized")
        except Exception as e:
            print(f"[WARN] LP Diagnostician failed: {e}")
            self.mental_models_catalogue = None
            self.lp_diagnostician = None

        # ⭐ CPAL Stage 2 — LPProgressionRanker (RNN-backed or heuristic).
        # Wraps LPProgressionRNN; falls back to a heuristic ranker when
        # torch is unavailable, the model is untrained, or history is
        # too short. The facade hides all that from _select_intervention.
        try:
            from src.reinforcement_learning.lp_progression_rnn import (
                LPProgressionRanker, LPProgressionRNN,
            )
            rnn_model = LPProgressionRNN() if LPProgressionRNN is not None else None
            self.lp_ranker = LPProgressionRanker(rnn_model)
            print("[OK] LPProgressionRanker initialized "
                  f"({'RNN' if rnn_model is not None else 'heuristic-only'})")
        except Exception as e:
            print(f"[WARN] LPProgressionRanker failed: {e}")
            self.lp_ranker = None

        
        # ⭐ NEW: Reinforcement Learning Agent
        if use_rl:
            from src.reinforcement_learning import TeachingRLAgent
            from src.reinforcement_learning.teaching_agent import ContinuousImprovementLoop
            
            self.rl_agent = TeachingRLAgent(config, models)
            self.improvement_loop = ContinuousImprovementLoop(self.rl_agent)
            
            print("[OK] RL Agent initialized - System will learn from every interaction!")
        
        # ⭐ NEW: Hierarchical Multi-Task RL
        if use_hierarchical_rl:
            from src.reinforcement_learning.hierarchical_multi_task_rl import HierarchicalMultiTaskRL
            
            self.hierarchical_rl = HierarchicalMultiTaskRL(config)
            
            print("[OK] Hierarchical Multi-Task RL initialized - 4-level decision making active!")
        

        
    def process_session(self, session_data: Dict) -> Dict:
        """
        Main processing pipeline for a debugging session
        
        Steps:
        1. Multi-modal encoding (HVSAE)
        2. Cognitive diagnosis (Student State Tracker)
        3. Psychological assessment (Personality Profiler)
        4. Behavioral analysis (RNN/HMM)
        5. Knowledge gap identification (CSE-KG + Student Graph)
        6. Intervention selection
        7. Personalized content generation
        8. Delivery
        
        Args:
            session_data: Dictionary with session information:
                - student_id
                - code: Buggy code
                - error_message
                - action_sequence
                - timestamps
                - recent_history
                
        Returns:
            Dictionary with intervention and analysis
        """
        # Track session start time for metrics
        student_id = session_data.get('student_id', 'unknown')
        session_start_time = time.time()
        self.session_start_times[student_id] = session_start_time
        
        student_id = session_data['student_id']
        
        # === STEP 1: MULTI-MODAL ENCODING ===
        print(f"Processing session for student {student_id}...")
        
        encoding_results = self._encode_session(session_data)
        latent = encoding_results['latent']
        
        # === STEP 1b: THREE-CHANNEL PROMPT ANALYSIS (Psychological Integration) ===
        # All 12 theories run simultaneously on the prompt BEFORE intervention selection.
        # This populates: Cognitive Graph, Progression Graph, Psychological Graph
        # and surfaces the recommended intervention with gate conditions checked.
        three_channel_result = {}
        if self.state_tracker:
            try:
                three_channel_result = self.state_tracker.analyse_prompt(student_id, session_data)
                print(f"[3-Channel] stage={three_channel_result['progression_graph']['stage']}, "
                      f"enc={three_channel_result['content_channel']['encoding_strength']}, "
                      f"attr={three_channel_result['psychological_graph']['attribution']}, "
                      f"imp={three_channel_result['psychological_graph']['imposter_flag']}, "
                      f"→ {three_channel_result['recommended_intervention']['type']}")
            except Exception as e:
                print(f"[WARN] Three-channel analysis failed: {e}")

        # === STEP 1c: CPAL STAGE 1 — LP DIAGNOSTIC LAYER ===
        # See mental_models_cpal_methodology.docx Part 3 Stage 1.
        # Runs wrong-model identification, LP level classification (L1-L4
        # on logical_step / logical_step_detail), and the plateau check
        # before any intervention is selected. The resulting lp_diagnostic
        # object threads through Stages 2-5.
        lp_diagnostic: Optional[Dict] = None
        if self.lp_diagnostician is not None and self.state_tracker is not None:
            try:
                concept_for_lp = self._extract_concept(session_data)
                # Stage 5 persistence hook — pull the student's stored LP
                # level and streak for this concept so the plateau rule
                # has history to reason over.
                lp_state_loaded = self.state_tracker.load_lp_state(
                    student_id, concept_for_lp
                ) or {}
                student_text = (
                    session_data.get("question")
                    or session_data.get("error_message")
                    or ""
                )
                diagnosis = self.lp_diagnostician.diagnose(
                    student_id       = student_id,
                    concept          = concept_for_lp,
                    question_text    = student_text,
                    stored_lp_level  = lp_state_loaded.get("lp_level"),
                    stored_lp_streak = int(lp_state_loaded.get("lp_streak", 0)),
                )
                lp_diagnostic = diagnosis.to_dict()
                # log what fired
                wm = lp_diagnostic.get("wrong_model_id") or "-"
                plateau = "PLATEAU" if lp_diagnostic["plateau_flag"] else "ok"
                print(f"[LP-Diag] concept={concept_for_lp} "
                      f"level={lp_diagnostic['current_lp_level']} "
                      f"streak={lp_diagnostic['lp_streak']} "
                      f"wm={wm} {plateau}")
            except Exception as e:
                print(f"[WARN] LP Diagnostic failed: {e}")
                import traceback; traceback.print_exc()
                lp_diagnostic = None


        # === STEP 2: COGNITIVE DIAGNOSIS ===
        cognitive_assessment = self._diagnose_cognition(student_id, session_data)
        
        # === STEP 3: PSYCHOLOGICAL ASSESSMENT ===
        psychological_assessment = self._assess_psychology(student_id, session_data)
        
        # === STEP 4: BEHAVIORAL ANALYSIS ===
        behavioral_analysis = self._analyze_behavior(session_data)
        
        # === STEP 5: KNOWLEDGE GAP IDENTIFICATION ===
        knowledge_gaps = self._identify_gaps(
            student_id,
            cognitive_assessment,
            session_data,
            behavioral_analysis,
        )
        
        # === STEP 6: INTERVENTION SELECTION ===
        # PSYCHOLOGICAL GATE: Fixed Attribution or Imposter Flag must be cleared
        # before any instructional advance (T11 Attribution + T12 Imposter).
        psychologically_gated = (
            three_channel_result.get("recommended_intervention", {}).get("gate_triggered", False)
        )
        if psychologically_gated and three_channel_result.get("recommended_intervention"):
            intervention = three_channel_result["recommended_intervention"]
            print(f"[Gate] Psychological gate -> {intervention['type']} (blocks_advance={intervention.get('blocks_advance')})")
        # LP PLATEAU OVERRIDE — CPAL Stage 2.
        # Methodology Part 3 Stage 2: "If plateau_flag is True, the
        # function returns trace_scaffold immediately with no further
        # processing." Psychological gate still wins (it's a safety
        # gate), but plateau beats everything else pedagogical.
        elif lp_diagnostic is not None and lp_diagnostic.get("plateau_flag"):
            intervention_type = lp_diagnostic["plateau_intervention"]
            intervention = {
                "type":           intervention_type,
                "priority":       1.0,
                "confidence":     1.0,
                "rationale":      (
                    f"CPAL Stage 2 LP plateau override: student has been at "
                    f"L2 on '{lp_diagnostic['concept']}' for "
                    f"{lp_diagnostic['lp_streak']} sessions; "
                    f"{intervention_type} is the plateau-breaking intervention "
                    f"(Chi et al. 1989/1994 — mechanism-level self-explanation)."
                ),
                "alternatives":   [],
                "lp_driven":      True,
                "plateau":        True,
            }
            print(f"[LP-Gate] Plateau override -> {intervention_type} "
                  f"(concept={lp_diagnostic['concept']}, "
                  f"streak={lp_diagnostic['lp_streak']})")
        # Can use either standard selection or hierarchical multi-task RL
        elif self.use_hierarchical_rl:
            intervention = self._select_intervention_hierarchical(
                student_id=student_id,
                session_data=session_data,
                cognitive_assessment=cognitive_assessment,
                psychological_assessment=psychological_assessment,
                behavioral_analysis=behavioral_analysis,
                knowledge_gaps=knowledge_gaps
            )
        elif not psychologically_gated:
            # Pull real signals from the three-channel analyser into the
            # context so the InterventionRecommender's hard gate
            # (attr=='fixed' or imposter) can actually fire on the right cases
            # and mastery/encoding can drive the scoring.
            tc = three_channel_result or {}
            pg = tc.get('psychological_graph', {}) or {}
            cg = tc.get('content_channel', {}) or {}
            mastery_profile = cognitive_assessment.get('mastery_profile', {}) or {}
            avg_mastery = (sum(mastery_profile.values())/len(mastery_profile)
                           if mastery_profile else 0.30)
            intervention = self._select_intervention(
                student_profile={
                    'personality': psychological_assessment.get('personality', {}),
                    'learning_style': psychological_assessment.get('learning_style', {}),
                    'mastery_profile': mastery_profile,
                },
                context={
                    'emotional_state': behavioral_analysis.get('emotion', 'neutral'),
                    'knowledge_gaps': knowledge_gaps,
                    'time_stuck': session_data.get('time_stuck', 0),
                    'recent_interventions': self._get_recent_interventions(student_id),
                    # Full student state so the recommender's gate + bucket lookup work
                    'encoding_strength': cg.get('encoding_strength', 'surface'),
                    'attribution':       pg.get('attribution', 'neutral'),
                    'imposter_flag':     pg.get('imposter_flag', False),
                    'high_anxiety':      pg.get('high_anxiety', False),
                    'avg_mastery':       avg_mastery,
                    # CPAL Stage 2 — LP diagnostic flows into the selector
                    # so the LP-validity gate can filter the ranked output.
                    'lp_diagnostic':     lp_diagnostic,
                    'student_id':        student_id,
                },
            )

        # === STEP 7: PERSONALIZED CONTENT GENERATION ===
        # Fix 1: three_channel_result now passed into content generation
        content = self._generate_content(
            latent=latent,
            intervention=intervention,
            student_profile=psychological_assessment,
            knowledge_gaps=knowledge_gaps,
            student_id=student_id,
            session_data=session_data,
            cognitive_assessment=cognitive_assessment,
            behavioral_analysis=behavioral_analysis,
            three_channel_result=three_channel_result,
            lp_diagnostic=lp_diagnostic,
        )
        
        # === RECORD SESSION ===
        self._record_session(student_id, session_data, intervention, content)
        
        # === DYNAMIC LEARNING: Learn from this session ===
        self._learn_from_session(
            session_data,
            cognitive_assessment,
            behavioral_analysis,
            knowledge_gaps,
            intervention,  # Pass intervention to track effectiveness
            lp_diagnostic=lp_diagnostic,
            student_id=student_id,
        )

        # === RETURN RESULT ===
        # Fix 8: three_channel analysis now in return payload
        return {
            'intervention': intervention,
            'content': content,
            'analysis': {
                'cognitive':        cognitive_assessment,
                'psychological':    psychological_assessment,
                'behavioral':       behavioral_analysis,
                'knowledge_gaps':   knowledge_gaps,
                'three_channel':    three_channel_result,
                'lp_diagnostic':    lp_diagnostic,
            },
            'encoding': encoding_results
        }
    
    def _learn_from_session(self, session_data: Dict, cognitive_assessment: Dict,
                           behavioral_analysis: Dict, knowledge_gaps: List[Dict],
                           intervention: Dict = None,
                           lp_diagnostic: Dict = None,
                           student_id: str = None):
        """
        DYNAMIC LEARNING: Learn misconceptions and cognitive chains from session

        Updates graphs with new patterns discovered from student behavior.

        CPAL Stage 4 + Stage 5:
          - If session_data contains a 'student_reply' (the student's
            response to the previous tutor turn), we classify it to get
            post_lp_level and compute delta_lp = post - pre. This is the
            primary training signal the methodology document calls for.
          - Either way, we build a session state vector and persist it
            alongside the updated LP state. These vectors become the
            input sequence to LPProgressionRNN on future sessions.
        """
        try:
            # Get adaptive explainer (has access to pedagogical_kg and coke_graph)
            adaptive_explainer = self.models.get('adaptive_explainer')

            if adaptive_explainer:
                # Learn from session (existing pedagogical-KG learning)
                if adaptive_explainer.pedagogical_kg and hasattr(adaptive_explainer.pedagogical_kg, 'pedagogical_builder'):
                    pedagogical_builder = adaptive_explainer.pedagogical_kg.pedagogical_builder
                    code = session_data.get('code')
                    error_message = session_data.get('error_message')

                    # Extract concept from knowledge gaps or error
                    concept = None
                    if knowledge_gaps:
                        concept = knowledge_gaps[0].get('concept')
                    elif error_message:
                        # Extract from error
                        if "RecursionError" in error_message:
                            concept = "recursion"
                        elif "IndexError" in error_message:
                            concept = "arrays"
                        elif "UnboundLocalError" in error_message:
                            concept = "variable_scope"
                        elif "TypeError" in error_message:
                            concept = "type_system"
                        elif "AttributeError" in error_message:
                            concept = "object_oriented"

                    # 1. Learn misconceptions
                    if concept or error_message or code:
                        learned_mc = pedagogical_builder.learn_from_session(
                            code=code,
                            error_message=error_message,
                            concept=concept
                        )
                        if learned_mc:
                            print(f"[Orchestrator] [OK] Learned misconception: {learned_mc.id}")

                    # 2. Learn cognitive load
                    if concept:
                        learned_load = pedagogical_builder.learn_cognitive_load_from_session(
                            concept=concept,
                            session_data=session_data
                        )
                        if learned_load:
                            print(f"[Orchestrator] [OK] Learned cognitive load for: {concept}")

                    # 3. Learn learning progression from mastery sequence
                    if cognitive_assessment and cognitive_assessment.get('mastery_profile'):
                        mastery_profile = cognitive_assessment['mastery_profile']
                        # Extract concept sequence from knowledge gaps or session
                        concepts_learned = list(mastery_profile.keys())
                        if len(concepts_learned) >= 2:
                            pedagogical_builder.learn_progression_from_session(
                                concept_sequence=concepts_learned,
                                student_mastery=mastery_profile
                            )

                    # 4. Learn intervention effectiveness (will be updated with feedback)
                    # Track intervention usage for later effectiveness learning
                    if intervention and intervention.get('type'):
                        intervention_id = f"int_{intervention.get('type')}_{concept or 'general'}"
                        # Effectiveness will be updated when we get feedback
                        print(f"[Orchestrator] [Tracking] intervention: {intervention_id}")

            # COKE graph learning happens automatically in infer_theory_of_mind()
            # (already called during content generation via adaptive_explainer)

            # ─────────────────────────────────────────────────────────
            # CPAL Stage 4 + Stage 5 — LP gain measurement & persistence
            # ─────────────────────────────────────────────────────────
            self._cpal_stage4_5(
                student_id      = student_id,
                session_data    = session_data,
                lp_diagnostic   = lp_diagnostic,
                intervention    = intervention,
                behavioral      = behavioral_analysis,
                cognitive       = cognitive_assessment,
            )

        except Exception as e:
            print(f"[Orchestrator] [WARN] Error in dynamic learning: {e}")
            import traceback
            traceback.print_exc()
            # Don't fail the session if learning fails

    def _cpal_stage4_5(self, student_id: str,
                        session_data: Dict,
                        lp_diagnostic: Optional[Dict],
                        intervention: Optional[Dict],
                        behavioral: Dict,
                        cognitive: Dict) -> None:
        """Run the CPAL Stage 4 post-reply classification and Stage 5
        persistence. Safe to call with missing inputs — it no-ops.
        """
        if (lp_diagnostic is None
                or self.state_tracker is None
                or self.lp_diagnostician is None
                or not student_id):
            return

        concept  = lp_diagnostic.get("concept")
        pre_lvl  = lp_diagnostic.get("current_lp_level", "L1")
        if not concept:
            return

        # Classify the student's reply to the previous tutor turn, if
        # one was captured in session_data (Stage 4 post-reply).
        reply_text = (session_data.get("student_reply")
                      or session_data.get("post_reply")
                      or "")
        if reply_text:
            # Module-level helper on the on-disk lp_diagnostic — thin
            # wrapper around classify_lp_level that returns the 3-tuple
            # we need here.
            from src.orchestrator.lp_diagnostic import classify_post_reply
            ls, lsd, post_lvl = classify_post_reply(reply_text)
        else:
            # No reply yet — persist the pre-level as the recorded level
            # (the delta will be computed on the next session when a
            # reply has arrived).
            post_lvl = pre_lvl
            ls       = bool(lp_diagnostic.get("logical_step"))
            lsd      = bool(lp_diagnostic.get("logical_step_detail"))

        # delta_lp in {-3..+3} — positive = gain, negative = regression.
        level_idx = {"L1": 1, "L2": 2, "L3": 3, "L4": 4}
        delta_lp = level_idx.get(post_lvl, 1) - level_idx.get(pre_lvl, 1)

        # Build a session state vector and persist.
        try:
            from src.reinforcement_learning.lp_progression_rnn import (
                build_state_vector,
            )
            # Pull channel signals for the state vector
            content_ch = {}
            pg = {}
            progression = {}
            try:
                state = self.state_tracker.get_student_state(student_id)
                pg          = state.get("psychological_graph", {})
                progression = state.get("progression_graph", {})
                nodes       = state.get("cognitive_graph", {}).get("concept_nodes", {})
                concept_node = nodes.get(concept, {})
                content_ch = {
                    "encoding_strength": concept_node.get("encoding", "surface"),
                }
            except Exception:
                pass

            # Mastery for this concept (cognitive assessment > node)
            mastery_profile = (cognitive or {}).get("mastery_profile", {}) or {}
            mastery_for_concept = float(
                mastery_profile.get(concept, content_ch.get("mastery", 0.30))
            )

            vec = build_state_vector(
                lp_state = {
                    "lp_level":            pre_lvl,
                    "lp_streak":           int(lp_diagnostic.get("lp_streak", 0)),
                    "logical_step":        ls,
                    "logical_step_detail": lsd,
                    "plateau_flag":        bool(lp_diagnostic.get("plateau_flag", False)),
                },
                intervention_type = (intervention or {}).get("type"),
                delta_lp_last     = delta_lp,
                emotion           = (behavioral or {}).get("emotion", "neutral"),
                encoding_strength = content_ch.get("encoding_strength", "surface"),
                stage             = progression.get("stage", 1),
                scaffold_level    = progression.get("scaffold_level", 3),
                mastery           = mastery_for_concept,
            )
        except Exception as e:
            print(f"[WARN] build_state_vector failed: {e}")
            vec = None

        # Persist — this will update lp_level, lp_streak, append to
        # lp_history and session_state_vectors, and save to disk.
        try:
            self.state_tracker.persist_lp_state(
                student_id           = student_id,
                concept              = concept,
                new_lp_level         = post_lvl,
                logical_step         = ls,
                logical_step_detail  = lsd,
                delta_lp             = delta_lp,
                last_intervention    = (intervention or {}).get("type"),
                session_state_vector = vec,
            )
            tag = "REPLY" if reply_text else "NO_REPLY"
            print(f"[LP-Persist] [{tag}] concept={concept} "
                  f"{pre_lvl}→{post_lvl} delta={delta_lp:+d} "
                  f"intv={(intervention or {}).get('type')}")
        except Exception as e:
            print(f"[WARN] persist_lp_state failed: {e}")

    def _encode_session(self, session_data: Dict) -> Dict:
        """Encode session.
        Fix 2: when HVSAE model is unavailable (not yet trained on CodeNet),
        extract REAL features from the student text instead of random tensors.
        Features come from concept detection, error type, question structure,
        and three-channel content analysis — all meaningful signals."""
        hvsae = self.models.get('hvsae')

        if hvsae is None:
            # Build a real feature vector from session content
            code     = session_data.get('code', '')
            error    = session_data.get('error_message', '')
            question = session_data.get('question', '')
            text     = f"{question} {error} {code}".lower()

            # Feature 1: concept detection using Java keyword patterns
            from src.orchestrator.student_state_tracker import CONCEPT_KEYWORDS
            concept_vec = torch.zeros(len(CONCEPT_KEYWORDS))
            for i, (concept, kws) in enumerate(CONCEPT_KEYWORDS.items()):
                hits = sum(1 for kw in kws if kw.lower() in text)
                concept_vec[i] = min(1.0, hits / max(len(kws), 1))

            # Feature 2: structural signals
            has_code    = float(bool(code.strip()))
            has_error   = float(bool(error.strip()))
            q_words     = float(any(w in question.lower() for w in ['why','how','what','when','does']))
            code_lines  = float(min(len(code.split('\n')) / 20.0, 1.0))
            has_attempt = float(any(kw in question.lower() for kw in ['i tried','my code','here is','attempt']))

            # Feature 3: error type classification
            compile_signals = ['cannot find symbol','incompatible types','missing return',
                               'unreachable','error:','compile']
            runtime_signals = ['nullpointerexception','arrayindexout','exception in thread',
                               'stackoverflowerror']
            logic_signals   = ['wrong output','expected','but got','returns 0','always','never']
            compile_score = float(any(s in text for s in compile_signals))
            runtime_score = float(any(s in text for s in runtime_signals))
            logic_score   = float(any(s in text for s in logic_signals))

            struct_vec = torch.tensor([
                has_code, has_error, q_words, code_lines, has_attempt,
                compile_score, runtime_score, logic_score
            ])

            # Pad both to 256 and concatenate to latent
            pad_concept = torch.nn.functional.pad(concept_vec, (0, 256 - len(concept_vec)))
            pad_struct  = torch.nn.functional.pad(struct_vec,  (0, 256 - len(struct_vec)))
            latent = ((pad_concept + pad_struct) / 2).unsqueeze(0)  # (1, 256)

            return {
                'latent': latent,
                'mu': latent,
                'kappa': torch.ones(1, 1),
                'attention_weights': concept_vec.unsqueeze(0),
                'misconception_probs': concept_vec[:5].unsqueeze(0),
                'source': 'feature_extraction',
            }
        
        # Set to eval mode (important for batch norm with batch_size=1)
        hvsae.eval()
        
        # Prepare batch
        batch = self._prepare_batch(session_data)
        
        # Forward pass
        with torch.no_grad():
            outputs = hvsae.forward(batch, compute_graph=False)
        
        return {
            'latent': outputs.get('latent', torch.zeros(1, 256)),
            'mu': outputs.get('mu', torch.zeros(1, 256)),
            'kappa': outputs.get('kappa', torch.ones(1, 1)),
            'attention_weights': outputs.get('attention_weights'),
            'misconception_probs': torch.sigmoid(outputs.get('misconception_logits', torch.zeros(1, 5)))
        }
    
    def _diagnose_cognition(self, student_id: str, session_data: Dict) -> Dict:
        """Cognitive diagnosis — reads real BKT mastery from cognitive_graph nodes.
        Fix 5: no longer reads legacy float dict; uses proper BKT values from
        StudentStateTracker.update_from_session which runs real BKT equations."""
        if self.state_tracker is None:
            return {'mastery_profile': {}, 'knowledge_gaps': [], 'cognitive_graph': {}}

        # Primary source: cognitive_graph concept nodes (real BKT values)
        cg = self.state_tracker.get_cognitive_graph(student_id)
        concept_nodes = cg.get('concept_nodes', {})

        mastery_profile = {}
        knowledge_gaps  = []
        for concept, node in concept_nodes.items():
            m = node.get('mastery', 0.30)
            mastery_profile[concept] = m
            if m < 0.50:
                knowledge_gaps.append({
                    'concept':   concept,
                    'mastery':   m,
                    'encoding':  node.get('encoding', 'surface'),
                    'error_type': node.get('error', 'unknown'),
                    'week':      node.get('week', 0),
                })

        # Also pull learning trajectory for trend info
        trajectory = self.state_tracker.get_learning_trajectory(student_id)

        return {
            'mastery_profile':  mastery_profile,
            'knowledge_gaps':   knowledge_gaps,
            'cognitive_graph':  cg,
            'trajectory':       trajectory,
        }
    
    def _assess_psychology(self, student_id: str, session_data: Dict) -> Dict:
        """
        Psychological assessment using Nestor Bayesian Network (preferred) or Personality Profiler
        """
        # Try Nestor profiler first (better accuracy with Bayesian Network)
        nestor_profiler = self.models.get('nestor_profiler')
        
        if nestor_profiler:
            # Get or infer personality profile using Nestor
            personality = self._get_personality_profile(student_id, session_data)
            
            # Get learning styles from Nestor inference (if available)
            if student_id in self.session_history and 'nestor_inference' in self.session_history[student_id]:
                nestor_result = self.session_history[student_id]['nestor_inference']
                learning_style = nestor_result.get('learning_styles', {})
                # Convert to our format
                learning_style = {
                    'visual_verbal': learning_style.get('visual_verbal', 'visual'),
                    'active_reflective': learning_style.get('active_reflective', 'active'),
                    'sequential_global': learning_style.get('sequential_global', 'sequential')
                }
            else:
                # Fallback to dynamic inference
                learning_style = self._infer_learning_style(session_data)
            
            return {
                'personality': personality,
                'learning_style': learning_style,
                'source': 'nestor_bayesian_network'
            }
        
        # Fallback to regular personality profiler
        personality_profiler = self.models.get('personality_profiler')
        
        if personality_profiler is None:
            return {'personality': {}, 'learning_style': {}, 'source': 'none'}
        
        # Get or infer personality profile
        personality = self._get_personality_profile(student_id, session_data)
        
        # Infer learning style from behavior if needed
        learning_style = self._infer_learning_style(session_data)
        
        return {
            'personality': personality,
            'learning_style': learning_style,
            'source': 'personality_profiler'
        }
    
    def _analyze_behavior(self, session_data: Dict) -> Dict:
        """Behavioral analysis.
        Fix 6: when RNN/HMM are unavailable (untrained) fall back to the
        LanguageChannelAnalyser which gives real emotion signals from text
        rather than the previous two-check stub (? and 'still')."""
        rnn = self.models.get('behavioral_rnn')
        hmm = self.models.get('behavioral_hmm')

        # If we have no action sequence (e.g. a pure question with no
        # debugging activity yet), the RNN can't run — fall through to the
        # language-channel fallback below.
        if not session_data.get('action_sequence'):
            rnn = None
            hmm = None

        if rnn is None and hmm is None:
            # Use language channel for real emotion inference
            if self.state_tracker:
                question = session_data.get('question', '') or session_data.get('conversation', [{}])[-1].get('content', '')
                lang = self.state_tracker.language_channel.analyse(question)
                # Map language channel signals to emotion label
                if lang['high_anxiety']:
                    emotion = 'anxious'
                elif lang['attribution'] == 'fixed' or lang['self_efficacy'] == 'low':
                    emotion = 'frustrated'
                elif lang['self_efficacy'] == 'growth':
                    emotion = 'engaged'
                elif lang['srl_phase'] == 'monitoring':
                    emotion = 'confused'
                else:
                    emotion = 'neutral'
                return {
                    'emotion':        emotion,
                    'strategy':       lang['srl_phase'],
                    'attribution':    lang['attribution'],
                    'self_efficacy':  lang['self_efficacy'],
                    'imposter_flag':  lang['imposter_signal'],
                    'high_anxiety':   lang['high_anxiety'],
                    'source':         'language_channel',
                }
            return {'emotion': 'neutral', 'strategy': 'unknown'}
        
        # Prepare behavioral features
        action_sequence = session_data.get('action_sequence', [])
        
        analysis = {}
        
        # RNN analysis — needs at least one action; pack_padded_sequence
        # rejects empty tensors. Fall back to the language channel for
        # pure-question sessions (no debugging actions yet).
        if rnn is not None and len(action_sequence) > 0:
            # Convert to tensors (must be Long/Int for embedding)
            action_ids = torch.tensor([[
                self._action_to_id(a) for a in action_sequence
            ]], dtype=torch.long)
            # Shape (B=1, T) — BehavioralRNN.forward stacks time_deltas with outcomes on dim=-1
            time_deltas = torch.tensor(
                [session_data.get('time_deltas', [0]*len(action_sequence))],
                dtype=torch.float,
            )
            outcomes = torch.zeros_like(action_ids, dtype=torch.float)
            lengths = torch.tensor([len(action_sequence)], dtype=torch.long)
            
            rnn_analysis = rnn.analyze_strategy(action_ids, time_deltas, outcomes, lengths)
            # Handle both list and scalar returns
            def get_first(item):
                return item[0] if isinstance(item, list) and len(item) > 0 else item
            
            analysis.update({
                'emotion': get_first(rnn_analysis.get('emotion', ['neutral'])),
                'emotion_confidence': get_first(rnn_analysis.get('emotion_confidence', [0.5])),
                'effectiveness': get_first(rnn_analysis.get('effectiveness', [0.5])),
                'productivity': get_first(rnn_analysis.get('productivity', ['medium'])),
                'strategy_effectiveness': get_first(rnn_analysis.get('effectiveness', [0.5]))
            })
        
        # HMM analysis
        if hmm is not None and hmm.is_fitted:
            hmm_analysis = hmm.analyze_session(action_sequence)
            analysis['hmm_state'] = hmm_analysis['final_state']
            analysis['hmm_confidence'] = hmm_analysis['final_confidence']

            # Trained emotion classifier (MLP on HMM features). Only fires
            # when a checkpoint exists — otherwise we fall through to whatever
            # emotion label the RNN / language channel already produced.
            emo = self._get_emotion_classifier()
            if emo is not None:
                try:
                    feats = hmm._extract_features(action_sequence)
                    last = feats[-1]
                    import torch as _t
                    with _t.no_grad():
                        logits = emo['model'](_t.from_numpy(last).float().unsqueeze(0))
                        probs = _t.softmax(logits, dim=1).squeeze(0).tolist()
                        idx = int(max(range(len(probs)), key=lambda i: probs[i]))
                    analysis['emotion_cls_label'] = emo['classes'][idx]
                    analysis['emotion_cls_confidence'] = probs[idx]
                    # Override only when classifier is confident — keep RNN
                    # label otherwise to avoid regressions.
                    if probs[idx] >= 0.6:
                        analysis['emotion'] = emo['classes'][idx]
                except Exception as _e:
                    print(f"[Emotion] classifier call failed: {_e}")

        return analysis

    def _get_emotion_classifier(self):
        """Lazy-load the trained 7→64→5 MLP emotion classifier once."""
        if hasattr(self, '_emotion_clf_cache'):
            return self._emotion_clf_cache
        try:
            import torch as _t
            from pathlib import Path as _P
            ckpt = _P(self.config.get('emotion', {}).get(
                'checkpoint', 'checkpoints/emotion_classifier.pt'))
            if not ckpt.exists():
                self._emotion_clf_cache = None
                return None
            data = _t.load(ckpt, weights_only=False, map_location='cpu')
            hidden = data.get('hidden', 64)
            in_dim = data.get('in_dim', 7)
            classes = data.get('classes',
                ['neutral', 'confused', 'frustrated', 'engaged', 'understanding'])
            import torch.nn as _nn
            model = _nn.Sequential(
                _nn.Linear(in_dim, hidden), _nn.ReLU(), _nn.Dropout(0.2),
                _nn.Linear(hidden, hidden), _nn.ReLU(), _nn.Dropout(0.2),
                _nn.Linear(hidden, len(classes)),
            )
            # Handle state dict key prefix from training-time Sequential wrapper
            sd = data['state_dict']
            remap = {k.replace('net.', ''): v for k, v in sd.items()}
            model.load_state_dict(remap)
            model.eval()
            self._emotion_clf_cache = {'model': model, 'classes': classes}
            print(f"[Emotion] classifier loaded from {ckpt}")
            return self._emotion_clf_cache
        except Exception as _e:
            print(f"[Emotion] load failed: {_e}")
            self._emotion_clf_cache = None
            return None
    
    def _identify_gaps(self, student_id: str,
                      cognitive_assessment: Dict,
                      session_data: Dict,
                      behavioral_analysis: Optional[Dict] = None) -> List[Dict]:
        """Identify knowledge gaps grounded in the full ontology stack.

        Uses:
          - CSE-KG concept retrieval + prerequisite lookup
          - Pedagogical KG for misconceptions + cognitive load
          - UnifiedExplanationGenerator for Theory-of-Mind + misconception binding
          - Behavioral RNN output (emotion/strategy) for gap severity weighting
        """
        cse_kg = self.models.get('cse_kg_client')
        if cse_kg is None:
            return []

        concept_retriever = self.models.get('concept_retriever')
        pedagogical_kg = self.models.get('pedagogical_kg')
        unified_gen = self.models.get('unified_explanation_generator')

        code = session_data.get('code', '')
        error_message = session_data.get('error_message', '')

        # Candidate concepts: union of
        #   (a) concepts extracted from code + error via the CSE-KG retriever
        #   (b) low-mastery concepts already tracked for this student
        # This keeps gap identification working even before the local CSE-KG
        # graph has been built (build_local_cse_kg.py).
        if concept_retriever:
            concepts = list(concept_retriever.retrieve_from_code(code, error_message) or [])
        else:
            concepts = []
        mastery_keys = list((cognitive_assessment.get('mastery_profile') or {}).keys())
        for c in mastery_keys:
            if c not in concepts:
                concepts.append(c)

        # Unified Theory-of-Mind + misconception analysis (one-shot for this session)
        unified_analysis = None
        if unified_gen is not None and (code or error_message):
            try:
                unified_analysis = unified_gen.generate_unified_explanation(
                    code=code,
                    error_message=error_message,
                    student_data={'student_id': student_id,
                                  'mastery_profile': cognitive_assessment.get('mastery_profile', {})},
                )
            except Exception as e:
                print(f"[Orchestrator] Unified explanation failed: {e}")

        # Severity boost from trained behavioral RNN
        severity_boost = 0.0
        if behavioral_analysis:
            if behavioral_analysis.get('emotion') in ('frustrated', 'anxious', 'confused'):
                severity_boost += 0.15
            if behavioral_analysis.get('strategy') == 'trial_error':
                severity_boost += 0.10
            eff = behavioral_analysis.get('effectiveness')
            if isinstance(eff, (int, float)) and eff < 0.4:
                severity_boost += 0.10

        # Build a Java-specific prerequisite index from learning_progressions.json.
        # This replaces the general CSE-KG prereq lookup: our progressions already
        # encode the CS1-Java syllabus (week 1 → 5) with explicit per-concept prereqs,
        # so we don't need a separate CSE-KG local graph for a Java-focused system.
        prereq_index = {}
        if pedagogical_kg is not None:
            try:
                for lp in pedagogical_kg.pedagogical_builder.learning_progressions.values():
                    for c, pl in (lp.prerequisites or {}).items():
                        prereq_index.setdefault(c, set()).update(pl)
            except Exception:
                pass

        mastery = cognitive_assessment.get('mastery_profile', {}) or {}
        gaps = []
        for concept in concepts:
            m = mastery.get(concept)
            # Prerequisites: prefer the Java learning-progression index; fall
            # back to CSE-KG only if the concept isn't in our CS1 syllabus.
            prereqs = sorted(prereq_index.get(concept, set()))
            if not prereqs:
                try:
                    prereqs = cse_kg.get_prerequisites(concept) or []
                except Exception:
                    prereqs = []

            # Misconceptions + cognitive load from pedagogical KG
            misconceptions, cog_load = [], None
            if pedagogical_kg is not None:
                try:
                    info = pedagogical_kg.get_concept_full_info(concept) or {}
                    misconceptions = info.get('misconceptions', []) or []
                    cog_load = info.get('cognitive_load')
                except Exception:
                    pass

            # Classify gap
            if m is not None and m < self.intervention_threshold:
                gap_type, severity = 'low_mastery', (1.0 - m) + severity_boost
            elif misconceptions:
                gap_type, severity = 'misconception', 0.6 + severity_boost
            elif m is None and concept:
                gap_type, severity = 'unknown_mastery', 0.5 + severity_boost
            else:
                continue

            gaps.append({
                'type': gap_type,
                'concept': concept,
                'mastery': m,
                'severity': min(1.0, severity),
                'prerequisites': prereqs,
                'misconceptions': misconceptions,
                'cognitive_load': cog_load,
            })

        # Attach unified explanation (Theory of Mind + misconception) to the top gap
        if gaps and unified_analysis:
            gaps.sort(key=lambda g: g.get('severity', 0.0), reverse=True)
            gaps[0]['unified_explanation'] = unified_analysis

        return gaps
    
    def _select_intervention(self, student_profile: Dict, context: Dict) -> Dict:
        """Select optimal intervention.

        CPAL Stage 2 — when an lp_diagnostic is present in the context,
        this method:
          1. Asks the existing intervention_recommender (RL policy) for
             its ranked list, and filters that list through the LP-level
             validity gate (methodology Part 3 Stage 2 table).
          2. If the recommender returns nothing useful, consults
             LPProgressionRanker (sequence model over historical state
             vectors, with a heuristic fallback for cold-start).
          3. Only if both fail does it fall through to the original
             principled rule-based scorer.

        Plateau override is handled upstream in process_session — by the
        time we get here, plateau_flag can never be True.

        Fix 5b: when RL recommender is unavailable (no trained policy),
        use a principled rule-based scorer grounded in mastery, emotion,
        and learning style — not random Q-values. Every rule has a cited
        rationale."""

        lp_diag = context.get('lp_diagnostic')
        lp_level = (lp_diag or {}).get('current_lp_level', 'L1')
        plateau_flag = bool((lp_diag or {}).get('plateau_flag', False))

        # Lazy import to avoid circulars. `filter_interventions_by_lp` is
        # a module-level function on the on-disk lp_diagnostic (not a
        # classmethod).
        try:
            from src.orchestrator.lp_diagnostic import filter_interventions_by_lp
        except Exception:
            filter_interventions_by_lp = None   # type: ignore

        # ── 1. Existing recommender, filtered by LP-level validity gate ──
        recommender = self.models.get('intervention_recommender')
        if recommender:
            recommendations = recommender.recommend(student_profile, context, top_k=8)
            if recommendations:
                ranked = [(t, float(s)) for (t, s, _r) in recommendations]
                rationale_map = {t: r for (t, _s, r) in recommendations}
                if lp_diag is not None and filter_interventions_by_lp is not None:
                    filtered = filter_interventions_by_lp(ranked, lp_level)
                else:
                    filtered = ranked
                if filtered:
                    top_type, top_score = filtered[0]
                    return {
                        'type':         top_type,
                        'priority':     self._calculate_priority(context, top_score),
                        'confidence':   top_score,
                        'rationale': (
                            rationale_map.get(top_type, 'RL recommender')
                            + (f' (LP-gate: L={lp_level})' if lp_diag else '')
                        ),
                        'alternatives': filtered[1:],
                        'lp_driven':    lp_diag is not None,
                    }

        # ── 2. LPProgressionRanker — RNN/heuristic over LP history ──
        if lp_diag is not None and getattr(self, 'lp_ranker', None) is not None:
            try:
                student_id = context.get('student_id') or 'unknown'
                concept = lp_diag.get('concept')
                history = []
                if concept and self.state_tracker is not None:
                    history = self.state_tracker.get_session_state_vectors(
                        student_id, concept, max_len=20
                    )
                ranked = self.lp_ranker.rank(
                    session_state_vectors = history,
                    lp_level              = lp_level,
                    plateau_flag          = plateau_flag,
                )
                if filter_interventions_by_lp is not None:
                    ranked = filter_interventions_by_lp(ranked, lp_level)
                if ranked:
                    top_type, top_score = ranked[0]
                    return {
                        'type':         top_type,
                        'priority':     self._calculate_priority(context, top_score),
                        'confidence':   float(top_score),
                        'rationale': (
                            f'CPAL Stage 2 LPProgressionRanker '
                            f'(L={lp_level}, history={len(history)} sessions)'
                        ),
                        'alternatives': ranked[1:],
                        'lp_driven':    True,
                    }
            except Exception as e:
                print(f"[WARN] LPProgressionRanker fallback: {e}")

        # ── 3. Original principled heuristic fallback ──
        # Principled fallback — no random values
        emotion     = context.get('emotional_state', 'neutral')
        gaps        = context.get('knowledge_gaps', [])
        time_stuck  = context.get('time_stuck', 0)
        personality = student_profile.get('personality', {})
        ls          = student_profile.get('learning_style', {})
        mastery     = student_profile.get('mastery_profile', {})

        avg_mastery = (sum(mastery.values()) / len(mastery)) if mastery else 0.5
        is_frustrated = emotion in ('frustrated', 'anxious')
        is_stuck      = time_stuck > 120  # 2+ minutes
        is_visual     = ls.get('visual_verbal', 'visual') == 'visual'
        is_systematic = personality.get('cognitive_style', '') == 'systematic'
        is_conceptual = personality.get('learning_preference', '') == 'conceptual'

        # Helper to apply LP gate to heuristic returns
        def _lp_guard(candidate_type: str, fallback_type: str,
                      default: Dict) -> Dict:
            """If LP gate rejects the candidate, substitute the fallback."""
            if lp_diag is None or filter_interventions_by_lp is None:
                return default
            allowed = filter_interventions_by_lp(
                [(candidate_type, 1.0), (fallback_type, 0.5)], lp_level
            )
            if not allowed:
                return default
            # If the top candidate survived the gate, use it.
            if allowed[0][0] == candidate_type:
                return default
            # Otherwise the fallback is the next best allowed type.
            return {
                **default,
                'type': allowed[0][0],
                'rationale': (default.get('rationale', '')
                              + f' (LP-gate: substituted for L={lp_level})'),
            }

        # Gate: emotional support before instruction
        if is_frustrated and avg_mastery < 0.40:
            return _lp_guard('reduce_challenge', 'worked_example',
                {'type': 'reduce_challenge',    'priority': 0.95,
                 'rationale': 'Frustrated + low mastery: reduce complexity first',
                 'confidence': 0.90})
        if is_frustrated:
            return _lp_guard('worked_example', 'socratic_prompt',
                {'type': 'worked_example',      'priority': 0.88,
                 'rationale': 'Frustrated: concrete worked example before advancing',
                 'confidence': 0.85})

        # High mastery — advance
        if avg_mastery >= 0.80 and not is_stuck:
            return _lp_guard('transfer_task', 'increase_challenge',
                {'type': 'transfer_task',       'priority': 0.85,
                 'rationale': 'High mastery: challenge with transfer task',
                 'confidence': 0.82})
        if avg_mastery >= 0.65:
            return _lp_guard('increase_challenge', 'socratic_prompt',
                {'type': 'increase_challenge',  'priority': 0.78,
                 'rationale': 'Good mastery: increase challenge level',
                 'confidence': 0.75})

        # Stuck for a while — scaffolded example
        if is_stuck:
            if is_visual:
                return _lp_guard('worked_example', 'trace_scaffold',
                    {'type': 'worked_example',  'priority': 0.80,
                     'rationale': 'Stuck + visual learner: dual-coded worked example',
                     'confidence': 0.78})
            return _lp_guard('worked_example', 'trace_scaffold',
                {'type': 'worked_example',      'priority': 0.75,
                 'rationale': 'Stuck: scaffolded worked example',
                 'confidence': 0.72})

        # Conceptual learner — Socratic
        if is_conceptual and avg_mastery >= 0.40:
            return _lp_guard('socratic_prompt', 'worked_example',
                {'type': 'socratic_prompt',     'priority': 0.72,
                 'rationale': 'Conceptual learner at moderate mastery: Socratic discovery',
                 'confidence': 0.70})

        # Default: worked example
        return _lp_guard('worked_example', 'worked_example',
            {'type': 'worked_example',          'priority': 0.65,
             'rationale': 'Default: scaffolded worked example for current mastery level',
             'confidence': 0.62})
    
    def _select_intervention_hierarchical(self, student_id: str,
                                         session_data: Dict,
                                         cognitive_assessment: Dict,
                                         psychological_assessment: Dict,
                                         behavioral_analysis: Dict,
                                         knowledge_gaps: List[Dict]) -> Dict:
        """
        Select intervention using Hierarchical Multi-Task RL
        
        Uses 4-level decision making:
        - Meta-level: Student type and general strategy
        - Curriculum-level: Concept selection
        - Session-level: Multi-objective optimization
        - Intervention-level: Specific action
        """
        
        # Prepare comprehensive student state
        student_state = {
            'student_id': student_id,
            'student_type': self._infer_student_type(psychological_assessment, behavioral_analysis),
            'overall_progress': self._calculate_overall_progress(student_id),
            'completed_concepts': self._get_completed_concepts(student_id),
            'learning_goals': self._get_learning_goals(student_id),
            
            # Current session
            'current_concept': self._extract_concept(session_data),
            'mastery': self._get_average_mastery(cognitive_assessment),
            'emotion': behavioral_analysis.get('emotion', 'neutral'),
            'frustration_level': behavioral_analysis.get('frustration', 0.5),
            'engagement_score': behavioral_analysis.get('engagement', 0.5),
            'time_stuck': session_data.get('time_stuck', 0),
            
            # Knowledge gaps
            'knowledge_gaps': knowledge_gaps,
            
            # Personality
            'conscientiousness': psychological_assessment.get('personality', {}).get('conscientiousness', 0.5),
            'neuroticism': psychological_assessment.get('personality', {}).get('neuroticism', 0.5),
            'openness': psychological_assessment.get('personality', {}).get('openness', 0.5),
            'learning_style': psychological_assessment.get('learning_style', {}).get('visual_verbal', 'visual'),
            
            # Behavioral
            'behavioral_pattern': self._classify_behavior_pattern(behavioral_analysis),
            'dropout_risk': self._estimate_dropout_risk(behavioral_analysis),
            
            # Context
            'session_duration': session_data.get('session_duration', 0),
            'previous_interventions': self._get_recent_interventions(student_id),
            'time_of_day': datetime.now().strftime('%p').lower()
        }
        
        # Use hierarchical RL to make decision
        try:
            result = self.hierarchical_rl.teach_sarah(
                sarah_state=student_state,
                session_history=self._get_session_history(student_id)
            )
            
            # Extract intervention from multi-level decision
            session_plan = result['session_plan']
            
            return {
                'type': session_plan['intervention'],
                'priority': session_plan['q_combined'],
                'confidence': max(session_plan['objective_weights'].values()),
                'rationale': f"Hierarchical RL: {result['meta_strategy']['approach']} strategy, "
                           f"focusing on {session_plan['primary_objective']}",
                'meta_strategy': result['meta_strategy'],
                'curriculum_decision': result['curriculum_decision'],
                'multi_task_weights': session_plan['objective_weights'],
                'expected_outcomes': session_plan['expected_outcomes']
            }
        
        except Exception as e:
            print(f"⚠ Hierarchical RL failed: {e}, falling back to standard selection")
            return self._select_intervention(
                student_profile={
                    'personality': psychological_assessment.get('personality', {}),
                    'learning_style': psychological_assessment.get('learning_style', {}),
                    'mastery_profile': cognitive_assessment.get('mastery_profile', {})
                },
                context={
                    'emotional_state': behavioral_analysis.get('emotion', 'neutral'),
                    'knowledge_gaps': knowledge_gaps,
                    'time_stuck': session_data.get('time_stuck', 0),
                    'recent_interventions': self._get_recent_interventions(student_id)
                }
            )
    
    def _calculate_priority(self, context: Dict, base_score: float) -> float:
        """Calculate intervention priority"""
        priority = base_score
        
        # Knowledge gap urgency
        gaps = context.get('knowledge_gaps', [])
        if gaps:
            gap_urgency = sum(
                1.0 - g.get('mastery', 0.5) for g in gaps
            ) / len(gaps)
            priority += self.priority_factors['knowledge_gap'] * gap_urgency
        
        # Emotional state
        emotion = context.get('emotional_state', 'neutral')
        if emotion in ['frustrated', 'confused']:
            priority += self.priority_factors['emotional_state'] * 0.8
        
        # Time stuck
        time_stuck = context.get('time_stuck', 0)
        if time_stuck > 300:  # 5 minutes
            priority += self.priority_factors['time_stuck'] * min(time_stuck / 600, 1.0)
        
        return min(1.0, priority)
    
    def _generate_content(self, latent: torch.Tensor,
                         intervention: Dict,
                         student_profile: Dict,
                         knowledge_gaps: List[Dict],
                         student_id: str = None,
                         session_data: Dict = None,
                         cognitive_assessment: Dict = None,
                         behavioral_analysis: Dict = None,
                         three_channel_result: Dict = None,
                         lp_diagnostic: Dict = None) -> Dict:
        # Fix 1+2: three_channel_result carries psychological graph, progression graph,
        # content channel, and recommended intervention into the prompt builder.
        # CPAL Stage 3: lp_diagnostic carries the wrong-model + LP level +
        # plateau context into the prompt so _build_enhanced_prompt can
        # inject the LP-1 / LP-2 / LP-3 sections.
        """
        Generate personalized content using Adaptive Explanation Generator
        Integrated with HVSAE, Claude, and RL
        """
        # Initialize Adaptive Explanation Generator if not already done
        if 'adaptive_explainer' not in self.models:
            try:
                from src.knowledge_graph import AdaptiveExplanationGenerator
                self.models['adaptive_explainer'] = AdaptiveExplanationGenerator(self.config)
                print("[OK] Adaptive Explanation Generator initialized")
            except Exception as e:
                print(f"[WARN] Adaptive Explanation Generator failed: {e}")
                self.models['adaptive_explainer'] = None
        
        adaptive_explainer = self.models.get('adaptive_explainer')
        
        # Prepare student data for adaptive explainer
        if session_data and adaptive_explainer:
            # Extract concept from code/error
            concept = self._extract_concept(session_data)
            
            # Prepare comprehensive student data
            student_data = {
                "code": session_data.get("code", ""),
                "error_message": session_data.get("error_message", ""),
                "question": session_data.get("question", ""),
                "conversation": session_data.get("conversation", []),
                "concept": concept,
                "action_sequence": session_data.get("action_sequence", []),
                "time_stuck": session_data.get("time_stuck", 0),
                "theory_of_mind": {
                    "cognitive_state": behavioral_analysis.get("emotion", "engaged") if behavioral_analysis else "engaged"
                }
            }
            
            # Get adaptive explanation
            try:
                # Ensure student_id is available
                effective_student_id = student_id if student_id else (session_data.get('student_id', 'student') if session_data else 'student')
                adaptive_result = adaptive_explainer.generate_adaptive_explanation(
                    concept=concept,
                    student_id=effective_student_id,
                    student_data=student_data
                )
                
                # Use Enhanced Personalized Generator with Groq API
                if 'enhanced_generator' not in self.models:
                    try:
                        from src.orchestrator.enhanced_personalized_generator import EnhancedPersonalizedGenerator
                        ollama_model = self.config.get('ollama', {}).get('model', 'llama3.1')
                        ollama_url   = self.config.get('ollama', {}).get('url', 'http://localhost:11434')
                        gen = EnhancedPersonalizedGenerator()
                        gen._ollama_model = ollama_model
                        gen._ollama_url   = f"{ollama_url}/api/generate"
                        self.models['enhanced_generator'] = gen
                        print(f"[OK] Enhanced Personalized Generator initialized with Ollama ({ollama_model})")
                    except Exception as e:
                        print(f"[WARN] Enhanced generator setup failed: {e}")
                
                if self.models.get('enhanced_generator'):
                    try:
                        # Fix 1+2: three_channel data now in student_state so
                        # enhanced_personalized_generator can inject it into the prompt.
                        tc = three_channel_result or {}
                        student_state = {
                            'student_id': student_id,
                            'interaction_count': len(session_data.get('conversation', [])) + 1,
                            'personality': student_profile.get('personality', {}),
                            'knowledge_state': {
                                'overall_mastery': adaptive_result.get('prior_knowledge', {}).get('average_mastery', 0.5),
                                'mastery_history': [adaptive_result.get('prior_knowledge', {}).get('average_mastery', 0.5)]
                            },
                            # Psychological / progression data from three-channel analysis
                            'psychological_graph': tc.get('psychological_graph', {}),
                            'progression_graph':   tc.get('progression_graph', {}),
                            'content_channel':     tc.get('content_channel', {}),
                            'language_channel':    tc.get('language_channel', {}),
                            'recommended_intervention': tc.get('recommended_intervention', {}),
                            # CPAL Stage 3: LP diagnostic for the prompt builder
                            'lp_diagnostic': lp_diagnostic,
                        }
                        
                        # Get COKE cognitive state (QUERY ACTUALLY)
                        coke_cognitive_state = None
                        coke_info = {}
                        if adaptive_explainer and adaptive_explainer.coke_graph:
                            try:
                                # Predict cognitive state from conversation
                                coke_cognitive_state = adaptive_explainer.coke_graph.predict_cognitive_state(student_data)
                                cognitive_state_str = coke_cognitive_state.value if hasattr(coke_cognitive_state, 'value') else str(coke_cognitive_state)
                                
                                # Get behavioral response prediction
                                behavioral_response = 'ask_question'
                                try:
                                    if hasattr(adaptive_explainer.coke_graph, 'predict_behavioral_response'):
                                        behavioral_response = adaptive_explainer.coke_graph.predict_behavioral_response(coke_cognitive_state, student_data)
                                        if hasattr(behavioral_response, 'value'):
                                            behavioral_response = behavioral_response.value
                                except:
                                    pass
                                
                                # Get cognitive chain and behavioral response
                                cognitive_chain_desc = ''
                                try:
                                    # Get cognitive chains for this state
                                    if hasattr(adaptive_explainer.coke_graph, 'get_cognitive_chains_for_state'):
                                        chains = adaptive_explainer.coke_graph.get_cognitive_chains_for_state(coke_cognitive_state)
                                        if chains:
                                            chain = chains[0]  # Get first matching chain
                                            if hasattr(chain, 'behavioral_response'):
                                                behavioral_response = chain.behavioral_response.value if hasattr(chain.behavioral_response, 'value') else str(chain.behavioral_response)
                                            cognitive_chain_desc = f"Student is in {cognitive_state_str} state, likely to {behavioral_response}"
                                        else:
                                            # Use predict_behavioral_response as fallback
                                            if hasattr(adaptive_explainer.coke_graph, 'predict_behavioral_response'):
                                                context = student_data.get('error_message', '') or student_data.get('question', '')
                                                predicted_response = adaptive_explainer.coke_graph.predict_behavioral_response(coke_cognitive_state, context)
                                                behavioral_response = predicted_response.value if hasattr(predicted_response, 'value') else str(predicted_response)
                                                cognitive_chain_desc = f"Student is in {cognitive_state_str} state, likely to {behavioral_response}"
                                            else:
                                                cognitive_chain_desc = f"Student cognitive state: {cognitive_state_str}"
                                    else:
                                        cognitive_chain_desc = f"Student cognitive state: {cognitive_state_str}"
                                except Exception as e:
                                    cognitive_chain_desc = f"Student cognitive state: {cognitive_state_str}"
                                
                                coke_info = {
                                    'cognitive_state': cognitive_state_str,
                                    'mental_activity': cognitive_state_str,
                                    'behavioral_response': behavioral_response,
                                    'confidence': 0.8,
                                    'cognitive_chain': {'description': cognitive_chain_desc} if cognitive_chain_desc else {},
                                    'source': 'COKE Cognitive Knowledge Graph'
                                }
                                print(f"[OK] COKE queried: cognitive state = {cognitive_state_str}, behavioral response = {behavioral_response}")
                            except Exception as e:
                                print(f"[WARN] COKE analysis failed: {e}")
                                import traceback
                                traceback.print_exc()
                        
                        # Get CSE-KG information (QUERY ACTUALLY)
                        cse_kg_info = {}
                        if adaptive_explainer and adaptive_explainer.cse_kg:
                            try:
                                # Use _get_prerequisites from adaptive explainer which queries CSE-KG
                                prerequisites_list = adaptive_explainer._get_prerequisites(concept)
                                prerequisites = [p.get('concept', '') if isinstance(p, dict) else str(p) for p in prerequisites_list]
                                
                                # Get related concepts
                                related_concepts = []
                                try:
                                    if hasattr(adaptive_explainer.cse_kg, 'get_related_concepts'):
                                        related = adaptive_explainer.cse_kg.get_related_concepts(concept, max_distance=1)
                                        related_concepts = [r[0] if isinstance(r, tuple) else str(r) for r in related[:5]]
                                except:
                                    pass
                                
                                # Get concept definition/label
                                definition = f"Concept: {concept}"
                                try:
                                    if hasattr(adaptive_explainer.cse_kg, 'search_by_keywords'):
                                        search_results = adaptive_explainer.cse_kg.search_by_keywords([concept], limit=1)
                                        if search_results:
                                            definition = search_results[0].get('label', definition)
                                except:
                                    pass
                                
                                cse_kg_info = {
                                    'concept': concept,
                                    'prerequisites': prerequisites,
                                    'related_concepts': related_concepts,
                                    'definition': definition,
                                    'source': 'CSE-KG 2.0'
                                }
                                print(f"[OK] CSE-KG queried: {len(prerequisites)} prerequisites, {len(related_concepts)} related concepts")
                            except Exception as e:
                                print(f"[WARN] CSE-KG query failed: {e}")
                                import traceback
                                traceback.print_exc()
                        
                        # Get Pedagogical KG information (QUERY ACTUALLY)
                        pedagogical_kg_info = {}
                        if adaptive_explainer and adaptive_explainer.pedagogical_kg:
                            try:
                                # Query Pedagogical KG for full concept info
                                concept_full_info = adaptive_explainer.pedagogical_kg.get_concept_full_info(concept)
                                
                                # Get misconceptions (use pedagogical_builder method)
                                misconceptions = adaptive_explainer.pedagogical_kg.pedagogical_builder.get_misconceptions_for_concept(concept)
                                misconception_descriptions = []
                                if misconceptions:
                                    for m in misconceptions[:3]:
                                        if isinstance(m, dict):
                                            misconception_descriptions.append(m.get('description', m.get('name', str(m))))
                                        else:
                                            misconception_descriptions.append(str(m))
                                
                                # Get cognitive load
                                cognitive_load = adaptive_explainer.pedagogical_kg.get_cognitive_load_info(concept)
                                cognitive_load_level = 'moderate'
                                if cognitive_load:
                                    if isinstance(cognitive_load, dict):
                                        cognitive_load_level = cognitive_load.get('level', cognitive_load.get('total_load', 'moderate'))
                                    else:
                                        cognitive_load_level = str(cognitive_load)
                                
                                # Get learning progression
                                progression_desc = ''
                                if concept_full_info:
                                    if isinstance(concept_full_info, dict):
                                        progression = concept_full_info.get('learning_progression', {})
                                        if isinstance(progression, dict):
                                            progression_desc = progression.get('description', progression.get('steps', ''))
                                        else:
                                            progression_desc = str(progression)
                                
                                # Get interventions
                                interventions = []
                                if concept_full_info and isinstance(concept_full_info, dict):
                                    interventions_list = concept_full_info.get('interventions', [])
                                    for i in interventions_list[:3]:
                                        if isinstance(i, dict):
                                            interventions.append(i.get('type', i.get('name', str(i))))
                                        else:
                                            interventions.append(str(i))
                                
                                pedagogical_kg_info = {
                                    'progression': progression_desc,
                                    'misconceptions': misconception_descriptions,
                                    'cognitive_load': cognitive_load_level,
                                    'interventions': interventions,
                                    'source': 'Pedagogical Knowledge Graph'
                                }
                                print(f"[OK] Pedagogical KG queried: {len(misconception_descriptions)} misconceptions, cognitive load: {cognitive_load_level}")
                            except Exception as e:
                                print(f"[WARN] Pedagogical KG query failed: {e}")
                                import traceback
                                traceback.print_exc()
                        
                        # Prepare analysis for enhanced generator with ALL knowledge graphs
                        analysis = {
                            'emotion': behavioral_analysis.get('emotion', 'engaged') if behavioral_analysis else 'engaged',
                            'frustration_level': 0.7 if adaptive_result.get('learning_style_adaptation', {}).get('visual_verbal') == 'frustrated' else 0.3,
                            'engagement_score': 0.6,
                            'mastery_change': 0.0,
                            # Knowledge Graphs (CRITICAL)
                            'cse_kg': cse_kg_info,
                            'pedagogical_kg': pedagogical_kg_info,
                            'coke': coke_info,
                            # Fallback
                            'kg_knowledge': {
                                'name': concept,
                                'common_misconceptions': [g.get('concept', '') for g in adaptive_result.get('knowledge_gaps', [])],
                                'better_mental_model': adaptive_result.get('explanation', '')
                            }
                        }
                        
                        # Generate comprehensive response with all 10 features + Knowledge Graphs
                        enhanced_response = self.models['enhanced_generator'].generate_personalized_response(
                            student_id=student_id,
                            student_message=student_data.get('question', 'Help with code'),
                            student_state=student_state,
                            analysis=analysis,
                            code=student_data.get('code', ''),
                            code_analysis={
                                'errors': [{
                                    'type': 'logic_error',
                                    'line': 'N/A',
                                    'issue': student_data.get('error_message', ''),
                                    'fix': adaptive_result.get('explanation', '')
                                }] if student_data.get('error_message') else []
                            },
                            adaptive_analysis=adaptive_result  # Pass full adaptive analysis for KG access
                        )
                        adaptive_result['explanation'] = enhanced_response
                        print("[OK] Response generated with Enhanced Personalized Generator (Ollama)")
                    except Exception as e:
                        print(f"[WARN] Enhanced generator failed: {e}")
                        import traceback
                        traceback.print_exc()
                        # Fallback to direct Groq enhancement
                        try:
                            enhanced_response = self._enhance_with_ollama(
                                adaptive_result.get('explanation', ''),
                                student_data,
                                adaptive_result,
                                student_profile
                            )
                            adaptive_result['explanation'] = enhanced_response
                        except Exception as e2:
                            print(f"[WARN] Claude enhancement also failed: {e2}")
                
                # Calculate quantitative metrics
                metrics = self._calculate_complete_metrics(
                    session_data, adaptive_result, cognitive_assessment,
                    behavioral_analysis, student_profile, knowledge_gaps
                )
                
                # ===== DYNAMIC STATE UPDATE =====
                # Extract concepts from code/conversation
                concepts_identified = self._extract_concepts_dynamically(session_data, adaptive_result)
                
                # Infer cognitive state from conversation (COKE)
                cognitive_state = self._infer_cognitive_state_from_conversation(session_data, behavioral_analysis)
                
                # Calculate code correctness
                code_correctness = metrics['quantitative']['codebert_analysis']['correctness_score']
                response_quality = metrics['quantitative']['bert_explanation_quality']['quality_score']
                
                # Update student state tracker
                if self.state_tracker:
                    self.state_tracker.update_from_session(
                        student_id=student_id,
                        session_data=session_data,
                        cognitive_state=cognitive_state,
                        concepts_identified=concepts_identified,
                        code_correctness=code_correctness,
                        response_quality=response_quality
                    )
                    
                    # Mastery is already updated by Student State Tracker above
                
                return {
                    'intervention': intervention,
                    'content': {
                        'explanation': adaptive_result.get('explanation', ''),
                        'type': intervention['type']
                    },
                    'analysis': {
                        'cognitive': cognitive_assessment,
                        'psychological': student_profile,
                        'behavioral': behavioral_analysis,
                        'knowledge_gaps': knowledge_gaps
                    },
                    'adaptive_analysis': adaptive_result,
                    'metrics': metrics,
                    'encoding': encoding_results if 'encoding_results' in locals() else {},
                    'knowledge_graphs_used': adaptive_result.get('knowledge_graphs_used', {}),
                    'strategy': adaptive_result.get('strategy', 'scaffold_gradually'),
                    'complexity': adaptive_result.get('complexity', 3),
                    'cognitive_state_inferred': cognitive_state,
                    'concepts_identified': concepts_identified,
                    'state_updated': True
                }
            except Exception as e:
                print(f"[WARN] Adaptive explanation failed: {e}")
                import traceback
                traceback.print_exc()
        
        # Fallback to original content generator
        content_gen = self.models.get('content_generator')
        if content_gen:
            content = content_gen.generate(
                latent=latent,
                intervention_type=intervention['type'],
                student_profile=student_profile,
                knowledge_gaps=knowledge_gaps
            )
            return {
                'intervention': intervention,
                'content': content,
                'analysis': {
                    'cognitive': cognitive_assessment if cognitive_assessment else {},
                    'psychological': student_profile,
                    'behavioral': behavioral_analysis if behavioral_analysis else {}
                },
                'encoding': encoding_results if 'encoding_results' in locals() else {}
            }
        
        # Ultimate fallback
        return {
            'intervention': intervention,
            'content': {
                'explanation': 'Default explanation',
                'type': intervention['type']
            },
            'analysis': {
                'cognitive': {},
                'psychological': {},
                'behavioral': {}
            },
            'encoding': {}
        }
    
    def _extract_concept(self, session_data: Dict) -> str:
        """Extract concept from code/error"""
        code = session_data.get("code", "").lower()
        error = session_data.get("error_message", "").lower()
        
        # Simple concept extraction
        if "recursion" in code or "recursion" in error or "recursive" in code:
            return "recursion"
        elif "loop" in code or "for" in code or "while" in code:
            return "loops"
        elif "function" in code or "def" in code:
            return "functions"
        elif "class" in code or "object" in code:
            return "object_oriented"
        else:
            return "programming"
    
    def _extract_concepts_dynamically(self, session_data: Dict, adaptive_result: Dict) -> List[str]:
        """
        Dynamically extract concepts from code, error, and conversation
        Uses CSE-KG to identify actual concepts
        """
        concepts = []
        
        # Get from adaptive result if available
        if 'concepts_identified' in adaptive_result:
            concepts.extend(adaptive_result['concepts_identified'])
        
        # Extract from CSE-KG if available
        cse_kg = self.models.get('cse_kg_client')
        if cse_kg:
            try:
                # Extract from code
                code = session_data.get("code", "")
                error = session_data.get("error_message", "")
                question = session_data.get("question", "")
                
                # Use concept retriever if available
                concept_retriever = self.models.get('concept_retriever')
                if concept_retriever:
                    extracted = concept_retriever.retrieve_from_code(code, error)
                    concepts.extend(extracted)
                else:
                    # Fallback: simple keyword extraction
                    text = f"{code} {error} {question}".lower()
                    concept_keywords = {
                        'recursion': ['recursion', 'recursive', 'base case'],
                        'loops': ['loop', 'for', 'while', 'iterate'],
                        'functions': ['function', 'def', 'call'],
                        'variables': ['variable', 'assign', '='],
                        'conditional_statements': ['if', 'else', 'elif', 'conditional'],
                        'data_structures': ['list', 'dict', 'array', 'tuple'],
                        'algorithms': ['algorithm', 'sort', 'search'],
                        'object_oriented': ['class', 'object', 'method', 'attribute'],
                        'error_handling': ['try', 'except', 'error', 'exception']
                    }
                    
                    for concept, keywords in concept_keywords.items():
                        if any(kw in text for kw in keywords):
                            concepts.append(concept)
            except Exception as e:
                print(f"[WARN] Concept extraction failed: {e}")
        
        # Remove duplicates and return
        return list(set(concepts)) if concepts else [self._extract_concept(session_data)]
    
    def _infer_cognitive_state_from_conversation(self, session_data: Dict, behavioral_analysis: Dict) -> str:
        """
        Infer cognitive state from conversation using COKE
        """
        # Try COKE graph if available
        adaptive_explainer = self.models.get('adaptive_explainer')
        if adaptive_explainer and adaptive_explainer.coke_graph:
            try:
                cognitive_state = adaptive_explainer.coke_graph.predict_cognitive_state(session_data)
                return cognitive_state.value if hasattr(cognitive_state, 'value') else str(cognitive_state)
            except Exception as e:
                print(f"[WARN] COKE inference failed: {e}")
        
        # Fallback to behavioral analysis
        if behavioral_analysis:
            emotion = behavioral_analysis.get('emotion', 'neutral')
            if emotion in ['frustrated', 'confused', 'engaged', 'understanding']:
                return emotion
        
        # Fallback: analyze conversation text
        conversation = session_data.get('conversation', [])
        question = session_data.get('question', '')
        error = session_data.get('error_message', '')
        
        text = f"{question} {' '.join(str(c) for c in conversation)} {error}".lower()
        
        if any(word in text for word in ['confused', "don't understand", "don't get", 'help']):
            return 'confused'
        elif any(word in text for word in ['frustrated', 'stuck', 'hard', 'difficult']):
            return 'frustrated'
        elif any(word in text for word in ['understand', 'got it', 'see', 'clear']):
            return 'understanding'
        elif error:
            return 'confused'
        else:
            return 'engaged'
    
    def _enhance_with_ollama(self, base_explanation: str, student_data: Dict,
                            adaptive_result: Dict, student_profile: Dict) -> str:
        """Enhance explanation using local Ollama model."""
        import requests, os
        ollama_url   = self.config.get('ollama', {}).get('url',   'http://localhost:11434')
        ollama_model = self.config.get('ollama', {}).get('model', 'llama3.1')
        prompt = f"""You are an expert Java programming tutor.

STUDENT CONTEXT:
- Question: {student_data.get('question', 'Help with code')}
- Code: {str(student_data.get('code', 'N/A'))[:300]}
- Error: {student_data.get('error_message', 'None')}

STUDENT PROFILE:
- Learning Style: {student_profile.get('learning_style', {}).get('visual_verbal', 'visual')}
- Mastery: {adaptive_result.get('prior_knowledge', {}).get('average_mastery', 0.5):.0%}

BASE EXPLANATION:
{base_explanation}

Enhance this explanation:
1. More personalized to the student's learning style
2. Clearer and more encouraging
3. Include a concrete Java example
4. Address their specific question

Enhanced explanation:"""
        try:
            resp = requests.post(
                f"{ollama_url}/api/generate",
                json={"model": ollama_model, "prompt": prompt, "stream": False},
                timeout=300,
            )
            resp.raise_for_status()
            return resp.json().get("response", base_explanation).strip()
        except Exception as e:
            print(f"[WARN] Ollama enhancement error: {e}")
            return base_explanation

    def _calculate_complete_metrics(self, session_data: Dict, adaptive_result: Dict,
                                   cognitive_assessment: Dict, behavioral_analysis: Dict,
                                   student_profile: Dict, knowledge_gaps: List[Dict]) -> Dict:
        """
        Calculate complete quantitative and qualitative metrics using REAL models
        - CodeBERT for code analysis
        - BERT for text quality
        - Real time tracking
        """
        import time
        
        # DINA Mastery - DYNAMIC CALCULATION
        prior_knowledge = adaptive_result.get('prior_knowledge', {})
        previous_overall_mastery = prior_knowledge.get('average_mastery', 0.5)
        
        # Get previous mastery from state tracker
        student_id = session_data.get('student_id', 'unknown')
        if self.state_tracker:
            student_state = self.state_tracker.get_student_state(student_id)
            knowledge_state = student_state.get('knowledge_state', {})
            mastery_history = knowledge_state.get('mastery_history', [])
            if mastery_history:
                previous_overall_mastery = mastery_history[-1].get('overall_mastery', previous_overall_mastery)
        
        # Calculate current mastery based on code correctness and errors
        code_correctness = session_data.get('code_correctness', 0.5)
        error_message = session_data.get('error_message', '')
        
        # Adjust mastery based on performance
        mastery_delta = 0.0
        if code_correctness > 0.8:
            mastery_delta = 0.05  # Good performance
        elif code_correctness > 0.6:
            mastery_delta = 0.02  # Moderate performance
        elif code_correctness < 0.5 or error_message:
            mastery_delta = -0.03  # Poor performance or error
        
        current_overall_mastery = max(0.0, min(1.0, previous_overall_mastery + mastery_delta))
        
        # Update concept-specific mastery
        concept_mastery = prior_knowledge.get('mastery_scores', {}).copy()
        if not concept_mastery:
            # Initialize from knowledge gaps
            knowledge_gaps = adaptive_result.get('knowledge_gaps', [])
            for gap in knowledge_gaps:
                concept = gap.get('concept', '')
                if concept:
                    concept_mastery[concept] = gap.get('mastery', 0.5)
        
        # Update concept mastery based on performance
        for concept in concept_mastery:
            if code_correctness > 0.8:
                concept_mastery[concept] = min(1.0, concept_mastery[concept] + 0.05)
            elif code_correctness < 0.5:
                concept_mastery[concept] = max(0.0, concept_mastery[concept] - 0.03)
        
        dina_mastery = {
            "overall_mastery": current_overall_mastery,
            "concept_specific_mastery": concept_mastery,
            "strong_areas": [c for c, m in concept_mastery.items() if m >= 0.7],
            "weak_areas": [c for c, m in concept_mastery.items() if m < 0.5],
            "mastery_delta": mastery_delta
        }
        
        # [OK] REAL CodeBERT Analysis (using actual model)
        code = session_data.get("code", "")
        if self.metrics_calculator:
            codebert_analysis = self.metrics_calculator.calculate_codebert_analysis(code)
            print(f"[Metrics] [OK] CodeBERT analysis: correctness={codebert_analysis.get('correctness_score', 0):.2f}")
        else:
            # Fallback if calculator not available
            codebert_analysis = {
                "syntax_errors": abs(code.count("(") - code.count(")")),
                "logic_errors": 1 if "recursion" in code.lower() and "base" not in code.lower() else 0,
                "total_errors": 0,
                "correctness_score": 0.8,
                "code_quality": "needs_improvement",
                "model_used": "fallback",
                "analysis_method": "simple_heuristics"
            }
        
        # [OK] REAL BERT Explanation Quality (using actual model)
        explanation = adaptive_result.get('explanation', '')
        if self.metrics_calculator:
            bert_quality = self.metrics_calculator.calculate_bert_quality(explanation)
            print(f"[Metrics] [OK] BERT quality: score={bert_quality.get('quality_score', 0):.2f}")
        else:
            # Fallback if calculator not available
            words = explanation.lower().split()
            completeness = min(1.0, len([w for w in words if any(k in w for k in ["because", "reason", "why", "how", "explain"])]) / max(len(words), 1) * 10)
            clarity = min(1.0, len([w for w in words if any(k in w for k in ["clear", "simple", "step", "example"])]) / max(len(words), 1) * 10)
            bert_quality = {
                "quality_score": (completeness * 0.4 + clarity * 0.4 + (min(1.0, len(words) / 300) if len(words) >= 50 else len(words) / 50) * 0.2),
                "completeness": completeness,
                "clarity": clarity,
                "key_points_covered": int(completeness * 5),
                "model_used": "fallback",
                "analysis_method": "simple_heuristics"
            }
        
        # [OK] REAL Time Tracking (using actual timestamps)
        student_id = session_data.get('student_id', 'unknown')
        start_time = self.session_start_times.get(student_id)
        if self.metrics_calculator:
            time_tracking = self.metrics_calculator.calculate_time_tracking(session_data, start_time)
            print(f"[Metrics] [OK] Time tracking: duration={time_tracking.get('turn_duration_seconds', 0):.2f}s")
        else:
            # Fallback: calculate from time_deltas
            time_deltas = session_data.get('time_deltas', [])
            duration_seconds = sum(time_deltas) if time_deltas else 2.5
            time_tracking = {
                "turn_duration_seconds": float(duration_seconds),
                "turn_duration_minutes": float(duration_seconds / 60.0),
                "time_stuck_seconds": float(session_data.get('time_stuck', 0)),
                "calculation_method": "time_deltas"
            }
        
        # Nestor Profile
        nestor_profile = {
            "personality": student_profile.get('personality', {}),
            "learning_style": student_profile.get('learning_style', {}),
            "learning_strategy": adaptive_result.get('learning_style_adaptation', {}).get('order', 'systematic')
        }
        
        # COKE Analysis
        coke_analysis = {
            "cognitive_state": behavioral_analysis.get('emotion', 'engaged') if behavioral_analysis else 'engaged',
            "confidence": 0.8,
            "behavioral_response": "continue"
        }
        
        return {
            "quantitative": {
                "dina_mastery": dina_mastery,
                "codebert_analysis": codebert_analysis,
                "bert_explanation_quality": bert_quality,
                "time_tracking": time_tracking,
                "knowledge_graphs_used": adaptive_result.get('knowledge_graphs_used', {}),
                "nestor_profile": nestor_profile,
                "coke_analysis": coke_analysis
            },
            "qualitative": {
                "explanation_style": adaptive_result.get('strategy', 'scaffold_gradually'),
                "complexity_level": adaptive_result.get('complexity', 3),
                "personalization_factors": adaptive_result.get('personalization_factors', {}),
                "cognitive_state": coke_analysis['cognitive_state'],
                "learning_style": nestor_profile['learning_style']
            }
        }
    
    def _prepare_batch(self, session_data: Dict) -> Dict:
        """Prepare batch for HVSAE with proper tokenization"""
        from transformers import AutoTokenizer
        
        # Get code and error message
        code = session_data.get('code', '')
        error_message = session_data.get('error_message', '')
        
        # Tokenize code (CodeBERT)
        try:
            code_tokenizer = AutoTokenizer.from_pretrained('microsoft/codebert-base')
            code_tokens = code_tokenizer(
                code if code else 'def function(): pass',
                return_tensors='pt',
                padding=True,
                truncation=True,
                max_length=512
            )
        except Exception as e:
            print(f"[WARN] Code tokenization failed: {e}")
            code_tokens = {'input_ids': torch.zeros(1, 10, dtype=torch.long)}
        
        # Tokenize text (BERT)
        try:
            text_tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
            text_tokens = text_tokenizer(
                error_message if error_message else 'No error',
                return_tensors='pt',
                padding=True,
                truncation=True,
                max_length=256
            )
        except Exception as e:
            print(f"[WARN] Text tokenization failed: {e}")
            text_tokens = {'input_ids': torch.zeros(1, 10, dtype=torch.long)}
        
        # Prepare action sequence
        action_sequence = session_data.get('action_sequence', [])
        if not action_sequence:
            action_sequence = ['code_edit']
        
        # Convert actions to IDs
        action_ids = [self._action_to_id(a) for a in action_sequence[:10]]
        while len(action_ids) < 10:
            action_ids.append(0)  # Pad with 0
        
        # Prepare time deltas — COPY the list so padding here doesn't mutate
        # session_data for downstream consumers (e.g. _analyze_behavior).
        time_deltas = list(session_data.get('time_deltas') or [])
        if not time_deltas:
            time_deltas = [1.0] * len(action_ids)
        while len(time_deltas) < 10:
            time_deltas.append(1.0)
        
        # HVSAE.forward expects raw tensors (it calls .numel() on them),
        # not HuggingFace BatchEncoding objects — unwrap to input_ids here.
        code_ids = code_tokens['input_ids'] if hasattr(code_tokens, '__getitem__') else code_tokens
        text_ids = text_tokens['input_ids'] if hasattr(text_tokens, '__getitem__') else text_tokens

        # HuggingFace tokenizers emit IDs up to ~50k, but HVSAE was trained with
        # its own smaller vocabularies (code_vocab_size, text_vocab_size). Map
        # HF token IDs into the HVSAE vocab range via modulo so the embedding
        # lookup is always in-bounds.
        hv_cfg = self.config.get('hvsae', {})
        code_vocab = int(hv_cfg.get('code_vocab_size', 8000))
        text_vocab = int(hv_cfg.get('text_vocab_size', 6000))
        code_ids = code_ids.long() % code_vocab
        text_ids = text_ids.long() % text_vocab

        return {
            'code_tokens': code_ids,
            'text_tokens': text_ids,
            'action_sequence': torch.tensor([action_ids], dtype=torch.long),
            'timestamps': torch.tensor([[t] for t in time_deltas[:10]], dtype=torch.float).unsqueeze(0),
            'sequence_lengths': torch.tensor([min(len(action_sequence), 10)])
        }
    
    def _get_personality_profile(self, student_id: str, session_data: Dict) -> Dict:
        """
        Get or infer personality profile using Nestor Bayesian Network
        Uses bayesnestor for improved personality inference
        """
        # Check if we have stored profile
        if student_id in self.session_history:
            stored = self.session_history[student_id].get('personality', {})
            if stored:
                return stored
        
        # Try Nestor Bayesian Profiler first (better accuracy)
        nestor_profiler = self.models.get('nestor_profiler')
        if nestor_profiler:
            # Extract behavioral data from session
            behavioral_data = self._extract_behavioral_data_for_nestor(session_data, student_id)
            
            # Complete Nestor inference pipeline
            nestor_result = nestor_profiler.complete_inference(behavioral_data)
            
            # Store for future use
            if student_id:
                if student_id not in self.session_history:
                    self.session_history[student_id] = {}
                self.session_history[student_id]['personality'] = nestor_result['personality']
                self.session_history[student_id]['learning_styles'] = nestor_result['learning_styles']
                self.session_history[student_id]['nestor_inference'] = nestor_result
            
            print(f"[Nestor] [OK] Personality inferred using Bayesian Network")
            return nestor_result['personality']
        
        # Fix 4: Fallback uses _extract_behavioral_data_for_nestor which computes
        # REAL behavioral indicators from action sequences, time deltas, and code
        # structure — no more hardcoded 0.5/0.6/0.7 stubs.
        profiler = self.models.get('personality_profiler')
        behavioral_data = self._extract_behavioral_data_for_nestor(session_data, student_id)
        if profiler:
            return profiler.infer_from_behavior(behavioral_data)
        # Derive a minimal personality dict from behavioral_data directly
        org   = behavioral_data.get('organization',    0.5)
        pers  = behavioral_data.get('persistence',     0.5)
        expl  = behavioral_data.get('exploration_rate',0.5)
        return {
            'conscientiousness': round((org + pers) / 2, 2),
            'openness':          round(expl, 2),
            'learning_style':    'visual_sequential' if org > 0.6 else 'exploratory',
            'cognitive_style':   'systematic'        if pers > 0.6 else 'exploratory',
            'learning_preference': 'conceptual'      if expl < 0.4 else 'practical',
        }
    
    def _extract_behavioral_data_for_nestor(self, session_data: Dict, student_id: str) -> Dict:
        """
        Extract behavioral data for Nestor inference
        Combines session data with historical patterns
        """
        action_sequence = session_data.get('action_sequence', [])
        time_deltas = session_data.get('time_deltas', [])
        code = session_data.get('code', '')
        
        # Compute behavioral indicators
        behavioral_data = {}
        
        # Exploration rate: How many different actions tried
        unique_actions = len(set(action_sequence))
        total_actions = len(action_sequence)
        behavioral_data['exploration_rate'] = min(1.0, unique_actions / max(total_actions, 1))
        
        # Persistence: Time spent before giving up
        total_time = sum(time_deltas) if time_deltas else 0
        time_stuck = session_data.get('time_stuck', 0)
        behavioral_data['persistence'] = min(1.0, (total_time + time_stuck) / 300.0)  # Normalize to 5 minutes
        
        # Organization: Code structure quality (simplified)
        # Count indentation consistency, function definitions, etc.
        lines = code.split('\n') if code else []
        indented_lines = sum(1 for line in lines if line.strip().startswith((' ', '\t')))
        behavioral_data['organization'] = min(1.0, indented_lines / max(len(lines), 1))
        
        # Social interaction: Frequency of help-seeking
        help_actions = ['ask_question', 'search_documentation', 'help', 'question']
        help_count = sum(1 for action in action_sequence if any(h in str(action).lower() for h in help_actions))
        behavioral_data['social_interaction'] = min(1.0, help_count / max(total_actions, 1))
        
        # Emotional variability: Variance in time between actions
        if len(time_deltas) > 1:
            behavioral_data['emotional_variability'] = min(1.0, np.std(time_deltas) / 30.0)  # Normalize
        else:
            behavioral_data['emotional_variability'] = 0.5
        
        # Add historical data if available
        if student_id in self.session_history:
            history = self.session_history[student_id]
            # Average with historical patterns
            if 'behavioral_patterns' in history:
                hist = history['behavioral_patterns']
                behavioral_data['exploration_rate'] = (behavioral_data['exploration_rate'] + hist.get('exploration_rate', 0.5)) / 2
                behavioral_data['persistence'] = (behavioral_data['persistence'] + hist.get('persistence', 0.5)) / 2
                behavioral_data['organization'] = (behavioral_data['organization'] + hist.get('organization', 0.5)) / 2
        
        return behavioral_data
    
    def _infer_learning_style(self, session_data: Dict) -> Dict:
        """
        DYNAMIC LEARNING STYLE INFERENCE
        Infers learning style from multiple sources:
        1. Stored profile (if available)
        2. Behavioral patterns (action sequences)
        3. Chat text analysis (NLP keywords)
        4. Combines with confidence weights
        """
        student_id = session_data.get('student_id')
        
        # 1. Check if stored in session history (persistent profile)
        if student_id and student_id in self.session_history:
            stored = self.session_history[student_id].get('learning_style')
            if stored and any(stored.values()):  # If we have valid stored data
                print(f"[LearningStyle] Using stored profile for {student_id}")
                return stored
        
        # 2. Infer from behavior (action patterns)
        behavioral_style = self._infer_learning_style_from_behavior(session_data)
        
        # 3. Infer from chat text (NLP keywords)
        chat_style = self._infer_learning_style_from_chat(session_data)
        
        # 4. Combine with confidence weights (behavior > chat if both available)
        final_style = {}
        
        for dimension in ['visual_verbal', 'active_reflective', 'sequential_global']:
            # Prefer behavioral inference (more reliable), fallback to chat
            if behavioral_style.get(dimension):
                final_style[dimension] = behavioral_style[dimension]
            elif chat_style.get(dimension):
                final_style[dimension] = chat_style[dimension]
            else:
                # Ultimate fallback: neutral defaults
                defaults = {
                    'visual_verbal': 'visual',
                    'active_reflective': 'active',
                    'sequential_global': 'sequential'
                }
                final_style[dimension] = defaults[dimension]
        
        # Store for future use
        if student_id:
            if student_id not in self.session_history:
                self.session_history[student_id] = {}
            self.session_history[student_id]['learning_style'] = final_style
        
        print(f"[LearningStyle] Inferred: {final_style}")
        return final_style
    
    def _infer_learning_style_from_behavior(self, session_data: Dict) -> Dict:
        """
        Infer learning style from behavioral patterns (action sequences).
        Uses rule-based Felder-Silverman mapping from observed actions — no
        separate LearningStyleAssessor module needed.
        """
        try:
            action_sequence = session_data.get('action_sequence', [])
            time_deltas = session_data.get('time_deltas', [])
            code = session_data.get('code', '')
            
            # Analyze action patterns
            action_str = ' '.join(str(a).lower() for a in action_sequence)
            
            # Visual vs Verbal: Check for visualization/debugger usage
            uses_visualization = any(keyword in action_str for keyword in [
                'debugger', 'visual', 'diagram', 'graph', 'plot', 'visualize',
                'breakpoint', 'inspect', 'watch'
            ]) or 'print' not in action_str  # If they don't use print, might prefer visual
            
            # Active vs Reflective: Time before first run
            time_before_first_run = 60  # Default
            if time_deltas and len(time_deltas) > 0:
                # Time from start to first 'run' or 'test' action
                for i, action in enumerate(action_sequence):
                    if 'run' in str(action).lower() or 'test' in str(action).lower() or 'execute' in str(action).lower():
                        time_before_first_run = sum(time_deltas[:i]) if i < len(time_deltas) else 60
                        break
            
            # Sequential vs Global: Check fix pattern
            # Sequential: Fix errors one-by-one (incremental)
            # Global: Refactor whole code (big changes)
            incremental_fixes = True  # Default
            if len(action_sequence) > 2:
                # Count how many times they edit then run (incremental)
                edit_run_pairs = 0
                for i in range(len(action_sequence) - 1):
                    if 'edit' in str(action_sequence[i]).lower() or 'code' in str(action_sequence[i]).lower():
                        if 'run' in str(action_sequence[i+1]).lower() or 'test' in str(action_sequence[i+1]).lower():
                            edit_run_pairs += 1
                
                # If many edit-run pairs, they're incremental (sequential)
                # If few but large code changes, they're global
                incremental_fixes = edit_run_pairs > len(action_sequence) * 0.3
            
            # Rule-based Felder-Silverman mapping from the observed signals.
            inferred = {
                'visual_verbal':
                    'visual' if uses_visualization else 'verbal',
                'active_reflective':
                    'reflective' if time_before_first_run > 120 else 'active',
                'sequential_global':
                    'sequential' if incremental_fixes else 'global',
            }
            print(f"[LearningStyle] Behavioral inference: {inferred}")
            return inferred

        except Exception as e:
            print(f"[LearningStyle] Behavioral inference failed: {e}")
            return {}
    
    def _infer_learning_style_from_chat(self, session_data: Dict) -> Dict:
        """
        Infer learning style from chat text using NLP keyword analysis
        """
        conversation = session_data.get('conversation', [])
        question = session_data.get('question', '')
        error = session_data.get('error_message', '')
        
        # Combine all text
        text = f"{question} {' '.join(str(c) for c in conversation)} {error}".lower()
        
        if not text.strip():
            return {}
        
        styles = {}
        
        # 1. Visual vs Verbal
        visual_keywords = ['diagram', 'picture', 'visual', 'see', 'show', 'draw', 'image', 
                          'chart', 'graph', 'illustration', 'watch', 'look', 'view']
        verbal_keywords = ['explain', 'tell', 'describe', 'words', 'text', 'read', 'say',
                          'write', 'documentation', 'article', 'book', 'paragraph']
        
        visual_score = sum(1 for word in visual_keywords if word in text)
        verbal_score = sum(1 for word in verbal_keywords if word in text)
        
        if visual_score > verbal_score:
            styles['visual_verbal'] = 'visual'
        elif verbal_score > visual_score:
            styles['visual_verbal'] = 'verbal'
        # If tie, leave empty (will use behavior or default)
        
        # 2. Active vs Reflective
        active_keywords = ['try', 'do', 'practice', 'test', 'run', 'execute', 'code',
                          'implement', 'build', 'create', 'make', 'write code']
        reflective_keywords = ['think', 'understand', 'analyze', 'consider', 'plan',
                             'reason', 'logic', 'concept', 'theory', 'why', 'how']
        
        active_score = sum(1 for word in active_keywords if word in text)
        reflective_score = sum(1 for word in reflective_keywords if word in text)
        
        if active_score > reflective_score:
            styles['active_reflective'] = 'active'
        elif reflective_score > active_score:
            styles['active_reflective'] = 'reflective'
        
        # 3. Sequential vs Global
        sequential_keywords = ['step', 'first', 'then', 'next', 'order', 'sequence',
                              'one by one', 'step by step', 'in order', 'after', 'before']
        global_keywords = ['overall', 'big picture', 'whole', 'general', 'concept',
                          'entire', 'complete', 'all at once', 'together', 'overview']
        
        sequential_score = sum(1 for word in sequential_keywords if word in text)
        global_score = sum(1 for word in global_keywords if word in text)
        
        if sequential_score > global_score:
            styles['sequential_global'] = 'sequential'
        elif global_score > sequential_score:
            styles['sequential_global'] = 'global'
        
        if styles:
            print(f"[LearningStyle] Chat inference: {styles}")
        return styles
    
    def _action_to_id(self, action: str) -> int:
        """Convert action name to ID using the canonical ProgSnap2 map."""
        from src.models.behavioral import ACTION_MAP
        return ACTION_MAP.get(str(action).lower(), 4)  # default: edit (matches BehavioralRNN)
    
    def _get_recent_interventions(self, student_id: str) -> List[str]:
        """Get recent interventions for student"""
        if student_id not in self.session_history:
            return []
        
        history = self.session_history[student_id].get('interventions', [])
        return [i['type'] for i in history[-5:]]
    
    def _record_session(self, student_id: str, session_data: Dict,
                       intervention: Dict, content: Dict):
        """Record session for history"""
        if student_id not in self.session_history:
            self.session_history[student_id] = {}
        # Other code paths (e.g. update_student_profile) may have created the
        # entry without these keys — set them defensively.
        self.session_history[student_id].setdefault('interventions', [])
        self.session_history[student_id].setdefault('sessions', [])

        self.session_history[student_id]['interventions'].append({
            'type': intervention['type'],
            'timestamp': datetime.now(),
            'priority': intervention['priority']
        })
        
        self.session_history[student_id]['sessions'].append({
            'timestamp': datetime.now(),
            'code': session_data.get('code', ''),
            'intervention': intervention['type']
        })
    
    def record_outcome(self, student_id: str, intervention_type: str, 
                      effectiveness: float):
        """Record intervention outcome for learning"""
        recommender = self.models.get('intervention_recommender')
        if recommender:
            recommender.record_outcome(intervention_type, effectiveness)
    
    # === Helper Methods for Hierarchical RL ===
    
    def _infer_student_type(self, psychological: Dict, behavioral: Dict) -> str:
        """Infer student type from assessments"""
        emotion = behavioral.get('emotion', 'neutral')
        mastery_avg = 0.5  # Would calculate from cognitive assessment
        conscientiousness = psychological.get('personality', {}).get('conscientiousness', 0.5)
        
        if emotion == 'confused' and mastery_avg < 0.3:
            if conscientiousness > 0.7:
                return "systematic_beginner"
            else:
                return "chaotic_beginner"
        elif emotion == 'frustrated':
            return "frustrated_struggling"
        elif emotion == 'engaged' and mastery_avg > 0.6:
            return "engaged_intermediate"
        else:
            return "systematic_beginner"  # Default
    
    def _calculate_overall_progress(self, student_id: str) -> float:
        """Calculate student's overall progress"""
        if student_id not in self.session_history:
            return 0.0
        
        sessions = self.session_history[student_id].get('sessions', [])
        return min(len(sessions) / 100, 1.0)  # Simplified
    
    def _get_completed_concepts(self, student_id: str) -> List[str]:
        """Get list of completed concepts"""
        # Would track from DINA or history
        return []
    
    def _get_learning_goals(self, student_id: str) -> List[str]:
        """Get student's learning goals"""
        # Would be stored in profile
        return ["master_current_concept"]
    
    def _extract_concept(self, session_data: Dict) -> str:
        """Extract concept from session"""
        return session_data.get('problem_id', 'unknown')
    
    def _get_average_mastery(self, cognitive_assessment: Dict) -> float:
        """Get average mastery level"""
        mastery_profile = cognitive_assessment.get('mastery_profile', {})
        if not mastery_profile:
            return 0.5
        return np.mean(list(mastery_profile.values()))
    
    def _classify_behavior_pattern(self, behavioral_analysis: Dict) -> str:
        """Classify behavioral pattern"""
        effectiveness = behavioral_analysis.get('effectiveness', 0.5)
        if effectiveness > 0.7:
            return "systematic_effective"
        elif effectiveness > 0.4:
            return "systematic_struggling"
        else:
            return "random_exploration"
    
    def _estimate_dropout_risk(self, behavioral_analysis: Dict) -> float:
        """Estimate dropout risk"""
        emotion = behavioral_analysis.get('emotion', 'neutral')
        if emotion == 'frustrated':
            return 0.75
        elif emotion == 'confused':
            return 0.35
        else:
            return 0.15
    
    def _get_session_history(self, student_id: str) -> List:
        """Get student's session history"""
        if student_id not in self.session_history:
            return []
        return self.session_history[student_id].get('sessions', [])

