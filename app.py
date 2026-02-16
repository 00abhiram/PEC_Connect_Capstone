import streamlit as st
import database as db
import os
import base64
import requests
from datetime import datetime
from streamlit_lottie import st_lottie
from PIL import Image

# --- LOAD ASSETS ---
try:
    favicon = Image.open("favicon.png")
except:
    favicon = "🎓"

# --- PAGE CONFIGURATION ---
try:
    favicon = Image.open("favicon.png") # Your personal logo
except:
    favicon = "🎓"

st.set_page_config(
    page_title="PEC Connect",
    page_icon=favicon, # This logo appears on your phone's home screen
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Cloud DB
db.init_db()

# --- HELPERS ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def get_current_avatar():
    """
    Smart function to get the avatar. 
    Handles Cloud URLs (New) and Base64 (Old) automatically.
    """
    if "user" in st.session_state:
        # 1. Fetch raw data from DB
        avatar_data = db.get_user_avatar(st.session_state["user"])
        
        if avatar_data:
            # CASE A: It is a Cloud Storage URL (starts with http) -> Return as is
            if "http" in str(avatar_data):
                return avatar_data
            
            # CASE B: It is an old Base64 string -> Format it
            if len(str(avatar_data)) > 100:
                return f"data:image/png;base64,{avatar_data}"
        
        # CASE C: No avatar found -> Use Default Dicebear
        return f"https://api.dicebear.com/7.x/identicon/svg?seed={st.session_state['user']}"
    return None

# Load Assets
app_logo_b64 = get_base64_image("favicon.png")
college_banner_b64 = get_base64_image("pec_logo.png")

# --- 🎨 PROFESSIONAL CSS ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc;
        color: #0f172a;
    }}
    
    [data-testid="stHeader"] {{ background-color: rgba(0,0,0,0); }}
    .block-container {{ padding-top: 3rem; padding-bottom: 2rem; }}

    /* --- 🟢 SIDEBAR TOGGLE BUTTON (HIGH VISIBILITY FIX) --- */
    /* Target the button container */
    [data-testid="stSidebarCollapsedControl"] {{
        background-color: #2563eb !important; /* Bright Blue */
        color: white !important;
        border-radius: 50% !important; /* Circle Shape */
        padding: 8px !important;
        width: 45px !important;
        height: 45px !important;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3) !important;
        border: 2px solid white !important;
        transition: all 0.3s ease !important;
        display: grid;
        place-items: center;
        z-index: 999999 !important;
    }}
    
    /* Hover Effect */
    [data-testid="stSidebarCollapsedControl"]:hover {{
        transform: scale(1.1);
        background-color: #1d4ed8 !important; /* Darker Blue */
        box-shadow: 0 6px 15px rgba(37, 99, 235, 0.5) !important;
    }}
    
    /* The Arrow Icon Itself */
    [data-testid="stSidebarCollapsedControl"] svg {{
        fill: white !important;
        stroke: white !important;
        height: 24px !important;
        width: 24px !important;
    }}

    /* --- DASHBOARD HEADER (Professional Glass Look) --- */
    .custom-navbar {{
        display: flex; justify-content: space-between; align-items: center;
        background: rgba(255, 255, 255, 0.95); /* Glass Effect */
        backdrop-filter: blur(10px);
        padding: 15px 30px; 
        border-radius: 16px;
        border: 1px solid #e2e8f0; 
        margin-bottom: 30px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05);
    }}
    .nav-logo {{ width: 45px; height: 45px; object-fit: contain; margin-right: 15px; }}
    .brand-title {{ font-weight: 800; font-size: 1.5rem; color: #0f172a; letter-spacing: -0.5px; }}
    .brand-badge {{ 
        background: linear-gradient(135deg, #2563eb, #3b82f6); color: white; font-size: 0.75rem; 
        padding: 4px 12px; border-radius: 20px; font-weight: 700; letter-spacing: 0.5px; margin-left: 10px;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2);
    }}

    /* --- LOGIN STYLES --- */
    .hero-title {{ font-size: 3.5rem; font-weight: 900; color: #1e293b; line-height: 1.1; margin-bottom: 20px; }}
    .hero-highlight {{ color: #2563eb; }}
    .hero-sub {{ font-size: 1.1rem; color: #64748b; line-height: 1.6; margin-bottom: 30px; font-weight: 400; }}
    
    /* --- CARDS & STATS --- */
    .hero-box {{
        background: #0f172a; padding: 2.5rem; border-radius: 24px; 
        text-align: center; margin-bottom: 30px; 
        box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.6);
        display: flex; justify-content: center; align-items: center; overflow: hidden;
    }}
    .hero-college-img {{ max-width: 500px; width: 100%; height: auto; }}
    
    .stat-card {{
        background: white; padding: 25px; border-radius: 20px; text-align: center;
        border: 1px solid #f1f5f9; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
        transition: transform 0.2s;
    }}
    .stat-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); }}
    .stat-num {{ font-size: 2.2rem; font-weight: 800; color: #2563eb; letter-spacing: -1px; }}
    .stat-lbl {{ font-size: 0.85rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }}

    .notice-box {{
        background: #fffbeb; border-radius: 16px; padding: 18px 25px;
        border-left: 5px solid #f59e0b;
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 35px; box-shadow: 0 4px 6px -1px rgba(251, 191, 36, 0.1);
    }}

    .action-card {{
        background: white; padding: 30px; border-radius: 20px;
        text-align: center; border: 1px solid #f1f5f9;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); cursor: pointer; height: 100%;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);
    }}
    .action-card:hover {{ 
        transform: translateY(-8px); 
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05); border-color: #bfdbfe; 
    }}
    .ac-icon {{ font-size: 2.5rem; margin-bottom: 15px; display: block; }}
    .ac-title {{ font-weight: 700; color: #1e293b; margin-bottom: 5px; font-size: 1.1rem; }}
    .ac-desc {{ font-size: 0.85rem; color: #94a3b8; }}

    /* --- FOOTER --- */
    .pro-footer {{
        background: #1e293b; color: #f8fafc; padding: 50px 0; margin-top: 60px;
        border-top: 5px solid #2563eb; text-align: center;
    }}
    .footer-brand {{ font-size: 1.5rem; font-weight: 800; letter-spacing: -1px; margin-bottom: 10px; }}
    .footer-credits {{ color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px; }}
    .footer-link a {{ color: #60a5fa; text-decoration: none; font-weight: 600; transition: color 0.2s; }}
    .footer-link a:hover {{ color: #93c5fd; text-decoration: underline; }}

</style>
""", unsafe_allow_html=True)

# --- UI LOGIC ---

if "user" not in st.session_state:
    # === SCENE 1: THE SPLIT LOGIN ===
    st.markdown("<br>", unsafe_allow_html=True)
    c_left, c_mid, c_right = st.columns([1.3, 0.1, 1])
    
    with c_left:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div>
            <div class="hero-title">
                Unlock Your <br> <span class="hero-highlight">Academic Potential</span>
            </div>
            <div class="hero-sub">
                Welcome to <b>PEC Connect v2.0</b>. The official AI-powered academic companion for Pallavi Engineering College. Bridging the gap between students and success.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_right:
        # LOGIN CARD
        with st.container(border=True):
            if app_logo_b64:
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 15px;">
                    <img src="data:image/png;base64,{app_logo_b64}" style="width: 100px;">
                    <div class="login-header">PEC Connect</div>
                    <div style="color: #64748b; font-size: 0.95rem;">Student Success Portal</div>
                </div>
                """, unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["🔒 Secure Login", "📝 Register"])
            
            with tab1:
                u = st.text_input("Username", key="l_u", placeholder="Enter Username")
                p = st.text_input("Password", type="password", key="l_p")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🚀 Login to Portal", use_container_width=True, type="primary"):
                    user = db.check_login(u, p)
                    if user:
                        st.session_state["user"] = user['username']
                        st.session_state["role"] = user['role']
                        st.session_state["full_name"] = user.get('full_name', '')
                        st.rerun()
                    else:
                        st.error("Invalid Credentials or User Not Found.")
            
            with tab2:
                c1, c2 = st.columns(2)
                fullname = c1.text_input("Full Name *")
                email = c2.text_input("Email *")
                nu = st.text_input("Username *")
                np = st.text_input("Set Password *", type="password")
                c_role, c_year = st.columns(2)
                role = c_role.selectbox("Role", ["Student", "Mentor"])
                year = c_year.selectbox("Year", ["1st", "2nd", "3rd", "4th"])
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("✨ Create Account", use_container_width=True):
                    if fullname and email and nu and np:
                        if db.add_user(nu, np, role, year, fullname, email): 
                            st.success(f"🎉 Account Created for {fullname}! Please Login.")
                            st.balloons()
                        else:
                            st.error("User already exists.")
                    else:
                        st.warning("All fields marked * are required.")

else:
    # === SCENE 2: PRO DASHBOARD ===
    
    # 1. NAVBAR (Enhanced)
    avatar_img = get_current_avatar()
    logo_tag = f'<img src="data:image/png;base64,{app_logo_b64}" class="nav-logo">' if app_logo_b64 else '🎓'
    
    st.markdown(f"""
    <div class="custom-navbar">
        <div style="display:flex; align-items:center;">
            {logo_tag}
            <div>
                <div class="brand-title">PEC CONNECT <span class="brand-badge">v2.0</span></div>
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:20px;">
            <div style="text-align:right; line-height:1.2;">
                <div style="font-weight:700; font-size:1rem; color:#1e293b;">{st.session_state['user']}</div>
                <div style="font-size:0.8rem; color:#64748b;">{st.session_state['role']}</div>
            </div>
            <img src="{avatar_img}" style="width:48px; height:48px; border-radius:50%; border: 3px solid white; box-shadow: 0 4px 6px rgba(0,0,0,0.1); object-fit: cover;">
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. HERO BANNER
    hero_content = f'<img src="data:image/png;base64,{college_banner_b64}" class="hero-college-img">' if college_banner_b64 else "<h1>PALLAVI ENGINEERING COLLEGE</h1>"
    st.markdown(f"""<div class="hero-box">{hero_content}</div>""", unsafe_allow_html=True)

    # 3. NOTICE BOARD
    today = datetime.now().strftime("%d %b, %Y")
    st.markdown(f"""
    <div class="notice-box">
        <div>
            <span style="font-weight: 800; color: #d97706; margin-right: 12px; font-size: 1.1rem;">🔔 UPDATE:</span>
            <span style="color: #92400e; font-weight: 500;">R24 Mid-Term Examinations scheduled for next week. Check Syllabus in Profile.</span>
        </div>
        <div style="font-size: 0.85rem; font-weight: 700; background: rgba(255,255,255,0.5); padding: 4px 10px; border-radius: 8px;">{today}</div>
    </div>
    """, unsafe_allow_html=True)

    # 4. STATS
    try:
        n_users = db.supabase.table("users").select("*", count="exact").execute().count
        n_notes = db.supabase.table("notes").select("*", count="exact").execute().count
    except:
        n_users = 120 # Fallback
        n_notes = 45

    st.markdown("### 📊 Overview")
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-num">{n_users}</div>
            <div class="stat-lbl">Active Students</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{n_notes}</div>
            <div class="stat-lbl">Resources Shared</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">24/7</div>
            <div class="stat-lbl">AI Tutor Status</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">R24</div>
            <div class="stat-lbl">Regulation</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 5. ACTION GRID
    st.markdown("### 🚀 Launchpad")
    
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown('<div class="action-card"><div class="ac-icon">👤</div><div class="ac-title">My Profile</div><div class="ac-desc">View Rank & Badge</div></div>', unsafe_allow_html=True)
        if st.button("Go to Profile", use_container_width=True): st.switch_page("pages/08_👤_Profile.py")
        
    with c2:
        st.markdown('<div class="action-card"><div class="ac-icon">📚</div><div class="ac-title">Notes Market</div><div class="ac-desc">Download PDFs</div></div>', unsafe_allow_html=True)
        if st.button("Browse Notes", use_container_width=True): st.switch_page("pages/01_📚_Notes_Marketplace.py")

    with c3:
        st.markdown('<div class="action-card"><div class="ac-icon">🤖</div><div class="ac-title">AI Tutor</div><div class="ac-desc">Instant Doubts</div></div>', unsafe_allow_html=True)
        if st.button("Ask AI", use_container_width=True): st.switch_page("pages/02_🤖_AI_Study_Bot.py")

    with c4:
        st.markdown('<div class="action-card"><div class="ac-icon">📝</div><div class="ac-title">Mock Tests</div><div class="ac-desc">Practice Exams</div></div>', unsafe_allow_html=True)
        if st.button("Take Test", use_container_width=True): st.switch_page("pages/04_📝_Mock_Tests.py")

    # 6. PROFESSIONAL FOOTER
    st.markdown("""
    <div class="pro-footer">
        <div class="footer-brand">PEC CONNECT</div>
        <div class="footer-credits">
            Academic Excellence Portal • <span class="version-tag">Version 2.0.4</span> <br><br>
            Designed & Developed by <span style="color: white; font-weight: 600;">K. Abhi Ram Reddy & Team</span> <br>
            Department of CSM | Pallavi Engineering College
        </div>
        <div class="footer-link">
             <a href="https://pallaviengineeringcollege.ac.in/" target="_blank">🌐 Visit Official College Website</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Secure Logout", type="secondary", use_container_width=True):
        del st.session_state["user"]
        st.rerun()