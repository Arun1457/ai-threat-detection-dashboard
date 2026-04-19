import pandas as pd
import joblib

# ----------------------------
# Load combined logs
# ----------------------------
iot_logs = pd.read_csv(r"C:\study material\major_project\data\iot_logs.csv")
network_logs = pd.read_csv(r"C:\study material\major_project\data\network_logs.csv")
cloud_logs = pd.read_csv(r"C:\study material\major_project\data\cloud_logs.csv")

# Add a column to identify log source (optional)
iot_logs['source'] = 'IoT'
network_logs['source'] = 'Network'
cloud_logs['source'] = 'Cloud'

# Combine all logs
data = pd.concat([iot_logs, network_logs, cloud_logs], ignore_index=True)

# Save a copy of raw combined logs (optional)
data.to_csv(r"C:\study material\major_project\data\combined_logs.csv", index=False)

# ----------------------------
# Prepare features
# ----------------------------
X = data.drop(['timestamp', 'anomaly_flag'], axis=1, errors='ignore')  # drop target if exists
X = pd.get_dummies(X)

# ----------------------------
# Load trained model
# ----------------------------
model = joblib.load(r"C:\study material\major_project\backend\trained_model.pkl")

# ----------------------------
# Predict anomalies
# ----------------------------
data['anomaly_flag'] = model.predict(X)

# ----------------------------
# Save predictions
# ----------------------------
data.to_csv(r"C:\study material\major_project\data\predicted_logs.csv", index=False)
print("Predictions saved to predicted_logs.csv")
