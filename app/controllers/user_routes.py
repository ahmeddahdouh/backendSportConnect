import os
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from ..associations.user_sports import UserSports
from ..models import Sport
from ..services.user_service import UserService
from config import db
from sqlalchemy.exc import IntegrityError
from flask import (
    request,
    jsonify,
    Blueprint,
    send_from_directory,
    current_app,
)
import bcrypt
from . import row2dict
from flasgger import swag_from
import json
from datetime import timedelta
import uuid



auth_bp = Blueprint("auth", __name__)
user_service = UserService()


@auth_bp.route("/register", methods=["POST"])
@swag_from("../../static/docs/add_user_docs.yaml")
def register():
    try:
        user_data = request.get_json()  # on récupère les données JSON
        response = user_service.create_user(user_data)
        return jsonify(response), 201
    except ValueError as e:
        # Message d'erreur spécifique
        return jsonify({"error": str(e)}), 409  # Code HTTP 409 pour conflit
    except Exception as e:
        # Message d'erreur générique
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500  # Erreur serveur


@auth_bp.route(
    "users/<int:user_id>/sports", methods=["GET"]
)  # Obtenir la liste des sports joués par un joueur, et ses stats dans chaque sport
def get_sports(user_id):
    user_sports = UserSports.query.filter_by(user_id=user_id).all()
    user = User.query.get(user_id)

    if not user_sports:
        return {"message": "User has no associated sports."}, 404

    sports_data = []
    for entry in user_sports:
        sports_data.append(
            {
                "sport_id": entry.sport_id,
                "sport_name": Sport.query.get(entry.sport_id).sport_nom,
                "sport_stat": entry.sport_stat,
            }
        )

    return {
        "user_id": user_id,
        "firstname": user.firstname,
        "familyname": user.familyname,
        "sports": sports_data,
    }, 200


@auth_bp.route(
    "users/sports", methods=["POST"]
)  # On envoie un id user, un id sport, et un json (même vide) de stat
def add_sport():
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json.get("id")

    data = request.get_json()
    sport_id = data.get("sport_id")
    sport_stat = data.get("sport_stat", {})

    if not sport_id:
        return {"message": "sport_id is required."}, 400

    existing_entry = UserSports.query.filter_by(
        user_id=user_id, sport_id=sport_id
    ).first()
    if existing_entry:
        return {"message": "Sport already exists for this user."}, 400

    new_sport = UserSports(user_id=user_id, sport_id=sport_id, sport_stat=sport_stat)
    db.session.add(new_sport)
    db.session.commit()

    return {"message": "Sport added successfully."}, 201


@auth_bp.route(
    "users/sports/<int:sport_id>", methods=["PUT"]
)  # changer les stats d'un user pour un sport précis
def update_sport_stat(sport_id):
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json.get("id")

    data = request.get_json()

    user_sport = UserSports.query.filter_by(user_id=user_id, sport_id=sport_id).first()
    if not user_sport:
        return {"message": "Sport not found for this user."}, 404

    user_sport.sport_stat = data.get("sport_stat", user_sport.sport_stat)
    db.session.commit()

    return {"message": "Sport stats updated successfully."}, 200


@auth_bp.route(
    "users/sports/<int:sport_id>", methods=["DELETE"]
)  # suppression d'un sport joué
def delete_sport(sport_id):
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json.get("id")

    user_sport = UserSports.query.filter_by(user_id=user_id, sport_id=sport_id).first()
    if not user_sport:
        return {"message": "Sport not found for this user."}, 404

    db.session.delete(user_sport)
    db.session.commit()

    return {"message": "Sport removed successfully."}, 200


@auth_bp.route(
    "/users/<int:user_id>", methods=["PUT"])  # modification des informations de l'utilisateur
def update_user(user_id):
    data = request.get_json()
    try:
            user_service.update_user(data, user_id)
            return jsonify({"message": "User updated successfully."}), 200
    except ValueError as e:
        return jsonify({"erreur" : str(e)}),404
    except IntegrityError as e:
        return jsonify({"erreur":str(e)}),409
    except Exception as e:
        return jsonify({"erreur":str(e)}),500


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Missing data"}), 400

    result, status = user_service.login(username, password)
    return jsonify(result), status

@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    users = user_service.get_users()
    return jsonify(users), 200

@auth_bp.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@auth_bp.route("/users/profile", methods=["PUT"])
@jwt_required()
def update_profile_image():
    if "file" not in request.files:
        return jsonify({"message": "Missing file"}), 400
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "Missing file"}), 400
    try :
        profile_image = user_service.update_profile_image(current_user_json["id"], file)
        return jsonify({"image": profile_image }), 201
    except Exception as e:
        return jsonify({"erreur":str(e)}),500


@auth_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id: int):
    user = user_service.get_user_by_id(user_id)
    return user
