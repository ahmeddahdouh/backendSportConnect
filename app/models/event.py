from sqlalchemy.dialects.postgresql import JSONB
from config import db
from app.associations.event_users import Event_users

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String, nullable=False)
    event_description = db.Column(db.String(200), nullable=False)
    id_gestionnaire = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    id_sport = db.Column(db.Integer,db.ForeignKey("sports.id"),)
    event_ville = db.Column(db.String(50), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    event_max_utilisateur = db.Column(db.Integer, nullable=False)
    event_Items = db.Column(JSONB)
    is_private = db.Column(db.Boolean, nullable=False, default=False)
    is_team_vs_team = db.Column(db.Boolean, nullable=False, default=False)
    event_age_min = db.Column(db.Integer, nullable=False)
    event_age_max = db.Column(db.Integer, nullable=False)
    nombre_utilisateur_min = db.Column(db.Integer, nullable=False)
    users = db.relationship('User', secondary="event_users", back_populates='events')