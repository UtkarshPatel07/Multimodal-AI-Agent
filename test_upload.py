import requests
from PIL import Image
from io import BytesIO

# Create a simple test image
img = Image.new('RGB', (100, 100), color='red')
img_bytes = BytesIO()
img.save(img_bytes, format='PNG')
img_bytes.seek(0)

# Test upload
files = {'image': ('test.png', img_bytes, 'image/png')}
response = requests.post('http://localhost:5000/api/upload-image', files=files)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
