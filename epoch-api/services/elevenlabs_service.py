import os
import base64
import requests

VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel

def speak(text: str) -> str:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg"
        },
        json={
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        },
        timeout=30
    )
    
    response.raise_for_status()
    return base64.b64encode(response.content).decode("utf-8")
