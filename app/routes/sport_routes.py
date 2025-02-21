from flask import Blueprint
from config import db
from app.models.sport import Sport
from flask import Blueprint, request, jsonify
from . import row2dict

sport_bp = Blueprint('sport_bp', __name__)

@sport_bp.route('/',methods=['GET'])
def getAllSport():
   sports = Sport.query.all()
   return jsonify([row2dict(sport) for sport in sports])
