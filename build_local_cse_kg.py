"""
Download CSE-KG 2.0 data from SPARQL endpoint and build local graph
"""

import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from typing import Dict, List, Set, Optional
import json
import pickle
from pathlib import Path
from collections import defaultdict
import networkx as nx
import time


class CSEKGDownloader:
    """Download and build local CSE-KG 2.0 graph"""
    
    def __init__(self, endpoint: str = "http://cse.ckcest.cn/cskg/sparql"):
        self.endpoint = endpoint
        self.sparql = SPARQLWrapper(endpoint)
        self.sparql.setReturnFormat(JSON)
        self.namespace = "http://cse.ckcest.cn/cskg/"
        self.cskg = self.namespace
        
        # Local graph structure
        self.graph = nx.DiGraph()
        self.concepts = {}  # concept_id -> concept_info
        self.concept_keywords = defaultdict(set)  # keyword -> set of concept_ids
        
        # Output directory
        self.output_dir = Path("data/cse_kg_local")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def test_connection(self) -> bool:
        """Test if SPARQL endpoint is accessible"""
        print("Testing connection to CSE-KG 2.0 SPARQL endpoint...")
        try:
            query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT (COUNT(*) as ?count) WHERE {
                ?s ?p ?o .
            }
            LIMIT 1
            """
            self.sparql.setQuery(query)
            results = self.sparql.query().convert()
            print(f"[OK] Connection successful!")
            return True
        except Exception as e:
            print(f"[ERROR] Cannot connect to endpoint: {e}")
            return False
    
    def download_concepts(self, limit: int = 1000) -> List[Dict]:
        """Download concept entities from CSE-KG"""
        print(f"\nDownloading concepts (limit: {limit})...")
        
        query = f"""
        PREFIX cskg: <{self.cskg}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        
        SELECT DISTINCT ?concept ?label ?description ?type WHERE {{
            ?concept rdf:type ?type .
            FILTER(STRSTARTS(STR(?type), STR(cskg:)))
            OPTIONAL {{ ?concept rdfs:label ?label . }}
            OPTIONAL {{ ?concept rdfs:comment ?description . }}
            OPTIONAL {{ ?concept skos:definition ?description . }}
        }}
        LIMIT {limit}
        """
        
        try:
            self.sparql.setQuery(query)
            results = self.sparql.query().convert()
            bindings = results['results']['bindings']
            
            concepts = []
            for binding in bindings:
                concept_uri = binding['concept']['value']
                concept_id = concept_uri.replace(self.cskg, '').replace('cskg:', '')
                
                label = binding.get('label', {}).get('value', '')
                description = binding.get('description', {}).get('value', '')
                entity_type = binding.get('type', {}).get('value', '').replace(self.cskg, '')
                
                concepts.append({
                    'id': concept_id,
                    'uri': concept_uri,
                    'label': label,
                    'description': description,
                    'type': entity_type
                })
            
            print(f"  Downloaded {len(concepts)} concepts")
            return concepts
            
        except Exception as e:
            print(f"  [ERROR] Failed to download concepts: {e}")
            return []
    
    def download_relations(self, concepts: List[str], limit: int = 5000) -> List[Dict]:
        """Download relationships between concepts"""
        print(f"\nDownloading relations (limit: {limit})...")
        
        # Build filter for concept URIs
        concept_filters = " || ".join([
            f'STR(?source) = "{self.cskg}{c}"' for c in concepts[:100]  # Limit filter size
        ])
        
        query = f"""
        PREFIX cskg: <{self.cskg}>
        
        SELECT DISTINCT ?source ?relation ?target WHERE {{
            ?source ?relation ?target .
            FILTER(STRSTARTS(STR(?source), STR(cskg:)))
            FILTER(STRSTARTS(STR(?target), STR(cskg:)))
            FILTER(STRSTARTS(STR(?relation), STR(cskg:)))
            FILTER({concept_filters})
        }}
        LIMIT {limit}
        """
        
        try:
            self.sparql.setQuery(query)
            results = self.sparql.query().convert()
            bindings = results['results']['bindings']
            
            relations = []
            for binding in bindings:
                source_uri = binding['source']['value']
                target_uri = binding['target']['value']
                relation_uri = binding['relation']['value']
                
                source_id = source_uri.replace(self.cskg, '').replace('cskg:', '')
                target_id = target_uri.replace(self.cskg, '').replace('cskg:', '')
                relation_type = relation_uri.replace(self.cskg, '').replace('cskg:', '')
                
                relations.append({
                    'source': source_id,
                    'target': target_id,
                    'relation': relation_type
                })
            
            print(f"  Downloaded {len(relations)} relations")
            return relations
            
        except Exception as e:
            print(f"  [ERROR] Failed to download relations: {e}")
            return []
    
    def build_local_graph(self, concepts: List[Dict], relations: List[Dict]):
        """Build NetworkX graph from downloaded data"""
        print("\nBuilding local graph...")
        
        # Add nodes (concepts)
        for concept in concepts:
            concept_id = concept['id']
            self.graph.add_node(concept_id, **concept)
            self.concepts[concept_id] = concept
            
            # Build keyword index
            if concept['label']:
                keywords = self._extract_keywords(concept['label'])
                for keyword in keywords:
                    self.concept_keywords[keyword].add(concept_id)
            
            if concept['description']:
                keywords = self._extract_keywords(concept['description'])
                for keyword in keywords:
                    self.concept_keywords[keyword].add(concept_id)
        
        # Add edges (relations)
        for relation in relations:
            source = relation['source']
            target = relation['target']
            rel_type = relation['relation']
            
            if source in self.graph and target in self.graph:
                self.graph.add_edge(source, target, relation=rel_type)
        
        print(f"  Graph built: {len(self.graph.nodes())} nodes, {len(self.graph.edges())} edges")
        print(f"  Keyword index: {len(self.concept_keywords)} keywords")
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords from text"""
        import re
        # Remove special characters, split by spaces
        words = re.sub(r'[^\w\s]', ' ', text.lower()).split()
        # Filter meaningful words
        keywords = {w for w in words if len(w) > 2 and w not in ['the', 'and', 'for', 'are', 'with']}
        return keywords
    
    def save_local_graph(self):
        """Save local graph to files"""
        print("\nSaving local graph...")
        
        # Save graph as JSON
        graph_data = {
            'nodes': [
                {
                    'id': node,
                    **self.graph.nodes[node]
                }
                for node in self.graph.nodes()
            ],
            'edges': [
                {
                    'source': edge[0],
                    'target': edge[1],
                    'relation': self.graph.edges[edge].get('relation', 'relatedTo')
                }
                for edge in self.graph.edges()
            ]
        }
        
        graph_file = self.output_dir / "graph.json"
        with open(graph_file, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        print(f"  Saved graph to {graph_file}")
        
        # Save keyword index
        keyword_index = {
            keyword: list(concept_ids) 
            for keyword, concept_ids in self.concept_keywords.items()
        }
        
        keyword_file = self.output_dir / "keyword_index.json"
        with open(keyword_file, 'w', encoding='utf-8') as f:
            json.dump(keyword_index, f, indent=2, ensure_ascii=False)
        print(f"  Saved keyword index to {keyword_file}")
        
        # Save NetworkX graph as pickle
        graph_pickle = self.output_dir / "graph.pkl"
        with open(graph_pickle, 'wb') as f:
            pickle.dump(self.graph, f)
        print(f"  Saved NetworkX graph to {graph_pickle}")
        
        # Save concepts dictionary
        concepts_file = self.output_dir / "concepts.json"
        with open(concepts_file, 'w', encoding='utf-8') as f:
            json.dump(self.concepts, f, indent=2, ensure_ascii=False)
        print(f"  Saved concepts to {concepts_file}")
    
    def download_and_build(self, concept_limit: int = 1000, relation_limit: int = 5000):
        """Main method to download and build local graph"""
        print("="*80)
        print("CSE-KG 2.0 LOCAL GRAPH BUILDER")
        print("="*80)
        
        # Test connection
        if not self.test_connection():
            print("\n[WARNING] Cannot connect to SPARQL endpoint.")
            print("Will create a minimal local graph with common CS concepts...")
            self._create_fallback_graph()
            self.save_local_graph()
            return
        
        # Download concepts
        concepts = self.download_concepts(limit=concept_limit)
        if not concepts:
            print("\n[WARNING] No concepts downloaded. Creating fallback graph...")
            self._create_fallback_graph()
            self.save_local_graph()
            return
        
        # Download relations
        concept_ids = [c['id'] for c in concepts]
        relations = self.download_relations(concept_ids, limit=relation_limit)
        
        # Build graph
        self.build_local_graph(concepts, relations)
        
        # Save
        self.save_local_graph()
        
        print("\n" + "="*80)
        print("LOCAL GRAPH BUILD COMPLETE!")
        print("="*80)
        print(f"Graph saved to: {self.output_dir.absolute()}")
        print(f"Nodes: {len(self.graph.nodes())}")
        print(f"Edges: {len(self.graph.edges())}")
        print(f"Keywords indexed: {len(self.concept_keywords)}")
    
    def _create_fallback_graph(self):
        """Create a fallback graph with common CS concepts if download fails"""
        print("\nCreating fallback graph with common CS concepts...")
        
        # Common CS concepts
        common_concepts = [
            {'id': 'recursion', 'label': 'Recursion', 'description': 'A programming technique where a function calls itself', 'type': 'Concept', 'uri': f'{self.cskg}recursion'},
            {'id': 'iteration', 'label': 'Iteration', 'description': 'Repeating a process or loop', 'type': 'Concept', 'uri': f'{self.cskg}iteration'},
            {'id': 'array', 'label': 'Array', 'description': 'A data structure that stores elements in contiguous memory', 'type': 'Concept', 'uri': f'{self.cskg}array'},
            {'id': 'linked_list', 'label': 'Linked List', 'description': 'A linear data structure with nodes connected by pointers', 'type': 'Concept', 'uri': f'{self.cskg}linked_list'},
            {'id': 'tree', 'label': 'Tree', 'description': 'A hierarchical data structure with nodes and edges', 'type': 'Concept', 'uri': f'{self.cskg}tree'},
            {'id': 'graph', 'label': 'Graph', 'description': 'A data structure with vertices and edges', 'type': 'Concept', 'uri': f'{self.cskg}graph'},
            {'id': 'sorting', 'label': 'Sorting', 'description': 'Arranging data in a particular order', 'type': 'Task', 'uri': f'{self.cskg}sorting'},
            {'id': 'searching', 'label': 'Searching', 'description': 'Finding an element in a data structure', 'type': 'Task', 'uri': f'{self.cskg}searching'},
            {'id': 'dynamic_programming', 'label': 'Dynamic Programming', 'description': 'Solving complex problems by breaking them into simpler subproblems', 'type': 'Method', 'uri': f'{self.cskg}dynamic_programming'},
            {'id': 'greedy_algorithm', 'label': 'Greedy Algorithm', 'description': 'Making locally optimal choices at each step', 'type': 'Method', 'uri': f'{self.cskg}greedy_algorithm'},
            {'id': 'object_oriented_programming', 'label': 'Object-Oriented Programming', 'description': 'Programming paradigm based on objects and classes', 'type': 'Concept', 'uri': f'{self.cskg}object_oriented_programming'},
            {'id': 'inheritance', 'label': 'Inheritance', 'description': 'Mechanism where a class derives properties from another class', 'type': 'Concept', 'uri': f'{self.cskg}inheritance'},
            {'id': 'polymorphism', 'label': 'Polymorphism', 'description': 'Ability of objects to take multiple forms', 'type': 'Concept', 'uri': f'{self.cskg}polymorphism'},
            {'id': 'exception_handling', 'label': 'Exception Handling', 'description': 'Mechanism to handle runtime errors', 'type': 'Concept', 'uri': f'{self.cskg}exception_handling'},
            {'id': 'pointer', 'label': 'Pointer', 'description': 'Variable that stores memory address', 'type': 'Concept', 'uri': f'{self.cskg}pointer'},
        ]
        
        # Common relations
        common_relations = [
            {'source': 'recursion', 'target': 'function', 'relation': 'usesMethod'},
            {'source': 'linked_list', 'target': 'pointer', 'relation': 'requiresKnowledge'},
            {'source': 'tree', 'target': 'node', 'relation': 'requiresKnowledge'},
            {'source': 'graph', 'target': 'tree', 'relation': 'relatedTo'},
            {'source': 'sorting', 'target': 'array', 'relation': 'usesMethod'},
            {'source': 'searching', 'target': 'array', 'relation': 'usesMethod'},
            {'source': 'dynamic_programming', 'target': 'recursion', 'relation': 'relatedTo'},
            {'source': 'object_oriented_programming', 'target': 'inheritance', 'relation': 'requiresKnowledge'},
            {'source': 'object_oriented_programming', 'target': 'polymorphism', 'relation': 'requiresKnowledge'},
        ]
        
        self.build_local_graph(common_concepts, common_relations)


if __name__ == "__main__":
    downloader = CSEKGDownloader()
    downloader.download_and_build(concept_limit=1000, relation_limit=5000)


