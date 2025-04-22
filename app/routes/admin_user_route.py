#ici admin administre les users

from flask import Blueprint, jsonify
from app.models.user import User
from app.models.event import Event
from config import db


admin_user_bp = Blueprint("admin_user", __name__)

@admin_user_bp.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    users_data = [{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "firstname": user.firstname,
        "familyname": user.familyname,
        "city": user.city,
        "phone": user.phone,
        "age": user.age,
        "profileImage": user.profileImage
    } for user in users]
    return jsonify(users_data)


# supression de l'utilisateur

@admin_user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Utilisateur introuvable"}), 404

    # Mettre à jour tous les événements liés
    events = Event.query.filter_by(id_gestionnaire=user.id).all()
    for event in events:
         db.session.delete(event)

    # Ensuite, suppression de l'utilisateur
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Utilisateur supprimé"}), 200