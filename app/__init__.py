from flask import Flask

from app.models import db
from app.routes import auth_bp
from config import config


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.register_blueprint(auth_bp, url_prefix='/auth')
    return app

