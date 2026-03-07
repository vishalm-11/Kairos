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
        # Focus on conflicts, world issues, public relations, and foreign affairs
        # Use keywords that filter for relevant geopolitical news
        keywords = [
            "conflict", "crisis", "diplomacy", "foreign affairs", "international relations",
            "war", "peace", "treaty", "sanctions", "embassy", "summit", "talks",
            "protest", "unrest", "security", "defense", "military", "government",
            "politics", "election", "trade", "economy", "alliance", "tension"
        ]
        
        # Build query focusing on geopolitical news
        query = f'({country}) AND ({") OR (".join(keywords[:10])})'
        
        r = requests.get(
            "https://newsapi.org/v2/everything",
            params={
                "q": query,
                "sortBy": "publishedAt",
                "pageSize": 20,  # Fetch more to ensure we get 5 good results after filtering
                "language": "en",
                "apiKey": key,
                "searchIn": "title,description"
            },
            timeout=5
        )
        data = r.json()
        articles = data.get("articles", [])
        result = []
        
        # Filter articles for relevance
        for a in articles:
            title = clean(a.get("title", "")).lower()
            description = clean(a.get("description", "")).lower()
            url = a.get("url")
            
            # Skip irrelevant content (sports, entertainment, local news, etc.)
            irrelevant_keywords = [
                "sport", "football", "soccer", "basketball", "game", "match",
                "entertainment", "celebrity", "movie", "music", "tv show",
                "recipe", "cooking", "food", "restaurant", "weather forecast",
                "stock market", "cryptocurrency", "bitcoin", "crypto"
            ]
            
            # Check if article is relevant
            is_relevant = any(kw in title or kw in description for kw in keywords)
            is_irrelevant = any(ikw in title or ikw in description for ikw in irrelevant_keywords)
            
            # Ensure country name appears in title or description (for relevance)
            country_in_content = country.lower() in title or country.lower() in description
            
            if title and url and is_relevant and not is_irrelevant and country_in_content:
                result.append({
                    "title": clean(a.get("title", "")),  # Return original case
                    "url": url
                })
                if len(result) >= 5:
                    break
        
        # If we don't have enough relevant results, fall back to broader search
        if len(result) < 5:
            query_fallback = f'"{country}" AND (conflict OR crisis OR diplomacy OR foreign OR international OR government OR politics)'
            r2 = requests.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": query_fallback,
                    "sortBy": "publishedAt",
                    "pageSize": 15,  # Fetch more to ensure we get 5 results
                    "language": "en",
                    "apiKey": key,
                },
                timeout=5
            )
            data2 = r2.json()
            articles2 = data2.get("articles", [])
            for a in articles2:
                title = clean(a.get("title", ""))
                url = a.get("url")
                if title and url and title.lower() not in [r["title"].lower() for r in result]:
                    result.append({"title": title, "url": url})
                    if len(result) >= 5:
                        break
        
        # Ensure we return between 3 and 5 headlines
        return result[:5] if len(result) >= 3 else result
    except Exception as e:
        print(f"NewsAPI error: {e}")
        return []

def _fetch_gdelt(country: str) -> List[Dict[str, str]]:
    try:
        r = requests.get(
            f"https://api.gdeltproject.org/api/v2/doc/doc",
            params={"query": country, "mode": "artlist", "maxrecords": 10, "format": "json"},
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
                if len(result) >= 5:
                    break
        # Ensure we return between 3 and 5 headlines
        return result[:5] if len(result) >= 3 else result
    except Exception as e:
        print(f"GDELT error: {e}")
        return []
