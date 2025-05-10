from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
import json

from app.services.team_service import TeamService

team_bp = Blueprint("team", __name__)
team_service = TeamService()


@team_bp.route("/", methods=["POST"])
def create_team():
    """Création d'une équipe"""
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    manager_id = current_user_json.get("id")

    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")
    profile_picture = data.get("profile_picture", "")

    if not name:
        return {"message": "Team name is required."}, 400

    result, status_code = team_service.create_team(manager_id, name, description, profile_picture)
    return result, status_code


@team_bp.route("/<int:team_id>", methods=["DELETE"])
def delete_team(team_id):
    """Suppression d'une équipe"""
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    manager_id = current_user_json.get("id")

    result, status_code = team_service.delete_team(team_id, manager_id)
    return result, status_code


@team_bp.route("/<int:team_id>", methods=["PUT"])
def update_team(team_id):
    """Modification des informations de l'équipe"""
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    manager_id = current_user_json.get("id")

    data = request.get_json()

    result, status_code = team_service.update_team(team_id, manager_id, data)
    return result, status_code


@team_bp.route("/<int:team_id>/members", methods=["POST"])
def add_team_member(team_id):
    """Ajout d'un membre à l'équipe"""
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return {"message": "User ID is required."}, 400

    result, status_code = team_service.add_team_member(team_id, user_id)
    return result, status_code


@team_bp.route("/<int:team_id>/members/<int:user_id>", methods=["DELETE"])
def remove_team_member(team_id, user_id):
    """Suppression d'un membre de l'équipe"""
    result, status_code = team_service.remove_team_member(team_id, user_id)
    return result, status_code


@team_bp.route("/<int:team_id>/sports", methods=["POST"])
def add_team_sport(team_id):
    """Ajout d'un sport pratiqué par l'équipe"""
    data = request.get_json()
    sport_id = data.get("sport_id")
    sport_stat = data.get("sport_stat", {})

    if not sport_id:
        return {"message": "Sport ID is required."}, 400

    result, status_code = team_service.add_team_sport(team_id, sport_id, sport_stat)
    return result, status_code


@team_bp.route("/<int:team_id>/sports/<int:sport_id>", methods=["DELETE"])
def remove_team_sport(team_id, sport_id):
    """Suppression d'un sport joué par l'équipe"""
    result, status_code = team_service.remove_team_sport(team_id, sport_id)
    return result, status_code


@team_bp.route("/<int:team_id>/sports/<int:sport_id>", methods=["PUT"])
def update_team_sport_stat(team_id, sport_id):
    """Modification des stats d'une équipe dans un sport précis"""
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json.get("id")

    data = request.get_json()
    sport_stat = data.get("sport_stat", {})

    result, status_code = team_service.update_team_sport_stat(team_id, sport_id, user_id, sport_stat)
    return result, status_code


@team_bp.route("/<int:team_id>", methods=["GET"])
def get_team_info(team_id):
    """Récupère les informations détaillées d'une équipe"""
    result, status_code = team_service.get_team_info(team_id)
    return result, status_code


@team_bp.route("/users/teams", methods=["GET"])
def get_user_teams():
    """Récupère les équipes dont l'utilisateur est membre"""
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json.get("id")

    result, status_code = team_service.get_user_teams(user_id)
    return result, status_code