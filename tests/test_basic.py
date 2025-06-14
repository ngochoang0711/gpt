from business_analysis import create_app, db
import pytest

@pytest.fixture
def app():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    res = client.get('/')
    assert res.status_code == 200


def test_ai_query_error(client):
    res = client.post('/ai_query', data={'query': 'hi'})
    assert res.status_code == 500
    data = res.get_json()
    assert 'error' in data
