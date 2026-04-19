import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# ----------------------------
# Load cleaned logs
# ----------------------------
data = pd.read_csv(r"C:\study material\major_project\data\cleaned_logs.csv")

# Convert timestamp to datetime (optional, if needed)
data['timestamp'] = pd.to_datetime(data['timestamp'])

# ----------------------------
# Features & Target
# ----------------------------
# Drop timestamp and target column
X = data.drop(['timestamp', 'anomaly_flag'], axis=1)

# Convert all categorical columns to dummy/one-hot
X = pd.get_dummies(X)

y = data['anomaly_flag']

# ----------------------------
# Split data
# ----------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ----------------------------
# Train RandomForest model
# ----------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# ----------------------------
# Predict & evaluate
# ----------------------------
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")

# ----------------------------
# Save trained model
# ----------------------------
joblib.dump(model, r"C:\study material\major_project\backend\trained_model.pkl")
print("Model saved as trained_model.pkl")

