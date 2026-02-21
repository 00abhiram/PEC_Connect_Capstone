import streamlit as st
import database as db
from datetime import datetime
import time

db.init_db()

st.set_page_config(page_title="Doubt Forum", page_icon="🗣️", layout="wide")

st.markdown("""
<style>
    /* Question Card */
    .question-card {
        background: white; padding: 20px; border-radius: 12px;
        border: 1px solid #e2e8f0; margin-bottom: 20px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    /* Tags & Badges */
    .topic-tag {
        background-color: #f1f5f9; color: #475569; padding: 4px 12px;
        border-radius: 20px; font-size: 0.75rem; font-weight: 600;
        display: inline-block;
    }
    .solved-badge {
        background-color: #dcfce7; color: #166534; padding: 4px 12px;
        border-radius: 20px; font-size: 0.75rem; font-weight: 800; 
        margin-left: 10px; display: inline-block;
    }
    
    /* User Info */
    .user-name { font-weight: 700; color: #0f172a; font-size: 0.95rem; }
    .time-text { font-size: 0.8rem; color: #64748b; }
    
    /* Answer Section */
    .answer-box {
        background-color: #f8fafc; padding: 15px; border-radius: 10px;
        border-left: 4px solid #cbd5e1; margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

def get_relative_time(date_str):
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        now = datetime.now(dt.tzinfo)
        diff = now - dt
        seconds = diff.total_seconds()
        
        if seconds < 60: return "Just now"
        elif seconds < 3600: return f"{int(seconds//60)} mins ago"
        elif seconds < 86400: return f"{int(seconds//3600)} hours ago"
        else: return f"{int(seconds//86400)} days ago"
    except:
        return "Recently"

c1, c2 = st.columns([3, 1])
with c1:
    st.title("🗣️ PEC Community Forum")
    st.caption("Ask questions, share knowledge, and build your reputation.")
with c2:
    if "user" in st.session_state:
        st.markdown(f"<div style='text-align:right; color:#16a34a; font-weight:bold; padding-top:20px;'>● Online: {st.session_state['user']}</div>", unsafe_allow_html=True)

SUBJECTS = ["All", "M1 (Matrices)", "M2 (ODE)", "Engineering Chemistry", "Applied Physics", "PPS (C Programming)", "BEE (Basic Electrical)", "Python Programming", "Java (OOPs)", "General"]

col_search, col_filter, col_sort = st.columns([2, 2, 1])
with col_search:
    search_query = st.text_input("🔍 Search keywords...", label_visibility="collapsed")
with col_filter:
    filter_subject = st.selectbox("Topic", SUBJECTS, label_visibility="collapsed")
with col_sort:
    sort_order = st.selectbox("Sort", ["Newest", "Most Voted"], label_visibility="collapsed")

tab1, tab2 = st.tabs(["🔥 Browse Discussions", "✍️ Ask a Question"])

with tab1:
    questions = db.get_questions(filter_subject)
    
    if search_query:
        questions = [q for q in questions if search_query.lower() in q['question_text'].lower()]
    if sort_order == "Most Voted":
        questions.sort(key=lambda x: x.get('upvotes', 0), reverse=True)
    
    if not questions:
        st.info("No discussions found. Be the first to ask!")
    else:
        for q in questions:
            q_id = q['id']
            q_user = q['username']
            q_sub = q['subject']
            q_text = q['question_text']
            q_time = get_relative_time(q['timestamp'])
            q_votes = q.get('upvotes', 0)
            is_solved = q.get('is_solved', False)
            
            avatar_url = db.get_avatar_url(q_user)

            with st.container(border=True):
                c_img, c_meta, c_tag = st.columns([0.5, 4, 1.5])
                
                with c_img:
                    st.image(avatar_url, width=40) 
                
                with c_meta:
                    st.markdown(f"""
                    <div style="line-height:1.2;">
                        <div class="user-name">@{q_user}</div>
                        <div class="time-text">{q_time}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with c_tag:
                    solved_html = '<span class="solved-badge">✅ SOLVED</span>' if is_solved else ''
                    st.markdown(f'<div style="text-align:right;"><span class="topic-tag">{q_sub}</span>{solved_html}</div>', unsafe_allow_html=True)
                
                st.markdown(f"#### {q_text}")
                
                st.divider()
                
                c_vote, c_reply, c_space = st.columns([1, 2, 5])
                
                with c_vote:
                    if st.button(f"🔼 {q_votes}", key=f"v_{q_id}"):
                        db.upvote_question(q_id)
                        st.rerun()

                answers = db.get_answers(q_id)
                with c_reply:
                    st.caption(f"💬 {len(answers)} replies")
                
                with st.expander("View Discussion"):
                    if answers:
                        for ans in answers:
                            a_user = ans['username']
                            a_text = ans['answer_text']
                            a_time = get_relative_time(ans['timestamp'])
                            
                            a_av = db.get_avatar_url(a_user) 
                            
                            c_a_img, c_a_txt = st.columns([0.5, 11])
                            with c_a_img:
                                st.image(a_av, width=30)
                            with c_a_txt:
                                st.markdown(f"""
                                <div>
                                    <span style="font-weight:bold; font-size:0.9rem;">@{a_user}</span>
                                    <span style="color:#64748b; font-size:0.8rem; margin-left:8px;">• {a_time}</span>
                                </div>
                                """, unsafe_allow_html=True)
                                st.markdown(a_text)
                            st.divider()
                    else:
                        st.info("No answers yet.")

                    if "user" in st.session_state:
                        with st.form(key=f"rep_{q_id}"):
                            new_reply = st.text_area("Write a solution...", height=100, placeholder="Use markdown or ```code``` blocks")
                            if st.form_submit_button("🚀 Post Answer"):
                                if new_reply:
                                    db.post_answer(q_id, st.session_state["user"], new_reply)
                                    st.toast("Answer posted!")
                                    st.rerun()
                        
                        if st.session_state["user"] == q_user and not is_solved:
                            if st.button("✅ Mark Solved", key=f"sol_{q_id}"):
                                db.mark_solved(q_id)
                                st.rerun()

with tab2:
    st.markdown("### 📝 Ask the Community")
    
    if "user" not in st.session_state:
        st.error("Please Login to post.")
    else:
        with st.container(border=True):
            st.info("💡 **Tip:** Use triple backticks (```) for code blocks!")
            
            with st.form("ask_form"):
                subj = st.selectbox("Subject", SUBJECTS[1:])
                q_body = st.text_area("Describe your doubt...", height=200, 
                                    placeholder="Example:\nI am getting an error in my Python code:\n\n```python\nprint('Hello World')\n```")
                
                if st.form_submit_button("📢 Publish Question", type="primary"):
                    if q_body:
                        db.post_question(st.session_state["user"], subj, q_body)
                        st.balloons()
                        st.success("Published!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.warning("Please write something.")