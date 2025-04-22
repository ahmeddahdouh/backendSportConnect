from flask import Blueprint, jsonify, request
from app.models.admin import Admin
from config import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import bcrypt


admin_admin_bp = Blueprint('admin_admin_bp', __name__)

@admin_admin_bp.route('/api/admins', methods=['GET'])
def get_all_admins():
    admins = Admin.query.all()
    return jsonify([
        {
            "id": a.id,
            "username": a.username,
            "email": a.email,
            "firstname": a.firstname,
            "familyname": a.familyname,
            "city": a.city,
            "phone": a.phone,
            "age": a.age
        }
        for a in admins
    ])


@admin_admin_bp.route('/api/admins', methods=['POST'])
def create_admin():
    data = request.get_json()

    if Admin.query.filter((Admin.username == data['username']) | (Admin.email == data['email'])).first():
        return jsonify({"error": "Admin existe déjà"}), 409

    hashed_password = bcrypt.hashpw(data['password'].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    new_admin = Admin(
        username=data['username'],
        email=data['email'],
        password=hashed_password,
        firstname=data['firstname'],
        familyname=data['familyname'],
        city=data['city'],
        phone=data['phone'],
        age=data['age']
    )
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({"message": "Admin créé avec succès"}), 201

# supression de l'admin
@admin_admin_bp.route("/admins/<int:id>", methods=["DELETE"])
def delete_admin(id):
    admin = Admin.query.get(id)
    if not admin:
        return jsonify({"error": "Admin non trouvé"}), 404

    db.session.delete(admin)
    db.session.commit()
    return jsonify({"message": "Admin supprimé avec succès"}), 200

