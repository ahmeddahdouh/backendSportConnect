from app.repositories.event_repository import EventRepository


EventRepositor = EventRepository()
def list_events_admin():
    events = EventRepositor.get_all_events()
    return [{
        "id": event.id,
        "event_name": event.event_name,
        "event_description": event.event_description,
        "event_ville": event.event_ville,
        "event_date": event.event_date.strftime("%Y-%m-%d %H:%M:%S"),
        "event_max_utilisateur": event.event_max_utilisateur,
        "is_private": event.is_private,
        "members": [
            {
                "id": user.id,
                "firstname": user.firstname,
                "familyname": user.familyname
            } for user in event.users
        ]
    } for event in events]

def remove_event_by_id(event_id):
    event = EventRepositor.get_event_by_id(event_id)
    if not event:
        return None
    EventRepositor.delete_event(event)
    return event
