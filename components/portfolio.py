import streamlit as st
import datetime
from utils import data_handler

def render_portfolio():
    """
    Renders the portfolio page.
    Displays Long and Short positions in separate tables.
    Allows CSV export.
    """
    st.markdown("## 💼 My Portfolio")
    
    df = data_handler.get_portfolio_dataframe()
    
    if df.empty:
        st.info("Your portfolio is empty. Go to the Dashboard to analyze stocks and add them here.")
        return

    # Split into Long and Short
    # Long: BUY, WATCH
    # Short: SELL, AVOID
    
    long_mask = df['Recommendation'].str.upper().isin(['BUY', 'WATCH'])
    short_mask = df['Recommendation'].str.upper().isin(['SELL', 'AVOID'])
    
    long_df = df[long_mask]
    short_df = df[short_mask]
    
    st.subheader("📈 Long Positions (Buy/Watch)")
    if not long_df.empty:
        st.dataframe(long_df, use_container_width=True, hide_index=True)
    else:
        st.caption("No long positions added.")
        
    st.subheader("📉 Short/Risk Positions (Sell/Avoid)")
    if not short_df.empty:
        st.dataframe(short_df, use_container_width=True, hide_index=True)
    else:
        st.caption("No short positions added.")
        
    st.markdown("---")
    
    # Export
    csv = data_handler.convert_df_to_csv(df)
    filename = f"portfolio_{datetime.date.today().strftime('%Y-%m-%d')}.csv"
    
    st.download_button(
        label="📥 Download Portfolio (CSV)",
        data=csv,
        file_name=filename,
        mime="text/csv",
    )
