import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.db_manager import load_db, get_skill_level, get_skill_xp_bounds
from utils.ai_mock import mock_get_advice

st.set_page_config(page_title="Skill Tree", page_icon="🌳", layout="wide")
data = load_db()
skills = data.get("skills", {})

st.title("🌳 Skill Tree & Analyses")

col_radar, col_branches = st.columns([2, 1])

with col_radar:
    st.subheader("Radar de Compétences")
    
    # Préparation des données pour le radar
    df_skills = pd.DataFrame(dict(
        r=list(skills.values()),
        theta=list(skills.keys())
    ))
    
    # Logique de normalisation dynamique demandée (Max = 300 ou la plus haute branche)
    max_val = max(300, max(skills.values()) if skills else 300)
    
    fig = px.line_polar(df_skills, r='r', theta='theta', line_close=True)
    fig.update_traces(fill='toself', line_color='#4CAF50')
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max_val])),
        showlegend=False,
        margin=dict(l=40, r=40, t=20, b=20)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Conseil IA sous le graph
    with st.container(border=True):
        st.markdown(f"💡 **Conseil de l'IA :** {mock_get_advice()}")
        if st.button("Demander un autre conseil"):
            st.rerun()

with col_branches:
    st.subheader("Niveaux")
    for branch, xp in skills.items():
        lvl = get_skill_level(xp)
        cur_bound, next_bound = get_skill_xp_bounds(lvl)
        
        # Pourcentage pour la barre de progression (sécurité division par zéro)
        range_xp = next_bound - cur_bound
        progress = (xp - cur_bound) / range_xp if range_xp > 0 else 0
        
        st.write(f"**{branch}** - Niv. {lvl}")
        st.progress(min(max(progress, 0.0), 1.0))
        st.caption(f"{int(xp)} / {int(next_bound)} XP")

st.divider()

# --- TIMELINE ---
st.subheader("Gains d'XP sur les 7 derniers jours")
history = data.get("history", [])

if history:
    df_hist = pd.DataFrame(history)
    df_hist['date'] = pd.to_datetime(df_hist['date'])
    
    # Grouper par date et sommer l'XP
    df_trend = df_hist.groupby('date')['xp'].sum().reset_index()
    
    fig2 = px.line(df_trend, x="date", y="xp", markers=True, title="Activité Récente")
    fig2.update_traces(line_color="#ff4b4b")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Soumets des devoirs pour voir ton activité s'afficher ici !")