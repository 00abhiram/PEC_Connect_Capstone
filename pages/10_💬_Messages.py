import streamlit as st
import database as db
from datetime import datetime

db.init_db()

# Check for admin
is_admin = st.session_state.get("is_admin", False)

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
    
    section[data-testid="stSidebar"] { background: #FFFFFF !important; }
    section[data-testid="stSidebar"] * { color: #1a1a1a !important; }
    
    .admin-banner {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white; padding: 10px 20px; border-radius: 10px;
        margin-bottom: 15px;
    }
    .admin-banner h3 { margin: 0; }
    
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px 30px; border-radius: 20px; margin-bottom: 25px;
    }
    .header h1 { color: white; margin: 0; font-size: 1.8rem; font-weight: 800; }
    .header p { color: rgba(255,255,255,0.8); margin: 5px 0 0; }
    
    .person-card {
        background: white; border-radius: 16px; padding: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06); margin-bottom: 15px;
    }
    .person-img { width: 70px; height: 70px; border-radius: 50%; border: 3px solid #667eea; }
    .person-name { font-weight: 700; font-size: 1.1rem; color: #1e293b; }
    .person-username { color: #64748b; font-size: 0.9rem; }
    .person-msg { color: #94a3b8; font-size: 0.85rem; margin-top: 5px; }
    
    .chat-header {
        display: flex; align-items: center; gap: 15px;
        padding: 15px 0; border-bottom: 1px solid #e2e8f0; margin-bottom: 15px;
    }
    .chat-header-img { width: 45px; height: 45px; border-radius: 50%; border: 2px solid #667eea; }
    .chat-header h3 { margin: 0; font-weight: 700; color: #1e293b; font-size: 1.1rem; }
    .chat-header span { color: #10b981; font-size: 0.85rem; }
    
    .chat-container { min-height: 400px; max-height: 450px; overflow-y: auto; padding-right: 10px; }
    
    .msg-row { display: flex; margin-bottom: 12px; position: relative; }
    .msg-row.sent { justify-content: flex-end; }
    .msg-row.received { justify-content: flex-start; }
    
    .msg {
        max-width: 70%; padding: 12px 18px; border-radius: 18px;
        border: 2px solid #667eea; position: relative;
    }
    .msg-sent {
        background: linear-gradient(135deg, #667eea, #764ba2); color: white;
        border-bottom-right-radius: 4px;
    }
    .msg-received {
        background: #f1f5f9; color: #1e293b;
        border-bottom-left-radius: 4px;
    }
    .msg-img {
        max-width: 250px; border-radius: 12px; margin-bottom: 5px;
    }
    .msg-time { font-size: 0.7rem; opacity: 0.7; display: block; margin-top: 4px; }
    
    .clear-btn {
        background: #ef4444; color: white; border: none;
        padding: 8px 16px; border-radius: 8px; font-size: 0.85rem;
        cursor: pointer; float: right;
    }
    
    .empty { text-align: center; padding: 40px; color: #94a3b8; }
</style>

<script>
function scrollToBottom() {
    const container = document.querySelector('.chat-container');
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}

document.addEventListener('DOMContentLoaded', scrollToBottom);
window.addEventListener('load', scrollToBottom);

// Auto-refresh every 3 seconds for real-time updates
setTimeout(function() {
    window.location.reload();
}, 3000);
</script>
""", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.warning("Please Login.")
    st.stop()

current_user = st.session_state["user"]

if "msg_view" not in st.session_state:
    st.session_state.msg_view = "list"
if "msg_with" not in st.session_state:
    st.session_state.msg_with = None
if "msg_text" not in st.session_state:
    st.session_state.msg_text = ""
if "img_sent" not in st.session_state:
    st.session_state.img_sent = False

def get_connections():
    try:
        sent = db.supabase.table("connections").select("receiver").eq("sender", current_user).eq("status", "accepted").execute().data or []
        received = db.supabase.table("connections").select("sender").eq("receiver", current_user).eq("status", "accepted").execute().data or []
        
        usernames = set()
        for s in sent:
            r = s.get('receiver')
            if r: usernames.add(r)
        for r in received:
            s = r.get('sender')
            if s: usernames.add(s)
        
        connections = []
        for u in usernames:
            user_data = db.get_user_details(u)
            if user_data:
                connections.append(user_data)
        return connections
    except:
        return []

def send_and_clear():
    if st.session_state.msg_text.strip():
        db.send_message(current_user, st.session_state.msg_with, st.session_state.msg_text)
        st.session_state.msg_text = ""

# LIST VIEW
if st.session_state.msg_view == "list":
    st.markdown("""
    <div class="header">
        <h1>💬 Messages</h1>
        <p>Your connections</p>
    </div>
    """, unsafe_allow_html=True)
    
    if is_admin:
        st.markdown("""
        <div class="admin-banner">
            <h3>🛡️ Admin Mode - View All Conversations</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Admin: Send message to any user
        st.markdown("### 📤 Send Message to Any User")
        with st.expander("Compose Message (No Connection Required)"):
            admin_recipient = st.text_input("Recipient Username", placeholder="Enter username")
            admin_msg = st.text_area("Message")
            if st.button("Send Message"):
                if admin_recipient and admin_msg:
                    db.send_message("00abhiram", admin_recipient, admin_msg)
                    st.success(f"Message sent to {admin_recipient}!")
        
        st.markdown("---")
        
        # Admin: View all users and their messages
        st.markdown("### 👁️ Monitor Conversations")
        all_users = db.get_all_users()
        admin_user_select = st.selectbox("Select User to Monitor", [u.get('username', '') for u in all_users])
        
        if admin_user_select:
            st.markdown(f"### Chat with {admin_user_select}")
            # Show all messages involving this user
            all_msgs = db.get_all_messages()
            user_msgs = [m for m in all_msgs if m.get('sender_username') == admin_user_select or m.get('receiver_username') == admin_user_select]
            
            for m in user_msgs[:50]:
                sender = m.get('sender_username', '')
                receiver = m.get('receiver_username', '')
                content = m.get('content', '')
                tm = m.get('created_at', '')
                
                with st.expander(f"{sender} → {receiver}: {content[:30]}..."):
                    st.markdown(f"**From:** {sender}")
                    st.markdown(f"**To:** {receiver}")
                    st.markdown(f"**Message:** {content}")
                    st.markdown(f"**Time:** {tm}")
                    
                    if st.button(f"Delete Message", key=f"admin_del_msg_{m.get('id')}"):
                        db.delete_chat_message(m.get('id'))
                        st.success("Message deleted!")
                        st.rerun()
    
    connections = get_connections()
    
    if not connections:
        st.markdown('<div class="empty">👥 No connections yet.<br>Go to Campus Network to connect!</div>', unsafe_allow_html=True)
    else:
        for conn in connections:
            username = conn.get('username', '')
            full_name = conn.get('full_name', username)
            avatar = db.get_avatar_url(username)
            
            msgs = db.get_chat_history(current_user, username)
            last_msg = msgs[-1].get('content', '') if msgs else ''
            
            with st.container():
                c1, c2 = st.columns([1, 3])
                with c1:
                    st.image(avatar, width=70)
                with c2:
                    st.markdown(f"**{full_name}**")
                    st.caption(f"@{username}")
                    st.caption(f"💬 {last_msg[:25]}..." if last_msg else "No messages")
                
                if st.button(f"Chat with {username}", key=f"btn_{username}"):
                    st.session_state.msg_with = username
                    st.session_state.msg_view = "chat"
                    st.rerun()
                
                st.markdown("---")

# CHAT VIEW
else:
    username = st.session_state.msg_with
    
    if not username:
        st.session_state.msg_view = "list"
        st.rerun()
    
    partner_data = db.get_user_details(username)
    partner_name = partner_data.get('full_name', username) if partner_data else username
    partner_avatar = db.get_avatar_url(username)
    
    # Chat Header (no background card)
    st.markdown(f"""
    <div class="chat-header">
        <img src="{partner_avatar}" class="chat-header-img">
        <div>
            <h3>{partner_name}</h3>
            <span>🟢 Online</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 8])
    with col1:
        if st.button("← Back", key="back_btn"):
            st.session_state.msg_view = "list"
            st.session_state.msg_with = None
            st.rerun()
    with col2:
        if st.button("🗑️ Clear Chat", key="clear_chat"):
            db.clear_chat(current_user, username)
            st.rerun()
    
    # Messages (no background card)
    messages = db.get_chat_history(current_user, username)
    
    st.markdown('<div class="chat-container" id="chatContainer">', unsafe_allow_html=True)
    
    if not messages:
        st.markdown(f'<div class="empty">👋 Say hello to {partner_name}!</div>', unsafe_allow_html=True)
    else:
        for m in messages:
            is_me = m.get('sender_username') == current_user
            txt = m.get('content', '')
            tm = m.get('created_at', '')
            tm_str = tm[11:16] if tm else ''
            row_cls = "sent" if is_me else "received"
            msg_cls = "msg-sent" if is_me else "msg-received"
            msg_id = m.get('id')
            
            # Check if content is an image URL
            if txt.startswith('http') and any(ext in txt.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                content_html = f'<img src="{txt}" class="msg-img">'
            else:
                content_html = txt
            
            # Message with delete button using Streamlit columns
            c1, c2 = st.columns([8, 1]) if is_me else st.columns([1, 8])
            
            with c1:
                st.markdown(f"""
                <div class="msg-row {row_cls}">
                    <div class="msg {msg_cls}">
                        {content_html}
                        <span class="msg-time">{tm_str}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if is_me:
                with c2:
                    if st.button("🗑️", key=f"del_{msg_id}"):
                        db.delete_message(msg_id)
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Scroll to bottom after render
    st.markdown("""
    <script>
    setTimeout(function() {
        const container = document.getElementById('chatContainer');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    }, 100);
    </script>
    """, unsafe_allow_html=True)
    
    # Input section
    st.markdown('<div class="input-box">', unsafe_allow_html=True)
    
    with st.form("msg_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            msg = st.text_input("", placeholder="Type a message... (Press Enter to send)", key="msg_text", label_visibility="collapsed")
        with col2:
            submitted = st.form_submit_button("Send ➤")
        
        # Image upload inside form
        uploaded_file = st.file_uploader("🖼️ Add Image", type=['jpg', 'jpeg', 'png', 'gif', 'webp'], key="chat_img", label_visibility="collapsed")
        
        if submitted:
            # Send text if present
            if msg:
                db.send_message(current_user, username, msg)
            
            # Send image if present
            if uploaded_file:
                try:
                    file_ext = uploaded_file.name.split('.')[-1]
                    unique_name = f"{current_user}_{datetime.now().timestamp()}.{file_ext}"
                    
                    db.supabase.storage.from_("avatars").upload(
                        unique_name,
                        uploaded_file.getvalue(),
                        {"content-type": f"image/{file_ext}"}
                    )
                    img_url = db.supabase.storage.from_("avatars").get_public_url(unique_name)
                    
                    if img_url:
                        db.send_message(current_user, username, img_url)
                except Exception as e:
                    st.error("Failed to send image")
            
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
