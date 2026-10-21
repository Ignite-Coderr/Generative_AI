
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

EURI_API_URL = "https://api.euron.one/api/v1/euri/chat/completions"
EURI_API_TOKEN = os.getenv("EURI_API_TOKEN")

print(f"Testing Euri API with token: {EURI_API_TOKEN[:10]}...")

payload = {
    "messages": [
        {"role": "user", "content": "What is AGI?"}
    ],
    "model": "gpt-4.1-nano",
    "max_tokens": 100,
    "temperature": 0.7
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {EURI_API_TOKEN}"
}

try:
    response = requests.post(EURI_API_URL, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        print("Success!")
        print(response.json()['choices'][0]['message']['content'])
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"Exception: {e}")
