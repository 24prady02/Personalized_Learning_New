"""
Reinforcement Learning Teaching Agent
Learns optimal teaching strategies through interaction
"""

import torch
import torch.nn as nn
import torch.optim as optim
from typing import Dict, List, Tuple, Optional
import numpy as np
from collections import deque
import random


class TeachingRLAgent:
    """
    RL Agent that learns to teach optimally
    
    Key Idea: Treat teaching as a sequential decision problem
    
    State: Student's knowledge state + emotional state + session context
    Action: Which intervention/teaching strategy to use
    Reward: Student's learning gain + engagement + long-term retention
    
    The agent learns: "For THIS type of student in THIS state, 
                       THAT intervention works best!"
    """
    
    def __init__(self, config: Dict, models: Dict):
        self.config = config
        self.models = models
        
        # State space
        self.state_dim = 512  # Latent representation + context
        
        # Action space (teaching decisions)
        self.actions = {
            0: "visual_explanation",
            1: "guided_practice", 
            2: "interactive_exercise",
            3: "conceptual_deepdive",
            4: "motivational_support",
            5: "worked_example",
            6: "peer_comparison",
            7: "spaced_review",
            8: "challenge_problem",
            9: "error_analysis"
        }
        self.num_actions = len(self.actions)
        
        # Policy network (decides which teaching action to take)
        self.policy_net = TeachingPolicyNetwork(
            state_dim=self.state_dim,
            num_actions=self.num_actions,
            hidden_dims=[256, 128]
        )
        
        # Target network (for stable learning)
        self.target_net = TeachingPolicyNetwork(
            state_dim=self.state_dim,
            num_actions=self.num_actions,
            hidden_dims=[256, 128]
        )
        self.target_net.load_state_dict(self.policy_net.state_dict())
        
        # Optimizer
        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=0.001)
        
        # Experience replay buffer
        self.memory = deque(maxlen=10000)
        self.batch_size = 32
        
        # Reward calculator
        from .reward_function import RewardCalculator
        self.reward_calculator = RewardCalculator(config)
        
        # Knowledge graph updater
        from .knowledge_graph_updater import DynamicKGUpdater
        self.kg_updater = DynamicKGUpdater(config, models)
        
        # Exploration parameters
        self.epsilon = 1.0  # Start with full exploration
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.1
        
        # Discount factor
        self.gamma = 0.95
        
        # Training step counter
        self.steps = 0
        self.target_update_frequency = 100

        # Auto-load trained checkpoint if one exists so the policy isn't random
        default_ckpt = config.get('rl', {}).get(
            'checkpoint', 'checkpoints/rl_teaching_agent.pt'
        )
        try:
            from pathlib import Path as _P
            if _P(default_ckpt).exists():
                self.load_checkpoint(default_ckpt)
        except Exception as _e:
            print(f"[RL] checkpoint auto-load skipped: {_e}")

    def get_state_representation(self, session_data: Dict,
                                 analysis: Dict) -> torch.Tensor:
        """
        Encode current situation into state vector
        
        State includes:
        - Student's latent representation (from HVSAE)
        - Knowledge gaps (from Student State Tracker)
        - Emotional state (from RNN)
        - Personality (from Personality Profiler)
        - Session context (time stuck, attempts, etc.)
        """
        
        # Get latent representation
        latent = analysis['encoding']['latent']  # [256-dim]
        
        # Encode knowledge gaps
        gaps = analysis['cognitive']['knowledge_gaps']
        gap_encoding = self._encode_gaps(gaps)  # [64-dim]
        
        # Encode emotional state
        emotion = analysis['behavioral']['emotional_state']
        emotion_encoding = self._encode_emotion(emotion)  # [32-dim]
        
        # Encode personality
        personality = analysis['psychological']['personality']
        personality_encoding = self._encode_personality(personality)  # [64-dim]
        
        # Encode session context
        context = {
            'time_stuck': session_data.get('time_stuck', 0),
            'attempts': len(session_data.get('action_sequence', [])),
            'help_requested': 1 if 'search' in str(session_data.get('action_sequence', [])) else 0,
            'previous_interventions': len(analysis.get('history', {}).get('interventions', []))
        }
        context_encoding = self._encode_context(context)  # [96-dim]
        
        # Concatenate all
        state = torch.cat([
            latent.flatten(),
            gap_encoding,
            emotion_encoding,
            personality_encoding,
            context_encoding
        ], dim=0)  # [512-dim]
        
        return state
    
    def select_action(self, state: torch.Tensor, 
                     training: bool = True) -> Tuple[int, float]:
        """
        Select teaching action using epsilon-greedy policy
        
        Args:
            state: Current state representation
            training: Whether in training mode (explore) or inference (exploit)
            
        Returns:
            (action_id, q_value)
        """
        
        # Epsilon-greedy exploration
        if training and random.random() < self.epsilon:
            # Explore: Random action
            action = random.randint(0, self.num_actions - 1)
            q_value = 0.0
        else:
            # Exploit: Best action according to policy
            with torch.no_grad():
                q_values = self.policy_net(state.unsqueeze(0))
                action = q_values.argmax(dim=1).item()
                q_value = q_values[0, action].item()
        
        return action, q_value
    
    def store_experience(self, state: torch.Tensor, action: int,
                        reward: float, next_state: torch.Tensor,
                        done: bool):
        """
        Store experience in replay buffer
        
        Experience = (state, action, reward, next_state, done)
        """
        self.memory.append((state, action, reward, next_state, done))
    
    def learn_from_experience(self):
        """
        Learn from stored experiences using Deep Q-Learning
        """
        
        if len(self.memory) < self.batch_size:
            return None  # Not enough experiences yet
        
        # Sample batch from memory
        batch = random.sample(self.memory, self.batch_size)

        # Defensive coerce: replay buffer loaded from checkpoint stores
        # state vectors as numpy.ndarray, while live chat-app stores
        # store them as torch.Tensor. torch.stack() requires uniform
        # type, so coerce both to float tensors here.
        def _as_tensor(x):
            if isinstance(x, torch.Tensor):
                return x.float()
            return torch.as_tensor(x, dtype=torch.float)
        states      = torch.stack([_as_tensor(exp[0]) for exp in batch])
        actions     = torch.tensor([exp[1] for exp in batch], dtype=torch.long)
        rewards     = torch.tensor([exp[2] for exp in batch], dtype=torch.float)
        next_states = torch.stack([_as_tensor(exp[3]) for exp in batch])
        dones       = torch.tensor([exp[4] for exp in batch], dtype=torch.float)
        
        # Current Q-values
        current_q_values = self.policy_net(states).gather(1, actions.unsqueeze(1))
        
        # Target Q-values (using target network)
        with torch.no_grad():
            next_q_values = self.target_net(next_states).max(1)[0]
            target_q_values = rewards + self.gamma * next_q_values * (1 - dones)
        
        # Compute loss
        loss = nn.functional.mse_loss(current_q_values.squeeze(), target_q_values)
        
        # Optimize
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.policy_net.parameters(), 1.0)
        self.optimizer.step()
        
        # Decay epsilon
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        
        # Update target network periodically
        self.steps += 1
        if self.steps % self.target_update_frequency == 0:
            self.target_net.load_state_dict(self.policy_net.state_dict())
        
        return loss.item()
    
    def process_feedback(self, session_data: Dict, 
                        action_taken: int,
                        student_response: Dict) -> float:
        """
        Process student's response and learn from it
        
        This is where RL learning happens!
        
        Args:
            session_data: Original session
            action_taken: Which intervention was used
            student_response: How student responded
            
        Returns:
            Reward value
        """
        
        # Calculate reward based on student outcome
        reward = self.reward_calculator.calculate_reward(
            session_data=session_data,
            action_taken=action_taken,
            student_response=student_response
        )
        
        print(f"\n🎯 RL LEARNING:")
        print(f"   Action taken: {self.actions[action_taken]}")
        print(f"   Reward received: {reward:.3f}")
        
        # Update knowledge graph based on outcome
        self.kg_updater.update_from_interaction(
            session_data=session_data,
            student_response=student_response,
            success=reward > 0.5
        )
        
        return reward
    
    def train_episode(self, session_data: Dict, analysis: Dict,
                     student_response: Dict) -> Dict:
        """
        Complete RL training episode
        
        Episode = One teaching interaction with student
        
        Returns:
            Training metrics
        """
        
        # Get current state
        state = self.get_state_representation(session_data, analysis)
        
        # Select action (teaching intervention)
        action, q_value = self.select_action(state, training=True)
        
        print(f"\n🤖 RL AGENT DECISION:")
        print(f"   Selected action: {self.actions[action]}")
        print(f"   Q-value: {q_value:.3f}")
        print(f"   Exploration rate: {self.epsilon:.3f}")
        
        # Student receives intervention and responds
        # (this happens in the real teaching session)
        
        # After student responds, calculate reward
        reward = self.process_feedback(session_data, action, student_response)
        
        # Get next state (after intervention)
        next_analysis = self._analyze_post_intervention(student_response)
        next_state = self.get_state_representation(session_data, next_analysis)
        
        # Check if episode is done
        done = student_response.get('mastery_achieved', False) or \
               student_response.get('gave_up', False)
        
        # Store experience
        self.store_experience(state, action, reward, next_state, done)
        
        # Learn from experience
        loss = self.learn_from_experience()
        
        # Update knowledge graph
        kg_updates = self.kg_updater.update_from_interaction(
            session_data, student_response, reward > 0.5
        )
        
        return {
            'action': self.actions[action],
            'reward': reward,
            'q_value': q_value,
            'loss': loss,
            'epsilon': self.epsilon,
            'kg_updates': kg_updates,
            'experiences_stored': len(self.memory)
        }
    
    def _encode_gaps(self, gaps: List[Dict]) -> torch.Tensor:
        """Encode knowledge gaps into vector"""
        # Simplified encoding
        gap_vector = torch.zeros(64)
        for i, gap in enumerate(gaps[:64]):
            gap_vector[i] = gap.get('mastery', 0.5)
        return gap_vector
    
    def _encode_emotion(self, emotion: str) -> torch.Tensor:
        """Encode emotional state"""
        emotions = ['frustrated', 'engaged', 'confused', 'systematic', 'exploratory']
        emotion_id = emotions.index(emotion) if emotion in emotions else 0
        encoding = torch.zeros(32)
        encoding[emotion_id] = 1.0
        return encoding
    
    def _encode_personality(self, personality: Dict) -> torch.Tensor:
        """Encode personality traits"""
        traits = ['openness', 'conscientiousness', 'extraversion', 'agreeableness', 'neuroticism']
        encoding = torch.tensor([personality.get(t, 0.5) for t in traits] * 13, dtype=torch.float)[:64]
        return encoding
    
    def _encode_context(self, context: Dict) -> torch.Tensor:
        """Encode session context"""
        encoding = torch.zeros(96)
        encoding[0] = min(context['time_stuck'] / 300, 1.0)  # Normalize
        encoding[1] = min(context['attempts'] / 10, 1.0)
        encoding[2] = context['help_requested']
        encoding[3] = min(context['previous_interventions'] / 5, 1.0)
        return encoding
    
    def _analyze_post_intervention(self, student_response: Dict) -> Dict:
        """Analyze student state after intervention"""
        # This would call the models again to get updated state
        return {
            'encoding': {'latent': torch.randn(256)},  # Placeholder
            'cognitive': student_response.get('cognitive', {}),
            'behavioral': student_response.get('behavioral', {}),
            'psychological': student_response.get('psychological', {})
        }
    
    def save_checkpoint(self, path: str):
        """Save RL agent checkpoint"""
        torch.save({
            'policy_net': self.policy_net.state_dict(),
            'target_net': self.target_net.state_dict(),
            'optimizer': self.optimizer.state_dict(),
            'epsilon': self.epsilon,
            'steps': self.steps,
            'memory': list(self.memory)
        }, path)
        print(f"✓ RL agent checkpoint saved: {path}")
    
    def load_checkpoint(self, path: str):
        """Load RL agent checkpoint"""
        checkpoint = torch.load(path, weights_only=False, map_location='cpu')
        self.policy_net.load_state_dict(checkpoint['policy_net'])
        self.target_net.load_state_dict(checkpoint['target_net'])
        self.optimizer.load_state_dict(checkpoint['optimizer'])
        self.epsilon = checkpoint['epsilon']
        self.steps = checkpoint['steps']
        self.memory = deque(checkpoint['memory'], maxlen=10000)
        print(f"[RL] checkpoint loaded: {path}  "
              f"(steps={self.steps}, eps={self.epsilon:.3f})")


class PolicyGradientAgent:
    """
    Alternative RL approach using Policy Gradient (REINFORCE)
    Sometimes better for continuous learning
    """
    
    def __init__(self, config: Dict):
        self.config = config
        
        self.state_dim = 512
        self.num_actions = 10
        
        # Policy network
        self.policy = TeachingPolicyNetwork(self.state_dim, self.num_actions)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=0.0003)
        
        # Episode storage
        self.episode_states = []
        self.episode_actions = []
        self.episode_rewards = []
        
    def select_action(self, state: torch.Tensor) -> int:
        """Sample action from policy distribution"""
        with torch.no_grad():
            action_probs = self.policy(state.unsqueeze(0))
            action_probs = torch.softmax(action_probs, dim=1)
            
            # Sample from distribution
            action = torch.multinomial(action_probs, num_samples=1).item()
        
        # Store for learning
        self.episode_states.append(state)
        self.episode_actions.append(action)
        
        return action
    
    def store_reward(self, reward: float):
        """Store reward for current step"""
        self.episode_rewards.append(reward)
    
    def update_policy(self):
        """
        Update policy using REINFORCE algorithm
        Called at end of episode (teaching session)
        """
        
        if len(self.episode_rewards) == 0:
            return
        
        # Calculate discounted returns
        returns = []
        R = 0
        for reward in reversed(self.episode_rewards):
            R = reward + 0.95 * R
            returns.insert(0, R)
        
        returns = torch.tensor(returns, dtype=torch.float)
        
        # Normalize returns
        returns = (returns - returns.mean()) / (returns.std() + 1e-8)
        
        # Calculate policy gradient loss
        loss = 0
        for state, action, R in zip(self.episode_states, self.episode_actions, returns):
            action_probs = self.policy(state.unsqueeze(0))
            log_prob = torch.log_softmax(action_probs, dim=1)[0, action]
            loss += -log_prob * R
        
        # Optimize
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Clear episode
        self.episode_states = []
        self.episode_actions = []
        self.episode_rewards = []
        
        return loss.item()


class TeachingPolicyNetwork(nn.Module):
    """
    Neural network that learns teaching policy
    
    Input: State (student condition + context)
    Output: Q-values or probabilities for each teaching action
    """
    
    def __init__(self, state_dim: int, num_actions: int,
                 hidden_dims: List[int] = [256, 128]):
        super().__init__()
        
        layers = []
        prev_dim = state_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.Dropout(0.2)
            ])
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, num_actions))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, state: torch.Tensor) -> torch.Tensor:
        """
        Forward pass
        
        Args:
            state: [batch_size, state_dim]
            
        Returns:
            q_values or logits: [batch_size, num_actions]
        """
        return self.network(state)


class ContinuousImprovementLoop:
    """
    Manages continuous learning from all student interactions
    
    Every interaction improves the system!
    """
    
    def __init__(self, rl_agent: TeachingRLAgent):
        self.rl_agent = rl_agent
        self.improvement_metrics = {
            'total_interactions': 0,
            'successful_teachings': 0,
            'average_reward': 0.0,
            'policy_updates': 0
        }
    
    def process_interaction(self, session_data: Dict, 
                          analysis: Dict,
                          intervention_used: str,
                          student_outcome: Dict):
        """
        Process one teaching interaction and learn from it
        
        Args:
            session_data: Original student input
            analysis: System's analysis
            intervention_used: Which intervention was delivered
            student_outcome: How student responded
        """
        
        # Get state and action
        state = self.rl_agent.get_state_representation(session_data, analysis)
        action = list(self.rl_agent.actions.values()).index(intervention_used)
        
        # Calculate reward
        reward = self.rl_agent.reward_calculator.calculate_reward(
            session_data, action, student_outcome
        )
        
        # Get next state
        next_analysis = student_outcome.get('updated_analysis', analysis)
        next_state = self.rl_agent.get_state_representation(session_data, next_analysis)
        
        # Check if done
        done = student_outcome.get('mastery_achieved', False)
        
        # Store experience
        self.rl_agent.store_experience(state, action, reward, next_state, done)
        
        # Learn
        loss = self.rl_agent.learn_from_experience()
        
        # Update metrics
        self.improvement_metrics['total_interactions'] += 1
        if reward > 0.5:
            self.improvement_metrics['successful_teachings'] += 1
        
        # Update average reward (exponential moving average)
        alpha = 0.1
        self.improvement_metrics['average_reward'] = \
            alpha * reward + (1 - alpha) * self.improvement_metrics['average_reward']
        
        if loss is not None:
            self.improvement_metrics['policy_updates'] += 1
        
        print(f"\n📈 CONTINUOUS IMPROVEMENT:")
        print(f"   Total interactions: {self.improvement_metrics['total_interactions']}")
        print(f"   Success rate: {self.get_success_rate():.1%}")
        print(f"   Average reward: {self.improvement_metrics['average_reward']:.3f}")
        print(f"   Policy updates: {self.improvement_metrics['policy_updates']}")
        
        # Knowledge graph updates
        kg_updates = self.rl_agent.kg_updater.update_from_interaction(
            session_data, student_outcome, reward > 0.5
        )
        
        print(f"   Knowledge graph updates: {kg_updates['num_updates']}")
        
        return {
            'reward': reward,
            'loss': loss,
            'metrics': self.improvement_metrics,
            'kg_updates': kg_updates
        }
    
    def get_success_rate(self) -> float:
        """Calculate current success rate"""
        if self.improvement_metrics['total_interactions'] == 0:
            return 0.0
        return self.improvement_metrics['successful_teachings'] / \
               self.improvement_metrics['total_interactions']
    
    def get_improvement_report(self) -> Dict:
        """Generate report on system improvement"""
        return {
            'total_students_taught': self.improvement_metrics['total_interactions'],
            'success_rate': self.get_success_rate(),
            'average_reward_trend': self.improvement_metrics['average_reward'],
            'policy_quality': 'improving' if self.improvement_metrics['average_reward'] > 0.6 else 'learning',
            'experiences_learned_from': len(self.rl_agent.memory)
        }













