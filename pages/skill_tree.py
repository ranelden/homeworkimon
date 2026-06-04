import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from utils.db_manager import load_db, get_skill_level, get_skill_xp_bounds
from utils.ai_mock import mock_get_advice
from utils.config import SKILL_BRANCHES

st.set_page_config(page_title="Skill Tree", page_icon="🌳", layout="wide")
data = load_db()
skills = data.get("skills", {})
history = data.get("history", [])

st.title("🌳 Skill Tree & Analyses")
st.write("Visualise ton évolution RPG et analyse tes performances.")

col_radar, col_branches = st.columns([2, 1])

# ==========================================
# US-5.01, 5.02, 5.03 : RADAR CHART DYNAMIQUE
# ==========================================
with col_radar:
    st.subheader("Radar de Compétences")
    
    if sum(skills.values()) > 0:
        # Trouver la compétence dominante (US-5.02)
        dominant_skill = max(skills, key=skills.get)
        
        # Mappage de couleurs selon la compétence dominante (US-5.02)
        color_map = {
            "Logique": "#3498db", "Créativité": "#9b59b6", "Structure": "#e67e22",
            "Originalité": "#f1c40f", "Raisonnement": "#34495e", "Mémoire": "#2ecc71",
            "Expression": "#e74c3c", "Précision": "#1abc9c"
        }
        radar_color = color_map.get(dominant_skill, "#ff4b4b")

        # Préparation des données pour le hover interactif (US-5.03)
        hover_texts = []
        for branch, xp in skills.items():
            lvl = get_skill_level(xp)
            _, next_bound = get_skill_xp_bounds(lvl)
            xp_to_next = int(next_bound - xp)
            hover_texts.append(f"<b>{branch}</b><br>XP Actuel: {int(xp)}<br>Manque {xp_to_next} XP pour Niv. {lvl+1}")

        df_skills = pd.DataFrame(dict(r=list(skills.values()), theta=list(skills.keys())))
        max_val = max(300, max(skills.values())) # Normalisation
        
        # Construction du graphique avec Plotly Graph Objects pour un contrôle total
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=df_skills['r'],
            theta=df_skills['theta'],
            fill='toself',
            fillcolor=radar_color,
            line=dict(color=radar_color),
            opacity=0.7,
            hovertemplate="%{customdata}<extra></extra>", # US-5.03
            customdata=hover_texts
        ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, max_val])),
            showlegend=False,
            margin=dict(l=40, r=40, t=20, b=20)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"🌟 Compétence dominante : **{dominant_skill}**")
        
    else:
        st.info("Le radar s'affichera dès que tu auras soumis ton premier devoir dans le Habit Hub !")

    # ==========================================
    # US-5.05, 5.06 : CONSEIL IA
    # ==========================================
    with st.container(border=True):
        st.markdown(f"💡 **Conseil de l'IA :** {mock_get_advice()}")
        if st.button("🔄 Rafraîchir l'analyse"):
            st.rerun()

# ==========================================
# NIVEAUX DÉTAILLÉS (LOGIQUE POLYNOMIALE)
# ==========================================
with col_branches:
    st.subheader("Niveaux Détaillés")
    for branch in SKILL_BRANCHES:
        xp = skills.get(branch, 0.0)
        lvl = get_skill_level(xp)
        cur_bound, next_bound = get_skill_xp_bounds(lvl)
        
        range_xp = next_bound - cur_bound
        progress = (xp - cur_bound) / range_xp if range_xp > 0 else 0
        
        st.write(f"**{branch}** - Niv. {lvl}")
        st.progress(min(max(progress, 0.0), 1.0))
        st.caption(f"{int(xp)} / {int(next_bound)} XP")

st.divider()

# ==========================================
# US-5.04 : TIMELINE (LINE CHART 7 DERNIERS JOURS)
# ==========================================
st.subheader("📈 Gains d'XP (7 Derniers Jours)")

if history:
    # Traitement des données pour récupérer les 7 derniers jours
    df_hist = pd.DataFrame(history)
    # Assurer que la date est au bon format
    df_hist['date_obj'] = pd.to_datetime(df_hist['date'].str[:10], errors='coerce')
    
    seven_days_ago = pd.to_datetime(datetime.now().date() - timedelta(days=6))
    df_recent = df_hist[df_hist['date_obj'] >= seven_days_ago].copy()
    
    if not df_recent.empty:
        # Grouper par date et additionner les XP
        df_trend = df_recent.groupby('date_obj')['xp'].sum().reset_index()
        df_trend.rename(columns={'date_obj': 'Date', 'xp': 'XP Gagné'}, inplace=True)
        
        fig2 = px.line(
            df_trend, x="Date", y="XP Gagné", 
            markers=True, 
            text="XP Gagné"
        )
        fig2.update_traces(
            line_color="#2ecc71", 
            textposition="top center",
            marker=dict(size=8)
        )
        fig2.update_layout(yaxis_title="XP Total", xaxis_title="Date")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Aucune activité enregistrée sur les 7 derniers jours.")
else:
    st.info("Soumets des devoirs pour voir ton évolution s'afficher ici !")