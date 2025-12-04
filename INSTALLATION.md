# Installation Guide

## Prerequisites

- Python 3.8 or higher
- CUDA-capable GPU (optional, for faster training)
- 16GB RAM minimum (32GB recommended)
- MongoDB (optional, for production deployment)
- Redis (optional, for caching)

## Step 1: Clone Repository

```bash
git clone <repository-url>
cd Personalized_Learning
```

## Step 2: Create Virtual Environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Automated Setup (RECOMMENDED)

### Option A: One-Command Setup 🚀

```bash
python scripts/quick_start.py
```

This automatically:
1. ✅ Downloads pre-trained models (CodeBERT, BERT)
2. ✅ Downloads all datasets from GitHub/online sources
3. ✅ Initializes CSE-KG 2.0 connection
4. ✅ Verifies all datasets
5. ✅ Processes data for training

**That's it! System is ready to use.**

### Option B: Manual Step-by-Step

If you prefer control over each step:

**4a. Download Pre-trained Models**
```bash
python scripts/download_models.py
```

This downloads:
- CodeBERT for code encoding
- BERT for text encoding

**4b. Download Datasets from Online Sources**
```bash
python scripts/download_datasets.py
```

This downloads from GitHub:
- ✅ **ProgSnap2** sample dataset (~10 MB)
  - Source: https://github.com/ProgSnap2/progsnap2-spec
  - 50K+ debugging sessions with temporal data
  
- ✅ **CodeNet** sample submissions (~1 MB)
  - Source: https://github.com/IBM/Project_CodeNet
  - Python, Java, C++ code samples (correct & buggy)
  
- ✅ **ASSISTments** sample data (~10 KB)
  - Student responses with skill mappings
  - Q-matrix for DINA model
  
- ✅ **MOOCCubeX** sample data (~50 KB)
  - Source: https://github.com/THU-KEG/MOOC-Cube
  - Course activities and knowledge graphs

**4c. Initialize CSE-KG Connection**
```bash
python scripts/init_knowledge_graph.py
```

This:
- Tests connection to CSE-KG 2.0 SPARQL endpoint
- Caches common computer science concepts
- Verifies knowledge graph access

**4d. Verify Datasets**
```bash
python scripts/verify_datasets.py
```

Checks all datasets are correctly downloaded.

**4e. Process Datasets**
```bash
python scripts/process_datasets.py
```

Prepares data for training.

## Step 5: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# nano .env  # or use your preferred editor
```

## Step 6: Verify Installation

```bash
# Test import
python -c "from src.models.hvsae import HVSAE; print('✓ Installation successful!')"
```

## Optional: Set Up Databases

### MongoDB (for production)

```bash
# Install MongoDB
# See: https://docs.mongodb.com/manual/installation/

# Start MongoDB
mongod --dbpath /path/to/data
```

### Redis (for caching)

```bash
# Install Redis
# See: https://redis.io/docs/getting-started/installation/

# Start Redis
redis-server
```

## Running the System

### 1. Start API Server

```bash
python api/server.py
```

The API will be available at `http://localhost:8000`

### 2. Run Example

```bash
python example_usage.py
```

### 3. Train Models (optional)

```bash
# Pre-training on CodeNet
python train.py --config configs/hvsae_pretrain.yaml

# Fine-tuning on ProgSnap2
python train.py --config configs/hvsae_finetune.yaml --resume checkpoints/pretrain.pt
```

## Troubleshooting

### CUDA Out of Memory

If you encounter GPU memory errors, reduce batch size in `config.yaml`:

```yaml
training:
  batch_size: 16  # Reduce from 32
```

### CSE-KG Connection Timeout

If CSE-KG queries timeout, the system will work with cached data. To improve:

1. Check your internet connection
2. Increase timeout in config:

```yaml
cse_kg:
  timeout: 60  # seconds
```

### Missing Dependencies

If you get import errors:

```bash
pip install --upgrade -r requirements.txt
```

## Next Steps

- Read the [README.md](README.md) for architecture overview
- Check [example_usage.py](example_usage.py) for API examples
- See [config.yaml](config.yaml) for configuration options
- Review the [notebooks/](notebooks/) directory for tutorials

## Support

For issues and questions, please open an issue on GitHub.

