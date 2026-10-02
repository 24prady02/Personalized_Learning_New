"""
thresholds.py — every number the algorithm uses, in one place.

Mirrors the Thresholds sheet of docs/CPAL_LP_Classification_Algorithm.xlsx.
All are starting values, to be calibrated against teacher-labelled prompts.
"""

# Gate G1 Content
MIN_WORDS = 3

# Step 3 Concept linking
W_CODE, W_WORD, W_SEM, W_MIS = 2, 1, 4, 3
SEM_FLOOR = 0.40
MIS_FLOOR = 0.50
KEEP_SCORE = 1.0
RELATIVE_KEEP = 0.5
MAX_CONCEPTS = 3

# Gate G5 Weak link
WEAK_LINK = 0.5

# Gate G7 Parroting
PARROT_SIM = 0.85

# Step 6 E2 fact match
FACT_ENT = 0.5
FACT_SIM = 0.60
FACT_CONTRA_MAX = 0.3

# Gate G15 Ambiguity band (similarity)
BAND_LO = 0.45

# Gates G9 / G10 and misconception refuted
CONTRA = 0.6

# Misconception held / refuted
HELD_ENT = 0.5
HELD_SIM = 0.62          # minimum similarity for any held decision
HELD_SIM_STRONG = 0.75   # held on similarity alone (no NLI entailment)
REF_SIM = 0.50

# Stability
JUMP = 2          # Gate G17: levels gained in one prompt
PLATEAU = 3       # Rule R8: prompts at the same level
STALE = 3         # Gate G20: sessions before evidence is stale

# Step 11 Confidence
ID_CONF = 0.6
