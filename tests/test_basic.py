import pytest
from business_analysis import create_app, db
from werkzeug.security import generate_password_hash
from business_analysis.models import User

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()


def test_index(client):
    res = client.get('/')
    assert res.status_code == 200


def test_signup_missing_fields(client):
    res = client.post('/auth/signup', data={'username': ''})
    assert res.status_code == 400
    assert b'Username and password are required.' in res.data


def test_signup_duplicate_user(client, app):
    with app.app_context():
        user = User(username='alice', password=generate_password_hash('pass'))
        db.session.add(user)
        db.session.commit()
    res = client.post('/auth/signup', data={'username': 'alice', 'password': 'new'})
    assert res.status_code == 400
    assert b'Username exists' in res.data


def test_login_missing_fields(client):
    res = client.post('/auth/login', data={'username': 'bob'})
    assert res.status_code == 400
    assert b'Username and password are required.' in res.data


def test_login_invalid_credentials(client, app):
    with app.app_context():
        user = User(username='bob', password=generate_password_hash('pass'))
        db.session.add(user)
        db.session.commit()
    res = client.post('/auth/login', data={'username': 'bob', 'password': 'wrong'})
    assert res.status_code == 400
    assert b'Invalid credentials.' in res.data
