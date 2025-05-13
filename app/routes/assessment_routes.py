from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models.assessment import Assessment
from app.models.section import Section
from app.models.task import Task
from app import db

assessment_bp = Blueprint('assessment_routes', __name__, url_prefix='/assessments')

@assessment_bp.route('/new', methods=['GET'])
def newAssessmentForm():
    section_id = request.args.get('section_id', type=int)
    section = Section.query.get_or_404(section_id)
    return render_template('assessments/form.html', assessment=None, section=section)

@assessment_bp.route('/', methods=['POST'])
def createAssessment():
    section_id = request.form['section_id']
    section = Section.query.get_or_404(section_id)
    name = request.form['name']
    type_evaluate = request.form['type_evaluate']
    weighting = request.form.get('weighting', type=float)

    is_valid, total = Assessment.isValidWeightingInSection(section, weighting)
    if not is_valid:
        flash(f'Total weighting would exceed 100%. Current total: {total:.2f}%. You entered: {weighting:.2f}%.', 'danger')

        return render_template('assessments/form.html', section=section, assessment=None)

    assessment = Assessment(name=name, type_evaluate=type_evaluate,
                            weighting=weighting, section_id=section_id)
    db.session.add(assessment)
    db.session.commit()
    flash('Assessment created successfully.', 'success')
    return redirect(url_for('section_routes.show_section', id=section_id))

@assessment_bp.route('/<int:id>/show', methods=['GET'])
def showAssessment(id):
    assessment = Assessment.query.get_or_404(id)
    tasks = Task.query.filter_by(assessment_id=id).all()
    return render_template('assessments/show.html', assessment=assessment, tasks=tasks)

@assessment_bp.route('/<int:id>/edit', methods=['GET'])
def editAssessmentForm(id):
    assessment = Assessment.query.get_or_404(id)
    section = Section.query.get_or_404(assessment.section_id)
    return render_template('assessments/form.html', assessment=assessment, section=section)

@assessment_bp.route('/<int:id>', methods=['POST'])
def updateAssessment(id):
    assessment = Assessment.query.get_or_404(id)
    section = Section.query.get_or_404(assessment.section_id)
    name = request.form['name']
    type_evaluate = request.form['type_evaluate']
    weighting = request.form.get('weighting', type=float)

    is_valid, total = Assessment.isValidWeightingInSection(section, weighting, exclude_assessment=id)
    if not is_valid:
        flash(f'Total weighting would exceed 100%. Current total: {total:.2f}%. You entered: {weighting:.2f}%.', 'danger')

        return render_template('assessments/form.html', assessment=assessment, section=section)

    assessment.name = name
    assessment.type_evaluate = type_evaluate
    assessment.weighting = weighting
    db.session.commit()
    flash('Assessment updated successfully.', 'success')
    return redirect(url_for('section_routes.show_section', id=section.id))

@assessment_bp.route('/<int:id>/delete', methods=['POST'])
def deleteAssessment(id):
    assessment = Assessment.query.get_or_404(id)
    for task in assessment.tasks:
        db.session.delete(task)
    db.session.delete(assessment)
    db.session.commit()

    flash("Assessment deleted successfully", "success")
    return redirect(url_for('section_routes.show_section', id=assessment.section_id))
