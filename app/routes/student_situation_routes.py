from flask import Blueprint, request, render_template, redirect, url_for
from app.models.student_situation import StudentSituation
from app.models.student import Student
from app.models.section import Section

from app import db

student_situation_bp = Blueprint('student_situation_routes', __name__, url_prefix='/student_situations')

@student_situation_bp.route('/new', methods=['GET'])
def newStudentSituationForm():
    section_id = request.args.get('section_id', type=int)
    section = Section.query.get_or_404(section_id)

    assigned_student_ids = db.session.query(StudentSituation.student_id).filter_by(section_id=section_id).all()
    assigned_ids = {id for (id,) in assigned_student_ids}

    students = Student.query.filter(~Student.id.in_(assigned_ids)).all()

    return render_template("student_situations/form.html", section=section, students=students)

@student_situation_bp.route('/new', methods=['POST'])
def createStudentSituations():
    section_id = request.form.get('section_id')
    student_ids = request.form.getlist('student_ids')

    for student_id in student_ids:
        situation = StudentSituation(student_id=student_id, section_id=section_id)
        db.session.add(situation)
    
    db.session.commit()
    return redirect(url_for('section_routes.showSection', id=section_id))

@student_situation_bp.route('/<int:id>/show', methods=['GET'])
def showStudentSituation(id):
    student_situation = StudentSituation.query.get_or_404(id)
    tasks =student_situation.userSectionTasks()
    grades = student_situation.userGrades()
    return render_template(
        'student_situations/show.html',
        student_situation=student_situation,
        tasks=tasks,
        grades=grades
    )

@student_situation_bp.route('/<int:id>/edit', methods=['GET'])
def editStudentSituationForm(id):
    situation = StudentSituation.query.get_or_404(id)
    students = Student.query.all()
    sections = Section.query.all()
    return render_template('student_situations/form.html', situation=situation, students=students, sections=sections)

@student_situation_bp.route('/<int:id>', methods=['POST'])
def updateStudentSituation(id):
    situation = StudentSituation.query.get_or_404(id)
    situation.student_id = request.form['student_id']
    situation.section_id = request.form['section_id']
    situation.final_grade = request.form.get('final_grade', None)
    db.session.commit()

    return redirect(url_for('student_situation_routes.listStudentSituations'))

@student_situation_bp.route('/<int:id>/delete', methods=['POST'])
def deleteStudentSituation(id):
    situation = StudentSituation.query.get_or_404(id)    
    section_id = situation.section_id
    db.session.delete(situation)
    db.session.commit()
    return redirect(url_for('section_routes.showSection', id=section_id))