from flask import Blueprint, flash, redirect, render_template, request, url_for

from app import db
from app.models.assessment import Assessment
from app.models.task import Task

task_bp = Blueprint("task_routes", __name__, url_prefix="/tasks")


@task_bp.route("/new", methods=["GET"])
def new_task_form():
    assessment_id = request.args.get("assessment_id", type=int)
    assessment = Assessment.get_assessment_by_id(assessment_id)
    return render_template("tasks/form.html", task=None, assessment=assessment)


@task_bp.route("/new", methods=["POST"])
def create_task():
    assessment_id = request.form["assessment_id"]
    weighting = request.form.get("weighting", type=float)

    assessment = Assessment.get_assessment_by_id(assessment_id)
    optional = "optional" in request.form

    task = Task(
        assessment_id=assessment_id, weighting=weighting, optional=optional
    )

    db.session.add(task)
    db.session.flush()

    is_valid, total_weight = task.is_valid_weighting_in_assessment(
        weighting, task.id
    )
    if not is_valid:
        flash(
            (
                "Total task weighting cannot exceed 100%. "
                f"Current total: {total_weight}%"
            ),
            "danger",
        )
        return redirect(
            url_for(
                "task_routes.new_task_form", assessment=assessment, task=None
            )
        )

    db.session.commit()
    return redirect(
        url_for("assessment_routes.show_assessment", id=assessment_id)
    )


@task_bp.route("/<int:id>/edit", methods=["GET"])
def edit_task_form(id):
    task = Task.get_task_by_id(id)
    assessment = Assessment.query.get_or_404(task.assessment_id)
    return render_template("tasks/form.html", task=task, assessment=assessment)


@task_bp.route("/<int:id>/edit", methods=["POST"])
def update_task(id):
    task = Task.get_task_by_id(id)
    assessment_id = task.assessment_id
    weighting = request.form.get("weighting", type=float)
    optional = "optional" in request.form

    exclude_task_id = id
    is_valid, total_weight = task.is_valid_weighting_in_assessment(
        weighting, exclude_task_id
    )
    if not is_valid:
        flash(
            (
                "Total task weighting cannot exceed 100%. "
                f"Current total: {total_weight}%"
            ),
            "danger",
        )
        return redirect(url_for("task_routes.edit_task_form", id=id))

    task.weighting = weighting
    task.optional = optional
    db.session.commit()

    return redirect(
        url_for("assessment_routes.show_assessment", id=assessment_id)
    )

@task_bp.route("/task/<int:task_id>/report", methods=["GET"])
def download_task_report(task_id):
    return Task.export_task_grades_to_excel(task_id)


@task_bp.route("/<int:id>/delete", methods=["POST"])
def delete_task(id):
    task = Task.get_task_by_id(id)
    assessment_id = task.assessment_id

    db.session.delete(task)
    db.session.commit()

    return redirect(
        url_for("assessment_routes.show_assessment", id=assessment_id)
    )
