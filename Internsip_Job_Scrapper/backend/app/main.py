from fastapi import FastAPI, UploadFile, File
from app.resume_parser import extract_resume_text
from app.experience_classifier import classify_experience
from app.job_fetcher import fetch_jobs

app = FastAPI()

@app.post("/resume/upload")
async def upload_resume(resume: UploadFile = File(...)):
    text = extract_resume_text(resume)
    level = classify_experience(text)

    jobs = fetch_jobs(level)

    return {
        "resume_id": 1,
        "experience_level": level,
        "jobs": jobs[:10]
    }
