import os
import base64
from io import BytesIO
from anthropic import Anthropic
import json

class ReasoningService:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def generate_explanation(self, image_data, vision_analysis, query, conversation_history):
        """Generate step-by-step explanation using Claude"""
        try:
            # Try Claude first
            try:
                # Encode image
                from PIL import Image
                img = Image.open(BytesIO(image_data))
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                image_b64 = base64.b64encode(buffered.getvalue()).decode()
                
                # Build conversation context
                context = self._build_context(vision_analysis, conversation_history)
                
                # Create system prompt
                system_prompt = """You are an expert AI tutor that explains diagrams, images, and visual content.
Your task is to:
1. Analyze the image and the user's question
2. Provide a clear, step-by-step explanation
3. Reference specific parts of the image in your explanation
4. Use simple, accessible language
5. Structure your response with clear reasoning

When referencing image elements, use descriptive terms like "the red circle in the top-left", 
"the arrow pointing from A to B", etc. This helps with annotation generation.

Format your response as a natural explanation, as if you were a teacher pointing at a diagram."""
                
                # Build messages with image
                user_content = [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_b64
                        }
                    },
                    {
                        "type": "text",
                        "text": f"""Context about the image:
{context}

User's question: {query}

Please provide a detailed explanation that answers the question, referencing specific visual elements."""
                    }
                ]
                
                # Get explanation from Claude
                message = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=1500,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_content}]
                )
                
                explanation_text = message.content[0].text
            except Exception as api_error:
                print(f"Claude API error: {api_error}")
                # Fallback explanation
                explanation_text = f"""I apologize, but I'm currently unable to access the AI vision model due to API issues.

However, I can see that you've uploaded an image and asked: "{query}"

To use this system fully, you'll need to:
1. Check your Anthropic API account at https://console.anthropic.com/
2. Ensure your API key is valid and has credits
3. Verify your API key is set correctly in the .env file

Once your API key is active, this system will:
- Analyze your image in detail
- Provide step-by-step explanations
- Highlight relevant parts of the image
- Answer follow-up questions

The image has been uploaded successfully and is ready for analysis once API access is restored."""
            
            # Extract annotation hints from explanation
            annotations = self._extract_annotations(explanation_text, vision_analysis)
            
            return {
                "text": explanation_text,
                "annotations": annotations
            }
            
        except Exception as e:
            print(f"Reasoning error: {e}")
            return {
                "text": f"I apologize, but I encountered an error generating the explanation: {str(e)}",
                "annotations": []
            }
    
    def _build_context(self, vision_analysis, conversation_history):
        """Build context string from vision analysis"""
        context = f"Image Description: {vision_analysis.get('description', 'N/A')}\n"
        
        if vision_analysis.get('ocr_text'):
            context += f"\nText found in image: {vision_analysis['ocr_text']}\n"
        
        if vision_analysis.get('objects'):
            context += f"\nDetected {len(vision_analysis['objects'])} visual elements/regions\n"
        
        return context
    
    def _extract_annotations(self, explanation_text, vision_analysis):
        """Extract potential annotation points from explanation"""
        annotations = []
        
        # Simple keyword extraction for demonstration
        # In production, use more sophisticated NLP or ask GPT to output structured annotations
        keywords = ['top', 'bottom', 'left', 'right', 'center', 'arrow', 'circle', 'box', 'line']
        
        for keyword in keywords:
            if keyword in explanation_text.lower():
                annotations.append({
                    "type": "highlight",
                    "keyword": keyword,
                    "text": f"Referenced: {keyword}"
                })
        
        return annotations
