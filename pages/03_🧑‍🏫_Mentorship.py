import streamlit as st
import database as db
import random

# --- PAGE SETUP ---
st.set_page_config(page_title="Mentorship | PEC", page_icon="🧑‍🏫", layout="wide")
db.init_db()

# --- PROFESSIONAL CSS (Preply/Tutor.com Style) ---
st.markdown("""
<style>
    /* Card Container */
    .mentor-card {
        background: white; border: 1px solid #e0e0e0; border-radius: 16px;
        padding: 20px; transition: transform 0.2s; position: relative;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .mentor-card:hover {
        border-color: #3b82f6; transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.15);
    }
    
    /* Verified Badge */
    .verified-badge {
        background: #dcfce7; color: #166534; padding: 2px 8px;
        border-radius: 12px; font-size: 0.75rem; font-weight: 700;
        display: inline-block; margin-bottom: 5px;
    }
    
    /* Stats Row */
    .stat-row { display: flex; align-items: center; gap: 15px; font-size: 0.85rem; color: #64748b; margin: 10px 0; }
    .star-rating { color: #f59e0b; font-weight: 700; }
    
    /* Price Tag */
    .price-tag { font-size: 1.2rem; font-weight: 800; color: #0f172a; }
    .per-hr { font-size: 0.8rem; color: #64748b; font-weight: 400; }
</style>
""", unsafe_allow_html=True)

st.title("🧑‍🏫 PEC Mentorship Squad")
st.caption("Master complex subjects with 1-on-1 guidance from top seniors.")

# --- SUBJECT LIST ---
SUBJECTS = [
    "M1 (Matrices)", "M2 (ODE)", "BEE (Electrical)", "Engineering Physics", "Chemistry", "C Programming",
    "Data Structures", "Python", "Digital Electronics", "Java", "DBMS", "OS", "AI & ML", "Cyber Security"
]

# --- TABS ---
tab1, tab2 = st.tabs(["🔍 Find a Mentor", "🚀 Become a Mentor"])

# ==========================================
# TAB 1: FIND A MENTOR (Preply Style)
# ==========================================
with tab1:
    c_filter, c_price = st.columns([3, 1])
    subject_filter = c_filter.selectbox("I want to learn...", ["All Subjects"] + SUBJECTS)
    max_price = c_price.select_slider("Budget per hour", options=[0, 100, 200, 300, 500, 1000], value=500)
    
    # Fetch Data
    mentors = db.get_all_mentors()
    
    # Filter
    filtered = []
    for m in mentors:
        if subject_filter != "All Subjects" and subject_filter not in m['skills']: continue
        if m['rate'] > max_price: continue
        filtered.append(m)
    
    if not filtered:
        st.info("No mentors found matching your criteria.")
    else:
        st.markdown(f"**{len(filtered)} tutors available**")
        
        # Grid Layout
        cols = st.columns(3)
        for i, m in enumerate(filtered):
            with cols[i % 3]:
                username = m['username']
                # Fetch full name from users table if possible, else use username
                details = db.get_user_details(username)
                fullname = details.get('full_name', username) if details else username
                
                # Mock Stats (In a real app, these would come from DB)
                rating = round(random.uniform(4.5, 5.0), 1)
                sessions = random.randint(5, 50)
                
                with st.container():
                    # CARD START
                    st.markdown(f"""
                    <div class="mentor-card">
                        <div class="verified-badge">✅ Verified Senior</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Layout: Image Left, Info Right
                    c_img, c_info = st.columns([1, 2.5])
                    with c_img:
                        # FIX: Use the new Smart Avatar Function from database.py
                        avatar_url = db.get_avatar_url(username)
                        st.image(avatar_url, width=80)
                    
                    with c_info:
                        st.markdown(f"**{fullname}**")
                        st.markdown(f"<div class='star-rating'>⭐ {rating} <span style='color:#94a3b8; font-weight:400'>({sessions} reviews)</span></div>", unsafe_allow_html=True)
                        
                        # Skills (First 2 only)
                        skills = m['skills'].split(",")
                        tags = "".join([f"<span style='background:#f1f5f9; padding:2px 8px; border-radius:10px; font-size:10px; margin-right:4px;'>{s.strip()}</span>" for s in skills[:2]])
                        st.markdown(f"<div style='margin-top:5px;'>{tags}</div>", unsafe_allow_html=True)

                    # Bio Snippet
                    st.caption(f"_{m['bio'][:100]}..._")
                    
                    st.divider()
                    
                    # Footer: Price & Button
                    c_p, c_b = st.columns([1, 1.5])
                    with c_p:
                        price = "FREE" if m['rate'] == 0 else f"₹{m['rate']}"
                        st.markdown(f"<div class='price-tag'>{price}<span class='per-hr'>/hr</span></div>", unsafe_allow_html=True)
                    with c_b:
                        msg = f"Hi {fullname}, I found your profile on PEC Connect. I need help with {subject_filter}."
                        st.link_button("⚡ Book Trial", f"https://wa.me/{m['contact']}?text={msg}", type="primary", use_container_width=True)

# ==========================================
# TAB 2: BECOME A MENTOR
# ==========================================
with tab2:
    if "user" not in st.session_state:
        st.warning("Please Login to create a profile.")
        st.stop()
        
    my_user = st.session_state["user"]
    
    # Check if exists
    exists = next((m for m in mentors if m['username'] == my_user), None)
    
    if exists:
        st.success("🎉 Your Mentor Profile is Live!")
        with st.expander("Edit or Delete Profile"):
            if st.button("🗑️ Delete Profile", type="primary"):
                db.delete_mentor(my_user)
                st.rerun()
    else:
        st.subheader("🚀 Earn while you learn")
        st.caption("Share your knowledge and earn money or reputation points.")
        
        with st.form("new_mentor"):
            skills = st.multiselect("Subjects you can teach:", SUBJECTS)
            
            c1, c2 = st.columns(2)
            rate = c1.number_input("Hourly Rate (₹) (0 for Free)", value=150, step=50)
            contact = c2.text_input("WhatsApp Number (with Country Code)", value="91")
            
            bio = st.text_area("About You (The Pitch)", placeholder="I scored 98% in M1. I explain concepts using real-life examples...")
            
            if st.form_submit_button("Publish Profile"):
                if skills and contact and bio:
                    s_str = ", ".join(skills)
                    db.register_mentor(my_user, s_str, rate, contact, bio)
                    st.success("Profile Published!")
                    st.rerun()
                else:
                    st.error("Please fill all fields.")