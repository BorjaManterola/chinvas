from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.prerequisite import Prerequisite
from app.models.course import Course

prerequisite_bp = Blueprint('prerequisite_routes', __name__, url_prefix='/prerequisites')


@prerequisite_bp.route('/course/<int:course_id>/new', methods=['GET'])
def new_prerequisite_form(course_id):
    course = Course.query.get_or_404(course_id)
    all_courses = Course.query.filter(Course.id != course_id).all()
    return render_template('prerequisites/form.html', course=course, all_courses=all_courses, prerequisite=None)


@prerequisite_bp.route('/', methods=['POST'])
def create_prerequisite():
    course_id = request.form.get('course_id')
    prerequisite_id = request.form.get('prerequisite_id')

    if not course_id or not prerequisite_id:
        flash("All fields are required.", "danger")
        course = Course.query.get_or_404(course_id)
        all_courses = Course.query.filter(Course.id != course_id).all()
        return render_template('prerequisites/form.html', course=course, all_courses=all_courses, prerequisite=None)

    if course_id == prerequisite_id:
        flash("A course cannot be its own prerequisite.", "danger")
        return redirect(url_for('course_routes.show_course', id=course_id))

    exists = Prerequisite.query.get((course_id, prerequisite_id))
    if exists:
        flash("This prerequisite already exists.", "warning")
        return redirect(url_for('course_routes.show_course', id=course_id))

    prereq = Prerequisite(course_id=course_id, prerequisite_id=prerequisite_id)
    db.session.add(prereq)
    db.session.commit()
    flash("Prerequisite added successfully.", "success")
    return redirect(url_for('course_routes.show_course', id=course_id))


@prerequisite_bp.route('/<int:course_id>/<int:prerequisite_id>', methods=['GET'])
def show_prerequisite(course_id, prerequisite_id):
    prereq = Prerequisite.query.get_or_404((course_id, prerequisite_id))
    return render_template('prerequisites/show.html', prerequisite=prereq)


@prerequisite_bp.route('/<int:course_id>/<int:prerequisite_id>/delete', methods=['POST'])
def delete_prerequisite(course_id, prerequisite_id):
    prereq = Prerequisite.query.get_or_404((course_id, prerequisite_id))
    db.session.delete(prereq)
    db.session.commit()
    flash("Prerequisite removed successfully.", "success")
    return redirect(url_for('course_routes.show_course', id=course_id))
