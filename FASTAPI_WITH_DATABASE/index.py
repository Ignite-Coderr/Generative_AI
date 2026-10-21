# Import FastAPI framework to build APIs
from fastapi import FastAPI
from fastapi import HTTPException, status


# Import BaseModel from Pydantic for request body validation
from pydantic import BaseModel   # Used for schema validation

# Import psycopg2 to connect Python with PostgreSQL
import psycopg2

# Import RealDictCursor to return rows as dictionaries instead of tuples
from psycopg2.extras import RealDictCursor


# Create an instance of the FastAPI application
app = FastAPI()


# PostgreSQL database connection URL (Neon cloud database)
# Contains username, password, host, database name, and SSL configuration
db_url = (
    "postgresql://neondb_owner:npg_eg2DFy6GtRdn@ep-damp-bread-adq88voy-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)


# Define a Pydantic model for Student schema validation
# This ensures incoming request data has correct types
class Students(BaseModel):
    id: int      # Student ID
    name: str    # Student name
    age: int     # Student age


# Function to establish and return a PostgreSQL database connection
def get_connection_url():
    """
    Creates and returns a PostgreSQL database connection
    using psycopg2 and RealDictCursor.
    """
    conn = psycopg2.connect(
        db_url,
        cursor_factory=RealDictCursor
    )
    return conn


# Function to save student data into a local text file
def save_student_to_file(data: Students):
    """
    Appends student data into a local text file.
    """
    with open("students.txt", "a") as f:
        f.write(f"{data.id}, {data.name}, {data.age}\n")


# API endpoint to save student data into a text file
@app.post("/students")
def create_students(stud: Students):
    """
    Saves student data to a text file.
    """
    save_student_to_file(stud)
    return {"message": "Student Data Saved Successfully"}


# API endpoint to insert student data into PostgreSQL database
@app.post("/student/db/insert")
def store_student_in_db(student: Students):
    """
    Inserts student data into the PostgreSQL database.
    """
    # Establish database connection
    conn = get_connection_url()
    cursor = conn.cursor()

    # SQL query to insert a student record
    insert_query = """
        INSERT INTO student (id, name, age)
        VALUES (%s, %s, %s)
    """

    # Execute the query using parameterized values
    cursor.execute(
        insert_query,
        (student.id, student.name, student.age)
    )

    # Commit the transaction
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()

    return {"message": "Student inserted into database successfully"}


# API endpoint to update student data in PostgreSQL database
@app.put("/student/db/update/{student_id}")
def update_student(student_id: int, student: Students):
    """
    Updates name and age of a student using student_id.
    """
    # Establish database connection
    conn = get_connection_url()
    cursor = conn.cursor()

    # SQL query to update student record
    update_query = """
        UPDATE student
        SET name = %s, age = %s
        WHERE id = %s
    """

    # Execute update query
    cursor.execute(
        update_query,
        (student.name, student.age, student_id)
    )

    # If no rows were updated, the student ID does not exist
    if cursor.rowcount == 0:
        conn.rollback()
        cursor.close()
        conn.close()
        return {"message": "Student not found"}

    # Commit changes
    conn.commit()

    # Close cursor and connection
    cursor.close()
    conn.close()

    return {"message": "Student updated successfully"}


@app.delete("/student/db/delete/{student_id}")
def delete_student(student_id: int):
    conn = get_connection_url()
    cursor = conn.cursor()

    delete_query = "DELETE FROM student WHERE id = %s"
    cursor.execute(delete_query, (student_id,))

    # If no row was deleted, student does not exist
    if cursor.rowcount == 0:
        conn.rollback()
        cursor.close()
        conn.close()
        return {"message": "Student not found"}

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Student deleted successfully"}


# TODO: Fetching Data
@app.get("/student/db/{student_id}")
def get_data(student_id: int):
    """
    Retrieves a student record from PostgreSQL using student_id.
    Returns 404 if student is not found.
    """
    try:
        conn = get_connection_url()
        cursor = conn.cursor()

        select_query = """
            SELECT id, name, age
            FROM student
            WHERE id = %s
        """

        # ✅ FIXED LINE
        cursor.execute(select_query, (student_id,))
        student = cursor.fetchone()

        cursor.close()
        conn.close()

        if student is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )

        return {
            "status": "success",
            "data": student
        }

    except psycopg2.Error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )
