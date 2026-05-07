import random
import time

def mock_evaluate_effort():
    """Simule un appel API qui évalue l'effort et renvoie entre 10 et 50 XP."""
    time.sleep(1.5)  # Simule la latence réseau/IA
    return random.randint(10, 50)