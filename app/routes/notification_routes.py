from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.notification_route_service import NotificationRouteService

notification_bp = Blueprint("notification", __name__)
notification_route_service = NotificationRouteService()

@notification_bp.route("/", methods=["GET"])
@jwt_required()
def get_notifications():
    """Get all notifications for the current user"""
    try:
        current_user = get_jwt_identity()
        notifications = notification_route_service.get_notifications(current_user)
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
    try:
        current_user = get_jwt_identity()
        notification = notification_route_service.mark_as_read(notification_id, current_user)
        return jsonify(notification), 200
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
    try:
        current_user = get_jwt_identity()
        result = notification_route_service.mark_all_as_read(current_user)
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
    try:
        current_user = get_jwt_identity()
        result = notification_route_service.delete_notification(notification_id, current_user)
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
    try:
        current_user = get_jwt_identity()
        result = notification_route_service.delete_all_notifications(current_user)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        import traceback
        print(f"Exception in route: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500 