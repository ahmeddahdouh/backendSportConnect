from sqlalchemy.dialects.postgresql import JSONB
from config import db
from datetime import datetime, UTC

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String, nullable=False)
    event_description = db.Column(db.String(200), nullable=False)

    id_gestionnaire = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    id_sport = db.Column(db.Integer, db.ForeignKey("sports.id"))

    event_ville = db.Column(db.String(200), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    date_limite_inscription = db.Column(db.Date, nullable=True)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)

    event_max_utilisateur = db.Column(db.Integer, nullable=False)
    event_Items = db.Column(JSONB)

    is_private = db.Column(db.Boolean, nullable=False, default=False)
    is_team_vs_team = db.Column(db.Boolean, nullable=False, default=False)

    event_age_min = db.Column(db.Integer, nullable=True)
    event_age_max = db.Column(db.Integer, nullable=True)
    nombre_utilisateur_min = db.Column(db.Integer, nullable=True)

    event_image = db.Column(db.String, nullable=True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)

    is_paid = db.Column(db.Boolean, default=False)
    price = db.Column(db.Float, nullable=True)
    event_commande_participation = db.Column(db.String, nullable=True)
    commodites = db.Column(JSONB, nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC))

    users = db.relationship("User", secondary="event_users", back_populates="events")

    def to_dict(self, members):
        return {
            "id": self.id,
            "id_gestionnaire": self.id_gestionnaire,
            "id_sport": self.id_sport,
            "event_description": self.event_description,
            "event_ville": self.event_ville,
            "event_date": self.event_date.strftime("%Y-%m-%d") if self.event_date else None,
            "date_limite_inscription": self.date_limite_inscription.strftime("%Y-%m-%d") if self.date_limite_inscription else None,
            "event_max_utilisateur": self.event_max_utilisateur,
            "event_Items": self.event_Items,
            "is_private": self.is_private,
            "is_team_vs_team": self.is_team_vs_team,
            "event_age_min": self.event_age_min,
            "event_age_max": self.event_age_max,
            "nombre_utilisateur_min": self.nombre_utilisateur_min,
            "is_paid": self.is_paid,
            "price": self.price,
            "event_commande_participation": self.event_commande_participation,
            "commodites": self.commodites,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "members": [member.to_dict() for member in members],
        }
