import React, { useState, useRef, useEffect } from 'react'
import './MicrophoneTest.css'

function MicrophoneTest() {
  const [isTestingMic, setIsTestingMic] = useState(false)
  const [micLevel, setMicLevel] = useState(0)
  const [devices, setDevices] = useState([])
  const [selectedDevice, setSelectedDevice] = useState('')
  const audioContextRef = useRef(null)
  const analyserRef = useRef(null)
  const streamRef = useRef(null)
  const animationRef = useRef(null)

  useEffect(() => {
    // Get available microphones
    navigator.mediaDevices.enumerateDevices().then(deviceList => {
      const mics = deviceList.filter(device => device.kind === 'audioinput')
      setDevices(mics)
      if (mics.length > 0 && !selectedDevice) {
        setSelectedDevice(mics[0].deviceId)
      }
    })
  }, [selectedDevice])

  const startMicTest = async () => {
    try {
      const constraints = {
        audio: selectedDevice ? { deviceId: selectedDevice } : true
      }
      
      const stream = await navigator.mediaDevices.getUserMedia(constraints)
      streamRef.current = stream
      
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)()
      analyserRef.current = audioContextRef.current.createAnalyser()
      const source = audioContextRef.current.createMediaStreamSource(stream)
      source.connect(analyserRef.current)
      
      analyserRef.current.fftSize = 256
      const bufferLength = analyserRef.current.frequencyBinCount
      const dataArray = new Uint8Array(bufferLength)
      
      setIsTestingMic(true)
      
      const updateLevel = () => {
        analyserRef.current.getByteFrequencyData(dataArray)
        const average = dataArray.reduce((a, b) => a + b) / bufferLength
        setMicLevel(Math.round(average))
        animationRef.current = requestAnimationFrame(updateLevel)
      }
      
      updateLevel()
    } catch (err) {
      alert('Could not access microphone: ' + err.message)
    }
  }

  const stopMicTest = () => {
    if (animationRef.current) {
      cancelAnimationFrame(animationRef.current)
    }
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop())
    }
    if (audioContextRef.current) {
      audioContextRef.current.close()
    }
    setIsTestingMic(false)
    setMicLevel(0)
  }

  return (
    <div className="mic-test-container">
      <h3>🎤 Microphone Test</h3>
      
      <div className="mic-select">
        <label>Select Microphone:</label>
        <select 
          value={selectedDevice} 
          onChange={(e) => setSelectedDevice(e.target.value)}
          disabled={isTestingMic}
        >
          {devices.map(device => (
            <option key={device.deviceId} value={device.deviceId}>
              {device.label || `Microphone ${device.deviceId.slice(0, 8)}`}
            </option>
          ))}
        </select>
      </div>

      <button 
        className={`test-btn ${isTestingMic ? 'testing' : ''}`}
        onClick={isTestingMic ? stopMicTest : startMicTest}
      >
        {isTestingMic ? '⏹️ Stop Test' : '▶️ Test Microphone'}
      </button>

      {isTestingMic && (
        <div className="mic-level-container">
          <p>Speak into your microphone:</p>
          <div className="mic-level-bar">
            <div 
              className="mic-level-fill" 
              style={{ width: `${Math.min(micLevel * 2, 100)}%` }}
            />
          </div>
          <p className="mic-level-text">
            Level: {micLevel} {micLevel > 10 ? '✅ Good!' : '⚠️ Too quiet!'}
          </p>
          {micLevel < 10 && (
            <p className="mic-warning">
              ⚠️ Microphone is too quiet! Please:
              <br/>• Speak louder
              <br/>• Move closer to microphone
              <br/>• Check system microphone volume
              <br/>• Try a different microphone
            </p>
          )}
        </div>
      )}
    </div>
  )
}

export default MicrophoneTest
