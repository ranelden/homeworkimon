import streamlit as st
from utils.db_manager import load_db

st.title("🏠 Dashboard")

data = load_db()
user = data.get("user", {})

# Affichage des infos de base
st.write(f"**Bienvenue {user.get('name', 'Joueur')} !**")
st.write(f"Niveau Actuel : {user.get('level', 1)} | 🔥 Streak : {user.get('streak', 0)} jours")

st.divider()

st.subheader("Votre Équipe Active (Top 3)")
st.info("Bientôt disponible : L'affichage dynamique de vos 3 meilleurs monstres.")