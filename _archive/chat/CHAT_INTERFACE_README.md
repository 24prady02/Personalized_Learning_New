# 🎓 ChatGPT-like UI Interface for Personalized Learning

A beautiful, interactive web interface for the Personalized Learning System that provides a ChatGPT-like experience for students.

## ✨ Features

- **ChatGPT-like Interface**: Clean, modern chat UI with conversation history
- **Code Input Support**: Paste your code and get personalized feedback
- **Real-time Personalization**: 10 personalization features adapt responses to each student
- **Progress Tracking**: View your learning progress and mastery levels
- **Student Profiles**: Switch between different students or create new ones
- **BKT Integration**: Bayesian Knowledge Tracing tracks your learning state

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Key

Set your Groq API key as an environment variable:

**Windows:**
```cmd
set GROQ_API_KEY=your_api_key_here
```

**Linux/Mac:**
```bash
export GROQ_API_KEY=your_api_key_here
```

Or create a `.env` file:
```
GROQ_API_KEY=your_api_key_here
```

### 3. Launch the Interface

```bash
python chat_interface.py
```

The interface will automatically open in your browser at `http://localhost:7860`

## 📖 How to Use

### Basic Usage

1. **Enter Your Student ID**: Type your name or ID in the "Student ID" field and click "Update Student"
2. **Ask Questions**: Type your question in the chat input box
3. **Share Code** (Optional): Paste your code in the "Your Code" text area
4. **Get Personalized Responses**: The system will analyze your input and provide personalized explanations

### Example Interactions

**Question Only:**
```
Student: "I don't understand recursion. Can you explain it?"
```

**Question + Code:**
```
Student: "Why does my code fail?"

Code:
def find_max(numbers):
    max_num = 0
    for num in numbers:
        if num > max_num:
            max_num = num
    return max_num
```

**Follow-up Questions:**
```
Student: "What if I have negative numbers?"
```

The system remembers your conversation context and adapts accordingly!

## 🎯 Personalization Features

The interface uses 10 personalization features:

1. **Conversation Memory** - Remembers your previous questions
2. **Emotional Intelligence** - Adapts tone based on your emotional state
3. **Learning Style** - Matches your preferred learning approach (visual, conceptual, practical)
4. **Personality-Based** - Adjusts communication style to your personality
5. **Progress-Aware** - Acknowledges your current mastery level
6. **Interest & Context** - Incorporates your interests and context
7. **Format Preferences** - Adapts response format to your preferences
8. **Error-Specific Feedback** - Provides targeted feedback on code errors
9. **Metacognitive Guidance** - Helps you learn how to learn
10. **Adaptive Difficulty** - Adjusts complexity based on your progress

## 📊 Progress Panel

The right sidebar shows:
- **Student ID**: Your current identifier
- **Total Interactions**: Number of conversations
- **Overall Mastery**: Your current mastery percentage
- **Skills**: Breakdown of skills you're learning

## 🔧 Interface Controls

- **Send Button**: Submit your question
- **Clear Conversation**: Reset the chat history
- **Update Student**: Change to a different student profile
- **Refresh Progress**: Update the progress panel

## 🎨 Interface Layout

```
┌─────────────────────────────────────────────────────────┐
│  🎓 Personalized Learning System                        │
├──────────────────────────────┬──────────────────────────┤
│                              │  📊 Your Progress        │
│  Chat Interface              │  - Student ID            │
│  [Conversation History]      │  - Total Interactions    │
│                              │  - Overall Mastery       │
│  Your Question:              │  - Skills                │
│  [Input Box]        [Send]   │                          │
│                              │  Student ID:             │
│  Your Code (Optional):       │  [Input] [Update]        │
│  [Code Editor]               │                          │
│                              │  [Refresh Progress]      │
│  [Clear Conversation]        │                          │
└──────────────────────────────┴──────────────────────────┘
```

## 🐛 Troubleshooting

### Interface Won't Start

1. **Check API Key**: Make sure `GROQ_API_KEY` is set
2. **Check Port**: Port 7860 might be in use. Modify the port in `chat_interface.py`:
   ```python
   demo.launch(server_port=7861)  # Use different port
   ```

### No Response from System

1. **Check Internet Connection**: Groq API requires internet
2. **Check API Key Validity**: Verify your Groq API key is correct
3. **Check Console**: Look for error messages in the terminal

### Enhanced Generator Not Found

If you see "⚠️ Enhanced generator not found", the system will use a simpler response generation. This is fine for basic usage, but for full personalization, ensure `src/orchestrator/enhanced_personalized_generator.py` exists.

## 🔄 Integration with Full System

The chat interface integrates with:
- **BKT (Bayesian Knowledge Tracing)**: Tracks learning state
- **Enhanced Personalized Generator**: Provides 10 personalization features
- **Student State Manager**: Maintains student profiles
- **Code Analysis**: Detects errors and provides feedback

## 📝 Notes

- Conversation history is maintained per session
- Student state is saved automatically after each interaction
- The interface works best with the full system initialized, but can run standalone
- Code analysis works for Python code primarily

## 🚀 Next Steps

- Try asking different types of questions
- Share code snippets to get error-specific feedback
- Check your progress as you learn
- Experiment with different student IDs to see personalization differences

Enjoy your personalized learning experience! 🎉














