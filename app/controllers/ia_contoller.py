# app.py
from flask import Flask, request, jsonify
from app.services.ai_service import predict_category
from flask import Blueprint, jsonify, request


ia_bp = Blueprint('ia_bp', __name__)


@ia_bp.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({'error': 'Question is required'}), 400

    category = predict_category(question)
    return jsonify({'category': category})
