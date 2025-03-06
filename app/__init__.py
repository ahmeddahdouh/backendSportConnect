import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from app.routes.app_routes import main_bp
from app.routes.user_routes import auth_bp
from app.routes.event_routes import event_bp
from app.routes.sport_routes import sport_bp
from config import Config, db
from flask_cors import CORS

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def create_app():
    app = Flask(__name__)
    # application des cors
    CORS(app)

    JWTManager(app)
    CORS(app, resources={r"/auth/*": {"origins": "http://localhost:3000"}})
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp, url_prefix="")
    app.register_blueprint(event_bp, url_prefix="/event")
    app.register_blueprint(sport_bp, url_prefix="/sport")
    return app
