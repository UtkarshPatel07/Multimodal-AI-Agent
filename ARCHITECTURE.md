# 🏗️ System Architecture

## Overview

The Multimodal Explanation System follows a modular, service-oriented architecture with clear separation between frontend, backend, and AI services.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ ImageUpload  │  │ QueryInput   │  │ VoiceRecorder│      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────────────────────────────────────────┐      │
│  │         ExplanationDisplay Component              │      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend API (Flask)                       │
│  ┌──────────────────────────────────────────────────┐      │
│  │              API Routes & Controllers             │      │
│  │  /upload-image  /explain  /speech-to-text        │      │
│  └──────────────────────────────────────────────────┘      │
│                            │                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Vision     │  │   Speech     │  │  Reasoning   │     │
│  │   Service    │  │   Service    │  │   Service    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────────────────────────────────────────┐      │
│  │          Annotation Service                       │      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │ API Calls
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    External AI Services                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   GPT-4o     │  │   Whisper    │  │  OpenAI TTS  │     │
│  │  (Vision +   │  │   (STT)      │  │              │     │
│  │  Reasoning)  │  │              │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend Layer

#### 1. React Application
- **Framework**: React 18 with Vite
- **State Management**: React hooks (useState, useRef)
- **HTTP Client**: Axios
- **Styling**: CSS modules

#### 2. Key Components

**ImageUpload Component**
- Handles drag-and-drop and file selection
- Displays uploaded and annotated images
- Manages image state

**QueryInput Component**
- Text input for user questions
- Form validation
- Submit handling

**VoiceRecorder Component**
- Browser MediaRecorder API integration
- Real-time recording status
- Audio blob creation

**ExplanationDisplay Component**
- Renders AI-generated explanations
- Audio playback controls
- Feedback collection

### Backend Layer

#### 1. Flask API Server
- **Framework**: Flask 3.0
- **CORS**: Flask-CORS for cross-origin requests
- **Session Management**: In-memory (production: Redis)

#### 2. API Endpoints

```python
POST /api/upload-image
- Accepts: multipart/form-data (image file)
- Returns: session_id, preview

POST /api/speech-to-text
- Accepts: multipart/form-data (audio file)
- Returns: transcribed text

POST /api/explain
- Accepts: JSON (session_id, query)
- Returns: explanation, annotated_image, audio

POST /api/feedback
- Accepts: JSON (session_id, rating)
- Returns: confirmation
```

#### 3. Service Layer

**Vision Service** (`vision_service.py`)
- Image preprocessing and analysis
- GPT-4V integration for visual understanding
- OCR using Tesseract (optional)
- Object detection using OpenCV
- Returns structured image description

**Speech Service** (`speech_service.py`)
- Speech-to-Text using OpenAI Whisper
- Text-to-Speech using OpenAI TTS
- Audio format conversion
- Base64 encoding for web delivery

**Reasoning Service** (`reasoning_service.py`)
- Combines vision analysis with user query
- GPT-4o prompt engineering
- Step-by-step explanation generation
- Annotation hint extraction
- Conversation context management

**Annotation Service** (`annotation_service.py`)
- Image overlay generation
- Bounding box drawing
- Label placement
- Color management
- PIL/Pillow image manipulation

### Data Flow

#### 1. Image Upload Flow
```
User → ImageUpload → POST /upload-image → Vision Service → GPT-4V
                                         ↓
                                    Session Storage
```

#### 2. Text Query Flow
```
User → QueryInput → POST /explain → Reasoning Service → GPT-4o
                                   ↓
                              Annotation Service → Annotated Image
                                   ↓
                              Speech Service → Audio
                                   ↓
                              Response to Frontend
```

#### 3. Voice Query Flow
```
User → VoiceRecorder → Audio Blob → POST /speech-to-text → Whisper
                                                           ↓
                                                    Transcribed Text
                                                           ↓
                                                    [Text Query Flow]
```

## Technology Stack

### Frontend
- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Axios**: HTTP client
- **Web APIs**: MediaRecorder, Audio

### Backend
- **Python 3.9+**: Programming language
- **Flask**: Web framework
- **OpenCV**: Computer vision
- **Pillow**: Image processing
- **NumPy**: Numerical operations

### AI Services
- **OpenAI GPT-4o**: Multimodal reasoning
- **OpenAI Whisper**: Speech recognition
- **OpenAI TTS**: Speech synthesis
- **Tesseract**: OCR (optional)

## Design Patterns

### 1. Service Layer Pattern
Each AI capability is encapsulated in a dedicated service class:
- Separation of concerns
- Easy testing and mocking
- Swappable implementations

### 2. Session Management
```python
sessions = {
    'session_id': {
        'image_data': bytes,
        'vision_analysis': dict,
        'conversation_history': list
    }
}
```

### 3. Error Handling
- Try-catch blocks in all services
- Graceful degradation
- User-friendly error messages
- Logging for debugging

### 4. Async Processing (Future)
- Celery for background tasks
- WebSocket for real-time updates
- Queue system for high load

## Security Architecture

### 1. API Security
- CORS configuration
- Rate limiting (production)
- Input validation
- File type verification

### 2. Data Privacy
- Session-based storage (no persistence)
- No logging of sensitive data
- Secure API key management
- HTTPS in production

### 3. Authentication (Future)
- JWT tokens
- OAuth integration
- User accounts
- Role-based access

## Scalability Considerations

### 1. Horizontal Scaling
- Stateless backend design
- Load balancer ready
- Shared session storage (Redis)

### 2. Caching Strategy
- Response caching for identical queries
- Image analysis caching
- CDN for static assets

### 3. Database Integration (Future)
```
PostgreSQL/MongoDB
├── Users
├── Sessions
├── Conversations
└── Feedback
```

### 4. Microservices Evolution
```
API Gateway
├── Vision Service (separate container)
├── Speech Service (separate container)
├── Reasoning Service (separate container)
└── Annotation Service (separate container)
```

## Performance Optimization

### 1. Frontend
- Code splitting
- Lazy loading
- Image optimization
- Debouncing user input

### 2. Backend
- Connection pooling
- Request batching
- Async I/O
- GPU acceleration for CV

### 3. AI Services
- Model caching
- Batch inference
- Streaming responses
- Fallback models

## Monitoring & Observability

### 1. Logging
```python
import logging
logging.info(f"Processing query: {query}")
logging.error(f"Vision service error: {e}")
```

### 2. Metrics
- Request latency
- Error rates
- API usage
- User engagement

### 3. Health Checks
```python
@app.route('/health')
def health_check():
    return {"status": "healthy"}
```

## Future Enhancements

### 1. Real-time Collaboration
- Multiple users on same image
- Shared annotations
- Live explanations

### 2. Advanced Vision
- 3D model support
- Video analysis
- AR annotations

### 3. Personalization
- User preferences
- Learning style adaptation
- Domain-specific models

### 4. Mobile Support
- Native mobile apps
- Camera integration
- Offline mode
