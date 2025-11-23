# database/models.py
from dataclasses import dataclass

@dataclass
class Student:
    student_id: int
    name: str
    age: int
    gender: str
    subject: str
    marks: int
