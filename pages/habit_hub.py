import streamlit as st
from utils.db_manager import load_db, add_xp
from utils.config import SUBJECTS_CONFIG
from utils.ai_mock import extract_text, build_prompt, mock_evaluate_effort

st.set_page_config(page_title="Habit Hub - Submission", page_icon="📝", layout="wide")

# --- EVOLUTION MODAL (US-3.09) ---
@st.dialog("🌟 EVOLUTION!")
def show_evolution(subject, new_stage):
    st.balloons()
    st.write(f"### Amazing!")
    st.write(f"Your Homeworkimon for **{subject}** evolved to **Stage {new_stage}**!")
    
    img_prefix = SUBJECTS_CONFIG.get(subject, "math")
    img_path = f"img/{img_prefix}${new_stage}.png"
    try:
        st.image(img_path, width=200)
    except:
            st.info("(Evolution image)")

st.title("📝 Habit Hub")
st.write("Turn your school work into monster power.")

subjects = list(SUBJECTS_CONFIG.keys())

with st.container(border=True):
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # US-2.01, US-2.02: Selectbox avec recherche native
        selected_subject = st.selectbox("Assignment subject", ["Choose..."] + subjects)
        
        # US-2.13: Tag de difficulté perçue
        difficulty = st.radio("Perceived difficulty", ["Easy", "Medium", "Hard"], horizontal=True)
        
        # US-2.03: Large text field
        instructions = st.text_area("Teacher instructions", placeholder="Paste the prompt or expectations here...", height=150)
        
        # US-2.04: Live word counter
        word_count = len(instructions.split())
        st.caption(f"Word count: {word_count}")

    with col2:
        # US-2.05, US-2.06, US-2.08, US-3.12: Native drag & drop uploader, restricted to PDF/TXT
        uploaded_file = st.file_uploader("Your file (PDF or TXT)", type=["pdf", "txt"])
        st.info("Size limit: 5 MB. Supported formats: .pdf, .txt")

    submit_btn = st.button("Analyze my work ✨", type="primary", use_container_width=True)

# --- SUBMISSION LOGIC ---
if submit_btn:
    # US-2.07: Strict validations
    if selected_subject == "Choose...":
        st.error("Please choose a subject!")
    elif not instructions.strip():
        st.error("The AI needs the instructions to assess your work.")
    elif not uploaded_file:
        st.error("Your file is missing!")
    # US-3.11: Strict 5 MB limit
    elif uploaded_file.size > 5 * 1024 * 1024:
        st.error("The file exceeds the 5 MB limit.")
    else:
        # US-2.09: Styled loading icon
        with st.spinner(f"The AI is analyzing your {selected_subject} assignment..."):
            try:
                # Simulation IA
                text_content = extract_text(uploaded_file)
                prompt = build_prompt(instructions, text_content)
                base_xp, dist, reasoning = mock_evaluate_effort(prompt)
                
                # Mise à jour DB
                new_total, evolved, stage, final_xp = add_xp(selected_subject, base_xp, uploaded_file.name, dist, difficulty)
                
                # US-2.10: Success screen
                st.success(f"🎉 Great job! Your work was validated. +{final_xp} XP ({difficulty}).")
                
                # US-3.13: AI reasoning
                st.info(f"🤖 **AI feedback:** {reasoning}")
                
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
                    st.caption(f"🌳 Skills trained: {dist_str}")

                # US-3.09: Trigger modale d'évolution
                if evolved:
                    show_evolution(selected_subject, stage)
                
                # US-2.12: Bouton de soumission multiple
                st.divider()
                if st.button("🔄 Submit another assignment"):
                    st.rerun()

            except Exception as e:
                st.error("A system error occurred. Please try again.")

# --- ZONE DE SIGNALEMENT (US-3.10) ---
st.divider()
with st.expander("Un problème avec l'évaluation ?"):
    st.write("Si le score d'XP te semble injuste par rapport à ton effort, signale-le ici.")
    if st.button("🚩 Signaler l'évaluation"):
        st.toast("Signalement pris en compte ! Nos développeurs vont ajuster l'IA.", icon="✅")