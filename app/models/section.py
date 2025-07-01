import io

from flask import send_file
from openpyxl import Workbook

from app import db


class Section(db.Model):
    __tablename__ = "sections"
    id = db.Column(db.Integer, primary_key=True)
    period_id = db.Column(
        db.Integer,
        db.ForeignKey("periods.id", ondelete="CASCADE"),
        nullable=False,
    )
    teacher_id = db.Column(
        db.Integer,
        db.ForeignKey("teachers.id", ondelete="CASCADE"),
        nullable=False,
    )
    type_evaluate = db.Column(db.String(50))
    created_at = db.Column(
        db.DateTime, server_default=db.func.current_timestamp()
    )

    assessments = db.relationship(
        "Assessment",
        backref="section",
        lazy=True,
        cascade="all, delete-orphan",
    )
    student_situations = db.relationship(
        "StudentSituation",
        backref="section",
        lazy=True,
        cascade="all, delete-orphan",
    )
    teacher = db.relationship(
        "Teacher",
        backref=db.backref("sections", cascade="all, delete", lazy=True),
    )

    def get_section_students(self):
        return [ss.student for ss in self.student_situations]

    @staticmethod
    def get_section_by_id(id):
        section = Section.query.get_or_404(id)
        return section

    @staticmethod
    def get_all_sections():
        sections = Section.query.all()
        return sections

    def get_section_assessments(self):
        return self.assessments

    def get_section_student_situations(self):
        return self.student_situations

    def export_final_grades_to_excel(self):
        try:
            data_rows = self._build_final_grades_excel_rows()
        except Exception as e:
            raise RuntimeError(f"Error building Excel rows: {str(e)}")

        wb = Workbook()
        ws = wb.active
        ws.title = "Final Grades"

        headers = ["Student ID", "Student Name", "Final Grade"]
        ws.append(headers)

        for row in data_rows:
            ws.append(row)

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=f"section_{self.id}_final_grades.xlsx"
        )

    def _build_final_grades_excel_rows(self):
        rows = []
        situations = self.get_section_student_situations()
        for sit in situations:
            student = sit.student
            rows.append([
                student.id,
                student.name,
                sit.final_grade if sit.final_grade is not None else "N/A"
            ])