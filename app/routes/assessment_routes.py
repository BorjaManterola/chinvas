from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.assessment import Assessment
from app.models.task import Task
from app.models.section import Section
from app import db

assessment_bp= Blueprint('assessment_routes', __name__)

@assessment_bp.route('/sections/<int:id>/assessments')
def manage_assessments(id):
    section = Section.query.get_or_404(id)
    assessments = Assessment.query.filter_by(section_id=id).all()
    return render_template('assessments/index.html', section=section, assessments=assessments)

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
            if weighting < 0 or weighting > 100:
                flash('Weighting must be between 0 and 100', 'danger')
                return render_template('assessments/form.html', section=section, assessment=None)
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
        return redirect(url_for('assessment_routes.manage_assessments', id=id))

    return render_template('assessments/form.html', section=section, assessment=None)

@assessment_bp.route('/assessments/<int:id>/edit', methods=['GET', 'POST'])
def edit_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    section = Section.query.get_or_404(assessment.section_id)

    if request.method == 'POST':
        name = request.form.get('name')
        type_evaluate = request.form.get('type_evaluate')
        weighting = request.form.get('weighting')

        if not name or not type_evaluate or not weighting:
            flash('All fields are required', 'danger')
            return render_template('assessments/form.html', assessment=assessment, section=section)

        try:
            weighting = int(weighting)
            if weighting < 0 or weighting > 100:
                flash('Weighting must be between 0 and 100', 'danger')
                return render_template('assessments/form.html', assessment=assessment, section=section)
        except ValueError:
            flash('Weighting must be a number', 'danger')
            return render_template('assessments/form.html', assessment=assessment, section=section)

        total_weight = db.session.query(db.func.sum(Assessment.weighting)).filter_by(
            section_id=assessment.section_id).filter(Assessment.id != id).scalar() or 0
        if total_weight + weighting > 100:
            flash(f'Total weighting cannot exceed 100%. Current total: {total_weight}%', 'danger')
            return render_template('assessments/form.html', assessment=assessment, section=section)

        assessment.name = name
        assessment.type_evaluate = type_evaluate
        assessment.weighting = weighting
        db.session.commit()

        flash('Assessment updated successfully', 'success')
        return redirect(url_for('assessment_routes.manage_assessments', id=assessment.section_id))

    return render_template('assessments/form.html', assessment=assessment, section=section)

@assessment_bp.route('/assessments/<int:id>/delete', methods=['POST'])
def delete_assessment(id):
    assessment = Assessment.query.get_or_404(id)
    section_id = assessment.section_id
    
    # Check if there are tasks associated with this assessment
    tasks = Task.query.filter_by(assesstment_id=id).all()
    if tasks:
        flash('Cannot delete assessment with associated tasks. Delete tasks first.', 'danger')
        return redirect(url_for('assessment_routes.manage_assessments', id=section_id))
    
    db.session.delete(assessment)
    db.session.commit()
    
    flash('Assessment deleted successfully', 'success')
    return redirect(url_for('assessment_routes.manage_assessments', id=section_id))

@assessment_bp.route('/assessments/<int:id>/tasks')
def view_tasks(id):
    assessment = Assessment.query.get_or_404(id)
    tasks = Task.query.filter_by(assesstment_id=id).all()
    return render_template('tasks/index.html', assessment=assessment, tasks=tasks)

@assessment_bp.route('/assessments/<int:id>/tasks/new', methods=['GET', 'POST'])
def create_task(id):
    assessment = Assessment.query.get_or_404(id)
    
    if request.method == 'POST':
        name = request.form.get('name')
        optional = request.form.get('optional') == 'on'
        weighting = request.form.get('weighting')
        date = request.form.get('date')
        
        if not name or not weighting or not date:
            flash('Name, weighting and date are required', 'danger')
            return render_template('tasks/create.html', assessment=assessment)
        
        try:
            weighting = int(weighting)
            if weighting < 0 or weighting > 100:
                flash('Weighting must be between 0 and 100', 'danger')
                return render_template('tasks/create.html', assessment=assessment)
        except ValueError:
            flash('Weighting must be a number', 'danger')
            return render_template('tasks/create.html', assessment=assessment)
        
        # Check if total weighting of tasks exceeds 100%
        total_weight = db.session.query(db.func.sum(Task.weighting)).filter_by(assesstment_id=id).scalar() or 0
        if total_weight + weighting > 100:
            flash(f'Total task weighting cannot exceed 100%. Current total: {total_weight}%', 'danger')
            return render_template('tasks/create.html', assessment=assessment)
        
        task = Task(
            assesstment_id=id,
            name=name,
            optional=optional,
            weighting=weighting,
            date=date
        )
        db.session.add(task)
        db.session.commit()
        
        flash('Task created successfully', 'success')
        return redirect(url_for('assessment_routes.view_tasks', id=id))
    
    return render_template('tasks/create.html', assessment=assessment)

