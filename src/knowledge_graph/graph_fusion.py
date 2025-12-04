"""
Graph Fusion Module
Fuses CSE-KG 2.0 (global domain knowledge) with student-specific knowledge graphs
"""

import torch
import torch.nn as nn
from typing import Dict, List, Optional, Tuple
import networkx as nx
import numpy as np


class GraphFusion(nn.Module):
    """
    Fuses two knowledge graphs:
    1. CSE-KG 2.0: Global computer science domain knowledge
    2. Student Graph: Personal knowledge state and mastery levels
    
    Uses attention mechanism to weight contributions from each graph
    """
    
    def __init__(self, config: Dict):
        super().__init__()
        
        self.config = config
        
        # Fusion parameters
        self.cse_kg_weight = config['graph_fusion']['cse_kg_weight']
        self.student_weight = config['graph_fusion']['student_graph_weight']
        self.fusion_strategy = config['graph_fusion']['fusion_strategy']
        
        # Embedding dimensions
        self.concept_dim = 256
        
        # Learnable fusion weights
        if self.fusion_strategy == 'attention_weighted':
            self.attention = nn.Sequential(
                nn.Linear(self.concept_dim * 2, 128),
                nn.Tanh(),
                nn.Linear(128, 2),  # Weight for [CSE-KG, Student]
                nn.Softmax(dim=-1)
            )
        elif self.fusion_strategy == 'gated':
            self.gate = nn.Sequential(
                nn.Linear(self.concept_dim * 2, self.concept_dim),
                nn.Sigmoid()
            )
        
        # Alignment layer (project CSE-KG embeddings to student space)
        self.cse_kg_projection = nn.Linear(self.concept_dim, self.concept_dim)
        self.student_projection = nn.Linear(self.concept_dim, self.concept_dim)
        
    def forward(self, cse_kg_embeddings: torch.Tensor,
                student_embeddings: torch.Tensor,
                concept_ids: Optional[torch.Tensor] = None) -> Dict[str, torch.Tensor]:
        """
        Fuse embeddings from both graphs
        
        Args:
            cse_kg_embeddings: [num_concepts, concept_dim] - from CSE-KG
            student_embeddings: [num_concepts, concept_dim] - student's knowledge state
            concept_ids: [num_concepts] - concept identifiers (optional)
            
        Returns:
            Dictionary with fused embeddings and fusion weights
        """
        # Project to common space
        cse_kg_proj = self.cse_kg_projection(cse_kg_embeddings)
        student_proj = self.student_projection(student_embeddings)
        
        if self.fusion_strategy == 'attention_weighted':
            # Attention-based fusion
            combined = torch.cat([cse_kg_proj, student_proj], dim=-1)
            weights = self.attention(combined)  # [N, 2]
            
            # Weighted combination
            fused = weights[:, 0:1] * cse_kg_proj + weights[:, 1:2] * student_proj
            
            return {
                'fused_embeddings': fused,
                'fusion_weights': weights,
                'cse_kg_weight': weights[:, 0],
                'student_weight': weights[:, 1]
            }
            
        elif self.fusion_strategy == 'gated':
            # Gated fusion
            combined = torch.cat([cse_kg_proj, student_proj], dim=-1)
            gate = self.gate(combined)
            
            fused = gate * cse_kg_proj + (1 - gate) * student_proj
            
            return {
                'fused_embeddings': fused,
                'gate_values': gate
            }
            
        elif self.fusion_strategy == 'hierarchical':
            # Hierarchical: CSE-KG provides structure, student provides activation
            # Combine multiplicatively
            fused = cse_kg_proj * student_proj
            
            return {
                'fused_embeddings': fused
            }
        
        else:
            # Simple weighted average (fixed weights from config)
            fused = self.cse_kg_weight * cse_kg_proj + \
                   self.student_weight * student_proj
            
            return {
                'fused_embeddings': fused
            }
    
    def update_student_graph(self, student_graph: Dict, 
                            cse_kg_subgraph: Dict,
                            latent_representation: torch.Tensor) -> Dict:
        """
        Update student knowledge graph using CSE-KG structure and HVSAE latent
        
        Args:
            student_graph: Current student knowledge graph
            cse_kg_subgraph: Relevant CSE-KG subgraph
            latent_representation: Student's latent representation from HVSAE
            
        Returns:
            Updated student graph
        """
        # Extract concepts from both graphs
        student_concepts = set(student_graph.get('concepts', []))
        cse_kg_concepts = set(node['uri'] for node in cse_kg_subgraph['nodes'])
        
        # Add new concepts from CSE-KG if relevant
        new_concepts = cse_kg_concepts - student_concepts
        
        updated_graph = student_graph.copy()
        
        for concept in new_concepts:
            # Initialize with low activation (not yet mastered)
            updated_graph.setdefault('concept_activations', {})[concept] = 0.1
            updated_graph.setdefault('mastery_levels', {})[concept] = 0.0
        
        # Update relationships based on CSE-KG structure
        for edge in cse_kg_subgraph['edges']:
            source = edge['source']
            target = edge['target']
            relation = edge['relation']
            
            if source in updated_graph.get('concepts', []) and \
               target in updated_graph.get('concepts', []):
                # Add edge to student graph
                updated_graph.setdefault('edges', []).append({
                    'source': source,
                    'target': target,
                    'relation': relation,
                    'weight': 1.0  # Can be adjusted based on evidence
                })
        
        return updated_graph


class KnowledgeGraphBuilder:
    """
    Builds and maintains student-specific knowledge graphs
    Integrates observations from learning sessions
    """
    
    def __init__(self, config: Dict, cse_kg_client):
        self.config = config
        self.cse_kg_client = cse_kg_client
        
        # NetworkX graph for easy manipulation
        self.global_graph = nx.DiGraph()
        
    def build_from_cse_kg(self, concepts: List[str]) -> nx.DiGraph:
        """
        Build a knowledge graph from CSE-KG for given concepts
        
        Args:
            concepts: List of concept names
            
        Returns:
            NetworkX directed graph
        """
        G = nx.DiGraph()
        
        # Add nodes
        for concept in concepts:
            concept_info = self.cse_kg_client.get_concept_info(concept)
            if concept_info:
                G.add_node(
                    concept,
                    **concept_info
                )
        
        # Add edges (relationships)
        for concept in concepts:
            # Get prerequisites
            prereqs = self.cse_kg_client.get_prerequisites(concept)
            for prereq in prereqs:
                G.add_edge(prereq, concept, relation='prerequisite')
            
            # Get related concepts
            related = self.cse_kg_client.get_related_concepts(concept, max_distance=1)
            for related_concept, relation, _ in related:
                if related_concept in concepts:
                    G.add_edge(concept, related_concept, relation=relation)
        
        return G
    
    def initialize_student_graph(self, student_id: str, 
                                relevant_concepts: List[str]) -> Dict:
        """
        Initialize a new student knowledge graph
        
        Args:
            student_id: Student identifier
            relevant_concepts: Concepts relevant to student's learning
            
        Returns:
            Student graph dictionary
        """
        # Get CSE-KG structure
        base_graph = self.build_from_cse_kg(relevant_concepts)
        
        # Initialize student-specific data
        student_graph = {
            'student_id': student_id,
            'concepts': relevant_concepts,
            'concept_activations': {c: 0.5 for c in relevant_concepts},  # Neutral
            'mastery_levels': {c: 0.0 for c in relevant_concepts},  # Unmastered
            'misconceptions': {},
            'edges': [],
            'update_history': []
        }
        
        # Copy structure from base graph
        for edge in base_graph.edges(data=True):
            student_graph['edges'].append({
                'source': edge[0],
                'target': edge[1],
                'relation': edge[2].get('relation', 'related'),
                'weight': 1.0
            })
        
        return student_graph
    
    def update_from_session(self, student_graph: Dict,
                          session_data: Dict) -> Dict:
        """
        Update student graph based on learning session
        
        Args:
            student_graph: Current student graph
            session_data: Data from recent session (concepts encountered, success, etc.)
            
        Returns:
            Updated student graph
        """
        updated = student_graph.copy()
        
        # Update activations for encountered concepts
        for concept in session_data.get('concepts_encountered', []):
            if concept in updated['concept_activations']:
                # Increase activation (concept was accessed)
                current = updated['concept_activations'][concept]
                updated['concept_activations'][concept] = min(1.0, current + 0.1)
        
        # Update mastery based on performance
        if 'concept_performance' in session_data:
            for concept, performance in session_data['concept_performance'].items():
                if concept in updated['mastery_levels']:
                    # Update mastery using exponential moving average
                    current_mastery = updated['mastery_levels'][concept]
                    alpha = 0.2  # Learning rate
                    updated['mastery_levels'][concept] = \
                        alpha * performance + (1 - alpha) * current_mastery
        
        # Record misconceptions
        if 'detected_misconceptions' in session_data:
            for misconception in session_data['detected_misconceptions']:
                concept = misconception['concept']
                if concept not in updated['misconceptions']:
                    updated['misconceptions'][concept] = []
                updated['misconceptions'][concept].append({
                    'description': misconception['description'],
                    'timestamp': session_data.get('timestamp'),
                    'strength': misconception.get('confidence', 0.5)
                })
        
        # Add to update history
        updated['update_history'].append({
            'timestamp': session_data.get('timestamp'),
            'session_id': session_data.get('session_id'),
            'concepts_updated': list(session_data.get('concepts_encountered', []))
        })
        
        return updated
    
    def identify_knowledge_gaps(self, student_graph: Dict, 
                               target_concept: str) -> List[Dict]:
        """
        Identify knowledge gaps preventing mastery of target concept
        
        Args:
            student_graph: Student's knowledge graph
            target_concept: Concept student is trying to learn
            
        Returns:
            List of gap descriptions with suggested remediation
        """
        gaps = []
        
        # Check if target concept exists
        if target_concept not in student_graph['concepts']:
            gaps.append({
                'type': 'unknown_concept',
                'concept': target_concept,
                'severity': 'high',
                'recommendation': 'Introduce concept from scratch'
            })
            return gaps
        
        # Get prerequisites from CSE-KG
        prereqs = self.cse_kg_client.get_prerequisites(target_concept)
        
        # Check mastery of prerequisites
        for prereq in prereqs:
            if prereq in student_graph['mastery_levels']:
                mastery = student_graph['mastery_levels'][prereq]
                if mastery < 0.5:
                    gaps.append({
                        'type': 'missing_prerequisite',
                        'concept': prereq,
                        'mastery': mastery,
                        'severity': 'high',
                        'recommendation': f'Review {prereq} before continuing'
                    })
        
        # Check for misconceptions
        if target_concept in student_graph['misconceptions']:
            for misconception in student_graph['misconceptions'][target_concept]:
                if misconception['strength'] > 0.6:
                    gaps.append({
                        'type': 'misconception',
                        'concept': target_concept,
                        'description': misconception['description'],
                        'severity': 'medium',
                        'recommendation': 'Address misconception directly'
                    })
        
        return gaps
    
    def suggest_learning_path(self, student_graph: Dict,
                            target_concept: str) -> List[str]:
        """
        Suggest optimal learning path to target concept
        
        Args:
            student_graph: Student's knowledge graph
            target_concept: Goal concept
            
        Returns:
            Ordered list of concepts to learn
        """
        # Build prerequisite graph
        prereq_graph = nx.DiGraph()
        
        for edge in student_graph['edges']:
            if edge['relation'] == 'prerequisite':
                prereq_graph.add_edge(edge['source'], edge['target'])
        
        # Find path from mastered concepts to target
        mastered = [
            c for c, m in student_graph['mastery_levels'].items()
            if m > 0.7
        ]
        
        # Try to find shortest path
        paths = []
        for source in mastered:
            try:
                path = nx.shortest_path(prereq_graph, source, target_concept)
                paths.append(path)
            except nx.NetworkXNoPath:
                continue
        
        if paths:
            # Return shortest path, excluding already mastered
            shortest = min(paths, key=len)
            return [c for c in shortest if student_graph['mastery_levels'].get(c, 0) < 0.7]
        else:
            # No path found, return direct prerequisites
            return self.cse_kg_client.get_prerequisites(target_concept)






