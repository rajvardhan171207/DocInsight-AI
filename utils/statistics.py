import math
import re

def document_statistics(text):
    words = len(re.findall(r"\b\w+\b", text))
    characters = len(text)
    sentences = len(re.findall(r"[.!?]+", text))

    # Average reading speed = 220 words/minute
    total_minutes = max(1, math.ceil(words / 220))

    if total_minutes >= 60:
        hours = total_minutes // 60
        minutes = total_minutes % 60
        reading_time = f"{hours} hr {minutes} min"
    else:
        reading_time = f"{total_minutes} min"

    return {
        "words": words,
        "characters": characters,
        "sentences": sentences,
        "reading_time": reading_time
    }