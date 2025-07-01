from unittest.mock import MagicMock, patch
import pytest

from app.models.assessment import Assessment

def test_get_assessment_weighting():
    a = Assessment(weighting=15.0)
    assert a.get_assessment_weighting() == 15.0


def test_get_assessment_tasks(mocker):
    mock_query = mocker.MagicMock()
    mock_query.filter_by.return_value.all.return_value = ["Task1", "Task2"]
    mocker.patch("app.models.assessment.db.session.query", return_value=mock_query)
    result = Assessment.get_assessment_tasks(3)
    assert result == ["Task1", "Task2"]

def test_get_assessment_section(mocker):
    mock_assessment = MagicMock()
    mock_assessment.section_id = 7
    mocker.patch("app.models.assessment.Assessment.get_assessment_by_id", return_value=mock_assessment)
    mock_query = mocker.MagicMock()
    mock_query.get_or_404.return_value = "MockedSection"
    mocker.patch("app.models.assessment.db.session.query", return_value=mock_query)
    result = Assessment.get_assessment_section(8)
    assert result == "MockedSection"
