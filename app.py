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
st.set_page_config(
    page_title="PEC Connect | Student Portal",
    page_icon=favicon,
    layout="wide",
    initial_sidebar_state="collapsed"
)

db.init_db()

# --- HELPERS ---
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def get_current_avatar():
    if "user" in st.session_state:
        conn = db.sqlite3.connect('pec_data.db')
        c = conn.cursor()
        c.execute("SELECT avatar FROM users WHERE username=?", (st.session_state["user"],))
        res = c.fetchone()
        conn.close()
        if res and res[0]: return f"data:image/png;base64,{res[0]}"
        return f"https://api.dicebear.com/7.x/identicon/svg?seed={st.session_state['user']}"
    return None

# Load Assets
app_logo_b64 = get_base64_image("favicon.png")
college_banner_b64 = get_base64_image("pec_logo.png")

# --- 🎨 PROFESSIONAL CSS ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc; /* Global Light Grey Background */
        color: #0f172a;
    }}
    
    /* --- SIDEBAR FIX --- */
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0);
    }}
    
    .block-container {{ padding-top: 3rem; padding-bottom: 2rem; }}

    /* --- LOGIN LEFT SIDE TYPOGRAPHY --- */
    .hero-title {{
        font-size: 3.5rem; font-weight: 900; color: #1e293b; 
        line-height: 1.1; margin-bottom: 20px;
    }}
    .hero-highlight {{ color: #2563eb; }}
    
    .hero-sub {{
        font-size: 1.1rem; color: #64748b; line-height: 1.6; margin-bottom: 30px; font-weight: 400;
    }}
    
    .feature-list li {{
        margin-bottom: 12px; font-size: 1rem; color: #475569; display: flex; align-items: center;
    }}
    .check-icon {{ color: #10b981; margin-right: 12px; font-weight: bold; }}

    /* --- FIX: LOGIN CARD STYLING --- */
    /* This targets the specific container for the login form */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: white;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }}

    .login-logo-img {{
        width: 180px; 
        height: auto; 
        margin-bottom: 10px;
        display: block; margin-left: auto; margin-right: auto;
    }}
    .login-header {{ font-size: 1.8rem; font-weight: 800; color: #0f172a; margin-bottom: 5px; }}
    
    /* --- DASHBOARD NAVBAR --- */
    .custom-navbar {{
        display: flex; justify-content: space-between; align-items: center;
        background: white; padding: 12px 25px; border-radius: 12px;
        border-bottom: 2px solid #e2e8f0; margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03);
    }}
    .nav-logo {{ width: 70px; height: 70px; object-fit: contain; }}
    .brand-title {{ font-weight: 800; font-size: 1.4rem; color: #0f172a; }}
    .brand-badge {{ 
        background: #eff6ff; color: #2563eb; font-size: 0.7rem; 
        padding: 4px 10px; border-radius: 20px; font-weight: 700; letter-spacing: 0.5px; margin-left: 10px;
    }}

    /* --- HERO & STATS --- */
    .hero-box {{
        background: #0f172a; padding: 2.5rem; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; 
        box-shadow: 0 15px 30px -10px rgba(15, 23, 42, 0.5);
        display: flex; justify-content: center; align-items: center;
        overflow: hidden;
    }}
    .hero-college-img {{ max-width: 500px; width: 50%; height: auto; opacity: 0.9; }}
    
    .stat-row {{
        display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px;
    }}
    .stat-card {{
        background: white; padding: 20px; border-radius: 16px; text-align: center;
        border: 1px solid #e2e8f0; box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        transition: transform 0.2s;
    }}
    .stat-card:hover {{ transform: translateY(-5px); border-color: #cbd5e1; }}
    .stat-num {{ font-size: 2rem; font-weight: 800; color: #3b82f6; }}
    .stat-lbl {{ font-size: 0.85rem; font-weight: 600; color: #64748b; text-transform: uppercase; }}

    /* --- NOTICE BOX --- */
    .notice-box {{
        background: #fffbeb; border-radius: 12px; padding: 15px 20px;
        border: 1px solid #fcd34d; color: #92400e;
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 30px;
    }}

    /* --- ACTION GRID --- */
    .action-grid {{
        display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px;
    }}
    .action-card {{
        background: white; padding: 30px; border-radius: 16px;
        text-align: center; border: 1px solid #e2e8f0;
        transition: all 0.3s ease; cursor: pointer; height: 100%;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    }}
    .action-card:hover {{ 
        transform: translateY(-8px); 
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); border-color: #3b82f6; 
    }}
    .ac-icon {{ font-size: 2.2rem; margin-bottom: 10px; display: block; }}
    .ac-title {{ font-weight: 700; color: #1e293b; margin-bottom: 5px; font-size: 1.05rem; }}
    .ac-desc {{ font-size: 0.8rem; color: #94a3b8; }}

    /* --- FOOTER --- */
    .pro-footer {{
        background: #1e293b; color: #f8fafc; padding: 40px 0; margin-top: 50px;
        border-top: 4px solid #3b82f6; text-align: center;
    }}
    .footer-brand {{ font-size: 1.2rem; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 10px; }}
    .footer-credits {{ color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px; }}
    .footer-link a {{ color: #60a5fa; text-decoration: none; font-weight: 600; }}
    .footer-link a:hover {{ text-decoration: underline; }}
    .version-tag {{ 
        background: rgba(255,255,255,0.1); padding: 3px 10px; 
        border-radius: 20px; font-size: 0.75rem; color: #e2e8f0; margin-left: 8px;
    }}

</style>
""", unsafe_allow_html=True)

# --- UI LOGIC ---

if "user" not in st.session_state:
    # === SCENE 1: THE SPLIT LOGIN (Perfected) ===
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
            <ul class="feature-list">
                <li><span class="check-icon">✓</span> Verified R24/R22 Notes & Resources</li>
                <li><span class="check-icon">✓</span> 24/7 AI Tutor & Doubt Solver</li>
                <li><span class="check-icon">✓</span> Real-time Mock Tests & Analytics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with c_right:
        # LOGIN CARD (Using Native Container for strict wrapping)
        with st.container(border=True): # <--- THIS FIXES THE LAYOUT ISSUE
            if app_logo_b64:
                st.markdown(f"""
                <div style="text-align: center; margin-bottom: 15px;">
                    <img src="data:image/png;base64,{app_logo_b64}" class="login-logo-img">
                    <div class="login-header">PEC Connect</div>
                    <div style="color: #64748b; font-size: 0.95rem;">Student Success Portal</div>
                </div>
                """, unsafe_allow_html=True)
            
            tab1, tab2 = st.tabs(["🔒 Secure Login", "📝 Register"])
            
            with tab1:
                u = st.text_input("Username", key="l_u", placeholder="Enter Roll Number")
                p = st.text_input("Password", type="password", key="l_p")
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🚀 Login to Portal", use_container_width=True, type="primary"):
                    user = db.check_login(u, p)
                    if user:
                        st.session_state["user"] = user[0]
                        st.session_state["role"] = user[2]
                        st.rerun()
                    else:
                        st.error("Invalid Credentials.")
            
            with tab2:
                c1, c2 = st.columns(2)
                fullname = c1.text_input("Full Name")
                email = c2.text_input("Email")
                nu = st.text_input("Roll Number")
                np = st.text_input("Set Password", type="password")
                c_role, c_year = st.columns(2)
                role = c_role.selectbox("Role", ["Student", "Mentor"])
                year = c_year.selectbox("Year", ["1st", "2nd", "3rd", "4th"])
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("✨ Create Account", use_container_width=True):
                    if db.add_user(nu, np, role, year): 
                        st.success("Registration Successful! Please Login.")

else:
    # === SCENE 2: PRO DASHBOARD ===
    
    # 1. NAVBAR
    avatar_img = get_current_avatar()
    logo_tag = f'<img src="data:image/png;base64,{app_logo_b64}" class="nav-logo">' if app_logo_b64 else '🎓'
    
    st.markdown(f"""
    <div class="custom-navbar">
        <div style="display:flex; align-items:center; gap:15px;">
            {logo_tag}
            <div>
                <span class="brand-title">PEC CONNECT</span>
                <span class="brand-badge">v2.0</span>
            </div>
        </div>
        <div style="display:flex; align-items:center; gap:20px;">
            <div style="text-align:right; line-height:1.2;">
                <div style="font-weight:700; font-size:0.95rem; color:#1e293b;">{st.session_state['user']}</div>
                <div style="font-size:0.75rem; color:#64748b;">{st.session_state['role']}</div>
            </div>
            <img src="{avatar_img}" style="width:42px; height:42px; border-radius:50%; border: 2px solid #e2e8f0;">
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. HERO BANNER
    hero_content = f'<img src="data:image/png;base64,{college_banner_b64}" class="hero-college-img">' if college_banner_b64 else "<h1>PALLAVI ENGINEERING COLLEGE</h1>"
    st.markdown(f"""<div class="hero-box">{hero_content}</div>""", unsafe_allow_html=True)

    # 3. NOTICE BOARD (Live Updates)
    today = datetime.now().strftime("%d %b, %Y")
    st.markdown(f"""
    <div class="notice-box">
        <div>
            <span style="font-weight: 800; color: #d97706; margin-right: 10px;">📢 LATEST UPDATE:</span>
            <span style="color: #92400e;">R24 Mid-Term Examinations scheduled for next week. Check Syllabus in Profile.</span>
        </div>
        <div style="font-size: 0.85rem; font-weight: 600;">{today}</div>
    </div>
    """, unsafe_allow_html=True)

    # 4. LIVE STATS
    conn = db.sqlite3.connect('pec_data.db')
    c = conn.cursor()
    n_users = c.execute("SELECT count(*) FROM users").fetchone()[0]
    n_notes = c.execute("SELECT count(*) FROM notes").fetchone()[0]
    conn.close()

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