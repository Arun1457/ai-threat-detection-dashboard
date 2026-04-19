import pandas as pd
import random
from datetime import datetime, timedelta

# Generate synthetic system logs
records = []
start_time = datetime.now() - timedelta(days=2)

system_components = ['CPU', 'Memory', 'Disk', 'Network', 'GPU']
event_types = ['Usage spike', 'Failure', 'Overheating', 'Restart', 'Update']

for i in range(500):  # generate 500 rows
    timestamp = start_time + timedelta(minutes=i * 5)
    component = random.choice(system_components)
    event = random.choice(event_types)
    severity = random.choice(['Low', 'Medium', 'High', 'Critical'])
    metric_value = round(random.uniform(20, 100), 2)

    records.append({
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'component': component,
        'event': event,
        'severity': severity,
        'metric_value': metric_value
    })

# Save to CSV
df = pd.DataFrame(records)
df.to_csv(r"C:\study material\major_project\data\system_logs.csv", index=False)
print("System logs generated and saved to system_logs.csv")
