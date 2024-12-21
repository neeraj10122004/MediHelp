from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import os
import requests
import json
import re
import google.generativeai as genai
from flask_cors import CORS

# Configure Generative AI
genai.configure(api_key="AIzaSyA50tLF5dWf8KZ1B1vztgwj4Za7Yzt-w6M")

# API Keys for Google Custom Search

api_key = "AIzaSyCHcbZ83HTbR_TOcyCh9inGXblu8EZo-ZA"
cx = "73ab211e213614850"

# Predefined dataset of symptoms
dataa = [
    'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
    'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition',
    'spotting_urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss',
    'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes',
    'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea',
    'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea',
    'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload',
    'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm',
    'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain',
    'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
    'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
    'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties',
    'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain',
    'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements',
    'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort',
    'foul_smell_of_urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
    'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain',
    'abnormal_menstruation', 'dischromic_patches', 'watering_from_eyes', 'increased_appetite', 'polyuria',
    'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration', 'visual_disturbances',
    'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding',
    'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum',
    'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scarring',
    'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister',
    'red_sore_around_nose', 'yellow_crust_ooze'
]

app = Flask(__name__)
CORS(app)

# Serve models from the 'models' directory
app.config['MODEL_DIR'] = os.path.join(os.getcwd(), 'models')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        matrix = data.get('matrix', [])
        flattened_array = np.array(matrix).flatten()
        query = "+".join([dataa[i] for i, val in enumerate(flattened_array) if val == 1])

        # Load the predictive model
        model_path = os.path.join(app.config['MODEL_DIR'], 'medical.h5')
        model = tf.keras.models.load_model(model_path)

        # Prepare input for prediction
        input_tensor = np.expand_dims(flattened_array, axis=0)
        predictions = model.predict(input_tensor)[0]

        # Identify the most likely illness
        illness = [
            'Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Peptic ulcer disease', 'AIDS',
            'Diabetes', 'Gastroenteritis', 'Bronchial Asthma', 'Hypertension', 'Migraine', 'Cervical spondylosis',
            'Paralysis (brain hemorrhage)', 'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'Hepatitis A',
            'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis',
            'Common Cold', 'Pneumonia', 'Dimorphic hemorrhoids (piles)', 'Heart attack', 'Varicose veins',
            'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthritis', 'Arthritis',
            '(vertigo) Paroxysmal Positional Vertigo', 'Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo'
        ]
        max_index = np.argmax(predictions)
        predicted_illness = illness[max_index]
        confidence = predictions[max_index]

        # Generate search results
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}"
        search_response = requests.get(url).json()
        search_results = search_response.get('items', [])

        return jsonify({
            'predicted_illness': predicted_illness,
            'confidence': confidence,
            'search_results': search_results
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/submit2', methods=['POST'])
def submit2():
    print("submit 2")
    try:
        data = request.get_json()
        text_input = data.get('textinput',"")
        print(text_input)

        # Prompt for symptom extraction
        prompt = (
            f"You are an intelligent assistant tasked with extracting symptoms from a predefined dataset based on a "
            f"user-provided text description. The dataset contains: {dataa}. "
            f"User's text input: {text_input}. "
            f"List the matching symptoms from the dataset."
        )

        # Generate symptoms
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt, generation_config=genai.GenerationConfig(
            max_output_tokens=1000, temperature=0.1
        ))
        output_text = response.text
        extracted_symptoms = re.findall(r"\w+", output_text)

        # Filter symptoms that match the dataset
        verified_symptoms = [symptom for symptom in extracted_symptoms if symptom in dataa]
        print(verified_symptoms)

        return jsonify({'extracted_symptoms': verified_symptoms})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
