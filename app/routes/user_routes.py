from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.models.user import User
from app import db

user_bp = Blueprint('user_routes', __name__, url_prefix='/users')

# ✅ Lista de usuarios (HTML)
@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return render_template('users/index.html', users=users)

# ✅ Ver usuario individual como JSON (opcional para API)
@user_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role
    })

# ✅ Mostrar formulario para nuevo usuario (HTML)
@user_bp.route('/create', methods=['GET'])
def new_user_form():
    return render_template('users/form.html', user=None)

# ✅ Crear usuario (HTML o JSON)
@user_bp.route('/', methods=['POST'])
def create_user():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    name = data.get('name')
    email = data.get('email')
    role = data.get('role')
    entry_date = data.get('entry_date')

    # Server-side validation
    if not name or not email or not role:
        return jsonify({'error': 'Name, email, and role are required'}), 400

    if role == 'Student' and not entry_date:
        return jsonify({'error': 'Entry date is required for students'}), 400

    if role == 'Teacher' and entry_date:
        return jsonify({'error': 'Teachers should not have an entry date'}), 400

    user = User(name=name, email=email, role=role, entry_date=entry_date if entry_date else None)
    db.session.add(user)
    db.session.commit()

    if request.is_json:
        return jsonify({'message': 'User created successfully', 'id': user.id}), 201
    return redirect(url_for('user_routes.get_users'))

# ✅ Mostrar formulario para editar usuario
@user_bp.route('/<int:id>/edit', methods=['GET'])
def edit_user_form(id):
    user = User.query.get_or_404(id)
    return render_template('users/form.html', user=user)

# ✅ Actualizar usuario (formulario HTML)
@user_bp.route('/<int:id>', methods=['POST'])
def update_user(id):
    user = User.query.get_or_404(id)
    user.name = request.form['name']
    user.email = request.form['email']
    user.role = request.form['role']
    user.entry_date = request.form.get('entry_date')
    db.session.commit()
    return redirect(url_for('user_routes.get_users'))

# ✅ Eliminar usuario (desde formulario HTML)
@user_bp.route('/<int:id>/delete', methods=['POST'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('user_routes.get_users'))