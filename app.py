import streamlit as st
import pandas as pd
from components import dashboard, news_feed, analysis, portfolio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(
    page_title="MarketPulseAI",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Financial Terminal Look
# Custom CSS for Dark Theme with Light Accents
st.markdown("""
<style>
    /* Main App Background - Dark Grey */
    .stApp {
        background-color: #262730;
        color: #FAFAFA;
    }
    
    /* Sidebar - Darker Grey */
    section[data-testid="stSidebar"] {
        background-color: #1E1E1E;
        color: #FAFAFA;
    }
    
    /* Sidebar Text Color Override */
    section[data-testid="stSidebar"] .stMarkdown, 
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p {
        color: #FAFAFA !important;
    }
    
    /* Card/Container Styling - Light Grey for Article Selection (Specific Request) */
    /* This targets st.container(border=True) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #E3E8EF;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #d1d5db;
    }
    
    /* Ensure text inside these light cards is dark */
    div[data-testid="stVerticalBlockBorderWrapper"] p,
    div[data-testid="stVerticalBlockBorderWrapper"] h1,
    div[data-testid="stVerticalBlockBorderWrapper"] h2,
    div[data-testid="stVerticalBlockBorderWrapper"] h3,
    div[data-testid="stVerticalBlockBorderWrapper"] div,
    div[data-testid="stVerticalBlockBorderWrapper"] span {
        color: #1c1e21 !important;
    }
    
    /* Buttons - Bright Blue */
    .stButton button {
        background-color: #1A73E8;
        color: white;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        box_shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        background-color: #1557b0;
        box_shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        transform: translateY(-1px);
    }
    
    /* Dataframes - Dark Mode Friendly */
    .stDataFrame {
        border: 1px solid #444;
        border-radius: 8px;
        background-color: #1E1E1E;
    }
    
    /* Headers - Lighter Blue for Dark Background */
    h1, h2, h3 {
        font-family: 'Inter', 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        color: #64B5F6; /* Lighter Blue */
        font-weight: 700;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #64B5F6;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = []
if 'step' not in st.session_state:
    st.session_state.step = 1 # 1: Dashboard, 2: News, 3: Analysis
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = None

def main():
    st.sidebar.title("MarketPulseAI 📈")
    st.sidebar.markdown("---")
    
    # Navigation
    view = st.sidebar.radio("Navigation", ["Dashboard", "Portfolio"])
    
    st.sidebar.markdown("---")
    st.sidebar.info("Powered by Gemini 2.5 Flash")
    
    if view == "Dashboard":
        if st.session_state.step == 1:
            dashboard.render_dashboard()
        elif st.session_state.step == 2:
            news_feed.render_news_feed()
        elif st.session_state.step == 3:
            analysis.render_analysis()
            
    elif view == "Portfolio":
        portfolio.render_portfolio()

if __name__ == "__main__":
    main()
