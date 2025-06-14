from business_analysis import create_app, db
from business_analysis import models
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


def signup(client, username="user", password="pass"):
    return client.post(
        "/auth/signup",
        data={"username": username, "password": password},
        follow_redirects=True,
    )


def test_task_toggle_and_delete(client, app):
    signup(client)

    # Add a task
    client.post("/add_task", data={"title": "Test"}, follow_redirects=True)

    with app.app_context():
        task = db.session.execute(db.select(models.Task)).scalars().first()
        assert task is not None
        task_id = task.id
        assert task.completed is False

    # Toggle completion
    res = client.get(f"/toggle_task/{task_id}", follow_redirects=True)
    assert res.status_code == 200
    assert b"Complete" in res.data

    with app.app_context():
        task = models.Task.query.get(task_id)
        assert task.completed is True

    # Delete task
    res = client.get(f"/delete_task/{task_id}", follow_redirects=True)
    assert res.status_code == 200

    with app.app_context():
        assert models.Task.query.get(task_id) is None
