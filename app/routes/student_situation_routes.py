from flask import Blueprint, redirect, render_template, request, url_for

from app import db
from app.models.section import Section
from app.models.student import Student
from app.models.student_situation import StudentSituation

student_situation_bp = Blueprint(
    "student_situation_routes", __name__, url_prefix="/student_situations"
)


@student_situation_bp.route("/new", methods=["GET"])
def new_student_situation_form():
    section_id = request.args.get("section_id", type=int)
    section = Section.get_section_by_id(section_id)

    assigned_ids = StudentSituation.get_assigned_students_ids_in_section(
        section_id
    )

    available_students = Student.get_available_students(assigned_ids)

    return render_template(
        "student_situations/form.html",
        section=section,
        students=available_students,
    )


@student_situation_bp.route("/new", methods=["POST"])
def create_student_situations():
    section_id = request.form.get("section_id")
    student_ids = request.form.getlist("student_ids")

    for student_id in student_ids:
        situation_exists = StudentSituation.get_student_situation_by_exact_values(
            section_id=section_id,
            student_id=student_id,
        )
        if not situation_exists:
            situation = StudentSituation(
                student_id=student_id, section_id=section_id
            )
            db.session.add(situation)

    db.session.commit()
    return redirect(url_for("section_routes.show_section", id=section_id))


@student_situation_bp.route("/<int:id>/show", methods=["GET"])
def show_student_situation(id):
    student_situation = StudentSituation.get_student_situation_by_id(id)
    grades = student_situation.get_user_grades_in_section()
    return render_template(
        "student_situations/show.html",
        student_situation=student_situation,
        grades=grades,
    )


@student_situation_bp.route("/<int:id>/edit", methods=["GET"])
def edit_student_situation_form(id):
    situation = StudentSituation.get_student_situation_by_id(id)
    students = Student.get_all_students()
    sections = Section.get_all_sections()
    return render_template(
        "student_situations/form.html",
        situation=situation,
        students=students,
        sections=sections,
    )


@student_situation_bp.route("/<int:id>", methods=["POST"])
def update_student_situation(id):
    student_id = request.form.get("student_id")
    section_id = request.form.get("section_id")
    final_grade = request.form.get("final_grade", None)

    situation = StudentSituation.get_student_situation_by_id(id)
    situation.student_id = student_id
    situation.section_id = section_id
    situation.final_grade = final_grade if final_grade else None
    db.session.commit()

    return redirect(url_for("student_situation_routes.show_student_situation"))


@student_situation_bp.route("/<int:id>/delete", methods=["POST"])
def delete_student_situation(id):
    situation = StudentSituation.get_student_situation_by_id(id)
    section_id = situation.section_id
    db.session.delete(situation)
    db.session.commit()
    return redirect(url_for("section_routes.show_section", id=section_id))
