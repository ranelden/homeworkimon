import streamlit as st
from utils.db_manager import load_db, add_xp
from utils.config import SUBJECTS_CONFIG
from utils.ai_mock import extract_text, build_prompt, mock_evaluate_effort

st.set_page_config(page_title="Habit Hub - Dépôt", page_icon="📝", layout="wide")

# --- MODALE D'ÉVOLUTION (US-3.09) ---
@st.dialog("🌟 ÉVOLUTION !")
def show_evolution(subject, new_stage):
    st.balloons()
    st.write(f"### Incroyable !")
    st.write(f"Ton Homeworkimon de **{subject}** a évolué vers le **Stade {new_stage}** !")
    
    img_prefix = SUBJECTS_CONFIG.get(subject, "math")
    img_path = f"img/{img_prefix}${new_stage}.png"
    try:
        st.image(img_path, width=200)
    except:
        st.info("(Image de l'évolution)")
    
    if st.button("Génial !"):
        st.rerun()

st.title("📝 Habit Hub")
st.write("Transforme tes efforts scolaires en puissance de monstre.")

subjects = list(SUBJECTS_CONFIG.keys())

with st.container(border=True):
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # US-2.01, US-2.02: Selectbox avec recherche native
        selected_subject = st.selectbox("Matière du devoir", ["Choisir..."] + subjects)
        
        # US-2.13: Tag de difficulté perçue
        difficulty = st.radio("Difficulté perçue", ["Easy", "Medium", "Hard"], horizontal=True)
        
        # US-2.03: Champ de texte large
        instructions = st.text_area("Consignes du professeur", placeholder="Colle ici l'énoncé ou les attentes...", height=150)
        
        # US-2.04: Compteur de mots en temps réel
        word_count = len(instructions.split())
        st.caption(f"Nombre de mots : {word_count}")

    with col2:
        # US-2.05, US-2.06, US-2.08, US-3.12: Uploader natif drag & drop, restreint PDF/TXT
        uploaded_file = st.file_uploader("Ton fichier (PDF ou Texte)", type=["pdf", "txt"])
        st.info("Limite de taille : 5 Mo. Formats supportés : .pdf, .txt")

    submit_btn = st.button("Analyser mon travail ✨", type="primary", use_container_width=True)

# --- LOGIQUE DE SOUMISSION ---
if submit_btn:
    # US-2.07: Validations strictes
    if selected_subject == "Choisir...":
        st.error("N'oublie pas de choisir une matière !")
    elif not instructions.strip():
        st.error("L'IA a besoin des consignes pour t'évaluer.")
    elif not uploaded_file:
        st.error("Il manque ton fichier !")
    # US-3.11: Limite stricte de 5 Mo
    elif uploaded_file.size > 5 * 1024 * 1024:
        st.error("Le fichier dépasse la limite autorisée de 5Mo.")
    else:
        # US-2.09: Icône de chargement stylisée
        with st.spinner(f"L'IA analyse ton devoir de {selected_subject}..."):
            try:
                # Simulation IA
                text_content = extract_text(uploaded_file)
                prompt = build_prompt(instructions, text_content)
                base_xp, dist, reasoning = mock_evaluate_effort(prompt)
                
                # Mise à jour DB
                new_total, evolved, stage, final_xp = add_xp(selected_subject, base_xp, uploaded_file.name, dist, difficulty)
                
                # US-2.10: Écran de succès
                st.success(f"🎉 Bravo ! Ton travail a été validé. +{final_xp} XP ({difficulty}).")
                
                # US-3.13: Raisonnement de l'IA
                st.info(f"🤖 **Retour de l'IA :** {reasoning}")
                
                res_col1, res_col2 = st.columns([1, 3])
                with res_col1:
                    # US-2.11: Avatar de la matière spécifique affiché sur l'écran de récompense
                    img_prefix = SUBJECTS_CONFIG.get(selected_subject, "math")
                    try:
                        st.image(f"img/{img_prefix}${stage}.png", width=100)
                    except:
                        pass
                with res_col2:
                    st.metric("Nouveau Total XP", f"{new_total} XP", delta=f"+{final_xp}")
                    dist_str = ", ".join([f"{b} (+{int(final_xp*w)})" for b, w in dist.items()])
                    st.caption(f"🌳 Compétences entraînées : {dist_str}")

                # US-3.09: Trigger modale d'évolution
                if evolved:
                    show_evolution(selected_subject, stage)
                
                # US-2.12: Bouton de soumission multiple
                st.divider()
                if st.button("🔄 Faire une nouvelle soumission"):
                    st.rerun()

            except Exception as e:
                st.error("Une erreur système est survenue. Merci de réessayer.")

# --- ZONE DE SIGNALEMENT (US-3.10) ---
st.divider()
with st.expander("Un problème avec l'évaluation ?"):
    st.write("Si le score d'XP te semble injuste par rapport à ton effort, signale-le ici.")
    if st.button("🚩 Signaler l'évaluation"):
        st.toast("Signalement pris en compte ! Nos développeurs vont ajuster l'IA.", icon="✅")