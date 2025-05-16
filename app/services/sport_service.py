from app.repositories.sport_repository import SportRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_sports_repository import UserSportsRepository


class SportService:
    def __init__(self):
        self.sport_repository = SportRepository()
        self.user_repository = UserRepository()
        self.user_sports_repository = UserSportsRepository()

    def get_all_sports(self):
        """Récupère tous les sports disponibles"""
        return self.sport_repository.get_all_sports()

    def get_sports_by_user_id(self, user_id):
        """Obtient la liste des sports joués par un utilisateur avec ses statistiques"""
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404

        user_sports = self.user_sports_repository.get_sports_by_user_id(user_id)
        if not user_sports:
            return {"message": "User has no associated sports."}, 404

        sports_data = []
        for entry in user_sports:
            sport = self.sport_repository.get_sport_by_id(entry.sport_id)
            sports_data.append({
                "sport_id": entry.sport_id,
                "sport_name": sport.sport_nom,
                "sport_stat": entry.sport_stat,
            })

        return {
            "user_id": user_id,
            "firstname": user.firstname,
            "familyname": user.familyname,
            "sports": sports_data,
        }, 200

    def add_sport_to_user(self, user_id, sport_id, sport_stat):
        """Ajoute un sport à un utilisateur avec ses statistiques"""
        # Vérifier si le sport existe déjà pour cet utilisateur
        if self.user_sports_repository.exists(user_id, sport_id):
            return {"message": "Sport already exists for this user."}, 400

        # Ajouter le sport à l'utilisateur
        self.user_sports_repository.add_sport_to_user(user_id, sport_id, sport_stat)

        return {"message": "Sport added successfully."}, 201

    def update_sport_stats(self, user_id, sport_id, sport_stat):
        """Met à jour les statistiques d'un sport pour un utilisateur"""
        # Vérifier si le sport existe pour cet utilisateur
        user_sport = self.user_sports_repository.get_user_sport(user_id, sport_id)
        if not user_sport:
            return {"message": "Sport not found for this user."}, 404

        # Mettre à jour les statistiques
        self.user_sports_repository.update_sport_stats(user_id, sport_id, sport_stat)

        return {"message": "Sport stats updated successfully."}, 200

    def delete_sport_from_user(self, user_id, sport_id):
        """Supprime un sport de la liste des sports joués par un utilisateur"""
        # Vérifier si le sport existe pour cet utilisateur
        user_sport = self.user_sports_repository.get_user_sport(user_id, sport_id)
        if not user_sport:
            return {"message": "Sport not found for this user."}, 404

        # Supprimer le sport
        self.user_sports_repository.delete_sport_from_user(user_id, sport_id)

        return {"message": "Sport removed successfully."}, 200