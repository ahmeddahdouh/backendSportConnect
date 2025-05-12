from flask import Blueprint, jsonify
from app.services.admin_event_service import list_events_admin, remove_event_by_id

admin_event_bp = Blueprint("admin_event_bp", __name__)

@admin_event_bp.route('/api/events', methods=["GET"])
def get_all_events_admin():
    return jsonify(list_events_admin())

@admin_event_bp.route("/event/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = remove_event_by_id(event_id)
    if not event:
        return jsonify({"message": "Event introuvable"}), 404
    return jsonify({"message": "Event supprimé"}), 200
