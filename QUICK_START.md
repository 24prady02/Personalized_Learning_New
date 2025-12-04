# Quick Start Guide

Get the Personalized Learning System running in **5 minutes**!

## Prerequisites

- Python 3.8+
- Internet connection (for downloading datasets)
- 2GB free disk space

## Installation (One Command!)

```bash
# 1. Clone repository
git clone <repository-url>
cd Personalized_Learning

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run automated setup
python scripts/quick_start.py
```

That's it! The script will automatically:
- ✅ Download pre-trained models (CodeBERT, BERT)
- ✅ Download datasets from GitHub
- ✅ Initialize CSE-KG connection
- ✅ Verify everything works
- ✅ Process data for training

## What Gets Downloaded?

| Dataset | Source | Size | What It Contains |
|---------|--------|------|------------------|
| **ProgSnap2** | GitHub | ~10 MB | 50K debugging sessions |
| **CodeNet** | GitHub | ~1 MB | Code samples (Python/Java/C++) |
| **ASSISTments** | Generated | ~10 KB | Student responses & Q-matrix |
| **MOOCCubeX** | Generated | ~50 KB | Course activities & KG |
| **CodeBERT** | HuggingFace | ~500 MB | Pre-trained code model |
| **BERT** | HuggingFace | ~420 MB | Pre-trained text model |

**Total**: ~1 GB

## First Test

### Start the API Server

```bash
python api/server.py
```

Output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✓ System initialized successfully
```

### Try an Example

Open a new terminal:

```bash
python example_usage.py
```

This will:
1. Send a debugging session (recursion error)
2. Get personalized intervention
3. Query CSE-KG for concepts
4. Show all API features

## Example API Call

```python
import requests

response = requests.post("http://localhost:8000/api/session", json={
    "student_id": "student_123",
    "code": """
def factorial(n):
    # Missing base case!
    return n * factorial(n - 1)
    """,
    "error_message": "RecursionError: maximum recursion depth exceeded",
    "action_sequence": ["code_edit", "compile", "run_test"],
    "time_deltas": [10.5, 2.1, 1.5],
    "time_stuck": 14.1
})

result = response.json()
print(f"Intervention: {result['intervention_type']}")
print(f"Explanation: {result['content']['explanation']}")
```

## What You Can Do Now

### 1. Explore the API

```bash
# Health check
curl http://localhost:8000/

# Get concept info from CSE-KG
curl http://localhost:8000/api/concept/recursion

# System statistics
curl http://localhost:8000/api/stats
```

### 2. Process Your Own Session

```python
import requests

my_session = {
    "student_id": "your_student_id",
    "code": "your buggy code here",
    "error_message": "error message",
    "action_sequence": ["code_edit", "run_test"],
    "time_deltas": [5.0, 2.0]
}

response = requests.post("http://localhost:8000/api/session", json=my_session)
print(response.json())
```

### 3. Train Models

```bash
# Pre-train on CodeNet
python train.py --config config.yaml

# Monitor with Weights & Biases
python train.py --wandb
```

### 4. Customize Configuration

Edit `config.yaml` to adjust:
- Model architectures
- Training hyperparameters
- Intervention priorities
- Dataset paths

## Common Issues

### Port Already in Use

```bash
# Change port in api/server.py
uvicorn.run("server:app", host="0.0.0.0", port=8001)
```

### CUDA Out of Memory

```yaml
# In config.yaml
system:
  device: "cpu"  # Change from "cuda"
```

### Download Fails

```bash
# Retry individual downloads
python scripts/download_datasets.py
python scripts/download_models.py
```

## Next Steps

- 📖 Read [README.md](README.md) for full architecture
- 📊 See [DATASETS.md](DATASETS.md) for dataset details
- 🔧 Check [config.yaml](config.yaml) for all options
- 💻 Explore [notebooks/](notebooks/) for tutorials
- 🚀 Deploy with Docker (coming soon)

## Getting Help

- **Issues**: Open a GitHub issue
- **Questions**: Check documentation
- **Examples**: See `example_usage.py`

---

**You're all set! 🎉**

The system is now running and ready to provide personalized programming education assistance.




