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
