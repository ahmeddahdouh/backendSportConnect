import os
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app.models.event import Event
from app.associations.event_users import event_users
from config import db
from sqlalchemy.exc import IntegrityError
from flask import request,abort, make_response, jsonify, Blueprint, send_from_directory, current_app
import bcrypt
from . import row2dict
from flasgger import swag_from
import json
from datetime import timedelta
import uuid

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
@swag_from('../../static/docs/add_user_docs.yaml')
def register():
    data = request.get_json()
    # Récupération des champs requis
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirmPassword")
    firstname = data.get("firstname")
    familyname = data.get("familyname")
    city = data.get("city")
    phone = data.get("phone")
    age = data.get("age")

    # Vérification des champs obligatoires
    if not all([username, email, password, confirm_password, firstname, familyname, city, phone, age]):
        return jsonify({"message": "Missing data"}), 400

    # Vérification de la correspondance des mots de passe
    if password != confirm_password:
        return jsonify({"message": "Passwords do not match"}), 400

    # Vérification que l'âge est bien un entier positif
    try:
        age = int(age)
        if age <= 0:
            return jsonify({"message": "Invalid age"}), 400
    except ValueError:
        return jsonify({"message": "Age must be an integer"}), 400

    # Hachage du mot de passe
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    # Création de l'utilisateur
    user = User(
        username=username,
        email=email,
        password=hashed_password,
        firstname=firstname,
        familyname=familyname,
        city=city,
        phone=phone,
        age=age
    )

    try:
        # Tentative d'ajout de l'utilisateur à la base de données
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username or email already exists"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@auth_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()

    # Récupérer l'utilisateur
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Mise à jour des champs s'ils sont fournis
    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "firstname" in data:
        user.firstname = data["firstname"]
    if "familyname" in data:
        user.familyname = data["familyname"]
    if "city" in data:
        user.city = data["city"]
    if "phone" in data:
        user.phone = data["phone"]
    if "age" in data:
        try:
            user.age = int(data["age"])
            if user.age <= 0:
                return jsonify({"message": "Invalid age"}), 400
        except ValueError:
            return jsonify({"message": "Age must be an integer"}), 400
    if "password" in data:
        hashed_password = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user.password = hashed_password

    try:
        # Sauvegarde en base de données
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username or email already exists"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message": "Missing data"}), 400
    user = User.query.filter_by(username=username).first()
    if user:
        if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            access_token = create_access_token(identity=
                                               json.dumps({'username': user.username,
                                                           'id': user.id,
                                                           'profileImage': user.profileImage,
                                                           }
                                                          ),
                                               expires_delta=timedelta(hours=1))
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    else:
        return jsonify({"message": "User does not exist"}), 401


@auth_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    users = User.query.all()
    print(users)
    return jsonify([row2dict(user) for user in users])


@auth_bp.route('/uploads/<filename>',methods=["GET"])
def uploaded_file(filename):
    print(current_app.config['UPLOAD_FOLDER'])
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@auth_bp.route("/users/profile",methods=["PUT"])
@jwt_required()
def update_profile_image():
    if "file" not in request.files:
        return jsonify({"message": "Missing file"}), 400

    current_user = get_jwt_identity()
    current_user_json = json.loads(current_user)

    file = request.files["file"]
    if file.filename == "" :
        return jsonify({"message": "Missing file"}), 400
    file_ext = file.filename.split(".")[-1]
    unique_id = uuid.uuid4()
    profileImageName = str(unique_id) + "." + file_ext
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], profileImageName)
    file.save(file_path)
    user = User.query.get(current_user_json["id"])
    user.profileImage = profileImageName
    db.session.commit()

    return jsonify({"image":user.profileImage}), 201


@auth_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id: int):
    user = User.query.get(user_id)

    if not user:
        abort(make_response(jsonify(message="Id organisateur n'existe pas"), 400))

    # Récupérer tous les événements auxquels l'utilisateur participe
    events = Event.query.join(event_users).filter(event_users.c.user_id == user_id).all()

    # Construire la liste des événements
    events_list = [
        {
            "id": event.id,
            "event_name": event.event_name,
            "event_description": event.event_description,
            "event_ville": event.event_ville,
            "event_date": event.event_date,
            "event_max_utilisateur": event.event_max_utilisateur,
            "is_private": event.is_private,
            "is_team_vs_team": event.is_team_vs_team,
            "event_age_min": event.event_age_min,
            "event_age_max": event.event_age_max,
            "nombre_utilisateur_min": event.nombre_utilisateur_min,
        }
        for event in events
    ]

    # Ajouter la liste des événements à la réponse utilisateur
    user_data = row2dict(user)
    user_data["events"] = events_list

    return jsonify(user_data)
