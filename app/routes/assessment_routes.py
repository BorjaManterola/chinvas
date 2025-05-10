from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.assessment import Assessment
from app.models.task import Task
from app.models.section import Section
from app import db

assessment_bp = Blueprint('assessment_routes', __name__, url_prefix='/assessments')


@assessment_bp.route('/section/<int:section_id>/new', methods=['GET'])
def new_assessment_form(section_id):
    section = Section.query.get_or_404(section_id)
    return render_template('assessments/form.html', assessment=None, section=section)


@assessment_bp.route('/', methods=['POST'])
def create_assessment():
    section_id = request.form.get('section_id')
    section = Section.query.get_or_404(section_id)

    if not _validate_assessment_form(request.form, None, section):
        return render_template('assessments/form.html', assessment=None, section=section)

    assessment = Assessment(
        section_id=section.id,
        name=request.form['name'],
        type_evaluate=request.form['type_evaluate'],
        weighting=int(request.form['weighting'])
    )

    db.session.add(assessment)
    db.session.commit()
    flash('Assessment created successfully.', 'success')
    return redirect(url_for('section_routes.show_section', id=section.id))


@assessment_bp.route('/<int:id>', methods=['GET'])
def show_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    tasks = Task.query.filter_by(assessment_id=id).all()
    return render_template('assessments/show.html', assessment=assessment, tasks=tasks)


@assessment_bp.route('/<int:id>/edit', methods=['GET'])
def edit_assessment_form(id):
    assessment = Assessment.query.get_or_404(id)
    section = Section.query.get_or_404(assessment.section_id)
    return render_template('assessments/form.html', assessment=assessment, section=section)


@assessment_bp.route('/<int:id>', methods=['POST'])
def update_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    section = Section.query.get_or_404(assessment.section_id)

    if not _validate_assessment_form(request.form, assessment, section):
        return render_template('assessments/form.html', assessment=assessment, section=section)

    _update_assessment_from_form(assessment, request.form)
    db.session.commit()
    flash('Assessment updated successfully.', 'success')
    return redirect(url_for('section_routes.show_section', id=section.id))


@assessment_bp.route('/<int:id>/delete', methods=['POST'])
def delete_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    section_id = assessment.section_id
    db.session.delete(assessment)
    db.session.commit()
    flash('Assessment deleted successfully.', 'success')
    return redirect(url_for('section_routes.show_section', id=section_id))


# Helpers

def _validate_assessment_form(form, assessment, section):
    name = form.get('name')
    type_evaluate = form.get('type_evaluate')
    weighting = form.get('weighting')

    if not name or not type_evaluate or not weighting:
        flash('All fields are required.', 'danger')
        return False

    try:
        weighting = int(weighting)
    except ValueError:
        flash('Weighting must be a number.', 'danger')
        return False

    if section.type_evaluate == 'Percentage':
        if weighting < 0 or weighting > 100:
            flash('Weighting must be between 0 and 100.', 'danger')
            return False

        total_weight = db.session.query(db.func.sum(Assessment.weighting))\
            .filter_by(section_id=section.id)\
            .filter(Assessment.id != (assessment.id if assessment else 0))\
            .scalar() or 0

        if total_weight + weighting > 100:
            flash(f'Total percentage cannot exceed 100%. Current total: {total_weight}%', 'danger')
            return False

    return True


def _update_assessment_from_form(assessment, form):
    assessment.name = form.get('name')
    assessment.type_evaluate = form.get('type_evaluate')
    assessment.weighting = int(form.get('weighting'))
