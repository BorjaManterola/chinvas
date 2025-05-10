from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.member import Member
from app.models.group import Group
from app.models.student import Student
from app import db

member_bp = Blueprint('member_routes', __name__, url_prefix='/members')


@member_bp.route('/group/<int:group_id>/new', methods=['GET'])
def new_member_form(group_id):
    group = Group.query.get_or_404(group_id)
    # Opcionalmente filtra solo usuarios que no están ya asignados
    users = User.query.all()
    return render_template('members/form.html', member=None, group=group, users=users)


@member_bp.route('/', methods=['POST'])
def create_member():
    group_id = request.form.get('group_id')
    user_id = request.form.get('user_id')

    if not group_id or not user_id:
        flash("All fields are required.", "danger")
        group = Group.query.get_or_404(group_id)
        users = User.query.all()
        return render_template('members/form.html', member=None, group=group, users=users)

    existing = Member.query.get((group_id, user_id))
    if existing:
        flash("This user is already a member of the group.", "warning")
        return redirect(url_for('group_routes.show_group', id=group_id))

    member = Member(group_id=group_id, user_id=user_id)
    db.session.add(member)
    db.session.commit()
    flash("Member added successfully.", "success")
    return redirect(url_for('group_routes.show_group', id=group_id))


@member_bp.route('/<int:group_id>/<int:user_id>', methods=['GET'])
def show_member(group_id, user_id):
    member = Member.query.get_or_404((group_id, user_id))
    return render_template('members/show.html', member=member)


@member_bp.route('/<int:group_id>/<int:user_id>/delete', methods=['POST'])
def delete_member(group_id, user_id):
    member = Member.query.get_or_404((group_id, user_id))
    db.session.delete(member)
    db.session.commit()
    flash("Member removed successfully.", "success")
    return redirect(url_for('group_routes.show_group', id=group_id))
