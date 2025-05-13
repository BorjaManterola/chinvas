from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.student import Student
from app import db

student_bp = Blueprint('student_routes', __name__, url_prefix='/students')

@student_bp.route('/new', methods=['GET'])
def newstudentForm():
    return render_template('students/form.html', student=None)

@student_bp.route('/', methods=['POST'])
def createStudent():
    name = request.form.get('name')
    email = request.form.get('email')
    entry_date = request.form.get('entry_date')

    if not name or not email:
        flash("Name and email are required.", "danger")
        return render_template('students/form.html', student=None)

    student = Student(name=name, email=email, entry_date=entry_date)
    db.session.add(student)
    db.session.commit()
    flash("Student created successfully.", "success")
    return redirect(url_for('student_routes.get_students'))

@student_bp.route('/', methods=['GET'])
def getStudents():
    students = Student.query.all()
    return render_template('students/index.html', students=students)


@student_bp.route('/<int:id>', methods=['GET'])
def showStudent(id):
    student = Student.query.get_or_404(id)
    return render_template('students/show.html', student=student)

@student_bp.route('/<int:id>/edit', methods=['GET'])
def editStudentForm(id):
    student = Student.query.get_or_404(id)
    return render_template('students/form.html', student=student)


@student_bp.route('/<int:id>', methods=['POST'])
def updateStudent(id):
    student = Student.query.get_or_404(id)
    student.name = request.form.get('name')
    student.email = request.form.get('email')
    student.entry_date = request.form.get('entry_date')
    db.session.commit()
    flash("Student updated successfully.", "success")
    return redirect(url_for('student_routes.get_students'))

@student_bp.route('/<int:id>/delete', methods=['POST'])
def deleteStudent(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully.", "success")
    return redirect(url_for('student_routes.get_students'))
