# ==========================================
# CONFIGURATION GLOBALE HOMEWORKIMON
# ==========================================

# Liste des matières et préfixes des fichiers images associés.
# Pour ajouter une matière, il suffit de l'ajouter ici et de glisser 
# les images correspondantes dans le dossier img/ (ex: anglais$1.png)
SUBJECTS_CONFIG = {
    "Mathématiques": "math",
    "Sciences": "physique",
    "Français": "francais",
    "Histoire": "histoire"
}

# Paliers d'évolution (XP requis pour atteindre chaque stade)
THRESHOLDS = {
    1: 0, 
    2: 300, 
    3: 1000
}

# Branches de compétences pour le Skill Tree (Radar Chart)
SKILL_BRANCHES = [
    "Logique", 
    "Créativité", 
    "Structure", 
    "Originalité", 
    "Raisonnement", 
    "Mémoire", 
    "Expression", 
    "Précision"
]

# Liste des Quêtes Journalières aléatoires
DAILY_QUESTS = [
    "Soumettre un devoir de Mathématiques aujourd'hui.",
    "Soumettre un devoir difficile (+50% XP).",
    "Travailler ta bête noire (Matière avec le moins d'XP).",
    "Faire évoluer un Homeworkimon vers le stade supérieur.",
    "Gagner au moins 40 XP en une seule soumission."
]