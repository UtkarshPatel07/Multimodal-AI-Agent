import React, { useRef, useState, useEffect } from 'react'
import './ExplanationDisplay.css'

function ExplanationDisplay({ explanation, audioUrl, onFeedback }) {
  const audioRef = useRef(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [feedbackGiven, setFeedbackGiven] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const speechSynthRef = useRef(null)

  // Initialize speech synthesis
  useEffect(() => {
    if ('speechSynthesis' in window) {
      speechSynthRef.current = window.speechSynthesis
    }
  }, [])

  // Stop speech when component unmounts
  useEffect(() => {
    return () => {
      if (speechSynthRef.current) {
        speechSynthRef.current.cancel()
      }
    }
  }, [])

  const toggleAudio = () => {
    // Use browser's speech synthesis instead of audio file
    if (isSpeaking) {
      // Stop speaking
      if (speechSynthRef.current) {
        speechSynthRef.current.cancel()
        setIsSpeaking(false)
      }
    } else {
      // Start speaking
      if (speechSynthRef.current && explanation) {
        const utterance = new SpeechSynthesisUtterance(explanation)
        
        // Configure voice settings
        utterance.rate = 0.9 // Slightly slower for clarity
        utterance.pitch = 1.0
        utterance.volume = 1.0
        
        // Try to use a good quality voice
        const voices = speechSynthRef.current.getVoices()
        const englishVoice = voices.find(voice => 
          voice.lang.startsWith('en') && voice.name.includes('Google')
        ) || voices.find(voice => voice.lang.startsWith('en'))
        
        if (englishVoice) {
          utterance.voice = englishVoice
        }
        
        utterance.onstart = () => setIsSpeaking(true)
        utterance.onend = () => setIsSpeaking(false)
        utterance.onerror = () => setIsSpeaking(false)
        
        speechSynthRef.current.speak(utterance)
      }
    }
  }

  const handleFeedback = (rating) => {
    onFeedback(rating)
    setFeedbackGiven(true)
    setTimeout(() => setFeedbackGiven(false), 2000)
  }

  return (
    <div className="explanation-display">
      <div className="explanation-header">
        <h3>💡 Explanation</h3>
        <button className="audio-btn" onClick={toggleAudio}>
          {isSpeaking ? '⏸️ Stop Speaking' : '🔊 Read Aloud'}
        </button>
      </div>

      <div className="explanation-text">
        {explanation}
      </div>

      <div className="feedback-section">
        <p>Was this explanation helpful?</p>
        <div className="feedback-buttons">
          <button
            className="feedback-btn"
            onClick={() => handleFeedback('positive')}
            disabled={feedbackGiven}
          >
            👍 Yes
          </button>
          <button
            className="feedback-btn"
            onClick={() => handleFeedback('negative')}
            disabled={feedbackGiven}
          >
            👎 No
          </button>
        </div>
        {feedbackGiven && <p className="feedback-thanks">Thanks for your feedback!</p>}
      </div>
    </div>
  )
}

export default ExplanationDisplay
