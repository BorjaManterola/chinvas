from flask import Blueprint, redirect, render_template, request, url_for

from app import db
from app.models.grade import Grade
from app.models.student import Student
from app.models.task import Task

grade_bp = Blueprint("grade_routes", __name__, url_prefix="/grades")


@grade_bp.route("/new", methods=["GET"])
def new_grade_form():
    student_id = request.args.get("student_id", type=int)
    task_id = request.args.get("task_id", type=int)

    student = Student.query.get_or_404(student_id)
    task = Task.query.get_or_404(task_id)

    return render_template(
        "grades/form.html", grade=None, student=student, task=task
    )


@grade_bp.route("/new", methods=["POST"])
def create_grade():
    student_id = request.form.get("student_id", type=int)
    task_id = request.form.get("task_id", type=int)
    score = request.form.get("score", type=float)

    if score is None:
        return redirect(
            url_for(
                "grade_routes.new_grade_form",
                student_id=student_id,
                task_id=task_id,
            )
        )

    grade = Grade(student_id=student_id, task_id=task_id, score=score)
    db.session.add(grade)
    db.session.commit()

    return redirect(
        url_for("student_situation_routes.show_student_situation", id=student_id)
    )


@grade_bp.route("/<int:id>/edit", methods=["GET"])
def edit_grade_form(id):
    grade = Grade.get_grade_by_id(id)
    student = Student.get_student_by_id(grade.student_id)
    task = Task.get_task_by_id(grade.task_id)

    return render_template(
        "grades/form.html", grade=grade, student=student, task=task
    )


@grade_bp.route("/<int:id>/edit", methods=["POST"])
def update_grade(id):
    grade = Grade.get_grade_by_id(id)
    score = request.form.get("score", type=float)

    if score is None:
        return redirect(url_for("grade_routes.edit_grade_form", id=id))

    grade.score = score
    db.session.commit()

    return redirect(
        url_for(
            "student_situation_routes.show_student_situation",
            id=grade.student_id,
        )
    )


@grade_bp.route("/<int:id>/delete", methods=["POST"])
def delete_grade(id):
    grade = Grade.get_grade_by_id(id)
    student_id = grade.student_id

    db.session.delete(grade)
    db.session.commit()

    return redirect(
        url_for("student_situation_routes.show_student_situation", id=student_id)
    )
