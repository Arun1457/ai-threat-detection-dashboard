import pandas as pd
import random
from datetime import datetime
from datetime import timedelta

def generate_timestamps(n, start_date="2025-01-01", end_date="2025-10-15"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    return [start + (end - start) * random.random() for _ in range(n)]

n = 500

users = [f"user_{i}" for i in range(1, 51)]
auth_types = ["login", "logout", "failed_login", "password_change", "suspicious_login"]
sources = ["web_portal", "mobile_app", "ssh", "vpn"]

data = pd.DataFrame({
    "timestamp": generate_timestamps(n),
    "user_id": [random.choice(users) for _ in range(n)],
    "auth_action": [random.choice(auth_types) for _ in range(n)],
    "source": [random.choice(sources) for _ in range(n)],
    # a small percent labeled anomalous (simulate ground truth)
    "anomaly_flag": [random.choices([0,1], weights=[0.95,0.05])[0] for _ in range(n)]
})

# Save to data folder (relative path)
data.to_csv(r"C:\study material\major_project\data\auth_logs.csv", index=False)
print("Auth logs generated and saved to auth_logs.csv")
