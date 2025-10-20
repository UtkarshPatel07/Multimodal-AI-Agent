import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv('backend/.env')

api_key = os.getenv('ANTHROPIC_API_KEY')
client = Anthropic(api_key=api_key)

print("Testing different Claude models...")

models_to_try = [
    "claude-3-5-sonnet-20241022",
    "claude-3-5-sonnet-20240620",
    "claude-3-sonnet-20240229",
    "claude-3-opus-20240229",
]

for model in models_to_try:
    try:
        print(f"\nTrying: {model}")
        message = client.messages.create(
            model=model,
            max_tokens=50,
            messages=[{"role": "user", "content": "Say hello"}]
        )
        print(f"✅ {model} WORKS!")
        print(f"   Response: {message.content[0].text}")
        break
    except Exception as e:
        print(f"❌ {model} failed: {str(e)[:100]}")
