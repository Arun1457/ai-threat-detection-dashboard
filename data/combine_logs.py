import pandas as pd
import os

# Define file paths
base_path = r"C:\study material\major_project\data"

iot_path = os.path.join(base_path, "iot_logs.csv")
network_path = os.path.join(base_path, "network_logs.csv")
cloud_path = os.path.join(base_path, "cloud_logs.csv")
auth_path = os.path.join(base_path, "auth_logs.csv")
system_path = os.path.join(base_path, "system_logs.csv")

# Load available logs safely
def load_csv(path, source_name):
    if os.path.exists(path):
        df = pd.read_csv(path)
        df['source'] = source_name
        print(f"✅ Loaded {source_name} logs ({len(df)} rows)")
        return df
    else:
        print(f"⚠️ Missing file: {source_name}")
        return pd.DataFrame()

# Load each log
iot_logs = load_csv(iot_path, 'IoT')
network_logs = load_csv(network_path, 'Network')
cloud_logs = load_csv(cloud_path, 'Cloud')
auth_logs = load_csv(auth_path, 'Auth')
system_logs = load_csv(system_path, 'System')

# Standardize and rename columns
def standardize_columns(df, rename_dict):
    for old, new in rename_dict.items():
        if old in df.columns:
            df.rename(columns={old: new}, inplace=True)
    return df

# Apply renaming
iot_logs = standardize_columns(iot_logs, {
    'device_id': 'entity', 'activity_type': 'activity', 'resource_accessed': 'resource'
})
network_logs = standardize_columns(network_logs, {
    'src_ip': 'entity', 'dest_ip': 'destination', 'protocol': 'protocol', 'port': 'port'
})
cloud_logs = standardize_columns(cloud_logs, {
    'user_id': 'entity', 'action': 'activity', 'resource': 'resource'
})
auth_logs = standardize_columns(auth_logs, {
    'user_id': 'entity', 'action': 'activity', 'status': 'resource'
})
system_logs = standardize_columns(system_logs, {
    'process_name': 'entity', 'activity_type': 'activity', 'cpu_usage': 'resource'
})

# List of all logs
all_logs = [iot_logs, network_logs, cloud_logs, auth_logs, system_logs]

# Ensure uniform columns
for df in all_logs:
    for col in ['destination', 'port', 'protocol', 'anomaly_flag']:
        if col not in df.columns:
            df[col] = None

# Merge all logs
combined_logs = pd.concat(all_logs, ignore_index=True, sort=False)

# Arrange consistent column order
columns_order = ['timestamp', 'source', 'entity', 'activity', 'resource', 'destination', 'port', 'protocol', 'anomaly_flag']
combined_logs = combined_logs[[c for c in columns_order if c in combined_logs.columns]]

# Convert timestamp
combined_logs['timestamp'] = pd.to_datetime(combined_logs['timestamp'], errors='coerce')

# Save final combined file
output_path = os.path.join(base_path, "combined_logs.csv")
combined_logs.to_csv(output_path, index=False)
print(f"\n✅ Combined logs saved successfully to {output_path}")
