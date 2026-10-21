# Implement a REST API endpoint using a framework like Flask or FastAPI that allows users to update existing records in a MongoDB collection. The API should accept a unique identifier (e.g., _id) and a JSON payload containing the fields to be updated. Ensure proper error handling and validation of input data. Deploy this API to Render, documenting the deployment process.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="MongoDB Update API")

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = AsyncIOMotorClient(MONGO_URI)
db = client["employee"]
collection = db["employee_collection"]

# Utility to convert ObjectId to string
def serialize_doc(doc):
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


# INSERT endpoint (for testing)
@app.post("/employee/insert")
async def insert_employee():
    doc = {
        "name": "Aman",
        "age": 25,
        "department": "Data Science",
        "salary": 50000
    }
    result = await collection.insert_one(doc)
    return {"inserted_id": str(result.inserted_id)}


# Pydantic model for update payload
class UpdateEmployee(BaseModel):
    name: str | None = None
    age: int | None = Field(None, ge=18, le=65)
    department: str | None = None
    salary: int | None = Field(None, gt=0)


# UPDATE endpoint
@app.put("/employee/update/{employee_id}")
async def update_employee(employee_id: str, payload: UpdateEmployee):

    # Validate ObjectId
    if not ObjectId.is_valid(employee_id):
        raise HTTPException(status_code=400, detail="Invalid employee ID")

    update_data = {k: v for k, v in payload.dict().items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")

    result = await collection.update_one(
        {"_id": ObjectId(employee_id)},   # ✅ FIXED HERE
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")

    updated_doc = await collection.find_one({"_id": ObjectId(employee_id)})

    return {
        "message": "Employee updated successfully",
        "data": serialize_doc(updated_doc)
    }
