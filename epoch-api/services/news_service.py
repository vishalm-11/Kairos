import os
import requests
import re

def clean(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text).strip()

def fetch_news(country: str) -> list:
    headlines = _fetch_newsapi(country)
    if not headlines:
        headlines = _fetch_gdelt(country)
    if not headlines:
        headlines = [f"No recent news available for {country}"]
    return headlines

def _fetch_newsapi(country: str) -> list:
    try:
        key = os.getenv("NEWS_API_KEY")
        r = requests.get(
            "https://newsapi.org/v2/everything",
            params={"q": country, "sortBy": "publishedAt", "pageSize": 5, "language": "en", "apiKey": key},
            timeout=5
        )
        data = r.json()
        articles = data.get("articles", [])
        return [clean(a["title"]) for a in articles if a.get("title") and clean(a["title"])]
    except Exception:
        return []

def _fetch_gdelt(country: str) -> list:
    try:
        r = requests.get(
            f"https://api.gdeltproject.org/api/v2/doc/doc",
            params={"query": country, "mode": "artlist", "maxrecords": 5, "format": "json"},
            timeout=5
        )
        data = r.json()
        articles = data.get("articles", [])
        return [clean(a["title"]) for a in articles if a.get("title") and clean(a["title"])]
    except Exception:
        return []
