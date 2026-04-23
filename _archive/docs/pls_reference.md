+-----------------------------------------------------------------------+
| **PERSONALIZED LEARNING SYSTEMS**                                     |
|                                                                       |
| Comprehensive Technical Reference                                     |
|                                                                       |
| *12 Psychological Theories × Datasets × ML Architectures × Prompt     |
| Engine Methodology*                                                   |
|                                                                       |
| 3-Graph Architecture: Cognitive Graph \| Progression Graph \|         |
| Psychological Graph                                                   |
+-----------------------------------------------------------------------+

**Executive Summary**

This document is the master technical reference for the AI-Driven
Programming Education Platform. It synthesizes three foundational
sources --- the Learner State Architecture, the Prompt Analysis Engine
Methodology, and the Psychological Theories Integration --- into a
single unified reference that answers four questions for each of the 12
psychological theories underpinning the system:

> 1\. What does the theory explain and how is it defined?
>
> 2\. How does it integrate with the Prompt Analysis Engine and the
> 3-Graph Architecture?
>
> 3\. What datasets are used to train and validate the models that
> operationalize it?
>
> 4\. What deep learning and ML architectures implement the theory
> computationally?

  -----------------------------------------------------------------------
  **CORE INSIGHT:** *One student prompt → three simultaneous graph
  updates. The content updates the Cognitive Graph. The structure and
  independence update the Progression Graph. The language and framing
  update the Psychological Graph. All 12 theories operate as lenses
  reading from these three shared graphs.*

  -----------------------------------------------------------------------

**1. System Architecture Overview**

**1.1 The Three-Graph Architecture**

The learner state model consolidates 12 psychological theories into 3
interconnected knowledge graphs. Each graph tracks a fundamentally
different dimension of the learner. Theories operate as lenses reading
from these graphs in different combinations, eliminating redundancy and
producing a unified learner state.

+---------------+---------------------+-------------------------------+
| **Graph**     | **Description**     | **Theories & Signals**        |
+===============+=====================+===============================+
| COGNITIVE     | Encodes concept     | Theories: Information         |
| GRAPH (What   | nodes and           | Processing, Dual Coding,      |
| is Known)     | prerequisite        | Elaboration                   |
|               | relationships. 9    |                               |
|               | concept nodes       | Signals: Terminology          |
|               | across 3 tiers.     | precision, relational         |
|               | Updates from        | reasoning, dual-channel       |
|               | Content Channel.    | expression, transfer          |
|               |                     | indicators                    |
+---------------+---------------------+-------------------------------+
| PROGRESSION   | 7 stage nodes from  | Theories: ZPD,                |
| GRAPH         | Observation to      | Constructivism, Cognitive     |
| (             | Expert Autonomy.    | Apprenticeship, Situated      |
| Developmental | Updates from        | Learning                      |
| Stage)        | Structure Channel.  |                               |
|               |                     | Signals: Attempt presence,    |
|               |                     | question targeting, scaffold  |
|               |                     | usage, real-world framing     |
+---------------+---------------------+-------------------------------+
| PSYCHOLOGICAL | 9 psychological     | Theories: SCT, SRL, Flow,     |
| GRAPH         | state nodes ---     | Attribution, Imposter         |
| (Beliefs &    | positive, negative, | Syndrome                      |
| Motivation)   | SRL phases. Updates |                               |
|               | from Language       | Signals: Efficacy language,   |
|               | Channel.            | attribution narration, SRL    |
|               |                     | markers, flow indicators      |
+---------------+---------------------+-------------------------------+

**1.2 Theory-to-Graph Mapping**

  -----------------------------------------------------------------------
  **Theory**                   **Graph Mapping**
  ---------------------------- ------------------------------------------
  Information Processing       Cognitive Graph (Primary)
  Theory                       

  Dual Coding Theory           Cognitive Graph (Primary)

  Elaboration Theory           Cognitive Graph (Primary)

  Constructivist Learning      Progression Graph (Primary) + Cognitive
  Theory                       (Secondary)

  Zone of Proximal Development Progression Graph (Primary)

  Cognitive Apprenticeship     Progression Graph (Primary)
  Theory                       

  Situated Learning Theory     Progression Graph (Primary) + Cognitive
                               (Secondary)

  Social Cognitive Theory      Psychological Graph (Primary) +
                               Progression (Secondary)

  Self-Regulated Learning      Psychological Graph (Primary) +
  Theory                       Progression (Secondary)

  Flow Theory                  Psychological Graph (Primary) + Cognitive
                               (Secondary)

  Attribution Theory           Psychological Graph (Primary)

  Imposter Syndrome            Psychological Graph (Primary)
  -----------------------------------------------------------------------

**1.3 The Three-Channel Prompt Analysis Model**

Every student prompt is analyzed through three parallel channels
simultaneously before any graph update occurs. No prompt is routed to a
single channel --- all three channels process every input at once.

  ------------------------------------------------------------------------
  **Channel**     **Target Graph**   **Analyzes For**
  --------------- ------------------ -------------------------------------
  Content Channel Cognitive Graph    Concept identification, terminology
                                     precision, causal vs. surface
                                     reasoning, dual coding expression,
                                     cross-concept connections, schema
                                     transfer evidence

  Structure       Progression Graph  Prior attempt presence, question
  Channel                            targeting (global vs. specific), hint
                                     usage behavior, reasoning
                                     articulation, real-world framing,
                                     problem formulation vs. answering

  Language        Psychological      First-person ability statements,
  Channel         Graph              success/failure attribution
                                     narration, SRL phase markers
                                     (planning, monitoring, reflection),
                                     confidence-performance alignment,
                                     imposter distortion signals
  ------------------------------------------------------------------------

**1.4 Cognitive Graph: Nine Concept Nodes**

  -------------------------------------------------------------------------
  **Node ID**   **Concept**       **Tier**        **Cognitive Load & Dual
                                                  Coding Profile**
  ------------- ----------------- --------------- -------------------------
  variables     Variables & Data  Tier 1          Low --- foundational
                Types             Foundation      schema; Dual coding:
                                                  Verbal + Visual

  control       Control Flow      Tier 1          Med-High --- comparison +
                (if/else)         Foundation      branching; Visual
                                                  dominant

  loops         Loops             Tier 1          Med-High --- counter +
                                  Foundation      condition dual load;
                                                  Verbal + Visual

  functions     Functions         Tier 2          High --- abstraction
                                  Intermediate    layer; Verbal dominant

  datastructs   Data Structures   Tier 2          Med --- spatial memory
                                  Intermediate    aids; Visual dominant

  debugging     Debugging         Tier 2          Med --- metacognitive;
                Strategies        Intermediate    cross-cuts all nodes;
                                                  Verbal dominant

  recursion     Recursion         Tier 3 Advanced Very High --- highest WM
                                                  load; Visual dominant
                                                  (call stack essential)

  oop           Object-Oriented   Tier 3 Advanced High --- needs
                Prog.                             functions + data types;
                                                  Verbal + Visual

  algorithms    Algorithms        Tier 3 Advanced Very High --- terminal
                                                  elaboration node; Visual
                                                  dominant
  -------------------------------------------------------------------------

**1.5 Progression Graph: Seven Developmental Stages**

  --------------------------------------------------------------------------
  **Stage**   **Name**           **Behavioral Definition & Key Prompt
                                 Signal**
  ----------- ------------------ -------------------------------------------
  Stage 1     Observation        No attempt made. Requests complete solution
                                 or asks what code means. ZPD: overwhelmed.

  Stage 2a    Guided             Works with existing code. Can modify but
              Modification       not create from scratch.

  Stage 2b    Scaffolded         Attempts with scaffolding. Makes genuine
              Practice           attempts but uses support frequently.

  Stage 3     Coached Problem    Attempts independently; checks reasoning;
              Solving            explains approach; seeks validation.

  Stage 4a    Independent        Solves alone first; then asks for
              Solution           improvement/optimization.

  Stage 4b    Transfer &         Applies concepts to new real-world contexts
              Application        without prompting.

  Stage 5     Expert Autonomy    Formulates own problems; proposes
                                 architectural decisions; near-expert
                                 reasoning.
  --------------------------------------------------------------------------

**1.6 Psychological Graph: Nine State Nodes**

  ---------------------------------------------------------------------------
  **Node**           **Valence**   **Description**
  ------------------ ------------- ------------------------------------------
  High Anxiety       NEGATIVE      Challenge \>\> perceived skill. Flow
                                   channel broken. SRL monitoring collapses.

  Low Self-Efficacy  NEGATIVE      Persistent belief in inability.
                                   Forethought phase skipped. Mastery
                                   experiences urgently needed.

  Fixed Attribution  NEGATIVE      Failure → stable, uncontrollable causes.
                                   Success → luck. Locks in low efficacy.

  Forethought /      NEUTRAL+      SRL Phase 1 active. Goal-setting and
  Planning                         planning before task begins.

  Flow State         POSITIVE      Challenge-skill balanced. Deep focus.
                                   Intrinsic persistence. Peak encoding
                                   quality.

  Performance /      NEUTRAL+      SRL Phase 2 active. Real-time strategy
  Monitoring                       adjustment during task.

  Growth             POSITIVE      Belief that ability grows with effort.
  Self-Efficacy                    Expands flow channel. Drives ambitious
                                   goals.

  Self-Reflection /  NEUTRAL+      SRL Phase 3 active. Post-task evaluation.
  Evaluation                       Critical node --- imposter distortion
                                   occurs here.

  Adaptive           POSITIVE      Failure → controllable causes
  Attribution                      (effort/strategy). Success → internal
                                   capability. Efficacy compounds.
  ---------------------------------------------------------------------------

**1.7 Adaptive Intervention Types**

  ---------------------------------------------------------------------------
  **Intervention**       **Trigger Conditions**
  ---------------------- ----------------------------------------------------
  reduce_challenge       Surface encoding + Stage 1 + High Anxiety or Low
                         Self-Efficacy. Student is overwhelmed.

  worked_example         Surface encoding + Stage 1--2 + not in crisis.
                         Student needs concept modeled with narration.

  socratic_prompt        Partial encoding + Stage 2b--3. Student has schema
                         but needs targeted questioning to deepen it.

  attribution_reframe    Fixed Attribution OR Imposter Flag = TRUE. Must
                         address before any instructional advancement.

  mastery_surface        Solid/deep encoding + Imposter Flag TRUE or Low
                         Self-Efficacy despite good performance.

  increase_challenge     Solid/deep encoding + Stage 3+ + Growth
                         Self-Efficacy or Flow State confirmed.

  transfer_task          Deep encoding + Stage 4+ + ZPD at_boundary or
                         internalized. Apply logic in novel context.

  validate_and_advance   All three graphs positive: solid/deep + Stage 4+ +
                         Growth Efficacy/Flow + Adaptive Attribution.
  ---------------------------------------------------------------------------

**2. The 12 Theories: Complete Integration Reference**

Each section below provides the complete integration profile for one
theory: its definition, measurement instruments, recommended datasets,
ML architectures, its specific role in the Prompt Analysis Engine, and
the adaptive interventions it drives.

  -----------------------------------------------------------------------
  **GROUP A: How the Brain Processes & Encodes Information**

  -----------------------------------------------------------------------

Theories in Group A read primarily from the Cognitive Graph. They govern
how the Content Channel classifies concept encoding strength, dual
coding profiles, and cross-concept elaboration. These three theories
together produce the complete Cognitive Graph update for every student
prompt.

+-----+----------------------------------------------------------------+
| *   | **Information Processing Theory**                              |
| *T0 |                                                                |
| 1** | *Group A: How the Brain Processes & Encodes Information \|     |
|     | Primary: Cognitive Graph*                                      |
+-----+----------------------------------------------------------------+

**Definition & Theoretical Foundation**

Views learning as a sequence of cognitive operations: attention,
encoding, working memory management, and long-term retrieval. Learning
only occurs when information passes through all four stages
successfully. Working memory has strict capacity limits, making chunking
and sequencing critical design decisions.

  -----------------------------------------------------------------------
  **PROMPT SIGNAL:** *Short, panicked questions or asking the same
  question repeatedly signals working memory overload. Fluent, sequential
  questions signal successful encoding.*

  -----------------------------------------------------------------------

**Measurement Scales & Instruments**

Cognitive Load Scale (Paas, 1992); Nasa-TLX for task load; Working
Memory Capacity tasks (Operation Span, Reading Span).

**Recommended Datasets**

> **1.** EduNet (student interaction logs from MOOCs --- edX, Coursera):
> sequential prompt patterns, session dwell time, repeat-question
> detection.
>
> **2.** ASSISTments Dataset (Worcester Polytechnic): hint usage
> frequency, error repetition across sessions.
>
> **3.** Open University Learning Analytics Dataset (OULAD): weekly
> activity logs, assessment performance sequences.
>
> **4.** Khan Academy User Interaction Data: step-by-step problem
> attempts with time-on-task per sub-step.
>
> **5.** CodeWorkout Dataset: coding attempt logs with time stamps for
> detecting overload patterns.

**Deep Learning & ML Architectures**

> **1.** Long Short-Term Memory (LSTM) / Transformer-based sequence
> models: model temporal dependencies in session-level interaction logs
> to detect working memory overload patterns from sequential prompt
> data.
>
> **2.** Hidden Markov Models (HMMs): model latent cognitive states
> (attention, encoding, retrieval) from observable student action
> sequences.
>
> **3.** Attention-based BERT fine-tuned on student text: classify
> prompt complexity and cognitive load level from natural language.
>
> **4.** Bayesian Knowledge Tracing (BKT): probabilistic estimation of
> knowledge state transitions from attempt sequences.
>
> **5.** Gradient-Boosted Trees (XGBoost / LightGBM): predict encoding
> failure from tabular session features (dwell time, hint count, error
> rate).

**Role in the Prompt Analysis Engine**

  -----------------------------------------------------------------------
  The Content Channel scans for terminology precision and sequential
  reasoning. Vague or repeated questions trigger \"working memory
  overload\" flag → system reduces challenge and applies chunking
  scaffolds. The Structure Channel checks whether the student breaks
  problems into sub-steps, indicating chunking strategy.

  -----------------------------------------------------------------------

**Adaptive Interventions Triggered**

worked_example (reduce cognitive load), reduce_challenge, Socratic
chunk-by-chunk prompting.

+-----+----------------------------------------------------------------+
| *   | **Dual Coding Theory**                                         |
| *T0 |                                                                |
| 2** | *Group A: How the Brain Processes & Encodes Information \|     |
|     | Primary: Cognitive Graph*                                      |
+-----+----------------------------------------------------------------+

**Definition & Theoretical Foundation**

Humans process information through two partially independent but
interconnected systems: a verbal system for language-based processing
and a nonverbal system for imagery-based processing. Concepts encoded
through both channels are more robust, more retrievable, and better
transferred to novel contexts.

  -----------------------------------------------------------------------
  **PROMPT SIGNAL:** *A student who understands code can describe what it
  does verbally AND reason about its logical flow. Students encoding only
  through syntax have single-channel encoding.*

  -----------------------------------------------------------------------

**Measurement Scales & Instruments**

Dual Coding Encoding Profile (verbal_only / visual_only / dual) assessed
per concept node via prompt analysis; Paivio\'s Imagery Value Rating
Scale.

**Recommended Datasets**

> **1.** CSEDM Dataset (Computer Science Education Data Mining): code +
> explanation pairs that allow verbal/visual coding profile extraction.
>
> **2.** CodeHelp Interaction Logs: student natural-language
> explanations of their code alongside code snippets.
>
> **3.** GitHub Copilot Study Dataset (Microsoft Research): verbal
> descriptions of intended code behavior vs. actual implementation.
>
> **4.** Programming Education Interaction Corpus (PEIC): annotated
> student explanations tagged for verbal vs. structural reasoning.
>
> **5.** Khan Academy Computer Science logs: student comment-to-code
> ratio as dual coding proxy measure.

**Deep Learning & ML Architectures**

> **1.** Multi-modal Transformers (e.g., CodeBERT + RoBERTa): jointly
> encode the code (visual/structural) and the natural language
> explanation (verbal) to classify dual-channel vs. single-channel
> encoding.
>
> **2.** Graph Neural Networks (GNNs): represent the concept graph and
> detect which nodes have dual vs. single encoding based on edge
> evidence from student explanations.
>
> **3.** Contrastive Learning (SimCLR-style): learn representations that
> distinguish verbal-only, visual-only, and dual-encoded explanations.
>
> **4.** Semantic Textual Similarity models (sentence-BERT): measure
> alignment between a student\'s verbal description and the actual
> structural behavior of their code.
>
> **5.** Random Forest classifier: predict dual coding profile from
> engineered features (code-to-text ratio, structural keyword density,
> diagram reference count).

**Role in the Prompt Analysis Engine**

  -----------------------------------------------------------------------
  The Content Channel assigns a dual_coding profile (none / verbal_only /
  visual_only / dual) to each active concept node. When verbal_only is
  detected for a visual-dominant concept (e.g., recursion, control flow),
  the engine triggers a visual scaffolding response --- call stack
  diagrams, flowcharts, or execution traces.

  -----------------------------------------------------------------------

**Adaptive Interventions Triggered**

Visual scaffold insertion, worked_example with diagram narration,
mastery_surface with both verbal and structural confirmation.

+-----+----------------------------------------------------------------+
| *   | **Elaboration Theory**                                         |
| *T0 |                                                                |
| 3** | *Group A: How the Brain Processes & Encodes Information \|     |
|     | Primary: Cognitive Graph*                                      |
+-----+----------------------------------------------------------------+

**Definition & Theoretical Foundation**

Content organized from simple to complex, with increasing levels of
detail added progressively, produces deeper and more connected mental
models. Knowledge is structured hierarchically and revisited at higher
complexity levels over time.

  -----------------------------------------------------------------------
  **PROMPT SIGNAL:** *A student connecting a new concept to a prior one
  (\"this is like what we did with loops, but\...\") shows elaborative
  processing. Isolated surface-level responses indicate no bridging.*

  -----------------------------------------------------------------------

**Measurement Scales & Instruments**

Cross-concept bridging count per session; edge density growth in
cognitive graph; elaboration coding rubric applied to student
explanations.

**Recommended Datasets**

> **1.** ASSISTments Problem Set Sequences: prerequisite-ordered problem
> sets allowing elaboration depth measurement across concept tiers.
>
> **2.** Cognitive Tutor Algebra Dataset (Carnegie Learning):
> hierarchical concept sequences with hint-usage and error patterns per
> difficulty level.
>
> **3.** OULAD (Open University Learning Analytics): module-to-module
> progression data showing when students build on prior material.
>
> **4.** edX MOOC Data (HarvardX/MITx): discussion forum posts where
> students explicitly connect new content to previous modules.
>
> **5.** CodeWorkout Sequences: ordered programming problems from Tier 1
> through Tier 3 difficulty, enabling elaboration trajectory analysis.

**Deep Learning & ML Architectures**

> **1.** Knowledge Graph Embedding models (TransE, RotatE): represent
> concept nodes and prerequisite edges as embeddings; predict edge
> strength from student prompt evidence.
>
> **2.** Hierarchical Attention Networks (HAN): model the hierarchical
> structure of concept tiers and detect cross-tier elaboration signals
> in student text.
>
> **3.** Curriculum Learning-based Sequence Models: train models that
> explicitly reflect the Tier 1 → Tier 2 → Tier 3 progression and
> identify schema elaboration events.
>
> **4.** Dependency Parsing + Co-reference resolution NLP pipeline:
> extract cross-concept references from student free text to identify
> bridging statements.
>
> **5.** Graph Convolutional Networks (GCN): propagate encoding signals
> across concept graph edges to estimate downstream elaboration
> readiness.

**Role in the Prompt Analysis Engine**

  -----------------------------------------------------------------------
  The Content Channel detects cross-concept bridging language and updates
  edge weights between concept nodes in the Cognitive Graph. Deep
  encoding level is assigned when cross-concept connections are observed.
  The engine uses the concept tier structure to sequence adaptive
  challenges from simpler to more complex nodes.

  -----------------------------------------------------------------------

**Adaptive Interventions Triggered**

increase_challenge, transfer_task, Socratic questions that require
cross-concept bridging, validate_and_advance.

  -----------------------------------------------------------------------
  **GROUP B: How Learning Deepens Through Practice & Context**

  -----------------------------------------------------------------------

Theories in Group B read primarily from the Progression Graph. They
govern how the Structure Channel classifies developmental stage, ZPD
boundary position, and the type of scaffold the student needs. They
answer the question: where is this student in their journey toward
independence?

+-----+----------------------------------------------------------------+
| *   | **Constructivist Learning Theory**                             |
| *T0 |                                                                |
| 4** | *Group B: How Learning Deepens Through Practice & Context \|   |
|     | Primary: Progression Graph \| Secondary: Cognitive Graph*      |
+-----+----------------------------------------------------------------+

**Definition & Theoretical Foundation**

Learners actively construct their own understanding and knowledge of the
world by experiencing things and reflecting on those experiences, rather
than passively receiving information. Meaning is built by the learner
through experience, hypothesis testing, and self-correction.

  -----------------------------------------------------------------------
  **PROMPT SIGNAL:** *Students forming hypotheses (\"I think this fails
  because\...\") and self-correcting mid-conversation are constructing
  genuine understanding. Students who only ask for answers without
  reasoning are not.*

  -----------------------------------------------------------------------

**Measurement Scales & Instruments**

Constructivist Learning Environment Survey (CLES); Behavioral
Constructivism Index: frequency of self-correction, hypothesis
generation rate, concept reuse in new contexts, transfer task
performance.

**Recommended Datasets**

> **1.** ASSISTments Dataset: hint-request patterns and self-correction
> frequency after errors --- direct constructivism behavioral proxies.
>
> **2.** Cognitive Tutor (Carnegie Learning): tracks hypothesis
> generation and self-correction explicitly in scaffolded
> problem-solving sessions.
>
> **3.** PISA 2018 Dataset: collaborative problem-solving items that
> reward active hypothesis testing and conceptual construction.
>
> **4.** CodeHelp Interaction Logs: student attempts with revision
> history showing active knowledge construction through iteration.
>
> **5.** Programming Education Interaction Corpus (PEIC): annotated for
> active construction indicators (hypothesis present, self-correction,
> concept transfer).

**Deep Learning & ML Architectures**

> **1.** Recurrent Neural Networks (RNN/LSTM) on attempt sequences:
> detect self-correction and hypothesis-test cycles across multiple
> attempts on the same problem.
>
> **2.** Natural Language Inference (NLI) models (RoBERTa fine-tuned):
> classify whether a student statement represents hypothesis generation,
> self-correction, or passive reception.
>
> **3.** Reinforcement Learning from Human Feedback (RLHF)-style reward
> model: assign higher reward to responses demonstrating active
> construction (hypothesis + test + correction) vs. passive
> answer-seeking.
>
> **4.** Topic modeling (LDA, BERTopic): identify whether student
> explanations demonstrate conceptual depth vs. surface syntax
> repetition.
>
> **5.** Bayesian Network: probabilistic model linking constructivism
> indicators (hypothesis presence, attempt count, self-correction) to
> progression stage assignment.

**Role in the Prompt Analysis Engine**

  -----------------------------------------------------------------------
  The Structure Channel detects whether the student attempted before
  asking, formed a hypothesis, or self-corrected. Active construction
  signals advance Progression Graph stage. Passive reception
  (answer-seeking without reasoning) keeps the student in early
  Progression stages and triggers worked_example or Socratic scaffolds.

  -----------------------------------------------------------------------

**Adaptive Interventions Triggered**

socratic_prompt, worked_example, reduce_challenge (if no construction
evident), increase_challenge (if robust construction observed).

+-----+----------------------------------------------------------------+
| *   | **Zone of Proximal Development (ZPD)**                         |
| *T0 |                                                                |
| 5** | *Group B: How Learning Deepens Through Practice & Context \|   |
|     | Primary: Progression Graph*                                    |
+-----+----------------------------------------------------------------+

**Definition & Theoretical Foundation**

The range of development where an individual can achieve higher levels
of understanding and skill with the guidance of an adult or capable
peer. Distinguishes between what a student can do independently (actual
development) and what they can achieve with support (potential
development).

  -----------------------------------------------------------------------
  **PROMPT SIGNAL:** *The type of help requested reveals ZPD position.
  Asking for a complete solution signals overwhelm (outside ZPD). Asking
  targeted questions after an attempt signals being inside the ZPD.
  Solving independently then verifying signals internalization.*

  -----------------------------------------------------------------------

**Measurement Scales & Instruments**

Scaffold-fading performance stability: (1) scaffolded accuracy, (2)
independent accuracy, (3) transfer accuracy. ZPD boundary = gap between
scaffolded and independent performance. Self-report: \"I could solve
similar problems without help\" (1--7 scale).

**Recommended Datasets**

> **1.** ASSISTments Scaffolded Problem Sequences: direct measurement of
> scaffolded vs. unscaffolded performance gaps per student per concept.
>
> **2.** Cognitive Tutor ZPD Logs: faded hint data enabling
> scaffold-fading performance stability analysis.
>
> **3.** Khan Academy Mastery Learning Data: progression through
> \"mastered,\" \"practiced,\" \"needs review\" states --- a direct ZPD
> operationalization.
>
> **4.** OULAD: comparison of assessed vs. unassessed performance in
> different support conditions.
>
> **5.** Juho Kim\'s MOOClet Dataset: A/B tested scaffolding conditions
> providing natural experimental ZPD measurement.

**Deep Learning & ML Architectures**

> **1.** Item Response Theory (IRT) + Deep Knowledge Tracing (DKT):
> estimate the boundary between current and potential performance;
> predict when a student is inside vs. outside the ZPD for each concept.
>
> **2.** Deep Knowledge Tracing (DKT, Piech et al.): LSTM-based model
> that predicts the probability of correct response on next item --- the
> backbone for ZPD boundary estimation.
>
> **3.** Performance Gap Regression Models: predict the
> scaffolded-to-independent performance gap using concept encoding
> strength and session features.
>
> **4.** Causal Inference Models (DoWhy, CausalML): estimate the causal
> effect of scaffold removal on performance to identify true
> internalization vs. scaffold dependence.
>
> **5.** Multi-Armed Bandit / Contextual Bandit: dynamically select the
> optimal scaffolding level for each student to keep them in the ZPD in
> real time.

**Role in the Prompt Analysis Engine**

  -----------------------------------------------------------------------
  The Structure Channel classifies ZPD boundary position (overwhelmed /
  inside_zpd / at_boundary / internalized) alongside stage assignment.
  The ZPD position directly determines scaffolding intensity. The
  cross-graph consistency rules use ZPD position to override intervention
  type when cognitive ability and progression stage contradict each
  other.

  -----------------------------------------------------------------------

**Adaptive Interventions Triggered**

reduce_challenge (overwhelmed), socratic_prompt (inside_zpd),
transfer_task (at_boundary), validate_and_advance (internalized).

+-----+----------------------------------------------------------------+
| *   | **Cognitive Apprenticeship Theory**                            |
| *T0 |                                                                |
| 6** | *Group B: How Learning Deepens Through Practice & Context \|   |
|     | Primary: Progression Graph*                                    |
+-----+----------------------------------------------------------------+

**Definition & Theoretical Foundation**

Emphasizes knowledge applicable in real-world settings through six
teaching methods: modeling, coaching, scaffolding (from traditional
apprenticeship) plus articulation, reflection, and exploration.
Describes a clear progression from observation to full autonomy.

  -----------------------------------------------------------------------
  **PROMPT SIGNAL:** *Depth and independence of prompts reveals
  apprenticeship phase. \"How do I do this?\" is coaching phase. \"I did
  it this way --- is there a better approach?\" is reflection phase. \"I
  want to try building X from scratch\" is exploration phase.*

  -----------------------------------------------------------------------

**Measurement Scales & Instruments**

Maastricht Clinical Teaching Questionnaire (MCTQ); Phase detection
rubric mapping prompts to modeling / coaching / scaffolding /
articulation / reflection / exploration stages.

**Recommended Datasets**

> **1.** Stack Overflow Question Archive: expert-to-novice knowledge
> transfer patterns that parallel cognitive apprenticeship modeling
> phase.
>
> **2.** GitHub Issue Tracker + Pull Request Comments: real-world
> coaching/reflection exchanges between novice contributors and senior
> reviewers.
>
> **3.** CodeHelp Platform Logs: tutoring interaction logs naturally
> structured around the six apprenticeship phases.
>
> **4.** CSEDM Dataset: problem-solving sessions with tutor feedback
> coded for modeling, scaffolding, and coaching events.
>
> **5.** MIT OpenCourseWare 6.00x Forum Data: discussion posts revealing
> student phase transitions from observation through exploration.

**Deep Learning & ML Architectures**

> **1.** Multi-label Sequence Classifier (BERT/RoBERTa fine-tuned):
> classify each student prompt into one of the six Cognitive
> Apprenticeship phases simultaneously.
>
> **2.** Hidden Markov Model over phase sequences: model transitions
> between apprenticeship phases across a session to detect stage
> advancement or regression.
>
> **3.** Few-shot learning with GPT-class models: classify
> apprenticeship phase from minimal examples using in-context learning,
> useful when labeled data is scarce.
>
> **4.** Ordinal Regression Models: predict apprenticeship phase as an
> ordered variable (Observation \< Coaching \< Scaffolding \<
> Articulation \< Reflection \< Exploration).
>
> **5.** Reinforcement Learning: optimize the sequence of modeling,
> coaching, and scaffolding actions to accelerate phase progression
> toward Expert Autonomy.

**Role in the Prompt Analysis Engine**

  -----------------------------------------------------------------------
  The Structure Channel uses Cognitive Apprenticeship phase detection to
  enrich Progression Graph stage assignment. The prompt analysis
  distinguishes whether the student is in an observation, coaching, or
  exploration mode, mapping these to Stage 1 through Stage 5. The six
  apprenticeship methods inform which intervention type to apply at each
  stage.

  -----------------------------------------------------------------------

**Adaptive Interventions Triggered**

worked_example (modeling phase), socratic_prompt
(coaching/articulation), increase_challenge (exploration phase),
validate_and_advance (near-expert reflection).

+-----+----------------------------------------------------------------+
| *   | **Situated Learning Theory**                                   |
| *T0 |                                                                |
| 7** | *Group B: How Learning Deepens Through Practice & Context \|   |
|     | Primary: Progression Graph \| Secondary: Cognitive Graph*      |
+-----+----------------------------------------------------------------+

**Definition & Theoretical Foundation**

Learning occurs most effectively when embedded in authentic contexts and
social participation rather than isolated, decontextualized instruction.
Students should see themselves as developing members of a real community
of practice. Identity formation (\"I am becoming a programmer\") is a
measurable outcome.

  -----------------------------------------------------------------------
  **PROMPT SIGNAL:** *Students connecting code to real-world purpose
  (\"in a real app you would need to\...\") show situated understanding.
  Students treating code as abstract syntax detached from any use do
  not.*

  -----------------------------------------------------------------------

**Measurement Scales & Instruments**

Community of Practice Identity Scale; Real-world framing frequency in
prompts; Transfer task performance in domain-shifted contexts.

**Recommended Datasets**

> **1.** GitHub Open Source Contribution Logs: authentic
> community-of-practice participation data showing identity development
> through real project contribution.
>
> **2.** Stack Overflow User Activity Timelines: situated community
> participation from novice question-asker to expert responder ---
> direct identity trajectory data.
>
> **3.** Kaggle Competition Participation Data: authentic,
> context-embedded programming challenges with community feedback loops.
>
> **4.** FreeCodeCamp Project Completion Logs: project-based learning
> with real-world output framing (web apps, data visualizations).
>
> **5.** Replit Multiplayer Coding Session Logs: collaborative,
> context-embedded programming sessions.

**Deep Learning & ML Architectures**

> **1.** Named Entity Recognition (NER) + domain classification: detect
> real-world context references in student prompts (app names, data
> domains, industry terms) to measure situated framing frequency.
>
> **2.** Community Embedding Models (node2vec on GitHub contribution
> graphs): represent a student\'s position within a community of
> practice as an embedding.
>
> **3.** Transfer Learning fine-tuned on domain-specific corpora:
> measure how well a student\'s reasoning generalizes across programming
> domains as a situated learning proxy.
>
> **4.** Social Network Analysis + GNN: model the community-of-practice
> graph and predict identity development from participation patterns.
>
> **5.** Semantic Similarity (sentence-BERT): measure alignment between
> student\'s framing and real-world application language to score
> situated encoding.

**Role in the Prompt Analysis Engine**

  -----------------------------------------------------------------------
  The Structure Channel detects real-world framing language in student
  prompts, which advances the student to Stage 4b (Transfer &
  Application) and Stage 5 (Expert Autonomy) in the Progression Graph.
  The Content Channel uses situated framing as a cross-concept bridging
  signal (deep encoding indicator). Transfer tasks are the engine\'s
  primary instrument for situated learning activation.

  -----------------------------------------------------------------------

**Adaptive Interventions Triggered**

transfer_task, validate_and_advance, real-world context injection in
scaffolds (worked examples reference authentic use cases).

  -----------------------------------------------------------------------
  **GROUP C: Motivation, Belief & Self-Regulation**

  -----------------------------------------------------------------------

Theories in Group C read primarily from the Psychological Graph. They
govern how the Language Channel classifies the student\'s belief state,
self-regulation phase, attribution style, and engagement quality. The
Psychological Graph overrides Progression for intervention type when
beliefs and performance contradict each other.

+-----+----------------------------------------------------------------+
| *   | **Social Cognitive Theory (SCT)**                              |
| *T0 |                                                                |
| 8** | *Group C: Motivation, Belief & Self-Regulation \| Primary:     |
|     | Psychological Graph \| Secondary: Progression Graph*           |
+-----+----------------------------------------------------------------+

**Definition & Theoretical Foundation**

Developed by Bandura, SCT explains learning as a dynamic interaction
between personal factors, behavior, and environment through reciprocal
determinism. Central constructs are self-efficacy (belief in
capability), observational learning, outcome expectations, and
self-regulation. Students\' beliefs about their ability shape effort,
persistence, strategy use, and performance as much as actual ability
does.

  -----------------------------------------------------------------------
  **PROMPT SIGNAL:** *\"I can\'t do this\" and \"I\'ll never understand
  recursion\" signal low self-efficacy. \"I think I almost have it, let
  me try another approach\" signals healthy efficacy. Tracking this ratio
  over time is a direct efficacy readout.*

  -----------------------------------------------------------------------

**Measurement Scales & Instruments**

General Self-Efficacy Scale (GSE, Schwarzer & Jerusalem, 1995); Computer
Programming Self-Efficacy Scale (CPSES); Bandura\'s Self-Efficacy
Subscale from the MSLQ.

**Recommended Datasets**

> **1.** MSLQ Validated Dataset (Pintrich et al.): self-efficacy items
> paired with academic performance --- the gold standard SCT validation
> dataset.
>
> **2.** ASSISTments + Self-report Pairs: behavioral engagement metrics
> paired with periodic self-efficacy surveys.
>
> **3.** edX HarvardX Dataset: engagement dropout patterns combined with
> pre-course confidence self-reports.
>
> **4.** Cognitive Tutor SCT Annotations: sessions with coded
> self-efficacy language and corresponding performance trajectories.
>
> **5.** BrainStation Coding Bootcamp Survey Data: longitudinal
> self-efficacy + performance pairs across an intensive coding program.

**Deep Learning & ML Architectures**

> **1.** Sentiment Analysis + Efficacy Language Classifier (BERT
> fine-tuned on MSLQ language): classify first-person ability statements
> as high/low self-efficacy with internal/external attribution.
>
> **2.** Longitudinal Mixed-Effects Models: track self-efficacy
> trajectories over multiple sessions, separating stable trait from
> volatile state efficacy.
>
> **3.** Recurrent Sequence Models (LSTM): model how efficacy signals
> compound or decay across an interaction session, capturing reciprocal
> determinism dynamics.
>
> **4.** Causal Inference (Propensity Score Matching): estimate the
> causal effect of mastery experiences (correct solutions) on subsequent
> self-efficacy scores.
>
> **5.** Survival Analysis Models: predict time-to-dropout as a function
> of self-efficacy trajectory --- critical for early warning systems.

**Role in the Prompt Analysis Engine**

  -----------------------------------------------------------------------
  The Language Channel extracts the efficacy_language quotation and
  assigns the primary Psychological node (Low Self-Efficacy / Growth
  Self-Efficacy). This directly gates the intervention type: Low
  Self-Efficacy triggers mastery_surface or attribution_reframe before
  any instructional advancement. The cross-graph rule \"Psychological
  overrides Progression\" is grounded entirely in SCT\'s finding that
  beliefs shape performance as much as ability does.

  -----------------------------------------------------------------------

**Adaptive Interventions Triggered**

mastery_surface, attribution_reframe, validate_and_advance with explicit
competence affirmation, reduce_challenge to enable mastery experiences.

+-----+----------------------------------------------------------------+
| *   | **Self-Regulated Learning (SRL) Theory**                       |
| *T0 |                                                                |
| 9** | *Group C: Motivation, Belief & Self-Regulation \| Primary:     |
|     | Psychological Graph \| Secondary: Progression Graph*           |
+-----+----------------------------------------------------------------+

**Definition & Theoretical Foundation**

The intentional and strategic adaptation of learning activities to
achieve goals. Zimmerman\'s model identifies three phases: forethought
(goal-setting before the task), performance (real-time monitoring during
the task), and self-reflection (evaluation and causal attribution after
the task).

  -----------------------------------------------------------------------
  **PROMPT SIGNAL:** *Planning (\"before I start, I want to understand
  X\"), monitoring (\"I tried this but it\'s not working because I
  think\...\"), and reflecting (\"I got it right but I\'m not sure why\")
  together form a complete SRL profile.*

  -----------------------------------------------------------------------

**Measurement Scales & Instruments**

Motivated Strategies for Learning Questionnaire (MSLQ); Learning and
Study Strategies Inventory (LASSI); Online Self-Regulated Learning
Questionnaire (OSLQ); Academic Self-Regulated Learning Scale (A-SRL-S,
Magno, 2010).

**Recommended Datasets**

> **1.** MSLQ Validation Dataset: the canonical SRL self-report dataset
> with all three phases measured and academic outcome correlations.
>
> **2.** ASSISTments Behavioral SRL Proxies: hint timing (before/after
> attempt), revision patterns, and resubmission behavior as monitoring
> indicators.
>
> **3.** Coursera/edX Learner Behavior Logs: time spent on instructions
> before coding (forethought), mid-module activity patterns
> (performance), and post-module review (reflection).
>
> **4.** Khan Academy Mastery Learning Logs: strategic hint use vs.
> immediate hint use --- direct Forethought/Monitoring distinction.
>
> **5.** PISA 2018 Learning Strategies Module: validated cross-national
> SRL behavioral and self-report data for model benchmarking.

**Deep Learning & ML Architectures**

> **1.** SRL Phase Classifier (BERT/RoBERTa fine-tuned on SRL-annotated
> corpora): classify each student utterance into Forethought /
> Performance / Reflection phase from natural language markers.
>
> **2.** Multi-task Learning model: simultaneously predict SRL phase,
> engagement level, and intervention type from the same prompt
> representation.
>
> **3.** Sequence-to-sequence Transformer: model the temporal flow of
> SRL phases across a session and predict phase transitions.
>
> **4.** Behavioral Pattern Mining (Sequential Pattern Mining, GSP):
> extract frequent behavioral patterns that indicate each SRL phase from
> log data.
>
> **5.** Structural Equation Modeling (SEM): validate the causal pathway
> from SRL phase quality to concept encoding strength and progression
> stage advancement.

**Role in the Prompt Analysis Engine**

  -----------------------------------------------------------------------
  The Language Channel detects Forethought markers (\"before I start\"),
  Performance/Monitoring markers (\"I tried X because Y\"), and
  Reflection markers (\"looking back, I should have\"). The SRL phase is
  included in the structured output report and directly determines the
  construction of the next scaffold --- Forethought students receive
  planning guides, Monitoring students receive Socratic probes,
  Reflection students receive attribution reframing. The SRL phase also
  cross-validates Progression stage (Monitoring active → Stage 3+
  expected).

  -----------------------------------------------------------------------

**Adaptive Interventions Triggered**

All interventions are shaped by SRL phase. Forethought: goal
clarification scaffolds. Performance: socratic_prompt. Reflection:
attribution_reframe, mastery_surface. SRL phase absent: worked_example
to model the monitoring cycle.

+-----+----------------------------------------------------------------+
| *   | **Flow Theory**                                                |
| *T1 |                                                                |
| 0** | *Group C: Motivation, Belief & Self-Regulation \| Primary:     |
|     | Psychological Graph \| Secondary: Cognitive Graph*             |
+-----+----------------------------------------------------------------+

**Definition & Theoretical Foundation**

A psychological state of optimal engagement and enjoyment --- being \"in
the zone\" --- that occurs when challenge and skill are in balance. Flow
is characterized by sustained attention, challenge-skill equilibrium,
and intrinsic persistence.

  -----------------------------------------------------------------------
  **PROMPT SIGNAL:** *Short panicked questions signal anxiety (challenge
  exceeds skill). Careless or disengaged prompts signal boredom (skill
  exceeds challenge). Deep, focused, progressively complex questions with
  natural momentum signal flow.*

  -----------------------------------------------------------------------

**Measurement Scales & Instruments**

Flow State Scale (FSS, Jackson & Marsh, 1996): 36 items, internal
consistency α = 0.83, hierarchical model. Flow Short Scale (16 items):
Fluency + Absorption + Worry. Behavioral composite: time-on-task,
tab-switching rate, error-correction cycles, voluntary continuation past
required modules. Challenge-Skill discrepancy: \|perceived_difficulty --
perceived_skill\| ≈ 0 → flow conditions.

**Recommended Datasets**

> **1.** Khan Academy Engagement Logs: session length, voluntary
> continuation, and skip rates as behavioral flow proxies.
>
> **2.** edX Learner Engagement Dataset: time-on-task distribution,
> click patterns, and video replay rates as attention/absorption
> indicators.
>
> **3.** ASSISTments Time-on-Task Data: millisecond-level response time
> data for challenge-skill equilibrium estimation.
>
> **4.** Kaggle Kernel Session Data: long uninterrupted coding sessions
> as flow state behavioral indicators.
>
> **5.** EEG + Experience Sampling Method Studies (Nakamura &
> Csikszentmihalyi paradigm datasets): physiological + momentary
> self-report gold standard for flow state validation.

**Deep Learning & ML Architectures**

> **1.** Bidirectional LSTM on session interaction sequences: detect
> flow-indicative patterns (sustained engagement, progressive depth,
> absence of panic or boredom markers) across time.
>
> **2.** Anomaly Detection (Autoencoder): identify departures from
> baseline engagement patterns as anxiety or boredom signals.
>
> **3.** Regression models (Ridge / Gradient Boosting) on behavioral
> composites: predict FSS-validated flow state from behavioral
> indicators (dwell time, error cycles, continuation rate).
>
> **4.** Reinforcement Learning (RL) agent for challenge calibration:
> optimize challenge level in real time to maintain challenge-skill
> balance --- the direct computational instantiation of Flow Theory.
>
> **5.** Time-series classification (TimeSeriesForest, ROCKET): classify
> engagement trajectory shapes (sustained flow vs. anxiety spike vs.
> boredom plateau) from session-level behavioral logs.

**Role in the Prompt Analysis Engine**

  -----------------------------------------------------------------------
  The Language Channel detects flow state from conversational momentum
  (progressive depth, absence of panic language) and assigns the Flow
  State node. The Psychological Graph uses Flow as a positive gateway ---
  students in Flow receive increase_challenge and transfer tasks. Anxiety
  detection (challenge \> skill) triggers reduce_challenge immediately.
  The cross-graph rule uses Cognitive encoding depth as a secondary
  signal to distinguish anxiety (partial encoding + negative language)
  from boredom (solid encoding + disengaged language).

  -----------------------------------------------------------------------

**Adaptive Interventions Triggered**

increase_challenge (flow confirmed), reduce_challenge (anxiety
detected), transfer_task (flow + deep encoding), challenge calibration
scaffolds (boredom: skill exceeds challenge).

+-----+----------------------------------------------------------------+
| *   | **Attribution Theory**                                         |
| *T1 |                                                                |
| 1** | *Group C: Motivation, Belief & Self-Regulation \| Primary:     |
|     | Psychological Graph*                                           |
+-----+----------------------------------------------------------------+

**Definition & Theoretical Foundation**

A theoretical framework about how people ascribe causes to their own and
others\' behavior, particularly whether motives are internal/personal
(dispositional) or external/circumstantial (situational). Kelley\'s
three principles: covariation, discounting, and augmentation. Critical
dimension: internal controllable (effort, strategy) vs. external or
fixed (luck, innate ability) attributions.

  -----------------------------------------------------------------------
  **PROMPT SIGNAL:** *\"I got it wrong because I\'m bad at this\" is
  internal, stable, uncontrollable --- damaging. \"I got it wrong because
  I didn\'t read the error message carefully\" is internal, unstable,
  controllable --- healthy. Attribution style is directly readable in how
  students narrate failure.*

  -----------------------------------------------------------------------

**Measurement Scales & Instruments**

Multidimensional Multiattributional Causality Scale (MMCS);
Attributional Style Questionnaire (ASQ); Attributional Complexity Scale
(ACS); post-task open-ended prompt: \"What most influenced your
performance on this task?\"

**Recommended Datasets**

> **1.** ASQ Validation Dataset (Seligman et al.): the canonical
> attribution style instrument with depression/achievement outcome
> correlations.
>
> **2.** ASSISTments Post-Error Attribution Probes: brief Likert items
> after incorrect responses (\"My performance was due to my ability /
> effort / task difficulty / luck\").
>
> **3.** PISA Achievement Motivation Module: cross-national
> self-attribution data linked to academic performance.
>
> **4.** Cognitive Tutor Attribution-Coded Sessions: tutor interaction
> logs annotated for fixed vs. growth attribution language.
>
> **5.** Coding Bootcamp Exit Survey Data: longitudinal attribution
> style × dropout correlation data.

**Deep Learning & ML Architectures**

> **1.** Causal Attribution Classifier (BERT fine-tuned on ASQ + causal
> language corpora): classify attribution sentences into
> (internal/external) × (stable/unstable) ×
> (controllable/uncontrollable) --- the Weiner attribution dimensions.
>
> **2.** Named Entity Recognition + Dependency Parsing: extract causal
> sentences (\"because I\...\", \"it was due to\...\") from student
> prompts for attribution analysis.
>
> **3.** Longitudinal Logistic Regression: model the relationship
> between repeated fixed attribution patterns and dropout / performance
> decline over time.
>
> **4.** Text-based Sentiment-Causal Pipeline: combine sentiment
> analysis (negative affect) with causal attribution detection for joint
> Psychological Graph node assignment.
>
> **5.** Counterfactual Reasoning Detection models: identify students
> who exhibit \"it would have been different if only\...\" language as
> an indicator of controllable-unstable attribution style.

**Role in the Prompt Analysis Engine**

  -----------------------------------------------------------------------
  The Language Channel\'s attribution sentence identification step is the
  primary instrument for this theory. Attribution sentences are flagged
  for priority analysis in the input pre-processing stage. The engine
  assigns Fixed Attribution or Adaptive Attribution to the Psychological
  node and uses this to gate the attribution_reframe intervention. The
  imposter flag detection logic builds directly on attribution
  classification (success + luck attribution + correct performance =
  imposter pattern).

  -----------------------------------------------------------------------

**Adaptive Interventions Triggered**

attribution_reframe (fixed attribution detected), mastery_surface +
adaptive attribution framing (imposter pattern), strategy-focused
reframing prompts (\"What strategy did you use that worked?\").

+-----+----------------------------------------------------------------+
| *   | **Imposter Syndrome**                                          |
| *T1 |                                                                |
| 2** | *Group C: Motivation, Belief & Self-Regulation \| Primary:     |
|     | Psychological Graph*                                           |
+-----+----------------------------------------------------------------+

**Definition & Theoretical Foundation**

A psychological experience where high-achieving individuals doubt their
accomplishments and fear being exposed as frauds despite evidence of
competence. In learning contexts, it manifests as a systematic mismatch
between actual performance and self-perceived competence ---
specifically, discounting successes while amplifying failures.

  -----------------------------------------------------------------------
  **PROMPT SIGNAL:** *A student who solves a problem correctly then says
  \"I probably just got lucky\" or \"I\'m sure there\'s a better way and
  I just don\'t know it\" is displaying imposter cognition. Also watch
  for excessive apologizing, over-qualification, and dismissing correct
  reasoning.*

  -----------------------------------------------------------------------

**Measurement Scales & Instruments**

Clance Impostor Phenomenon Scale (CIPS, 20 items);
Confidence-Performance Discrepancy Score: (self-rated confidence) minus
(actual performance); behavioral indicators: excessive hint usage
despite good performance, avoiding advanced modules, over-checking
correct solutions.

**Recommended Datasets**

> **1.** CIPS Validation Dataset (Clance & Imes): canonical imposter
> syndrome measurement data with achievement and self-report
> correlations.
>
> **2.** ASSISTments Confidence-Performance Data: student confidence
> ratings before/after problems paired with objective accuracy ---
> direct discrepancy score computation.
>
> **3.** Coding Bootcamp Self-Report Longitudinal Data: imposter
> feelings, demographic data, and performance trajectories over a
> 12-week intensive program.
>
> **4.** GitHub Activity + Self-Report Studies: imposter syndrome
> prevalence and behavioral patterns in open-source contribution
> contexts.
>
> **5.** Imposter Syndrome in CS Education Survey Data (multiple
> institutions): large-scale validated dataset linking CIPS scores to CS
> course outcomes.

**Deep Learning & ML Architectures**

> **1.** Confidence-Performance Discrepancy Model (regression): predict
> imposter flag from the gap between self-reported confidence and
> objective accuracy --- the most direct computational
> operationalization.
>
> **2.** Distortion Detection Classifier (BERT fine-tuned): detect
> imposter-specific language patterns at the Self-Reflection node (luck
> attribution on success, minimizing, over-apologizing, peer
> comparison).
>
> **3.** Anomaly Detection over session sequences: identify students
> whose positive performance trajectory does not match their efficacy
> language trajectory --- the core imposter diagnostic pattern.
>
> **4.** Multi-task Learning (imposter detection + attribution
> classification + efficacy estimation): share representations across
> related psychological constructs for more accurate joint detection.
>
> **5.** Longitudinal Mixed Effects Model: track CIPS-equivalent
> behavioral scores over time to distinguish state imposter activation
> (triggered by difficulty spike) from trait imposter tendency.

**Role in the Prompt Analysis Engine**

  -----------------------------------------------------------------------
  Imposter Syndrome operates as a distortion flag at the Self-Reflection
  node rather than as a primary node. The engine checks: correct solution
  produced + luck/minimizing/over-apologizing language + peer comparison
  → IMPOSTER FLAG = TRUE. When the flag is TRUE, the cross-graph
  consistency rule forces mastery_surface before any instructional
  advancement. The next scaffold explicitly names what the student
  demonstrated (\"Notice what you just did\...\") to counter the
  discounting mechanism.

  -----------------------------------------------------------------------

**Adaptive Interventions Triggered**

mastery_surface (surface competence evidence explicitly),
attribution_reframe (redirect from luck/fraud attribution), normative
reassurance, validate_and_advance only after distortion addressed.

**3. Cross-Graph Interaction & Consistency Rules**

The three graphs influence each other through six bidirectional
pathways. Understanding these pathways is critical for resolving
contradictions between graph placements --- the most diagnostically
significant signals in the system.

  -----------------------------------------------------------------------
  **Cross-Graph         **Mechanism**
  Pathway**             
  --------------------- -------------------------------------------------
  Cognitive →           What a student knows determines where they are
  Progression           developmentally. Strong encoding of loops and
                        functions places a student further along the
                        Progression Graph automatically.

  Progression →         Developmental stage shapes self-efficacy. A
  Psychological         student successfully solving coached problems
                        will show higher efficacy than one overwhelmed at
                        observation.

  Psychological →       Beliefs and emotional state directly affect
  Cognitive             encoding quality. A student in flow encodes more
                        deeply than an anxious student.

  Cognitive →           Concept mastery produces mastery experiences that
  Psychological         build self-efficacy (SCT). Successfully encoding
                        recursion changes how a student narrates their
                        capability.

  Psychological →       Self-regulation drives stage advancement. An
  Progression           SRL-active student (forethought phase) advances
                        faster. Low efficacy causes stalling in early
                        stages.

  Progression →         Higher developmental stages expose students to
  Cognitive             more complex material, forcing deeper schema
                        construction and elaboration.
  -----------------------------------------------------------------------

**3.1 Priority Resolution for Contradictions**

When cross-graph signals contradict each other, three priority rules
apply in order:

1.  Psychological Graph overrides Progression for intervention type.
    Even if a student is developmentally ready for Stage 4 challenges,
    active Imposter distortion or High Anxiety must be addressed first.
    Advancing challenge before addressing belief state will worsen both.

2.  Cognitive Graph overrides Progression for concept-specific
    placement. A student who is generally at Stage 3 but has
    surface-level encoding of recursion specifically is placed at Stage
    2b for recursion. Progression stage is concept-specific.

3.  Structure Channel signals override Language Channel signals for
    stage assignment. Behavioral independence (attempt made, solution
    completed) is more reliable than self-reported confidence. A student
    who says \"I have no idea\" but submits a correct solution is placed
    at Stage 4, not Stage 1.

**3.2 Expected Correlations & Diagnostic Deviations**

  -----------------------------------------------------------------------
  **Expected Correlation** **Diagnostic Significance of Deviation**
  ------------------------ ----------------------------------------------
  Solid/deep Cognitive     If Cognitive solid but Progression Stage 1--2:
  encoding → Stage 3+      student has theoretical knowledge but
  expected                 confidence/anxiety is blocking engagement.
                           Likely Low Self-Efficacy or Anxiety in
                           Psychological Graph.

  Stage 4+ Progression →   If Stage 4+ but Psychological shows Low
  Growth Efficacy or Flow  Self-Efficacy or Imposter Flag: student is
  expected                 performing beyond what they believe they can
                           do. Classic imposter pattern --- most urgent
                           intervention case.

  SRL                      If Monitoring/Reflection active but
  Monitoring/Reflection →  Progression shows Stage 1--2: re-examine ---
  Stage 3+ expected        monitoring signals may be about a prior,
                           different task.

  Fixed Attribution across Single-session Fixed Attribution may be
  sessions → stalled       situational. Repeated across sessions with no
  Progression              Progression advancement = learned helplessness
                           pattern.
  -----------------------------------------------------------------------

**4. Complete Worked Examples: Prompt → Three-Graph Classification**

The following four examples trace the complete classification logic from
raw student prompt to structured intervention recommendation,
illustrating how the theories, datasets, and ML architectures converge
in practice.

  -----------------------------------------------------------------------
  **EXAMPLE 1 --- Overwhelmed Beginner: All Negative Signals Aligned**

  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
  **STUDENT PROMPT:** *\"My loop isn\'t working. Can you just fix it for
  me? I\'ve been staring at this for an hour and nothing makes sense.
  I\'m probably just not smart enough for programming.\"*

  -----------------------------------------------------------------------

  -------------------------------------------------------------------------
  **Graph**       **Classification**           **Evidence**
  --------------- ---------------------------- ----------------------------
  COGNITIVE GRAPH loops node: surface          \"nothing makes sense\" ---
                  encoding. No prior attempt   no causal or structural
                  described. No error          reasoning present. Encoding
                  characterized. No reasoning  level: surface.
                  offered. No dual-channel     
                  expression. \"Nothing makes  
                  sense\" = global confusion,  
                  not specific gap.            

  PROGRESSION     Stage 1 --- Observation.     \"Can you just fix it for
  GRAPH           \"Fix it for me\" = complete me?\" --- absence of attempt
                  solution request. No prior   is the primary gate. Stage:
                  attempt. ZPD position:       1, ZPD: overwhelmed.
                  overwhelmed --- no specific  
                  failure point identified,    
                  challenge has exceeded       
                  current schema.              

  PSYCHOLOGICAL   Primary: Low Self-Efficacy.  \"I\'m probably just not
  GRAPH           \"I\'m probably just not     smart enough for
                  smart enough for             programming\" --- Efficacy
                  programming\" =              language extracted.
                  fixed-ability global         
                  attribution. Secondary:      
                  Fixed Attribution. SRL:      
                  none. Imposter flag: FALSE   
                  (this is genuine low         
                  efficacy, not imposter       
                  distortion).                 
  -------------------------------------------------------------------------

  -----------------------------------------------------------------------
  **INTERVENTION:** *worked_example → Normalize difficulty (\"most
  learners find this confusing initially\" --- light attribution
  reframe). Present expert-narrated loop trace. Do NOT request another
  attempt yet --- another failure would deepen Fixed Attribution.*

  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
  **NEXT SCAFFOLD:** *\"Let\'s look at one loop together before you try
  again. I\'ll trace through it step by step and narrate what\'s
  happening at each line. Your only job right now is to follow along ---
  you don\'t need to write anything yet.\"*

  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
  **EXAMPLE 2 --- Developing Learner Inside ZPD: Monitoring Active**

  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
  **STUDENT PROMPT:** *\"I tried writing a for loop to sum a list but I
  keep getting the wrong answer. I think the issue is that I\'m starting
  my counter at 1 instead of 0, so it skips the first element. I changed
  it but now I\'m getting an index error. for i in range(1, len(nums)):
  total += nums\[i\]\"*

  -----------------------------------------------------------------------

  -------------------------------------------------------------------------
  **Graph**       **Classification**           **Evidence**
  --------------- ---------------------------- ----------------------------
  COGNITIVE GRAPH loops: partial encoding.     \"starting at 1 instead of
                  Student correctly identifies 0, so it skips the first
                  off-by-one error class and   element\" --- causal
                  reasons causally (\"starting reasoning present. Partial
                  at 1 → skips first           (not solid): new error after
                  element\"). After fix,       fix reveals gap in range()
                  encounters new error ---     mechanics.
                  range() behavior not fully   
                  encoded. Dual coding:        
                  verbal_only --- linguistic   
                  reasoning without            
                  structural/index diagram     
                  thinking.                    

  PROGRESSION     Stage 3 --- Coached Problem  \"I tried\... I think the
  GRAPH           Solving. Prior attempt       issue is\... I changed
                  present (wrote code,         it\...\" --- attempt +
                  observed failure, formed     hypothesis + test cycle =
                  hypothesis, tested fix,      Stage 3 signal.
                  encountered new error).      
                  Question is targeted at      
                  specific failure point, not  
                  global. ZPD: inside_zpd ---  
                  schema present, gap          
                  localized.                   

  PSYCHOLOGICAL   Primary: Monitoring (SRL     \"I tried writing a for loop
  GRAPH           Phase 2). \"I tried X        to sum a list\" --- Efficacy
                  because I thought Y but      language: effort + strategy
                  now\...\" = canonical Phase  attribution throughout.
                  2. Secondary: Growth         
                  Self-Efficacy --- did not    
                  give up after first error,   
                  continued iterating. No      
                  fixed attribution. Imposter: 
                  FALSE.                       
  -------------------------------------------------------------------------

  -----------------------------------------------------------------------
  **INTERVENTION:** *socratic_prompt --- student is inside ZPD,
  monitoring phase active, schema present. Providing the answer directly
  would short-circuit the monitoring process currently operating well.*

  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
  **NEXT SCAFFOLD:** *\"You\'ve correctly identified that range(1,
  len(nums)) skips index 0. Now look at what range(0, len(nums)) gives
  you for a list of 5 elements --- what are the index values it
  generates, and which of those is out of bounds?\"*

  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
  **EXAMPLE 3 --- Imposter Contradiction: Stage 4 Performance, Imposter
  Distortion**

  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
  **STUDENT PROMPT:** *\"Before I start, I want to make sure I understand
  the problem: I need to filter a list to keep only even numbers, right?
  My plan is to use a for loop with an if condition checking num % 2 ==
  0. I wrote it and it works, but I\'m wondering if there\'s a more
  Pythonic way. I saw list comprehensions mentioned but I\'m probably not
  good enough to use those yet.\"*

  -----------------------------------------------------------------------

  -------------------------------------------------------------------------
  **Graph**       **Classification**           **Evidence**
  --------------- ---------------------------- ----------------------------
  COGNITIVE GRAPH loops: solid. control:       \"My plan is to use a for
                  solid. Student plans before  loop with an if condition
                  coding, implements           checking num % 2 == 0\" ---
                  correctly, and describes     planning + dual-channel
                  both the conceptual goal and description = solid
                  structural mechanism. Dual   encoding.
                  coding: dual --- verbal      
                  (\"filter to keep only even  
                  numbers\") + structural      
                  (\"for loop with if          
                  condition checking num % 2   
                  == 0\").                     

  PROGRESSION     Stage 4a --- Independent     \"Before I start\... my plan
  GRAPH           Solution. Explicit planning  is\... I wrote it and it
                  before coding, working       works\... wondering if
                  solution achieved            there\'s a more Pythonic
                  independently, asks for      way\" --- solution-first
                  improvement not completion.  behavior = Stage 4a.
                  ZPD: at_boundary --- solid   
                  performance, ready for list  
                  comprehensions.              

  PSYCHOLOGICAL   Primary: Forethought (SRL    \"I\'m probably not good
  GRAPH           Phase 1). \"Before I         enough to use those yet\"
                  start\... my plan is\...\" = --- Efficacy language.
                  clearest possible Phase 1.   Contradiction with Stage 4
                  IMPOSTER FLAG = TRUE. \"I\'m Cognitive + Progression =
                  probably not good enough to  imposter detection.
                  use those yet\" =            
                  confidence-performance       
                  mismatch. Stage 4 behavior + 
                  inability self-assessment =  
                  imposter pattern.            
  -------------------------------------------------------------------------

  -----------------------------------------------------------------------
  **CROSS-GRAPH CONTRADICTION:** *Cognitive + Progression both show Stage
  4+ readiness. Psychological shows Imposter distortion at
  Self-Reflection. Resolution: Psychological overrides ---
  mastery_surface BEFORE validate_and_advance. Jumping to list
  comprehensions without attribution reframe would reinforce the fraud
  narrative.*

  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
  **NEXT SCAFFOLD:** *\"Before we look at list comprehensions --- notice
  what you just did: you described the problem accurately, planned the
  solution before writing it, wrote code that works correctly, and then
  asked how to improve it. That is exactly what experienced Python
  developers do. List comprehensions are the next natural step, and you
  already understand the logic they\'re built on. Let\'s look at one.\"*

  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
  **EXAMPLE 4 --- Expert Autonomy: Flow State, Deep Encoding, Transfer**

  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
  **STUDENT PROMPT:** *\"I implemented binary search and it works on
  sorted lists. It breaks when there are duplicates and I need to return
  all matching indices. I think the issue is fundamental to binary search
  --- it assumes uniqueness. Would modifying the mid-point logic help or
  do I need a partition-based approach? I\'m also wondering if this
  connects to how databases handle index lookups.\"*

  -----------------------------------------------------------------------

  -------------------------------------------------------------------------
  **Graph**       **Classification**           **Evidence**
  --------------- ---------------------------- ----------------------------
  COGNITIVE GRAPH algorithms: deep. recursion: \"I think the issue is
                  solid. datastructs: deep.    fundamental to binary search
                  Student identifies           --- it assumes uniqueness\"
                  fundamental algorithmic      --- cross-concept
                  assumption (uniqueness),     architectural reasoning.
                  evaluates two architectural  Unprompted database
                  strategies, and draws an     connection = deep transfer
                  unprompted cross-domain      encoding.
                  connection to databases.     
                  Cross-concept bridging +     
                  design-level reasoning =     
                  deep encoding. Dual coding:  
                  dual.                        

  PROGRESSION     Stage 5 --- Expert Autonomy. \"Would modifying the
  GRAPH           Working implementation       mid-point logic help or do I
                  present. Question is         need a partition-based
                  architectural evaluation,    approach?\" ---
                  not task completion. Student design/architecture question
                  formulated the problem       with no single correct
                  independently, identified    answer = Stage 5 signal.
                  non-obvious edge case,       
                  proposed two solution        
                  candidates, made real-world  
                  connection. ZPD:             
                  internalized --- new ZPD     
                  boundary at partition        
                  algorithms and database      
                  indexing.                    

  PSYCHOLOGICAL   Primary: Flow State. Natural \"I think the issue is
  GRAPH           depth and momentum ---       fundamental to binary search
                  thinking at boundary of      --- it assumes uniqueness\"
                  knowledge, not seeking       --- Efficacy language:
                  rescue. Secondary: Growth    confident analytical
                  Self-Efficacy ---            framing, zero apologizing.
                  cross-domain connection      
                  reflects expansion           
                  orientation. SRL:            
                  performance (mid-problem,    
                  monitoring two competing     
                  hypotheses). Imposter:       
                  FALSE.                       
  -------------------------------------------------------------------------

  -----------------------------------------------------------------------
  **INTERVENTION:** *transfer_task --- student does not need binary
  search scaffolding. Needs a problem requiring same divide-and-conquer
  logic in a genuinely new context. The database connection they raised
  is the natural transfer candidate.*

  -----------------------------------------------------------------------

  -----------------------------------------------------------------------
  **NEXT SCAFFOLD:** *\"Your instinct about partition-based search is
  correct --- that\'s exactly how database B-tree index lookups handle
  duplicate keys. Before I explain the full mechanism: given what you
  know about binary search\'s divide-and-conquer logic, how would you
  design a range query --- find all records where the key is between 100
  and 200 --- in a sorted structure?\"*

  -----------------------------------------------------------------------

**5. Master Dataset Reference**

The following table consolidates all recommended datasets across all 12
theories, organized by primary graph and theory. This serves as the
implementation team\'s reference for data acquisition and model
training.

  ----------------------------------------------------------------------------------
  **Dataset**           **Primary Graph** **Theories        **Key Signals Provided**
                                          Served**          
  --------------------- ----------------- ----------------- ------------------------
  EduNet (MOOC          Cognitive         Information       Sequential prompt
  interaction logs)                       Processing        patterns, session dwell
                                                            time, working memory
                                                            overload indicators

  ASSISTments Dataset   All Graphs        IPT,              Hint usage, error
                                          Constructivism,   repetition,
                                          ZPD, SRL,         self-correction, ZPD
                                          Attribution       scaffolding sequences,
                                                            attribution probes

  Open University LA    Cognitive +       IPT, Elaboration, Weekly activity logs,
  Dataset (OULAD)       Progression       ZPD               assessment sequences,
                                                            module progression data

  Khan Academy          All Graphs        IPT, ZPD, Flow,   Step-by-step attempts,
  Interaction Logs                        SRL               time stamps, voluntary
                                                            continuation, mastery
                                                            state transitions

  CodeWorkout Dataset   Cognitive +       IPT, Elaboration, Ordered coding attempts
                        Progression       ZPD               across Tier 1--3
                                                            difficulty with time
                                                            stamps

  CSEDM Dataset         Cognitive         Dual Coding,      Code + explanation
                                          Cognitive         pairs, verbal/visual
                                          Apprenticeship    reasoning annotations

  CodeHelp Interaction  Cognitive +       Dual Coding,      Student explanations
  Logs                  Progression       Constructivism,   alongside code, revision
                                          Cognitive         history showing
                                          Apprenticeship    construction

  GitHub Copilot Study  Cognitive         Dual Coding       Verbal descriptions of
  Dataset                                                   code behavior vs. actual
                                                            implementation pairs

  Cognitive Tutor       Cognitive +       Elaboration,      Prerequisite-ordered
  Dataset               Progression       Constructivism,   sequences, faded hint
                                          ZPD               data, ZPD scaffold
                                                            comparison

  Stack Overflow        Progression       Situated          Expert-to-novice
  Archive                                 Learning,         transfer patterns,
                                          Cognitive         community-of-practice
                                          Apprenticeship    participation
                                                            trajectories

  GitHub Contribution   Progression +     Situated          Identity development
  Logs                  Psychological     Learning,         through project
                                          Cognitive         contribution,
                                          Apprenticeship    coaching/reflection
                                                            exchanges

  Kaggle Competition    Progression       Situated          Authentic
  Data                                    Learning, Flow    context-embedded
                                                            challenges with
                                                            community feedback, long
                                                            session indicators

  MSLQ Validation       Psychological     SCT, SRL,         Self-efficacy + SRL +
  Dataset                                 Attribution       academic performance
                                                            gold standard dataset

  edX HarvardX/MITx     Psychological +   SCT, Flow, SRL    Dropout patterns,
  Dataset               Progression                         confidence self-reports,
                                                            engagement trajectories,
                                                            discussion posts

  ASQ Validation        Psychological     Attribution       Attribution style ×
  Dataset                                 Theory            depression/achievement
                                                            outcome correlations
                                                            (Seligman et al.)

  CIPS Validation       Psychological     Imposter Syndrome Clance Impostor
  Dataset                                                   Phenomenon Scale ×
                                                            achievement data

  Coding Bootcamp       Psychological     Imposter          Imposter feelings,
  Longitudinal Data                       Syndrome, SCT,    self-efficacy,
                                          Attribution       performance trajectories
                                                            over 12-week intensive
                                                            programs

  EEG + ESM Flow        Psychological     Flow Theory       Physiological +
  Studies                                                   momentary self-report
                                                            gold standard for flow
                                                            state validation

  FreeCodeCamp Project  Progression       Situated Learning Real-world output
  Logs                                                      framing, project
                                                            completion, community
                                                            engagement

  PISA 2018 Learning    Psychological     SRL, Attribution  Cross-national
  Module                                                    self-regulation +
                                                            attribution + academic
                                                            performance data
  ----------------------------------------------------------------------------------

**6. Master ML Architecture Reference**

The following table consolidates all recommended deep learning and ML
architectures across all 12 theories, organized by architecture family
and the theories they serve.

  ------------------------------------------------------------------------------------------
  **Architecture**         **Family**      **Theories        **Role in System**
                                           Served**          
  ------------------------ --------------- ----------------- -------------------------------
  Deep Knowledge Tracing   LSTM / Sequence ZPD, IPT,         Predicts probability of correct
  (DKT)                                    Constructivism    response on next item; backbone
                                                             for ZPD boundary estimation and
                                                             knowledge state tracking

  BERT / RoBERTa           Transformer NLP Attribution, SRL, Classification of attribution
  Fine-tuned                               SCT, Imposter,    sentences, SRL phases, efficacy
                                           Cognitive         language, apprenticeship phase
                                           Apprenticeship    from natural language

  CodeBERT + RoBERTa       Multi-modal     Dual Coding       Joint encoding of code
  Multi-modal              Transformer                       (structural) + explanation
                                                             (verbal) for dual coding
                                                             profile classification

  Knowledge Graph          Graph Embedding Elaboration, Dual Represent concept nodes and
  Embeddings (TransE,                      Coding            prerequisite edges; detect
  RotatE)                                                    elaboration strength from
                                                             cross-concept signals

  Graph Neural Networks    Graph Neural    Dual Coding,      Propagate encoding signals
  (GCN, GNN)               Network         Situated Learning across concept graph; model
                                                             community-of-practice structure

  Hidden Markov Models     Probabilistic   IPT, Cognitive    Model latent
  (HMMs)                   Sequence        Apprenticeship    cognitive/apprenticeship states
                                                             from observable action
                                                             sequences

  Bayesian Knowledge       Bayesian /      IPT,              Probabilistic estimation of
  Tracing (BKT)            Probabilistic   Constructivism    knowledge state transitions;
                                                             complement to DKT

  Multi-Armed / Contextual Reinforcement   ZPD, Flow         Dynamically select optimal
  Bandit                   Learning                          scaffold level / challenge
                                                             level to keep students in ZPD /
                                                             flow channel in real time

  Reinforcement Learning   RL              Cognitive         Optimize sequence of
  (Policy Optimization)                    Apprenticeship,   modeling/coaching/scaffolding
                                           Flow              actions to accelerate phase
                                                             progression; optimize challenge
                                                             calibration for flow

  Sentiment Analysis +     NLP Pipeline    Attribution, SCT  Combine sentiment (negative
  Causal Pipeline                                            affect) with causal attribution
                                                             detection for joint
                                                             psychological node assignment

  Confidence-Performance   Regression      Imposter          Predict imposter flag from gap
  Regression                               Syndrome,         between self-reported
                                           Attribution       confidence and objective
                                                             accuracy

  Anomaly Detection        Unsupervised DL Flow, Imposter    Detect departures from baseline
  (Autoencoder)                            Syndrome          engagement (flow disruption) or
                                                             mismatches between performance
                                                             and efficacy trajectories

  Hierarchical Attention   Deep NLP        Elaboration       Model hierarchical concept tier
  Networks (HAN)                                             structure; detect cross-tier
                                                             elaboration signals in student
                                                             text

  Ordinal Regression       Supervised ML   Cognitive         Predict ordered stage/phase
                                           Apprenticeship,   variables (Observation \<
                                           ZPD               Coaching \< Exploration;
                                                             overwhelmed \< inside_zpd \<
                                                             internalized)

  Structural Equation      Statistical ML  SRL, SCT          Validate causal pathways from
  Modeling (SEM)                                             SRL phase quality and
                                                             self-efficacy to encoding
                                                             strength and progression stage

  Sequential Pattern       Pattern Mining  SRL,              Extract frequent behavioral
  Mining (GSP)                             Constructivism    patterns indicating each SRL
                                                             phase and constructivism
                                                             indicators from log data

  Survival Analysis        Statistical ML  SCT               Predict time-to-dropout as
                                                             function of self-efficacy
                                                             trajectory; early warning
                                                             system for at-risk students

  Causal Inference (DoWhy, Causal ML       ZPD, SCT          Estimate causal effect of
  CausalML)                                                  scaffold removal on performance
                                                             (ZPD internalization); mastery
                                                             experiences on efficacy (SCT)

  Multi-task Learning      Deep Learning   Imposter, SCT,    Share representations across
  (shared encoder)                         Attribution       imposter detection, attribution
                                                             classification, and efficacy
                                                             estimation for accurate joint
                                                             inference

  NLI Models (RoBERTa      Transformer NLP Constructivism,   Classify whether a student
  fine-tuned)                              Attribution       statement represents hypothesis
                                                             generation, self-correction, or
                                                             passive reception; causal
                                                             attribution detection
  ------------------------------------------------------------------------------------------

**7. Implementation Principles & Design Decisions**

**7.1 Single Input, Three Parallel Outputs**

The most important architectural principle: the system does not route
prompts to specific theories or graphs based on keyword matching. Every
prompt goes through all three channels simultaneously. This prevents
fragmented assessments where the cognitive picture contradicts the
psychological picture because they were built from different input
subsets.

**7.2 State Persistence vs. State Decay**

Psychological states (Graph 3) are more volatile than cognitive states
(Graph 1) or progression states (Graph 2). A student\'s self-efficacy
can shift within a single session based on a success or failure
experience. Concept encoding is more stable. The system should weight
recent psychological signals more heavily than older ones, while
weighting cognitive signals across a longer time window.

**7.3 Per-Concept Graph Positions**

A student is not at a single position in the Progression Graph --- they
may be at Stage 4 for loops but Stage 2 for recursion. The system
maintains per-concept positions in both Cognitive and Progression
Graphs, while maintaining a single aggregate position in the
Psychological Graph (since self-efficacy and attribution style are more
global traits, though they can fluctuate concept-by-concept in the short
term).

**7.4 The Reflection Node as the Critical Intervention Point**

Across all five theories in the Psychological Graph, the Self-Reflection
/ Evaluation node (SRL Phase 3) is the highest-leverage intervention
point. It is where attribution style is either reinforced or corrected,
where imposter distortion perpetuates or is interrupted, and where the
SRL cycle either feeds forward productively or collapses. Adaptive
systems that invest most heavily in structuring the reflection phase ---
through guided post-task prompts, explicit attribution framing, and
mastery-evidence surfacing --- produce the most durable motivational and
self-regulatory gains.

**7.5 Avoiding Pathologization**

The attribution reframing, imposter syndrome interventions, and
anxiety-reduction responses described here must be implemented without
labeling or pathologizing the learner. Adaptive responses should feel
like natural instructional support --- not clinical interventions. The
system must never expose its internal psychological state assessment to
the student.

**7.6 Output Schema**

The engine produces a structured JSON classification report for every
student prompt:

+-----------------------------------------------------------------------+
| { \"cognitive\": { \"primary_concept\": \"node_id\",                  |
|                                                                       |
| \"nodes\": \[{ \"node_id\": \"loops\", \"encoding_strength\":         |
| \"partial\",                                                          |
|                                                                       |
| \"dual_coding\": \"verbal_only\", \"evidence\": \"exact phrase from   |
| prompt\" }\] },                                                       |
|                                                                       |
| \"progression\": { \"node\": \"coached\", \"zpd_boundary\":           |
| \"inside_zpd\", \"confidence\": \"high\", \"evidence\": \"\...\" },   |
|                                                                       |
| \"psychological\": { \"primary_node\": \"monitoring\",                |
| \"secondary_node\": \"growth_efficacy\",                              |
|                                                                       |
| \"srl_phase\": \"performance\", \"imposter_flag\": false,             |
| \"efficacy_language\": \"\...\" },                                    |
|                                                                       |
| \"adaptive\": { \"primary_intervention\": \"socratic_prompt\",        |
|                                                                       |
| \"intervention_rationale\": \"\...\", \"next_scaffold\": \"exact      |
| question for student\" } }                                            |
+-----------------------------------------------------------------------+

**8. Summary**

  -----------------------------------------------------------------------
  **CORE ARCHITECTURE SUMMARY:** *Cognitive Graph tracks what is encoded
  and how deeply. Progression Graph tracks where the student is on the
  journey to independence. Psychological Graph tracks whether the
  student\'s beliefs will sustain or undermine that journey. All three
  must be understood together. One prompt → three simultaneous updates →
  one unified, actionable learner state.*

  -----------------------------------------------------------------------

This document provides the complete reference for implementing,
validating, and extending the AI-driven personalized learning system.
Every classification decision is traceable to a specific phrase or
behavior in the student\'s prompt. Every theory is operationalized
through concrete datasets and validated ML architectures. Every
intervention is grounded in the intersection of all three graph states.

The 12 theories are not a checklist --- they are a multidimensional lens
that, when applied through the 3-graph framework, produces a complete
picture of what the student knows, where they are in their development,
and what they believe about themselves. The unified prompt analysis
framework transforms every student message from a simple request into a
rich, multi-dimensional signal that updates all three graphs
simultaneously, enabling the adaptive system to respond not just to what
the student asks, but to who the student is at that moment ---
cognitively, developmentally, and psychologically.

*--- End of Document ---*
