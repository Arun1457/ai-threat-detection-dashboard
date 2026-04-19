# auth.py

import streamlit as st

# --- User Credentials ---
USERS = {
    "Arun": "1457",
    "Mrunali": "2004",
    "Dina": "0000",
    "Pranjal": "1234"
}

# --- Login Function ---
def login():
    st.title("🔐 Enterprise Threat Detection Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state['logged_in'] = True
            st.session_state['user'] = username
            st.success(f"Welcome, {username} 👋")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# --- Logout Function ---
def logout():
    st.session_state['logged_in'] = False
    st.session_state['user'] = None