import streamlit as st
import database as db
import pandas as pd
import base64
import plotly.graph_objects as go

st.set_page_config(page_title="My Profile", page_icon="👤", layout="wide")
db.init_db()

# --- CSS FOR IDENTITY CARD ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .profile-card {
        background: white; border-radius: 24px; padding: 40px 20px;
        text-align: center; box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        border: 1px solid #f1f5f9; max-width: 400px; margin: 0 auto;
    }
    .avatar-wrapper {
        width: 130px; height: 130px; margin: 0 auto 20px auto;
        position: relative; border-radius: 50%;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6); padding: 4px;
    }
    .avatar-img {
        width: 100%; height: 100%; border-radius: 50%;
        object-fit: cover; border: 4px solid white; background-color: white;
    }
    .user-handle { font-size: 1.5rem; font-weight: 800; color: #0f172a; margin-bottom: 5px; }
    .user-role { 
        font-size: 0.9rem; color: #64748b; font-weight: 500; 
        background: #f1f5f9; padding: 5px 12px; border-radius: 20px;
        display: inline-block; margin-bottom: 25px;
    }
    .stats-row {
        display: flex; justify-content: center; gap: 30px;
        border-top: 1px solid #f1f5f9; padding-top: 25px; margin-top: 10px;
    }
    .stat-value { font-size: 1.2rem; font-weight: 700; color: #0f172a; display: block; }
    .stat-label { font-size: 0.75rem; color: #94a3b8; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; }
</style>
""", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.warning("Please Login.")
    st.stop()

username = st.session_state["user"]

# Fetch Data
conn = db.sqlite3.connect('pec_data.db')
c = conn.cursor()
c.execute("SELECT * FROM users WHERE username=?", (username,))
user_data = c.fetchone()
conn.close()

# Avatar
avatar_data = user_data[5] 
avatar_src = f"data:image/png;base64,{avatar_data}" if avatar_data else f"https://api.dicebear.com/7.x/identicon/svg?seed={username}"

# --- MAIN LAYOUT ---
st.title("👤 My Profile")

c1, c2 = st.columns([1, 2])

with c1:
    # 1. PROFILE CARD
    st.markdown(f"""
    <div class="profile-card">
        <div class="avatar-wrapper"><img src="{avatar_src}" class="avatar-img"></div>
        <div class="user-handle">@{username}</div>
        <div class="user-role">{user_data[2]} • {user_data[3]}</div>
        <div class="stats-row">
            <div><span class="stat-value">{user_data[4]}</span><span class="stat-label">Points</span></div>
            <div><span class="stat-value">#12</span><span class="stat-label">Rank</span></div>
            <div><span class="stat-value">Active</span><span class="stat-label">Status</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. TOAST UPLOAD
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📸 Update Photo"):
        uploaded_file = st.file_uploader("Upload image", type=['png', 'jpg'])
        if uploaded_file and st.button("Save New Photo"):
            bytes_data = uploaded_file.getvalue()
            b64_str = base64.b64encode(bytes_data).decode()
            db.update_avatar(username, b64_str)
            st.toast("Profile photo updated successfully!", icon="✅") # <--- TOAST HERE
            st.rerun()

with c2:
    t1, t2 = st.tabs(["📊 Skill Radar", "⚙️ Settings"])
    
    with t1:
        # --- 3. THE PROFESSIONAL RADAR CHART ---
        conn = db.sqlite3.connect('pec_data.db')
        # Get Max Score per subject
        df = pd.read_sql_query("SELECT subject, MAX(score) as max_score FROM test_results WHERE username=? GROUP BY subject", conn, params=(username,))
        conn.close()

        if not df.empty:
            # Normalize scores (assuming max is 10)
            categories = df['subject'].tolist()
            values = df['max_score'].tolist()
            
            # Close the loop for radar chart
            categories = categories
            values = values
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=username,
                line_color='#4f46e5'
            ))

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                showlegend=False,
                margin=dict(t=20, b=20, l=20, r=20),
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            # Placeholder Radar for new users
            st.info("Take a mock test to generate your Skill Radar!")
            categories = ['Python', 'Math', 'Java', 'Logic', 'BEE']
            values = [0, 0, 0, 0, 0]
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(r=[2,2,2,2,2], theta=categories, fill='toself', line_color='#e2e8f0'))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)

    with t2:
        st.write("Account Details")
        st.text_input("Email", value=f"{username}@pec.edu.in")
        if st.button("Update Info"):
            st.toast("Settings saved!", icon="💾") # <--- TOAST HERE