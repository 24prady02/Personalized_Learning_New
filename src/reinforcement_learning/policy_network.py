"""
Policy Network for Teaching RL Agent
"""

import torch
import torch.nn as nn
from typing import List


class TeachingPolicyNetwork(nn.Module):
    """Neural network that learns optimal teaching policy"""
    
    def __init__(self, state_dim: int, num_actions: int,
                 hidden_dims: List[int] = [256, 128]):
        super().__init__()
        
        layers = []
        prev_dim = state_dim
        
        for hidden_dim in hidden_dims:
            layers.extend([
                nn.Linear(prev_dim, hidden_dim),
                nn.ReLU(),
                nn.LayerNorm(hidden_dim),
                nn.Dropout(0.2)
            ])
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, num_actions))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, state: torch.Tensor) -> torch.Tensor:
        return self.network(state)




















