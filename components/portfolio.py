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
        st.info("Portfolio is empty or database connection missing. Please check your configuration.")
        return

    # Group by Sector
    sectors = df['Sector'].unique()
    
    for sector in sectors:
        st.markdown(f"### 🏭 {sector}")
        sector_df = df[df['Sector'] == sector]
        
        # Display as a styled dataframe or custom cards
        # Using dataframe for density
        st.dataframe(
            sector_df[[
                "Ticker", "Name", "Recommendation", "Price", 
                "Date Added", "Short Term Plan", "Long Term Plan"
            ]],
            use_container_width=True,
            hide_index=True
        )
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
