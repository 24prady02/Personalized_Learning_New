"""
Build the real CSE-KG 2.0 graph structure from downloaded Turtle files
Extracts all nodes (concepts, methods, tasks) and edges (relationships)
"""

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, RDFS
from pathlib import Path
import json
import pickle
import networkx as nx
from collections import defaultdict
from tqdm import tqdm

class RealCSEKGBuilder:
    """Build graph structure from real CSE-KG 2.0 Turtle files"""
    
    def __init__(self):
        self.data_dir = Path("data/cse_kg_full/extracted/cskg")
        self.output_dir = Path("data/cse_kg_full")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Namespaces
        self.cskg = Namespace("http://scholkg.kmi.open.ac.uk/cskg/resource/")
        self.cskg_ont = Namespace("http://scholkg.kmi.open.ac.uk/cskg/ontology#")
        
        # Graph structures
        self.rdf_graph = Graph()
        self.nx_graph = nx.DiGraph()
        self.concepts = {}
        self.relations = []
        self.concept_keywords = defaultdict(set)
        
    def load_all_turtle_files(self):
        """Load all Turtle files into RDF graph - FAST VERSION"""
        print("="*80)
        print("LOADING ALL CSE-KG 2.0 TURTLE FILES (FAST MODE)")
        print("="*80)
        
        ttl_files = sorted(list(self.data_dir.glob("*.ttl")))
        print(f"Found {len(ttl_files)} Turtle files")
        
        # Process files in batches for faster loading
        batch_size = 10
        for i in tqdm(range(0, len(ttl_files), batch_size), desc="Loading batches"):
            batch = ttl_files[i:i+batch_size]
            for ttl_file in batch:
                try:
                    # Parse directly without storing full graph initially
                    temp_graph = Graph()
                    temp_graph.parse(str(ttl_file), format='turtle')
                    # Add to main graph
                    for triple in temp_graph:
                        self.rdf_graph.add(triple)
                except Exception as e:
                    continue
        
        print(f"\n[SUCCESS] Loaded {len(self.rdf_graph)} triples from RDF graph")
        return len(self.rdf_graph) > 0
    
    def extract_concepts(self):
        """Extract all concepts, methods, tasks from the graph - FAST VERSION"""
        print("\n" + "="*80)
        print("EXTRACTING CONCEPTS, METHODS, TASKS (FAST MODE)")
        print("="*80)
        
        # Get all unique subjects and objects that are CSE-KG resources - FAST
        entities = set()
        cskg_str = str(self.cskg)
        
        print("Collecting entities...")
        # Use iterator for faster processing
        triples = list(self.rdf_graph)
        for subject, predicate, obj in tqdm(triples, desc="Processing triples"):
            # Add subjects
            subj_str = str(subject)
            if subj_str.startswith(cskg_str):
                entities.add(subject)
            # Add objects that are resources
            obj_str = str(obj)
            if isinstance(obj, URIRef) and obj_str.startswith(cskg_str):
                entities.add(obj)
        
        print(f"Found {len(entities)} unique entities")
        
        # Extract information for each entity - FAST with batching
        print("\nExtracting entity information...")
        entities_list = list(entities)
        cskg_str = str(self.cskg)
        
        for entity in tqdm(entities_list, desc="Processing entities"):
            entity_str = str(entity)
            entity_id = entity_str.replace(cskg_str, "").replace("cskg:", "")
            
            # Get labels - faster lookup
            labels = [str(o) for o in self.rdf_graph.objects(entity, RDFS.label)]
            label = labels[0] if labels else entity_id
            
            # Get descriptions - only first one
            comments = [str(o) for o in self.rdf_graph.objects(entity, RDFS.comment)]
            description = comments[0] if comments else ""
            
            # Get type - simplified
            types = [str(o) for o in self.rdf_graph.objects(entity, RDF.type)]
            entity_type = "Concept"
            if types:
                type_str = types[0]
                if "Method" in type_str:
                    entity_type = "Method"
                elif "Task" in type_str:
                    entity_type = "Task"
                elif "Material" in type_str:
                    entity_type = "Material"
            
            # Store concept
            self.concepts[entity_id] = {
                'id': entity_id,
                'uri': entity_str,
                'label': label,
                'description': description,
                'type': entity_type
            }
            
            # Add to NetworkX graph
            self.nx_graph.add_node(entity_id, **self.concepts[entity_id])
            
            # Build keyword index - only for non-empty labels
            if label and label != entity_id:
                keywords = self._extract_keywords(label)
                for keyword in keywords:
                    self.concept_keywords[keyword].add(entity_id)
        
        print(f"\n[SUCCESS] Extracted {len(self.concepts)} concepts")
        return len(self.concepts) > 0
    
    def extract_relations(self):
        """Extract all relationships between concepts - FAST VERSION"""
        print("\n" + "="*80)
        print("EXTRACTING RELATIONSHIPS (FAST MODE)")
        print("="*80)
        
        # Extract statement triples - FAST with pre-filtering
        print("Processing relationships...")
        cskg_str = str(self.cskg)
        cskg_ont_str = str(self.cskg_ont)
        concepts_set = set(self.concepts.keys())  # For fast lookup
        
        triples = list(self.rdf_graph)
        for subject, predicate, obj in tqdm(triples, desc="Extracting relations"):
            # Fast string checks
            if not isinstance(subject, URIRef) or not isinstance(obj, URIRef):
                continue
                
            source_str = str(subject)
            target_str = str(obj)
            
            if not (source_str.startswith(cskg_str) and target_str.startswith(cskg_str)):
                continue
            
            source_id = source_str.replace(cskg_str, "").replace("cskg:", "")
            target_id = target_str.replace(cskg_str, "").replace("cskg:", "")
            
            # Only process if both nodes exist
            if source_id not in concepts_set or target_id not in concepts_set:
                continue
            
            predicate_str = str(predicate)
            
            # Extract relation type - fast
            if predicate_str.startswith(cskg_ont_str):
                relation_type = predicate_str.replace(cskg_ont_str, "").replace("cskg-ont:", "")
            else:
                relation_type = predicate_str.split('/')[-1].split('#')[-1]
            
            self.relations.append({
                'source': source_id,
                'target': target_id,
                'relation': relation_type
            })
            
            # Add edge to NetworkX graph
            self.nx_graph.add_edge(source_id, target_id, relation=relation_type)
        
        print(f"\n[SUCCESS] Extracted {len(self.relations)} relationships")
        return len(self.relations) > 0
    
    def _extract_keywords(self, text: str):
        """Extract keywords from text"""
        import re
        words = re.sub(r'[^\w\s]', ' ', text.lower()).split()
        keywords = {w for w in words if len(w) > 2 and w not in ['the', 'and', 'for', 'are', 'with', 'from']}
        return keywords
    
    def save_graph_structure(self):
        """Save the complete graph structure"""
        print("\n" + "="*80)
        print("SAVING GRAPH STRUCTURE")
        print("="*80)
        
        # Save concepts (nodes)
        concepts_file = self.output_dir / "concepts.json"
        print(f"Saving {len(self.concepts)} concepts...")
        with open(concepts_file, 'w', encoding='utf-8') as f:
            json.dump(self.concepts, f, indent=2, ensure_ascii=False)
        print(f"  [OK] Saved to {concepts_file}")
        
        # Save relations (edges)
        relations_file = self.output_dir / "relations.json"
        print(f"Saving {len(self.relations)} relations...")
        with open(relations_file, 'w', encoding='utf-8') as f:
            json.dump(self.relations, f, indent=2, ensure_ascii=False)
        print(f"  [OK] Saved to {relations_file}")
        
        # Save NetworkX graph
        graph_file = self.output_dir / "graph.pkl"
        print(f"Saving NetworkX graph ({len(self.nx_graph.nodes())} nodes, {len(self.nx_graph.edges())} edges)...")
        with open(graph_file, 'wb') as f:
            pickle.dump(self.nx_graph, f)
        print(f"  [OK] Saved to {graph_file}")
        
        # Save keyword index
        keyword_index = {
            keyword: list(concept_ids) 
            for keyword, concept_ids in self.concept_keywords.items()
        }
        keyword_file = self.output_dir / "keyword_index.json"
        print(f"Saving {len(keyword_index)} keyword mappings...")
        with open(keyword_file, 'w', encoding='utf-8') as f:
            json.dump(keyword_index, f, indent=2, ensure_ascii=False)
        print(f"  [OK] Saved to {keyword_file}")
        
        # Save graph structure as JSON (for visualization)
        graph_json = {
            'nodes': [
                {
                    'id': node,
                    **self.nx_graph.nodes[node]
                }
                for node in self.nx_graph.nodes()
            ],
            'edges': [
                {
                    'source': edge[0],
                    'target': edge[1],
                    'relation': self.nx_graph.edges[edge].get('relation', 'relatedTo')
                }
                for edge in self.nx_graph.edges()
            ]
        }
        graph_json_file = self.output_dir / "graph_structure.json"
        print(f"Saving graph structure JSON...")
        with open(graph_json_file, 'w', encoding='utf-8') as f:
            json.dump(graph_json, f, indent=2, ensure_ascii=False)
        print(f"  [OK] Saved to {graph_json_file}")
        
        # Save summary
        summary = {
            'source': 'CSE-KG 2.0 Full Dataset (Real Data)',
            'num_concepts': len(self.concepts),
            'num_relations': len(self.relations),
            'num_nodes': len(self.nx_graph.nodes()),
            'num_edges': len(self.nx_graph.edges()),
            'num_keywords': len(keyword_index),
            'graph_density': nx.density(self.nx_graph),
            'is_connected': nx.is_weakly_connected(self.nx_graph) if len(self.nx_graph.nodes()) > 0 else False
        }
        summary_file = self.output_dir / "summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"  [OK] Saved summary to {summary_file}")
        
        print("\n" + "="*80)
        print("GRAPH STRUCTURE BUILD COMPLETE!")
        print("="*80)
        print(f"Nodes: {len(self.nx_graph.nodes())}")
        print(f"Edges: {len(self.nx_graph.edges())}")
        print(f"Concepts: {len(self.concepts)}")
        print(f"Relations: {len(self.relations)}")
        print(f"Keywords indexed: {len(keyword_index)}")
        print(f"\nSaved to: {self.output_dir.absolute()}")
    
    def build(self):
        """Main method to build the graph"""
        # Load Turtle files
        if not self.load_all_turtle_files():
            print("[ERROR] Failed to load Turtle files")
            return False
        
        # Extract concepts
        if not self.extract_concepts():
            print("[ERROR] Failed to extract concepts")
            return False
        
        # Extract relations
        if not self.extract_relations():
            print("[WARNING] No relations extracted, but continuing...")
        
        # Save everything
        self.save_graph_structure()
        
        return True


if __name__ == "__main__":
    builder = RealCSEKGBuilder()
    builder.build()

