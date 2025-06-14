from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.models.assessment import Assessment
from app.models.section import Section

assessment_bp = Blueprint(
    "assessment_routes", __name__, url_prefix="/assessments"
)


@assessment_bp.route("/new", methods=["GET"])
def new_assessment_form():
    section_id = request.args.get("section_id", type=int)
    section = Section.get_section_by_id(section_id)
    return render_template(
        "assessments/form.html", assessment=None, section=section
    )


@assessment_bp.route("/new", methods=["POST"])
def create_assessment():
    section_id = request.form["section_id"]
    name = request.form["name"]
    type_evaluate = request.form["type_evaluate"]
    weighting = request.form.get("weighting", type=float)
    section = Section.get_section_by_id(section_id)

    assessment = Assessment(
        name=name,
        type_evaluate=type_evaluate,
        weighting=weighting,
        section_id=section_id,
    )

    db.session.add(assessment)
    db.session.flush()

    is_valid, total_weight = assessment.is_valid_weighting_in_section(
        weighting, assessment.id
    )

    if not is_valid:
        flash(
            (
                f"Total weighting would exceed 100%. "
                f"Current total: {total_weight:.2f}%. "
                f"You entered: {weighting:.2f}%."
            ),
            "danger",
        )
        return render_template(
            "assessments/form.html", section=section, assessment=None
        )

    db.session.commit()
    return redirect(url_for("section_routes.show_section", id=section_id))


@assessment_bp.route("/<int:id>", methods=["GET"])
def show_assessment(id):
    assessment = Assessment.get_assessment_by_id(id)
    tasks = Assessment.get_assessment_tasks(id)
    return render_template(
        "assessments/show.html", assessment=assessment, tasks=tasks
    )


@assessment_bp.route("/<int:id>/edit", methods=["GET"])
def edit_assessment_form(id):
    assessment = Assessment.get_assessment_by_id(id)
    section = Assessment.get_assessment_section(id)
    return render_template(
        "assessments/form.html", assessment=assessment, section=section
    )


@assessment_bp.route("/<int:id>/edit", methods=["POST"])
def update_assessment(id):
    assessment = Assessment.get_assessment_by_id(id)
    section = Assessment.get_assessment_section(id)
    name = request.form["name"]
    type_evaluate = request.form["type_evaluate"]
    weighting = request.form.get("weighting", type=float)

    is_valid, total_weight = assessment.is_valid_weighting_in_section(
        weighting, assessment.id
    )

    if not is_valid:
        flash(
            (
                f"Total weighting would exceed 100%. "
                f"Current total: {total_weight:.2f}%. "
                f"You entered: {weighting:.2f}%."
            ),
            "danger",
        )
        return render_template(
            "assessments/form.html", assessment=assessment, section=section
        )

    assessment.name = name
    assessment.type_evaluate = type_evaluate
    assessment.weighting = weighting
    db.session.commit()

    return redirect(url_for("section_routes.show_section", id=section.id))


@assessment_bp.route("/<int:id>/delete", methods=["POST"])
def delete_assessment(id):
    assessment = Assessment.get_assessment_by_id(id)
    for task in assessment.tasks:
        db.session.delete(task)
    db.session.delete(assessment)
    db.session.commit()

    return redirect(
        url_for("section_routes.show_section", id=assessment.section_id)
    )
