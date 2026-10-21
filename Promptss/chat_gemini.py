from google import genai
from google.genai import types

client = genai.Client(api_key='AIzaSyCA5fEZUCTGq62fOFD9q_xbFtR6OMo7h1k')
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='Why is the sky blue?'
)
print(response.text)