from flask import Blueprint, request, jsonify
from app.models.period import Period
from app import db

period_bp = Blueprint('periods', __name__, url_prefix='/periods')

@period_bp.route('/', methods=['GET'])
def get_periods():
    periods = Period.query.all()
    return jsonify([{ 'id': p.id, 'course_id': p.course_id, 'nrc': p.nrc, 'semester': p.semester } for p in periods])

@period_bp.route('/<int:id>', methods=['GET'])
def get_period(id):
    period = Period.query.get_or_404(id)
    return jsonify({ 'id': period.id, 'course_id': period.course_id, 'nrc': period.nrc, 'semester': period.semester })

@period_bp.route('/', methods=['POST'])
def create_period():
    data = request.get_json()
    period = Period(course_id=data['course_id'], nrc=data['nrc'], semester=data['semester'])
    db.session.add(period)
    db.session.commit()
    return jsonify({ 'message': 'Periodo creado', 'id': period.id }), 201

@period_bp.route('/<int:id>', methods=['PUT'])
def update_period(id):
    period = Period.query.get_or_404(id)
    data = request.get_json()
    period.course_id = data.get('course_id', period.course_id)
    period.nrc = data.get('nrc', period.nrc)
    period.semester = data.get('semester', period.semester)
    db.session.commit()
    return jsonify({ 'message': 'Periodo actualizado' })

@period_bp.route('/<int:id>', methods=['DELETE'])
def delete_period(id):
    period = Period.query.get_or_404(id)
    db.session.delete(period)
    db.session.commit()
    return jsonify({ 'message': 'Periodo eliminado' })