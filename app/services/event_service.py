from dataclasses import asdict
from datetime import datetime

from flask import jsonify

from app.controllers import row2dict
from app.models import Event
from app.repositories.event_repository import EventRepository


class EventService:

    def __init__(self):
        self.event_repository = EventRepository()

    def create_event(self, event_data):
        event = self.event_repository.add_event(event_data)
        return event

    def get_events_by_user_id(user_id):
        events = EventRepository.get_events_by_user_id(user_id)
        events_list = [row2dict(event) for event in events]
        return events_list

    def get_events_filtred(self, filter):
        events = self.event_repository.get_events_filtred(filter)
        events_to_return = [
            {**row2dict(event.Event), "username": event.username}
            for event in events
        ]

        for event in events_to_return:
            event_obj = Event.query.get(event["id"])
            event["members"] = [
                {"id": user.id, "firstname": user.firstname, "familyname": user.familyname}
                for user in event_obj.users
            ]

        return jsonify(events_to_return)

    def get_event_by_id(self, event_id):
        return self.event_repository.get_event_by_id(event_id)

    def update_event(self, event, data):
       return  self.event_repository.update_event(event, data)
