from flask import Blueprint, redirect, render_template, request, url_for

from app import db
from app.models.teacher import Teacher

teacher_bp = Blueprint("teacher_routes", __name__, url_prefix="/teachers")


@teacher_bp.route("/new", methods=["GET"])
def new_teacher_form():
    return render_template("teachers/form.html", teacher=None)


@teacher_bp.route("/new", methods=["POST"])
def create_teacher():
    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        return render_template("teachers/form.html", teacher=None)

    teacher = Teacher(name=name, email=email)
    db.session.add(teacher)
    db.session.commit()
    return redirect(url_for("teacher_routes.get_teachers"))


@teacher_bp.route("/", methods=["GET"])
def teachers_index():
    teachers = Teacher.get_all_teachers()
    return render_template("teachers/index.html", teachers=teachers)


@teacher_bp.route("/<int:id>/edit", methods=["GET"])
def edit_teacher_form(id):
    teacher = Teacher.get_teacher_by_id(id)
    return render_template("teachers/form.html", teacher=teacher)


@teacher_bp.route("/<int:id>/edit", methods=["POST"])
def update_teacher(id):
    teacher = Teacher.get_teacher_by_id(id)
    teacher.name = request.form.get("name")
    teacher.email = request.form.get("email")
    db.session.commit()
    return redirect(url_for("teacher_routes.get_teachers"))


@teacher_bp.route("/<int:id>/delete", methods=["POST"])
def delete_teacher(id):
    teacher = Teacher.get_teacher_by_id(id)
    db.session.delete(teacher)
    db.session.commit()
    return redirect(url_for("teacher_routes.get_teachers"))
