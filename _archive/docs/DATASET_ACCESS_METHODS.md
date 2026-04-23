# Dataset Access Methods: Online vs. Local

## Summary: How Each Dataset is Accessed

| Dataset | Access Method | Online/Local | Details |
|---------|--------------|--------------|---------|
| **CSE-KG 2.0** | **Online (Live SPARQL)** | 🌐 **ONLINE** | Queried via SPARQL endpoint with local caching |
| **ASSISTments** | **Downloaded Locally** | 💾 **LOCAL** | Downloaded CSV file, stored locally |
| **ProgSnap2** | **Downloaded Locally** | 💾 **LOCAL** | Downloaded from GitHub, stored locally |
| **CodeNet** | **Downloaded Locally** | 💾 **LOCAL** | Downloaded from GitHub, stored locally |
| **MOOCCubeX** | **Downloaded/Generated Locally** | 💾 **LOCAL** | Sample generated or downloaded, stored locally |

---

## Detailed Breakdown

### 1. CSE-KG 2.0 (Computer Science Knowledge Graph) 🌐

**Access Method: ONLINE (Live SPARQL Queries)**

- **Endpoint**: `http://cse.ckcest.cn/cskg/sparql`
- **Method**: Real-time SPARQL queries via HTTP
- **Caching**: Results are cached locally for performance
- **Cache Location**: `data/cse_kg_cache/*.pkl`
- **Cache Duration**: 24 hours (configurable)

**How It Works:**
```python
# System queries CSE-KG online endpoint
client = CSEKGClient(config)
# First query: Goes online → Caches result locally
info = client.get_concept_info("recursion")
# Subsequent queries: Uses cached result (if available)
```

**Advantages:**
- ✅ Always up-to-date (real-time data)
- ✅ No local storage needed for full graph
- ✅ Local caching improves performance
- ✅ Access to 26,000+ entities without downloading

**Disadvantages:**
- ⚠️ Requires internet connection
- ⚠️ Dependent on endpoint availability
- ⚠️ First query may be slower

**Code Location**: `src/knowledge_graph/cse_kg_client.py`

---

### 2. ASSISTments Dataset 💾

**Access Method: LOCAL (Downloaded CSV File)**

- **Source**: https://sites.google.com/site/assistmentsdata/
- **Method**: Download CSV file, store locally
- **File Location**: `data/assistments/skill_builder_data.csv` (sample) or `data/assistments/2012-2013-data-with-predictions-4-final.csv` (full)
- **Format**: CSV file with student responses

**How It Works:**
```python
# System reads from local CSV file
import pandas as pd
df = pd.read_csv('data/assistments/skill_builder_data.csv')
# Process locally - no online access needed
```

**Download Process:**
1. User downloads from ASSISTments website
2. Saves to `data/assistments/` directory
3. System reads from local file

**Advantages:**
- ✅ Works offline
- ✅ Fast access (no network latency)
- ✅ Full control over data
- ✅ Can process large datasets efficiently

**Disadvantages:**
- ⚠️ Requires manual download (full dataset)
- ⚠️ Takes up local storage space
- ⚠️ Data may become outdated

**Code Location**: `validate_on_assistments.py`, `scripts/download_datasets.py`

**Note**: There is **NO online API** for ASSISTments - it must be downloaded as a CSV file.

---

### 3. ProgSnap2 Dataset 💾

**Access Method: LOCAL (Downloaded from GitHub)**

- **Source**: https://github.com/ProgSnap2/progsnap2-spec
- **Method**: Download CSV files from GitHub, store locally
- **File Location**: `data/progsnap2/MainTable.csv`
- **Format**: CSV files with debugging session data

**How It Works:**
```python
# System downloads from GitHub
downloader = DatasetDownloader()
downloader.download_progsnap2_sample()
# Then reads from local file
df = pd.read_csv('data/progsnap2/MainTable.csv')
```

**Download Process:**
1. System automatically downloads from GitHub
2. Stores in `data/progsnap2/` directory
3. System reads from local files

**Advantages:**
- ✅ Works offline after download
- ✅ Fast access
- ✅ Automatic download script available

**Disadvantages:**
- ⚠️ Requires initial download
- ⚠️ Takes up local storage

**Code Location**: `scripts/download_datasets.py`

---

### 4. CodeNet Dataset 💾

**Access Method: LOCAL (Downloaded from GitHub)**

- **Source**: https://github.com/IBM/Project_CodeNet
- **Method**: Download code files from GitHub, store locally
- **File Location**: `data/codenet/{python,java,cpp}/*.txt`
- **Format**: Plain text code files

**How It Works:**
```python
# System downloads from GitHub
downloader = DatasetDownloader()
downloader.download_codenet_sample()
# Then reads from local files
with open('data/codenet/python/factorial.py', 'r') as f:
    code = f.read()
```

**Download Process:**
1. System automatically downloads sample from GitHub
2. Stores in `data/codenet/` directory
3. System reads from local files

**Advantages:**
- ✅ Works offline after download
- ✅ Fast access
- ✅ Automatic download script available

**Disadvantages:**
- ⚠️ Full dataset is 100GB+ (only samples downloaded)
- ⚠️ Takes up local storage

**Code Location**: `scripts/download_datasets.py`

---

### 5. MOOCCubeX Dataset 💾

**Access Method: LOCAL (Generated Sample or Downloaded)**

- **Source**: https://github.com/THU-KEG/MOOC-Cube (or generated sample)
- **Method**: Generate sample data or download JSON files, store locally
- **File Location**: `data/moocsxcube/{entities,relations,knowledge_graph}.json`
- **Format**: JSON files with course structure data

**How It Works:**
```python
# System generates sample or downloads
downloader = DatasetDownloader()
downloader.download_mooccubex_sample()
# Then reads from local JSON files
with open('data/moocsxcube/entities.json', 'r') as f:
    entities = json.load(f)
```

**Download Process:**
1. System generates sample data OR downloads from GitHub
2. Stores in `data/moocsxcube/` directory
3. System reads from local JSON files

**Advantages:**
- ✅ Works offline
- ✅ Fast access
- ✅ Can generate samples without download

**Disadvantages:**
- ⚠️ Sample data is limited
- ⚠️ Full dataset requires download

**Code Location**: `scripts/download_datasets.py`

---

## Quick Reference

### Online Access (Requires Internet)
- ✅ **CSE-KG 2.0**: Live SPARQL queries (with local caching)

### Local Access (Works Offline)
- ✅ **ASSISTments**: Downloaded CSV file
- ✅ **ProgSnap2**: Downloaded CSV files
- ✅ **CodeNet**: Downloaded code files
- ✅ **MOOCCubeX**: Generated/Downloaded JSON files

---

## Configuration

### CSE-KG 2.0 Online Access
```yaml
# config.yaml
cse_kg:
  sparql_endpoint: "http://cse.ckcest.cn/cskg/sparql"  # Online endpoint
  local_cache: true  # Enable local caching
  cache_dir: "data/cse_kg_cache"  # Cache location
```

### Local Dataset Paths
```yaml
# config.yaml
datasets:
  assistments:
    path: "data/assistments/skill_builder_data.csv"  # Local file
  progsnap2:
    path: "data/progsnap2/MainTable.csv"  # Local file
  codenet:
    path: "data/codenet"  # Local directory
  moocsxcube:
    path: "data/moocsxcube"  # Local directory
```

---

## Answer to Your Question

**Q: Is ASSISTments used online or downloaded locally?**

**A: ASSISTments is DOWNLOADED LOCALLY** (not accessed online)

- ❌ **NO online API** - Must download CSV file
- ✅ **Local CSV file** - Stored in `data/assistments/`
- ✅ **Works offline** - No internet needed after download
- ✅ **Read from disk** - System reads from local file

**To use ASSISTments:**
1. Download CSV from: https://sites.google.com/site/assistmentsdata/
2. Save to: `data/assistments/2012-2013-data-with-predictions-4-final.csv`
3. System reads from local file (no online access)

---

## Summary Table

| Dataset | Online? | Local? | Requires Internet? | Notes |
|---------|---------|--------|-------------------|-------|
| **CSE-KG 2.0** | ✅ Yes | ✅ Cached | ✅ Yes (first time) | SPARQL endpoint, cached locally |
| **ASSISTments** | ❌ No | ✅ Yes | ❌ No (after download) | CSV file, must download manually |
| **ProgSnap2** | ❌ No | ✅ Yes | ❌ No (after download) | CSV files, auto-downloaded |
| **CodeNet** | ❌ No | ✅ Yes | ❌ No (after download) | Code files, auto-downloaded |
| **MOOCCubeX** | ❌ No | ✅ Yes | ❌ No (after download) | JSON files, generated/downloaded |

---

## Conclusion

**Only CSE-KG 2.0 is accessed online** (via SPARQL endpoint with local caching).

**All other datasets (ASSISTments, ProgSnap2, CodeNet, MOOCCubeX) are stored locally** and accessed from disk.

**For ASSISTments specifically**: It is **NOT accessed online** - you must download the CSV file and store it locally. The system then reads from the local file.












