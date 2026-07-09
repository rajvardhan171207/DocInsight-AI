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
You are an expert AI Document Analyst.

Analyze the following document carefully and return ONLY valid JSON in the exact format below.

{{
    "summary":"...",
    "document_type":"...",
    "sentiment":"...",
    "recommendations":"..."
}}

Instructions:

1. Summary:
   -Write a clear and detailed summary between 150 and 300 words, depending on the document length.
   - Cover all important topics, sections, facts, and conclusions.
   - Preserve the logical flow of the document.
   - Do not omit any major information.
   - Do not repeat the same point.
   - Use simple, professional English.
   - Do NOT add information that is not present in the document.

2. Document Type:
   - Identify the most appropriate document type.

3. Sentiment:
   - Return ONLY one of these:
     - Positive
     - Neutral
     - Negative

4. Recommendations:
   - Provide exactly 5 practical recommendations.
   - Return them as bullet points.
   - Recommendations should be relevant to the document.

IMPORTANT:
- Return ONLY valid JSON.
- Do not use markdown.
- Do not use ```json.
- Do not include any explanation outside the JSON.

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