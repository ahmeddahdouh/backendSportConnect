from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity
import json
from app.associations.team_users_sports import TeamUsers, TeamSports
from config import db
from app.models.team import Team

team_bp = Blueprint("team", __name__)


@team_bp.route("/", methods=["POST"])  # création d'une équipe
def create_team():
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    manager_id = current_user_json.get("id")

    data = request.get_json()
    name = data.get("name")
    description = data.get("description", "")
    profile_picture = data.get("profile_picture", "")

    if not name:
        return {"message": "Team name is required."}, 400

    new_team = Team(
        name=name,
        description=description,
        profile_picture=profile_picture,
        manager_id=manager_id,
    )
    db.session.add(new_team)
    db.session.commit()

    return {"message": "Team created successfully.", "team_id": new_team.id}, 201


@team_bp.route("/<int:team_id>", methods=["DELETE"])  # suppression d'une équipe
def delete_team(team_id):
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    manager_id = current_user_json.get("id")

    team = Team.query.get(team_id)
    if not team:
        return {"message": "Team not found."}, 404

    if team.manager_id != manager_id:
        return {"message": "Unauthorized."}, 403

    db.session.delete(team)
    db.session.commit()

    return {"message": "Team deleted successfully."}, 200


@team_bp.route(
    "/<int:team_id>", methods=["PUT"]
)  # modification des informations de l'équipe
def update_team(team_id):
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    manager_id = current_user_json.get("id")

    team = Team.query.get(team_id)
    if not team:
        return {"message": "Team not found."}, 404

    if team.manager_id != manager_id:
        return {"message": "Unauthorized."}, 403

    data = request.get_json()
    team.name = data.get("name", team.name)
    team.description = data.get("description", team.description)
    team.profile_picture = data.get("profile_picture", team.profile_picture)
    team.manager_id = data.get("manager_id", team.manager_id)

    db.session.commit()

    return {"message": "Team updated successfully."}, 200


@team_bp.route(
    "/<int:team_id>/members", methods=["POST"]
)  # ajout d'un membre à l'équipe
def add_team_member(team_id):
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return {"message": "User ID is required."}, 400

    new_member = TeamUsers(user_id=user_id, team_id=team_id)
    db.session.add(new_member)
    db.session.commit()

    return {"message": "Member added successfully."}, 201


@team_bp.route(
    "/<int:team_id>/members/<int:user_id>", methods=["DELETE"]
)  # suppression d'un membre de l'équipe
def remove_team_member(team_id, user_id):
    member = TeamUsers.query.filter_by(team_id=team_id, user_id=user_id).first()
    if not member:
        return {"message": "Member not found in the team."}, 404

    db.session.delete(member)
    db.session.commit()

    return {"message": "Member removed successfully."}, 200


@team_bp.route(
    "/<int:team_id>/sports", methods=["POST"]
)  # ajout d'un sport pratiqué par l'équipe
def add_team_sport(team_id):
    data = request.get_json()
    sport_id = data.get("sport_id")
    sport_stat = data.get("sport_stat", {})

    if not sport_id:
        return {"message": "Sport ID is required."}, 400

    new_sport = TeamSports(team_id=team_id, sport_id=sport_id, sport_stat=sport_stat)
    db.session.add(new_sport)
    db.session.commit()

    return {"message": "Sport added successfully."}, 201


@team_bp.route(
    "/<int:team_id>/sports/<int:sport_id>", methods=["DELETE"]
)  # suppression d'un sport joué par l'équipe
def remove_team_sport(team_id, sport_id):
    team_sport = TeamSports.query.filter_by(team_id=team_id, sport_id=sport_id).first()
    if not team_sport:
        return {"message": "Sport not found in the team."}, 404

    db.session.delete(team_sport)
    db.session.commit()

    return {"message": "Sport removed successfully."}, 200


@team_bp.route(
    "/<int:team_id>/sports/<int:sport_id>", methods=["PUT"]
)  # Modification des stats d'une équipe dans un sport précis
def update_team_sport_stat(team_id, sport_id):
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json.get("id")

    # Verify if the user is the manager of the team
    team = Team.query.get(team_id)
    if not team:
        return {"message": "Team not found."}, 404

    if team.manager_id != user_id:
        return {"message": "You are not authorized to update this team's stats."}, 403

    # Retrieve the team sport entry
    team_sport = TeamSports.query.filter_by(team_id=team_id, sport_id=sport_id).first()
    if not team_sport:
        return {"message": "This sport is not associated with the team."}, 404

    data = request.get_json()
    team_sport.sport_stat = data.get("sport_stat", team_sport.sport_stat)
    db.session.commit()

    return {"message": "Team sport stats updated successfully."}, 200


@team_bp.route("/<int:team_id>", methods=["GET"])  #
def get_team_info(team_id):
    team = Team.query.get(team_id)
    if not team:
        return {"message": "Team not found."}, 404

    # Get sports played by the team
    team_sports = TeamSports.query.filter_by(team_id=team_id).all()
    sports_data = [
        {"sport_id": ts.sport_id, "sport_stat": ts.sport_stat} for ts in team_sports
    ]

    # Get team members
    team_members = TeamUsers.query.filter_by(team_id=team_id).all()
    members_data = [{"user_id": tu.user_id} for tu in team_members]

    # Return full team details
    return {
        "team_id": team.id,
        "name": team.name,
        "description": team.description,
        "profile_picture": team.profile_picture,
        "manager_id": team.manager_id,
        "sports": sports_data,
        "members": members_data,
    }, 200


@team_bp.route("/users/teams", methods=["GET"])
def get_user_teams():
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json.get("id")

    user_teams = TeamUsers.query.filter_by(user_id=user_id).all()

    if not user_teams:
        return {"message": "User has not joined any teams."}, 404

    teams_data = []
    for entry in user_teams:
        team = Team.query.get(entry.team_id)
        teams_data.append(
            {
                "team_id": team.id,
                "name": team.name,
                "description": team.description,
                "profile_picture": team.profile_picture,
            }
        )

    return {"user_id": user_id, "teams": teams_data}, 200
