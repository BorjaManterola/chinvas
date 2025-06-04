from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from app import db
from app.models.course import Course
from app.models.prerequisite import Prerequisite

course_bp = Blueprint("course_routes", __name__, url_prefix="/courses")


@course_bp.route("/new", methods=["GET"])
def new_course_form():
    return render_template("courses/form.html", course=None)


@course_bp.route("/new", methods=["POST"])
def create_course():
    if request.is_json:
        data = request.get_json()
        name = data.get("name")
        code = data.get("code")
        credits = data.get("credits")
    else:
        name = request.form.get("name")
        code = request.form.get("code")
        credits = request.form.get("credits")

    if not name or not code or not credits:
        return render_template("courses/form.html", course=None)

    try:
        credits = int(credits)
    except ValueError:
        return render_template("courses/form.html", course=None)

    course = Course(name=name, code=code, credits=credits)
    db.session.add(course)
    db.session.commit()

    if request.is_json:
        return jsonify({"message": "Course created", "id": course.id}), 201

    return redirect(url_for("course_routes.get_courses"))

@course_bp.route("/", methods=["GET"])
def get_courses():
    courses = Course.query.all()
    return render_template("courses/index.html", courses=courses)


@course_bp.route("/<int:id>/show", methods=["GET"])
def show_course(id):
    course = Course.query.get_or_404(id)
    prerequisites = (
        db.session.query(Prerequisite, Course)
        .join(Course, Prerequisite.prerequisite_id == Course.id)
        .filter(Prerequisite.course_id == id)
        .all()
    )
    return render_template(
        "courses/show.html", course=course, prerequisites=prerequisites
    )


@course_bp.route("/<int:id>/edit", methods=["GET"])
def edit_course_form(id):
    course = Course.query.get_or_404(id)
    return render_template("courses/form.html", course=course)


@course_bp.route("/<int:id>/edit", methods=["POST"])
def update_course(id):
    course = Course.query.get_or_404(id)
    course.name = request.form["name"]
    course.code = request.form["code"]
    try:
        course.credits = int(request.form["credits"])
    except ValueError:
        return render_template("courses/form.html", course=course)

    db.session.commit()
    return redirect(url_for("course_routes.get_courses"))


@course_bp.route("/<int:id>/delete", methods=["POST"])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for("course_routes.get_courses"))
