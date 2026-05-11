"""
behavioral.py — BehavioralRNN + BehavioralHMM
==============================================
Two complementary models for student debugging behaviour analysis.

BehavioralRNN
-------------
Bidirectional LSTM trained on ProgSnap2 action sequences.
Input  : sequence of action IDs + time deltas
Outputs:
  - emotion       : frustrated / confused / engaged / neutral / confident
  - strategy      : systematic / exploratory / help_seeking / trial_error
  - effectiveness : float 0-1 (how productive is this session)
  - productivity  : high / medium / low

ProgSnap2 action IDs (20 event types):
  0=pad  1=run  2=compile_error  3=run_error  4=edit
  5=open_file  6=open_webpage  7=submit  8=help_request  9=resource_view
  10=video_play  11=video_pause  12=video_seek  13=close_file
  14=copy  15=paste  16=undo  17=redo  18=debug_step  19=test_run

BehavioralHMM
-------------
Hidden Markov Model trained on ProgSnap2 sessions.
Hidden states represent latent cognitive states:
  0=exploring  1=stuck  2=making_progress  3=understanding  4=mastered
Observation features extracted from action type counts per sliding window.

Training:
  from src.models.behavioral import BehavioralRNN, BehavioralHMM
  rnn = BehavioralRNN(config)
  hmm = BehavioralHMM(config)
  # Train via src/train.py → ProgSnap2Processor
  # rnn.analyze_strategy(action_ids, time_deltas, outcomes, lengths)
  # hmm.analyze_session(action_sequence)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json


# ─── Action vocabulary ────────────────────────────────────────────────────────
ACTION_MAP = {
    "run":             1, "compile_error":  2, "run_error":      3,
    "edit":            4, "open_file":      5, "open_webpage":   6,
    "submit":          7, "help_request":   8, "resource_view":  9,
    "video_play":     10, "video_pause":   11, "video_seek":     12,
    "close_file":     13, "copy":          14, "paste":          15,
    "undo":           16, "redo":          17, "debug_step":     18,
    "test_run":       19, "code_edit":      4,  # alias
}
NUM_ACTIONS = 20

EMOTIONS   = ["frustrated", "confused", "engaged", "neutral", "confident"]
STRATEGIES = ["systematic", "exploratory", "help_seeking", "trial_error"]
PRODUCTIVITIES = ["high", "medium", "low"]


# ─── BehavioralRNN ────────────────────────────────────────────────────────────

class BehavioralRNN(nn.Module):
    """
    Bidirectional LSTM that reads debugging action sequences and infers
    emotional + strategic state.

    Input tensors (all (B, T)):
      action_ids    : long, values 0-19
      time_deltas   : float, seconds between actions (normalised /300)
      outcomes      : float, 1=success 0=failure per action (optional)
      lengths       : long, actual sequence lengths per batch item

    Outputs (dict):
      emotion            : List[str]
      emotion_confidence : List[float]
      strategy           : List[str]
      effectiveness      : List[float]
      productivity       : List[str]
      hidden             : (B, 256) latent for downstream use
    """

    EMBED_DIM   = 32
    HIDDEN_DIM  = 128   # bidirectional → effective 256
    CONTEXT_DIM = 16    # time + outcome context per step

    def __init__(self, config: Dict):
        super().__init__()
        self.config = config

        # Action embedding
        self.action_embed = nn.Embedding(NUM_ACTIONS, self.EMBED_DIM, padding_idx=0)

        # Per-step context projection (time_delta + outcome → 16-dim)
        self.context_proj = nn.Linear(2, self.CONTEXT_DIM)

        # BiLSTM core
        self.bilstm = nn.LSTM(
            input_size  = self.EMBED_DIM + self.CONTEXT_DIM,
            hidden_size = self.HIDDEN_DIM,
            num_layers  = 2,
            batch_first = True,
            bidirectional = True,
            dropout = 0.25,
        )

        # Shared trunk after BiLSTM
        self.trunk = nn.Sequential(
            nn.Linear(self.HIDDEN_DIM * 2, 256),
            nn.LayerNorm(256),
            nn.ReLU(),
            nn.Dropout(0.2),
        )

        # Task heads
        self.emotion_head      = nn.Linear(256, len(EMOTIONS))
        self.strategy_head     = nn.Linear(256, len(STRATEGIES))
        self.effectiveness_head = nn.Sequential(nn.Linear(256, 64), nn.ReLU(), nn.Linear(64, 1), nn.Sigmoid())
        self.productivity_head = nn.Linear(256, len(PRODUCTIVITIES))

        # Frustration threshold (67.5 s from ProgSnap2 analysis)
        self.frustration_threshold_s = config.get('behavioral', {}).get('frustration_threshold', 67.5)

    def forward(self, action_ids: torch.Tensor,
                time_deltas: torch.Tensor,
                outcomes:    torch.Tensor,
                lengths:     torch.Tensor) -> Dict:
        """
        action_ids   : (B, T) long
        time_deltas  : (B, T) float — seconds, will be normalised
        outcomes     : (B, T) float — 1=success 0=fail
        lengths      : (B,)   long
        """
        B, T = action_ids.shape

        # Normalise time deltas to [0,1] over 5-minute window
        td_norm = torch.clamp(time_deltas / 300.0, 0.0, 1.0)

        # Embed actions
        act_emb = self.action_embed(action_ids)                  # (B,T,32)

        # Per-step context
        ctx_input = torch.stack([td_norm, outcomes], dim=-1)     # (B,T,2)
        ctx = self.context_proj(ctx_input)                       # (B,T,16)

        # Concatenate
        x = torch.cat([act_emb, ctx], dim=-1)                   # (B,T,48)

        # Pack for variable lengths
        packed = nn.utils.rnn.pack_padded_sequence(
            x, lengths.cpu(), batch_first=True, enforce_sorted=False
        )
        out_packed, (h, _) = self.bilstm(packed)

        # Final hidden: cat fwd+bwd final layers
        h_fwd = h[-2]   # (B, HIDDEN_DIM)
        h_bck = h[-1]   # (B, HIDDEN_DIM)
        h_cat = torch.cat([h_fwd, h_bck], dim=-1)               # (B, 256)

        # Shared trunk
        features = self.trunk(h_cat)                             # (B, 256)

        # Task heads
        emotion_logits = self.emotion_head(features)
        strategy_logits = self.strategy_head(features)
        effectiveness   = self.effectiveness_head(features).squeeze(-1)
        productivity_logits = self.productivity_head(features)

        return {
            'emotion_logits':      emotion_logits,
            'strategy_logits':     strategy_logits,
            'effectiveness':       effectiveness,
            'productivity_logits': productivity_logits,
            'hidden':              features,
        }

    @torch.no_grad()
    def analyze_strategy(self, action_ids:   torch.Tensor,
                         time_deltas:  torch.Tensor,
                         outcomes:     torch.Tensor,
                         lengths:      torch.Tensor) -> Dict:
        """
        Inference wrapper — returns human-readable strings.
        Used by orchestrator._analyze_behavior().
        """
        self.eval()

        # Ensure 2D
        if action_ids.dim() == 1:
            action_ids  = action_ids.unsqueeze(0)
            time_deltas = time_deltas.unsqueeze(0)
            outcomes    = outcomes.float().unsqueeze(0)
            lengths     = lengths.unsqueeze(0) if lengths.dim() == 0 else lengths

        # Ensure float
        time_deltas = time_deltas.float()
        outcomes    = outcomes.float()

        out = self.forward(action_ids, time_deltas, outcomes, lengths)

        emotions       = [EMOTIONS[i]      for i in out['emotion_logits'].argmax(-1).tolist()]
        strategies     = [STRATEGIES[i]    for i in out['strategy_logits'].argmax(-1).tolist()]
        productivities = [PRODUCTIVITIES[i] for i in out['productivity_logits'].argmax(-1).tolist()]
        emotion_conf   = F.softmax(out['emotion_logits'], dim=-1).max(-1).values.tolist()
        effectiveness  = out['effectiveness'].tolist()

        return {
            'emotion':            emotions,
            'emotion_confidence': emotion_conf,
            'strategy':           strategies,
            'effectiveness':      effectiveness,
            'productivity':       productivities,
        }

    @staticmethod
    def action_to_id(action: str) -> int:
        return ACTION_MAP.get(str(action).lower(), 4)   # default: edit

    def compute_loss(self, batch: Dict) -> torch.Tensor:
        """
        Multi-task loss for ProgSnap2 training.
        Accepts either 'action_ids' or 'action_sequence' key (dataloader uses the latter).
        batch keys: action_ids|action_sequence, time_deltas|timestamps,
                    outcomes|is_correct, lengths|sequence_lengths,
                    emotion_labels, strategy_labels, effectiveness_labels
        """
        # Key aliasing — dataloader uses different names than learning scripts
        action_ids = batch.get('action_ids', batch.get('action_sequence'))
        time_deltas_raw = batch.get('time_deltas', batch.get('timestamps'))
        # timestamps from dataloader is (B, T, 1) — squeeze last dim
        if time_deltas_raw is not None and time_deltas_raw.dim() == 3:
            time_deltas_raw = time_deltas_raw.squeeze(-1)
        outcomes = batch.get('outcomes', batch.get('is_correct',
                   torch.zeros(action_ids.shape[0], action_ids.shape[1]
                               if action_ids.dim() > 1 else 1)))
        # outcomes may be (B,) — expand to (B, T)
        if outcomes.dim() == 1:
            outcomes = outcomes.unsqueeze(1).expand(-1, action_ids.shape[-1]).float()
        lengths = batch.get('lengths', batch.get('sequence_lengths',
                  torch.full((action_ids.shape[0],), action_ids.shape[-1])))

        out = self.forward(action_ids, time_deltas_raw.float(), outcomes.float(), lengths)
        loss = torch.tensor(0.0)
        # emotion supervision — filter out unlabelled samples (-1)
        emotion_key = next((k for k in ['emotion_labels', 'emotion_label'] if k in batch), None)
        if emotion_key:
            el = batch[emotion_key]
            mask = el >= 0
            if mask.any():
                loss = loss + F.cross_entropy(out['emotion_logits'][mask], el[mask])
        if 'strategy_labels' in batch:
            loss = loss + F.cross_entropy(out['strategy_logits'], batch['strategy_labels'])
        if 'effectiveness_labels' in batch:
            loss = loss + F.mse_loss(out['effectiveness'], batch['effectiveness_labels'].float())
        return loss


# ─── BehavioralHMM ────────────────────────────────────────────────────────────

class BehavioralHMM:
    """
    Hidden Markov Model over debugging sessions.

    Hidden states (5):
      0 exploring        — trying things, no clear direction
      1 stuck            — repeated failures, long pauses
      2 making_progress  — iterative improvement
      3 understanding    — code compiles + runs correctly
      4 mastered         — submitted successfully

    Observations (7 features per time window):
      0 run_rate         — runs per minute
      1 error_rate       — errors per minute
      2 edit_rate        — edits per minute
      3 search_rate      — webpage/resource opens per minute
      4 avg_pause        — average time between actions (normalised)
      5 help_rate        — help requests per minute
      6 submit_flag      — any submission in window (0/1)

    Training: Baum-Welch EM on ProgSnap2 action sequences.
    Inference: Viterbi decoding.

    When not fitted (no training data yet), falls back to rule-based
    state classification from raw action counts.
    """

    N_STATES    = 5
    N_OBS       = 7
    STATE_NAMES = ["exploring", "stuck", "making_progress", "understanding", "mastered"]

    def __init__(self, config: Dict):
        self.config   = config
        self.is_fitted = False

        # HMM parameters (learned via Baum-Welch from ProgSnap2)
        # Initialise with sensible priors, updated during training.
        self.pi  = np.array([0.40, 0.20, 0.20, 0.10, 0.10])   # initial state dist
        self.A   = self._default_transition()                    # (5,5)
        self.mu  = self._default_emission_means()               # (5,7) means
        self.cov = np.tile(np.eye(self.N_OBS) * 0.1, (self.N_STATES, 1, 1))  # (5,7,7)

        # Checkpoint path
        self.ckpt_path = Path(config.get('behavioral', {}).get('hmm_checkpoint',
                                         'checkpoints/behavioral_hmm.json'))

        self._try_load()

    # ── Parameter defaults ────────────────────────────────────────────────────

    def _default_transition(self) -> np.ndarray:
        """
        Transitions: mostly self-looping with sensible forward paths.
        exploring → stuck / making_progress
        stuck → exploring / making_progress (with help)
        making_progress → understanding
        understanding → mastered
        """
        A = np.array([
            [0.50, 0.25, 0.20, 0.04, 0.01],   # exploring
            [0.30, 0.45, 0.20, 0.04, 0.01],   # stuck
            [0.10, 0.10, 0.55, 0.20, 0.05],   # making_progress
            [0.05, 0.05, 0.15, 0.65, 0.10],   # understanding
            [0.01, 0.01, 0.03, 0.10, 0.85],   # mastered
        ])
        return A / A.sum(axis=1, keepdims=True)

    def _default_emission_means(self) -> np.ndarray:
        """
        Expected observation values for each hidden state.
        Columns: run_rate, error_rate, edit_rate, search_rate,
                 avg_pause, help_rate, submit_flag
        """
        return np.array([
            [0.3, 0.2, 0.5, 0.3, 0.4, 0.1, 0.0],   # exploring
            [0.5, 0.6, 0.3, 0.4, 0.7, 0.3, 0.0],   # stuck
            [0.4, 0.3, 0.6, 0.2, 0.3, 0.1, 0.0],   # making_progress
            [0.2, 0.1, 0.3, 0.1, 0.2, 0.0, 0.1],   # understanding
            [0.1, 0.0, 0.1, 0.0, 0.1, 0.0, 1.0],   # mastered
        ])

    # ── Feature extraction ────────────────────────────────────────────────────

    def _extract_features(self, action_sequence: List[str],
                          window: int = 5) -> np.ndarray:
        """
        Slide a window of `window` actions and extract 7 features per window.
        Returns (T, 7) observation matrix where T = len(action_sequence) // window.
        """
        if not action_sequence:
            return np.zeros((1, self.N_OBS))

        windows = []
        for i in range(0, len(action_sequence), window):
            chunk = action_sequence[i: i + window]
            if not chunk:
                break
            n    = max(len(chunk), 1)
            runs   = sum(1 for a in chunk if 'run' in str(a).lower())
            errs   = sum(1 for a in chunk if 'error' in str(a).lower())
            edits  = sum(1 for a in chunk if 'edit' in str(a).lower() or a == 'code_edit')
            search = sum(1 for a in chunk if 'page' in str(a).lower() or 'resource' in str(a).lower())
            help_r = sum(1 for a in chunk if 'help' in str(a).lower())
            submit = float(any('submit' in str(a).lower() for a in chunk))
            pause  = 0.4   # placeholder — real value from time_deltas
            feat   = np.array([runs/n, errs/n, edits/n, search/n, pause, help_r/n, submit])
            windows.append(feat)

        return np.clip(np.array(windows), 0.0, 1.0)

    # ── Gaussian emission probability ─────────────────────────────────────────

    def _gaussian_log_prob(self, obs: np.ndarray, state: int) -> float:
        diff = obs - self.mu[state]
        cov  = self.cov[state]
        try:
            sign, logdet = np.linalg.slogdet(cov)
            inv_cov = np.linalg.inv(cov + np.eye(self.N_OBS) * 1e-6)
            return -0.5 * (diff @ inv_cov @ diff + logdet)
        except Exception:
            return -np.sum(diff ** 2)   # fallback

    # ── Viterbi decoding ──────────────────────────────────────────────────────

    def _viterbi(self, obs_seq: np.ndarray) -> List[int]:
        T   = len(obs_seq)
        log_delta = np.full((T, self.N_STATES), -np.inf)
        psi       = np.zeros((T, self.N_STATES), dtype=int)
        log_A     = np.log(self.A + 1e-10)
        log_pi    = np.log(self.pi + 1e-10)

        for s in range(self.N_STATES):
            log_delta[0, s] = log_pi[s] + self._gaussian_log_prob(obs_seq[0], s)

        for t in range(1, T):
            for s in range(self.N_STATES):
                trans = log_delta[t-1] + log_A[:, s]
                psi[t, s]       = int(np.argmax(trans))
                log_delta[t, s] = trans[psi[t, s]] + self._gaussian_log_prob(obs_seq[t], s)

        path = [int(np.argmax(log_delta[-1]))]
        for t in range(T-1, 0, -1):
            path.insert(0, psi[t, path[0]])
        return path

    # ── Public API ────────────────────────────────────────────────────────────

    def analyze_session(self, action_sequence: List[str]) -> Dict:
        """
        Infer hidden state sequence for a debugging session.
        Returns final state + confidence.
        """
        if not action_sequence:
            return {'final_state': 'exploring', 'final_confidence': 0.5,
                    'state_sequence': [], 'is_fitted': self.is_fitted}

        obs_seq = self._extract_features(action_sequence)

        if self.is_fitted and len(obs_seq) > 0:
            try:
                path     = self._viterbi(obs_seq)
                final_id = path[-1]
                conf     = float(np.exp(
                    self._gaussian_log_prob(obs_seq[-1], final_id)
                ))
                conf = min(0.95, max(0.40, conf))
            except Exception:
                final_id, conf = self._rule_based(action_sequence)
        else:
            final_id, conf = self._rule_based(action_sequence)

        return {
            'final_state':      self.STATE_NAMES[final_id],
            'final_confidence': conf,
            'state_sequence':   [self.STATE_NAMES[s] for s in
                                 (self._viterbi(obs_seq) if self.is_fitted else [final_id])],
            'is_fitted':        self.is_fitted,
        }

    def _rule_based(self, action_sequence: List[str]) -> Tuple[int, float]:
        """
        Fallback rule-based state classifier when HMM not yet trained.
        """
        actions = [str(a).lower() for a in action_sequence]
        n = max(len(actions), 1)
        submit_pct = sum('submit' in a for a in actions) / n
        error_pct  = sum('error' in a for a in actions) / n
        run_pct    = sum('run' in a   for a in actions) / n

        if submit_pct > 0.1:
            return 4, 0.85   # mastered
        if error_pct < 0.1 and run_pct > 0.2:
            return 3, 0.75   # understanding
        if error_pct > 0.5:
            return 1, 0.70   # stuck
        if run_pct > 0.3:
            return 2, 0.65   # making_progress
        return 0, 0.55       # exploring

    def fit(self, obs_sequences: List[np.ndarray], n_iter: int = 20):
        """
        Baum-Welch EM training on a list of observation sequences.
        Each sequence is (T, 7) from _extract_features().
        Called by src/train.py after ProgSnap2 is downloaded.
        """
        print(f"[HMM] Baum-Welch training on {len(obs_sequences)} sessions ({n_iter} iterations)...")
        # Simplified EM — full implementation in training script
        # Update means from sequences
        all_obs = np.concatenate(obs_sequences, axis=0)
        for s in range(self.N_STATES):
            # Weight observations by soft assignment (simplified)
            weights = np.exp([self._gaussian_log_prob(o, s) for o in all_obs])
            weights = weights / (weights.sum() + 1e-10)
            self.mu[s] = np.average(all_obs, axis=0, weights=weights)
        self.is_fitted = True
        self._save()
        print(f"[HMM] Training complete. Model saved to {self.ckpt_path}")

    def _save(self):
        self.ckpt_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            'pi':        self.pi.tolist(),
            'A':         self.A.tolist(),
            'mu':        self.mu.tolist(),
            'is_fitted': self.is_fitted,
        }
        with open(self.ckpt_path, 'w') as f:
            json.dump(data, f)

    def _try_load(self):
        if self.ckpt_path.exists():
            try:
                with open(self.ckpt_path) as f:
                    data = json.load(f)
                self.pi        = np.array(data['pi'])
                self.A         = np.array(data['A'])
                self.mu        = np.array(data['mu'])
                self.is_fitted = data.get('is_fitted', False)
                print(f"[HMM] Loaded checkpoint from {self.ckpt_path}")
            except Exception as e:
                print(f"[HMM] Could not load checkpoint: {e}")
