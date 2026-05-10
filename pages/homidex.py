import streamlit as st
import pandas as pd
from utils.db_manager import load_db, get_stage_from_xp
from utils.config import SUBJECTS_CONFIG, THRESHOLDS

st.set_page_config(page_title="Homidex & Profil", page_icon="🐉", layout="wide")
data = load_db()

@st.dialog("Fiche Détaillée")
def monster_card(subject, monster_data, current_xp, history):
    st.markdown(f"### {monster_data.get('name')} ({subject})")
    stage = get_stage_from_xp(current_xp)
    img_prefix = SUBJECTS_CONFIG.get(subject, "math")
    st.image(f"img/{img_prefix}${stage}.png", width=150)
    
    st.metric("XP Total", current_xp)
    if stage < 3:
        st.write(f"Prochaine évolution à {THRESHOLDS[stage+1]} XP")
    
    st.divider()
    st.write("**Derniers devoirs soumis :**")
    subj_history = [h for h in history if h["subject"] == subject][-5:] # Les 5 derniers
    if not subj_history:
        st.info("Aucun devoir soumis pour le moment.")
    else:
        for h in reversed(subj_history):
            fname = h['file_name'][:25] + "..." if len(h['file_name']) > 25 else h['file_name']
            st.caption(f"📄 {fname} | **+{h['xp']} XP**")

st.title("🐉 Homidex & Profil")

# --- GALERIE HOMIDEX ---
st.subheader("Ta Collection")
cols = st.columns(4)
for i, (subject, img_prefix) in enumerate(SUBJECTS_CONFIG.items()):
    with cols[i % 4]:
        current_xp = data.get("xp_by_subject", {}).get(subject, 0)
        monster_data = data.get("homidex", {}).get(subject, {})
        
        with st.container(border=True):
            st.write(f"**{subject}**")
            # Logique d'ombre demandée
            if current_xp == 0:
                st.image(f"img/{img_prefix}$1$shadow.png", width=100)
                st.caption("Non découvert")
            else:
                stage = monster_data.get("stage", 1)
                st.image(f"img/{img_prefix}${stage}.png", width=100)
                st.caption(f"{monster_data.get('name')} (Stade {stage})")
                
                if st.button("Voir", key=f"btn_{subject}"):
                    monster_card(subject, monster_data, current_xp, data.get("history", []))

# --- HISTORIQUE GLOBAL ---
st.divider()
st.subheader("Historique d'XP")

history = data.get("history", [])
if history:
    # On prépare la donnée pour un joli tableau Streamlit
    df = pd.DataFrame(history)
    # Tronquer les noms trop longs
    df["Fichier"] = df["file_name"].apply(lambda x: x[:30] + "..." if len(x) > 30 else x)
    df = df.rename(columns={"date": "Date", "subject": "Matière", "xp": "XP Gagné"})
    df = df.sort_index(ascending=False).head(10) # 10 derniers globaux
    
    st.dataframe(df[["Date", "Matière", "Fichier", "XP Gagné"]], use_container_width=True, hide_index=True)
else:
    st.info("Tu n'as pas encore soumis de devoirs.")