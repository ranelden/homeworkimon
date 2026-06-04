import json
import os
from datetime import datetime
from utils.config import SUBJECTS_CONFIG, THRESHOLDS, SKILL_BRANCHES

DB_PATH = "database.json"

def _sync_db_with_config(data):
    """
    US-3.05: Synchronise et initialise toutes les clés manquantes du JSON.
    Garantit que la base ne crashe jamais si on ajoute des features.
    """
    if "user" not in data: 
        data["user"] = {"streak": 0, "last_date": ""}
    if "settings" not in data: 
        data["settings"] = {"nickname": "Étudiant", "title": "Novice", "theme_color": "#ff4b4b"}
    if "xp_by_subject" not in data: 
        data["xp_by_subject"] = {}
    if "homidex" not in data: 
        data["homidex"] = {}
    if "skills" not in data: 
        data["skills"] = {branch: 0.0 for branch in SKILL_BRANCHES}
    if "history" not in data: 
        data["history"] = []
        
    db_updated = False
    
    # Synchronisation des matières depuis config.py
    for subject, img_prefix in SUBJECTS_CONFIG.items():
        if subject not in data["xp_by_subject"]:
            data["xp_by_subject"][subject] = 0
            db_updated = True
        if subject not in data["homidex"]:
            data["homidex"][subject] = {
                "name": f"{img_prefix.capitalize()}imon", 
                "custom_name": f"{img_prefix.capitalize()}imon", 
                "stage": 1
            }
            db_updated = True
            
    if db_updated: 
        save_db(data)
        
    return data

def load_db():
    """Charge le JSON ou le crée s'il n'existe pas."""
    if not os.path.exists(DB_PATH):
        base_data = {"user": {"streak": 0, "last_date": ""}}
        synced_data = _sync_db_with_config(base_data)
        save_db(synced_data)
        return synced_data
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return _sync_db_with_config(json.load(f))

def save_db(data):
    """Sauvegarde les données de manière formatée."""
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def reset_db():
    """US-4.08: Supprime et recrée la base de données pour les tests."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    return load_db()

def get_stage_from_xp(xp):
    """Calcule le stade d'évolution actuel en fonction de l'XP (US-3.07, 3.08)."""
    if xp >= THRESHOLDS[3]: return 3
    elif xp >= THRESHOLDS[2]: return 2
    return 1

# ==========================================
# MATHÉMATIQUES DU SKILL TREE (US-5.01)
# ==========================================
def get_skill_level(xp):
    """Calcule le niveau polynomial infini d'une branche de compétence."""
    return int((xp / 50.0) ** (1 / 1.2)) + 1

def get_skill_xp_bounds(level):
    """Retourne l'XP de base et l'XP requis pour le niveau donné."""
    current_bound = 50.0 * ((level - 1) ** 1.2)
    next_bound = 50.0 * (level ** 1.2)
    return current_bound, next_bound

# ==========================================
# MOTEUR PRINCIPAL D'ATTRIBUTION D'XP
# ==========================================
def add_xp(subject, base_xp, file_name, branch_distribution, difficulty):
    """
    Fonction centrale exécutée lors d'un dépôt (US-3.06).
    Gère le Streak, le multiplicateur, l'XP, l'Homidex, les Skills et l'Historique.
    """
    data = load_db()
    
    # Format de date : YYYY-MM-DD
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 1. Gestion du Streak (US-1.09, US-1.10)
    last_date = data["user"].get("last_date", "")
    if last_date != today:
        if not last_date: 
            data["user"]["streak"] = 1
        else:
            last_date_obj = datetime.strptime(last_date, "%Y-%m-%d")
            delta = (datetime.now() - last_date_obj).days
            if delta == 1:
                data["user"]["streak"] += 1
            else:
                data["user"]["streak"] = 1 # Perte du streak si > 24h
    data["user"]["last_date"] = today
    
    # 2. Multiplicateur de difficulté (US-2.13)
    mult = 1.0
    if difficulty == "Hard": mult = 1.5
    elif difficulty == "Easy": mult = 0.8
    final_xp = int(base_xp * mult)

    # 3. Mise à jour XP Matière
    old_xp = data["xp_by_subject"].get(subject, 0)
    new_xp = old_xp + final_xp
    data["xp_by_subject"][subject] = new_xp
    
    # 4. Évolution Homidex (US-3.07)
    old_stage = get_stage_from_xp(old_xp)
    new_stage = get_stage_from_xp(new_xp)
    has_evolved = new_stage > old_stage
    data["homidex"][subject]["stage"] = new_stage
        
    # 5. Mise à jour des Skills
    for branch, weight in branch_distribution.items():
        data["skills"][branch] += (final_xp * weight)
        
    # 6. Historique précis (US-1.08)
    data["history"].append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), # Exact timestamp
        "subject": subject,
        "file_name": file_name,
        "difficulty": difficulty,
        "xp": final_xp
    })
        
    save_db(data)
    
    return new_xp, has_evolved, new_stage, final_xp