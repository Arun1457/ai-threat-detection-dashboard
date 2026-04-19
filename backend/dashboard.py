# dashboard.py
from auth import login, logout
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
from io import BytesIO

st.set_page_config(page_title="Unified Threat Detection Dashboard", layout="wide")

# --- SESSION INIT ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# --- LOGIN FLOW ---
if not st.session_state['logged_in']:
    login()
    st.stop()

# --- AUTO REFRESH (every 5 seconds) ---
if 'last_refresh' not in st.session_state:
    st.session_state['last_refresh'] = time.time()

if time.time() - st.session_state['last_refresh'] > 5:
    st.session_state['last_refresh'] = time.time()
    st.rerun()

# Paths
PRED_CSV = "../data/predicted_combined_logs.csv"

st.title("AI-Driven Unified Threat Detection Dashboard")

st.sidebar.write(f"👤 Logged in as: {st.session_state.get('user', 'Unknown')}")

if st.sidebar.button("Logout"):
    logout()
    st.rerun()

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    # Ensure timestamp is datetime
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    return df

# Load dataset
# Load dataset
try:
    data = load_data(PRED_CSV)

except FileNotFoundError:
    st.error(f"Predictions file not found: {PRED_CSV}\nRun prediction script first.")
    st.stop()

# --- AI RISK FUNCTION ---
def assign_ai_risk_score(row):
    score = 0

    if row['severity'] == 'Critical':
        score += 50
    elif row['severity'] == 'High':
        score += 30
    elif row['severity'] == 'Medium':
        score += 15

    score += row.get('confidence', 0) * 50

    return min(score, 100)

# Apply AI scoring
data['ai_risk_score'] = data.apply(assign_ai_risk_score, axis=1)
from sklearn.ensemble import IsolationForest

def detect_anomalies(df):

    # Select numeric features
    features = []

    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            features.append(col)

    # Remove unwanted columns if present
    features = [f for f in features if f not in ['timestamp']]

    if len(features) == 0:
        return df

    model = IsolationForest(
        contamination=0.2,   # ↑ increase sensitivity
        random_state=42
    )

    df['anomaly_flag'] = model.fit_predict(df[features])

    df['anomaly_flag'] = df['anomaly_flag'].apply(
        lambda x: 'Anomaly' if x == -1 else 'Normal'
    )

    return df

# Sidebar: Filters
st.sidebar.header("Filters & Controls")

# Clear filters button
if 'clear_filters' not in st.session_state:
    st.session_state.clear_filters = False

if st.sidebar.button("Clear filters"):
    st.session_state.clear_filters = True

# Options
sources = data['source'].dropna().unique().tolist() if 'source' in data.columns else []
entities = data['entity'].dropna().unique().tolist() if 'entity' in data.columns else []
activities = data['activity'].dropna().unique().tolist() if 'activity' in data.columns else []

default_sources = sources
default_entities = entities
default_activities = activities

min_date = data['timestamp'].min().date() if 'timestamp' in data.columns else None
max_date = data['timestamp'].max().date() if 'timestamp' in data.columns else None

# Multiselect widgets
if st.session_state.clear_filters:
    selected_sources = st.sidebar.multiselect("Log Sources", sources, default_sources)
    selected_entities = st.sidebar.multiselect("Entities / Users", entities, default_entities)
    selected_activities = st.sidebar.multiselect("Activity / Action", activities, default_activities)
    st.session_state.clear_filters = False
else:
    selected_sources = st.sidebar.multiselect("Log Sources", sources, default_sources)
    selected_entities = st.sidebar.multiselect("Entities / Users", entities, default_entities)
    selected_activities = st.sidebar.multiselect("Activity / Action", activities, default_activities)

# Date widget
if min_date and max_date:
    date_range = st.sidebar.date_input("Date range", value=(min_date, max_date))
    if not date_range or len(date_range) != 2:
        date_range = (min_date, max_date)
else:
    date_range = (None, None)

# Apply filters
filtered = data.copy()
if 'source' in filtered.columns and selected_sources:
    filtered = filtered[filtered['source'].isin(selected_sources)]
if 'entity' in filtered.columns and selected_entities:
    filtered = filtered[filtered['entity'].isin(selected_entities)]
if 'activity' in filtered.columns and selected_activities:
    filtered = filtered[filtered['activity'].isin(selected_activities)]

# Date filtering
if 'timestamp' in filtered.columns and date_range[0] is not None and date_range[1] is not None:
    start = pd.to_datetime(date_range[0])
    end = pd.to_datetime(date_range[1]) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    filtered = filtered[(filtered['timestamp'] >= start) & (filtered['timestamp'] <= end)]

# Safety: ensure prediction column exists
pred_col = 'predicted_anomaly'
if pred_col not in filtered.columns or filtered[pred_col].sum() == 0:
    # fallback to anomaly_flag if predicted not present or all zeros
    pred_col = 'anomaly_flag' if 'anomaly_flag' in filtered.columns else None

# Convert to numeric
if pred_col:
    filtered[pred_col] = pd.to_numeric(filtered[pred_col], errors='coerce').fillna(0).astype(int)


# Summary KPIs
st.subheader("Summary Metrics")
col1, col2, col3, col4 = st.columns([1.2,1,1,1])

total_logs = len(filtered)
anomalies = filtered[pred_col].sum() if pred_col else 0
normal_logs = total_logs - anomalies

col1.metric("Total Logs", f"{total_logs:,}")
col2.metric("Anomalies Detected", f"{anomalies:,}")
col3.metric("Normal Logs", f"{normal_logs:,}")
percent = (anomalies/total_logs*100) if total_logs>0 else 0
col4.metric("Anomaly Rate", f"{percent:.2f}%")
# --- Critical Alerts Panel ---
if 'severity' in filtered.columns:
    critical_count = len(filtered[filtered['severity'] == 'Critical'])
    high_count = len(filtered[filtered['severity'] == 'High'])

    if critical_count > 0:
        st.error(f"🚨 {critical_count} Critical Threats Detected!")

    if high_count > 0:
        st.warning(f"⚠️ {high_count} High Severity Threats Detected!")

st.markdown("---")

# Table + download
st.subheader("Predicted Logs (filtered)")

if not filtered.empty:
    # Highlight anomalies in table
    def highlight_severity(row):
        if 'severity' not in row:
            return [''] * len(row)

        color_map = {
            'Critical': 'background-color: red',
            'High': 'background-color: orange',
            'Medium': 'background-color: yellow',
            'Low': 'background-color: lightgreen',
            'Normal': ''
        }

        color = color_map.get(row['severity'], '')
        return [color] * len(row)

    st.dataframe(
        filtered.reset_index(drop=True).style.apply(highlight_severity, axis=1),
        height=300
    )

else:
    st.info("No logs available for this selection.")
# --- SOAR Response Actions ---
st.markdown("---")
st.subheader("⚡ Response Actions")

# Show only High & Critical threats
alerts = filtered[filtered['severity'].isin(['High', 'Critical'])]

if alerts.empty:
    st.info("No high or critical threats for action.")
else:

    for i, row in alerts.head(10).iterrows():

        st.write(f"🚨 Threat from {row['entity']} | Severity: {row['severity']}")
        st.write(f"🤖 AI Risk Score: {row['ai_risk_score']:.1f}")
        st.write(f"🧠 Anomaly Status: {row['anomaly_flag']}")
        # --- AUTO AI RESPONSE ---
        if row['anomaly_flag'] == 'Anomaly':
            st.error(f"🚨 AI DETECTED ANOMALY: {row['entity']}")

        elif row['ai_risk_score'] > 75:
            st.error(f"🚫 AUTO-BLOCKED (AI): {row['entity']}")

        elif row['ai_risk_score'] > 50:
            st.warning(f"⚡ AI INVESTIGATING: {row['entity']}")

        elif row['ai_risk_score'] > 25:
            st.info(f"👁 Monitoring: {row['entity']}")

        else:
            st.success(f"✅ Normal activity: {row['entity']}")
        #---Buttons---
        col1, col2, col3 = st.columns(3)

        if col1.button(f"Block {row['entity']}", key=f"block_{i}"):
            st.success(f"✅ {row['entity']} blocked!")

        if col2.button(f"Ignore {i}", key=f"ignore_{i}"):
            st.info("Ignored")
        if col3.button(f"Investigate {i}", key=f"invest_{i}"):
            st.warning(f"🔍 Investigating {row['entity']}...")

            st.write("### 🔎 Threat Details")
            st.write(f"Entity: {row['entity']}")
            st.write(f"Source: {row['source']}")
            st.write(f"Activity: {row['activity']}")
            st.write(f"Resource: {row['resource']}")
            st.write(f"Confidence: {row['confidence']:.2f}")
            st.write(f"Severity: {row['severity']}")

        st.markdown("---")

# Download button
def convert_df_to_bytes(df):
    return df.to_csv(index=False).encode('utf-8')
csv_bytes = convert_df_to_bytes(filtered)
st.download_button("Download Filtered Logs (CSV)", data=csv_bytes, file_name="filtered_predicted_logs.csv", mime="text/csv")

st.markdown("---")
st.subheader("Visual Insights")

# Two-column charts
cht1, cht2 = st.columns(2)

with cht1:
    st.markdown("**Activity / Action vs Anomaly**")
    if not filtered.empty and 'activity' in filtered.columns:
        plt.figure(figsize=(8,4))
        sns.countplot(data=filtered, x='activity', hue=pred_col, palette='Set2')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(plt.gcf())
        plt.clf()
    else:
        st.info("No activity/action data available.")

with cht2:
    st.markdown("**Anomalies by Source**")
    if not filtered.empty and 'source' in filtered.columns:
        agg = filtered.groupby('source')[pred_col].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(6,3.5))
        agg.plot(kind='bar', ax=ax)
        ax.set_ylabel("Anomaly Count")
        ax.set_xlabel("Source")
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
        plt.clf()
    else:
        st.info("No source data available.")

# Timeline
st.markdown("**Anomalies Over Time**")
if not filtered.empty and 'timestamp' in filtered.columns:
    ts = filtered.set_index('timestamp').resample('D')[pred_col].sum()
    fig, ax = plt.subplots(figsize=(10,3))
    ts.plot(ax=ax)
    ax.set_ylabel("Anomalies (count/day)")
    ax.set_xlabel("Date")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.clf()
else:
    st.info("No timestamp data available.")

# Top entities
st.markdown("**Top Entities by Anomaly Count**")
if not filtered.empty and 'entity' in filtered.columns:
    top = filtered.groupby('entity')[pred_col].sum().sort_values(ascending=False).head(10)
    st.table(top.reset_index().rename(columns={pred_col: 'anomaly_count'}))
else:
    st.info("No entity data available.")

st.markdown("---")
st.caption("Dashboard built for demo / college project. Synthetic data used — adjust labels for production.")
