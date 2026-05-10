import streamlit as st
from utils.db_manager import load_db, add_xp
from utils.config import SUBJECTS_CONFIG
from utils.ai_mock import extract_text, build_prompt, mock_evaluate_effort

st.set_page_config(page_title="Habit Hub - Dépôt", page_icon="📝", layout="wide")

@st.dialog("🌟 ÉVOLUTION !")
def show_evolution(subject, new_stage):
    st.balloons()
    st.write(f"### Incroyable !")
    st.write(f"Ton Homeworkimon de **{subject}** a évolué vers le **Stade {new_stage}** !")
    
    img_prefix = SUBJECTS_CONFIG.get(subject, "math")
    img_path = f"img/{img_prefix}${new_stage}.png"
    try:
        # Image réduite dans la pop-up
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
        selected_subject = st.selectbox("Matière du devoir", ["Choisir..."] + subjects)
        instructions = st.text_area("Consignes du professeur", placeholder="Colle ici l'énoncé ou les attentes...", height=150)
        
        word_count = len(instructions.split())
        st.caption(f"Nombre de mots : {word_count}")

    with col2:
        uploaded_file = st.file_uploader("Ton fichier (PDF ou Texte)", type=["pdf", "txt"])
        st.info("Limite de taille : 5 Mo. Formats : .pdf, .txt")

    submit_btn = st.button("Analyser mon travail ✨", type="primary", use_container_width=True)

if submit_btn:
    if selected_subject == "Choisir...": st.error("Choisis une matière !")
    elif not instructions.strip(): st.error("Il manque les consignes.")
    elif not uploaded_file: st.error("Il manque le fichier !")
    else:
        with st.spinner(f"L'IA analyse ton devoir..."):
            try:
                # Mock AI mis à jour
                text_content = extract_text(uploaded_file)
                prompt = build_prompt(instructions, text_content)
                xp_gained, distribution = mock_evaluate_effort(prompt)
                
                # Sauvegarde en base avec le nom du fichier et la distrib
                file_name = uploaded_file.name
                new_total, evolved, stage = add_xp(selected_subject, xp_gained, file_name, distribution)
                
                # Succès
                st.success(f"Bravo ! +{xp_gained} XP en {selected_subject}.")
                
                # Message détaillé des branches
                dist_str = ", ".join([f"{b} (+{int(xp_gained*w)})" for b, w in distribution.items()])
                st.caption(f"Compétences entraînées : {dist_str}")

                if evolved:
                    show_evolution(selected_subject, stage)
                
            except Exception as e:
                st.error("Une erreur est survenue.")
                
st.divider()
with st.expander("Un problème avec l'évaluation ?"):
    st.write("Si le score d'XP te semble injuste par rapport à ton effort, signale-le ici.")
    if st.button("🚩 Signaler l'évaluation"):
        st.toast("Signalement pris en compte. Nos développeurs vont ajuster l'IA.")

