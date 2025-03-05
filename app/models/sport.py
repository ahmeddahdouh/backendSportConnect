from sqlalchemy.dialects.postgresql import JSONB
from config import db

class Sport(db.Model):
    __tablename__ = 'sports'
    id = db.Column(db.Integer,primary_key=True)
    sport_nom = db.Column(db.String(50),nullable=False)
    stat_solo = db.Column(JSONB)
    stat_equipe = db.Column(JSONB)
    nbr_equipe = db.Column(db.Integer)
    nbr_joueur_max = db.Column(db.Integer)





