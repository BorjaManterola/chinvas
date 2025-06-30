from flask import Blueprint, redirect, render_template, request, url_for

from app import db
from app.models.student import Student

student_bp = Blueprint("student_routes", __name__, url_prefix="/students")


@student_bp.route("/new", methods=["GET"])
def new_student_form():
    return render_template("students/form.html", student=None)


@student_bp.route("/new", methods=["POST"])
def create_student():
    name = request.form.get("name")
    email = request.form.get("email")
    entry_date = request.form.get("entry_date")

    if not name or not email:
        return render_template("students/form.html", student=None)

    if Student.get_student_by_email(email):
        return render_template(
            "students/form.html",
            student=None,
            error="Email already exists."
        )

    student = Student(name=name, email=email, entry_date=entry_date)
    db.session.add(student)
    db.session.commit()
    return redirect(url_for("student_routes.students_index"))


@student_bp.route("/", methods=["GET"])
def students_index():
    students = Student.get_all_students()
    return render_template("students/index.html", students=students)


@student_bp.route("/<int:id>", methods=["GET"])
def show_student(id):
    student = Student.get_student_by_id(id)
    return render_template("students/show.html", student=student)


@student_bp.route("/<int:id>/edit", methods=["GET"])
def edit_student_form(id):
    student = Student.get_student_by_id(id)
    return render_template("students/form.html", student=student)


@student_bp.route("/<int:id>/edit", methods=["POST"])
def update_student(id):
    name = request.form.get("name")
    email = request.form.get("email")
    entry_date = request.form.get("entry_date")

    student = Student.get_student_by_id(id)
    student.name = name
    student.email = email
    student.entry_date = entry_date
    db.session.commit()
    return redirect(url_for("student_routes.students_index"))


@student_bp.route("/<int:id>/delete", methods=["POST"])
def delete_student(id):
    student = Student.get_student_by_id(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for("student_routes.students_index"))

@student_bp.route("/students/<int:student_id>/history", methods=["GET"])
def download_student_history(student_id):
    return Student.export_academic_history(student_id)
