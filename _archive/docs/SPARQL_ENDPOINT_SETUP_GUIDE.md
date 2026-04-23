# SPARQL Endpoint Setup Guide

## Overview

The CSE-KG client uses a SPARQL endpoint to query the Computer Science Knowledge Graph for:
- **Prerequisites** (what concepts are needed before learning a concept)
- **Related concepts** (concepts connected to the current one)
- **Concept definitions** and metadata

## Current Configuration

The system is configured to use the public CSE-KG 2.0 SPARQL endpoint:

```yaml
cse_kg:
  sparql_endpoint: http://w3id.org/cskg/sparql
  local_cache: true
  cache_dir: data/cse_kg_cache
  namespace: http://cse.ckcest.cn/cskg/
```

## Option 1: Test Current Endpoint

First, let's test if the public endpoint is accessible:

```bash
python scripts/test_sparql_endpoint.py
```

This will:
1. Test connection to `http://w3id.org/cskg/sparql`
2. Query for prerequisites of "recursion"
3. Show what data is available

## Option 2: Use Local SPARQL Endpoint (Recommended)

If the public endpoint is unavailable or doesn't have prerequisite data, set up a local SPARQL endpoint.

### Step 1: Install Apache Jena Fuseki

**Windows:**
```bash
# Download from: https://jena.apache.org/download/index.cgi
# Extract to C:\apache-jena-fuseki
```

**Linux/Mac:**
```bash
# Download and extract
wget https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-4.10.0.tar.gz
tar -xzf apache-jena-fuseki-4.10.0.tar.gz
cd apache-jena-fuseki-4.10.0
```

### Step 2: Create CSE-KG Dataset

1. **Start Fuseki:**
```bash
# Windows
cd C:\apache-jena-fuseki
fuseki-server.bat

# Linux/Mac
./fuseki-server
```

2. **Access Web UI:** Open `http://localhost:3030`

3. **Create New Dataset:**
   - Click "Add Dataset"
   - Name: `csekg`
   - Type: "Persistent (TDB2)"
   - Click "Create"

### Step 3: Load CSE-KG Data

You need RDF/Turtle files with CSE-KG data. If you have them:

```bash
# Using Fuseki Web UI:
# 1. Go to http://localhost:3030/csekg
# 2. Click "Upload data"
# 3. Select your .ttl or .rdf files
# 4. Click "Upload"

# Or using command line:
curl -X POST \
  -H "Content-Type: text/turtle" \
  --data-binary @csekg_data.ttl \
  http://localhost:3030/csekg/data
```

### Step 4: Update Config

Update `config.yaml`:

```yaml
cse_kg:
  sparql_endpoint: http://localhost:3030/csekg/sparql  # Local endpoint
  local_cache: true
  cache_dir: data/cse_kg_cache
  namespace: http://cse.ckcest.cn/cskg/
```

## Option 3: Enhance Local Fallback (Quick Fix)

If you can't set up a SPARQL endpoint, enhance the local fallback to include prerequisites.

### Step 1: Create Prerequisites Data File

Create `data/cse_kg_local/prerequisites.json`:

```json
{
  "recursion": {
    "prerequisites": [
      {
        "concept": "functions",
        "mastery": 0.75,
        "status": "mastered"
      },
      {
        "concept": "conditional_statements",
        "mastery": 0.65,
        "status": "partial"
      },
      {
        "concept": "base_case",
        "mastery": 0.15,
        "status": "critical_gap"
      }
    ],
    "related_concepts": [
      {
        "concept": "iteration",
        "relation": "relatedTo"
      },
      {
        "concept": "loops",
        "relation": "relatedTo"
      },
      {
        "concept": "tail_recursion",
        "relation": "relatedTo"
      }
    ]
  },
  "arrays": {
    "prerequisites": [
      {
        "concept": "variables",
        "mastery": 0.8,
        "status": "mastered"
      },
      {
        "concept": "loops",
        "mastery": 0.7,
        "status": "mastered"
      }
    ],
    "related_concepts": [
      {
        "concept": "lists",
        "relation": "relatedTo"
      },
      {
        "concept": "indexing",
        "relation": "relatedTo"
      }
    ]
  }
}
```

### Step 2: Update Local Client

The local client will automatically load this file if it exists. The system will use it as a fallback when SPARQL queries fail.

## Option 4: Use Alternative Public Endpoints

Try these alternative SPARQL endpoints:

1. **DBpedia SPARQL:**
   ```yaml
   sparql_endpoint: https://dbpedia.org/sparql
   namespace: http://dbpedia.org/resource/
   ```

2. **Wikidata SPARQL:**
   ```yaml
   sparql_endpoint: https://query.wikidata.org/sparql
   namespace: http://www.wikidata.org/entity/
   ```

   Note: You'll need to adapt the SPARQL queries for these endpoints.

## Testing the Endpoint

Create `scripts/test_sparql_endpoint.py`:

```python
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
    print(f"Connecting to: {config['cse_kg']['sparql_endpoint']}")
    client = CSEKGClient(config)
    
    # Test 1: Get concept info
    print("\n[Test 1] Getting concept info for 'recursion'...")
    try:
        info = client.get_concept_info("recursion")
        if info:
            print(f"  ✓ Found: {info.get('labels', ['N/A'])[0]}")
        else:
            print("  ✗ Not found")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Test 2: Get prerequisites
    print("\n[Test 2] Getting prerequisites for 'recursion'...")
    try:
        prereqs = client.get_prerequisites("recursion")
        if prereqs:
            print(f"  ✓ Found {len(prereqs)} prerequisites:")
            for p in prereqs[:5]:
                print(f"    - {p}")
        else:
            print("  ✗ No prerequisites found")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Test 3: Get related concepts
    print("\n[Test 3] Getting related concepts for 'recursion'...")
    try:
        related = client.get_related_concepts("recursion", max_distance=1)
        if related:
            print(f"  ✓ Found {len(related)} related concepts:")
            for r in related[:5]:
                print(f"    - {r[0]} (via {r[1]})")
        else:
            print("  ✗ No related concepts found")
    except Exception as e:
        print(f"  ✗ Error: {e}")
    
    # Test 4: Direct SPARQL query
    print("\n[Test 4] Testing direct SPARQL query...")
    try:
        query = """
        PREFIX cskg: <http://cse.ckcest.cn/cskg/>
        SELECT ?s ?p ?o WHERE {
            ?s ?p ?o
        } LIMIT 5
        """
        results = client._query_sparql(query, use_cache=False)
        if results:
            print(f"  ✓ Query successful, got {len(results)} results")
        else:
            print("  ✗ Query returned no results")
    except Exception as e:
        print(f"  ✗ Query failed: {e}")
        print("  → This means the SPARQL endpoint is not accessible")
        print("  → The system will use local fallback")

if __name__ == "__main__":
    test_endpoint()
```

Run it:
```bash
python scripts/test_sparql_endpoint.py
```

## Quick Fix: Add Prerequisites to Local Cache

If you want to quickly add prerequisites without setting up a full SPARQL endpoint, create the prerequisites file:

```bash
# Create directory
mkdir -p data/cse_kg_local

# Create prerequisites file (see Option 3 above)
# Then the local client will use it automatically
```

## Recommended Approach

**For Development:**
- Use **Option 3** (Local Fallback with JSON) - Quick and works offline

**For Production:**
- Use **Option 2** (Local Fuseki) - Full SPARQL support, scalable

**For Testing:**
- Use **Option 1** (Test Current Endpoint) - See what's available

## Troubleshooting

### "SPARQL query error" messages

This means the endpoint is not accessible. The system will automatically fall back to local data.

**Solutions:**
1. Check internet connection
2. Try a different endpoint
3. Use local fallback (Option 3)

### Empty prerequisites

If prerequisites are empty, it means:
1. The SPARQL endpoint doesn't have prerequisite relationships
2. The local cache doesn't have prerequisite data

**Solutions:**
1. Add prerequisites to `data/cse_kg_local/prerequisites.json`
2. Set up local Fuseki with prerequisite data
3. Use the enhanced local client

### Connection timeout

If queries timeout:

```yaml
cse_kg:
  timeout: 30  # seconds (add to config.yaml)
```

## Next Steps

1. **Test current endpoint:** `python scripts/test_sparql_endpoint.py`
2. **If it fails:** Use Option 3 (local JSON fallback)
3. **For production:** Set up local Fuseki (Option 2)

