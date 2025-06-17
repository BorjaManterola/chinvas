from flask import Blueprint, redirect, render_template, request, url_for

from app import db
from app.models.course import Course
from app.models.prerequisite import Prerequisite

prerequisite_bp = Blueprint(
    "prerequisite_routes", __name__, url_prefix="/prerequisites"
)


@prerequisite_bp.route("/new", methods=["GET"])
def new_prerequisite_form():
    course_id = request.args.get("course_id", type=int)

    course = Course.get_course_by_id(course_id)
    assigned_courses_ids = Prerequisite.get_assigned_courses_ids(course_id)

    all_courses = Course.get_unassigned_courses(
        course_id, assigned_courses_ids
    )

    return render_template(
        "prerequisites/form.html", course=course, all_courses=all_courses
    )


@prerequisite_bp.route("/new", methods=["POST"])
def create_prerequisites():
    course_id = request.form.get("course_id")
    prereq_ids = request.form.getlist("prereq_ids")

    for prereq_id in prereq_ids:
        exist_prerequisite = Prerequisite.get_prerequisite_by_exact_values(
            prereq_id, course_id
        )

        if not exist_prerequisite:
            prereq = Prerequisite(
                course_id=course_id, prerequisite_id=prereq_id
            )
            db.session.add(prereq)

    db.session.commit()

    return redirect(url_for("course_routes.show_course", id=course_id))


@prerequisite_bp.route("/<int:id>/delete", methods=["POST"])
def delete_prerequisite(id):
    prereq = Prerequisite.get_prerequisite_by_id(id)
    if not prereq:
        return redirect(url_for("course_routes.get_courses"))
    course_id = prereq.course_id

    db.session.delete(prereq)
    db.session.commit()

    return redirect(url_for("course_routes.show_course", id=course_id))
