from sqlalchemy.exc import IntegrityError

from app.models import User
from app.models import Event
from config import db


class UserRepository:

    def get_user_by_id(self, user_id):
        result = User.query.filter_by(id=user_id).first()
        return result

    def get_events_by_user_id(self, user_id):
        results = (
            db.session.query(Event)
            .join(User, User.id == Event.id_gestionnaire)
            .filter(User.id == 1)
            .all()
        )

    def add_user(self, user_data):
        user_db = User(**user_data)
        try:
            db.session.add(user_db)
            db.session.commit()
        except IntegrityError as Ie:
            db.session.rollback()
            raise ValueError({"message integrity error":f"{Ie.orig if Ie.orig else Ie }"})

        except Exception as e:
            db.session.rollback()
            raise e

    def update_user(self):
        try:
            db.session.commit()
        except IntegrityError as e :
            db.session.rollback()
            raise IntegrityError(f'{e.orig if e.orig else e}')
        except Exception as e:
            db.session.rollback()
            raise e

    def get_users(self):
        return db.session.query(User).all()

    def update_profile_image(self):
        try :
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


    def get_user_by_username(self, username):
        return User.query.filter_by(username=username).first()