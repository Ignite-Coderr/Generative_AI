
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

api_token = os.getenv("EURI_API_TOKEN")
if not api_token:
    print("Error: EURI_API_TOKEN not found in environment.")
    exit(1)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_token}"
}

payload = {
    "input": "The quick brown fox jumps over the lazy dog",
    "model": "text-embedding-ada-002"
}

# Potential endpoints
endpoints = [
    "https://api.euron.one/api/v1/embeddings",
    "https://api.euron.one/api/v1/euri/embeddings", # Based on chat endpoint structure
    "https://api.euron.one/v1/embeddings",
]

for url in endpoints:
    print(f"Testing URL: {url}")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("Success!")
            print(response.json())
            break
        else:
            print("Response:", response.text[:200])
    except Exception as e:
        print(f"Failed: {e}")
    print("-" * 20)
