import os
from flask import Flask
from flask_jwt_extended import JWTManager
from app.controllers.team_routes import team_bp
from app.controllers.user_routes import auth_bp
from app.controllers.event_routes import event_bp
from app.controllers.sport_routes import sport_bp
from config import Config, db
from flasgger import Swagger
from flask_cors import CORS

from app.controllers.admin_event_controller import admin_event_bp
from app.controllers.admin_user_controller import admin_user_bp 
from app.controllers.admin_controller import admin_admin_bp


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
UPLOAD_FOLDER = "uploads"
TEAM_PHOTOS_FOLDER = os.path.join(UPLOAD_FOLDER, "team_photos")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEAM_PHOTOS_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def create_app():
    app = Flask(__name__)
    # application des cors
    CORS(app)
    app.config["UPLOAD_FOLDER"] = os.path.abspath("uploads")
    app.config["TEAM_PHOTOS_FOLDER"] = os.path.abspath(TEAM_PHOTOS_FOLDER)
    # declaration de
    swagger = Swagger(app)
    JWTManager(app)
    CORS(app, resources={r"/auth/*": {"origins": "http://localhost:3000"}})
    app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(event_bp, url_prefix="/event")
    app.register_blueprint(sport_bp, url_prefix="/sport")
    app.register_blueprint(team_bp, url_prefix="/team")

       #admin
    #app.register_blueprint(admin_bp)
    app.register_blueprint(admin_event_bp)
    app.register_blueprint(admin_user_bp)
    app.register_blueprint(admin_admin_bp)



    return app
