from app import db
from app.models.grade import Grade
from app.models.task import Task


class StudentSituation(db.Model):
    __tablename__ = "student_situations"
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(
        db.Integer,
        db.ForeignKey("sections.id", ondelete="CASCADE"),
        nullable=False,
    )
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id", ondelete="CASCADE"),
        nullable=False,
    )
    final_grade = db.Column(db.Numeric(2, 1))

    @staticmethod
    def get_assessment_tasks(assessment):
        tasks = (
            db.session.query(Task).filter_by(assessment_id=assessment.id).all()
        )
        return tasks

    def get_user_tasks_in_section(self):
        tasks = []
        for assessment in self.section.assessments:
            tasks += self.get_assessment_tasks(assessment)
        return tasks

    def get_user_grades_in_section(self):
        grades = (
            db.session.query(Grade).filter_by(student_id=self.student_id).all()
        )
        return grades
