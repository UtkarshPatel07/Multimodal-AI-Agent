"""
Streaming Audio Service - Real-time voice processing
Handles streaming transcription and TTS without database
"""

import asyncio
import numpy as np
import webrtcvad
import whisper
from io import BytesIO
import wave
import tempfile
import os

class StreamingAudioService:
    def __init__(self):
        print("🎤 Initializing Streaming Audio Service...")
        
        # Load Whisper model for streaming
        self.whisper_model = whisper.load_model("base.en")
        
        # Voice Activity Detection
        self.vad = webrtcvad.Vad(2)  # Aggressiveness: 0-3
        
        # Audio buffer for accumulating chunks
        self.audio_buffer = []
        self.sample_rate = 16000
        
        # Conversation context (in-memory, no database)
        self.conversation_history = []
        self.max_history = 10  # Keep last 10 exchanges
        
        print("✅ Streaming Audio Service ready")
    
    async def transcribe_chunk(self, audio_data):
        """
        Transcribe audio chunk in real-time
        Returns text if speech detected, None otherwise
        """
        try:
            # Convert bytes to numpy array
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Check if speech is present using VAD
            if not self.contains_speech(audio_data):
                return None
            
            # Add to buffer
            self.audio_buffer.append(audio_np)
            
            # Transcribe when buffer has enough audio (~2 seconds)
            if len(self.audio_buffer) >= 2:
                combined_audio = np.concatenate(self.audio_buffer)
                
                # Transcribe with Whisper
                result = self.whisper_model.transcribe(
                    combined_audio,
                    language='en',
                    fp16=False,
                    verbose=False
                )
                
                text = result['text'].strip()
                
                # Clear buffer after transcription
                self.audio_buffer = []
                
                if text:
                    print(f"📝 Transcribed: {text}")
                    return text
            
            return None
        
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            return None
    
    def contains_speech(self, audio_data):
        """Check if audio contains speech using VAD"""
        try:
            # VAD requires specific frame sizes (10, 20, or 30 ms)
            frame_duration = 30  # ms
            frame_size = int(self.sample_rate * frame_duration / 1000) * 2  # 2 bytes per sample
            
            # Check if frame has speech
            if len(audio_data) >= frame_size:
                frame = audio_data[:frame_size]
                return self.vad.is_speech(frame, self.sample_rate)
            
            return False
        
        except Exception as e:
            # If VAD fails, assume speech is present
            return True
    
    def is_sentence_complete(self, text):
        """Check if transcription is a complete sentence"""
        # Simple heuristic: ends with punctuation or question mark
        return text.endswith(('.', '?', '!')) or len(text.split()) > 5
    
    def add_to_history(self, role, content):
        """Add message to conversation history (in-memory)"""
        self.conversation_history.append({
            'role': role,
            'content': content
        })
        
        # Keep only recent history
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]
    
    def get_context_prompt(self):
        """Get conversation context for Claude"""
        if not self.conversation_history:
            return ""
        
        # Format recent history for context
        context = "\n\nConversation history (remember this context):\n"
        for msg in self.conversation_history[-10:]:  # Last 5 exchanges
            role = "User" if msg['role'] == 'user' else "Assistant"
            context += f"{role}: {msg['content']}\n"
        
        context += "\nRemember the above conversation and maintain context in your responses.\n"
        return context
    
    def get_conversation_summary(self):
        """Get a summary of the conversation for display"""
        if not self.conversation_history:
            return "No conversation yet"
        
        summary = []
        for msg in self.conversation_history[-6:]:
            role = "You" if msg['role'] == 'user' else "AI"
            summary.append(f"{role}: {msg['content'][:100]}...")
        
        return "\n".join(summary)
    
    def clear_buffer(self):
        """Clear audio buffer"""
        self.audio_buffer = []
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        print("🔄 Conversation reset")
