# database/queries.py
from typing import List
from .database import get_connection
from .models import Student

def create_students_table():
    query = """
    CREATE TABLE IF NOT EXISTS students (
        student_id INT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        age INT,
        gender VARCHAR(10),
        subject VARCHAR(100),
        marks INT
    );
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)

def insert_student(student: Student):
    query = """
    INSERT INTO students (student_id, name, age, gender, subject, marks)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    values = (
        student.student_id,
        student.name,
        student.age,
        student.gender,
        student.subject,
        student.marks,
    )
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)

def get_all_students() -> List[Student]:
    query = "SELECT student_id, name, age, gender, subject, marks FROM students;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    return [
        Student(
            student_id=row[0],
            name=row[1],
            age=row[2],
            gender=row[3],
            subject=row[4],
            marks=row[5],
        )
        for row in rows
    ]

def delete_student_by_id(student_id: int) -> bool:
    """
    Deleta um estudante pelo ID.
    Retorna True se algum registro foi deletado, False caso contrário.
    """
    query = "DELETE FROM students WHERE student_id = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (student_id,))
            # rowcount = número de linhas afetadas pelo DELETE
            return cur.rowcount > 0