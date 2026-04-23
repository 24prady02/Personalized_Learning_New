"""
Train BehavioralHMM with full Baum-Welch EM on ProgSnap2 action sequences.
Saves checkpoint to checkpoints/behavioral_hmm.json so src/models/behavioral.py
_try_load() picks it up instead of running with hand-written priors.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
import time
import numpy as np
import pandas as pd

from src.models.behavioral import BehavioralHMM


PROGSNAP2_CSV = Path("data/progsnap2/MainTable.csv")
CKPT = Path("checkpoints/behavioral_hmm.json")
N_STATES = 5
N_OBS = 7


def load_sequences_per_student(csv_path: Path, max_students: int = 800):
    print(f"[HMM] loading {csv_path}")
    df = pd.read_csv(csv_path)
    df = df.sort_values(["SubjectID", "ServerTimestamp"])
    sequences = []
    for sid, grp in df.groupby("SubjectID", sort=False):
        events = grp["EventType"].astype(str).tolist()
        if len(events) >= 5:
            sequences.append(events)
        if len(sequences) >= max_students:
            break
    print(f"[HMM] collected {len(sequences)} student sessions "
          f"(avg length {np.mean([len(s) for s in sequences]):.1f})")
    return sequences


def forward(obs, pi, A, mu, cov):
    T, D = obs.shape
    S = len(pi)
    log_alpha = np.full((T, S), -np.inf)
    log_b = np.zeros((T, S))
    for t in range(T):
        for s in range(S):
            log_b[t, s] = _log_gaussian(obs[t], mu[s], cov[s])
    log_alpha[0] = np.log(pi + 1e-12) + log_b[0]
    for t in range(1, T):
        for j in range(S):
            log_alpha[t, j] = log_b[t, j] + _logsumexp(log_alpha[t-1] + np.log(A[:, j] + 1e-12))
    return log_alpha, log_b


def backward(log_b, A):
    T, S = log_b.shape
    log_beta = np.zeros((T, S))
    for t in range(T-2, -1, -1):
        for i in range(S):
            log_beta[t, i] = _logsumexp(
                np.log(A[i] + 1e-12) + log_b[t+1] + log_beta[t+1]
            )
    return log_beta


def _logsumexp(x):
    m = np.max(x)
    if not np.isfinite(m):
        return -np.inf
    return m + np.log(np.sum(np.exp(x - m)) + 1e-30)


def _log_gaussian(x, mu, cov):
    d = x - mu
    inv = np.linalg.inv(cov + 1e-6 * np.eye(len(cov)))
    sign, logdet = np.linalg.slogdet(cov + 1e-6 * np.eye(len(cov)))
    return -0.5 * (len(x) * np.log(2*np.pi) + logdet + d @ inv @ d)


def baum_welch(sequences, n_iter=15, verbose=True):
    # init from the module's defaults
    hmm = BehavioralHMM({'behavioral': {'hmm_checkpoint': str(CKPT)}})
    pi, A, mu, cov = hmm.pi.copy(), hmm.A.copy(), hmm.mu.copy(), hmm.cov.copy()

    # convert raw event lists to windowed obs matrices
    obs_list = [hmm._extract_features(s) for s in sequences]
    obs_list = [o for o in obs_list if o.shape[0] >= 2]
    if verbose:
        print(f"[HMM] {len(obs_list)} windowed obs sequences, "
              f"avg T={np.mean([o.shape[0] for o in obs_list]):.1f}")

    prev_ll = -np.inf
    for it in range(n_iter):
        t0 = time.time()
        total_gamma = np.zeros((N_STATES,))
        total_xi = np.zeros((N_STATES, N_STATES))
        weighted_obs_sum = np.zeros((N_STATES, N_OBS))
        weighted_count = np.zeros((N_STATES,))
        start_gamma = np.zeros((N_STATES,))
        ll_sum = 0.0

        for obs in obs_list:
            T = obs.shape[0]
            log_alpha, log_b = forward(obs, pi, A, mu, cov)
            log_beta = backward(log_b, A)
            seq_ll = _logsumexp(log_alpha[-1])
            ll_sum += seq_ll

            log_gamma = log_alpha + log_beta - seq_ll
            gamma = np.exp(log_gamma)

            start_gamma += gamma[0]

            # xi
            for t in range(T-1):
                denom = seq_ll
                for i in range(N_STATES):
                    for j in range(N_STATES):
                        log_xi = (log_alpha[t, i] + np.log(A[i, j] + 1e-12)
                                  + log_b[t+1, j] + log_beta[t+1, j] - denom)
                        total_xi[i, j] += np.exp(log_xi)

            total_gamma += gamma.sum(axis=0)
            weighted_obs_sum += gamma.T @ obs
            weighted_count += gamma.sum(axis=0)

        # M-step
        pi = start_gamma / (start_gamma.sum() + 1e-12)
        A = total_xi / (total_xi.sum(axis=1, keepdims=True) + 1e-12)
        mu = weighted_obs_sum / (weighted_count[:, None] + 1e-12)

        if verbose:
            print(f"  iter {it+1:02d}/{n_iter}  "
                  f"log-lik={ll_sum:.1f}  delta={ll_sum - prev_ll:+.2f}  "
                  f"t={time.time()-t0:.1f}s")
        if abs(ll_sum - prev_ll) < 0.5 and it > 2:
            print(f"[HMM] converged at iter {it+1}")
            break
        prev_ll = ll_sum

    return pi, A, mu, cov


def main():
    sequences = load_sequences_per_student(PROGSNAP2_CSV, max_students=800)
    pi, A, mu, cov = baum_welch(sequences, n_iter=15)

    CKPT.parent.mkdir(parents=True, exist_ok=True)
    with open(CKPT, "w") as f:
        json.dump({
            "pi": pi.tolist(),
            "A": A.tolist(),
            "mu": mu.tolist(),
            "is_fitted": True,
        }, f, indent=2)
    print(f"[HMM] saved {CKPT}")

    # quick verification
    hmm2 = BehavioralHMM({'behavioral': {'hmm_checkpoint': str(CKPT)}})
    print(f"[HMM] reload check: is_fitted={hmm2.is_fitted}")
    print(f"[HMM] learned transition A (rows sum to 1):")
    for i, row in enumerate(hmm2.A):
        print(f"   {BehavioralHMM.STATE_NAMES[i]:<18} {row}")


if __name__ == "__main__":
    main()
