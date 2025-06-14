from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Task
from . import db
import json

main_bp = Blueprint('main', __name__)

# Load templates from json file
with open('business_analysis/data/templates.json') as f:
    TEMPLATES = json.load(f)


def fake_ai_response(query):
    # Placeholder for AI integration
    return f"AI Assistant response to: {query}"

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)

@main_bp.route('/templates')
@login_required
def templates():
    return render_template('templates.html', templates=TEMPLATES)

@main_bp.route('/add_task', methods=['POST'])
@login_required
def add_task():
    title = request.form['title']
    task = Task(user_id=current_user.id, title=title)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main_bp.route('/ai_query', methods=['POST'])
@login_required
def ai_query():
    query = request.form['query']
    answer = fake_ai_response(query)
    return jsonify({'answer': answer})
