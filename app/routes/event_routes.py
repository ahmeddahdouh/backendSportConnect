from threading import Event

from flask import Blueprint

event_bp = Blueprint('event', __name__)

@event_bp.route("/",methods=['POST'])
def add_event():
    from flask import request

    data = request.get_json()

    id_gestionnaire = data['id_gestionnaire']
    id_sport = data['id_sport']
    event_ville = data['event_ville']
    event_date = data['event_date']
    event_max_utilisateur = data['event_max_utilisateur']
    event_Items = data['event_Items']
    is_private = data['is_private']
    is_team_vs_team = data['is_team_vs_team']
    event_age_min = data['event_age_min']
    event_age_max = data['event_age_max']
    nombre_utilisateur_min = data['nombre_utilisateur_min']

    # Création de l'objet Event
    event = Event(
        id_gestionnaire=id_gestionnaire,
        id_sport=id_sport,
        event_ville=event_ville,
        event_date=event_date,
        event_max_utilisateur=event_max_utilisateur,
        event_Items=event_Items,
        is_private=is_private,
        is_team_vs_team=is_team_vs_team,
        event_age_min=event_age_min,
        event_age_max=event_age_max,
        nombre_utilisateur_min=nombre_utilisateur_min
    )

    db.session.add(event)
    db.session.commit()
    db.session.flush()




@event_bp.route("/",methods=['GET'])
def  get_event():
    return ("hello events ")