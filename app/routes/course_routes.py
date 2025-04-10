from flask import Blueprint, request, jsonify
from app.models.course import Course
from app import db

course_bp = Blueprint('courses', __name__, url_prefix='/courses')

@course_bp.route('/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([{ 'id': c.id, 'name': c.name, 'description': c.description } for c in courses])

@course_bp.route('/<int:id>', methods=['GET'])
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify({ 'id': course.id, 'name': course.name, 'description': course.description })

@course_bp.route('/', methods=['POST'])
def create_course():
    data = request.get_json()
    course = Course(name=data['name'], description=data.get('description'))
    db.session.add(course)
    db.session.commit()
    return jsonify({ 'message': 'Curso creado', 'id': course.id }), 201

@course_bp.route('/<int:id>', methods=['PUT'])
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json()
    course.name = data.get('name', course.name)
    course.description = data.get('description', course.description)
    db.session.commit()
    return jsonify({ 'message': 'Curso actualizado' })

@course_bp.route('/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({ 'message': 'Curso eliminado' })