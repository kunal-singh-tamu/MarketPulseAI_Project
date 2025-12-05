import os
import json
import datetime
import google.generativeai as genai
import streamlit as st
from typing import List, Dict, Any

# Mock Data for Fallback
MOCK_NEWS = [
    {
        "headline": "Tech Sector Rallies as AI Demand Surges",
        "source": "MarketWatch",
        "date": "2023-10-26",
        "snippet": "Major tech stocks are seeing significant gains today as earnings reports highlight insatiable demand for AI infrastructure."
    },
    {
        "headline": "Federal Reserve Signals Potential Rate Pause",
        "source": "Bloomberg",
        "date": "2023-10-25",
        "snippet": "Fed officials hint that rising bond yields may do the work of tightening for them, suggesting a pause in rate hikes."
    },
    {
        "headline": "Oil Prices Stabilize Amid Geopolitical Tensions",
        "source": "Reuters",
        "date": "2023-10-25",
        "snippet": "Crude oil futures are trading flat as traders weigh supply risks against global economic growth concerns."
    },
    {
        "headline": "New EV Regulations Proposed in EU",
        "source": "CNBC",
        "date": "2023-10-24",
        "snippet": "The European Union is considering stricter regulations on electric vehicle imports to protect domestic manufacturers."
    },
    {
        "headline": "Crypto Market Cap Reclaims $1 Trillion",
        "source": "CoinDesk",
        "date": "2023-10-26",
        "snippet": "Bitcoin's recent rally has pushed the total cryptocurrency market capitalization back above the psychological $1 trillion mark."
    }
]

MOCK_ANALYSIS = {
    "sentiment": "Positive",
    "summary": [
        "The market is showing resilience with tech leading the way, driven by AI optimism.",
        "Historically, Q4 rallies are common following a pause in rate hikes.",
        "Short-term outlook remains bullish as earnings beat expectations.",
        "Long-term growth is supported by the AI infrastructure supercycle.",
        "Key risks include persistent inflation and geopolitical instability."
    ],
    "recommendations": [
        {
            "ticker": "NVDA",
            "company_name": "NVIDIA Corp",
            "reasoning": "Dominant player in AI chips; direct beneficiary of the current AI infrastructure boom.",
            "action": "BUY",
            "price": "450.00",
            "short_term_plan": "Buy on pullbacks to $440 support level.",
            "long_term_plan": "Hold for 3-5 years as AI adoption matures."
        },
        {
            "ticker": "MSFT",
            "company_name": "Microsoft Corp",
            "reasoning": "Strong cloud growth and integration of AI across its product suite.",
            "action": "BUY",
            "price": "330.00",
            "short_term_plan": "Accumulate positions below $325.",
            "long_term_plan": "Core portfolio holding for steady compounding."
        },
        {
            "ticker": "GOOGL",
            "company_name": "Alphabet Inc.",
            "reasoning": "Attractive valuation relative to peers and improving ad revenue outlook.",
            "action": "WATCH",
            "price": "135.00",
            "short_term_plan": "Wait for breakout above $140.",
            "long_term_plan": "Re-evaluate if regulatory headwinds subside."
        },
        {
            "ticker": "XOM",
            "company_name": "Exxon Mobil",
            "reasoning": "Oil prices stabilizing provides a floor, but limited upside compared to tech.",
            "action": "WATCH",
            "price": "108.00",
            "short_term_plan": "Trade the range between $105 and $115.",
            "long_term_plan": "Use as a dividend income generator."
        },
        {
            "ticker": "TSLA",
            "company_name": "Tesla Inc.",
            "reasoning": "Regulatory headwinds in EU and margin compression concerns.",
            "action": "AVOID",
            "price": "210.00",
            "short_term_plan": "Avoid catching the falling knife.",
            "long_term_plan": "Wait for margin stabilization before entry."
        }
    ]
}

def configure_genai():
    """Configures the Gemini API client."""
    # Prioritize environment variable
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        try:
            if "GOOGLE_API_KEY" in st.secrets:
                api_key = st.secrets["GOOGLE_API_KEY"]
        except FileNotFoundError:
            pass # No secrets file found
        except Exception:
            pass
    
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

from utils import news_scraper

def fetch_news(topic: str) -> List[Dict[str, str]]:
    """
    Fetches news using DuckDuckGo news search.
    Returns empty list if search fails or returns no results (no automatic fallback).
    """
    print(f"Searching for {topic}...")
    # Use the new get_sector_news function
    real_news = news_scraper.get_sector_news(topic)
    
    if real_news:
        return real_news
    
    print("Search returned no results.")
    return []

import yfinance as yf

def analyze_news(selected_news: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Analyzes the selected news using Gemini to produce a structured report.
    Scrapes the full content of selected articles before sending to LLM.
    Fetches real-time prices for recommended stocks using yfinance.
    """
    if not configure_genai():
        # If configuration fails, we can either raise an error or return mock data.
        # The user requested explicit error handling, so let's raise an exception if API key is missing.
        # However, configure_genai returns False if no key. Let's check key explicitly or let the caller handle it.
        # But for now, let's stick to the plan: if configure_genai fails, it means no key.
        raise ValueError("Google API Key not found. Please check your .env file.")

    # Use gemini-2.5-flash as requested
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Scrape full text for selected articles
    articles_content = []
    for item in selected_news:
        url = item.get('url')
        headline = item.get('headline', 'No Headline')
        source = item.get('source', 'Unknown Source')
        snippet = item.get('snippet', '')
        
        content_block = f"Headline: {headline}\nSource: {source}\nSnippet: {snippet}"
        
        if url:
            print(f"Scraping {url}...")
            content = news_scraper.scrape_article(url)
            if content:
                # Limit content length but ensure we send enough
                content_block += f"\nFull Content: {content[:10000]}" 
        
        articles_content.append(content_block)

    news_text = "\n\n---\n\n".join(articles_content)
    
    # Log character count
    print(f"Sending {len(news_text)} characters of context to Gemini...")
    
    prompt = f"""
    Analyze the following financial news articles and provide a detailed market assessment.
    
    News Context:
    {news_text}
    
    Output must be a valid JSON object with the following schema:
    {{
        "sentiment": "Positive" | "Negative" | "Neutral",
        "summary": [
            "Bullet point 1: Overall Market Sentiment",
            "Bullet point 2: Historical Context/Past Effect",
            "Bullet point 3: Short-term Outlook",
            "Bullet point 4: Long-term Outlook",
            "Bullet point 5: Key Risks/Opportunities"
        ],
        "recommendations": [
            {{
                "ticker": "Stock Ticker",
                "company_name": "Company Name",
                "reasoning": "Brief reasoning based on news.",
                "action": "BUY" | "SELL" | "WATCH" | "AVOID",
                "price": "Estimated Current Price",
                "short_term_plan": "Specific short-term action (e.g., Buy on dip, Sell calls)",
                "long_term_plan": "Specific long-term strategy (e.g., Hold for 5 years, Exit on bounce)"
            }}
        ]
    }}
    Provide exactly 5 recommendations.
    """
    
    response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
    
    text = response.text
    # Clean up json markdown if present
    if text.startswith("```json"):
        text = text[7:-3]
    elif text.startswith("```"):
        text = text[3:-3]
        
    analysis_data = json.loads(text)
    
    # Post-processing: Fetch Real-Time Prices
    if "recommendations" in analysis_data:
        print("Fetching real-time prices...")
        for rec in analysis_data["recommendations"]:
            ticker = rec.get("ticker")
            if ticker:
                try:
                    # Use fast_info for latest price
                    stock = yf.Ticker(ticker)
                    # fast_info is generally faster than history
                    # 'last_price' might be available, or 'regularMarketPrice' depending on yfinance version
                    # Let's try fast_info first, then history
                    price = None
                    if hasattr(stock, 'fast_info'):
                         price = stock.fast_info.get('last_price')
                    
                    if price is None:
                        # Fallback to history
                        hist = stock.history(period="1d")
                        if not hist.empty:
                            price = hist['Close'].iloc[-1]
                            
                    if price:
                        rec["price"] = f"{price:.2f}"
                        print(f"Updated price for {ticker}: {price:.2f}")
                    else:
                        rec["price"] = f"{rec.get('price')} (Approx)"
                        
                except Exception as e:
                    print(f"Could not fetch price for {ticker}: {e}")
                    rec["price"] = f"{rec.get('price')} (Approx)"

    return analysis_data
