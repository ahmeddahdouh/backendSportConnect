# ai_service.py
import numpy as np
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences  
from app.models.donne_IA.dataset_sport import data, sport_list
from app.repositories.event_repository import EventRepository


event = EventRepository()

# Charger le modèle et le tokenizer
model = tf.keras.models.load_model("app/models/donne_IA/model.h5")

with open('app/models/donne_IA/tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

# Liste des réponses uniques
unique_answers = []
for item in data:
    if item['answer'] not in unique_answers:
        unique_answers.append(item['answer'])


def predict_category(question, threshold=0.3):
    seq = tokenizer.texts_to_sequences([question])
    pad = pad_sequences(seq, maxlen=10, padding='post')
    pred = model.predict(pad)[0]
    idx = np.argmax(pred)
    if pred[idx] < threshold:
        return "Je ne suis pas sûr de comprendre. Peux-tu reformuler ?", []

    answer = unique_answers[idx]
    sport = extract_sport_de_answer(answer)

    if sport:
        descriptions = event.get_events_description_by_sport(sport)
        if descriptions:
            message = f"{answer}\n\n\nVoici la liste des événements liés à {sport} dans notre base :"
            return message, descriptions
        else:
            message = f"{answer}\n\nAucun événement trouvé pour le sport : {sport} dans notre base."
            return message, []
    else:
        return answer, []


def extract_sport_de_answer(answer):
    answer_lower = answer.lower()
    for sport in sport_list:
        if sport in answer_lower:
            return sport
    return None
