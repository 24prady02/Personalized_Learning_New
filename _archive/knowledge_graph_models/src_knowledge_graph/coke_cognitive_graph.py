"""
COKE: Cognitive Knowledge Graph for Machine Theory of Mind
Based on: ACL 2024 - "COKE: A Cognitive Knowledge Graph for Machine Theory of Mind"

Models human mental activities and subsequent behavioral/affective responses
Formalizes Theory of Mind as cognitive chains
"""

import torch
import torch.nn as nn
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import networkx as nx
import json
from pathlib import Path


class CognitiveState(Enum):
    """Cognitive states in COKE framework"""
    PERCEIVING = "perceiving"
    BELIEVING = "believing"
    DESIRING = "desiring"
    INTENDING = "intending"
    KNOWING = "knowing"
    UNDERSTANDING = "understanding"
    CONFUSED = "confused"
    INSIGHT = "insight"
    FRUSTRATED = "frustrated"
    ENGAGED = "engaged"


class BehavioralResponse(Enum):
    """Behavioral responses in COKE framework"""
    ASK_QUESTION = "ask_question"
    SEARCH_INFO = "search_info"
    TRY_AGAIN = "try_again"
    GIVE_UP = "give_up"
    CONTINUE = "continue"
    EXPLAIN = "explain"
    HELP_OTHERS = "help_others"
    COLLABORATE = "collaborate"


@dataclass
class CognitiveChain:
    """
    Cognitive chain: Mental activity → Behavioral/Affective response
    Based on COKE framework
    """
    id: str
    mental_activity: CognitiveState
    context: str  # Social/learning context
    behavioral_response: BehavioralResponse
    affective_response: Optional[str] = None
    confidence: float = 0.5
    frequency: float = 0.0  # How often this chain occurs


class COKECognitiveGraph:
    """
    COKE: Cognitive Knowledge Graph for Machine Theory of Mind
    
    Models:
    - Cognitive states (perceiving, believing, understanding, etc.)
    - Cognitive chains (mental activity → behavioral response)
    - Theory of Mind (predicting student mental states)
    """
    
    def __init__(self, config: Dict):
        """
        Args:
            config: Configuration dictionary
        """
        self.config = config
        
        # Graph structure (NetworkX)
        self.cognitive_graph = nx.MultiDiGraph()
        
        # Cognitive chains database
        self.cognitive_chains: Dict[str, CognitiveChain] = {}
        
        # State transition probabilities
        self.state_transitions: Dict[Tuple[CognitiveState, CognitiveState], float] = {}
        
        # Load or initialize cognitive chains (learned data takes priority)
        self._load_or_initialize_cognitive_chains()
        self._build_cognitive_graph()
    
    def _load_or_initialize_cognitive_chains(self):
        """Load learned cognitive chains or initialize with defaults"""
        # Try to load learned chains first
        data_dir = Path(self.config.get('pedagogical_kg', {}).get('data_dir', 'data/pedagogical_kg'))
        chains_file = data_dir / "coke_chains.json"
        
        if chains_file.exists():
            try:
                with open(chains_file, 'r', encoding='utf-8') as f:
                    chains_data = json.load(f)
                    learned_count = 0
                    for chain_data in chains_data:
                        # Map string enums to actual enums
                        mental_activity = CognitiveState(chain_data.get("mental_activity", "engaged"))
                        behavioral_response = BehavioralResponse(chain_data.get("behavioral_response", "continue"))
                        
                        chain = CognitiveChain(
                            id=chain_data.get("id", f"chain_{mental_activity.value}_to_{behavioral_response.value}"),
                            mental_activity=mental_activity,
                            context=chain_data.get("context", "working_on_problem"),
                            behavioral_response=behavioral_response,
                            affective_response=chain_data.get("affective_response"),
                            confidence=chain_data.get("confidence", 0.5),
                            frequency=chain_data.get("frequency", 0.0)
                        )
                        self.cognitive_chains[chain.id] = chain
                        learned_count += 1
                    print(f"[COKE] Loaded {learned_count} cognitive chains from learned data")
                    return
            except Exception as e:
                print(f"[COKE] Error loading learned chains: {e}, using defaults")
        
        # Fallback to hardcoded defaults
        print("[COKE] No learned cognitive chains found, using hardcoded defaults")
        self._initialize_default_cognitive_chains()
    
    def _initialize_default_cognitive_chains(self):
        """Initialize cognitive chains based on COKE framework (hardcoded defaults)"""
        # Common cognitive chains for programming education
        default_chains = [
            {
                "id": "chain_confused_to_ask",
                "mental_activity": CognitiveState.CONFUSED,
                "context": "encountering_error",
                "behavioral_response": BehavioralResponse.ASK_QUESTION,
                "affective_response": "frustrated",
                "confidence": 0.8,
                "frequency": 0.6
            },
            {
                "id": "chain_understanding_to_continue",
                "mental_activity": CognitiveState.UNDERSTANDING,
                "context": "solved_problem",
                "behavioral_response": BehavioralResponse.CONTINUE,
                "affective_response": "engaged",
                "confidence": 0.9,
                "frequency": 0.7
            },
            {
                "id": "chain_insight_to_explain",
                "mental_activity": CognitiveState.INSIGHT,
                "context": "gained_understanding",
                "behavioral_response": BehavioralResponse.EXPLAIN,
                "affective_response": "satisfied",
                "confidence": 0.75,
                "frequency": 0.5
            },
            {
                "id": "chain_frustrated_to_search",
                "mental_activity": CognitiveState.FRUSTRATED,
                "context": "stuck_on_problem",
                "behavioral_response": BehavioralResponse.SEARCH_INFO,
                "affective_response": "determined",
                "confidence": 0.7,
                "frequency": 0.65
            },
            {
                "id": "chain_engaged_to_collaborate",
                "mental_activity": CognitiveState.ENGAGED,
                "context": "working_with_peers",
                "behavioral_response": BehavioralResponse.COLLABORATE,
                "affective_response": "motivated",
                "confidence": 0.8,
                "frequency": 0.55
            }
        ]
        
        for chain_data in default_chains:
            chain = CognitiveChain(
                id=chain_data["id"],
                mental_activity=chain_data["mental_activity"],
                context=chain_data["context"],
                behavioral_response=chain_data["behavioral_response"],
                affective_response=chain_data.get("affective_response"),
                confidence=chain_data["confidence"],
                frequency=chain_data["frequency"]
            )
            self.cognitive_chains[chain.id] = chain
        # End of _initialize_default_cognitive_chains
    
    def _build_cognitive_graph(self):
        """Build cognitive knowledge graph structure"""
        # Add cognitive state nodes
        for state in CognitiveState:
            self.cognitive_graph.add_node(
                state.value,
                type="cognitive_state",
                state=state
            )
        
        # Add behavioral response nodes
        for response in BehavioralResponse:
            self.cognitive_graph.add_node(
                response.value,
                type="behavioral_response",
                response=response
            )
        
        # Add cognitive chains as edges
        for chain in self.cognitive_chains.values():
            self.cognitive_graph.add_edge(
                chain.mental_activity.value,
                chain.behavioral_response.value,
                chain_id=chain.id,
                context=chain.context,
                confidence=chain.confidence,
                frequency=chain.frequency,
                relation="cognitive_chain"
            )
        
        # Add state transition edges (based on learning progression)
        transitions = [
            (CognitiveState.CONFUSED, CognitiveState.UNDERSTANDING, 0.6),
            (CognitiveState.UNDERSTANDING, CognitiveState.KNOWING, 0.7),
            (CognitiveState.KNOWING, CognitiveState.INSIGHT, 0.5),
            (CognitiveState.FRUSTRATED, CognitiveState.ENGAGED, 0.4),
            (CognitiveState.PERCEIVING, CognitiveState.BELIEVING, 0.8),
            (CognitiveState.BELIEVING, CognitiveState.INTENDING, 0.6)
        ]
        
        for from_state, to_state, prob in transitions:
            self.cognitive_graph.add_edge(
                from_state.value,
                to_state.value,
                relation="state_transition",
                probability=prob
            )
            self.state_transitions[(from_state, to_state)] = prob
    
    def predict_cognitive_state(self, student_data: Dict) -> CognitiveState:
        """
        Predict student's current cognitive state using Theory of Mind
        
        Extracts from:
        1. Conversation text (questions, statements)
        2. Code and errors
        3. Behavioral actions
        
        Args:
            student_data: Dictionary with student information
                - conversation: List of conversation messages
                - question: Student's question/text
                - code: Student's code
                - error_message: Error if any
                - action_sequence: Recent actions
                - time_stuck: Time spent stuck
                
        Returns:
            Predicted cognitive state
        """
        # ===== EXTRACT FROM CONVERSATION TEXT =====
        conversation_text = ""
        
        # Get conversation messages
        if "conversation" in student_data:
            conversation = student_data["conversation"]
            if isinstance(conversation, list):
                conversation_text = " ".join([
                    msg.get("content", "") or msg.get("text", "") or str(msg)
                    for msg in conversation
                    if isinstance(msg, dict)
                ])
            elif isinstance(conversation, str):
                conversation_text = conversation
        
        # Get question/text directly
        if "question" in student_data:
            conversation_text += " " + str(student_data["question"])
        if "text" in student_data:
            conversation_text += " " + str(student_data["text"])
        if "message" in student_data:
            conversation_text += " " + str(student_data["message"])
        
        conversation_lower = conversation_text.lower()
        
        # Analyze conversation for cognitive indicators
        confusion_indicators = [
            "i don't understand", "i don't get it", "confused", "what does",
            "how does", "why does", "not sure", "unclear", "don't know",
            "help me", "can you explain", "what is", "what's wrong",
            "i'm stuck", "doesn't work", "not working"
        ]
        
        frustration_indicators = [
            "frustrated", "annoying", "stupid", "hate", "give up",
            "this is hard", "too difficult", "impossible", "can't do",
            "tired", "exhausted", "waste of time"
        ]
        
        understanding_indicators = [
            "i see", "i understand", "got it", "makes sense", "ah",
            "now i get it", "clear", "that helps", "thanks"
        ]
        
        insight_indicators = [
            "oh!", "aha!", "eureka", "i see now", "that's it",
            "brilliant", "perfect", "exactly"
        ]
        
        engaged_indicators = [
            "interesting", "cool", "let me try", "i want to",
            "can i", "show me more", "tell me about"
        ]
        
        # Count indicators in conversation
        confusion_count = sum(1 for ind in confusion_indicators if ind in conversation_lower)
        frustration_count = sum(1 for ind in frustration_indicators if ind in conversation_lower)
        understanding_count = sum(1 for ind in understanding_indicators if ind in conversation_lower)
        insight_count = sum(1 for ind in insight_indicators if ind in conversation_lower)
        engaged_count = sum(1 for ind in engaged_indicators if ind in conversation_lower)
        
        # ===== EXTRACT FROM CODE/ERRORS =====
        has_error = bool(student_data.get("error_message"))
        time_stuck = student_data.get("time_stuck", 0)
        recent_actions = student_data.get("action_sequence", [])
        
        # ===== COMBINE CONVERSATION + CODE ANALYSIS =====
        
        # Priority: Conversation text analysis (most direct)
        if insight_count > 0:
            return CognitiveState.INSIGHT
        elif understanding_count > 0:
            return CognitiveState.UNDERSTANDING
        elif frustration_count > 0 or (has_error and time_stuck > 60):
            return CognitiveState.FRUSTRATED
        elif confusion_count > 0 or (has_error and time_stuck < 30):
            return CognitiveState.CONFUSED
        elif engaged_count > 0:
            return CognitiveState.ENGAGED
        elif not has_error and len(recent_actions) > 0:
            return CognitiveState.UNDERSTANDING
        elif "search" in str(recent_actions).lower():
            return CognitiveState.PERCEIVING
        else:
            return CognitiveState.ENGAGED
    
    def predict_behavioral_response(self, cognitive_state: CognitiveState,
                                   context: str) -> BehavioralResponse:
        """
        Predict behavioral response given cognitive state and context
        
        Args:
            cognitive_state: Current cognitive state
            context: Learning context
            
        Returns:
            Predicted behavioral response
        """
        # Find matching cognitive chain
        matching_chains = [
            chain for chain in self.cognitive_chains.values()
            if chain.mental_activity == cognitive_state
            and context in chain.context
        ]
        
        if matching_chains:
            # Return most frequent/confident chain
            best_chain = max(matching_chains, 
                           key=lambda c: c.confidence * c.frequency)
            return best_chain.behavioral_response
        
        # Default responses
        default_responses = {
            CognitiveState.CONFUSED: BehavioralResponse.ASK_QUESTION,
            CognitiveState.FRUSTRATED: BehavioralResponse.SEARCH_INFO,
            CognitiveState.UNDERSTANDING: BehavioralResponse.CONTINUE,
            CognitiveState.INSIGHT: BehavioralResponse.EXPLAIN,
            CognitiveState.ENGAGED: BehavioralResponse.CONTINUE
        }
        
        return default_responses.get(cognitive_state, BehavioralResponse.CONTINUE)
    
    def get_cognitive_chain(self, from_state: CognitiveState,
                          to_response: BehavioralResponse) -> Optional[CognitiveChain]:
        """Get cognitive chain between state and response"""
        for chain in self.cognitive_chains.values():
            if chain.mental_activity == from_state and \
               chain.behavioral_response == to_response:
                return chain
        return None
    
    def get_cognitive_chains_for_state(self, cognitive_state: CognitiveState) -> List[CognitiveChain]:
        """
        Get all cognitive chains for a given cognitive state
        
        Args:
            cognitive_state: The cognitive state to find chains for
            
        Returns:
            List of cognitive chains matching the state
        """
        matching_chains = [
            chain for chain in self.cognitive_chains.values()
            if chain.mental_activity == cognitive_state
        ]
        return matching_chains
    
    def get_state_transition_probability(self, from_state: CognitiveState,
                                       to_state: CognitiveState) -> float:
        """Get probability of transitioning between cognitive states"""
        return self.state_transitions.get((from_state, to_state), 0.0)
    
    def infer_theory_of_mind(self, student_data: Dict) -> Dict:
        """
        Infer student's Theory of Mind (mental state prediction)
        
        Extracts Theory of Mind from:
        1. Conversation text (questions, statements, emotions)
        2. Code and errors
        3. Behavioral patterns
        
        Args:
            student_data: Student information
                - conversation: List of messages or conversation text
                - question: Student's question
                - code: Student's code
                - error_message: Error if any
                - action_sequence: Recent actions
                - time_stuck: Time spent stuck
                
        Returns:
            Theory of Mind inference including:
            - Predicted cognitive state
            - Predicted behavioral response
            - Confidence
            - Reasoning (extracted from conversation)
            - Conversation_indicators: What was detected in conversation
        """
        # Extract conversation text
        conversation_text = ""
        if "conversation" in student_data:
            conv = student_data["conversation"]
            if isinstance(conv, list):
                conversation_text = " ".join([
                    msg.get("content", "") or msg.get("text", "") or str(msg)
                    for msg in conv if isinstance(msg, dict)
                ])
            else:
                conversation_text = str(conv)
        
        if "question" in student_data:
            conversation_text += " " + str(student_data["question"])
        
        # Predict cognitive state (now includes conversation analysis)
        cognitive_state = self.predict_cognitive_state(student_data)
        
        # Extract context from conversation
        context = student_data.get("context", "general")
        if conversation_text:
            if "error" in conversation_text.lower() or "wrong" in conversation_text.lower():
                context = "encountering_error"
            elif "help" in conversation_text.lower() or "explain" in conversation_text.lower():
                context = "seeking_help"
            elif "understand" in conversation_text.lower():
                context = "gained_understanding"
        
        # Predict behavioral response
        behavioral_response = self.predict_behavioral_response(cognitive_state, context)
        
        # Get cognitive chain
        chain = self.get_cognitive_chain(cognitive_state, behavioral_response)
        
        # Create reasoning from conversation
        reasoning_parts = []
        if conversation_text:
            reasoning_parts.append(f"From conversation: student expresses {cognitive_state.value}")
        else:
            reasoning_parts.append(f"Student is {cognitive_state.value}")
        
        reasoning_parts.append(f"likely to {behavioral_response.value}")
        
        result = {
            "cognitive_state": cognitive_state.value,
            "behavioral_response": behavioral_response.value,
            "confidence": chain.confidence if chain else 0.5,
            "reasoning": " | ".join(reasoning_parts),
            "cognitive_chain_id": chain.id if chain else None,
            "conversation_analyzed": bool(conversation_text),
            "extracted_from_conversation": conversation_text[:100] if conversation_text else None
        }
        
        # DYNAMIC LEARNING: Learn from this session
        self.learn_from_session(student_data, cognitive_state, behavioral_response, context)
        
        return result
    
    def learn_from_session(self, student_data: Dict, 
                          cognitive_state: CognitiveState,
                          behavioral_response: BehavioralResponse,
                          context: str):
        """
        DYNAMIC LEARNING: Learn cognitive chain from student session
        
        Updates or creates cognitive chain based on actual student behavior
        """
        # Find or create chain
        chain_id = f"chain_{cognitive_state.value}_to_{behavioral_response.value}"
        
        if chain_id in self.cognitive_chains:
            # Update existing chain (increase frequency, confidence)
            chain = self.cognitive_chains[chain_id]
            # Increment frequency slightly (exponential moving average)
            chain.frequency = min(1.0, chain.frequency * 0.99 + 0.01)
            # Increase confidence with more evidence
            chain.confidence = min(1.0, chain.confidence + 0.001)
        else:
            # Learn new chain
            chain = CognitiveChain(
                id=chain_id,
                mental_activity=cognitive_state,
                context=context,
                behavioral_response=behavioral_response,
                affective_response=self._get_affective_response(cognitive_state.value),
                confidence=0.5,  # Start with medium confidence
                frequency=0.01  # Start with low frequency
            )
            self.cognitive_chains[chain_id] = chain
            print(f"[COKE] Learned new cognitive chain: {chain_id}")
        
        # Rebuild graph with updated chains
        self._build_cognitive_graph()
        
        # Save learned chains periodically (every 10 sessions)
        if len(self.cognitive_chains) % 10 == 0:
            self._save_learned_chains()
    
    def _get_affective_response(self, cognitive_state: str) -> str:
        """Get affective response for cognitive state"""
        affective_map = {
            "confused": "frustrated",
            "frustrated": "determined",
            "understanding": "satisfied",
            "engaged": "motivated",
            "insight": "satisfied"
        }
        return affective_map.get(cognitive_state, "neutral")
    
    def _save_learned_chains(self):
        """Save learned cognitive chains to file"""
        try:
            data_dir = Path(self.config.get('pedagogical_kg', {}).get('data_dir', 'data/pedagogical_kg'))
            data_dir.mkdir(parents=True, exist_ok=True)
            chains_file = data_dir / "coke_chains.json"
            
            chains_data = []
            for chain in self.cognitive_chains.values():
                chains_data.append({
                    "id": chain.id,
                    "mental_activity": chain.mental_activity.value,
                    "context": chain.context,
                    "behavioral_response": chain.behavioral_response.value,
                    "affective_response": chain.affective_response,
                    "confidence": chain.confidence,
                    "frequency": chain.frequency
                })
            
            with open(chains_file, 'w', encoding='utf-8') as f:
                json.dump(chains_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[COKE] Error saving learned chains: {e}")

