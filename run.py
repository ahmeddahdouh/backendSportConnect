from flask import Flask, jsonify
from flask_cors import CORS
from app import create_app

app = create_app()
CORS(app, resources={r"/auth/*": {"origins": "http://localhost:3001"}})


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/firstjsonapi')
def firstjsonapi():
    return jsonify({"message":'hello world from json'})




if __name__ == '__main__':
    app.run()
