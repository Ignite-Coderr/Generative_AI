# 🚀 AI Generation API (FastAPI)

A FastAPI application that provides:
- Text generation using GPT-5 mini
- Image generation using OpenAI Image API
- Rate limiting to prevent API abuse

---

## 🛠️ Features
- Text generation endpoint
- Image generation endpoint
- IP-based rate limiting
- Secure API key handling via environment variables

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone <repo-url>
cd project


---
### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt


---
### 3️⃣ Configure API Key
Create a .env file:
```bash
OPENAI_API_KEY=your_openai_api_key


---
### 4️⃣ Run Server
```bash
python -m uvicorn main:app --reload
