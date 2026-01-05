import requests
import json
from config import PERPLEXITY_API_KEY

PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"

def perplexity_verify(headline: str):
    """
    Uses Perplexity API to verify a claim, specifically useful for recent events (post-2024).
    Returns a verdict and explanation.
    """
    if not PERPLEXITY_API_KEY:
        return {"verdict": "UNCERTAIN", "summary": "Perplexity API key missing."}

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = (
        "You are an expert fact-checker. verification agent. "
        "Analyze the user's claim strictly based on the latest available information (including post-2024 events). "
        "Return a JSON object with two keys: "
        "'verdict' (one of: 'SAFE TO PROCEED', 'POTENTIAL MISINFORMATION', 'UNCERTAIN') "
        "and 'summary' (a brief explanation of why)."
    )

    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Verify this claim: {headline}"}
        ],
        "temperature": 0.0
    }

    try:
        response = requests.post(PERPLEXITY_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        content = data["choices"][0]["message"]["content"]
        
        # Attempt to parse JSON from the extracted content
        # Perplexity might wrap code in backticks, so we clean it.
        cleaned_content = content.replace("```json", "").replace("```", "").strip()
        
        try:
            result = json.loads(cleaned_content)
            return result
        except json.JSONDecodeError:
            # Fallback if it returns plain text
            if "POTENTIAL MISINFORMATION" in content.upper():
                return {"verdict": "POTENTIAL MISINFORMATION", "summary": content}
            elif "SAFE TO PROCEED" in content.upper():
                return {"verdict": "SAFE TO PROCEED", "summary": content}
            else:
                return {"verdict": "UNCERTAIN", "summary": content}

    except Exception as e:
        return {"verdict": "UNCERTAIN", "summary": f"Perplexity Error: {str(e)}"}
