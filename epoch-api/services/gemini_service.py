import os
from google import genai

def summarize_news(country: str, headlines: list) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in environment variables")
    
    headlines_text = "\n".join(f"- {h}" for h in headlines)
    
    prompt = f"""You are a calm, authoritative live news anchor broadcasting to a global audience.
Summarize these recent headlines about {country} in exactly 3-4 sentences.
Speak naturally and conversationally, as if reading live on air.
Be factual, concise, and impactful. Do not use bullet points or markdown.
Only return the spoken summary text — nothing else.

Headlines:
{headlines_text}"""

    # Try different API versions and model names
    # Based on available models: gemini-2.5-flash is the latest stable model
    models_to_try = [
        # Try the latest stable models first
        ("v1", "gemini-2.5-flash"),
        ("v1", "gemini-2.0-flash"),
        ("v1", "gemini-2.5-flash-lite"),
        # Try default API version
        (None, "gemini-2.5-flash"),
        (None, "gemini-2.0-flash"),
        (None, "gemini-2.5-flash-lite"),
        # Fallback to older models if needed
        ("v1", "gemini-flash-latest"),
        (None, "gemini-flash-latest"),
    ]
    
    last_error = None
    for api_version, model_name in models_to_try:
        try:
            if api_version:
                client = genai.Client(
                    api_key=api_key,
                    http_options={"api_version": api_version}
                )
            else:
                # Default API version
                client = genai.Client(api_key=api_key)
            
            print(f"Trying model: {model_name} with API version: {api_version or 'default'}")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            
            if not response or not hasattr(response, 'text'):
                raise ValueError("Invalid response from Gemini API")
            
            text = response.text.strip()
            # Strip any markdown code fences if present
            text = text.replace("```", "").strip()
            
            if not text:
                text = f"Recent developments in {country} continue to unfold as global observers monitor the situation closely."
            
            print(f"Successfully used model: {model_name}")
            return text
            
        except Exception as e:
            last_error = e
            print(f"Failed with {model_name} ({api_version or 'default'}): {str(e)[:100]}")
            continue
    
    # If all models failed, raise the last error
    raise Exception(f"Gemini API error: All model attempts failed. Last error: {str(last_error)}")
