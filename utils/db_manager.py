import json
import os

DB_PATH = "database.json"

def load_db():
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def add_xp(subject, xp_amount):
    data = load_db()
    if subject in data.get("xp_by_subject", {}):
        data["xp_by_subject"][subject] += xp_amount
        save_db(data)
        return data["xp_by_subject"][subject]
    return None