from app.models.event import Event
from app.models.user import User
from app.associations.event_users import event_users
from flask import Blueprint, request, jsonify
from config import db
from .user_routes import get_user_by_id
from . import row2dict

event_bp = Blueprint("event", __name__)

event_bp = Blueprint('event', __name__)

@event_bp.route("/", methods=["POST"])
def add_event():
    from flask import request

    data = request.get_json()

    id_gestionnaire = data["id_gestionnaire"]

    user = get_user_by_id(id_gestionnaire)

    event_name = data["event_name"]
    id_sport = data["id_sport"]
    event_ville = data["event_ville"]
    event_date = data["event_date"]
    event_max_utilisateur = data["event_max_utilisateur"]
    event_Items = data["event_Items"]
    is_private = data["is_private"]
    is_team_vs_team = data["is_team_vs_team"]
    event_age_min = data["event_age_min"]
    event_age_max = data["event_age_max"]
    nombre_utilisateur_min = data["nombre_utilisateur_min"]
    event_description = data["event_description"]

    if not user:
        return jsonify({"error": "User does not exist"}), 400

    # Création de l'objet Event
    event = Event(
        id_gestionnaire=id_gestionnaire,
        event_name=event_name,
        event_description=event_description,
        id_sport=id_sport,
        event_ville=event_ville,
        event_date=event_date,
        event_max_utilisateur=event_max_utilisateur,
        event_Items=event_Items,
        is_private=is_private,
        is_team_vs_team=is_team_vs_team,
        event_age_min=event_age_min,
        event_age_max=event_age_max,
        nombre_utilisateur_min=nombre_utilisateur_min,
    )

    db.session.add(event)
    db.session.commit()
    db.session.flush()

    return (
        jsonify({"message": "Événement ajouté avec succès", "event_id": event.id}),
        201,
    )


@event_bp.route("/booking", methods=["GET"])
def get_events():
    events = Event.query.all()
    events_to_return = [row2dict(event) for event in events]
    for event in events_to_return:
        event["username"] = get_user_by_id(int(event['id_gestionnaire'])).get_json()['username']
    return jsonify(events_to_return)


@event_bp.route("/<int:event_id>", methods=["GET"])
def get_event_by_id(event_id):
    event = Event.query.get(event_id)

    if not event:
        return jsonify({"error": "Événement non trouvé"}), 404

    return (
        jsonify(
            {
                "id": event.id,
                "id_gestionnaire": event.id_gestionnaire,
                "id_sport": event.id_sport,
                "event_description": event.event_description,
                "event_ville": event.event_ville,
                "event_date": event.event_date,
                "event_max_utilisateur": event.event_max_utilisateur,
                "event_Items": event.event_Items,
                "is_private": event.is_private,
                "is_team_vs_team": event.is_team_vs_team,
                "event_age_min": event.event_age_min,
                "event_age_max": event.event_age_max,
                "nombre_utilisateur_min": event.nombre_utilisateur_min,
            }
        ),
        200,
    )


@event_bp.route("/<int:event_id>", methods=["DELETE"])
def delete_event_by_id(event_id):
    event = Event.query.get(event_id)

    if not event:
        return jsonify({"error": "Événement non trouvé"}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": f"Événement {event_id} supprimé avec succès"}), 200


@event_bp.route("/",methods=['GET'])
def get_events():
    events = Event.query.all()
    return jsonify([row2dict(event) for event in events])

@event_bp.route("/<int:event_id>", methods=['GET'])
def get_event_by_id(event_id):
    event = Event.query.get(event_id)

    if not event:
        return jsonify({"error": "Événement non trouvé"}), 404

    return jsonify({
        "id": event.id,
        "id_gestionnaire": event.id_gestionnaire,
        "id_sport": event.id_sport,
        "event_ville": event.event_ville,
        "event_date": event.event_date,
        "event_max_utilisateur": event.event_max_utilisateur,
        "event_Items": event.event_Items,
        "is_private": event.is_private,
        "is_team_vs_team": event.is_team_vs_team,
        "event_age_min": event.event_age_min,
        "event_age_max": event.event_age_max,
        "nombre_utilisateur_min": event.nombre_utilisateur_min
    }), 200



@event_bp.route("/<int:event_id>", methods=['DELETE'])
def delete_event_by_id(event_id):
    event = Event.query.get(event_id)

    if not event:
        return jsonify({"error": "Événement non trouvé"}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": f"Événement {event_id} supprimé avec succès"}), 200


def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d