from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Project
from . import db

project_bp = Blueprint('projects', __name__, url_prefix='/projects')

@project_bp.route('/')
@login_required
def list_projects():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('projects/list.html', projects=projects)

@project_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description')
        project = Project(user_id=current_user.id, name=name, description=description)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('projects.list_projects'))
    return render_template('projects/form.html', project=None)

@project_bp.route('/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        return redirect(url_for('projects.list_projects'))
    if request.method == 'POST':
        project.name = request.form['name']
        project.description = request.form.get('description')
        db.session.commit()
        return redirect(url_for('projects.list_projects'))
    return render_template('projects/form.html', project=project)

@project_bp.route('/<int:project_id>/delete', methods=['POST'])
@login_required
def delete(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id == current_user.id:
        db.session.delete(project)
        db.session.commit()
    return redirect(url_for('projects.list_projects'))

@project_bp.route('/<int:project_id>')
@login_required
def detail(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        return redirect(url_for('projects.list_projects'))
    tab = request.args.get('tab', 'overview')
    return render_template('projects/detail.html', project=project, tab=tab)
