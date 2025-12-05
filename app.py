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
st.markdown("""
<style>
    /* Dark Theme adjustments */
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Monospace for data */
    .stDataFrame, .stTable {
        font-family: 'Courier New', monospace;
    }
    
    /* Button styling */
    .stButton button {
        border-radius: 0px;
        font-weight: bold;
        border: 1px solid #444;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
    }
    
    /* Card styling */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background-color: #161b22;
        border-radius: 5px;
        padding: 10px;
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
    st.sidebar.info("Powered by Gemini 1.5 Flash")
    
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
