import streamlit as st
import database as db

st.set_page_config(page_title="Network", page_icon="🌐", layout="wide")
db.init_db()

# --- PROFESSIONAL CARD CSS ---
st.markdown("""
<style>
    .net-card {
        background: white; border: 1px solid #e0e0e0; border-radius: 12px;
        padding: 20px; text-align: center; transition: 0.2s; height: 100%;
    }
    .net-card:hover { box-shadow: 0 10px 20px rgba(0,0,0,0.08); transform: translateY(-3px); }
    
    .net-avatar {
        width: 90px; height: 90px; border-radius: 50%; object-fit: cover;
        margin-bottom: 10px; border: 3px solid #f0f2f5;
    }
    .net-name { font-weight: 700; font-size: 1.1rem; color: #1c1e21; }
    .net-role { font-size: 0.85rem; color: #65676b; margin-bottom: 15px; }
    
    .btn-connect { width: 100%; background: #e7f3ff; color: #1877f2; border: none; padding: 8px; border-radius: 6px; font-weight: 600; }
    .btn-pending { width: 100%; background: #f0f2f5; color: #65676b; padding: 8px; border-radius: 6px; }
</style>
""", unsafe_allow_html=True)

st.title("🌐 Campus Network")

# --- FILTERS ---
c_search, c_filt = st.columns([3, 1])
search = c_search.text_input("🔍 Search Students", placeholder="Search by name, skill, or roll no...")
role_filter = c_filt.selectbox("Filter", ["All", "Student", "Mentor"])

# --- DATA ---
users = db.search_users(search) if search else db.get_leaderboard()
if role_filter != "All": users = [u for u in users if u.get('role') == role_filter]
if "user" in st.session_state: users = [u for u in users if u.get('username') != st.session_state["user"]]

if not users:
    st.info("No users found.")
else:
    cols = st.columns(4) # 4 Cards per row for cleaner look
    
    for i, user in enumerate(users):
        with cols[i % 4]:
            uname = user.get('username')
            fname = user.get('full_name', uname)
            role = user.get('role', 'Student')
            
            # UPDATED: Use the new Smart Avatar Function from database.py
            av = db.get_avatar_url(uname)
            
            # 1. Visual Card
            st.markdown(f"""
            <div class="net-card">
                <img src="{av}" class="net-avatar">
                <div class="net-name">{fname}</div>
                <div class="net-role">@{uname} • {role}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # 2. Logic Buttons
            if "user" in st.session_state:
                status = db.get_connection_status(st.session_state["user"], uname)
                
                # We use columns inside the grid column to place buttons
                b1, b2 = st.columns(2)
                with b1:
                    if status == 'accepted':
                        if st.button("💬 Chat", key=f"msg_{uname}", type="primary", use_container_width=True):
                            st.session_state["chat_with"] = uname
                            st.switch_page("pages/10_💬_Messages.py")
                    elif status == 'pending':
                        st.button("🕒 Sent", key=f"wait_{uname}", disabled=True, use_container_width=True)
                    else:
                        if st.button("➕ Connect", key=f"add_{uname}", use_container_width=True):
                            db.send_connection_request(st.session_state["user"], uname)
                            st.toast(f"Request sent to {uname}")
                            st.rerun()
                with b2:
                    if st.button("👤 View", key=f"view_{uname}", use_container_width=True):
                        st.session_state["viewing_user"] = uname
                        st.switch_page("pages/08_👤_Profile.py")