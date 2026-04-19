import pandas as pd
import numpy as np

print("📂 Loading combined logs...")
# Load the combined logs (IoT, Network, Cloud, Auth, System)
data = pd.read_csv(r"C:\study material\major_project\data\combined_logs.csv")
print(f"✅ Loaded {len(data)} rows and {len(data.columns)} columns")

# -------------------
# Handle missing values
# -------------------
print("⚠️ Handling missing values...")
data.fillna("Unknown", inplace=True)

# -------------------
# Convert timestamp to datetime
# -------------------
data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')

# -------------------
# Encode all categorical columns
# -------------------
categorical_cols = ['source', 'entity', 'activity', 'resource', 'destination', 'protocol']
print("🔠 Encoding categorical columns...")
for col in categorical_cols:
    if col in data.columns:
        data[col] = data[col].astype('category').cat.codes
print("✅ Encoding completed!")

# -------------------
# Ensure anomaly_flag exists
# -------------------
if 'anomaly_flag' not in data.columns:
    print("⚠️ 'anomaly_flag' column not found! Creating synthetic target for testing (0/1 random values).")
    data['anomaly_flag'] = np.random.randint(0, 2, size=len(data))

# -------------------
# Save cleaned data
# -------------------
output_file = r"C:\study material\major_project\data\cleaned_combined_logs.csv"
data.to_csv(output_file, index=False)
print(f"✅ Combined logs cleaned and saved to {output_file}")
