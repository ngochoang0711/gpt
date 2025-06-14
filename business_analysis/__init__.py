from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        SQLALCHEMY_DATABASE_URI='sqlite:///business_analysis.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        GEMINI_API_KEY=os.environ.get('GEMINI_API_KEY'),
    )
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        from . import models
        db.create_all()

        from .auth import auth_bp
        from .main import main_bp
        from .project import project_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)
        app.register_blueprint(project_bp)

        return app
