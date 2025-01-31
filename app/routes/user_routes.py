import bcrypt
from flask import Blueprint , request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from app.models import User,db


auth_bp = Blueprint('auth', __name__)




from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirmPassword")

    # Vérification des champs requis
    if not username or not email or not password or not confirm_password:
        return jsonify({"message": 'Missing data'}), 400

    # Vérification de la correspondance des mots de passe
    if password != confirm_password:
        return jsonify({"message": 'Passwords do not match'}), 400

    # Hachage du mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password = hashed_password.decode('utf8')

    # Création de l'utilisateur
    user = User(username=username, email=email, password=hashed_password)

    try:
        # Tentative d'ajout de l'utilisateur dans la base de données
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": 'User registered successfully'}), 201
    except IntegrityError as e:
        # En cas de violation des contraintes d'intégrité (par exemple, e-mail ou nom d'utilisateur déjà pris)
        db.session.rollback()  # Annule la transaction pour éviter d'avoir un état corrompu
        return jsonify({"message": 'Username or email already exists'}), 409
    except Exception as e:
        # En cas d'autres erreurs
        db.session.rollback()  # Annule la transaction pour éviter d'avoir un état corrompu
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500


@auth_bp.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message":'Missing data'}), 400
    user = User.query.filter_by(username=username).first()
    if user:
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            access_token = create_access_token(identity=user.username)
            return jsonify(access_token=access_token),200
        else:
            return jsonify({"message":'Invalid credentials'}), 401
    else:
        return jsonify({"message":'User does not exist'}), 401

@auth_bp.route('/users',methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([row2dict(user) for user in users])

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d