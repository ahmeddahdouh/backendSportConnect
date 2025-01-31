from flask import Blueprint, jsonify

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@main_bp.route('/firstjsonapi')
def firstjsonapi():
    return jsonify({"message":'hello world from json'})