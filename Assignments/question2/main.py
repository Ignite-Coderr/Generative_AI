from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import requests
import os

# =========================
# Load Environment Variables
# =========================
load_dotenv()

EURON_API_KEY = os.getenv("EURON_API_KEY")

if not EURON_API_KEY:
    raise RuntimeError("EURON_API_KEY not found in .env file")

# =========================
# EURON API URLs
# =========================
TEXT_API_URL = "https://api.euron.one/api/v1/euri/chat/completions"
IMAGE_API_URL = "https://api.euron.one/api/v1/euri/images/generations"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {EURON_API_KEY}"
}

# =========================
# Rate Limiter
# =========================
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="EURON AI Generation API")

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

# =========================
# Request Models
# =========================
class TextRequest(BaseModel):
    prompt: str = Field(..., min_length=3)


class ImageRequest(BaseModel):
    prompt: str = Field(..., min_length=3)

# =========================
# TEXT GENERATION ENDPOINT
# =========================
@app.post("/generate-text")
@limiter.limit("5/minute")
def generate_text(request: Request, data: TextRequest):
    """
    Generates text using EURON GPT model
    Rate limit: 5 requests/minute/IP
    """
    payload = {
        "model": "gpt-4.1-nano",
        "max_tokens": 1000,
        "temperature": 0.7,
        "messages": [
            {
                "role": "user",
                "content": data.prompt
            }
        ]
    }

    try:
        response = requests.post(TEXT_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()

        result = response.json()

        return {
            "prompt": data.prompt,
            "response": result
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Text generation failed: {str(e)}"
        )

# =========================
# IMAGE GENERATION ENDPOINT
# =========================
@app.post("/generate-image")
@limiter.limit("3/minute")
def generate_image(request: Request, data: ImageRequest):
    """
    Generates images using EURON image generation API
    Rate limit: 3 requests/minute/IP
    """
    payload = {
        "prompt": data.prompt,
        "model": "black-forest-labs/FLUX.1-schnell",
        "n": 2,
        "size": "1024x1024",
        "quality": "standard",
        "response_format": "url",
        "style": "vivid"
    }

    try:
        response = requests.post(IMAGE_API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()

        result = response.json()

        return {
            "prompt": data.prompt,
            "images": result
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Image generation failed: {str(e)}"
        )

# =========================
# RATE LIMIT HANDLER
# =========================
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded. Try again later."}
    )
