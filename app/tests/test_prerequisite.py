from unittest.mock import patch, MagicMock
from app.models import prerequisite


def test_get_prerequisite_by_id():
    with patch("app.models.prerequisite.Prerequisite.get_prerequisite_by_id", return_value="FakePrereq") as mock_method:
        result = prerequisite.Prerequisite.get_prerequisite_by_id(42)
        mock_method.assert_called_once_with(42)
        assert result == "FakePrereq"


def test_get_assigned_courses_ids():
    fake_ids = [(1,), (2,), (3,)]
    mock_query = MagicMock()
    mock_query.filter_by.return_value.all.return_value = fake_ids

    with patch("app.models.prerequisite.db.session.query", return_value=mock_query):
        result = prerequisite.Prerequisite.get_assigned_courses_ids(10)
        assert result == {1, 2, 3}
        mock_query.filter_by.assert_called_once_with(course_id=10)
