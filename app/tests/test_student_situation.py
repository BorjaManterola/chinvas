from unittest.mock import patch, MagicMock
from app.models.student_situation import StudentSituation

def test_get_student_situation_by_exact_values():
    mock_query = MagicMock()
    mock_filter = mock_query.filter_by.return_value
    mock_filter.first.return_value = "ExactSituation"

    with patch("app.models.student_situation.db.session.query", return_value=mock_query):
        result = StudentSituation.get_student_situation_by_exact_values(1, 2)
        mock_query.filter_by.assert_called_once_with(section_id=1, student_id=2)
        assert result == "ExactSituation"


def test_get_assigned_students_ids_in_section():
    mock_query = MagicMock()
    mock_query.filter_by.return_value.all.return_value = [(1,), (2,), (3,)]

    with patch("app.models.student_situation.db.session.query", return_value=mock_query):
        result = StudentSituation.get_assigned_students_ids_in_section(5)
        assert result == {1, 2, 3}


def test_calculate_user_grade_in_assessment():
    task = MagicMock()
    task.get_weighting.return_value = 1
    task.is_optional.return_value = False
    task.id = 10

    grade = MagicMock()
    grade.get_score.return_value = 6.0
    grade.task_id = 10

    assessment = MagicMock()
    assessment.tasks = [task]

    situation = StudentSituation()
    situation.student_id = 1
    situation.get_assessment_tasks = MagicMock(return_value=[task])
    situation.get_user_grades_in_asessment = MagicMock(return_value=[grade])

    result = situation.calculate_user_grade_in_assessment(assessment)

    assert result == 6.0
