from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random

class AnnotationService:
    def __init__(self):
        self.colors = [
            (255, 0, 0, 128),      # Red
            (0, 255, 0, 128),      # Green
            (0, 0, 255, 128),      # Blue
            (255, 255, 0, 128),    # Yellow
            (255, 0, 255, 128),    # Magenta
            (0, 255, 255, 128),    # Cyan
        ]
    
    def create_annotations(self, image_data, explanation, vision_analysis):
        """Create annotated image with highlights and labels"""
        try:
            # Load image
            image = Image.open(BytesIO(image_data)).convert('RGBA')
            
            # Create overlay for annotations
            overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Try to load a font
            try:
                font = ImageFont.truetype("arial.ttf", 16)
                font_small = ImageFont.truetype("arial.ttf", 12)
            except:
                font = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Get objects from vision analysis
            objects = vision_analysis.get('objects', [])
            annotations = explanation.get('annotations', [])
            
            # Annotate detected objects if we have annotations
            if objects and annotations:
                for i, obj in enumerate(objects[:len(annotations)]):
                    bbox = obj['bbox']
                    x, y, w, h = bbox
                    
                    # Draw bounding box
                    color = self.colors[i % len(self.colors)]
                    draw.rectangle(
                        [x, y, x + w, y + h],
                        outline=color[:3] + (255,),
                        width=3
                    )
                    
                    # Add label if available
                    if i < len(annotations):
                        label = annotations[i].get('text', f'Element {i+1}')
                        # Draw label background
                        text_bbox = draw.textbbox((x, y - 20), label, font=font_small)
                        draw.rectangle(text_bbox, fill=color)
                        draw.text((x, y - 20), label, fill=(255, 255, 255, 255), font=font_small)
            
            # Add general highlight if no specific objects
            elif not objects:
                # Add a general annotation indicator
                width, height = image.size
                draw.rectangle(
                    [10, 10, width - 10, height - 10],
                    outline=(255, 215, 0, 200),
                    width=5
                )
                draw.text(
                    (20, 20),
                    "Analysis Complete",
                    fill=(255, 215, 0, 255),
                    font=font
                )
            
            # Composite overlay onto original image
            annotated = Image.alpha_composite(image, overlay)
            
            # Convert back to RGB
            annotated = annotated.convert('RGB')
            
            return annotated
            
        except Exception as e:
            print(f"Annotation error: {e}")
            # Return original image on error
            return Image.open(BytesIO(image_data))
