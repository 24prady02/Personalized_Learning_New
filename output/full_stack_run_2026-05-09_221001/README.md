# Full-stack run summary

- Stamp: 2026-05-09_221001
- Target concept: null_pointer
- Ollama model: qwen2.5-coder:7b
- Generation: TTFT=12.889677047729492s, total=53.50973582267761s, 2428 chars
- Wrong-model matched: NP-C
- LP level: L1 -> L2

## Files
- transcript.txt   -- full stdout (every component step + Ollama stream)
- prompt.txt       -- the assembled Ollama prompt (~7k chars)
- response.md      -- the final LLM response
- diagnostic.json  -- structured per-component outputs + lp_diagnostic