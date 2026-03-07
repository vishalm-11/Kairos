import os
from google import genai

def summarize_news(country: str, headlines, economics: dict = None) -> str:
    # Handle both old format (list of strings) and new format (list of dicts)
    if headlines and isinstance(headlines[0], dict):
        headline_titles = [h.get("title", "") for h in headlines if h.get("title")]
    else:
        headline_titles = [h for h in headlines if isinstance(h, str)]
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in environment variables")
    
    headlines_text = "\n".join(f"- {h}" for h in headline_titles)
    
    # Build economics context text if available
    economics_text = ""
    if economics:
        if economics.get("currency") and economics["currency"].get("formatted"):
            economics_text += f"\nCurrency: {economics['currency']['formatted']}"
        if economics.get("stock") and economics["stock"].get("formatted"):
            economics_text += f"\nMarkets: {economics['stock']['formatted']}"
    
    prompt = f"""You are a calm, authoritative live news anchor broadcasting to a global audience.
Summarize the situation in {country} in exactly 3-4 sentences spoken naturally as if live on air.
If economic data is provided, naturally weave one brief reference to it into your summary.
Be factual, concise, and impactful. Do not use bullet points or markdown. Only return the spoken summary — nothing else.

Headlines:
{headlines_text}
{f"Economic Context:{economics_text}" if economics_text else ""}"""

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
