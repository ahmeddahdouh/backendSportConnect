from app.services.user_service import UserService
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from ..models import Event
from ..models import User
from flask import Blueprint, request, jsonify
from config import db
from .user_routes import user_service
import json
from ..services.event_service import EventService

event_service = EventService()
user_service = UserService()

event_bp = Blueprint("event", __name__)


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
                jsonify(
                    {"message": "Événement ajouté avec succès", "event_id": event.id}
                ),
                201,
            )
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Erreur interne du serveur : ${str(e)}"}), 500


@event_bp.route("/booking", methods=["GET"])
@jwt_required()
def get_events():
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    return event_service.get_events_filtred(
        Event.id_gestionnaire != int(current_user_json["id"])
    )


@event_bp.route("/curentEvents", methods=["GET"])
@jwt_required()
def get_curent_user_events():
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    return event_service.get_events_filtred(
        Event.id_gestionnaire == int(current_user_json["id"])
    )


@event_bp.route("/participate", methods=["POST"])
def participate_event():
    data = request.get_json()
    user_id = data.get("user_id")
    event_id = int(data.get("event_id"))

    if not user_id or not event_id:
        return jsonify({"error": "user_id et event_id sont requis"}), 400

    try:
        result = event_service.participate_user_to_event(user_id, event_id)
        return jsonify(result), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except LookupError as le:
        return jsonify({"error": str(le)}), 404
    except FileExistsError as fe:
        return jsonify({"error": str(fe)}), 409


@event_bp.route("/unparticipate/<int:event_id>", methods=["DELETE"])
@jwt_required()
def unparticipate_event(event_id: int):
    current_user = get_jwt_identity()
    user_id = json.loads(current_user)["id"]

    try:
        result = event_service.unparticipate_user_to_event(user_id, event_id)
        return jsonify(result), 200
    except LookupError as le:
        return jsonify({"error": str(le)}), 404
    except FileExistsError as fe:
        return jsonify({"error": str(fe)}), 409


@event_bp.route("/<int:event_id>", methods=["GET"])
def get_event_by_id(event_id):

    try:
        result = event_service.get_event_by_id(event_id)
        return jsonify(result), 200
    except LookupError as le:
        return jsonify({"error": str(le)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@event_bp.route("/<int:event_id>", methods=["DELETE"])
def delete_event_by_id(event_id):
    event = event_service.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Événement non trouvé"}), 404
    else:
        try:
            result = event_service.delete_event(event_id)
            return jsonify(result), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@event_bp.route("/<int:event_id>/infomanager", methods=["GET"])
def get_event_info_manager(event_id):
    event = event_service.get_event_by_id(event_id)
    if not event:
        return jsonify({"error": "Événement non trouvé"}), 404
    manager = user_service.get_user_by_id(event["id_gestionnaire"])

    try:
        result = event_service.get_info_manager(manager)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@event_bp.route("/<int:event_id>", methods=["PUT"])
@jwt_required()
def update_event(event_id):
    # recupérer le id du current user via le token envoyé
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json.get("id")

    event = event_service.get_event_by_id(event_id)
    if not event:
        return {"message": "Event not found."}, 404

    print(event["id_gestionnaire"])

    if int(event["id_gestionnaire"]) != user_id:
        return {
            "message": "Unauthorized. Only the event manager can update this event."
        }, 403

    data = request.get_json()

    try:
        event_service.update_event(event, data)
        return {"message": "Event updated successfully.", "event": event}, 200
    except ValueError as e:
        return {"error": str(e)}, 400
    except Exception as e:
        return {"error": str(e)}, 500
