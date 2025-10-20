import requests
from PIL import Image
from io import BytesIO
import json

print("=" * 70)
print("TESTING FULL WORKFLOW")
print("=" * 70)

# Step 1: Create a test image
print("\n1. Creating test image...")
img = Image.new('RGB', (200, 200), color='blue')
img_bytes = BytesIO()
img.save(img_bytes, format='PNG')
img_bytes.seek(0)
print("✅ Test image created (200x200px, blue)")

# Step 2: Upload image
print("\n2. Uploading image...")
files = {'image': ('test.png', img_bytes, 'image/png')}
response = requests.post('http://localhost:5000/api/upload-image', files=files)
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    session_id = data['session_id']
    print(f"✅ Upload successful!")
    print(f"Session ID: {session_id}")
    print(f"Preview: {data['preview'][:100]}...")
else:
    print(f"❌ Upload failed: {response.text}")
    exit(1)

# Step 3: Ask a question
print("\n3. Asking a question...")
query_data = {
    'session_id': session_id,
    'query': 'What color is this image?'
}
response = requests.post('http://localhost:5000/api/explain', json=query_data)
print(f"Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"✅ Explanation received!")
    print(f"Explanation: {data['explanation'][:200]}...")
    print(f"Has annotated image: {'annotated_image' in data}")
    print(f"Has audio: {'audio' in data and len(data['audio']) > 0}")
else:
    print(f"❌ Explanation failed: {response.text}")

# Step 4: Test health endpoint
print("\n4. Testing health endpoint...")
response = requests.get('http://localhost:5000/health')
print(f"Status Code: {response.status_code}")
if response.status_code == 200:
    print(f"✅ Health check passed: {response.json()}")
else:
    print(f"❌ Health check failed")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
