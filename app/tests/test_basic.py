import pytest
from flask import Flask
from app.routes.app_routes import main_bp  # Adjust this import based on your project structure

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)  # Register your blueprint
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_hello_world(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode() == "Hello World!"
