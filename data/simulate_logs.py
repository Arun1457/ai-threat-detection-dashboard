# simulate_logs.py
import pandas as pd
import random
from datetime import datetime, timedelta

# Number of sample logs
NUM_LOGS = 500

# Sample devices / users
devices = [f'device_{i}' for i in range(1, 21)]
activities = ['login', 'logout', 'file_access', 'network_access', 'cloud_upload', 'cloud_download']
resources = ['server1', 'server2', 'database', 'cloud_bucket1', 'cloud_bucket2']

# Generate random timestamps
def random_date(start, end):
    delta = end - start
    random_sec = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=random_sec)

# Create data
logs = []
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()

for _ in range(NUM_LOGS):
    log = {
        'timestamp': random_date(start_date, end_date).strftime("%Y-%m-%d %H:%M:%S"),
        'device_id': random.choice(devices),
        'activity_type': random.choice(activities),
        'resource_accessed': random.choice(resources),
        'anomaly_flag': random.choices([0, 1], weights=[90, 10])[0]  # 10% malicious
    }
    logs.append(log)

# Save to CSV
df = pd.DataFrame(logs)
df.to_csv('logs.csv', index=False)
print("Sample logs generated and saved to logs.csv")

