from flask import Blueprint, request, jsonify
from app.models.assessment import Assessment
from app import db

assessment_bp = Blueprint('assessments', __name__, url_prefix='/assessments')

@assessment_bp.route('/', methods=['GET'])
def get_assessments():
    assessments = Assessment.query.all()
    return jsonify([{ 'id': a.id, 'section_id': a.section_id, 'name': a.name, 'type_evaluate': a.type_evaluate, 'weighting': a.weighting } for a in assessments])

@assessment_bp.route('/<int:id>', methods=['GET'])
def get_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    return jsonify({ 'id': assessment.id, 'section_id': assessment.section_id, 'name': assessment.name, 'type_evaluate': assessment.type_evaluate, 'weighting': assessment.weighting })

@assessment_bp.route('/', methods=['POST'])
def create_assessment():
    data = request.get_json()
    assessment = Assessment(section_id=data['section_id'], name=data['name'], type_evaluate=data['type_evaluate'], weighting=data['weighting'])
    db.session.add(assessment)
    db.session.commit()
    return jsonify({ 'message': 'Evaluación creada', 'id': assessment.id }), 201

@assessment_bp.route('/<int:id>', methods=['PUT'])
def update_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    data = request.get_json()
    assessment.section_id = data.get('section_id', assessment.section_id)
    assessment.name = data.get('name', assessment.name)
    assessment.type_evaluate = data.get('type_evaluate', assessment.type_evaluate)
    assessment.weighting = data.get('weighting', assessment.weighting)
    db.session.commit()
    return jsonify({ 'message': 'Evaluación actualizada' })

@assessment_bp.route('/<int:id>', methods=['DELETE'])
def delete_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    db.session.delete(assessment)
    db.session.commit()
    return jsonify({ 'message': 'Evaluación eliminada' })