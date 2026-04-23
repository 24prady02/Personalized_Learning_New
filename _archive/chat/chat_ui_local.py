"""
Local Web UI for Personalized Learning Chat
Simple Flask-based interface that runs on localhost only
"""

import os
import sys
from flask import Flask, render_template_string, request, jsonify
from chat_interface_simple import ChatInterface

# Get API key
groq_api_key = os.getenv('GROQ_API_KEY')
if not groq_api_key:
    print("[ERROR] GROQ_API_KEY environment variable not set!")
    print("[INFO] Please set it using: set GROQ_API_KEY=your_api_key")
    sys.exit(1)

# Initialize chat interface
chat = ChatInterface(groq_api_key)

app = Flask(__name__)

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personalized Learning Chat</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container {
            width: 90%;
            max-width: 900px;
            height: 90vh;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 24px;
            margin-bottom: 5px;
        }
        
        .header p {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
        }
        
        .message {
            margin-bottom: 20px;
            display: flex;
            animation: fadeIn 0.3s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message-content {
            max-width: 70%;
            padding: 12px 16px;
            border-radius: 18px;
            word-wrap: break-word;
        }
        
        .message.user .message-content {
            background: #667eea;
            color: white;
            border-bottom-right-radius: 4px;
        }
        
        .message.bot .message-content {
            background: white;
            color: #333;
            border: 1px solid #e0e0e0;
            border-bottom-left-radius: 4px;
        }
        
        .message.bot .message-content pre {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 10px 0;
        }
        
        .input-container {
            padding: 20px;
            background: white;
            border-top: 1px solid #e0e0e0;
        }
        
        .input-wrapper {
            display: flex;
            gap: 10px;
        }
        
        #messageInput {
            flex: 1;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 25px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.3s;
        }
        
        #messageInput:focus {
            border-color: #667eea;
        }
        
        #sendButton {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        #sendButton:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        #sendButton:active {
            transform: translateY(0);
        }
        
        #sendButton:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 10px;
            color: #667eea;
            font-style: italic;
        }
        
        .code-toggle {
            margin-top: 10px;
            padding: 10px;
            background: #f0f0f0;
            border-radius: 8px;
            display: none;
        }
        
        .code-toggle textarea {
            width: 100%;
            min-height: 100px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            resize: vertical;
        }
        
        .code-toggle button {
            margin-top: 5px;
            padding: 5px 15px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        
        .student-info {
            padding: 10px 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
            font-size: 12px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Personalized Learning Chat</h1>
            <p>AI-Powered Programming Tutor</p>
        </div>
        
        <div class="student-info" id="studentInfo">
            Student: <span id="studentName">Student</span> | 
            Interactions: <span id="interactionCount">0</span> | 
            Mastery: <span id="mastery">0%</span>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message bot">
                <div class="message-content">
                    👋 Hello! I'm your personalized learning assistant. Ask me anything about programming, or share your code for feedback!
                </div>
            </div>
        </div>
        
        <div class="loading" id="loading">🤖 Thinking...</div>
        
        <div class="input-container">
            <div class="code-toggle" id="codeToggle">
                <label><strong>Your Code (Optional):</strong></label>
                <textarea id="codeInput" placeholder="Paste your code here..."></textarea>
                <button onclick="toggleCode()">Done</button>
            </div>
            
            <div class="input-wrapper">
                <input 
                    type="text" 
                    id="messageInput" 
                    placeholder="Type your question here... (Type 'code:' to add code)"
                    onkeypress="handleKeyPress(event)"
                >
                <button id="sendButton" onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>
    
    <script>
        let currentCode = null;
        
        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }
        
        function toggleCode() {
            const toggle = document.getElementById('codeToggle');
            const input = document.getElementById('messageInput');
            if (toggle.style.display === 'none' || toggle.style.display === '') {
                toggle.style.display = 'block';
                input.placeholder = 'Type your question about the code...';
            } else {
                currentCode = document.getElementById('codeInput').value;
                toggle.style.display = 'none';
                input.placeholder = 'Type your question here... (Type "code:" to add code)';
            }
        }
        
        function addMessage(text, isUser) {
            const container = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            
            // Format code blocks
            text = text.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
            text = text.replace(/\n/g, '<br>');
            
            contentDiv.innerHTML = text;
            messageDiv.appendChild(contentDiv);
            container.appendChild(messageDiv);
            
            container.scrollTop = container.scrollHeight;
        }
        
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const button = document.getElementById('sendButton');
            const loading = document.getElementById('loading');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Check for code command
            if (message.toLowerCase().startsWith('code:')) {
                toggleCode();
                input.value = '';
                return;
            }
            
            // Add user message
            addMessage(message, true);
            input.value = '';
            button.disabled = true;
            loading.style.display = 'block';
            
            // Get code if available
            const code = currentCode || document.getElementById('codeInput').value || null;
            if (code) {
                currentCode = code;
                document.getElementById('codeInput').value = '';
            }
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        code: code
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    addMessage(data.response, false);
                    updateStudentInfo(data.student_info);
                } else {
                    addMessage('❌ Error: ' + data.error, false);
                }
            } catch (error) {
                addMessage('❌ Error: ' + error.message, false);
            } finally {
                button.disabled = false;
                loading.style.display = 'none';
                currentCode = null;
            }
        }
        
        function updateStudentInfo(info) {
            if (info) {
                document.getElementById('studentName').textContent = info.student_id || 'Student';
                document.getElementById('interactionCount').textContent = info.interactions || 0;
                document.getElementById('mastery').textContent = (info.mastery || 0) + '%';
            }
        }
        
        // Load initial student info
        fetch('/api/student-info')
            .then(r => r.json())
            .then(data => updateStudentInfo(data));
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        code = data.get('code', None)
        
        if not message:
            return jsonify({'success': False, 'error': 'Message is required'})
        
        # Process message
        result = chat.process_message(message, code)
        
        # Get student info
        student_info = chat.get_student_info()
        info_dict = {}
        for line in student_info.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                if 'mastery' in key:
                    info_dict['mastery'] = float(value.replace('%', ''))
                elif 'interactions' in key:
                    info_dict['interactions'] = int(value) if value.isdigit() else 0
                elif 'student' in key:
                    info_dict['student_id'] = value
        
        return jsonify({
            'success': True,
            'response': result['response'],
            'student_info': info_dict
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/student-info', methods=['GET'])
def student_info():
    try:
        info = chat.get_student_info()
        info_dict = {}
        for line in info.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                value = value.strip()
                if 'mastery' in key:
                    info_dict['mastery'] = float(value.replace('%', ''))
                elif 'interactions' in key:
                    info_dict['interactions'] = int(value) if value.isdigit() else 0
                elif 'student' in key:
                    info_dict['student_id'] = value
        
        return jsonify(info_dict)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 Starting Local Chat UI")
    print("="*80)
    print("\n✅ Interface ready!")
    print("🌐 Open your browser and go to: http://127.0.0.1:5000")
    print("\n💡 Press Ctrl+C to stop the server")
    print("="*80 + "\n")
    
    app.run(host='127.0.0.1', port=5000, debug=False)














