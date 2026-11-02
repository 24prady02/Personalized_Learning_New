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

LABEL_MIS = """You compare a student's words with the wrong rules and right rules of one Java concept. The edges below are judged together: the same words can fit several wrong rules, and you choose, for each edge, whether the student's own reasoning follows it.

Program:
{code}

Question: {question}

Student's answer, split into numbered clauses:
{clauses}

Concept: {concept}
Edges (each with its wrong rule and the right rule):
{edges}

For each edge decide:
- held: the answer follows the wrong rule in what sets it apart from the right rule. Where the answer gives a reason, the reason must be this wrong rule's own; a result this rule would also predict, reached by a different reason, does not hold it. When several wrong rules could fit the same words, held goes to the one(s) whose claim the student actually makes; a student can hold more than one;
- correct: the answer follows the right rule where the two differ, by stating it or by doing it (code or a value in the answer that does what the right rule says and the wrong rule would get wrong counts);
- not applied: the answer neither follows nor contradicts this rule, or the rule is about something that appears neither in the program nor in the answer.

Reply with exactly one line per edge, in this format and nothing else:
edge_id | held or correct or not applied | clauses: the numbers of the clauses that show it, e.g. 2, 4 (write none if not applied) | confidence: a number from 0 to 1

Example. Student's answer, split into numbered clauses:
c1: {ex_answer}
Concept: definite_assignment
Edges:
- mis:definite_assignment->LocalVariablesAutoInitialized | wrong rule: A local variable that is declared but not assigned holds 0 (or false, or null). | right rule: Java refuses to compile a read of a local variable that may not have been assigned.
- mis:definite_assignment->DeclarationAssignsNull | wrong rule: A declared int holds null until assigned. | right rule: An int can never hold null; an unassigned local has no value the program may read.
Reply:
mis:definite_assignment->LocalVariablesAutoInitialized | held | clauses: 1 | confidence: 0.95
mis:definite_assignment->DeclarationAssignsNull | not applied | clauses: none | confidence: 0.9
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
Clauses: the numbers of the clauses that show it, e.g. 2, 4 (write none if not applied)
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
Clauses: the numbers of the clauses that show it, e.g. 2, 4 (write none if not shown)
Confidence: a number from 0 to 1
"""


def few_shot_fields() -> dict[str, str]:
    return {"ex_code": FEW_SHOT["code"], "ex_question": FEW_SHOT["question"], "ex_answer": FEW_SHOT["answer"]}
