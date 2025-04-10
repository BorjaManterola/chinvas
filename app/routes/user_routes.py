from flask import Blueprint, request, jsonify
from app.models.user import User
from flask import render_template
from app import db

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return render_template('users/index.html', users=users)

@user_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({ 'id': user.id, 'name': user.name, 'email': user.email, 'role': user.role })

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(name=data['name'], email=data['email'], role=data['role'], entry_date=data.get('entry_date'))
    db.session.add(user)
    db.session.commit()
    return jsonify({ 'message': 'Usuario creado', 'id': user.id }), 201

@user_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    user.entry_date = data.get('entry_date', user.entry_date)
    db.session.commit()
    return jsonify({ 'message': 'Usuario actualizado' })

@user_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({ 'message': 'Usuario eliminado' })

@user_bp.route('/form', methods=['GET'])
def user_form():
    return render_template('users/form.html')