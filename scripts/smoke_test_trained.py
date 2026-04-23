"""
Smoke test: verify all four trained checkpoints load and produce a forward
pass / inference without errors. Exits non-zero on failure.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import torch

print("=" * 55)
print("Trained-component smoke test")
print("=" * 55)

# 1. BehavioralHMM
print("\n[1/4] BehavioralHMM")
from src.models.behavioral import BehavioralHMM
hmm = BehavioralHMM({'behavioral': {'hmm_checkpoint': 'checkpoints/behavioral_hmm.json'}})
assert hmm.is_fitted, "HMM should be loaded as trained"
feats = hmm._extract_features(['Run.Program', 'Compile.Error', 'File.Edit',
                                'Run.Program', 'Run.Error', 'File.Edit',
                                'Run.Program', 'Submit', 'File.Edit', 'Run.Program'])
out = hmm.analyze_session(['Run.Program', 'Compile.Error', 'File.Edit', 'Submit'])
print(f"   is_fitted={hmm.is_fitted}")
print(f"   feature shape: {feats.shape}")
print(f"   session analysis -> final_state={out['final_state']} conf={out['final_confidence']:.3f}")

# 2. Nestor
print("\n[2/4] NestorBayesianProfiler")
from src.models.nestor.nestor_bayesian_profiler import NestorBayesianProfiler
prof = NestorBayesianProfiler({'nestor': {'data_dir': 'data/nestor'}})
assert prof.is_trained, "Nestor CPTs should load as trained"
result = prof.complete_inference({
    'exploration_rate': 0.7, 'persistence': 0.6,
    'organization': 0.8, 'social_interaction': 0.4,
    'emotional_variability': 0.3,
})
print(f"   is_trained={prof.is_trained}")
print(f"   personality: { {k: round(v,2) for k,v in result['personality'].items()} }")
print(f"   intervention_preference: {result['intervention_preference']}")
print(f"   top-3 elements: {result['recommended_elements']}")

# 3. Emotion classifier (via orchestrator loader)
print("\n[3/4] EmotionClassifier (direct)")
data = torch.load('checkpoints/emotion_classifier.pt', weights_only=False, map_location='cpu')
classes = data['classes']
import torch.nn as nn
model = nn.Sequential(
    nn.Linear(7, 64), nn.ReLU(), nn.Dropout(0.2),
    nn.Linear(64, 64), nn.ReLU(), nn.Dropout(0.2),
    nn.Linear(64, len(classes)),
)
model.load_state_dict({k.replace('net.', ''): v for k, v in data['state_dict'].items()})
model.eval()
# frustrated pattern: high run_rate, high error_rate, low edit
x = torch.tensor([[0.8, 0.7, 0.2, 0.1, 0.4, 0.2, 0.0]])
with torch.no_grad():
    p = torch.softmax(model(x), dim=1).squeeze().tolist()
pred = classes[int(np.argmax(p))]
print(f"   classes: {classes}")
print(f"   pred for (high run+error, low edit): {pred} (probs {[round(v,2) for v in p]})")

# 4. RL agent
print("\n[4/4] TeachingRLAgent")
# Minimal config + models — avoid full orchestrator init to keep test focused
config = {'rl': {'checkpoint': 'checkpoints/rl_teaching_agent.pt'}}
from src.reinforcement_learning.teaching_agent import TeachingRLAgent
agent = TeachingRLAgent(config, models={})
# sample forward pass
with torch.no_grad():
    q = agent.policy_net(torch.randn(1, 512))
print(f"   epsilon after load: {agent.epsilon:.3f}")
print(f"   steps after load: {agent.steps}")
print(f"   Q-values shape: {q.shape}  argmax action: {int(q.argmax().item())}")

print("\n" + "=" * 55)
print("ALL FOUR COMPONENTS LOAD AND FORWARD CLEANLY")
print("=" * 55)
