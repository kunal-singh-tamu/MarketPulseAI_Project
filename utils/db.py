import os
import streamlit as st
from supabase import create_client, Client
import datetime

# Initialize Supabase Client
@st.cache_resource
def init_connection():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        return None
    return create_client(url, key)

def get_client():
    return init_connection()

def seed_default_portfolio(client):
    """
    Seeds the portfolio with default stocks if empty.
    """
    try:
        # Check if empty
        response = client.table("portfolio").select("id", count="exact").execute()
        if response.count == 0:
            default_data = [
                {
                    "ticker": "TSLA",
                    "company_name": "Tesla Inc.",
                    "sector": "Automotive",
                    "recommendation": "WATCH",
                    "price_at_analysis": 245.50,
                    "short_term_plan": "Monitor for breakout above $250.",
                    "long_term_plan": "Hold for EV market expansion.",
                    "created_at": datetime.datetime.now().isoformat()
                },
                {
                    "ticker": "MSFT",
                    "company_name": "Microsoft Corp.",
                    "sector": "Artificial Intelligence",
                    "recommendation": "BUY",
                    "price_at_analysis": 415.00,
                    "short_term_plan": "Accumulate on dips.",
                    "long_term_plan": "Long-term AI leader.",
                    "created_at": datetime.datetime.now().isoformat()
                },
                {
                    "ticker": "ORCL",
                    "company_name": "Oracle Corp.",
                    "sector": "Database/Cloud",
                    "recommendation": "BUY",
                    "price_at_analysis": 112.30,
                    "short_term_plan": "Buy for cloud growth.",
                    "long_term_plan": "Stable enterprise cash flow.",
                    "created_at": datetime.datetime.now().isoformat()
                }
            ]
            client.table("portfolio").insert(default_data).execute()
            return True
    except Exception as e:
        print(f"Seeding error: {e}")
        return False
    return False

def fetch_portfolio():
    """
    Fetches portfolio data from Supabase.
    """
    client = get_client()
    if not client:
        return []
    
    try:
        # Try to seed if empty (this is a simple check, might want to optimize in prod)
        seed_default_portfolio(client)
        
        response = client.table("portfolio").select("*").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"Database Error: {e}")
        return []

def save_position(data: dict):
    """
    Saves a position to Supabase.
    """
    client = get_client()
    if not client:
        st.error("Database connection not established. Check API keys.")
        return False
        
    try:
        client.table("portfolio").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Error saving to DB: {e}")
        return False
