from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List
import json
import os

app = FastAPI()

JSON_FILE = "courses.json"


# =========================
# Pydantic Model
# =========================
class Course(BaseModel):
    course_id: int = Field(..., gt=0, description="Course ID must be positive")
    course_name: str = Field(..., min_length=2)
    credits: int = Field(..., ge=1, le=10)
    instructor: str = Field(..., min_length=2)


# =========================
# Helper Function
# =========================
def save_courses_to_json(courses: List[Course]):
    data = [course.dict() for course in courses]

    # If file exists, append data
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.extend(data)

    with open(JSON_FILE, "w") as f:
        json.dump(existing_data, f, indent=4)


# =========================
# POST API
# =========================
@app.post("/courses", status_code=status.HTTP_201_CREATED)
def create_courses(courses: List[Course]):
    if not courses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course list cannot be empty"
        )

    save_courses_to_json(courses)

    return {
        "message": "Courses stored successfully",
        "total_courses_added": len(courses)
    }
