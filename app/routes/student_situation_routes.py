from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from app.models.student_situation import StudentSituation
from app.models.student import Student
from app.models.section import Section
from app import db

student_situation_bp = Blueprint('student_situation_routes', __name__, url_prefix='/student_situations')

@student_situation_bp.route('/new', methods=['GET'])
def new_student_situation_form():
    section_id = request.args.get('section_id', type=int)
    section = Section.query.get_or_404(section_id)
    students = Student.query.all()
    return render_template('student_situations/form.html', section=section, students=students)

@student_situation_bp.route('/', methods=['POST'])
def create_student_situation():
    student_id = request.form['student_id']
    section_id = request.form['section_id']
    final_grade = request.form.get('final_grade', None)

    situation = StudentSituation(student_id=student_id, section_id=section_id, final_grade=final_grade or None)
    db.session.add(situation)
    db.session.commit()

    return redirect(url_for('student_situation_routes.list_student_situations'))

@student_situation_bp.route('/', methods=['GET'])
def list_student_situations():
    situations = StudentSituation.query.all()
    return render_template('student_situations/index.html', situations=situations)

@student_situation_bp.route('/<int:id>/show', methods=['GET'])
def show_student_situation(id):
    situation = StudentSituation.query.get_or_404(id)
    return render_template('student_situations/show.html', situation=situation)

@student_situation_bp.route('/<int:id>/edit', methods=['GET'])
def edit_student_situation_form(id):
    situation = StudentSituation.query.get_or_404(id)
    students = Student.query.all()
    sections = Section.query.all()
    return render_template('student_situations/form.html', situation=situation, students=students, sections=sections)

@student_situation_bp.route('/<int:id>', methods=['POST'])
def update_student_situation(id):
    situation = StudentSituation.query.get_or_404(id)
    situation.student_id = request.form['student_id']
    situation.section_id = request.form['section_id']
    situation.final_grade = request.form.get('final_grade', None)
    db.session.commit()

    return redirect(url_for('student_situation_routes.list_student_situations'))

@student_situation_bp.route('/<int:id>/delete', methods=['POST'])
def delete_student_situation(id):
    situation = StudentSituation.query.get_or_404(id)
    db.session.delete(situation)
    db.session.commit()
    return redirect(url_for('student_situation_routes.list_student_situations'))
