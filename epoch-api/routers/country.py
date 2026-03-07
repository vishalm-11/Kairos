from fastapi import APIRouter, HTTPException
from services.news_service import fetch_news
from services.gemini_service import summarize_news
from services.elevenlabs_service import speak

router = APIRouter()

@router.get("/country/{country_name}")
async def get_country_data(country_name: str):
    try:
        headlines = fetch_news(country_name)
        summary = summarize_news(country_name, headlines)
        audio_base64 = speak(summary)
        return {
            "country": country_name,
            "headlines": headlines,
            "summary": summary,
            "audio_base64": audio_base64
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
