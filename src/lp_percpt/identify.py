"""
identify.py — Stage A: which Chapter-1 concepts is a student prompt about?

Every prompt is scored against all 173 concepts of the Chapter-1 graph:

    score = W_CODE * code-cue hits in the student's text (max 2 counted)
          + W_CODE_SHOWN * code-cue hit only in the question's code (max 1 counted)
          + W_ASKED * a cue in the question part asked or the code lines it names
          + W_WORD * word-cue points (max 3 cues; a multi-word phrase counts 2)
          + W_SEM  * max(0, meaning_sim - SEM_FLOOR)
          + W_MIS  * max(0, misconception_sim - MIS_FLOOR)      (thresholds.py)

  meaning_sim        best cosine between a clause and the concept's
                     "label: description" or one of its execution facts
  misconception_sim  best cosine between a clause and the wrong_belief of a
                     misconception linked to the concept

A concept is kept when score >= KEEP_SCORE and score >= RELATIVE_KEEP * best
score; at most MAX_CONCEPTS are returned, best first.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .knowledge import Concept, PercptKnowledge
from . import models
from .thresholds import (KEEP_SCORE, MAX_CONCEPTS, MAX_CONCEPTS_PICK, MAX_CONCEPTS_V2, MIS_FLOOR, RELATIVE_KEEP,
                         SEM_FLOOR, W_ASKED, W_CODE, W_CODE_SHOWN, W_MIS, W_SEM, W_WORD)

_SPLIT_RE = re.compile(r"(?<=[.!?;])\s+|\n+|\s+(?:but|however|whereas|although)\s+", re.I)


def split_clauses(text: str) -> List[str]:
    parts = [p.strip(" ,") for p in _SPLIT_RE.split(text or "") if p and p.strip(" ,")]
    return [p for p in parts if len(p) > 1]


def _word_hit(phrase: str, text: str) -> bool:
    if re.fullmatch(r"[\w .'-]+", phrase):
        return re.search(r"(?<!\w)" + re.escape(phrase) + r"(?:s|es)?(?!\w)", text) is not None
    return phrase in text


@dataclass
class ConceptHit:
    concept: str
    score: float
    confidence: float
    @property
    def cue_linked(self) -> bool:
        """True when a code or word cue fired (not meaning / misconception only)."""
        return bool(self.code_cues or self.word_cues)

    code_cues: List[str] = field(default_factory=list)
    word_cues: List[str] = field(default_factory=list)
    meaning_sim: float = 0.0
    meaning_match: str = ""
    misconception_sim: float = 0.0
    misconception_match: Optional[str] = None


def _cue_hits(c: Concept, text_lower: str, text: str, code: str):
    in_text = [p.pattern for p in c.code_cues if p.search(text)]
    in_code = [p.pattern for p in c.code_cues if code and p.pattern not in in_text and p.search(code)]
    words = [w for w in c.word_cues if _word_hit(w, text_lower)]
    return in_text, in_code, words


def _focus(asked: str, code: str) -> str:
    """The part asked plus the code lines it names (by a variable or call): what
    the answer is about. "What is months used for?" -> String[] months = {...};"""
    names = {w for w in re.findall(r"\b[A-Za-z_]\w*\b", asked or "") if len(w) > 2}
    lines = [l for l in (code or "").split("\n") if names & set(re.findall(r"\b[A-Za-z_]\w*\b", l))]
    return (asked or "") + "\n" + "\n".join(lines)


def identify(text: str, kg: PercptKnowledge, code: str = "",
             clauses: Optional[List[str]] = None, asked: str = "") -> List[ConceptHit]:
    """asked: the question part the prompt answers; a concept it (or the code it
    names) cues gets W_ASKED, so the answer is linked to what was asked."""
    text_lower = (text or "").lower()
    focus = _focus(asked, code) if asked else ""
    focus_lower = focus.lower()
    clauses = clauses if clauses is not None else split_clauses(text)

    concepts = list(kg.concepts.values())
    meaning_targets: List[str] = []
    meaning_owner: List[str] = []
    for c in concepts:
        for s in [f"{c.label.replace('_', ' ')}: {c.description}"] + c.facts:
            meaning_targets.append(s)
            meaning_owner.append(c.id)
    mis_ids = list(kg.misconceptions)
    mis_texts = [kg.misconceptions[m].wrong_belief for m in mis_ids]

    sem = models.similarity(clauses, meaning_targets) if clauses else None
    mis = models.similarity(clauses, mis_texts) if clauses else None

    best_sem: Dict[str, tuple] = {}
    if sem is not None and sem.size:
        col_best = sem.max(axis=0)
        for j, owner in enumerate(meaning_owner):
            if col_best[j] > best_sem.get(owner, (0.0, ""))[0]:
                best_sem[owner] = (float(col_best[j]), meaning_targets[j])
    best_mis: Dict[str, tuple] = {}
    if mis is not None and mis.size:
        col_best = mis.max(axis=0)
        for j, mid in enumerate(mis_ids):
            for cid in kg.misconceptions[mid].concepts:
                if col_best[j] > best_mis.get(cid, (0.0, None))[0]:
                    best_mis[cid] = (float(col_best[j]), mid)

    hits: List[ConceptHit] = []
    for c in concepts:
        code_h, shown_h, word_h = _cue_hits(c, text_lower, text or "", code)
        s_sim, s_txt = best_sem.get(c.id, (0.0, ""))
        m_sim, m_id = best_mis.get(c.id, (0.0, None))
        # a multi-word phrase cue ("loop variable") is more specific than a single word
        word_pts = sum(2 if " " in w.strip() else 1 for w in word_h[:3])
        asked_h = bool(focus) and (any(p.search(focus) for p in c.code_cues)
                                   or any(_word_hit(w, focus_lower) for w in c.word_cues))
        mode = link_meaning_mode()
        meaning = W_SEM * max(0.0, s_sim - SEM_FLOOR) + W_MIS * max(0.0, m_sim - MIS_FLOOR)
        if mode == "student":
            # only the student's own sentences: no points for cues found only in the question's code or text
            score = W_CODE * min(len(code_h), 2) + W_WORD * word_pts + meaning
        elif mode == "grounded":
            # student's sentences only, and a code cue counts only when the sentence also means the concept
            cue = W_CODE * min(len(code_h), 2) if s_sim > SEM_FLOOR or m_sim > MIS_FLOOR else 0.0
            score = cue + W_WORD * word_pts + meaning
        elif mode == "grounded_q":
            # original scoring, but the answer's code-symbol points count only when the sentence also means the concept
            cue = W_CODE * min(len(code_h), 2) if s_sim > SEM_FLOOR or m_sim > MIS_FLOOR else 0.0
            score = (cue + W_CODE_SHOWN * min(len(shown_h), 1) + W_WORD * word_pts + W_ASKED * asked_h + meaning)
        elif mode == "meaning":
            # meaning first (doubled weights), the student's own cues only break ties
            score = 2 * meaning + 0.25 * min(len(code_h), 2) + 0.1 * min(word_pts, 3)
        else:
            score = (W_CODE * min(len(code_h), 2) + W_CODE_SHOWN * min(len(shown_h), 1) + W_WORD * word_pts
                     + W_ASKED * asked_h
                     + W_SEM * max(0.0, s_sim - SEM_FLOOR)
                     + W_MIS * max(0.0, m_sim - MIS_FLOOR))
        if score <= 0:
            continue
        hits.append(ConceptHit(
            concept=c.id, score=round(score, 3), confidence=round(min(1.0, score / 3.0), 2),
            code_cues=code_h + shown_h, word_cues=word_h,
            meaning_sim=round(s_sim, 3), meaning_match=s_txt,
            misconception_sim=round(m_sim, 3),
            misconception_match=m_id if m_sim >= MIS_FLOOR else None))
    if link_pick():
        # a wide shortlist for the judge to choose from: every concept scoring >= KEEP_SCORE, best first
        # (ties broken by meaning), up to MAX_CONCEPTS_PICK; the judge keeps only the ones the answer is about
        hits.sort(key=lambda h: (-h.score, -max(h.meaning_sim, h.misconception_sim)))
        return [h for h in hits if h.score >= KEEP_SCORE][:MAX_CONCEPTS_PICK]
    if link_v2():
        # ties broken by meaning, not graph order; a concept needs some meaning (or misconception)
        # similarity to be kept, never code cues alone; up to MAX_CONCEPTS_V2 kept
        hits.sort(key=lambda h: (-h.score, -max(h.meaning_sim, h.misconception_sim)))
        hits = [h for h in hits if h.meaning_sim > SEM_FLOOR or h.misconception_sim > MIS_FLOOR]
        cap = MAX_CONCEPTS_V2
    else:
        hits.sort(key=lambda h: -h.score)
        cap = MAX_CONCEPTS
    if not hits or hits[0].score < KEEP_SCORE:
        return []
    top = hits[0].score
    return [h for h in hits if h.score >= KEEP_SCORE and h.score >= RELATIVE_KEEP * top][:cap]


def link_meaning_mode() -> str:
    """LP_LINK_MODE = student | grounded | meaning (default: the original scoring). The keep rule is unchanged:
    score >= KEEP_SCORE and >= RELATIVE_KEEP x best, at most MAX_CONCEPTS."""
    return os.environ.get("LP_LINK_MODE", "")


def link_pick() -> bool:
    """LP_LINK_PICK=1: send the judge a shortlist of up to MAX_CONCEPTS_PICK concepts; the engine stores only
    the ones the judge gives a level (the judge chooses what the answer is about)."""
    return os.environ.get("LP_LINK_PICK") == "1"


def link_v2() -> bool:
    """LP_LINK_V2=1: the wider keep rule (cap 5, meaning tie-break, no cue-only concepts);
    the engine then stores only the kept concepts the judge gives a level."""
    return os.environ.get("LP_LINK_V2") == "1"
