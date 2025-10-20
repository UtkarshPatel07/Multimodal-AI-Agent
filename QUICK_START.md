# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## Prerequisites

✅ Python 3.9+ installed  
✅ Node.js 18+ installed  
✅ OpenAI API key ready

## Installation (Windows)

### Automated Installation

```bash
# Run the installer
install.bat
```

This will:
- Create Python virtual environment
- Install all backend dependencies
- Install all frontend dependencies
- Create .env file from template

### Manual Installation

```bash
# Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

## Configuration

Edit `backend/.env`:
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

Get your API key from: https://platform.openai.com/api-keys

## Running the App

### Automated Start

```bash
# Run the starter script
start.bat
```

### Manual Start

```bash
# Terminal 1: Backend
cd backend
python app.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

## Access

Open browser: **http://localhost:3000**

## First Test

1. **Upload Image**: Drag any diagram or flowchart
2. **Ask Question**: Type "What is this?" or click 🎤 to speak
3. **Get Explanation**: View text, annotated image, and audio

## Example Queries

- "How does this work?"
- "Explain the flow in this diagram"
- "What is the purpose of each component?"
- "Walk me through this step by step"

## Troubleshooting

### "Module not found"
```bash
cd backend
pip install -r requirements.txt
```

### "Port already in use"
Change port in `backend/.env`:
```env
PORT=5001
```

### "OpenAI API error"
- Check API key is correct
- Verify you have credits
- Check internet connection

### "Microphone not working"
- Allow microphone permissions in browser
- Use HTTPS in production

## Next Steps

- Read full [README.md](README.md) for details
- Check [EXAMPLES.md](EXAMPLES.md) for use cases
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- See [DEPLOYMENT.md](DEPLOYMENT.md) for production setup

## Need Help?

- Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
- Review [TESTING.md](TESTING.md) for testing procedures
- Open an issue on GitHub

## System Requirements

**Minimum:**
- 4GB RAM
- 2 CPU cores
- Internet connection

**Recommended:**
- 8GB+ RAM
- 4+ CPU cores
- Fast internet

## Cost Estimate

OpenAI API usage (approximate):
- Image analysis: $0.01-0.03 per request
- Explanation: $0.02-0.05 per request
- Speech-to-text: $0.006 per minute
- Text-to-speech: $0.015 per 1000 characters

Typical query: **$0.05-0.10**

## Tips for Best Results

1. **Clear Images**: Use high-resolution, well-lit images
2. **Specific Questions**: Ask focused questions
3. **Follow-ups**: Use conversation context for deeper understanding
4. **Voice Input**: Speak clearly in quiet environment

## Common Use Cases

✅ Education: Explain textbook diagrams  
✅ Engineering: Analyze technical drawings  
✅ Science: Understand lab setups  
✅ Business: Interpret charts and flows  
✅ Games: Strategy analysis  

## Features at a Glance

🖼️ **Image Upload**: Drag-and-drop or click  
💬 **Text Input**: Type your questions  
🎤 **Voice Input**: Speak naturally  
🤖 **AI Explanation**: GPT-4o powered  
🎨 **Annotations**: Visual highlights  
🔊 **Audio Output**: Listen to explanations  
👍 **Feedback**: Rate explanations  

## What's Next?

After getting familiar with the basics:
- Try different types of diagrams
- Experiment with complex questions
- Use follow-up queries
- Provide feedback to improve the system

Happy explaining! 🎉
