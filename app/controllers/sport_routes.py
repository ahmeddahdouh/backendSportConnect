import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity

from app.services.sport_service import SportService

sport_bp = Blueprint("sport_bp", __name__)
sport_service = SportService()


@sport_bp.route("/", methods=["GET"])
def get_all_sports():
    """Récupère tous les sports disponibles"""
    sports = sport_service.get_all_sports()
    return jsonify(sports)


@sport_bp.route("/<int:user_id>", methods=["GET"])
def get_sports_by_user_id(user_id):
    """Obtenir la liste des sports joués par un joueur, et ses stats dans chaque sport"""
    result, status_code = sport_service.get_sports_by_user_id(user_id)
    return result, status_code


@sport_bp.route("/users/sports", methods=["POST"])
def add_sport():
    """Ajoute un sport à un utilisateur avec ses statistiques"""
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json.get("id")

    data = request.get_json()
    sport_id = data.get("sport_id")
    sport_stat = data.get("sport_stat", {})

    if not sport_id:
        return {"message": "sport_id is required."}, 400

    result, status_code = sport_service.add_sport_to_user(user_id, sport_id, sport_stat)
    return result, status_code


@sport_bp.route("/<int:sport_id>", methods=["PUT"])
def update_sport_stat(sport_id):
    """Met à jour les statistiques d'un sport pour un utilisateur"""
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json.get("id")

    data = request.get_json()
    sport_stat = data.get("sport_stat", {})

    result, status_code = sport_service.update_sport_stats(user_id, sport_id, sport_stat)
    return result, status_code


@sport_bp.route("/users/sports/<int:sport_id>", methods=["DELETE"])
def delete_sport(sport_id):
    """Supprime un sport de la liste des sports joués par un utilisateur"""
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json.get("id")

    result, status_code = sport_service.delete_sport_from_user(user_id, sport_id)
    return result, status_code