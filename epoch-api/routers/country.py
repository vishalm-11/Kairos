from fastapi import APIRouter, HTTPException
from services.news_service import fetch_news
from services.gemini_service import summarize_news, get_sentiment, get_related_countries
from services.elevenlabs_service import speak
from services.economics_service import get_economic_pulse, get_top_stocks, get_stock_index, COUNTRY_ECONOMIC_DATA
import asyncio
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()
executor = ThreadPoolExecutor(max_workers=3)

@router.get("/country/{country_name}")
async def get_country_data(country_name: str):
    try:
        print(f"Fetching data for country: {country_name}")
        
        # Fetch headlines first (fast)
        headlines = fetch_news(country_name)
        print(f"Headlines fetched: {len(headlines)} items")
        print(f"Headlines content: {headlines}")
        
        # Filter out the "No recent news" fallback message for summary
        valid_headlines = [h for h in headlines if h.get("title") and "No recent news available" not in h.get("title", "")]
        
        # Fetch economic data (can be slow, but acceptable)
        try:
            economics = get_economic_pulse(country_name)
            print(f"Economics fetched for {country_name}: {economics}")
        except Exception as e:
            import traceback
            print(f"Error fetching economics for {country_name}: {e}")
            print(traceback.format_exc())
            economics = {"currency_code": None, "currency": None, "stock": None}
        
        # Extract just titles for Gemini summary (use valid headlines only)
        headline_titles = [h["title"] for h in valid_headlines if h.get("title")]
        
        # If no valid headlines, use a default message for summary
        if not headline_titles:
            headline_titles = [f"Recent news about {country_name}"]
            print(f"WARNING: No valid headlines for summary, using default")
        
        # Ensure headlines is always a list and filter out fallback messages
        if not headlines:
            headlines = []
        else:
            # Remove any "No recent news" fallback messages
            headlines = [h for h in headlines if h.get("title") and "No recent news available" not in h.get("title", "")]
        
        print(f"Final headlines being returned: {len(headlines)} items")
        if headlines:
            for i, h in enumerate(headlines):
                print(f"  Headline {i+1}: {h.get('title', 'NO TITLE')[:60]}...")
        else:
            print(f"  WARNING: No valid headlines to return!")
        
        # Run all async operations in parallel for maximum speed
        loop = asyncio.get_event_loop()
        
        # Start all operations in parallel
        summary_future = loop.run_in_executor(
            executor, 
            summarize_news, 
            country_name, 
            headline_titles,
            economics
        )
        top_stocks_future = loop.run_in_executor(executor, get_top_stocks, country_name, headlines)
        sentiment_future = loop.run_in_executor(executor, get_sentiment, country_name, headlines)
        related_countries_future = loop.run_in_executor(executor, get_related_countries, country_name, headlines)
        
        # Wait for summary first (needed for audio)
        summary = await summary_future
        print(f"Summary generated: {len(summary)} characters")
        
        # Generate audio while other operations complete
        audio_future = loop.run_in_executor(executor, speak, summary)
        
        # Wait for all remaining operations
        audio_base64, top_stocks, sentiment, related_countries = await asyncio.gather(
            audio_future,
            top_stocks_future,
            sentiment_future,
            related_countries_future,
            return_exceptions=True
        )
        
        print(f"Audio generated: {len(audio_base64) if not isinstance(audio_base64, Exception) else 0} characters")
        
        # Handle exceptions - do not silently swallow ElevenLabs errors
        if isinstance(audio_base64, Exception):
            print(f"Error generating audio: {audio_base64}")
            raise HTTPException(
                status_code=502,
                detail=f"Audio generation failed: {str(audio_base64)}"
            )
        if isinstance(top_stocks, Exception):
            print(f"Error fetching top stocks: {top_stocks}")
            top_stocks = []
        if isinstance(sentiment, Exception):
            print(f"Error fetching sentiment: {sentiment}")
            sentiment = {"score": 5, "label": "Neutral", "reasoning": "Unable to determine sentiment."}
        if isinstance(related_countries, Exception):
            print(f"Error fetching related countries: {related_countries}")
            related_countries = []
        
        print(f"Top stocks fetched: {len(top_stocks)} stocks")
        print(f"Sentiment: {sentiment}")
        print(f"Related countries: {related_countries}")
        
        return {
            "country": country_name,
            "headlines": headlines,  # Now includes URLs
            "summary": summary,
            "audio_base64": audio_base64,
            "economics": economics,
            "top_stocks": top_stocks,
            "sentiment": sentiment,
            "related_countries": related_countries,
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing {country_name}: {error_details}")
        raise HTTPException(status_code=500, detail=f"Error processing {country_name}: {str(e)}")

@router.get("/markets")
async def get_all_markets(countries: str | None = None):
    """Get current index data. If countries param provided (comma-separated), fetch only those. Otherwise return all."""
    if countries:
        country_list = [c.strip() for c in countries.split(",") if c.strip()]
    else:
        country_list = list(COUNTRY_ECONOMIC_DATA.keys())
    
    results = {}
    for country in country_list:
        meta = COUNTRY_ECONOMIC_DATA.get(country)
        if not meta or not meta.get("index"):
            results[country] = None
            continue
        try:
            stock = get_stock_index(meta["index"], meta["index_name"])
            results[country] = stock
        except Exception as e:
            print(f"Error fetching market data for {country}: {e}")
            results[country] = None
    return results
