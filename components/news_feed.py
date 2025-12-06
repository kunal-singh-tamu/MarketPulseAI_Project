import pandas as pd
import streamlit as st
from utils import ai_engine

def render_news_feed():
    """
    Renders the news feed for the selected topic.
    Allows user to select articles and proceed to analysis.
    """
    topic = st.session_state.get("current_topic")
    if not topic:
        st.error("No topic selected.")
        if st.button("Back to Dashboard"):
            st.session_state.step = 1
            st.rerun()
        return

    st.markdown(f"## 📰 Latest News for: **{topic}**")
    
    # Fetch news if not already in session state or if topic changed
    # We use a separate key 'news_topic' to track which topic the current news belongs to
    if "fetched_news" not in st.session_state or st.session_state.get("news_topic") != topic:
        with st.spinner(f"Fetching latest news for {topic}..."):
            st.session_state.fetched_news = ai_engine.fetch_news(topic)
            st.session_state.news_topic = topic
            # Reset selection when new news is fetched
            st.session_state.selected_indices = [i for i in range(len(st.session_state.fetched_news))]

    news_items = st.session_state.fetched_news
    
    if not news_items:
        st.warning(f"No recent news found for {topic} (last 3 days).")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Use Mock Data"):
                st.session_state.fetched_news = ai_engine.MOCK_NEWS
                st.session_state.selected_indices = [i for i in range(len(ai_engine.MOCK_NEWS))]
                st.rerun()
        with col2:
            if st.button("Back to Dashboard"):
                st.session_state.step = 1
                st.rerun()
        return

    # Data Freshness Table
    st.markdown("### 📊 Data Freshness")
    try:
        freshness_data = []
        for item in news_items:
            freshness_data.append({
                "Source": item.get('source'),
                "Date": item.get('date'),
                "Headline": item.get('headline'),
                "Link": item.get('url') # Add URL for the link column
            })
        
        df = pd.DataFrame(freshness_data)
        if not df.empty:
            st.dataframe(
                df, 
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Link": st.column_config.LinkColumn(
                        "Article Link",
                        display_text="Read Article"
                    )
                }
            )
    except Exception as e:
        st.error(f"Error displaying freshness table: {e}")

    with st.form("news_selection_form"):
        st.markdown("### Select Articles for Analysis")
        st.markdown("Uncheck irrelevant articles to improve analysis quality.")
        
        selected_indices = []
        
        for i, item in enumerate(news_items):
            # Default to checked
            is_checked = st.checkbox(
                f"**{item['headline']}** - *{item['source']}* ({item['date']})",
                value=True,
                key=f"news_{i}",
                help=item['snippet']
            )
            st.caption(f"{item['snippet']}")
            st.markdown("---")
            
            if is_checked:
                selected_indices.append(i)
        
        submitted = st.form_submit_button("⚡ Process Analysis", type="primary")
        
        if submitted:
            if not selected_indices:
                st.error("Please select at least one article.")
            else:
                selected_articles = [news_items[i] for i in selected_indices]
                st.session_state.selected_articles = selected_articles
                st.session_state.step = 3 # Move to Analysis
                st.rerun()
