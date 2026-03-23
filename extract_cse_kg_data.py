"""
Extract and display data from CSE-KG 2.0
Queries the knowledge graph and shows what concepts, relationships, and data are available
"""

import sys
import yaml
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from src.knowledge_graph.cse_kg_client import CSEKGClient
    from src.knowledge_graph.query_engine import ConceptRetriever, QueryEngine
    print("[OK] Successfully imported CSE-KG modules")
except ImportError as e:
    print(f"[WARNING] Import error: {e}")
    print("   Trying to install missing dependencies...")
    print("   Please install: pip install SPARQLWrapper rdflib")
    print("\n   Attempting to show CSE-KG structure without live queries...")
    show_cse_kg_structure()
    sys.exit(0)
    sys.exit(1)


def extract_concepts_from_text():
    """Extract concepts from sample text"""
    print("\n" + "="*80)
    print("1. EXTRACTING CONCEPTS FROM TEXT")
    print("="*80)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize client
    try:
        client = CSEKGClient(config)
        print("✓ CSE-KG Client initialized")
    except Exception as e:
        print(f"⚠ Error initializing client: {e}")
        print("   This might be due to network issues or SPARQL endpoint being down")
        return
    
    # Sample texts
    sample_texts = [
        "I'm struggling with recursion and base cases",
        "How do I implement a linked list in Python?",
        "What is object-oriented programming?",
        "I need help with sorting algorithms",
        "How does dynamic programming work?"
    ]
    
    for text in sample_texts:
        print(f"\n📝 Text: '{text}'")
        try:
            concepts = client.extract_concepts(text)
            if concepts:
                print(f"   ✓ Found {len(concepts)} concepts: {concepts}")
            else:
                print("   ⚠ No concepts found")
        except Exception as e:
            print(f"   ❌ Error: {e}")


def query_concept_info():
    """Query information about specific concepts"""
    print("\n" + "="*80)
    print("2. QUERYING CONCEPT INFORMATION")
    print("="*80)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    try:
        client = CSEKGClient(config)
    except Exception as e:
        print(f"⚠ Error initializing client: {e}")
        return
    
    # Test concepts
    test_concepts = [
        "recursion",
        "object_oriented_programming",
        "linked_list",
        "sorting",
        "dynamic_programming"
    ]
    
    for concept in test_concepts:
        print(f"\n🔍 Concept: '{concept}'")
        try:
            info = client.get_concept_info(concept)
            if info:
                print(f"   ✓ Found concept info:")
                print(f"      URI: {info.get('uri', 'N/A')}")
                print(f"      Labels: {info.get('labels', [])[:3]}")
                print(f"      Descriptions: {info.get('descriptions', [])[:1]}")
            else:
                print("   ⚠ Concept not found in CSE-KG")
        except Exception as e:
            print(f"   ❌ Error: {e}")


def get_prerequisites():
    """Get prerequisites for concepts"""
    print("\n" + "="*80)
    print("3. GETTING PREREQUISITES")
    print("="*80)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    try:
        client = CSEKGClient(config)
    except Exception as e:
        print(f"⚠ Error initializing client: {e}")
        return
    
    test_concepts = ["recursion", "linked_list", "sorting"]
    
    for concept in test_concepts:
        print(f"\n📚 Concept: '{concept}'")
        try:
            prereqs = client.get_prerequisites(concept)
            if prereqs:
                print(f"   ✓ Prerequisites: {prereqs[:5]}")
            else:
                print("   ⚠ No prerequisites found")
        except Exception as e:
            print(f"   ❌ Error: {e}")


def get_related_concepts():
    """Get related concepts"""
    print("\n" + "="*80)
    print("4. GETTING RELATED CONCEPTS")
    print("="*80)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    try:
        client = CSEKGClient(config)
    except Exception as e:
        print(f"⚠ Error initializing client: {e}")
        return
    
    test_concepts = ["recursion", "linked_list"]
    
    for concept in test_concepts:
        print(f"\n🔗 Concept: '{concept}'")
        try:
            related = client.get_related_concepts(concept, max_distance=1)
            if related:
                print(f"   ✓ Found {len(related)} related concepts:")
                for rel_concept, relation, distance in related[:5]:
                    print(f"      - {rel_concept} (via {relation})")
            else:
                print("   ⚠ No related concepts found")
        except Exception as e:
            print(f"   ❌ Error: {e}")


def test_concept_retriever():
    """Test ConceptRetriever with code samples"""
    print("\n" + "="*80)
    print("5. TESTING CONCEPT RETRIEVER WITH CODE")
    print("="*80)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    try:
        client = CSEKGClient(config)
        retriever = ConceptRetriever(client)
        print("✓ ConceptRetriever initialized")
    except Exception as e:
        print(f"⚠ Error initializing: {e}")
        return
    
    # Sample code snippets
    code_samples = [
        {
            "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
            "error": None
        },
        {
            "code": "class Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None",
            "error": None
        },
        {
            "code": "def quick_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr)//2]",
            "error": "RecursionError: maximum recursion depth exceeded"
        }
    ]
    
    for i, sample in enumerate(code_samples, 1):
        print(f"\n💻 Code Sample {i}:")
        print(f"   Code: {sample['code'][:50]}...")
        if sample['error']:
            print(f"   Error: {sample['error']}")
        
        try:
            concepts = retriever.retrieve_from_code(
                sample['code'],
                sample['error'],
                top_k=5
            )
            if concepts:
                print(f"   ✓ Extracted concepts: {concepts}")
            else:
                print("   ⚠ No concepts extracted")
        except Exception as e:
            print(f"   ❌ Error: {e}")


def test_query_engine():
    """Test QueryEngine for complex queries"""
    print("\n" + "="*80)
    print("6. TESTING QUERY ENGINE")
    print("="*80)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    try:
        client = CSEKGClient(config)
        query_engine = QueryEngine(client)
        print("✓ QueryEngine initialized")
    except Exception as e:
        print(f"⚠ Error initializing: {e}")
        return
    
    # Test queries
    test_queries = [
        "student struggling with recursion",
        "how to learn linked lists",
        "what are the prerequisites for sorting algorithms"
    ]
    
    for query in test_queries:
        print(f"\n❓ Query: '{query}'")
        try:
            results = query_engine.find_concept_context("recursion", context_type='learning')
            if results:
                print(f"   ✓ Found context:")
                print(f"      Prerequisites: {results.get('prerequisites', [])[:3]}")
                print(f"      Related: {len(results.get('related_concepts', []))} concepts")
            else:
                print("   ⚠ No results")
        except Exception as e:
            print(f"   ❌ Error: {e}")


def show_cse_kg_structure():
    """Show CSE-KG 2.0 structure without live queries"""
    print("\n" + "="*80)
    print("CSE-KG 2.0 STRUCTURE (from config)")
    print("="*80)
    
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    cse_kg_config = config.get('cse_kg', {})
    
    print(f"\nSPARQL Endpoint: {cse_kg_config.get('sparql_endpoint', 'N/A')}")
    print(f"Namespace: {cse_kg_config.get('namespace', 'N/A')}")
    print(f"Cache Directory: {cse_kg_config.get('cache_dir', 'N/A')}")
    print(f"Local Cache: {cse_kg_config.get('local_cache', False)}")
    
    print(f"\nEntity Types:")
    for entity_type in cse_kg_config.get('entity_types', []):
        print(f"  - {entity_type}")
    
    print(f"\nRelation Types:")
    for relation_type in cse_kg_config.get('relation_types', []):
        print(f"  - {relation_type}")
    
    print("\n" + "="*80)
    print("To extract actual data, install dependencies:")
    print("  pip install SPARQLWrapper rdflib")
    print("Then run this script again to query the live SPARQL endpoint.")
    print("="*80)


def check_cache():
    """Check what's in the cache"""
    print("\n" + "="*80)
    print("7. CHECKING CACHE")
    print("="*80)
    
    cache_dir = Path('data/cse_kg_cache')
    if cache_dir.exists():
        cache_files = list(cache_dir.glob('*.pkl'))
        print(f"✓ Cache directory exists: {cache_dir}")
        print(f"   Found {len(cache_files)} cached queries")
        if cache_files:
            print(f"   Sample files: {[f.name for f in cache_files[:5]]}")
    else:
        print(f"⚠ Cache directory does not exist: {cache_dir}")
        print("   Will be created on first query")


def main():
    """Main execution"""
    print("="*80)
    print("CSE-KG 2.0 DATA EXTRACTION")
    print("="*80)
    print("\nThis script will query CSE-KG 2.0 and extract sample data.")
    print("Note: Requires internet connection to access SPARQL endpoint.")
    print()
    
    # Check cache first
    check_cache()
    
    # Run extraction tests
    try:
        extract_concepts_from_text()
        query_concept_info()
        get_prerequisites()
        get_related_concepts()
        test_concept_retriever()
        test_query_engine()
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*80)
    print("EXTRACTION COMPLETE")
    print("="*80)
    print("\nNote: If queries failed, it might be due to:")
    print("  1. Network connectivity issues")
    print("  2. SPARQL endpoint being down")
    print("  3. Missing dependencies (SPARQLWrapper, rdflib)")
    print("  4. Concept names not matching CSE-KG 2.0 naming conventions")


if __name__ == "__main__":
    main()

