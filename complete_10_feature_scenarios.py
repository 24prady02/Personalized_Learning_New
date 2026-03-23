"""
Complete 10 Personalization Feature Conversation Scenarios
Each with 4-5 question-response pairs, showing adaptive responses
with qualitative and quantitative metrics
"""

COMPLETE_SCENARIOS = {
    "feature_001_conversation_memory": {
        "scenario_id": "feature_001",
        "feature_name": "Conversation Memory & Context",
        "conversation": [
            {
                "turn": 1,
                "question": "What is a linked list?",
                "response": "A linked list is a data structure where elements are connected using pointers. Each element (node) contains data and a reference to the next node. Think of it like a treasure hunt where each clue points to the next location!",
                "metrics": {
                    "qualitative": {"uses_metaphor": True, "builds_context": True},
                    "quantitative": {"response_length": 156, "metaphor_count": 1, "context_score": 0.8}
                }
            },
            {
                "turn": 2,
                "question": "How do I create one in Python?",
                "response": "Great question! Building on the treasure hunt analogy, here's how to create a linked list in Python:\n\n```python\nclass Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None  # This is like the clue pointing to next location\n```\n\nNotice how `next` is like the pointer to the next treasure location!",
                "metrics": {
                    "qualitative": {"references_previous": True, "maintains_metaphor": True},
                    "quantitative": {"previous_references": 2, "metaphor_continuity": 1.0, "context_score": 0.9}
                }
            },
            {
                "turn": 3,
                "question": "What if I want to add a node at the beginning?",
                "response": "Excellent! You're thinking about insertion operations. Remember our treasure hunt? Adding at the beginning is like adding a new starting point!\n\n```python\ndef insert_at_beginning(head, data):\n    new_node = Node(data)\n    new_node.next = head  # New node points to old head\n    return new_node\n```\n\nThis is similar to how we connected nodes before - we're just making the new node the first 'clue' in our hunt!",
                "metrics": {
                    "qualitative": {"strong_context_reference": True, "builds_on_previous": True},
                    "quantitative": {"previous_references": 3, "context_continuity": 0.95}
                }
            },
            {
                "turn": 4,
                "question": "I'm confused about when to use head vs the node itself",
                "response": "That's a common point of confusion! Let me clarify using our treasure hunt analogy:\n\n- **head** = The STARTING POINT of the hunt (first clue)\n- **node** = Any individual clue in the chain\n\nWhen you do `head = insert_at_beginning(head, data)`, you're creating a new starting clue that points to the old starting clue. Think of it like: if you find a clue BEFORE the first one, that becomes your new starting point!",
                "metrics": {
                    "qualitative": {"uses_established_metaphor": True, "specific_clarification": True},
                    "quantitative": {"previous_references": 4, "context_continuity": 0.98}
                }
            },
            {
                "turn": 5,
                "question": "Now I understand! Can you show me how to traverse it?",
                "response": "Wonderful! I'm glad the treasure hunt analogy helped! Traversing is like following all the clues from start to finish:\n\n```python\ndef traverse(head):\n    current = head  # Start at the first clue\n    while current:  # While there's a clue to follow\n        print(current.data)\n        current = current.next  # Move to next clue\n```\n\nYou start at `head` (first clue) and keep following `next` pointers until you reach `None` (end of hunt). This builds on everything we've discussed!",
                "metrics": {
                    "qualitative": {"celebrates_success": True, "maintains_metaphor": True, "connects_all_concepts": True},
                    "quantitative": {"previous_references": 5, "context_continuity": 1.0, "overall_score": 0.95}
                }
            }
        ],
        "summary": {"conversation_memory_score": 0.95, "context_continuity": 0.96}
    },
    "feature_002_emotional_intelligence": {
        "scenario_id": "feature_002",
        "feature_name": "Emotional Intelligence & Tone Adaptation",
        "conversation": [
            {
                "turn": 1,
                "question": "I've been stuck on recursion for 3 hours! Nothing works!",
                "response": "I completely understand your frustration - this is really challenging! Let's take a deep breath and break this down into tiny, manageable steps. You're not alone in finding recursion difficult; it's one of the most common struggles for students.\n\nLet's start with just ONE simple example, and we'll go very slowly. What specific error are you seeing?",
                "metrics": {
                    "qualitative": {"tone": "gentle_supportive", "normalizes_struggle": True, "reassuring": True},
                    "quantitative": {"encouragement_phrases": 3, "tone_appropriateness": 0.95, "frustration_acknowledgment": 1.0}
                }
            },
            {
                "turn": 2,
                "question": "It just keeps crashing! RecursionError: maximum recursion depth exceeded",
                "response": "Ah, I see the issue! This is actually a very common mistake - you're missing a base case. Don't worry, this happens to almost everyone learning recursion!\n\nThink of recursion like climbing stairs: you need to know when to STOP. The base case is your stopping point.\n\nCan you show me your code? I'll help you find where to add the base case - we'll do it together, step by step.",
                "metrics": {
                    "qualitative": {"maintains_supportive_tone": True, "normalizes_error": True, "collaborative": True},
                    "quantitative": {"encouragement_phrases": 2, "reassurance_words": 3, "tone_consistency": 0.9}
                }
            },
            {
                "turn": 3,
                "question": "Here's my code: def factorial(n): return n * factorial(n-1)",
                "response": "Perfect! I can see exactly what's happening. Your function is missing the base case - it never stops calling itself!\n\nHere's the fix:\n\n```python\ndef factorial(n):\n    if n <= 1:  # BASE CASE - this is when we stop!\n        return 1\n    return n * factorial(n - 1)\n```\n\nThe `if n <= 1: return 1` is your stopping point. You were SO close! This is a great learning moment. Try it now - I bet it works!",
                "metrics": {
                    "qualitative": {"positive_encouragement": True, "builds_confidence": True, "celebrates_effort": True},
                    "quantitative": {"encouragement_phrases": 3, "confidence_boost_score": 0.9}
                }
            },
            {
                "turn": 4,
                "question": "It works! But I still don't really understand WHY it works",
                "response": "That's a fantastic question! Understanding the 'why' is the key to really mastering recursion.\n\nLet's trace through what happens:\n\n`factorial(3)` calls `factorial(2)`\n  → `factorial(2)` calls `factorial(1)`\n    → `factorial(1)` hits the base case and returns 1\n  → `factorial(2)` gets 1, multiplies by 2, returns 2\n→ `factorial(3)` gets 2, multiplies by 3, returns 6\n\nIt's like a stack of plates - you keep adding plates (calls) until you hit the bottom (base case), then you work your way back up! Does this visualization help?",
                "metrics": {
                    "qualitative": {"celebrates_success": True, "enthusiastic": True, "provides_deep_explanation": True},
                    "quantitative": {"positive_feedback": 2, "explanation_depth": 0.9, "tone_evolution": "frustrated → confident"}
                }
            },
            {
                "turn": 5,
                "question": "Yes! The stack visualization really helped. Can you give me another example?",
                "response": "Absolutely! I'm so glad the visualization clicked for you! You've made incredible progress - from being stuck to really understanding the concept!\n\nLet's try Fibonacci numbers:\n\n```python\ndef fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n```\n\nNotice the pattern? Base case first, then recursive calls. You've got this! Try tracing through `fibonacci(4)` using the stack visualization we just learned.",
                "metrics": {
                    "qualitative": {"strong_celebration": True, "acknowledges_journey": True, "confident_tone": True},
                    "quantitative": {"celebration_phrases": 3, "progress_acknowledgment": 1.0, "emotional_journey_score": 0.9}
                }
            }
        ],
        "summary": {"emotional_intelligence_score": 0.93, "tone_adaptation": 0.95, "frustration_reduction": 0.85}
    }
    # ... (I'll create a script to generate all 10 complete scenarios)
}














