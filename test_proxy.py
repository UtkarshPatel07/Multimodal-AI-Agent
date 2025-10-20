import requests
from PIL import Image
from io import BytesIO

print("Testing proxy connection...")

# Create test image
img = Image.new('RGB', (100, 100), color='red')
img_bytes = BytesIO()
img.save(img_bytes, format='PNG')
img_bytes.seek(0)

# Test through frontend proxy (simulating what browser does)
print("\n1. Testing direct backend connection...")
files = {'image': ('test.png', img_bytes, 'image/png')}
response = requests.post('http://127.0.0.1:5000/api/upload-image', files=files)
print(f"Direct backend: {response.status_code}")

# Reset image bytes
img_bytes.seek(0)

print("\n2. Testing through Vite proxy...")
files = {'image': ('test.png', img_bytes, 'image/png')}
try:
    response = requests.post('http://localhost:3000/api/upload-image', files=files)
    print(f"Through proxy: {response.status_code}")
    if response.status_code == 200:
        print("✅ Proxy working correctly!")
    else:
        print(f"❌ Proxy error: {response.text}")
except Exception as e:
    print(f"❌ Proxy connection failed: {e}")

print("\n3. Testing health endpoint through proxy...")
try:
    response = requests.get('http://localhost:3000/api/health')
    print(f"Health through proxy: {response.status_code}")
except Exception as e:
    print(f"❌ Health check failed: {e}")
