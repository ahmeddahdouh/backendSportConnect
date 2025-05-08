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


if __name__ == "__main__":
    # Get configuration from environment variables with secure defaults
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '127.0.0.1')  # Default to localhost
    port = int(os.getenv('FLASK_PORT', '5000'))
    
    # Only allow debug mode in development
    if debug_mode and os.getenv('FLASK_ENV') != 'development':
        print("Warning: Debug mode is only allowed in development environment")
        debug_mode = False
    
    app.run(host=host, port=port, debug=debug_mode)

