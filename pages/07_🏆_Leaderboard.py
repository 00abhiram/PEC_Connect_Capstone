import streamlit as st
import database as db

db.init_db()

def get_cached_leaderboard():
    return db.get_full_leaderboard()

# Sidebar toggle CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body { font-family: 'Inter', sans-serif; }
    
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
    
    .page-header {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        padding: 30px; border-radius: 20px; margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(245, 158, 11, 0.3);
    }
    .page-title { color: white; font-size: 2rem; font-weight: 800; margin: 0; }
    .page-subtitle { color: rgba(255,255,255,0.9); font-size: 1rem; margin-top: 5px; }
    
    .podium-wrapper {
        background: linear-gradient(180deg, #1e1e2e 0%, #11111b 100%);
        border-radius: 24px; padding: 40px 20px; margin-bottom: 40px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .podium-container {
        display: flex; justify-content: center; align-items: flex-end; gap: 20px;
    }
    .podium-place {
        text-align: center; border-radius: 20px 20px 0 0;
        padding: 25px 20px; width: 160px; position: relative;
        transition: all 0.3s ease;
    }
    .podium-place:hover { transform: translateY(-10px); }
    
    .p-1 { 
        height: 300px; 
        background: linear-gradient(180deg, #FFD700 0%, #FDB931 100%); 
        z-index: 3;
        box-shadow: 0 0 40px rgba(255, 215, 0, 0.4);
    }
    .p-2 { 
        height: 240px; 
        background: linear-gradient(180deg, #E0E0E0 0%, #BDBDBD 100%);
        box-shadow: 0 0 30px rgba(192, 192, 192, 0.3);
    }
    .p-3 { 
        height: 190px; 
        background: linear-gradient(180deg, #CD7F32 0%, #A05A2C 100%);
        box-shadow: 0 0 25px rgba(205, 127, 50, 0.3);
    }
    
    .avatar-circle {
        width: 90px; height: 90px; border-radius: 50%; 
        border: 5px solid white;
        object-fit: cover; margin-bottom: 15px; 
        background: white; box-shadow: 0 5px 20px rgba(0,0,0,0.2);
    }
    .crown { font-size: 50px; position: absolute; top: -35px; left: 50%; transform: translateX(-50%); }
    
    .rank-number { font-size: 1.5rem; font-weight: 800; color: white; }
    .rank-name { font-size: 1rem; font-weight: 700; color: white; margin: 5px 0; }
    .rank-points { font-size: 1.2rem; font-weight: 600; color: rgba(255,255,255,0.9); }
    
    .stat-card {
        background: white; border-radius: 16px; padding: 20px;
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    .stat-number { font-size: 1.8rem; font-weight: 800; color: #f59e0b; }
    .stat-label { font-size: 0.8rem; color: #64748b; }
    
    .filter-tabs {
        display: flex; gap: 10px; margin-bottom: 20px;
        overflow-x: auto; padding-bottom: 10px;
    }
    .filter-tab {
        padding: 10px 20px; border-radius: 25px; font-weight: 600;
        cursor: pointer; transition: all 0.2s; white-space: nowrap;
        border: 2px solid transparent;
    }
    .filter-tab.active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white; border-color: transparent;
    }
    .filter-tab:not(.active) {
        background: #f1f5f9; color: #64748b;
    }
    
    .leader-card {
        background: white; border-radius: 16px; padding: 16px 20px;
        display: flex; align-items: center; gap: 15px;
        margin-bottom: 12px; border: 1px solid #f1f5f9;
        transition: all 0.2s;
    }
    .leader-card:hover {
        border-color: #667eea; box-shadow: 0 5px 20px rgba(102, 126, 234, 0.1);
        transform: translateX(5px);
    }
    .leader-card.top-3 {
        background: linear-gradient(135deg, #fefce8 0%, #fef9c3 100%);
        border-color: #fde047;
    }
    
    .rank-badge {
        width: 40px; height: 40px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; font-size: 1rem;
    }
    .rank-1 { background: linear-gradient(135deg, #FFD700, #FDB931); color: white; }
    .rank-2 { background: linear-gradient(135deg, #E0E0E0, #BDBDBD); color: white; }
    .rank-3 { background: linear-gradient(135deg, #CD7F32, #A05A2C); color: white; }
    .rank-other { background: #f1f5f9; color: #64748b; }
    
    .leader-avatar {
        width: 50px; height: 50px; border-radius: 50%;
        object-fit: cover; border: 2px solid #e2e8f0;
    }
    
    .leader-info { flex: 1; }
    .leader-name { font-weight: 700; color: #1e293b; font-size: 1rem; }
    .leader-sub { font-size: 0.8rem; color: #94a3b8; }
    
    .leader-points {
        text-align: right;
    }
    .points-val { font-size: 1.3rem; font-weight: 800; color: #667eea; }
    .points-label { font-size: 0.7rem; color: #94a3b8; }
    
    .medal-icon { font-size: 1.2rem; margin-right: 5px; }
    
    .category-badge {
        padding: 4px 10px; border-radius: 12px; font-size: 0.7rem; font-weight: 600;
    }
    .badge-tests { background: #dbeafe; color: #2563eb; }
    .badge-forum { background: #dcfce7; color: #16a34a; }
    .badge-mentor { background: #fce7f3; color: #db2777; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1 class="page-title">🏆 Leaderboard</h1>
    <p class="page-subtitle">Top performers at PEC - Earn points from tests, mentorship & community</p>
</div>
""", unsafe_allow_html=True)

col_refresh, col_spacer = st.columns([1, 10])
with col_refresh:
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()

if "leaderboard_filter" not in st.session_state:
    st.session_state.leaderboard_filter = "All"

leaderboard_data = get_cached_leaderboard()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{len(leaderboard_data)}</div>
        <div class="stat-label">Total Students</div>
    </div>
    """, unsafe_allow_html=True)
with c2:
    total_tests = sum(u.get('tests_taken', 0) for u in leaderboard_data)
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{total_tests}</div>
        <div class="stat-label">Tests Completed</div>
    </div>
    """, unsafe_allow_html=True)
with c3:
    total_answers = sum(u.get('answers_given', 0) for u in leaderboard_data)
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{total_answers}</div>
        <div class="stat-label">Doubts Solved</div>
    </div>
    """, unsafe_allow_html=True)
with c4:
    mentors = sum(1 for u in leaderboard_data if u.get('is_mentor', False))
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-number">{mentors}</div>
        <div class="stat-label">Active Mentors</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

if leaderboard_data:
    u1 = leaderboard_data[0] if len(leaderboard_data) > 0 else None
    u2 = leaderboard_data[1] if len(leaderboard_data) > 1 else None
    u3 = leaderboard_data[2] if len(leaderboard_data) > 2 else None

    st.markdown("### 🥇 Top 3 Champions")
    
    # Get avatar URLs using database function
    u1_avatar = db.get_avatar_url(u1.get('username', '')) if u1 else ""
    u2_avatar = db.get_avatar_url(u2.get('username', '')) if u2 else ""
    u3_avatar = db.get_avatar_url(u3.get('username', '')) if u3 else ""
    
    html_code = '<div class="podium-wrapper"><div class="podium-container">'
    
    if u2:
        html_code += f"""
        <div class="podium-place p-2">
            <div class="rank-number">🥈 #2</div>
            <img src="{u2_avatar}" class="avatar-circle">
            <div class="rank-name">@{u2['username']}</div>
            <div class="rank-points">{u2['points']} pts</div>
        </div>"""
    
    if u1:
        html_code += f"""
        <div class="podium-place p-1">
            <div class="crown">👑</div>
            <div class="rank-number">🥇 #1</div>
            <img src="{u1_avatar}" class="avatar-circle">
            <div class="rank-name">@{u1['username']}</div>
            <div class="rank-points">{u1['points']} pts</div>
        </div>"""
            
    if u3:
        html_code += f"""
        <div class="podium-place p-3">
            <div class="rank-number">🥉 #3</div>
            <img src="{u3_avatar}" class="avatar-circle">
            <div class="rank-name">@{u3['username']}</div>
            <div class="rank-points">{u3['points']} pts</div>
        </div>"""
            
    html_code += '</div></div>'
    st.markdown(html_code, unsafe_allow_html=True)

st.markdown("---")

st.markdown("### 📊 Full Rankings")

c_search, c_filter = st.columns([2, 1])
with c_search:
    search = st.text_input("🔍 Find a student...", placeholder="Search by username...", key="leader_search")

filtered = leaderboard_data
if search:
    filtered = [u for u in leaderboard_data if search.lower() in u.get('username', '').lower()]

for i, user in enumerate(filtered[:50]):
    rank = i + 1
    is_me = "user" in st.session_state and st.session_state.get("user") == user.get('username')
    
    rank_class = f"rank-{rank}" if rank <= 3 else "rank-other"
    top_class = "top-3" if rank <= 3 else ""
    
    medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"#{rank}"
    
    # Get avatar URL using database function
    username = user.get('username', '')
    avatar = db.get_avatar_url(username) if username else f"https://api.dicebear.com/7.x/identicon/svg?seed={username}"
    
    badges = ""
    if user.get('tests_taken', 0) > 0:
        badges += f'<span class="category-badge badge-tests">📝 {user.get("test_points", 0)} pts</span>'
    if user.get('answers_given', 0) > 0:
        badges += f'<span class="category-badge badge-forum">💬 {user.get("forum_points", 0)} pts</span>'
    if user.get('is_mentor', False):
        badges += f'<span class="category-badge badge-mentor">🧑‍🏫 {user.get("mentor_points", 0)} pts</span>'
    
    with st.container():
        st.markdown(f"""
        <div class="leader-card {top_class}">
            <div class="rank-badge {rank_class}">{medal}</div>
            <img src="{avatar}" class="leader-avatar">
            <div class="leader-info">
                <div class="leader-name">@{user.get('username', 'Unknown')}</div>
                <div class="leader-sub">{badges}</div>
            </div>
            <div class="leader-points">
                <div class="points-val">{user.get('points', 0)}</div>
                <div class="points-label">points</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if is_me:
            st.caption("👆 This is you!")

if not filtered:
    st.info("No students found matching your search.")
