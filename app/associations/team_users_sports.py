from sqlalchemy.dialects.postgresql import JSONB
from config import db

class TeamUsers(db.Model):
    __tablename__ = 'team_users'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), primary_key=True)

class TeamSports(db.Model):
    __tablename__ = 'team_sports'
    sport_id = db.Column(db.Integer, db.ForeignKey('sports.id'), primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), primary_key=True)
    sport_stat = db.Column(JSONB)

