# ASAG and Explanation Assessment by Alignment to Rubric Items, Reference Answers, Concept Maps and Knowledge Graphs

Context: intro Java programming explanations, about 365 answers with overall labels, 19 with edge-level gold, no generative LLM at run time. "Per-element" means the method produces a judgement for each rubric item, facet or graph edge, not only a single score.

## Q1. Graph-alignment ASAG (Mohler 2011, Ramachandran 2015, Sultan 2016 and follow-ups)

### Takeaway
Classic graph-alignment ASAG aligns the reference answer to the student answer (dependency-graph nodes, word-order graph patterns, or word-aligner pairs) and turns that alignment into features for one overall score. The alignment step does produce per-node or per-word matches as an intermediate, which can be reused as per-element judgements. Results on the Mohler Data Structures (CS) dataset rose from r=0.52 (Mohler 2011) to about r=0.59–0.63 (Sultan 2016), without any LLM. Mohler's node-alignment scorer was trained on only "a small set of manually aligned graphs", which is close to our 19-edge-gold setting.

### Cited Findings
- **Mohler, Bunescu & Mihalcea (2011), ACL, pp. 752–762.** Three-stage pipeline:
  - (1) Every node in the instructor's dependency graph is scored against every node in the student's graph, using lexical, semantic and syntactic features of the node pair and of their subgraphs. The scoring function is trained with the averaged perceptron "on a small set of manually aligned graphs".
  - (2) Hungarian algorithm for the optimal bipartite matching, plus "question demoting", which discounts words copied from the question.
  - (3) SVMRank or SVR combines 8 alignment features with bag-of-words (BOW) similarity features into one grade. — [ACL Anthology P11-1076](https://aclanthology.org/P11-1076/)
- Mohler 2011 data and results:
  - Data: 80 undergraduate Data Structures questions across 10 assignments and 2 exams, 31 students, 2,273 answers graded 0–5 by 2 graders. Inter-annotator agreement (IAA) was r=0.586, RMSE 0.659.
  - Alignment score alone (no learning): r=0.411, rising to 0.428 with question demoting.
  - Best hybrid model: SVMRank r=0.518. Best RMSE 0.978 (SVR hybrid), best median RMSE 0.862. Evaluation used 12-fold leave-one-assignment-out cross-validation. — [ACL Anthology P11-1076 PDF](https://aclanthology.org/P11-1076.pdf)
- **Ramachandran, Cheng & Foltz (2015), BEA workshop, pp. 97–106.** Builds word-order graphs from human rubric texts and top-scoring student answers to extract important patterns automatically, replacing hand-written regular expressions. Semantic metrics group related words as alternative answers. The patterns become features for stacked random-forest regressors. — [ACL Anthology W15-0612](https://aclanthology.org/W15-0612/)
- Ramachandran 2015 results:
  - ASAP-SAS: mean QWK 0.78, against 0.77 for Tandalla's hand-written regex (difference not statistically significant). The Kaggle-best regex random-forest scored 0.70 on its own; human benchmark 0.90.
  - Mohler dataset: r=0.61. Table 3 reports RMSE 0.86 and median RMSE 0.77 (assignment-level model), or RMSE 0.88 and median 0.82 (question-level model, 1,142 train / 1,131 test answers).
  - **Inconsistency:** the conclusion states "RMSE of 0.77", which appears to be the *median* RMSE. — [W15-0612 PDF](https://aclanthology.org/W15-0612.pdf)
- **Sultan, Salazar & Sumner (2016), NAACL-HLT, pp. 1070–1075.** Features:
  - The alignment proportion: the share of content words in the reference and student answers that have a semantically similar partner in the other text, found with a monolingual word aligner.
  - Embedding similarity, question demoting, term weighting and length ratio.
  - Ridge regression on Mohler; random forest on SemEval. — [ACL Anthology N16-1123](https://aclanthology.org/N16-1123/)
- Sultan 2016 results:
  - Mohler, out-of-domain training: r=0.592, RMSE 0.887, against Mohler 2011's 0.518 / 0.978. Removing the alignment features drops r to 0.519.
  - Mohler, in-domain setup: r=0.63, RMSE 0.85, against Ramachandran's 0.61 / 0.86.
  - SciEntsBank 5-way weighted F1: Unseen Answers (UA) 0.582, Unseen Questions (UQ) 0.554, Unseen Domains (UD) 0.545. Best SemEval systems: ETS 0.535/0.487/0.447 and SoftCardinality 0.537/0.492/0.471. — [N16-1123 PDF](https://aclanthology.org/N16-1123.pdf)
- **Agarwal et al. (2022), NAACL, "MitiGaTe".** Multi-Relational Graph Transformer. Parses the student response into an AMR graph split into one subgraph per relation, encodes it with a graph transformer, and compares it with the reference-answer subgraphs. Reported as state of the art on the Mohler dataset; the abstract gives no numbers. — [ACL Anthology 2022.naacl-main.146](https://aclanthology.org/2022.naacl-main.146/)

### Inferences
- The Mohler dataset is undergraduate CS (Data Structures, including programming basics), the closest public benchmark to intro-Java explanations. Its alignment methods are a natural non-LLM baseline.
- Mohler's stage-1 node scorer, a perceptron trained on a few hand-aligned graphs, is effectively an "edge/node-level classifier from little gold". It is a template for training a per-edge matcher on our 19 edge-gold answers and then using the 365 overall labels to fit the aggregation stage, as Mohler's SVM stage does.
- Sultan's aligner is unsupervised and fast. Its per-word alignments can be grouped by graph edge (head and dependent concept) to give per-edge "covered / not covered" judgements with no training.
- Absolute gains are modest: Mohler-dataset r tops out around 0.6, near human IAA of 0.586. Overall-score agreement is a weak signal of per-element accuracy.

### Gaps
- Mohler 2011 does not state the exact size of the manually aligned training set in the text extracted here, nor any node-alignment accuracy. Check Section 3.1 of the full paper.
- MitiGaTe's numbers were not retrieved.
- Unverified follow-ups (from memory, not checked):
  - Heilman & Madnani 2013 (ETS, SemEval)
  - Riordan et al. 2017 (neural ASAG)
  - Kumar et al. 2019 (AutoSAS)
  - Graph-based ASAG on Mohler via GNNs: Tan et al. 2020? (unverified)

## Q2. Facet- and rubric-item-based assessment (Nielsen facets, SemEval-2013 Task 7, analytic and rubric-aware scoring)

### Takeaway
The closest prior art to per-edge grading is Nielsen's facet model. Each reference answer is broken into facets, which are (term1, relation, term2) triples, i.e. graph edges. Each facet is labelled Expressed, Contradicted or Unaddressed against the student answer. The SemEval-2013 partial-entailment pilot reached weighted F1 of about 0.75–0.82 per facet with a non-LLM entailment system plus WordNet. Analytic per-criterion scoring (Mizumoto 2019) and rubric injection (Wang 2019) show rubric conditioning helps most in low-data settings.

### Cited Findings
- **Nielsen, Ward & Martin (2009), Natural Language Engineering, "Recognizing entailment in intelligent tutoring systems".** Argues for finer-grained answer analysis, with reference answers decomposed into facets. — [Cambridge NLE](https://www.cambridge.org/core/journals/natural-language-engineering/article/recognizing-entailment-in-intelligent-tutoring-systems/C4925CE6B644A53F5B3D460328126BD1)
- **Nielsen, Ward, Martin & Palmer (2008), LREC.** Annotated facet-level entailment for student science answers, with 86.2% inter-annotator agreement on facet labels. — [LREC 2008 (L08-1166)](https://preview.aclanthology.org/author-url/L08-1166)
- **Dzikovska, Nielsen, Brew et al. (2013), SemEval-2013 Task 7, pp. 263–274.**
  - Tasks: 5-way, 3-way and 2-way student-response labelling on Beetle and SciEntsBank, with 9 teams, plus a pilot partial-entailment task.
  - Facet definition: a triplet of two key terms and a relation (e.g. "contains – seeds", relation Material). Each facet is judged Expressed or Unaddressed for a given student answer.
  - Pilot test set: 16,263 facets (5,945 Expressed, 10,318 Unaddressed). — [ACL Anthology S13-2045 PDF](https://aclanthology.org/S13-2045.pdf)
- Partial-entailment pilot results (only participant: UKP-BIU):
  - Best run (Run 2): weighted-average F1 0.782 / 0.765 / 0.816 on UA / UQ / UD; macro F1 0.753 / 0.73 / 0.804.
  - Majority baseline: weighted F1 0.54 / 0.547 / 0.478. — [S13-2045 PDF, Table 7](https://aclanthology.org/S13-2045.pdf)
- **Zesch, Levy, Gurevych & Dagan (2013), UKP-BIU, SemEval.** Per-facet methods:
  - "Exact": both facet words appear among the lemmatised student tokens.
  - "WordNet": the facet words or their WordNet relatives appear.
  - BIUTEE: an entailment engine.
  These are combined by majority voting; no LLM. — [S13-2048 PDF](https://aclanthology.org/S13-2048.pdf)
- **Levy, Zesch, Dagan & Gurevych (2013), ACL short paper, "Recognizing Partial Textual Entailment".** Micro-F1 on faceted SciEntsBank (UA / UQ / UD):

  | Method | UA | UQ | UD |
  |---|---|---|---|
  | Baseline | 0.670 | 0.688 | 0.731 |
  | BaseLex | 0.756 | 0.710 | 0.760 |
  | BaseSyn | 0.744 | 0.733 | 0.770 |
  | Majority vote of methods | 0.782 | 0.765 | 0.816 |

  It also tests a simple rule that aggregates facet judgements into a complete-entailment decision for the whole answer. — [ACL Anthology P13-2080](https://aclanthology.org/P13-2080.pdf)
- SemEval-2013 main 2-way task, macro-F1 (one sample of rows):
  - SoftCardinality: 0.774 / 0.635 / 0.715 / 0.737 / 0.705, mean 0.713.
  - Lexical baseline: mean 0.682.
  - Median system: 0.676. — [S13-2045 PDF, Table 6](https://aclanthology.org/S13-2045.pdf)
- **Mizumoto et al. (2019), BEA workshop, pp. 316–325.**
  - Tasks: analytic score prediction (one score per rubric criterion) and justification identification (the span of the response that earns each analytic score).
  - Dataset: 6 Japanese reading-comprehension prompts × 2,100 responses, with 3–4 analytic criteria per prompt.
  - Inter-annotator agreement per criterion: mean Kappa 0.84, QWK 0.87. — [ACL Anthology W19-4433](https://aclanthology.org/W19-4433.pdf)
- **Wang, Inoue, Ouchi, Mizumoto & Inui (2019), DeepLo workshop, "Inject Rubrics into Short Answer Grading System".**
  - Method: a rubric component using word-level attention between the answer and the rubric text, on top of a bi-LSTM baseline (Riordan et al. 2017).
  - Data: ASAP-SAS, averaging 1,308 training answers per prompt.
  - Results: baseline QWK 0.770 at 100% of the training data. The gains are largest in low-resource settings (about +0.05 QWK at 12.5% training data, per the search summary). — [ACL Anthology D19-6119](https://aclanthology.org/D19-6119.pdf)
- **Künnecke, Filighera, Leong & Steuer (2024), arXiv 2403.01811.**
  - Method: weakly supervised annotation of justification cues, plus a neuro-symbolic grader that scores from detected cues.
  - Data: Short Answer Feedback (SAF), bilingual and multi-domain.
  - Result: RMSE improved by 0.24–0.3 over the prior state of the art on SAF. Preprint, not peer-reviewed. — [arXiv 2403.01811](https://arxiv.org/abs/2403.01811)

### Inferences
- **Direct mapping to our setup:** our concept-graph edges correspond to Nielsen facets. Facet labels (Expressed / Contradicted / Unaddressed) are a ready-made per-edge label scheme with published agreement (86.2%).
- **The UKP-BIU recipe** (exact match, then WordNet, then entailment, combined by majority) is non-LLM, needs almost no training data, and reached weighted F1 of about 0.78 per facet. That is a realistic per-edge baseline.
- **Off-the-shelf NLI models** (e.g. DeBERTa-MNLI cross-encoders) would be the modern drop-in for BIUTEE. This is our inference; no source here tests them on facets.
- **Using the overall labels:** the 365 holistic labels can calibrate the aggregation from per-edge judgements to an overall label. Levy 2013 shows that even a simple aggregation rule from facets gives a usable whole-answer decision.
- **Justification identification** (Mizumoto) is the span-level version of "which part of the student text supports edge e". It is useful for showing evidence in an interface.

### Gaps
- Nielsen's original facet classifier accuracies (Nielsen et al. 2008/2009) were not retrieved.
- Full SemEval 5-way leaderboard numbers per team were not retrieved, apart from those quoted in Sultan 2016.
- Mizumoto 2019 model results (analytic QWK, justification F1) were not extracted.
- No source found that applies facet entailment to programming or code explanations.

## Q3. Concept-map extraction and comparison (Villalón & Calvo; Ruiz-Primo; Ifenthaler; Clariana)

### Takeaway
Concept-map mining from student essays (Villalón & Calvo) and graph-comparison measures (Ifenthaler's SMD/AKOVIA; Clariana's ALA-Reader) give a measurement framework for comparing a student-derived graph with an expert referent map. Their extraction accuracy and validity evidence is mostly older and modest. ALA-Reader scores maps as percent agreement of links with an expert referent, which is essentially per-edge matching.

### Cited Findings
- **Villalón & Calvo (2011), Educational Technology & Society 14(3), "Concept Maps as Cognitive Visualizations of Writing Assignments".** Automatic concept-map extraction evaluated on 43 manually annotated university essays. Complete maps (concepts plus labelled relations) are possible, with precision depending on the level of summarisation (number of concepts). The method was integrated into the Glosser writing-feedback tool. Their 2008 work proposed a formal definition of concept map mining (CMM) and an evaluation framework. — [summary via Adelaide repository / citing sources](https://drmc.library.adelaide.edu.au/dspace/bitstream/2440/99194/2/hdl_99194.pdf)
- A key limitation of concept-map mining is the lack of an evaluation framework. Researchers often treat expert-built maps as the gold standard. — [search summary of CMM literature](https://www.scitepress.org/Papers/2014/48423/48423.pdf)
- **Ifenthaler (2010), ETR&D 58(1), 81–97, "Relational, structural, and semantic analysis of graphical representations and concept maps".** SMD framework (Surface, Matching, Deep structure) covering relational, structural and semantic levels. — [Curtin espace](https://espace.curtin.edu.au/handle/20.500.11937/23814)
- **Ifenthaler (2014), Technology, Knowledge and Learning 19(1), 241–248, AKOVIA.** Automated analysis of natural-language and graphical knowledge representations with seven quantitative similarity measures; tested for reliability and validity. — [Curtin espace](https://espace.curtin.edu.au/handle/20.500.11937/31696)
- **Clariana's ALA-Reader (v1.01, 2005).** Converts a written summary into a cognitive map, then scores it as percent agreement with an expert referent map. Its author describes it as "rudimentary". — [EduTech Wiki: ALA-Reader](https://edutechwiki.unige.ch/en/ALA-Reader)
- **Taricani & Clariana (2006), ETR&D.** Automatically scored open-ended concept maps from link data and from geometric distance between terms. Link-based scores related more to terminology test scores; distance-based scores related more to comprehension. — [Penn State Pure](https://pure.psu.edu/en/publications/a-technique-for-automatically-scoring-open-ended-concept-maps/)
- **Marshall, Chen & Madhusudan (2006), Decision Support Systems 42(3).** A similarity-flooding algorithm with element anchoring to match nodes and substructures between concept maps. Reported 91% combined recall on student-drawn maps. — [Univ. of Arizona](https://experts.arizona.edu/en/publications/matching-knowledge-elements-in-concept-maps-using-a-similarity-fl/)
- **Limongelli et al. (2016), LNCS.** Seven similarity measures for concept maps in educational applications. — [search result, Roma Tre IRIS](https://iris.uniroma3.it/handle/11590/321165)
- **Burrows, Gurevych & Stein (2015), IJAIED 25(1), 60–117, "The Eras and Trends of Automatic Short Answer Grading".** Names "concept mapping" as the first era of ASAG. — [OpenAlex DOI 10.1007/s40593-014-0026-8](https://api.openalex.org/works/doi:10.1007%2FS40593-014-0026-8)

### Inferences
- Ifenthaler's propositional or semantic matching measures, and ALA-Reader's link agreement with an expert map, define the *aggregate* graph-similarity scores. Our per-edge judgements could be summed into such a score, giving a validated vocabulary for the overall grade (e.g. proportion of expert propositions matched).
- Marshall's 91% node-matching recall suggests node/concept alignment is the easier part. Relation (edge) correctness is where the difficulty lies, consistent with facet-level F1 of about 0.75–0.8.

### Gaps
- Ruiz-Primo's work on concept-map assessment (reliability and validity of scoring against expert maps) was not retrieved.
- Villalón & Calvo's exact precision and recall values were not retrieved.
- Validity statistics comparing ALA-Reader to human expert scores (Clariana, Koul & Salehi) were not found.
- The exact definitions of AKOVIA's seven measures were not verified. From memory, they are surface, graphical, structural, gamma, concept, propositional and balanced-semantic matching (unverified).

## Q4. Knowledge-graph-enhanced ASAG and explanation grading (2019–2026), including code explanations

### Takeaway
Recent KG-enhanced ASAG (2025–2026) is dominated by GraphRAG pipelines that use an LLM at run time, so it fails our constraint. Non-LLM graph work in this period mainly uses AMR or graph transformers (MitiGaTe 2022). The closest code-explanation work is the SelfCode corpora (Java self-explanations, Rus group). Their non-LLM SVR on Sentence-BERT plus ITS semantic features reaches r≈0.71 with expert ratings. It is holistic per line or sentence, not per concept.

### Cited Findings
- **Chu et al. (2026), arXiv 2603.19276 / EDM 2026 short paper, "From Flat to Structural: Enhancing ASAG with GraphRAG".**
  - Builds a KG from reference materials and grading rubrics, using Microsoft GraphRAG for construction and HippoRAG for associative traversal.
  - Retrieves connected subgraphs as evidence for grading.
  - Evaluated on an NGSS science dataset; reported to beat flat vector RAG. No numbers on the abstract page.
  - Relies on an LLM grader. — [arXiv 2603.19276](https://arxiv.org/abs/2603.19276); [EDM 2026](https://educationaldatamining.org/edm2026/proceedings/2026.EDM.short-papers.234/index.html)
- **Xu & Corter (2026), AAAI, "Graph RAG for ASAG with Feedback".**
  - Instructor-curated fact graph that grounds LLM scores and feedback.
  - Evaluated on SAF (31 topics) with unseen-question and unseen-answer splits.
  - GraphRAG accuracy was comparable to vector RAG, with gains in traceability. — [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/42125)
- **GRASP (arXiv 2609.03857).** Graph-augmented retrieval over question and reference-answer nodes for label-free multi-topic exams. — [papers.cool](https://papers.cool/arxiv/2609.03857)
- **Knowledge graph plus Neural Tensor Network for answer assessment (2020).** Concept graph built from reference answers, with knowledge-completion embeddings. Bibliographic details could not be retrieved (PMC blocked the fetch). — [PMC7334163](https://pmc.ncbi.nlm.nih.gov/articles/PMC7334163)
- **Agarwal et al. (2022), NAACL, MitiGaTe.** AMR relation subgraphs compared between reference and student answer, evaluated on the Mohler CS dataset. — [ACL Anthology](https://aclanthology.org/2022.naacl-main.146/)
- **SelfCode (FLAIRS 2023), Rus group, University of Memphis.** 1,770 pairs of student and expert line-by-line self-explanations of Java code examples, with expert semantic-similarity ratings, plus a baseline model; corpus on GitHub. — [Memphis Digital Commons](https://digitalcommons.memphis.edu/facpubs/20224)
- **Automated Assessment of Student Self-explanation During Source Code Comprehension (FLAIRS 2022).** Best model was SVR on Sentence-BERT plus ITS semantic-similarity features, r=0.7088 with human judgements. — [FLAIRS 2022](https://journals.flvc.org/FLAIRS/article/view/130540)
- **SelfCode 2.0 (FLAIRS 2025).** 3,019 student–expert Java explanation pairs, annotated for similarity, correctness and completeness. — [NSF PAR 10613654](https://par.nsf.gov/biblio/10613654-selfcode-annotated-corpus-student-expert-line-line-explanations-code-examples-automated-assessment)
- **Related work on Java explanations.** It reports that the amount of self-explanation correlated with learning gains. It also suggests that Java code explanations may need different assessment techniques than narrative or science text. — [NSF PAR search, Rus](https://par.nsf.gov/search/author:%22Rus,%20Vasile%22)

### Inferences
- **SelfCode and SelfCode 2.0** are the most relevant public data for intro-Java explanation assessment. Their "completeness" annotation is conceptually close to edge coverage. They could serve for pretraining or transfer before fine-tuning an edge matcher on our 19 edge-gold answers.
- **GraphRAG ASAG** shows the field is moving to rubric/KG structuring, but its run-time LLM dependency rules it out. The graph-construction ideas (instructor KG from rubric and reference answers) still transfer offline.

### Gaps
- No peer-reviewed non-LLM paper was found that grades programming explanations against a concept graph edge by edge.
- Numbers for the 2020 KG+NTN paper and for GraphRAG 2026 were not retrieved.
- Possibly relevant but unverified (from memory, not checked):
  - Bernius et al. (Athena/CoFee, TUM): clustering-based feedback for CS text exercises.
  - Condor et al. (2021–2022): ASAG on UC Berkeley CS/statistics.
  - Leinonen et al. (2023): LLM-based code explanations; excluded anyway because it uses an LLM.

## Q5. Which methods give per-element (per-edge) judgements, work with few labels, and need no generative LLM?

### Takeaway
The best fits are Nielsen/SemEval facet entailment (with UKP-BIU-style lexical, WordNet and entailment voting), Mohler-style node alignment trained on a handful of hand-aligned answers, and Sultan's unsupervised word aligner grouped by edge. Rubric-attention and analytic-score models (Wang 2019, Mizumoto 2019) give per-criterion outputs but need hundreds to thousands of labels per prompt.

### Cited Findings
- **Facet entailment.**
  - Per-element output: per-facet Expressed / Unaddressed labels.
  - Label needs: minimal; the Exact and WordNet components are unsupervised.
  - Results: weighted F1 about 0.78–0.82 on SciEntsBank facets. — [S13-2045](https://aclanthology.org/S13-2045.pdf); [S13-2048](https://aclanthology.org/S13-2048.pdf); [P13-2080](https://aclanthology.org/P13-2080.pdf)
- **Mohler 2011.**
  - Per-element output: a per-node alignment score.
  - Label needs: the perceptron node scorer was trained on "a small set of manually aligned graphs"; the overall SVM used other assignments as training data.
  - Results: alignment-only r=0.41–0.43; hybrid r=0.518. — [P11-1076](https://aclanthology.org/P11-1076.pdf)
- **Sultan 2016.**
  - Per-element output: word-level alignments from an unsupervised aligner.
  - Label needs: only the overall regressor needs labels.
  - Results: r=0.592 on Mohler. — [N16-1123](https://aclanthology.org/N16-1123.pdf)
- **Ramachandran 2015.** Rubric text plus top-scoring answers become graph patterns; each pattern match is an interpretable per-pattern feature. Needs per-prompt training answers (1,142 on Mohler). — [W15-0612](https://aclanthology.org/W15-0612.pdf)
- **Wang 2019 (rubric injection).** Benefit largest at 12.5% of the training data. Even then, that means roughly 160 answers per prompt, given the average of 1,308 training answers. — [D19-6119](https://aclanthology.org/D19-6119.pdf)
- **Mizumoto 2019 (analytic scoring).** Per-criterion scores and justification spans, but trained on 2,100 responses per prompt. — [W19-4433](https://aclanthology.org/W19-4433.pdf)

### Inferences
- **Recommended stack for 365 overall labels plus 19 edge-gold answers:**
  - (a) For each concept-graph edge (a facet triple), compute unsupervised evidence features: exact or lemma match of both endpoint concepts (UKP "Exact"), WordNet or embedding relatives (with a Java synonym lexicon in place of WordNet), Sultan-style alignment coverage, and an NLI cross-encoder entailment probability for a templated edge sentence such as "X calls Y".
  - (b) Fit a small per-edge classifier (logistic regression or perceptron, as in Mohler) on the 19 edge-gold answers × edges. This likely gives a few hundred edge instances.
  - (c) Use the 365 overall labels as weak supervision. One option is to fit the aggregation from edge judgements to the overall label (Levy-style rule or a learned weighting). Another is EM or multiple-instance learning to refine edge thresholds. This step is our inference, not a published recipe.
- **Evaluation:** report per-edge Expressed/Unaddressed F1 against the 19 gold answers, comparable to SemEval pilot weighted F1 of about 0.78, alongside overall-label agreement.
- **Domain shift:** code vocabulary (identifiers, `System.out.println`, "loop runs n times") is poorly covered by WordNet. The SelfCode corpus and a code-aware sentence encoder may be needed. This is uncertain; no source found evaluates it.

### Gaps
- No source reports per-edge accuracy as a function of the number of edge-gold examples (learning curves at about 20 answers).
- No published non-LLM system was found that combines facet entailment with weak supervision from holistic labels. Treat the proposed recipe as a hypothesis.
- No published per-facet performance with modern NLI cross-encoders on SciEntsBank Extra was retrieved. Such work likely exists (2019+) but was not verified.
