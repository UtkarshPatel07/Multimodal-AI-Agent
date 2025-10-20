"""
Wake Word Detection Service
Listens for "Hey Assistant" or custom wake word
Uses lightweight model for always-on listening
"""

import numpy as np
import threading
import time
from collections import deque

class WakeWordService:
    def __init__(self, wake_word="hey assistant"):
        self.wake_word = wake_word.lower()
        self.is_listening = False
        self.callback = None
        
        # Simple energy-based detection (can be upgraded to Porcupine later)
        self.energy_threshold = 500
        self.audio_buffer = deque(maxlen=100)  # Keep last 100 chunks
        
        print(f"🎤 Wake Word Service initialized: '{wake_word}'")
    
    def start_listening(self, callback):
        """
        Start listening for wake word
        callback: function to call when wake word detected
        """
        self.callback = callback
        self.is_listening = True
        print(f"👂 Listening for wake word: '{self.wake_word}'")
    
    def stop_listening(self):
        """Stop listening for wake word"""
        self.is_listening = False
        print("⏹️ Wake word detection stopped")
    
    def process_audio_chunk(self, audio_data):
        """
        Process audio chunk for wake word detection
        Returns True if wake word detected
        """
        if not self.is_listening:
            return False
        
        try:
            # Convert to numpy array
            audio_np = np.frombuffer(audio_data, dtype=np.int16)
            
            # Calculate energy (simple voice activity)
            energy = np.abs(audio_np).mean()
            
            # Add to buffer
            self.audio_buffer.append(energy)
            
            # Check if energy spike (potential speech)
            if energy > self.energy_threshold:
                # Check recent energy pattern
                recent_energy = list(self.audio_buffer)[-10:]
                avg_energy = np.mean(recent_energy)
                
                # If sustained energy, likely wake word
                if avg_energy > self.energy_threshold * 0.7:
                    print(f"🔔 Wake word detected! (energy: {energy:.0f})")
                    
                    if self.callback:
                        self.callback()
                    
                    # Reset buffer to avoid repeated triggers
                    self.audio_buffer.clear()
                    return True
            
            return False
        
        except Exception as e:
            print(f"❌ Wake word detection error: {e}")
            return False
    
    def set_sensitivity(self, sensitivity):
        """
        Set detection sensitivity (0.0 to 1.0)
        Higher = more sensitive (more false positives)
        Lower = less sensitive (might miss wake word)
        """
        # Adjust threshold based on sensitivity
        base_threshold = 500
        self.energy_threshold = base_threshold * (1.0 - sensitivity * 0.5)
        print(f"🎚️ Sensitivity set to {sensitivity:.2f} (threshold: {self.energy_threshold:.0f})")

# Note: For production, upgrade to Porcupine or custom trained model
# This is a simple energy-based detector for demo purposes
