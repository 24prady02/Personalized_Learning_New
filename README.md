# Personalized Learning System for Programming Education

## Abstract
This project studies an AI-driven personalized learning system for programming education. It combines student modeling, knowledge graph integration, and adaptive teaching strategies to deliver targeted interventions and explanations during learning sessions. The repository is organized to support transparent and reproducible research workflows.

## Research Questions
1. How effectively can adaptive teaching policies improve student mastery over static feedback?
2. Which student-modeling signals (knowledge tracing, behavior, misconceptions) best predict learning gains?
3. How does knowledge graph grounding affect explanation quality and student outcomes?

## Repository Structure
- `README.md`: Project overview and replication steps.
- `requirements.txt`: Python dependencies for the project.
- `data/raw/`: Original datasets (or pointers/download scripts when files are too large).
- `data/processed/`: Cleaned and transformed datasets.
- `src/preprocessing.py`: Data loading and preprocessing entry pipeline.
- `src/model.py`: Baseline model interface used by training/evaluation.
- `src/train.py`: Reproducible training entrypoint.
- `src/evaluate.py`: Reproducible evaluation entrypoint.
- `src/utils/`: Utility modules (configuration and metrics helpers).
- `notebooks/`: Exploratory analysis and visualization notebooks.
- `experiments/logs/`: Experiment logs and metadata.
- `results/`: Output metrics, tables, and figures.
- `paper/main.tex`: LaTeX manuscript source.
- `paper/references.bib`: Bibliography file.
- `paper/figures/`: Manuscript figures.
- `slides/`: Presentation materials.

## Environment Setup
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
# source venv/bin/activate

pip install -r requirements.txt
```

## How to Run
### 1) Preprocess Data
```bash
python src/preprocessing.py
```

### 2) Train
```bash
python src/train.py --data data/processed/your_dataset.csv --out experiments/logs/train_metrics.json
```

### 3) Evaluate
```bash
python src/evaluate.py --data data/processed/your_dataset.csv --out results/eval_metrics.json
```

## Dataset Source and Access
- Primary sources include educational coding datasets such as ProgSnap2, CodeNet, ASSISTments, and MOOCCubeX.
- Use scripts in `scripts/` (for example dataset download and verification utilities) to fetch or validate data.
- If a dataset is too large for Git, keep it out of version control and store access instructions or links in this repository.

## Notes on Reproducibility
- Commit frequently with meaningful messages.
- Use feature branches for in-progress experiments and merge stable work into `main`.
- Do not commit secrets, API keys, large raw datasets, or model checkpoints.
