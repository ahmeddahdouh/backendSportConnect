# 📄 app/controllers/channel_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from app.services.channel_service import ChannelService

channel_bp = Blueprint("channel", __name__)
channel_service = ChannelService()

@channel_bp.route("/create", methods=["POST"])
@jwt_required()
def create_channel():
    data = request.get_json()
    name = data.get("name")
    event_id = data.get("eventId")
    admin_id = data.get("adminId")

    if not all([name, event_id, admin_id]):
        return jsonify({"error": "Paramètres manquants"}), 400

    channel = channel_service.create_channel(name, event_id, admin_id)
    return jsonify({"message": "Canal créé", "channel_id": channel.id}), 201

@channel_bp.route("/addMember", methods=["POST"])
@jwt_required()
def add_member():
    data = request.get_json()
    event_id = data.get("eventId")
    user_id = data.get("userId")
    if not event_id or not user_id:
        return jsonify({"error": "eventId et userId sont requis"}), 400
    return channel_service.add_member(event_id, user_id)

@channel_bp.route("/removeMember", methods=["POST"])
@jwt_required()
def remove_member():
    data = request.get_json()
    event_id = data.get("eventId")
    user_id = data.get("userId")
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    current_user_id = current_user_json.get("id")
    if not event_id or not user_id:
        return jsonify({"error": "eventId et userId sont requis"}), 400
    return channel_service.remove_member(event_id, user_id, current_user_id)

@channel_bp.route("/message", methods=["POST"])
@jwt_required()
def send_message():
    data = request.get_json()
    event_id = data.get("eventId")
    message = data.get("message")
    current_user = get_jwt_identity()
    user_id = json.loads(current_user).get("id")
    if not event_id or not message:
        return jsonify({"error": "eventId et message requis"}), 400
    return channel_service.send_message(event_id, user_id, message)

@channel_bp.route("/<int:event_id>/messages", methods=["GET"])
@jwt_required()
def get_messages(event_id):
    return jsonify(channel_service.get_messages(event_id))