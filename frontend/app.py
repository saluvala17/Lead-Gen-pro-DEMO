import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load local .env file (only used for local development)
load_dotenv()

# The Backend URL is pulled from Railway's environment variables.
# It defaults to localhost if the variable isn't found.
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000").strip("/")

st.set_page_config(page_title="ConstructFlow Pro", page_icon="🏗️")
st.title("🏗️ ConstructFlow Pro")

# --- Sidebar: Add New Lead ---
with st.sidebar.form("new_lead"):
    st.header("Add New Lead")
    name = st.text_input("Project Name", placeholder="e.g. Skyline Apartments")
    budget = st.number_input("Budget ($)", min_value=0, step=500)
    days = st.slider("Days to Start", 1, 90, 30)
    
    if st.form_submit_button("Submit"):
        if not name:
            st.error("Please enter a project name.")
        else:
            try:
                # We use 'params' to safely encode URL parameters
                payload = {"name": name, "budget": budget, "days": days}
                res = requests.post(f"{API_URL}/add-lead", params=payload, timeout=10)
                
                if res.status_code == 200:
                    st.success(f"✅ Lead '{name}' added successfully!")
                else:
                    st.error(f"❌ Backend Error: {res.status_code}")
            except requests.exceptions.ConnectionError:
                st.error(f"📡 Connection Failed! The app is trying to connect to: {API_URL}. Check your BACKEND_URL in Railway.")

# --- Main Section: Display Leads ---
st.subheader("Current Sales Pipeline")

if st.button("🔄 Refresh Leads List"):
    try:
        res = requests.get(f"{API_URL}/leads", timeout=10)
        if res.status_code == 200:
            leads = res.json()
            if leads:
                st.table(leads)
            else:
                st.info("No leads found in the database yet.")
        else:
            st.error(f"Failed to fetch leads. Status: {res.status_code}")
    except Exception as e:
        st.error(f"Could not connect to database: {e}")