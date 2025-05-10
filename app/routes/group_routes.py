from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.group import Group
from app.models.section import Section
from app import db

group_bp = Blueprint('group_routes', __name__, url_prefix='/groups')


@group_bp.route('/section/<int:section_id>/new', methods=['GET'])
def new_group_form(section_id):
    section = Section.query.get_or_404(section_id)
    return render_template('groups/form.html', group=None, section=section)


@group_bp.route('/', methods=['POST'])
def create_group():
    section_id = request.form.get('section_id')
    name = request.form.get('name')

    if not name or not section_id:
        flash("All fields are required.", "danger")
        section = Section.query.get_or_404(section_id)
        return render_template("groups/form.html", group=None, section=section)

    group = Group(name=name, section_id=section_id)
    db.session.add(group)
    db.session.commit()

    flash("Group created successfully.", "success")
    return redirect(url_for('section_routes.show_section', id=section_id))


@group_bp.route('/<int:id>', methods=['GET'])
def show_group(id):
    group = Group.query.get_or_404(id)
    return render_template('groups/show.html', group=group)


@group_bp.route('/<int:id>/edit', methods=['GET'])
def edit_group_form(id):
    group = Group.query.get_or_404(id)
    section = Section.query.get_or_404(group.section_id)
    return render_template('groups/form.html', group=group, section=section)


@group_bp.route('/<int:id>', methods=['POST'])
def update_group(id):
    group = Group.query.get_or_404(id)
    name = request.form.get('name')

    if not name:
        flash("Group name is required.", "danger")
        section = Section.query.get_or_404(group.section_id)
        return render_template("groups/form.html", group=group, section=section)

    group.name = name
    db.session.commit()
    flash("Group updated successfully.", "success")
    return redirect(url_for('group_routes.show_group', id=group.id))


@group_bp.route('/<int:id>/delete', methods=['POST'])
def delete_group(id):
    group = Group.query.get_or_404(id)
    section_id = group.section_id
    db.session.delete(group)
    db.session.commit()
    flash("Group deleted successfully.", "success")
    return redirect(url_for('section_routes.show_section', id=section_id))
