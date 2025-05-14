from flask import Blueprint, request, render_template, redirect, url_for, flash
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

    schedule, error = Schedule.handleScheduleCreation(year, semester)

    if schedule:
        try:
            return schedule.exportScheduleToExcel()
        except Exception as e:
            flash(f"Schedule created, but Excel download failed: {str(e)}", "warning")
            return redirect(url_for("schedule_routes.getSchedules"))
    else:
        flash(error, "danger")
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
