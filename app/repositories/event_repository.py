from datetime import datetime

from sqlalchemy.exc import IntegrityError

from app.associations.event_users import EventUsers
from app.models import Event, User
from config import db
from sqlalchemy import func


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



    def get_events_sorted_by_distance_and_date(self, latitude, longitude,return_all_events,user_id):

        distance_expr = (
                6371 * func.acos(
            func.cos(func.radians(latitude)) *
            func.cos(func.radians(Event.latitude)) *
            func.cos(func.radians(Event.longitude) - func.radians(longitude)) +
            func.sin(func.radians(latitude)) *
            func.sin(func.radians(Event.latitude))
        )
        ).label("distance")

        if(return_all_events and user_id):
            return (
            db.session.query(Event, distance_expr).
            filter_by(id_gestionnaire=user_id)
            .order_by(distance_expr, Event.event_date.desc())
            .limit(4)
            .all() )
        if(return_all_events):
            return (
                db.session.query(Event, distance_expr).
                filter_by(id_gestionnaire=user_id)
                .limit(4)
                .all())
        else :
            return (
                db.session.query(Event, distance_expr)
                .order_by(distance_expr, Event.event_date.desc())
                .all())


    def get_events_sorted_by_date(self):
        return (
            db.session.query(Event)
            .order_by(Event.event_date.desc())
            .limit(4)
            .all()
        )

    def get_event_by_id(self, event_id):
        return Event.query.get(event_id)

    def update_event(self):
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise IntegrityError(str(e.orig) if e.orig else str(e))
        except Exception as e:
            db.session.rollback()
            raise e





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
