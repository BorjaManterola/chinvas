from flask import Blueprint, request, jsonify
from app.models.group import Group
from app import db

group_bp = Blueprint('groups', __name__, url_prefix='/groups')

@group_bp.route('/', methods=['GET'])
def get_groups():
    groups = Group.query.all()
    return jsonify([{ 'id': g.id, 'section_id': g.section_id, 'name': g.name } for g in groups])

@group_bp.route('/<int:id>', methods=['GET'])
def get_group(id):
    group = Group.query.get_or_404(id)
    return jsonify({ 'id': group.id, 'section_id': group.section_id, 'name': group.name })

@group_bp.route('/', methods=['POST'])
def create_group():
    data = request.get_json()
    group = Group(section_id=data['section_id'], name=data['name'])
    db.session.add(group)
    db.session.commit()
    return jsonify({ 'message': 'Grupo creado', 'id': group.id }), 201

@group_bp.route('/<int:id>', methods=['PUT'])
def update_group(id):
    group = Group.query.get_or_404(id)
    data = request.get_json()
    group.section_id = data.get('section_id', group.section_id)
    group.name = data.get('name', group.name)
    db.session.commit()
    return jsonify({ 'message': 'Grupo actualizado' })

@group_bp.route('/<int:id>', methods=['DELETE'])
def delete_group(id):
    group = Group.query.get_or_404(id)
    db.session.delete(group)
    db.session.commit()
    return jsonify({ 'message': 'Grupo eliminado' })