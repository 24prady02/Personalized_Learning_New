"""
Build a working knowledge graph retrieval system using MOOCCubeX data
This will create a local graph structure that can be queried for concept retrieval
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import networkx as nx


class MOOCCubeXKnowledgeGraph:
    """Build and query knowledge graph from MOOCCubeX data"""
    
    def __init__(self, data_path: str = "data/moocsxcube"):
        self.data_path = Path(data_path)
        self.graph = nx.DiGraph()
        self.concept_map = {}  # concept_id -> concept_name
        self.concept_keywords = defaultdict(set)  # keyword -> set of concept_ids
        self.concept_videos = defaultdict(list)  # concept_id -> list of video_ids
        self.concept_problems = defaultdict(list)  # concept_id -> list of problem_ids
        
        print("Building knowledge graph from MOOCCubeX...")
        self._load_entities()
        self._load_relations()
        self._build_keyword_index()
        print(f"[OK] Knowledge graph built: {len(self.graph.nodes())} nodes, {len(self.graph.edges())} edges")
    
    def _load_entities(self):
        """Load entities from MOOCCubeX"""
        entities_path = self.data_path / 'entities.json'
        if not entities_path.exists():
            print(f"[WARNING] {entities_path} not found")
            return
        
        print("  Loading entities...")
        with open(entities_path, 'r', encoding='utf-8') as f:
            entities = json.load(f)
        
        # Load concepts
        concepts = entities.get('concept', [])
        print(f"  Found {len(concepts)} concepts")
        
        for concept in concepts[:1000]:  # Limit to first 1000 for performance
            concept_id = concept.get('id', '')
            if not concept_id:
                continue
            
            # Extract concept name (remove ID prefix if present)
            concept_name = concept_id.replace('concept_', '').replace('K_', '')
            
            # Filter for CS-related concepts
            if '计算机' in concept_id or 'computer' in concept_id.lower() or self._is_cs_concept(concept_id):
                self.concept_map[concept_id] = concept_name
                self.graph.add_node(concept_id, name=concept_name, type='concept')
    
    def _is_cs_concept(self, concept_id: str) -> bool:
        """Check if concept is CS-related"""
        cs_keywords = [
            'recursion', 'function', 'array', 'list', 'tree', 'graph', 'sort', 'search',
            'algorithm', 'data structure', 'programming', 'code', 'variable', 'loop',
            'class', 'object', 'inheritance', 'polymorphism', 'pointer', 'stack', 'queue',
            'hash', 'binary', 'linked', 'node', 'pointer', 'memory', 'recursive'
        ]
        concept_lower = concept_id.lower()
        return any(keyword in concept_lower for keyword in cs_keywords)
    
    def _load_relations(self):
        """Load relations from MOOCCubeX"""
        relations_dir = self.data_path / 'relations'
        if not relations_dir.exists():
            print(f"[WARNING] {relations_dir} not found")
            return
        
        print("  Loading relations...")
        
        # Load concept-video relations
        cv_path = relations_dir / 'concept-video.txt'
        if cv_path.exists():
            print(f"  Loading concept-video relations from {cv_path.name}...")
            with open(cv_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f):
                    if line_num >= 10000:  # Limit for performance
                        break
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        concept_id, video_id = parts[0], parts[1]
                        if concept_id in self.concept_map:
                            self.concept_videos[concept_id].append(video_id)
                            # Add video as node
                            if not self.graph.has_node(video_id):
                                self.graph.add_node(video_id, type='video')
                            # Add edge
                            self.graph.add_edge(concept_id, video_id, relation='has_video')
            
            print(f"    Loaded {sum(len(v) for v in self.concept_videos.values())} concept-video relations")
        
        # Load concept-problem relations
        cp_path = relations_dir / 'concept-problem.txt'
        if cp_path.exists():
            print(f"  Loading concept-problem relations from {cp_path.name}...")
            with open(cp_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f):
                    if line_num >= 10000:  # Limit for performance
                        break
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        concept_id, problem_id = parts[0], parts[1]
                        if concept_id in self.concept_map:
                            self.concept_problems[concept_id].append(problem_id)
                            # Add problem as node
                            if not self.graph.has_node(problem_id):
                                self.graph.add_node(problem_id, type='problem')
                            # Add edge
                            self.graph.add_edge(concept_id, problem_id, relation='has_problem')
            
            print(f"    Loaded {sum(len(v) for v in self.concept_problems.values())} concept-problem relations")
        
        # Build concept-concept relationships based on shared videos/problems
        print("  Building concept-concept relationships...")
        self._build_concept_relationships()
    
    def _build_concept_relationships(self):
        """Build relationships between concepts based on shared resources"""
        # Concepts that share videos are related
        video_to_concepts = defaultdict(list)
        for concept_id, videos in self.concept_videos.items():
            for video_id in videos:
                video_to_concepts[video_id].append(concept_id)
        
        # Add edges between concepts that share videos
        for video_id, concepts in video_to_concepts.items():
            if len(concepts) > 1:
                for i, c1 in enumerate(concepts):
                    for c2 in concepts[i+1:]:
                        if not self.graph.has_edge(c1, c2):
                            self.graph.add_edge(c1, c2, relation='related_to', weight=1.0)
                        else:
                            # Increase weight
                            self.graph[c1][c2]['weight'] = self.graph[c1][c2].get('weight', 1.0) + 0.5
        
        # Concepts that share problems are related
        problem_to_concepts = defaultdict(list)
        for concept_id, problems in self.concept_problems.items():
            for problem_id in problems:
                problem_to_concepts[problem_id].append(concept_id)
        
        for problem_id, concepts in problem_to_concepts.items():
            if len(concepts) > 1:
                for i, c1 in enumerate(concepts):
                    for c2 in concepts[i+1:]:
                        if not self.graph.has_edge(c1, c2):
                            self.graph.add_edge(c1, c2, relation='related_to', weight=1.0)
                        else:
                            self.graph[c1][c2]['weight'] = self.graph[c1][c2].get('weight', 1.0) + 0.5
    
    def _build_keyword_index(self):
        """Build keyword index for concept retrieval"""
        print("  Building keyword index...")
        
        for concept_id, concept_name in self.concept_map.items():
            # Extract keywords from concept name
            keywords = self._extract_keywords(concept_name)
            for keyword in keywords:
                self.concept_keywords[keyword].add(concept_id)
        
        print(f"    Indexed {len(self.concept_keywords)} keywords for {len(self.concept_map)} concepts")
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords from text"""
        # Remove special characters, split by common delimiters
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        keywords = set()
        for word in words:
            if len(word) > 2:  # Skip very short words
                keywords.add(word)
        
        # Also add common programming terms
        programming_terms = {
            'recursion', 'recursive', 'function', 'array', 'list', 'tree', 'graph',
            'sort', 'search', 'algorithm', 'data', 'structure', 'programming',
            'variable', 'loop', 'class', 'object', 'inheritance', 'polymorphism',
            'pointer', 'stack', 'queue', 'hash', 'binary', 'linked', 'node'
        }
        
        for term in programming_terms:
            if term in text.lower():
                keywords.add(term)
        
        return keywords
    
    def retrieve_concepts_from_code(self, code: str, error_message: str = None, top_k: int = 5) -> List[str]:
        """Retrieve concepts from code using graph structure"""
        text = code.lower()
        if error_message:
            text += " " + error_message.lower()
        
        # Score concepts based on keyword matches
        concept_scores = defaultdict(float)
        
        for keyword, concept_ids in self.concept_keywords.items():
            if keyword in text:
                for concept_id in concept_ids:
                    concept_scores[concept_id] += 1.0
        
        # Boost scores for concepts with more connections (more important)
        for concept_id in concept_scores:
            degree = self.graph.degree(concept_id)
            concept_scores[concept_id] *= (1.0 + degree * 0.1)  # Boost by connectivity
        
        # Sort by score
        ranked = sorted(concept_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return concept names
        results = []
        for concept_id, score in ranked[:top_k]:
            concept_name = self.concept_map.get(concept_id, concept_id)
            results.append(concept_name)
        
        return results
    
    def retrieve_concepts_from_query(self, query: str, top_k: int = 5) -> List[Dict]:
        """Retrieve concepts from natural language query"""
        keywords = query.lower().split()
        
        concept_scores = defaultdict(float)
        
        for keyword in keywords:
            if keyword in self.concept_keywords:
                for concept_id in self.concept_keywords[keyword]:
                    concept_scores[concept_id] += 1.0
        
        # Boost by graph connectivity
        for concept_id in concept_scores:
            degree = self.graph.degree(concept_id)
            concept_scores[concept_id] *= (1.0 + degree * 0.1)
        
        ranked = sorted(concept_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for concept_id, score in ranked[:top_k]:
            concept_name = self.concept_map.get(concept_id, concept_id)
            videos = self.concept_videos.get(concept_id, [])
            problems = self.concept_problems.get(concept_id, [])
            
            results.append({
                'concept_id': concept_id,
                'concept_name': concept_name,
                'score': score,
                'num_videos': len(videos),
                'num_problems': len(problems),
                'degree': self.graph.degree(concept_id)
            })
        
        return results
    
    def get_related_concepts(self, concept_id: str, max_distance: int = 1) -> List[Tuple[str, str, int]]:
        """Get related concepts using graph traversal"""
        if concept_id not in self.graph:
            return []
        
        related = []
        visited = set()
        
        # BFS to find related concepts
        queue = [(concept_id, 0)]  # (node, distance)
        visited.add(concept_id)
        
        while queue:
            current, distance = queue.pop(0)
            
            if distance > max_distance:
                continue
            
            # Get neighbors
            for neighbor in self.graph.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    edge_data = self.graph.get_edge_data(current, neighbor, {})
                    relation = edge_data.get('relation', 'related_to')
                    related.append((neighbor, relation, distance + 1))
                    queue.append((neighbor, distance + 1))
        
        return related
    
    def get_concept_info(self, concept_id: str) -> Dict:
        """Get information about a concept"""
        if concept_id not in self.graph:
            return None
        
        concept_name = self.concept_map.get(concept_id, concept_id)
        videos = self.concept_videos.get(concept_id, [])
        problems = self.concept_problems.get(concept_id, [])
        related = self.get_related_concepts(concept_id, max_distance=1)
        
        return {
            'concept_id': concept_id,
            'concept_name': concept_name,
            'videos': videos[:10],  # Limit
            'problems': problems[:10],  # Limit
            'related_concepts': [
                {
                    'concept_id': r[0],
                    'concept_name': self.concept_map.get(r[0], r[0]),
                    'relation': r[1],
                    'distance': r[2]
                }
                for r in related[:10]
            ],
            'degree': self.graph.degree(concept_id)
        }
    
    def save_graph(self, output_path: str = "data/moocsxcube/kg_graph.json"):
        """Save graph structure to JSON"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        graph_data = {
            'nodes': [
                {
                    'id': node,
                    'name': self.concept_map.get(node, node),
                    'type': self.graph.nodes[node].get('type', 'unknown'),
                    'degree': self.graph.degree(node)
                }
                for node in self.graph.nodes()
            ],
            'edges': [
                {
                    'source': edge[0],
                    'target': edge[1],
                    'relation': self.graph.edges[edge].get('relation', 'unknown'),
                    'weight': self.graph.edges[edge].get('weight', 1.0)
                }
                for edge in self.graph.edges()
            ],
            'statistics': {
                'num_nodes': len(self.graph.nodes()),
                'num_edges': len(self.graph.edges()),
                'num_concepts': len(self.concept_map),
                'num_videos': sum(len(v) for v in self.concept_videos.values()),
                'num_problems': sum(len(v) for v in self.concept_problems.values())
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Graph saved to {output_path}")
        return graph_data


def test_kg_retrieval():
    """Test the knowledge graph retrieval"""
    print("="*80)
    print("TESTING MOOCCubeX KNOWLEDGE GRAPH RETRIEVAL")
    print("="*80)
    
    # Build graph
    kg = MOOCCubeXKnowledgeGraph()
    
    # Test 1: Retrieve from code
    print("\n1. Testing concept retrieval from code:")
    code = "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)"
    concepts = kg.retrieve_concepts_from_code(code, top_k=5)
    print(f"   Code: {code[:50]}...")
    print(f"   Retrieved concepts: {concepts}")
    
    # Test 2: Retrieve from query
    print("\n2. Testing concept retrieval from query:")
    query = "I'm struggling with recursion and base cases"
    results = kg.retrieve_concepts_from_query(query, top_k=5)
    print(f"   Query: '{query}'")
    for i, result in enumerate(results, 1):
        print(f"   {i}. {result['concept_name']} (score: {result['score']:.2f}, degree: {result['degree']})")
    
    # Test 3: Get related concepts
    if results:
        print("\n3. Testing related concepts:")
        concept_id = results[0]['concept_id']
        related = kg.get_related_concepts(concept_id, max_distance=2)
        print(f"   Concept: {results[0]['concept_name']}")
        print(f"   Related concepts: {len(related)}")
        for r in related[:5]:
            concept_name = kg.concept_map.get(r[0], r[0])
            print(f"      - {concept_name} (via {r[1]}, distance: {r[2]})")
    
    # Test 4: Get concept info
    if results:
        print("\n4. Testing concept info:")
        concept_id = results[0]['concept_id']
        info = kg.get_concept_info(concept_id)
        if info:
            print(f"   Concept: {info['concept_name']}")
            print(f"   Videos: {len(info['videos'])}")
            print(f"   Problems: {len(info['problems'])}")
            print(f"   Related: {len(info['related_concepts'])}")
            print(f"   Degree: {info['degree']}")
    
    # Save graph
    print("\n5. Saving graph structure...")
    graph_data = kg.save_graph()
    
    print("\n" + "="*80)
    print("GRAPH STATISTICS")
    print("="*80)
    stats = graph_data['statistics']
    print(f"Nodes: {stats['num_nodes']}")
    print(f"Edges: {stats['num_edges']}")
    print(f"Concepts: {stats['num_concepts']}")
    print(f"Videos: {stats['num_videos']}")
    print(f"Problems: {stats['num_problems']}")
    print("="*80)
    
    return kg


if __name__ == "__main__":
    kg = test_kg_retrieval()















