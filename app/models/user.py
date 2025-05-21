from datetime import date

from sqlalchemy import ARRAY

from config import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    familyname = db.Column(db.String(100), nullable=False)

    # Adresse complète
    address = db.Column(db.String(255), nullable=True)
    postal_code = db.Column(db.String(10), nullable=True)
    city = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    phone = db.Column(db.String(15), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)

    profile_image = db.Column(db.String, nullable=True)

    events = db.relationship("Event", secondary="event_users", back_populates="users")
    consent = db.Column(db.Boolean, nullable=True, default=False)
    bibliography = db.Column(db.String, nullable=True)
    interests  = db.Column(ARRAY(db.String), nullable=True)


    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"