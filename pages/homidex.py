import streamlit as st
import pandas as pd
import urllib.parse
from utils.db_manager import load_db, reset_db, save_db, get_stage_from_xp
from utils.config import SUBJECTS_CONFIG, THRESHOLDS

st.set_page_config(page_title="Homidex & Profil", page_icon="🐉", layout="wide")

# --- MODALE CARTE DÉTAILLÉE DE L'AVATAR (US-4.14, 4.07, 4.15) ---
@st.dialog("Détails du Homeworkimon")
def monster_detail_card(subject, current_xp, monster_data, history):
    stage = monster_data.get("stage", 1)
    img_prefix = SUBJECTS_CONFIG.get(subject, "math")
    
    # US-4.07 : Nom unique de l'avatar
    custom_name = monster_data.get("custom_name", monster_data.get("name"))
    st.markdown(f"### {custom_name} ({subject})")
    
    col_img, col_info = st.columns([1, 1])
    with col_img:
        try: st.image(f"img/{img_prefix}${stage}.png", width=150)
        except: st.info("Image Actuelle")
    with col_info:
        st.metric("Niveau Actuel", f"Stade {stage}")
        st.metric("XP Total", current_xp)
        
        # Formulaire pour renommer l'avatar (US-4.07)
        new_name = st.text_input("Renommer ton monstre :", value=custom_name, key=f"rename_{subject}")
        if st.button("Sauvegarder le nom", key=f"btn_rename_{subject}"):
            data = load_db()
            data["homidex"][subject]["custom_name"] = new_name
            save_db(data)
            st.rerun()

    # US-4.15 : Silhouette de l'évolution future
    if stage < 3:
        st.divider()
        st.write("**Prochaine évolution mystère :**")
        st.caption(f"XP requis : {THRESHOLDS[stage+1]} XP")
        try:
            st.image(f"img/{img_prefix}${stage+1}$shadow.png", width=80)
        except:
            st.info("👤 Silhouette mystère")
    
    # Historique spécifique à la matière (US-4.14)
    st.divider()
    st.write("**Historique de tes devoirs soumis :**")
    subj_history = [h for h in history if h.get("subject") == subject]
    if subj_history:
        for h in reversed(subj_history[-3:]): # Les 3 derniers
            st.caption(f"📄 {h.get('file_name')} | +{h.get('xp')} XP")
    else:
        st.info("Aucun devoir.")

# --- CHARGEMENT DATA & UI ---
data = load_db()
st.title("🐉 Homidex & Profil")

# Création des 4 onglets
tab_galerie, tab_table, tab_profil, tab_settings = st.tabs([
    "Galerie Homidex", "Classement XP", "Carte Joueur & Badges", "Paramètres"
])

# ==========================================
# ONGLET 1 : GALERIE (US-4.12, 4.13)
# ==========================================
with tab_galerie:
    st.subheader("Ta Collection de Monstres")
    cols = st.columns(4)
    for i, (subject, img_prefix) in enumerate(SUBJECTS_CONFIG.items()):
        with cols[i % 4]:
            current_xp = data.get("xp_by_subject", {}).get(subject, 0)
            monster_data = data.get("homidex", {}).get(subject, {})
            
            with st.container(border=True):
                st.write(f"**{subject}**")
                if current_xp == 0:
                    # US-4.13: Silhouette non découverte
                    try:
                        st.image(f"img/{img_prefix}$1$shadow.png", width=100)
                    except:
                        st.info("Ombre")
                    st.caption("Non découvert")
                else:
                    stage = monster_data.get("stage", 1)
                    custom_name = monster_data.get("custom_name", monster_data.get("name"))
                    try:
                        st.image(f"img/{img_prefix}${stage}.png", width=100)
                    except:
                        st.info("Image")
                    st.caption(f"{custom_name} (Lvl {stage})")
                    
                    # US-4.14: Ouverture de la carte détaillée
                    if st.button("Détails", key=f"details_{subject}"):
                        monster_detail_card(subject, current_xp, monster_data, data.get("history", []))

# ==========================================
# ONGLET 2 : CLASSEMENT XP (US-4.01, 4.02)
# ==========================================
with tab_table:
    st.subheader("📊 Tableau Récapitulatif d'XP")
    xp_dict = data.get("xp_by_subject", {})
    if xp_dict:
        # Streamlit DataFrame gère le tri nativement (US-4.02)
        df_xp = pd.DataFrame(list(xp_dict.items()), columns=["Matière", "Total XP"])
        st.dataframe(df_xp, hide_index=True, use_container_width=True)
    else:
        st.info("Aucune donnée d'XP pour le moment.")

# ==========================================
# ONGLET 3 : PROFIL & BADGES (US-6.03 à 6.05, 4.03, 4.04, 4.05, 4.11, 5.07)
# ==========================================
with tab_profil:
    st.subheader("💳 Ta Carte Joueur")
    
    history = data.get("history", [])
    total_dev = len(history)
    streak = data.get("user", {}).get("streak", 0)
    nickname = data.get("settings", {}).get("nickname", "Étudiant")
    title = data.get("settings", {}).get("title", "Novice")
    
    # US-6.03: Player Card Visuelle
    with st.container(border=True):
        col_card1, col_card2 = st.columns([1, 2])
        with col_card1:
            st.image("https://api.dicebear.com/7.x/bottts/svg?seed=" + nickname, width=100)
        with col_card2:
            st.markdown(f"### {nickname}")
            st.markdown(f"*{title}*")
            st.write(f"🔥 Streak: {streak} jours | 📚 Devoirs: {total_dev}")
        
        c_down, c_share1, c_share2 = st.columns(3)
        
        # US-6.04: Bouton Télécharger (Format TXT textuel pour le MVP)
        card_data = f"Joueur: {nickname}\nTitre: {title}\nStreak: {streak}\nDevoirs Soumis: {total_dev}"
        c_down.download_button("⬇️ Exporter Carte", card_data, "player_card.txt")
        
        # US-6.05: Partages réseaux (Liens pré-générés)
        share_text = urllib.parse.quote(f"J'ai un streak de {streak} jours sur Homeworkimon ! 🔥")
        c_share1.markdown(f"[🐦 Partager sur X/Twitter](https://twitter.com/intent/tweet?text={share_text})")
        c_share2.markdown(f"[💬 Lancer Discord](https://discord.com/app)")

    st.divider()
    
    st.subheader("🏅 Vitrine de Badges")
    
    # Logique des badges
    b1_unlocked = total_dev >= 1
    b1_date = history[0]["date"].split(" ")[0] if b1_unlocked else ""
    
    b2_unlocked = streak >= 3
    b2_date = data["user"].get("last_date", "Récemment") if b2_unlocked else ""
    
    b3_unlocked = any(xp >= 300 for xp in data.get("xp_by_subject", {}).values())
    b3_date = "Récemment" if b3_unlocked else ""

    b_col1, b_col2, b_col3 = st.columns(3)
    
    # US-4.03 (Succès), US-4.04 (Grisé), US-4.05 (Tooltip "help"), US-4.11 (Date)
    with b_col1:
        if b1_unlocked: st.success(f"🎯 Premier Sang\n\nDébloqué le : {b1_date}")
        else: st.button("🔒 Premier Sang", help="Soumettre 1 premier devoir.", disabled=True, key="bdg1")
            
    with b_col2:
        if b2_unlocked: st.success(f"🔥 En Feu\n\nDébloqué le : {b2_date}")
        else: st.button("🔒 En Feu", help="Atteindre un Streak de 3 jours.", disabled=True, key="bdg2")
            
    with b_col3:
        if b3_unlocked: st.success(f"🧬 Évolution\n\nDébloqué le : {b3_date}")
        else: st.button("🔒 Évolution", help="Faire évoluer un monstre au stade 2.", disabled=True, key="bdg3")

    st.divider()
    # US-5.07 : Export CSV
    if history:
        csv = pd.DataFrame(history).to_csv(index=False).encode('utf-8')
        st.download_button("📊 Exporter mon historique d'XP (CSV)", csv, "homeworkimon_data.csv", "text/csv")

# ==========================================
# ONGLET 4 : PARAMÈTRES (US-4.06, 4.09, 4.10, 6.06, 4.08)
# ==========================================
with tab_settings:
    st.subheader("⚙️ Paramètres & Personnalisation")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        # US-4.06: Choix du pseudo
        new_name = st.text_input("Ton Pseudo", value=data.get("settings", {}).get("nickname", "Étudiant"))
        
        # US-4.10: Choix du Titre débloqué
        titles = ["Novice", "L'Érudit", "Le Chercheur", "Maître des Monstres"]
        current_title = data.get("settings", {}).get("title", "Novice")
        new_title = st.selectbox("Titre affiché", titles, index=titles.index(current_title) if current_title in titles else 0)
    
    with col_s2:
        # US-4.09: Theme Color
        theme_color = st.color_picker("Couleur du Thème", "#ff4b4b")
        
        # US-6.06: Toggle Mode Sombre
        dark_mode = st.toggle("Mode Sombre (UI Native)")
        
    if st.button("Sauvegarder le profil", type="primary"):
        data["settings"]["nickname"] = new_name
        data["settings"]["title"] = new_title
        save_db(data)
        st.success("Profil mis à jour !")
        st.rerun()
        
    st.divider()
    # US-4.08: Reset Data (Pour tester les onboarding/silhouettes)
    st.error("Zone de Danger (Testeurs)")
    if st.button("🗑️ Reset Data (Supprimer toute la progression)"):
        reset_db()
        st.toast("Base de données réinitialisée !")
        st.rerun()