# Mapping Student Free Text onto a Misconception Catalogue

Constraint context used for "fit" notes: intro Java, no LLM at run time, deterministic preferred, about 365 student answers that have only overall level labels (no per-misconception labels).

## Eedi "Mining Misconceptions in Mathematics" (Kaggle, 2024)

### Takeaway
This competition is the closest analogue to "map text onto a catalogue of described misconceptions". The input is a math question plus a wrong multiple-choice distractor, and the output is a ranking over a bank of about 2,587 misconception descriptions, scored by MAP@25. Every top solution used a fine-tuned bi-encoder retriever followed by a reranker, with LLMs (Qwen 14B–32B) as backbones and LLM-generated synthetic data or rationales. The parts that carry over without an LLM at run time are the frozen small embedding retriever and the trick of enriching the catalogue entries with longer explanations written offline. The 2nd-place efficiency-prize solution showed this works with untuned all-MiniLM-L6-v2.

### Cited Findings
- Task: given a distractor (wrong MC answer) and a list of misconception descriptions, predict which misconceptions match. Many test-set misconceptions were unseen during training — [Eedi news](https://www.eedi.com/news/from-wrong-answers-to-real-insights-how-we-used-a-kaggle-challenge-to-map-student-misconceptions)
- Label bank size: 2,587 math misconceptions — [Silver-medal repo, DaoyuanLi2816](https://github.com/DaoyuanLi2816/Kaggle-Eedi-Mining-Misconceptions-in-Mathematics-Silver-Medal)
- Metric: MAP@25 (up to 25 ranked predictions; a hit at rank n scores 1/n) — [search summary of Eedi/Kaggle materials](https://github.com/jimzijun/Eedi---Mining-Misconceptions-in-Mathematics) (secondary; the Kaggle page itself was not fetched)
- 1st place (Team MTH 101, Raja Biswas): two-stage retrieve-and-rerank. Stage 1 used two Qwen models with LoRA and contrastive learning. Stage 2 used Claude-generated short student rationales to rerank the candidates. Trained on about 10k synthetic plus 1.8k real examples — [Eedi news](https://www.eedi.com/news/from-wrong-answers-to-real-insights-how-we-used-a-kaggle-challenge-to-map-student-misconceptions)
- 2nd place (Yonekawa, Wang, Okuyama, Hong): chain-of-thought prompting with Qwen2.5, synthetic data to augment misconceptions, listwise reranking of the top 25, and post-training quantization — [Eedi news](https://www.eedi.com/news/from-wrong-answers-to-real-insights-how-we-used-a-kaggle-challenge-to-map-student-misconceptions)
- 3rd place (Waseda Pochi): Qwen2.5-14B embeddings for retrieval, Qwen2.5-32B reranking, QLoRA through FlagEmbedding, and a scaling factor that boosts scores of misconceptions unseen in training to match the test distribution — [Eedi news](https://www.eedi.com/news/from-wrong-answers-to-real-insights-how-we-used-a-kaggle-challenge-to-map-student-misconceptions)
- Efficiency prize 1st (Dipam Chakraborty): Qwen2.5-0.5B with prefix caching. Missing data was generated with Claude 3.5 and GPT-4o. Final model was a SLERP merge of 6 models, each trained about 2.5 h on an RTX 4080 — [Eedi news](https://www.eedi.com/news/from-wrong-answers-to-real-insights-how-we-used-a-kaggle-challenge-to-map-student-misconceptions)
- Efficiency prize 2nd (Ryuji Sakata): all-MiniLM-L6-v2 (22.7M params) with no fine-tuning. Gains came from better query construction, and adding misconception explanations (generated offline with Qwen2.5-32B) to the catalogue entries "improved retrieval performance significantly" — [Eedi news](https://www.eedi.com/news/from-wrong-answers-to-real-insights-how-we-used-a-kaggle-challenge-to-map-student-misconceptions)
- Silver-medal pipeline: a bi-encoder LoRA retriever (Qwen2.5-32B-Instruct, 4-bit) with iterative self-mined hard negatives, then a generative listwise reranker over the top 5. Retriever MAP@25 on a held-out fold was 0.4238, with Recall@1/10/25/50/100 of 0.30/0.69/0.81/0.90/0.94. Final private LB was about 0.50 (silver, top 5%) — [DaoyuanLi2816 repo](https://github.com/DaoyuanLi2816/Kaggle-Eedi-Mining-Misconceptions-in-Mathematics-Silver-Medal)
- On a Banking77 ablation in the same repo, a zero-shot backbone scored MAP@25 0.069, random negatives 0.788, and self-mined hard negatives 0.838. Contrastive fine-tuning with hard negatives is therefore the main driver — [DaoyuanLi2816 repo](https://github.com/DaoyuanLi2816/Kaggle-Eedi-Mining-Misconceptions-in-Mathematics-Silver-Medal)
- A 4th-place deck describes using an LLM to generate a misconception hypothesis from the question and distractor, then using it as the retrieval query, plus synthetic data generation — [Speakerdeck 4th place (via search snippet)](https://speakerdeck.com/rist/4th-place-solution-eedi-mining-misconceptions-in-mathematics); 5th-place code is at [ebinan92/Eedi-5th-solution](https://github.com/ebinan92/Eedi-5th-solution) (not read)

### Inferences
- Top private-LB MAP@25 was roughly 0.5–0.65 (silver was about 0.50; the winning score was not verified), even with 32B models and thousands of examples. Fine-grained catalogue mapping is hard, so a 365-answer Java setting should expect top-k suggestions rather than a single reliable label.
- Run-time-LLM-free pieces that transfer:
  - A frozen sentence-embedding retriever (MiniLM or similar).
  - Catalogue enrichment written offline: longer explanations, example wrong answers and paraphrases per misconception, created once by humans or by an LLM and then frozen.
  - Query construction (question + student answer).
  - Score calibration for unseen labels.
- Deterministic inference is possible because embedding plus cosine similarity is deterministic. Fine-tuning needs per-misconception labels, which the 365 overall-level answers do not have.
- Eedi's input is a distractor (a short answer), not a free-text explanation. Java explanations are longer and closer to the MAP or EiPE setups.

### Gaps
- The 1st-place final MAP@25 and the official winner writeup were not retrieved, and neither were the exact train size (my recollection is about 1,869 questions / 4 distractors each, but this is unverified) or the full leaderboard.
- I could not find an MAP@25 for a pure untuned-embedding baseline on Eedi data.

## MAP "Charting Student Math Misunderstandings" (Kaggle, 2025)

### Takeaway
Students choose an MC answer and write a free-text explanation. Models predict a `Category:Misconception` label with 6 categories × about 35 misconceptions, about 65 combined classes, scored by MAP@3. The training data covers only 15 questions, and the test set uses the same questions, so this is a closed-set, per-question classification problem. Winners fine-tuned 14B–32B LLMs as classifiers (private LB about 0.948). A DeBERTa-v3-large classifier reached about 0.91–0.92, but its cross-question CV was only 0.29, so it barely generalizes to unseen questions. The category scheme is a useful template for separating "states the correct rule" from "states the misconception".

### Cited Findings
- Task: given question, chosen answer and free-text explanation, (1) judge whether the answer is correct, (2) classify the explanation as Correct / Misconception / Neither, and (3) identify the misconception type, e.g. "Longer_is_bigger" — [Zenn (Matsuo Inst. team)](https://zenn.dev/mkj/articles/1f374627377474)
- Labels: 6 categories (True_Correct, True_Neither, True_Misconception, False_Correct, False_Neither, False_Misconception) × 35 misconception types or NA. MAP@3 metric. One solution deduplicated to 35,960 rows. Private-LB medal cutoffs: gold ≈0.94792, silver ≈0.94625, bronze ≈0.94579 — [Zenn](https://zenn.dev/mkj/articles/1f374627377474)
- Top solutions:
  - 1st: Qwen3-32B + GLM-Z1-32B with suffix classification over candidate labels.
  - 2nd: merged 65 classes into 37, limited candidates per question, added synthetic data.
  - 3rd: Qwen2.5 14/32/72B with per-question label reduction.
  - 4th: Qwen3-Reranker-8B pointwise reranker with distillation.
  - 5th: Gemma2-9B / Qwen / DeepSeekMath ensemble.
  - The source does not give individual scores — [Zenn](https://zenn.dev/mkj/articles/1f374627377474)
- The Zenn team (about 9th): Qwen2.5-32B + DeepSeek-R1-Distill-32B with QLoRA, with the 65 labels added as special tokens. Ensemble scored 0.948 private; single models 0.944–0.946. A minimal prompt worked best. Rerankers and 70B models did not help — [Zenn](https://zenn.dev/mkj/articles/1f374627377474)
- DeBERTa-v3-large 5-fold classifier (65 classes, training data has only 15 unique questions):
  - GroupKFold-by-question CV MAP@3: 0.2925
  - Public / private LB: 0.919 / 0.911 single model; 0.931 / 0.924 fold ensemble.
  - The card notes test shares question IDs with train, which inflates LB — [HF model card](https://huggingface.co/lyixuan0718/map-deberta-v3-large-5fold)
- MiRAGE (Van Duc et al., arXiv 2511.01182, 2025) on the MAP dataset: retrieval + CoT reasoning + reranking + ensemble, MAP@1/3/5 = 0.82/0.92/0.93. Its embedding-only retrieval module (MathBERT) alone reached MAP@3 0.83. Labels are defined as answer correctness × explanation quality (Correct / Misconception / Neither) × misconception type, with misconception = NA unless the explanation shows a specific identifiable error — [arXiv html](https://arxiv.org/html/2511.01182v1)

### Inferences
- The 0.29 grouped-CV versus 0.91 same-question LB gap is the most important number here for the Java project. Supervised classifiers on a small number of items learn item-specific surface cues. With 365 answers, per-item models will overfit unless the questions are fixed and reused.
- The MathBERT retrieval-only result (MAP@3 0.83) suggests embedding-only matching can get within about 10 points of LLM pipelines when the candidate set per question is small (a few misconceptions per question). Restricting candidates per question was a common winning trick, and it is directly transferable: map each Java item to its 2–5 plausible catalogue misconceptions.
- The 2-axis scheme (Correct / Misconception / Neither, crossed with answer correctness) maps naturally onto "correct rule" versus "misconception" nodes.

### Gaps
- No official Kaggle winner writeups were read directly. Per-team private scores for ranks 1–5 were not found.
- The exact public training-row count was not found (about 36k after dedup, per one team).

## Programming-education misconception catalogues and automated detection

### Takeaway
Java/CS1 misconception catalogues with textual descriptions exist; progmiscon.org is the best fit, with 200+ entries including Java, each linked to the language spec and with refutation texts. Automated detection work, however, focuses on student code (mutant-trained BERT classifiers, AST embeddings, clustering), not on free-text explanations. EiPE autograding of explanations exists but grades correctness, not which misconception. I found no published system that NLI-matches student explanations against a programming misconception catalogue, so this appears to be an open gap.

### Cited Findings
- Chiodini, Moreno Santos, Gallidabino, Tafliovich, Santos, Hauswirth, "A Curated Inventory of Programming Language Misconceptions", ITiCSE 2021, pp. 380–386:
  - Defines a PL misconception as a statement refutable purely from language syntax/semantics.
  - Links each misconception to the language spec, to textbooks that may trigger it, to research papers, and to support for educational platforms — [USI PDF](https://luce.si.usi.ch/assets/publications/chiodiniCuratedInventoryProgramming2021.pdf); [USI record](https://search.usi.ch/en/publications/67486)
- Companion EC-TEL 2021 demo "Conceptual checks for programming teachers": students judge true/false statements about PL concepts, built on refutation texts. The inventory had more than 200 misconceptions at the time — [USI record](https://search.usi.ch/en/publications/67488)
- Steveny et al. (UCLouvain), "Feedback with BERT: When Detecting Students' Misconceptions Becomes Automatic", RKDE workshop 2024:
  - Multi-label BERT classifier trained on mutants of real student submissions, with each mutation injecting one of 14 misconceptions.
  - F1 up to 72.9% on real student mistakes.
  - Input is code, not explanations — [UCLouvain record](https://research.dial.uclouvain.be/handle/2078.5/256585)
- Prasad, Greenman, Nelson, Krishnamurthi, "Conceptual Mutation Testing for Student Programming Misconceptions" (arXiv 2401.00021, 2024): clusters failing student tests into conceptual mutants, which outperformed expert-written ones — [arXiv](https://arxiv.org/pdf/2401.00021)
- Hoq et al. (EDM 2025, arXiv 2505.10913): an explainable AST embedding model (Subtree-based Attention Neural Network) flags logical errors in student code and links them to misconceptions. They argue earlier association-rule methods fail for general-purpose tasks — [arXiv](https://arxiv.org/html/2505.10913v1)
- Shi et al. (LAK 2021, arXiv 2103.04448): code embeddings plus clustering of incorrect block-based submissions surfaced misconceptions experts had missed (discovery, not catalogue mapping) — [arXiv](https://arxiv.org/abs/2103.04448v1)
- Fowler, Chen, Azad, West, Zilles, "Autograding 'Explain in Plain English' questions using NLP", SIGCSE 2021:
  - Described as the first EiPE autograder, deployed in a large CS1.
  - 87–89% accuracy on exam questions, comparable to trained TAs.
  - Includes error analysis of misgraded answers — [Illinois experts page](https://experts.illinois.edu/en/publications/autograding/); [pub page](https://lagrange.mechse.illinois.edu/pubs/FoChAzWeZi2021/)
- Smith & Zilles, "Evaluating LLM Code Generation as an Autograding Mechanism for EiPE Questions", SIGCSE 2024 (arXiv 2311.14903 "Code Generation Based Grading"): GPT-4 generates code from the student's explanation and unit tests grade it. Agreement with humans was measured, and the method was more lenient than humans on low-level descriptions. It needs an LLM at run time — [arXiv](https://arxiv.org/pdf/2311.14903); [Illinois](https://experts.illinois.edu/en/publications/evaluating-large-language-model-code-generation-as-an-autograding/)
- Denny co-authored "Explaining Code with a Purpose" (ITiCSE 2024), which extends the code-generation EiPE approach — [search result via arXiv 2403.06050](https://arxiv.org/html/2403.06050v1)

### Inferences
- The Fowler et al. 2021 grader is the most constraint-compatible EiPE precedent (classical NLP, no LLM). From memory and unverified, it used per-question classifiers on n-gram features trained on hundreds of labelled responses per question. That would need per-question labels the project lacks.
- The mutant-based training idea (synthesise labelled examples per misconception, then train a small classifier) transfers to text: write or offline-generate example explanations for each catalogue misconception and its correct-rule counterpart, then train or tune a small deterministic model or embedding index on them.
- progmiscon entries are structured as a misconception statement plus a correct explanation/refutation, which gives exactly the "wrong belief + correct rule" pairs needed for contrastive matching.

### Gaps
- I could not verify by fetching Sorva's misconception list (Sorva 2012 dissertation, about 160 novice misconceptions), Qian & Lehman 2017 (ACM TOCE review), or Kaczmarczyk et al. 2010 (SIGCSE, misconceptions about memory/objects/loops via interviews). Treat their details as unverified recollection.
- I found no paper using NLI/entailment or cross-encoders to match CS student explanations against a misconception catalogue. Searches returned none.
- Data sizes and features for Fowler et al. 2021 were not in the abstract; the full PDF was not read.

## Science/math misconception detection in short answers

### Takeaway
Pre-LLM short-answer misconception work is either unsupervised discovery (clustering embeddings) or small rule-based or classifier pilots on one item. Recent Eedi-derived work shows fine-tuned classifiers miss many "hidden" misconceptions and produce many false alarms at realistic prevalence.

### Cited Findings
- Michalenko, Lan, Baraniuk, "Data-Mining Textual Responses to Uncover Misconception Patterns" (L@S 2017; arXiv 1703.08544): AP Biology short answers from OpenStax Tutor are embedded with Word2Vec, GloVe and an LSTM, then a probabilistic model fitted by MCMC discovers misconceptions with no instructor-provided list. It is reported to classify well whether a response shows a misconception — [arXiv](https://arxiv.org/pdf/1703.08544)
- Becker, Kahanda, Kazi, ASEE 2021 WIP, "Detection of Student Misconceptions of Electrical Circuit Concepts in a Short Answer Question Using NLP":
  - Rule-based lexical spaCy matcher plus a BERT pilot.
  - 185 responses to one question, checked for 7 misconceptions.
  - Results described only as "very promising"; no numbers on the page — [UNF](https://digitalcommons.unf.edu/unf_faculty_publications/1180)
- Imran & Bulathwela, "The Correct Answer Trap" (AIED PEAF workshop 2026, arXiv 2606.23205), on 20,964 Eedi responses:
  - Targets hidden misconceptions behind correct answers.
  - Fine-tuned classifiers detect only 57%; an open-weight reasoning model detects 84%.
  - At realistic prevalence, false alarms outnumber true detections about 8:1.
  - Proposes a rubric separating answer correctness from method validity and a detect-verify-escalate design with follow-up diagnostic questions — [arXiv](https://arxiv.org/abs/2606.23205)

### Inferences
- The 8:1 false-alarm finding argues for using catalogue matches as flags for teacher review or follow-up items, not as authoritative labels, especially with small data.
- The rule-based spaCy approach on 185 responses is the closest data-size analogue to 365 answers and is fully deterministic. Keyword/pattern rules per misconception are a viable baseline.

### Gaps
- No misconception-labelled version of SciEntsBank/Beetle was found in this search. SemEval-2013 Task 7 labels (correct / partially correct / contradictory / irrelevant / non-domain) are known to me from training, unverified here; they do not name specific misconceptions.
- No NAEP misconception-detection paper was retrieved.

## Separating "states the misconception" from "states the correct rule" when wording overlaps

### Takeaway
None of the sources solved this with pure lexical/embedding similarity. Winning systems get the separation from supervised training on labelled contrasts: MAP's Correct vs Misconception categories, hard negatives, and rerankers. Without per-misconception labels and without a run-time LLM, the most defensible approach is contrastive scoring. Score each answer against both the misconception text and its correct-rule counterpart, and decide on the margin, using a small cross-encoder/NLI model or rules for negation and direction.

### Cited Findings
- MAP explicitly labels explanation quality as Correct / Misconception / Neither, separate from answer correctness, and sets misconception to NA unless the explanation shows a specific error. Models learn the distinction from about 36k labelled rows — [MiRAGE](https://arxiv.org/html/2511.01182v1); [Zenn](https://zenn.dev/mkj/articles/1f374627377474)
- Self-mined hard negatives raised retrieval MAP@25 from 0.788 (random negatives) to 0.838, and zero-shot embeddings scored 0.069 on that intent task. Untuned embeddings separate near-synonymous labels poorly — [DaoyuanLi2816 repo](https://github.com/DaoyuanLi2816/Kaggle-Eedi-Mining-Misconceptions-in-Mathematics-Silver-Medal)
- Eedi winners added a reranking stage (Qwen 32B, or Claude-generated rationales) after embedding retrieval to fix ordering among close candidates — [Eedi news](https://www.eedi.com/news/from-wrong-answers-to-real-insights-how-we-used-a-kaggle-challenge-to-map-student-misconceptions)
- progmiscon pairs each misconception with refutation/correct-semantics text, i.e. it supplies the correct-rule counterpart — [USI PDF](https://luce.si.usi.ch/assets/publications/chiodiniCuratedInventoryProgramming2021.pdf)
- "The Correct Answer Trap" separates answer correctness from method validity in its rubric — [arXiv](https://arxiv.org/abs/2606.23205)

### Inferences
These are design suggestions, not findings from the sources.
- Bi-encoder cosine similarity will score "== compares object contents" and "== does not compare object contents" almost identically. Recommended setup:
  1. Retrieve candidates with embeddings, restricted per question.
  2. Run an off-the-shelf NLI cross-encoder (e.g. a DeBERTa MNLI model, deterministic in eval mode) for entailment versus contradiction against both the misconception statement and the correct-rule statement.
  3. Assign the misconception only if entail(misconception) − entail(correct rule) exceeds a threshold tuned on a small hand-labelled subset (say 50–100 of the 365).
- Add deterministic negation/polarity rules for key Java contrasts (== vs equals, pass-by-value, integer division, String immutability).
- The overall level labels on the 365 answers can serve only as weak validation: misconception flags should correlate with lower levels.

### Gaps
- I found no published evaluation of NLI-based correct-vs-misconception discrimination on student programming explanations. The recommended pipeline is untested in the literature reviewed.
