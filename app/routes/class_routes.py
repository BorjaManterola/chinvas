from flask import Blueprint, request, render_template, redirect, url_for
from app.models.class_ import Class
from app.models.section import Section
from app.models.schedule import Schedule
from app.models.classroom import Classroom
from app import db

class_bp = Blueprint('class_routes', __name__, url_prefix='/classes')

@class_bp.route('/new', methods=['GET'])
def newClassForm():
    section_id = request.args.get('section_id', type=int)
    section = Section.query.get_or_404(section_id)
    classrooms = Classroom.query.all()
    schedules = Schedule.query.all()
    return render_template("classes/form.html", section=section, classrooms=classrooms, schedules=schedules)

@class_bp.route('/new', methods=['POST'])
def createClass():
    section_id = request.form.get('section_id', type=int)
    classroom_id = request.form.get('classroom_id', type=int)
    schedule_id = request.form.get('schedule_id', type=int)
    day_of_week = request.form.get('day_of_week')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')

    if not all([section_id, classroom_id, schedule_id, day_of_week, start_time, end_time]):
        return redirect(url_for('class_routes.newClassForm', section_id=section_id))

    new_class = Class(
        section_id=section_id,
        classroom_id=classroom_id,
        schedule_id=schedule_id,
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time
    )
    db.session.add(new_class)
    db.session.commit()
    return redirect(url_for('section_routes.showSection', id=section_id))

@class_bp.route('/', methods=['GET'])
def listClasses():
    classes = Class.query.all()
    return render_template("classes/index.html", classes=classes)

@class_bp.route('/<int:id>/delete', methods=['POST'])
def deleteClass(id):
    class_instance = Class.query.get_or_404(id)
    section_id = class_instance.section_id
    db.session.delete(class_instance)
    db.session.commit()
    return redirect(url_for('section_routes.showSection', id=section_id))
