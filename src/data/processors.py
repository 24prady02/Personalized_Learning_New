"""
src/data/processors.py
======================
Dataset processors for all four training datasets.

Each processor:
  1. Reads the raw downloaded files
  2. Cleans and normalises them
  3. Returns a pandas DataFrame with a consistent schema

Common output columns (all processors):
  student_id    str   — anonymised student identifier
  problem_id    str   — problem or item identifier
  code          str   — Java/Python source code (empty string if not available)
  error_message str   — compiler/runtime error (empty string if none)
  actions       list  — sequence of action strings (empty list if not available)
  time_deltas   list  — seconds between actions (empty list if not available)
  is_correct    int   — 1 = correct / successful, 0 = incorrect
  concept       str   — skill/concept name (empty string if unknown)
  emotion_label int   — 0=frustrated 1=confused 2=engaged 3=neutral 4=confident
                        (-1 if not available — excluded from loss)

Additional columns per processor:
  CodeNet:    language, submission_type (correct/buggy)
  ProgSnap2:  session_id, final_code, event_count, time_stuck
  ASSISTments: attempt_count, skill_name, hint_count  (q_matrix returned separately)
  MOOCCubeX:  course_id, concept_sequence
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


# ── Shared helpers ─────────────────────────────────────────────────────────────

def _safe_read_csv(path: Path, **kwargs) -> pd.DataFrame:
    """Read CSV with multiple encoding fallbacks."""
    for enc in ['utf-8', 'latin-1', 'cp1252']:
        try:
            return pd.read_csv(path, encoding=enc, **kwargs)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Cannot decode {path}")


def _infer_emotion_from_actions(actions: List[str]) -> int:
    """
    Rule-based emotion label from action sequences.
    Mirrors BehavioralHMM._rule_based() logic.
    Returns int label.
    """
    if not actions:
        return 3  # neutral
    n = max(len(actions), 1)
    error_rate  = sum('error' in str(a).lower() for a in actions) / n
    submit_rate = sum('submit' in str(a).lower() for a in actions) / n
    run_rate    = sum('run' in str(a).lower() for a in actions) / n
    if submit_rate > 0.15:
        return 4  # confident
    if error_rate > 0.5:
        return 0  # frustrated
    if run_rate > 0.3 and error_rate > 0.2:
        return 1  # confused
    if run_rate > 0.2:
        return 2  # engaged
    return 3       # neutral


# Map Java error strings to concept names
_ERROR_TO_CONCEPT = {
    'NullPointerException':         'null_pointer',
    'ArrayIndexOutOfBoundsException': 'array_index',
    'cannot find symbol':           'variable_scope',
    'incompatible types':           'type_mismatch',
    'missing return':               'missing_return',
    'unreachable statement':        'unreachable_code',
    'non-static':                   'static_vs_instance',
    'no suitable constructor':      'no_default_constructor',
    'StackOverflowError':           'infinite_loop',
    'StringIndexOutOfBoundsException': 'string_immutability',
    'ClassCastException':           'type_mismatch',
}


def _concept_from_error(error: str) -> str:
    for pattern, concept in _ERROR_TO_CONCEPT.items():
        if pattern.lower() in error.lower():
            return concept
    return ''


# ── CodeNetProcessor ───────────────────────────────────────────────────────────

class CodeNetProcessor:
    """
    Processes IBM Project CodeNet Java submissions.

    Expected directory layout (after download_datasets.py):
        data/codenet/
            java/
                correct/   *.java   (accepted submissions)
                buggy/     *.java   (wrong answer / compile error)
            metadata.csv           (problem_id, submission_id, language, status)

    Falls back to any .java/.py files found under the path if metadata
    is missing — useful for small sample datasets.
    """

    def __init__(self, data_path: str, config: Dict):
        self.path   = Path(data_path)
        self.config = config
        self.max_code_len = config.get('hvsae', {}).get('max_code_len', 512)

    def process(self) -> pd.DataFrame:
        print(f"[CodeNet] Processing from {self.path}")
        if not self.path.exists():
            print(f"[CodeNet] Path not found: {self.path}")
            return pd.DataFrame()

        rows = []

        # Try metadata CSV first
        meta_path = self.path / 'metadata.csv'
        if meta_path.exists():
            rows = self._process_with_metadata(meta_path)
        else:
            rows = self._process_files_only()

        if not rows:
            print("[CodeNet] No samples found.")
            return pd.DataFrame()

        df = pd.DataFrame(rows)
        print(f"[CodeNet] Loaded {len(df)} samples "
              f"({df['is_correct'].sum()} correct, {(~df['is_correct'].astype(bool)).sum()} buggy)")
        return df

    def _process_with_metadata(self, meta_path: Path) -> List[Dict]:
        meta = _safe_read_csv(meta_path)
        rows = []
        for _, row in meta.iterrows():
            code_path = self.path / str(row.get('file_path', ''))
            code = code_path.read_text(errors='replace')[:self.max_code_len] if code_path.exists() else ''
            rows.append(self._make_row(
                student_id=str(row.get('submission_id', f'sub_{len(rows)}')),
                problem_id=str(row.get('problem_id', 'unknown')),
                code=code,
                error=str(row.get('error_message', '')),
                is_correct=int(str(row.get('status', '')).lower() in ('accepted', '1', 'correct')),
                language=str(row.get('language', 'java')),
            ))
        return rows

    def _process_files_only(self) -> List[Dict]:
        rows = []
        for lang_dir in ['java', 'python', 'cpp', '']:
            base = self.path / lang_dir if lang_dir else self.path
            for subdir, is_correct in [('correct', 1), ('buggy', 0),
                                        ('accepted', 1), ('wrong', 0), ('', 0)]:
                d = base / subdir if subdir else base
                if not d.is_dir():
                    continue
                for f in list(d.glob('*.java')) + list(d.glob('*.py')):
                    code = f.read_text(errors='replace')[:self.max_code_len]
                    rows.append(self._make_row(
                        student_id=f.stem,
                        problem_id=f.parent.name,
                        code=code,
                        error='',
                        is_correct=is_correct,
                        language='java' if f.suffix == '.java' else 'python',
                    ))
        return rows

    @staticmethod
    def _make_row(student_id, problem_id, code, error, is_correct, language) -> Dict:
        return {
            'student_id':    student_id,
            'problem_id':    problem_id,
            'code':          code,
            'error_message': error,
            'actions':       [],
            'time_deltas':   [],
            'is_correct':    is_correct,
            'concept':       _concept_from_error(error),
            'emotion_label': -1,
            'language':      language,
            'submission_type': 'correct' if is_correct else 'buggy',
        }


# ── ProgSnap2Processor ────────────────────────────────────────────────────────

class ProgSnap2Processor:
    """
    Processes ProgSnap2 CS1 debugging session data.

    Expected file (after download_datasets.py):
        data/progsnap2/MainTable.csv

    Columns used:
        SubjectID, ProblemID, EventType, ServerTimestamp,
        CodeStateSection (or CodeState), Score

    Aggregates events into per-session rows.
    Each session = one (SubjectID, ProblemID) pair.
    """

    EVENT_ACTION_MAP = {
        'Run.Program':     'run',
        'Compile.Error':   'compile_error',
        'Run.Error':       'run_error',
        'File.Edit':       'edit',
        'File.Open':       'open_file',
        'Webpage.Open':    'open_webpage',
        'Submit':          'submit',
        'HelpRequest':     'help_request',
        'Resource.View':   'resource_view',
        'Video.Play':      'video_play',
        'Video.Pause':     'video_pause',
    }

    def __init__(self, data_path: str, config: Dict):
        self.path     = Path(data_path)
        self.config   = config
        self.max_seq  = config.get('behavioral', {}).get('max_sequence_len', 50)

    def process(self) -> pd.DataFrame:
        print(f"[ProgSnap2] Processing from {self.path}")

        # Find the main CSV
        csv_path = None
        for name in ['MainTable.csv', 'MainTable_cs1.csv', 'main_table.csv']:
            p = self.path / name if self.path.is_dir() else self.path
            if p.exists():
                csv_path = p
                break
            if self.path.is_dir():
                matches = list(self.path.glob(f'**/{name}'))
                if matches:
                    csv_path = matches[0]
                    break

        if csv_path is None:
            print(f"[ProgSnap2] No CSV found under {self.path}")
            return pd.DataFrame()

        try:
            df = _safe_read_csv(csv_path, nrows=200_000)
            print(f"[ProgSnap2] Loaded {len(df)} events from {csv_path.name}")
        except Exception as e:
            print(f"[ProgSnap2] Error reading CSV: {e}")
            return pd.DataFrame()

        return self._aggregate_sessions(df)

    def _aggregate_sessions(self, df: pd.DataFrame) -> pd.DataFrame:
        # Normalise column names
        df.columns = [c.strip() for c in df.columns]
        subject_col  = next((c for c in df.columns if 'subject' in c.lower()), None)
        problem_col  = next((c for c in df.columns if 'problem' in c.lower()), None)
        event_col    = next((c for c in df.columns if 'event' in c.lower() and 'type' in c.lower()), None)
        time_col     = next((c for c in df.columns if 'timestamp' in c.lower()), None)
        code_col     = next((c for c in df.columns if 'code' in c.lower()), None)
        score_col    = next((c for c in df.columns if 'score' in c.lower() or 'correct' in c.lower()), None)

        if not subject_col or not problem_col:
            print("[ProgSnap2] Cannot find SubjectID/ProblemID columns.")
            return pd.DataFrame()

        rows = []
        for (sid, pid), group in df.groupby([subject_col, problem_col]):
            group = group.sort_values(time_col) if time_col else group

            # Action sequence
            actions = []
            if event_col:
                actions = [self.EVENT_ACTION_MAP.get(str(e), 'edit')
                           for e in group[event_col].tolist()][:self.max_seq]

            # Time deltas (seconds)
            time_deltas = []
            if time_col:
                times = pd.to_numeric(group[time_col], errors='coerce').fillna(0).tolist()
                time_deltas = [float(times[i] - times[i-1])
                               for i in range(1, len(times))][:self.max_seq]

            # Final code
            final_code = ''
            if code_col:
                codes = group[code_col].dropna().tolist()
                final_code = str(codes[-1])[:512] if codes else ''

            # Correctness
            is_correct = 0
            if score_col:
                scores = pd.to_numeric(group[score_col], errors='coerce').fillna(0)
                is_correct = int(scores.max() > 0)
            elif 'submit' in [str(a).lower() for a in actions]:
                is_correct = 1

            # Time stuck: total seconds
            time_stuck = float(sum(abs(d) for d in time_deltas))

            rows.append({
                'student_id':    str(sid),
                'problem_id':    str(pid),
                'code':          final_code,
                'error_message': '',
                'actions':       actions,
                'time_deltas':   time_deltas,
                'is_correct':    is_correct,
                'concept':       '',
                'emotion_label': _infer_emotion_from_actions(actions),
                'session_id':    f'{sid}_{pid}',
                'final_code':    final_code,
                'event_count':   len(group),
                'time_stuck':    time_stuck,
            })

        result = pd.DataFrame(rows)
        print(f"[ProgSnap2] Aggregated {len(result)} sessions")
        return result


# ── ASSISTmentsProcessor ──────────────────────────────────────────────────────

class ASSISTmentsProcessor:
    """
    Processes ASSISTments skill builder dataset.

    Expected file (after download_datasets.py):
        data/assistments/skill_builder_data.csv
        OR  2012-2013-data-with-predictions-4-final.csv

    Columns used:
        user_id, problem_id, correct, skill_name (or skill_id),
        attempt_count, hint_count

    Returns (responses_df, q_matrix_df) tuple.
    q_matrix_df has columns: problem_id, skill_name (long format).
    """

    def __init__(self, data_path: str, config: Dict):
        self.path   = Path(data_path)
        self.config = config

    def process(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        print(f"[ASSISTments] Processing from {self.path}")

        csv_path = None
        for name in ['skill_builder_data.csv',
                     '2012-2013-data-with-predictions-4-final.csv',
                     'assistments_data.csv']:
            p = self.path / name if self.path.is_dir() else self.path
            if p.exists():
                csv_path = p
                break
            if self.path.is_dir():
                matches = list(self.path.glob(f'**/{name}'))
                if matches:
                    csv_path = matches[0]
                    break

        if csv_path is None:
            print(f"[ASSISTments] No CSV found under {self.path}")
            return pd.DataFrame(), pd.DataFrame()

        try:
            df = _safe_read_csv(csv_path)
            print(f"[ASSISTments] Loaded {len(df)} responses from {csv_path.name}")
        except Exception as e:
            print(f"[ASSISTments] Error reading CSV: {e}")
            return pd.DataFrame(), pd.DataFrame()

        return self._process(df)

    def _process(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        df.columns = [c.strip().lower() for c in df.columns]

        user_col    = next((c for c in df.columns if 'user' in c), None)
        problem_col = next((c for c in df.columns if 'problem' in c), None)
        correct_col = next((c for c in df.columns if 'correct' in c), None)
        skill_col   = next((c for c in df.columns
                            if 'skill' in c and 'name' in c), None) or \
                      next((c for c in df.columns if 'skill' in c), None)
        attempt_col = next((c for c in df.columns if 'attempt' in c), None)
        hint_col    = next((c for c in df.columns if 'hint' in c), None)

        if not user_col or not correct_col:
            print("[ASSISTments] Missing required columns.")
            return pd.DataFrame(), pd.DataFrame()

        responses = pd.DataFrame({
            'user_id':     df[user_col].astype(str),
            'problem_id':  df[problem_col].astype(str) if problem_col else 'unknown',
            'correct':     pd.to_numeric(df[correct_col], errors='coerce').fillna(0).astype(int),
            'skill_name':  df[skill_col].astype(str) if skill_col else '',
            'attempt_count': pd.to_numeric(df[attempt_col], errors='coerce').fillna(1).astype(int)
                             if attempt_col else 1,
            'hint_count':  pd.to_numeric(df[hint_col], errors='coerce').fillna(0).astype(int)
                           if hint_col else 0,
        })

        # Build Q-matrix (problem → skill mapping)
        if skill_col and problem_col:
            q_matrix = responses[['problem_id', 'skill_name']].drop_duplicates()
        else:
            q_matrix = pd.DataFrame(columns=['problem_id', 'skill_name'])

        print(f"[ASSISTments] {len(responses)} responses, "
              f"{responses['user_id'].nunique()} students, "
              f"{responses['skill_name'].nunique()} skills")
        return responses, q_matrix


# ── MOOCCubeXProcessor ────────────────────────────────────────────────────────

class MOOCCubeXProcessor:
    """
    Processes MOOCCubeX course activity data.

    Expected files (after download_datasets.py):
        data/moocsxcube/entities.json
        data/moocsxcube/relations.json
        data/moocsxcube/knowledge_graph.json

    Extracts concept sequences per student for learning progression training.
    """

    def __init__(self, data_path: str, config: Dict):
        self.path   = Path(data_path)
        self.config = config

    def process(self) -> pd.DataFrame:
        print(f"[MOOCCubeX] Processing from {self.path}")

        entities_path = self.path / 'entities.json'
        relations_path = self.path / 'relations.json'

        if not entities_path.exists():
            print(f"[MOOCCubeX] entities.json not found under {self.path}")
            return pd.DataFrame()

        try:
            with open(entities_path) as f:
                entities = json.load(f)
            with open(relations_path) as f:
                relations = json.load(f)
        except Exception as e:
            print(f"[MOOCCubeX] Error reading JSON: {e}")
            return pd.DataFrame()

        return self._process(entities, relations)

    def _process(self, entities: Dict, relations: Dict) -> pd.DataFrame:
        students = entities.get('student', [])
        concepts = {c['id']: c.get('name', c['id'])
                    for c in entities.get('concept', [])}

        rows = []
        for student in students:
            sid = student.get('id', f's_{len(rows)}')
            # Build concept sequence from relations
            concept_ids = [r['concept_id'] for r in relations
                           if r.get('student_id') == sid]
            concept_seq = [concepts.get(cid, cid) for cid in concept_ids]

            rows.append({
                'student_id':       str(sid),
                'problem_id':       'mooccubex',
                'code':             '',
                'error_message':    '',
                'actions':          [],
                'time_deltas':      [],
                'is_correct':       1,
                'concept':          concept_seq[-1] if concept_seq else '',
                'emotion_label':    -1,
                'course_id':        student.get('course_id', ''),
                'concept_sequence': concept_seq,
            })

        result = pd.DataFrame(rows)
        print(f"[MOOCCubeX] Loaded {len(result)} student records")
        return result
