from app.controllers import row2dict
from app.models.sport import Sport



class SportRepository:
    def get_all_sports(self):
        """Récupère tous les sports disponibles"""
        sports = Sport.query.all()
        return [row2dict(sport) for sport in sports]

    def get_sport_by_id(self, sport_id):
        """Récupère un sport par son ID"""
        return Sport.query.get(sport_id)