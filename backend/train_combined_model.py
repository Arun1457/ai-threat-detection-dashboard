import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# --- Paths ---
DATA_PATH = r"C:\study material\major_project\data\cleaned_combined_logs.csv"
MODEL_PATH = r"C:\study material\major_project\backend\combined_model.pkl"

# --- Load cleaned data ---
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ File not found: {DATA_PATH}")

print("📂 Loading cleaned logs...")
data = pd.read_csv(DATA_PATH)
print(f"✅ Loaded {data.shape[0]} rows and {data.shape[1]} columns")

# --- Encode categorical (non-numeric) columns ---
print("🔠 Encoding categorical columns...")
for col in data.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col].astype(str))
print("✅ Encoding completed!")

# --- Check or create target column ---
if 'anomaly_flag' not in data.columns:
    print("⚠️ 'anomaly_flag' column not found! Creating synthetic target for testing (0/1 random values).")
    np.random.seed(42)
    data['anomaly_flag'] = np.random.randint(0, 2, size=len(data))

# --- Split features and target ---
X = data.drop(['timestamp', 'anomaly_flag'], axis=1, errors='ignore')
y = data['anomaly_flag']

# --- Train/Test split ---
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Train Random Forest model ---
print("🚀 Training model...")
model = RandomForestClassifier(random_state=42, n_estimators=100)
model.fit(X_train, y_train)
print("✅ Model trained successfully!")

# --- Evaluate model ---
accuracy = model.score(X_test, y_test)
print(f"📊 Model Accuracy: {accuracy * 100:.2f}%")

# --- Save trained model ---
joblib.dump(model, MODEL_PATH)
print(f"💾 Model saved to: {MODEL_PATH}")
