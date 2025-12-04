"""
GIKT: Graph-based Interaction Model for Knowledge Tracing
Based on: ArXiv 2020 - "GIKT: A Graph-based Interaction Model for Knowledge Tracing"

Uses Graph Convolutional Networks to model:
- Student-question-skill interactions
- Question-skill correlations
- Skill dependencies
- Long-term dependencies in exercise history
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv, GATConv
from torch_geometric.data import Data, Batch
from typing import Dict, List, Optional, Tuple
import numpy as np
import networkx as nx
from collections import defaultdict


class GIKTModel(nn.Module):
    """
    GIKT: Graph-based Interaction Model for Knowledge Tracing
    
    Architecture:
    1. Graph Convolutional Network for question-skill graph
    2. Student embedding network
    3. Interaction modeling (student × question × skill)
    4. Prediction network for next performance
    """
    
    def __init__(self, config: Dict):
        """
        Args:
            config: Configuration dictionary with GIKT settings
        """
        super().__init__()
        
        self.config = config
        
        # Hyperparameters
        self.student_embed_dim = config.get('student_embed_dim', 128)
        self.question_embed_dim = config.get('question_embed_dim', 128)
        self.skill_embed_dim = config.get('skill_embed_dim', 128)
        self.hidden_dim = config.get('hidden_dim', 256)
        self.num_gcn_layers = config.get('num_gcn_layers', 2)
        self.dropout = config.get('dropout', 0.2)
        
        # Embeddings
        self.student_embedding = nn.Embedding(
            config.get('num_students', 1000),
            self.student_embed_dim
        )
        self.question_embedding = nn.Embedding(
            config.get('num_questions', 1000),
            self.question_embed_dim
        )
        self.skill_embedding = nn.Embedding(
            config.get('num_skills', 100),
            self.skill_embed_dim
        )
        
        # Graph Convolutional Networks for question-skill graph
        self.gcn_layers = nn.ModuleList()
        input_dim = self.question_embed_dim + self.skill_embed_dim
        
        for i in range(self.num_gcn_layers):
            self.gcn_layers.append(
                GCNConv(input_dim if i == 0 else self.hidden_dim, self.hidden_dim)
            )
        
        # Interaction modeling
        self.interaction_net = nn.Sequential(
            nn.Linear(
                self.student_embed_dim + self.question_embed_dim + self.skill_embed_dim,
                self.hidden_dim
            ),
            nn.ReLU(),
            nn.Dropout(self.dropout),
            nn.Linear(self.hidden_dim, self.hidden_dim),
            nn.ReLU()
        )
        
        # Prediction network
        self.prediction_net = nn.Sequential(
            nn.Linear(self.hidden_dim * 2, self.hidden_dim),
            nn.ReLU(),
            nn.Dropout(self.dropout),
            nn.Linear(self.hidden_dim, 1),
            nn.Sigmoid()
        )
        
        # LSTM for temporal dependencies
        self.lstm = nn.LSTM(
            self.hidden_dim,
            self.hidden_dim,
            num_layers=1,
            batch_first=True,
            dropout=self.dropout
        )
    
    def build_question_skill_graph(self, question_skill_pairs: List[Tuple[int, int]]) -> Data:
        """
        Build question-skill bipartite graph
        
        Args:
            question_skill_pairs: List of (question_id, skill_id) pairs
            
        Returns:
            PyTorch Geometric Data object
        """
        # Create bipartite graph
        G = nx.Graph()
        
        # Add nodes (questions and skills)
        question_nodes = set()
        skill_nodes = set()
        
        for q_id, s_id in question_skill_pairs:
            question_nodes.add(q_id)
            skill_nodes.add(s_id)
            G.add_edge(f"q_{q_id}", f"s_{s_id}")
        
        # Create edge index for PyTorch Geometric
        # Map question and skill IDs to node indices
        node_to_idx = {}
        idx = 0
        
        for q_id in question_nodes:
            node_to_idx[f"q_{q_id}"] = idx
            idx += 1
        
        for s_id in skill_nodes:
            node_to_idx[f"s_{s_id}"] = idx
            idx += 1
        
        # Build edge index
        edge_index = []
        for q_id, s_id in question_skill_pairs:
            q_idx = node_to_idx[f"q_{q_id}"]
            s_idx = node_to_idx[f"s_{s_id}"]
            edge_index.append([q_idx, s_idx])
            edge_index.append([s_idx, q_idx])  # Undirected
        
        edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
        
        # Node features (embeddings)
        num_nodes = len(node_to_idx)
        node_features = torch.zeros(num_nodes, self.question_embed_dim + self.skill_embed_dim)
        
        for node, idx in node_to_idx.items():
            if node.startswith("q_"):
                q_id = int(node[2:])
                node_features[idx, :self.question_embed_dim] = \
                    self.question_embedding(torch.tensor(q_id))
            else:
                s_id = int(node[2:])
                node_features[idx, self.question_embed_dim:] = \
                    self.skill_embedding(torch.tensor(s_id))
        
        return Data(x=node_features, edge_index=edge_index)
    
    def forward(self, student_ids: torch.Tensor,
                question_ids: torch.Tensor,
                skill_ids: torch.Tensor,
                question_skill_graph: Data,
                exercise_history: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Forward pass
        
        Args:
            student_ids: [batch_size] student IDs
            question_ids: [batch_size] question IDs
            skill_ids: [batch_size] skill IDs
            question_skill_graph: Graph data for question-skill relationships
            exercise_history: [batch_size, seq_len, hidden_dim] previous exercises
            
        Returns:
            [batch_size, 1] prediction probabilities
        """
        batch_size = student_ids.size(0)
        
        # Get embeddings
        student_embeds = self.student_embedding(student_ids)  # [batch, student_dim]
        question_embeds = self.question_embedding(question_ids)  # [batch, question_dim]
        skill_embeds = self.skill_embedding(skill_ids)  # [batch, skill_dim]
        
        # Graph convolution on question-skill graph
        x = question_skill_graph.x
        edge_index = question_skill_graph.edge_index
        
        for i, gcn_layer in enumerate(self.gcn_layers):
            x = gcn_layer(x, edge_index)
            if i < len(self.gcn_layers) - 1:
                x = F.relu(x)
                x = F.dropout(x, p=self.dropout, training=self.training)
        
        # Get question and skill features from graph
        # (Simplified - in practice, need to map question/skill IDs to graph nodes)
        question_graph_features = question_embeds  # Use embeddings as proxy
        skill_graph_features = skill_embeds
        
        # Interaction modeling
        interaction_input = torch.cat([
            student_embeds,
            question_graph_features,
            skill_graph_features
        ], dim=1)
        
        interaction_features = self.interaction_net(interaction_input)
        
        # Temporal modeling with LSTM (if history provided)
        if exercise_history is not None:
            lstm_out, _ = self.lstm(exercise_history)
            last_hidden = lstm_out[:, -1, :]  # Last timestep
            combined_features = torch.cat([interaction_features, last_hidden], dim=1)
        else:
            combined_features = torch.cat([
                interaction_features,
                torch.zeros(batch_size, self.hidden_dim, device=student_ids.device)
            ], dim=1)
        
        # Prediction
        predictions = self.prediction_net(combined_features)
        
        return predictions


class GIKTKnowledgeTracer:
    """
    High-level interface for GIKT knowledge tracing
    """
    
    def __init__(self, config: Dict):
        """
        Args:
            config: Configuration dictionary
        """
        self.config = config
        
        # Initialize GIKT model
        self.model = GIKTModel(config)
        
        # Question-skill mappings
        self.question_skill_map: Dict[int, List[int]] = defaultdict(list)
        
        # Student exercise history
        self.student_history: Dict[int, List[Dict]] = defaultdict(list)
    
    def add_question_skill_mapping(self, question_id: int, skill_ids: List[int]):
        """Add question-skill relationship"""
        self.question_skill_map[question_id] = skill_ids
    
    def record_exercise(self, student_id: int, question_id: int,
                       skill_ids: List[int], correct: bool):
        """Record student exercise"""
        self.student_history[student_id].append({
            'question_id': question_id,
            'skill_ids': skill_ids,
            'correct': correct,
            'timestamp': len(self.student_history[student_id])
        })
    
    def predict_performance(self, student_id: int, question_id: int) -> float:
        """
        Predict student performance on a question
        
        Args:
            student_id: Student ID
            question_id: Question ID
            
        Returns:
            Probability of correct answer (0.0 to 1.0)
        """
        # Get skill IDs for question
        skill_ids = self.question_skill_map.get(question_id, [0])
        skill_id = skill_ids[0]  # Use first skill
        
        # Build question-skill graph
        question_skill_pairs = [
            (q_id, s_id)
            for q_id, skills in self.question_skill_map.items()
            for s_id in skills
        ]
        
        if not question_skill_pairs:
            question_skill_pairs = [(question_id, skill_id)]
        
        graph_data = self.model.build_question_skill_graph(question_skill_pairs)
        
        # Get student history
        history = self.student_history.get(student_id, [])
        
        # Prepare inputs
        student_tensor = torch.tensor([student_id], dtype=torch.long)
        question_tensor = torch.tensor([question_id], dtype=torch.long)
        skill_tensor = torch.tensor([skill_id], dtype=torch.long)
        
        # Get exercise history (last 10 exercises)
        if history:
            history_tensor = torch.zeros(1, min(len(history), 10), self.model.hidden_dim)
            # Simplified - in practice, encode history properly
        else:
            history_tensor = None
        
        # Predict
        self.model.eval()
        with torch.no_grad():
            prediction = self.model(
                student_tensor,
                question_tensor,
                skill_tensor,
                graph_data,
                history_tensor
            )
        
        return prediction.item()
    
    def get_student_knowledge_state(self, student_id: int) -> Dict:
        """
        Get student's knowledge state across all skills
        
        Args:
            student_id: Student ID
            
        Returns:
            Dictionary with skill mastery levels
        """
        history = self.student_history.get(student_id, [])
        
        # Calculate mastery per skill
        skill_performance = defaultdict(list)
        
        for exercise in history:
            for skill_id in exercise['skill_ids']:
                skill_performance[skill_id].append(exercise['correct'])
        
        mastery = {}
        for skill_id, performances in skill_performance.items():
            mastery[skill_id] = sum(performances) / len(performances) if performances else 0.0
        
        return {
            'student_id': student_id,
            'skill_mastery': mastery,
            'total_exercises': len(history),
            'overall_mastery': sum(mastery.values()) / len(mastery) if mastery else 0.0
        }












