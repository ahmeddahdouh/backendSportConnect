from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = create_app()
jwt = JWTManager(app)
main_bp = Blueprint("main", __name__)


if __name__ == '__main__':
    # Only run in development environment
    if os.getenv('FLASK_ENV') != 'production':
        app.run(host='127.0.0.1', port=5000, debug=True)
    else:
        print("This script should only be used in development environment.")
        print("For production, use gunicorn with main.py")

