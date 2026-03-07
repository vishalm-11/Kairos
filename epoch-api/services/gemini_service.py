import os
from google import genai

def summarize_news(country: str, headlines: list) -> str:
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
        http_options={"api_version": "v1"}
    )
    
    headlines_text = "\n".join(f"- {h}" for h in headlines)
    
    prompt = f"""You are a calm, authoritative live news anchor broadcasting to a global audience.
Summarize these recent headlines about {country} in exactly 3-4 sentences.
Speak naturally and conversationally, as if reading live on air.
Be factual, concise, and impactful. Do not use bullet points or markdown.
Only return the spoken summary text — nothing else.

Headlines:
{headlines_text}"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    
    text = response.text.strip()
    # Strip any markdown code fences if present
    text = text.replace("```", "").strip()
    return text
