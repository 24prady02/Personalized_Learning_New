# ITS and Assessment Approaches that Map Student Text/Steps onto Expectations, Misconceptions, Constraints, or Learning-Progression Levels

Target context: intro Java programming; deterministic at run time (no LLM); few labels. Throughout, "[VERIFIED]" = read in a fetched primary/near-primary source this session; "[SNIPPET]" = from search-result abstracts/snippets only; "[BACKGROUND]" = well-known bibliographic fact from prior knowledge, cited to DOI/landing page but NOT re-read this session. Treat [BACKGROUND] numbers as needing verification.

## 1. AutoTutor family: expectation–misconception tailored (EMT) dialogue

### Takeaway
AutoTutor maps each student turn onto a hand-authored per-question curriculum script of expectations (good answer sentences) and misconceptions ("bad answers") by thresholding LSA cosine, later combined with hand-written regular expressions. The method is deterministic at run time and needs no labelled training data, only a corpus for the LSA space and authored expectations. Agreement with humans is "fair", somewhat below human–human agreement. The thresholds need tuning: a fixed 0.65 cosine was too high.

### Cited Findings
- **Mapping and authoring:** AutoTutor "matches student responses to the expectations and probable bad answers for each question by calculating the LSA cosine between them". The expectations, bad answers and dialogue moves (hints, pumps, prompts, assertions) sit in hand-authored "curriculum scripts". General domain knowledge sits in the LSA corpus. The next dialogue move is chosen from the cosines. [VERIFIED] — [Penumatsa et al. 2003, FLAIRS-16, "The Right Threshold Value…"](https://cdn.aaai.org/FLAIRS/2003/Flairs03-082.pdf)
- **Threshold evidence:** AutoTutor 2.0 (conceptual physics) declared a match when cosine > 0.65. In the 2003 study, 24 students each answered 8 physics problems. Two expert physics tutors labelled each expectation as explicitly present, implicitly present or absent. For each expectation, the score was the maximum cosine over all combinations of the student's sentences. [VERIFIED] — [Penumatsa et al. 2003](https://cdn.aaai.org/FLAIRS/2003/Flairs03-082.pdf)
- **Threshold result:** The mean cosine for expectations that experts rated *explicitly present* was only **0.42**, far below the 0.65 threshold. Both expectation length and student-answer length significantly shifted cosines, so the authors recommend a threshold that depends on length. No kappa or accuracy was reported; results appear as figures only. [VERIFIED] — [Penumatsa et al. 2003](https://cdn.aaai.org/FLAIRS/2003/Flairs03-082.pdf)
- **Later evaluation (Learning@Scale 2019):** The AutoTutor Conversation Engine (ACE) "uses a combination of LSA and Regular Expressions (RegEx)". It was evaluated on 219 MTurk respondents × 118 electronics questions, giving 5,202 response–expectation pairings. RegEx and LSA were moderately correlated. "Agreement between ACE and human was fair, but slightly lower than agreement between human[s]". [SNIPPET] — [Carmon et al. 2019, L@S, "Semantic Matching Evaluation of User Responses to Electronics Questions in AutoTutor"](https://unpaywall.org/10.1145%2F3330430.3333649)
- **Thesis follow-up:** The RegEx–LSA correlation was ρ(5202) = .471. Agreement was evaluated at stringent, intermediate and lenient thresholds. The best computer–human F1 came within about .006 of human–human F1. The two sources differ slightly: "fair, slightly lower" (2019) versus "similar to humans" (2021 thesis, after optimisation). [SNIPPET] — [Carmon 2021, U. Memphis thesis](https://digitalcommons.memphis.edu/etd/2148)
- **Length-adjusted thresholds:** The best agreement with subject-matter experts came when the cosine threshold was a function of both student-answer length and expectation length. [SNIPPET] — [Penumatsa et al. 2006 (via search)](https://digitalcommons.memphis.edu/facpubs/7460)
- **Revised LSA algorithm:** Hu et al. 2003 introduced a revised LSA algorithm that "significantly improves the precision" of AutoTutor's natural-language understanding. [SNIPPET] — [Hu et al. 2003](https://digitalcommons.memphis.edu/facpubs/7294)
- **DeepTutor / SEMILAR (Rus et al.):** DeepTutor is a dialogue tutor for physics that is "based on learning progressions". SEMILAR is a Java library of semantic-similarity methods (LSA, LDA, greedy lexical matching, and others) tuned on DeepTutor data. [SNIPPET] — [Rus et al. (Memphis faculty pubs)](https://digitalcommons.memphis.edu/facpubs/3198)
- **Adding context:** Banjade & Rus (EDM 2019) argue that similarity to a reference answer alone misses dialogue context. Adding learner knowledge level and question difficulty through Probabilistic Soft Logic improved correctness inference on the DT-Grade dataset by more than 7 percentage points of accuracy over a similarity-only model. [SNIPPET] — [Banjade & Rus, "Assessing student response in tutorial dialogue context using probabilistic soft logic"](https://digitalcommons.memphis.edu/facpubs/2545)
- **Original paper:** The original AutoTutor LSA paper is Graesser, Wiemer-Hastings, Wiemer-Hastings, Harter, Person & TRG (2000), *Interactive Learning Environments* 8(2). [BACKGROUND] An early FLAIRS-99 AutoTutor LSA paper also exists. [SNIPPET] — [FLAIRS-99](https://cdn.aaai.org/FLAIRS/1999/FLAIRS99-034.pdf)

### Inferences
- The EMT pattern fits the user's constraints directly. Per question, hand-author a few expectations and misconceptions (graph nodes), match student text by deterministic similarity plus regex, and threshold the result. Data needs are an unlabelled corpus (or no corpus, if lexical or regex only) and the author's time. No labels are needed except to calibrate thresholds.
- The AutoTutor evidence says to (a) score coverage per expectation rather than per whole answer, (b) take the maximum over student sentence subsets, (c) calibrate thresholds on a small labelled set and make them depend on length, and (d) combine regex (high precision for key terms such as Java keywords and identifiers) with a soft similarity score.
- Generic LSA trained on English will handle code tokens (`i++`, `arr.length`) poorly. A domain corpus (Java textbook plus forum posts) or hand-made regex synonyms would be needed.

### Gaps
- No headline kappa or accuracy for the original LSA-vs-judge matching was found. The 2003 paper reports only means in figures.
- The DeepTutor expectation-matching accuracy figures (for example, on the DT-Grade dataset) were not retrieved. AutoTutor Lite and ARIES/OperationARIES matching evaluations were not retrieved.

## 2. Constraint-based modelling (CBM: Ohlsson; Mitrovic SQL-Tutor, KERMIT, EER-Tutor, J-LATTE)

### Takeaway
CBM represents domain knowledge as hand-authored constraints, each a pair (relevance condition Cr, satisfaction condition Cs): "if Cr holds, Cs ought to hold". A student solution is diagnosed by the set of constraints that are relevant but violated. It is deterministic and needs no training data, but authoring is expert-intensive. A Java CBM tutor exists (J-LATTE, 2009). CBM checks constraints on structured solutions; no evidence was found of it being applied to free text.

### Cited Findings
- **Constraint form:** A constraint is evaluated in two stages. If the relevance condition is met but the satisfaction condition is not, the solution violates the constraint. Mitrovic's general form is "if Cr is true, Cs ought to be true as well". SQL-Tutor compiles constraints into a "relevance network" and a "satisfaction network". [SNIPPET, secondary summaries] — [Mitrovic 2010 chapter (UBC course copy, now 404)](https://www.cs.ubc.ca/~conati/522/532b-2022/papers/Mitrovic2010.pdf); [Summary of Mitrovic & Ohlsson 99](https://nats-www.informatik.uni-hamburg.de/bin/view/User/SummaryForMitrovicOhlsson99)
- **Evaluation paper:** Mitrovic & Ohlsson (1999), "Evaluation of a Constraint-Based Tutor for a Database Language", *IJAIED* 10(3–4), 238–256. Mitrovic, Martin & Mayo (2002, UMUAI) report three SQL-Tutor evaluation studies from 1998–99. [SNIPPET] — [DOI 10.1023/A:1015022619307](https://www.doi.org/10.1023/A:1015022619307)
- **Implementation critique:** SQL-Tutor's constraints are LISP code fragments that embed domain knowledge in ad hoc functions. The representation is "as loose as Ohlsson's description". [SNIPPET] — [PhD thesis, Hamburg](https://nats-www.informatik.uni-hamburg.de:443/pub/INCOM/Literatur/phd_0301.pdf)
- **J-LATTE (Java):** Holland, Mitrovic & Martin (2009), "J-LATTE: a constraint-based tutor for Java", ICCE 2009, pp. 142–146. It teaches a subset of Java using syntactic and semantic constraints. [SNIPPET] — [ITS survey arXiv 1812.09628](https://arxiv.org/pdf/1812.09628); [ICCE follow-up](https://library.apsce.net/index.php/ICCE/article/download/4954/4883/6227)
- **Reducing authoring cost:** ASPIRE is the authoring and deployment environment for CBM tutors, built to cut the cost of writing constraints. Ontology-based constraint generation has also been explored. [SNIPPET] — [ASPIRE](https://researchers.mq.edu.au/en/publications/aspire-an-authoring-system-and-deployment-environment-for-constra/); [ontologies to author CBM](https://research.monash.edu/en/publications/using-ontologies-to-author-constraint-based-intelligent-tutoring-/)
- **Origin:** Ohlsson (1994), "Constraint-based student modeling", in Greer & McCalla (eds.), *Student Modelling*, Springer NATO ASI. KERMIT (ER modelling, Suraweera & Mitrovic 2002) and EER-Tutor are other CBM tutors. [BACKGROUND]

### Inferences
- For Java steps or code, constraints of the form "if the loop uses an index into array A (relevance), then the bound must be `< A.length` (satisfaction)" map naturally onto misconception nodes such as off-by-one errors.
- For free-text explanations, a constraint's relevance or satisfaction condition could be implemented as a regex or similarity test against an expectation. That would be a hybrid of CBM and AutoTutor. No published system doing this was found, so the hybrid is speculative.
- Constraint violations are deterministic, binary evidence. They could serve as emission observations in an HMM or Bayesian network over concept nodes.

### Gaps
- The exact constraint counts for SQL-Tutor, KERMIT and EER-Tutor, the hours-per-constraint authoring figures, and the learning-gain effect sizes were not retrieved (the Mitrovic 2010 PDF returned 404).
- J-LATTE evaluation results were not retrieved.
- No CBM-on-free-text paper was found.

## 3. Model tracing and bug libraries (Anderson Cognitive Tutors; BUGGY; VanLehn)

### Takeaway
Model tracing matches each student step against hand-written production rules, both correct rules and "buggy" rules that encode misconceptions. Bug libraries such as BUGGY enumerate procedural bugs. Both are deterministic and expert-authored, and both suit step-level programming tasks better than free text. Only bibliographic background was gathered this session.

### Cited Findings
- **BUGGY:** Brown & Burton (1978), "Diagnostic models for procedural bugs in basic mathematical skills", *Cognitive Science* 2(2), 155–192. [BACKGROUND] — [DOI 10.1207/s15516709cog0202_4](https://doi.org/10.1207/s15516709cog0202_4)
- **Cognitive Tutors:** Anderson, Corbett, Koedinger & Pelletier (1995), "Cognitive Tutors: Lessons learned", *Journal of the Learning Sciences* 4(2), 167–207. Model tracing plus knowledge tracing, including the LISP tutor. [BACKGROUND] — [DOI 10.1207/s15327809jls0402_2](https://doi.org/10.1207/s15327809jls0402_2)
- **Knowledge tracing (BKT):** Corbett & Anderson (1995), "Knowledge tracing: Modeling the acquisition of procedural knowledge", *UMUAI* 4, 253–278. BKT is a 2-state HMM per skill with parameters P(L0), P(T), P(G), P(S). It was developed in the LISP programming tutor. [BACKGROUND] — [DOI 10.1007/BF01099821](https://doi.org/10.1007/BF01099821)
- **VanLehn's review:** VanLehn (2006), "The behavior of tutoring systems", *IJAIED* 16(3), describes the step-level inner loop. [BACKGROUND]

### Inferences
- Lineage for the user's design: BKT is literally an HMM, so Viterbi or forward-backward decoding of mastery states is standard. Extending it to a prerequisite graph gives the Bayesian-network approaches in §4.
- Buggy rules correspond to misconception nodes. Matching a student's step to a buggy rule is the step-level analogue of AutoTutor's misconception matching.

### Gaps
- No quantitative results were retrieved this session for model tracing accuracy or for the size of BUGGY's bug catalogue. The well-known figure of about 110 primitive subtraction bugs, attributed to Burton 1982 / DEBUGGY, is unverified.

## 4. Bayesian networks and knowledge tracing over solution or prerequisite graphs; HMM/Viterbi decoding

### Takeaway
Andes builds a Bayesian network directly from the solution graph: rule, fact and goal nodes for each problem, plus long-term rule-mastery nodes. Observed student entries update beliefs over unobserved knowledge and the plan the student is following. This is the closest classical analogue to "probabilistic inference over a domain graph". Graph-based knowledge tracing (GKT) learns the graph with a GNN instead. HMM-plus-Viterbi decoding of latent student strategies is established in programming-education research.

### Cited Findings
- **Andes journal paper:** Conati, Gertner & VanLehn (2002), "Using Bayesian Networks to Manage Uncertainty in Student Modeling", *UMUAI* 12(4), 371–417. The BN handles both knowledge assessment and plan recognition, and predicts student actions during problem solving. It covers assessment during worked-example study, and the model was scaled up to a field-evaluated system. [SNIPPET] — [PDF mirror](https://www.cse.unr.edu/~sjose/Papers%20Referenced/Using%20Bayesian%20Networks%20to%20Manage%20Uncertainty%20in%20Student%20Modeling.pdf); [bibsonomy](https://bibsonomy.org/bibtex/11fdc79a44fb06b6b6b528d2ad44cd2c)
- **Andes origins and hints:** Conati, Gertner, VanLehn & Druzdzel (1997, UM'97) introduced online BN student modelling for coached problem solving. Gertner, Conati & VanLehn (1998, AAAI) used the same network to generate procedural hints. [SNIPPET] — [UM97](https://www.academia.edu/12404465/On_Line_Student_Modeling_for_Coached_Problem_Solving_Using_Bayesian_Networks); [AAAI-98](https://mlanthology.org/aaai/1998/gertner1998aaai-procedural)
- **GKT (Nakagawa, Iwasawa & Matsuo 2019):** "Graph-based knowledge tracing: Modeling student proficiency using graph neural network", IEEE/WIC/ACM Web Intelligence, pp. 156–163; journal version in *Web Intelligence* 19 (2021) 87–102. It casts knowledge tracing as time-series node classification on a concept graph. Because "the knowledge graph structure is not explicitly provided in most cases", they propose several ways to build the graph (learned or statistical). It was evaluated on 2 open datasets and claims better prediction and interpretability. [SNIPPET] — [paper summary](https://sotaverified.org/papers/graph-based-knowledge-tracing-modeling); [journal](https://journals.sagepub.com/doi/pdf/10.3233/WEB-210458)
- **HMMs in programming education:**
  - Kiesmüller et al. (2010) trained an HMM classifier on 65 learners aged 12–13 in a programming environment and ran it online to identify problem-solving strategies in real time. [SNIPPET] — [Uni Duisburg-Essen DDI](https://ddi.informatik.uni-due.de/en/research/publications/online-identification-of-learner-problem-solving-strategies-using-pattern-recognition-methods-9735)
  - Shih, Koedinger & Scheines (2010) used HMM clustering to discover student strategies in tutors and linked those strategies to learning outcomes. [SNIPPET] — [CMU PDF](https://www.cmu.edu/dietrich/philosophy/docs/scheines/Shih_Koedinger_Scheines_2010.pdf)
  - A 2026 tutorial recovers the most probable latent-state sequence for each learner with Viterbi, and warns that state labels are identifiable only up to permutation. [SNIPPET] — [arXiv 2604.16900](https://arxiv.org/pdf/2604.16900)
  - Rodríguez & Boyer (2015) built HMMs of individual and paired students in visual programming. [SNIPPET] — [Springer](https://www.springerprofessional.de/discovering-individual-and-collaborative-problem-solving-modes-w/2469956)

### Inferences
- The Andes design suits few labels: the network structure comes from the expert's solution or domain graph, and conditional probabilities can be set by hand (for example, guess and slip near 0.1–0.2) rather than learned. Inference is deterministic exact or junction-tree inference. This matches "deterministic, no LLM, few labels" better than GKT, which needs large interaction logs such as ASSISTments-scale data.
- Unsupervised HMM states are not tied to named misconceptions. The permutation issue means that to decode onto *named* graph nodes, emissions must be anchored, for example with authored expectation and misconception matchers as in §1, rather than learned freely.

### Gaps
- The Andes BN's quantitative accuracy and network size, and GKT's AUC values, were not retrieved.
- No paper was found that runs Viterbi over a *named* misconception or learning-progression graph using text-matching emissions. This appears to be a genuine gap and possibly a novelty claim, but that is unconfirmed.

## 5. Automated scoring against learning progressions and SOLO levels (science LPs; code explanations)

### Takeaway
Learning-progression (LP) scoring in science uses supervised bag-of-words ensembles trained per item, with about 360–850 human-scored responses per item, and reaches 72–98% human–machine agreement. That is far more labelled data than "few labels" allows. For code, SOLO-level classification of "Explain in Plain English" (EiPE) responses mostly reduces to multistructural versus relational. Non-LLM NLP grading of EiPE correctness reached 87–89% accuracy. Recent level classification uses LLMs (segmentation: κ = 0.61), which the user's constraints exclude, though the segment-count heuristic itself could be done deterministically.

### Cited Findings
- **Kaldaras & Haudek (2022), *Frontiers in Education* 7, "Validation of automated scoring for learning progression-aligned NGSS performance assessments"** [VERIFIED] — [Frontiers](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2022.968289/full)
  - Target: a scientific-argumentation LP, levels 0–2 with sub-levels a–d.
  - Items and data: 19 items (Sugar, Bacteria, Gases); 932 students in grades 5–8; **361–848 human-scored responses per item**.
  - Engine: Constructed-Response Classifier (RTextTools), bag-of-words with an ensemble of 8 algorithms. Two variants: analytic (trained on rubric components) and holistic.
  - Agreement:
    - Analytic: accuracy 73.0–96.6%, Spearman ρ 0.604–0.969.
    - Holistic: accuracy 72.1–98.3%, ρ 0.476–0.953.
  - Validity: 4 items (S5, G6, G7, G8) were flagged as threats to validity. Errors clustered on rubric components that require interpretation, such as particle-level and model-based reasoning. The holistic model was a "harsher scorer".
- **Zhai-group argumentation study:** 17 argumentation tasks aligned to 3 LP levels, with 361 responses used to train per-item ML models; it examined which task features affect machine accuracy. [SNIPPET] — [arXiv 2405.06660](https://arxiv.org/html/2405.06660v1)
- **Other Zhai-group work:** Zhai, He & Krajcik (2022) ML-scored scientific models (*JRST* 59(10), 1765–1794). A 2023 Frontiers editorial notes that analytic rubrics raise human–machine agreement. [SNIPPET] — [editorial](https://www.frontiersin.org/articles/10.3389/feduc.2023.1183030/full); [MSU AI4ED](https://ai4ed.msu.edu/research)
- **ETS c-rater:** Liu, Rios, Heilman, Gerard & Linn (2016), "Validation of automated scoring of science assessments", *JRST*, using the c-rater-ML engine. Whether it targets learning-progression levels specifically was **not confirmed**. Liu et al. (2014) scored 4 multi-level science items with c-rater and found moderate-to-good agreement, concluding c-rater was "not yet" a replacement for human raters. [SNIPPET] — [ETS 2016](https://www.ets.org/research/policy_research_reports/publications/article/2016/jvpr.html); [Liu et al. 2014](https://core.ac.uk/works/76539887)
- **LP-based assessment with automated scoring** is also discussed at [Georgia Southern](https://scholars.georgiasouthern.edu/en/publications/the-application-of-automated-scoring-technology-in-learning-progr/) (details not retrieved). [SNIPPET]
- **SOLO in programming (human coding):**
  - Whalley, Lister, Thompson, Clear, Robbins, Kumar & Prasad (2006), ACE 2006 (Australasian Computing Education conference), first used Bloom and SOLO to classify novice "explain in plain English" responses. Multistructural = line-by-line description; relational = overall purpose. [VERIFIED as cited in Smith et al. 2025] — [arXiv 2503.12216](https://arxiv.org/pdf/2503.12216)
  - Clear, Whalley, Lister, Carbone, Hu, Sheard, Simon & Thompson (2008), "Reliably classifying novice programmer exam responses using the SOLO taxonomy" (NACCQ), proposed augmented SOLO categories for programming. [SNIPPET] — [UTS OPUS](https://opus.lib.uts.edu.au/handle/10453/12626)
  - Lopez, Whalley, Robbins & Lister (2008, ICER) related reading, tracing and writing skills. [VERIFIED as cited] — [arXiv 2503.12216](https://arxiv.org/pdf/2503.12216)
- **Non-LLM EiPE autograding:** Fowler, Chen, Azad, West & Zilles (2021), "Autograding 'Explain in Plain English' questions using NLP", SIGCSE '21, pp. 1163–1169. It reports "an accuracy of 87–89%, which is similar in performance to course teaching assistants trained to perform this task". The abstract does not give the features, classifier or data size. Smith et al. note that such models "require a high degree of authoring overhead to label data". [VERIFIED abstract] — [Illinois page](https://lagrange.mechse.illinois.edu/pubs/FoChAzWeZi2021/); [arXiv 2503.12216](https://arxiv.org/pdf/2503.12216)
- **Smith IV, Fowler, Denny & Zilles (2025), ITiCSE 2025, "Counting the Trees in the Forest"** [VERIFIED] — [arXiv 2503.12216](https://arxiv.org/pdf/2503.12216)
  - Method: an LLM segments the student's explanation and maps each segment to code lines. If the number of segments exceeds a threshold, the response is labelled multistructural; otherwise relational.
  - Data: a large CS1 course in Australasia. Humans coded multistructural-correct / relational-correct / incorrect with κ = 0.80 and 0.83 on 200-response subsets.
  - Results:
    - Threshold 1, raw: 68% agreement, κ = 0.30, F1 = 0.61.
    - Threshold 2: 81% agreement, κ = 0.61, F1 = 0.80, precision 0.83, recall 0.81.
    - After removing segments that are only function definitions, threshold 1 reached 81% agreement, κ = 0.61, F1 = 0.79.
  - Released in the open-source `eiplgrader` package.
- **LLM SOLO classification:** GPT-4o and GPT-5 show "only modest agreement" with human SOLO ratings (27 high-school students), and struggle to separate adjacent low levels. [SNIPPET] — [Princeton collaborate listing](https://collaborate.princeton.edu/en/publications/examining-students-code-comprehension-with-llms-in-block-and-text/)
- **Code generation as grading:** Smith & Zilles proposed generating code from the student's explanation with an LLM and running unit tests. This separates correct from incorrect explanations but not high-level from low-level ones. [VERIFIED as described] — [arXiv 2503.12216](https://arxiv.org/pdf/2503.12216)

### Inferences
- The relational-versus-multistructural distinction can probably be approximated deterministically by counting how many distinct code lines or tokens the explanation references: identifiers, operators and line-level verbs versus purpose words such as "returns the largest", "counts", "finds". This mirrors Smith et al.'s segment-count idea without an LLM. It is untested.
- LP or SOLO levels could be treated as ordered nodes, with deterministic evidence (expectation coverage from §1 plus constraint checks from §2) feeding a small hand-parameterised HMM or Bayesian network (§4) to infer the level. The science LP work shows that per-item supervised scoring needs hundreds of labels per item, which supports the case for authored-expectation approaches under "few labels".
- The lowest SOLO levels (prestructural and unistructural) are hardest to separate, for humans and LLMs alike, so the expected error is highest there.

### Gaps
- The features, classifier and dataset size of Fowler et al. 2021 were not retrieved.
- Teague & Lister SOLO papers were not retrieved.
- The ETS c-rater LP-specific study was not confirmed.
- Zhai et al.'s exact LP accuracy figures (for example, κ values) were not retrieved.
- No deterministic, non-LLM SOLO-level classifier for code explanations with reported agreement was found.

## Summary table (what maps onto what)

| System / paper | Maps | Onto | Method | Authoring vs. learned | Data needs | Reported result | Fit to Java / deterministic / few labels |
|---|---|---|---|---|---|---|---|
| AutoTutor (Graesser et al. 2000; Penumatsa 2003; Carmon 2019) | Student turns | Expectations and misconceptions per question | LSA cosine threshold plus RegEx | Hand-authored scripts; LSA space unsupervised | Domain corpus; small labelled set for thresholds | Explicit-present mean cosine 0.42 vs 0.65 threshold; ACE–human agreement "fair", near human–human after tuning; RegEx–LSA ρ = .471 (n = 5202) | High |
| DeepTutor / SEMILAR (Rus et al.) | Student turns | Expectations (LP-based tutor) | Semantic similarity suite; PSL with context | Authored expectations plus tuned models | DT-Grade labelled data | PSL > similarity-only by >7% accuracy | Medium–high |
| CBM: SQL-Tutor, KERMIT, EER-Tutor, J-LATTE (Ohlsson 1994; Mitrovic) | Solutions (structured or code) | Violated constraints (Cr, Cs) | Pattern match | Fully hand-authored (ASPIRE eases it) | None | Evaluations exist (numbers not retrieved) | High for code; untested on text |
| Model tracing / BUGGY / BKT (Anderson; Brown & Burton; Corbett & Anderson) | Steps | Correct and buggy productions; skill mastery | Rule matching; 2-state HMM | Rules authored; BKT parameters learned or set | Logs for BKT fitting | — | High for steps |
| Andes BN (Conati, Gertner & VanLehn 2002) | Entries | Solution-graph nodes and rule mastery | Bayesian network | Structure from solution graph; CPTs set | Little | Field-evaluated (numbers not retrieved) | High |
| GKT (Nakagawa et al. 2019) | Responses | Concept-graph nodes | GNN | Learned graph and weights | Large logs | Improved on 2 datasets (AUC not retrieved) | Low (data-hungry) |
| Kaldaras & Haudek 2022 | Argument text | LP levels 0–2 | BoW ensemble (CRC) | Learned per item | 361–848 labels per item | 72–98% accuracy | Low (labels) |
| Fowler et al. 2021 | EiPE text | Correct / incorrect | NLP classifier | Learned | Labelled per question | 87–89% accuracy, TA-level | Medium |
| Smith et al. 2025 | EiPE text | Multistructural / relational (SOLO) | LLM segmentation plus count threshold | Few labels | LLM at run time | κ = 0.61, 81% agreement | Idea reusable; LLM excluded |
