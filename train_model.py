import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import lightgbm as lgb
import joblib

# Load updated dataset
data = pd.read_csv("health_cost_data1.csv")

# Encode categorical features
data["sex"] = data["sex"].map({"male": 0, "female": 1})
data["smoker"] = data["smoker"].map({"yes": 1, "no": 0})
data["region"] = data["region"].map({"southwest": 0, "southeast": 1, "northwest": 2, "northeast": 3})

# One-hot encode 'disease' column
disease_ohe = pd.get_dummies(data["disease"], prefix="disease")
data = pd.concat([data.drop("disease", axis=1), disease_ohe], axis=1)

# Interaction features
data["bmi_smoker"] = data["bmi"] * data["smoker"]
data["age_bmi"] = data["age"] * data["bmi"]

# Log transform of target
data["charges"] = np.log1p(data["charges"])

# target
X = data.drop("charges", axis=1)
y = data["charges"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = lgb.LGBMRegressor(random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(np.expm1(y_test), np.expm1(y_pred)))
r2 = r2_score(np.expm1(y_test), np.expm1(y_pred))
accuracy_percent = r2 * 100  # Convert R² score to percentage

print(f"RMSE: ₹{rmse:,.2f}")
print(f"R² Score: {r2:.4f}")
print(f"Model Accuracy (based on R²): {accuracy_percent:.2f}%")

# Save the trained model
joblib.dump(model, "healthcare_model_ohe.pkl")

# Save the feature column names 
joblib.dump(X.columns.tolist(), "model_columns.pkl")
