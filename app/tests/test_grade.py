from unittest.mock import patch, MagicMock
from app.models import grade


def test_get_grade_by_id():
    with patch("app.models.grade.Grade.get_grade_by_id", return_value="FakeGrade") as mock_method:
        result = grade.Grade.get_grade_by_id(10)
        mock_method.assert_called_once_with(10)
        assert result == "FakeGrade"


def test_get_grades_by_task_id():
    with patch("app.models.grade.Grade.get_grades_by_task_id", return_value=["G1", "G2"]) as mock_method:
        result = grade.Grade.get_grades_by_task_id(5)
        mock_method.assert_called_once_with(5)
        assert result == ["G1", "G2"]


def test_get_grade_by_student_id_and_task_id():
    with patch("app.models.grade.Grade.get_grade_by_student_id_and_task_id", return_value="G42") as mock_method:
        result = grade.Grade.get_grade_by_student_id_and_task_id(1, 99)
        mock_method.assert_called_once_with(1, 99)
        assert result == "G42"


def test_get_score():
    g = grade.Grade(score=7.0)
    assert g.get_score() == 7.0


def test_set_default_score():
    g = grade.Grade(score=None)
    g.set_default_score()
    assert g.score == 1.0
