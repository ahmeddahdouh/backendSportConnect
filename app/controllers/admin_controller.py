from flask import Blueprint, jsonify, request
from app.services.admin_service import AdminService 



admin_admin_bp = Blueprint('admin_admin_bp', __name__)

admin_service = AdminService()

@admin_admin_bp.route('/api/admins', methods=['GET'])
def get_all_admins():
    admins = admin_service.list_admins()
    return jsonify(admins)

@admin_admin_bp.route('/api/admins', methods=['POST'])
def create_admin_route():
    data = request.get_json()
    new_admin, error = admin_service.create_admin(data)
    if error:
        return jsonify({"error": error}), 409
    return jsonify({"message": "Admin créé avec succès"}), 201

@admin_admin_bp.route("/admins/<int:id>", methods=["DELETE"])
def delete_admin(id):
    admin = admin_service.remove_admin(id)
    if not admin:
        return jsonify({"error": "Admin non trouvé"}), 404
    return jsonify({"message": "Admin supprimé avec succès"}), 200


@admin_admin_bp.route("/loginAdmin", methods=["POST"])
def login_admin():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Champs requis"}), 400

    response, status = admin_service.login_admin(email, password)
    return jsonify(response), status