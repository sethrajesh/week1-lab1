import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIConnectionError

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: Open AI key not found")
    print("Copy .env.example to .env and add your key ")
    sys.exit(1)

client = OpenAI(api_key=api_key)
MODEL=os.getenv("OPENAI_MODEL","gpt-4.1-mini")

print("Sending prompt: What is generative AI in one sentence")

try:
    response=client.chat.completions.create(
        model=MODEL,
        messages=[
                {"role": "system", "content": "you are a helpful assistant. Be concise"},
                {"role": "user", "content": "what are generative AI in one sentence"},
            ],
        temperature=0.7,
        max_tokens=100,
        )
    print(f"Response: {response.choices[0].message.content}")
    print(f"Tokens used: {response.usage.total_tokens} ")
    
except AuthenticationError:
        print("Error: Invalid API key. Check your .env file. ")
except APIConnectionError:
        print("Error: Cannot connect. Check your internet. ")
except Exception as e:
        print("Unexpected error: {e}")