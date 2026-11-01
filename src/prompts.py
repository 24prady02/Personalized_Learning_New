"""The three prompts of the ToG traversal (edge prune, edge label, level ladder): the only places the model is asked.

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

Candidate edges of this concept. A misconception/error edge shows the wrong rule (logic) and the right rule (twin_logic); a concept edge shows the rule that links the two concepts.
{edges}

Task: pick the {n} edges whose rule the student's answer engages with, either by following the wrong rule, by following the right rule, or by breaking / confirming the link. Rate each with a score in (0, 1]; the scores of the picked edges must sum to 1. Ignore edges the answer says nothing about.

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

# ---------------------------------------------------------------- 3. level ladder

LEVEL_LADDER = """You place a student's answer on a learning-progression ladder for one Java concept, going from L0 up to L4 and stopping at the first level whose deciding question is answered in favour of that level.

Program:
{code}

Question: {question}

Student's answer, split into clauses:
{clauses}

Concept: {concept}

Levels, in order. Each level has a deciding question and the ways an answer can show that level. Choose at most one way per level.
{levels}

Go through L0, L1, L2, L3, L4 in that order. At each level ask its deciding question. If the answer belongs to that level, stop and report that level and the way that fits; otherwise go up. If no level fits, report none.

Reply in exactly three lines and nothing else:
Level: L0 | L1 | L2 | L3 | L4 | none
Way: the name of the way, or none
Quote: the exact words from the student's answer that show it (verbatim), or none
"""


def few_shot_fields() -> dict[str, str]:
    return {"ex_code": FEW_SHOT["code"], "ex_question": FEW_SHOT["question"], "ex_answer": FEW_SHOT["answer"]}
