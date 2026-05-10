import random
import time
from utils.config import SKILL_BRANCHES

def extract_text(uploaded_file):
    return "Texte extrait..."

def build_prompt(instructions, text):
    return f"Consignes: {instructions}\nTexte: {text}"

def mock_evaluate_effort(prompt):
    """Simule l'évaluation ET la répartition sur les branches."""
    time.sleep(1.5)
    xp_total = random.randint(10, 50)
    
    # Choix de 1 à 3 branches aléatoires
    branches_cibles = random.sample(SKILL_BRANCHES, random.randint(1, 3))
    
    # Répartition aléatoire des pourcentages (qui font 100% à la fin)
    weights = [random.random() for _ in branches_cibles]
    total_w = sum(weights)
    distribution = {b: w/total_w for b, w in zip(branches_cibles, weights)}
    
    return xp_total, distribution

def mock_get_advice():
    """Génère un conseil aléatoire pour le Skill Tree."""
    advices = [
        "Essaie de diversifier tes devoirs pour développer ta Créativité.",
        "Ta Logique est excellente, continue de faire des exercices de maths !",
        "Un peu plus de Structure ne ferait pas de mal, relis bien tes plans.",
        "Ton Raisonnement est solide, attaque-toi à des sujets plus complexes.",
        "Pense à soigner ton Expression dans tes prochaines rédactions."
    ]
    return random.choice(advices)