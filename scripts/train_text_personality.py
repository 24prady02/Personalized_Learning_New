"""
Train a text -> Big Five classifier on the Pennebaker Essays dataset.
V2: fine-tune the encoder end-to-end (not just a frozen head). Prior frozen-
head version collapsed to ~0.5 predictions (F1 below majority-class baseline);
unfreezing gives the model capacity to pick up Big-Five signals in text.

Strategy:
  - Use MiniLM-L6-v2 (22M params) as a fine-tunable encoder.
  - Mean-pool token embeddings, then 384 -> 256 -> 5 head.
  - Single-encode each essay (truncate to 256 tokens, no chunk averaging —
    that was destroying long-range signal).
  - Lower LR for encoder (2e-5), higher LR for head (1e-3).
  - BCE with 5 traits, sigmoid output, 8 epochs with AMP for speed.

Outputs:
  checkpoints/text_personality.pt
  keys: encoder_name, encoder_state_dict, head_state_dict,
        in_dim, hidden, traits_*, mean_f1
"""
import sys, os, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "3")

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
ESSAYS = Path("data/personality_text/essays.csv")
CKPT = Path("checkpoints/text_personality.pt")
ENCODER_NAME = "sentence-transformers/all-MiniLM-L6-v2"
TRAITS = ["cOPN", "cCON", "cEXT", "cAGR", "cNEU"]
NAMES  = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]


class EssaysDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=256):
        self.texts = texts
        self.labels = labels
        self.tok = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        enc = self.tok(self.texts[idx], truncation=True, max_length=self.max_len,
                       padding="max_length", return_tensors="pt")
        return {
            "input_ids": enc["input_ids"].squeeze(0),
            "attention_mask": enc["attention_mask"].squeeze(0),
            "labels": torch.from_numpy(self.labels[idx]),
        }


class Big5Model(nn.Module):
    def __init__(self, encoder, hidden=256, n_out=5):
        super().__init__()
        self.encoder = encoder
        h_in = encoder.config.hidden_size
        self.head = nn.Sequential(
            nn.Linear(h_in, hidden), nn.GELU(),
            nn.Dropout(0.2),
            nn.Linear(hidden, n_out),
        )

    def forward(self, input_ids, attention_mask):
        out = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        # mean-pool non-pad tokens
        last = out.last_hidden_state  # (B, T, H)
        mask = attention_mask.unsqueeze(-1).float()
        pooled = (last * mask).sum(1) / mask.sum(1).clamp(min=1)
        return self.head(pooled)


def main():
    print(f"[Text-Big5] loading {ESSAYS}")
    df = pd.read_csv(ESSAYS, encoding="latin-1", on_bad_lines="skip")
    texts = df["TEXT"].astype(str).tolist()
    y = np.stack([(df[t] == "y").astype(np.float32).values for t in TRAITS], axis=1)
    print(f"[Text-Big5] {len(texts)} essays, label means: "
          f"{ {NAMES[i]: float(y[:, i].mean()) for i in range(5)} }")

    from transformers import AutoTokenizer, AutoModel
    print(f"[Text-Big5] loading {ENCODER_NAME}")
    tok = AutoTokenizer.from_pretrained(ENCODER_NAME)
    encoder = AutoModel.from_pretrained(ENCODER_NAME)
    model = Big5Model(encoder, hidden=256).to(DEVICE)

    rng = np.random.default_rng(0)
    idx = rng.permutation(len(texts))
    split = int(0.85 * len(texts))
    tr_idx, va_idx = idx[:split], idx[split:]

    tr_ds = EssaysDataset([texts[i] for i in tr_idx], y[tr_idx], tok)
    va_ds = EssaysDataset([texts[i] for i in va_idx], y[va_idx], tok)
    tr_dl = DataLoader(tr_ds, batch_size=16, shuffle=True, num_workers=0)
    va_dl = DataLoader(va_ds, batch_size=32, shuffle=False, num_workers=0)

    # two LR groups: low for encoder, high for head
    opt = optim.AdamW([
        {"params": model.encoder.parameters(), "lr": 2e-5},
        {"params": model.head.parameters(),    "lr": 1e-3},
    ], weight_decay=1e-4)
    loss_fn = nn.BCEWithLogitsLoss()
    scaler = torch.amp.GradScaler(DEVICE) if DEVICE == "cuda" else None

    print(f"[Text-Big5] training on {DEVICE}  |  {len(tr_idx)} train, {len(va_idx)} val")
    best_f1 = 0.0
    best_state = None
    for ep in range(8):
        t0 = time.time()
        model.train()
        losses = []
        for batch in tr_dl:
            batch = {k: v.to(DEVICE) for k, v in batch.items()}
            opt.zero_grad()
            if scaler is not None:
                with torch.amp.autocast("cuda"):
                    logits = model(batch["input_ids"], batch["attention_mask"])
                    loss = loss_fn(logits, batch["labels"])
                scaler.scale(loss).backward()
                scaler.unscale_(opt)
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                scaler.step(opt)
                scaler.update()
            else:
                logits = model(batch["input_ids"], batch["attention_mask"])
                loss = loss_fn(logits, batch["labels"])
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                opt.step()
            losses.append(loss.item())

        model.eval()
        with torch.no_grad():
            ps, ys = [], []
            for batch in va_dl:
                batch_dev = {k: v.to(DEVICE) for k, v in batch.items()}
                logits = model(batch_dev["input_ids"], batch_dev["attention_mask"])
                ps.append(torch.sigmoid(logits).cpu().numpy())
                ys.append(batch["labels"].numpy())
            P = np.concatenate(ps)
            Y = np.concatenate(ys)

        acc = ((P >= 0.5) == (Y >= 0.5)).mean(axis=0)
        f1s = []
        for t in range(5):
            tp = ((P[:, t] >= 0.5) & (Y[:, t] >= 0.5)).sum()
            fp = ((P[:, t] >= 0.5) & (Y[:, t] < 0.5)).sum()
            fn = ((P[:, t] < 0.5) & (Y[:, t] >= 0.5)).sum()
            prec = tp / max(tp+fp, 1)
            rec  = tp / max(tp+fn, 1)
            f1 = 2*prec*rec / max(prec+rec, 1e-6)
            f1s.append(f1)
        mean_f1 = float(np.mean(f1s))
        if mean_f1 > best_f1:
            best_f1 = mean_f1
            best_state = {
                "encoder": {k: v.detach().cpu().clone() for k, v in model.encoder.state_dict().items()},
                "head":    {k: v.detach().cpu().clone() for k, v in model.head.state_dict().items()},
            }
        pred_mean = P.mean(axis=0)
        pred_std  = P.std(axis=0)
        print(f"  ep {ep+1}  loss={np.mean(losses):.4f}  "
              f"val_acc=[{' '.join(f'{NAMES[i][:3]}:{acc[i]:.2f}' for i in range(5))}]  "
              f"F1=[{' '.join(f'{NAMES[i][:3]}:{f1s[i]:.2f}' for i in range(5))}]  "
              f"mean_F1={mean_f1:.3f}  "
              f"pred_std={np.mean(pred_std):.3f}  "
              f"t={time.time()-t0:.0f}s")

    print(f"[Text-Big5] best mean F1 = {best_f1:.3f}")
    CKPT.parent.mkdir(parents=True, exist_ok=True)
    torch.save({
        "encoder_name":         ENCODER_NAME,
        "encoder_state_dict":   best_state["encoder"],
        "head_state_dict":      best_state["head"],
        "in_dim":               model.encoder.config.hidden_size,
        "hidden":               256,
        "traits_col_names":     TRAITS,
        "traits_bigfive_names": NAMES,
        "dataset":              "pennebaker_essays_2467",
        "mean_f1":              best_f1,
        "format_version":       2,
    }, CKPT)
    print(f"[Text-Big5] saved {CKPT}  ({CKPT.stat().st_size/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
