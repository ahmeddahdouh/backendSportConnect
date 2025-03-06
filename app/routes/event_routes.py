from app.models.event import Event
from app.models.user import User
from flask import Blueprint, request, jsonify
from config import db
from app.associations.event_users import Event_users
from .user_routes import get_user_by_id
from . import row2dict

event_bp = Blueprint('event', __name__)

@event_bp.route("/", methods=["POST"])
def add_event():
    from flask import request
    data = request.get_json()

    id_gestionnaire = data["id_gestionnaire"]
    user = get_user_by_id(id_gestionnaire)

    if not user:
        return jsonify({"error": "User does not exist"}), 400

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
    db.session.flush()  # On génère l'ID de l'événement avant d'ajouter les relations

    db.session.commit()
    db.session.flush()

    return (
        jsonify({"message": "Événement ajouté avec succès", "event_id": event.id}),
        201,
    )


@event_bp.route("/participate", methods=["POST"])
def participate_event():
    data = request.get_json()
    user_id = data.get("user_id")
    event_id = data.get("event_id")

    if not user_id or not event_id:
        return jsonify({"error": "user_id et event_id sont requis"}), 400

    user = User.query.get(user_id)
    event = Event.query.get(event_id)

    if not user or not event:
        return jsonify({"error": "Utilisateur ou événement non trouvé"}), 404

    # Vérifier si l'utilisateur est déjà inscrit à cet événement
    existing_entry = Event_users.query.get((user_id,event_id))


    if existing_entry:
        return jsonify({"message": "L'utilisateur est déjà inscrit à cet événement"}), 409
    event_user_db = Event_users(user_id=user_id, event_id=event_id)

    # Insérer l'utilisateur dans l'événement
    db.session.execute(event_users.insert().values(user_id=user_id, event_id=event_id))
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
                "members": members,  # Ajout de la liste des utilisateurs participants
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

@event_bp.route("/booking", methods=["GET"])
def get_events():
    events = Event.query.all()
    for event in events:
        members = [
            {"id": user.id, "firstname": user.firstname, "familyname": user.familyname}
            for user in event["users"]
        ]
        event["username"] = get_user_by_id(int(event['id_gestionnaire'])).get_json()['username']

    return jsonify(events_to_return)






