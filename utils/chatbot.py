import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

# Load environment variables
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


# Create Gemini client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_document(document, question):

    prompt = f"""
You are an AI document assistant.

Answer the question only using the information from the document.

Document:
{document}

Question:
{question}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )

        return response.text

    except ServerError:
        return "⚠️ Gemini AI is currently experiencing high demand. Please try again after a few minutes."

    except Exception as e:
        return f"Error: {str(e)}"