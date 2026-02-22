import streamlit as st
import database as db
from datetime import datetime
import time

db.init_db()

# Check for admin
is_admin = st.session_state.get("is_admin", False)

st.markdown("""
<style>
    #MainMenu, footer { visibility: hidden !important; }
    html, body { font-family: 'Segoe UI', sans-serif; }
    
    /* Keep header visible for sidebar toggle */
    header { visibility: visible !important; }
    
    /* Make sidebar toggle highly visible on mobile */
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        opacity: 1 !important;
        position: fixed !important;
        left: 8px !important;
        top: 10px !important;
        z-index: 999999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] button {
        visibility: visible !important;
        opacity: 1 !important;
        display: flex !important;
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border: 2px solid #ffd700 !important;
        border-radius: 8px !important;
        width: 40px !important;
        height: 36px !important;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.5), 0 0 8px rgba(255, 215, 0, 0.4) !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.7), 0 0 12px rgba(255, 215, 0, 0.6) !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="stSidebarCollapsedControl"] span {
        visibility: visible !important;
        opacity: 1 !important;
        fill: white !important;
        color: white !important;
    }
    
    /* Sidebar width */
    section[data-testid="stSidebar"] {
        width: 250px !important;
    }
    
    /* Sidebar expand button - always visible on left edge */
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        opacity: 1 !important;
        position: fixed !important;
        left: 0px !important;
        top: 12px !important;
        z-index: 999999 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 60px !important;
        height: 50px !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] button,
    [data-testid="stSidebarCollapsedControl"] button * {
        visibility: visible !important;
        opacity: 1 !important;
        display: flex !important;
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border: 3px solid #ffd700 !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.6), 0 0 15px rgba(255, 215, 0, 0.6) !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] button:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.8), 0 0 25px rgba(255, 215, 0, 0.8) !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="stSidebarCollapsedControl"] span,
    [data-testid="stSidebarCollapsedControl"] path {
        visibility: visible !important;
        opacity: 1 !important;
        fill: white !important;
        color: white !important;
        width: 28px !important;
        height: 28px !important;
    }
    
    .admin-banner {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white; padding: 10px 20px; border-radius: 10px;
        margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;
    }
    .admin-banner h3 { margin: 0; }
    
    .page-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 25px 30px; border-radius: 16px; margin-bottom: 25px;
    }
    .page-title { color: white; font-size: 1.8rem; font-weight: 800; margin: 0; }
    .page-subtitle { color: rgba(255,255,255,0.85); font-size: 0.95rem; margin-top: 6px; }
    
    .config-card {
        background: white; border: 1px solid #e2e8f0;
        border-radius: 16px; padding: 20px; margin-bottom: 20px;
    }
    
    .question-card {
        background: white; border: 1px solid #e2e8f0;
        border-radius: 16px; padding: 20px; margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    .question-card:hover {
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
    }
    
    .topic-tag {
        background: linear-gradient(135deg, #667eea20, #764ba220);
        color: #475569; padding: 5px 12px;
        border-radius: 20px; font-size: 0.75rem; font-weight: 600;
    }
    .solved-badge {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white; padding: 5px 12px;
        border-radius: 20px; font-size: 0.7rem; font-weight: 700; 
        margin-left: 8px;
    }
    
    .vote-btn {
        background: #f1f5f9; border: none; border-radius: 12px;
        padding: 12px 16px; cursor: pointer; transition: all 0.2s;
        text-align: center; min-width: 60px;
    }
    .vote-btn:hover { background: #e2e8f0; }
    .vote-btn-voted {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }
    .vote-count {
        font-size: 1.2rem; font-weight: 700; color: #1e293b;
    }
    .vote-label {
        font-size: 0.7rem; color: #64748b;
    }
    
    .user-name { font-weight: 700; color: #1e293b; font-size: 0.9rem; }
    .time-text { font-size: 0.75rem; color: #94a3b8; }
    
    .answer-card {
        background: #f8fafc; padding: 15px; border-radius: 12px;
        border-left: 4px solid #667eea; margin-top: 12px;
    }
    
    .stat-card {
        background: white; border: 1px solid #e2e8f0;
        border-radius: 12px; padding: 15px; text-align: center;
    }
    .stat-num { font-size: 1.5rem; font-weight: 700; color: #667eea; }
    .stat-lbl { font-size: 0.75rem; color: #64748b; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1 class="page-title">🗣️ Doubt Forum</h1>
    <p class="page-subtitle">Ask questions and get answers from the community</p>
</div>
""", unsafe_allow_html=True)

if is_admin:
    st.markdown("""
    <div class="admin-banner">
        <h3>🛡️ Admin Mode - Full Access</h3>
    </div>
    """, unsafe_allow_html=True)

def get_relative_time(date_str):
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        now = datetime.now(dt.tzinfo)
        diff = now - dt
        seconds = diff.total_seconds()
        
        if seconds < 60: return "Just now"
        elif seconds < 3600: return f"{int(seconds//60)} min ago"
        elif seconds < 86400: return f"{int(seconds//3600)} hours ago"
        else: return f"{int(seconds//86400)} days ago"
    except:
        return "Recently"

SUBJECTS_BY_YEAR = {
    "1st Year": ["M1 - Matrices & Calculus", "M2 - Differential Equations & Vector Calculus", "Engineering Chemistry", "Applied Physics", "Programming for Problem Solving (C)", "Python Programming", "Basic Electrical Engineering", "Engineering Drawing", "Engineering Workshop", "IT Workshop", "English - Communication Skills", "Environmental Science"],
    "2nd Year - CSE": ["Discrete Mathematics", "Data Structures", "Digital Logic Design", "Computer Organization & Architecture", "Object Oriented Programming (Java)", "Operating Systems", "Database Management Systems", "Software Engineering", "Probability & Statistics"],
    "2nd Year - CSE-AIML": ["Discrete Mathematics", "Data Structures", "Object Oriented Programming (Python)", "Operating Systems", "Database Management Systems", "Probability & Statistics", "Linear Algebra", "AI Fundamentals"],
    "2nd Year - ECE": ["Electronic Devices & Circuits", "Network Theory", "Signals & Systems", "Analog Electronics", "Digital Electronics", "Microprocessors & Microcontrollers"],
    "2nd Year - EEE": ["Electrical Circuit Analysis", "Electrical Machines - I", "Power Systems - I", "Control Systems", "Power Electronics"],
    "2nd Year - Mechanical": ["Engineering Mechanics", "Strength of Materials", "Fluid Mechanics", "Thermodynamics", "Manufacturing Processes"],
    "2nd Year - Civil": ["Building Materials & Construction", "Surveying", "Structural Analysis - I", "Concrete Technology"],
    "3rd Year - CSE": ["Algorithms", "Compiler Design", "Computer Networks", "Artificial Intelligence", "Machine Learning", "Data Science", "Cloud Computing", "Web Technologies"],
    "3rd Year - CSE-AIML": ["Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision", "Data Science", "Neural Networks"],
    "3rd Year - ECE": ["Communication Theory", "Digital Signal Processing", "VLSI Design", "Microwave Engineering", "Embedded Systems"],
    "3rd Year - EEE": ["Power Systems - II", "Power Electronics", "Renewable Energy Sources", "Electrical Drives"],
    "3rd Year - Mechanical": ["Thermal Engineering", "Heat Transfer", "Design of Machine Elements", "CAD/CAM"],
    "3rd Year - Civil": ["Structural Analysis - II", "RCC & Steel Structures", "Geotechnical Engineering", "Water Resources Engineering"],
    "4th Year - CSE": ["Deep Learning", "Big Data Analytics", "Cybersecurity", "Internet of Things (IoT)", "Blockchain Technology"],
    "4th Year - CSE-AIML": ["Advanced Deep Learning", "Computer Vision", "Reinforcement Learning", "Generative AI", "Edge AI"],
    "4th Year - ECE": ["Wireless Communications", "Optical Communications", "Image Processing", "Neural Networks & Fuzzy Logic"],
    "4th Year - EEE": ["Power System Protection", "Smart Grid", "Renewable Energy Systems", "Electric Vehicles"],
    "4th Year - Mechanical": ["Refrigeration & Air Conditioning", "Automobile Engineering", "Robotics & Automation"],
    "4th Year - Civil": ["Prestressed Concrete", "Bridge Engineering", "Environmental Engineering", "Construction Management"],
    "Labs": ["C Programming Lab", "Python Lab", "Data Structures Lab", "DBMS Lab", "OS Lab", "AI/ML Lab", "Java Programming Lab"],
    "Other": ["GATE Preparation", "Interview Preparation", "Aptitude & Reasoning", "General"]
}

ALL_SUBJECTS = []
for year_subjects in SUBJECTS_BY_YEAR.values():
    ALL_SUBJECTS.extend(year_subjects)
ALL_SUBJECTS = sorted(ALL_SUBJECTS)

with st.container(border=True):
    c1, c2, c3 = st.columns([2, 2, 1])
    with c1:
        search_query = st.text_input("🔍 Search doubts...", placeholder="Search keywords...")
    with c2:
        filter_year = st.selectbox("📚 Year", ["All Years"] + list(SUBJECTS_BY_YEAR.keys()))
    with c3:
        sort_order = st.selectbox("📊 Sort", ["Newest", "Most Voted", "Unsolved"])
    
    if filter_year == "All Years":
        filter_subject = "All"
    else:
        filter_subject = st.selectbox("📖 Subject", ["All Subjects"] + SUBJECTS_BY_YEAR[filter_year])

tab1, tab2 = st.tabs(["🔥 Browse Discussions", "✍️ Ask a Question"])

with tab1:
    questions = db.get_questions(filter_subject if filter_subject != "All Subjects" else "All")
    
    if search_query:
        questions = [q for q in questions if search_query.lower() in q['question_text'].lower() or 
                     q.get('subject', '').lower() in search_query.lower()]
    
    if sort_order == "Most Voted":
        questions.sort(key=lambda x: x.get('upvotes', 0), reverse=True)
    elif sort_order == "Unsolved":
        questions = [q for q in questions if not q.get('is_solved', False)]
    
    if not questions:
        st.markdown("""
        <div style="text-align: center; padding: 50px; background: #f8fafc; border-radius: 16px; border: 2px dashed #cbd5e1;">
            <h3 style="color: #64748b;">🔍 No doubts found</h3>
            <p style="color: #94a3b8;">Be the first to ask a question!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        total_questions = len(questions)
        solved_count = len([q for q in questions if q.get('is_solved', False)])
        total_votes = sum(q.get('upvotes', 0) for q in questions)
        
        c_stats1, c_stats2, c_stats3 = st.columns(3)
        with c_stats1:
            st.metric("Total Questions", total_questions)
        with c_stats2:
            st.metric("Solved", solved_count)
        with c_stats3:
            st.metric("Total Upvotes", total_votes)
        
        st.markdown("---")
        
        for q in questions:
            q_id = q['id']
            q_user = q['username']
            q_sub = q['subject']
            q_text = q['question_text']
            q_time = get_relative_time(q['timestamp'])
            q_votes = q.get('upvotes', 0)
            is_solved = q.get('is_solved', False)
            q_image = q.get('image_url', '')
            
            avatar_url = db.get_avatar_url(q_user)
            
            has_voted = False
            if "user" in st.session_state:
                user_votes = db.get_user_votes(st.session_state.get("user", ""))
                if q_id in user_votes:
                    has_voted = True
            
            is_owner = "user" in st.session_state and st.session_state["user"] == q_user
            
            with st.container(border=True):
                # Admin controls
                if is_admin:
                    c_admin1, c_admin2 = st.columns(2)
                    with c_admin1:
                        if st.button("🗑️ Delete", key=f"admin_del_{q_id}"):
                            db.delete_doubt(q_id)
                            st.success("Deleted!")
                            st.rerun()
                    with c_admin2:
                        if st.button("⚠️ Warn User", key=f"admin_warn_{q_id}"):
                            warning_msg = f"Your doubt '{q_text[:50]}...' has been removed for violating community guidelines."
                            db.send_warning(q_user, warning_msg)
                            db.delete_doubt(q_id)
                            st.warning("Warning sent and doubt deleted!")
                            st.rerun()
                
                c_top1, c_top2 = st.columns([5, 1])
                with c_top1:
                    solved_html = '<span class="solved-badge">✅ SOLVED</span>' if is_solved else '<span style="background:#fef3c7; color:#b45309; padding:5px 12px; border-radius:20px; font-size:0.7rem; font-weight:700; margin-left:8px;">⏳ UNSOLVED</span>'
                    st.markdown(f'<span class="topic-tag">{q_sub}</span>{solved_html}', unsafe_allow_html=True)
                with c_top2:
                    if is_owner:
                        if st.button("🗑️ Delete", key=f"del_{q_id}", type="primary"):
                            db.delete_question(q_id)
                            st.success("Deleted!")
                            st.rerun()
                
                st.markdown(f"### {q_text}")
                
                if q_image:
                    st.image(q_image, width=400, caption="Attached Image")
                
                c_avatar, c_meta = st.columns([0.5, 4])
                with c_avatar:
                    st.image(avatar_url, width=45)
                with c_meta:
                    st.markdown(f"**@{q_user}**")
                    st.caption(q_time)
                
                st.divider()
                
                c_vote, c_reply = st.columns([1, 4])
                with c_vote:
                    vote_class = "vote-btn vote-btn-voted" if has_voted else "vote-btn"
                    vote_icon = "⬆️" if has_voted else "🔼"
                    if "user" in st.session_state:
                        if st.button(f"{vote_icon}\n{q_votes}\nUpvote", key=f"v_{q_id}"):
                            db.upvote_question(q_id, st.session_state["user"])
                            st.rerun()
                    else:
                        st.markdown(f"""
                        <div class="{vote_class}">
                            <div class="vote-count">{q_votes}</div>
                            <div class="vote-label">votes</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with c_reply:
                    answers = db.get_answers(q_id)
                    with st.expander(f"💬 {len(answers)} Answers"):
                        if answers:
                            for ans in answers:
                                a_user = ans['username']
                                a_text = ans['answer_text']
                                a_time = get_relative_time(ans['timestamp'])
                                a_av = db.get_avatar_url(a_user)
                                
                                st.markdown(f"**@{a_user}** · {a_time}")
                                st.markdown(a_text)
                                st.divider()
                        else:
                            st.info("No answers yet. Be the first to help!")
                        
                        if "user" in st.session_state:
                            new_reply = st.text_area("Write your answer...", key=f"ans_{q_id}", placeholder="Help others by answering...")
                            if st.button("🚀 Post Answer", key=f"post_{q_id}"):
                                if new_reply:
                                    db.post_answer(q_id, st.session_state["user"], new_reply)
                                    st.success("Answer posted!")
                                    st.rerun()
                        
                        if is_owner and not is_solved:
                            if st.button("✅ Mark as Solved", key=f"sol_{q_id}"):
                                db.mark_solved(q_id)
                                st.rerun()

if "doubt_key" not in st.session_state:
    st.session_state.doubt_key = 0

with tab2:
    st.markdown("### 📝 Ask the Community")
    
    if "user" not in st.session_state:
        st.error("🔐 Please login to post your doubt.")
    else:
        with st.container(border=True):
            st.info("💡 **Tip:** Use triple backticks (```) for code blocks and attach images for better clarity!")
            
            c_year, c_subj = st.columns(2)
            with c_year:
                ask_year = st.selectbox("📚 Year", list(SUBJECTS_BY_YEAR.keys()), key=f"doubt_year_{st.session_state.doubt_key}")
            with c_subj:
                subj = st.selectbox("📖 Subject", SUBJECTS_BY_YEAR[ask_year], key=f"doubt_subj_{st.session_state.doubt_key}")
            
            q_body = st.text_area("📝 Describe your doubt in detail...", height=150, 
                                key=f"doubt_text_{st.session_state.doubt_key}",
                                placeholder="Example:\nI am getting an error in my Python code:\n\n```python\nprint('Hello World')\n```")
            
            uploaded_file = st.file_uploader("📷 Attach Image (optional)", 
                                            type=['png', 'jpg', 'jpeg', 'gif', 'webp'],
                                            key=f"doubt_image_{st.session_state.doubt_key}",
                                            help="Attach a screenshot or image to explain your doubt better")
            
            image_url = ""
            if uploaded_file is not None:
                st.image(uploaded_file, width=200, caption="Preview")
                with st.spinner("Uploading image..."):
                    image_url = db.upload_doubt_image(uploaded_file.getvalue(), uploaded_file.type, st.session_state["user"])
                if image_url:
                    st.success("✅ Image uploaded!")
            
            if st.button("📢 Publish Question", type="primary", use_container_width=True):
                if q_body.strip():
                    try:
                        result = db.post_question(st.session_state["user"], subj, q_body, image_url)
                        if result:
                            st.balloons()
                            st.success("🎉 Question posted successfully!")
                            # Increment key to reset form and refresh
                            st.session_state.doubt_key += 1
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("Failed to post question. Please try again.")
                    except Exception as e:
                        st.error(f"Error posting question: {e}")
                else:
                    st.warning("Please write your doubt!")

# Force refresh questions after posting
if "refresh_questions" in st.session_state and st.session_state.refresh_questions:
    st.session_state.refresh_questions = False
    time.sleep(0.3)
    st.rerun()
