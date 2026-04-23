# Local Chat UI - Quick Start

A beautiful, local web interface for the Personalized Learning System that runs entirely on your computer - no cloud hosting needed!

## 🚀 Quick Start

### 1. Run the UI

```bash
python chat_ui_local.py
```

### 2. Open in Browser

The interface will automatically tell you the URL. Usually:
```
http://127.0.0.1:5000
```

Just open this URL in your web browser!

## ✨ Features

- **ChatGPT-like Interface**: Clean, modern chat UI
- **Local Only**: Runs on your computer, no cloud needed
- **Code Input Support**: Click "code:" or type "code:" to add code
- **Real-time Responses**: See responses as they're generated
- **Student Progress**: View your learning progress in the header
- **Beautiful Design**: Modern gradient design with smooth animations

## 🎯 How to Use

1. **Ask Questions**: Type your question in the input box and press Enter or click Send
2. **Add Code**: 
   - Type `code:` in the input box, or
   - Click the code toggle button
   - Paste your code
   - Click "Done"
   - Then ask your question about the code
3. **View Progress**: Your student progress is shown in the header (interactions, mastery)

## 📋 Example Usage

1. **Simple Question**:
   ```
   You: What is recursion?
   Bot: [Personalized explanation...]
   ```

2. **With Code**:
   ```
   You: code:
   [Paste code]
   Done
   You: Why does this fail?
   Bot: [Error-specific feedback...]
   ```

## 🔧 Technical Details

- **Framework**: Flask (lightweight Python web framework)
- **Host**: 127.0.0.1 (localhost only - not accessible from internet)
- **Port**: 5000 (default)
- **Backend**: Uses `chat_interface_simple.py` for processing
- **No Internet Required**: After initial setup, works completely offline (except for Groq API calls)

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## 💡 Tips

- The interface remembers your conversation within the session
- Student progress is saved automatically
- Code formatting is preserved in responses
- The UI is responsive and works on different screen sizes

## 🐛 Troubleshooting

### Port 5000 Already in Use

If you see "Address already in use", you can change the port in `chat_ui_local.py`:

```python
app.run(host='127.0.0.1', port=5001, debug=False)  # Change 5000 to 5001
```

### Browser Won't Connect

1. Make sure the server is running (check terminal)
2. Use the exact URL shown: `http://127.0.0.1:5000`
3. Don't use `https://` - it's `http://` only
4. Try refreshing the page

### No Response

1. Check the terminal for error messages
2. Make sure Groq API key is configured
3. Check your internet connection (needed for Groq API)

Enjoy your local chat interface! 🎉

















