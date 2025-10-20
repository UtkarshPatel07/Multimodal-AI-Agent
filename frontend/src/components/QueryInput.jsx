import React, { useState } from 'react'
import './QueryInput.css'

function QueryInput({ onSubmit, disabled }) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) {
      onSubmit(query)
      setQuery('')
    }
  }

  return (
    <form className="query-input-form" onSubmit={handleSubmit}>
      <textarea
        className="query-textarea"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask a question about the image... (e.g., 'How does this circuit work?', 'Explain the flow in this diagram')"
        disabled={disabled}
        rows={4}
      />
      <button
        type="submit"
        className="submit-btn"
        disabled={disabled || !query.trim()}
      >
        🔍 Get Explanation
      </button>
    </form>
  )
}

export default QueryInput
