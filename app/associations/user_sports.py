from sqlalchemy.dialects.postgresql import JSONB
from config import db

from sqlalchemy.dialects.postgresql import JSONB
from config import db

class UserSports(db.Model):
    __tablename__ = 'user_sports'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    sport_id = db.Column(db.Integer, db.ForeignKey('sports.id'), primary_key=True)
    sport_stat = db.Column(JSONB)




