"""
10 Personalization Feature Conversation Scenarios
Each scenario contains 4-5 question-response pairs showing adaptive personalization
with qualitative and quantitative metrics for each response
"""

CONVERSATION_SCENARIOS = [
    {
        "scenario_id": "feature_001",
        "feature_name": "Conversation Memory & Context",
        "description": "System remembers and builds on previous conversation",
        "student_profile": {
            "student_id": "student_001",
            "mastery": 0.3,
            "learning_style": "visual",
            "personality": {"openness": 0.7, "neuroticism": 0.4}
        },
        "conversation": [
            {
                "turn": 1,
                "question": "What is a linked list?",
                "response": "A linked list is a data structure where elements are connected using pointers. Each element (node) contains data and a reference to the next node. Think of it like a treasure hunt where each clue points to the next location!",
                "features_detected": {
                    "conversation_memory": False,  # First question
                    "learning_style_adaptation": True,  # Visual metaphor used
                    "emotional_intelligence": False
                },
                "metrics": {
                    "qualitative": {
                        "uses_visual_metaphor": True,
                        "builds_context": True,
                        "appropriate_for_level": True
                    },
                    "quantitative": {
                        "response_length": 156,
                        "metaphor_count": 1,
                        "concept_clarity_score": 0.8
                    }
                }
            },
            {
                "turn": 2,
                "question": "How do I create one in Python?",
                "response": "Great question! Building on the treasure hunt analogy, here's how to create a linked list in Python:\n\n```python\nclass Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None  # This is like the clue pointing to next location\n\n# Create nodes\nnode1 = Node(10)\nnode2 = Node(20)\nnode1.next = node2  # Connect them!\n```\n\nNotice how `next` is like the pointer to the next treasure location!",
                "features_detected": {
                    "conversation_memory": True,  # References "treasure hunt" from previous
                    "learning_style_adaptation": True,  # Continues visual metaphor
                    "context_building": True
                },
                "metrics": {
                    "qualitative": {
                        "references_previous_metaphor": True,
                        "maintains_visual_style": True,
                        "provides_code_example": True,
                        "connects_to_previous": True
                    },
                    "quantitative": {
                        "previous_references": 2,  # "treasure hunt", "clue"
                        "metaphor_continuity": 1.0,
                        "code_example_present": True,
                        "context_continuity_score": 0.9
                    }
                }
            },
            {
                "turn": 3,
                "question": "What if I want to add a node at the beginning?",
                "response": "Excellent! You're thinking about insertion operations. Remember our treasure hunt? Adding at the beginning is like adding a new starting point!\n\n```python\ndef insert_at_beginning(head, data):\n    new_node = Node(data)\n    new_node.next = head  # New node points to old head\n    return new_node  # New node becomes the head\n```\n\nThis is similar to how we connected nodes before - we're just making the new node the first 'clue' in our hunt!",
                "features_detected": {
                    "conversation_memory": True,  # Strong reference to previous context
                    "learning_style_adaptation": True,  # Maintains visual metaphor
                    "progress_awareness": True,  # Acknowledges student's progress
                    "context_building": True
                },
                "metrics": {
                    "qualitative": {
                        "strong_context_reference": True,
                        "metaphor_consistency": True,
                        "acknowledges_progress": True,
                        "builds_on_previous": True
                    },
                    "quantitative": {
                        "previous_references": 3,  # "treasure hunt", "clue", "connected"
                        "metaphor_continuity": 1.0,
                        "progress_acknowledgment": 1,
                        "context_continuity_score": 0.95
                    }
                }
            },
            {
                "turn": 4,
                "question": "I'm confused about when to use head vs the node itself",
                "response": "That's a common point of confusion! Let me clarify using our treasure hunt analogy:\n\n- **head** = The STARTING POINT of the hunt (first clue)\n- **node** = Any individual clue in the chain\n\nWhen you do `head = insert_at_beginning(head, data)`, you're:\n1. Creating a new starting clue (new_node)\n2. Making it point to the old starting clue (new_node.next = head)\n3. Making it the NEW starting point (return new_node)\n\nThink of it like: if you find a clue BEFORE the first one, that becomes your new starting point!",
                "features_detected": {
                    "conversation_memory": True,  # Uses established metaphor
                    "learning_style_adaptation": True,  # Visual explanation
                    "emotional_intelligence": True,  # Normalizes confusion
                    "error_diagnostic": True,  # Addresses specific confusion
                    "context_building": True
                },
                "metrics": {
                    "qualitative": {
                        "uses_established_metaphor": True,
                        "normalizes_struggle": True,
                        "specific_clarification": True,
                        "maintains_consistency": True
                    },
                    "quantitative": {
                        "previous_references": 4,  # Multiple references to treasure hunt
                        "metaphor_continuity": 1.0,
                        "reassurance_phrases": 1,  # "common point"
                        "context_continuity_score": 0.98
                    }
                }
            },
            {
                "turn": 5,
                "question": "Now I understand! Can you show me how to traverse it?",
                "response": "Wonderful! I'm glad the treasure hunt analogy helped! Traversing is like following all the clues from start to finish:\n\n```python\ndef traverse(head):\n    current = head  # Start at the first clue\n    while current:  # While there's a clue to follow\n        print(current.data)  # Read the clue\n        current = current.next  # Move to next clue\n```\n\nYou start at `head` (first clue) and keep following `next` pointers until you reach `None` (end of hunt). This builds on everything we've discussed!",
                "features_detected": {
                    "conversation_memory": True,  # Strong - uses established metaphor throughout
                    "learning_style_adaptation": True,  # Continues visual style
                    "emotional_intelligence": True,  # Celebrates understanding
                    "progress_awareness": True,  # Acknowledges learning
                    "context_building": True
                },
                "metrics": {
                    "qualitative": {
                        "celebrates_success": True,
                        "maintains_metaphor": True,
                        "connects_all_concepts": True,
                        "shows_progress": True
                    },
                    "quantitative": {
                        "previous_references": 5,  # Multiple references
                        "metaphor_continuity": 1.0,
                        "positive_feedback": 1,
                        "context_continuity_score": 1.0,  # Perfect continuity
                        "overall_feature_score": 0.95
                    }
                }
            }
        ],
        "summary_metrics": {
            "conversation_memory_score": 0.95,
            "average_context_continuity": 0.96,
            "metaphor_consistency": 1.0,
            "feature_utilization": "Excellent"
        }
    },
    {
        "scenario_id": "feature_002",
        "feature_name": "Emotional Intelligence & Tone Adaptation",
        "description": "System adapts tone based on student's emotional state",
        "student_profile": {
            "student_id": "student_002",
            "mastery": 0.2,
            "frustration_level": 0.8,
            "emotion": "frustrated"
        },
        "conversation": [
            {
                "turn": 1,
                "question": "I've been stuck on recursion for 3 hours! Nothing works!",
                "response": "I completely understand your frustration - this is really challenging! Let's take a deep breath and break this down into tiny, manageable steps. You're not alone in finding recursion difficult; it's one of the most common struggles for students.\n\nLet's start with just ONE simple example, and we'll go very slowly. What specific error are you seeing?",
                "features_detected": {
                    "emotional_intelligence": True,  # Detects high frustration
                    "tone_adaptation": True,  # Gentle, supportive tone
                    "reassurance": True,
                    "step_size_adaptation": True  # Breaks into smaller steps
                },
                "metrics": {
                    "qualitative": {
                        "tone": "gentle_supportive",
                        "normalizes_struggle": True,
                        "encouraging": True,
                        "reduces_anxiety": True
                    },
                    "quantitative": {
                        "encouragement_phrases": 3,  # "understand", "not alone", "common"
                        "reassurance_words": 2,
                        "tone_appropriateness": 0.95,
                        "frustration_acknowledgment": 1.0
                    }
                }
            },
            {
                "turn": 2,
                "question": "It just keeps crashing! RecursionError: maximum recursion depth exceeded",
                "response": "Ah, I see the issue! This is actually a very common mistake - you're missing a base case. Don't worry, this happens to almost everyone learning recursion!\n\nThink of recursion like climbing stairs: you need to know when to STOP. The base case is your stopping point.\n\nCan you show me your code? I'll help you find where to add the base case - we'll do it together, step by step.",
                "features_detected": {
                    "emotional_intelligence": True,  # Maintains supportive tone
                    "error_diagnostic": True,  # Identifies the issue
                    "reassurance": True,  # Normalizes the error
                    "collaborative_language": True
                },
                "metrics": {
                    "qualitative": {
                        "maintains_supportive_tone": True,
                        "normalizes_error": True,
                        "collaborative": True,
                        "specific_help": True
                    },
                    "quantitative": {
                        "encouragement_phrases": 2,  # "common", "almost everyone"
                        "reassurance_words": 3,  # "Don't worry", "happens to", "together"
                        "tone_consistency": 0.9,
                        "support_level": 0.95
                    }
                }
            },
            {
                "turn": 3,
                "question": "Here's my code: def factorial(n): return n * factorial(n-1)",
                "response": "Perfect! I can see exactly what's happening. Your function is missing the base case - it never stops calling itself!\n\nHere's the fix - we need to tell it when to stop:\n\n```python\ndef factorial(n):\n    if n <= 1:  # BASE CASE - this is when we stop!\n        return 1\n    return n * factorial(n - 1)\n```\n\nThe `if n <= 1: return 1` is your stopping point. When n becomes 1 or 0, we stop recursing and just return 1.\n\nYou were SO close! This is a great learning moment. Try it now - I bet it works!",
                "features_detected": {
                    "emotional_intelligence": True,  # Encouraging, positive
                    "error_diagnostic": True,  # Specific fix
                    "progress_acknowledgment": True,  # "SO close"
                    "confidence_boosting": True
                },
                "metrics": {
                    "qualitative": {
                        "positive_encouragement": True,
                        "specific_solution": True,
                        "builds_confidence": True,
                        "celebrates_effort": True
                    },
                    "quantitative": {
                        "encouragement_phrases": 3,  # "Perfect", "SO close", "great learning"
                        "positive_feedback": 2,
                        "confidence_boost_score": 0.9,
                        "tone_appropriateness": 0.95
                    }
                }
            },
            {
                "turn": 4,
                "question": "It works! But I still don't really understand WHY it works",
                "response": "That's a fantastic question! Understanding the 'why' is the key to really mastering recursion.\n\nLet's trace through what happens:\n\n`factorial(3)` calls `factorial(2)`\n  → `factorial(2)` calls `factorial(1)`\n    → `factorial(1)` hits the base case and returns 1\n  → `factorial(2)` gets 1, multiplies by 2, returns 2\n→ `factorial(3)` gets 2, multiplies by 3, returns 6\n\nIt's like a stack of plates - you keep adding plates (calls) until you hit the bottom (base case), then you work your way back up, removing plates one by one!\n\nDoes this visualization help?",
                "features_detected": {
                    "emotional_intelligence": True,  # Enthusiastic, celebrates success
                    "learning_style_adaptation": True,  # Visual metaphor
                    "conceptual_depth": True,  # Explains "why"
                    "progress_awareness": True  # Acknowledges they got it working
                },
                "metrics": {
                    "qualitative": {
                        "celebrates_success": True,
                        "provides_deep_explanation": True,
                        "uses_visual_metaphor": True,
                        "encourages_understanding": True
                    },
                    "quantitative": {
                        "positive_feedback": 2,  # "fantastic", "key to mastering"
                        "explanation_depth": 0.9,
                        "metaphor_quality": 0.85,
                        "tone_evolution": "frustrated → confident"  # Shows emotional journey
                    }
                }
            },
            {
                "turn": 5,
                "question": "Yes! The stack visualization really helped. Can you give me another example?",
                "response": "Absolutely! I'm so glad the visualization clicked for you! You've made incredible progress - from being stuck to really understanding the concept!\n\nLet's try Fibonacci numbers - they're perfect for practicing recursion:\n\n```python\ndef fibonacci(n):\n    if n <= 1:  # Base case\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)  # Two recursive calls!\n```\n\nNotice the pattern? Base case first, then recursive calls. You've got this! Try tracing through `fibonacci(4)` using the stack visualization we just learned.",
                "features_detected": {
                    "emotional_intelligence": True,  # Celebrates progress enthusiastically
                    "progress_awareness": True,  # Acknowledges journey
                    "learning_style_adaptation": True,  # References visualization
                    "confidence_boosting": True,
                    "adaptive_difficulty": True  # Provides next challenge
                },
                "metrics": {
                    "qualitative": {
                        "strong_celebration": True,
                        "acknowledges_journey": True,
                        "references_previous_learning": True,
                        "appropriate_challenge": True
                    },
                    "quantitative": {
                        "celebration_phrases": 3,  # "so glad", "incredible progress", "You've got this"
                        "progress_acknowledgment": 1.0,
                        "confidence_level": 0.95,
                        "emotional_journey_score": 0.9  # Frustrated → Confident
                    }
                }
            }
        ],
        "summary_metrics": {
            "emotional_intelligence_score": 0.93,
            "tone_adaptation_accuracy": 0.95,
            "frustration_reduction": 0.85,  # From 0.8 to ~0.2
            "confidence_building": 0.9,
            "feature_utilization": "Excellent"
        }
    },
    {
        "scenario_id": "feature_003",
        "feature_name": "Learning Style - Visual Learner",
        "description": "System adapts to visual learning preferences",
        "student_profile": {
            "student_id": "student_003",
            "mastery": 0.4,
            "learning_style": "visual",
            "preferences": {"format": "diagrams", "examples": "visual"}
        },
        "conversation": [
            {
                "turn": 1,
                "question": "I don't understand how pointers work in linked lists",
                "response": "Great question! Let me show you visually. Imagine a linked list like a chain of paper clips:\n\n```
[Data: 10] → [Data: 20] → [Data: 30] → None
   ↑              ↑              ↑
 node1          node2          node3
```\n\nEach paper clip (node) has:\n- **Data**: The value it holds (10, 20, 30)\n- **Next**: A pointer to the next paper clip\n\nThe arrow (→) shows the connection. When you do `node1.next = node2`, you're physically connecting the first paper clip to the second!\n\nCan you visualize this chain in your mind?",
                "features_detected": {
                    "learning_style_adaptation": True,  # Visual diagram and metaphor
                    "visual_elements": True,
                    "spatial_descriptions": True
                },
                "metrics": {
                    "qualitative": {
                        "uses_visual_diagram": True,
                        "spatial_metaphor": True,
                        "concrete_imagery": True,
                        "visualization_prompt": True
                    },
                    "quantitative": {
                        "visual_keywords": 4,  # "visually", "imagine", "chain", "visualize"
                        "diagram_elements": 1,
                        "spatial_descriptions": 3,
                        "visual_style_score": 0.95
                    }
                }
            },
            {
                "turn": 2,
                "question": "What happens when I add a node in the middle?",
                "response": "Excellent! Let's visualize this step-by-step. Picture your chain:\n\n**Before:**\n```
[A] → [B] → [C] → None
```\n\n**Step 1:** Create new node [X]\n```
[A] → [B] → [C] → None
       ↑
      [X]  (floating, not connected yet)
```\n\n**Step 2:** Make [X] point to [B]\n```
[A] → [B] → [C] → None
       ↑
      [X] ──┘
```\n\n**Step 3:** Make [A] point to [X]\n```
[A] → [X] → [B] → [C] → None
```\n\nSee how we 'spliced' [X] into the chain? The visual flow helps understand the pointer manipulation!",
                "features_detected": {
                    "learning_style_adaptation": True,  # Multiple visual diagrams
                    "step_by_step_visual": True,
                    "spatial_reasoning": True
                },
                "metrics": {
                    "qualitative": {
                        "multiple_visual_steps": True,
                        "progressive_diagrams": True,
                        "spatial_manipulation": True,
                        "visual_flow": True
                    },
                    "quantitative": {
                        "visual_keywords": 5,  # "visualize", "picture", "see", "visual", "flow"
                        "diagram_count": 4,  # 4 different states shown
                        "spatial_descriptions": 4,
                        "visual_style_score": 0.98
                    }
                }
            },
            {
                "turn": 3,
                "question": "Can you show me what happens in memory?",
                "response": "Absolutely! Let's visualize the actual memory layout. Think of memory like a grid of boxes:\n\n```
Memory Address    |  Data  |  Next Pointer
------------------|--------|---------------
0x1000            |   10   |  0x2000  → points to address 0x2000
0x2000            |   20   |  0x3000  → points to address 0x3000
0x3000            |   30   |  None    → end of list
```\n\nWhen you do `current = current.next`, you're:\n1. Looking at current node's 'Next Pointer' (e.g., 0x2000)\n2. Jumping to that memory address\n3. Reading the data there\n\nIt's like following street addresses - each node tells you where the next one lives! The visual of memory addresses really helps, right?",
                "features_detected": {
                    "learning_style_adaptation": True,  # Memory visualization
                    "conceptual_depth": True,  # Explains memory addresses
                    "visual_metaphor": True  # Street addresses
                },
                "metrics": {
                    "qualitative": {
                        "memory_visualization": True,
                        "address_metaphor": True,
                        "concrete_example": True,
                        "maintains_visual_style": True
                    },
                    "quantitative": {
                        "visual_keywords": 6,  # "visualize", "grid", "see", "visual", "street addresses", "visual"
                        "diagram_elements": 1,  # Memory table
                        "spatial_metaphors": 2,  # "grid", "street addresses"
                        "visual_style_score": 0.97
                    }
                }
            },
            {
                "turn": 4,
                "question": "What if I want to delete a node?",
                "response": "Great question! Let's visualize deletion. Imagine you want to remove [B] from this chain:\n\n**Before deletion:**\n```
[A] → [B] → [C] → None
```\n\n**The process:**\n1. Find [B] (the node to delete)\n2. Make [A]'s pointer skip [B] and point directly to [C]\n\n**After deletion:**\n```
[A] ──────────→ [C] → None
      (skips B)
```\n\n**In code:**\n```python\nprev.next = node_to_delete.next  # Skip over the node!\n```\n\nThink of it like removing a link from a chain - you connect the links on either side, and the middle one falls away! The visual really makes this clear, doesn't it?",
                "features_detected": {
                    "learning_style_adaptation": True,  # Visual deletion process
                    "spatial_manipulation": True,
                    "metaphor_consistency": True  # Continues chain metaphor
                },
                "metrics": {
                    "qualitative": {
                        "visual_deletion_process": True,
                        "before_after_diagram": True,
                        "consistent_metaphor": True,
                        "spatial_understanding": True
                    },
                    "quantitative": {
                        "visual_keywords": 5,  # "visualize", "imagine", "see", "visual", "visual"
                        "diagram_count": 2,  # Before and after
                        "spatial_descriptions": 3,
                        "visual_style_score": 0.96
                    }
                }
            },
            {
                "turn": 5,
                "question": "I think I understand now! Can you give me a visual exercise?",
                "response": "Perfect! I love that you're thinking visually! Here's a fun exercise:\n\n**Visual Challenge:**\nDraw this linked list on paper:\n```
[5] → [10] → [15] → [20] → None
```\n\nNow, **without writing code**, trace through what happens when you:\n1. Insert [7] between [5] and [10]\n2. Delete [15]\n3. Add [25] at the end\n\nDraw each step! This visual practice will really cement your understanding. The act of drawing helps your brain form stronger connections.\n\nOnce you've drawn it, we can write the code together!",
                "features_detected": {
                    "learning_style_adaptation": True,  # Visual exercise
                    "progress_awareness": True,  # Celebrates understanding
                    "hands_on_visual": True,
                    "adaptive_pedagogy": True  # Drawing exercise
                },
                "metrics": {
                    "qualitative": {
                        "visual_exercise": True,
                        "celebrates_understanding": True,
                        "encourages_drawing": True,
                        "hands_on_learning": True
                    },
                    "quantitative": {
                        "visual_keywords": 4,  # "visually", "draw", "visual", "drawing"
                        "exercise_type": "visual",
                        "engagement_score": 0.95,
                        "visual_style_score": 0.98,
                        "overall_feature_score": 0.96
                    }
                }
            }
        ],
        "summary_metrics": {
            "visual_adaptation_score": 0.97,
            "average_visual_keywords": 4.8,
            "diagram_usage": "Consistent",
            "spatial_metaphor_consistency": 0.95,
            "feature_utilization": "Excellent"
        }
    }
]

# Continue with remaining 7 scenarios...
# (I'll create a complete version with all 10)

















