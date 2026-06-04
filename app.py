import streamlit as st

# ==========================================
# CONFIGURATION GLOBALE
# ==========================================
# st.set_page_config doit toujours être la première commande Streamlit exécutée.
st.set_page_config(
    page_title="Homeworkimon",
    page_icon="👾",
    layout="wide",
    initial_sidebar_state="expanded" # Gère la responsivité native (US-1.03)
)

# ==========================================
# ROUTEUR ET NAVIGATION (US-1.01, US-1.02)
# ==========================================
# Définition de l'arborescence des pages de l'application
pages = {
    "Menu Principal": [
        st.Page("pages/dashboard.py", title="Dashboard", icon="🏠"),
        st.Page("pages/habit_hub.py", title="Habit Hub", icon="📝"),
        st.Page("pages/homidex.py", title="Homidex & Profil", icon="🐉"),
        st.Page("pages/skill_tree.py", title="Skill Tree", icon="🌳"),
    ]
}

# Initialisation du moteur de navigation natif de Streamlit
pg = st.navigation(pages)

# Lancement de la page sélectionnée
pg.run()