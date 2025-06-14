import io

from flask import send_file
from openpyxl import Workbook

from app import db


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    optional = db.Column(db.Boolean, default=False)
    weighting = db.Column(db.Float, nullable=False)
    assessment_id = db.Column(
        db.Integer,
        db.ForeignKey("assessments.id", ondelete="CASCADE"),
        nullable=False,
    )

    grades = db.relationship(
        "Grade",
        back_populates="task",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    @staticmethod
    def get_task_by_id(id):
        task = Task.query.get_or_404(id)
        return task

    @staticmethod
    def get_sum_weighting_in_assessment(assessment_id, exclude_task_id):
        sum = db.session.query(db.func.sum(Task.weighting)).filter(
            Task.assessment_id == assessment_id, Task.id != exclude_task_id
        )
        return sum.scalar() or 0.0

    def is_valid_weighting_in_assessment(self, new_weighting, exclude_task_id):
        if self.assessment.type_evaluate != "Percentage":
            return True, 0.0

        weighting_sum = self.get_sum_weighting_in_assessment(
            self.assessment.id, exclude_task_id
        )

        total_weight = weighting_sum + new_weighting
        is_valid_weight = total_weight <= 100 + 1e-5
        return is_valid_weight, total_weight

    @staticmethod
    def export_task_grades_to_excel(task_id):
        from app.models.grade import Grade
        from app.models.student import Student
        task = Task.get_task_by_id(task_id)
        grades = Grade.get_grades_by_task_id(task_id)
        assessment = task.assessment

        wb = Workbook()
        ws = wb.active
        ws.title = "Grades"

        headers = ["Student ID", "Student Name", "Score"]
        ws.append(headers)

        for grade in grades:
            student = Student.get_student_by_id(grade.student_id)
            ws.append([
                student.id,
                student.name,
                grade.score
            ])

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=f"assesment_{assessment.name}_task_{task_id}_grades.xlsx"
        )
