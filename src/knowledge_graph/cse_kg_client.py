"""
CSE-KG 2.0 Client for querying the Computer Science Knowledge Graph
Provides access to concepts, methods, tasks, materials, and their relationships
"""

import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Namespace, URIRef, Literal
from typing import Dict, List, Set, Optional, Tuple
import pickle
import os
from pathlib import Path
import hashlib
import json

# Try to import local client as fallback
try:
    from .local_cse_kg_client import LocalCSEKGClient
    LOCAL_CLIENT_AVAILABLE = True
except ImportError:
    LOCAL_CLIENT_AVAILABLE = False


class CSEKGClient:
    """
    Client for querying CSE-KG 2.0 (Computer Science Knowledge Graph)
    
    Provides access to:
    - Concepts (cskg:object_oriented_programming, cskg:recursion, etc.)
    - Methods (cskg:random_forest, cskg:deep_learning, etc.)
    - Tasks (cskg:sentiment_analysis, cskg:tree_traversal, etc.)
    - Materials (datasets, papers, etc.)
    - Relationships (requiresKnowledge, usesMethod, solvesTask, etc.)
    """
    
    def __init__(self, config: Dict):
        """
        Args:
            config: Configuration dictionary with CSE-KG settings
        """
        self.config = config
        
        # SPARQL endpoint
        self.endpoint = config['cse_kg']['sparql_endpoint']
        self.sparql = SPARQLWrapper(self.endpoint)
        self.sparql.setReturnFormat(JSON)
        
        # Namespace
        self.cskg = Namespace(config['cse_kg']['namespace'])
        
        # Cache settings
        self.use_cache = config['cse_kg']['local_cache']
        self.cache_dir = Path(config['cse_kg']['cache_dir'])
        if self.use_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Entity and relation types
        self.entity_types = config['cse_kg']['entity_types']
        self.relation_types = config['cse_kg']['relation_types']
        
        # Local cache for frequent queries
        self.concept_cache = {}
        self.relation_cache = {}
        
        # Initialize local client (PREFERRED - use local graph instead of SPARQL)
        self.local_client = None
        self.use_local_only = False  # Flag to use local only
        
        if LOCAL_CLIENT_AVAILABLE:
            try:
                self.local_client = LocalCSEKGClient(config)
                # Check if local graph has data
                if self.local_client.graph and len(self.local_client.graph.nodes()) > 0:
                    self.use_local_only = True
                    print("[CSE-KG] Using LOCAL graph (no SPARQL queries)")
                else:
                    print("[CSE-KG] Local graph empty, will try SPARQL with local fallback")
            except Exception as e:
                print(f"[WARN] Could not initialize local CSE-KG client: {e}")
        
    def _get_cache_path(self, query: str) -> Path:
        """Generate cache file path for a query"""
        query_hash = hashlib.md5(query.encode()).hexdigest()
        return self.cache_dir / f"{query_hash}.pkl"
    
    def _query_sparql(self, query: str, use_cache: bool = True) -> List[Dict]:
        """
        Execute SPARQL query with caching
        Uses LOCAL graph if available, otherwise tries SPARQL with local fallback
        
        Args:
            query: SPARQL query string
            use_cache: Whether to use cache
            
        Returns:
            List of result bindings
        """
        # USE LOCAL GRAPH FIRST if available (no SPARQL queries)
        if self.use_local_only and self.local_client:
            return self._fallback_to_local(query)
        
        # Check cache
        if use_cache and self.use_cache:
            cache_path = self._get_cache_path(query)
            if cache_path.exists():
                with open(cache_path, 'rb') as f:
                    return pickle.load(f)
        
        # Try SPARQL only if local graph not available
        if not self.use_local_only:
            try:
                self.sparql.setQuery(query)
                results = self.sparql.query().convert()
                bindings = results['results']['bindings']
                
                # Cache results
                if use_cache and self.use_cache:
                    cache_path = self._get_cache_path(query)
                    with open(cache_path, 'wb') as f:
                        pickle.dump(bindings, f)
                
                return bindings
            
            except Exception as e:
                # Fallback to local graph
                if self.local_client:
                    print(f"[CSE-KG] SPARQL query error: {e}, using local graph")
                    return self._fallback_to_local(query)
                else:
                    print(f"[CSE-KG] SPARQL query error: {e}, no local fallback available")
                    return []
        else:
            # Use local graph directly
            return self._fallback_to_local(query)
    
    def _fallback_to_local(self, query: str) -> List[Dict]:
        """Fallback to local graph when SPARQL fails"""
        if not self.local_client:
            return []
        
        # Simple query parsing - extract concept names from query
        # This is a basic fallback, not full SPARQL parsing
        query_lower = query.lower()
        
        # Try to extract concept from common query patterns
        if 'select' in query_lower and 'where' in query_lower:
            # Extract concept URI from query
            import re
            uri_pattern = r'<([^>]+)>'
            uris = re.findall(uri_pattern, query)
            
            if uris:
                concept_uri = uris[0]
                concept_info = self.local_client.get_concept_info(concept_uri)
                if concept_info:
                    # Convert to SPARQL result format
                    results = []
                    for key, value in concept_info.items():
                        if isinstance(value, str):
                            results.append({
                                'property': {'value': key},
                                'value': {'value': value}
                            })
                    return results
        
        return []
    
    def get_concept_info(self, concept_uri: str) -> Optional[Dict]:
        """
        Get concept information - uses LOCAL graph if available
        """
        # Use local client if available (preferred)
        if self.use_local_only and self.local_client:
            return self.local_client.get_concept_info(concept_uri)
        """
        Get detailed information about a concept
        
        Args:
            concept_uri: URI or local name (e.g., "cskg:recursion" or "recursion")
            
        Returns:
            Dictionary with concept properties
        """
        # Normalize URI
        if not concept_uri.startswith('http'):
            concept_uri = f"{self.cskg}{concept_uri.replace('cskg:', '')}"
        
        # Check cache
        if concept_uri in self.concept_cache:
            return self.concept_cache[concept_uri]
        
        # Use local client if available (preferred - no SPARQL)
        if self.use_local_only and self.local_client:
            result = self.local_client.get_concept_info(concept_uri)
            if result:
                self.concept_cache[concept_uri] = result
                return result
        
        # Try local client first (even if not use_local_only)
        if self.local_client:
            result = self.local_client.get_concept_info(concept_uri)
            if result:
                self.concept_cache[concept_uri] = result
                return result
        
        query = f"""
        PREFIX cskg: <{self.cskg}>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        
        SELECT DISTINCT ?property ?value WHERE {{
            <{concept_uri}> ?property ?value .
        }}
        """
        
        results = self._query_sparql(query)
        
        if not results:
            # Final fallback to local
            if self.local_client:
                return self.local_client.get_concept_info(concept_uri)
            return None
        
        # Parse results into dictionary
        concept_info = {
            'uri': concept_uri,
            'labels': [],
            'descriptions': [],
            'types': [],
            'broader': [],
            'narrower': [],
            'related': []
        }
        
        for result in results:
            prop = result['property']['value']
            val = result['value']['value']
            
            if 'label' in prop:
                concept_info['labels'].append(val)
            elif 'description' in prop or 'definition' in prop:
                concept_info['descriptions'].append(val)
            elif 'type' in prop:
                concept_info['types'].append(val)
            elif 'broader' in prop:
                concept_info['broader'].append(val)
            elif 'narrower' in prop:
                concept_info['narrower'].append(val)
            elif 'related' in prop:
                concept_info['related'].append(val)
        
        # Cache
        self.concept_cache[concept_uri] = concept_info
        
        return concept_info
    
    def get_prerequisites(self, concept: str) -> List[str]:
        """
        Get prerequisites - uses LOCAL graph if available
        
        Args:
            concept: Concept name or URI
            
        Returns:
            List of prerequisite concept URIs
        """
        # Use local client if available (preferred - no SPARQL)
        if self.use_local_only and self.local_client:
            return self.local_client.get_prerequisites(concept)
        
        # Try local client first (even if not use_local_only)
        if self.local_client:
            result = self.local_client.get_prerequisites(concept)
            if result:
                return result
        
        concept_uri = self._normalize_uri(concept)
        
        query = f"""
        PREFIX cskg: <{self.cskg}>
        
        SELECT DISTINCT ?prereq WHERE {{
            <{concept_uri}> cskg:requiresKnowledge ?prereq .
        }}
        """
        
        results = self._query_sparql(query)
        if results:
            return [r['prereq']['value'] for r in results]
        
        # Fallback to local
        if self.local_client:
            return self.local_client.get_prerequisites(concept)
        return []
    
    def get_related_concepts(self, concept: str, 
                           relation_type: Optional[str] = None,
                           max_distance: int = 1) -> List[Tuple[str, str, int]]:
        """
        Get concepts related to the given concept - uses LOCAL graph if available
        
        Args:
            concept: Source concept
            relation_type: Specific relation type (optional)
            max_distance: Maximum distance in graph (1 = direct neighbors)
            
        Returns:
            List of (concept_uri, relation_type, distance) tuples
        """
        # Use local client if available (preferred - no SPARQL)
        if self.use_local_only and self.local_client:
            return self.local_client.get_related_concepts(concept, relation_type, max_distance)
        
        # Try local client first (even if not use_local_only)
        if self.local_client:
            result = self.local_client.get_related_concepts(concept, relation_type, max_distance)
            if result:
                return result
        
        concept_uri = self._normalize_uri(concept)
        
        if max_distance == 1:
            # Direct neighbors only
            if relation_type:
                query = f"""
                PREFIX cskg: <{self.cskg}>
                SELECT DISTINCT ?related WHERE {{
                    {{ <{concept_uri}> cskg:{relation_type} ?related . }}
                    UNION
                    {{ ?related cskg:{relation_type} <{concept_uri}> . }}
                }}
                LIMIT 100
                """
            else:
                query = f"""
                PREFIX cskg: <{self.cskg}>
                SELECT DISTINCT ?related ?relation WHERE {{
                    {{ <{concept_uri}> ?relation ?related . }}
                    UNION
                    {{ ?related ?relation <{concept_uri}> . }}
                    FILTER(STRSTARTS(STR(?relation), STR(cskg:)))
                }}
                LIMIT 100
                """
            
            results = self._query_sparql(query)
            
            if relation_type:
                return [(r['related']['value'], relation_type, 1) for r in results]
            else:
                return [
                    (r['related']['value'], 
                     r['relation']['value'].split('/')[-1], 
                     1) 
                    for r in results if 'related' in r
                ]
        
        else:
            # Multi-hop traversal (more expensive)
            # Simplified implementation
            visited = set()
            current_level = [concept_uri]
            related = []
            
            for distance in range(1, max_distance + 1):
                next_level = []
                for c in current_level:
                    neighbors = self.get_related_concepts(c, relation_type, max_distance=1)
                    for neighbor, rel, _ in neighbors:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            next_level.append(neighbor)
                            related.append((neighbor, rel, distance))
                
                current_level = next_level
                if not current_level:
                    break
            
            return related
    
    def get_methods_for_task(self, task: str) -> List[Dict]:
        """
        Get methods that can solve a given task
        
        Args:
            task: Task name or URI (e.g., "sentiment_analysis")
            
        Returns:
            List of method dictionaries with metadata
        """
        task_uri = self._normalize_uri(task)
        
        query = f"""
        PREFIX cskg: <{self.cskg}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?method ?label ?description WHERE {{
            ?method cskg:solvesTask <{task_uri}> .
            OPTIONAL {{ ?method rdfs:label ?label . }}
            OPTIONAL {{ ?method rdfs:comment ?description . }}
        }}
        LIMIT 50
        """
        
        results = self._query_sparql(query)
        
        methods = []
        for r in results:
            methods.append({
                'uri': r['method']['value'],
                'label': r.get('label', {}).get('value', ''),
                'description': r.get('description', {}).get('value', '')
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
        concept_uri = self._normalize_uri(concept)
        
        # CSE-KG might not have explicit misconceptions, 
        # so we look for related concepts with specific patterns
        query = f"""
        PREFIX cskg: <{self.cskg}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?related ?label ?type WHERE {{
            {{ <{concept_uri}> cskg:relatedTo ?related . }}
            UNION
            {{ ?related cskg:relatedTo <{concept_uri}> . }}
            ?related rdfs:label ?label .
            ?related rdf:type ?type .
        }}
        LIMIT 20
        """
        
        results = self._query_sparql(query)
        
        # Filter for potential misconceptions
        misconceptions = []
        for r in results:
            label = r.get('label', {}).get('value', '').lower()
            # Look for patterns that indicate misconceptions
            if any(keyword in label for keyword in ['error', 'mistake', 'confusion', 'misunderstanding']):
                misconceptions.append({
                    'uri': r['related']['value'],
                    'description': label,
                    'type': r.get('type', {}).get('value', '')
                })
        
        return misconceptions
    
    def extract_concepts(self, text: str) -> List[str]:
        """
        Extract CS concepts from natural language text
        Uses keyword matching against CSE-KG entities
        
        Args:
            text: Natural language description
            
        Returns:
            List of concept names
        """
        text_lower = text.lower()
        
        # Query for concepts with labels matching text
        query = f"""
        PREFIX cskg: <{self.cskg}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?concept ?label WHERE {{
            ?concept rdf:type ?type .
            ?concept rdfs:label ?label .
            FILTER(STRSTARTS(STR(?type), STR(cskg:)))
        }}
        LIMIT 1000
        """
        
        results = self._query_sparql(query)
        
        # Find matches
        concepts = []
        for r in results:
            label = r.get('label', {}).get('value', '').lower()
            if label and label in text_lower:
                concept_name = r['concept']['value'].split('/')[-1]
                concepts.append(concept_name)
        
        return list(set(concepts))
    
    def get_concept_hierarchy(self, concept: str, levels: int = 2) -> Dict:
        """
        Get hierarchical structure around a concept
        
        Args:
            concept: Root concept
            levels: Number of levels up and down
            
        Returns:
            Dictionary representing hierarchy
        """
        concept_uri = self._normalize_uri(concept)
        
        hierarchy = {
            'concept': concept_uri,
            'parents': [],
            'children': [],
            'siblings': []
        }
        
        # Get broader concepts (parents)
        query = f"""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT DISTINCT ?parent WHERE {{
            <{concept_uri}> skos:broader ?parent .
        }}
        """
        results = self._query_sparql(query)
        hierarchy['parents'] = [r['parent']['value'] for r in results]
        
        # Get narrower concepts (children)
        query = f"""
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        SELECT DISTINCT ?child WHERE {{
            <{concept_uri}> skos:narrower ?child .
        }}
        """
        results = self._query_sparql(query)
        hierarchy['children'] = [r['child']['value'] for r in results]
        
        # Get siblings (same parent)
        if hierarchy['parents']:
            parent = hierarchy['parents'][0]
            query = f"""
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
            SELECT DISTINCT ?sibling WHERE {{
                <{parent}> skos:narrower ?sibling .
                FILTER(?sibling != <{concept_uri}>)
            }}
            """
            results = self._query_sparql(query)
            hierarchy['siblings'] = [r['sibling']['value'] for r in results]
        
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
        # Try local client first (much faster)
        if self.local_client:
            result = self.local_client.search_by_keywords(keywords, entity_type, limit)
            if result:
                return result
        
        # Build filter for keywords
        keyword_filters = " || ".join([
            f'CONTAINS(LCASE(?label), "{kw.lower()}")'
            for kw in keywords
        ])
        
        type_filter = ""
        if entity_type:
            type_filter = f"FILTER(?type = cskg:{entity_type})"
        
        query = f"""
        PREFIX cskg: <{self.cskg}>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        
        SELECT DISTINCT ?entity ?label ?type WHERE {{
            ?entity rdfs:label ?label .
            ?entity rdf:type ?type .
            {type_filter}
            FILTER({keyword_filters})
        }}
        LIMIT {limit}
        """
        
        results = self._query_sparql(query)
        
        entities = []
        for r in results:
            entities.append({
                'uri': r['entity']['value'],
                'label': r.get('label', {}).get('value', ''),
                'type': r.get('type', {}).get('value', '').split('/')[-1]
            })
        
        # Fallback to local if SPARQL returned nothing
        if not entities and self.local_client:
            return self.local_client.search_by_keywords(keywords, entity_type, limit)
        
        return entities
    
    def _normalize_uri(self, concept: str) -> str:
        """Convert concept name to full URI"""
        if concept.startswith('http'):
            return concept
        else:
            return f"{self.cskg}{concept.replace('cskg:', '')}"
    
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
        if include_relations is None:
            include_relations = self.relation_types
        
        nodes = []
        edges = []
        
        # Add nodes
        for concept in concepts:
            concept_uri = self._normalize_uri(concept)
            concept_info = self.get_concept_info(concept_uri)
            if concept_info:
                nodes.append(concept_info)
        
        # Add edges between concepts
        for i, source in enumerate(concepts):
            source_uri = self._normalize_uri(source)
            for j, target in enumerate(concepts):
                if i >= j:
                    continue
                target_uri = self._normalize_uri(target)
                
                # Check for relationships
                for relation in include_relations:
                    query = f"""
                    PREFIX cskg: <{self.cskg}>
                    ASK {{
                        {{ <{source_uri}> cskg:{relation} <{target_uri}> . }}
                        UNION
                        {{ <{target_uri}> cskg:{relation} <{source_uri}> . }}
                    }}
                    """
                    
                    results = self._query_sparql(query, use_cache=True)
                    # ASK queries return boolean
                    if results:
                        edges.append({
                            'source': source_uri,
                            'target': target_uri,
                            'relation': relation
                        })
        
        return {
            'nodes': nodes,
            'edges': edges
        }






