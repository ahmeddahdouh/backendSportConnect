from flask import abort, make_response, jsonify

from app.controllers import row2dict
from app.repositories.user_repository import UserRepository


class UserService:

    def __init__(self):
        self.user_repository = UserRepository()

    def get_user_by_id(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            abort(make_response(jsonify(message="Id organisateur n'existe pas"), 400))

        events_list = self.user_repository.get_events_by_user_id(user_id)

        # Ajouter la liste des événements à la réponse utilisateur
        user_data = row2dict(user)
        user_data["events"] = events_list

        return jsonify(user_data)
