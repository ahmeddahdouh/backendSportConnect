from flask import Blueprint, jsonify
from app.services.admin_user_service import AdminUserService

admin_user_bp = Blueprint("admin_user", __name__)
admin_user_service = AdminUserService()

@admin_user_bp.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(admin_user_service.list_users())

@admin_user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    response, status = admin_user_service.delete_user_by_id(user_id)
    return jsonify(response), status
