from config import db
from app.associations.user_sports import UserSports


class UserSportsRepository:
    def get_sports_by_user_id(self, user_id):
        """Récupère tous les sports associés à un utilisateur"""
        return UserSports.query.filter_by(user_id=user_id).all()

    def get_user_sport(self, user_id, sport_id):
        """Récupère une association spécifique entre un utilisateur et un sport"""
        return UserSports.query.filter_by(user_id=user_id, sport_id=sport_id).first()

    def exists(self, user_id, sport_id):
        """Vérifie si un sport est déjà associé à un utilisateur"""
        user_sport = UserSports.query.filter_by(user_id=user_id, sport_id=sport_id).first()
        return user_sport is not None

    def add_sport_to_user(self, user_id, sport_id, sport_stat):
        """Ajoute un sport à un utilisateur avec ses statistiques"""
        new_user_sport = UserSports(user_id=user_id, sport_id=sport_id, sport_stat=sport_stat)
        db.session.add(new_user_sport)
        db.session.commit()

    def update_sport_stats(self, user_id, sport_id, sport_stat):
        """Met à jour les statistiques d'un sport pour un utilisateur"""
        user_sport = self.get_user_sport(user_id, sport_id)
        if user_sport:
            user_sport.sport_stat = sport_stat
            db.session.commit()

    def delete_sport_from_user(self, user_id, sport_id):
        """Supprime un sport de la liste des sports joués par un utilisateur"""
        user_sport = self.get_user_sport(user_id, sport_id)
        if user_sport:
            db.session.delete(user_sport)
            db.session.commit()