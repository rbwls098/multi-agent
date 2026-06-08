import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")

print(f"Loaded Model: {model}")
print(f"API Key exists: {bool(api_key)}")

try:
     client = OpenAI(api_key=api_key)
     response = client.chat.completions.create(
         model=model,
         messages=[{"role": "user", "content": "Hello! Are you working?"}]
     )
     print("API Response:", response.choices[0].message.content)
except Exception as e:
     print("Error:", e)