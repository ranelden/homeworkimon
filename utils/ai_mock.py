import random
import time
from utils.config import SKILL_BRANCHES

def extract_text(uploaded_file):
    """
    US-3.01: Extrait le texte brut d'un fichier PDF ou TXT.
    (Simulation pour le MVP)
    """
    return "Raw text extracted from the simulated document..."

def build_prompt(instructions, text):
    """
    US-3.02: Compile les consignes et le texte en un prompt standardisé.
    """
    return f"Instructions: {instructions}\n\nStudent text: {text}\n\nEvaluate the effort provided."

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
        "Your effort is clearly visible; the structure is solid, but originality could be stronger.",
        "Excellent research work; the reasoning is very solid.",
        "The instructions were followed, but written expression could use a bit more polish.",
        "Very nice creativity in your approach to this assignment!",
        "The assignment is a bit short, but the core logic is present."
    ]
    reasoning = random.choice(reasonings)
    
    return base_xp, distribution, reasoning

def mock_get_advice():
    """
    US-5.05: Retourne un conseil généré par l'IA pour orienter l'apprentissage sur le Skill Tree.
    """
    advices = [
        "Try diversifying your assignments to develop your Creativity.",
        "Your Logic is excellent; keep doing math exercises!",
        "A bit more Structure would help; review your outlines before writing.",
        "Your Reasoning is solid; tackle more complex topics to push your limits.",
        "Take care with your Expression in future essays by using richer vocabulary."
    ]
    return random.choice(advices)