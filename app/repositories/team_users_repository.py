from config import db
from app.associations.team_users_sports import TeamUsers


class TeamUsersRepository:
    def get_member(self, team_id, user_id):
        """Récupère un membre spécifique d'une équipe"""
        return TeamUsers.query.filter_by(team_id=team_id, user_id=user_id).first()

    def get_members_by_team_id(self, team_id):
        """Récupère tous les membres d'une équipe"""
        return TeamUsers.query.filter_by(team_id=team_id).all()

    def get_teams_by_user_id(self, user_id):
        """Récupère toutes les équipes d'un utilisateur"""
        return TeamUsers.query.filter_by(user_id=user_id).all()

    def add_member(self, team_id, user_id):
        """Ajoute un membre à une équipe"""
        new_member = TeamUsers(user_id=user_id, team_id=team_id)
        db.session.add(new_member)
        db.session.commit()

    def remove_member(self, member):
        """Supprime un membre d'une équipe"""
        db.session.delete(member)
        db.session.commit()