"""
End-to-end programmatic test of the quiz API after wiring LPDiagnostician,
level-aware explanation, anti-cliche guardrails, and lp_sub_criteria probe
picking into student_app.py.

Drives the actual HTTP endpoints (the same ones the frontend hits):
    GET  /api/start         → first quiz item
    POST /api/answer        → record MCQ choice
    POST /api/correct       → submit belief, get probe OR explanation
    POST /api/probe_answer  → if probed, submit follow-up

Two passes per quiz item, varying the belief level:
  Pass A — VAGUE belief (should trigger a probe; then follow-up; then
            explanation shaped for the graded level).
  Pass B — PRECISE belief that names mechanism (should skip probe; explanation
            shaped for L3+ — no re-teach).

The server must already be running on port 8001:
    python -m uvicorn api.student_app:app --port 8001
"""
import json
import sys
import time
from pathlib import Path

import requests

BASE = "http://localhost:8001"


def post(path: str, payload: dict) -> dict:
    r = requests.post(f"{BASE}{path}", json=payload, timeout=120)
    r.raise_for_status()
    return r.json()


def get(path: str) -> dict:
    r = requests.get(f"{BASE}{path}", timeout=10)
    r.raise_for_status()
    return r.json()


def run_pass(label: str, belief: str, max_probes: int = 2) -> None:
    print("=" * 78)
    print(f"PASS: {label}")
    print("=" * 78)
    sess = get("/api/start")
    sid = sess["session_id"]
    item = sess["item"]
    print(f"  session     : {sid}")
    print(f"  item.concept: {item['concept']}")
    print(f"  item.title  : {item['title']}")
    print(f"  question    : {item['question']}")

    # Pick the FIRST option as the MCQ choice — quiz routes via belief, not MCQ.
    choice = item["options"][0]["key"]
    print(f"  choice      : {choice}")
    post("/api/answer", {"session_id": sid, "choice": choice, "belief": ""})

    print(f"\n  -> /api/correct  belief = {belief!r}")
    resp = post("/api/correct", {"session_id": sid, "belief": belief})

    probe_n = 0
    # Follow the probe ladder (up to max_probes per item).
    while resp.get("type") == "probe" and probe_n < max_probes:
        probe_n += 1
        print(f"\n  +-- PROBE #{probe_n}/{resp.get('probe_round_max')} "
              f"(target {resp.get('probe_target_level')})")
        print(f"  |   question: {resp.get('probe_question')}")
        # Send a plausible probe answer that tries to name the mechanism.
        answer = (
            "I think it's because each new String() creates its own object in "
            "memory, so the two variables don't point to the same place."
        )
        print(f"  |   -> /api/probe_answer  answer = {answer!r}")
        resp = post("/api/probe_answer",
                    {"session_id": sid, "probe_answer": answer})
        print(f"  +-- response type now: {resp.get('type')}")

    print(f"\n  FINAL response type: {resp.get('type')}")
    if resp.get("type") == "explanation":
        print(f"  verdict           : you={resp['your_choice']} correct={resp['correct_choice']}")
        print(f"  next_item_id      : {resp.get('next_item_id')}")
        print(f"  --- explanation text ---")
        for line in (resp.get("explanation") or "").splitlines():
            print(f"  | {line}")
    elif resp.get("type") == "probe":
        print(f"  STILL probing after cap — should not happen.")


def main() -> None:
    # Quick health check
    try:
        h = get("/api/health")
        print(f"health: {h}")
    except Exception as e:
        print(f"Server not reachable at {BASE} — start it with:\n"
              f"    python -m uvicorn api.student_app:app --port 8001")
        sys.exit(2)

    # Pass A — vague belief expected to trigger probe
    run_pass(
        "A — vague belief (expect probe -> follow-up -> explanation)",
        belief="I think it just compares them somehow, not sure why == is wrong",
    )

    print("\n")
    # Pass B — precise belief that traces mechanism
    run_pass(
        "B — precise belief (expect no probe; L3-shaped explanation)",
        belief=("each new String() allocates a separate object on the heap; "
                "the two variables hold different addresses, so == checks the "
                "addresses and returns false, while .equals() compares the "
                "characters one by one"),
    )


if __name__ == "__main__":
    main()
