# CPAL — Setup Guide (Ollama + Cursor)

## What you need
- Python 3.10 or higher
- Ollama installed (free, local LLM runner)
- 8GB RAM minimum (16GB recommended for llama3.1)
- Cursor IDE

---

## Step 1 — Install Ollama

Go to **ollama.com** and download for your OS. Install it.

Then open a terminal and pull the model:

```bash
# If you have 16GB+ RAM (better quality)
ollama pull llama3.1

# If you have 8GB RAM (smaller, faster)
ollama pull llama3.2
```

Then start Ollama:

```bash
ollama serve
```

Leave this terminal running. Ollama must be running whenever you use CPAL.

If you use `llama3.2`, open `config.yaml` and change:
```yaml
ollama:
  model: "llama3.2"
```

---

## Step 2 — Open in Cursor

Open Cursor → **File → Open Folder** → select the `pls_fixed` folder.

---

## Step 3 — Create Python virtual environment

Open the Cursor terminal (`Ctrl+backtick`) and run:

```bash
python -m venv venv
```

Activate it:

```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

---

## Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

If the full install is slow, install essentials first:

```bash
pip install torch transformers networkx fastapi uvicorn pyyaml numpy pandas scikit-learn python-dotenv requests
```

---

## Step 5 — Set up Java knowledge base (run once)

```bash
python scripts/setup_java_knowledge.py
```

You should see:
```
[OK] Saved data/pedagogical_kg/misconceptions.json (20 items)
[OK] Saved data/pedagogical_kg/learning_progressions.json (5 items)
[OK] Saved data/pedagogical_kg/cognitive_loads.json (20 items)
[OK] Saved data/pedagogical_kg/interventions.json (8 items)
[OK] Saved data/pedagogical_kg/lp_rubric.json (20 items)
[DONE] Java Pedagogical KG ready.
```

---

## Step 6 — Run the server

```bash
uvicorn api.server:app --reload --port 8000
```

You should see:
```
[OK] Enhanced Personalized Generator with Ollama (llama3.1) initialized
[OK] Student State Tracker initialized
✓ System initialized successfully
INFO: Uvicorn running on http://127.0.0.1:8000
```

---

## Step 7 — Test with a student message

Open a new terminal tab (keep server running), activate venv, then:

```bash
curl -X POST http://localhost:8000/api/session \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "test_001",
    "code": "String s1 = new String(\"hello\"); String s2 = new String(\"hello\"); if (s1 == s2) { System.out.println(\"equal\"); }",
    "error_message": "",
    "question": "Why does this print nothing even though the strings look the same?",
    "action_sequence": ["edit", "run"],
    "time_stuck": 45.0
  }'
```

You will get a JSON response with a personalized tutoring explanation.

---

## Troubleshooting

**"Ollama not reachable"**
Make sure you ran `ollama serve` in a separate terminal and it is still running.

**Server crashes on startup**
Check that you ran `python scripts/setup_java_knowledge.py` first.

**Slow responses**
Normal for CPU — llama3.1 takes 30-90 seconds per response on CPU.
Switch to llama3.2 for faster responses (slightly lower quality).

**ModuleNotFoundError**
Make sure your venv is activated before running uvicorn.

---

## Switching models

Edit `config.yaml`:

```yaml
ollama:
  model: "llama3.2"    # faster, 8GB RAM
  # model: "llama3.1"  # better quality, 16GB RAM
  # model: "mistral"   # alternative option
```

Then restart the server.

---

## What runs locally vs what needs internet

| Component | Runs locally | Needs internet |
|---|---|---|
| LLM response generation | ✅ Ollama | — |
| Three-channel analysis | ✅ regex | — |
| BKT mastery tracking | ✅ | — |
| Java pedagogical KG | ✅ | — |
| CSE-KG domain queries | — | ✅ SPARQL endpoint |
| Dataset downloads | — | ✅ first time only |

The system runs fully offline except for CSE-KG SPARQL queries
which are cached after first use.
