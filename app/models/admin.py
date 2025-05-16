# models/admin.py

from config import db

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    firstname = db.Column(db.String(200), nullable=False)
    familyname = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
