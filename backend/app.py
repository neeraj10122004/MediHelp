from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import os
import requests
import json
import pandas as pd
import google.generativeai as genai
import re
from datetime import datetime
import pymongo
from pymongo import *

genai.configure(api_key="AIzaSyDEWge2PzWvKDCLHkPFhD4xdsvB7GPSqss")
cluster = MongoClient("mongodb+srv://root:root@cluster0.q6rbb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = cluster["MediHelp"]

#api_key = "AIzaSyBHyLJ20AujrTdKg3GrVdoDpsquQ_kcPB0"
#cx = "d7f2fb0f0d77049cc"
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
import ast 

df = pd.read_csv('embedding.csv')
df['Embeddings'] = df['Embeddings'].apply(ast.literal_eval)
import random

def find_best_passage3(query, dataframe, top_k=3, noise_factor=0.01):
    """
    Compute the cosine similarity between the query and each document in the dataframe,
    with a bit of randomness for more accurate and diverse results.
    """
    model1 = genai.GenerativeModel('gemini-1.5-pro-latest')
    a1 = model1.generate_content(f'''Convert the following user query into a structured JSON format with specified fields:

User Query: "{query}"

The output should include:
- **Personal Information**: Age, Gender, Height, Weight, Activity Level, Dietary Preference.
- **Nutrition Targets**: Daily Calorie Target, Protein, Sugar, Sodium, Carbohydrates, Fiber, Fat.
- **Health Condition**: Disease or dietary focus.

Ensure the format matches the example structure and do not enter any commnets etc andmentioin 0 if any daat is not devicable:
"
  "Ages": 25,
  "Gender": "Male",
  "Height": 180,
  "Weight": 80,
  "Activity Level": "Moderately Active",
  "Dietary Preference": "Omnivore",
  "Daily Calorie Target": 2000,
  "Protein": 120,
  "Sugar": 125.0,
  "Sodium": 24.0,
  "Calories": 2020,
  "Carbohydrates": 250,
  "Fiber": 30.0,
  "Fat": 60,
  "Disease": "Weight Gain""
'''
)
    embed_model = 'models/embedding-001'

    print(a1.text)
    query_embedding = genai.embed_content(
        model=embed_model,
        content=a1.text,
        task_type="retrieval_query"
    )["embedding"]
    
    doc_embeddings = np.stack(dataframe['Embeddings'])  
    
    
    doc_embeddings_norm = doc_embeddings / np.linalg.norm(doc_embeddings, axis=1, keepdims=True)
    query_embedding_norm = query_embedding / np.linalg.norm(query_embedding)  
    
  
    cosine_similarities = np.dot(doc_embeddings_norm, query_embedding_norm)
   
    cosine_similarities += np.random.uniform(-noise_factor, noise_factor, size=cosine_similarities.shape)
    
   
    top_k_indices = np.argsort(cosine_similarities)[-top_k:]  
    
    
    chosen_idx = random.choice(top_k_indices)
    
    return dataframe.iloc[chosen_idx]['Text'] 
def make_prompt(query, relevant_passage):
  
  escaped = relevant_passage.replace("'", "").replace('"', "").replace("\n", " ")
  prompt = """You are a helpful and informative bot that answers questions using text from the reference passage included below. \
  However, you are talking to a non-technical audience, so be sure to break down complicated concepts and \
  strike a friendly and converstional tone. \
  just use this passage as an reference and generate dite plan and ignore the disease part depend more on passage for diet suggistions and dont mention any comments
  use diete plan used in passage only and dont explain just specift the dite plan
  QUESTION: '{query}'
  PASSAGE: '{relevant_passage}'

    ANSWER:
  """.format(query=query, relevant_passage=escaped)

  return prompt


app = Flask(__name__)

# Allow CORS for your frontend
from flask_cors import CORS

CORS(app, resources={r"/submit": {"origins": "http://localhost:5173"}})
CORS(app, resources={r"/submit2": {"origins": "http://localhost:5173"}})
CORS(app, resources={r"/create_verify_user": {"origins": "http://localhost:5173"}})
CORS(app, resources={r"/add_record": {"origins": "http://localhost:5173"}})
CORS(app, resources={r"/view_record": {"origins": "http://localhost:5173"}})
CORS(app, resources={r"/chat": {"origins": "http://localhost:5173"}})
# Serve model files statically
app.config['MODEL_DIR'] = os.path.join(os.getcwd(), 'models')

@app.route('/create_verify_user', methods=['POST'])
def create_verify_user():
    print("create_verify_user")
    try:
        data = request.get_json()
        id = data.get('googleid','')
        try: 
            db.MediHelp.insert_one({"_id": id,"history":[]})
            return jsonify({'predictions': 'done'})
        except Exception as e:
            return jsonify({'predictions': 'already exist'})
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500




@app.route('/submit', methods=['POST'])
def submit():
    llm=""
    try:
        data = request.get_json()
        matrix = data.get('matrix', [])
        query = ""
        print('Received Matrix:', matrix)
        llm+="symptoms : "
        user_symptoms=[]

        # Flatten the matrix into a 1D array
        flattened_array = np.array(matrix).flatten()
        print('Flattened Matrix:', flattened_array)
        for i in range(0,len(flattened_array)):
            if(flattened_array[i]==1):
                user_symptoms.append(str(dataa[i]))
                query+=f" {str(dataa[i])}"
                llm+=f" {str(dataa[i])}"

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
        return jsonify({'predictions': ret , 'url':retu,'llm' : response.text,'symptoms' : user_symptoms})

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
            array.append(0)
        for j in verified_symptoms:
            query=query + f" {j}"
            llm= llm + f" {j}"
            array[dataa.index(j)]=1
                
        
        flattened_array = np.array(array)
        print(flattened_array)
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
        query+=f" {st}"
        llm+=f" expecting condition : {st}"
        query=query[1:]
        print(ret)
        print(query)
        

        url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={query}"
        ##url="https://cse.google.com/cse?cx=73ab211e213614850"
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
        return jsonify({'predictions': ret , 'url':retu,'llm' : response.text, 'extracted_symptoms': extracted_symptoms ,'symptoms': verified_symptoms })

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500
    
@app.route('/add_record', methods=['POST'])
def add_record():
    print("add_record")
    try:
        data = request.get_json()
        print(data)
        id = data.get('googleid','')
        predictions=data.get('predictions','') 
        url=data.get('url',[]) 
        llm=data.get('llm','') 
        extracted_symptoms=data.get('extracted_symptoms',[]) 
        symptoms = data.get('symptoms',[]) 
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        print("hello")
        document = db.MediHelp.find_one({"_id": id})
        print(document)
        history = list(document.get('history',[])) 
        print(history)
        history.append({'date':date,'predictions':predictions,'url':url,'llm':llm,'extracted_symptoms':extracted_symptoms,'symptoms':symptoms})
        db.MediHelp.update_one({"_id": id},{"$set":{"history":history}})
        return jsonify({'predictions': 'done'})
            
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

@app.route('/view_record', methods=['POST'])
def view_record():
    print("view_record")
    try:
        data = request.get_json()
        id = data.get('googleid','')
        document = db.MediHelp.find_one({"_id": id})
        history = document.get('history',[]) 
        return jsonify({'history': history})
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        resp = data.get('resp','')
        passage = find_best_passage3(resp, df)
        prompt = make_prompt(resp, passage)
        model1 = genai.GenerativeModel('gemini-1.5-pro-latest')
        answer = model1.generate_content(prompt)

        return jsonify({'result': answer.text})
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500
if __name__ == '__main__':
    app.run(debug=True, port=5000)
