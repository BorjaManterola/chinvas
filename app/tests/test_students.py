from unittest.mock import patch
from app.models import student


def test_get_student_by_id():
    with patch("app.models.student.Student.get_student_by_id", return_value="FakeStudent") as mock_method:
        result = student.Student.get_student_by_id(1)
        mock_method.assert_called_once_with(1)
        assert result == "FakeStudent"


def test_get_all_students():
    with patch("app.models.student.Student.get_all_students", return_value=["S1", "S2"]) as mock_method:
        result = student.Student.get_all_students()
        mock_method.assert_called_once()
        assert result == ["S1", "S2"]


def test_get_available_students():
    with patch("app.models.student.Student.get_available_students", return_value=["AvailableStudent"]) as mock_method:
        result = student.Student.get_available_students([1, 2])
        mock_method.assert_called_once_with([1, 2])
        assert result == ["AvailableStudent"]


def test_get_student_by_email():
    with patch("app.models.student.Student.get_student_by_email", return_value="MailStudent") as mock_method:
        result = student.Student.get_student_by_email("test@example.com")
        mock_method.assert_called_once_with("test@example.com")
        assert result == "MailStudent"
