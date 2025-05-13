from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.teacher import Teacher
from app import db

teacher_bp = Blueprint('teacher_routes', __name__, url_prefix='/teachers')

@teacher_bp.route('/new', methods=['GET', 'POST'])
def createTeacher():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        if not name or not email:
            flash("Name and email are required.", "danger")
            return render_template('teachers/form.html', teacher=None)

        teacher = Teacher(name=name, email=email)
        db.session.add(teacher)
        db.session.commit()
        flash("Teacher created successfully.", "success")
        return redirect(url_for('teacher_routes.index'))

    return render_template('teachers/form.html', teacher=None)

@teacher_bp.route('/', methods=['GET'])
def getTeachers():
    teachers = Teacher.query.all()
    return render_template('teachers/index.html', teachers=teachers)

@teacher_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def editTeacher(id):
    teacher = Teacher.query.get_or_404(id)
    if request.method == 'POST':
        teacher.name = request.form['name']
        teacher.email = request.form['email']
        db.session.commit()
        flash("Teacher updated successfully.", "success")
        return redirect(url_for('teacher_routes.index'))

    return render_template('teachers/form.html', teacher=teacher)

@teacher_bp.route('/<int:id>/delete', methods=['POST'])
def deleteTeacher(id):
    teacher = Teacher.query.get_or_404(id)
    db.session.delete(teacher)
    db.session.commit()
    flash("Teacher deleted successfully.", "success")
    return redirect(url_for('teacher_routes.index'))