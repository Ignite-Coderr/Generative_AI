# 🎓 Student Management API (FastAPI + PostgreSQL)

A simple **Student Management REST API** built using **FastAPI** and **PostgreSQL (Neon Cloud)**.  
This project demonstrates **CRUD operations**, **request validation with Pydantic**, and **local file persistence** for learning and practice purposes.

---

## 🚀 Features

- ✅ Create student records  
- ✅ Store student data in:
  - PostgreSQL database (Neon Cloud)
  - Local text file  
- ✅ Update student details  
- ✅ Delete student records  
- ✅ Schema validation using Pydantic  
- ✅ Interactive API documentation (Swagger UI)  

---

## 🛠️ Tech Stack

| Component | Technology |
|---------|------------|
| Backend Framework | FastAPI |
| Database | PostgreSQL (Neon Cloud) |
| DB Driver | psycopg2 |
| Validation | Pydantic |
| API Docs | Swagger UI (OpenAPI) |

---

## 📂 Project Structure

```text
.
├── index.py              # Main FastAPI application
├── students.txt          # File-based storage (auto-generated)
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
