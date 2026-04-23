"""
Local CSE-KG 2.0 Client
Uses locally downloaded graph data instead of SPARQL queries
"""

import json
import pickle
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict
import networkx as nx


class LocalCSEKGClient:
    """
    Local client for CSE-KG 2.0 using downloaded graph data
    Provides same interface as CSEKGClient but uses local files
    """
    
    def __init__(self, config: Dict):
        """
        Args:
            config: Configuration dictionary with CSE-KG settings
        """
        self.config = config
        self.namespace = config['cse_kg']['namespace']
        self.cskg = self.namespace
        
        # Load local graph
        local_dir = Path("data/cse_kg_local")
        self.graph = None
        self.concepts = {}
        self.concept_keywords = defaultdict(set)
        
        # Try to load from local files
        graph_pickle = local_dir / "graph.pkl"
        concepts_file = local_dir / "concepts.json"
        keyword_file = local_dir / "keyword_index.json"
        
        if graph_pickle.exists():
            print(f"Loading local CSE-KG graph from {graph_pickle}...")
            with open(graph_pickle, 'rb') as f:
                self.graph = pickle.load(f)
            print(f"  Loaded {len(self.graph.nodes())} nodes, {len(self.graph.edges())} edges")
        
        if concepts_file.exists():
            with open(concepts_file, 'r', encoding='utf-8') as f:
                self.concepts = json.load(f)
            print(f"  Loaded {len(self.concepts)} concepts")
        
        if keyword_file.exists():
            with open(keyword_file, 'r', encoding='utf-8') as f:
                keyword_data = json.load(f)
                for keyword, concept_ids in keyword_data.items():
                    self.concept_keywords[keyword] = set(concept_ids)
            print(f"  Loaded {len(self.concept_keywords)} keyword mappings")
        
        if not self.graph:
            print("[WARNING] Local CSE-KG graph not found. Run build_local_cse_kg.py first.")
            # Create empty graph
            self.graph = nx.DiGraph()
    
    def get_concept_info(self, concept_uri: str) -> Optional[Dict]:
        """
        Get detailed information about a concept
        
        Args:
            concept_uri: URI or local name (e.g., "cskg:recursion" or "recursion")
            
        Returns:
            Dictionary with concept properties
        """
        # Normalize to concept ID
        concept_id = self._normalize_id(concept_uri)
        
        if concept_id in self.concepts:
            concept = self.concepts[concept_id].copy()
            concept['uri'] = f"{self.cskg}{concept_id}"
            
            # Add related concepts
            if self.graph and concept_id in self.graph:
                neighbors = list(self.graph.neighbors(concept_id))
                concept['related'] = [
                    {'uri': f"{self.cskg}{n}", 'id': n}
                    for n in neighbors[:10]
                ]
            
            return concept
        
        return None
    
    def get_prerequisites(self, concept: str) -> List[str]:
        """
        Get prerequisite concepts for a given concept
        
        Args:
            concept: Concept name or URI
            
        Returns:
            List of prerequisite concept URIs
        """
        concept_id = self._normalize_id(concept)
        
        if not self.graph or concept_id not in self.graph:
            return []
        
        # Find incoming edges with 'requiresKnowledge' or 'isPrerequisiteOf'
        prerequisites = []
        for predecessor in self.graph.predecessors(concept_id):
            edge_data = self.graph.get_edge_data(predecessor, concept_id, {})
            relation = edge_data.get('relation', '')
            if 'prerequisite' in relation.lower() or 'requires' in relation.lower():
                prerequisites.append(f"{self.cskg}{predecessor}")
        
        return prerequisites
    
    def get_related_concepts(self, concept: str, 
                           relation_type: Optional[str] = None,
                           max_distance: int = 1) -> List[Tuple[str, str, int]]:
        """
        Get concepts related to the given concept
        
        Args:
            concept: Source concept
            relation_type: Specific relation type (optional)
            max_distance: Maximum distance in graph (1 = direct neighbors)
            
        Returns:
            List of (concept_uri, relation_type, distance) tuples
        """
        concept_id = self._normalize_id(concept)
        
        if not self.graph or concept_id not in self.graph:
            return []
        
        related = []
        visited = set([concept_id])
        
        # BFS traversal
        queue = [(concept_id, 0)]
        
        while queue:
            current, distance = queue.pop(0)
            
            if distance >= max_distance:
                continue
            
            # Get neighbors
            for neighbor in self.graph.neighbors(current):
                if neighbor in visited:
                    continue
                
                visited.add(neighbor)
                edge_data = self.graph.get_edge_data(current, neighbor, {})
                rel = edge_data.get('relation', 'relatedTo')
                
                # Filter by relation type if specified
                if relation_type is None or relation_type.lower() in rel.lower():
                    related.append((f"{self.cskg}{neighbor}", rel, distance + 1))
                    queue.append((neighbor, distance + 1))
        
        return related
    
    def get_methods_for_task(self, task: str) -> List[Dict]:
        """
        Get methods that can solve a given task
        
        Args:
            task: Task name or URI
            
        Returns:
            List of method dictionaries with metadata
        """
        task_id = self._normalize_id(task)
        
        if not self.graph or task_id not in self.graph:
            return []
        
        methods = []
        # Find concepts connected to this task with 'solvesTask' or 'usesMethod'
        for neighbor in self.graph.neighbors(task_id):
            edge_data = self.graph.get_edge_data(task_id, neighbor, {})
            rel = edge_data.get('relation', '')
            if 'method' in rel.lower() or 'solve' in rel.lower():
                concept_info = self.concepts.get(neighbor, {})
                methods.append({
                    'uri': f"{self.cskg}{neighbor}",
                    'label': concept_info.get('label', neighbor),
                    'description': concept_info.get('description', '')
                })
        
        return methods
    
    def get_common_misconceptions(self, concept: str) -> List[Dict]:
        """
        Retrieve common misconceptions related to a concept
        
        Args:
            concept: Concept name
            
        Returns:
            List of misconception descriptions
        """
        # This would require specific misconception data
        # For now, return related concepts that might be confused
        related = self.get_related_concepts(concept, max_distance=1)
        
        misconceptions = []
        for uri, relation, _ in related[:5]:
            concept_id = self._normalize_id(uri)
            concept_info = self.concepts.get(concept_id, {})
            if concept_info:
                misconceptions.append({
                    'uri': uri,
                    'description': f"Commonly confused with {concept_info.get('label', concept_id)}",
                    'type': 'related_concept'
                })
        
        return misconceptions
    
    def extract_concepts(self, text: str) -> List[str]:
        """
        Extract CS concepts from natural language text
        Uses keyword matching against local graph
        
        Args:
            text: Natural language description
            
        Returns:
            List of concept names
        """
        text_lower = text.lower()
        concept_scores = defaultdict(int)
        
        # Match keywords
        for keyword, concept_ids in self.concept_keywords.items():
            if keyword in text_lower:
                for concept_id in concept_ids:
                    concept_scores[concept_id] += 1
        
        # Sort by score
        ranked = sorted(concept_scores.items(), key=lambda x: x[1], reverse=True)
        return [concept_id for concept_id, _ in ranked[:10]]
    
    def get_concept_hierarchy(self, concept: str, levels: int = 2) -> Dict:
        """
        Get hierarchical structure around a concept
        
        Args:
            concept: Root concept
            levels: Number of levels up and down
            
        Returns:
            Dictionary representing hierarchy
        """
        concept_id = self._normalize_id(concept)
        
        hierarchy = {
            'concept': f"{self.cskg}{concept_id}",
            'parents': [],
            'children': [],
            'siblings': []
        }
        
        if not self.graph or concept_id not in self.graph:
            return hierarchy
        
        # Get parents (broader concepts)
        for predecessor in self.graph.predecessors(concept_id):
            edge_data = self.graph.get_edge_data(predecessor, concept_id, {})
            if 'broader' in edge_data.get('relation', '').lower() or 'parent' in edge_data.get('relation', '').lower():
                hierarchy['parents'].append(f"{self.cskg}{predecessor}")
        
        # Get children (narrower concepts)
        for successor in self.graph.neighbors(concept_id):
            edge_data = self.graph.get_edge_data(concept_id, successor, {})
            if 'narrower' in edge_data.get('relation', '').lower() or 'child' in edge_data.get('relation', '').lower():
                hierarchy['children'].append(f"{self.cskg}{successor}")
        
        # Get siblings (same parents)
        if hierarchy['parents']:
            parent_id = self._normalize_id(hierarchy['parents'][0])
            for sibling in self.graph.neighbors(parent_id):
                if sibling != concept_id:
                    hierarchy['siblings'].append(f"{self.cskg}{sibling}")
        
        return hierarchy
    
    def search_by_keywords(self, keywords: List[str], 
                          entity_type: Optional[str] = None,
                          limit: int = 20) -> List[Dict]:
        """
        Search CSE-KG by keywords
        
        Args:
            keywords: List of search keywords
            entity_type: Filter by entity type (Method, Task, etc.)
            limit: Maximum results
            
        Returns:
            List of matching entities
        """
        concept_scores = defaultdict(int)
        
        # Score concepts by keyword matches
        for keyword in keywords:
            keyword_lower = keyword.lower()
            if keyword_lower in self.concept_keywords:
                for concept_id in self.concept_keywords[keyword_lower]:
                    concept_scores[concept_id] += 1
        
        # Filter by entity type if specified
        if entity_type:
            filtered_scores = {}
            for concept_id, score in concept_scores.items():
                concept_info = self.concepts.get(concept_id, {})
                if entity_type.lower() in concept_info.get('type', '').lower():
                    filtered_scores[concept_id] = score
            concept_scores = filtered_scores
        
        # Sort and return top results
        ranked = sorted(concept_scores.items(), key=lambda x: x[1], reverse=True)
        
        entities = []
        for concept_id, score in ranked[:limit]:
            concept_info = self.concepts.get(concept_id, {})
            entities.append({
                'uri': f"{self.cskg}{concept_id}",
                'label': concept_info.get('label', concept_id),
                'type': concept_info.get('type', 'Concept')
            })
        
        return entities
    
    def _normalize_id(self, concept: str) -> str:
        """Convert concept URI or name to local ID"""
        if concept.startswith('http'):
            return concept.replace(self.cskg, '').replace('cskg:', '')
        else:
            return concept.replace('cskg:', '')
    
    def build_subgraph(self, concepts: List[str], 
                      include_relations: List[str] = None) -> Dict:
        """
        Build a subgraph containing specified concepts and their relationships
        
        Args:
            concepts: List of concept names/URIs
            include_relations: Which relation types to include
            
        Returns:
            Dictionary with nodes and edges
        """
        concept_ids = [self._normalize_id(c) for c in concepts]
        
        nodes = []
        edges = []
        
        # Add nodes
        for concept_id in concept_ids:
            if concept_id in self.concepts:
                concept_info = self.concepts[concept_id].copy()
                concept_info['uri'] = f"{self.cskg}{concept_id}"
                nodes.append(concept_info)
        
        # Add edges between concepts
        if self.graph:
            for i, source in enumerate(concept_ids):
                if source not in self.graph:
                    continue
                for j, target in enumerate(concept_ids):
                    if i >= j or target not in self.graph:
                        continue
                    
                    if self.graph.has_edge(source, target):
                        edge_data = self.graph.get_edge_data(source, target, {})
                        relation = edge_data.get('relation', 'relatedTo')
                        
                        if include_relations is None or relation in include_relations:
                            edges.append({
                                'source': f"{self.cskg}{source}",
                                'target': f"{self.cskg}{target}",
                                'relation': relation
                            })
        
        return {
            'nodes': nodes,
            'edges': edges
        }















