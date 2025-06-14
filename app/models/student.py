import io

from flask import send_file
from openpyxl import Workbook

from app import db


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    entry_date = db.Column(db.Date)
    created_at = db.Column(
        db.DateTime, server_default=db.func.current_timestamp()
    )

    grades = db.relationship(
        "Grade", backref="student", cascade="all, delete", lazy=True
    )
    student_situations = db.relationship(
        "StudentSituation", backref="student", cascade="all, delete", lazy=True
    )

    @staticmethod
    def get_student_by_id(id):
        student = Student.query.get_or_404(id)
        return student

    @staticmethod
    def get_all_students():
        students = Student.query.all()
        return students

    @staticmethod
    def get_available_students(assigned_ids):
        students = Student.query.filter(~Student.id.in_(assigned_ids)).all()
        return students

    @staticmethod
    def get_student_by_email(email):
        student = Student.query.filter_by(email=email).first()
        return student

    @staticmethod
    def export_closed_course_grades(student_id):
        student = Student.get_student_by_id(student_id)
        situations = student.student_situations

        wb = Workbook()
        ws = wb.active
        ws.title = "Academic History"

        headers = ["Course", "Instance", "Section", "Year", "Semester", "Final Grade"]
        ws.append(headers)

        for sit in situations:
            if sit.final_grade is None:
                continue
            section = sit.section
            period = section.period
            course = period.course

            ws.append([
                course.name,
                course.code if hasattr(course, 'code') else course.id,
                section.id,
                period.year,
                period.semester,
                sit.final_grade
            ])

        output = io.BytesIO()
        wb.save(output)
        output.seek(0)

        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=f"student_{student.name}_academic_history.xlsx"
        )
