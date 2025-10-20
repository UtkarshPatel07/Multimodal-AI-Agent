# 📋 Setup Guide

## Step-by-Step Installation

### 1. Prerequisites Check

Ensure you have:
- Python 3.9 or higher: `python --version`
- Node.js 18 or higher: `node --version`
- pip: `pip --version`
- npm: `npm --version`

### 2. Get OpenAI API Key

1. Go to https://platform.openai.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy and save it securely

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
# OR
cp .env.example .env    # Mac/Linux

# Edit .env file and add your OpenAI API key
# Use notepad, vim, or any text editor
notepad .env
```

### 4. Frontend Setup

```bash
# Navigate to frontend directory (from root)
cd frontend

# Install dependencies
npm install
```

### 5. Running the Application

#### Option A: Run Both Services Together

From the root directory:
```bash
npm run dev
```

#### Option B: Run Separately

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### 6. Access the Application

Open your browser and go to:
```
http://localhost:3000
```

The backend API runs on:
```
http://localhost:5000
```

## Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Issue: "OpenAI API key not found"

**Solution:**
- Check that `backend/.env` file exists
- Verify `OPENAI_API_KEY=sk-...` is set correctly
- No spaces around the `=` sign
- No quotes around the key

### Issue: Port already in use

**Solution:**
```bash
# Change port in backend/.env
PORT=5001

# Change port in frontend/vite.config.js
server: {
  port: 3001
}
```

### Issue: CORS errors

**Solution:**
- Ensure backend is running on port 5000
- Check proxy configuration in `frontend/vite.config.js`
- Restart both services

### Issue: Microphone not working

**Solution:**
- Grant microphone permissions in browser
- Use HTTPS in production (required for mic access)
- Check browser console for errors

### Issue: Image upload fails

**Solution:**
- Check file size (< 10MB recommended)
- Ensure file is valid image format (PNG, JPG)
- Check backend logs for errors

## Optional Enhancements

### Install Tesseract OCR (for better text detection)

**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH
3. Restart terminal

**Mac:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
```

### Google Cloud Vision (Optional)

1. Create Google Cloud project
2. Enable Vision API
3. Download credentials JSON
4. Set in `.env`:
```env
GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

## Testing the System

### 1. Test Image Upload
- Upload a simple diagram or flowchart
- Verify it displays correctly

### 2. Test Text Query
- Type: "What is shown in this image?"
- Wait for explanation
- Check annotated image appears

### 3. Test Voice Input
- Click "Press to Speak"
- Allow microphone access
- Ask: "Explain this diagram"
- Verify transcription and explanation

### 4. Test Audio Output
- After getting explanation
- Click "Play Audio"
- Verify speech plays correctly

## Next Steps

- Read the main README.md for usage examples
- Check DEPLOYMENT.md for production deployment
- Explore the code in `backend/services/` and `frontend/src/`
- Customize the UI in CSS files
- Add domain-specific knowledge to prompts

## Getting Help

If you encounter issues:
1. Check the console logs (browser and terminal)
2. Verify all dependencies are installed
3. Ensure API keys are valid
4. Check network connectivity
5. Review error messages carefully

## System Requirements

**Minimum:**
- 4GB RAM
- 2 CPU cores
- 1GB free disk space
- Internet connection

**Recommended:**
- 8GB+ RAM
- 4+ CPU cores
- 5GB free disk space
- Fast internet connection
