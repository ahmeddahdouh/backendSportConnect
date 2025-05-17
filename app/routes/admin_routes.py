import bcrypt
from app.models.event import Event
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app.models.admin import Admin
import json
from config import db



from app.models.user import User

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/loginAdmin", methods=["POST"])
def admin_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Champs requis"}), 400

    admin = Admin.query.filter_by(email=email).first()

    if not admin:
        return jsonify({"error": "Admin introuvable"}), 404

    try:
        
        if admin.password.startswith('$2b$'):
            if not bcrypt.checkpw(password.encode("utf-8"), admin.password.encode("utf-8")):
                return jsonify({"error": "Mot de passe incorrect"}), 401
        else:
            if password != admin.password:
                return jsonify({"error": "Mot de passe incorrect"}), 401
    except Exception as e:
        print("Erreur bcrypt :", e)
        return jsonify({"error": "Erreur interne"}), 500

    admin_token = create_access_token(identity=json.dumps({
        "id": admin.id,
        "username": admin.username,
        "email": admin.email,
        "role": "admin"
    }))

    return jsonify({
        "admin_token": admin_token,
        "admin": {
            "id": admin.id,
            "username": admin.username
        }
    }), 200
