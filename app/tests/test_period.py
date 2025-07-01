from unittest.mock import patch, MagicMock
from app.models import period


def test_get_period_by_id():
    with patch("app.models.period.Period.get_period_by_id", return_value="FakePeriod") as mock_method:
        result = period.Period.get_period_by_id(1)
        mock_method.assert_called_once_with(1)
        assert result == "FakePeriod"


def test_get_all_periods():
    with patch("app.models.period.Period.get_all_periods", return_value=["P1", "P2"]) as mock_method:
        result = period.Period.get_all_periods()
        mock_method.assert_called_once()
        assert result == ["P1", "P2"]


def test_get_period_by_exact_values():
    with patch("app.models.period.Period.get_period_by_exact_values", return_value="MatchedPeriod") as mock_method:
        result = period.Period.get_period_by_exact_values(10, 2025, "2")
        mock_method.assert_called_once_with(10, 2025, "2")
        assert result == "MatchedPeriod"


def test_set_students_final_grades():
    situation_mock = MagicMock()
    section_mock = MagicMock()
    section_mock.student_situations = [situation_mock]
    p = period.Period(sections=[section_mock])

    p.set_students_final_grades()

    situation_mock.set_user_situation_final_grade.assert_called_once()
