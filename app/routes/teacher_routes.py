from flask import Blueprint, render_template, request, redirect, url_for
from app.models.teacher import Teacher
from app import db

teacher_bp = Blueprint('teacher_routes', __name__, url_prefix='/teachers')

@teacher_bp.route('/new', methods=['GET'])
def newTeacherForm():
    return render_template('teachers/form.html', teacher=None)

@teacher_bp.route('/new', methods=['POST'])
def createTeacher():
    name = request.form.get('name')
    email = request.form.get('email')

    if not name or not email:
        return render_template('teachers/form.html', teacher=None)

    teacher = Teacher(name=name, email=email)
    db.session.add(teacher)
    db.session.commit()
    return redirect(url_for('teacher_routes.getTeachers'))

@teacher_bp.route('/', methods=['GET'])
def getTeachers():
    teachers = Teacher.query.all()
    return render_template('teachers/index.html', teachers=teachers)

@teacher_bp.route('/<int:id>/edit', methods=['GET'])
def editTeacherForm(id):
    teacher = Teacher.query.get_or_404(id)
    return render_template('teachers/form.html', teacher=teacher)

@teacher_bp.route('/<int:id>/edit', methods=['POST'])
def updateTeacher(id):
    teacher = Teacher.query.get_or_404(id)
    teacher.name = request.form.get('name')
    teacher.email = request.form.get('email')
    db.session.commit()
    return redirect(url_for('teacher_routes.getTeachers'))

@teacher_bp.route('/<int:id>/delete', methods=['POST'])
def deleteTeacher(id):
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    return redirect(url_for('teacher_routes.getTeachers'))
