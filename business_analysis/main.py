from flask import Blueprint, render_template, request, redirect, url_for, jsonify
main
from flask_login import login_required, current_user
from .models import Task
from . import db
import json
import requests

main_bp = Blueprint('main', __name__)

# Load templates from json file
with open('business_analysis/data/templates.json') as f:
    TEMPLATES = json.load(f)


def gemini_ai_response(query):
    """Call the Gemini API with the provided query string."""
    api_key = current_app.config.get("GEMINI_API_KEY")
    if not api_key:
        return None, "GEMINI_API_KEY not configured"

    endpoint = (
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    )
    params = {"key": api_key}
    payload = {"contents": [{"parts": [{"text": query}]}]}

    try:
        resp = requests.post(endpoint, params=params, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        answer = (
            data.get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text")
        )
        return answer, None
    except Exception:
        return None, "Failed to fetch response"

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

@main_bp.route('/toggle_task/<int:task_id>')
@login_required
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    task.toggle()
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main_bp.route('/delete_task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        abort(403)
    task.delete()
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main_bp.route('/ai_query', methods=['POST'])
@login_required
def ai_query():
    query = request.form['query']
    answer, error = gemini_ai_response(query)
    if error:
        return jsonify({'error': error}), 500
    return jsonify({'answer': answer})
