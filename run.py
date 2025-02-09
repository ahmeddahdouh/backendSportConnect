from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app import create_app

app = create_app()
jwt = JWTManager(app)
main_bp = Blueprint("main", __name__)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
