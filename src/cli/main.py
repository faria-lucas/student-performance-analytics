# src/cli/main.py
from database.models import Student
from database.queries import (create_students_table, 
                              insert_student, 
                              get_all_students, 
                              delete_student_by_id, 
                              get_student_by_id,
                              update_student,
)

from src.analytics.marks_analysis import print_analytics_summary

def show_menu():
    print("\n=== Student Performance CLI ===")
    print("1. Criar/verificar tabela students")
    print("2. Inserir novo estudante")
    print("3. Listar estudantes")
    print("4. Deletar estudante por ID")
    print("5. Atualizar estudante por ID")
    print("6. Ver resumo de analytics")
    print("0. Sair")

def handle_create_table():
    create_students_table()
    print("Tabela 'students' criada/verificada com sucesso.")

def handle_insert_student():
    try:
        student_id = int(input("Student ID: "))
    except ValueError:
        print("ID inválido. Digite um número inteiro.")
        return

    name = input("Nome: ")
    try:
        age = int(input("Idade: "))
    except ValueError:
        print("Idade inválida. Digite um número inteiro.")
        return

    gender = input("Gênero: ")
    subject = input("Disciplina: ")
    try:
        marks = int(input("Nota: "))
    except ValueError:
        print("Nota inválida. Digite um número inteiro.")
        return

    student = Student(
        student_id=student_id,
        name=name,
        age=age,
        gender=gender,
        subject=subject,
        marks=marks,
    )

    inserted = insert_student(student)
    if inserted:
        print("Estudante inserido com sucesso!")
    else:
        print(f"Já existe um estudante com o ID {student_id}. Escolha outro ID.")


def handle_list_students():
    students = get_all_students()
    if not students:
        print("Nenhum estudante cadastrado.")
        return

    print("\nID | Nome | Idade | Gênero | Disciplina | Nota")
    print("-" * 50)
    for s in students:
        print(f"{s.student_id} | {s.name} | {s.age} | {s.gender} | {s.subject} | {s.marks}")

def handle_delete_student():
    try:
        student_id = int(input("Informe o ID do estudante a ser deletado: "))
    except ValueError:
        print("ID inválido. Digite um número inteiro.")
        return

    deleted = delete_student_by_id(student_id)
    if deleted:
        print(f"Estudante com ID {student_id} foi deletado com sucesso.")
    else:
        print(f"Nenhum estudante encontrado com ID {student_id}.")

def handle_show_analytics():
    print_analytics_summary(top_n=5)


def main():
    while True:
        show_menu()
        choice = input("Escolha uma opção: ")

        if choice == "1":
            handle_create_table()
        elif choice == "2":
            handle_insert_student()
        elif choice == "3":
            handle_list_students()
        elif choice == "4":
            handle_delete_student()
        elif choice == "5":
            handle_update_student()
        elif choice == "6":
            handle_show_analytics() 
        elif choice == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def handle_update_student():
    try:
        student_id = int(input("Informe o ID do estudante a ser atualizado: "))
    except ValueError:
        print("ID inválido. Digite um número inteiro.")
        return

    existing = get_student_by_id(student_id)
    if existing is None:
        print(f"Nenhum estudante encontrado com ID {student_id}.")
        return

    print("\nDados atuais do estudante:")
    print(f"ID: {existing.student_id}")
    print(f"Nome: {existing.name}")
    print(f"Idade: {existing.age}")
    print(f"Gênero: {existing.gender}")
    print(f"Disciplina: {existing.subject}")
    print(f"Nota: {existing.marks}")

    print("\nDigite os novos valores. Deixe em branco para manter o valor atual.\n")

    # Nome
    new_name = input(f"Nome [{existing.name}]: ").strip()
    if not new_name:
        new_name = existing.name

    # Idade
    new_age_input = input(f"Idade [{existing.age}]: ").strip()
    if not new_age_input:
        new_age = existing.age
    else:
        try:
            new_age = int(new_age_input)
        except ValueError:
            print("Idade inválida. Mantendo valor atual.")
            new_age = existing.age

    # Gênero
    new_gender = input(f"Gênero [{existing.gender}]: ").strip()
    if not new_gender:
        new_gender = existing.gender

    # Disciplina
    new_subject = input(f"Disciplina [{existing.subject}]: ").strip()
    if not new_subject:
        new_subject = existing.subject

    # Nota
    new_marks_input = input(f"Nota [{existing.marks}]: ").strip()
    if not new_marks_input:
        new_marks = existing.marks
    else:
        try:
            new_marks = int(new_marks_input)
        except ValueError:
            print("Nota inválida. Mantendo valor atual.")
            new_marks = existing.marks

    updated_student = Student(
        student_id=existing.student_id,
        name=new_name,
        age=new_age,
        gender=new_gender,
        subject=new_subject,
        marks=new_marks,
    )

    updated = update_student(updated_student)
    if updated:
        print(f"Estudante com ID {student_id} atualizado com sucesso.")
    else:
        print("Nenhuma alteração foi aplicada.")

if __name__ == "__main__":
    main()
