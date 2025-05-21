from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app import create_app
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the Flask application
app = create_app()
jwt = JWTManager(app)
main_bp = Blueprint("main", __name__)

if __name__ == '__main__':
    # Development server configuration
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 8080))
    
    print(f"Starting development server on {host}:{port}")
    print(f"Debug mode: {'enabled' if debug_mode else 'disabled'}")
    
    app.run(
        host=host,
        port=port,
        debug=debug_mode,
        use_reloader=True
    )
