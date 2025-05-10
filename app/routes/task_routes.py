from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.models.task import Task
from app.models.assessment import Assessment
from app.models.grade import Grade
from app.models.student import Student
from app.models.section import Section
from app.models.student_situation import StudentSituation
from app import db
from datetime import datetime

task_bp = Blueprint('task_routes', __name__)


@task_bp.route('/<int:id>/create', methods=['GET'])
def new_task_form(id):
    assessment = Assessment.query.get_or_404(id)
    return render_template('tasks/form.html', task=None, assessment=assessment)


@task_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json() if request.is_json else request.form

    is_valid, error_response = _validate_task_data(data)
    if not is_valid:
        return error_response

    task = _create_task_from_data(data)
    db.session.commit()

    if request.is_json:
        return jsonify({'message': 'Task created successfully', 'id': task.id}), 201

    return redirect(url_for('assessment_routes.show_assessment', id=task.assessment_id))


def _validate_task_data(data):
    required_fields = ['name', 'weighting', 'date', 'assessment_id']
    for field in required_fields:
        if not data.get(field):
            return False, jsonify({'error': f'{field} is required'}), 400

    try:
        weighting = int(data.get('weighting'))
        if weighting < 0 or weighting > 100:
            return False, jsonify({'error': 'Weighting must be between 0 and 100'}), 400
    except ValueError:
        return False, jsonify({'error': 'Weighting must be a number'}), 400

    total_weight = db.session.query(db.func.sum(Task.weighting)) \
        .filter_by(assessment_id=data.get('assessment_id')).scalar() or 0
    if total_weight + weighting > 100:
        return False, jsonify({
            'error': f'Total task weighting cannot exceed 100%. Current total: {total_weight}%'
        }), 400

    try:
        datetime.strptime(data.get('date'), '%Y-%m-%d').date()
    except ValueError:
        return False, jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

    return True, None


def _create_task_from_data(data):
    task = Task(
        name=data.get('name'),
        optional=data.get('optional', 'false').lower() == 'true',
        weighting=int(data.get('weighting')),
        date=datetime.strptime(data.get('date'), '%Y-%m-%d').date(),
        assessment_id=data.get('assessment_id')
    )
    db.session.add(task)
    return task



@task_bp.route('/<int:id>/edit', methods=['GET'])
def edit_task_form(id):
    task = Task.query.get_or_404(id)
    assessment = Assessment.query.get_or_404(task.assessment_id)
    return render_template('tasks/form.html', task=task, assessment=assessment)

@task_bp.route('/<int:id>', methods=['POST'])
def update_task(id):
    task = Task.query.get_or_404(id)
    assessment = Assessment.query.get_or_404(task.assessment_id)

    is_valid, result = _validate_update_task_data(request.form, assessment, task.id)
    if not is_valid:
        flash(result['message'], 'danger')
        return render_template('tasks/form.html', task=task, assessment=assessment)

    _update_task_fields(task, result)
    db.session.commit()

    flash('Task updated successfully', 'success')
    return redirect(url_for('assessment_routes.show_assessment', id=task.assessment_id))


def _validate_update_task_data(form, assessment, task_id):
    name = form.get('name')
    optional = form.get('optional') == 'on'
    weighting = form.get('weighting')
    date = form.get('date')

    if not name or not weighting or not date:
        return False, {'message': 'Name, weighting and date are required'}

    try:
        weighting = int(weighting)
        if weighting < 0 or (weighting > 100 and assessment.type_evaluate == 'Percentage'):
            return False, {'message': 'Weighting must be between 0 and 100'}
    except ValueError:
        return False, {'message': 'Weighting must be a number'}

    total_weight = db.session.query(db.func.sum(Task.weighting)) \
        .filter_by(assessment_id=assessment.id) \
        .filter(Task.id != task_id).scalar() or 0
    if total_weight + weighting > 100 and assessment.type_evaluate == 'Percentage':
        return False, {'message': f'Total task weighting cannot exceed 100%. Current total: {total_weight}%'}

    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return False, {'message': 'Invalid date format. Use YYYY-MM-DD'}

    return True, {
        'name': name,
        'optional': optional,
        'weighting': weighting,
        'date': date_obj
    }


def _update_task_fields(task, data):
    task.name = data['name']
    task.optional = data['optional']
    task.weighting = data['weighting']
    task.date = data['date']



@task_bp.route('/<int:id>/delete', methods=['POST'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    assessment_id = task.assessment_id

    db.session.delete(task)
    db.session.commit()

    flash('Task deleted successfully', 'success')
    return redirect(url_for('assessment_routes.show_assessment', id=assessment_id))
