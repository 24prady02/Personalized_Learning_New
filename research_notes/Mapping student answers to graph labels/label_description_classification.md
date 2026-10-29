# Label-Description Text Classification (zero/few-shot) for Mapping Student Sentences onto Knowledge-Graph Edge-Logic Labels

Scope: methods that classify a short text by comparing it to natural-language label descriptions (e.g., a misconception's wrong-belief sentence vs its correct-rule sentence, a prerequisite sentence, a learning-level "way" description), with zero or few labelled examples and **no generative LLM at run time**. Small local encoders (MiniLM, MPNet, DeBERTa) are acceptable.

## Q1. Which zero-/few-shot methods use label semantics, and what do they need and report?

### Takeaway
Three families fit: (a) **entailment-as-classification** (NLI cross-encoder scores "student sentence ⟹ label sentence"), (b) **bi-encoder / nearest-label similarity** (embed the sentence and each label description, then take the argmax cosine, optionally with label-description fine-tuning), and (c) **few-shot contrastive fine-tuning of a sentence encoder (SetFit)** once tens of examples exist. All three run deterministically on small local encoders. Label-description *training* (Gao et al. 2023) is the most direct match to "labels are sentences, little or no labelled data".

### Cited Findings

**Entailment-as-classification (NLI cross-encoders)**
- Yin, Hay & Roth (2019), "Benchmarking Zero-shot Text Classification: Datasets, Evaluation and Entailment Approach", EMNLP-IJCNLP 2019, pp. 3914–3923. Frames 0-shot classification as textual entailment: text = premise, label → hypothesis. Covers topic, emotion and situation, and adds a "label-fully-unseen" setting — [ACL Anthology](https://aclanthology.org/D19-1404/)
- Hypotheses were built two ways: label name in a template ("this text is about sports") or the label's WordNet definition. A text is positive if either hypothesis is entailed — [ar5iv](https://ar5iv.labs.arxiv.org/html/1909.00161)
- Label-fully-unseen results (BERT entailment models, no task data). Topic accuracy, emotion and situation weighted F1:
  - MNLI: 37.9 / 22.3 / 15.4
  - FEVER: 40.1 / 24.7 / 21.0
  - RTE: 43.8 / 12.6 / 37.2
  - Ensemble: 45.7 / 25.2 / 38.0 (sum 108.9, vs 101.0 for a Wikipedia-based baseline)
  — [ar5iv](https://ar5iv.labs.arxiv.org/html/1909.00161)
- Label-partially-unseen setting (fine-tuned on seen labels), MNLI v0, seen/unseen: topic 70.9/52.1, emotion 33.4/26.6, situation 74.8/53.4. Unseen-label performance drops sharply — [ar5iv](https://ar5iv.labs.arxiv.org/html/1909.00161)
- **Definitions alone performed poorly.** Words plus definitions gave mixed results: they helped emotion and the ensemble sum (108.9 vs 105.0), but hurt topic/situation for some models. Long, descriptive hypotheses are not automatically better than short ones — [ar5iv](https://ar5iv.labs.arxiv.org/html/1909.00161)
- Laurer, van Atteveldt, Casas & Welbers (2023), "Less Annotating, More Classifying: Addressing the Data Scarcity Issue of Supervised Machine Learning with Deep Transfer Learning and BERT-NLI", *Political Analysis* (doi 10.1017/pan.2023.20). It reformulates any classification task as entailment vs not-entailment via label verbalisation, for few-shot use. Released models include DeBERTa-v3-base-mnli-fever-anli (763,913 NLI pairs) and DeBERTa-v3-large-mnli-fever-anli-ling-wanli (885,242 pairs) — [HF model card](https://huggingface.co/MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli/blob/b3546ea6b0346eb6f8d5d68b13c7dc6d0376b3d7/README.md); [cnb mirror card](https://cnb.cool/ai-models/MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli)
- Laurer et al. (2023/24), "Building Efficient Universal Classifiers with Natural Language Inference" (arXiv 2312.17543). Training on 5 NLI datasets plus 28 non-NLI datasets (389 classes) improved zero-shot by 9.4% over NLI-only models. Caveat: NLI needs one forward pass per class hypothesis, so cost grows with the number of labels — [arXiv](https://arxiv.org/html/2312.17543v2)

**Label-description training / label-semantics pre-training**
- Gao, Ghosh & Gimpel (2023), "The Benefits of Label-Description Training for Zero-Shot Text Classification", EMNLP 2023, pp. 13823–13844. Instead of labelling texts, it fine-tunes on a small set of *descriptions of each label*: label terms, dictionary/encyclopedia entries and short templates. It is **17–19% absolute more accurate than zero-shot** on topic and sentiment datasets, less sensitive to prompt/verbalizer choice, reusable across tasks with the same labels, and can beat supervised out-of-domain models. Code: github.com/lingyugao/LabelDescTraining — [arXiv](https://arxiv.org/pdf/2305.02239); [ACL Anthology](https://aclanthology.org/2023.emnlp-main.853)
- Mueller et al. (2022), "Label Semantic Aware Pre-training for Few-shot Text Classification" (LSAP), ACL 2022, pp. 8318–8334. Secondary pre-training of T5 on sentence–label pairs that are mined automatically. Reports significant few-shot gains on intent (ATIS, Snips, TOPv2) and topic (AG News, Yahoo) tasks. Note: the backbone is generative (T5), though labels are scored rather than freely generated. No exact numbers retrieved — [arXiv](https://arxiv.org/pdf/2204.07128); [ACL Anthology](https://aclanthology.org/2022.acl-long.570)

**Similarity / nearest-label (bi-encoder) and retrieval-style**
- Schopf, Braun & Matthes (2022/23), "Evaluating Unsupervised Text Classification: Zero-shot and Similarity-based Approaches" (arXiv 2211.16285). A systematic comparison of similarity-based and zero-shot (NLI) classification of unseen classes on 4 datasets. It introduces Lbl2TransformerVec, which beats prior unsupervised approaches. Using **SBERT/SimCSE embeddings improves similarity-based classification further** — [arXiv](https://arxiv.org/abs/2211.16285v2)
- Schopf et al., "Semantic Label Representations with Lbl2Vec" (WEBIST 2021/Springer 2023). It needs only a few keywords per class, outperforms a widely used zero-shot approach, and **more precise keywords significantly improve results** — [TUM](https://www.cs.cit.tum.de/sebis/publications/2023/sc23a); [pypi](https://pypi.org/project/lbl2vec)
- Wang, Chi, Zhang & Yang (2023), "PESCO: Prompt-enhanced Self Contrastive Learning for Zero-shot Text Classification", ACL 2023, pp. 14897–14911. Treats classification as retrieving labels for a document query, with prompt-enhanced label text and self-training via contrastive learning on unlabelled data. Reports **98.5% on DBpedia with no labelled data**; per-dataset tables not retrieved — [ACL Anthology](https://aclanthology.org/2023.acl-long.832); [arXiv](https://arxiv.org/abs/2305.14963v1)

**Few-shot Siamese/contrastive (SetFit)**
- Tunstall, Reimers, Jo, Bates, Korat, Wasserblat & Pereg (2022), "Efficient Few-Shot Learning Without Prompts" (SetFit), arXiv 2209.11055. Contrastive Siamese fine-tuning of a Sentence Transformer on generated pairs, then a classification head (e.g., logistic regression). No prompts and no LLM — [arXiv](https://arxiv.org/abs/2209.11055)
- Pair generation: for each class, R positive pairs (same class) and R negative pairs (different class), default R=20. K examples yield up to K(K−1)/2 pairs — [arXiv HTML](https://arxiv.org/html/2209.11055v1)
- Results at 8 examples/class:

  | Model | SST-5 | AmazonCF | CR | Emotion | Enron | Avg |
  |---|---|---|---|---|---|---|
  | SetFit-MPNet (110M) | 43.6 | 40.3 | 88.5 | 48.8 | 90.1 | 62.3 |
  | T-Few 3B | 55.0 | 19.0 | 92.1 | 57.4 | 93.1 | 63.4 |
  | Plain fine-tune | 33.5 | 9.2 | 58.8 | 28.7 | 85.0 | 43.0 |

  — [arXiv HTML](https://arxiv.org/html/2209.11055v1)
- Further SetFit numbers:
  - At 64 examples/class: SetFit 75.3 avg vs T-Few 3B 70.3.
  - RAFT: SetFit-RoBERTa (355M) 71.3 vs GPT-3 62.7.
  - SetFit-MiniLM (15M) averages 60.3 with 123× fewer inference FLOPs than T-Few.
  - Training takes about 30 s (~$0.025) on one V100-class GPU.
  — [arXiv HTML](https://arxiv.org/html/2209.11055v1)

**Extreme multi-label with label text (for large label inventories)**
- DECAF (Mittal et al. 2021) embeds instances and label text separately, shortlists labels with a ranker, then applies label attention. ECLARE (Mittal et al., WWW 2021) adds a **label–label correlation graph**: a text encoder (LTE), a graph-augmented label encoder (GALE) and a per-label refinement vector, fused by attention. It beats DECAF and X-Transformer on LF-AmazonTitles-131K and LF-WikiSeeAlsoTitles-320K. SiameseXML learns joint Siamese label/instance embeddings — [Review of XMC](https://arxiv.org/pdf/2302.05971); [ECLARE arXiv](https://arxiv.org/pdf/2108.00261); [DECAF ar5iv](https://ar5iv.labs.arxiv.org/html/2108.00368)

**Education-domain analogue**
- Eedi (2026), "Misconception Diagnosis From Student-Tutor Dialogue: Generate, Retrieve, Rerank" (arXiv 2602.02414). An LLM proposes a misconception, an embedding model retrieves the nearest tutor-defined label from a library, and an LLM reranks. **Retrieval degrades when student responses are short or symbolic.** Dataset: 922 dialogues. Uses an LLM at run time, so it does not meet the constraint, but the embedding-retrieval stage is the reusable part — [arXiv](https://arxiv.org/pdf/2602.02414); [Eedi blog](https://www.eedi.com/news/misconception-diagnosis-from-student-tutor-dialogue-generate-retrieve-rerank)
- A CEUR workshop paper on 20,964 Eedi math responses reports that BERT detects only 57% of misconceptions hidden behind correct answers, and recommends keeping a teacher in the loop — [CEUR](https://ceur-ws.org/Vol-4282/short7.pdf)

### Inferences
- For the knowledge graph, the label "description" already exists as a sentence (wrong belief, correct rule, prerequisite statement, "way" description). That is exactly the hypothesis in Yin et al. and the training text in Gao et al. A pipeline could:
  1. Zero-shot: use a bi-encoder (MiniLM/MPNet) to shortlist the top-k edge sentences by cosine.
  2. Zero-shot: rerank the shortlist with an NLI cross-encoder (DeBERTa-v3-base-mnli), using P(entail) − P(contradict).
  3. As labelled examples accrue: fine-tune with SetFit, or do Gao-style label-description training by adding paraphrases of each edge sentence as training data.

  All steps are deterministic at inference and need no generative LLM.
- Yin et al.'s finding that definitions alone underperform short label names suggests keeping edge sentences short and canonical. A single long description may need to be split into several hypotheses, with the max score taken (inference, not tested on educational data).
- The NLI cross-encoder costs one pass per label. Bi-encoder shortlisting first keeps it tractable when a concept has many edges.

### Gaps
- No exact accuracy numbers were retrieved for LSAP, Laurer et al. (Political Analysis) few-shot curves, the Lbl2TransformerVec tables, or PESCO beyond DBpedia.
- TARS (Halder et al., COLING 2020, "Task-Aware Representation of Sentences") and label-description attention models (e.g., LSAN/LEAM) are known from background knowledge but were not verified in this session.
- No benchmark found that evaluates these methods on short student sentences against KG edge sentences. Transfer to education is untested.

## Q2. Which methods are deterministic, LLM-free at inference, and work with tens to hundreds of labels/examples?

### Takeaway
NLI cross-encoders (DeBERTa-v3), bi-encoder nearest-label (SBERT/MiniLM/MPNet), Lbl2Vec-style similarity, label-description training and SetFit are all encoder-only (15M–435M parameters) and deterministic at inference. SetFit is the best-documented option for 8–64 labelled examples per class. LSAP (T5) and Eedi's pipeline rely on generative models.

### Cited Findings
- SetFit-MPNet is 110M parameters (~420 MB) and SetFit-MiniLM 15M (~70 MB), vs 11.4 GB for T0-3B. With 8 examples/class SetFit is roughly on par with 3B-parameter T-Few (62.3 vs 63.4 avg), and it wins at 64/class — [arXiv HTML](https://arxiv.org/html/2209.11055v1)
- The NLI zero-shot classifiers are DeBERTa-v3 base/large encoders. Cost scales linearly with the number of candidate labels (one pass per hypothesis) — [arXiv 2312.17543](https://arxiv.org/html/2312.17543v2)
- Label-description training needs **no labelled task texts**, only label descriptions, and is robust to template choice — [arXiv](https://arxiv.org/pdf/2305.02239)
- Similarity-based classification with SBERT/SimCSE needs only label keywords or descriptions, and improves with more precise label text — [arXiv 2211.16285](https://arxiv.org/abs/2211.16285v2); [TUM Lbl2Vec](https://www.cs.cit.tum.de/sebis/publications/2023/sc23a)
- LSAP uses a T5 (generative) backbone, so it is not suitable if any generative model is excluded at run time — [arXiv](https://arxiv.org/pdf/2204.07128)

### Inferences
- Recommended stack under the constraints:
  1. Zero labels: MiniLM/MPNet bi-encoder plus a DeBERTa-v3-base NLI reranker.
  2. Tens of labels: SetFit on the same MPNet body, with each edge sentence and its paraphrases as extra "anchor" examples.
  3. Hundreds of labels: fine-tune the cross-encoder on (student sentence, edge sentence, entail/contradict/neutral) triples.
- Determinism: encoder inference is deterministic given fixed weights and eval mode. Only GPU nondeterminism in floating point is a minor concern (general knowledge, not from a source).

### Gaps
- No head-to-head study was found comparing SetFit, NLI and label-description training on the same tiny educational dataset.

## Q3. Contrastive label pairs that differ by negation or a key word (wrong belief vs correct rule)

### Takeaway
This is the biggest risk. Standard sentence embeddings (SBERT/MPNet) give high cosine similarity to minimal negation pairs, so nearest-label matching will confuse "wrong belief" and "correct rule". Remedies with evidence:
- An **NLI cross-encoder**, which explicitly models contradiction, used as the decision step.
- **Negation-aware fine-tuning** of the bi-encoder (NegMPNet, trained with negated sentences as contrastive negatives).
- **SimCSE-style hard negatives** drawn from NLI contradictions.
- **SetFit pairs that deliberately pair** wrong-belief and correct-rule examples as negatives.

Negation benchmarks show even large models remain brittle.

### Cited Findings
- Anschütz et al. found that SBERT and S³BERT give moderately high similarity to "The man likes cheese" vs "The man doesn't like cheese". Another source reports that minimal negation pairs have high cosine similarity despite contradictory meaning — [search summary; SBERT studies (arXiv 2206.07023)](https://arxiv.org/pdf/2206.07023); [arXiv 2507.12782](https://arxiv.org/pdf/2507.12782v1) (summary-level; not independently read in full)
- Anschütz, Miguel Lozano & Groh (2023), "This is not correct! Negation-aware Evaluation of Language Generation Systems", INLG 2023.
  - Data: the CANNOT dataset, 68,780 balanced negated/paraphrase pairs built with a rule-based negator (spaCy + LemmInflect).
  - Training: fine-tunes all-mpnet-base-v2 for 1 epoch with MultipleNegativesRankingLoss, so negated sentences act as contrasts. The result is **NegMPNet** (HF: tum-nlp/NegMPNet).
  - Negation sensitivity on DEMETR critical negation: **0.65 vs 0.14** for base MPNet. Antonym: 0.24 vs 0.07.
  - Cost: STS average falls 80.28 → 77.58 and MTEB average 58.78 → 57.16, while MTEB classification rises 65.07 → 70.83.
  — [ar5iv](https://ar5iv.labs.arxiv.org/html/2307.13989); [HF](https://huggingface.co/tum-nlp/NegMPNet)
- Gao, Yao & Chen (2021), SimCSE (EMNLP 2021). The supervised version uses **NLI contradiction sentences as hard negatives**, which raises STS from 84.9 to 86.2 in its ablation. This is the standard recipe for pushing contradictory near-paraphrases apart — [arXiv](https://arxiv.org/pdf/2104.08821)
- García-Ferrero et al. (2023), "This is not a Dataset: A Large Negation Benchmark to Challenge Large Language Models", EMNLP 2023. Contains 381,300 WordNet-derived sentences. LLMs do well on affirmative sentences but struggle on negated ones and lean on superficial cues. Fine-tuning helps only partly. Zero-shot accuracy is about 50–66% (e.g., Flan-T5-xxl 66.1) — [arXiv](https://arxiv.org/abs/2310.15941); [Papers with Code](https://astro.paperswithcode.com/paper/this-is-not-a-dataset-a-large-negation)
- ScoNe-NLI (She et al., ACL 2023 short) builds contrast sets of six examples with up to two negations, where zero, one or both negations affect the NLI label. It is a benchmark for checking whether an entailment model handles scope correctly — [ACL virtual](https://virtual2023.aclweb.org/paper_P4433.html)
- CONDAQA (Ravichander et al., EMNLP 2022) is a contrastive negation reading-comprehension dataset with over 200 negation cues — [arXiv](https://arxiv.org/pdf/2211.00295)
- SetFit's negative pairs are sampled from different classes. Sampling is random by default, so hard pairs are not guaranteed — [arXiv HTML](https://arxiv.org/html/2209.11055v1)

### Inferences
- Treat each misconception as a **paired label** (wrong belief W, correct rule C). Decide with an NLI cross-encoder score such as entail(s, W) − entail(s, C), or contradict(s, C), rather than raw cosine. NLI models are trained to separate entailment from contradiction, while cosine is known to collapse negation pairs.
- If a bi-encoder is used for retrieval, (a) swap in NegMPNet or fine-tune MiniLM with the CANNOT recipe, and (b) in SetFit, **force W/C hard-negative pairs**: student sentences labelled W paired with the C text, and vice versa. Retrieve both W and C together, and let the pair-level decision step choose between them.
- Data augmentation: the CANNOT rule-based negator can auto-generate C↔W variants and paraphrases to enlarge tiny training sets.
- Validate on a ScoNe-style contrast set built from the graph's own W/C pairs before deployment.

### Gaps
- No paper was found that specifically studies classification where *label pairs* are negations of each other (contrastive label-pair classification). Evidence is indirect, from negation-aware embeddings and NLI benchmarks.
- Educational misconception texts often differ by a key word or quantity (e.g., "larger denominator means larger fraction") rather than an explicit "not". Antonym sensitivity remains weak even in NegMPNet (0.24), and no source evaluates such domain-specific minimal pairs.

## Q4. Adapting to labels that form a graph or hierarchy

### Takeaway
Hierarchical text classification (HTC) injects the label graph into the encoder or the label representations, through GNN or Tree-LSTM label encoders (HiAGM) or contrastive hierarchy-guided encoders (HGCLR). These methods are fully supervised and give gains of 1–2 F1 points over BERT on standard benchmarks. For zero/few-shot use, the more relevant line is **entailment over the hierarchy** (Bhambhoria et al. 2023) and **label-graph-augmented label embeddings** (ECLARE). Few-shot HTC work increasingly uses retrieval or LLMs.

### Cited Findings
- HiAGM (Zhou et al., ACL 2020, "Hierarchy-Aware Global Model") encodes the label hierarchy with structure encoders and fuses text with hierarchy through multi-label attention. Micro/Macro-F1:
  - WOS 85.82/80.28
  - RCV1-V2 83.96/63.35
  - NYT 74.97/60.83
  - BERT+HiAGM on WOS: 86.04/80.19
  — [HTLA, arXiv 2409.00788](https://arxiv.org/pdf/2409.00788)
- HGCLR (Wang et al., ACL 2022) embeds the hierarchy directly into the text encoder via contrastive learning with hierarchy-guided positive samples. Micro/Macro-F1:
  - WOS 87.11/81.20 (+1.5 / +2.1 over BERT)
  - RCV1-V2 86.49/68.31
  - NYT 78.86/67.96
  — [arXiv 2203.03825](https://arxiv.org/pdf/2203.03825); [HTLA table](https://arxiv.org/pdf/2409.00788)
- A later paper (HBGL, arXiv 2205.02613) argues that HGCLR gives negligible improvement over HiMatch, and reports +2.23/+2.76 Macro-F1 over HGCLR on NYT/RCV1-V2 by exploiting global and local hierarchies — [arXiv](https://arxiv.org/pdf/2205.02613). Gains in this line are small and contested.
- Bhambhoria, Chen & Zhu (2023), "A Simple and Effective Framework for Strict Zero-Shot Hierarchical Classification", ACL 2023 short. Recasts hierarchical datasets as long-tail leaf prediction and uses an **entailment–contradiction model trained only on NLI** (strict zero-shot), with no parameter updates. The approach also combines this with LLMs. A third-party aggregator lists WOS depth-2 accuracy 61.78; unverified — [arXiv](https://arxiv.org/pdf/2305.15282); [ACL Anthology](https://aclanthology.org/2023.acl-short.152)
- ECLARE uses a label–label correlation graph to build graph-augmented label embeddings from label text. This helps rare labels — [ECLARE](https://arxiv.org/pdf/2108.00261)
- "Retrieval-style In-Context Learning for Few-shot Hierarchical Text Classification" (arXiv 2406.17534) is a few-shot HTC approach based on retrieval plus an LLM. It is noted as a direction, but it needs an LLM — [arXiv](https://arxiv.org/pdf/2406.17534)

### Inferences
- The knowledge graph is not a tree. Edges carry typed semantics (misconception-of, prerequisite-of, level-way), so HTC tree methods transfer only partly. The cheapest adaptations:
  1. **Graph-constrained candidate sets.** Score only the edge sentences attached to the concept or question in context. This shrinks NLI cost and removes distractors.
  2. **ECLARE-style label smoothing over the graph.** Average a label's embedding with its neighbours' (e.g., one GCN-style propagation step over edge-sentence embeddings) for rare labels.
  3. **Hierarchical decoding.** Pick the concept node first, then the edge type, then W vs C, with entailment at each step as in Bhambhoria et al.
- Supervised HTC (HiAGM/HGCLR) needs thousands of labelled documents, so it does not fit tiny data. Its hierarchy-guided contrastive positives could be borrowed for SetFit pair generation: treat siblings under the same concept as semi-hard negatives.

### Gaps
- No paper was found on zero/few-shot classification against a typed educational knowledge graph whose labels are edge sentences.
- Original HiAGM and HGCLR numbers were taken from a later paper's comparison table (HTLA), not from the original PDFs.
- The Bhambhoria et al. accuracy figures come from an aggregator and are unverified. The internal score-propagation mechanism was not confirmed.
