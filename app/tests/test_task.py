from unittest.mock import patch, MagicMock
from app.models.task import Task

def test_is_optional_true():
    task = Task(optional=True)
    assert task.is_optional() is True


def test_is_optional_false():
    task = Task(optional=False)
    assert task.is_optional() is False


def test_is_valid_weighting_not_percentage():
    task = Task()
    task.assessment = MagicMock(type_evaluate="Absolute")
    is_valid, total_weight = task.is_valid_weighting_in_assessment(50, 0)
    assert is_valid is True
    assert total_weight == 0.0


def test_is_valid_weighting_valid_percentage():
    task = Task()
    task.assessment = MagicMock(id=1, type_evaluate="Percentage")

    with patch.object(Task, "get_sum_weighting_in_assessment", return_value=80.0):
        is_valid, total = task.is_valid_weighting_in_assessment(15.0, 99)
        assert is_valid is True
        assert round(total, 2) == 95.0


def test_is_valid_weighting_invalid_percentage():
    task = Task()
    task.assessment = MagicMock(id=1, type_evaluate="Percentage")

    with patch.object(Task, "get_sum_weighting_in_assessment", return_value=95.0):
        is_valid, total = task.is_valid_weighting_in_assessment(10.0, 99)
        assert is_valid is False
        assert round(total, 2) == 105.0
