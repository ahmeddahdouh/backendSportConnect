from config import db


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    profile_picture = db.Column(db.String(), nullable=True)
    manager_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    manager = db.relationship("User", backref=db.backref("managed_teams", lazy=True))
