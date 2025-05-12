from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.task import Task
from app.models.assessment import Assessment
from app import db

task_bp = Blueprint('task_routes', __name__, url_prefix='/tasks')

@task_bp.route('/new/<int:assessment_id>', methods=['GET'])
def new_task_form(assessment_id):
    """Render the form to create a new task."""
    assessment = Assessment.query.get_or_404(assessment_id)
    return render_template('tasks/form.html', task=None, assessment=assessment)

@task_bp.route('/', methods=['POST'])
def create_task():
    """Handle the creation of a new task."""
    assessment_id = request.form.get('assessment_id')
    weighting = request.form.get('weighting', type=float)
    optional = 'optional' in request.form

    if not assessment_id or weighting is None:
        flash("All fields are required.", "danger")
        return redirect(url_for('assessment_routes.show_assessment', id=assessment_id))

    is_valid, total_weight = Task.is_valid_weighting(assessment_id, weighting, exclude_task_id=id)
    if not is_valid:
        flash(f"Total task weighting cannot exceed 100%. Current total: {total_weight}%", "danger")
        return redirect(url_for('task_routes.edit_task_form', id=id))

    task = Task(assessment_id=assessment_id, weighting=weighting, optional=optional)
    db.session.add(task)
    db.session.commit()

    flash("Task created successfully.", "success")
    return redirect(url_for('assessment_routes.show_assessment', id=assessment_id))

@task_bp.route('/<int:id>/edit', methods=['GET'])
def edit_task_form(id):
    """Render the form to edit an existing task."""
    task = Task.query.get_or_404(id)
    assessment = Assessment.query.get_or_404(task.assessment_id)
    return render_template('tasks/form.html', task=task, assessment=assessment)

@task_bp.route('/<int:id>', methods=['POST'])
def update_task(id):
    """Handle the update of an existing task."""
    task = Task.query.get_or_404(id)
    assessment_id = task.assessment_id
    weighting = request.form.get('weighting', type=float)
    optional = 'optional' in request.form

    if weighting is None:
        flash("Weighting is required.", "danger")
        return redirect(url_for('task_routes.edit_task_form', id=id))

    is_valid, total_weight = Task.is_valid_weighting(assessment_id, weighting, exclude_task_id=id)
    if not is_valid:
        flash(f"Total task weighting cannot exceed 100%. Current total: {total_weight}%", "danger")
        return redirect(url_for('task_routes.edit_task_form', id=id))


    task.weighting = weighting
    task.optional = optional
    db.session.commit()

    flash("Task updated successfully.", "success")
    return redirect(url_for('assessment_routes.show_assessment', id=assessment_id))

@task_bp.route('/<int:id>/delete', methods=['POST'])
def delete_task(id):
    """Handle the deletion of a task."""
    task = Task.query.get_or_404(id)
    assessment_id = task.assessment_id

    db.session.delete(task)
    db.session.commit()

    flash("Task deleted successfully.", "success")
    return redirect(url_for('assessment_routes.show_assessment', id=assessment_id))