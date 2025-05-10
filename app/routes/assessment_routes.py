from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.assessment import Assessment
from app.models.task import Task
from app.models.section import Section
from app import db

assessment_bp= Blueprint('assessment_routes', __name__)

@assessment_bp.route('/sections/<int:id>/assessments/new', methods=['GET', 'POST'])
def create_assessment(id):
    section = Section.query.get_or_404(id)

    if request.method == 'POST':
        name = request.form.get('name')
        type_evaluate = request.form.get('type_evaluate')
        weighting = request.form.get('weighting')

        if not name or not type_evaluate or not weighting:
            flash('All fields are required', 'danger')
            return render_template('assessments/form.html', section=section, assessment=None)

        try:
            weighting = int(weighting)
        except ValueError:
            flash('Weighting must be a number', 'danger')
            return render_template('assessments/form.html', section=section, assessment=None)

        total_weight = db.session.query(db.func.sum(Assessment.weighting)).filter_by(section_id=id).scalar() or 0
        if total_weight + weighting > 100 and section.type_evaluate == 'Percentage':
            flash(f'Total percentage cannot exceed 100%. Current total: {total_weight}%', 'danger')
            return render_template('assessments/form.html', section=section, assessment=None)

        assessment = Assessment(
            section_id=id,
            name=name,
            type_evaluate=type_evaluate,
            weighting=weighting
        )
        db.session.add(assessment)
        db.session.commit()

        flash('Assessment created successfully', 'success')
        return redirect(url_for('section_routes.show_section', id=id))

    return render_template('assessments/form.html', section=section, assessment=None)

@assessment_bp.route('/assessments/<int:id>', methods=['GET'])
def show_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    tasks = Task.query.filter_by(assessment_id=id).all()
    return render_template('assessments/show.html', assessment=assessment, tasks=tasks)

@assessment_bp.route('/assessments/<int:id>/edit', methods=['GET', 'POST'])
def edit_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    section = Section.query.get_or_404(assessment.section_id)

    if request.method == 'POST':
        if not _validate_assessment_form(request.form, assessment, section):
            return render_template('assessments/form.html', assessment=assessment, section=section)

        _update_assessment_from_form(assessment, request.form)
        db.session.commit()

        flash('Assessment updated successfully', 'success')
        return redirect(url_for('section_routes.show_section', id=section.id))

    return render_template('assessments/form.html', assessment=assessment, section=section)


def _validate_assessment_form(form, assessment, section):
    name = form.get('name')
    type_evaluate = form.get('type_evaluate')
    weighting = form.get('weighting')

    if not name or not type_evaluate or not weighting:
        flash('All fields are required', 'danger')
        return False

    try:
        weighting = int(weighting)
    except ValueError:
        flash('Weighting must be a number', 'danger')
        return False

    if section.type_evaluate == 'Percentage':
        if weighting < 0 or weighting > 100:
            flash('Weighting must be between 0 and 100', 'danger')
            return False

        total_weight = db.session.query(db.func.sum(Assessment.weighting)).filter_by(
            section_id=assessment.section_id).filter(Assessment.id != assessment.id).scalar() or 0

        if total_weight + weighting > 100:
            flash(f'Total percentage cannot exceed 100%. Current total: {total_weight}%', 'danger')
            return False

    return True


def _update_assessment_from_form(assessment, form):
    assessment.name = form.get('name')
    assessment.type_evaluate = form.get('type_evaluate')
    assessment.weighting = int(form.get('weighting'))


@assessment_bp.route('/assessments/<int:id>/delete', methods=['POST'])
def delete_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    section_id = assessment.section_id  # ✅ Guarda el ID antes de eliminar
    
    db.session.delete(assessment)
    db.session.commit()

    flash('Assessment deleted successfully', 'success')
    return redirect(url_for('section_routes.show_section', id=section_id))