from app.services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import Event, User
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
    """
    Crée un nouvel événement avec les données fournies.
    Vérifie que le gestionnaire existe avant de créer l'événement.
    """
    data = json.loads(request.form["data"])
    id_gestionnaire = data["id_gestionnaire"]
    user = user_service.get_user_by_id(id_gestionnaire)
    if "file" not in request.files:
        return jsonify({"message": "Fichier manquant"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "Nom de fichier vide"}), 400

    if not user:
        raise ValueError("L'utilisateur n'existe pas")
    else:
        try:
            event = event_service.create_event(data,file)
            return jsonify({
                "message": "Événement ajouté avec succès",
                "event_id": event.id
            }), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": f"Erreur interne du serveur : {str(e)}"}), 500

@event_bp.route("/booking", methods=["GET"])
@jwt_required()
def get_events():
    """
    Récupère tous les événements sauf ceux créés par l'utilisateur actuellement connecté.
    """
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    return event_service.get_events_filtred(
        Event.id_gestionnaire != int(current_user_json["id"])
    )


@event_bp.route("/sortedEvents", methods=["GET"])
def get_events_sorted_by_date():
    """
    Récupère tous les événements sauf ceux créés par l'utilisateur actuellement connecté.
    """
    return event_service.get_events_sorted_by_date()




@event_bp.route("/curentEvents", methods=["GET"])
@jwt_required()
def get_curent_user_events():
    """
    Récupère les événements créés par l'utilisateur actuellement connecté.
    """
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    return event_service.get_events_filtred(
        Event.id_gestionnaire == int(current_user_json["id"])
    )

@event_bp.route("/participate", methods=["POST"])
def participate_event():
    """
    Permet à un utilisateur de participer à un événement donné.
    """
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
    """
    Permet à l'utilisateur connecté de se désinscrire d'un événement.
    """
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
    """
    Récupère les détails d'un événement par son identifiant.
    """
    try:
        result = event_service.get_event_by_id(event_id)
        return jsonify(result), 200
    except LookupError as le:
        return jsonify({"error": str(le)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@event_bp.route("/<int:event_id>", methods=["DELETE"])
def delete_event_by_id(event_id):
    """
    Supprime un événement par son identifiant.
    """
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
    """
    Récupère les informations du gestionnaire de l’événement spécifié.
    """
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
    """
    Met à jour un événement si l'utilisateur connecté est le gestionnaire.
    """
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json.get("id")

    event = event_service.get_event_by_id(event_id)
    if not event:
        return {"message": "Événement introuvable."}, 404

    if int(event["id_gestionnaire"]) != user_id:
        return {"message": "Non autorisé. Seul le gestionnaire peut modifier cet événement."}, 403

    data = request.get_json()

    try:
        event_service.update_event(event, data)
        return {
            "message": "Événement mis à jour avec succès.",
            "event": event
        }, 200
    except ValueError as e:
        return {"error": str(e)}, 400
    except Exception as e:
        return {"error": str(e)}, 500
