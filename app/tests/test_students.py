from app.models.student import Student

def test_student_init():
    student = Student(name="Juan Pérez", email="juan@example.com")
    assert student.name == "Juan Pérez"
    assert student.email == "juan@example.com"

def test_student_str_repr():
    student = Student(name="Pedro Test", email="pedro@test.cl")
    assert str(student)
