import pandas as pd
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder
import os

# --- Paths ---
DATA_PATH = r"C:\study material\major_project\data\combined_logs.csv"
MODEL_PATH = r"C:\study material\major_project\backend\combined_model.pkl"
OUTPUT_PATH = r"C:\study material\major_project\data\test_predictions.csv"

# --- Load data and model ---
data = pd.read_csv(DATA_PATH)
model = joblib.load(MODEL_PATH)
print(f"✅ Loaded data ({data.shape[0]} rows) and model")

# --- Inject 30 detectable anomalies ---
print("⚙️ Injecting 30 detectable anomalies...")
anomaly_rows = []
np.random.seed(42)

for i in range(30):
    anomaly_rows.append({
        "timestamp": pd.Timestamp.now(),
        "source": np.random.choice(["IoT", "Network", "Cloud"]),
        "entity": f"anomaly_entity_{i}",
        "activity": np.random.choice(["unauthorized_access", "data_exfiltration", "malware_activity"]),
        "resource": "Malicious_Resource",
        "destination": f"255.255.255.{i}",
        "port": 65535,
        "protocol": "malware",
        "anomaly_flag": 1
    })

anomalies = pd.DataFrame(anomaly_rows)

# --- Combine with original data ---
data = pd.concat([data, anomalies], ignore_index=True)
print(f"✅ Total rows after injection: {data.shape[0]}")

# --- Encode only categorical columns (exclude timestamp) ---
categorical_cols = ['source', 'entity', 'activity', 'resource', 'destination', 'protocol']
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col].astype(str))  # ensure everything is string
    label_encoders[col] = le

# --- Prepare features ---
X = data.drop(['timestamp', 'anomaly_flag'], axis=1, errors='ignore')

# --- Align columns with model ---
if hasattr(model, 'feature_names_in_'):
    model_features = model.feature_names_in_
    for col in model_features:
        if col not in X.columns:
            X[col] = 0
    X = X[model_features]

# --- Predict ---
data['predicted_anomaly'] = model.predict(X)

# --- Save results ---
data.to_csv(OUTPUT_PATH, index=False)
print(f"💾 Predictions with anomalies saved to: {OUTPUT_PATH}")

# --- Report detected anomalies ---
detected = data[data['predicted_anomaly'] == 1]
print(f"Total anomalies detected by model: {len(detected)}")
print(detected.tail(10))
