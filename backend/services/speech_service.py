import os
import base64
from io import BytesIO
import whisper
import torch
import soundfile as sf
from pydub import AudioSegment
import tempfile
import numpy as np

class SpeechService:
    def __init__(self):
        print("🎤 Initializing Whisper speech recognition...")
        # Load Whisper model (using 'base' for good balance of speed and accuracy)
        # Options: tiny, base, small, medium, large
        try:
            self.whisper_model = whisper.load_model("base")
            print("✅ Whisper model loaded successfully!")
        except Exception as e:
            print(f"⚠️ Could not load Whisper model: {e}")
            self.whisper_model = None
    
    def transcribe_audio(self, audio_data):
        """Convert speech to text using Whisper AI"""
        try:
            if not self.whisper_model:
                raise Exception("Whisper model not loaded")
            
            print(f"🎤 Received audio data: {len(audio_data)} bytes")
            
            # Save audio data to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_audio:
                temp_audio.write(audio_data)
                temp_audio_path = temp_audio.name
            
            print(f"💾 Saved to temp file: {temp_audio_path}")
            
            try:
                # Convert webm to wav using pydub
                audio = AudioSegment.from_file(temp_audio_path)
                
                # Convert to wav
                wav_path = temp_audio_path.replace('.webm', '.wav')
                audio.export(wav_path, format='wav')
                print(f"🔄 Converted to WAV: {wav_path}")
                
                # Transcribe using Whisper
                print("🎯 Transcribing with Whisper...")
                result = self.whisper_model.transcribe(
                    wav_path,
                    language='en',
                    fp16=False,  # Use FP32 for CPU
                    verbose=False
                )
                
                transcribed_text = result['text'].strip()
                print(f"✅ Transcription: '{transcribed_text}'")
                
                # Clean up temp files
                try:
                    os.unlink(temp_audio_path)
                    os.unlink(wav_path)
                except:
                    pass
                
                if not transcribed_text:
                    raise Exception("No speech detected in audio")
                
                return transcribed_text
                
            except Exception as e:
                print(f"❌ Transcription error: {e}")
                # Clean up on error
                try:
                    os.unlink(temp_audio_path)
                    if os.path.exists(wav_path):
                        os.unlink(wav_path)
                except:
                    pass
                raise Exception(f"Failed to transcribe: {str(e)}")
            
        except Exception as e:
            print(f"❌ Speech-to-text error: {e}")
            raise Exception(f"Failed to transcribe audio: {str(e)}")
    
    def text_to_speech(self, text):
        """Convert text to speech - using browser Web Speech API"""
        try:
            # Browser handles TTS
            print("🔊 Text-to-speech: Using browser-side TTS")
            return ""
            
        except Exception as e:
            print(f"Text-to-speech error: {e}")
            return ""
