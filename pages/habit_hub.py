import streamlit as st
from utils.db_manager import load_db, add_xp
from utils.ai_mock import mock_evaluate_effort

st.title("📝 Habit Hub (Dépôt)")
st.write("Déposez votre devoir pour gagner de l'XP et faire évoluer vos monstres !")

data = load_db()
subjects = list(data.get("xp_by_subject", {}).keys())

# Formulaire de dépôt
with st.container():
    selected_subject = st.selectbox("Choisissez la matière ciblée", [""] + subjects)
    
    instructions = st.text_area("Consignes du professeur", placeholder="Collez ici les consignes de votre devoir...")
    
    uploaded_file = st.file_uploader("Uploadez votre devoir (PDF, TXT - Max 5Mo)", type=["pdf", "txt"])

    if st.button("Soumettre et évaluer avec l'IA", type="primary"):
        # Validation des champs
        if not selected_subject:
            st.error("Veuillez sélectionner une matière.")
        elif not instructions.strip():
            st.error("Veuillez entrer les consignes du professeur.")
        elif not uploaded_file:
            st.error("Veuillez uploader un fichier.")
        else:
            # Validation de la taille du fichier (5 Mo = 5 * 1024 * 1024 bytes)
            if uploaded_file.size > 5 * 1024 * 1024:
                st.error("Le fichier dépasse la limite autorisée de 5Mo.")
            else:
                # Traitement simulé
                with st.spinner("L'IA analyse votre effort..."):
                    xp_gained = mock_evaluate_effort()
                    new_total_xp = add_xp(selected_subject, xp_gained)
                
                st.success(f"🎉 Félicitations ! Vous avez gagné **{xp_gained} XP** en {selected_subject} !")
                st.info(f"Total XP {selected_subject} : {new_total_xp}")