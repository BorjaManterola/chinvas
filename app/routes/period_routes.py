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


@period_bp.route('/courses', methods=['GET'])
def get_period_courses():
    selected_period = None
    courses = []
    sections = []

    year = request.args.get('year', type=int)
    semester = request.args.get('semester')
    
    if year and semester:
        selected_period = {
            'year': year,
            'semester': semester
        }
        
        matching_periods = Period.query.filter_by(year=year, semester=semester).all()
        
        if matching_periods:
            period_ids = [p.id for p in matching_periods]
            
            courses = Course.query.join(Period).filter(
                Period.id.in_(period_ids)
            ).distinct().all()

            # Aquí obtenemos las secciones de los periodos seleccionados
            sections = Section.query.filter(Section.period_id.in_(period_ids)).all()
    
    return render_template(
        'courses/period.html',
        selected_period=selected_period,
        courses=courses,
        sections=sections
    )


import csv
import random
from flask import send_file, request, Blueprint
from io import BytesIO, StringIO


@period_bp.route('/generate_schedule', methods=['GET'])
def generate_schedule():
    year = request.args.get('year', type=int)
    semester = request.args.get('semester')

    if not year or not semester:
        return "Missing year or semester", 400

    matching_periods = Period.query.filter_by(year=year, semester=semester).all()
    if not matching_periods:
        return "No periods found", 404

    period_ids = [p.id for p in matching_periods]
    sections = Section.query.filter(Section.period_id.in_(period_ids)).all()

    hours = [
        ("09:00", "10:00"), ("10:00", "11:00"), ("11:00", "12:00"),
        ("12:00", "13:00"), ("14:00", "15:00"), ("15:00", "16:00"),
        ("16:00", "17:00"), ("17:00", "18:00")
    ]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    used_slots = set()
    used_professors = set()

    rooms = [f"Room {i}" for i in range(1, 11)]

    # Usamos StringIO para escribir como texto
    text_output = StringIO()
    writer = csv.writer(text_output)
    writer.writerow(["Section ID", "Course ID", "Teacher ID", "Room", "Day", "Start Time", "End Time"])

    for section in sections:
        success = False
        for _ in range(100):
            day = random.choice(days)
            start, end = random.choice(hours)
            room = random.choice(rooms)
            slot = (room, day, start)
            prof_slot = (section.teacher_id, day, start)

            if slot not in used_slots and prof_slot not in used_professors:
                writer.writerow([section.id, section.period.course_id, section.teacher_id, room, day, start, end])
                used_slots.add(slot)
                used_professors.add(prof_slot)
                success = True
                break
        if not success:
            writer.writerow([section.id, section.period.course_id, section.teacher_id, "N/A", "N/A", "N/A", "N/A"])

    # Convertimos el contenido a binario
    binary_output = BytesIO()
    binary_output.write(text_output.getvalue().encode('utf-8'))
    binary_output.seek(0)

    filename = f'schedule_{year}_{semester}.csv'
    return send_file(binary_output, mimetype='text/csv', as_attachment=True, download_name=filename)