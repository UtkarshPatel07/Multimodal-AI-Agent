import React, { useState, useRef } from 'react'
import './VoiceRecorder.css'

function VoiceRecorder({ onRecordingComplete, disabled }) {
  const [isRecording, setIsRecording] = useState(false)
  const [recordingTime, setRecordingTime] = useState(0)
  const mediaRecorderRef = useRef(null)
  const chunksRef = useRef([])
  const timerRef = useRef(null)

  const startRecording = async () => {
    try {
      console.log('🎤 Requesting microphone access...')
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        } 
      })
      
      console.log('✅ Microphone access granted')
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      chunksRef.current = []
      
      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data)
          console.log('📦 Audio chunk received:', e.data.size, 'bytes')
        }
      }
      
      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
        console.log('🎤 Recording complete! Blob size:', blob.size, 'bytes')
        
        if (blob.size > 0) {
          onRecordingComplete(blob)
        } else {
          alert('No audio recorded. Please try again.')
        }
        
        stream.getTracks().forEach(track => track.stop())
        setRecordingTime(0)
        if (timerRef.current) {
          clearInterval(timerRef.current)
        }
      }
      
      mediaRecorder.start()
      setIsRecording(true)
      
      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1)
      }, 1000)
      
      console.log('🔴 Recording started - speak now!')
      
    } catch (err) {
      console.error('❌ Microphone error:', err)
      alert('Could not access microphone.\n\nPlease:\n1. Allow microphone access\n2. Check microphone is connected\n3. Try again')
    }
  }
  
  const stopRecording = () => {
    console.log('⏹️ Stopping recording...')
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      if (timerRef.current) {
        clearInterval(timerRef.current)
      }
    }
  }
  
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div className="voice-recorder">
      <button
        className={`record-btn ${isRecording ? 'recording' : ''}`}
        onClick={isRecording ? stopRecording : startRecording}
        disabled={disabled}
      >
        {isRecording ? (
          <>
            <span className="pulse"></span>
            🎤 Stop Recording ({formatTime(recordingTime)})
          </>
        ) : (
          '🎤 Press to Speak'
        )}
      </button>
      {isRecording && (
        <div className="recording-status">
          <p className="recording-hint">
            🔴 Recording... Speak clearly into your microphone
          </p>
          <p className="recording-hint" style={{fontSize: '0.9rem', color: 'rgba(255,255,255,0.7)'}}>
            Click "Stop Recording" when done (or record for up to 30 seconds)
          </p>
        </div>
      )}
    </div>
  )
}

export default VoiceRecorder
