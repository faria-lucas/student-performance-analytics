# src/cli/main.py
from database.models import Student
from database.queries import create_students_table, insert_student, get_all_students, delete_student_by_id

def show_menu():
    print("\n=== Student Performance CLI ===")
    print("1. Criar/verificar tabela students")
    print("2. Inserir novo estudante")
    print("3. Listar estudantes")
    print("4. Deletar estudante por ID")
    print("0. Sair")

def handle_create_table():
    create_students_table()
    print("Tabela 'students' criada/verificada com sucesso.")

def handle_insert_student():
    student_id = int(input("Student ID: "))
    name = input("Nome: ")
    age = int(input("Idade: "))
    gender = input("Gênero: ")
    subject = input("Disciplina: ")
    marks = int(input("Nota: "))

    student = Student(
        student_id=student_id,
        name=name,
        age=age,
        gender=gender,
        subject=subject,
        marks=marks,
    )
    insert_student(student)
    print("Estudante inserido com sucesso!")

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
        elif choice == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
