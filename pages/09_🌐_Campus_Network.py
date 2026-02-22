import streamlit as st
import database as db

db.init_db()

# Check for admin
is_admin = st.session_state.get("is_admin", False)

# Sidebar toggle CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Keep header visible for sidebar toggle */
    [data-testid="stHeader"] { 
        display: block !important; 
        visibility: visible !important;
    }
    #MainMenu, footer { visibility: hidden !important; }
    
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
    
    section[data-testid="stSidebar"] { background: #FFFFFF !important; }
    section[data-testid="stSidebar"] * { color: #1a1a1a !important; }
    
    .admin-banner {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white; padding: 10px 20px; border-radius: 10px;
        margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;
    }
    .admin-banner h3 { margin: 0; }
    
    .network-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 24px; padding: 40px; margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.25);
    }
    .network-title { color: white; font-size: 2.2rem; font-weight: 800; margin: 0; }
    .network-subtitle { color: rgba(255,255,255,0.85); font-size: 1.1rem; margin-top: 8px; }
    
    .stTextInput > div > div > input {
        border-radius: 12px; border: 2px solid #e2e8f0;
        padding: 12px 16px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #667eea; box-shadow: 0 0 0 3px rgba(102,126,234,0.1);
    }
    
    .user-card {
        background: white; border-radius: 16px; padding: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06); border: 1px solid #f1f5f9;
    }
    .user-card:hover { box-shadow: 0 8px 25px rgba(102,126,234,0.15); }
    
    .user-avatar {
        width: 80px; height: 80px; border-radius: 50%;
        object-fit: cover; border: 3px solid #667eea;
    }
    
    .user-name { font-weight: 700; font-size: 1.1rem; color: #1e293b; }
    .user-username { color: #64748b; font-size: 0.9rem; }
    .user-role {
        display: inline-block; background: linear-gradient(135deg, #667eea20, #764ba220);
        color: #667eea; padding: 4px 10px; border-radius: 12px;
        font-size: 0.75rem; font-weight: 600;
    }
    
    .btn-connect {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important; border: none !important;
        border-radius: 10px !important; font-weight: 600 !important;
        padding: 10px 20px !important;
    }
    .btn-connect:hover {
        box-shadow: 0 5px 15px rgba(102,126,234,0.4) !important;
    }
    
    .btn-view {
        background: #f1f5f9 !important; color: #1e293b !important;
        border: none !important; border-radius: 10px !important;
        font-weight: 600 !important; padding: 10px 20px !important;
    }
    .btn-view:hover { background: #e2e8f0 !important; }
    
    .btn-message {
        background: #10b981 !important; color: white !important;
        border: none !important; border-radius: 10px !important;
        font-weight: 600 !important; padding: 10px 20px !important;
    }
    
    .stat-pill {
        background: #f8fafc; padding: 6px 12px; border-radius: 20px;
        font-size: 0.8rem; color: #64748b;
    }
    .stat-pill strong { color: #667eea; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="network-header">
    <h1 class="network-title">🌐 Campus Network</h1>
    <p class="network-subtitle">Connect with talented students across all years</p>
</div>
""", unsafe_allow_html=True)

if is_admin:
    st.markdown("""
    <div class="admin-banner">
        <h3>🛡️ Admin Mode - Full Access</h3>
    </div>
    """, unsafe_allow_html=True)

c_search, c_filter = st.columns([3, 1])
with c_search:
    search = st.text_input("🔍", placeholder="Search students by name or username...", key="net_search")

with c_filter:
    role_filter = st.selectbox("Filter", ["All", "Student", "Mentor"], key="net_role_filter")

if search:
    users = db.search_users(search) or []
else:
    users = db.get_leaderboard() or []

current_user = st.session_state.get("user")
if current_user:
    users = [u for u in users if u.get('username') != current_user]

if role_filter != "All":
    users = [u for u in users if u.get('role') == role_filter]

total_students = len(users)
mentors = len([u for u in users if u.get('role') == 'Mentor'])

col1, col2 = st.columns(2)
with col1: st.metric("Total Students", total_students)
with col2: st.metric("Mentors", mentors)

st.markdown("---")

if not users:
    st.info("👥 No students found. Try adjusting your search or filter.")
else:
    for user in users[:12]:
        uname = user.get('username', '')
        
        user_details = db.get_user_details(uname)
        if user_details:
            fname = user_details.get('full_name', uname)
            role = user_details.get('role', 'Student')
            points = user_details.get('points', 0)
            streak = user_details.get('streak', 0)
            
            year_raw = user_details.get('year', '1')
            try:
                year_val = int(year_raw) if isinstance(year_raw, str) else (year_raw if isinstance(year_raw, int) else 1)
            except:
                year_val = 1
            year_map = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th"}
            year_display = year_map.get(year_val, f"{year_val}th")
        else:
            fname = uname
            role = 'Student'
            points = 0
            streak = 0
            year_display = "1st"
        
        av = db.get_avatar_url(uname)
        
        col_avatar, col_info, col_actions = st.columns([1, 2, 2])
        
        with col_avatar:
            st.image(av, width=80, output_format="PNG")
        
        with col_info:
            st.markdown(f"**{fname}**")
            st.caption(f"@{uname}")
            st.markdown(f'<span class="user-role">{role}</span>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="margin-top: 8px;">
                <span class="stat-pill"><strong>⭐</strong> {points} pts</span>
                <span class="stat-pill"><strong>🔥</strong> {streak}</span>
                <span class="stat-pill"><strong>📅</strong> {year_display} Year</span>
            </div>
            """, unsafe_allow_html=True)
        
        with col_actions:
            # Admin controls
            if is_admin and uname != current_user:
                c_admin1, c_admin2 = st.columns(2)
                with c_admin1:
                    if st.button("🗑️", key=f"admin_del_{uname}", help="Delete User Account"):
                        db.delete_user(uname)
                        st.success("User deleted!")
                        st.rerun()
                with c_admin2:
                    if st.button("⚠️", key=f"admin_warn_{uname}", help="Warn User"):
                        warning_msg = "Your account has been flagged for suspicious activity. Please contact admin."
                        db.send_warning(uname, warning_msg)
                        st.warning("Warning sent!")
                        st.rerun()
            
            if current_user:
                status = db.get_connection_status(current_user, uname)
                
                if status == 'accepted':
                    if st.button("💬 Message", key=f"msg_{uname}", type="primary", use_container_width=True):
                        st.session_state["chat_with"] = uname
                        st.switch_page("pages/10_💬_Messages.py")
                    if st.button("👤 View Profile", key=f"view_{uname}", use_container_width=True):
                        st.session_state["viewing_user"] = uname
                        st.switch_page("pages/08_👤_Profile.py")
                elif status == 'pending':
                    st.button("🕒 Request Sent", key=f"wait_{uname}", disabled=True, use_container_width=True)
                else:
                    if st.button("➕ Connect", key=f"add_{uname}", type="primary", use_container_width=True):
                        db.send_connection_request(current_user, uname)
                        st.rerun()
                    if st.button("👤 View Profile", key=f"view2_{uname}", use_container_width=True):
                        st.session_state["viewing_user"] = uname
                        st.switch_page("pages/08_👤_Profile.py")
            else:
                if st.button("👤 View Profile", key=f"view3_{uname}", use_container_width=True):
                    st.session_state["viewing_user"] = uname
                    st.switch_page("pages/08_👤_Profile.py")
        
        st.markdown("---")
