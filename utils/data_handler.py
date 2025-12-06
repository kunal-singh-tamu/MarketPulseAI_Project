import pandas as pd
import streamlit as st
import datetime
from utils import db

def add_to_portfolio(stock_data: dict, source_topic: str):
    """
    Adds a stock to the database portfolio.
    stock_data expected keys: ticker, company_name, action, price
    """
    # Helper to safely convert price
    def _safe_float(val):
        try:
            if isinstance(val, (int, float)):
                return float(val)
            # Try to clean string
            clean_val = str(val).replace('$', '').replace(',', '').strip()
            return float(clean_val)
        except (ValueError, TypeError):
            return 0.0

    entry = {
        "ticker": stock_data.get("ticker"),
        "company_name": stock_data.get("company_name"),
        "sector": source_topic, # Using source topic as Sector
        "recommendation": stock_data.get("action"),
        "price_at_analysis": _safe_float(stock_data.get("price")),
        "short_term_plan": stock_data.get("short_term_plan", "N/A"),
        "long_term_plan": stock_data.get("long_term_plan", "N/A"),
        # created_at is handled by DB or default
    }
    
    success = db.save_position(entry)
    if success:
        st.success(f"Added {entry['ticker']} to Portfolio!")
        # Clear cache to refresh data on next load
        st.cache_data.clear()

def get_portfolio_dataframe() -> pd.DataFrame:
    """
    Returns the portfolio as a Pandas DataFrame from DB.
    """
    data = db.fetch_portfolio()
    
    if not data:
        # Return empty with correct columns
        return pd.DataFrame(columns=[
            "Ticker", "Name", "Sector", "Recommendation", 
            "Date Added", "Price", "Short Term Plan", "Long Term Plan"
        ])
    
    df = pd.DataFrame(data)
    
    # Rename columns to match UI expectations if needed, or adjust UI
    # DB columns: ticker, company_name, sector, recommendation, price_at_analysis, short_term_plan, long_term_plan, created_at
    
    df = df.rename(columns={
        "ticker": "Ticker",
        "company_name": "Name",
        "sector": "Sector",
        "recommendation": "Recommendation",
        "price_at_analysis": "Price",
        "short_term_plan": "Short Term Plan",
        "long_term_plan": "Long Term Plan"
    })
    
    # Format Date
    if 'created_at' in df.columns:
        df['Date Added'] = pd.to_datetime(df['created_at']).dt.strftime("%Y-%m-%d")
    else:
        df['Date Added'] = datetime.date.today().strftime("%Y-%m-%d")
        
    return df

def convert_df_to_csv(df: pd.DataFrame) -> str:
    """
    Converts DataFrame to CSV string for download.
    """
    return df.to_csv(index=False).encode('utf-8')
