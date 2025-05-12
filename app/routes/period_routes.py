from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models.period import Period
from app.models.course import Course
from app.models.section import Section

from app import db

period_bp = Blueprint('period_routes', __name__, url_prefix='/periods')


@period_bp.route('/new', methods=['GET'])
def new_period_form():
    course_id = request.args.get('course_id', type=int)
    course = Course.query.get(course_id) if course_id else None
    return render_template('periods/form.html', period=None, course=course)


@period_bp.route('/', methods=['POST'])
def create_period():
    year = request.form['year']
    semester = request.form['semester']
    course_id = request.form['course_id']

    try:
        year = int(year)
    except ValueError:
        flash("Year must be a number.", "danger")
        course = Course.query.get(course_id)
        return render_template('periods/form.html', period=None, course=course)

    period = Period(year=year, semester=semester, course_id=course_id)
    db.session.add(period)
    db.session.commit()

    return redirect(url_for('course_routes.show_course', id=course_id))


@period_bp.route('/', methods=['GET'])
def list_periods():
    periods = Period.query.all()
    return render_template('periods/index.html', periods=periods)


@period_bp.route('/<int:id>/show', methods=['GET'])
def show_period(id):
    period = Period.query.get_or_404(id)
    return render_template('periods/show.html', period=period)


@period_bp.route('/<int:id>/edit', methods=['GET'])
def edit_period_form(id):
    period = Period.query.get_or_404(id)
    return render_template('periods/form.html', period=period, course=period.course)


@period_bp.route('/<int:id>', methods=['POST'])
def update_period(id):
    period = Period.query.get_or_404(id)
    try:
        period.year = int(request.form['year'])
    except ValueError:
        flash("Year must be a number.", "danger")
        return render_template('periods/form.html', period=period, course=period.course)

    period.semester = request.form['semester']
    db.session.commit()
    return redirect(url_for('course_routes.show_course', id=period.course_id))


@period_bp.route('/<int:id>/delete', methods=['POST'])
def delete_period(id):
    period = Period.query.get_or_404(id)
    course_id = period.course_id
    db.session.delete(period)
    db.session.commit()
    return redirect(url_for('course_routes.show_course', id=course_id))

@period_bp.route('/periods/<int:id>/close', methods=['POST'])
def close_period(id):
    period = Period.query.get_or_404(id)
    period.opened = False
    db.session.commit()
    flash('The period has been closed successfully.', 'success')
    return redirect(url_for('period_routes.show_period', id=id))