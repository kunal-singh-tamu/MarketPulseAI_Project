# Stable Build Notes

**Date:** 2025-12-05
**Git Commit:** `34657567806eeee8a07bd5903e72d13643b4385a`

## Status
This version represents a stable, working implementation of the MarketPulseAI application. All core integrations are functional.

## Verified Features
1.  **Real-Time News**:
    - Source: DuckDuckGo News Search
    - Filter: Articles older than 3 days are discarded.
    - Fallback: UI prompts user to use mock data if no recent news is found.
2.  **AI Analysis**:
    - Model: `gemini-2.5-flash`
    - Input: Full article text (scraped via `trafilatura`) + Source + Snippet.
    - Output: Structured JSON with Sentiment, Summary, and 5 Recommendations.
3.  **Real-Time Pricing**:
    - Integration: `yfinance`
    - Logic: Post-processes LLM recommendations to fetch the latest market price.
4.  **Error Handling**:
    - Explicit UI errors for missing API keys or failed analysis.
    - Graceful degradation to mock data upon user request.

## Fallback Instructions
If future updates break the application, you can revert to this state using:
```bash
git checkout 34657567806eeee8a07bd5903e72d13643b4385a
```
Or simply refer to this commit in the GitHub repository history.
