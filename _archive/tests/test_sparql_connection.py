"""
Test SPARQL connection to CSE-KG 2.0 endpoint
"""

import sys
import yaml
from pathlib import Path

try:
    from SPARQLWrapper import SPARQLWrapper, JSON
    SPARQL_AVAILABLE = True
except ImportError:
    print("SPARQLWrapper not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "SPARQLWrapper", "-q"])
    from SPARQLWrapper import SPARQLWrapper, JSON
    SPARQL_AVAILABLE = True

import requests
import time


def test_endpoint_connectivity():
    """Test if endpoint is accessible"""
    print("Testing CSE-KG 2.0 endpoint connectivity...")
    
    endpoint = "http://cse.ckcest.cn/cskg/sparql"
    
    # Test 1: Simple HTTP request
    try:
        print(f"   Testing HTTP connection to {endpoint}...")
        response = requests.get(endpoint, timeout=10)
        print(f"   [OK] HTTP Status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"   [ERROR] Cannot connect: {e}")
        return False


def test_simple_sparql_query():
    """Test a simple SPARQL query"""
    print("\nTesting simple SPARQL query...")
    
    endpoint = "http://cse.ckcest.cn/cskg/sparql"
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    
    # Very simple query to test connectivity
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    SELECT ?s ?p ?o WHERE {
        ?s ?p ?o .
    }
    LIMIT 5
    """
    
    try:
        print("   Executing query...")
        sparql.setQuery(query)
        results = sparql.query().convert()
        bindings = results['results']['bindings']
        print(f"   [OK] Query successful! Got {len(bindings)} results")
        if bindings:
            print(f"   Sample result: {bindings[0]}")
        return True
    except Exception as e:
        print(f"   [ERROR] Query failed: {e}")
        return False


def test_concept_query():
    """Test querying for a specific concept"""
    print("\nTesting concept query (recursion)...")
    
    endpoint = "http://cse.ckcest.cn/cskg/sparql"
    namespace = "http://cse.ckcest.cn/cskg/"
    
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    
    # Query for recursion concept
    query = f"""
    PREFIX cskg: <{namespace}>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?concept ?label WHERE {{
        ?concept rdfs:label ?label .
        FILTER(CONTAINS(LCASE(?label), "recursion"))
    }}
    LIMIT 10
    """
    
    try:
        print("   Executing query...")
        sparql.setQuery(query)
        results = sparql.query().convert()
        bindings = results['results']['bindings']
        print(f"   [OK] Found {len(bindings)} concepts matching 'recursion'")
        for i, result in enumerate(bindings[:5], 1):
            concept = result.get('concept', {}).get('value', 'N/A')
            label = result.get('label', {}).get('value', 'N/A')
            print(f"   {i}. {label} - {concept}")
        return True, bindings
    except Exception as e:
        print(f"   [ERROR] Query failed: {e}")
        return False, []


def test_prerequisite_query():
    """Test querying prerequisites"""
    print("\nTesting prerequisite query...")
    
    endpoint = "http://cse.ckcest.cn/cskg/sparql"
    namespace = "http://cse.ckcest.cn/cskg/"
    
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)
    
    # Try to find a concept and its prerequisites
    query = f"""
    PREFIX cskg: <{namespace}>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT DISTINCT ?concept ?label ?prereq ?prereqLabel WHERE {{
        ?concept rdfs:label ?label .
        ?concept cskg:requiresKnowledge ?prereq .
        ?prereq rdfs:label ?prereqLabel .
        FILTER(CONTAINS(LCASE(?label), "recursion"))
    }}
    LIMIT 10
    """
    
    try:
        print("   Executing query...")
        sparql.setQuery(query)
        results = sparql.query().convert()
        bindings = results['results']['bindings']
        print(f"   [OK] Found {len(bindings)} prerequisite relationships")
        for i, result in enumerate(bindings[:5], 1):
            concept = result.get('label', {}).get('value', 'N/A')
            prereq = result.get('prereqLabel', {}).get('value', 'N/A')
            print(f"   {i}. {concept} requires {prereq}")
        return True, bindings
    except Exception as e:
        print(f"   [ERROR] Query failed: {e}")
        return False, []


def main():
    """Test SPARQL connectivity and queries"""
    print("="*80)
    print("CSE-KG 2.0 SPARQL CONNECTION TEST")
    print("="*80)
    
    # Test 1: HTTP connectivity
    if not test_endpoint_connectivity():
        print("\n[WARNING] Endpoint not accessible. This might be a network issue.")
        print("The system will use fallback keyword matching instead.")
        return
    
    # Test 2: Simple SPARQL query
    if not test_simple_sparql_query():
        print("\n[WARNING] SPARQL queries are not working.")
        return
    
    # Test 3: Concept query
    success, concepts = test_concept_query()
    
    # Test 4: Prerequisite query
    success2, prereqs = test_prerequisite_query()
    
    if success or success2:
        print("\n" + "="*80)
        print("[OK] SPARQL queries are working!")
        print("="*80)
        print("\nThe CSE-KG 2.0 endpoint is accessible and queries are successful.")
    else:
        print("\n" + "="*80)
        print("[WARNING] Some queries failed, but basic connectivity works.")
        print("="*80)


if __name__ == "__main__":
    main()















