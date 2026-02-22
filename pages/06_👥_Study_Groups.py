import streamlit as st
import database as db
from datetime import datetime, timedelta

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
    
    .admin-banner {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white; padding: 10px 20px; border-radius: 10px;
        margin-bottom: 15px;
    }
    .admin-banner h3 { margin: 0; }
    
    .page-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 24px 30px; border-radius: 16px; margin-bottom: 24px;
    }
    .page-title { color: white; font-size: 1.8rem; font-weight: 800; margin: 0; }
    .page-subtitle { color: rgba(255,255,255,0.8); font-size: 0.9rem; margin-top: 4px; }
    
    .sidebar-section {
        background: #1e1e2e; min-height: 100vh; padding: 15px; border-radius: 12px;
    }
    
    .room-item {
        padding: 12px 16px; margin-bottom: 8px; border-radius: 12px;
        cursor: pointer; transition: all 0.2s;
        display: flex; align-items: center; gap: 10px;
    }
    .room-item:hover { background: #313244; }
    .room-item.active { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
    .room-icon { font-size: 1.3rem; }
    .room-name { font-weight: 600; color: #cdd6f4; font-size: 0.95rem; }
    
    .chat-header {
        background: #181825; padding: 15px 20px; border-radius: 12px 12px 0 0;
        display: flex; justify-content: space-between; align-items: center;
    }
    .chat-title { font-size: 1.2rem; font-weight: 700; color: #cdd6f4; }
    .chat-subtitle { font-size: 0.8rem; color: #9399b2; }
    
    .message-bubble {
        padding: 12px 16px; margin-bottom: 10px; border-radius: 16px;
        max-width: 70%;
    }
    .message-sent {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; margin-left: auto; border-bottom-right-radius: 4px;
    }
    .message-received {
        background: #313244; color: #cdd6f4; border-bottom-left-radius: 4px;
    }
    .message-sender {
        font-size: 0.75rem; font-weight: 700; color: #89b4fa; margin-bottom: 4px;
    }
    .message-time {
        font-size: 0.65rem; opacity: 0.7; text-align: right; margin-top: 4px;
    }
    
    .online-dot {
        width: 10px; height: 10px; background: #a6e3a1; border-radius: 50%;
        display: inline-block;
    }
    
    .create-room-card {
        background: #313244; padding: 20px; border-radius: 16px;
        border: 2px dashed #585b70;
    }
    
    .member-badge {
        background: #313244; padding: 4px 12px; border-radius: 20px;
        font-size: 0.75rem; color: #9399b2;
    }
    
    .action-btn {
        background: #313244; border: none; padding: 8px 16px;
        border-radius: 8px; color: #cdd6f4; cursor: pointer;
    }
    .action-btn:hover { background: #45475a; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1 class="page-title">👥 Study Groups</h1>
    <p class="page-subtitle">Join rooms, find study partners, and learn together</p>
</div>
""", unsafe_allow_html=True)

if is_admin:
    st.markdown("""
    <div class="admin-banner">
        <h3>🛡️ Admin Mode - Monitor All Messages</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Admin: Delete rooms
    st.markdown("### 🗑️ Admin - Delete Rooms")
    all_rooms = db.get_all_rooms()
    for room in all_rooms:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.markdown(f"**{room.get('room_name', 'Unknown')}**")
        with c2:
            if st.button(f"Delete", key=f"admin_del_room_{room.get('room_name')}"):
                db.delete_room(room.get('room_name'))
                st.success(f"Room {room.get('room_name')} deleted!")
                st.rerun()
    
    st.markdown("---")
    
    # Admin: View all study group messages
    if st.checkbox("📋 View All Study Group Messages (Admin)"):
        all_study_msgs = db.get_all_study_messages()
        st.markdown(f"### Total Messages: {len(all_study_msgs)}")
        
        for msg in all_study_msgs[:100]:
            with st.expander(f"{msg.get('username', 'Unknown')} in {msg.get('room_name', 'Unknown')}: {msg.get('message', '')[:50]}..."):
                st.markdown(f"**Room:** {msg.get('room_name', 'N/A')}")
                st.markdown(f"**User:** {msg.get('username', 'N/A')}")
                st.markdown(f"**Message:** {msg.get('message', 'N/A')}")
                st.markdown(f"**Time:** {msg.get('created_at', 'N/A')}")
                
                if st.button(f"Delete Message", key=f"admin_del_study_{msg.get('id')}"):
                    db.delete_study_message(msg.get('id'))
                    st.success("Message deleted!")
                    st.rerun()

if "selected_room" not in st.session_state:
    st.session_state.selected_room = None
if "show_create" not in st.session_state:
    st.session_state.show_create = False

available_rooms = db.get_all_rooms()

c_rooms, c_chat = st.columns([1, 3])

with c_rooms:
    st.markdown("### 📚 Study Rooms")
    
    with st.expander("➕ Create New Room", expanded=st.session_state.show_create):
        with st.form("create_room_form"):
            new_room_name = st.text_input("Room Name", placeholder="Ex: Backlog Batch 2026")
            room_desc = st.text_area("Description (optional)", placeholder="What's this room about?")
            if st.form_submit_button("✨ Create Room", type="primary"):
                if new_room_name.strip():
                    final_name = "📢 " + new_room_name
                    if db.create_new_room(final_name):
                        st.success(f"Created {final_name}!")
                        st.session_state.selected_room = final_name
                        st.session_state.show_create = False
                        st.rerun()
                    else:
                        st.warning("Room already exists!")
                else:
                    st.warning("Please enter a room name!")
    
    st.markdown("---")
    
    st.markdown("**Available Rooms**")
    for room in available_rooms:
        room_name = room.get('room_name', '') if isinstance(room, dict) else str(room)
        is_active = st.session_state.selected_room == room_name
        room_icon = "📢" if "📢" in room_name else "💬"
        room_clean = room_name.replace("📢 ", "").replace("💬 ", "") if isinstance(room_name, str) else str(room_name)
        
        btn_style = "background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);" if is_active else "background: #313244;"
        
        if st.button(f"{room_icon} {room_clean}", key=f"room_{room_name}", 
                    use_container_width=True,
                    type="secondary" if not is_active else "primary"):
            st.session_state.selected_room = room_name
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📊 Quick Stats")
    st.metric("Total Rooms", len(available_rooms))
    st.metric("Active Members", len(available_rooms) * 3)

with c_chat:
    if not st.session_state.selected_room:
        st.markdown("""
        <div style="text-align: center; padding: 80px 20px; background: #1e1e2e; border-radius: 16px;">
            <h2 style="color: #9399b2;">👋 Welcome to Study Groups!</h2>
            <p style="color: #6c7086;">Select a room from the left to start chatting</p>
            <p style="font-size: 3rem;">💬</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        room = st.session_state.selected_room
        
        st.markdown(f"""
        <div class="chat-header">
            <div>
                <div class="chat-title">{room.replace('📢 ', '').replace('💬 ', '')}</div>
                <div class="chat-subtitle"><span class="online-dot"></span> Active now</div>
            </div>
            <div>
                <span class="member-badge">👥 {len(db.get_group_messages(room))} messages</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if "user" not in st.session_state:
            st.warning("🔐 Please login to chat in this room!")
        else:
            messages = db.get_group_messages(room)
            
            chat_container = st.container(height=450, border=False)
            
            with chat_container:
                if not messages:
                    st.markdown("""
                    <div style="text-align: center; padding: 60px 20px; color: #6c7086;">
                        <p style="font-size: 2rem;">💭</p>
                        <p>No messages yet. Be the first to say hello!</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    for msg in messages:
                        sender = msg['username']
                        text = msg['message']
                        ts = msg.get('timestamp', '')
                        time_sent = ts[11:16] if ts else "Now"
                        
                        is_me = sender == st.session_state["user"]
                        
                        if is_me:
                            st.markdown(f"""
                            <div class="message-bubble message-sent">
                                <div>{text}</div>
                                <div class="message-time">{time_sent}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            avatar_url = db.get_avatar_url(sender)
                            st.markdown(f"""
                            <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                                <img src="{avatar_url}" style="width: 35px; height: 35px; border-radius: 50%;">
                                <div class="message-bubble message-received">
                                    <div class="message-sender">@{sender}</div>
                                    <div>{text}</div>
                                    <div class="message-time">{time_sent}</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
            
            with st.form(key="chat_form", clear_on_submit=True):
                c_input, c_send = st.columns([5, 1])
                with c_input:
                    new_msg = st.text_input("Message...", placeholder="Type your message...", 
                                          label_visibility="collapsed", key="msg_input")
                with c_send:
                    sent = st.form_submit_button("➤", use_container_width=True)
                
                if sent and new_msg.strip():
                    db.send_group_message(st.session_state["user"], room, new_msg)
                    st.rerun()
            
            st.caption("💡 Tip: Be respectful and helpful to fellow students!")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6c7086; font-size: 0.8rem;">
    Made with ❤️ by PEC Connect | Study Groups
</div>
""", unsafe_allow_html=True)
