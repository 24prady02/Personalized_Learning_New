# Dataset Documentation

## 📥 Automatic Dataset Downloading

The system automatically downloads datasets from public sources on GitHub and elsewhere. No manual downloading required!

## Available Datasets

### 1. ProgSnap2 (Debugging Sessions)

**Source**: https://github.com/ProgSnap2/progsnap2-spec

**What it downloads**:
- Sample dataset from ProgSnap2 specification repository
- CS1 dataset from iSnap Fall 2017 (~50K debugging sessions)
- Contains: EventID, SubjectID, ProblemID, EventType, CodeState, timestamps

**File downloaded**: `data/progsnap2/MainTable.csv`

**Size**: ~10-50 MB (depending on which dataset)

**Format**:
```csv
EventID,SubjectID,ProblemID,EventType,ServerTimestamp,CodeStateSection
1,student_001,p001,Run.Program,1234567890,def factorial(n)...
2,student_001,p001,Compile.Error,1234567895,def factorial(n)...
```

**Usage in system**:
- Fine-tuning behavioral RNN/HMM models
- Debugging strategy classification
- Temporal action sequence analysis

---

### 2. CodeNet Sample (Code Submissions)

**Source**: https://github.com/IBM/Project_CodeNet

**What it downloads**:
- Sample code submissions (correct and buggy)
- Python, Java, C++ examples
- Problem metadata

**Note**: Full CodeNet is 100GB+. The script downloads/creates representative samples.

**Files created**: `data/codenet/{python,java,cpp}/*.txt`

**Samples included**:
- ✅ Correct factorial implementation
- ✅ Buggy factorial (missing base case)
- ✅ Correct Fibonacci
- ✅ Buggy array access (IndexError)
- ✅ NullPointerException example

**Usage in system**:
- HVSAE pre-training
- Code understanding
- Error pattern recognition

---

### 3. ASSISTments (Student Responses)

**Source**: Publicly available skill-builder dataset

**What it creates**:
- Sample student response data
- Problem-skill mappings
- Q-matrix structure

**File created**: `data/assistments/skill_builder_data.csv`

**Format**:
```csv
user_id,problem_id,correct,skill_name,attempt_count
1,101,1,Addition,1
1,102,0,Subtraction,2
2,101,1,Addition,1
```

**Sample size**: 90 responses (expandable)

**Usage in system**:
- DINA model training
- Q-matrix construction
- Concept mastery estimation
- **Nestor Bayesian Network training** (personality → learning style → strategy relationships)

**Note**: For full ASSISTments dataset (500K+ responses), visit:
https://sites.google.com/site/assistmentsdata/

---

### 4. MOOCCubeX (Course Activities)

**Source**: https://github.com/THU-KEG/MOOC-Cube

**What it creates**:
- Sample student-course interactions
- Concept relationships
- Knowledge graph structure

**Files created**:
- `data/moocsxcube/entities.json`
- `data/moocsxcube/relations.json`
- `data/moocsxcube/knowledge_graph.json`

**Structure**:
```json
{
  "student": [{"id": "s001", "level": "beginner"}],
  "course": [{"id": "c001", "name": "Intro to Programming"}],
  "concept": [{"id": "concept_001", "name": "variables"}]
}
```

**Usage in system**:
- Knowledge graph validation
- Course prerequisite modeling
- Student activity analysis
- **Nestor training data** (student personality, learning styles, strategies, and intervention preferences)

---

### 5. CSE-KG 2.0 (Computer Science Knowledge Graph)

**Source**: http://cse.ckcest.cn/cskg/sparql

**What it provides**:
- 26,000+ CS entities (Methods, Tasks, Materials, Concepts)
- Relationships: requiresKnowledge, usesMethod, solvesTask
- SPARQL endpoint for live queries
- Local caching for performance

**Not downloaded**: This is a live endpoint, queries are cached locally

**Cache location**: `data/cse_kg_cache/*.pkl`

**Usage in system**:
- Domain knowledge backbone
- Prerequisite identification
- Concept explanation grounding
- Q-matrix enhancement

---

## Download Scripts

### Main Script: `scripts/download_datasets.py`

```python
from scripts.download_datasets import DatasetDownloader

downloader = DatasetDownloader()
downloader.download_all()  # Download everything

# Or download individually:
downloader.download_progsnap2_sample()
downloader.download_codenet_sample()
downloader.download_assistments_data()
downloader.download_mooccubex_sample()
```

### Features:
- ✅ Progress bars for downloads
- ✅ Automatic extraction (zip, tar, gz)
- ✅ Checks for existing files
- ✅ Error handling and retry
- ✅ Creates sample data when full datasets unavailable

---

## Verification

After downloading, verify datasets:

```bash
python scripts/verify_datasets.py
```

**Output**:
```
=== Verifying ProgSnap2 ===
✓ MainTable.csv found: 1250 rows

=== Verifying CodeNet ===
✓ python: 4 code files
✓ java: 2 code files

=== Verifying ASSISTments ===
✓ skill_builder_data.csv found: 90 responses
  Students: 3
  Problems: 6
  Skills: 9

=== Verifying MOOCCubeX ===
✓ entities.json found
✓ relations.json found
✓ knowledge_graph.json found

VERIFICATION SUMMARY
ProgSnap2        : ✓ PASS
CodeNet          : ✓ PASS
ASSISTments      : ✓ PASS
MOOCCubeX        : ✓ PASS
```

---

## Processing

Process downloaded datasets for training:

```bash
python scripts/process_datasets.py
```

This creates processed files in `data/processed/`:
- `codenet_processed.csv`
- `progsnap2_processed.csv`
- `assistments_responses.csv`
- `assistments_qmatrix.csv`
- `moocsxcube_processed.csv`

---

## Dataset Sizes

| Dataset | Raw Size | Processed Size | Records |
|---------|----------|----------------|---------|
| ProgSnap2 | ~10 MB | ~5 MB | 1K-50K sessions |
| CodeNet | ~1 MB | ~500 KB | 6-10 samples |
| ASSISTments | ~10 KB | ~10 KB | 90-500K responses |
| MOOCCubeX | ~50 KB | ~50 KB | 100-2M activities |
| CSE-KG 2.0 | N/A (online) | Cached | 26K+ entities |

---

## Expanding Datasets

### Adding More CodeNet Data

To use full CodeNet (14M submissions):

1. Download from IBM: https://developer.ibm.com/exchanges/data/all/project-codenet/
2. Extract to `data/codenet/`
3. Update `config.yaml`:
   ```yaml
   codenet:
     path: "data/codenet"
     languages: ["python", "java", "cpp", "javascript"]
   ```

### Adding Full ProgSnap2 Datasets

Available datasets:
- iSnap Fall 2015-2018
- Python snapshots
- Hour of Code datasets

Download from: https://github.com/ProgSnap2/ProgSnap2-CS1-Datasets

### Getting Full ASSISTments

1. Register at: https://sites.google.com/site/assistmentsdata/
2. Download skill builder dataset
3. Place in `data/assistments/`

---

## Custom Datasets

### Adding Your Own Data

The system supports custom datasets. Create a processor:

```python
# src/data/processors.py

class CustomProcessor(BaseProcessor):
    def process(self) -> pd.DataFrame:
        # Your processing logic
        data = []
        # ... load your data ...
        return pd.DataFrame(data)
```

Then use it:

```python
from src.data.processors import CustomProcessor

processor = CustomProcessor("data/custom", config)
df = processor.process()
```

---

## Data Privacy

All sample datasets are:
- ✅ Publicly available
- ✅ Anonymized
- ✅ No personal information
- ✅ Educational use permitted

For production use with real student data:
- Ensure proper consent
- Follow FERPA/GDPR guidelines
- Anonymize personal identifiers
- Secure data storage

---

## Troubleshooting

### Download Fails

```bash
# Retry with individual downloads
python -c "from scripts.download_datasets import DatasetDownloader; DatasetDownloader().download_progsnap2_sample()"
```

### Disk Space

Minimum: 500 MB
Recommended: 2 GB (for caching)

### Slow Downloads

- CSE-KG queries are cached after first use
- Large datasets (CodeNet full) take time
- Use sample datasets for development

---

## Data Attribution

When using these datasets, please cite:

**ProgSnap2**:
```bibtex
@article{hovemeyer2021progsnap2,
  title={ProgSnap2: A flexible format for programming process data},
  author={Hovemeyer, David and others},
  year={2021}
}
```

**CodeNet**:
```bibtex
@article{puri2021codenet,
  title={Project CodeNet: A Large-Scale AI for Code Dataset for Learning a Diversity of Coding Tasks},
  author={Puri, Ruchir and others},
  year={2021}
}
```

**ASSISTments**:
```bibtex
@article{feng2009addressing,
  title={Addressing the assessment challenge with an online system},
  author={Feng, Mingyu and others},
  journal={User Modeling and User-Adapted Interaction},
  year={2009}
}
```

**CSE-KG**:
```bibtex
@inproceedings{chen2021cse,
  title={CSE-KG: A Computer Science Knowledge Graph},
  author={Chen, Xuming and others},
  year={2021}
}
```













