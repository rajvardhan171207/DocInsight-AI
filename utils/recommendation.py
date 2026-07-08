from utils.gemini import client

def generate_recommendation(text):

    prompt = f"""
You are an AI document reviewer.

Read this document and provide 4-5 professional recommendations.

Document:

{text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        return response.text

    except Exception:
        return "No recommendations available."