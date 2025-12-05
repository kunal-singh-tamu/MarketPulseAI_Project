import streamlit as st

def render_dashboard():
    """
    Renders the main dashboard with Trending Topics and Search.
    Updates st.session_state.current_topic and st.session_state.step upon selection.
    """
    st.markdown("## Market Pulse Dashboard")
    st.markdown("Select a trending sector or search for a specific ticker/topic.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 Trending Sectors")
        trending_topics = [
            "Artificial Intelligence",
            "Green Energy",
            "Cryptocurrency",
            "Biotech",
            "Semiconductors"
        ]
        
        for topic in trending_topics:
            if st.button(f"Analyze {topic}", key=f"btn_{topic}", use_container_width=True):
                st.session_state.current_topic = topic
                st.session_state.step = 2 # Move to News Ingestion
                st.rerun()
                
    with col2:
        st.subheader("🔍 Deep Dive")
        st.markdown("Enter a stock ticker (e.g., NVDA) or industry.")
        
        search_query = st.text_input("Search Topic", placeholder="Enter ticker or topic...")
        
        if st.button("Start Analysis", key="search_btn", use_container_width=True):
            if search_query:
                st.session_state.current_topic = search_query
                st.session_state.step = 2 # Move to News Ingestion
                st.rerun()
            else:
                st.warning("Please enter a topic to search.")
