import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta
from utils.db_manager import load_db, get_stage_from_xp
from utils.config import SUBJECTS_CONFIG, THRESHOLDS, DAILY_QUESTS

st.set_page_config(page_title="Dashboard - Homeworkimon", page_icon="🏠", layout="wide")

# --- INJECTION CSS (Pour l'effet Hover des blocs) ---
st.markdown("""
<style>
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #ff4b4b !important;
    box-shadow: 0px 0px 15px rgba(255, 75, 75, 0.4);
    transition: all 0.3s ease-in-out;
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)
# ------------------------------------------

data = load_db()
history = data.get("history", [])

# US-1.11: Citation motivationnelle aléatoire
QUOTES = [
    "Le succès, c'est tomber sept fois, se relever huit.",
    "L'éducation est l'arme la plus puissante pour changer le monde.",
    "Chaque petit effort compte.",
    "La persévérance est la clé de toutes les évolutions."
]

st.title("🏠 Dashboard")

# --- HEADER : PROFIL & STREAK ---
col_profile, col_stats = st.columns([2, 1])
with col_profile:
    nickname = data.get('settings', {}).get('nickname', 'Étudiant')
    st.write(f"### Bienvenue, {nickname} !")
    st.caption(f"_{random.choice(QUOTES)}_")

with col_stats:
    streak = data.get("user", {}).get("streak", 0)
    # US-1.09, US-1.10: Icône de flamme ou grise selon le streak
    flame = "🔥" if streak > 0 else "🌑"
    st.metric(label=f"{flame} Streak Actuel", value=f"{streak} Jours")

st.divider()

# --- QUÊTES (US-7.01, US-7.03) ---
col_q1, col_q2 = st.columns(2)
with col_q1:
    st.info(f"📜 **Quête du jour :** {random.choice(DAILY_QUESTS)}")
    
with col_q2:
    # Calcul de la quête hebdomadaire (Ex: 5 devoirs cette semaine)
    week_ago = datetime.now() - timedelta(days=7)
    submissions_this_week = 0
    for h in history:
        try:
            # Sécurité si le format date varie
            h_date = datetime.strptime(h["date"], "%Y-%m-%d %H:%M:%S")
        except:
            h_date = datetime.strptime(h["date"][:10], "%Y-%m-%d")
        if h_date >= week_ago:
            submissions_this_week += 1
            
    st.write("**Quête Hebdomadaire :** Soumettre 5 devoirs")
    st.progress(min(submissions_this_week / 5.0, 1.0))
    st.caption(f"{submissions_this_week} / 5 devoirs soumis ces 7 derniers jours")

st.divider()

# --- ÉQUIPE ACTIVE / TOP 3 (US-1.04, 1.05, 1.06) ---
st.subheader("⚔️ Ton Équipe Active (Top 3)")
xp_data = data.get("xp_by_subject", {})
top_3 = sorted(xp_data.items(), key=lambda x: x[1], reverse=True)[:3]

if not top_3 or sum(xp for _, xp in top_3) == 0:
    st.info("Ton équipe est encore vide. Dépose un devoir dans le Habit Hub pour commencer ton aventure !")
else:
    cols = st.columns(3)
    for index, (subject, current_xp) in enumerate(top_3):
        with cols[index]:
            with st.container(border=True):
                monster_data = data.get("homidex", {}).get(subject, {})
                monster_name = monster_data.get("name", "Monstre Inconnu")
                
                st.markdown(f"#### {subject}")
                st.caption(f"🐲 **{monster_name}**")
                
                stage = get_stage_from_xp(current_xp)
                img_prefix = SUBJECTS_CONFIG.get(subject, "math")
                img_path = f"img/{img_prefix}${stage}.png"
                
                try:
                    st.image(img_path, width=120) 
                except:
                    st.warning(f"Image introuvable : {img_path}")
                
                # Barres de progression et XP Exacts
                if stage >= 3:
                    st.progress(1.0)
                    st.success(f"Niveau Max ! ({current_xp} XP)")
                else:
                    base_xp = THRESHOLDS[stage]
                    next_xp = THRESHOLDS[stage + 1]
                    progress_pct = (current_xp - base_xp) / (next_xp - base_xp)
                    st.progress(progress_pct)
                    st.write(f"**{current_xp}** / {next_xp} XP")

st.divider()

# --- RECHERCHE ET HISTORIQUE (US-1.07, US-1.08, US-1.12) ---
col_hist, col_search = st.columns([2, 1])

with col_search:
    st.subheader("🔍 Recherche")
    search_query = st.text_input("Trouver un devoir (mot-clé, matière...)")

with col_hist:
    st.subheader("🕒 Activité Récente")
    if not history:
        st.info("Aucun devoir soumis pour le moment.")
    else:
        # Filtrage si recherche active
        filtered_history = history
        if search_query:
            query = search_query.lower()
            filtered_history = [
                h for h in history 
                if query in h.get("file_name", "").lower() or query in h.get("subject", "").lower()
            ]
        
        # Récupération des 5 derniers éléments (US-1.07)
        last_5 = list(reversed(filtered_history))[:5]
        
        if not last_5:
            st.warning("Aucun résultat ne correspond à ta recherche.")
        else:
            for item in last_5:
                with st.container(border=True):
                    # US-1.08: Timestamp exact
                    st.write(f"**{item.get('subject')}** | 📄 {item.get('file_name')} | 🟢 +{item.get('xp')} XP")
                    st.caption(f"🗓️ Soumis le : {item.get('date')} | Difficulté : {item.get('difficulty', 'Non précisée')}")