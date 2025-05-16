from config import db
from app.associations.team_users_sports import TeamSports


class TeamSportsRepository:
    def get_team_sport(self, team_id, sport_id):
        """Récupère une association spécifique entre une équipe et un sport"""
        return TeamSports.query.filter_by(team_id=team_id, sport_id=sport_id).first()

    def get_sports_by_team_id(self, team_id):
        """Récupère tous les sports pratiqués par une équipe"""
        return TeamSports.query.filter_by(team_id=team_id).all()

    def add_sport(self, team_id, sport_id, sport_stat):
        """Ajoute un sport à une équipe"""
        new_sport = TeamSports(team_id=team_id, sport_id=sport_id, sport_stat=sport_stat)
        db.session.add(new_sport)
        db.session.commit()

    def remove_sport(self, team_sport):
        """Supprime un sport d'une équipe"""
        db.session.delete(team_sport)
        db.session.commit()

    def update_sport_stats(self, team_sport, sport_stat):
        """Met à jour les statistiques d'un sport pour une équipe"""
        team_sport.sport_stat = sport_stat
        db.session.commit()