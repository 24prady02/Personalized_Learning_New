# Lightweight, deterministic / non-generative methods for matching student sentences to label texts with very few labels

Setting this research serves: no generative LLM at run time; deterministic preferred; ~365 answers with overall levels, 19 with edge-level gold.

Source-verification legend:
- (V) means the source was fetched or read in this session.
- (S) means the claim comes from a search-result snippet or abstract only.
- (K) means a standard reference cited from prior knowledge by its canonical ID. It was not fetched this session, so the report writer should treat its details as needing verification.

## 1. Retrieval baselines (TF-IDF, BM25, LSA, embedding averages) for short-answer / label matching in education

### Takeaway
In educational answer assessment, simple lexical overlap is a hard baseline to beat, especially for unseen questions or domains. In SemEval-2013 Task 7, only about half the submitted results beat the lexical-overlap baseline. LSA cosine matching against "expectations" (AutoTutor) is the classic deterministic precedent, and its key tunable is the cosine threshold, which works best when it depends on length. Dense sentence embeddings (MiniLM) are the modern cheap baseline, but they still lean on lexical overlap and benefit from a reranker.

### Cited Findings
- **SemEval-2013 Task 7 (Dzikovska et al., 2013, *SEM/SemEval, pp. 263–274)** is the joint Student Response Analysis + 8th RTE challenge. It has 5-way, 3-way and 2-way labels (correct / partially correct / contradictory / irrelevant / non-domain) and three test splits: unseen answers (UA), unseen questions (UQ) and unseen domains (UD). It had 9 teams. (V) — [ACL Anthology S13-2045](https://aclanthology.org/S13-2045)
- Data: BEETLE has 56 electricity/electronics questions and ~3,000 answers. SciEntsBank has ~10,000 answers to 197 questions across 15 science domains. (V) — [S13-2045](https://aclanthology.org/S13-2045)
- Lexical-overlap baseline, 5-way weighted F1: BEETLE UA 0.483, UQ 0.463; SciEntsBank UA 0.435, UQ 0.402, UD 0.396. Majority baseline is ~0.23–0.26. The best systems were ETS2 at 0.705 (BEETLE UA) and 0.614 (BEETLE UQ), and CoMeT1 at 0.598 (SciEnts UA). On SciEnts UQ and UD, the best results were only ~0.49 and ~0.47 (SoftCardinality1), barely above the lexical 0.402 and 0.396. (V) — [S13-2045](https://aclanthology.org/S13-2045)
- 5-way macro F1, lexical baseline: 0.424 / 0.414 / 0.375 / 0.329 / 0.311. ETS2 scored 0.619 on BEETLE UA. (V) — [S13-2045](https://aclanthology.org/S13-2045)
- 2-way macro F1: the lexical baseline scored 0.788 on BEETLE UA and 0.725 on BEETLE UQ, against the best systems' ~0.833 and ~0.72. On BEETLE UQ, the lexical baseline was roughly as good as the best system. (V; table layout was garbled in text extraction, so the BEETLE values are the reliably parsed ones) — [S13-2045](https://aclanthology.org/S13-2045)
- The overview paper concludes: "Beating the lexical overlap baseline proved to be more challenging, being achieved by just over half of the results with about half of those being statistically significant improvements." ETS2 was best on BEETLE UQ but was statistically *worse* than the lexical baseline on SciEnts UQ/UD. (V) — [S13-2045](https://aclanthology.org/S13-2045)
- Moving from seen to unseen questions costs a lot. The best 5-way weighted F1 drops 0.09 from BUA to BUQ and 0.13 from SUA to SUQ. On 2-way, the drop is 0.11 (BEETLE) and 0.03 (SciEnts). (V) — [S13-2045](https://aclanthology.org/S13-2045)
- Several top systems emphasised text-to-text similarity features; the paper names Celi, ETS and SoftCardinality. SoftCardinality is a deterministic soft set-overlap measure. (V) — [S13-2045](https://aclanthology.org/S13-2045)
- The precursor dataset paper, Dzikovska, Nielsen & Brew (NAACL 2012, pp. 200–210), "Towards Effective Tutorial Feedback for Explanation Questions: A Dataset and Baselines", compares three baselines and explicitly aims to prompt contradiction-detection work. (S) — [N12-1021](https://aclanthology.org/N12-1021/)
- **AutoTutor LSA:** an expectation counts as covered when the LSA cosine between the student turn(s) and the expectation is at or above a threshold T. Previous AutoTutor versions used T between 0.40 and 0.75. (S) — [FLAIRS 2005](https://cdn.aaai.org/FLAIRS/2005/Flairs05-085.pdf)
- Penumatsa et al. (IJAIT 2006), "The right threshold value", found the best agreement with expert raters when the cosine threshold is a function of the lengths of both the student answer and the expectation. (S) — [Memphis digital commons](https://digitalcommons.memphis.edu/facpubs/8806)
- The FLAIRS 2003 AutoTutor study computes the LSA cosine between each expectation and every combination of student sentences, then takes the max. This deliberately biases scoring toward "covered". (S) — [FLAIRS 2003](https://cdn.aaai.org/FLAIRS/2003/Flairs03-082.pdf)
- Wiemer-Hastings et al. (FLAIRS 1999) describe how AutoTutor assesses student contributions with LSA. (S) — [FLAIRS99-034](https://cdn.aaai.org/FLAIRS/1999/FLAIRS99-034.pdf)
- A later Memphis thesis (Carmon, 2021) evaluated a hybrid of LSA and regular expressions against human ratings at stringent, intermediate and lenient thresholds. (S) — [Memphis ETD 2148](https://digitalcommons.memphis.edu/etd/2148)
- **Eedi "Mining Misconceptions in Mathematics" (Kaggle 2024):** the task links distractors to misconception labels and is scored by MAP@25. Eedi's own minimalist baseline used all-MiniLM-L6-v2 with no fine-tuning and focused on query construction. Top solutions used LLM embedders plus a 32B reranker, which is outside these constraints. (S) — [Eedi blog](https://eedi.com/blog/from-wrong-answers-to-real-insights-how-we-used-a-kaggle-challenge-to-map-student-misconceptions)
- A 2026 study of misconception diagnosis from student–tutor dialogue found that MiniLM-L6-v2 cosine retrieval gives good initial candidates but "relies heavily on lexical overlap". A reranker fixed many cases where the gold label ranked 2nd or lower. (S) — [arXiv 2602.02414](https://arxiv.org/pdf/2602.02414)
- In general IR, DPR beat BM25 by 9–19 points absolute top-20 accuracy on open-domain QA (Karpukhin et al., EMNLP 2020). Other studies find BM25 competitive, and hybrid retrieval is standard practice. (S) — [DPR](https://PapersWithCode.com/paper/dense-passage-retrieval-for-open-domain)

### Inferences
- Given 19 edge-level gold examples, a deterministic lexical/LSA/embedding cosine with a **length-dependent threshold** (per AutoTutor) and a **max over sentence combinations** is a defensible, citable baseline. Any learned component should be reported against it, as SemEval-2013 did.
- The SemEval UQ/UD results suggest that methods tuned to specific labels or questions generalise poorly. With unseen labels at test time, expect performance near lexical-baseline level unless an NLI-style transfer model is used (see section 4).
- Hybrid BM25 plus a small sentence embedder, followed by a non-generative cross-encoder reranker, matches the Eedi/dialogue findings and stays within the "no generative LLM" constraint.

### Gaps
- I found no published head-to-head of BM25 vs TF-IDF vs LSA vs SBERT on misconception or rubric matching with exact numbers. No BM25 baseline was found for the Eedi data.
- I did not retrieve the exact AutoTutor LSA agreement numbers (e.g. correlations with expert raters) from the 2003 and 2006 papers.
- SciEntsBank 2-way per-system numbers could not be cleanly parsed from the PDF layout.

## 2. Natural logic inference (NatLog, NaturalLI) and symbolic WordNet-based entailment

### Takeaway
Natural logic gives deterministic, explainable entailment and contradiction judgments, including exclusion (antonymy, negation) via MacCartney's seven basic relations and monotonicity projection. It is precise but low-recall: NaturalLI reports 91% precision at 49% recall on common-sense facts. It works best as a high-precision component combined with a statistical matcher. I found no published use of it in short-answer assessment.

### Cited Findings
- MacCartney & Manning (COLING 2008, best paper), "Modeling Semantic Containment and Exclusion in NLI", extends natural logic from containment/monotonicity to exclusion and implicativity, without full semantic interpretation. They report a **27% error reduction on FraCaS** relative to earlier work. Combining it with an existing RTE system gave significant gains on RTE3. (S) — [C08-1066](https://aclanthology.org/C08-1066/)
- An extended version appeared at IWCS 2009 ("An extended model of natural logic"). (S) — [Stanford PDF](https://www-nlp.stanford.edu/pubs/natlog-iwcs09.pdf)
- Angeli & Manning (EMNLP 2014, pp. 534–545), "NaturalLI: Natural Logic Inference for Common Sense Reasoning", searches over a large plain-text fact database with natural logic mutations, so no translation to formal logic is needed. It captures strict natural-logic inferences on FraCaS and predicts common-sense facts at **49% recall / 91% precision**. (S) — [D14-1059](https://aclanthology.org/D14-1059/)
- Angeli's thesis reports a 4x recall improvement over lemmatized lookup while keeping precision above 90%. (S) — [Angeli thesis](https://nlp.stanford.edu/~angeli/papers/thesis.pdf)
- NaturalLI code: [GitHub (mirror)](https://github.com/vegeta03/naturalli) (S)

### Inferences
- For deciding "agree vs contradict" between a student sentence and a label, the natural-logic relations map directly. Equivalence or forward entailment means agree. Alternation or negation means contradict. Independence means unknown.
- Main limits from the literature: low recall, dependence on alignment or edit sequences between the two sentences, lexical-relation coverage (WordNet), and fragility on paraphrase. Use it as a deterministic high-precision override, for example to flip a similarity match to "contradiction" when it detects negation or antonymy, rather than as the primary classifier.

### Gaps
- I did not retrieve absolute FraCaS accuracy figures; MacCartney's thesis is often quoted at ~70% overall FraCaS, but this is unverified here.
- I found no application of NatLog/NaturalLI to educational short answers or rubric matching.
- I found no measured coverage of WordNet-based entailment on student text.

## 3. Weak / distant supervision, data programming, self-training, auxiliary signals

### Takeaway
Snorkel-style labelling functions (keyword/regex rules, LSA/embedding thresholds, natural-logic negation detectors, answer-level overall grades) combined by a label model can turn ~365 coarsely labelled answers into noisy edge-level training data. I found no published education-specific Snorkel study and no study that labels student explanations from code-execution results.

### Cited Findings
- Ratner et al. (VLDB 2017; VLDB Journal 2020), "Snorkel: Rapid Training Data Creation with Weak Supervision": users write labelling functions that label or abstain. A generative label model, learned without ground truth, combines them into probabilistic labels, which then train a discriminative model. Snorkel beat distant-supervision baselines by an average of **132%** across its applications. (S) — [arXiv 1711.10160](https://arxiv.org/pdf/1711.10160); [VLDB J.](https://link.springer.com/article/10.1007/s00778-019-00552-1)
- Weak classifiers (e.g. a cosine-threshold matcher) can themselves serve as labelling functions. (S) — [Snorkel paper](https://arxiv.org/pdf/1711.10160)

### Inferences
- Candidate labelling functions for this project:
  1. Lexical/LSA/SBERT cosine above a length-dependent threshold means agree.
  2. A negation or antonym mismatch detected via natural logic or WordNet means contradict.
  3. Answer-level overall level as a weak prior. A "level 0" answer is unlikely to agree with advanced labels.
  4. Hand-written rubric keyword rules.
  5. Where student code exists, execution or test outcomes as weak evidence about whether the explanation is correct. This last one is not demonstrated in the literature I found.
- The 19 edge-level gold examples should be held out to evaluate the label model, not used to train it.

### Gaps
- I found no education or EDM papers using Snorkel or data programming for short answers or misconceptions in this session.
- I found nothing on code-execution-derived labels for explanations.
- Self-training results for automatic short-answer grading (ASAG) were not retrieved.

## 4. Small cross-encoders / NLI fine-tuning and contrastive few-shot methods

### Takeaway
Transfer from general NLI (MNLI) is the strongest documented low-data route to answer-vs-reference entailment. On SemEval-2013 it gave up to 13 points absolute macro-F1 over the previous SOTA, and it generalises better to unseen domains. An entailment formulation reaches near-SOTA with about 10% of SciEntsBank training data. Off-the-shelf NLI models are known to mishandle negation, so contrastive hard negatives (negated or antonym pairs) matter. SetFit-style contrastive fine-tuning of small sentence encoders is the documented few-shot path that needs no generative model.

### Cited Findings
- Camus & Filighera (AIED 2020, LNCS pp. 177–190), "Investigating Transformers for ASAG", fine-tuned BERT, RoBERTa, ALBERT, XLM, XLM-R and distilled models on SemEval-2013 SciEntsBank (3-way). They report up to **13% absolute macro-F1 improvement** over SOTA. Transfer from a RoBERTa-large model already fine-tuned on MNLI "yields a significant improvement" and improves generalisation to a separate domain. Distilled models (40% smaller) lose at most about 2 points against the prior SOTA. Large models beat base models significantly. (V) — [TU Darmstadt PDF](https://www.kom.tu-darmstadt.de/papers/CF20-1.pdf?download)
- An entailment-based ASAG thesis (UPV/EHU) reformulates grading as textual entailment. It is competitive few-shot and near SOTA with **~10% of SciEntsBank training data**. Adding out-of-domain QA pairs can *hurt*. (S) — [ADDI EHU 10810/61822](https://addi.ehu.es/handle/10810/61822?show=full)
- Saha et al. (2019), "Joint Multi-Domain Learning for ASAG": SciEntsBank domains have only 70–697 training samples each, and task-specific models generally beat transfer on this dataset. (S) — [arXiv 1902.09183](https://arxiv.org/pdf/1902.09183)
- A T5 ASAG thesis (Twente) found domain-independent fine-tuning preferable to domain-specific fine-tuning in data-sparse cases. (S) — [Twente essay 83879](https://essay.utwente.nl/essays/83879)
- Hossain et al. (EMNLP 2020), "An Analysis of NLI Benchmarks through the Lens of Negation": negation is rare in MNLI, SNLI and RTE, and usually unimportant there. On a new benchmark where negation is critical, SOTA transformers struggle. (S) — [2020.emnlp-main.732](https://aclanthology.org/2020.emnlp-main.732)
- Tunstall et al. (2022; NeurIPS ENLSP workshop), SetFit: contrastive Siamese fine-tuning of a Sentence Transformer on a few labelled pairs, plus a classification head. It needs no prompts, is competitive with PET/PEFT, and is an order of magnitude faster. SetFit-RoBERTa-large (355M) beat PET and GPT-3 on RAFT. (S) — [arXiv 2209.11055](https://arxiv.org/abs/2209.11055v1); [HF blog](https://huggingface.co/blog/setfit)

### Inferences
- A practical recipe:
  1. Start from an off-the-shelf MNLI cross-encoder, which is deterministic at inference.
  2. Treat label text as the hypothesis and the student sentence as the premise.
  3. Optionally fine-tune for a few epochs on Snorkel-generated pairs plus synthetic hard negatives: negated or antonym-swapped versions of the label texts, labelled contradiction.
  4. Evaluate on the 19 gold edges.
- The evidence on how much in-domain data is needed is thin. "~10% of SciEntsBank" is a few hundred to ~1,000 pairs, which is still more than 19. Expect zero-shot MNLI transfer, plus thresholds calibrated on the gold set, to be the realistic regime.

### Gaps
- I did not extract exact per-split numbers from the Camus & Filighera table.
- There is no direct evidence on curves with 10–50 examples for NLI adaptation in education.
- No study combined negation hard-negative augmentation with ASAG specifically.

## 5. Structured prediction / joint inference over a label graph with logical constraints

### Takeaway
ILP (Roth & Yih 2004), Markov Logic Networks (Richardson & Domingos 2006) and Probabilistic Soft Logic (Bach et al. 2017) all let local match or contradiction scores be combined with hard and soft constraints over a label graph. Examples are "cannot both agree with A and with its contradiction ¬A" and "prerequisite edges imply ordering". All three run deterministically at inference. PSL has a documented education use: modelling MOOC learner engagement (Ramesh, Goldwasser, Huang, Daumé III, Getoor; NIPS-WS 2013, AAAI 2014).

### Cited Findings
- Ramesh et al., "Modeling Learner Engagement in MOOCs using Probabilistic Soft Logic" (NIPS workshop 2013) encodes domain knowledge about student interactions and performance as PSL rules on Coursera data. Modelling engagement helps predict performance. (S) — [LINQS PDF](https://linqs.org/assets/resources/ramesh-dde13.pdf)
- Ramesh et al. (AAAI 2014), "Learning Latent Engagement Patterns of Students in Online Courses", uses latent engagement variables in PSL linking behaviour to course completion. It keeps predictive power with partial (early) data. (S) — [AAAI 2014 PDF](https://linqs.org/assets/resources/ramesh-aaai14.pdf)
- PSL has been applied to activity and natural-language features (forum posts) for student performance (survey of MOOC success prediction). (S) — [arXiv 1711.06349](https://arxiv.org/pdf/1711.06349)
- PSL overview slides (Bach, ICML 2017). (S) — [slides](https://cs.brown.edu/people/sbach/files/bach-icml17-slides.pdf)
- (K) Roth & Yih, "A Linear Programming Formulation for Global Inference in Natural Language Tasks", CoNLL 2004 (ACL Anthology W04-2401). It combines local entity and relation classifiers under global constraints via ILP and improved over the local classifiers. — [W04-2401](https://aclanthology.org/W04-2401/)
- (K) Richardson & Domingos, "Markov Logic Networks", Machine Learning 62 (2006), pp. 107–136. — [doi:10.1007/s10994-006-5833-1](https://doi.org/10.1007/s10994-006-5833-1)
- (K) Bach, Broecheler, Huang & Getoor, "Hinge-Loss Markov Random Fields and Probabilistic Soft Logic", JMLR 18 (2017). Inference is convex, so MAP is exact and deterministic. — [JMLR v18](https://jmlr.org/papers/v18/15-631.html)

### Inferences
- PSL fits best here:
  - Convex MAP inference is fast and deterministic.
  - Soft truth values accept cosine and NLI scores directly.
  - Rules can encode label-graph structure, e.g. `Agree(s, A) & Contradicts(A, B) -> !Agree(s, B)`, `Agree(s, child) -> Agree(s, parent)` for prerequisites, and consistency with the answer's overall level.
  - Rule weights can be hand-set or learned from the 19 gold edges plus the 365 overall-level answers, used as distant supervision.
- ILP is the simplest choice for hard constraints only.
- Constrained Viterbi or HMM decoding applies if labels form a sequence or progression (e.g. learning-progression levels).

### Gaps
- I found no application of ILP, MLN or PSL to short-answer *assessment* or label-graph matching specifically. The education uses found are engagement and performance modelling.
- Constrained Viterbi/HMM for student modelling (e.g. BKT variants with constraints) was not searched in this session.
- Exact reported numbers for the PSL MOOC papers were not retrieved.
