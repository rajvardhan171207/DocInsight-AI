import os
from dotenv import load_dotenv
from google import genai

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
print("API Key:", os.getenv("GEMINI_API_KEY"))
print("Model: gemini-3.1-flash-lite")

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("Gemini.py API Key:", os.getenv("GEMINI_API_KEY"))
def generate_summary(text):
    prompt = f"""
You are an AI document analyst.

Generate a professional summary of the following document.

Document:

{text}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text
def classify_document(text):

    

    prompt = f"""
You are an AI document classifier.

Identify the type of this document.

Return ONLY one category from the list below.

Categories:
- Research Paper
- Resume
- Invoice
- Legal Document
- Medical Report
- Assignment
- Business Report
- Contract
- Letter
- Other

Document:

{text}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text.strip()
def analyze_sentiment(text):

    prompt = f"""
You are an AI sentiment analyzer.

Analyze the sentiment of this document.

Return ONLY one word.

Choices:
- Positive
- Neutral
- Negative

Document:

{text}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text.strip()
def generate_recommendations(text):

    prompt = f"""
You are an AI document reviewer.

Read the document and provide 5 short recommendations to improve it.

Return the answer as bullet points only.

Document:

{text}
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=prompt
    )

    return response.text