import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv('backend/.env')

api_key = os.getenv('ANTHROPIC_API_KEY')

print("=" * 70)
print("TESTING CLAUDE API KEY")
print("=" * 70)

print(f"\n1. API Key Found: {api_key[:30]}..." if api_key else "NO KEY FOUND")
print(f"   Key Length: {len(api_key)} characters")
print(f"   Key Format: {'✅ Correct' if api_key.startswith('sk-ant-api03-') else '❌ Invalid format'}")

print("\n2. Testing API Connection...")
try:
    client = Anthropic(api_key=api_key)
    
    # Test with a simple message
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=50,
        messages=[
            {"role": "user", "content": "Say 'Hello, I am Claude!'"}
        ]
    )
    
    print("✅ API Key is VALID!")
    print(f"   Response: {message.content[0].text}")
    
except Exception as e:
    print(f"❌ API Key is INVALID!")
    print(f"   Error: {e}")
    print("\n   Possible issues:")
    print("   - Key is incomplete or truncated")
    print("   - Key has expired")
    print("   - Account has no credits")
    print("   - Key was copied incorrectly")
    print("\n   Please get a new key from:")
    print("   https://console.anthropic.com/settings/keys")

print("\n" + "=" * 70)
