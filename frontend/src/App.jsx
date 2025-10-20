import React, { useState, useRef } from 'react'
import axios from 'axios'
import './App.css'

// Configure axios base URL for production
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'
axios.defaults.baseURL = API_URL
import ImageUpload from './components/ImageUpload'
import QueryInput from './components/QueryInput'
import ExplanationDisplay from './components/ExplanationDisplay'
import VoiceRecorder from './components/VoiceRecorder'
import MicrophoneTest from './components/MicrophoneTest'
import StreamingVoiceChat from './components/StreamingVoiceChat'

function App() {
  const [mode, setMode] = useState('standard') // 'standard' or 'streaming'
  const [sessionId, setSessionId] = useState(null)
  const [uploadedImage, setUploadedImage] = useState(null)
  const [annotatedImage, setAnnotatedImage] = useState(null)
  const [explanation, setExplanation] = useState('')
  const [audioUrl, setAudioUrl] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleImageUpload = async (file) => {
    try {
      setLoading(true)
      setError(null)
      
      console.log('Uploading file:', file.name, file.type, file.size)
      
      const formData = new FormData()
      formData.append('image', file)
      if (sessionId) {
        formData.append('session_id', sessionId)
      }

      console.log('Sending request to /api/upload-image')
      const response = await axios.post('/api/upload-image', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      console.log('Upload response:', response.data)
      setSessionId(response.data.session_id)
      setUploadedImage(URL.createObjectURL(file))
      setAnnotatedImage(null)
      setExplanation('')
      setAudioUrl(null)
      
      // Clear the query input
      const textarea = document.querySelector('.query-textarea')
      if (textarea) {
        textarea.value = ''
      }
      
    } catch (err) {
      console.error('Upload error:', err)
      console.error('Error response:', err.response)
      setError(err.response?.data?.error || err.message || 'Failed to upload image')
    } finally {
      setLoading(false)
    }
  }

  const handleQuerySubmit = async (query) => {
    if (!sessionId) {
      setError('Please upload an image first')
      return
    }

    try {
      setLoading(true)
      setError(null)

      const response = await axios.post('/api/explain', {
        session_id: sessionId,
        query: query
      })

      setExplanation(response.data.explanation)
      setAnnotatedImage(response.data.annotated_image)
      setAudioUrl(response.data.audio)
      
      // Don't auto-play - let user click "Read Aloud" button
      
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate explanation')
    } finally {
      setLoading(false)
    }
  }

  const handleVoiceQuery = async (audioBlob) => {
    if (!sessionId) {
      setError('Please upload an image first')
      return
    }

    try {
      setLoading(true)
      setError(null)
      console.log('Voice query received, sending to server...')
      
      // Send audio to backend for Whisper transcription
      const formData = new FormData()
      formData.append('audio', audioBlob, 'audio.webm')
      
      console.log('📤 Sending audio to Whisper...')
      const transcribeResponse = await axios.post('/api/speech-to-text', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      
      const transcribedText = transcribeResponse.data.text
      console.log('✅ Whisper transcribed:', transcribedText)
      
      // Update query box with transcribed text
      const textarea = document.querySelector('.query-textarea')
      if (textarea) {
        textarea.value = transcribedText
      }
      
      // Submit the transcribed text as a query
      await handleQuerySubmit(transcribedText)
      
    } catch (err) {
      console.error('Voice query error:', err)
      setError(err.response?.data?.error || 'Failed to process voice query')
      setLoading(false)
    }
  }

  const handleFeedback = async (rating) => {
    try {
      await axios.post('/api/feedback', {
        session_id: sessionId,
        rating: rating
      })
    } catch (err) {
      console.error('Failed to submit feedback:', err)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎯 Multimodal Explanation System</h1>
        <p>Upload an image, ask a question (text or voice), and get an AI-powered explanation</p>
        
        <div className="mode-switcher">
          <button 
            className={`mode-btn ${mode === 'standard' ? 'active' : ''}`}
            onClick={() => setMode('standard')}
          >
            📝 Standard Mode
          </button>
          <button 
            className={`mode-btn ${mode === 'streaming' ? 'active' : ''}`}
            onClick={() => setMode('streaming')}
          >
            🎤 Streaming Voice Chat (NEW!)
          </button>
        </div>
      </header>

      <main className="app-main">
        {error && (
          <div className="error-banner">
            <span>⚠️ {error}</span>
            <button onClick={() => setError(null)}>✕</button>
          </div>
        )}
        
        {mode === 'streaming' ? (
          <StreamingVoiceChat currentImage={uploadedImage} />
        ) : (

        <div className="content-grid">
          <div className="left-panel">
            <ImageUpload 
              onImageUpload={handleImageUpload}
              uploadedImage={uploadedImage}
              annotatedImage={annotatedImage}
              loading={loading}
            />
          </div>

          <div className="right-panel">
            <div className="query-section">
            <h2>Ask a Question</h2>
            
            {/* Microphone Test Tool */}
            <MicrophoneTest />
            
            <QueryInput 
              onSubmit={handleQuerySubmit}
              disabled={!sessionId || loading}
            />
            <div className="voice-section">
              <p>Or use voice:</p>
              <VoiceRecorder 
                onRecordingComplete={handleVoiceQuery}
                disabled={!sessionId || loading}
                onTranscriptChange={(text) => {
                  // Update query input with voice transcript in real-time
                  const textarea = document.querySelector('.query-textarea')
                  if (textarea) {
                    textarea.value = text
                  }
                }}
              />
            </div>
          </div>

            {loading && (
              <div className="loading-indicator">
                <div className="spinner"></div>
                <p>Analyzing and generating explanation...</p>
              </div>
            )}

            {explanation && (
              <ExplanationDisplay 
                explanation={explanation}
                audioUrl={audioUrl}
                onFeedback={handleFeedback}
              />
            )}
          </div>
        </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Powered by Claude 3 Haiku, Whisper AI, and advanced vision models</p>
      </footer>
    </div>
  )
}

export default App
