from app.repositories.team_repository import TeamRepository
from app.repositories.team_users_repository import TeamUsersRepository
from app.repositories.team_sports_repository import TeamSportsRepository


class TeamService:
    def __init__(self):
        self.team_repository = TeamRepository()
        self.team_users_repository = TeamUsersRepository()
        self.team_sports_repository = TeamSportsRepository()

    def create_team(self, manager_id, name, description, profile_picture):
        """Crée une nouvelle équipe"""
        team_id = self.team_repository.create_team(manager_id, name, description, profile_picture)
        return {"message": "Team created successfully.", "team_id": team_id}, 201

    def delete_team(self, team_id, manager_id):
        """Supprime une équipe"""
        team = self.team_repository.get_team_by_id(team_id)
        if not team:
            return {"message": "Team not found."}, 404

        if team.manager_id != manager_id:
            return {"message": "Unauthorized."}, 403

        self.team_repository.delete_team(team)
        return {"message": "Team deleted successfully."}, 200

    def update_team(self, team_id, manager_id, data):
        """Met à jour les informations d'une équipe"""
        team = self.team_repository.get_team_by_id(team_id)
        if not team:
            return {"message": "Team not found."}, 404

        if team.manager_id != manager_id:
            return {"message": "Unauthorized."}, 403

        # Mise à jour des données de l'équipe
        name = data.get("name", team.name)
        description = data.get("description", team.description)
        profile_picture = data.get("profile_picture", team.profile_picture)
        new_manager_id = data.get("manager_id", team.manager_id)

        self.team_repository.update_team(team, name, description, profile_picture, new_manager_id)
        return {"message": "Team updated successfully."}, 200

    def add_team_member(self, team_id, user_id):
        """Ajoute un membre à une équipe"""
        # Vérification optionnelle: on pourrait vérifier si l'équipe existe

        # Vérification optionnelle: on pourrait vérifier si l'utilisateur est déjà membre

        self.team_users_repository.add_member(team_id, user_id)
        return {"message": "Member added successfully."}, 201

    def remove_team_member(self, team_id, user_id):
        """Supprime un membre d'une équipe"""
        member = self.team_users_repository.get_member(team_id, user_id)
        if not member:
            return {"message": "Member not found in the team."}, 404

        self.team_users_repository.remove_member(member)
        return {"message": "Member removed successfully."}, 200

    def add_team_sport(self, team_id, sport_id, sport_stat):
        """Ajoute un sport à une équipe"""
        # Vérification optionnelle: on pourrait vérifier si l'équipe existe

        # Vérification optionnelle: on pourrait vérifier si le sport n'est pas déjà associé

        self.team_sports_repository.add_sport(team_id, sport_id, sport_stat)
        return {"message": "Sport added successfully."}, 201

    def remove_team_sport(self, team_id, sport_id):
        """Supprime un sport d'une équipe"""
        team_sport = self.team_sports_repository.get_team_sport(team_id, sport_id)
        if not team_sport:
            return {"message": "Sport not found in the team."}, 404

        self.team_sports_repository.remove_sport(team_sport)
        return {"message": "Sport removed successfully."}, 200

    def update_team_sport_stat(self, team_id, sport_id, user_id, sport_stat):
        """Met à jour les statistiques d'un sport pour une équipe"""
        # Vérifier si l'équipe existe
        team = self.team_repository.get_team_by_id(team_id)
        if not team:
            return {"message": "Team not found."}, 404

        # Vérifier si l'utilisateur est le manager de l'équipe
        if team.manager_id != user_id:
            return {"message": "You are not authorized to update this team's stats."}, 403

        # Vérifier si le sport est associé à l'équipe
        team_sport = self.team_sports_repository.get_team_sport(team_id, sport_id)
        if not team_sport:
            return {"message": "This sport is not associated with the team."}, 404

        # Mettre à jour les statistiques
        self.team_sports_repository.update_sport_stats(team_sport, sport_stat)
        return {"message": "Team sport stats updated successfully."}, 200

    def get_team_info(self, team_id):
        """Récupère les informations détaillées d'une équipe"""
        team = self.team_repository.get_team_by_id(team_id)
        if not team:
            return {"message": "Team not found."}, 404

        # Récupérer les sports pratiqués par l'équipe
        team_sports = self.team_sports_repository.get_sports_by_team_id(team_id)
        sports_data = [
            {"sport_id": ts.sport_id, "sport_stat": ts.sport_stat} for ts in team_sports
        ]

        # Récupérer les membres de l'équipe
        team_members = self.team_users_repository.get_members_by_team_id(team_id)
        members_data = [{"user_id": tu.user_id} for tu in team_members]

        # Retourner les informations complètes de l'équipe
        return {
            "team_id": team.id,
            "name": team.name,
            "description": team.description,
            "profile_picture": team.profile_picture,
            "manager_id": team.manager_id,
            "sports": sports_data,
            "members": members_data,
        }, 200

    def get_user_teams(self, user_id):
        """Récupère les équipes dont l'utilisateur est membre"""
        user_teams = self.team_users_repository.get_teams_by_user_id(user_id)
        if not user_teams:
            return {"message": "User has not joined any teams."}, 404

        teams_data = []
        for entry in user_teams:
            team = self.team_repository.get_team_by_id(entry.team_id)
            teams_data.append({
                "team_id": team.id,
                "name": team.name,
                "description": team.description,
                "profile_picture": team.profile_picture,
            })

        return {"user_id": user_id, "teams": teams_data}, 200