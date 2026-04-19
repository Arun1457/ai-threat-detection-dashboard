import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Helper function to generate timestamps
def generate_timestamps(n, start_date="2025-01-01", end_date="2025-10-15"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return [start + (end - start) * random.random() for _ in range(n)]

# 1. IoT Device Logs
n_iot = 500
iot_data = pd.DataFrame({
    "timestamp": generate_timestamps(n_iot),
    "device_id": [f"device_{random.randint(1,20)}" for _ in range(n_iot)],
    "activity_type": [random.choice(["file_access","network_access","cloud_download"]) for _ in range(n_iot)],
    "resource_accessed": [random.choice(["database","server1","cloud_bucket1","cloud_bucket2"]) for _ in range(n_iot)],
    "anomaly_flag": [random.choices([0,1], weights=[0.95,0.05])[0] for _ in range(n_iot)]
})
iot_data.to_csv("iot_logs.csv", index=False)
print("IoT logs generated.")

# 2. Network Traffic Logs
n_net = 500
network_data = pd.DataFrame({
    "timestamp": generate_timestamps(n_net),
    "src_ip": [f"192.168.{random.randint(0,255)}.{random.randint(1,254)}" for _ in range(n_net)],
    "dest_ip": [f"10.0.{random.randint(0,255)}.{random.randint(1,254)}" for _ in range(n_net)],
    "port": [random.choice([22,80,443,8080]) for _ in range(n_net)],
    "protocol": [random.choice(["TCP","UDP","ICMP"]) for _ in range(n_net)],
    "anomaly_flag": [random.choices([0,1], weights=[0.97,0.03])[0] for _ in range(n_net)]
})
network_data.to_csv("network_logs.csv", index=False)
print("Network logs generated.")

# 3. Cloud Logs
n_cloud = 500
cloud_data = pd.DataFrame({
    "timestamp": generate_timestamps(n_cloud),
    "user_id": [f"user_{random.randint(1,50)}" for _ in range(n_cloud)],
    "action": [random.choice(["login","upload","download","delete"]) for _ in range(n_cloud)],
    "resource": [random.choice(["s3_bucket1","s3_bucket2","db_server","vm_instance"]) for _ in range(n_cloud)],
    "anomaly_flag": [random.choices([0,1], weights=[0.96,0.04])[0] for _ in range(n_cloud)]
})
cloud_data.to_csv("cloud_logs.csv", index=False)
print("Cloud logs generated.")
