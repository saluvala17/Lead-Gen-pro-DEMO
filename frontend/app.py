import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("🏗️ ConstructFlow Pro")

# Feature: Lead Input with Urgency Calculation
with st.sidebar.form("new_lead"):
    st.header("Add New Lead")
    name = st.text_input("Project Name")
    budget = st.number_input("Budget ($)", min_value=0)
    days = st.slider("Days to Start", 1, 90, 30)
    if st.form_submit_button("Submit"):
        res = requests.post(f"{API_URL}/add-lead?name={name}&budget={budget}&days={days}")
        if res.status_code == 200:
            st.success("Lead added!")

# Display lead table
if st.button("Refresh Leads"):
    leads = requests.get(f"{API_URL}/leads").json()
    st.table(leads)