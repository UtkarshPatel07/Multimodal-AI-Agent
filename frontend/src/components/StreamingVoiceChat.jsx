import React, { useState, useRef, useEffect } from 'react';
import './StreamingVoiceChat.css';

function StreamingVoiceChat({ currentImage }) {
  const [isConnected, setIsConnected] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [transcription, setTranscription] = useState('');
  const [response, setResponse] = useState('');
  const [conversationHistory, setConversationHistory] = useState([]);
  const [status, setStatus] = useState('Disconnected');
  
  const wsRef = useRef(null);
  const audioContextRef = useRef(null);
  const processorRef = useRef(null);
  const streamRef = useRef(null);
  
  // Connect to WebSocket on mount
  useEffect(() => {
    connectWebSocket();
    
    return () => {
      disconnectWebSocket();
    };
  }, []);
  
  // Send image when it changes
  useEffect(() => {
    if (isConnected && currentImage && wsRef.current) {
      // Convert image to base64 and send
      const reader = new FileReader();
      reader.onload = () => {
        wsRef.current.send(JSON.stringify({
          type: 'upload_image',
          image: reader.result
        }));
      };
      reader.readAsDataURL(currentImage);
    }
  }, [currentImage, isConnected]);
  
  const connectWebSocket = () => {
    try {
      const ws = new WebSocket('ws://localhost:8765');
      
      ws.onopen = () => {
        console.log('✅ WebSocket connected');
        setIsConnected(true);
        setStatus('Connected');
        wsRef.current = ws;
      };
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
      };
      
      ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
        setStatus('Error');
      };
      
      ws.onclose = () => {
        console.log('❌ WebSocket disconnected');
        setIsConnected(false);
        setStatus('Disconnected');
        
        // Try to reconnect after 3 seconds
        setTimeout(connectWebSocket, 3000);
      };
      
    } catch (error) {
      console.error('Connection error:', error);
      setStatus('Connection Failed');
    }
  };
  
  const disconnectWebSocket = () => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
    
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
  };
  
  const handleWebSocketMessage = (data) => {
    switch (data.type) {
      case 'transcription':
        setTranscription(data.text);
        if (!data.partial) {
          // Add to history
          addToHistory('user', data.text);
        }
        break;
      
      case 'response':
        setResponse(data.text);
        addToHistory('assistant', data.text);
        setTranscription(''); // Clear transcription
        
        // Speak response
        speakText(data.text);
        break;
      
      case 'status':
        setStatus(data.status);
        break;
      
      case 'error':
        console.error('Server error:', data.message);
        alert(`Error: ${data.message}`);
        break;
      
      case 'history':
        // Update conversation history
        if (data.full_history) {
          setConversationHistory(data.full_history);
        }
        break;
      
      default:
        console.log('Unknown message type:', data.type);
    }
  };
  
  const addToHistory = (role, content) => {
    setConversationHistory(prev => [
      ...prev,
      { role, content, timestamp: new Date().toISOString() }
    ]);
  };
  
  const startListening = async () => {
    try {
      // Get microphone access
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
          sampleRate: 16000
        }
      });
      
      streamRef.current = stream;
      
      // Create audio context
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)({
        sampleRate: 16000
      });
      
      const source = audioContextRef.current.createMediaStreamSource(stream);
      
      // Create processor for chunking audio
      const processor = audioContextRef.current.createScriptProcessor(4096, 1, 1);
      processorRef.current = processor;
      
      processor.onaudioprocess = (e) => {
        if (!isListening || !wsRef.current) return;
        
        const inputData = e.inputBuffer.getChannelData(0);
        
        // Convert to Int16Array for server
        const int16Data = new Int16Array(inputData.length);
        for (let i = 0; i < inputData.length; i++) {
          int16Data[i] = Math.max(-32768, Math.min(32767, inputData[i] * 32768));
        }
        
        // Send audio chunk to server
        if (wsRef.current.readyState === WebSocket.OPEN) {
          wsRef.current.send(int16Data.buffer);
        }
      };
      
      source.connect(processor);
      processor.connect(audioContextRef.current.destination);
      
      // Tell server to start listening
      wsRef.current.send(JSON.stringify({ type: 'start_listening' }));
      
      setIsListening(true);
      setStatus('Listening...');
      
    } catch (err) {
      console.error('Microphone error:', err);
      alert('Could not access microphone. Please check permissions.');
    }
  };
  
  const stopListening = () => {
    // Tell server to stop
    if (wsRef.current) {
      wsRef.current.send(JSON.stringify({ type: 'stop_listening' }));
    }
    
    // Stop audio processing
    if (processorRef.current) {
      processorRef.current.disconnect();
    }
    
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    
    if (audioContextRef.current) {
      audioContextRef.current.close();
    }
    
    setIsListening(false);
    setStatus('Connected');
  };
  
  const speakText = (text) => {
    // Use browser text-to-speech
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1.0;
      utterance.pitch = 1.0;
      utterance.volume = 1.0;
      window.speechSynthesis.speak(utterance);
    }
  };
  
  const resetConversation = () => {
    if (wsRef.current) {
      wsRef.current.send(JSON.stringify({ type: 'reset_conversation' }));
    }
    setConversationHistory([]);
    setTranscription('');
    setResponse('');
  };
  
  return (
    <div className="streaming-voice-chat">
      <div className="chat-header">
        <h2>🎤 Voice Assistant</h2>
        <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
          {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
        </div>
      </div>
      
      <div className="conversation-display">
        <div className="conversation-history">
          <h3>💬 Conversation History</h3>
          {conversationHistory.length === 0 ? (
            <p className="empty-history">No conversation yet. Start speaking!</p>
          ) : (
            <div className="history-list">
              {conversationHistory.map((msg, idx) => (
                <div key={idx} className={`message ${msg.role}`}>
                  <span className="role">{msg.role === 'user' ? '👤 You' : '🤖 AI'}:</span>
                  <span className="content">{msg.content}</span>
                </div>
              ))}
            </div>
          )}
        </div>
        
        <div className="current-interaction">
          {transcription && (
            <div className="transcription-box">
              <strong>🎤 You're saying:</strong>
              <p>{transcription}</p>
            </div>
          )}
          
          {response && (
            <div className="response-box">
              <strong>🤖 AI Response:</strong>
              <p>{response}</p>
            </div>
          )}
        </div>
      </div>
      
      <div className="controls">
        <button
          className={`voice-button ${isListening ? 'listening' : ''}`}
          onClick={isListening ? stopListening : startListening}
          disabled={!isConnected}
        >
          {isListening ? (
            <>
              <span className="pulse"></span>
              🎤 Listening... (Click to stop)
            </>
          ) : (
            '🎤 Start Voice Conversation'
          )}
        </button>
        
        <button
          className="reset-button"
          onClick={resetConversation}
          disabled={!isConnected || conversationHistory.length === 0}
        >
          🔄 Reset Conversation
        </button>
      </div>
      
      <div className="status-bar">
        <span>Status: {status}</span>
        {currentImage && <span>📷 Image loaded</span>}
      </div>
    </div>
  );
}

export default StreamingVoiceChat;
