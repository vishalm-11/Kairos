from fastapi import APIRouter, HTTPException
from services.news_service import fetch_news
from services.gemini_service import summarize_news
from services.elevenlabs_service import speak
from services.economics_service import get_economic_pulse
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
        
        # Fetch economic data (can be slow, but acceptable)
        try:
            economics = get_economic_pulse(country_name)
            print(f"Economics fetched for {country_name}: {economics}")
        except Exception as e:
            import traceback
            print(f"Error fetching economics for {country_name}: {e}")
            print(traceback.format_exc())
            economics = {"currency_code": None, "currency": None, "stock": None}
        
        # Extract just titles for Gemini summary
        headline_titles = [h["title"] for h in headlines]
        
        # Run Gemini and ElevenLabs in parallel for speed
        loop = asyncio.get_event_loop()
        
        # Generate summary (can take a few seconds) - now includes economics
        summary_future = loop.run_in_executor(
            executor, 
            summarize_news, 
            country_name, 
            headline_titles,
            economics
        )
        
        # Wait for summary, then generate audio
        summary = await summary_future
        print(f"Summary generated: {len(summary)} characters")
        
        # Generate audio (can take a few seconds)
        audio_base64 = await loop.run_in_executor(
            executor,
            speak,
            summary
        )
        print(f"Audio generated: {len(audio_base64)} characters")
        
        return {
            "country": country_name,
            "headlines": headlines,  # Now includes URLs
            "summary": summary,
            "audio_base64": audio_base64,
            "economics": economics,
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing {country_name}: {error_details}")
        raise HTTPException(status_code=500, detail=f"Error processing {country_name}: {str(e)}")
