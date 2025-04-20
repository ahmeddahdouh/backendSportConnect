from datetime import datetime

from app.models import Event, User
from config import db


class EventRepository:

    def add_event(self, event_data):
        event = Event(**event_data)
        db.session.add(event)
        db.session.commit()
        db.session.flush()
        return event

    def get_events_by_user_id(self, user_id):
        return Event.query.filter_by(id_gestionnaire=user_id).all()

    def get_events_filtred(self, filter):
        return db.session.query(Event, User.username.label("username")).join(
            User, User.id == Event.id_gestionnaire
        ).filter(filter).all()

    def get_event_by_id(self, event_id):
        return Event.query.get(event_id)

    def update_event(self, event, data):

        excluded_fields = {"id", "created_at"}

        [setattr(event, key, value) for key, value in data.items() if
         hasattr(event, key) and key not in excluded_fields]

        if "event_date" in data:
            try:
                event.event_date = datetime.strptime(data["event_date"], "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return {"message": "Invalid date format. Use YYYY-MM-DD HH:MM:SS."}, 400
        db.session.commit()
