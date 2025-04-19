import datetime
from app.services.user_service import UserService
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from ..models import Event
from ..models import User
from app.associations.event_users import  EventUsers
from flask import Blueprint, request, jsonify
from config import db
from .user_routes import user_service
import json
from ..services.event_service import EventService

event_service = EventService()
user_service = UserService()

event_bp = Blueprint('event', __name__)

@event_bp.route("/", methods=["POST"])
def add_event():
    data = request.get_json()
    id_gestionnaire = data["id_gestionnaire"]
    user = user_service.get_user_by_id(id_gestionnaire)

    if not user:
        raise ValueError("User does not exist")
    else:
        try:
            event = event_service.create_event(data)
            return (
                jsonify({"message": "Événement ajouté avec succès", "event_id": event.id}),
                201,
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Erreur interne du serveur."}), 500

@event_bp.route("/booking", methods=["GET"])
@jwt_required()
def get_events():
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    return event_service.get_events_filtred(Event.id_gestionnaire != int(current_user_json['id']))

@event_bp.route("/curentEvents", methods=["GET"])
@jwt_required()
def get_curent_user_events():
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    return event_service.get_events_filtred(Event.id_gestionnaire == int(current_user_json['id']))


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

    event_user_db = EventUsers.query.get((user_id,event_id))
    if event_user_db:
        return jsonify({"message": "L'utilisateur est déjà inscrit à cet événement"}), 409

    event_users = EventUsers(**data)
    db.session.add(event_users)
    db.session.flush()
    db.session.commit()
    db.session.flush()

    return jsonify({"message": "Utilisateur ajouté à l'événement avec succès"}), 201


@event_bp.route("/unparticipate/<int:event_id>", methods=["DELETE"])
@jwt_required()
def unparticipate_event(event_id:int):
    current_user = get_jwt_identity()
    user_id = json.loads(current_user)['id']

    participation_db  = EventUsers.query.get((user_id,event_id))
    if not participation_db:
        return jsonify({"message":"enrgistrement non trouvé "}),404
    else :
        db.session.delete(participation_db)
        db.session.commit()

    return  jsonify({"message":"Participation supprimer avec succées "}),200




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

@event_bp.route("/<int:event_id>/infomanager", methods=["GET"])
def get_event_info_manager(event_id):
    event = Event.query.get(event_id)
    if not event:
        return jsonify({"error": "Événement non trouvé"}), 404
    manager = User.query.get(event.id_gestionnaire)
    infomanager = {"firstname": manager.firstname, "familyname": manager.familyname, "profileimage": manager.profileImage, "age": manager.age} #age à remplacer par + tard score moyen des events
    return jsonify(infomanager),200

@event_bp.route("/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json.get("id")

    event = Event.query.get(event_id)
    if not event:
        return {"message": "Event not found."}, 404

    # Check if the user is the event manager
    if event.id_gestionnaire != user_id:
        return {"message": "Unauthorized. Only the event manager can update this event."}, 403

    data = request.get_json()

    # Update all possible fields, including the sport and manager (although manager should not change)
    event.event_name = data.get("event_name", event.event_name)
    event.event_description = data.get("event_description", event.event_description)
    event.event_ville = data.get("event_ville", event.event_ville)

    # Update the event manager's ID (this is typically not changed, but left for flexibility)
    event.id_gestionnaire = data.get("id_gestionnaire", event.id_gestionnaire)

    # Update the sport played by the event
    event.id_sport = data.get("id_sport", event.id_sport)

    # Update maximum number of users and items related to the event
    event.event_max_utilisateur = data.get("event_max_utilisateur", event.event_max_utilisateur)
    event.event_Items = data.get("event_Items", event.event_Items)

    event.is_private = data.get("is_private", event.is_private)
    event.is_team_vs_team = data.get("is_team_vs_team", event.is_team_vs_team)
    event.event_age_min = data.get("event_age_min", event.event_age_min)
    event.event_age_max = data.get("event_age_max", event.event_age_max)
    event.nombre_utilisateur_min = data.get("nombre_utilisateur_min", event.nombre_utilisateur_min)


    # Validate and update event date
    if "event_date" in data:
        try:
            event.event_date = datetime.strptime(data["event_date"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD HH:MM:SS."}, 400

    # Commit the changes to the database
    db.session.commit()

    return {"message": "Event updated successfully.", "event": event.to_dict([])}, 200


