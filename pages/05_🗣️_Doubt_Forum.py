import streamlit as st
import database as db
from datetime import datetime

# Initialize DB
db.init_db()

# --- PAGE CONFIG ---
st.set_page_config(page_title="Doubt Forum | PEC", page_icon="🗣️", layout="wide")

st.title("🗣️ PEC Student Community")
st.caption("Stuck on a problem? Ask your seniors or batchmates here.")

# --- SIDEBAR ---
with st.sidebar:
    if "user" in st.session_state:
        st.success(f"👤 Logged in as: {st.session_state['user']}")
    else:
        st.warning("🔒 Login to Post/Reply")
    
    st.divider()
    filter_subject = st.selectbox("Filter Topics:", ["All", "M1 (Matrices)", "Java", "Python", "BEE", "Chemistry", "General"])

# --- TAB LAYOUT ---
tab1, tab2 = st.tabs(["💬 Browse Doubts", "➕ Ask a Doubt"])

# ==========================================
# TAB 1: BROWSE & ANSWER
# ==========================================
with tab1:
    st.subheader(f"Recent Discussions in {filter_subject}")
    
    # Fetch questions
    questions = db.get_questions(filter_subject)
    
    if not questions:
        st.info("No doubts asked yet. Be the first!")
    else:
        for q in questions:
            # q = (id, username, subject, text, timestamp)
            q_id = q[0]
            q_user = q[1]
            q_sub = q[2]
            q_text = q[3]
            q_time = q[4]
            
            with st.container(border=True):
                c1, c2 = st.columns([1, 5])
                with c1:
                    st.markdown(f"**@{q_user}**")
                    st.caption(f"📅 {q_time[:10]}")
                    st.caption(f"🏷️ {q_sub}")
                with c2:
                    # Use markdown to preserve line breaks in the question text
                    st.markdown(f"### {q_text.replace(chr(10), '<br>')}", unsafe_allow_html=True)
                    
                    # Fetch Answers
                    answers = db.get_answers(q_id)
                    
                    with st.expander(f"💬 View {len(answers)} Replies"):
                        # Show existing answers
                        for ans in answers:
                            # Use markdown to preserve line breaks in answers
                            formatted_ans = ans[3].replace("\n", "<br>")
                            st.markdown(f"""
                            <div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 5px;'>
                                <b>@{ans[2]}:</b><br>{formatted_ans}
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Add new answer form
                        if "user" in st.session_state:
                            with st.form(key=f"ans_form_{q_id}"):
                                # CHANGE: st.text_area allows multiple lines!
                                new_ans = st.text_area("Write a reply...", height=100, placeholder="Type here... (Press Enter for new line)")
                                
                                if st.form_submit_button("🚀 Reply"):
                                    if new_ans:
                                        db.post_answer(q_id, st.session_state["user"], new_ans)
                                        st.toast("Reply posted! You earned +5 Points.")
                                        st.rerun()
                                    else:
                                        st.warning("Cannot post empty reply.")
                        else:
                            st.caption("🔒 Login to reply")

# ==========================================
# TAB 2: ASK A DOUBT
# ==========================================
with tab2:
    st.subheader("❓ Post a New Question")
    
    if "user" not in st.session_state:
        st.error("Please Login on the Home Page to ask questions.")
    else:
        with st.form("ask_form"):
            subj = st.selectbox("Subject", ["M1 (Matrices)", "Java", "Python", "BEE", "Chemistry", "General"])
            # This was already a text_area, so it supported multiline
            query = st.text_area("What's your doubt?", height=150, placeholder="Ex: I don't understand how to find the Rank of a Matrix...\n\nHere is my code so far...")
            
            if st.form_submit_button("📢 Post Question"):
                if query:
                    db.post_question(st.session_state["user"], subj, query)
                    st.balloons()
                    st.success("Question posted successfully! Check the 'Browse' tab.")
                else:
                    st.warning("Please write something first.")