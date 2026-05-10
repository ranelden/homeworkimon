import json
import os
from datetime import datetime
from utils.config import SUBJECTS_CONFIG, THRESHOLDS, SKILL_BRANCHES

DB_PATH = "database.json"

def _sync_db_with_config(data):
    if "xp_by_subject" not in data: data["xp_by_subject"] = {}
    if "homidex" not in data: data["homidex"] = {}
    if "skills" not in data: data["skills"] = {branch: 0.0 for branch in SKILL_BRANCHES}
    if "history" not in data: data["history"] = [] # Historique des devoirs
        
    db_updated = False
    
    # Synchro matières
    for subject, img_prefix in SUBJECTS_CONFIG.items():
        if subject not in data["xp_by_subject"]:
            data["xp_by_subject"][subject] = 0
            db_updated = True
        if subject not in data["homidex"]:
            data["homidex"][subject] = {"name": f"{img_prefix.capitalize()}imon", "stage": 1}
            db_updated = True
            
    # Synchro compétences
    for branch in SKILL_BRANCHES:
        if branch not in data["skills"]:
            data["skills"][branch] = 0.0
            db_updated = True
            
    if db_updated: save_db(data)
    return data

def load_db():
    if not os.path.exists(DB_PATH):
        base_data = {"user": {"name": "Étudiant", "level": 1, "streak": 0}}
        synced_data = _sync_db_with_config(base_data)
        save_db(synced_data)
        return synced_data
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return _sync_db_with_config(json.load(f))

def save_db(data):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_stage_from_xp(xp):
    if xp >= THRESHOLDS[3]: return 3
    elif xp >= THRESHOLDS[2]: return 2
    return 1

# Calcul polynomial infini : Niveau = (XP/50)^(1/1.2) + 1
def get_skill_level(xp):
    return int((xp / 50.0) ** (1 / 1.2)) + 1

# XP requis pour le niveau actuel et le suivant
def get_skill_xp_bounds(level):
    current_bound = 50.0 * ((level - 1) ** 1.2)
    next_bound = 50.0 * (level ** 1.2)
    return current_bound, next_bound

def add_xp(subject, xp_amount, file_name, branch_distribution):
    data = load_db()
    
    # 1. Update XP Matière
    old_xp = data["xp_by_subject"].get(subject, 0)
    new_xp = old_xp + xp_amount
    data["xp_by_subject"][subject] = new_xp
    
    # 2. Update Homidex
    old_stage = get_stage_from_xp(old_xp)
    new_stage = get_stage_from_xp(new_xp)
    has_evolved = new_stage > old_stage
    data["homidex"][subject]["stage"] = new_stage
        
    # 3. Update Skills (Branches)
    for branch, weight in branch_distribution.items():
        data["skills"][branch] += (xp_amount * weight)
        
    # 4. Update History
    data["history"].append({
        "date": datetime.now().strftime("%Y-%m-%d"),
        "subject": subject,
        "file_name": file_name,
        "xp": xp_amount
    })
        
    save_db(data)
    return new_xp, has_evolved, new_stage