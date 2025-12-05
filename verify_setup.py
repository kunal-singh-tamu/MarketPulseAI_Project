import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    print("Checking imports...")
    from utils import ai_engine, data_handler
    from components import dashboard, news_feed, analysis, portfolio
    print("Imports successful.")

    print("Checking AI Engine Mock Data...")
    # We now test the scraper if possible, but for verification script we might want to stick to basic checks
    # Let's try to import the scraper
    from utils import news_scraper
    print("News Scraper import successful.")
    
    # Test search (lightweight)
    try:
        print("Testing Yahoo Finance Search...")
        results = news_scraper.search_yahoo_finance("Apple", max_results=1)
        if results:
            print(f"Search successful. Found: {results[0]['headline']}")
        else:
            print("Search returned no results (could be network/rate limit).")
    except Exception as e:
        print(f"Search failed: {e}")

    news = ai_engine.fetch_news("Test Topic")
    if len(news) > 0:
        print(f"Fetch News successful. Got {len(news)} items.")
    else:
        print("Fetch News failed.")

    analysis_result = ai_engine.analyze_news(news)
    if "sentiment" in analysis_result:
        print(f"Analysis successful. Sentiment: {analysis_result['sentiment']}")
    else:
        print("Analysis failed.")

    print("Checking Data Handler...")
    data_handler.add_to_portfolio({"ticker": "TEST", "company_name": "Test Co", "action": "BUY", "price": "100"}, "Test Topic")
    # Note: st.session_state won't work here without streamlit context, but the function logic can be checked if we mock st.session_state or just rely on the import check.
    # Since data_handler uses st.session_state directly, it will fail if run as pure python script.
    # So we skip execution of data_handler functions that depend on st.session_state.
    print("Data Handler import successful.")

    print("Verification Complete.")

except Exception as e:
    print(f"Verification Failed: {e}")
