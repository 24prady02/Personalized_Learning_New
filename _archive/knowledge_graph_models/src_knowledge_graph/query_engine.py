"""
Query Engine for sophisticated CSE-KG queries
Provides high-level query interface for the system
"""

from typing import Dict, List, Optional, Tuple
import numpy as np
from collections import defaultdict


class QueryEngine:
    """
    High-level query engine for CSE-KG 2.0
    Provides complex queries combining multiple criteria
    """
    
    def __init__(self, cse_kg_client):
        self.client = cse_kg_client
        
    def find_alternative_methods(self, task: str, 
                                current_method: str,
                                criteria: Optional[Dict] = None) -> List[Dict]:
        """
        Find alternative methods for a task
        
        Args:
            task: Task to solve
            current_method: Current method being used
            criteria: Filter criteria (e.g., {'simpler_than': current_method})
            
        Returns:
            List of alternative methods with comparisons
        """
        # Get all methods for task
        methods = self.client.get_methods_for_task(task)
        
        # Filter out current method
        alternatives = [m for m in methods if m['uri'] != current_method]
        
        # Apply criteria if provided
        if criteria:
            # This would require method complexity/difficulty metadata
            # Placeholder implementation
            pass
        
        return alternatives
    
    def find_concept_context(self, concept: str, 
                           context_type: str = 'learning') -> Dict:
        """
        Get rich contextual information for a concept
        
        Args:
            concept: Target concept
            context_type: Type of context ('learning', 'research', 'application')
            
        Returns:
            Dictionary with contextual information
        """
        context = {
            'concept': concept,
            'prerequisites': [],
            'related_concepts': [],
            'applications': [],
            'common_patterns': [],
            'misconceptions': []
        }
        
        # Prerequisites
        context['prerequisites'] = self.client.get_prerequisites(concept)
        
        # Related concepts
        related = self.client.get_related_concepts(concept, max_distance=1)
        context['related_concepts'] = [
            {'concept': r[0], 'relation': r[1]} 
            for r in related[:10]
        ]
        
        # Applications (tasks that use this concept)
        # This would require querying for tasks
        
        # Misconceptions
        context['misconceptions'] = self.client.get_common_misconceptions(concept)
        
        return context
    
    def find_learning_resources(self, concept: str,
                               student_profile: Optional[Dict] = None) -> List[Dict]:
        """
        Find appropriate learning resources for a concept
        
        Args:
            concept: Concept to learn
            student_profile: Student's learning preferences and level
            
        Returns:
            Ranked list of learning resources
        """
        # Query CSE-KG for materials related to concept
        materials = []
        
        # Get related materials from CSE-KG
        query = f"""
        PREFIX cskg: <{self.client.cskg}>
        
        SELECT DISTINCT ?material ?type ?title WHERE {{
            ?material cskg:relatedTo cskg:{concept} .
            ?material rdf:type cskg:Material .
            OPTIONAL {{ ?material cskg:title ?title . }}
        }}
        LIMIT 20
        """
        
        results = self.client._query_sparql(query)
        
        for r in results:
            materials.append({
                'uri': r['material']['value'],
                'type': r.get('type', {}).get('value', ''),
                'title': r.get('title', {}).get('value', '')
            })
        
        # Rank based on student profile if provided
        if student_profile:
            materials = self._rank_materials(materials, student_profile)
        
        return materials
    
    def _rank_materials(self, materials: List[Dict], 
                       profile: Dict) -> List[Dict]:
        """
        Rank materials based on student profile
        """
        # Placeholder: rank by learning style preference
        learning_style = profile.get('learning_style', {})
        
        for material in materials:
            score = 0
            
            # Visual learners prefer videos/diagrams
            if learning_style.get('visual_verbal') == 'visual':
                if 'video' in material.get('type', '').lower():
                    score += 0.5
                if 'diagram' in material.get('type', '').lower():
                    score += 0.4
            
            # Verbal learners prefer text
            if learning_style.get('visual_verbal') == 'verbal':
                if 'article' in material.get('type', '').lower():
                    score += 0.5
                if 'book' in material.get('type', '').lower():
                    score += 0.4
            
            material['relevance_score'] = score
        
        # Sort by score
        materials.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return materials
    
    def explain_relationship(self, concept1: str, concept2: str) -> Optional[str]:
        """
        Explain the relationship between two concepts
        
        Args:
            concept1: First concept
            concept2: Second concept
            
        Returns:
            Natural language explanation of relationship
        """
        # Get related concepts
        related = self.client.get_related_concepts(concept1, max_distance=2)
        
        # Find concept2 in results
        for uri, relation, distance in related:
            if concept2 in uri:
                if distance == 1:
                    return f"{concept1} is directly related to {concept2} via '{relation}'"
                else:
                    return f"{concept1} is related to {concept2} at distance {distance}"
        
        return None
    
    def find_similar_concepts(self, concept: str, 
                            similarity_metric: str = 'structural',
                            top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Find concepts similar to the given concept
        
        Args:
            concept: Target concept
            similarity_metric: 'structural' (graph-based) or 'semantic'
            top_k: Number of results
            
        Returns:
            List of (concept, similarity_score) tuples
        """
        if similarity_metric == 'structural':
            # Based on shared neighbors in graph
            concept_neighbors = set(
                r[0] for r in self.client.get_related_concepts(concept, max_distance=1)
            )
            
            # Get siblings (concepts with same parents)
            hierarchy = self.client.get_concept_hierarchy(concept)
            siblings = hierarchy.get('siblings', [])
            
            similar = []
            for sibling in siblings:
                sibling_neighbors = set(
                    r[0] for r in self.client.get_related_concepts(sibling, max_distance=1)
                )
                
                # Jaccard similarity
                intersection = len(concept_neighbors & sibling_neighbors)
                union = len(concept_neighbors | sibling_neighbors)
                similarity = intersection / union if union > 0 else 0
                
                similar.append((sibling, similarity))
            
            similar.sort(key=lambda x: x[1], reverse=True)
            return similar[:top_k]
        
        else:
            # Semantic similarity would require embeddings
            # Placeholder
            return []


class ConceptRetriever:
    """
    Retrieves relevant concepts from CSE-KG based on code/text queries
    """
    
    def __init__(self, cse_kg_client):
        self.client = cse_kg_client
        
        # Cache of concept keywords for faster retrieval
        self.concept_keywords = {}
        self._build_keyword_index()
    
    def _build_keyword_index(self):
        """
        Build inverted index of keywords → concepts
        """
        # This would typically be pre-computed and loaded
        # Placeholder implementation
        common_concepts = [
            'recursion', 'iteration', 'array', 'list', 'tree', 'graph',
            'sorting', 'searching', 'dynamic_programming', 'greedy',
            'object_oriented_programming', 'inheritance', 'polymorphism',
            'exception_handling', 'null_pointer', 'stack_overflow',
            'concurrency', 'threading', 'synchronization'
        ]
        
        for concept in common_concepts:
            # Get concept info
            info = self.client.get_concept_info(concept)
            if info:
                # Extract keywords from labels and descriptions
                keywords = set()
                for label in info.get('labels', []):
                    keywords.update(label.lower().split())
                for desc in info.get('descriptions', []):
                    keywords.update(desc.lower().split()[:10])  # First 10 words
                
                for keyword in keywords:
                    if keyword not in self.concept_keywords:
                        self.concept_keywords[keyword] = []
                    self.concept_keywords[keyword].append(concept)
    
    def retrieve_from_code(self, code: str, 
                          error_message: Optional[str] = None,
                          top_k: int = 5) -> List[str]:
        """
        Retrieve relevant concepts from code snippet
        
        Args:
            code: Source code
            error_message: Optional error message
            top_k: Number of concepts to retrieve
            
        Returns:
            List of concept names
        """
        # Simple keyword matching
        text = code.lower()
        if error_message:
            text += " " + error_message.lower()
        
        # Count concept mentions
        concept_scores = defaultdict(int)
        
        for keyword, concepts in self.concept_keywords.items():
            if keyword in text:
                for concept in concepts:
                    concept_scores[concept] += 1
        
        # Sort by score
        ranked = sorted(concept_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [concept for concept, _ in ranked[:top_k]]
    
    def retrieve_from_query(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Retrieve concepts from natural language query
        
        Args:
            query: Natural language question/query
            top_k: Number of results
            
        Returns:
            List of concept dictionaries with metadata
        """
        # Extract keywords from query
        keywords = query.lower().split()
        
        # Search CSE-KG
        results = self.client.search_by_keywords(keywords, limit=top_k * 2)
        
        # Re-rank by relevance (number of keyword matches)
        for result in results:
            label = result.get('label', '').lower()
            score = sum(1 for kw in keywords if kw in label)
            result['relevance_score'] = score
        
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return results[:top_k]






