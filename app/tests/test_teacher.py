from unittest.mock import patch
from app.models.teacher import Teacher


def test_get_all_teachers():
    with patch("app.models.teacher.Teacher.get_all_teachers", return_value=["T1", "T2"]) as mock_method:
        result = Teacher.get_all_teachers()
        assert result == ["T1", "T2"]
        mock_method.assert_called_once()


def test_get_teacher_by_id():
    with patch("app.models.teacher.Teacher.get_teacher_by_id", return_value="MockTeacher") as mock_method:
        result = Teacher.get_teacher_by_id(1)
        assert result == "MockTeacher"
        mock_method.assert_called_once_with(1)


def test_get_teacher_by_email():
    with patch("app.models.teacher.Teacher.get_teacher_by_email", return_value="TeacherEmail") as mock_method:
        result = Teacher.get_teacher_by_email("test@example.com")
        assert result == "TeacherEmail"
        mock_method.assert_called_once_with("test@example.com")
