import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze_document(text):

    prompt = f"""
You are an expert AI document analyst.

Analyze the following document.

Return ONLY valid JSON in this format:

{{
    "summary":"...",
    "document_type":"...",
    "sentiment":"...",
    "recommendations":"..."
}}

Rules:
- Summary should be 8-10 lines.
- Detect document type.
- Detect sentiment (Positive, Neutral or Negative).
- Give 5 short recommendations.

Document:

{text}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    result = response.text.strip()

    # Remove markdown if Gemini returns it
    result = result.replace("```json", "")
    result = result.replace("```", "")

    try:
        return json.loads(result)

    except Exception:

        return {
            "summary": result,
            "document_type": "Unknown",
            "sentiment": "Neutral",
            "recommendations": "No recommendations available."
        }