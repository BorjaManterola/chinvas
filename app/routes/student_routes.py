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

    student = Student(name=name, email=email, entry_date=entry_date)
    db.session.add(student)
    db.session.commit()
    return redirect(url_for("student_routes.get_students"))


@student_bp.route("/", methods=["GET"])
def get_students():
    students = Student.query.all()
    return render_template("students/index.html", students=students)


@student_bp.route("/<int:id>", methods=["GET"])
def show_student(id):
    student = Student.query.get_or_404(id)
    return render_template("students/show.html", student=student)


@student_bp.route("/<int:id>/edit", methods=["GET"])
def edit_student_form(id):
    student = Student.query.get_or_404(id)
    return render_template("students/form.html", student=student)


@student_bp.route("/<int:id>/edit", methods=["POST"])
def update_student(id):
    student = Student.query.get_or_404(id)
    student.name = request.form.get("name")
    student.email = request.form.get("email")
    student.entry_date = request.form.get("entry_date")
    db.session.commit()
    return redirect(url_for("student_routes.get_students"))


@student_bp.route("/<int:id>/delete", methods=["POST"])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for("student_routes.get_students"))
