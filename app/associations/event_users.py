from config import db

class EventUsers(db.Model):
    __tablename__ = 'event_users'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), primary_key=True)



