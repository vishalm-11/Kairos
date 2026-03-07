import os
import requests
import re
from typing import List, Dict

def clean(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text).strip()

def fetch_news(country: str) -> List[Dict[str, str]]:
    """
    Returns list of dicts with 'title' and 'url' keys
    """
    headlines = _fetch_newsapi(country)
    if not headlines:
        headlines = _fetch_gdelt(country)
    if not headlines:
        return [{"title": f"No recent news available for {country}", "url": None}]
    return headlines

def _fetch_newsapi(country: str) -> List[Dict[str, str]]:
    try:
        key = os.getenv("NEWS_API_KEY")
        # Improve query to get more relevant results
        query = f"{country} OR \"{country}\""
        r = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": query,
                "sortBy": "publishedAt",
                "pageSize": 5,
                "language": "en",
                "apiKey": key,
                "searchIn": "title,description"  # Focus on title and description
            },
            timeout=5
        )
        data = r.json()
        articles = data.get("articles", [])
        result = []
        for a in articles:
            title = clean(a.get("title", ""))
            url = a.get("url")
            if title and url:
                result.append({"title": title, "url": url})
        return result[:5]  # Return top 5
    except Exception as e:
        print(f"NewsAPI error: {e}")
        return []

def _fetch_gdelt(country: str) -> List[Dict[str, str]]:
    try:
        r = requests.get(
            f"https://api.gdeltproject.org/api/v2/doc/doc",
            params={"query": country, "mode": "artlist", "maxrecords": 5, "format": "json"},
            timeout=5
        )
        data = r.json()
        articles = data.get("articles", [])
        result = []
        for a in articles:
            title = clean(a.get("title", ""))
            url = a.get("url") or a.get("seendate")
            if title:
                result.append({"title": title, "url": url})
        return result[:5]
    except Exception as e:
        print(f"GDELT error: {e}")
        return []
