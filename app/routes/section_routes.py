from flask import Blueprint, request, jsonify
from app.models.section import Section
from app import db

section_bp = Blueprint('sections', __name__, url_prefix='/sections')

@section_bp.route('/', methods=['GET'])
def get_sections():
    sections = Section.query.all()
    return jsonify([{ 'id': s.id, 'period_id': s.period_id, 'code': s.code, 'type_evaluate': s.type_evaluate } for s in sections])

@section_bp.route('/<int:id>', methods=['GET'])
def get_section(id):
    section = Section.query.get_or_404(id)
    return jsonify({ 'id': section.id, 'period_id': section.period_id, 'code': section.code, 'type_evaluate': section.type_evaluate })

@section_bp.route('/', methods=['POST'])
def create_section():
    data = request.get_json()
    section = Section(period_id=data['period_id'], code=data['code'], type_evaluate=data['type_evaluate'])
    db.session.add(section)
    db.session.commit()
    return jsonify({ 'message': 'Sección creada', 'id': section.id }), 201

@section_bp.route('/<int:id>', methods=['PUT'])
def update_section(id):
    section = Section.query.get_or_404(id)
    data = request.get_json()
    section.period_id = data.get('period_id', section.period_id)
    section.code = data.get('code', section.code)
    section.type_evaluate = data.get('type_evaluate', section.type_evaluate)
    db.session.commit()
    return jsonify({ 'message': 'Sección actualizada' })

@section_bp.route('/<int:id>', methods=['DELETE'])
def delete_section(id):
    section = Section.query.get_or_404(id)
    db.session.delete(section)
    db.session.commit()
    return jsonify({ 'message': 'Sección eliminada' })