"""
Actually download REAL CSE-KG 2.0 data from the SPARQL endpoint
This will query the endpoint and download actual concepts and relationships
"""

from SPARQLWrapper import SPARQLWrapper, JSON
import json
import json as json_lib
from pathlib import Path
from collections import defaultdict
import networkx as nx
import pickle
import time

class RealCSEKGDownloader:
    """Download REAL CSE-KG 2.0 data from SPARQL endpoint"""
    
    def __init__(self):
        self.endpoint = "http://w3id.org/cskg/sparql"
        self.sparql = SPARQLWrapper(self.endpoint)
        self.sparql.setReturnFormat(JSON)
        self.namespace = "https://w3id.org/cskg/resource/"
        
        self.output_dir = Path("data/cse_kg_real")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.concepts = {}
        self.relations = []
        self.graph = nx.DiGraph()
        self.concept_keywords = defaultdict(set)
    
    def download_real_concepts(self, limit=500):
        """Download REAL concepts from CSE-KG 2.0"""
        print(f"\n{'='*80}")
        print("DOWNLOADING REAL CSE-KG 2.0 CONCEPTS FROM SPARQL ENDPOINT")
        print(f"{'='*80}")
        print(f"Endpoint: {self.endpoint}")
        print(f"Limit: {limit} concepts")
        
        # Query for concepts (Methods, Tasks, Concepts, etc.)
        query = f"""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX cskg: <{self.namespace}>
        
        SELECT DISTINCT ?concept ?label ?description ?type WHERE {{
            ?concept rdf:type ?type .
            FILTER(STRSTARTS(STR(?type), STR(cskg:)) || STRSTARTS(STR(?type), "https://w3id.org/cskg/ontology#"))
            OPTIONAL {{ ?concept rdfs:label ?label . }}
            OPTIONAL {{ ?concept rdfs:comment ?description . }}
        }}
        LIMIT {limit}
        """
        
        print("\nExecuting SPARQL query...")
        try:
            self.sparql.setQuery(query)
            response = self.sparql.query()
            
            # Handle response - might be bytes or dict
            if hasattr(response, 'convert'):
                results = response.convert()
            else:
                # Try to parse as JSON
                import json as json_lib
                if isinstance(response, bytes):
                    results = json_lib.loads(response.decode('utf-8'))
                else:
                    results = response
            
            # Handle different response formats
            if isinstance(results, dict):
                bindings = results.get('results', {}).get('bindings', [])
            elif isinstance(results, bytes):
                try:
                    results = json_lib.loads(results.decode('utf-8'))
                    bindings = results.get('results', {}).get('bindings', [])
                except:
                    print(f"  [WARNING] Could not parse bytes response. Response preview: {results[:200]}")
                    bindings = []
            else:
                print(f"  [WARNING] Unexpected response type: {type(results)}")
                print(f"  Response preview: {str(results)[:200]}")
                bindings = []
            
            print(f"  Received {len(bindings)} results from SPARQL endpoint")
            
            for binding in bindings:
                concept_uri = binding['concept']['value']
                concept_id = concept_uri.replace(self.namespace, '').replace('cskg:', '')
                
                label = binding.get('label', {}).get('value', '') if 'label' in binding else ''
                description = binding.get('description', {}).get('value', '') if 'description' in binding else ''
                entity_type = binding.get('type', {}).get('value', '') if 'type' in binding else ''
                
                # Extract type name
                if '/' in entity_type:
                    entity_type = entity_type.split('/')[-1]
                
                self.concepts[concept_id] = {
                    'id': concept_id,
                    'uri': concept_uri,
                    'label': label or concept_id,
                    'description': description,
                    'type': entity_type
                }
                
                # Add to graph
                self.graph.add_node(concept_id, **self.concepts[concept_id])
                
                # Build keyword index
                if label:
                    keywords = self._extract_keywords(label)
                    for keyword in keywords:
                        self.concept_keywords[keyword].add(concept_id)
            
            print(f"  [SUCCESS] Downloaded {len(self.concepts)} REAL concepts from CSE-KG 2.0!")
            return True
            
        except Exception as e:
            print(f"  [ERROR] Failed to download: {e}")
            print(f"  Error type: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            return False
    
    def download_real_relations(self, limit=1000):
        """Download REAL relationships between concepts"""
        if not self.concepts:
            print("[WARNING] No concepts downloaded yet. Run download_real_concepts() first.")
            return False
        
        print(f"\nDownloading REAL relationships (limit: {limit})...")
        
        # Get first 50 concept URIs for relation queries
        concept_uris = [c['uri'] for c in list(self.concepts.values())[:50]]
        
        # Query for relationships
        uri_filters = " || ".join([f'STR(?source) = "{uri}"' for uri in concept_uris[:20]])
        
        query = f"""
        PREFIX cskg: <{self.namespace}>
        
        SELECT DISTINCT ?source ?relation ?target WHERE {{
            ?source ?relation ?target .
            FILTER(STRSTARTS(STR(?source), STR(cskg:)))
            FILTER(STRSTARTS(STR(?target), STR(cskg:)))
            FILTER(STRSTARTS(STR(?relation), STR(cskg:)) || STRSTARTS(STR(?relation), "https://w3id.org/cskg/ontology#"))
            FILTER({uri_filters})
        }}
        LIMIT {limit}
        """
        
        try:
            self.sparql.setQuery(query)
            results = self.sparql.query().convert()
            bindings = results.get('results', {}).get('bindings', [])
            
            print(f"  Received {len(bindings)} relationships from SPARQL endpoint")
            
            for binding in bindings:
                source_uri = binding['source']['value']
                target_uri = binding['target']['value']
                relation_uri = binding['relation']['value']
                
                source_id = source_uri.replace(self.namespace, '').replace('cskg:', '')
                target_id = target_uri.replace(self.namespace, '').replace('cskg:', '')
                relation_type = relation_uri.split('/')[-1].split('#')[-1]
                
                # Only add if both nodes exist
                if source_id in self.concepts and target_id in self.concepts:
                    self.relations.append({
                        'source': source_id,
                        'target': target_id,
                        'relation': relation_type
                    })
                    
                    # Add edge to graph
                    self.graph.add_edge(source_id, target_id, relation=relation_type)
            
            print(f"  [SUCCESS] Downloaded {len(self.relations)} REAL relationships!")
            return True
            
        except Exception as e:
            print(f"  [ERROR] Failed to download relations: {e}")
            return False
    
    def _extract_keywords(self, text: str):
        """Extract keywords from text"""
        import re
        words = re.sub(r'[^\w\s]', ' ', text.lower()).split()
        keywords = {w for w in words if len(w) > 2 and w not in ['the', 'and', 'for', 'are', 'with']}
        return keywords
    
    def save_real_data(self):
        """Save the REAL downloaded data"""
        print(f"\nSaving REAL CSE-KG 2.0 data...")
        
        # Save concepts
        concepts_file = self.output_dir / "concepts.json"
        with open(concepts_file, 'w', encoding='utf-8') as f:
            json.dump(self.concepts, f, indent=2, ensure_ascii=False)
        print(f"  Saved {len(self.concepts)} concepts to {concepts_file}")
        
        # Save relations
        relations_file = self.output_dir / "relations.json"
        with open(relations_file, 'w', encoding='utf-8') as f:
            json.dump(self.relations, f, indent=2, ensure_ascii=False)
        print(f"  Saved {len(self.relations)} relations to {relations_file}")
        
        # Save graph
        graph_file = self.output_dir / "graph.pkl"
        with open(graph_file, 'wb') as f:
            pickle.dump(self.graph, f)
        print(f"  Saved graph ({len(self.graph.nodes())} nodes, {len(self.graph.edges())} edges) to {graph_file}")
        
        # Save keyword index
        keyword_index = {
            keyword: list(concept_ids) 
            for keyword, concept_ids in self.concept_keywords.items()
        }
        keyword_file = self.output_dir / "keyword_index.json"
        with open(keyword_file, 'w', encoding='utf-8') as f:
            json.dump(keyword_index, f, indent=2, ensure_ascii=False)
        print(f"  Saved {len(keyword_index)} keyword mappings to {keyword_file}")
        
        # Save summary
        summary = {
            'source': 'REAL CSE-KG 2.0 SPARQL Endpoint',
            'endpoint': self.endpoint,
            'download_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'num_concepts': len(self.concepts),
            'num_relations': len(self.relations),
            'num_nodes': len(self.graph.nodes()),
            'num_edges': len(self.graph.edges()),
            'num_keywords': len(keyword_index)
        }
        summary_file = self.output_dir / "summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"  Saved summary to {summary_file}")
        
        print(f"\n{'='*80}")
        print("REAL CSE-KG 2.0 DATA DOWNLOADED SUCCESSFULLY!")
        print(f"{'='*80}")
        print(f"Location: {self.output_dir.absolute()}")
        print(f"Concepts: {len(self.concepts)}")
        print(f"Relations: {len(self.relations)}")
        print(f"Graph: {len(self.graph.nodes())} nodes, {len(self.graph.edges())} edges")
    
    def download_all(self, concept_limit=500, relation_limit=1000):
        """Download everything"""
        print("="*80)
        print("DOWNLOADING REAL CSE-KG 2.0 DATA FROM ONLINE")
        print("="*80)
        
        # Download concepts
        if self.download_real_concepts(limit=concept_limit):
            # Download relations
            self.download_real_relations(limit=relation_limit)
            
            # Save everything
            self.save_real_data()
            
            return True
        else:
            print("\n[FAILED] Could not download real data from SPARQL endpoint")
            return False


if __name__ == "__main__":
    downloader = RealCSEKGDownloader()
    downloader.download_all(concept_limit=500, relation_limit=1000)

