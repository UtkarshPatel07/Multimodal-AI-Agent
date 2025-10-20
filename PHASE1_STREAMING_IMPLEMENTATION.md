# 🎯 Phase 1: Real-Time Streaming Audio Implementation

## Goal
Transform the current request-response voice system into a **real-time streaming voice assistant** with natural turn-taking and low latency.

---

## 🏗️ Architecture Overview

### Current Flow (Request-Response):
```
User clicks button → Records full audio → Uploads → Transcribes → Gets response
```

### New Flow (Streaming):
```
User speaks → Audio chunks stream → Real-time transcription → Immediate response → Streaming TTS
```

---

## 📋 Implementation Steps

### Step 1: WebSocket Server Setup

**File: `backend/websocket_server.py`**

```python
"""
WebSocket server for real-time audio streaming
Handles bidirectional audio communication
"""

import asyncio
import websockets
import json
from services.streaming_audio_service import StreamingAudioService

class VoiceWebSocketServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.audio_service = StreamingAudioService()
        self.active_connections = set()
    
    async def handle_client(self, websocket, path):
        """Handle individual client connection"""
        self.active_connections.add(websocket)
        print(f"Client connected. Total: {len(self.active_connections)}")
        
        try:
            async for message in websocket:
                # Handle different message types
                if isinstance(message, bytes):
                    # Audio data
                    await self.process_audio_chunk(websocket, message)
                else:
                    # Control messages (JSON)
                    await self.handle_control_message(websocket, message)
        
        except websockets.exceptions.ConnectionClosed:
            print("Client disconnected")
        finally:
            self.active_connections.remove(websocket)
    
    async def process_audio_chunk(self, websocket, audio_data):
        """Process incoming audio chunk"""
        # Transcribe chunk
        text = await self.audio_service.transcribe_chunk(audio_data)
        
        if text:
            # Send transcription back
            await websocket.send(json.dumps({
                'type': 'transcription',
                'text': text
            }))
            
            # Generate response if sentence complete
            if self.audio_service.is_sentence_complete(text):
                response = await self.audio_service.generate_response(text)
                
                # Stream TTS audio back
                async for audio_chunk in self.audio_service.text_to_speech_stream(response):
                    await websocket.send(audio_chunk)
    
    async def handle_control_message(self, websocket, message):
        """Handle control messages (start, stop, etc.)"""
        data = json.loads(message)
        
        if data['type'] == 'start_listening':
            await websocket.send(json.dumps({'status': 'listening'}))
        
        elif data['type'] == 'stop_listening':
            await websocket.send(json.dumps({'status': 'stopped'}))
    
    def start(self):
        """Start WebSocket server"""
        print(f"Starting WebSocket server on ws://{self.host}:{self.port}")
        start_server = websockets.serve(self.handle_client, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    server = VoiceWebSocketServer()
    server.start()
```

---

### Step 2: Streaming Audio Service

**File: `backend/services/streaming_audio_service.py`**

```python
"""
Streaming audio processing service
Handles real-time transcription and TTS
"""

import asyncio
import numpy as np
import webrtcvad
from io import BytesIO
import whisper
from queue import Queue
import threading

class StreamingAudioService:
    def __init__(self):
        # Load Whisper model
        print("Loading Whisper model for streaming...")
        self.whisper_model = whisper.load_model("base.en")
        
        # Voice Activity Detection
        self.vad = webrtcvad.Vad(2)  # Aggressiveness: 0-3
        
        # Audio buffer
        self.audio_buffer = []
        self.sample_rate = 16000
        self.chunk_duration = 1.0  # 1 second chunks
        
        # Transcription buffer
        self.transcription_buffer = []
        
        print("✅ Streaming audio service ready")
    
    async def transcribe_chunk(self, audio_data):
        """Transcribe audio chunk in real-time"""
        try:
            # Convert bytes to numpy array
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Check if speech is present (VAD)
            if not self.contains_speech(audio_data):
                return None
            
            # Add to buffer
            self.audio_buffer.append(audio_np)
            
            # Transcribe when buffer is large enough
            if len(self.audio_buffer) >= 2:  # ~2 seconds
                combined_audio = np.concatenate(self.audio_buffer)
                
                # Transcribe
                result = self.whisper_model.transcribe(
                    combined_audio,
                    language='en',
                    fp16=False,
                    verbose=False
                )
                
                text = result['text'].strip()
                
                # Clear buffer
                self.audio_buffer = []
                
                return text
            
            return None
        
        except Exception as e:
            print(f"Transcription error: {e}")
            return None
    
    def contains_speech(self, audio_data):
        """Check if audio contains speech using VAD"""
        try:
            # VAD requires specific frame sizes (10, 20, or 30 ms)
            frame_duration = 30  # ms
            frame_size = int(self.sample_rate * frame_duration / 1000) * 2  # 2 bytes per sample
            
            # Check first frame
            if len(audio_data) >= frame_size:
                frame = audio_data[:frame_size]
                return self.vad.is_speech(frame, self.sample_rate)
            
            return False
        
        except Exception as e:
            # If VAD fails, assume speech is present
            return True
    
    def is_sentence_complete(self, text):
        """Check if transcription is a complete sentence"""
        # Simple heuristic: ends with punctuation
        return text.endswith(('.', '?', '!'))
    
    async def generate_response(self, text):
        """Generate AI response to transcribed text"""
        # TODO: Integrate with Claude or local LLM
        # For now, echo back
        return f"You said: {text}"
    
    async def text_to_speech_stream(self, text):
        """Convert text to speech and stream audio chunks"""
        # TODO: Integrate streaming TTS (Bark, Kokoro)
        # For now, yield placeholder
        yield b"audio_chunk_placeholder"

```

---

### Step 3: Frontend WebSocket Client

**File: `frontend/src/services/websocket.js`**

```javascript
/**
 * WebSocket client for real-time audio streaming
 */

class VoiceWebSocket {
  constructor(url = 'ws://localhost:8765') {
    this.url = url;
    this.ws = null;
    this.isConnected = false;
    this.onTranscription = null;
    this.onAudioChunk = null;
  }

  connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url);
      
      this.ws.onopen = () => {
        console.log('✅ WebSocket connected');
        this.isConnected = true;
        resolve();
      };
      
      this.ws.onmessage = (event) => {
        if (typeof event.data === 'string') {
          // JSON message (transcription, control)
          const data = JSON.parse(event.data);
          
          if (data.type === 'transcription' && this.onTranscription) {
            this.onTranscription(data.text);
          }
        } else {
          // Binary data (audio)
          if (this.onAudioChunk) {
            this.onAudioChunk(event.data);
          }
        }
      };
      
      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        reject(error);
      };
      
      this.ws.onclose = () => {
        console.log('WebSocket disconnected');
        this.isConnected = false;
      };
    });
  }

  sendAudioChunk(audioData) {
    if (this.isConnected && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(audioData);
    }
  }

  sendControl(message) {
    if (this.isConnected && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
}

export default VoiceWebSocket;
```

---

### Step 4: Streaming Voice Chat Component

**File: `frontend/src/components/StreamingVoiceChat.jsx`**

```javascript
import React, { useState, useRef, useEffect } from 'react';
import VoiceWebSocket from '../services/websocket';
import './StreamingVoiceChat.css';

function StreamingVoiceChat() {
  const [isListening, setIsListening] = useState(false);
  const [transcription, setTranscription] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  
  const wsRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioContextRef = useRef(null);
  
  useEffect(() => {
    // Initialize WebSocket
    wsRef.current = new VoiceWebSocket();
    
    wsRef.current.onTranscription = (text) => {
      setTranscription(prev => prev + ' ' + text);
    };
    
    wsRef.current.onAudioChunk = (audioData) => {
      // Play audio response
      playAudioChunk(audioData);
    };
    
    // Connect
    wsRef.current.connect()
      .then(() => setIsConnected(true))
      .catch(err => console.error('Connection failed:', err));
    
    return () => {
      if (wsRef.current) {
        wsRef.current.disconnect();
      }
    };
  }, []);
  
  const startListening = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      
      // Create audio context for processing
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      
      // Create processor for chunking
      const processor = audioContextRef.current.createScriptProcessor(4096, 1, 1);
      
      processor.onaudioprocess = (e) => {
        const inputData = e.inputBuffer.getChannelData(0);
        
        // Convert to Int16Array
        const int16Data = new Int16Array(inputData.length);
        for (let i = 0; i < inputData.length; i++) {
          int16Data[i] = Math.max(-32768, Math.min(32767, inputData[i] * 32768));
        }
        
        // Send chunk to server
        if (wsRef.current && wsRef.current.isConnected) {
          wsRef.current.sendAudioChunk(int16Data.buffer);
        }
      };
      
      source.connect(processor);
      processor.connect(audioContextRef.current.destination);
      
      setIsListening(true);
      wsRef.current.sendControl({ type: 'start_listening' });
      
    } catch (err) {
      console.error('Microphone error:', err);
      alert('Could not access microphone');
    }
  };
  
  const stopListening = () => {
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
    
    setIsListening(false);
    wsRef.current.sendControl({ type: 'stop_listening' });
  };
  
  const playAudioChunk = (audioData) => {
    // TODO: Implement audio playback
    console.log('Playing audio chunk:', audioData.byteLength, 'bytes');
  };
  
  return (
    <div className="streaming-voice-chat">
      <div className="connection-status">
        {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
      </div>
      
      <div className="transcription-display">
        <p>{transcription || 'Start speaking...'}</p>
      </div>
      
      <button
        className={`voice-button ${isListening ? 'listening' : ''}`}
        onClick={isListening ? stopListening : startListening}
        disabled={!isConnected}
      >
        {isListening ? '🎤 Listening...' : '🎤 Start Conversation'}
      </button>
    </div>
  );
}

export default StreamingVoiceChat;
```

---

## 📦 Required Dependencies

### Backend:
```bash
pip install websockets webrtcvad pyaudio numpy
```

### Frontend:
```bash
npm install socket.io-client
```

---

## 🧪 Testing Plan

### Test 1: WebSocket Connection
```bash
# Terminal 1: Start WebSocket server
python backend/websocket_server.py

# Terminal 2: Test connection
python -c "import websockets; import asyncio; asyncio.run(websockets.connect('ws://localhost:8765'))"
```

### Test 2: Audio Streaming
```bash
# Open frontend
npm run dev

# Click "Start Conversation"
# Speak and verify real-time transcription
```

### Test 3: Voice Activity Detection
```bash
# Test VAD accuracy
python backend/test_vad.py
```

---

## 🎯 Success Criteria

- [ ] WebSocket server runs without errors
- [ ] Audio chunks stream in real-time (< 100ms latency)
- [ ] VAD correctly detects speech vs silence
- [ ] Transcription appears within 1-2 seconds
- [ ] No audio dropouts or glitches

---

## 🚀 Next Steps After Phase 1

1. **Optimize latency** - Reduce chunk size, faster models
2. **Add TTS streaming** - Integrate Bark or Kokoro
3. **Implement wake-word** - Phase 2
4. **Add memory** - Phase 3

---

**Ready to implement? Let's start with the WebSocket server!**
