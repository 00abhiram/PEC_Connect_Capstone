import streamlit as st
import database as db
import os
import base64
from datetime import datetime

db.init_db()

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def get_current_avatar():
    if "user" in st.session_state:
        avatar_data = db.get_user_avatar(st.session_state["user"])
        if avatar_data:
            if "http" in str(avatar_data):
                return avatar_data
            if len(str(avatar_data)) > 100:
                return f"data:image/png;base64,{avatar_data}"
        return f"https://api.dicebear.com/7.x/identicon/svg?seed={st.session_state['user']}"
    return None

app_logo_b64 = get_base64_image("favicon.png")
college_banner_b64 = get_base64_image("pec_logo.png")

# Set page config with logo
st.set_page_config(
    page_title="PEC Connect",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
    /* Hide top menu and footer */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    
    /* Keep header visible for default sidebar toggle */
    header {
        visibility: visible !important;
    }
    
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
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        width: 250px !important;
    }
    
    /* Input fields styling */
    .stTextInput input {
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
    }
    .stTextInput input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Button styling */
    .stButton > button {
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        border-color: #667eea !important;
        background: #667eea !important;
        color: white !important;
    }
    
    /* Form submit button */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border: none !important;
        color: white !important;
        border-radius: 8px !important;
    }
    .stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #5a71d4, #6a4190) !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        border: 2px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background: #667eea !important;
        color: white !important;
    }
    
    /* Selectbox styling */
    .stSelectbox div[data-baseweb="select"] {
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
    }
    
    /* Cards styling with borders */
    .stat-card, .quick-card, .notice-bar, .hero-box, .header-bar {
        border: 2px solid #e2e8f0 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    }
    
    .stat-card {
        background: white !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }
    
    .quick-card {
        background: white !important;
        border-radius: 12px !important;
        padding: 20px !important;
        transition: all 0.3s ease !important;
    }
    .quick-card:hover {
        border-color: #667eea !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2) !important;
    }
    
    .header-bar {
        background: white !important;
        border-radius: 12px !important;
        padding: 20px 25px !important;
    }
    
    /* Section title styling */
    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin: 25px 0 15px 0;
        color: #1e293b;
        padding-bottom: 10px;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Notice bar */
    .notice-bar {
        background: white !important;
        border-radius: 12px !important;
        padding: 15px 20px !important;
        border: 2px solid #e2e8f0 !important;
    }
    
    /* Hero box */
    .hero-box {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border-radius: 12px !important;
        border: 2px solid #e2e8f0 !important;
        padding: 25px !important;
        margin: 20px 0 !important;
    }
    
    /* Sidebar user section */
    .sidebar-user {
        background: #f8fafc;
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        border: 2px solid #e2e8f0;
    }
    
    /* Logout button styling */
    .stButton > button[kind="secondary"] {
        background: #fee2e2 !important;
        color: #dc2626 !important;
        border: 2px solid #fecaca !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #dc2626 !important;
        color: white !important;
        border-color: #dc2626 !important;
    }
    
    html, body { font-family: 'Segoe UI', sans-serif; }
    
    /* Login page - white background */
    .stApp {
        background: #FFFFFF !important;
    }
    
    /* Fix any white boxes */
    [data-testid="stAppViewContainer"] {
        background: #FFFFFF !important;
    }
    [data-testid="stMain"] {
        background: #FFFFFF !important;
    }
    
    /* Login card - fits logo perfectly */
    .login-card {
        background: white;
        border: 2px solid #667eea;
        border-radius: 16px;
        padding: 20px 30px;
        width: 340px;
        margin: 20px auto;
        box-shadow: 0 8px 30px rgba(102, 126, 234, 0.2);
    }
    
    /* Main content */
    .main-content {
        padding: 25px;
    }
    
    /* Header bar */
    .header-bar {
        background: white;
        border-radius: 14px;
        padding: 20px 25px;
        margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Stats cards */
    .stat-card {
        background: white;
        border-radius: 14px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        border: 2px solid #e2e8f0;
    }
    .stat-num {
        font-size: 2.2rem;
        font-weight: 800;
        color: #667eea;
    }
    .stat-lbl {
        font-size: 0.8rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    /* Quick action cards */
    .quick-card {
        background: white;
        border-radius: 14px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        transition: 0.3s;
        border: 2px solid #e2e8f0;
    }
    .quick-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    .quick-icon { font-size: 2.5rem; }
    .quick-title { font-weight: 700; margin-top: 10px; }
    .quick-desc { font-size: 0.8rem; color: #888; }
    
    /* Quick Access Button Styling */
    .stButton > button[kind="secondary"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #5a71d4, #6a4190) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Notice bar */
    .notice-bar {
        background: linear-gradient(90deg, #fef3c7, #fde68a);
        border-radius: 12px;
        padding: 14px 20px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
    }
    
    /* Hero */
    .hero-box {
        background: linear-gradient(135deg, #1e293b, #334155);
        border-radius: 14px;
        padding: 25px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Section title */
    .section-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 15px;
        color: #1e293b;
    }
    
    /* Footer */
    .app-footer {
        background: #1e293b;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        margin-top: 30px;
    }
    .footer-text {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    .footer-text b {
        color: white;
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<script>
    // Force sidebar to stay visible
    setInterval(function() {
        var sidebar = document.querySelector('[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.style.visibility = 'visible';
            sidebar.style.opacity = '1';
            sidebar.style.width = '250px';
        }
    }, 100);
</script>
""", unsafe_allow_html=True)

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

if st.query_params.get("logout") == "true":
    logout()

# ==================== LOGIN PAGE ====================
if "user" not in st.session_state:
    # Clean centered login
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Logo and Title
        if app_logo_b64:
            st.markdown(f'''
            <div style="text-align:center;margin-bottom:15px;">
                <img src="data:image/png;base64,{app_logo_b64}" style="width:140px;height:140px;border-radius:15px;border:4px solid #667eea;box-shadow:0 4px 20px rgba(102,126,234,0.3);">
            </div>
            ''', unsafe_allow_html=True)
        st.markdown("### 🎓 PEC Connect")
        st.markdown("*Your Academic Success Portal*")
        st.markdown("---")
        st.markdown("### 🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            login_btn = st.form_submit_button("🚀 Sign In", use_container_width=True)
            
            if login_btn:
                if username and password:
                    # Check for admin first (hidden admin login)
                    if username == "00abhiram" and password == "sita":
                        st.session_state["is_admin"] = True
                        st.session_state["admin_user"] = "00abhiram"
                        st.session_state["user"] = "00abhiram"
                        st.session_state["role"] = "admin"
                        st.rerun()
                    else:
                        user = db.check_login(username, password)
                        if user:
                            st.session_state["user"] = user['username']
                            st.session_state["role"] = user['role']
                            st.session_state["full_name"] = user.get('full_name', '')
                            st.rerun()
                        else:
                            st.error("❌ Invalid Credentials")
        
        st.markdown("---")
        
        with st.expander("📝 New User? Register Here"):
            with st.form("register_form"):
                c1, c2 = st.columns(2)
                with c1:
                    reg_name = st.text_input("Full Name", placeholder="Your name")
                with c2:
                    reg_email = st.text_input("Email", placeholder="your.email@example.com")
                
                c3, c4 = st.columns(2)
                with c3:
                    reg_user = st.text_input("Username", placeholder="Choose username")
                with c4:
                    reg_pass = st.text_input("Password", type="password", placeholder="Create password")
                
                c5, c6 = st.columns(2)
                with c5:
                    reg_role = st.selectbox("I am a", ["Student", "Mentor"])
                with c6:
                    reg_year = st.selectbox("Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
                
                reg_btn = st.form_submit_button("✨ Create Account", use_container_width=True)
                
                if reg_btn:
                    if reg_name and reg_email and reg_user and reg_pass:
                        year_val = reg_year.replace(" Year", "")
                        if db.add_user(reg_user, reg_pass, reg_role, year_val, reg_name, reg_email):
                            st.success("🎉 Account created! Please login.")
                        else:
                            st.error("Username already exists!")
                    else:
                        st.warning("Please fill all fields!")
        
        st.markdown("---")

# ==================== MAIN APP ====================
else:
    avatar_img = get_current_avatar()
    user_name = st.session_state.get("user", "User")
    user_role = st.session_state.get("role", "Student")
    
    # Main content
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Header
    today = datetime.now().strftime("%A, %d %B %Y")
    
    # Header with logo and welcome
    today = datetime.now().strftime("%A, %d %B %Y")
    
    # Header section with logo
    st.markdown(f'''
    <div class="header-bar">
        <div style="display:flex;align-items:center;gap:15px;">
            <img src="data:image/png;base64,{app_logo_b64}" style="width:60px;border-radius:12px;" onerror="this.style.display='none'">
            <div>
                <h2 style="margin:0;color:#1e293b;font-weight:700;">PEC Connect</h2>
                <p style="margin:5px 0 0 0;color:#64748b;">👋 Welcome back, <span style="color:#667eea;font-weight:700;">{user_name}</span>!</p>
                <p style="margin:2px 0 0 0;color:#94a3b8;font-size:0.85rem;">{today}</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Welcome message banner
    st.markdown(f'''
    <div style="background:linear-gradient(135deg, #667eea, #764ba2);border-radius:16px;padding:25px;margin:20px 0;text-align:center;">
        <h2 style="color:white;margin:0;font-size:1.8rem;font-weight:700;">🎓 Welcome to PEC Connect, {user_name}!</h2>
        <p style="color:rgba(255,255,255,0.9);margin:10px 0 0 0;font-size:1.1rem;">Your one-stop destination for academic excellence • Notes, AI Tutor, Mock Tests & More</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # College Banner
    if college_banner_b64:
        st.markdown(f'<div style="text-align:center;margin:15px 0;"><img src="data:image/png;base64,{college_banner_b64}" style="max-width:100%;max-height:100px;border-radius:12px;border:2px solid #e2e8f0;"></div>', unsafe_allow_html=True)
    
    # Notice - Show latest approved alert
    latest_alert = db.get_alerts()
    if latest_alert:
        notice_msg = latest_alert[0].get('message', '🔔 R24 Mid-Term Exams scheduled - Check Syllabus in Profile')
    else:
        notice_msg = "🔔 R24 Mid-Term Exams scheduled - Check Syllabus in Profile"
    
    st.markdown(f'''
    <div class="notice-bar">
        <span>🔔 {notice_msg}</span>
        <span style="background:rgba(255,255,255,0.5);padding:3px 10px;border-radius:6px;font-size:12px;">{datetime.now().strftime("%d %b")}</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # Check if admin
    is_admin = st.session_state.get("is_admin", False)
    
    # User: Request notification update
    if not is_admin and "user" in st.session_state:
        with st.expander("📢 Request Notification Update"):
            st.markdown("**Submit a request to update the front notification:**")
            with st.form("notification_request"):
                notif_title = st.text_input("Notification Title", placeholder="e.g., Exam Schedule Update")
                notif_desc = st.text_area("Description (2 lines max)", placeholder="Describe the announcement in detail...")
                notif_date = st.date_input("Select Date")
                submit_req = st.form_submit_button("Submit Request")
                
                if submit_req:
                    if notif_title and notif_desc and notif_date:
                        if db.create_notification_request(notif_title, notif_desc, str(notif_date), st.session_state["user"]):
                            st.success("Request submitted to admin for approval!")
                        else:
                            st.error("Failed to submit request")
                    else:
                        st.warning("Please fill all fields")
    
    # Alert Notifications
    alerts = db.get_alerts()
    if alerts:
        for alert in alerts[:5]:
            st.markdown(f"""
            <div style="background: #fee2e2; border-left: 4px solid #dc2626; padding: 15px; border-radius: 8px; margin-bottom: 10px;">
                <strong>🔔 ALERT:</strong> {alert.get('message', '')}
            </div>
            """, unsafe_allow_html=True)
    
    # Admin: Create alert
    is_admin = st.session_state.get("is_admin", False)
    if is_admin:
        with st.expander("🛡️ Admin - Settings"):
            st.markdown("### 🔐 Change Admin Password")
            new_admin_pass = st.text_input("New Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")
            if st.button("Update Password"):
                if new_admin_pass and confirm_pass:
                    if new_admin_pass == confirm_pass:
                        if db.update_password("00abhiram", new_admin_pass):
                            st.success("Admin password updated successfully!")
                        else:
                            st.error("Failed to update password")
                    else:
                        st.error("Passwords do not match!")
                else:
                    st.warning("Please fill both fields")
        
        # Create Alert - outside the settings expander
        with st.expander("🛡️ Admin - Create Alert Notification"):
            new_alert = st.text_area("Alert Message")
            if st.button("Post Alert"):
                if new_alert:
                    db.create_alert(new_alert)
                    st.success("Alert posted!")
                    st.rerun()
        
        # Review Notification Requests - outside the settings expander
        with st.expander("📢 Review Notification Requests"):
            requests = db.get_notification_requests()
            pending_requests = [r for r in requests if r.get('status') == 'pending']
            
            if not pending_requests:
                st.info("No pending notification requests")
            else:
                for req in pending_requests:
                    with st.container():
                        st.markdown(f"""
                        <div style="background: #fef3c7; border: 2px solid #f59e0b; border-radius: 12px; padding: 15px; margin-bottom: 10px;">
                            <strong>📌 {req.get('title', 'N/A')}</strong><br>
                            <small>Requested by: {req.get('requested_by', 'N/A')}</small><br>
                            <p style="margin: 10px 0;">📝 {req.get('description', 'N/A')}</p>
                            <small>📅 Date: {req.get('date', 'N/A')}</small>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button(f"✅ Approve", key=f"approve_req_{req.get('id')}"):
                                db.approve_notification_request(
                                    req.get('id'),
                                    req.get('title'),
                                    req.get('description'),
                                    req.get('date')
                                )
                                st.success("Request approved and notification posted!")
                                st.rerun()
                        with c2:
                            if st.button(f"❌ Reject", key=f"reject_req_{req.get('id')}"):
                                db.reject_notification_request(req.get('id'))
                                st.warning("Request rejected")
                                st.rerun()
            
            # Show all requests
            if requests:
                st.markdown("#### All Requests")
                for req in requests[:10]:
                    status_color = "🟡" if req.get('status') == 'pending' else "🟢" if req.get('status') == 'approved' else "🔴"
                    st.markdown(f"- {status_color} **{req.get('title')}** - {req.get('status')} (by {req.get('requested_by')})")
        
        # Delete alerts
        if alerts:
            st.markdown("### Existing Alerts")
            for alert in alerts:
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"📢 {alert.get('message', '')}")
                with c2:
                    if st.button("Delete", key=f"del_alert_{alert.get('id')}"):
                        db.delete_alert(alert.get('id'))
                        st.rerun()
    
    # Stats
    try:
        n_users = len(db.supabase.table("users").select("*").execute().data or [])
        n_notes = len(db.supabase.table("notes").select("*").execute().data or [])
    except:
        n_users, n_notes = 120, 45
    
    st.markdown('<div class="section-title">📊 Dashboard Overview</div>', unsafe_allow_html=True)
    
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown(f'''<div class="stat-card"><div class="stat-num">{n_users}</div><div class="stat-lbl">Active Students</div></div>''', unsafe_allow_html=True)
    with s2:
        st.markdown(f'''<div class="stat-card"><div class="stat-num">{n_notes}</div><div class="stat-lbl">Resources</div></div>''', unsafe_allow_html=True)
    with s3:
        st.markdown('''<div class="stat-card"><div class="stat-num">24/7</div><div class="stat-lbl">AI Status</div></div>''', unsafe_allow_html=True)
    with s4:
        st.markdown('''<div class="stat-card"><div class="stat-num">R24</div><div class="stat-lbl">Regulation</div></div>''', unsafe_allow_html=True)
    
    # Quick Access - Clickable navigation
    st.markdown('<div class="section-title">🚀 Quick Access</div>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('''<div class="quick-card"><div class="quick-icon">📚</div><div class="quick-title">Notes Market</div><div class="quick-desc">Browse & Download</div></div>''', unsafe_allow_html=True)
        if st.button("📚 Open Notes", key="btn_notes", use_container_width=True):
            st.switch_page("pages/01_📚_Notes_Marketplace.py")
    with c2:
        st.markdown('''<div class="quick-card"><div class="quick-icon">🤖</div><div class="quick-title">AI Tutor</div><div class="quick-desc">Ask Doubts</div></div>''', unsafe_allow_html=True)
        if st.button("🤖 Open AI Tutor", key="btn_ai", use_container_width=True):
            st.switch_page("pages/02_🤖_AI_Study_Bot.py")
    with c3:
        st.markdown('''<div class="quick-card"><div class="quick-icon">📝</div><div class="quick-title">Mock Tests</div><div class="quick-desc">Practice Online</div></div>''', unsafe_allow_html=True)
        if st.button("📝 Open Mock Tests", key="btn_tests", use_container_width=True):
            st.switch_page("pages/04_📝_Mock_Tests.py")
    with c4:
        st.markdown('''<div class="quick-card"><div class="quick-icon">💬</div><div class="quick-title">Forum</div><div class="quick-desc">Ask Questions</div></div>''', unsafe_allow_html=True)
        if st.button("💬 Open Forum", key="btn_forum", use_container_width=True):
            st.switch_page("pages/05_🗣️_Doubt_Forum.py")
    
    # Logout button at bottom
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Admin logout
    if st.session_state.get("is_admin", False):
        if st.button("🚪 Exit Admin Mode", use_container_width=True, type="primary"):
            del st.session_state["is_admin"]
            del st.session_state["admin_user"]
            st.rerun()
    
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
        logout()
    
    # Footer - now visible on dark background
    st.markdown('''
    <div class="app-footer">
        <div class="footer-text">
            <b>PEC Connect v2.0</b> • Designed by <b>K. Abhi Ram Reddy & Team</b><br>
            Department of CSM | Pallavi Engineering College
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
