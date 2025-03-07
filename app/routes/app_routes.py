from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def hello_world():
    # put application's code here
    """
        Exemple d'endpoint avec documentation Flasgger.
        ---
        responses:
          200:
            description: Retourne un message de bienvenue
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Hello, world!"
        """
    return "Hello World!"


@main_bp.route("/firstjsonapi")
def firstjsonapi():
    return jsonify({"message": "hello world from json"})
