from flask import Blueprint, request, render_template, redirect, url_for
from app.models.section import Section
from app.models.period import Period
from app.models.user import User
from app.models.assessment import Assessment
from app.models.usersituation import UserSituation  # Asegúrate de importar esto también
from app import db

section_bp = Blueprint('section_routes', __name__, url_prefix='/sections')


@section_bp.route('/', methods=['GET'])
def list_sections():
    sections = Section.query.all()
    return render_template('sections/index.html', sections=sections)


@section_bp.route('/new', methods=['GET'])
def new_section_form():
    teachers = User.query.filter_by(role='Teacher').all()
    period_id = request.args.get('period_id', type=int)
    period = Period.query.get(period_id) if period_id else None
    return render_template('sections/form.html', section=None, period=period, teachers=teachers)


@section_bp.route('/', methods=['POST'])
def create_section():
    period_id = request.form['period_id']
    nrc = request.form['nrc']
    type_evaluate = request.form['type_evaluate']

    section = Section(nrc=nrc, period_id=period_id, type_evaluate=type_evaluate)
    db.session.add(section)
    db.session.flush()  # Para obtener section.id antes del commit

    # Procesar profesores seleccionados
    teacher_ids = request.form.getlist('teacher_ids')
    for teacher_id in teacher_ids:
        usersituation = UserSituation(
            user_id=int(teacher_id),
            section_id=section.id,
            situation='teacher',
            final_grade=None
        )
        db.session.add(usersituation)

    db.session.commit()
    return redirect(url_for('period_routes.show_period', id=period_id))


@section_bp.route('/<int:id>/edit', methods=['GET'])
def edit_section_form(id):
    section = Section.query.get_or_404(id)
    teachers = User.query.filter_by(role='Teacher').all()
    return render_template('sections/form.html', section=section, period=section.period, teachers=teachers)


@section_bp.route('/<int:id>', methods=['POST'])
def update_section(id):
    section = Section.query.get_or_404(id)
    section.nrc = request.form['nrc']
    section.type_evaluate = request.form['type_evaluate']
    db.session.commit()
    return redirect(url_for('period_routes.show_period', id=section.period_id))


@section_bp.route('/<int:id>/delete', methods=['POST'])
def delete_section(id):
    section = Section.query.get_or_404(id)
    period_id = section.period_id
    db.session.delete(section)
    db.session.commit()
    return redirect(url_for('period_routes.show_period', id=period_id))

@section_bp.route('/<int:id>/show', methods=['GET'])
def show_section(id):
    section = Section.query.get_or_404(id)
    usersituations = section.usersituations
    teachers = [us.user for us in usersituations if us.situation.strip().lower() == "teacher"]
    students = [us.user for us in usersituations if us.situation.strip().lower() == "student"]

    return render_template('sections/show.html', section=section, teachers=teachers, students=students)

@section_bp.route('/<int:id>/assign-students', methods=['POST'])
def assign_students(id):
    section = Section.query.get_or_404(id)
    student_ids = request.form.getlist('student_ids')

    for student_id in student_ids:
        usersituation = UserSituation(
            user_id=int(student_id),
            section_id=section.id,
            situation='student',  # ¡importante que sea exactamente 'student'!
            final_grade=None
        )
        db.session.add(usersituation)

    db.session.commit()
    return redirect(url_for('section_routes.show_section', id=section.id))

@section_bp.route('/<int:id>/assign-teachers', methods=['POST'])
def assign_teachers(id):
    section = Section.query.get_or_404(id)
    teacher_ids = request.form.getlist('teacher_ids')

    for teacher_id in teacher_ids:
        usersituation = UserSituation(
            user_id=int(teacher_id),
            section_id=section.id,
            situation='teacher',
            final_grade=None
        )
        db.session.add(usersituation)

    db.session.commit()
    return redirect(url_for('section_routes.show_section', id=section.id))

@section_bp.route('/<int:id>/assessments')
def manage_assessments(id):
    section = Section.query.get_or_404(id)
    assessments = Assessment.query.filter_by(section_id=id).all()
    return render_template('assessments/index.html', section=section, assessments=assessments)