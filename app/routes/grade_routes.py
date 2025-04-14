from flask import Blueprint, request, jsonify
from app.models.grade import Grade
from app import db

grade_bp = Blueprint('grades', __name__, url_prefix='/grades')

@grade_bp.route('/', methods=['POST'])
def create_grade():
    data = request.get_json()
    grade = Grade(user_id=data['user_id'], task_id=data['task_id'], score=data['score'], feedback=data.get('feedback'))
    db.session.add(grade)
    db.session.commit()
    return jsonify({ 'message': 'Nota creada', 'id': grade.id }), 201

@grade_bp.route('/', methods=['GET'])
def get_grades():
    grades = Grade.query.all()
    return jsonify([{ 'id': g.id, 'user_id': g.user_id, 'task_id': g.task_id, 'score': g.score, 'feedback': g.feedback } for g in grades])

@grade_bp.route('/<int:id>', methods=['GET'])
def get_grade(id):
    grade = Grade.query.get_or_404(id)
    return jsonify({ 'id': grade.id, 'user_id': grade.user_id, 'task_id': grade.task_id, 'score': grade.score, 'feedback': grade.feedback })

@grade_bp.route('/<int:id>', methods=['PUT'])
def update_grade(id):
    grade = Grade.query.get_or_404(id)
    data = request.get_json()
    grade.user_id = data.get('user_id', grade.user_id)
    grade.task_id = data.get('task_id', grade.task_id)
    grade.score = data.get('score', grade.score)
    grade.feedback = data.get('feedback', grade.feedback)
    db.session.commit()
    return jsonify({ 'message': 'Nota actualizada' })

@grade_bp.route('/<int:id>', methods=['DELETE'])
def delete_grade(id):
    grade = Grade.query.get_or_404(id)
    db.session.delete(grade)
    db.session.commit()
    return jsonify({ 'message': 'Nota eliminada' })