from flask import Blueprint, request, jsonify
from app.models.member import Member
from app import db

member_bp = Blueprint('members', __name__, url_prefix='/members')

@member_bp.route('/', methods=['GET'])
def get_members():
    members = Member.query.all()
    return jsonify([{ 'group_id': m.group_id, 'user_id': m.user_id } for m in members])

@member_bp.route('/<int:group_id>/<int:user_id>', methods=['GET'])
def get_member(group_id, user_id):
    member = Member.query.get_or_404((group_id, user_id))
    return jsonify({ 'group_id': member.group_id, 'user_id': member.user_id })

@member_bp.route('/', methods=['POST'])
def create_member():
    data = request.get_json()
    member = Member(group_id=data['group_id'], user_id=data['user_id'])
    db.session.add(member)
    db.session.commit()
    return jsonify({ 'message': 'Miembro creado' }), 201

@member_bp.route('/<int:group_id>/<int:user_id>', methods=['DELETE'])
def delete_member(group_id, user_id):
    member = Member.query.get_or_404((group_id, user_id))
    db.session.delete(member)
    db.session.commit()
    return jsonify({ 'message': 'Miembro eliminado' })