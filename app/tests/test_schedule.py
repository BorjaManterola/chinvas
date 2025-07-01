import pytest
from unittest.mock import patch, MagicMock
from app.models.schedule import Schedule

def test_validate_inputs_success():
    valid, error = Schedule.validate_inputs("2025", "Fall")
    assert valid is True
    assert error is None


def test_validate_inputs_missing():
    valid, error = Schedule.validate_inputs("", "")
    assert not valid
    assert error == "Year and semester are required."


def test_validate_inputs_non_integer_year():
    valid, error = Schedule.validate_inputs("twenty", "Fall")
    assert not valid
    assert error == "Year must be a number."


def test_build_schedule():
    with patch("app.models.schedule.db.session.add") as mock_add, \
         patch("app.models.schedule.db.session.flush") as mock_flush:
        result = Schedule.build_schedule(2025, "Spring")
        assert isinstance(result, Schedule)
        assert result.year == 2025
        assert result.semester == "Spring"
        mock_add.assert_called_once()
        mock_flush.assert_called_once()