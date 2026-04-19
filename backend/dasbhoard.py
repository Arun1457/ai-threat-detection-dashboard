import streamlit as st
import pandas as pd

# Load predicted logs
data = pd.read_csv(r"C:\study material\major_project\data\predicted_logs.csv")

st.title("IoT Device Logs Dashboard")

st.subheader("Predicted Logs")
st.dataframe(data)

# Basic stats
st.subheader("Summary")
st.write("Total logs:", len(data))
st.write("Anomalies detected:", data['anomaly_flag'].sum())
