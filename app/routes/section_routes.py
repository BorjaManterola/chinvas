from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models.section import Section
from app.models.period import Period
from app.models.teacher import Teacher
from app import db

section_bp = Blueprint('section_routes', __name__, url_prefix='/sections')


@section_bp.route('/new', methods=['GET'])
def new_section_form():
    period_id = request.args.get('period_id', type=int)
    period = Period.query.get_or_404(period_id)
    teachers = Teacher.query.all()
    return render_template('sections/form.html', section=None, period=period, teachers=teachers)

@section_bp.route('/', methods=['POST'])
def create_section():
    period_id = request.form.get('period_id')
    teacher_id = request.form.get('teacher_id')
    type_evaluate = request.form.get('type_evaluate')

    if not teacher_id or not type_evaluate:
        flash("All fields are required.", "danger")
        period = Period.query.get(period_id)
        teachers = Teacher.query.all()
        return render_template('sections/form.html', section=None, period=period, teachers=teachers)

    section = Section(period_id=period_id, teacher_id=teacher_id, type_evaluate=type_evaluate)
    db.session.add(section)
    db.session.commit()
    flash("Section created successfully.", "success")
    return redirect(url_for('period_routes.show_period', id=period_id))

@section_bp.route('/<int:id>/show', methods=['GET'])
def show_section(id):
    section = Section.query.get_or_404(id)
    assessments = section.assessments
    student_situations = section.student_situations
    return render_template(
        'sections/show.html',
        section=section,
        assessments=assessments,
        students=student_situations
    )

@section_bp.route('/<int:id>/edit', methods=['GET'])
def edit_section_form(id):
    section = Section.query.get_or_404(id)
    teachers = Teacher.query.all()
    return render_template('sections/form.html', section=section, period=section.period, teachers=teachers)

@section_bp.route('/<int:id>', methods=['POST'])
def update_section(id):
    section = Section.query.get_or_404(id)
    section.teacher_id = request.form.get('teacher_id')
    section.type_evaluate = request.form.get('type_evaluate')
    db.session.commit()
    flash("Section updated successfully.", "success")
    return redirect(url_for('period_routes.show_period', id=section.period_id))


@section_bp.route('/<int:id>/delete', methods=['POST'])
def delete_section(id):
    section = Section.query.get_or_404(id)
    period_id = section.period_id
    db.session.delete(section)
    db.session.commit()
    flash("Section deleted successfully.", "success")
    return redirect(url_for('period_routes.show_period', id=period_id))