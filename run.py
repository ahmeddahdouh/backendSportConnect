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

# This file is used by gunicorn in production
# To run in development mode, use main.py instead

if __name__ == '__main__':
    # Only run in development environment
    if os.getenv('FLASK_ENV') == 'development':
        debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        if debug_mode:
            app.logger.warning("Debug mode is enabled. This should not be used in production!")
        app.run(
            host='127.0.0.1',
            port=int(os.getenv('FLASK_PORT', 8080)),
            debug=debug_mode
        )
    else:
        print("This script should only be used in development environment.")
        print("For production, use gunicorn with main.py")

