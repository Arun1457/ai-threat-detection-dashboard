import pandas as pd
import joblib
import os
from severity_engine import assign_severity
import numpy as np

# --- Paths ---
DATA_PATH = r"C:\study material\major_project\data\combined_logs.csv"
MODEL_PATH = r"C:\study material\major_project\backend\combined_model.pkl"
OUTPUT_PATH = r"C:\study material\major_project\data\predicted_combined_logs.csv"

# --- Load combined logs ---
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ File not found: {DATA_PATH}")

data = pd.read_csv(DATA_PATH)
print(f"✅ Loaded {data.shape[0]} rows and {data.shape[1]} columns from combined_logs.csv")

# --- Load trained model ---
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"❌ Model not found: {MODEL_PATH}")

model = joblib.load(MODEL_PATH)
print("✅ Loaded trained model")

# --- Prepare features ---
X = data.drop(['timestamp', 'anomaly_flag'], axis=1, errors='ignore')

# One-hot encode categorical columns
X = pd.get_dummies(X)
print("🔠 One-hot encoding applied to categorical columns")

# Align features with model
if hasattr(model, 'feature_names_in_'):
    model_features = model.feature_names_in_
    for col in model_features:
        if col not in X.columns:
            X[col] = 0
    X = X[model_features]
    print("✅ Features aligned with trained model")

# --- Make predictions ---
data['predicted_anomaly'] = model.predict(X)

base_conf = model.predict_proba(X)[:, 1]

# Add slight randomness
data['confidence'] = base_conf + np.random.uniform(-0.2, 0.2, size=len(base_conf))

# Keep values between 0 and 1
data['confidence'] = data['confidence'].clip(0, 1)

print("🚀 Predictions completed")

# --- Add severity ---
data['severity'] = data.apply(assign_severity, axis=1)

# --- Save predicted logs ---
data.to_csv(OUTPUT_PATH, index=False)
print(f"💾 Predicted logs saved to: {OUTPUT_PATH}")
