import random
import time
from utils.config import SKILL_BRANCHES

def extract_text(uploaded_file):
    """
    US-3.01: Extrait le texte brut d'un fichier PDF ou TXT.
    (Simulation pour le MVP)
    """
    return "Texte brut extrait du document simulé..."

def build_prompt(instructions, text):
    """
    US-3.02: Compile les consignes et le texte en un prompt standardisé.
    """
    return f"Consignes: {instructions}\n\nTexte de l'élève: {text}\n\nÉvalue l'effort fourni."

def mock_evaluate_effort(prompt):
    """
    Simule l'API LLM (OpenAI/Gemini).
    - US-3.04: Retourne un score numérique (XP).
    - US-3.13: Retourne une phrase de justification.
    - Génère une répartition de l'XP sur 1 à 3 branches de compétences.
    """
    time.sleep(1.5)  # Simule le temps de traitement réseau/IA
    
    # 1. Calcul de l'XP (Score entre 10 et 50)
    base_xp = random.randint(10, 50)
    
    # 2. Répartition des compétences (Skill Tree)
    # Choix de 1 à 3 compétences aléatoires parmi les 8
    branches_cibles = random.sample(SKILL_BRANCHES, random.randint(1, 3))
    
    # Attribution de poids aléatoires
    weights = [random.random() for _ in branches_cibles]
    total_weight = sum(weights)
    
    # Normalisation pour que la somme fasse 100% (1.0)
    distribution = {b: w/total_weight for b, w in zip(branches_cibles, weights)}
    
    # 3. Justification de l'IA (US-3.13)
    reasonings = [
        "L'effort est bien visible, la structure est claire mais l'originalité peut être creusée.",
        "Excellent travail de recherche, le raisonnement est très solide.",
        "Les consignes sont respectées, mais l'expression écrite mérite un peu plus d'attention.",
        "Très belle créativité dans l'approche de ce devoir !",
        "Le devoir est un peu court, mais la logique principale est acquise."
    ]
    reasoning = random.choice(reasonings)
    
    return base_xp, distribution, reasoning

def mock_get_advice():
    """
    US-5.05: Retourne un conseil généré par l'IA pour orienter l'apprentissage sur le Skill Tree.
    """
    advices = [
        "Essaie de diversifier tes devoirs pour développer ta Créativité.",
        "Ta Logique est excellente, continue de faire des exercices de maths !",
        "Un peu plus de Structure ne ferait pas de mal, relis bien tes plans avant de rédiger.",
        "Ton Raisonnement est solide, attaque-toi à des sujets plus complexes pour repousser tes limites.",
        "Pense à soigner ton Expression dans tes prochaines rédactions en utilisant un vocabulaire plus riche."
    ]
    return random.choice(advices)