from flask import Blueprint, redirect, render_template, request, url_for

from app import db
from app.models.period import Period
from app.models.section import Section
from app.models.teacher import Teacher

section_bp = Blueprint("section_routes", __name__, url_prefix="/sections")


@section_bp.route("/new", methods=["GET"])
def new_section_form():
    period_id = request.args.get("period_id", type=int)

    period = Period.get_period_by_id(period_id)
    teachers = Teacher.get_all_teachers()
    return render_template(
        "sections/form.html", section=None, period=period, teachers=teachers
    )


@section_bp.route("/new", methods=["POST"])
def create_section():
    period_id = request.form.get("period_id")
    teacher_id = request.form.get("teacher_id")
    type_evaluate = request.form.get("type_evaluate")

    section = Section(
        period_id=period_id, teacher_id=teacher_id, type_evaluate=type_evaluate
    )
    db.session.add(section)
    db.session.commit()
    return redirect(url_for("period_routes.show_period", id=period_id))


@section_bp.route("/<int:id>", methods=["GET"])
def show_section(id):
    section = Section.get_section_by_id(id)
    assessments = section.get_section_assessments()
    student_situations = section.get_section_student_situations()
    return render_template(
        "sections/show.html",
        section=section,
        assessments=assessments,
        students=student_situations,
    )


@section_bp.route("/<int:id>/edit", methods=["GET"])
def edit_section_form(id):
    section = Section.get_section_by_id(id)
    teachers = Teacher.query.all()
    return render_template(
        "sections/form.html",
        section=section,
        period=section.period,
        teachers=teachers,
    )


@section_bp.route("/<int:id>/edit", methods=["POST"])
def update_section(id):
    teacher_id = request.form.get("teacher_id")
    type_evaluate = request.form.get("type_evaluate")

    section = Section.get_section_by_id(id)

    section.teacher_id = teacher_id
    section.type_evaluate = type_evaluate

    db.session.commit()
    return redirect(url_for("period_routes.show_period", id=section.period_id))


@section_bp.route("/<int:id>/delete", methods=["POST"])
def delete_section(id):
    section = Section.get_section_by_id(id)
    period_id = section.period_id
    db.session.delete(section)
    db.session.commit()
    return redirect(url_for("period_routes.show_period", id=period_id))
