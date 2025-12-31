import os
from fastapi import FastAPI
from typing import Optional
from supabase import create_client
import sentry_sdk
from dotenv import load_dotenv

load_dotenv()
sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), traces_sample_rate=1.0)

app = FastAPI()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

@app.get("/leads")
def get_leads():
    # Fetches all rows from the 'jobs_lead_gen' table in Supabase
    return supabase.table("jobs_lead_gen").select("*").execute().data

@app.post("/add-lead")
def add_lead(name: str, budget: int, days: int, priority: Optional[str] = "normal"):
    # FEATURE: Lead Urgency Scoring
    urgency = "Warm"
    if budget > 15000 and days < 14: urgency = "🔥 High"
    elif days > 60: urgency = "❄️ Low"

    # Minimal priority validation: allow low/normal/high (case-insensitive)
    allowed = {"low", "normal", "high"}
    p = (priority or "normal").strip().lower()
    if p not in allowed:
        p = "normal"

    data = {"name": name, "budget": budget, "urgency": urgency, "priority": p}
    return supabase.table("jobs_lead_gen").insert(data).execute().data