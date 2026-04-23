"""
Run 3 Codebase Conversation Tests for feature_test_results_2
These are realistic codebase conversations that help test the system output
"""

import os
import json
from datetime import datetime
from chat_interface_simple import ChatInterface
import sys

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Try to use REAL models first
USE_REAL_MODELS = True
try:
    from feature_test_results.enhanced_metrics_real import (
        RealDINAModel, RealCodeBERT, RealBERT, 
        RealNestor, TimeTracker, CSEKGConceptExtractor,
        calculate_learning_outcome_metrics
    )
    print("✓ Using REAL AI models (DINA, CodeBERT, BERT, Nestor, CSE-KG)")
except ImportError:
    USE_REAL_MODELS = False
    try:
        from feature_test_results.enhanced_metrics import (
            SimulatedDINAModel as RealDINAModel,
            SimulatedCodeBERT as RealCodeBERT,
            SimulatedBERT as RealBERT,
            SimulatedNestor as RealNestor,
            TimeTracker, calculate_learning_outcome_metrics
        )
        CSEKGConceptExtractor = None
        print("⚠ Using SIMULATED models (fallback)")
    except ImportError:
        sys.path.insert(0, os.path.join(current_dir, 'feature_test_results'))
        from enhanced_metrics import (
            SimulatedDINAModel as RealDINAModel,
            SimulatedCodeBERT as RealCodeBERT,
            SimulatedBERT as RealBERT,
            SimulatedNestor as RealNestor,
            TimeTracker, calculate_learning_outcome_metrics
        )
        CSEKGConceptExtractor = None
        print("⚠ Using SIMULATED models (fallback)")

try:
    from feature_test_results.dynamic_analysis import (
        ConceptExtractor, CodeGenerator, KnowledgeTracker
    )
except ImportError:
    sys.path.insert(0, os.path.join(current_dir, 'feature_test_results'))
    from dynamic_analysis import (
        ConceptExtractor, CodeGenerator, KnowledgeTracker
    )

# Get API key
groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key:
    print("[ERROR] GROQ_API_KEY environment variable not set!")
    print("[INFO] Please set it using: set GROQ_API_KEY=your_api_key")
    sys.exit(1)


# 3 Realistic Codebase Conversation Scenarios
CODEBASE_CONVERSATIONS = [
    {
        "conversation_id": "conv_001",
        "title": "Recursion Debugging - Missing Base Case",
        "description": "Student struggles with recursion, missing base case causes infinite loop",
        "student_profile": {
            "student_id": "student_recursion_001",
            "mastery": 0.25,
            "learning_style": "verbal",
            "personality": {"openness": 0.6, "neuroticism": 0.7, "conscientiousness": 0.5}
        },
        "conversation": [
            {
                "turn": 1,
                "question": "I'm trying to write a recursive function to calculate factorial, but I keep getting an error. Can you help me understand what's wrong?",
                "code": "def factorial(n):\n    return n * factorial(n - 1)\n\nprint(factorial(5))",
                "error_message": "RecursionError: maximum recursion depth exceeded"
            },
            {
                "turn": 2,
                "question": "Oh I see! I need a base case. But I'm confused - when should the recursion stop? What value should I return?",
                "code": "def factorial(n):\n    if n == 0:  # Is this right?\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(5))"
            },
            {
                "turn": 3,
                "question": "Great! That works. But I'm still confused - why does factorial(0) return 1? That seems weird to me.",
                "code": "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(0))  # Why is this 1?"
            },
            {
                "turn": 4,
                "question": "Thanks for explaining! Now I want to try a different recursive problem - Fibonacci. Can you check if my approach is correct?",
                "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n - 1) + fibonacci(n - 2)\n\nprint(fibonacci(10))"
            },
            {
                "turn": 5,
                "question": "It works but it's really slow for larger numbers. Is there a way to make it faster? I heard about memoization but I don't understand how it works.",
                "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n - 1) + fibonacci(n - 2)\n\nprint(fibonacci(35))  # This takes forever!"
            }
        ]
    },
    {
        "conversation_id": "conv_002",
        "title": "Tree Traversal Learning - Understanding DFS vs BFS",
        "description": "Student learns about tree data structures and different traversal methods",
        "student_profile": {
            "student_id": "student_tree_001",
            "mastery": 0.4,
            "learning_style": "visual",
            "personality": {"openness": 0.8, "neuroticism": 0.3, "conscientiousness": 0.7}
        },
        "conversation": [
            {
                "turn": 1,
                "question": "I'm learning about binary trees. I created a simple tree structure but I'm not sure how to traverse it. Can you help me understand the different ways?",
                "code": "class TreeNode:\n    def __init__(self, val):\n        self.val = val\n        self.left = None\n        self.right = None\n\n# Create a tree\nroot = TreeNode(1)\nroot.left = TreeNode(2)\nroot.right = TreeNode(3)\nroot.left.left = TreeNode(4)\nroot.left.right = TreeNode(5)\n\n# How do I traverse this?"
            },
            {
                "turn": 2,
                "question": "I tried to implement in-order traversal but I'm getting confused about when to visit the node. Is this correct?",
                "code": "def inorder_traversal(root):\n    if root:\n        inorder_traversal(root.left)\n        print(root.val)  # Visit node\n        inorder_traversal(root.right)\n\ninorder_traversal(root)"
            },
            {
                "turn": 3,
                "question": "That works! But what's the difference between in-order, pre-order, and post-order? When would I use each one?",
                "code": "def preorder_traversal(root):\n    if root:\n        print(root.val)  # Visit first\n        preorder_traversal(root.left)\n        preorder_traversal(root.right)\n\n# What's the difference and when to use each?"
            },
            {
                "turn": 4,
                "question": "I understand DFS now. But I heard about BFS (breadth-first search) - how is that different? Can you show me how to implement it?",
                "code": "def bfs_traversal(root):\n    # I know I need a queue, but I'm not sure how to use it\n    queue = []\n    queue.append(root)\n    # What next?"
            },
            {
                "turn": 5,
                "question": "Great! Now I understand both DFS and BFS. When would I choose one over the other? Are there specific problems where one is better?",
                "code": "# I can implement both now, but when to use which?\n# DFS:\ndef dfs(root):\n    if root:\n        dfs(root.left)\n        dfs(root.right)\n\n# BFS:\ndef bfs(root):\n    from collections import deque\n    queue = deque([root])\n    while queue:\n        node = queue.popleft()\n        if node:\n            queue.append(node.left)\n            queue.append(node.right)"
            }
        ]
    },
    {
        "conversation_id": "conv_003",
        "title": "Algorithm Optimization - From O(n²) to O(n log n)",
        "description": "Student learns about time complexity and how to optimize algorithms",
        "student_profile": {
            "student_id": "student_algo_001",
            "mastery": 0.55,
            "learning_style": "active",
            "personality": {"openness": 0.7, "neuroticism": 0.4, "conscientiousness": 0.8}
        },
        "conversation": [
            {
                "turn": 1,
                "question": "I wrote a function to find if two numbers in an array sum to a target, but it's really slow for large arrays. Can you help me understand why?",
                "code": "def two_sum(nums, target):\n    for i in range(len(nums)):\n        for j in range(i + 1, len(nums)):\n            if nums[i] + nums[j] == target:\n                return [i, j]\n    return []\n\n# This works but is slow for large arrays\nprint(two_sum([2, 7, 11, 15], 9))"
            },
            {
                "turn": 2,
                "question": "I see - it's O(n²) because of nested loops. I heard about using a hash map to make it faster. Can you help me understand how that works?",
                "code": "def two_sum(nums, target):\n    # I know I should use a dictionary, but how?\n    seen = {}\n    for i, num in enumerate(nums):\n        # What should I check here?\n        pass"
            },
            {
                "turn": 3,
                "question": "That's much faster! Now I'm trying to sort an array. I wrote bubble sort but it's also slow. What's a better way?",
                "code": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n    return arr\n\n# This is O(n²) - is there a faster way?"
            },
            {
                "turn": 4,
                "question": "I learned about merge sort and it's O(n log n). I tried to implement it but I'm getting confused about the merge step. Can you help?",
                "code": "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    \n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    \n    # How do I merge left and right?\n    return []"
            },
            {
                "turn": 5,
                "question": "Perfect! Now I understand merge sort. But when would I use merge sort vs quicksort? Are there trade-offs I should know about?",
                "code": "def merge_sort(arr):\n    # I can implement this now\n    pass\n\ndef quicksort(arr):\n    # I know quicksort exists but when to use which?\n    pass\n\n# What are the differences and trade-offs?"
            }
        ]
    }
]


def run_conversation_test(conversation_data, output_dir):
    """Run a single conversation test and save results"""
    conversation_id = conversation_data["conversation_id"]
    print(f"\n{'='*80}")
    print(f"Running: {conversation_data['title']}")
    print(f"ID: {conversation_id}")
    print(f"{'='*80}\n")
    
    # Create output directory
    conv_dir = os.path.join(output_dir, conversation_id)
    os.makedirs(conv_dir, exist_ok=True)
    
    # Initialize models
    config_path = os.path.join(current_dir, 'config.yaml')
    import yaml
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    dina_model = RealDINAModel(config)
    codebert = RealCodeBERT(config)
    bert = RealBERT(config)
    nestor = RealNestor(config_path)
    time_tracker = TimeTracker()
    
    cse_kg_extractor = None
    if CSEKGConceptExtractor and USE_REAL_MODELS:
        try:
            cse_kg_extractor = CSEKGConceptExtractor(config_path)
        except Exception as e:
            print(f"Warning: CSE-KG extractor not available: {e}")
    
    # Initialize chat interface
    chat = ChatInterface(api_key=groq_api_key)
    
    # Track conversation
    conversation_turns = []
    student_id = conversation_data["student_profile"]["student_id"]
    
    # Process each turn
    for turn_data in conversation_data["conversation"]:
        turn = turn_data["turn"]
        question = turn_data["question"]
        code = turn_data.get("code", "")
        error_message = turn_data.get("error_message", "")
        
        print(f"\n--- Turn {turn} ---")
        print(f"Question: {question[:100]}...")
        if code:
            print(f"Code: {code[:80]}...")
        
        # Start timing
        time_tracker.start_turn(student_id, turn)
        
        # Get response from chat interface
        try:
            response = chat.process_message(
                student_id=student_id,
                message=question,
                code=code if code else None,
                error_message=error_message if error_message else None
            )
            explanation = response.get("explanation", response.get("response", ""))
        except Exception as e:
            print(f"Error getting response: {e}")
            explanation = f"Error processing message: {str(e)}"
        
        # End timing
        duration = time_tracker.end_turn(student_id, turn)
        
        # Calculate metrics
        metrics = calculate_learning_outcome_metrics(
            student_id=student_id,
            turn=turn,
            code=code,
            question=question,
            explanation=explanation,
            error_message=error_message,
            dina_model=dina_model,
            codebert=codebert,
            bert=bert,
            nestor=nestor,
            cse_kg_extractor=cse_kg_extractor,
            behavior_patterns={
                "proactive": turn > 1,
                "help_seeking": "?" in question or "help" in question.lower(),
                "frustrated": any(word in question.lower() for word in ["stuck", "confused", "wrong", "error"])
            }
        )
        
        # Store turn data
        turn_result = {
            "turn": turn,
            "question": question,
            "code": code,
            "error_message": error_message,
            "explanation": explanation,
            "metrics": metrics,
            "response_time": duration
        }
        conversation_turns.append(turn_result)
        
        print(f"✓ Turn {turn} completed (Response time: {duration:.2f}s)")
    
    # Save results
    results_file = os.path.join(conv_dir, "results.json")
    with open(results_file, 'w') as f:
        json.dump({
            "conversation_id": conversation_id,
            "title": conversation_data["title"],
            "description": conversation_data["description"],
            "student_profile": conversation_data["student_profile"],
            "turns": conversation_turns,
            "timestamp": datetime.now().isoformat()
        }, f, indent=2)
    
    # Generate summary
    generate_summary(conversation_data, conversation_turns, conv_dir)
    
    print(f"\n✓ Conversation {conversation_id} completed!")
    print(f"  Results saved to: {conv_dir}")
    
    return conversation_turns


def generate_summary(conversation_data, turns, output_dir):
    """Generate a markdown summary of the conversation"""
    summary_lines = [
        f"# {conversation_data['title']}",
        "",
        f"**Conversation ID**: {conversation_data['conversation_id']}",
        f"**Description**: {conversation_data['description']}",
        "",
        "## Student Profile",
        "",
        f"- **Student ID**: {conversation_data['student_profile']['student_id']}",
        f"- **Initial Mastery**: {conversation_data['student_profile']['mastery']:.1%}",
        f"- **Learning Style**: {conversation_data['student_profile']['learning_style']}",
        "",
        "## Conversation Summary",
        "",
        "### Metrics Overview",
        "",
        "| Turn | Mastery | Code Quality | Explanation Quality | Engagement | Student Type |",
        "|------|---------|--------------|---------------------|------------|--------------|"
    ]
    
    for turn in turns:
        metrics = turn.get("metrics", {})
        mastery = metrics.get("mastery", {}).get("overall", 0) * 100
        code_quality = metrics.get("code_quality", {}).get("overall", 0) * 100
        explanation_quality = metrics.get("explanation_quality", {}).get("overall", 0) * 100
        engagement = metrics.get("engagement", {}).get("overall", 0) * 100
        student_type = metrics.get("student_type", {}).get("type", "unknown")
        
        summary_lines.append(
            f"| Turn {turn['turn']} | {mastery:.1f}% | {code_quality:.1f}% | "
            f"{explanation_quality:.1f}% | {engagement:.1f}% | {student_type} |"
        )
    
    # Add detailed turn information
    summary_lines.extend([
        "",
        "## Detailed Turn Analysis",
        ""
    ])
    
    for turn in turns:
        metrics = turn.get("metrics", {})
        summary_lines.extend([
            f"### Turn {turn['turn']}",
            "",
            f"**Question**: {turn['question']}",
            "",
            "**Code**:",
            "```python",
            turn.get("code", "N/A"),
            "```",
            "",
            f"**Response Time**: {turn.get('response_time', 0):.2f}s",
            "",
            "**Metrics**:",
            f"- Mastery: {metrics.get('mastery', {}).get('overall', 0):.1%}",
            f"- Code Quality: {metrics.get('code_quality', {}).get('overall', 0):.1%}",
            f"- Explanation Quality: {metrics.get('explanation_quality', {}).get('overall', 0):.1%}",
            f"- Engagement: {metrics.get('engagement', {}).get('overall', 0):.1%}",
            "",
            "---",
            ""
        ])
    
    # Write summary
    summary_file = os.path.join(output_dir, "SUMMARY.md")
    with open(summary_file, 'w') as f:
        f.write("\n".join(summary_lines))
    
    print(f"  Summary saved to: {summary_file}")


def main():
    """Run all conversation tests"""
    print("="*80)
    print("Codebase Conversation Tests - feature_test_results_2")
    print("="*80)
    
    # Create output directory
    output_dir = os.path.join(current_dir, "feature_test_results_2")
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nOutput directory: {output_dir}")
    print(f"Total conversations: {len(CODEBASE_CONVERSATIONS)}\n")
    
    # Run each conversation
    all_results = {}
    for conversation in CODEBASE_CONVERSATIONS:
        try:
            results = run_conversation_test(conversation, output_dir)
            all_results[conversation["conversation_id"]] = results
        except Exception as e:
            print(f"\n✗ Error running {conversation['conversation_id']}: {e}")
            import traceback
            traceback.print_exc()
    
    # Generate overall summary
    summary_file = os.path.join(output_dir, "OVERALL_SUMMARY.md")
    with open(summary_file, 'w') as f:
        f.write("# Codebase Conversation Tests - Overall Summary\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write(f"Total Conversations: {len(all_results)}\n\n")
        
        for conv_id, results in all_results.items():
            f.write(f"## {conv_id}\n\n")
            f.write(f"- Turns: {len(results)}\n")
            if results:
                avg_time = sum(t.get('response_time', 0) for t in results) / len(results)
                f.write(f"- Average Response Time: {avg_time:.2f}s\n")
            f.write("\n")
    
    print(f"\n{'='*80}")
    print("All conversation tests completed!")
    print(f"Results saved to: {output_dir}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()









