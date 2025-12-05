import pandas as pd
import streamlit as st
import datetime

def add_to_portfolio(stock_data: dict, source_topic: str):
    """
    Adds a stock to the session state portfolio.
    stock_data expected keys: ticker, company_name, action, price
    """
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = []
    
    entry = {
        "Ticker": stock_data.get("ticker"),
        "Name": stock_data.get("company_name"),
        "Recommendation": stock_data.get("action"),
        "Date Added": datetime.date.today().strftime("%Y-%m-%d"),
        "Price at Analysis": stock_data.get("price"),
        "Source Topic": source_topic,
        "Short Term Plan": stock_data.get("short_term_plan", "N/A"),
        "Long Term Plan": stock_data.get("long_term_plan", "N/A")
    }
    
    # Check for duplicates (optional, but good UX)
    # For now, we allow multiples as they might be from different dates/topics
    st.session_state.portfolio.append(entry)

def get_portfolio_dataframe() -> pd.DataFrame:
    """
    Returns the portfolio as a Pandas DataFrame.
    """
    if 'portfolio' not in st.session_state or not st.session_state.portfolio:
        return pd.DataFrame(columns=["Ticker", "Name", "Recommendation", "Date Added", "Price at Analysis", "Source Topic", "Short Term Plan", "Long Term Plan"])
    
    return pd.DataFrame(st.session_state.portfolio)

def convert_df_to_csv(df: pd.DataFrame) -> str:
    """
    Converts DataFrame to CSV string for download.
    """
    return df.to_csv(index=False).encode('utf-8')
