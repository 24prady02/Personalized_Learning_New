# 🚀 Ollama Setup Guide - Free AI Generation

## Why Ollama?

✅ **Easiest** free AI setup  
✅ **Fast** inference (works well on CPU)  
✅ **Free** unlimited usage  
✅ **Offline** after initial download  
✅ **Multiple models** available  

---

## Quick Setup (3 Steps - 5 Minutes)

### Step 1: Download Ollama

Visit: **https://ollama.ai/**

Click **"Download for Windows"**

Run the installer (takes 1 minute)

### Step 2: Install a Model

Open PowerShell or CMD and run:

```bash
ollama run llama3.2
```

This will:
- Download Llama 3.2 model (~2GB, one-time)
- Start Ollama server automatically
- Take 5-10 minutes depending on internet speed

**Alternative models:**
```bash
ollama run phi3              # Smaller, faster (1.3GB)
ollama run mistral           # Good balance (4GB)
ollama run deepseek-coder    # Code-focused (6.7GB)
```

### Step 3: Test It

Run this in Python:

```bash
python src/orchestrator/ollama_generator.py
```

You should see:
```
✅ Ollama connected! Using model: llama3.2
```

---

## Verification

```bash
# Check if Ollama is running
ollama list

# Should show:
# NAME            SIZE    MODIFIED
# llama3.2:latest 2.0GB   2 minutes ago
```

---

## Using in Your System

```python
from src.orchestrator.ollama_generator import OllamaGenerator

# Initialize
generator = OllamaGenerator(model="llama3.2")

# Generate response based on YOUR models
response = generator.generate_teaching_response(
    student_state=...,      # From DINA, Nestor, RNN
    knowledge_gaps=...,     # From DINA
    intervention_type=...,  # From RL
    student_input=...,      # Student's question
    kg_knowledge=...        # From CSE-KG!
)

print(response)  # AI-generated, model-driven content!
```

---

## Troubleshooting

**"Ollama not found"**
- Make sure you installed from https://ollama.ai/
- Restart terminal after installation

**"Model not found"**
```bash
ollama run llama3.2  # Downloads and runs
```

**"Connection refused"**
```bash
ollama serve  # Start server manually
```

**Slow generation?**
- Normal on CPU (10-30 seconds)
- Consider using Groq API for faster results

---

## Next Steps

Once Ollama is running:

1. Test basic generation:
   ```bash
   python src/orchestrator/ollama_generator.py
   ```

2. See it integrated with your models:
   ```bash
   python demo_ollama_integrated.py
   ```

3. Use in full system:
   ```python
   # In orchestrator
   generator = OllamaGenerator()
   ```

---

## Model Comparison

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **phi3** | 1.3GB | Very Fast | Good | Quick responses |
| **llama3.2** | 2GB | Fast | Great | Balanced (recommended) |
| **mistral** | 4GB | Medium | Excellent | High quality |
| **deepseek-coder** | 6.7GB | Slower | Excellent | Code teaching |

Start with **llama3.2** - best balance!

---

## Summary

```
Download Ollama (1 min)
   ↓
ollama run llama3.2 (5-10 min download)
   ↓
python ollama_generator.py
   ↓
AI-Generated Teaching Content! ✅
```

**Total time: 10-15 minutes for complete setup!**


















