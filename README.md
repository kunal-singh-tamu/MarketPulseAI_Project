# MarketPulseAI

**Live Demo:** https://market-pulse-ai.streamlit.app/

MarketPulseAI is a financial intelligence tool designed to aggregate real-time market news, perform sentiment analysis using advanced Large Language Models (LLMs), and provide actionable stock recommendations. It serves as a personal research assistant for investors, helping them cut through the noise of daily financial news.
<img width="1611" height="828" alt="Screenshot 2025-12-06 at 9 41 12 PM" src="https://github.com/user-attachments/assets/346a50bf-dc65-4350-b96f-20142281a419" />


## Features & Functionality

### 1. Real-Time News Aggregation
*   **Functionality**: Fetches the latest financial news articles from the web based on user-selected sectors (e.g., AI, Green Energy) or specific stock tickers.
*   **Utility**: Ensures users are analyzing the most current market data, filtering out outdated information (older than 3 days) to maintain relevance.

### 2. AI-Powered Sentiment Analysis
*   **Functionality**: Uses Google's Gemini 2.5 Flash model to read and analyze the content of fetched news articles.
*   **Utility**: Converts raw text into structured insights, providing a sentiment score (Bullish/Bearish/Neutral), a concise summary, and specific investment opportunities.

### 3. Strategic Recommendations
*   **Functionality**: Generates detailed short-term and long-term trading plans for identified stocks.
*   **Utility**: Moves beyond simple news summaries by offering concrete actionable advice, such as entry points, risk management strategies, and growth outlooks.

### 4. Portfolio Management
*   **Functionality**: Allows users to save promising stocks to a persistent portfolio, grouped by sector. It tracks the price at the time of analysis and the specific strategy for each position.
*   **Utility**: Helps users organize their investment ideas and track the performance of their research over time.

### 5. Live Market Data
*   **Functionality**: Integrates with Yahoo Finance to display real-time stock prices alongside the AI analysis.
*   **Utility**: Provides immediate context on valuation, allowing users to see if a recommended stock is currently trading at a favorable price.

## Technology Stack

*   **Frontend**: Streamlit (Python-based web framework)
*   **LLM Integration**: Google Gemini 2.5 Flash (via `google-generativeai`)
*   **Database**: Supabase (PostgreSQL) for persistent portfolio storage
*   **Market Data**: `yfinance` for real-time stock pricing
*   **Search & Scraping**: `duckduckgo-search` for finding articles and `trafilatura` for extracting content
*   **Data Processing**: Pandas for data manipulation and structure

## Setup & Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/kunal-singh-tamu/MarketPulseAI_Project.git
    cd MarketPulseAI_Project
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration**
    Create a `.env` file in the root directory with the following keys:
    ```bash
    GOOGLE_API_KEY=your_gemini_api_key
    SUPABASE_URL=your_supabase_project_url
    SUPABASE_KEY=your_supabase_anon_key
    ```

4.  **Run the Application**
    ```bash
    streamlit run app.py
    ```
