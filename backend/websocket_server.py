"""
WebSocket Server for Real-Time Voice Assistant
Handles streaming audio, wake-word detection, and conversation context
"""

import asyncio
import websockets
import json
import base64
from services.streaming_audio_service import StreamingAudioService
from services.reasoning_service import ReasoningService
from services.vision_service import VisionService

class VoiceWebSocketServer:
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.active_connections = {}  # session_id -> connection info
        
        # Services
        self.audio_service = StreamingAudioService()
        self.reasoning_service = ReasoningService()
        self.vision_service = VisionService()
        
        print(f"🚀 Voice WebSocket Server initialized")
    
    async def handle_client(self, websocket, path):
        """Handle individual client connection"""
        session_id = id(websocket)
        
        # Store connection info
        self.active_connections[session_id] = {
            'websocket': websocket,
            'audio_service': StreamingAudioService(),  # Each session gets own service
            'current_image': None,
            'listening': False
        }
        
        print(f"✅ Client connected. Session: {session_id}")
        
        try:
            async for message in websocket:
                await self.handle_message(session_id, message)
        
        except websockets.exceptions.ConnectionClosed:
            print(f"❌ Client disconnected. Session: {session_id}")
        
        finally:
            # Cleanup
            if session_id in self.active_connections:
                del self.active_connections[session_id]
    
    async def handle_message(self, session_id, message):
        """Handle incoming message (audio or control)"""
        conn = self.active_connections[session_id]
        websocket = conn['websocket']
        audio_service = conn['audio_service']
        
        try:
            if isinstance(message, bytes):
                # Audio data chunk
                await self.process_audio_chunk(session_id, message)
            
            else:
                # JSON control message
                data = json.loads(message)
                await self.handle_control_message(session_id, data)
        
        except Exception as e:
            print(f"❌ Error handling message: {e}")
            await websocket.send(json.dumps({
                'type': 'error',
                'message': str(e)
            }))
    
    async def process_audio_chunk(self, session_id, audio_data):
        """Process incoming audio chunk"""
        conn = self.active_connections[session_id]
        websocket = conn['websocket']
        audio_service = conn['audio_service']
        
        if not conn['listening']:
            return
        
        try:
            # Transcribe chunk
            text = await audio_service.transcribe_chunk(audio_data)
            
            if text:
                # Send transcription to client
                await websocket.send(json.dumps({
                    'type': 'transcription',
                    'text': text,
                    'partial': not audio_service.is_sentence_complete(text)
                }))
                
                # If sentence is complete, generate response
                if audio_service.is_sentence_complete(text):
                    await self.generate_response(session_id, text)
        
        except Exception as e:
            print(f"❌ Audio processing error: {e}")
    
    async def generate_response(self, session_id, user_text):
        """Generate AI response with conversation context"""
        conn = self.active_connections[session_id]
        websocket = conn['websocket']
        audio_service = conn['audio_service']
        
        try:
            # Add user message to history
            audio_service.add_to_history('user', user_text)
            
            # Get conversation context
            context = audio_service.get_context_prompt()
            
            # Build prompt with context
            if conn['current_image']:
                # Image + text query with context
                prompt = f"{context}\n\nCurrent question: {user_text}"
                
                # Analyze with vision service
                analysis = self.vision_service.analyze_image(
                    conn['current_image'],
                    prompt
                )
                
                response_text = analysis.get('description', 'I could not analyze the image.')
            
            else:
                # Text-only conversation with context
                prompt = f"{context}\n\nUser: {user_text}\n\nAssistant:"
                
                # Generate response with reasoning service
                response_text = self.reasoning_service.generate_explanation(
                    prompt,
                    context=""  # Context already in prompt
                )
            
            # Add assistant response to history
            audio_service.add_to_history('assistant', response_text)
            
            # Send response to client
            await websocket.send(json.dumps({
                'type': 'response',
                'text': response_text,
                'conversation_summary': audio_service.get_conversation_summary()
            }))
            
            print(f"💬 Response sent: {response_text[:100]}...")
        
        except Exception as e:
            print(f"❌ Response generation error: {e}")
            await websocket.send(json.dumps({
                'type': 'error',
                'message': f"Failed to generate response: {str(e)}"
            }))
    
    async def handle_control_message(self, session_id, data):
        """Handle control messages"""
        conn = self.active_connections[session_id]
        websocket = conn['websocket']
        audio_service = conn['audio_service']
        
        msg_type = data.get('type')
        
        if msg_type == 'start_listening':
            conn['listening'] = True
            audio_service.clear_buffer()
            await websocket.send(json.dumps({
                'type': 'status',
                'status': 'listening'
            }))
            print(f"🎤 Started listening. Session: {session_id}")
        
        elif msg_type == 'stop_listening':
            conn['listening'] = False
            await websocket.send(json.dumps({
                'type': 'status',
                'status': 'stopped'
            }))
            print(f"⏹️ Stopped listening. Session: {session_id}")
        
        elif msg_type == 'upload_image':
            # Store image for context
            image_data = data.get('image')
            if image_data:
                # Decode base64 image
                import base64
                from io import BytesIO
                image_bytes = base64.b64decode(image_data.split(',')[1])
                conn['current_image'] = image_bytes
                
                await websocket.send(json.dumps({
                    'type': 'status',
                    'status': 'image_uploaded'
                }))
                print(f"🖼️ Image uploaded. Session: {session_id}")
        
        elif msg_type == 'clear_image':
            conn['current_image'] = None
            await websocket.send(json.dumps({
                'type': 'status',
                'status': 'image_cleared'
            }))
        
        elif msg_type == 'reset_conversation':
            audio_service.reset_conversation()
            await websocket.send(json.dumps({
                'type': 'status',
                'status': 'conversation_reset'
            }))
            print(f"🔄 Conversation reset. Session: {session_id}")
        
        elif msg_type == 'get_history':
            await websocket.send(json.dumps({
                'type': 'history',
                'summary': audio_service.get_conversation_summary(),
                'full_history': audio_service.conversation_history
            }))
    
    def start(self):
        """Start WebSocket server"""
        print(f"\n{'='*60}")
        print(f"🚀 Starting Voice WebSocket Server")
        print(f"{'='*60}")
        print(f"📡 WebSocket URL: ws://{self.host}:{self.port}")
        print(f"🎤 Features: Streaming Audio + Conversation Context")
        print(f"{'='*60}\n")
        
        start_server = websockets.serve(
            self.handle_client,
            self.host,
            self.port,
            max_size=10 * 1024 * 1024  # 10MB max message size
        )
        
        asyncio.get_event_loop().run_until_complete(start_server)
        print("✅ Server started successfully!")
        print("💡 Waiting for connections...\n")
        
        asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    server = VoiceWebSocketServer()
    server.start()
