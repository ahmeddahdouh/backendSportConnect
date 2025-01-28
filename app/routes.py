import bcrypt
from flask import Blueprint , request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_swagger_ui import get_swaggerui_blueprint

from app.models import User,db
auth_bp = Blueprint('auth', __name__)
jwt = JWTManager()

@auth_bp.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirmPassword")
    print(confirm_password)

    if not username or not email or not password:
        return jsonify({"message":'Missing data'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username = username,email=email,password = hashed_password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": 'User registered successfully'}), 201

@auth_bp.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"message":'Missing data'}), 400
    user = User.query.filter_by(username=username).first()
    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token),200
    else:
        return jsonify({"message":'Invalid credentials'}), 401

@auth_bp.route('/users',methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([row2dict(user) for user in users])

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d