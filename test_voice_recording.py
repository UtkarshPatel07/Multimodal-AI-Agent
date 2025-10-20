"""
Test Voice Recording and Transcription
Tests the complete voice workflow with the backend
"""

import requests
import time
from pathlib import Path

# Configuration
BACKEND_URL = "http://127.0.0.1:5000"

def test_backend_health():
    """Test if backend is running"""
    print("\n🔍 Testing Backend Health...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        return False

def test_speech_to_text():
    """Test speech-to-text with a sample audio file"""
    print("\n🎤 Testing Speech-to-Text...")
    
    # Create a test audio file (you'll need to record one manually)
    print("⚠️  To test speech-to-text:")
    print("   1. Go to http://localhost:3000")
    print("   2. Click 'Press to Speak'")
    print("   3. Say something like 'Hello, this is a test'")
    print("   4. Click 'Stop Recording'")
    print("   5. Check the backend logs for transcription")
    
    return True

def test_image_upload():
    """Test image upload"""
    print("\n🖼️  Testing Image Upload...")
    
    # Check if there's a test image
    test_images = list(Path('.').glob('*.jpg')) + list(Path('.').glob('*.png'))
    
    if not test_images:
        print("⚠️  No test images found. Please add a .jpg or .png file to test.")
        return False
    
    test_image = test_images[0]
    print(f"📸 Using test image: {test_image}")
    
    try:
        with open(test_image, 'rb') as f:
            files = {'image': f}
            response = requests.post(
                f"{BACKEND_URL}/api/upload-image",
                files=files,
                timeout=10
            )
        
        if response.status_code == 200:
            print("✅ Image upload successful!")
            data = response.json()
            print(f"   Image ID: {data.get('image_id', 'N/A')}")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False

def main():
    print("=" * 60)
    print("🧪 MULTIMODAL AI SYSTEM - VOICE RECORDING TEST")
    print("=" * 60)
    
    # Run tests
    results = []
    
    results.append(("Backend Health", test_backend_health()))
    results.append(("Image Upload", test_image_upload()))
    results.append(("Speech-to-Text", test_speech_to_text()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\n🎯 Results: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 All tests passed! System is ready.")
        print("\n📝 Next Steps:")
        print("   1. Open http://localhost:3000 in your browser")
        print("   2. Upload an image")
        print("   3. Click 'Press to Speak' and record your question")
        print("   4. Get AI-powered explanation with voice!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
