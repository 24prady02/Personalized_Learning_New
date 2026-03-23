"""
Test SPARQL endpoint connection and queries
"""

import yaml
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from src.knowledge_graph.cse_kg_client import CSEKGClient

def test_endpoint():
    """Test SPARQL endpoint"""
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Create client
    print("=" * 70)
    print("SPARQL ENDPOINT TEST")
    print("=" * 70)
    print(f"\nConnecting to: {config['cse_kg']['sparql_endpoint']}")
    print(f"Namespace: {config['cse_kg']['namespace']}")
    print(f"Cache enabled: {config['cse_kg']['local_cache']}")
    
    client = CSEKGClient(config)
    
    # Test 1: Get concept info
    print("\n" + "=" * 70)
    print("[Test 1] Getting concept info for 'recursion'...")
    print("=" * 70)
    try:
        info = client.get_concept_info("recursion")
        if info:
            print(f"  [OK] Found concept:")
            print(f"    Labels: {info.get('labels', ['N/A'])}")
            print(f"    Types: {info.get('types', [])}")
            print(f"    Descriptions: {len(info.get('descriptions', []))} found")
        else:
            print("  [FAIL] Not found")
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Get prerequisites
    print("\n" + "=" * 70)
    print("[Test 2] Getting prerequisites for 'recursion'...")
    print("=" * 70)
    try:
        prereqs = client.get_prerequisites("recursion")
        if prereqs:
            print(f"  [OK] Found {len(prereqs)} prerequisites:")
            for i, p in enumerate(prereqs[:10], 1):
                print(f"    {i}. {p}")
        else:
            print("  [FAIL] No prerequisites found")
            print("  -> This is why prerequisites are empty in output")
            print("  -> Solution: Use local fallback or set up local SPARQL endpoint")
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Get related concepts
    print("\n" + "=" * 70)
    print("[Test 3] Getting related concepts for 'recursion'...")
    print("=" * 70)
    try:
        related = client.get_related_concepts("recursion", max_distance=1)
        if related:
            print(f"  [OK] Found {len(related)} related concepts:")
            for i, r in enumerate(related[:10], 1):
                concept = r[0] if isinstance(r, tuple) else r
                relation = r[1] if isinstance(r, tuple) and len(r) > 1 else "relatedTo"
                print(f"    {i}. {concept} (via {relation})")
        else:
            print("  [FAIL] No related concepts found")
    except Exception as e:
        print(f"  [ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Direct SPARQL query
    print("\n" + "=" * 70)
    print("[Test 4] Testing direct SPARQL query...")
    print("=" * 70)
    try:
        query = f"""
        PREFIX cskg: <{config['cse_kg']['namespace']}>
        SELECT ?s ?p ?o WHERE {{
            ?s ?p ?o
        }} LIMIT 5
        """
        print("  Query:")
        print(f"  {query.strip()}")
        results = client._query_sparql(query, use_cache=False)
        if results:
            print(f"  [OK] Query successful, got {len(results)} results")
            print("  Sample result:")
            if results:
                for key, value in list(results[0].items())[:3]:
                    print(f"    {key}: {value.get('value', 'N/A')}")
        else:
            print("  [FAIL] Query returned no results")
            print("  -> Endpoint might be accessible but has no data")
    except Exception as e:
        print(f"  [ERROR] Query failed: {e}")
        print("  -> This means the SPARQL endpoint is not accessible")
        print("  -> The system will use local fallback")
        import traceback
        traceback.print_exc()
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print("\nIf prerequisites are empty:")
    print("  1. Check SPARQL_ENDPOINT_SETUP_GUIDE.md")
    print("  2. Use local fallback: Create data/cse_kg_local/prerequisites.json")
    print("  3. Set up local Fuseki: See Option 2 in the guide")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_endpoint()

