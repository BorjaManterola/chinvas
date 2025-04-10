from flask import Blueprint, request, jsonify
from app.models.task import Task
from app import db

task_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@task_bp.route('/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{ 'id': t.id, 'assesstment_id': t.assesstment_id, 'name': t.name, 'optional': t.optional, 'weighting': t.weighting, 'date': t.date } for t in tasks])

@task_bp.route('/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify({ 'id': task.id, 'assesstment_id': task.assesstment_id, 'name': task.name, 'optional': task.optional, 'weighting': task.weighting, 'date': task.date })

@task_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    task = Task(assesstment_id=data['assesstment_id'], name=data['name'], optional=data['optional'], weighting=data['weighting'], date=data['date'])
    db.session.add(task)
    db.session.commit()
    return jsonify({ 'message': 'Tarea creada', 'id': task.id }), 201

@task_bp.route('/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    task.assesstment_id = data.get('assesstment_id', task.assesstment_id)
    task.name = data.get('name', task.name)
    task.optional = data.get('optional', task.optional)
    task.weighting = data.get('weighting', task.weighting)
    task.date = data.get('date', task.date)
    db.session.commit()
    return jsonify({ 'message': 'Tarea actualizada' })

@task_bp.route('/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({ 'message': 'Tarea eliminada' })