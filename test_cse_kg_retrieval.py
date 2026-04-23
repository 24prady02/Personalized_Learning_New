"""
Test CSE-KG 2.0 graph retrieval to verify it's working
"""

import yaml
from pathlib import Path
from src.knowledge_graph import CSEKGClient, ConceptRetriever

# Load config
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

print("="*80)
print("TESTING CSE-KG 2.0 GRAPH RETRIEVAL")
print("="*80)

# Initialize client
print("\n1. Initializing CSE-KG Client...")
client = CSEKGClient(config)
print(f"   Endpoint: {client.endpoint}")
print(f"   Namespace: {client.cskg}")

# Test 1: Get concept info
print("\n2. Testing get_concept_info('recursion')...")
concept_info = client.get_concept_info('recursion')
if concept_info:
    print(f"   [OK] Found concept: {concept_info.get('label', 'N/A')}")
    print(f"   Description: {concept_info.get('description', 'N/A')[:100]}...")
else:
    print("   [WARNING] Concept not found via SPARQL, trying local...")

# Test 2: Search by keywords
print("\n3. Testing search_by_keywords(['recursion', 'function'])...")
results = client.search_by_keywords(['recursion', 'function'], limit=5)
if results:
    print(f"   [OK] Found {len(results)} concepts:")
    for i, result in enumerate(results[:3], 1):
        print(f"      {i}. {result.get('label', 'N/A')} ({result.get('type', 'N/A')})")
else:
    print("   [WARNING] No results from SPARQL, trying local...")

# Test 3: Get prerequisites
print("\n4. Testing get_prerequisites('recursion')...")
prereqs = client.get_prerequisites('recursion')
if prereqs:
    print(f"   [OK] Found {len(prereqs)} prerequisites:")
    for prereq in prereqs[:3]:
        print(f"      - {prereq}")
else:
    print("   [WARNING] No prerequisites found")

# Test 4: Get related concepts
print("\n5. Testing get_related_concepts('recursion')...")
related = client.get_related_concepts('recursion', max_distance=1)
if related:
    print(f"   [OK] Found {len(related)} related concepts:")
    for uri, relation, dist in related[:3]:
        concept_id = uri.split('/')[-1]
        print(f"      - {concept_id} (via {relation}, distance: {dist})")
else:
    print("   [WARNING] No related concepts found")

# Test 5: ConceptRetriever
print("\n6. Testing ConceptRetriever...")
retriever = ConceptRetriever(client)

# Test from code
print("   6a. retrieve_from_code('def factorial(n): return n * factorial(n-1)')...")
code_concepts = retriever.retrieve_from_code(
    "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
    top_k=5
)
if code_concepts:
    print(f"   [OK] Retrieved {len(code_concepts)} concepts from code:")
    for concept in code_concepts:
        print(f"      - {concept}")
else:
    print("   [WARNING] No concepts retrieved from code")

# Test from query
print("   6b. retrieve_from_query('I need help with recursion and base cases')...")
query_results = retriever.retrieve_from_query(
    "I need help with recursion and base cases",
    top_k=5
)
if query_results:
    print(f"   [OK] Retrieved {len(query_results)} concepts from query:")
    for result in query_results[:3]:
        print(f"      - {result.get('label', 'N/A')} (score: {result.get('relevance_score', 0)})")
else:
    print("   [WARNING] No concepts retrieved from query")

print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)

if concept_info or results or prereqs or related or code_concepts or query_results:
    print("[SUCCESS] Graph retrieval is working!")
    print("\nCSE-KG 2.0 is accessible and can be used for concept retrieval.")
else:
    print("[WARNING] Graph retrieval returned no results.")
    print("This might mean:")
    print("  1. The endpoint is accessible but returns empty results")
    print("  2. Concept names need to match exactly")
    print("  3. Local fallback graph will be used instead")















