from app.models import Event, User
from config import db

class EventRepository:

    def add_event(self,event_data):
        event = Event(**event_data)
        db.session.add(event)
        db.session.commit()
        db.session.flush()
        return event

    def get_events_by_user_id(self,user_id):
        return Event.query.filter_by(id_gestionnaire=user_id).all()

    def get_events_filtred(self, filter):
        return db.session.query(Event,User.username.label("username")).join(
                User, User.id == Event.id_gestionnaire
                ).filter(filter).all()