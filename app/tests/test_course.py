from unittest.mock import patch
from app.models import course


def test_get_unassigned_courses():
    with patch("app.models.course.Course.get_unassigned_courses", return_value=["C1", "C2"]) as mock_method:
        result = course.Course.get_unassigned_courses(1, [3, 4])
        mock_method.assert_called_once_with(1, [3, 4])
        assert result == ["C1", "C2"]


def test_get_course_by_id():
    with patch("app.models.course.Course.get_course_by_id", return_value="FakeCourse") as mock_method:
        result = course.Course.get_course_by_id(42)
        mock_method.assert_called_once_with(42)
        assert result == "FakeCourse"


def test_get_all_courses():
    with patch("app.models.course.Course.get_all_courses", return_value=["C1", "C2"]) as mock_method:
        result = course.Course.get_all_courses()
        mock_method.assert_called_once()
        assert result == ["C1", "C2"]


def test_get_course_by_code():
    with patch("app.models.course.Course.get_course_by_code", return_value="CourseABC") as mock_method:
        result = course.Course.get_course_by_code("ING101")
        mock_method.assert_called_once_with("ING101")
        assert result == "CourseABC"
