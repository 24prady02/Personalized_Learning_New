"""
src/data/dataloader.py
======================
PyTorch Dataset and DataLoader for CPAL training.

create_dataloaders(config, train_df, val_df, test_df)
  → {'train': DataLoader, 'val': DataLoader, 'test': DataLoader}

Batch keys produced (all tensors on CPU, moved to device by Trainer._to_device):
  code_tokens       LongTensor  (B, max_code_len)
  text_tokens       LongTensor  (B, max_text_len)
  action_sequence   LongTensor  (B, max_seq_len)
  timestamps        FloatTensor (B, max_seq_len, 1)
  sequence_lengths  LongTensor  (B,)
  is_correct        FloatTensor (B,)
  emotion_label     LongTensor  (B,)   — -1 for unlabelled samples
  concept_label     LongTensor  (B,)   — -1 for unlabelled samples
  student_ids       list[str]
  problem_ids       list[str]
"""

import re
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader, Dataset

from src.models.behavioral import ACTION_MAP, NUM_ACTIONS
from src.orchestrator.student_state_tracker import CONCEPT_KEYWORDS

# ── Concept → integer label ────────────────────────────────────────────────────
CONCEPT_LABELS: Dict[str, int] = {c: i for i, c in enumerate(CONCEPT_KEYWORDS.keys())}
NUM_CONCEPTS = len(CONCEPT_LABELS)


# ── Simple tokenizers ─────────────────────────────────────────────────────────

_SPLIT_RE = re.compile(r'\W+')

def _tokenize_code(text: str, vocab_size: int = 8000, max_len: int = 128) -> List[int]:
    """Character-level tokenizer for Java/Python code."""
    tokens = [ord(c) % vocab_size for c in str(text)[:max_len]]
    return tokens

def _tokenize_text(text: str, vocab_size: int = 6000, max_len: int = 64) -> List[int]:
    """Word-level tokenizer for natural language."""
    words = _SPLIT_RE.split(str(text).lower())[:max_len]
    return [hash(w) % vocab_size for w in words if w]


# ── Dataset ────────────────────────────────────────────────────────────────────

class PLSDataset(Dataset):
    """
    PyTorch Dataset wrapping a pandas DataFrame.

    Tokenises code and text on the fly (no pre-computed token files needed).
    Action sequences are mapped to integer IDs via ACTION_MAP.
    """

    def __init__(self, df: pd.DataFrame, config: Dict):
        self.df          = df.reset_index(drop=True)
        self.max_code    = config.get('hvsae', {}).get('max_code_len', 128)
        self.max_text    = config.get('hvsae', {}).get('max_text_len', 64)
        self.max_seq     = config.get('behavioral', {}).get('max_sequence_len', 50)
        self.code_vocab  = config.get('hvsae', {}).get('code_vocab_size', 8000)
        self.text_vocab  = config.get('hvsae', {}).get('text_vocab_size', 6000)

    def __len__(self) -> int:
        return len(self.df)

    def __getitem__(self, idx: int) -> Dict:
        row = self.df.iloc[idx]

        # ── Code tokens ───────────────────────────────────────────────────────
        code_toks = _tokenize_code(
            row.get('code', ''), self.code_vocab, self.max_code
        )

        # ── Text tokens (question or error) ───────────────────────────────────
        text_src  = str(row.get('question', row.get('error_message', '')))
        text_toks = _tokenize_text(text_src, self.text_vocab, self.max_text)

        # ── Action sequence ───────────────────────────────────────────────────
        raw_actions = row.get('actions', [])
        if isinstance(raw_actions, str):
            try:
                raw_actions = eval(raw_actions)
            except Exception:
                raw_actions = []
        if not isinstance(raw_actions, (list, tuple)):
            raw_actions = []
        action_ids = [ACTION_MAP.get(str(a).lower(), 4) for a in raw_actions][:self.max_seq]
        seq_len    = len(action_ids)

        # ── Time deltas ───────────────────────────────────────────────────────
        raw_deltas = row.get('time_deltas', [])
        if isinstance(raw_deltas, str):
            try:
                raw_deltas = eval(raw_deltas)
            except Exception:
                raw_deltas = []
        if not isinstance(raw_deltas, (list, tuple)):
            raw_deltas = []
        deltas = []
        for d in raw_deltas[:self.max_seq]:
            try:
                deltas.append(float(d) / 300.0)
            except (TypeError, ValueError):
                deltas.append(0.0)

        # Pad to max_seq
        code_toks  += [0] * (self.max_code - len(code_toks))
        text_toks  += [0] * (self.max_text - len(text_toks))
        action_ids += [0] * (self.max_seq  - len(action_ids))
        deltas     += [0.0] * (self.max_seq - len(deltas))

        # ── Labels ────────────────────────────────────────────────────────────
        is_correct    = float(row.get('is_correct', 0))

        emotion_raw   = row.get('emotion_label', -1)
        emotion_label = int(emotion_raw) if emotion_raw is not None else -1

        concept_str   = str(row.get('concept', ''))
        concept_label = CONCEPT_LABELS.get(concept_str, -1)

        # Ensure fixed-shape tensors: timestamps must be [max_seq, 1]
        code_toks  = code_toks[:self.max_code]
        text_toks  = text_toks[:self.max_text]
        action_ids = action_ids[:self.max_seq]
        deltas     = deltas[:self.max_seq]
        ts_tensor  = torch.zeros(self.max_seq, 1, dtype=torch.float)
        for i, d in enumerate(deltas):
            ts_tensor[i, 0] = float(d)

        return {
            'code_tokens':      torch.tensor(code_toks,  dtype=torch.long),
            'text_tokens':      torch.tensor(text_toks,  dtype=torch.long),
            'action_sequence':  torch.tensor(action_ids, dtype=torch.long),
            'timestamps':       ts_tensor,
            'sequence_lengths': torch.tensor(max(seq_len, 1), dtype=torch.long),
            'is_correct':       torch.tensor(is_correct,    dtype=torch.float),
            'emotion_label':    torch.tensor(emotion_label, dtype=torch.long),
            'concept_label':    torch.tensor(concept_label, dtype=torch.long),
            'student_id':       str(row.get('student_id', 'unknown')),
            'problem_id':       str(row.get('problem_id', 'unknown')),
        }


def _collate_fn(batch: List[Dict]) -> Dict:
    """
    Custom collate — stacks tensors, collects string lists.
    Handles variable-length sequence_lengths correctly.
    """
    tensor_keys = [
        'code_tokens', 'text_tokens', 'action_sequence',
        'timestamps', 'is_correct', 'emotion_label', 'concept_label',
    ]
    result = {}
    for key in tensor_keys:
        result[key] = torch.stack([item[key] for item in batch])

    # sequence_lengths: stack scalar tensors into 1-D
    result['sequence_lengths'] = torch.stack(
        [item['sequence_lengths'] for item in batch]
    )

    # String lists
    result['student_ids'] = [item['student_id'] for item in batch]
    result['problem_ids'] = [item['problem_id'] for item in batch]

    return result


# ── Public API ────────────────────────────────────────────────────────────────

def create_dataloaders(
    config: Dict,
    train_df: pd.DataFrame,
    val_df:   pd.DataFrame,
    test_df:  Optional[pd.DataFrame] = None,
) -> Dict[str, DataLoader]:
    """
    Create train / val / (optional) test DataLoaders from DataFrames.

    Args:
        config:   full system config dict (from config.yaml)
        train_df: training data DataFrame
        val_df:   validation data DataFrame
        test_df:  test data DataFrame (optional)

    Returns:
        dict with keys 'train', 'val', and optionally 'test'.
    """
    batch_size   = config.get('training', {}).get('batch_size', 32)
    num_workers  = config.get('training', {}).get('num_workers', 0)

    loaders = {}

    if len(train_df) > 0:
        train_ds = PLSDataset(train_df, config)
        loaders['train'] = DataLoader(
            train_ds,
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
            collate_fn=_collate_fn,
            drop_last=len(train_ds) > batch_size,   # avoid single-sample batches
        )
        print(f"[DataLoader] train: {len(train_ds)} samples, "
              f"{len(loaders['train'])} batches (bs={batch_size})")

    if len(val_df) > 0:
        val_ds = PLSDataset(val_df, config)
        loaders['val'] = DataLoader(
            val_ds,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
            collate_fn=_collate_fn,
        )
        print(f"[DataLoader] val:   {len(val_ds)} samples, "
              f"{len(loaders['val'])} batches")

    if test_df is not None and len(test_df) > 0:
        test_ds = PLSDataset(test_df, config)
        loaders['test'] = DataLoader(
            test_ds,
            batch_size=batch_size,
            shuffle=False,
            num_workers=num_workers,
            collate_fn=_collate_fn,
        )
        print(f"[DataLoader] test:  {len(test_ds)} samples, "
              f"{len(loaders['test'])} batches")

    return loaders
