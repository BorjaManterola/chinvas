from flask import Blueprint, request, render_template, redirect, url_for, flash
from app import db
from app.models.grade import Grade
from app.models.task import Task
from app.models.student import Student
from app.models.student_situation import StudentSituation
from app.models.assessment import Assessment

grade_bp = Blueprint('grade_routes', __name__, url_prefix='/grades')

@grade_bp.route('/new', methods=['GET'])
def new_grade_form():
    user_id = request.args.get('user_id', type=int)
    task_id = request.args.get('task_id', type=int)

    user = User.query.get_or_404(user_id)
    task = Task.query.get_or_404(task_id)
    assessment = Assessment.query.get_or_404(task.assessment_id)
    usersituation = UserSituation.query.filter_by(user_id=user_id, section_id=assessment.section_id).first()


    return render_template('grades/form.html', grade=None, user=user, task=task, usersituation=usersituation)


@grade_bp.route('/', methods=['POST'])
def create_grade():
    grade = Grade(
        user_id=request.form['user_id'],
        task_id=request.form['task_id'],
        score=request.form['score'],
        feedback=request.form.get('feedback', '')
    )
    db.session.add(grade)
    db.session.commit()

    task = Task.query.get_or_404(grade.task_id)
    assessment = Assessment.query.get_or_404(task.assessment_id)
    usersituation = UserSituation.query.filter_by(user_id=grade.user_id, section_id=assessment.section_id).first()

    return redirect(url_for('usersituation_routes.show', id=usersituation.id))


@grade_bp.route('/<int:id>/edit', methods=['GET'])
def edit_grade_form(id):
    grade = Grade.query.get_or_404(id)
    user = User.query.get_or_404(grade.user_id)
    task = Task.query.get_or_404(grade.task_id)
    assessment = Assessment.query.get_or_404(task.assessment_id)
    usersituation = UserSituation.query.filter_by(user_id=grade.user_id, section_id=assessment.section_id).first()

    return render_template('grades/form.html', grade=grade, user=user, task=task, usersituation=usersituation)


@grade_bp.route('/<int:id>', methods=['POST'])
def update_grade(id):
    grade = Grade.query.get_or_404(id)
    grade.score = request.form['score']
    grade.feedback = request.form.get('feedback', '')
    db.session.commit()

    task = Task.query.get_or_404(grade.task_id)
    assessment = Assessment.query.get_or_404(task.assessment_id)
    usersituation = UserSituation.query.filter_by(user_id=grade.user_id, section_id=assessment.section_id).first()
    return redirect(url_for('usersituation_routes.show', id=usersituation.id))


@grade_bp.route('/<int:id>/delete', methods=['POST'])
def delete_grade(id):
    grade = Grade.query.get_or_404(id)
    usersituation_id = request.form.get('usersituation_id')
    db.session.delete(grade)
    db.session.commit()
    flash("Grade deleted successfully.", "success")

    return redirect(url_for('usersituation_routes.show', id=usersituation_id))
