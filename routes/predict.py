from flask import Blueprint, request, jsonify
import joblib
import numpy as np
import pandas as pd
import os

predict = Blueprint('predict', __name__)

# Correct path to model file
model_path = os.path.join(os.path.dirname(__file__), '..', 'healthcare_model_ohe.pkl')
model = joblib.load(model_path)

DISEASE_ORDER = [
    "Cancer",
    "Chronic Kidney Disease",
    "Heart Disease",
    "Organ Transplant",
    "Stroke"
]

@predict.route('/predict', methods=['POST'])
def predict_cost():
    try:
        data = request.get_json()
        print("Received Data:", data)

        sex_map = {"male": 0, "female": 1}
        smoker_map = {"yes": 1, "no": 0}
        region_map = {"southwest": 0, "southeast": 1, "northwest": 2, "northeast": 3}

        age = float(data.get('age'))
        bmi = float(data.get('bmi'))
        children = int(data.get('children'))
        sex = sex_map.get(data.get('sex').lower(), -1)
        smoker = smoker_map.get(data.get('smoker').lower(), -1)
        region = region_map.get(data.get('region').lower(), -1)
        disease = data.get('disease')

        if -1 in (sex, smoker, region) or disease not in DISEASE_ORDER:
            return jsonify({"error": "Invalid input data"}), 400

        disease_ohe = [1 if disease == d else 0 for d in DISEASE_ORDER]
        bmi_smoker = bmi * smoker
        age_bmi = age * bmi

        features = np.array([[age, sex, bmi, children, smoker, region] + disease_ohe + [bmi_smoker, age_bmi]])
        prediction = model.predict(features)[0]
        predicted_cost = np.expm1(prediction)

        return jsonify({"predicted_cost": round(predicted_cost, 2)}), 200


    except Exception as e:
        print("Prediction Error:", str(e))
        return jsonify({"error": "Prediction failed. Check input format."}), 500
