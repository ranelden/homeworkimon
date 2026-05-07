import streamlit as st

# Configuration globale de l'app
st.set_page_config(page_title="Homeworkimon", page_icon="👾", layout="wide")

# Configuration du menu de navigation latéral
pages = {
    "Menu Principal": [
        st.Page("pages/dashboard.py", title="Dashboard", icon="🏠"),
        st.Page("pages/habit_hub.py", title="Habit Hub", icon="📝"),
        st.Page("pages/homidex.py", title="Homidex & Profil", icon="🐉"),
        st.Page("pages/skill_tree.py", title="Skill Tree", icon="🌳"),
    ]
}

pg = st.navigation(pages)
pg.run()