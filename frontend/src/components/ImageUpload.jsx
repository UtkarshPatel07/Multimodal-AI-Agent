import React, { useRef } from 'react'
import './ImageUpload.css'

function ImageUpload({ onImageUpload, uploadedImage, annotatedImage, loading }) {
  const fileInputRef = useRef(null)

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      onImageUpload(file)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file && file.type.startsWith('image/')) {
      onImageUpload(file)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
  }

  return (
    <div className="image-upload-container">
      <h2>📸 Upload Image</h2>
      
      {!uploadedImage ? (
        <div
          className="upload-zone"
          onClick={() => fileInputRef.current?.click()}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
        >
          <div className="upload-icon">📁</div>
          <p>Click or drag image here</p>
          <p className="upload-hint">PNG, JPG, or PDF</p>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*,.pdf"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
        </div>
      ) : (
        <div className="image-display">
          <img
            src={annotatedImage || uploadedImage}
            alt="Uploaded diagram"
            className="uploaded-image"
          />
          <button
            className="change-image-btn"
            onClick={() => fileInputRef.current?.click()}
            disabled={loading}
          >
            Change Image
          </button>
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*,.pdf"
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
        </div>
      )}
    </div>
  )
}

export default ImageUpload
