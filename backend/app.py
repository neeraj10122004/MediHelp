from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import os
import requests
import json
import pandas as pd
import google.generativeai as genai
import re
genai.configure(api_key="AIzaSyA50tLF5dWf8KZ1B1vztgwj4Za7Yzt-w6M")


api_key = "AIzaSyCHcbZ83HTbR_TOcyCh9inGXblu8EZo-ZA"
cx = "73ab211e213614850"
dataa = [
      'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting',
      'burning_micturition', 'spotting_urination', 'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy', 'patches_in_throat', 'irregular_sugar_level',
      'cough', 'high_fever', 'sunken_eyes', 'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain',
      'constipation', 'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision',
      'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
      'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger',
      'extra_marital_contacts', 'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck', 'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance',
      'unsteadiness', 'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of_urine', 'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability',
      'muscle_pain', 'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'dischromic_patches', 'watering_from_eyes', 'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum',
      'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum',
      'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scarring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
      'yellow_crust_ooze',
    ]
app = Flask(__name__)

# Allow CORS for your frontend
from flask_cors import CORS

CORS(app, resources={r"/submit": {"origins": "https://5173-neeraj10122004-medihelp-44vvu9arfl4.ws-us117.gitpod.io"}})
CORS(app, resources={r"/submit2": {"origins": "https://5173-neeraj10122004-medihelp-44vvu9arfl4.ws-us117.gitpod.io"}})

# Serve model files statically
app.config['MODEL_DIR'] = os.path.join(os.getcwd(), 'models')

@app.route('/submit', methods=['POST'])
def submit():
    llm=""
    try:
        data = request.get_json()
        matrix = data.get('matrix', [])
        query = ""
        print('Received Matrix:', matrix)
        llm+="symptoms : "

        # Flatten the matrix into a 1D array
        flattened_array = np.array(matrix).flatten()
        print('Flattened Matrix:', flattened_array)
        for i in range(0,len(flattened_array)):
            if(flattened_array[i]==1):

                query+="+"
                query+=str(dataa[i])
                llm+=f"+ {str(dataa[i])}"

        print(flattened_array.shape)

        # Load the model
        model = tf.keras.models.load_model('medical.h5')  # Adjust the path if necessary

        # Ensure input shape is correct for the model
        input_tensor = np.expand_dims(flattened_array, axis=0)  # Add batch dimension

        # Make predictions
        predictions = model.predict(input_tensor)
        print(predictions)
        # Send predictions as JSON response
        predictions=predictions.tolist()
        print(predictions)
        illness=['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction','Peptic ulcer disease', 'AIDS', 'Diabetes', 'Gastroenteritis', 'Bronchial Asthma', 'Hypertension', 'Migraine', 'Cervical spondylosis', 'Paralysis (brain hemorrhage)', 'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemorrhoids (piles)', 'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthritis', 'Arthritis', '(vertigo) Paroxysmal Positional Vertigo', 'Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']
        # Convert predictions to a flat list
        predictions = predictions[0]  # Extract the first row (since batch size is 1)
        max_value = max(predictions)
        max_index = predictions.index(max_value)


        # Find the index of the maximum element
        max_index =predictions.index(max_value)
        print(max_index)
        print(illness[max_index])
        st=str(illness[max_index])
        val=str(max_value)
        ret=f" {val} : {st}"
        query+=st
        llm+=f" expecting condition : {st}"
        query=query[1:]
        print(ret)
        print(query)
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}"
        response = requests.get(url)
        data = json.loads(response.text)
        retu=[]

        # Check for errors or empty search results
        if 'error' in data:
            print("Error:", data['error']['message'])
        elif 'items' not in data:
            print("No search results found.")
        else:
            # Extract search results
            search_results = data['items']

            # Create a list to store the data
            all_data = []
            for result in search_results:
                title = result['title']
                link = result['link']
                snippet = result['snippet']
                all_data.append({'Title': title, 'Link': link, 'Snippet': snippet})
                # Create a pandas DataFrame using pd.DataFrame()
            retu=all_data

                # Display the DataFrame
            print(retu)
        print("llm response : ")
        print(llm)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(llm,
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1,

            ),
                                  safety_settings={'HARASSMENT':'block_none'}
        )
        print(response.text)
        return jsonify({'predictions': ret , 'url':retu,'llm' : response.text})

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

@app.route('/submit2', methods=['POST'])
def submit2():
    print("submit2")
    llm=""
    try:
        data = request.get_json()
        textinput = data.get('textinput',"")
        print(textinput)
        # Define the prompt
        prompt = (
            f"You are an intelligent assistant tasked with extracting symptoms from a predefined dataset based on a user-provided text description. "
            f"The dataset, called 'dataa', contains the following symptoms: {dataa}. "
            f"Analyze the user's text input and match the mentioned symptoms to those in the dataset. "
            f"If a symptom is implied or synonymous with those in the dataset, include it in the output. "
            f"The result should be a concise list of matching symptoms.\n\n"
            f"User's text input: {textinput}\n\n"
            f"Output format:\n"
            f"- List of matching symptoms: [symptom1, symptom2, symptom3, ...]\n\n"
            f"Generate the list of matching symptoms now."
        )

        print(prompt)

        # Initialize the Generative AI model
        model = genai.GenerativeModel('gemini-pro')

        # Generate the response
        response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1,
        ),
        safety_settings={'HARASSMENT': 'block_none'}
        )


    

# Output from the model
        output_text = response.text

# Extract symptoms from the output
        extracted_symptoms = re.findall(r"- (.+)", output_text)

# Verify symptoms against the dataset
        verified_symptoms = [symptom for symptom in extracted_symptoms if symptom in dataa]

# Print results
        print("Extracted Symptoms:", extracted_symptoms)
        print("Verified Symptoms:", verified_symptoms)

# Print the response
        print(response.text)




        query = ""
        llm+="symptoms : "
        
        # Flatten the matrix into a 1D array
        array=[]
        jj=0
        for i in range(0,len(dataa)):
            if(jj<len(verified_symptoms)):
                if(verified_symptoms[jj]==dataa[i]):
                    array.append(1)
                else:
                    array.append(0)
            else:
                array.append(0)
            jj+=1
        
        flattened_array = np.array(array)

        print(flattened_array.shape)

        # Load the model
        model = tf.keras.models.load_model('medical.h5')  # Adjust the path if necessary

        # Ensure input shape is correct for the model
        input_tensor = np.expand_dims(flattened_array, axis=0)  # Add batch dimension

        # Make predictions
        predictions = model.predict(input_tensor)
        print(predictions)
        # Send predictions as JSON response
        predictions=predictions.tolist()
        print(predictions)
        illness=['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction','Peptic ulcer disease', 'AIDS', 'Diabetes', 'Gastroenteritis', 'Bronchial Asthma', 'Hypertension', 'Migraine', 'Cervical spondylosis', 'Paralysis (brain hemorrhage)', 'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemorrhoids (piles)', 'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthritis', 'Arthritis', '(vertigo) Paroxysmal Positional Vertigo', 'Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']
        # Convert predictions to a flat list
        predictions = predictions[0]  # Extract the first row (since batch size is 1)
        max_value = max(predictions)
        max_index = predictions.index(max_value)


        # Find the index of the maximum element
        max_index =predictions.index(max_value)
        print(max_index)
        print(illness[max_index])
        st=str(illness[max_index])
        val=str(max_value)
        ret=f" {val} : {st}"
        query+=st
        llm+=f" expecting condition : {st}"
        query=query[1:]
        print(ret)
        print(query)
        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}"
        response = requests.get(url)
        data = json.loads(response.text)
        retu=[]

        # Check for errors or empty search results
        if 'error' in data:
            print("Error:", data['error']['message'])
        elif 'items' not in data:
            print("No search results found.")
        else:
            # Extract search results
            search_results = data['items']

            # Create a list to store the data
            all_data = []
            for result in search_results:
                title = result['title']
                link = result['link']
                snippet = result['snippet']
                all_data.append({'Title': title, 'Link': link, 'Snippet': snippet})
                # Create a pandas DataFrame using pd.DataFrame()
            retu=all_data

                # Display the DataFrame
            print(retu)
        print("llm response : ")
        print(llm)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(llm,
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=0.1,

            ),
                                  safety_settings={'HARASSMENT':'block_none'}
        )
        print(response.text)
        return jsonify({'predictions': ret , 'url':retu,'llm' : response.text})

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
