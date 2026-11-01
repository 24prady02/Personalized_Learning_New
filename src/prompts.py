"""The prompts of the ToG traversal: one edge prune prompt and three edge label prompts (misconception edge, concept
edge, level way). These are the only places the model is asked.

Every prompt is a plain string with {placeholders}; traverse.py fills them. The few-shot example is the
reference case S000 (code, question, answer) with a worked reply in the exact output format each prompt expects.
"""
from __future__ import annotations

FEW_SHOT = {
    "code": "int count;\nSystem.out.println(count);",
    "question": "What does the system print?",
    "answer": "It will print 0.",
}

# ---------------------------------------------------------------- 1. edge prune (ToG relation prune)

PRUNE = """You read a student's answer to a question about a short Java program and decide which rules the answer engages with.

Program:
{code}

Question: {question}

Student's answer: "{answer}"

Concept under consideration: {concept}

Candidate edges of this concept. A misconception/error edge shows the wrong rule (logic) and the right rule (twin_logic); a concept edge shows the rule that links the two concepts; a level way (lvl:) shows one way an answer can display a level of understanding of the concept.
{edges}

Task: pick the {n} edges whose rule the student's answer engages with, either by following the wrong rule, by following the right rule, by breaking / confirming the link, or by doing what a level way describes. Rate each with a score in (0, 1]; the scores of the picked edges must sum to 1. Ignore edges the answer says nothing about.

Reply with one line per picked edge, in this exact format and nothing else:
{{edge_id (Score: 0.6)}}
{{edge_id (Score: 0.4)}}

Example. Program:
{ex_code}
Question: {ex_question}
Student's answer: "{ex_answer}"
Concept under consideration: definite_assignment
Candidate edges:
- mis:definite_assignment->LocalVariablesAutoInitialized | wrong rule: A local variable that is declared but not assigned holds 0 (or false, or null). | right rule: Java refuses to compile a read of a local variable that may not have been assigned.
- err:declaration->DeclarationWithoutType | wrong rule: Declares a variable without a type. | right rule: Every declaration names a type.
Reply:
{{mis:definite_assignment->LocalVariablesAutoInitialized (Score: 1.0)}}
"""

# ---------------------------------------------------------------- 2. edge label

LABEL_MIS = """You compare a student's words with a wrong rule and the right rule about one Java concept.

Program:
{code}

Question: {question}

Student's answer, split into clauses:
{clauses}

Edge: {edge_id}
Wrong rule (logic): {logic}
Right rule (twin_logic): {twin_logic}

Decide:
- held: the answer follows the wrong rule;
- correct: the answer follows the right rule where the two differ;
- not applied: the answer does not touch this rule.

Reply in exactly three lines and nothing else:
Label: held | correct | not applied
Quote: the exact words from the student's answer that show it (copy them verbatim; write none if not applied)
Confidence: a number from 0 to 1

Example. Student's answer: "{ex_answer}"
Edge: mis:definite_assignment->LocalVariablesAutoInitialized
Wrong rule: A local variable that is declared but not assigned holds 0 (or false, or null).
Right rule: Java refuses to compile a read of a local variable that may not have been assigned.
Reply:
Label: held
Quote: It will print 0.
Confidence: 0.95
"""

LABEL_CONCEPT = """You check whether a student's answer confirms or breaks the rule that links two Java concepts.

Program:
{code}

Question: {question}

Student's answer, split into clauses:
{clauses}

Edge: {edge_id}  ({source} -> {target}, {etype})
Rule (logic): {logic}

Decide:
- confirmed: the answer applies this rule correctly;
- broken: the answer contradicts this rule or fails to carry it over;
- not applied: the answer does not touch this rule.

Reply in exactly three lines and nothing else:
Label: confirmed | broken | not applied
Quote: the exact words from the student's answer that show it (copy them verbatim; write none if not applied)
Confidence: a number from 0 to 1
"""

LABEL_WAY = """You check whether a student's answer shows one way of understanding a Java concept.

Program:
{code}

Question: {question}

Student's answer, split into clauses:
{clauses}

Concept: {concept}
Way: {way}
What an answer that shows this way does: {rule}

Decide:
- shown: the answer does what this way describes, in its own words or in code (states that rule, traces it, predicts it, relates it, applies it);
- not shown: the answer does not do this.

Reply in exactly three lines and nothing else:
Label: shown | not shown
Quote: the exact words from the student's answer that show it (copy them verbatim; write none if not shown)
Confidence: a number from 0 to 1
"""


def few_shot_fields() -> dict[str, str]:
    return {"ex_code": FEW_SHOT["code"], "ex_question": FEW_SHOT["question"], "ex_answer": FEW_SHOT["answer"]}
