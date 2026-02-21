import streamlit as st
import database as db

st.set_page_config(page_title="Leaderboard", page_icon="🏆", layout="wide")
db.init_db()

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    
    .podium-container {
        display: flex; justify-content: center; align-items: flex-end; gap: 15px;
        margin-bottom: 50px; padding-top: 20px;
    }
    .podium-place {
        text-align: center; color: white; border-radius: 15px 15px 0 0;
        padding: 20px; width: 140px; position: relative;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    .podium-place:hover { transform: translateY(-10px); }
    
    .p-1 { height: 280px; background: linear-gradient(135deg, #FFD700, #FDB931); border: 2px solid #fff; z-index: 2; }
    .p-2 { height: 200px; background: linear-gradient(135deg, #E0E0E0, #BDBDBD); opacity: 0.9; }
    .p-3 { height: 160px; background: linear-gradient(135deg, #CD7F32, #A05A2C); opacity: 0.9; }
    
    .avatar-circle {
        width: 80px; height: 80px; border-radius: 50%; border: 4px solid white;
        object-fit: cover; margin-bottom: 10px; background: white;
    }
    .crown { font-size: 40px; position: absolute; top: -30px; left: 50%; transform: translateX(-50%); }
    
    .league-badge {
        padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold;
        text-transform: uppercase; letter-spacing: 1px; color: white;
    }
    .diamond { background: #b9f2ff; color: #0077b6; border: 1px solid #0077b6; }
    .gold { background: #fff9c4; color: #fbc02d; border: 1px solid #fbc02d; }
    .silver { background: #f5f5f5; color: #616161; border: 1px solid #9e9e9e; }
    
    .list-card {
        background: white; padding: 15px; border-radius: 12px;
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 10px; border: 1px solid #f0f2f5;
        transition: all 0.2s;
    }
    .list-card:hover { border-color: #3b82f6; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🏆 Champions League</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Compete with the best minds at PEC</p>", unsafe_allow_html=True)

top_students = db.get_leaderboard()

def get_league(points):
    if points > 1000: return "💎 DIAMOND"
    elif points > 500: return "🥇 GOLD"
    elif points > 200: return "🥈 SILVER"
    return "🥉 BRONZE"

if not top_students:
    st.info("No champions yet. Be the first!")
else:
    u1 = top_students[0] if len(top_students) > 0 else None
    u2 = top_students[1] if len(top_students) > 1 else None
    u3 = top_students[2] if len(top_students) > 2 else None

    html_code = '<div class="podium-container">'
    
    if u2:
        av2 = db.get_avatar_url(u2['username']) 
        html_code += f"""
        <div class="podium-place p-2">
            <img src="{av2}" class="avatar-circle">
            <h3>#2</h3>
            <b>@{u2['username']}</b>
            <p>{u2['points']} pts</p>
        </div>"""
    
    if u1:
        av1 = db.get_avatar_url(u1['username']) 
        html_code += f"""
        <div class="podium-place p-1">
            <div class="crown">👑</div>
            <img src="{av1}" class="avatar-circle">
            <h3>#1</h3>
            <b>@{u1['username']}</b>
            <p>{u1['points']} pts</p>
        </div>"""
        
    if u3:
        av3 = db.get_avatar_url(u3['username'])
        html_code += f"""
        <div class="podium-place p-3">
            <img src="{av3}" class="avatar-circle">
            <h3>#3</h3>
            <b>@{u3['username']}</b>
            <p>{u3['points']} pts</p>
        </div>"""
        
    html_code += '</div>'
    st.markdown(html_code, unsafe_allow_html=True)

    st.write("---")
    
    search = st.text_input("🔍 Find a student...", placeholder="Enter username")
    filtered_list = [s for s in top_students if search.lower() in s['username'].lower()] if search else top_students

    c1, c2, c3, c4 = st.columns([0.5, 3, 2, 1])
    c1.markdown("**Rank**")
    c2.markdown("**Student**")
    c3.markdown("**League**")
    c4.markdown("**Points**")

    for i, user in enumerate(filtered_list):
        rank = i + 1
        is_me = "user" in st.session_state and st.session_state["user"] == user['username']
        bg_color = "#eff6ff" if is_me else "white"
        
        league_name = get_league(user['points'])
        l_style = "diamond" if "DIAMOND" in league_name else "gold" if "GOLD" in league_name else "silver"
        
        list_av = db.get_avatar_url(user['username'])

        with st.container():
            st.markdown(f"""
            <div class="list-card" style="background-color: {bg_color};">
                <div style="width: 10%; font-weight: bold; font-size: 1.2rem;">#{rank}</div>
                <div style="width: 40%; display: flex; align-items: center; gap: 10px;">
                    <img src="{list_av}" style="width: 35px; height: 35px; border-radius: 50%; object-fit: cover;">
                    <div>
                        <div style="font-weight: 600;">{user['username']}</div>
                        <div style="font-size: 0.8rem; color: #64748b;">{user.get('full_name', 'Student')}</div>
                    </div>
                </div>
                <div style="width: 30%;">
                    <span class="league-badge {l_style}">{league_name}</span>
                </div>
                <div style="width: 20%; font-weight: 800; text-align: right; color: #3b82f6;">{user['points']}</div>
            </div>
            """, unsafe_allow_html=True)