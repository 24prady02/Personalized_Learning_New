"""
End-to-end test: student prompt -> Big Five -> Nestor learning profile.
Runs a handful of prompts that should produce noticeably different profiles
and confirms the pipeline produces plausible, differentiated output.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.nestor.nestor_bayesian_profiler import NestorBayesianProfiler


PROMPTS = [
    # should read as high-openness / exploratory / conceptual
    ("explorer", "I'm fascinated by how recursion actually works under the hood — "
                 "is the call stack like a hidden deque, or is there something more "
                 "elegant going on with how the runtime tracks frames? I tried tracing "
                 "factorial by hand and it's beautiful but I want to understand *why* "
                 "it works, not just that it does."),

    # high-neuroticism / anxious / imposter
    ("anxious", "Honestly I think I'm just bad at programming. Everyone in my class "
                "gets this stuff and I feel stupid for not being able to figure out "
                "why my loop never ends. I've been staring at this for two hours and "
                "nothing I try works. I don't think I'm cut out for CS."),

    # high-conscientiousness / structured / detail-oriented
    ("structured", "I've been working through the chapter exercises in order and I've "
                   "verified my solutions for 1-7 all compile and pass the provided "
                   "tests. For exercise 8 I want to make sure I understand the "
                   "expected input format before I start — what does the spec mean by "
                   "'trailing whitespace is ignored'?"),

    # high-extraversion / casual / social
    ("social", "yooo okay so me and my study group were debating whether you should "
               "use a HashMap or a TreeMap for this thing. I think HashMap is faster "
               "but Alex says TreeMap gives you ordering for free. what do u think? "
               "also can we talk through it on discord tonight?"),

    # high-agreeableness / polite / collaborative
    ("collaborative", "Hi! Sorry to bother you — I was hoping you could help me "
                      "understand why my code produces the wrong output for n=0. I "
                      "don't want to take too much of your time, but any hints would "
                      "be really appreciated. Thank you so much!"),
]


def main():
    print("=" * 70)
    print("Prompt -> Big Five -> Nestor pipeline")
    print("=" * 70)
    prof = NestorBayesianProfiler({"nestor": {"data_dir": "data/nestor"}})
    assert prof.is_trained, "Nestor CPTs should be loaded"

    for tag, prompt in PROMPTS:
        print(f"\n--- {tag.upper()} ---")
        print(f"prompt: {prompt[:140]}{'...' if len(prompt) > 140 else ''}")
        out = prof.infer_from_prompt(prompt)
        p = out['personality']
        s = out['learning_styles']
        i = out['intervention_preference']
        t = out['learning_strategies']
        print(f"source: {out['personality_source']}")
        print(f"Big5   : " + "  ".join(
            f"{k[:3]}={p[k]:.2f}"
            for k in ('openness', 'conscientiousness', 'extraversion',
                      'agreeableness', 'neuroticism')
        ))
        print(f"style (label):  {s['visual_verbal']:>8} / "
              f"{s['sensing_intuitive']:>10} / "
              f"{s['active_reflective']:>10} / "
              f"{s['sequential_global']:>10}")
        print(f"style (score):  vis→verb={s['visual_verbal_score']:.2f} "
              f"sens→intu={s['sensing_intuitive_score']:.2f} "
              f"act→refl={s['active_reflective_score']:.2f} "
              f"seq→glob={s['sequential_global_score']:.2f}")
        print(f"strategy scores: deep={t['deep_processing_score']:.2f} "
              f"elab={t['elaboration_score']:.2f} "
              f"org={t['organization_score']:.2f} "
              f"meta={t['metacognition_score']:.2f}")
        print(f"top-3 elements : {out['recommended_elements']}")
        print(f"intervention   : {i}")


if __name__ == "__main__":
    main()
