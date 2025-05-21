import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..services.user_service import UserService
from sqlalchemy.exc import IntegrityError
from flask import (request,jsonify,Blueprint,send_from_directory,current_app)
from flasgger import swag_from
import json

auth_bp = Blueprint("auth", __name__)
user_service = UserService()


@auth_bp.route("/register", methods=["POST"])
@swag_from("../../static/docs/add_user_docs.yaml")
def register():
    """
    Enregistre un nouvel utilisateur.

    Cette route reçoit des données JSON pour créer un nouvel utilisateur via le service `user_service`.
    Retourne un message de succès avec un code 201, ou un message d'erreur en cas de problème.
    """
    try:
        user_data = request.get_json()
        response = user_service.create_user(user_data)
        return jsonify(response), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        return jsonify({"error": f"Une erreur inattendue est survenue : {str(e)}"}), 500


@auth_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """
    Met à jour les informations d'un utilisateur existant.

    Prend un identifiant d'utilisateur dans l'URL et des données JSON dans le corps de la requête.
    Retourne un message de succès ou une erreur.
    """
    data = request.get_json()
    try:
        user_service.update_user(data, user_id)
        return jsonify({"message": "Utilisateur mis à jour avec succès."}), 200
    except ValueError as e:
        return jsonify({"erreur": str(e)}), 404
    except IntegrityError as e:
        return jsonify({"erreur": str(e)}), 409
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authentifie un utilisateur.

    Reçoit un nom d'utilisateur et un mot de passe en JSON.
    Retourne un token JWT si les identifiants sont valides.
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Données manquantes"}), 400

    result, status = user_service.login(username, password)
    return jsonify(result), status


@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    """
    Récupère la liste de tous les utilisateurs.

    Cette route nécessite une authentification JWT.
    Retourne un tableau JSON d'utilisateurs.
    """
    users = user_service.get_users()
    return jsonify(users), 200


@auth_bp.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    """
    Sert un fichier téléchargé depuis le dossier d'upload.

    Prend le nom du fichier en paramètre et retourne le fichier s'il existe.
    """
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@auth_bp.route("/uploads/team_photos/<filename>", methods=["GET"])
def uploaded_event_photos(filename):
    """
    Sert un fichier téléchargé depuis le dossier d'upload.

    Prend le nom du fichier en paramètre et retourne le fichier s'il existe.
    """
    return send_from_directory(current_app.config["TEAM_PHOTOS_FOLDER"], filename)


@auth_bp.route("/users/profile", methods=["PUT"])
@jwt_required()
def update_profile_image():
    """
    Met à jour l'image de profil de l'utilisateur authentifié.

    Nécessite un fichier dans la requête et un JWT valide.
    Retourne l'image mise à jour ou une erreur.
    """
    if "file" not in request.files:
        return jsonify({"message": "Fichier manquant"}), 400
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "Nom de fichier vide"}), 400
    try:
        profile_image = user_service.update_profile_image(current_user_json["id"], file)
        return jsonify({"image": profile_image}), 201
    except Exception as e:
        return jsonify({"erreur": str(e)}), 500


@auth_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id: int):
    """
    Récupère les informations d'un utilisateur via son identifiant.

    Retourne les données utilisateur sous forme JSON.
    """
    user = user_service.get_user_by_id(user_id)
    return user

@auth_bp.route("/users/phone", methods=["GET"])
@jwt_required()
def get_user_by_phone():
    """
    Get user information by phone number.
    
    Query Parameters:
        phone (str): The phone number to search for
        
    Returns:
        JSON response with user data if found, 404 if not found
    """
    try:
        phone = request.args.get('phone')
        if not phone:
            return jsonify({
                "message": "Phone number is required",
                "error": "Missing phone parameter"
            }), 400
            
        user = user_service.get_user_by_phone(phone)
        return jsonify(user), 200
    except ValueError as e:
        return jsonify({
            "message": "User not found",
            "error": str(e)
        }), 404
    except Exception as e:
        return jsonify({
            "message": "Error processing phone number",
            "error": str(e)
        }), 500
