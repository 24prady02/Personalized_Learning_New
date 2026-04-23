# Knowledge Graph Sources Analysis

## Overview

This document clarifies which knowledge graphs come from **online sources** vs **local files**.

---

## 📊 Graph Sources Breakdown

### 1. **CSE-KG 2.0 (Computer Science Knowledge Graph)**

**Status**: ⚠️ **ONLINE (with local fallback)**

**Primary Source**: 
- **Online SPARQL Endpoint**: `http://w3id.org/cskg/sparql`
- Queries are made **live** to the online endpoint
- Results are **cached locally** in `data/cse_kg_cache/*.pkl`

**Fallback Options**:
1. **Local Cache**: If query was made before, uses cached result
2. **Local Graph**: If endpoint fails, falls back to `data/cse_kg_local/graph.pkl` (if downloaded)

**Configuration** (`config.yaml`):
```yaml
cse_kg:
  sparql_endpoint: http://w3id.org/cskg/sparql  # ONLINE
  local_cache: true                               # Caches online queries
  cache_dir: data/cse_kg_cache                    # Local cache location
```

**Dependencies**:
- ✅ **Requires internet** for first-time queries
- ✅ **Works offline** if cached or local graph exists
- ⚠️ **26,000+ entities** available online

**Files**:
- `src/knowledge_graph/cse_kg_client.py` - Online SPARQL client
- `src/knowledge_graph/local_cse_kg_client.py` - Local fallback

---

### 2. **Pedagogical Knowledge Graph**

**Status**: ✅ **COMPLETELY LOCAL**

**Source**: 
- **Local JSON files** in `data/pedagogical_kg/`
- **No online dependencies**
- Default data is **created programmatically** if files don't exist

**Files**:
- `data/pedagogical_kg/misconceptions.json` - Misconceptions database
- `data/pedagogical_kg/learning_progressions.json` - Learning paths
- `data/pedagogical_kg/cognitive_loads.json` - Cognitive load data
- `data/pedagogical_kg/interventions.json` - Intervention mappings

**Initialization**:
- If files don't exist, `PedagogicalKGBuilder` creates default data
- All data is **stored locally** as JSON
- **No internet required**

**Configuration** (`config.yaml`):
```yaml
pedagogical_kg:
  enabled: true
  data_dir: data/pedagogical_kg  # LOCAL ONLY
  auto_save: true
```

**Dependencies**:
- ✅ **No internet required**
- ✅ **Fully offline**
- ✅ **Extensible** - Easy to add/edit data

**Files**:
- `src/knowledge_graph/pedagogical_kg_builder.py` - Local builder
- `src/knowledge_graph/pedagogical_kg_schema.py` - Schema definitions

---

### 3. **Student-Specific Knowledge Graphs**

**Status**: ✅ **LOCAL (Built Dynamically)**

**Source**:
- **Built dynamically** from student interactions
- Uses **CSE-KG structure** (from online/local) as base
- **Personalized** per student with mastery levels, misconceptions, etc.

**Storage**:
- Created in-memory during session processing
- Can be persisted to database/files
- **No online dependency** (except for CSE-KG structure)

**Files**:
- `src/knowledge_graph/graph_fusion.py` - Student graph builder

---

## 🔄 How They Work Together

```
┌─────────────────────────────────────────┐
│  CSE-KG 2.0 (ONLINE)                    │
│  └─> http://w3id.org/cskg/sparql        │
│      └─> Cached: data/cse_kg_cache/      │
│      └─> Fallback: data/cse_kg_local/   │
└─────────────────────────────────────────┘
           │
           ├─> Provides domain knowledge structure
           │
           ▼
┌─────────────────────────────────────────┐
│  Pedagogical KG (LOCAL)                 │
│  └─> data/pedagogical_kg/*.json         │
│      • Misconceptions                   │
│      • Learning progressions            │
│      • Cognitive loads                  │
│      • Interventions                    │
└─────────────────────────────────────────┘
           │
           ├─> Extends with pedagogical data
           │
           ▼
┌─────────────────────────────────────────┐
│  Unified Pedagogical-CS KG               │
│  └─> Combines both sources              │
│      • Domain knowledge (CSE-KG)        │
│      • Pedagogical needs (Local)       │
└─────────────────────────────────────────┘
           │
           ├─> Used as base structure
           │
           ▼
┌─────────────────────────────────────────┐
│  Student-Specific Graphs (LOCAL)        │
│  └─> Built dynamically per student      │
│      • Mastery levels                   │
│      • Personal misconceptions          │
│      • Learning history                 │
└─────────────────────────────────────────┘
```

---

## 📋 Summary Table

| Graph | Source | Online? | Local? | Internet Required? |
|-------|--------|---------|--------|-------------------|
| **CSE-KG 2.0** | SPARQL endpoint | ✅ Yes | ✅ Cached | ⚠️ First time only |
| **Pedagogical KG** | Local JSON files | ❌ No | ✅ Yes | ❌ No |
| **Student Graphs** | Built dynamically | ❌ No | ✅ Yes | ❌ No (unless CSE-KG needed) |

---

## 🎯 Key Points

### CSE-KG 2.0 (ONLINE)
- ✅ **Primary**: Online SPARQL endpoint
- ✅ **Cached**: Queries cached locally for performance
- ✅ **Fallback**: Local graph if endpoint unavailable
- ⚠️ **Requires internet** for new queries (unless cached)

### Pedagogical KG (LOCAL)
- ✅ **Completely local** - No online dependencies
- ✅ **Default data** created automatically
- ✅ **Extensible** - Easy to add/edit
- ✅ **Works offline** - No internet needed

### Student Graphs (LOCAL)
- ✅ **Built dynamically** from interactions
- ✅ **Personalized** per student
- ✅ **No online dependency** (except for CSE-KG structure)

---

## 💡 Recommendations

### For Offline Use:
1. **Download CSE-KG locally** first (if possible)
2. **Use local cache** - Run queries once to populate cache
3. **Pedagogical KG** - Already fully local
4. **Student graphs** - Already local

### For Online Use:
1. **CSE-KG** - Queries online endpoint (with caching)
2. **Pedagogical KG** - Uses local files
3. **Student graphs** - Built locally

---

## 🔧 Making Everything Local

If you want to make CSE-KG fully local:

1. **Download CSE-KG dataset**:
   ```bash
   python download_cse_kg_full.py
   ```

2. **Build local graph**:
   ```bash
   python build_local_cse_kg.py
   ```

3. **Update config** to prefer local:
   ```yaml
   cse_kg:
     local_cache: true
     prefer_local: true  # If implemented
   ```

---

## ✅ Conclusion

- **CSE-KG**: ⚠️ **ONLINE** (with local cache/fallback)
- **Pedagogical KG**: ✅ **LOCAL** (completely offline)
- **Student Graphs**: ✅ **LOCAL** (built dynamically)

**Total Online Dependency**: Only CSE-KG (and only for new queries, cached queries work offline)












