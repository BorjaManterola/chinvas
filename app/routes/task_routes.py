from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.task import Task
from app.models.assessment import Assessment
from app.models.grade import Grade
from app.models.user import User
from app.models.section import Section
from app.models.usersituation import UserSituation
from app import db
from datetime import datetime

task_bp = Blueprint('task_routes', __name__)


@task_bp.route('/<int:id>/create', methods=['GET'])
def new_task_form(id):
    assessment = Assessment.query.get_or_404(id)
    return render_template('tasks/form.html', task=None, assessment=assessment)

@task_bp.route('/', methods=['POST'])
def create_task():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    name = data.get('name')
    optional = data.get('optional', 'false').lower() == 'true'
    weighting = data.get('weighting')
    date = data.get('date')
    assessment_id = data.get('assessment_id')

    if not name or not weighting or not date or not assessment_id:
        return jsonify({'error': 'Name, weighting, date, and assessment_id are required'}), 400

    try:
        weighting = int(weighting)
        if weighting < 0 or weighting > 100:
            return jsonify({'error': 'Weighting must be between 0 and 100'}), 400
    except ValueError:
        return jsonify({'error': 'Weighting must be a number'}), 400

    total_weight = db.session.query(db.func.sum(Task.weighting)).filter_by(assesstment_id=assessment_id).scalar() or 0
    if total_weight + weighting > 100:
        return jsonify({'error': f'Total task weighting cannot exceed 100%. Current total: {total_weight}%'}), 400

    try:
        task_date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    task = Task(name=name, optional=optional, weighting=weighting, date=task_date, assesstment_id=assessment_id)
    db.session.add(task)
    db.session.commit()

    if request.is_json:
        return jsonify({'message': 'Task created successfully', 'id': task.id}), 201
    return redirect(url_for('assessment_routes.show_assessment', id=assessment_id))


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
