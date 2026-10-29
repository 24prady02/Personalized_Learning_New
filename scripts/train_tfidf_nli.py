"""Train a TF-IDF pair classifier on the graph-built NLI pairs (no student answers).

For a pair (graph text, statement) the features are the TF-IDF anchors of
edgelogic.EdgeLogicReader (code tokens, numbers, content words, with words
after "no / not" marked as negated), split three ways:

* ``S:tok`` anchors both texts share,
* ``P:tok`` anchors only the graph text has,
* ``H:tok`` anchors only the statement has,

each weighted by its rarity in the graph, plus the overlap score and the
negation of each side. A logistic regression learns from data/nli_pairs.json
which shared / missing anchors mean agree (1), contradict (0) or unrelated (2).

Checks, both graph-only:
1. accuracy on the dev split (concepts never seen in training);
2. side test: every misconception whose node restates its wrong belief or its
   correct rule in other words - is the restatement put on the right side?

    python scripts/train_tfidf_nli.py   -> models/tfidf-nli.pkl
"""

from __future__ import annotations

import json
import pickle
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from lp_graph.edgelogic import reader_for  # noqa: E402
from lp_graph.graph import KG  # noqa: E402
from lp_graph.tfidf_nli import pair_features  # noqa: E402


def main() -> int:
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.linear_model import LogisticRegression

    kg = KG()
    r = reader_for(kg)
    pairs = json.load(open(ROOT / "data" / "nli_pairs.json", encoding="utf-8"))
    train = [p for p in pairs if p["split"] == "train"]
    dev = [p for p in pairs if p["split"] == "dev"]
    vec = DictVectorizer()
    x_tr = vec.fit_transform([pair_features(r, p["premise"], p["hypothesis"]) for p in train])
    x_dev = vec.transform([pair_features(r, p["premise"], p["hypothesis"]) for p in dev])
    clf = LogisticRegression(max_iter=2000, C=1.0, class_weight="balanced", random_state=13)
    clf.fit(x_tr, [p["label"] for p in train])
    pred = clf.predict(x_dev)
    acc = sum(int(a == p["label"]) for a, p in zip(pred, dev)) / max(1, len(dev))
    print(f"dev accuracy: {acc:.3f} on {len(dev)} pairs of unseen concepts")
    names = {0: "contradiction", 1: "entailment", 2: "neutral"}
    for k, n in names.items():
        tp = sum(1 for a, p in zip(pred, dev) if a == k and p["label"] == k)
        print(f"  {n:13} precision {tp / max(1, sum(1 for a in pred if a == k)):.2f}"
              f"  recall {tp / max(1, sum(1 for p in dev if p['label'] == k)):.2f}")

    # side test on the graph's own restatements
    nodes = {m["id"]: m for m in kg.knowledge.raw.get("misconceptions_and_errors", [])}
    model = {"vec": vec, "clf": clf}
    from lp_graph.tfidf_nli import side as tside
    right = wrong_ok = total_w = total_r = flagged_r = undecided = 0
    for ms in kg.mis_edges.values():
        for m in ms:
            node = nodes.get(m.mis, {})
            if not (m.wrong and m.right):
                continue
            wb, cr = node.get("wrong_belief"), node.get("correct_rule")
            if wb and wb != m.wrong:
                total_w += 1
                s = tside(r, model, wb, m.wrong, m.right)
                wrong_ok += s == "wrong"
                undecided += s is None
            if cr and cr != m.right:
                total_r += 1
                s = tside(r, model, cr, m.wrong, m.right)
                right += s == "right"
                flagged_r += s == "wrong"
                undecided += s is None
    print(f"side test: wrong-belief restatements put on the wrong side {wrong_ok}/{total_w}; "
          f"correct-rule restatements put on the right side {right}/{total_r}, wrongly flagged {flagged_r}; "
          f"undecided {undecided}")
    out = ROOT / "models" / "tfidf-nli.pkl"
    out.parent.mkdir(exist_ok=True)
    pickle.dump(model, open(out, "wb"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
