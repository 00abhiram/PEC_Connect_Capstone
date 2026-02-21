import streamlit as st
import database as db

db.init_db()
st.set_page_config(page_title="Study Groups", page_icon="👥", layout="wide")

st.title("👥 Virtual Study Rooms")
st.caption("Join a room, find study partners, and learn together.")

with st.sidebar:
    st.header("🚪 Select Room")
    
    available_rooms = db.get_all_rooms()
    room = st.radio("Available Groups:", available_rooms)
    
    st.info(f"You are in: **{room}**")
    st.divider()

    with st.expander("➕ Create New Room"):
        with st.form("create_room_form"):
            new_room_name = st.text_input("Room Name", placeholder="Ex: Backlog Batch 2026")
            if st.form_submit_button("Create"):
                if new_room_name:
                    final_name = "📢 " + new_room_name
                    if db.create_new_room(final_name):
                        st.success(f"Created {final_name}!")
                        st.rerun()
                    else:
                        st.warning("Room already exists!")

    if st.button("🔄 Refresh Chat"):
        st.rerun()

if "user" not in st.session_state:
    st.warning("🔒 Please Login to join the chat.")
    st.stop()

st.subheader(f"💬 {room}")
messages = db.get_group_messages(room)

chat_container = st.container(height=400, border=True)

if not messages:
    chat_container.info("No messages yet. Be the first to say hello!")
else:
    with chat_container:
        for msg in messages:
            sender = msg['username']
            text = msg['message']
            time_sent = msg['timestamp'][11:16] if 'timestamp' in msg else "Now"
            
            if sender == st.session_state["user"]:
                st.markdown(f"""
                <div style='text-align: right; margin: 5px;'>
                    <span style='background-color: #dcf8c6; padding: 8px 12px; border-radius: 15px; display: inline-block;'>
                        <b>You</b> <small style='opacity:0.6'>{time_sent}</small><br>{text}
                    </span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='text-align: left; margin: 5px;'>
                    <span style='background-color: #f1f0f0; padding: 8px 12px; border-radius: 15px; display: inline-block;'>
                        <b style='color:#d97706'>@{sender}</b> <small style='opacity:0.6'>{time_sent}</small><br>{text}
                    </span>
                </div>
                """, unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    with col1:
        new_msg = st.text_input("Message...", placeholder="Type here...", label_visibility="collapsed")
    with col2:
        sent = st.form_submit_button("➤")
    
    if sent and new_msg:
        db.send_group_message(st.session_state["user"], room, new_msg)
        st.rerun()