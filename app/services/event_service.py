import uuid
import os
from flask import jsonify, current_app
from app.controllers import row2dict
from app.models import Event
import app
from app.repositories.event_repository import EventRepository
from app.repositories.user_repository import UserRepository


class EventService:

    def __init__(self):
        self.user_repository = UserRepository()
        self.event_repository = EventRepository()

    def create_event(self, event_data,file):
        file_ext = file.filename.split(".")[-1]
        unique_id = uuid.uuid4()
        eventImageName = str(unique_id) + "." + file_ext
        file_path = os.path.join(current_app.config["TEAM_PHOTOS_FOLDER"], eventImageName)
        file.save(file_path)
        event_data["event_image"] = eventImageName
        event = self.event_repository.add_event(event_data)
        return event

    def get_events_by_user_id(user_id):
        events = EventRepository.get_events_by_user_id(user_id)
        events_list = [row2dict(event) for event in events]
        return events_list

    def get_events_filtred(self, filter):
        events = self.event_repository.get_events_filtred(filter)
        events_to_return = [
            {**row2dict(event.Event), "username": event.username} for event in events
        ]

        for event in events_to_return:
            event_obj = Event.query.get(event["id"])
            event["members"] = [
                {
                    "id": user.id,
                    "firstname": user.firstname,
                    "familyname": user.familyname,
                }
                for user in event_obj.users
            ]

        return jsonify(events_to_return)

    def get_events_sorted_by_date(self):
        events = self.event_repository.get_events_sorted_by_date()
        events_to_return = [
            {**row2dict(event)} for event in events
        ]
        return jsonify(events_to_return)

    def get_event_by_id(self, event_id):
        event = self.event_repository.get_event_by_id(event_id)
        if not event:
            raise LookupError("Événement non trouvé")
        # Récupération des utilisateurs participants à l'événement
        members = [
            {"id": user.id, "firstname": user.firstname, "familyname": user.familyname}
            for user in event.users
        ]
        event = {**row2dict(event), "members": members}
        return event

    def update_event(self, event, data):
        return self.event_repository.update_event(event, data)

    def participate_user_to_event(self, user_id, event_id):
        event = self.event_repository.get_event_by_id(event_id)
        user = self.user_repository.get_user_by_id(user_id)

        if not event or not user:
            raise LookupError("utilisateur ou evenement non trouvé ")

        if self.event_repository.is_user_alredy_participating(event_id, user_id):
            raise FileExistsError("L'utilisateur est déjà inscrit à cet événement")

        self.event_repository.add_user_to_event(user_id, event_id)

        return {"message": "Utilisateur ajouté à l'événement avec succès"}

    def unparticipate_user_to_event(self, user_id, event_id):
        participation_db = self.event_repository.is_user_alredy_participating(
            event_id, user_id
        )
        if not participation_db:
            raise LookupError("enrgistrement non trouvé ")
        else:
            try:
                self.event_repository.delete_participation(participation_db)
                return {"message": "Utilisateur désinscrit de l'événement avec succès"}
            except Exception as e:
                raise FileExistsError("Erreur lors de la suppression du registrement")

    def delete_event(self, event_id):
        try:
            self.event_repository.delete_event(event_id)
            return {"message": "événement supprimé avec succès"}
        except Exception as e:
            raise e

        return jsonify({"message": f"Événement {event_id} supprimé avec succès"}), 200

    def get_info_manager(self, manager):
        infomanager = {
            "firstname": manager.firstname,
            "familyname": manager.familyname,
            "profileimage": manager.profileImage,
            "age": manager.age,
        }
        return infomanager
