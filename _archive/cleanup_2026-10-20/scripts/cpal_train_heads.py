"""
Train the two "last layer" heads on top of frozen HVSAE latent:

  LPLevelHead       256 → 128 → 4    (L1, L2, L3, L4)
  WrongModelSubHead 256 → 128 → 60   (20 concepts × {A,B,C})

Training data is derived from the catalogue:
  LP examples  = rubric lines (80) + templated variants + optional Ollama paraphrases
  WM examples  = signals (180) + beliefs (60) + origins (60) + paraphrases

Each training text is encoded through the pretrained HVSAE (frozen) to
produce a 256-d latent vector, which is the input to the heads.

Saves:
  checkpoints/cpal_lp_head.pt
  checkpoints/cpal_wm_subhead.pt
"""
import os, sys, json, time, random
from pathlib import Path
from typing import List, Dict, Tuple

import numpy as np
import torch
import torch.nn as nn

ROOT = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, str(ROOT))

from src.models.hvsae import HVSAE

CATALOGUE_PATH = ROOT / "data" / "mental_models" / "wrong_models_catalogue.json"
CHECKPOINT_DIR = ROOT / "checkpoints"
LP_HEAD_PATH   = CHECKPOINT_DIR / "cpal_lp_head.pt"
WM_HEAD_PATH   = CHECKPOINT_DIR / "cpal_wm_subhead.pt"

LP_LEVELS    = ["L1", "L2", "L3", "L4"]
LP_LVL_TO_ID = {lvl: i for i, lvl in enumerate(LP_LEVELS)}

# Use Ollama paraphrase augmentation? Costs ~5 min but gives much more
# semantic diversity. Set to False for deterministic+fast training.
USE_OLLAMA_AUG = os.environ.get("CPAL_USE_OLLAMA", "0") == "1"
PARAPHRASES_PER_EXAMPLE = int(os.environ.get("CPAL_PARAPHRASES", "3"))
OLLAMA_URL = "http://localhost:11434/api/generate"
# Use llama3.2 (3B) for augmentation — 2-3x faster than qwen2.5-coder:7b
# and paraphrase quality is sufficient for training data.
OLLAMA_MODEL = os.environ.get("CPAL_OLLAMA_MODEL", "llama3.2:latest")


# ==========================================================================
# Step 1: load catalogue + HVSAE
# ==========================================================================
def load_hvsae():
    print("[1/5] Loading HVSAE from checkpoints/best.pt")
    ck = torch.load(CHECKPOINT_DIR / "best.pt", map_location="cpu",
                    weights_only=False)
    m = HVSAE(ck["config"])
    m.load_state_dict(ck["hvsae_state"])
    m.eval()
    for p in m.parameters():
        p.requires_grad = False  # FROZEN
    return m, ck["config"]


def load_catalogue():
    print("[1/5] Loading catalogue")
    with open(CATALOGUE_PATH, encoding="utf-8") as f:
        return json.load(f)


# ==========================================================================
# Step 2: build raw training pairs from catalogue
# ==========================================================================
def load_corpus_if_present(catalogue: dict):
    """If a student-voice corpus exists, use it. Returns the same
    (lp_ex, wm_ex, concepts, wm_labels) shape as build_examples but
    populated from the corpus file."""
    corpus_path = ROOT / "data" / "mental_models" / "training_corpus.json"
    if not corpus_path.exists():
        return None
    with open(corpus_path, encoding="utf-8") as f:
        corpus = json.load(f)
    concepts = sorted(catalogue["concepts"].keys())
    # Build wm_labels in the same order build_examples uses
    wm_labels = []
    for cid in concepts:
        for wm in catalogue["concepts"][cid].get("wrong_models", []):
            wm_labels.append((cid, wm["id"]))
    lp_ex = corpus.get("lp", [])
    wm_ex = corpus.get("wm", [])
    print(f"[2/5] Loaded student-voice corpus: "
          f"{len(lp_ex)} LP + {len(wm_ex)} WM examples")
    return lp_ex, wm_ex, concepts, wm_labels


def build_examples(catalogue: dict) -> Tuple[List[Dict], List[Dict],
                                              List[str], List[Tuple[str,str]]]:
    """Returns (lp_examples, wm_examples, concept_ids, wm_labels).

    lp_examples: list of {"text": str, "concept": str, "lp_level": "L1"..}
    wm_examples: list of {"text": str, "concept": str, "wm_id": "SE-A"..}
    concept_ids: sorted list of 20 concept ids
    wm_labels:   global label space for WM head: [(concept, wm_suffix),...]
                 e.g. [("type_mismatch","TM-A"), ("type_mismatch","TM-B"), ...]
    """
    concepts = sorted(catalogue["concepts"].keys())

    lp_ex: List[Dict] = []
    wm_ex: List[Dict] = []
    wm_labels: List[Tuple[str, str]] = []

    for cid in concepts:
        entry = catalogue["concepts"][cid]
        # LP: rubric lines
        for lvl, text in entry.get("lp_rubric", {}).items():
            if lvl in LP_LVL_TO_ID and text:
                lp_ex.append({"text": text, "concept": cid, "lp_level": lvl})

        # WM: for each wrong model, every signal + belief + origin
        for wm in entry.get("wrong_models", []):
            wm_full_id = wm["id"]  # e.g. "TM-A"
            wm_labels.append((cid, wm_full_id))
            for sig in wm.get("conversation_signals", []):
                wm_ex.append({"text": sig, "concept": cid, "wm_id": wm_full_id})
            if wm.get("wrong_belief"):
                wm_ex.append({"text": wm["wrong_belief"], "concept": cid,
                              "wm_id": wm_full_id})
            if wm.get("origin"):
                wm_ex.append({"text": wm["origin"], "concept": cid,
                              "wm_id": wm_full_id})

    # De-duplicate wm_labels preserving order
    seen = set(); uniq = []
    for t in wm_labels:
        if t not in seen:
            seen.add(t); uniq.append(t)
    return lp_ex, wm_ex, concepts, uniq


# ==========================================================================
# Step 3: augment via Ollama (optional — can skip for fast training)
# ==========================================================================
def ollama_paraphrase(text: str, n: int = 3, timeout: float = 25.0) -> List[str]:
    import requests
    prompt = (
        f"Generate {n} different ways a student might say the following, "
        f"each expressing the same misconception or LP-level understanding "
        f"using varied vocabulary. Output ONE paraphrase per line, no "
        f"numbering, no quotes, no explanation.\n\n"
        f"Original: {text}\n\nParaphrases:"
    )
    try:
        r = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt,
                  "stream": False,
                  "options": {"temperature": 0.8,
                              "num_predict": int(os.environ.get("CPAL_NUM_PREDICT", "80"))}},
            timeout=timeout,
        )
        r.raise_for_status()
        out = r.json().get("response", "")
        lines = [l.strip("-• \t") for l in out.splitlines() if l.strip()]
        # Filter: paraphrases should be sentences of reasonable length
        lines = [l for l in lines if 6 < len(l) < 200 and l[0].isalpha()]
        return lines[:n]
    except Exception:
        return []


def augment(examples: List[Dict], label_key: str, n: int) -> List[Dict]:
    if not USE_OLLAMA_AUG or n <= 0:
        return examples
    cache_path = ROOT / "data" / "mental_models" / f"paraphrase_cache_{label_key}.json"
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache = {}
    if cache_path.exists():
        with open(cache_path, encoding="utf-8") as f:
            cache = json.load(f)
        print(f"[2/5] loaded {len(cache)} cached paraphrases from {cache_path.name}")

    print(f"[2/5] Ollama-augmenting {len(examples)} {label_key} examples "
          f"({n} paraphrases each, model={OLLAMA_MODEL})")
    out: List[Dict] = list(examples)  # keep originals
    start = time.time()
    changed = 0
    for i, ex in enumerate(examples, 1):
        key = ex["text"][:200]
        if key in cache:
            paras = cache[key]
        else:
            paras = ollama_paraphrase(ex["text"], n=n)
            cache[key] = paras
            changed += 1
            if changed % 10 == 0:
                with open(cache_path, "w", encoding="utf-8") as f:
                    json.dump(cache, f, indent=1)
        for p in paras:
            new_ex = dict(ex); new_ex["text"] = p; new_ex["synthetic"] = True
            out.append(new_ex)
        if i % 20 == 0 or i == len(examples):
            pct = 100 * i / len(examples)
            elapsed = time.time() - start
            print(f"    augment {label_key} [{i}/{len(examples)}] {pct:.0f}%  "
                  f"elapsed={elapsed:.0f}s  new_total={len(out)}", flush=True)
    # Final cache save
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=1)
    return out


# ==========================================================================
# Step 4: encode examples via HVSAE → feature matrix
# ==========================================================================
def build_tokenizer():
    try:
        from transformers import AutoTokenizer
        return AutoTokenizer.from_pretrained("bert-base-uncased")
    except Exception:
        return None


def encode_texts(hvsae: HVSAE, texts: List[str], tok, text_vocab: int = 6000,
                 max_len: int = 64) -> torch.Tensor:
    feats = []
    for t in texts:
        t = (t or "").strip() or "empty"
        if tok is not None:
            ids = tok(t, return_tensors="pt", padding=True, truncation=True,
                      max_length=max_len)["input_ids"].long() % text_vocab
        else:
            words = t.lower().split()[:max_len]
            ids = torch.tensor(
                [[abs(hash(w)) % text_vocab for w in words]], dtype=torch.long)
        batch = {"code_tokens": torch.zeros(1, 10, dtype=torch.long),
                 "text_tokens": ids,
                 "action_sequence": torch.ones(1, 8, dtype=torch.long)}
        with torch.no_grad():
            out = hvsae.forward(batch, compute_graph=False)
        feats.append(out["latent"].squeeze(0))
    return torch.stack(feats)  # (N, 256)


# ==========================================================================
# Step 5: define + train heads
# ==========================================================================
class MLPHead(nn.Module):
    def __init__(self, in_dim: int, hidden: int, num_classes: int, dropout=0.3):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, hidden), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden, hidden // 2), nn.ReLU(), nn.Dropout(dropout),
            nn.Linear(hidden // 2, num_classes),
        )

    def forward(self, x): return self.net(x)


def train_head(feats: torch.Tensor, labels: torch.Tensor, num_classes: int,
               tag: str, epochs: int = 60, batch: int = 64, lr: float = 1e-3,
               weight_decay: float = 1e-4, val_frac: float = 0.15) -> nn.Module:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    feats  = feats.to(device)
    labels = labels.to(device)
    rng = torch.Generator().manual_seed(42)
    n = feats.size(0)
    perm = torch.randperm(n, generator=rng)
    n_val = max(1, int(n * val_frac))
    val_idx, train_idx = perm[:n_val], perm[n_val:]

    head = MLPHead(feats.size(1), 128, num_classes).to(device)
    opt = torch.optim.Adam(head.parameters(), lr=lr, weight_decay=weight_decay)
    print(f"    training on device: {device}")
    loss_fn = nn.CrossEntropyLoss()
    best_val = 0.0
    best_state = None
    print(f"[4/5] Training {tag} head  "
          f"(n={n}, train={len(train_idx)}, val={len(val_idx)}, "
          f"classes={num_classes})")
    for ep in range(1, epochs + 1):
        head.train()
        shuffled = train_idx[torch.randperm(len(train_idx), generator=rng)]
        total_loss = 0.0; total_correct = 0
        for i in range(0, len(shuffled), batch):
            idx = shuffled[i:i + batch]
            x, y = feats[idx], labels[idx]
            logits = head(x)
            loss = loss_fn(logits, y)
            opt.zero_grad(); loss.backward(); opt.step()
            total_loss += loss.item() * len(idx)
            total_correct += (logits.argmax(dim=-1) == y).sum().item()
        train_acc = total_correct / len(shuffled)
        # Validation
        head.eval()
        with torch.no_grad():
            vlog = head(feats[val_idx])
            val_acc = (vlog.argmax(dim=-1) == labels[val_idx]).float().mean().item()
        if ep % 10 == 0 or ep == 1:
            print(f"    epoch {ep:3d}: loss={total_loss/len(shuffled):.3f}  "
                  f"train_acc={train_acc:.3f}  val_acc={val_acc:.3f}")
        if val_acc > best_val:
            best_val = val_acc
            best_state = {k: v.detach().clone() for k, v in head.state_dict().items()}
    print(f"    best val_acc={best_val:.3f}")
    if best_state is not None:
        head.load_state_dict(best_state)
    head = head.cpu()  # save on CPU so loader doesn't need CUDA
    return head


# ==========================================================================
# Main pipeline
# ==========================================================================
def main():
    hvsae, _cfg = load_hvsae()
    cat = load_catalogue()

    corpus = load_corpus_if_present(cat)
    if corpus is not None:
        lp_ex, wm_ex, concepts, wm_labels = corpus
    else:
        lp_ex, wm_ex, concepts, wm_labels = build_examples(cat)
        print(f"[2/5] Catalogue raw: {len(lp_ex)} LP examples, "
              f"{len(wm_ex)} WM examples, {len(wm_labels)} WM classes")
        lp_ex = augment(lp_ex, "LP", PARAPHRASES_PER_EXAMPLE)
        wm_ex = augment(wm_ex, "WM", PARAPHRASES_PER_EXAMPLE)
        print(f"[2/5] After augmentation: {len(lp_ex)} LP / {len(wm_ex)} WM")

    # Encode through frozen HVSAE
    print("[3/5] Encoding training texts via HVSAE (frozen)")
    tok = build_tokenizer()
    lp_texts = [e["text"] for e in lp_ex]
    wm_texts = [e["text"] for e in wm_ex]
    t0 = time.time()
    lp_feats = encode_texts(hvsae, lp_texts, tok)
    wm_feats = encode_texts(hvsae, wm_texts, tok)
    print(f"    encoded {len(lp_ex)+len(wm_ex)} texts in {time.time()-t0:.1f}s  "
          f"lp_feats={tuple(lp_feats.shape)}  wm_feats={tuple(wm_feats.shape)}")

    lp_labels = torch.tensor([LP_LVL_TO_ID[e["lp_level"]] for e in lp_ex],
                             dtype=torch.long)
    wm_label_to_id = {t: i for i, t in enumerate(wm_labels)}
    wm_y = torch.tensor(
        [wm_label_to_id[(e["concept"], e["wm_id"])] for e in wm_ex],
        dtype=torch.long,
    )

    # Train heads
    lp_head = train_head(lp_feats, lp_labels, num_classes=4, tag="LP")
    wm_head = train_head(wm_feats, wm_y, num_classes=len(wm_labels),
                         tag="WM", epochs=80)

    # Save
    print("[5/5] Saving head checkpoints")
    torch.save({
        "state_dict": lp_head.state_dict(),
        "in_dim":     lp_feats.size(1),
        "num_classes": 4,
        "labels":     LP_LEVELS,
        "num_examples": len(lp_ex),
    }, LP_HEAD_PATH)
    torch.save({
        "state_dict": wm_head.state_dict(),
        "in_dim":     wm_feats.size(1),
        "num_classes": len(wm_labels),
        "labels":     wm_labels,              # list of (concept, wm_id)
        "concepts":   concepts,
        "num_examples": len(wm_ex),
    }, WM_HEAD_PATH)
    print(f"    saved:")
    print(f"      {LP_HEAD_PATH}   ({LP_HEAD_PATH.stat().st_size/1024:.1f} KB)")
    print(f"      {WM_HEAD_PATH}   ({WM_HEAD_PATH.stat().st_size/1024:.1f} KB)")
    print("Done.")


if __name__ == "__main__":
    main()
