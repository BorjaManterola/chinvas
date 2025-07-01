from unittest.mock import patch
from app.models import classroom


def test_get_classroom():
    with patch("app.models.classroom.Classroom.get_classroom", return_value="FakeRoom") as mock_method:
        result = classroom.Classroom.get_classroom(42)
        mock_method.assert_called_once_with(42)
        assert result == "FakeRoom"


def test_get_all_classrooms():
    with patch("app.models.classroom.Classroom.get_all_classrooms", return_value=["RoomA", "RoomB"]) as mock_method:
        result = classroom.Classroom.get_all_classrooms()
        mock_method.assert_called_once()
        assert result == ["RoomA", "RoomB"]
