from config import db
from app.models.team import Team


class TeamRepository:
    def get_team_by_id(self, team_id):
        """Récupère une équipe par son ID"""
        return Team.query.get(team_id)

    def create_team(self, manager_id, name, description, profile_picture):
        """Crée une nouvelle équipe"""
        new_team = Team(
            name=name,
            description=description,
            profile_picture=profile_picture,
            manager_id=manager_id,
        )
        db.session.add(new_team)
        db.session.commit()
        return new_team.id

    def delete_team(self, team):
        """Supprime une équipe"""
        db.session.delete(team)
        db.session.commit()

    def update_team(self, team, name, description, profile_picture, manager_id):
        """Met à jour les informations d'une équipe"""
        team.name = name
        team.description = description
        team.profile_picture = profile_picture
        team.manager_id = manager_id
        db.session.commit()