"""
Script to initialize CSE-KG connection and cache
"""

import yaml
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))

from src.knowledge_graph import CSEKGClient


def init_cse_kg():
    """Initialize CSE-KG client and warm up cache"""
    
    print("Initializing CSE-KG 2.0 client...")
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Create client
    client = CSEKGClient(config)
    
    # Test connection
    print("Testing SPARQL endpoint connection...")
    
    # Query for common CS concepts to warm cache
    common_concepts = [
        'recursion', 'iteration', 'array', 'list', 'tree', 'graph',
        'sorting', 'searching', 'dynamic_programming', 'object_oriented_programming'
    ]
    
    print(f"Caching {len(common_concepts)} common concepts...")
    
    for concept in common_concepts:
        try:
            info = client.get_concept_info(concept)
            if info:
                print(f"  ✓ {concept}")
            else:
                print(f"  ✗ {concept} (not found)")
        except Exception as e:
            print(f"  ✗ {concept} (error: {e})")
    
    print("\nCSE-KG initialized successfully!")
    print(f"Cache directory: {client.cache_dir}")


if __name__ == "__main__":
    init_cse_kg()

















