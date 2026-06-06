"""
End-to-end smoke test for the CSO-grounded student knowledge graph.

Simulates 4 fully-instrumented diagnose() turns for student 'maya', populating
EVERY per-turn CPAL analysis (LP, DINA mastery, wrong-model, three-channel
state, intervention, RL reward, heuristic flags, probe state, fact-check),
then dumps the resulting graph as JSON.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.knowledge_graph.student_graph_service import StudentGraphService


TURNS = [
    {
        "diag":            {"concept": "command_line_args", "current_lp_level": "L1",
                            "diagnostic_confidence": 0.45, "wrong_model_id": "CL-A"},
        "mastery_before":  0.20, "mastery": 0.32,
        "text":            "args[0] is empty when nothing passed.",
        "three_channel":   {
            "cognitive":     {"encoding_strength": "surface", "dual_coding": "verbal_only"},
            "progression":   {"stage": "1", "zpd_position": "overwhelmed", "scaffold_level": "high"},
            "psychological": {"attribution": "adaptive", "imposter_signal": False,
                              "high_anxiety": False, "self_efficacy": "neutral"},
        },
        "intervention":    {"type": "worked_example", "rationale": "L1 + surface encoding",
                            "gate_triggered": False},
        "reward":          {"total": 0.05, "breakdown": {"learning_gain": 0.10, "engagement": 0.06,
                                                         "zpd_alignment": -0.50, "emotional_state": 0.0,
                                                         "attribution_shift": 0.0, "lp_gain": 0.0}},
        "heuristics":      {"substance_penalty": False, "mech_vocab_bump": False,
                            "l2_rule_naming": False, "parroting_downgrade": False,
                            "transfer_upgrade": False},
        "probe_state":     {"count": 1, "cap": 8, "criteria": ["args length"]},
        "fact_check":      {"passed": True, "stripped": 0},
    },
    {
        "diag":            {"concept": "command_line_args", "current_lp_level": "L2",
                            "diagnostic_confidence": 0.62, "wrong_model_id": "CL-A"},
        "mastery_before":  0.32, "mastery": 0.55,
        "text":            "You have to pass at least one argument.",
        "three_channel":   {
            "cognitive":     {"encoding_strength": "partial", "dual_coding": "verbal+code"},
            "progression":   {"stage": "2b", "zpd_position": "at_boundary", "scaffold_level": "medium"},
            "psychological": {"attribution": "adaptive", "imposter_signal": False,
                              "high_anxiety": False, "self_efficacy": "neutral"},
        },
        "intervention":    {"type": "rule_naming", "rationale": "L2 rule named, push to mechanism",
                            "gate_triggered": False},
        "reward":          {"total": 0.28, "breakdown": {"learning_gain": 0.40, "engagement": 0.18,
                                                         "zpd_alignment": 0.20, "emotional_state": 0.0,
                                                         "attribution_shift": 0.0, "lp_gain": 0.50}},
        "heuristics":      {"substance_penalty": False, "mech_vocab_bump": False,
                            "l2_rule_naming": True, "parroting_downgrade": False,
                            "transfer_upgrade": False},
        "probe_state":     {"count": 2, "cap": 8, "criteria": ["args length", "runtime exception"]},
        "fact_check":      {"passed": True, "stripped": 0},
    },
    {
        "diag":            {"concept": "command_line_args", "current_lp_level": "L3",
                            "diagnostic_confidence": 0.81, "wrong_model_id": None},
        "mastery_before":  0.55, "mastery": 0.78,
        "text":            "args is an array; no args -> length 0 -> args[0] out of bounds.",
        "three_channel":   {
            "cognitive":     {"encoding_strength": "solid", "dual_coding": "dual"},
            "progression":   {"stage": "3", "zpd_position": "in_zpd", "scaffold_level": "low"},
            "psychological": {"attribution": "adaptive", "imposter_signal": False,
                              "high_anxiety": False, "self_efficacy": "growth"},
        },
        "intervention":    {"type": "trace_scaffold",
                            "rationale": "plateau cleared at L3 via mechanism trace",
                            "gate_triggered": True},
        "reward":          {"total": 0.62, "breakdown": {"learning_gain": 0.50, "engagement": 0.22,
                                                         "zpd_alignment": 1.00, "emotional_state": 0.10,
                                                         "attribution_shift": 0.0, "lp_gain": 0.50}},
        "heuristics":      {"substance_penalty": False, "mech_vocab_bump": True,
                            "l2_rule_naming": False, "parroting_downgrade": False,
                            "transfer_upgrade": False},
        "probe_state":     {"count": 3, "cap": 8,
                            "criteria": ["args length", "runtime exception", "args content"]},
        "fact_check":      {"passed": True, "stripped": 0},
    },
    {
        "diag":            {"concept": "string_equality", "current_lp_level": "L1",
                            "diagnostic_confidence": 0.40, "wrong_model_id": "SE-A"},
        "mastery_before":  0.20, "mastery": 0.25,
        "text":            "== works on int so it should work on strings too.",
        "three_channel":   {
            "cognitive":     {"encoding_strength": "surface", "dual_coding": "verbal_only"},
            "progression":   {"stage": "1", "zpd_position": "overwhelmed", "scaffold_level": "high"},
            "psychological": {"attribution": "adaptive", "imposter_signal": False,
                              "high_anxiety": False, "self_efficacy": "neutral"},
        },
        "intervention":    {"type": "worked_example",
                            "rationale": "L1 + WM detected on new concept",
                            "gate_triggered": False},
        "reward":          {"total": 0.04, "breakdown": {"learning_gain": 0.04, "engagement": 0.10,
                                                         "zpd_alignment": -0.50, "emotional_state": 0.0,
                                                         "attribution_shift": 0.0, "lp_gain": 0.0}},
        "heuristics":      {"substance_penalty": False, "mech_vocab_bump": False,
                            "l2_rule_naming": False, "parroting_downgrade": False,
                            "transfer_upgrade": False},
        "probe_state":     {"count": 1, "cap": 8, "criteria": ["== references"]},
        "fact_check":      {"passed": True, "stripped": 0},
    },
]


def main() -> None:
    svc = StudentGraphService.shared()
    for t in TURNS:
        svc.record_turn(student_id="maya",
                         diag=t["diag"], mastery=t["mastery"],
                         mastery_before=t["mastery_before"],
                         misconception_text=t["text"],
                         three_channel=t["three_channel"],
                         intervention=t["intervention"],
                         reward=t["reward"],
                         heuristics=t["heuristics"],
                         probe_state=t["probe_state"],
                         fact_check=t["fact_check"],
                         expand_cso=True, persist=False)

    payload = svc.render_payload("maya")
    out = ROOT / "output" / "maya_student_graph.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    print(f"Graph payload written to {out}")
    print()
    print("=== SUMMARY ===")
    print(json.dumps(payload["summary"], indent=2))
    print()
    print("=== ENGAGED NODES ===")
    for n in payload["nodes"]:
        if not n["is_neighbour_only"]:
            print()
            print(json.dumps(n, indent=2, default=str))


if __name__ == "__main__":
    main()
