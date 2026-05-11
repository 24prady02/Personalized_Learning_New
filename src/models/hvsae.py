"""
HVSAE — Hierarchical Variational Sequential Autoencoder
=========================================================
Encodes three modalities simultaneously:
  1. Code tokens       (pre-trained CodeBERT tokenizer → BiLSTM → latent)
  2. Text/question     (BERT tokenizer → BiLSTM → latent)
  3. Action sequence   (embedding → LSTM → latent)

All three streams are fused into a shared 256-dim latent vector z via a
Mixture-of-Experts (MoE) gating network.

Pre-training:
  - Code stream:   CodeNet (correct + buggy Java submissions)
  - Text stream:   ProgSnap2 student messages
  - Action stream: ProgSnap2 action sequences

The fallback (Fix 2 in orchestrator) uses real feature extraction when
this model has not been trained yet.  Once trained on CodeNet + ProgSnap2,
load the checkpoint and this model replaces the fallback automatically.

Training:
    from src.models.hvsae import HVSAE
    model = HVSAE(config)
    # Train via src/train.py with CodeNet + ProgSnap2 dataloaders
    # Save checkpoint to checkpoints/hvsae_best.pt
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Optional, Tuple


class CodeEncoder(nn.Module):
    """
    Encodes Java source code into a semantic embedding.
    Uses character-level tokenization as fallback when CodeBERT is unavailable.
    When CodeBERT is available (transformers installed + downloaded), swap in
    AutoModel.from_pretrained('microsoft/codebert-base').
    """

    VOCAB_SIZE = 8000   # Java token vocabulary
    EMBED_DIM  = 128
    HIDDEN_DIM = 256

    def __init__(self):
        super().__init__()
        self.embedding  = nn.Embedding(self.VOCAB_SIZE, self.EMBED_DIM, padding_idx=0)
        self.bilstm     = nn.LSTM(self.EMBED_DIM, self.HIDDEN_DIM // 2,
                                  num_layers=2, batch_first=True,
                                  bidirectional=True, dropout=0.2)
        self.projection = nn.Linear(self.HIDDEN_DIM, 128)
        self.dropout    = nn.Dropout(0.1)

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        """token_ids: (B, L)  →  out: (B, 128)"""
        x = self.dropout(self.embedding(token_ids))        # (B,L,128)
        _, (h, _) = self.bilstm(x)                        # h: (4,B,128)
        # cat forward + backward final hidden
        h_cat = torch.cat([h[-2], h[-1]], dim=-1)          # (B,256)
        return F.relu(self.projection(h_cat))              # (B,128)


class TextEncoder(nn.Module):
    """Encodes student question/error text."""

    VOCAB_SIZE = 6000
    EMBED_DIM  = 128
    HIDDEN_DIM = 256

    def __init__(self):
        super().__init__()
        self.embedding  = nn.Embedding(self.VOCAB_SIZE, self.EMBED_DIM, padding_idx=0)
        self.bilstm     = nn.LSTM(self.EMBED_DIM, self.HIDDEN_DIM // 2,
                                  num_layers=2, batch_first=True,
                                  bidirectional=True, dropout=0.2)
        self.projection = nn.Linear(self.HIDDEN_DIM, 128)
        self.dropout    = nn.Dropout(0.1)

    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        x = self.dropout(self.embedding(token_ids))
        _, (h, _) = self.bilstm(x)
        h_cat = torch.cat([h[-2], h[-1]], dim=-1)
        return F.relu(self.projection(h_cat))


class ActionEncoder(nn.Module):
    """Encodes debugging action sequences (from ProgSnap2 event types)."""

    NUM_ACTIONS = 20   # run, compile_error, edit, search, submit, …
    EMBED_DIM   = 32
    HIDDEN_DIM  = 64

    def __init__(self):
        super().__init__()
        self.embedding = nn.Embedding(self.NUM_ACTIONS, self.EMBED_DIM, padding_idx=0)
        self.lstm      = nn.LSTM(self.EMBED_DIM, self.HIDDEN_DIM,
                                 num_layers=1, batch_first=True)
        self.projection = nn.Linear(self.HIDDEN_DIM, 64)

    def forward(self, action_ids: torch.Tensor) -> torch.Tensor:
        """action_ids: (B, T)  →  out: (B, 64)"""
        x = self.embedding(action_ids)
        _, (h, _) = self.lstm(x)
        return F.relu(self.projection(h.squeeze(0)))


class FusionGating(nn.Module):
    """
    Mixture-of-Experts gating that weights three stream embeddings.
    Learns which modality is most informative for each sample.
    """

    def __init__(self, stream_dim: int = 128 + 128 + 64):
        super().__init__()
        self.gate = nn.Sequential(
            nn.Linear(stream_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 3),   # 3 experts: code, text, action
            nn.Softmax(dim=-1)
        )
        # Project each stream to same dim before fusion
        self.proj_code   = nn.Linear(128, 256)
        self.proj_text   = nn.Linear(128, 256)
        self.proj_action = nn.Linear(64,  256)

    def forward(self, code_emb: torch.Tensor,
                text_emb: torch.Tensor,
                action_emb: torch.Tensor) -> torch.Tensor:
        combined = torch.cat([code_emb, text_emb, action_emb], dim=-1)
        weights  = self.gate(combined)                     # (B,3)
        c = self.proj_code(code_emb)                       # (B,256)
        t = self.proj_text(text_emb)                       # (B,256)
        a = self.proj_action(action_emb)                   # (B,256)
        fused = (weights[:, 0:1] * c +
                 weights[:, 1:2] * t +
                 weights[:, 2:3] * a)                      # (B,256)
        return fused


class VariationalBottleneck(nn.Module):
    """VAE-style reparameterisation for latent space regularisation."""

    def __init__(self, input_dim: int = 256, latent_dim: int = 256):
        super().__init__()
        self.mu_layer  = nn.Linear(input_dim, latent_dim)
        self.log_var   = nn.Linear(input_dim, latent_dim)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        mu      = self.mu_layer(x)
        log_var = self.log_var(x)
        std     = torch.exp(0.5 * log_var)
        eps     = torch.randn_like(std)
        z       = mu + eps * std                           # reparameterisation
        return z, mu, log_var


class MisconceptionHead(nn.Module):
    """
    Auxiliary output head — predicts which of the 20 Java misconceptions
    is most likely given the latent z.  Trained with soft labels derived
    from the Java concept keyword matching during pre-training.
    """

    def __init__(self, latent_dim: int = 256, num_concepts: int = 20):
        super().__init__()
        self.head = nn.Sequential(
            nn.Linear(latent_dim, 64),
            nn.ReLU(),
            nn.Linear(64, num_concepts)
        )

    def forward(self, z: torch.Tensor) -> torch.Tensor:
        return self.head(z)          # (B, 20) logits


class HVSAE(nn.Module):
    """
    Full HVSAE model.

    Forward pass returns a dict with:
      latent          (B,256)  — fused variational latent
      mu              (B,256)  — VAE mean
      log_var         (B,256)  — VAE log-variance (for KL loss)
      attention_weights (B,3)  — gating weights per modality
      misconception_logits (B,20) — Java concept probability logits

    Training loss (in src/train.py):
      L = reconstruction_loss + beta * KL_loss + concept_cross_entropy
    """

    def __init__(self, config: Dict):
        super().__init__()
        self.config       = config
        self.code_encoder  = CodeEncoder()
        self.text_encoder  = TextEncoder()
        self.action_encoder = ActionEncoder()
        self.fusion        = FusionGating()
        self.variational   = VariationalBottleneck()
        self.misconception = MisconceptionHead()
        self._beta         = config.get('hvsae', {}).get('beta', 0.1)  # KL weight

    def forward(self, batch: Dict, compute_graph: bool = False) -> Dict:
        """
        batch keys (all optional — zeros used for missing):
          code_tokens    (B, L_code)
          text_tokens    (B, L_text)
          action_sequence (B, T)
        """
        B = 1   # default batch size

        # ── Code stream ───────────────────────────────────────────────
        code_ids = batch.get('code_tokens')
        if code_ids is None or code_ids.numel() == 0:
            code_emb = torch.zeros(B, 128)
        else:
            code_emb = self.code_encoder(code_ids)

        # ── Text stream ───────────────────────────────────────────────
        text_ids = batch.get('text_tokens')
        if text_ids is None or text_ids.numel() == 0:
            text_emb = torch.zeros(B, 128)
        else:
            text_emb = self.text_encoder(text_ids)

        # ── Action stream ─────────────────────────────────────────────
        action_ids = batch.get('action_sequence')
        if action_ids is None or action_ids.numel() == 0:
            action_emb = torch.zeros(B, 64)
        else:
            action_emb = self.action_encoder(action_ids)

        # ── Fusion ────────────────────────────────────────────────────
        fused = self.fusion(code_emb, text_emb, action_emb)   # (B,256)

        # ── Variational bottleneck ────────────────────────────────────
        z, mu, log_var = self.variational(fused)

        # ── Misconception head ────────────────────────────────────────
        misconception_logits = self.misconception(z)

        # Gating weights for interpretability
        combined = torch.cat([code_emb, text_emb, action_emb], dim=-1)
        attn = self.fusion.gate(combined)                     # (B,3)

        return {
            'latent':               z,
            'mu':                   mu,
            'log_var':              log_var,
            'attention_weights':    attn,
            'misconception_logits': misconception_logits,
        }

    def compute_loss(self, batch: Dict, concept_labels: Optional[torch.Tensor] = None) -> Dict:
        """
        Full training loss:
          KL divergence + concept cross-entropy
        Returns dict with individual loss components.
        """
        out = self.forward(batch)
        mu, log_var = out['mu'], out['log_var']

        # KL divergence
        kl_loss = -0.5 * torch.mean(1 + log_var - mu.pow(2) - log_var.exp())

        # Concept supervision (if labels available)
        concept_loss = torch.tensor(0.0)
        if concept_labels is not None:
            concept_loss = F.cross_entropy(out['misconception_logits'], concept_labels)

        total = self._beta * kl_loss + concept_loss
        return {
            'total':        total,
            'kl':           kl_loss,
            'concept':      concept_loss,
            'latent':       out['latent'],
        }

    def tokenize_code(self, code: str, max_len: int = 128) -> torch.Tensor:
        """Simple character-level tokenizer for code. Replace with CodeBERT tokenizer after install."""
        tokens = [ord(c) % CodeEncoder.VOCAB_SIZE for c in code[:max_len]]
        tokens += [0] * (max_len - len(tokens))
        return torch.tensor([tokens], dtype=torch.long)

    def tokenize_text(self, text: str, max_len: int = 64) -> torch.Tensor:
        """Simple word-level tokenizer. Replace with BERT tokenizer after install."""
        words  = text.lower().split()[:max_len]
        tokens = [hash(w) % TextEncoder.VOCAB_SIZE for w in words]
        tokens += [0] * (max_len - len(tokens))
        return torch.tensor([tokens], dtype=torch.long)
