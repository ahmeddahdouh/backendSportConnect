from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

from app.services.channel_service import ChannelService

channel_bp = Blueprint("channel", __name__)
channel_service = ChannelService()

@channel_bp.route("/message", methods=["POST"])
@jwt_required()
def send_message():
    current_user = json.loads(get_jwt_identity())
    data = request.get_json()
    print("\n",data)
    
    content = data['message']
    
    event_id = data['event_id']

    if not content or not event_id:
        return jsonify({"error": "Champs requis manquants"}), 400

    try:
        result = channel_service.send_message(user_id=current_user["id"], event_id=event_id, content=content)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@channel_bp.route("/message/<int:event_id>", methods=["GET"])
@jwt_required()
def get_messages(event_id):
    try:
        messages = channel_service.get_messages(event_id)
        return jsonify(messages), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
