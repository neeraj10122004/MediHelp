from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import os

app = Flask(__name__)

# Allow CORS for your frontend
from flask_cors import CORS
CORS(app, resources={r"/submit": {"origins": "https://5173-neeraj10122004-medihelp-44vvu9arfl4.ws-us117.gitpod.io"}})

# Serve model files statically
app.config['MODEL_DIR'] = os.path.join(os.getcwd(), 'models')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        matrix = data.get('matrix', [])

        print('Received Matrix:', matrix)

        # Flatten the matrix into a 1D array
        flattened_array = np.array(matrix).flatten()
        print('Flattened Matrix:', flattened_array)
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
        print(ret)

        return jsonify({'predictions': ret})

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
