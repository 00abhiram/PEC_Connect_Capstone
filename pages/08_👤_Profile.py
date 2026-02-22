import streamlit as st
import database as db
import pandas as pd
import plotly.graph_objects as go

db.init_db()

# Check for admin
is_admin = st.session_state.get("is_admin", False)
admin_user = st.session_state.get("admin_user", "")

# Professional Profile Page CSS
st.markdown("""
<style>
    /* Keep header visible for sidebar toggle */
    [data-testid="stHeader"] { 
        display: block !important; 
        visibility: visible !important;
    }
    #MainMenu, footer { visibility: hidden !important; }
    html, body { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    
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
    
    /* Admin Banner */
    .admin-banner {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white; padding: 12px 20px; border-radius: 12px;
        margin-bottom: 20px; display: flex; align-items: center; gap: 10px;
        box-shadow: 0 4px 15px rgba(220, 38, 38, 0.3);
    }
    .admin-banner h3 { margin: 0; font-size: 1rem; }
    
    /* Profile Hero Section */
    .profile-hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 24px; padding: 40px;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        margin-bottom: 30px;
        position: relative;
        overflow: hidden;
    }
    .profile-hero::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 300px;
        height: 300px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
    }
    
    .profile-avatar {
        width: 140px; height: 140px;
        border-radius: 50%;
        border: 5px solid white;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        object-fit: cover;
    }
    
    .profile-name {
        font-size: 2rem; font-weight: 800; color: white;
        margin-top: 15px; letter-spacing: -0.5px;
    }
    .profile-username {
        font-size: 1.1rem; color: rgba(255,255,255,0.85);
        font-weight: 500; margin-top: 5px;
    }
    .profile-headline {
        font-size: 1rem; color: rgba(255,255,255,0.75);
        margin-top: 8px; max-width: 500px;
    }
    
    /* Stats Cards */
    .stats-container {
        display: flex; gap: 15px; margin-top: 25px;
    }
    .stat-card {
        background: rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        border-radius: 16px; padding: 15px 25px;
        text-align: center; border: 1px solid rgba(255,255,255,0.2);
    }
    .stat-card-num {
        font-size: 1.8rem; font-weight: 800; color: white;
    }
    .stat-card-lbl {
        font-size: 0.75rem; color: rgba(255,255,255,0.7);
        text-transform: uppercase; letter-spacing: 1px;
    }
    
    /* Action Buttons */
    .action-btn {
        background: white; color: #667eea;
        border: none; padding: 12px 24px; border-radius: 12px;
        font-weight: 600; cursor: pointer; transition: all 0.3s;
        display: inline-flex; align-items: center; gap: 8px;
    }
    .action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    }
    .action-btn-outline {
        background: transparent; color: white;
        border: 2px solid rgba(255,255,255,0.5);
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.3rem; font-weight: 700; color: #1e293b;
        margin: 30px 0 20px 0; padding-bottom: 10px;
        border-bottom: 2px solid #e2e8f0;
    }
    .section-header span {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Skill Badges */
    .skill-badge {
        background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
        color: #0369a1; padding: 10px 18px; border-radius: 25px;
        font-size: 0.85rem; font-weight: 600; display: inline-block; margin: 4px;
        border: 1px solid #bae6fd;
        box-shadow: 0 2px 8px rgba(3, 105, 161, 0.1);
    }
    .skill-badge-verified {
        background: linear-gradient(135deg, #ecfdf5, #d1fae5);
        color: #047857; border-color: #a7f3d0;
    }
    
    /* Note Cards */
    .note-card {
        background: white; border: 1px solid #e2e8f0;
        padding: 20px; border-radius: 16px; margin-bottom: 15px;
        display: flex; justify-content: space-between; align-items: center;
        transition: all 0.3s; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .note-card:hover {
        border-color: #667eea; box-shadow: 0 8px 25px rgba(102,126,234,0.15);
        transform: translateY(-2px);
    }
    .note-title { font-weight: 700; color: #1e293b; font-size: 1rem; }
    .note-meta { font-size: 0.8rem; color: #64748b; margin-top: 4px; }
    .note-price {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white; padding: 10px 18px; border-radius: 10px;
        font-weight: 700;
    }
    
    /* Connection Request Items */
    .request-card {
        background: white; border: 1px solid #e2e8f0;
        border-radius: 16px; padding: 16px; margin-bottom: 12px;
        display: flex; align-items: center; justify-content: space-between;
        transition: all 0.2s;
    }
    .request-card:hover {
        border-color: #667eea; box-shadow: 0 4px 15px rgba(102,126,234,0.1);
    }
    .request-user {
        display: flex; align-items: center; gap: 12px;
    }
    .request-avatar {
        width: 50px; height: 50px; border-radius: 50%;
        border: 2px solid #667eea;
    }
    .request-name { font-weight: 700; color: #1e293b; }
    .request-fullname { font-size: 0.85rem; color: #64748b; }
    
    /* Action Buttons in Request */
    .accept-btn {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white; border: none; padding: 10px 20px;
        border-radius: 10px; font-weight: 600; cursor: pointer;
    }
    .reject-btn {
        background: #fee2e2; color: #dc2626;
        border: none; padding: 10px 20px;
        border-radius: 10px; font-weight: 600; cursor: pointer;
    }
    
    /* Edit Profile Card */
    .edit-card {
        background: white; border-radius: 20px; padding: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        margin-bottom: 25px;
    }
    .edit-header {
        font-size: 1.2rem; font-weight: 700; color: #1e293b;
        margin-bottom: 20px; display: flex; align-items: center; gap: 10px;
    }
    
    /* Delete Account Section */
    .delete-card {
        background: #fef2f2; border: 2px solid #fecaca;
        border-radius: 16px; padding: 25px; margin-top: 30px;
    }
    .delete-title {
        color: #dc2626; font-weight: 700; font-size: 1.1rem;
        margin-bottom: 10px; display: flex; align-items: center; gap: 8px;
    }
    .delete-warning {
        color: #991b1b; font-size: 0.9rem; margin-bottom: 15px;
    }
    
    /* Tabs Styling */
    .profile-tabs .stTabs [data-baseweb="tab-list"] { 
        gap: 10px; border-bottom: 2px solid #e2e8f0; 
    }
    .profile-tabs .stTabs [data-baseweb="tab"] {
        height: 50px; padding: 0 24px; border-radius: 12px 12px 0 0;
        background: transparent; color: #64748b; font-weight: 600;
        border: none; border-bottom: 3px solid transparent;
    }
    .profile-tabs .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #667eea !important;
        border-bottom: 3px solid #667eea;
    }
    
    /* Social Links */
    .social-link {
        display: inline-flex; align-items: center; gap: 8px;
        padding: 12px 20px; border-radius: 12px; text-decoration: none;
        font-weight: 600; transition: all 0.3s;
    }
    .linkedin-link { background: #e0f2fe; color: #0077b5; }
    .linkedin-link:hover { background: #0077b5; color: white; }
    .github-link { background: #f1f5f9; color: #1e293b; }
    .github-link:hover { background: #1e293b; color: white; }
    
    /* Empty State */
    .empty-state {
        text-align: center; padding: 50px 20px;
        background: #f8fafc; border-radius: 16px;
    }
    .empty-icon { font-size: 3rem; margin-bottom: 15px; }
    .empty-text { color: #64748b; font-size: 1rem; }
    
    /* Fullscreen Button */
    .fullscreen-btn {
        display: block;
        margin: 10px auto 0;
        background: rgba(255,255,255,0.2);
        color: white;
        border: 1px solid rgba(255,255,255,0.3);
        padding: 8px 16px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.85rem;
        transition: all 0.3s;
    }
    .fullscreen-btn:hover {
        background: rgba(255,255,255,0.3);
    }
</style>
""", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.warning("Please Login.")
    st.stop()

current_user = st.session_state["user"]
target_user = st.session_state.get("viewing_user", current_user)

# Admin controls in sidebar
if is_admin:
    st.sidebar.markdown("---")
    st.sidebar.markdown("🛡️ **Admin Controls**")
    
    admin_view_user = st.sidebar.text_input("View User Profile", placeholder="Enter username")
    if admin_view_user:
        st.session_state["viewing_user"] = admin_view_user
        st.rerun()
    
    if st.sidebar.button("🗑️ Delete This Account"):
        if target_user != admin_user:
            db.delete_user(target_user)
            st.sidebar.success(f"Account {target_user} deleted!")
            st.session_state["viewing_user"] = current_user
            st.rerun()
        else:
            st.sidebar.error("Cannot delete admin account!")
    
    if st.sidebar.button("⚠️ Send Warning"):
        warning_msg = "Your account has been flagged for violating community guidelines. Contact admin."
        db.send_warning(target_user, warning_msg)
        st.sidebar.warning(f"Warning sent to {target_user}!")

is_me = (current_user == target_user)
user_data = db.get_user_details(target_user)
if not user_data: st.error("User not found."); st.stop()

avatar_src = db.get_avatar_url(target_user)
fullname = user_data.get('full_name', target_user)
headline = user_data.get('headline', "Student at Pallavi Engineering College")
about_text = user_data.get('about_text', "")
verified_skills = db.get_verified_skills(target_user)

year_raw = user_data.get('year', '1')
try:
    year_val = int(year_raw) if isinstance(year_raw, str) else (year_raw if isinstance(year_raw, int) else 1)
except:
    year_val = 1

year_map = {1: "1st Year", 2: "2nd Year", 3: "3rd Year", 4: "4th Year"}
year_display = year_map.get(year_val, f"{year_val}th Year")

user_points = user_data.get('points', 0)
user_streak = user_data.get('streak', 0)

# Profile Hero Section with Purple Background
st.markdown(f"""
<div class="profile-hero-section" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; padding: 30px; margin-bottom: 25px; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);">
    <div style="display: flex; align-items: center; gap: 25px;">
        <div style="flex-shrink: 0;">
            <img src="{avatar_src}" style="width: 120px; height: 120px; border-radius: 50%; border: 4px solid white; box-shadow: 0 8px 25px rgba(0,0,0,0.2); object-fit: cover;">
        </div>
        <div style="flex: 1;">
            <div style="font-size: 1.8rem; font-weight: 800; color: white; letter-spacing: -0.5px;">{fullname}</div>
            <div style="font-size: 1.1rem; color: rgba(255,255,255,0.85); font-weight: 500; margin-top: 4px;">@{target_user}</div>
            <div style="font-size: 0.95rem; color: rgba(255,255,255,0.75); margin-top: 6px;">{headline}</div>
            <div style="display: flex; gap: 15px; margin-top: 18px;">
                <div style="background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); border-radius: 12px; padding: 12px 20px; text-align: center; border: 1px solid rgba(255,255,255,0.25);">
                    <div style="font-size: 1.5rem; font-weight: 800; color: white;">{user_points}</div>
                    <div style="font-size: 0.7rem; color: rgba(255,255,255,0.7); text-transform: uppercase; letter-spacing: 1px;">Points</div>
                </div>
                <div style="background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); border-radius: 12px; padding: 12px 20px; text-align: center; border: 1px solid rgba(255,255,255,0.25);">
                    <div style="font-size: 1.5rem; font-weight: 800; color: white;">{user_streak} 🔥</div>
                    <div style="font-size: 0.7rem; color: rgba(255,255,255,0.7); text-transform: uppercase; letter-spacing: 1px;">Streak</div>
                </div>
                <div style="background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); border-radius: 12px; padding: 12px 20px; text-align: center; border: 1px solid rgba(255,255,255,0.25);">
                    <div style="font-size: 1.5rem; font-weight: 800; color: white;">{year_display}</div>
                    <div style="font-size: 0.7rem; color: rgba(255,255,255,0.7); text-transform: uppercase; letter-spacing: 1px;">Year</div>
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Action Buttons
action_cols = st.columns([1, 1, 1])
with action_cols[0]:
    if is_me:
        st.markdown("###")  # Spacer
with action_cols[1]:
    if not is_me:
        status = db.get_connection_status(current_user, target_user)
        if status == 'accepted':
            if st.button("💬 Message", use_container_width=True, type="primary"):
                st.session_state["chat_with"] = target_user
                st.switch_page("pages/10_💬_Messages.py")
        elif status == 'pending':
            st.button("🕒 Request Sent", disabled=True, use_container_width=True)
        else:
            if st.button("➕ Connect", use_container_width=True, type="primary"):
                db.send_connection_request(current_user, target_user)
                st.rerun()
with action_cols[2]:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

# Edit Profile Section - using expander instead of session_state
if is_me:
    with st.expander("⚙️ Edit My Profile", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            n_name = st.text_input("Full Name", value=fullname, key="n_name")
            n_year = st.selectbox("Year", ["1", "2", "3", "4"], index=year_val-1, help="Select your year", key="n_year")
        with c2:
            n_head = st.text_input("Headline", value=headline, placeholder="e.g., CSE Student | AI Enthusiast", key="n_head")
        
        n_bio = st.text_area("About", value=about_text, placeholder="Tell others about yourself...", key="n_bio")
        
        c3, c4 = st.columns(2)
        with c3:
            n_li = st.text_input("LinkedIn URL", value=user_data.get("linkedin_url", ""), key="n_li")
        with c4:
            n_gh = st.text_input("GitHub URL", value=user_data.get("github_url", ""), key="n_gh")
        
        n_pic = st.file_uploader("Change Profile Picture", type=['png','jpg','jpeg'], key="n_pic")
        
        col_save, col_cancel = st.columns(2)
        with col_save:
            if st.button("💾 Save Changes", type="primary", use_container_width=True, key="save_profile"):
                updates = {"full_name": n_name, "headline": n_head, "year": n_year, "about_text": n_bio, "linkedin_url": n_li, "github_url": n_gh}
                if n_pic:
                    db.update_avatar(current_user, n_pic.getvalue(), n_pic.type)
                db.supabase.table("users").update(updates).eq("username", current_user).execute()
                st.success("Profile updated!")
                st.rerun()
        with col_cancel:
            if st.button("Cancel", use_container_width=True, key="cancel_profile"):
                st.rerun()

# About Section
if about_text:
    st.markdown('<div class="section-header">About</div>', unsafe_allow_html=True)
    st.markdown(f"<div style='color: #475569; line-height: 1.8; font-size: 1rem;'>{about_text}</div>", unsafe_allow_html=True)

# Skills Section
if verified_skills:
    st.markdown('<div class="section-header">🏆 Verified Skills</div>', unsafe_allow_html=True)
    for skill in verified_skills:
        st.markdown(f"<span class='skill-badge skill-badge-verified'>✓ {skill}</span>", unsafe_allow_html=True)
    st.markdown("")

# Links Section
li = user_data.get('linkedin_url', '')
gh = user_data.get('github_url', '')
if li or gh:
    st.markdown('<div class="section-header">🔗 Links</div>', unsafe_allow_html=True)
    if li:
        st.markdown(f'<a href="{li}" target="_blank" class="social-link linkedin-link">LinkedIn ↗</a>', unsafe_allow_html=True)
    if gh:
        st.markdown(f'<a href="{gh}" target="_blank" class="social-link github-link">GitHub ↗</a>', unsafe_allow_html=True)

st.markdown("---")

# Tabs Section
t_labels = ["📊 Skills & Stats", "📚 My Notes"]
if is_me: t_labels.append("🔔 Requests")

tabs = st.tabs(t_labels)

with tabs[0]:
    tests = db.get_user_test_history(target_user)
    has_skills = verified_skills and len(verified_skills) > 0
    
    if tests and len(tests) > 0:
        df = pd.DataFrame(tests)
        if not df.empty and 'subject' in df.columns:
            if 'score' in df.columns and 'total_questions' in df.columns:
                df['percentage'] = (df['score'] / df['total_questions']) * 100
                dfg = df.groupby('subject')['percentage'].max().reset_index()
                r_vals = dfg['percentage'].round(1).tolist()
            elif 'score' in df.columns:
                dfg = df.groupby('subject')['score'].max().reset_index()
                r_vals = dfg['score'].tolist()
            else:
                r_vals = None
            
            if r_vals:
                theta_vals = dfg['subject'].tolist()
                fig = go.Figure(go.Scatterpolar(r=r_vals, theta=theta_vals, fill='toself', line_color='#667eea', fillcolor='rgba(102, 126, 234, 0.3)'))
                fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], tickcolor='#64748b', gridcolor='#e2e8f0')), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=30, b=30, l=30, r=30), height=350)
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("**Recent Tests:**")
                for _, row in df.tail(5).iterrows():
                    pct = f" ({row['percentage']:.1f}%)" if 'percentage' in row and 'percentage' in df.columns else ""
                    st.caption(f"📝 {row['subject']}: {row.get('score', 'N/A')}{pct}")
            else:
                st.info("No test data.")
    else:
        if has_skills:
            for skill in verified_skills:
                st.markdown(f"<span class='skill-badge skill-badge-verified'>✓ {skill}</span>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">🎯</div>
                <div class="empty-text">Take a mock test to unlock your Skill Radar!</div>
            </div>
            """, unsafe_allow_html=True)

with tabs[1]:
    user_notes = db.get_user_notes(target_user)
    if not user_notes:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📝</div>
            <div class="empty-text">No notes shared yet.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"**{len(user_notes)} Contributions**")
        for note in user_notes:
            st.markdown(f"""
            <div class="note-card">
                <div>
                    <div class="note-title">{note['title']}</div>
                    <div class="note-meta">{note['subject']}</div>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span class="note-price">₹{note['price']}</span>
                    <a href="{note['link']}" target="_blank" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 10px 18px; border-radius: 10px; text-decoration: none; font-weight: 600;">Download</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

if is_me and len(tabs) > 2:
    with tabs[2]:
        reqs = db.get_pending_requests(current_user)
        if not reqs:
            st.markdown("""
            <div class="empty-state">
                <div class="empty-icon">📬</div>
                <div class="empty-text">No pending connection requests.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"**{len(reqs)} Pending Requests**")
            for r in reqs:
                sender = r['sender']
                s_data = db.get_user_details(sender)
                s_name = s_data.get('full_name', sender) if s_data else sender
                s_avatar = db.get_avatar_url(sender)
                
                st.markdown(f"""
                <div class="request-card">
                    <div class="request-user">
                        <img src="{s_avatar}" class="request-avatar">
                        <div>
                            <div class="request-name">@{sender}</div>
                            <div class="request-fullname">{s_name}</div>
                        </div>
                    </div>
                    <div style="display: flex; gap: 10px;">
                """, unsafe_allow_html=True)
                
                c1, c2 = st.columns([1, 1], vertical_alignment="center")
                with c1:
                    if st.button("✅ Accept", key=f"a_{sender}", use_container_width=True):
                        db.respond_to_request(sender, current_user, "accept")
                        st.rerun()
                with c2:
                    if st.button("❌ Reject", key=f"r_{sender}", use_container_width=True):
                        db.respond_to_request(sender, current_user, "reject")
                        st.rerun()

# Delete Account Section
if is_me:
    st.markdown("---")
    with st.expander("🗑️ Delete Account", expanded=False):
        st.markdown("""
        <div class="delete-card">
            <div class="delete-title">⚠️ Danger Zone</div>
            <div class="delete-warning">This action cannot be undone! All your data will be permanently deleted.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.checkbox("I understand this is irreversible", key="delete_check"):
            if st.button("Delete My Account", type="primary", key="delete_btn"):
                if db.delete_user_data(current_user):
                    st.success("Account deleted!")
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()

# Back button for non-own profile viewing
if not is_me:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to My Profile", use_container_width=True):
        st.session_state["viewing_user"] = current_user
        st.rerun()
