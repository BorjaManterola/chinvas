from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.models.schedule import Schedule
from app import db

schedule_bp = Blueprint('schedule_routes', __name__, url_prefix='/schedules')

@schedule_bp.route('/form', methods=['GET'])
def new_schedule_form():
    return render_template('schedules/form.html', schedule=None)

@schedule_bp.route('/', methods=['POST'])
def create_schedule():
    if request.is_json:
        data = request.get_json()
        year = data.get('year')
        semester = data.get('semester')
    else:
        year = request.form.get('year')
        semester = request.form.get('semester')

    if not year or not semester:
        flash("All fields are required.", "danger")
        return render_template("schedules/form.html", schedule=None)

    try:
        year = int(year)
    except ValueError:
        flash("Year must be a number.", "danger")
        return render_template("schedules/form.html", schedule=None)

    schedule = Schedule(year=year, semester=semester)
    db.session.add(schedule)
    db.session.commit()

    if request.is_json:
        return jsonify({'message': 'Schedule created', 'id': schedule.id}), 201

    return redirect(url_for('schedule_routes.get_schedules'))


@schedule_bp.route('/', methods=['GET'])
def get_schedules():
    year = request.args.get('year', type=int)
    if year:
        schedules = Schedule.query.filter_by(year=year).all()
    else:
        schedules = Schedule.query.all()
    return render_template('schedules/index.html', schedules=schedules)

@schedule_bp.route('/<int:id>', methods=['GET'])
def show_schedule(id):
    schedule = Schedule.query.get_or_404(id)
    return render_template('schedules/show.html', schedule=schedule)

@schedule_bp.route('/<int:id>/form', methods=['GET'])
def edit_schedule_form(id):
    schedule = Schedule.query.get_or_404(id)
    return render_template('schedules/form.html', schedule=schedule)

@schedule_bp.route('/<int:id>', methods=['POST'])
def update_schedule(id):
    schedule = Schedule.query.get_or_404(id)

    if request.is_json:
        data = request.get_json()
        year = data.get('year')
        semester = data.get('semester')
    else:
        year = request.form.get('year')
        semester = request.form.get('semester')

    try:
        schedule.year = int(year)
    except (ValueError, TypeError):
        flash("Year must be a number.", "danger")
        return render_template("schedules/form.html", schedule=schedule)

    schedule.semester = semester
    db.session.commit()

    if request.is_json:
        return jsonify({'message': 'Schedule updated'}), 200

    return redirect(url_for('schedule_routes.show_schedule', id=schedule.id))

@schedule_bp.route('/<int:id>/delete', methods=['POST'])
def delete_schedule(id):
    schedule = Schedule.query.get_or_404(id)
    db.session.delete(schedule)
    db.session.commit()
    flash("Schedule deleted successfully.", "success")
    return redirect(url_for('schedule_routes.get_schedules'))
