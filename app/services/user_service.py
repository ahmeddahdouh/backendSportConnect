import json
import os
import uuid
from datetime import timedelta

import bcrypt
from flask import abort, make_response, jsonify, current_app
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError

from app.controllers import row2dict
from app.models import User
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
        user_data["events"] =  [row2dict(event) for event in events_list]
        user_data["age"] = user.age
        return jsonify(user_data)

    def get_user_by_phone(self, phone):
        """
        Get user information by phone number.
        
        Args:
            phone (str): The phone number to search for
            
        Returns:
            dict: User data if found
            
        Raises:
            ValueError: If user is not found
        """
        user = self.user_repository.get_user_by_phone(phone)
        if not user:
            raise ValueError("User not found")
        return row2dict(user)

    def create_user(self, data):
        try:
            data["password"] = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            self.user_repository.add_user(data)
        except ValueError as e:
            raise ValueError(f"{e}")
        except Exception as e:
            raise e

    def update_user(self, data, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User does not exist")
        else:
            for k, v in data.items():
                if hasattr(user, k):
                    setattr(user, k, v)

            if "password" in data:
                hashed_password = bcrypt.hashpw(
                    data["password"].encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8")
                user.password = hashed_password
            try:
                self.user_repository.update_user()
            except IntegrityError as Ie:
                raise IntegrityError(f"{Ie.orig if Ie.orig else Ie}")
            except Exception as e:
                raise e

    def get_users(self):
        users = self.user_repository.get_users()
        return [row2dict(user) for user in users]

    def update_profile_image(self, user_id, file):
        file_ext = file.filename.split(".")[-1]
        unique_id = uuid.uuid4()
        profileImageName = str(unique_id) + "." + file_ext
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], profileImageName)
        file.save(file_path)
        user = self.user_repository.get_user_by_id(user_id)
        try :
            user.profile_image = profileImageName
            self.user_repository.update_profile_image()
            return profileImageName
        except Exception as e:
            raise e

    def login(self, username, password):
        user = self.user_repository.get_user_by_username(username)
        if not user:
            return {"message": "User does not exist"}, 404

        if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            return {"message": "Invalid credentials"}, 401

        access_token = create_access_token(
                identity=json.dumps({
                    "username": user.username,
                    "id": user.id,
                    "profileImage": user.profile_image
                }),
                expires_delta=timedelta(hours=1),
            )

        return {"access_token": access_token}, 200
