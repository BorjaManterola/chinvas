from flask import Blueprint, request, jsonify
from app.models.usersituation import UserSituation
from app import db

usersituation_bp = Blueprint('usersituations', __name__, url_prefix='/usersituations')

@usersituation_bp.route('/', methods=['GET'])
def get_usersituations():
    usersituations = UserSituation.query.all()
    return jsonify([{ 'user_id': us.user_id, 'section_id': us.section_id, 'situation': us.situation, 'final_grade': us.final_grade } for us in usersituations])

@usersituation_bp.route('/<int:user_id>/<int:section_id>', methods=['GET'])
def get_usersituation(user_id, section_id):
    usersituation = UserSituation.query.get_or_404((user_id, section_id))
    return jsonify({ 'user_id': usersituation.user_id, 'section_id': usersituation.section_id, 'situation': usersituation.situation, 'final_grade': usersituation.final_grade })

@usersituation_bp.route('/', methods=['POST'])
def create_usersituation():
    data = request.get_json()
    usersituation = UserSituation(user_id=data['user_id'], section_id=data['section_id'], situation=data['situation'], final_grade=data.get('final_grade'))
    db.session.add(usersituation)
    db.session.commit()
    return jsonify({ 'message': 'Situación de usuario creada' }), 201

@usersituation_bp.route('/<int:user_id>/<int:section_id>', methods=['PUT'])
def update_usersituation(user_id, section_id):
    usersituation = UserSituation.query.get_or_404((user_id, section_id))
    data = request.get_json()
    usersituation.situation = data.get('situation', usersituation.situation)
    usersituation.final_grade = data.get('final_grade', usersituation.final_grade)
    db.session.commit()
    return jsonify({ 'message': 'Situación de usuario actualizada' })

@usersituation_bp.route('/<int:user_id>/<int:section_id>', methods=['DELETE'])
def delete_usersituation(user_id, section_id):
    usersituation = UserSituation.query.get_or_404((user_id, section_id))
    db.session.delete(usersituation)
    db.session.commit()
    return jsonify({ 'message': 'Situación de usuario eliminada' })