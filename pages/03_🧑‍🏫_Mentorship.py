import streamlit as st
import sqlite3
import random

# --- PAGE SETUP ---
st.set_page_config(page_title="Mentorship | PEC", page_icon="🧑‍🏫", layout="wide")

st.title("🧑‍🏫 PEC Mentorship Squad")
st.caption("Connect with 'Verified' seniors. Clear backlogs with 1-on-1 guidance.")

# --- DATABASE CONNECTION ---
def get_db_connection():
    conn = sqlite3.connect('pec_data.db')
    return conn

# --- EXTENDED SUBJECT LIST (JNTUH R18/R22) ---
SUBJECTS = [
    # 1st Year
    "M1 (Matrices)", "M2 (ODE)", "BEE (Electrical)", "Engineering Physics", "Chemistry", "C Programming", "Engineering Drawing",
    # 2-1 Semester
    "Data Structures (DS)", "Python Programming", "Digital Logic Design (DLD)", "Discrete Math (MFCS)", "Electronic Devices (EDC)",
    # 2-2 Semester
    "Java Programming", "DBMS (Database)", "Operating Systems (OS)", "Computer Organization (COA)", "BEFA (Economics)",
    # 3rd & 4th Year
    "DAA (Algorithms)", "Web Technologies", "AI & ML", "Cloud Computing", "Compiler Design", "Cyber Security"
]

# --- TABS ---
tab1, tab2 = st.tabs(["🔍 Find a Mentor", "🚀 Become a Mentor"])

# ==========================================
# TAB 1: FIND A MENTOR (Advanced UI)
# ==========================================
with tab1:
    st.subheader("👨‍🏫 Top Rated Mentors")
    
    # 1. Advanced Filters
    c1, c2, c3 = st.columns(3)
    subject_filter = c1.selectbox("Filter by Subject", ["All"] + SUBJECTS)
    max_price = c2.slider("Max Hourly Rate (₹)", 0, 500, 200)
    sort_by = c3.selectbox("Sort By", ["Rating (High to Low)", "Price (Low to High)"])
    
    # 2. Query Database
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM mentors")
    all_mentors = c.fetchall()
    conn.close()
    
    # 3. Apply Logic
    filtered_mentors = []
    for m in all_mentors:
        # m = (user_id, skills, rate, contact, bio)
        
        # Subject Filter
        if subject_filter != "All" and subject_filter not in m[1]:
            continue
        # Price Filter
        if m[2] > max_price:
            continue
        
        filtered_mentors.append(m)
    
    # 4. Display "Advanced" Cards
    if not filtered_mentors:
        st.info("No mentors found. Be the first to join!")
    else:
        cols = st.columns(3)
        for i, mentor in enumerate(filtered_mentors):
            with cols[i % 3]:
                with st.container(border=True):
                    # Header with "Verified" Badge logic (Random for demo)
                    is_verified = True if i % 2 == 0 else False 
                    rating = round(random.uniform(4.0, 5.0), 1) # Fake rating for demo
                    
                    c1, c2 = st.columns([1, 4])
                    with c1:
                        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=50)
                    with c2:
                        st.markdown(f"**{mentor[0]}**")
                        if is_verified:
                            st.markdown("✅ *Verified Senior*")
                        st.caption(f"⭐ {rating}/5.0 (12 Sessions)")

                    st.markdown("---")
                    
                    # Skills Tags
                    skills_list = mentor[1].split(", ")
                    # Show first 2 skills as chips
                    for skill in skills_list[:2]:
                        st.markdown(f"<span style='background-color: #f0f2f6; padding: 4px 8px; border-radius: 4px; font-size: 12px;'>{skill}</span>", unsafe_allow_html=True)
                    if len(skills_list) > 2:
                        st.caption(f"+ {len(skills_list)-2} more subjects")
                    
                    st.write("") # Spacer
                    st.write(f"_{mentor[4]}_") # Bio
                    
                    # Price & Action
                    c_price, c_btn = st.columns([1, 1])
                    with c_price:
                        if mentor[2] == 0:
                            st.success("FREE")
                        else:
                            st.write(f"**₹{mentor[2]}/hr**")
                    with c_btn:
                        msg = f"Hi {mentor[0]}, I found your profile on PEC Connect. I need help with {subject_filter if subject_filter != 'All' else 'studies'}."
                        st.link_button("💬 Book", f"https://wa.me/{mentor[3]}?text={msg}", type="primary", use_container_width=True)

# ==========================================
# TAB 2: BECOME A MENTOR (With New Subjects)
# ==========================================
with tab2:
    st.subheader("🚀 Create Your Mentor Profile")
    
    if "user" not in st.session_state:
        st.error("🔒 Please Login to continue.")
    else:
        # Check if exists
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM mentors WHERE user_id=?", (st.session_state["user"],))
        exists = c.fetchone()
        conn.close()
        
        if exists:
            st.success("✅ You are already listed!")
            st.info("To update your profile, please delete it first and recreate.")
            if st.button("🗑️ Delete Profile"):
                conn = get_db_connection()
                c = conn.cursor()
                c.execute("DELETE FROM mentors WHERE user_id=?", (st.session_state["user"],))
                conn.commit()
                conn.close()
                st.rerun()
        else:
            with st.form("mentor_form"):
                st.write(f"**Mentor:** {st.session_state['user']}")
                
                # THE NEW HUGE SUBJECT LIST
                skills = st.multiselect("Select your Strong Subjects:", SUBJECTS)
                
                c1, c2 = st.columns(2)
                rate = c1.number_input("Hourly Rate (₹) (0 = Free)", min_value=0, value=100)
                contact = c2.text_input("WhatsApp Number", placeholder="919999999999")
                
                bio = st.text_area("Your Pitch (Bio)", placeholder="I passed Java with 95%. I can teach you the important 5 units in 2 days.")
                
                if st.form_submit_button("🚀 Launch Profile"):
                    if not skills or not contact:
                        st.error("Please fill all details!")
                    else:
                        skills_str = ", ".join(skills)
                        conn = get_db_connection()
                        c = conn.cursor()
                        # Ensure table exists
                        c.execute('''CREATE TABLE IF NOT EXISTS mentors
                                    (user_id TEXT PRIMARY KEY, subject_expertise TEXT, 
                                     hourly_rate INTEGER, contact_number TEXT, bio TEXT)''')
                        
                        c.execute("INSERT INTO mentors VALUES (?,?,?,?,?)", 
                                  (st.session_state["user"], skills_str, rate, contact, bio))
                        conn.commit()
                        conn.close()
                        st.balloons()
                        st.success("Profile Live! Go to 'Find a Mentor' tab to check it.")