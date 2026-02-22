import streamlit as st
import database as db
import pandas as pd
import plotly.graph_objects as go

db.init_db()

# Check for admin
is_admin = st.session_state.get("is_admin", False)
admin_user = st.session_state.get("admin_user", "")

# Sidebar toggle CSS
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
    
    .admin-banner {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white; padding: 10px 20px; border-radius: 10px;
        margin-bottom: 15px;
    }
    .admin-banner h3 { margin: 0; }
    
    .profile-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px; padding: 40px 30px 60px 30px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.25);
        margin-bottom: 60px;
    }
    
    .profile-content {
        margin-top: -40px;
    }
    
    .avatar-container {
        width: 150px; height: 150px;
        border-radius: 50%;
        border: 5px solid white;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        overflow: hidden;
        background: white;
        cursor: pointer;
    }
    
    .avatar-container img {
        width: 100%; height: 100%; object-fit: cover;
    }
    
    .stImage img {
        border-radius: 50% !important;
        border: 4px solid white !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
    }
    
    .username-text {
        font-size: 1.8rem; font-weight: 700; color: white;
    }
    .name-text {
        font-size: 1rem; color: rgba(255,255,255,0.9);
    }
    .headline-text {
        font-size: 0.95rem; color: rgba(255,255,255,0.8);
        margin-top: 8px;
    }
    
    .stat-box {
        background: white; border-radius: 16px; padding: 20px;
        text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    .stat-num { font-size: 1.5rem; font-weight: 700; color: #667eea; }
    .stat-lbl { font-size: 0.75rem; color: #64748b; text-transform: uppercase; }
    
    .skill-badge {
        background: linear-gradient(135deg, #667eea20, #764ba220);
        color: #667eea; padding: 6px 14px; border-radius: 20px;
        font-size: 0.8rem; font-weight: 600; display: inline-block; margin: 3px;
        border: 1px solid #667eea30;
    }
    
    .note-card {
        background: white; border: 1px solid #e2e8f0;
        padding: 16px; border-radius: 12px; margin-bottom: 10px;
        display: flex; justify-content: space-between; align-items: center;
        transition: all 0.2s;
    }
    .note-card:hover {
        border-color: #667eea; box-shadow: 0 4px 15px rgba(102,126,234,0.1);
    }
    .note-title { font-weight: 600; color: #1e293b; }
    .note-meta { font-size: 0.8rem; color: #94a3b8; }
    .note-download {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white; padding: 8px 16px; border-radius: 8px;
        text-decoration: none; font-size: 0.8rem; font-weight: 600;
    }
    
    .profile-tabs .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .profile-tabs .stTabs [data-baseweb="tab"] {
        height: 45px; padding: 0 20px; border-radius: 10px;
        background: #f1f5f9; color: #64748b; font-weight: 600;
    }
    .profile-tabs .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
    }
    
    .section-header {
        font-size: 1.1rem; font-weight: 700; color: #1e293b;
        margin-bottom: 15px;
    }
    
    .social-btn {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 8px 16px; border-radius: 8px;
        text-decoration: none; font-size: 0.85rem; font-weight: 600;
    }
    .linkedin-btn { background: #0077b5; color: white; }
    .github-btn { background: #333; color: white; }
    
    .request-item {
        background: white; border: 1px solid #e2e8f0;
        border-radius: 12px; padding: 12px 16px; margin-bottom: 10px;
        display: flex; align-items: center; justify-content: space-between;
    }
    .request-user {
        display: flex; align-items: center; gap: 10px;
    }
    .request-avatar {
        width: 40px; height: 40px; border-radius: 50%;
    }
    .request-name { font-weight: 600; }
    .request-fullname { font-size: 0.8rem; color: #64748b; }
</style>
""", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.warning("Please Login.")
    st.stop()

current_user = st.session_state["user"]
target_user = st.session_state.get("viewing_user", current_user)

if st.sidebar.button("🏠 Back to My Profile"):
    st.session_state["viewing_user"] = current_user
    st.rerun()

# Admin controls in sidebar
if is_admin:
    st.sidebar.markdown("---")
    st.sidebar.markdown("🛡️ **Admin Controls**")
    
    # View any user
    admin_view_user = st.sidebar.text_input("View User Profile", placeholder="Enter username")
    if admin_view_user:
        st.session_state["viewing_user"] = admin_view_user
        st.rerun()
    
    # Delete user account
    if st.sidebar.button("🗑️ Delete This Account"):
        if target_user != admin_user:
            db.delete_user(target_user)
            st.sidebar.success(f"Account {target_user} deleted!")
            st.session_state["viewing_user"] = current_user
            st.rerun()
        else:
            st.sidebar.error("Cannot delete admin account!")
    
    # Warn user
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

if "show_full_avatar" not in st.session_state:
    st.session_state.show_full_avatar = False

if st.session_state.show_full_avatar:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="background:white;border-radius:20px;padding:30px;box-shadow:0 10px 40px rgba(0,0,0,0.2);text-align:center;">
            <img src="{avatar_src}" style="width:250px;height:250px;border-radius:50%;object-fit:cover;border:4px solid #667eea;">
            <div style="margin-top:15px;font-weight:700;font-size:1.2rem;color:#1e293b;">@{target_user}</div>
            <div style="margin-top:5px;color:#64748b;">{fullname}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✕ Close", key="close_avatar_modal"):
            st.session_state.show_full_avatar = False
            st.rerun()

st.markdown(f"""
<div class="profile-banner">
    <div style="display: flex; align-items: flex-end; gap: 25px;">
        <div class="avatar-container">
            <img src="{avatar_src}" alt="Profile">
        </div>
        <div style="padding-bottom: 10px;">
            <div class="username-text">@{target_user}</div>
            <div class="name-text">{fullname}</div>
            <div class="headline-text">{headline}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.show_full_avatar:
    if st.button("👁️ View Profile Picture"):
        st.session_state.show_full_avatar = True
        st.rerun()

col_main, col_side = st.columns([2, 1])

with col_main:
    st.markdown("###")
    
    if is_me:
        with st.expander("⚙️ Edit Profile"):
            with st.form("edit_profile"):
                c1, c2 = st.columns(2)
                with c1:
                    n_name = st.text_input("Full Name", value=fullname)
                    n_year = st.selectbox("Year", ["1", "2", "3", "4"], index=year_val-1, help="Select your year")
                with c2:
                    n_head = st.text_input("Headline", value=headline, placeholder="e.g., CSE Student | AI Enthusiast")
                
                n_bio = st.text_area("About", value=about_text, placeholder="Tell others about yourself...")
                
                c3, c4 = st.columns(2)
                with c3:
                    n_li = st.text_input("LinkedIn URL", value=user_data.get("linkedin_url", ""))
                with c4:
                    n_gh = st.text_input("GitHub URL", value=user_data.get("github_url", ""))
                
                n_pic = st.file_uploader("Change Profile Picture", type=['png','jpg','jpeg'])
                
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True):
                        updates = {"full_name": n_name, "headline": n_head, "year": n_year, "about_text": n_bio, "linkedin_url": n_li, "github_url": n_gh}
                        if n_pic:
                            db.update_avatar(current_user, n_pic.getvalue(), n_pic.type)
                        db.supabase.table("users").update(updates).eq("username", current_user).execute()
                        st.success("Profile updated!")
                        st.rerun()
                with col_cancel:
                    if st.form_submit_button("Cancel", use_container_width=True):
                        st.rerun()
            
            with st.expander("🗑️ Delete Account", expanded=False):
                st.error("This action cannot be undone!")
                if st.checkbox("I understand this is irreversible"):
                    if st.button("Delete My Account", type="primary"):
                        if db.delete_user_data(current_user):
                            st.success("Account deleted!")
                            for key in list(st.session_state.keys()):
                                del st.session_state[key]
                            st.rerun()
    else:
        status = db.get_connection_status(current_user, target_user)
        if status == 'accepted':
            if st.button("💬 Message", type="primary", use_container_width=True):
                st.session_state["chat_with"] = target_user
                st.switch_page("pages/10_💬_Messages.py")
        elif status == 'pending':
            st.button("🕒 Request Sent", disabled=True, use_container_width=True)
        else:
            if st.button("➕ Connect", type="primary", use_container_width=True):
                db.send_connection_request(current_user, target_user)
                st.rerun()
    
    st.markdown("---")
    
    if verified_skills:
        st.markdown('<div class="section-header">🏆 Verified Skills</div>', unsafe_allow_html=True)
        for skill in verified_skills:
            st.markdown(f"<span class='skill-badge'>🏆 {skill}</span>", unsafe_allow_html=True)
        st.markdown("")

    if about_text:
        st.markdown('<div class="section-header">About</div>', unsafe_allow_html=True)
        st.markdown(f"<div style='color: #475569; line-height: 1.6;'>{about_text}</div>", unsafe_allow_html=True)

    li = user_data.get('linkedin_url', '')
    gh = user_data.get('github_url', '')
    if li or gh:
        st.markdown('<div class="section-header">Links</div>', unsafe_allow_html=True)
        if li:
            st.markdown(f'<a href="{li}" target="_blank" class="social-btn linkedin-btn">LinkedIn ↗</a>', unsafe_allow_html=True)
        if gh:
            st.markdown(f'<a href="{gh}" target="_blank" class="social-btn github-btn">GitHub ↗</a>', unsafe_allow_html=True)

with col_side:
    st.markdown("")
    st.markdown("""
    <div class="stat-box">
        <div class="stat-num">{}</div>
        <div class="stat-lbl">Points</div>
    </div>
    """.format(user_data.get('points', 0)), unsafe_allow_html=True)
    st.markdown("")
    st.markdown("""
    <div class="stat-box">
        <div class="stat-num">{} 🔥</div>
        <div class="stat-lbl">Streak</div>
    </div>
    """.format(user_data.get('streak', 0)), unsafe_allow_html=True)
    st.markdown("")
    st.markdown("""
    <div class="stat-box">
        <div class="stat-num">{}</div>
        <div class="stat-lbl">Year</div>
    </div>
    """.format(year_display), unsafe_allow_html=True)

st.markdown("---")

t_labels = ["📊 Skills", "📚 Notes"]
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
                    pct = f" ({row['percentage']:.1f}%)" if 'percentage' in df.columns else ""
                    st.caption(f"{row['subject']}: {row.get('score', 'N/A')}{pct}")
            else:
                st.info("No test data.")
        else:
            if has_skills:
                for skill in verified_skills:
                    st.markdown(f"<span class='skill-badge'>🏆 {skill}</span>", unsafe_allow_html=True)
            else:
                st.info("Take a mock test to unlock Skill Radar!")
    else:
        if has_skills:
            for skill in verified_skills:
                st.markdown(f"<span class='skill-badge'>🏆 {skill}</span>", unsafe_allow_html=True)
        else:
            st.info("🎯 Take a mock test to unlock your Skill Radar!")

with tabs[1]:
    user_notes = db.get_user_notes(target_user)
    if not user_notes:
        st.caption(f"📝 {target_user} hasn't shared any notes yet.")
    else:
        st.markdown(f"**{len(user_notes)} Contributions**")
        for note in user_notes:
            st.markdown(f"""
            <div class="note-card">
                <div>
                    <div class="note-title">{note['title']}</div>
                    <div class="note-meta">{note['subject']} • ₹{note['price']}</div>
                </div>
                <a href="{note['link']}" target="_blank" class="note-download">Download</a>
            </div>
            """, unsafe_allow_html=True)

if is_me and len(tabs) > 2:
    with tabs[2]:
        reqs = db.get_pending_requests(current_user)
        if not reqs:
            st.caption("📬 No pending connection requests.")
        else:
            st.markdown(f"**{len(reqs)} Pending Requests**")
            for r in reqs:
                sender = r['sender']
                s_data = db.get_user_details(sender)
                s_name = s_data.get('full_name', sender) if s_data else sender
                s_avatar = db.get_avatar_url(sender)
                
                c_req1, c_req2, c_req3 = st.columns([5, 1, 1])
                with c_req1:
                    st.markdown(f"""
                    <div class="request-item" style="margin:0;padding:0;border:none;">
                        <div class="request-user">
                            <img src="{s_avatar}" class="request-avatar">
                            <div>
                                <div class="request-name">@{sender}</div>
                                <div class="request-fullname">{s_name}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                with c_req2:
                    if st.button("✅", key=f"a_{sender}", help="Accept"):
                        db.respond_to_request(sender, current_user, "accept")
                        st.rerun()
                with c_req3:
                    if st.button("❌", key=f"r_{sender}", help="Reject"):
                        db.respond_to_request(sender, current_user, "reject")
                        st.rerun()
