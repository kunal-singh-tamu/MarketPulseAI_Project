import streamlit as st
from utils import ai_engine, data_handler

def render_analysis():
    """
    Renders the analysis report.
    Displays sentiment, summary, and stock recommendations.
    Allows adding stocks to portfolio.
    """
    selected_articles = st.session_state.get("selected_articles")
    topic = st.session_state.get("current_topic")
    
    if not selected_articles:
        st.error("No articles selected for analysis.")
        if st.button("Back"):
            st.session_state.step = 2
            st.rerun()
        return

    # Run analysis if not already done for this selection
    # We track 'analysis_topic' to know if we need to re-run
    if "analysis_result" not in st.session_state or st.session_state.get("analysis_topic") != topic:
        with st.spinner("Analyzing market sentiment and generating recommendations..."):
            try:
                st.session_state.analysis_result = ai_engine.analyze_news(selected_articles)
                st.session_state.analysis_topic = topic
            except Exception as e:
                st.error(f"Analysis Failed: {str(e)}")
                st.warning("⚠️ API Call Failed. Showing Fallback/Mock Data for debugging.")
                st.session_state.analysis_result = ai_engine.MOCK_ANALYSIS
                st.session_state.analysis_topic = topic

    result = st.session_state.analysis_result
    
    # Header
    st.markdown(f"## 📊 Market Analysis: **{topic}**")
    
    # Sentiment Banner
    sentiment = result.get("sentiment", "Neutral")
    color_map = {
        "Positive": "green",
        "Negative": "red",
        "Neutral": "gray"
    }
    color = color_map.get(sentiment, "gray")
    
    st.markdown(f"""
    <div style="background-color: rgba({0 if color=='red' else 0}, {128 if color=='green' else 0}, 0, 0.2); 
                padding: 15px; border-radius: 10px; border-left: 5px solid {color}; margin-bottom: 20px;">
        <h3 style="margin:0; color: {color};">Market Sentiment: {sentiment.upper()}</h3>
    </div>
    """, unsafe_allow_html=True)

    # Detailed Summary
    summary_points = result.get("summary", [])
    if isinstance(summary_points, list):
        st.subheader("📝 Executive Summary")
        for point in summary_points:
            st.markdown(f"- {point}")
    else:
        st.markdown(f"<p style='margin-top: 10px; font-size: 1.1em;'>{result.get('summary')}</p>", unsafe_allow_html=True)
    
    # Recommendations
    st.subheader("🎯 Stock Recommendations")
    
    recs = result.get("recommendations", [])
    
    if not recs:
        st.info("No specific stock recommendations generated.")
        return

    # Display cards
    cols = st.columns(len(recs) if len(recs) <= 3 else 3)
    
    for i, stock in enumerate(recs):
        # Wrap around columns
        col = cols[i % 3]
        
        with col:
            with st.container(border=True):
                st.markdown(f"### {stock.get('ticker')}")
                st.caption(stock.get('company_name'))
                
                action = stock.get('action', 'WATCH').upper()
                action_color = "green" if action in ["BUY", "WATCH"] else "red"
                
                st.markdown(f"**Action:** <span style='color:{action_color}'>{action}</span>", unsafe_allow_html=True)
                st.markdown(f"**Est. Price:** ${stock.get('price')}")
                st.markdown(f"*{stock.get('reasoning')}*")
                
                with st.expander("Strategy Details"):
                    st.markdown(f"**Short Term:** {stock.get('short_term_plan', 'N/A')}")
                    st.markdown(f"**Long Term:** {stock.get('long_term_plan', 'N/A')}")
                
                # Add to Portfolio Button
                # Use a unique key for each button
                btn_key = f"add_{stock.get('ticker')}_{i}"
                
                if st.button("➕ Add to Portfolio", key=btn_key):
                    data_handler.add_to_portfolio(stock, topic)
                    st.toast(f"Added {stock.get('ticker')} to Portfolio!", icon="✅")
    
    st.markdown("---")
    if st.button("Start New Analysis"):
        st.session_state.step = 1
        st.session_state.current_topic = None
        st.rerun()
