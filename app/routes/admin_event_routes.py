
from flask import Blueprint, jsonify
from app.models.event import Event
from config import db


admin_event_bp = Blueprint("admin_event_bp", __name__)

@admin_event_bp.route('/api/events', methods=["GET"])
def get_all_events_admin():
    events = Event.query.all()
    event_list = []
    for event in events:
        event_list.append({
            "id": event.id,
            "event_name": event.event_name,
            "event_description": event.event_description,
            "event_ville": event.event_ville,
            "event_date": event.event_date.strftime("%Y-%m-%d %H:%M:%S"),
            "event_max_utilisateur": event.event_max_utilisateur,
            "is_private": event.is_private,
            "members": [
                {
                    "id": user.id,
                    "firstname": user.firstname,
                    "familyname": user.familyname
                } for user in event.users
            ]
        })
    return jsonify(event_list)


@admin_event_bp.route("/event/<int:event_id>", methods=["DELETE"])
def delete_user(event_id):

    event = Event.query.get(event_id)
    if not event:
        return jsonify({"message": "Event introuvable"}), 404


    db.session.delete(event)
    db.session.commit()

    return jsonify({"message": "Event supprimé"}), 200