from flask import Blueprint, render_template, redirect, url_for, request
from app.models.usersituation import UserSituation
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
