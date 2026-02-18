import streamlit as st
import database as db

# Initialize DB
db.init_db()

st.set_page_config(page_title="PEC Connect", page_icon="🎓", layout="wide")

# --- CUSTOM CSS FOR "ADVANCED UI" ---
st.markdown("""
    <style>
    .stApp { background-color: #FAFAFA; }
    .css-1d391kg { padding-top: 1rem; } /* Reduce top padding */
    
    /* Card Styling */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 5px solid #8B0000;
    }
    
    /* Title Styling */
    .pec-title {
        font-size: 3rem;
        font-weight: 800;
        color: #8B0000;
        text-align: center;
        margin-bottom: 0px;
    }
    .pec-subtitle {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR LOGIN SYSTEM ---
# --- SIDEBAR LOGIN SYSTEM ---
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

        else:  # Signup
            new_user = st.text_input("New Username").strip()
            new_pass = st.text_input("New Password", type="password").strip()
            role = st.selectbox("I am a...", ["Student", "Alumni/Senior"])
            year = st.selectbox("Year", ["1st", "2nd", "3rd", "4th", "Passed Out"])

            if st.button("Create Account"):
                if db.add_user(new_user, new_pass, role, year):
                    st.success("Account Created! Go to Login.")
                else:
                    st.error("Username already exists.")

    else:
        st.subheader(f"👋 Hi, {st.session_state['user']}")
        st.caption(f"Role: {st.session_state['role']}")

        if st.button("Logout"):
            del st.session_state["user"]
            st.rerun()


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
