import pytest
from app import create_app
from flask import Flask
from app.controllers.sport_routes import sport_bp
from config import db

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_hello_world(client):
    response = client.get("/sport/")
    assert response.status_code == 200
