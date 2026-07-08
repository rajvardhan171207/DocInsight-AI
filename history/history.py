import json
import os
from datetime import datetime

HISTORY_FILE = "history/history.json"


def save_history(filename, category, stats):

    record = {
        "filename": filename,
        "category": category,
        "words": stats["words"],
        "characters": stats["characters"],
        "time": datetime.now().strftime("%d-%m-%Y %I:%M %p")
    }

    if os.path.exists(HISTORY_FILE):

        with open(HISTORY_FILE, "r") as f:
            data = json.load(f)

    else:
        data = []

    data.append(record)

    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)


def load_history():

    if os.path.exists(HISTORY_FILE):

        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
        

    return []
def get_dashboard_stats():

    data = load_history()

    total = len(data)

    pdf = sum(1 for item in data if item["filename"].lower().endswith(".pdf"))
    docx = sum(1 for item in data if item["filename"].lower().endswith(".docx"))
    txt = sum(1 for item in data if item["filename"].lower().endswith(".txt"))

    return {
        "total": total,
        "pdf": pdf,
        "docx": docx,
        "txt": txt
    }