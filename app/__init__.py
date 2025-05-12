import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from app.controllers.team_routes import team_bp
from app.controllers.user_routes import auth_bp
from app.controllers.event_routes import event_bp
from app.controllers.sport_routes import sport_bp
from config import Config, db
from flasgger import Swagger
from flask_cors import CORS

# Use a dedicated uploads directory in the application root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join(BASE_DIR, "uploads"))
TEAM_PHOTOS_FOLDER = os.getenv("TEAM_PHOTOS_FOLDER", os.path.join(UPLOAD_FOLDER, "team_photos"))
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def create_app(testing=False):
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to SportConnect API!"})
    
    @app.route('/test')
    def test_route():
        return jsonify({"message": "Test route works!"})
    
    if not testing:
        # Create upload directories if they don't exist with proper permissions
        try:
            os.makedirs(UPLOAD_FOLDER, mode=0o755, exist_ok=True)
            os.makedirs(TEAM_PHOTOS_FOLDER, mode=0o755, exist_ok=True)
        except Exception as e:
            app.logger.error(f"Failed to create upload directories: {e}")
            raise RuntimeError("Failed to create required upload directories")
        
        # application des cors
        CORS(app, resources={
            r"/*": {
                "origins": [
                    "http://localhost:3000",
                    "https://sportconnect-front-e283.vercel.app"
                ],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True
            }
        })
        app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
        app.config["TEAM_PHOTOS_FOLDER"] = TEAM_PHOTOS_FOLDER
        # declaration de
        swagger = Swagger(app)
        JWTManager(app)
        app.config.from_object(Config)
        db.init_app(app)
        with app.app_context():
            db.create_all()
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(event_bp, url_prefix="/event")
        app.register_blueprint(sport_bp, url_prefix="/sport")
        app.register_blueprint(team_bp, url_prefix="/team")
    
    return app
