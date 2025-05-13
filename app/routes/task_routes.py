from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.task import Task
from app.models.assessment import Assessment
from app import db

task_bp = Blueprint('task_routes', __name__, url_prefix='/tasks')

@task_bp.route('/new/<int:assessment_id>', methods=['GET'])
def newTaskForm(assessment_id):
    assessment = Assessment.query.get_or_404(assessment_id)
    return render_template('tasks/form.html', task=None, assessment=assessment)

@task_bp.route('/', methods=['POST'])
def createTask():
    assessment_id = request.form.get('assessment_id')
    weighting = request.form.get('weighting', type=float)
    optional = 'optional' in request.form

    task = Task(assessment_id=assessment_id, weighting=weighting, optional=optional)
    
    db.session.add(task)
    db.session.flush()
    
    is_valid, total_weight = task.isValidWeightingInAssessment(weighting, task.id)
    if not is_valid:
        flash(f"Total task weighting cannot exceed 100%. Current total: {total_weight}%", "danger")
        return redirect(url_for('task_routes.newTaskForm', assessment_id=assessment_id))

    db.session.commit()

    return redirect(url_for('assessment_routes.showAssessment', id=assessment_id))

@task_bp.route('/<int:id>/edit', methods=['GET'])
def editTaskForm(id):
    task = Task.query.get_or_404(id)
    assessment = Assessment.query.get_or_404(task.assessment_id)
    return render_template('tasks/form.html', task=task, assessment=assessment)

@task_bp.route('/<int:id>', methods=['POST'])
def updateTask(id):
    task = Task.query.get_or_404(id)
    assessment_id = task.assessment_id
    weighting = request.form.get('weighting', type=float)
    optional = 'optional' in request.form

    is_valid, total_weight = task.isValidWeightingInAssessment(weighting, exclude_task=id)
    if not is_valid:
        flash(f"Total task weighting cannot exceed 100%. Current total: {total_weight}%", "danger")
        return redirect(url_for('task_routes.editTaskForm', id=id))

    task.weighting = weighting
    task.optional = optional
    db.session.commit()

    return redirect(url_for('assessment_routes.showAssessment', id=assessment_id))

@task_bp.route('/<int:id>/delete', methods=['POST'])
def deleteTask(id):
    task = Task.query.get_or_404(id)
    assessment_id = task.assessment_id

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for('assessment_routes.showAssessment', id=assessment_id))