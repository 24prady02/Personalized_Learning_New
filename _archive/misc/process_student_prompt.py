"""
Process Student Prompt Through Complete System
"""

import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import os
# API key should be set via environment variable: set GROQ_API_KEY=your_api_key
if not os.getenv('GROQ_API_KEY'):
    print("[ERROR] GROQ_API_KEY environment variable not set!")
    print("[INFO] Please set it using: set GROQ_API_KEY=your_api_key")
    sys.exit(1)

from intelligent_chat_system import IntelligentChatSystem


def process_prompt():
    """Process the student's prompt"""
    
    # Student's natural message
    student_message = '''
I don't understand how these nodes are actually connected. When I write node1.next = node2, what is physically happening in memory? Is node2 inside node1? How does changing node2.next later affect the chain starting from node1?

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Creating nodes
node1 = Node("Apple")
node2 = Node("Banana")
node3 = Node("Cherry")

# Connecting them
node1.next = node2
node2.next = node3

# This creates: "Apple" -> "Banana" -> "Cherry" -> None
```
    '''
    
    # Initialize system
    api_key = os.getenv('GROQ_API_KEY')
    system = IntelligentChatSystem(api_key)
    
    # Process through complete system
    response = system.chat('student_linked_list', student_message)
    
    print("\n" + "="*80)
    print("✅ PROCESSING COMPLETE!")
    print("="*80)


if __name__ == "__main__":
    process_prompt()















