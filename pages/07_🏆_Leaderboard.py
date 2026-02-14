import streamlit as st
import database as db
import pandas as pd

# Initialize DB
db.init_db()

# --- PAGE CONFIG ---
st.set_page_config(page_title="Leaderboard | PEC", page_icon="🏆", layout="wide")

# --- CUSTOM CSS FOR "PRO" LOOK ---
st.markdown("""
<style>
    .big-font { font-size:20px !important; font-weight: bold; }
    .med-font { font-size:16px !important; color: #555; }
    .rank-card {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .rank-card:hover { transform: scale(1.02); }
    .gold { background: linear-gradient(135deg, #ffd700 0%, #fdb931 100%); color: black;}
    .silver { background: linear-gradient(135deg, #e0e0e0 0%, #bdbdbd 100%); color: black;}
    .bronze { background: linear-gradient(135deg, #cd7f32 0%, #a05a2c 100%); color: white;}
</style>
""", unsafe_allow_html=True)

st.title("🏆 PEC Hall of Fame")
st.caption("Recognizing the most active and brilliant minds of Pallavi Engineering College.")

# --- FETCH DATA ---
top_students = db.get_leaderboard()

if not top_students:
    st.info("No data yet. Be the first to take a test!")
else:
    # --- 1. THE WINNER'S PODIUM (Top 3) ---
    st.markdown("### 🌟 Top Performers")
    
    # We need at least 3 users to show a full podium, but code handles fewer
    col1, col2, col3 = st.columns([1, 1.2, 1]) # Middle column slightly wider for #1

    # REORDER: Rank 2 (Left), Rank 1 (Center), Rank 3 (Right)
    # This is a classic podium layout
    
    # --- RANK 2 (Silver) ---
    with col1:
        if len(top_students) > 1:
            u2 = top_students[1]
            st.markdown(f"""
            <div class="rank-card silver">
                <h1>🥈</h1>
                <img src="https://api.dicebear.com/7.x/identicon/svg?seed={u2[0]}" width="80" style="border-radius:50%">
                <h3>@{u2[0]}</h3>
                <p>{u2[1]} Points</p>
                <small>{u2[2]}</small>
            </div>
            """, unsafe_allow_html=True)

    # --- RANK 1 (Gold) ---
    with col2:
        if len(top_students) > 0:
            u1 = top_students[0]
            st.markdown(f"""
            <div class="rank-card gold">
                <h1>👑</h1>
                <img src="https://api.dicebear.com/7.x/identicon/svg?seed={u1[0]}" width="100" style="border-radius:50%; border: 3px solid white;">
                <h2 style="margin:0">@{u1[0]}</h2>
                <p class="big-font">{u1[1]} Points</p>
                <span style="background:black; color:gold; padding:4px 10px; border-radius:10px; font-size:12px;">PEC CHAMPION</span>
            </div>
            """, unsafe_allow_html=True)

    # --- RANK 3 (Bronze) ---
    with col3:
        if len(top_students) > 2:
            u3 = top_students[2]
            st.markdown(f"""
            <div class="rank-card bronze">
                <h1>🥉</h1>
                <img src="https://api.dicebear.com/7.x/identicon/svg?seed={u3[0]}" width="80" style="border-radius:50%">
                <h3>@{u3[0]}</h3>
                <p>{u3[1]} Points</p>
                <small>{u3[2]}</small>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # --- 2. THE REST OF THE LIST (Ranks 4-10) ---
    st.markdown("### 🚀 Rising Stars")
    
    if len(top_students) > 3:
        for i in range(3, len(top_students)):
            u = top_students[i] # (username, points, role, year)
            rank = i + 1
            
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns([0.5, 1, 3, 1])
                with c1:
                    st.markdown(f"**#{rank}**")
                with c2:
                    # Tiny avatar
                    st.image(f"https://api.dicebear.com/7.x/identicon/svg?seed={u[0]}", width=40)
                with c3:
                    st.markdown(f"**{u[0]}**")
                    st.caption(f"{u[2]} • {u[3]}")
                with c4:
                    st.markdown(f"**{u[1]} pts**")
    else:
        st.info("Join the race! We need more students to fill the Top 10.")

# --- 3. YOUR PERSONAL STATS (Floating or Bottom) ---
if "user" in st.session_state:
    st.divider()
    
    # Find my data
    my_data = None
    for i, s in enumerate(top_students):
        if s[0] == st.session_state["user"]:
            my_data = {"rank": i+1, "points": s[1]}
            break
            
    # If not in top 10, fetch from DB separately
    if not my_data:
        conn = db.sqlite3.connect('pec_data.db')
        c = conn.cursor()
        c.execute("SELECT points FROM users WHERE username=?", (st.session_state['user'],))
        res = c.fetchone()
        conn.close()
        my_pts = res[0] if res else 0
        my_data = {"rank": "10+", "points": my_pts}

    st.success(f"👤 **Your Stats:** Rank **#{my_data['rank']}** with **{my_data['points']} Points**. Keep pushing!")