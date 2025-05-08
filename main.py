from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
try:
    load_dotenv()
except:
    pass  # No .env file in production is fine

# Create the Flask application
app = create_app()
jwt = JWTManager(app)
main_bp = Blueprint("main", __name__)

# Only used when running locally
if __name__ == '__main__':
    # Default to localhost for security, can be overridden by environment variable
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 8080))
    app.run(host=host, port=port)
