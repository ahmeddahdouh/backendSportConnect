from app.models.events import Event
from flask import Blueprint, request, jsonify
from config import db

event_bp = Blueprint('event', __name__)

@event_bp.route("/",methods=['POST'])
def add_event():
    from flask import request

    data = request.get_json()

    id_gestionnaire = data['id_gestionnaire']
    id_sport = data['id_sport']
    event_ville = data['event_ville']
    event_date = data['event_date']
    event_max_utilisateur = data['event_max_utilisateur']
    event_Items = data['event_Items']
    is_private = data['is_private']
    is_team_vs_team = data['is_team_vs_team']
    event_age_min = data['event_age_min']
    event_age_max = data['event_age_max']
    nombre_utilisateur_min = data['nombre_utilisateur_min']

    # Création de l'objet Event
    event = Event(
        id_gestionnaire=id_gestionnaire,
        id_sport=id_sport,
        event_ville=event_ville,
        event_date=event_date,
        event_max_utilisateur=event_max_utilisateur,
        event_Items=event_Items,
        is_private=is_private,
        is_team_vs_team=is_team_vs_team,
        event_age_min=event_age_min,
        event_age_max=event_age_max,
        nombre_utilisateur_min=nombre_utilisateur_min
    )

    db.session.add(event)
    db.session.commit()
    db.session.flush()

    return jsonify({"message": "Événement ajouté avec succès", "event_id": event.id}), 201



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




def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d