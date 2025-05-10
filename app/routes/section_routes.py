from flask import Blueprint, request, render_template, redirect, url_for
from app.models.section import Section
from app.models.period import Period
from app.models.user import User
from app.models.assessment import Assessment
from app.models.usersituation import UserSituation  # Asegúrate de importar esto también
from app import db

section_bp = Blueprint('section_routes', __name__, url_prefix='/sections')

@section_bp.route('/new', methods=['GET'])
def new_section_form():
    teachers = User.query.filter_by(role='Teacher').all()
    period_id = request.args.get('period_id', type=int)
    period = Period.query.get(period_id) if period_id else None
    return render_template('sections/form.html', section=None, period=period, teachers=teachers)


@section_bp.route('/', methods=['POST'])
def create_section():
    form = request.form
    section = _create_section_from_form(form)
    _assign_teachers_to_section(form.getlist('teacher_ids'), section.id)

    db.session.commit()
    return redirect(url_for('period_routes.show_period', id=form['period_id']))


def _create_section_from_form(form):
    section = Section(
        nrc=form['nrc'],
        period_id=form['period_id'],
        type_evaluate=form['type_evaluate']
    )
    db.session.add(section)
    db.session.flush()  
    return section


def _assign_teachers_to_section(teacher_ids, section_id):
    for teacher_id in teacher_ids:
        usersituation = UserSituation(
            user_id=int(teacher_id),
            section_id=section_id,
            situation='teacher',
            final_grade=None
        )
        db.session.add(usersituation)

@section_bp.route('/<int:id>/show', methods=['GET'])
def show_section(id):
    section = Section.query.get_or_404(id)
    teachers, students = _get_teachers_and_students(section)
    assessments = _get_assessments_for_section(id)

    return render_template(
        'sections/show.html',
        section=section,
        teachers=teachers,
        students=students,
        assessments=assessments
    )


def _get_teachers_and_students(section):
    teachers = []
    students = []
    for us in section.usersituations:
        role = us.situation.strip().lower()
        if role == "teacher":
            teachers.append(us.user)
        elif role == "student":
            students.append(us.user)
    return teachers, students


def _get_assessments_for_section(section_id):
    return Assessment.query.filter_by(section_id=section_id).all()

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