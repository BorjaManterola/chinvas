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
    course = Course.query.get_or_404(course_id)
    assigned_ids = {
        id
        for (id,) in db.session.query(Prerequisite.prerequisite_id)
        .filter_by(course_id=course_id)
        .all()
    }
    all_courses = Course.query.filter(
        Course.id != course_id, ~Course.id.in_(assigned_ids)
    ).all()

    return render_template(
        "prerequisites/form.html", course=course, all_courses=all_courses
    )


@prerequisite_bp.route("/new", methods=["POST"])
def create_prerequisites():
    course_id = request.form.get("course_id")
    prereq_ids = request.form.getlist("prereq_ids")
    created = False
    for prereq_id in prereq_ids:
        exists = Prerequisite.query.filter_by(
            course_id=course_id, prerequisite_id=prereq_id
        ).first()

        if not exists:
            prereq = Prerequisite(
                course_id=course_id, prerequisite_id=prereq_id
            )
            db.session.add(prereq)
            db.session.commit()

    return redirect(url_for("course_routes.showCourse", id=course_id))


@prerequisite_bp.route("/<int:id>/delete", methods=["POST"])
def delete_prerequisite(id):
    prereq = Prerequisite.query.get_or_404(id)
    course_id = prereq.course_id

    db.session.delete(prereq)
    db.session.commit()

    return redirect(url_for("course_routes.showCourse", id=course_id))
