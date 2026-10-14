import json 
from pathlib import Path

db = Path("tickets_log.json").resolve()

def load_json():
    try:
        with open(db, 'r', encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_json():
    with open(db, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)