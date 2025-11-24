# src/analytics/marks_analysis.py
from typing import Dict, List
from statistics import mean

from database.models import Student
from database.queries import get_all_students


def group_students_by_subject(students: List[Student]) -> Dict[str, List[Student]]:
    """
    Agrupa estudantes por disciplina (subject).
    Retorna um dicionário: { "Math": [Student, Student, ...], ... }
    """
    grouped: Dict[str, List[Student]] = {}
    for student in students:
        grouped.setdefault(student.subject, []).append(student)
    return grouped


def calculate_average_marks_by_subject() -> Dict[str, float]:
    """
    Calcula a média de notas por disciplina.
    Retorna: { "Math": 82.5, "English": 74.0, ... }
    """
    students = get_all_students()
    if not students:
        return {}

    grouped = group_students_by_subject(students)
    averages: Dict[str, float] = {}

    for subject, subject_students in grouped.items():
        marks = [s.marks for s in subject_students]
        averages[subject] = round(mean(marks), 2)

    return averages


def get_top_students(limit: int = 5) -> List[Student]:
    """
    Retorna os top N estudantes com base nas notas (marks).
    Se houver notas iguais, a ordem entre eles não é garantida.
    """
    students = get_all_students()
    sorted_students = sorted(students, key=lambda s: s.marks, reverse=True)
    return sorted_students[:limit]


def get_overall_mark_stats() -> Dict[str, float]:
    """
    Retorna estatísticas gerais das notas:
    - média
    - mínimo
    - máximo
    """
    students = get_all_students()
    if not students:
        return {}

    marks = [s.marks for s in students]
    return {
        "count": len(marks),
        "average": round(mean(marks), 2),
        "min": min(marks),
        "max": max(marks),
    }


def print_analytics_summary(top_n: int = 5) -> None:
    """
    Imprime um resumo simples de analytics no terminal.
    Útil para testar o módulo isoladamente.
    """
    print("\n=== Analytics: Estatísticas de Notas ===")

    overall = get_overall_mark_stats()
    if not overall:
        print("Nenhum estudante cadastrado. Não há dados para análise.")
        return

    print(f"Total de estudantes: {overall['count']}")
    print(f"Média geral de notas: {overall['average']}")
    print(f"Nota mínima: {overall['min']}")
    print(f"Nota máxima: {overall['max']}")

    print("\nMédia de notas por disciplina:")
    averages = calculate_average_marks_by_subject()
    for subject, avg in averages.items():
        print(f" - {subject}: {avg}")

    print(f"\nTop {top_n} estudantes por nota:")
    top_students = get_top_students(limit=top_n)
    for idx, s in enumerate(top_students, start=1):
        print(f" {idx}. {s.name} ({s.subject}) - {s.marks} pontos")


if __name__ == "__main__":
    # permite rodar direto:
    # uv run python -m src.analytics.marks_analysis
    print_analytics_summary(top_n=5)
