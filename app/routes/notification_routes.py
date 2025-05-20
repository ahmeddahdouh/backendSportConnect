from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from app.services.notification_service import NotificationService

notification_bp = Blueprint("notification", __name__)
notification_service = NotificationService()

@notification_bp.route("/", methods=["GET"])
@jwt_required()
def get_notifications():
    """Get all notifications for the current user"""
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = int(current_user_json["id"])
    
    unread_only = request.args.get("unread_only", "false").lower() == "true"
    
    try:
        notifications = notification_service.get_user_notifications(user_id, unread_only)
        return jsonify(notifications), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        print(f"Exception in route: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@notification_bp.route("/<int:notification_id>/read", methods=["PUT"])
@jwt_required()
def mark_as_read(notification_id):
    """Mark a notification as read"""
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json["id"]
    
    try:
        notification = notification_service.mark_notification_as_read(notification_id, user_id)
        return jsonify(notification.to_dict()), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        print(f"Exception in route: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@notification_bp.route("/read-all", methods=["PUT"])
@jwt_required()
def mark_all_as_read():
    """Mark all notifications as read for the current user"""
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json["id"]
    
    try:
        result = notification_service.mark_all_as_read(user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        print(f"Exception in route: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@notification_bp.route("/<int:notification_id>", methods=["DELETE"])
@jwt_required()
def delete_notification(notification_id):
    """Delete a notification"""
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json["id"]
    
    try:
        result = notification_service.delete_notification(notification_id, user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        print(f"Exception in route: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@notification_bp.route("/", methods=["DELETE"])
@jwt_required()
def delete_all_notifications():
    """Delete all notifications for the current user"""
    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)
    user_id = current_user_json["id"]
    
    try:
        result = notification_service.delete_all_notifications(user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        print(f"Exception in route: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500 