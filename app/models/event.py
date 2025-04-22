from sqlalchemy.dialects.postgresql import JSONB
from config import db


class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String, nullable=False)
    event_description = db.Column(db.String(200), nullable=False)

    id_gestionnaire = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    id_sport = db.Column(db.Integer,db.ForeignKey("sports.id")),

    id_gestionnaire = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    id_sport = db.Column(db.Integer,db.ForeignKey("sports.id"),)

    event_ville = db.Column(db.String(200), nullable=False)
    event_date = db.Column(db.DateTime, nullable=False)
    event_max_utilisateur = db.Column(db.Integer, nullable=False)
    event_Items = db.Column(JSONB)
    is_private = db.Column(db.Boolean, nullable=False, default=False)
    is_team_vs_team = db.Column(db.Boolean, nullable=False, default=False)
    event_age_min = db.Column(db.Integer, nullable=False)
    event_age_max = db.Column(db.Integer, nullable=False)
    nombre_utilisateur_min = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    users = db.relationship("User", secondary="event_users", back_populates="events")

    def to_dict(self, members):
        return {
            "id": self.id,
            "id_gestionnaire": self.id_gestionnaire,
            "id_sport": self.id_sport,
            "event_description": self.event_description,
            "event_ville": self.event_ville,
            "event_date": (
                self.event_date.strftime("%Y-%m-%d %H:%M:%S")
                if self.event_date
                else None
            ),
            # Convertir la date
            "event_max_utilisateur": self.event_max_utilisateur,
            "event_Items": self.event_Items,
            "is_private": self.is_private,
            "is_team_vs_team": self.is_team_vs_team,
            "event_age_min": self.event_age_min,
            "event_age_max": self.event_age_max,
            "nombre_utilisateur_min": self.nombre_utilisateur_min,
            "members": [member.to_dict() for member in members],
            # Liste des participants
        }
