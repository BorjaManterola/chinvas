from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.task import Task
from app.models.assessment import Assessment
from app.models.grade import Grade
from app.models.user import User
from app.models.section import Section
from app.models.usersituation import UserSituation
from app import db
from datetime import datetime

task_bp = Blueprint('task_routes', __name__)

@task_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    assessment = Assessment.query.get_or_404(task.assesstment_id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        optional = request.form.get('optional') == 'on'
        weighting = request.form.get('weighting')
        date = request.form.get('date')
        
        if not name or not weighting or not date:
            flash('Name, weighting and date are required', 'danger')
            return render_template('tasks/edit.html', task=task, assessment=assessment)
        
        try:
            weighting = int(weighting)
            if weighting < 0 or weighting > 100:
                flash('Weighting must be between 0 and 100', 'danger')
                return render_template('tasks/edit.html', task=task, assessment=assessment)
        except ValueError:
            flash('Weighting must be a number', 'danger')
            return render_template('tasks/edit.html', task=task, assessment=assessment)
        
        # Check if total weighting of tasks exceeds 100%
        total_weight = db.session.query(db.func.sum(Task.weighting)).filter_by(
            assesstment_id=task.assesstment_id).filter(Task.id != id).scalar() or 0
        if total_weight + weighting > 100:
            flash(f'Total task weighting cannot exceed 100%. Current total: {total_weight}%', 'danger')
            return render_template('tasks/edit.html', task=task, assessment=assessment)
        
        task.name = name
        task.optional = optional
        task.weighting = weighting
        task.date = datetime.strptime(date, '%Y-%m-%d').date()
        db.session.commit()
        
        flash('Task updated successfully', 'success')
        return redirect(url_for('task_routes.view_tasks', id=task.assesstment_id))
    
    return render_template('tasks/edit.html', task=task, assessment=assessment)

@task_bp.route('/<int:id>/create', methods=['GET', 'POST'])
def create_task(id):
    assessment = Assessment.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form.get('name')
        optional = request.form.get('optional') == 'on'
        weighting = request.form.get('weighting')
        date = request.form.get('date')

        if not name or not weighting or not date:
            flash('Name, weighting, and date are required', 'danger')
            return render_template('tasks/form.html', task=None, assessment=assessment)

        try:
            weighting = int(weighting)
        except ValueError:
            flash('Weighting must be a number', 'danger')
            return render_template('tasks/form.html', task=None, assessment=assessment)

        # Check if total weighting of tasks exceeds 100%
        total_weight = db.session.query(db.func.sum(Task.weighting)).filter_by(
            assesstment_id=id).scalar() or 0
        if total_weight + weighting > 100:
            flash(f'Total task weighting cannot exceed 100%. Current total: {total_weight}%', 'danger')
            return render_template('tasks/form.html', task=None, assessment=assessment)

        new_task = Task(
            name=name,
            optional=optional,
            weighting=weighting,
            date=datetime.strptime(date, '%Y-%m-%d').date(),
            assesstment_id=id
        )
        db.session.add(new_task)
        db.session.commit()

        flash('Task created successfully', 'success')
        return redirect(url_for('task_routes.view_tasks', id=id))

    return render_template('tasks/form.html', task=None, assessment=assessment)

@task_bp.route('/<int:id>/delete', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    assessment_id = task.assesstment_id
    
    # Check if there are grades associated with this task
    grades = Grade.query.filter_by(task_id=id).all()
    if grades:
        flash('Cannot delete task with associated grades. Delete grades first.', 'danger')
        return redirect(url_for('assessment_routes.view_tasks', id=assessment_id))
    
    db.session.delete(task)
    db.session.commit()
    
    flash('Task deleted successfully', 'success')
    return redirect(url_for('assessment_routes.view_tasks', id=assessment_id))

@task_bp.route('/<int:id>/grades')
def manage_grades(id):
    task = Task.query.get_or_404(id)
    assessment = Assessment.query.get_or_404(task.assesstment_id)
    section = Section.query.get_or_404(assessment.section_id)
    
    # Get all students in the section
    students = User.query.join(UserSituation).filter(
        UserSituation.section_id == section.id,
        UserSituation.situation == 'student'
    ).all()
    
    # Get existing grades for the task
    grades = Grade.query.filter_by(task_id=id).all()
    grades_dict = {grade.user_id: grade for grade in grades}
    
    return render_template('tasks/grades.html', 
                          task=task, 
                          assessment=assessment, 
                          section=section,
                          students=students,
                          grades_dict=grades_dict)

@task_bp.route('/<int:id>/grades/edit', methods=['POST'])
def edit_grades(id):
    task = Task.query.get_or_404(id)
    assessment = Assessment.query.get_or_404(task.assesstment_id)
    
    # Process form data - expecting user_id and score pairs
    for key, value in request.form.items():
        if key.startswith('score_'):
            user_id = int(key.split('_')[1])
            score_str = value.strip()
            feedback = request.form.get(f'feedback_{user_id}', '')
            
            # Skip empty scores
            if not score_str:
                continue
                
            try:
                score = float(score_str)
                if score < 0 or score > 100:
                    flash(f'Score must be between 0 and 100 for user {user_id}', 'danger')
                    continue
            except ValueError:
                flash(f'Invalid score format for user {user_id}', 'danger')
                continue
                
            # Check if grade already exists
            grade = Grade.query.filter_by(user_id=user_id, task_id=id).first()
            
            if grade:
                # Update existing grade
                grade.score = score
                grade.feedback = feedback
            else:
                # Create new grade
                grade = Grade(
                    user_id=user_id,
                    task_id=id,
                    score=score,
                    feedback=feedback
                )
                db.session.add(grade)
    
    db.session.commit()
    flash('Grades updated successfully', 'success')
    return redirect(url_for('task_routes.manage_grades', id=id))

@task_bp.route('/<int:task_id>/grades/<int:user_id>/delete', methods=['POST'])
def delete_grade(task_id, user_id):
    grade = Grade.query.filter_by(task_id=task_id, user_id=user_id).first_or_404()
    db.session.delete(grade)
    db.session.commit()
    
    flash('Grade deleted successfully', 'success')
    return redirect(url_for('task_routes.manage_grades', id=task_id))