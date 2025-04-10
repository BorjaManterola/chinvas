from flask import Blueprint, request, render_template, redirect, url_for
from app.models.section import Section
from app.models.period import Period
from app import db

section_bp = Blueprint('section_routes', __name__, url_prefix='/sections')


@section_bp.route('/', methods=['GET'])
def list_sections():
    sections = Section.query.all()
    return render_template('sections/index.html', sections=sections)


@section_bp.route('/new', methods=['GET'])
def new_section_form():
    period_id = request.args.get('period_id', type=int)
    period = Period.query.get(period_id) if period_id else None
    return render_template('sections/form.html', section=None, period=period)


@section_bp.route('/', methods=['POST'])
def create_section():
    nrc = request.form['nrc']
    type_evaluate = request.form['type_evaluate']
    period_id = request.form['period_id']

    section = Section(nrc=nrc, type_evaluate=type_evaluate, period_id=period_id)
    db.session.add(section)
    db.session.commit()

    return redirect(url_for('period_routes.show_period', id=period_id))


@section_bp.route('/<int:id>/edit', methods=['GET'])
def edit_section_form(id):
    section = Section.query.get_or_404(id)
    return render_template('sections/form.html', section=section, period=section.period)


@section_bp.route('/<int:id>', methods=['POST'])
def update_section(id):
    section = Section.query.get_or_404(id)
    section.nrc = request.form['nrc']
    section.type_evaluate = request.form['type_evaluate']
    db.session.commit()
    return redirect(url_for('period_routes.show_period', id=section.period_id))


@section_bp.route('/<int:id>/delete', methods=['POST'])
def delete_section(id):
    section = Section.query.get_or_404(id)
    period_id = section.period_id
    db.session.delete(section)
    db.session.commit()
    return redirect(url_for('period_routes.show_period', id=period_id))
