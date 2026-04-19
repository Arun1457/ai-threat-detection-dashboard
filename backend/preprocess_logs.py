import pandas as pd

# ----------------------------
# Load individual log files
# ----------------------------
iot_data = pd.read_csv(r"C:\study material\major_project\data\iot_logs.csv")
network_data = pd.read_csv(r"C:\study material\major_project\data\network_logs.csv")
cloud_data = pd.read_csv(r"C:\study material\major_project\data\cloud_logs.csv")

# ----------------------------
# Standardize columns for merging
# ----------------------------
# For IoT logs
iot_data = iot_data.rename(columns={
    "resource_accessed": "resource",
    "activity_type": "activity"
})
iot_data['source'] = 'IoT'
iot_data['user_or_device'] = iot_data['device_id']
iot_data = iot_data[['timestamp', 'source', 'user_or_device', 'activity', 'resource', 'anomaly_flag']]

# For Network logs
network_data = network_data.rename(columns={
    "src_ip": "user_or_device",
    "dest_ip": "resource",
    "protocol": "activity"
})
network_data['source'] = 'Network'
network_data = network_data[['timestamp', 'source', 'user_or_device', 'activity', 'resource', 'anomaly_flag']]

# For Cloud logs
cloud_data = cloud_data.rename(columns={
    "user_id": "user_or_device",
    "action": "activity",
    "resource": "resource"
})
cloud_data['source'] = 'Cloud'
cloud_data = cloud_data[['timestamp', 'source', 'user_or_device', 'activity', 'resource', 'anomaly_flag']]

# ----------------------------
# Combine all logs
# ----------------------------
combined_data = pd.concat([iot_data, network_data, cloud_data], ignore_index=True)

# ----------------------------
# Handle missing values (if any)
# ----------------------------
combined_data.fillna("Unknown", inplace=True)

# ----------------------------
# Convert timestamp to datetime
# ----------------------------
combined_data['timestamp'] = pd.to_datetime(combined_data['timestamp'])

# ----------------------------
# Save cleaned data
# ----------------------------
combined_data.to_csv(r"C:\study material\major_project\data\cleaned_logs.csv", index=False)
print("Combined and cleaned logs saved as cleaned_logs.csv")
