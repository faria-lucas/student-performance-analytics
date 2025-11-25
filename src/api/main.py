# src/api/main.py
from typing import Optional
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database.models import Student as StudentDomain
from database.queries import (
    get_all_students,
    get_student_by_id,
    insert_student,
    update_student,
    delete_student_by_id,
)

app = FastAPI(
    title="Student Performance API",
    description="API para gerenciamento e análise de desempenho de estudantes.",
    version="0.1.0",
)


# ======== Pydantic Models (para requests/responses) ========

class StudentBase(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    subject: Optional[str] = None
    marks: Optional[int] = None


class StudentCreate(StudentBase):
    student_id: int   # ID vem no corpo do POST


class StudentUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    gender: str | None = None
    subject: str | None = None
    marks: int | None = None


class StudentResponse(StudentBase):
    student_id: int

    class Config:
        from_attributes = True   # permite criar a partir do dataclass StudentDomain


# ======== Helpers de conversão ========

def domain_to_response(student: StudentDomain) -> StudentResponse:
    return StudentResponse(
        student_id=student.student_id,
        name=student.name,
        age=student.age,
        gender=student.gender,
        subject=student.subject,
        marks=student.marks,
    )


def merge_student_update(
    existing: StudentDomain, update: StudentUpdate
) -> StudentDomain:
    """
    Aplica os campos do update (quando não nulos) em um StudentDomain existente.
    """
    return StudentDomain(
        student_id=existing.student_id,
        name=update.name if update.name is not None else existing.name,
        age=update.age if update.age is not None else existing.age,
        gender=update.gender if update.gender is not None else existing.gender,
        subject=update.subject if update.subject is not None else existing.subject,
        marks=update.marks if update.marks is not None else existing.marks,
    )


# ======== Rotas ========

@app.get("/students", response_model=List[StudentResponse])
def list_students():
    """Lista todos os estudantes."""
    students = get_all_students()
    return [domain_to_response(s) for s in students]


@app.get("/students/{student_id}", response_model=StudentResponse)
def get_student(student_id: int):
    """Busca um estudante pelo ID."""
    student = get_student_by_id(student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return domain_to_response(student)


@app.post("/students", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate):
    """
    Cria um novo estudante.
    Fails se student_id já existir.
    """
    # Reaproveita a validação já feita em insert_student (que retorna False se ID duplicado)
    new_student_domain = StudentDomain(
        student_id=student.student_id,
        name=student.name,
        age=student.age,
        gender=student.gender,
        subject=student.subject,
        marks=student.marks,
    )
    inserted = insert_student(new_student_domain)
    if not inserted:
        raise HTTPException(
            status_code=400,
            detail=f"Student with id {student.student_id} already exists",
        )

    return domain_to_response(new_student_domain)


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student_endpoint(student_id: int, update: StudentUpdate):
    """
    Atualiza um estudante (update parcial).
    Campos não enviados permanecem com o valor anterior.
    """
    existing = get_student_by_id(student_id)
    if existing is None:
        raise HTTPException(status_code=404, detail="Student not found")

    updated_domain = merge_student_update(existing, update)
    updated_ok = update_student(updated_domain)
    if not updated_ok:
        # Em teoria não deveria acontecer, mas deixamos por segurança
        raise HTTPException(status_code=400, detail="Update failed")

    return domain_to_response(updated_domain)


@app.delete("/students/{student_id}")
def delete_student_endpoint(student_id: int):
    """Deleta um estudante pelo ID."""
    deleted = delete_student_by_id(student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": f"Student {student_id} deleted successfully"}
