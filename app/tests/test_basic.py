import pytest
from app import create_app
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from app.routes.app_routes import main_bp
from app.routes.team_routes import team_bp
from app.routes.user_routes import auth_bp
from app.routes.event_routes import event_bp
from app.routes.sport_routes import sport_bp
from config import Config, db
from flasgger import Swagger
from flask_cors import CORS

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_hello_world(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode() == "Hello World!"
