from flask import Blueprint, request, render_template, redirect, url_for
from app import db
from app.models.grade import Grade
from app.models.task import Task
from app.models.student import Student
from app.models.student_situation import StudentSituation
from app.models.assessment import Assessment

grade_bp = Blueprint('grade_routes', __name__, url_prefix='/grades')

@grade_bp.route('/new', methods=['GET'])
def newGradeForm():
    student_id = request.args.get('student_id', type=int)
    task_id = request.args.get('task_id', type=int)

    student = Student.query.get_or_404(student_id)
    task = Task.query.get_or_404(task_id)

    return render_template('grades/form.html', grade=None, student=student, task=task)

@grade_bp.route('/new', methods=['POST'])
def createGrade():
    student_id = request.form.get('student_id', type=int)
    task_id = request.form.get('task_id', type=int)
    score = request.form.get('score', type=float)

    if score is None:
        return redirect(url_for('grade_routes.newGradeForm', student_id=student_id, task_id=task_id))

    grade = Grade(student_id=student_id, task_id=task_id, score=score)
    db.session.add(grade)
    db.session.commit()

    return redirect(url_for('student_situation_routes.showStudentSituation', id=student_id))

@grade_bp.route('/<int:id>/edit', methods=['GET'])
def editGradeForm(id):
    grade = Grade.query.get_or_404(id)
    student = Student.query.get_or_404(grade.student_id)
    task = Task.query.get_or_404(grade.task_id)

    return render_template('grades/form.html', grade=grade, student=student, task=task)

@grade_bp.route('/<int:id>/edit', methods=['POST'])
def updateGrade(id):
    grade = Grade.query.get_or_404(id)
    score = request.form.get('score', type=float)

    if score is None:
        return redirect(url_for('grade_routes.editGradeForm', id=id))

    grade.score = score
    db.session.commit()

    return redirect(url_for('student_situation_routes.showStudentSituation', id=grade.student_id))

@grade_bp.route('/<int:id>/delete', methods=['POST'])
def deleteGrade(id):
    grade = Grade.query.get_or_404(id)
    student_id = grade.student_id

    db.session.delete(grade)
    db.session.commit()

    return redirect(url_for('student_situation_routes.showStudentSituation', id=student_id))