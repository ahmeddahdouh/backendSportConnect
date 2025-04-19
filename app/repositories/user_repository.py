from app.models import User
from app.models import Event
from config import db

class UserRepository:

    def get_user_by_id(self,user_id):
        return User.query.get(user_id)


    def get_events_by_user_id(self,user_id):
        results = db.session.query(Event).join(
            User, User.id == Event.id_gestionnaire
        ).filter(
            User.id == 1
        ).all()