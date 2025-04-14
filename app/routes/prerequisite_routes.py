from flask import Blueprint, request, jsonify
from app.models.prerequisite import Prerequisite
from app import db

prerequisite_bp = Blueprint('prerequisites', __name__, url_prefix='/prerequisites')

@prerequisite_bp.route('/', methods=['POST'])
def create_prerequisite():
    data = request.get_json()
    prerequisite = Prerequisite(period_id=data['period_id'], prerequisite_id=data['prerequisite_id'])
    db.session.add(prerequisite)
    db.session.commit()
    return jsonify({ 'message': 'Prerrequisito creado', 'id': prerequisite.id }), 201

@prerequisite_bp.route('/', methods=['GET'])
def get_prerequisites():
    prerequisites = Prerequisite.query.all()
    return jsonify([{ 'id': p.id, 'period_id': p.period_id, 'prerequisite_id': p.prerequisite_id } for p in prerequisites])

@prerequisite_bp.route('/<int:id>', methods=['GET'])
def get_prerequisite(id):
    prerequisite = Prerequisite.query.get_or_404(id)
    return jsonify({ 'id': prerequisite.id, 'period_id': prerequisite.period_id, 'prerequisite_id': prerequisite.prerequisite_id })

@prerequisite_bp.route('/<int:id>', methods=['PUT'])
def update_prerequisite(id):
    prerequisite = Prerequisite.query.get_or_404(id)
    data = request.get_json()
    prerequisite.period_id = data.get('period_id', prerequisite.period_id)
    prerequisite.prerequisite_id = data.get('prerequisite_id', prerequisite.prerequisite_id)
    db.session.commit()
    return jsonify({ 'message': 'Prerrequisito actualizado' })

@prerequisite_bp.route('/<int:id>', methods=['DELETE'])
def delete_prerequisite(id):
    prerequisite = Prerequisite.query.get_or_404(id)
    db.session.delete(prerequisite)
    db.session.commit()
    return jsonify({ 'message': 'Prerrequisito eliminado' })