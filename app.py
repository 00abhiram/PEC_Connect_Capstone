import streamlit as st
import database as db

# Initialize DB
db.init_db()

st.set_page_config(page_title="PEC Connect", page_icon="🎓", layout="wide")

# ================= CUSTOM CSS =================
st.markdown("""
<style>
.stApp {
    background-color: #FAFAFA;
}
.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    text-align: center;
    border-left: 5px solid #8B0000;
}
</style>
""", unsafe_allow_html=True)

<<<<<<< HEAD
# --- SIDEBAR LOGIN SYSTEM ---
# --- SIDEBAR LOGIN SYSTEM ---
=======
# ================= SIDEBAR LOGIN SYSTEM =================
>>>>>>> 4e4ef34 (Finalized Scam Detector and Academic Risk features)
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/User_icon_2.svg/1024px-User_icon_2.svg.png", width=80)

    if "user" not in st.session_state:
        st.header("🔐 Login / Signup")
        choice = st.selectbox("Choose Action", ["Login", "Signup"])

        if choice == "Login":
            user = st.text_input("Username").strip()
            pasw = st.text_input("Password", type="password").strip()

            if st.button("Login"):
                account = db.check_login(user, pasw)

                if account:
                    st.session_state["user"] = user
                    st.session_state["role"] = account[2]
                    st.success(f"Welcome back, {user}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
<<<<<<< HEAD

        else:  # Signup
            new_user = st.text_input("New Username").strip()
            new_pass = st.text_input("New Password", type="password").strip()
=======
        else:
            new_user = st.text_input("New Username")
            new_pass = st.text_input("New Password", type="password")
>>>>>>> 4e4ef34 (Finalized Scam Detector and Academic Risk features)
            role = st.selectbox("I am a...", ["Student", "Alumni/Senior"])
            year = st.selectbox("Year", ["1st", "2nd", "3rd", "4th", "Passed Out"])

            if st.button("Create Account"):
                if db.add_user(new_user, new_pass, role, year):
                    st.success("Account Created! Go to Login.")
                else:
                    st.error("Username already exists.")
<<<<<<< HEAD

=======
>>>>>>> 4e4ef34 (Finalized Scam Detector and Academic Risk features)
    else:
        st.subheader(f"👋 Hi, {st.session_state['user']}")
        st.caption(f"Role: {st.session_state['role']}")

        if st.button("Logout"):
            del st.session_state["user"]
            st.rerun()

<<<<<<< HEAD

# --- MAIN DASHBOARD ---

if "user" not in st.session_state:
    st.markdown('<div class="pec-title">Pallavi Engineering College</div>', unsafe_allow_html=True)
    st.markdown('<div class="pec-subtitle">Student Success & Mentorship Portal</div>', unsafe_allow_html=True)
    st.warning("⚠️ Please Login or Signup from the Sidebar to continue.")
else:

    # Sidebar Navigation
    menu = st.sidebar.radio("📌 Navigation", ["Dashboard", "AI Tutor", "Notes Market", "Mentorship"])

    if menu == "Dashboard":
        st.markdown('<div class="pec-title">Pallavi Engineering College</div>', unsafe_allow_html=True)
        st.markdown('<div class="pec-subtitle">Student Success & Mentorship Portal</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.markdown('<div class="metric-card"><h3>👥 Active Students</h3><h2>1,240</h2><p>+12% this week</p></div>', unsafe_allow_html=True)
        col2.markdown('<div class="metric-card"><h3>📚 Notes Shared</h3><h2>850+</h2><p>R18 & R22 Patterns</p></div>', unsafe_allow_html=True)
        col3.markdown('<div class="metric-card"><h3>🏆 Top Mentor</h3><h2>Rohan K.</h2><p>CSE Dept</p></div>', unsafe_allow_html=True)

    elif menu == "AI Tutor":
        st.header("🤖 AI Tutor")
        question = st.text_area("Ask your doubt:")
        if st.button("Get Answer"):
            st.success("AI Response will appear here (Connect your API here)")

    elif menu == "Notes Market":
        st.header("📚 Notes Market")
        st.info("Upload and Download Notes feature here")

    elif menu == "Mentorship":
        st.header("🎯 Mentorship Connect")
        st.info("Connect with Alumni / Seniors")
=======
# ================= HERO SECTION =================
st.markdown("""
<div style='padding: 30px; border-radius: 15px; 
background: linear-gradient(90deg, #8B0000, #B22222); 
color: white; text-align:center; margin-bottom:30px;'>
<h1>🚀 PEC Connect AI Portal</h1>
<p>Your AI-Powered Academic & Placement Companion</p>
</div>
""", unsafe_allow_html=True)

# ================= DASHBOARD OVERVIEW =================
st.markdown("## 📊 Dashboard Overview")
col1, col2, col3 = st.columns(3)

col1.markdown('<div class="metric-card"><h3>👥 Active Students</h3><h2>1,240</h2><p style="color:green;">+12% this week</p></div>', unsafe_allow_html=True)
col2.markdown('<div class="metric-card"><h3>📚 Notes Shared</h3><h2>850+</h2><p>R18 & R22 Patterns</p></div>', unsafe_allow_html=True)
col3.markdown('<div class="metric-card"><h3>🤖 AI Tutor Status</h3><h2 style="color:green;">24/7 Active</h2><p>Instant Doubt Support</p></div>', unsafe_allow_html=True)

st.divider()

# ================= LAUNCHPAD =================
if "user" in st.session_state:
    st.markdown("## 🚀 AI Intelligence Launchpad")
    col_ai, col_side = st.columns([2, 1])

    with col_ai:
        st.markdown("""
        <div style='background-color:white; padding:30px; border-radius:15px; 
        box-shadow:0 6px 10px rgba(0,0,0,0.1); border-left:6px solid #8B0000;'>
            <h2>🤖 AI Tutor</h2>
            <p style='font-size:16px;'>Get instant answers and concept explanations anytime.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Ask AI Now", use_container_width=True):
            st.switch_page("pages/02_🤖_AI_Study_Bot.py")

    with col_side:
        if st.button("📉 Academic Risk Predictor", use_container_width=True):
            st.switch_page("pages/ACADEMIC_RISK_PREDICTOR.py")

        if st.button("🛡 Career Scam Analyzer", use_container_width=True):
            # UPDATED PATH TO LOWERCASE
            st.switch_page("pages/scam_detector.py")

        if st.button("📚 Notes Market", use_container_width=True):
            st.switch_page("pages/01_📚_Notes_Marketplace.py")

        if st.button("📝 Mock Tests", use_container_width=True):
            st.switch_page("pages/04_📝_Mock_Tests.py")
>>>>>>> 4e4ef34 (Finalized Scam Detector and Academic Risk features)
