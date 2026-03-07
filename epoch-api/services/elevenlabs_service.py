import os
import base64
import requests

VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel

def speak(text: str) -> str:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not set in environment variables")
    
    if not text or len(text.strip()) == 0:
        raise ValueError("Cannot generate audio for empty text")
    
    try:
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
        
        if not response.content:
            raise ValueError("Empty audio response from ElevenLabs")
        
        return base64.b64encode(response.content).decode("utf-8")
    except requests.exceptions.RequestException as e:
        raise Exception(f"ElevenLabs API error: {str(e)}")
