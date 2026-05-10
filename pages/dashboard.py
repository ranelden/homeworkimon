import streamlit as st
from utils.db_manager import load_db, get_stage_from_xp
from utils.config import SUBJECTS_CONFIG, THRESHOLDS

st.set_page_config(page_title="Dashboard - Homeworkimon", page_icon="🏠", layout="wide")

# --- INJECTION CSS (Pour l'effet Hover) ---
# On cible les conteneurs avec bordures de Streamlit pour ajouter une transition
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

st.title("🏠 Dashboard")

data = load_db()
user = data.get("user", {})

col_profile, col_stats = st.columns([2, 1])
with col_profile:
    st.write(f"### Bienvenue, {user.get('name', 'Joueur')} !")
    st.caption("Prêt à faire évoluer tes Homeworkimons aujourd'hui ?")

with col_stats:
    st.metric(label="🔥 Streak", value=f"{user.get('streak', 0)} Jours")

st.divider()

st.subheader("⚔️ Ton Équipe Active (Top 3)")

xp_data = data.get("xp_by_subject", {})
top_3 = sorted(xp_data.items(), key=lambda x: x[1], reverse=True)[:3]

if not top_3 or sum(xp for _, xp in top_3) == 0:
    st.info("Ton équipe est encore vide. Dépose un devoir dans le Habit Hub pour commencer ton aventure !")
else:
    cols = st.columns(3)
    for index, (subject, current_xp) in enumerate(top_3):
        with cols[index]:
            # Conteneur qui réagira au CSS "Hover"
            with st.container(border=True):
                # Récupération du nom du monstre depuis le JSON
                monster_data = data.get("homidex", {}).get(subject, {})
                monster_name = monster_data.get("name", "Monstre Inconnu")
                
                # Affichage du nom de la matière ET du monstre
                st.markdown(f"#### {subject}")
                st.caption(f"🐲 **{monster_name}**")
                
                stage = get_stage_from_xp(current_xp)
                img_prefix = SUBJECTS_CONFIG.get(subject, "math")
                img_path = f"img/{img_prefix}${stage}.png"
                
                # Image plus petite et centrée (width fixe au lieu de use_container_width)
                try:
                    st.image(img_path, width=120) 
                except:
                    st.warning(f"Image non trouvée : {img_path}")
                
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
st.caption("Homeworkimon v0.2.1 - UI Refinement")