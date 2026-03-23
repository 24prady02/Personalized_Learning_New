"""
Reinforcement Learning Module
Learns optimal teaching strategies from student interactions
"""

from .teaching_agent import TeachingRLAgent
from .reward_function import RewardCalculator
from .policy_network import TeachingPolicyNetwork
from .knowledge_graph_updater import DynamicKGUpdater

__all__ = [
    "TeachingRLAgent",
    "RewardCalculator",
    "TeachingPolicyNetwork",
    "DynamicKGUpdater"
]




















