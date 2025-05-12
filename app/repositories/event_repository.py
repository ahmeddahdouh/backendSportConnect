from datetime import datetime
from app.associations.event_users import EventUsers
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
        return (
            db.session.query(Event, User.username.label("username"))
            .join(User, User.id == Event.id_gestionnaire)
            .filter(filter)
            .all()
        )

    def get_events_sorted_by_date(self):
        return (
            db.session.query(Event)
            .order_by(Event.event_date.desc())
            .limit(4)
            .all()
        )

    def get_event_by_id(self, event_id):
        return Event.query.get(event_id)

    def update_event(self, event, data):

        excluded_fields = {"id", "created_at"}

        [
            setattr(event, key, value)
            for key, value in data.items()
            if hasattr(event, key) and key not in excluded_fields
        ]

        if "event_date" in data:
            try:
                event["event_date"] = datetime.strptime(
                    data["event_date"], "%Y-%m-%d %H:%M:%S"
                )
            except ValueError:
                return {"message": "Invalid date format. Use YYYY-MM-DD HH:MM:SS."}, 400
        db.session.commit()

    def is_user_alredy_participating(self, event_id, user_id):
        return (EventUsers.query.filter_by(event_id=event_id, user_id=user_id).first())

    def add_user_to_event(self, user_id, event_id):
        new_participation = EventUsers(user_id=user_id, event_id=event_id)
        db.session.add(new_participation)
        db.session.commit()

    def delete_participation(self, participation_db):
        db.session.delete(participation_db)
        db.session.commit()

    def delete_event(self, event_id):
        event = self.get_event_by_id(event_id)
        db.session.delete(event)
        db.session.commit()

    def get_all_events(self):
        return Event.query.all()