from duckduckgo_search import DDGS
import trafilatura
from typing import List, Dict
from datetime import datetime, timedelta
import dateutil.parser

def get_sector_news(topic: str, max_results: int = 10) -> List[Dict[str, str]]:
    """
    Fetches news articles about the topic using DuckDuckGo News search.
    Filters out articles older than 3 days.
    """
    results = []
    cutoff_date = datetime.now() - timedelta(days=3)
    
    try:
        with DDGS() as ddgs:
            # Search for news from the last week ('w') to ensure we get enough candidates to filter
            news_gen = ddgs.news(
                keywords=f"{topic} stock market",
                region="us-en",
                timelimit="w", 
                max_results=max_results * 2 # Fetch more to allow for filtering
            )
            
            for r in news_gen:
                if len(results) >= max_results:
                    break
                    
                article_date_str = r.get('date')
                if article_date_str:
                    try:
                        # Parse date string to datetime object
                        article_date = dateutil.parser.parse(article_date_str)
                        # Remove timezone info for comparison if needed, or ensure both are aware
                        if article_date.tzinfo is not None:
                             article_date = article_date.replace(tzinfo=None)
                        
                        if article_date >= cutoff_date:
                            results.append({
                                "headline": r.get('title'),
                                "source": r.get('source'),
                                "date": article_date_str,
                                "url": r.get('url'),
                                "snippet": r.get('body')
                            })
                    except Exception as e:
                        # If date parsing fails, we skip or include based on preference. 
                        # Here we include it but log warning, or just skip. 
                        # Let's skip to be safe about "freshness".
                        continue
                
    except Exception as e:
        print(f"Error searching DuckDuckGo: {e}")
        return []

    return results

def scrape_article(url: str) -> str:
    """
    Downloads and extracts the main text from a URL.
    """
    try:
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            text = trafilatura.extract(downloaded)
            return text if text else ""
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    
    return ""
