# ai_service.py
import numpy as np
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences  
from app.models.donne_IA.dataset_sport  import data

# Charger le modèle et le tokenizer
model = tf.keras.models.load_model("app/models/donne_IA/model.h5")

with open('app/models/donne_IA/tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

unique_answers = []
for item in data:
    if item['answer'] not in unique_answers:
        unique_answers.append(item['answer'])



def predict_category(question, threshold=0.4):  # 
    seq = tokenizer.texts_to_sequences([question])
    pad = pad_sequences(seq, maxlen=10, padding='post')
    pred = model.predict(pad)[0]
    idx = np.argmax(pred)
    if pred[idx] < threshold:
        return "Je ne suis pas sûr de comprendre. Peux-tu reformuler ?"
    return unique_answers[idx]
