from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
import base64
from io import BytesIO
from services.vision_service import VisionService
from services.speech_service import SpeechService
from services.reasoning_service import ReasoningService
from services.annotation_service import AnnotationService
import json

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize services
vision_service = VisionService()
speech_service = SpeechService()
reasoning_service = ReasoningService()
annotation_service = AnnotationService()

# Store session data (in production, use Redis or database)
sessions = {}

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Multimodal Explanation System API"}), 200

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    """Handle image upload and initial processing"""
    try:
        print("Upload image endpoint called")
        print(f"Request files: {request.files}")
        print(f"Request form: {request.form}")
        
        if 'image' not in request.files:
            print("ERROR: No image in request.files")
            return jsonify({"error": "No image provided"}), 400
        
        image_file = request.files['image']
        print(f"Image file received: {image_file.filename}")
        session_id = request.form.get('session_id', str(os.urandom(16).hex()))
        
        # Read and process image
        image_data = image_file.read()
        print(f"Image data size: {len(image_data)} bytes")
        
        # Analyze image with vision service
        print("Starting vision analysis...")
        vision_analysis = vision_service.analyze_image(image_data)
        
        # Store in session
        sessions[session_id] = {
            'image_data': image_data,
            'vision_analysis': vision_analysis,
            'conversation_history': []
        }
        
        print("Upload successful!")
        return jsonify({
            "session_id": session_id,
            "message": "Image uploaded successfully",
            "preview": vision_analysis.get('description', 'Image processed')
        }), 200
        
    except Exception as e:
        print(f"ERROR in upload_image: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    """Convert speech audio to text"""
    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio provided"}), 400
        
        audio_file = request.files['audio']
        audio_data = audio_file.read()
        
        # Transcribe audio
        text = speech_service.transcribe_audio(audio_data)
        
        return jsonify({"text": text}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/explain', methods=['POST'])
def explain():
    """Generate explanation for image + query"""
    try:
        data = request.json
        session_id = data.get('session_id')
        query = data.get('query')
        
        if not session_id or session_id not in sessions:
            return jsonify({"error": "Invalid session"}), 400
        
        if not query:
            return jsonify({"error": "No query provided"}), 400
        
        session = sessions[session_id]
        
        # Generate explanation using reasoning service
        explanation = reasoning_service.generate_explanation(
            image_data=session['image_data'],
            vision_analysis=session['vision_analysis'],
            query=query,
            conversation_history=session['conversation_history']
        )
        
        # Generate annotated image
        annotated_image = annotation_service.create_annotations(
            image_data=session['image_data'],
            explanation=explanation,
            vision_analysis=session['vision_analysis']
        )
        
        # Convert annotated image to base64
        buffered = BytesIO()
        annotated_image.save(buffered, format="PNG")
        annotated_image_b64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Generate speech output
        audio_b64 = speech_service.text_to_speech(explanation['text'])
        
        # Update conversation history
        session['conversation_history'].append({
            'query': query,
            'explanation': explanation['text']
        })
        
        return jsonify({
            "explanation": explanation['text'],
            "annotated_image": f"data:image/png;base64,{annotated_image_b64}",
            "audio": f"data:audio/mp3;base64,{audio_b64}",
            "annotations": explanation.get('annotations', [])
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def feedback():
    """Collect user feedback"""
    try:
        data = request.json
        session_id = data.get('session_id')
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        # In production, store in database
        print(f"Feedback received - Session: {session_id}, Rating: {rating}, Comment: {comment}")
        
        return jsonify({"message": "Feedback received"}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)
