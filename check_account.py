import os
from dotenv import load_dotenv
from anthropic import Anthropic
import requests

load_dotenv('backend/.env')

api_key = os.getenv('ANTHROPIC_API_KEY')

print("=" * 70)
print("CHECKING ANTHROPIC ACCOUNT")
print("=" * 70)

print(f"\nAPI Key: {api_key[:30]}...")
print(f"Key Length: {len(api_key)}")

# Try to make a simple API call
print("\nTesting API access...")

try:
    client = Anthropic(api_key=api_key)
    
    # Try the latest model
    models_to_try = [
        "claude-3-5-sonnet-latest",
        "claude-3-5-sonnet-20241022",
        "claude-3-opus-latest",
        "claude-3-sonnet-latest",
        "claude-3-haiku-20240307"
    ]
    
    for model in models_to_try:
        try:
            print(f"\nTrying: {model}")
            message = client.messages.create(
                model=model,
                max_tokens=20,
                messages=[{"role": "user", "content": "Hi"}]
            )
            print(f"✅ SUCCESS with {model}!")
            print(f"Response: {message.content[0].text}")
            print(f"\nYour account has access to: {model}")
            break
        except Exception as e:
            error_str = str(e)
            if "404" in error_str:
                print(f"❌ Model not found: {model}")
            elif "401" in error_str:
                print(f"❌ Authentication error - Invalid API key")
                break
            elif "403" in error_str:
                print(f"❌ Permission denied - Check account access")
                break
            else:
                print(f"❌ Error: {error_str[:150]}")
    
except Exception as e:
    print(f"\n❌ ACCOUNT ERROR:")
    print(f"   {e}")
    print("\n   Possible issues:")
    print("   1. API key is invalid or expired")
    print("   2. Account doesn't have access to Claude models")
    print("   3. Account needs to be activated")
    print("   4. Billing/credits issue")
    print("\n   Please check:")
    print("   - https://console.anthropic.com/settings/keys")
    print("   - https://console.anthropic.com/settings/billing")

print("\n" + "=" * 70)
