# 🎯 Multimodal Explanation System (Voice + Image)

A production-ready AI-powered system that accepts images/diagrams and user queries (text or voice) to generate comprehensive explanations with annotated visuals and speech output.

## 🌟 Features

- **Image Upload & Analysis**: Upload diagrams, charts, flowcharts, or any visual content
- **Multimodal Input**: Ask questions via text or voice (speech-to-text)
- **AI-Powered Reasoning**: Uses GPT-4o for intelligent visual understanding and explanation
- **Annotated Visuals**: Highlights key elements in the image with bounding boxes and labels
- **Voice Output**: Text-to-speech for hands-free learning
- **Interactive UI**: Clean, responsive web interface
- **Follow-up Questions**: Maintain conversation context for deeper exploration

## 🏗️ Architecture

### Backend (Python/Flask)
- **Vision Service**: Image analysis using GPT-4V, OCR, and object detection
- **Speech Service**: Whisper for STT, OpenAI TTS for speech output
- **Reasoning Service**: GPT-4o for generating step-by-step explanations
- **Annotation Service**: Creates visual overlays with highlights and labels

### Frontend (React/Vite)
- Modern React UI with component-based architecture
- Real-time audio recording and playback
- Drag-and-drop image upload
- Responsive design for all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- OpenAI API key

### Installation

1. **Clone and navigate to the project**
```bash
cd "Multimodal AI Agent"
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure Environment**
Create `backend/.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
PORT=5000
```

4. **Frontend Setup**
```bash
cd frontend
npm install
```

### Running the Application

**Option 1: Run both services together (from root)**
```bash
npm run dev
```

**Option 2: Run separately**

Terminal 1 (Backend):
```bash
cd backend
python app.py
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

Access the app at: `http://localhost:3000`

## 📖 Usage

1. **Upload an Image**: Click or drag-and-drop a diagram, chart, or image
2. **Ask a Question**: 
   - Type your question in the text area, OR
   - Click "Press to Speak" and ask verbally
3. **Get Explanation**: 
   - Read the AI-generated explanation
   - View annotated image with highlights
   - Listen to the audio explanation
4. **Follow-up**: Ask additional questions about the same image

## 🎓 Example Use Cases

- **Education**: Explain physics diagrams, chemistry structures, math graphs
- **Engineering**: Analyze circuit diagrams, flowcharts, system architectures
- **Games**: Understand strategy board positions (chess, Go, etc.)
- **Data Visualization**: Interpret charts, maps, and infographics
- **Accessibility**: Voice-based learning for visual content

## 🛠️ Technology Stack

- **AI Models**: OpenAI GPT-4o, Whisper, TTS
- **Backend**: Flask, Python, OpenCV, Pillow
- **Frontend**: React, Vite, Axios
- **Vision**: GPT-4V, Tesseract OCR, OpenCV
- **Speech**: OpenAI Whisper & TTS

## 📁 Project Structure

```
Multimodal AI Agent/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment template
│   └── services/
│       ├── vision_service.py      # Image analysis
│       ├── speech_service.py      # STT/TTS
│       ├── reasoning_service.py   # LLM reasoning
│       └── annotation_service.py  # Visual annotations
├── frontend/
│   ├── src/
│   │   ├── App.jsx           # Main application
│   │   ├── components/       # React components
│   │   └── *.css            # Styling
│   ├── package.json
│   └── vite.config.js
├── package.json              # Root package
└── README.md
```

## 🔒 Security & Privacy

- User-uploaded images are stored in memory only (session-based)
- No data persistence without explicit consent
- HTTPS recommended for production
- API keys stored securely in environment variables

## 🚀 Deployment

### Production Considerations
- Use production WSGI server (Gunicorn/uWSGI)
- Enable CORS properly for your domain
- Use Redis/database for session management
- Deploy on cloud platforms (AWS, GCP, Azure)
- Enable GPU instances for faster inference
- Implement rate limiting and caching

## 📊 Performance

- Target response time: < 5 seconds
- Supports concurrent users via scalable backend
- Optimized model inference with caching

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Additional vision models (Gemini, Claude)
- Multi-language support
- Video/animation support
- Mobile app version
- Fine-tuning on domain-specific data

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Built following the comprehensive product vision document for multimodal AI explanation systems, incorporating state-of-the-art models and best practices in explainable AI.
