# 🧪 Testing Guide

## Manual Testing Checklist

### 1. Image Upload Tests

#### Test 1.1: Basic Upload
- [ ] Click upload area
- [ ] Select a PNG image
- [ ] Verify image displays correctly
- [ ] Check session ID is created

#### Test 1.2: Drag and Drop
- [ ] Drag image file to upload zone
- [ ] Drop file
- [ ] Verify upload success

#### Test 1.3: File Type Validation
- [ ] Try uploading PDF
- [ ] Try uploading JPG
- [ ] Try uploading invalid file type
- [ ] Verify appropriate handling

#### Test 1.4: Large Files
- [ ] Upload 5MB image
- [ ] Upload 10MB image
- [ ] Check loading indicators
- [ ] Verify timeout handling

### 2. Text Query Tests

#### Test 2.1: Simple Query
- [ ] Upload test diagram
- [ ] Type: "What is this?"
- [ ] Submit query
- [ ] Verify explanation appears
- [ ] Check annotated image
- [ ] Verify audio plays

#### Test 2.2: Complex Query
- [ ] Ask detailed question
- [ ] Verify comprehensive explanation
- [ ] Check multiple annotations

#### Test 2.3: Follow-up Questions
- [ ] Ask initial question
- [ ] Ask follow-up: "Tell me more"
- [ ] Verify context is maintained

#### Test 2.4: Edge Cases
- [ ] Submit empty query (should be disabled)
- [ ] Submit very long query
- [ ] Submit special characters
- [ ] Verify proper handling

### 3. Voice Input Tests

#### Test 3.1: Basic Recording
- [ ] Click "Press to Speak"
- [ ] Allow microphone access
- [ ] Speak clearly: "Explain this diagram"
- [ ] Stop recording
- [ ] Verify transcription
- [ ] Check explanation generated

#### Test 3.2: Background Noise
- [ ] Record with background noise
- [ ] Verify transcription quality

#### Test 3.3: Different Accents
- [ ] Test with various accents
- [ ] Verify Whisper handles correctly

#### Test 3.4: Microphone Permissions
- [ ] Deny microphone access
- [ ] Verify error message
- [ ] Grant access
- [ ] Retry recording

### 4. Audio Output Tests

#### Test 4.1: Playback
- [ ] Get explanation
- [ ] Click "Play Audio"
- [ ] Verify audio plays
- [ ] Check pause functionality
- [ ] Test replay

#### Test 4.2: Audio Quality
- [ ] Listen to full explanation
- [ ] Verify clarity
- [ ] Check pronunciation

### 5. Annotation Tests

#### Test 5.1: Visual Highlights
- [ ] Upload diagram with clear elements
- [ ] Ask about specific parts
- [ ] Verify highlights appear
- [ ] Check bounding boxes
- [ ] Verify labels

#### Test 5.2: Multiple Annotations
- [ ] Ask complex question
- [ ] Verify multiple highlights
- [ ] Check color differentiation

### 6. Error Handling Tests

#### Test 6.1: Network Errors
- [ ] Disconnect internet
- [ ] Try to submit query
- [ ] Verify error message
- [ ] Reconnect
- [ ] Retry successfully

#### Test 6.2: API Errors
- [ ] Use invalid API key
- [ ] Verify error handling
- [ ] Check user-friendly message

#### Test 6.3: Timeout Handling
- [ ] Submit complex query
- [ ] Wait for response
- [ ] Verify timeout handling if needed

### 7. UI/UX Tests

#### Test 7.1: Responsive Design
- [ ] Test on desktop (1920x1080)
- [ ] Test on tablet (768px)
- [ ] Test on mobile (375px)
- [ ] Verify layout adapts

#### Test 7.2: Loading States
- [ ] Verify spinner appears during processing
- [ ] Check disabled states
- [ ] Verify loading messages

#### Test 7.3: Feedback System
- [ ] Submit query
- [ ] Click thumbs up
- [ ] Verify feedback recorded
- [ ] Check disabled state after feedback

### 8. Performance Tests

#### Test 8.1: Response Time
- [ ] Upload image
- [ ] Submit simple query
- [ ] Measure time to response
- [ ] Target: < 5 seconds

#### Test 8.2: Multiple Sessions
- [ ] Open multiple browser tabs
- [ ] Upload different images
- [ ] Submit queries simultaneously
- [ ] Verify no interference

## Automated Testing (Future)

### Unit Tests

```python
# backend/tests/test_vision_service.py
import pytest
from services.vision_service import VisionService

def test_analyze_image():
    service = VisionService()
    with open('test_image.png', 'rb') as f:
        result = service.analyze_image(f.read())
    assert 'description' in result
    assert result['description'] != ''
```

### Integration Tests

```python
# backend/tests/test_api.py
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_image(client):
    with open('test_image.png', 'rb') as img:
        response = client.post('/api/upload-image',
            data={'image': img})
    assert response.status_code == 200
    assert 'session_id' in response.json
```

### Frontend Tests

```javascript
// frontend/src/components/__tests__/ImageUpload.test.jsx
import { render, screen } from '@testing-library/react'
import ImageUpload from '../ImageUpload'

test('renders upload zone', () => {
  render(<ImageUpload onImageUpload={() => {}} />)
  expect(screen.getByText(/Click or drag/i)).toBeInTheDocument()
})
```

## Test Data

### Sample Images
Create a `test_data/` folder with:
- `circuit_diagram.png` - Simple electrical circuit
- `flowchart.png` - Algorithm flowchart
- `food_web.png` - Ecosystem diagram
- `math_graph.png` - Mathematical function
- `chess_board.png` - Chess position

### Sample Queries
```json
{
  "circuit": [
    "How does current flow?",
    "What is the voltage?",
    "Explain the resistor's role"
  ],
  "flowchart": [
    "Walk through this algorithm",
    "What happens at the decision point?",
    "Explain the loop"
  ],
  "general": [
    "What is this?",
    "Explain this diagram",
    "What am I looking at?"
  ]
}
```

## Performance Benchmarks

### Target Metrics
- Image upload: < 1 second
- Vision analysis: < 3 seconds
- Explanation generation: < 5 seconds
- Total response time: < 8 seconds
- Audio generation: < 2 seconds

### Load Testing
```bash
# Using Apache Bench
ab -n 100 -c 10 http://localhost:5000/health

# Using locust
locust -f locustfile.py --host=http://localhost:5000
```

## Browser Compatibility

Test on:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

## Accessibility Testing

- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] High contrast mode
- [ ] Focus indicators visible
- [ ] ARIA labels present

## Security Testing

- [ ] XSS prevention
- [ ] CSRF protection
- [ ] File upload validation
- [ ] API rate limiting
- [ ] Input sanitization

## Regression Testing

After each update:
1. Run full manual test suite
2. Check all critical paths
3. Verify no existing features broken
4. Test new features thoroughly

## Bug Reporting Template

```markdown
**Bug Description:**
Clear description of the issue

**Steps to Reproduce:**
1. Step one
2. Step two
3. Step three

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- Browser: Chrome 120
- OS: Windows 11
- Backend: Python 3.9

**Screenshots:**
Attach if applicable

**Console Errors:**
Paste any error messages
```
