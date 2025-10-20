import os
import base64
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
try:
    import pytesseract
except:
    pytesseract = None
from anthropic import Anthropic

class VisionService:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def analyze_image(self, image_data):
        """Analyze image using GPT-4V and OCR"""
        try:
            # Convert to PIL Image
            image = Image.open(BytesIO(image_data))
            
            # Get basic image info
            width, height = image.size
            format_name = image.format or "Unknown"
            
            # Try Claude Vision analysis
            vision_description = None
            try:
                # Encode image to base64
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                image_b64 = base64.b64encode(buffered.getvalue()).decode()
                
                # Determine media type
                media_type = "image/png"
                if format_name.lower() == "jpeg" or format_name.lower() == "jpg":
                    media_type = "image/jpeg"
                
                # Use Claude for vision analysis
                message = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1000,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": media_type,
                                        "data": image_b64
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": """Analyze this image in detail. Identify:
1. Main objects, shapes, and components
2. Text labels and annotations present
3. Spatial relationships between elements
4. Type of diagram/image (flowchart, circuit, chart, etc.)
5. Key visual elements that could be referenced in explanations

Provide a structured analysis."""
                                }
                            ]
                        }
                    ]
                )
                
                vision_description = message.content[0].text
            except Exception as api_error:
                print(f"Claude Vision API error: {api_error}")
                # Fallback to basic description
                vision_description = f"Image uploaded successfully. Size: {width}x{height}px, Format: {format_name}. Ready for analysis."
            
            # Perform OCR if available
            ocr_text = ""
            if pytesseract:
                try:
                    ocr_text = pytesseract.image_to_string(image)
                except:
                    pass
            
            # Detect objects/regions using basic CV
            objects = self._detect_objects(image_data)
            
            return {
                "description": vision_description,
                "ocr_text": ocr_text,
                "objects": objects,
                "image_size": image.size
            }
            
        except Exception as e:
            print(f"Vision analysis error: {e}")
            return {
                "description": "Image uploaded successfully",
                "ocr_text": "",
                "objects": [],
                "error": str(e)
            }
    
    def _detect_objects(self, image_data):
        """Basic object detection using OpenCV"""
        try:
            # Convert to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                print("Failed to decode image")
                return []
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect contours
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            objects = []
            for i, contour in enumerate(contours[:20]):  # Limit to 20 objects
                x, y, w, h = cv2.boundingRect(contour)
                if w > 20 and h > 20:  # Filter small objects
                    objects.append({
                        "id": f"obj_{i}",
                        "bbox": [int(x), int(y), int(w), int(h)],
                        "area": int(w * h)
                    })
            
            return objects
            
        except Exception as e:
            print(f"Object detection error: {e}")
            import traceback
            traceback.print_exc()
            return []
