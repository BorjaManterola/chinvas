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



def test_calculate_user_grade_in_assessment_all_tasks_scored():
    ss = StudentSituation(section_id=1, student_id=1)
    assessment = MagicMock()

    task1 = MagicMock()
    task1.is_optional.return_value = False
    task1.get_weighting.return_value = 2.0
    task1.id = 1

    task2 = MagicMock()
    task2.is_optional.return_value = False
    task2.get_weighting.return_value = 3.0
    task2.id = 2

    grade1 = MagicMock()
    grade1.task_id = 1
    grade1.get_score.return_value = 5.0

    grade2 = MagicMock()
    grade2.task_id = 2
    grade2.get_score.return_value = 3.0

    ss.get_assessment_tasks = lambda x: [task1, task2]
    ss.get_user_grades_in_asessment = lambda x: [grade1, grade2]

    final = ss.calculate_user_grade_in_assessment(assessment)
    expected = (5.0*2 + 3.0*3) / (2+3)
    assert final == expected


def test_calculate_user_grade_in_assessment_missing_mandatory_grade_sets_default():
    ss = StudentSituation(section_id=1, student_id=1)
    assessment = MagicMock()

    task = MagicMock()
    task.is_optional.return_value = False
    task.get_weighting.return_value = 4.0
    task.id = 1

    grade = MagicMock()
    grade.task_id = 1
    grade.get_score.return_value = None

    def set_default_score():
        grade.get_score.return_value = 1.0
    grade.set_default_score.side_effect = set_default_score

    ss.get_assessment_tasks = lambda x: [task]
    ss.get_user_grades_in_asessment = lambda x: [grade]

    final = ss.calculate_user_grade_in_assessment(assessment)
    expected = 1.0
    assert final == expected
    grade.set_default_score.assert_called_once()



def test_calculate_user_grade_in_assessment_all_optional_and_no_scores():
    ss = StudentSituation(section_id=1, student_id=1)
    assessment = MagicMock()

    task = MagicMock()
    task.is_optional.return_value = True
    task.get_weighting.return_value = 2.0
    task.id = 1


    grade = MagicMock()
    grade.task_id = 1
    grade.get_score.return_value = None

    ss.get_assessment_tasks = lambda x: [task]
    ss.get_user_grades_in_asessment = lambda x: [grade]

    final = ss.calculate_user_grade_in_assessment(assessment)

    assert final == 0.0


def test_calculate_total_weighting_in_section():
    ss = StudentSituation(section_id=1, student_id=1)
    mock_assessments = [type('A', (), {'weighting': 2.0})(),
                        type('A', (), {'weighting': 3.0})()]
    total = ss.calculate_total_weighting_in_section(mock_assessments)
    assert total == 5.0



def test_get_student_situation_assessments():
    ss = StudentSituation(section_id=1, student_id=1)
    mock_assessments = [MagicMock(), MagicMock()]
    ss.section = MagicMock()
    ss.section.assessments = mock_assessments

    result = ss.get_student_situation_assessments()
    assert result == mock_assessments

def test_get_user_tasks_in_section_calls_get_assessment_tasks(mocker):
    ss = StudentSituation(section_id=1, student_id=1)
    mock_assessments = [MagicMock(), MagicMock()]
    ss.section = MagicMock()
    ss.section.assessments = mock_assessments

    mocker.patch.object(ss, 'get_assessment_tasks', return_value=['task'])

    tasks = ss.get_user_tasks_in_section()
    assert tasks == ['task', 'task']
    assert ss.get_assessment_tasks.call_count == 2

def test_get_user_grades_in_section_calls_get_user_situation_grades_in_asessment(mocker):
    ss = StudentSituation(section_id=1, student_id=1)
    mock_assessments = [MagicMock(), MagicMock()]
    ss.section = MagicMock()
    ss.section.assessments = mock_assessments

    mocker.patch.object(ss, 'get_user_situation_grades_in_asessment', return_value=['grade'])

    grades = ss.get_user_grades_in_section()
    assert grades == ['grade', 'grade']
    assert ss.get_user_situation_grades_in_asessment.call_count == 2


def test_calculate_user_grade_in_assessment_skips_optional_none_score():
    ss = StudentSituation(section_id=1, student_id=1)
    assessment = MagicMock()

    task = MagicMock()
    task.id = 10
    task.is_optional.return_value = True
    task.get_weighting.return_value = 2.0

    grade = MagicMock()
    grade.task_id = 10
    grade.get_score.return_value = None

    ss.get_assessment_tasks = lambda x: [task]
    ss.get_user_grades_in_asessment = lambda x: [grade]

    result = ss.calculate_user_grade_in_assessment(assessment)
    assert result == 0.0  

def test_calculate_user_grade_in_assessment_skips_optional_none_score():
    ss = StudentSituation(section_id=1, student_id=1)
    assessment = MagicMock()

    task = MagicMock()
    task.id = 10
    task.is_optional.return_value = True
    task.get_weighting.return_value = 2.0

    grade = MagicMock()
    grade.task_id = 10
    grade.get_score.return_value = None

    ss.get_assessment_tasks = lambda x: [task]
    ss.get_user_grades_in_asessment = lambda x: [grade]

    result = ss.calculate_user_grade_in_assessment(assessment)
    assert result == 0.0 


def test_calculate_final_grade_discount_weighting_for_zero(mocker):
    ss = StudentSituation(section_id=1, student_id=1)

    assessment1 = MagicMock()
    assessment1.weighting = 3.0
    assessment1.get_assessment_weighting.return_value = 3.0

    assessment2 = MagicMock()
    assessment2.weighting = 2.0
    assessment2.get_assessment_weighting.return_value = 2.0

    ss.section = MagicMock()
    ss.section.assessments = [assessment1, assessment2]

    mocker.patch.object(ss, 'calculate_user_grade_in_assessment', side_effect=[0.0, 5.0])

    final_grade = ss.calculate_final_grade()

    expected = (5.0 * 2.0) / 2.0
    assert final_grade == expected



def test_calculate_user_grade_in_assessment_sets_default_if_missing_mandatory_score():
    ss = StudentSituation(section_id=1, student_id=1)
    assessment = MagicMock()

    task = MagicMock()
    task.id = 1
    task.is_optional.return_value = False
    task.get_weighting.return_value = 2.0

    grade = MagicMock()
    grade.task_id = 1
    grade.get_score.return_value = None

    def set_default():
        grade.get_score.return_value = 1.0
    grade.set_default_score.side_effect = set_default

    ss.get_assessment_tasks = lambda x: [task]
    ss.get_user_grades_in_asessment = lambda x: [grade]

    result = ss.calculate_user_grade_in_assessment(assessment)
    assert result == 1.0 
    grade.set_default_score.assert_called_once()


def test_get_assigned_students_ids_in_section_returns_unique_ids(mocker):
    mock_query = mocker.patch('app.models.student_situation.db.session.query')
    mock_query.return_value.filter_by.return_value.all.return_value = [(1,), (2,), (1,)]

    ids = StudentSituation.get_assigned_students_ids_in_section(10)
    assert ids == {1, 2}


def test_calculate_user_grade_in_assessment_fallback_when_no_weighting():
    ss = StudentSituation(section_id=1, student_id=1)
    assessment = MagicMock()

    ss.get_assessment_tasks = lambda x: []
    ss.get_user_grades_in_asessment = lambda x: []

    result = ss.calculate_user_grade_in_assessment(assessment)
    assert result == 0.0
