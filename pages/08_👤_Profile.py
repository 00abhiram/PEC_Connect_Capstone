import streamlit as st
import database as db
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Profile", page_icon="👤", layout="wide")
db.init_db()

# --- CSS FOR CLEAN LOOK & BADGES ---
st.markdown("""
<style>
    /* AVATAR STYLING */
    [data-testid="stImage"] img {
        border-radius: 50% !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* STATS BOX */
    .stat-box {
        text-align: center; padding: 10px; background: #f8fafc;
        border-radius: 8px; border: 1px solid #e2e8f0;
    }
    .stat-val { font-size: 1.2rem; font-weight: 800; color: #0f172a; }
    .stat-lbl { font-size: 0.8rem; color: #64748b; text-transform: uppercase; }
    
    /* BADGES */
    .verified-skill {
        background-color: #dcfce7; color: #15803d; padding: 2px 8px;
        border-radius: 12px; font-size: 0.75rem; font-weight: 700;
        display: inline-block; margin-right: 5px; border: 1px solid #bbf7d0;
    }
    
    /* NOTE CARD */
    .note-card {
        background: white; border: 1px solid #e2e8f0; padding: 15px;
        border-radius: 8px; margin-bottom: 10px; display: flex;
        justify-content: space-between; align-items: center;
        transition: transform 0.2s;
    }
    .note-card:hover { transform: translateX(5px); border-color: #3b82f6; }
    
    /* TEXT */
    .user-handle { font-size: 1.8rem; font-weight: 700; color: #1e293b; margin-bottom: 5px; }
    .bio-text { font-size: 0.95rem; color: #334155; margin-bottom: 15px; }
    .social-link { 
        text-decoration: none; color: #2563eb; font-weight: 600; 
        background: #eff6ff; padding: 5px 10px; border-radius: 5px; margin-right: 10px;
    }
</style>
""", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.warning("Please Login.")
    st.stop()

# --- LOGIC ---
current_user = st.session_state["user"]
target_user = st.session_state.get("viewing_user", current_user)

if st.sidebar.button("🏠 Back to My Profile"):
    st.session_state["viewing_user"] = current_user
    st.rerun()

is_me = (current_user == target_user)
user_data = db.get_user_details(target_user)
if not user_data: st.error("User not found."); st.stop()

# --- PREPARE DATA ---
# UPDATED: Use the new Smart Avatar Function from database.py
avatar_src = db.get_avatar_url(target_user)

fullname = user_data.get('full_name', target_user)
headline = user_data.get('headline', "Student")
about_text = user_data.get('about_text', "No bio yet.")
verified_skills = db.get_verified_skills(target_user)

# ==========================================
# 1. HEADER SECTION
# ==========================================
st.write("") 
c_img, c_info = st.columns([1.5, 4])

with c_img:
    st.image(avatar_src, width=180)

with c_info:
    # Row A: Handle + Buttons
    c_head, c_btn = st.columns([2, 2])
    with c_head:
        st.markdown(f'<div class="user-handle">@{target_user} <span style="color:#3b82f6; font-size:1rem;">✅</span></div>', unsafe_allow_html=True)
    with c_btn:
        if is_me:
            with st.expander("⚙️ Edit Profile"):
                with st.form("edit_profile"):
                    n_name = st.text_input("Name", value=fullname)
                    n_head = st.text_input("Headline", value=headline)
                    n_bio = st.text_area("Bio", value=about_text)
                    n_li = st.text_input("LinkedIn", value=user_data.get("linkedin_url", ""))
                    n_gh = st.text_input("GitHub", value=user_data.get("github_url", ""))
                    n_pic = st.file_uploader("Profile Pic", type=['png','jpg'])
                    
                    if st.form_submit_button("Save"):
                        updates = {
                            "full_name": n_name, 
                            "headline": n_head, 
                            "about_text": n_bio, 
                            "linkedin_url": n_li, 
                            "github_url": n_gh
                        }
                        
                        # UPDATED: Upload to Storage Bucket instead of saving Base64 string
                        if n_pic:
                            file_bytes = n_pic.getvalue()
                            file_type = n_pic.type
                            db.update_avatar(current_user, file_bytes, file_type)
                            
                        db.supabase.table("users").update(updates).eq("username", current_user).execute()
                        st.success("Profile Updated!")
                        st.rerun()
        else:
            status = db.get_connection_status(current_user, target_user)
            if status == 'accepted':
                if st.button("💬 Message", type="primary"):
                    st.session_state["chat_with"] = target_user
                    st.switch_page("pages/10_💬_Messages.py")
            elif status == 'pending':
                st.button("🕒 Request Sent", disabled=True)
            else:
                if st.button("➕ Connect", type="primary"):
                    db.send_connection_request(current_user, target_user)
                    st.rerun()

    # Row B: Stats
    st.markdown("<br>", unsafe_allow_html=True)
    c_s1, c_s2, c_s3 = st.columns(3)
    c_s1.markdown(f'<div class="stat-box"><div class="stat-val">{user_data.get("points", 0)}</div><div class="stat-lbl">Points</div></div>', unsafe_allow_html=True)
    c_s2.markdown(f'<div class="stat-box"><div class="stat-val">{user_data.get("streak", 0)} 🔥</div><div class="stat-lbl">Streak</div></div>', unsafe_allow_html=True)
    c_s3.markdown(f'<div class="stat-box"><div class="stat-val">{user_data.get("year", "1st")}</div><div class="stat-lbl">Year</div></div>', unsafe_allow_html=True)

    # Row C: Verified Skills
    if verified_skills:
        st.markdown("<div style='margin-top:10px;'>", unsafe_allow_html=True)
        for skill in verified_skills:
            st.markdown(f"<span class='verified-skill'>🏆 {skill} Expert</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Row D: Bio
    st.markdown(f'<div style="font-weight:600; margin-top:10px;">{fullname}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bio-text">{about_text}</div>', unsafe_allow_html=True)
    
    li = user_data.get('linkedin_url', '#')
    gh = user_data.get('github_url', '#')
    st.markdown(f'<a href="{li}" target="_blank" class="social-link">LinkedIn</a> <a href="{gh}" target="_blank" class="social-link">GitHub</a>', unsafe_allow_html=True)

st.divider()

# ==========================================
# 2. CONTENT TABS
# ==========================================
t_labels = ["📊 Skill Radar", "📚 Shared Notes"]
if is_me: t_labels.append("🔔 Requests")

tabs = st.tabs(t_labels)

# TAB 1: RADAR CHART
with tabs[0]:
    tests = db.get_user_test_history(target_user)
    if tests:
        df = pd.DataFrame(tests)
        if not df.empty and 'subject' in df.columns:
            dfg = df.groupby('subject')['score'].max().reset_index()
            fig = go.Figure(go.Scatterpolar(r=dfg['score'], theta=dfg['subject'], fill='toself', line_color='#2563eb'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), margin=dict(t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No test data found.")
    else:
        st.info("Take a mock test to unlock your Skill Radar!")

# TAB 2: MY NOTES
with tabs[1]:
    user_notes = db.get_user_notes(target_user)
    
    if not user_notes:
        st.caption(f"{target_user} hasn't shared any notes yet.")
    else:
        st.markdown(f"**{len(user_notes)} Contributions**")
        for note in user_notes:
            with st.container():
                st.markdown(f"""
                <div class="note-card">
                    <div>
                        <div style="font-weight:700; font-size:1rem;">{note['title']}</div>
                        <div style="font-size:0.8rem; color:#64748b;">{note['subject']} • ₹{note['price']}</div>
                    </div>
                    <a href="{note['link']}" target="_blank" style="text-decoration:none; background:#eff6ff; color:#2563eb; padding:5px 12px; border-radius:5px; font-size:0.8rem; font-weight:600;">Download</a>
                </div>
                """, unsafe_allow_html=True)

# TAB 3: REQUESTS (Me Only)
if is_me and len(tabs) > 2:
    with tabs[2]:
        reqs = db.get_pending_requests(current_user)
        if not reqs:
            st.caption("No pending requests.")
        else:
            for r in reqs:
                sender = r['sender']
                s_data = db.get_user_details(sender)
                s_name = s_data.get('full_name', sender) if s_data else sender
                
                with st.container():
                    c1, c2, c3 = st.columns([4, 1, 1])
                    c1.markdown(f"**@{sender}** ({s_name})")
                    if c2.button("✅", key=f"a_{sender}"):
                        db.respond_to_request(sender, current_user, "accept")
                        st.rerun()
                    if c3.button("❌", key=f"r_{sender}"):
                        db.respond_to_request(sender, current_user, "reject")
                        st.rerun()