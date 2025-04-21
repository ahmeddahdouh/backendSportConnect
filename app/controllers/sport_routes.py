import json

from flask_jwt_extended import get_jwt_identity

from app.models.sport import Sport
from flask import Blueprint, request, jsonify

from config import db
from . import row2dict
from ..associations.user_sports import UserSports
from ..models import User

sport_bp = Blueprint("sport_bp", __name__)


@sport_bp.route("/", methods=["GET"])
def getAllSport():
    sports = Sport.query.all()
    return jsonify([row2dict(sport) for sport in sports])

@sport_bp.route("/<int:user_id>", methods=["GET"])
# Obtenir la liste des sports joués par un joueur, et ses stats dans chaque sport
def get_sports_by_user_id(user_id):
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


@sport_bp.route("users/sports", methods=["POST"])
# On envoie un id user, un id sport, et un json (même vide) de stat
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


@sport_bp.route(
    "/<int:sport_id>", methods=["PUT"]
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


@sport_bp.route("users/sports/<int:sport_id>", methods=["DELETE"])  # suppression d'un sport joué
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


