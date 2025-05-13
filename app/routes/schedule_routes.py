from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from app.models.schedule import Schedule
from app.models.class_ import Class
from app import db
from app.models.section import Section
from app.models.period import Period
from app.models.course import Course
from app.models.classroom import Classroom

schedule_bp = Blueprint('schedule_routes', __name__, url_prefix='/schedules')

@schedule_bp.route('/form', methods=['GET'])
def newScheduleForm():
    return render_template('schedules/form.html', schedule=None)

@schedule_bp.route('/', methods=['POST'])
def createSchedule():
    if request.is_json:
        data = request.get_json()
        year = data.get("year")
        semester = data.get("semester")
    else:
        year = request.form.get("year")
        semester = request.form.get("semester")

    if not year or not semester:
        flash("Year and semester are required.", "danger")
        return render_template("schedules/form.html", schedule=None)

    try:
        year = int(year)
    except ValueError:
        flash("Year must be a number.", "danger")
        return render_template("schedules/form.html", schedule=None)

    existing = Schedule.query.filter_by(year=year, semester=semester).first()
    if existing:
        flash(f"A schedule for year {year} and semester '{semester}' already exists.", "danger")
        return render_template("schedules/form.html", schedule=None)

    schedule = Schedule(year=year, semester=semester)
    db.session.add(schedule)
    db.session.flush()

    result = schedule.generateSchedule()

    if not result["unassigned_sections"]:
        for c in result["classes_to_create"]:
            new_class = Class(
                section_id=c["section_id"],
                day_of_week=c["day_of_week"],
                start_time=c["start_time"],
                end_time=c["end_time"],
                classroom_id=c["classroom_id"],
                schedule_id=c["schedule_id"]
            )
            db.session.add(new_class)

        db.session.commit()
        try:
            return schedule.exportScheduleToExcel()
        except Exception as e:
            flash(f"Schedule created, but Excel download failed: {str(e)}", "warning")
        return redirect(url_for("schedule_routes.getSchedules"))
    else:
        db.session.rollback()
        msg = ["⚠ Could not generate schedule due to conflicts:"]
        for s in result["unassigned_sections"]:
            msg.append(f"Section {s['section_id']}: {s['reason']}")
        flash("<br>".join(msg), "danger")
        return render_template("schedules/form.html", schedule=None)

@schedule_bp.route('/', methods=['GET'])
def getSchedules():
    year = request.args.get('year', type=int)
    if year:
        schedules = Schedule.query.filter_by(year=year).all()
    else:
        schedules = Schedule.query.all()
    return render_template('schedules/index.html', schedules=schedules)

@schedule_bp.route('/<int:id>', methods=['GET'])
def showSchedule(id):
    schedule = Schedule.query.get_or_404(id)

    classes = db.session.query(Class).\
        join(Section, Class.section_id == Section.id).\
        join(Period, Section.period_id == Period.id).\
        join(Course, Period.course_id == Course.id).\
        join(Classroom, Class.classroom_id == Classroom.id).\
        filter(Class.schedule_id == id).\
        add_columns(
            Class.id.label("class_id"),
            Course.name.label("course_name"),
            Section.id.label("section_id"),
            Classroom.name.label("classroom_name"),
            Class.day_of_week,
            Class.start_time,
            Class.end_time
        ).all()

    return render_template("schedules/show.html", schedule=schedule, classes=classes)

@schedule_bp.route('/<int:id>/form', methods=['GET'])
def editScheduleForm(id):
    schedule = Schedule.query.get_or_404(id)
    return render_template('schedules/form.html', schedule=schedule)

@schedule_bp.route('/<int:id>', methods=['POST'])
def updateSchedule(id):
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

    return redirect(url_for('schedule_routes.showSchedule', id=schedule.id))

@schedule_bp.route('/<int:id>/delete', methods=['POST'])
def deleteSchedule(id):
    schedule = Schedule.query.get_or_404(id)
    db.session.delete(schedule)
    db.session.commit()
    flash("Schedule deleted successfully.", "success")
    return redirect(url_for('schedule_routes.getSchedules'))

@schedule_bp.route('/<int:id>/export')
def exportScheduleToExcel(id):
    schedule = Schedule.query.get_or_404(id)
    try:
        return schedule.exportScheduleToExcel()
    except Exception as e:
        flash(f"An error occurred while generating the Excel file: {str(e)}", "danger")
        return redirect(url_for("schedule_routes.showSchedule", id=id))
