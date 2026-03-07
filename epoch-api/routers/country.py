from fastapi import APIRouter, HTTPException
from services.news_service import fetch_news
from services.gemini_service import summarize_news
from services.elevenlabs_service import speak

router = APIRouter()

@router.get("/country/{country_name}")
async def get_country_data(country_name: str):
    try:
        print(f"Fetching data for country: {country_name}")
        headlines = fetch_news(country_name)
        print(f"Headlines fetched: {len(headlines)} items")
        
        summary = summarize_news(country_name, headlines)
        print(f"Summary generated: {len(summary)} characters")
        
        audio_base64 = speak(summary)
        print(f"Audio generated: {len(audio_base64)} characters")
        
        return {
            "country": country_name,
            "headlines": headlines,
            "summary": summary,
            "audio_base64": audio_base64
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error processing {country_name}: {error_details}")
        raise HTTPException(status_code=500, detail=f"Error processing {country_name}: {str(e)}")
