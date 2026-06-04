import streamlit as st
import pandas as pd
import urllib.parse
from utils.db_manager import load_db, reset_db, save_db, get_stage_from_xp
from utils.config import SUBJECTS_CONFIG, THRESHOLDS

st.set_page_config(page_title="Homidex & Profil", page_icon="🐉", layout="wide")

# --- MODALE CARTE DÉTAILLÉE DE L'AVATAR ---
@st.dialog("Détails du Homeworkimon")
def monster_detail_card(subject, current_xp, monster_data, history):
    stage = monster_data.get("stage", 1)
    img_prefix = SUBJECTS_CONFIG.get(subject, "math")
    
    custom_name = monster_data.get("custom_name", monster_data.get("name"))
    st.markdown(f"### {custom_name} ({subject})")
    
    col_img, col_info = st.columns([1, 1])
    with col_img:
        try: st.image(f"img/{img_prefix}${stage}.png", width=150)
        except: st.info("Image Actuelle")
    with col_info:
        st.metric("Niveau Actuel", f"Stade {stage}")
        st.metric("XP Total", current_xp)
        
        new_name = st.text_input("Renommer ton monstre :", value=custom_name, key=f"rename_{subject}")
        if st.button("Sauvegarder le nom", key=f"btn_rename_{subject}"):
            data = load_db()
            data["homidex"][subject]["custom_name"] = new_name
            save_db(data)
            st.rerun()

    # Prochaine évolution (Rappel dans la carte)
    if stage < 3:
        st.divider()
        st.write("**Prochaine évolution :**")
        st.caption(f"XP requis : {THRESHOLDS[stage+1]} XP")
        try:
            st.image(f"img/{img_prefix}${stage+1}$shadow.png", width=80)
        except:
            st.info("👤 Silhouette mystère")
    
    st.divider()
    st.write("**Historique de tes devoirs soumis :**")
    subj_history = [h for h in history if h.get("subject") == subject]
    if subj_history:
        for h in reversed(subj_history[-3:]):
            st.caption(f"📄 {h.get('file_name')} | +{h.get('xp')} XP")
    else:
        st.info("Aucun devoir.")

# --- CHARGEMENT DATA & UI ---
data = load_db()
st.title("🐉 Homidex & Profil")

tab_galerie, tab_table, tab_profil, tab_settings = st.tabs([
    "Galerie Homidex", "Classement XP", "Carte Joueur & Badges", "Paramètres"
])

# ==========================================
# ONGLET 1 : GALERIE (US-4.12, 4.13, 4.15)
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
                    
                    # US-4.15: AFFICHAGE CÔTE À CÔTE DE L'AVATAR ET DE L'OMBRE FUTURE
                    img_cols = st.columns(2)
                    with img_cols[0]:
                        try:
                            st.image(f"img/{img_prefix}${stage}.png", use_container_width=True)
                        except:
                            st.info("Image")
                    
                    with img_cols[1]:
                        if stage < 3:
                            try:
                                # On affiche le stade suivant en mode "ombre"
                                st.image(f"img/{img_prefix}${stage+1}$shadow.png", use_container_width=True)
                            except:
                                st.info("Ombre")
                    
                    st.caption(f"{custom_name} (Lvl {stage})")
                    
                    if st.button("Détails", key=f"details_{subject}", use_container_width=True):
                        monster_detail_card(subject, current_xp, monster_data, data.get("history", []))

# ==========================================
# ONGLET 2 : CLASSEMENT XP
# ==========================================
with tab_table:
    st.subheader("📊 Tableau Récapitulatif d'XP")
    xp_dict = data.get("xp_by_subject", {})
    if xp_dict:
        df_xp = pd.DataFrame(list(xp_dict.items()), columns=["Matière", "Total XP"])
        st.dataframe(df_xp, hide_index=True, use_container_width=True)
    else:
        st.info("Aucune donnée d'XP pour le moment.")

# ==========================================
# ONGLET 3 : PROFIL & BADGES
# ==========================================
with tab_profil:
    st.subheader("💳 Ta Carte Joueur")
    
    history = data.get("history", [])
    total_dev = len(history)
    streak = data.get("user", {}).get("streak", 0)
    nickname = data.get("settings", {}).get("nickname", "Étudiant")
    title = data.get("settings", {}).get("title", "Novice")
    
    with st.container(border=True):
        col_card1, col_card2 = st.columns([1, 2])
        with col_card1:
            st.image("https://api.dicebear.com/7.x/bottts/svg?seed=" + nickname, width=100)
        with col_card2:
            st.markdown(f"### {nickname}")
            st.markdown(f"*{title}*")
            st.write(f"🔥 Streak: {streak} jours | 📚 Devoirs: {total_dev}")
        
        c_down, c_share1, c_share2 = st.columns(3)
        card_data = f"Joueur: {nickname}\nTitre: {title}\nStreak: {streak}\nDevoirs Soumis: {total_dev}"
        c_down.download_button("⬇️ Exporter Carte", card_data, "player_card.txt")
        share_text = urllib.parse.quote(f"J'ai un streak de {streak} jours sur Homeworkimon ! 🔥")
        c_share1.markdown(f"[🐦 Partager sur X](https://twitter.com/intent/tweet?text={share_text})")
        c_share2.markdown(f"[💬 Lancer Discord](https://discord.com/app)")

    st.divider()
    st.subheader("🏅 Vitrine de Badges")
    
    b1_unlocked = total_dev >= 1
    b1_date = history[0]["date"].split(" ")[0] if b1_unlocked else ""
    
    b2_unlocked = streak >= 3
    b2_date = data["user"].get("last_date", "Récemment") if b2_unlocked else ""
    
    b3_unlocked = any(xp >= 300 for xp in data.get("xp_by_subject", {}).values())
    b3_date = "Récemment" if b3_unlocked else ""

    b_col1, b_col2, b_col3 = st.columns(3)
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
    if history:
        csv = pd.DataFrame(history).to_csv(index=False).encode('utf-8')
        st.download_button("📊 Exporter mon historique d'XP (CSV)", csv, "homeworkimon_data.csv", "text/csv")

# ==========================================
# ONGLET 4 : PARAMÈTRES
# ==========================================
with tab_settings:
    st.subheader("⚙️ Paramètres & Personnalisation")
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        new_name = st.text_input("Ton Pseudo", value=data.get("settings", {}).get("nickname", "Étudiant"))
        titles = ["Novice", "L'Érudit", "Le Chercheur", "Maître des Monstres"]
        current_title = data.get("settings", {}).get("title", "Novice")
        new_title = st.selectbox("Titre affiché", titles, index=titles.index(current_title) if current_title in titles else 0)
    
    with col_s2:
        theme_color = st.color_picker("Couleur du Thème", "#ff4b4b")
        dark_mode = st.toggle("Mode Sombre (UI Native)")
        
    if st.button("Sauvegarder le profil", type="primary"):
        data["settings"]["nickname"] = new_name
        data["settings"]["title"] = new_title
        save_db(data)
        st.success("Profil mis à jour !")
        st.rerun()
        
    st.divider()
    st.error("Zone de Danger (Testeurs)")
    if st.button("🗑️ Reset Data (Supprimer toute la progression)"):
        reset_db()
        st.toast("Base de données réinitialisée !")
        st.rerun()