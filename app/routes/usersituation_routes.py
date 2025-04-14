from flask import Blueprint, render_template, redirect, url_for, request
from app.models.usersituation import UserSituation
from app.models.section import Section
from app.models.user import User
from app import db

usersituation_bp = Blueprint('usersituation_routes', __name__, url_prefix='/usersituations')

@usersituation_bp.route('/<int:id>/show', methods=['GET'])
def show(id):
    usersituation = UserSituation.query.get_or_404(id)
    return render_template('usersituations/show.html', usersituation=usersituation)

@usersituation_bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    usersituation = UserSituation.query.get_or_404(id)
    section_id = usersituation.section_id
    db.session.delete(usersituation)
    db.session.commit()
    return redirect(url_for('section_routes.show_section', id=section_id))

@usersituation_bp.route('/assign/<int:section_id>', methods=['GET', 'POST'])
def assign_users(section_id):
    situation = request.args.get('situation')
    section = Section.query.get_or_404(section_id)

    if not situation or situation not in ['student', 'teacher']:
        return "Invalid or missing situation.", 400

    assigned_ids = {us.user_id for us in section.usersituations if us.situation.strip().lower() == situation}
    users = User.query.filter_by(role=situation.capitalize())\
                      .filter(~User.id.in_(assigned_ids)).all()

    if request.method == 'POST':
        selected_ids = request.form.getlist('user_ids')
        for user_id in selected_ids:
            db.session.add(UserSituation(
                user_id=int(user_id),
                section_id=section_id,
                situation=situation,
                final_grade=None
            ))
        db.session.commit()
        return redirect(url_for('section_routes.show_section', id=section_id))

    return render_template('usersituations/form.html', section=section, users=users, situation=situation)

