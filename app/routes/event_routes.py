from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from app.models.event import Event
from app.models.user import User
from app.associations.event_users import  EventUsers
from flask import Blueprint, request, jsonify
from config import db
from .user_routes import get_user_by_id, login
from . import row2dict
import json

event_bp = Blueprint('event', __name__)

@event_bp.route("/", methods=["POST"])
def add_event():
    from flask import request
    data = request.get_json()
    id_gestionnaire = data["id_gestionnaire"]
    user = get_user_by_id(id_gestionnaire)
    if not user:
        return jsonify({"error": "User does not exist"}), 400
    event = Event(**data)
    db.session.add(event)
    db.session.flush()
    db.session.commit()
    db.session.flush()
    return (
        jsonify({"message": "Événement ajouté avec succès", "event_id": event.id}),
        201,
    )




@event_bp.route("/booking", methods=["GET"])
@jwt_required()
def get_events():
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    return get_events_filtred(Event.id_gestionnaire != int(current_user_json['id']))

@event_bp.route("/curentEvents", methods=["GET"])
@jwt_required()
def get_curent_user_events():
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    return get_events_filtred(Event.id_gestionnaire == int(current_user_json['id']))


def get_events_filtred(filter):
    events = Event.query.filter(filter).all()
    events_to_return = [row2dict(event) for event in events]

    for event in events_to_return:
        # Ajout du username du gestionnaire
        event["username"] = get_user_by_id(int(event["id_gestionnaire"])).get_json()["username"]

        # Récupération des utilisateurs participants à l'événement
        event_obj = Event.query.get(event["id"])  # Récupération de l'objet Event
        event["members"] = [
            {"id": user.id, "firstname": user.firstname, "familyname": user.familyname}
            for user in event_obj.users
        ]

    return jsonify(events_to_return)

@event_bp.route("/participate", methods=["POST"])
def participate_event():
    from flask import request

    data = request.get_json()
    user_id = data.get("user_id")
    event_id = data.get("event_id")

    if not user_id or not event_id:
        return jsonify({"error": "user_id et event_id sont requis"}), 400
    user = User.query.get(user_id)
    event = Event.query.get(event_id)

    if not user or not event:
        return jsonify({"error": "Utilisateur ou événement non trouvé"}), 404

    event_user_db = EventUsers.query.get(user_id,event_id)
    print(event_user_db)


    if event_user_db:
        return jsonify({"message": "L'utilisateur est déjà inscrit à cet événement"}), 409

    event_users = EventUsers(**data)
    db.session.add(event_users)
    db.session.flush()
    db.session.commit()
    db.session.flush()

    return jsonify({"message": "Utilisateur ajouté à l'événement avec succès"}), 201


@event_bp.route("/<int:event_id>", methods=["GET"])
def get_event_by_id(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Événement non trouvé"}), 404
    # Récupération des utilisateurs participants à l'événement
    members = [
        {"id": user.id, "firstname": user.firstname, "familyname": user.familyname}
        for user in event.users
    ]
    return jsonify(event.to_dict(members)),200



@event_bp.route("/<int:event_id>", methods=["DELETE"])
def delete_event_by_id(event_id):
    event = Event.query.get(event_id)

    if not event:
        return jsonify({"error": "Événement non trouvé"}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": f"Événement {event_id} supprimé avec succès"}), 200





