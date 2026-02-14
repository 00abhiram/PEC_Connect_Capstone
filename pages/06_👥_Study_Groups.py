import streamlit as st
import database as db

db.init_db()

st.set_page_config(page_title="Study Groups | PEC", page_icon="👥", layout="wide")

st.title("👥 Virtual Study Rooms")
st.caption("Join a room, find study partners, and learn together.")

# --- SIDEBAR: Room Selection & Creation ---
with st.sidebar:
    st.header("🚪 Select Room")
    
    # 1. Fetch Rooms from Database
    available_rooms = db.get_all_rooms()
    
    # If DB is empty for some reason, fallback
    if not available_rooms:
        available_rooms = ["☕ General Lounge"]

    room = st.radio("Available Groups:", available_rooms)
    
    st.info(f"You are in: **{room}**")
    
    st.divider()
    
    # 2. CREATE NEW ROOM SECTION
    with st.expander("➕ Create New Room"):
        with st.form("create_room_form"):
            new_room_name = st.text_input("Room Name", placeholder="Ex: Backlog Batch 2026")
            # Optional: Add an emoji picker logic if you want
            is_created = st.form_submit_button("Create")
            
            if is_created:
                if new_room_name:
                    # Add a fun emoji if the user didn't add one
                    final_name = "📢 " + new_room_name if not any(x in new_room_name for x in ["🔥","☕","📚"]) else new_room_name
                    
                    success = db.create_new_room(final_name)
                    if success:
                        st.success(f"Created {final_name}!")
                        st.rerun() # Refresh to show new room in list
                    else:
                        st.warning("Room already exists!")
                else:
                    st.warning("Enter a name first.")

    if st.button("🔄 Refresh Chat"):
        st.rerun()

# --- MAIN CHAT INTERFACE ---
if "user" not in st.session_state:
    st.warning("🔒 Please Login to join the chat.")
    st.stop()

# 1. Display Messages
st.subheader(f"💬 {room}")
messages = db.get_group_messages(room)

# Container for chat history
chat_container = st.container(height=400, border=True)

if not messages:
    chat_container.info("No messages yet. Be the first to say hello!")
else:
    with chat_container:
        for msg in messages:
            # msg = (id, username, room, text, timestamp)
            sender = msg[1]
            text = msg[3]
            time_sent = msg[4][11:16] # Extract HH:MM
            
            if sender == st.session_state["user"]:
                # My messages (Right aligned)
                st.markdown(f"""
                <div style='text-align: right; background-color: #dcf8c6; padding: 8px; border-radius: 10px; margin: 5px; display: inline-block; float: right; clear: both;'>
                    <b>You</b> <small>{time_sent}</small><br>{text}
                </div>
                """, unsafe_allow_html=True)
            else:
                # Others' messages (Left aligned)
                st.markdown(f"""
                <div style='text-align: left; background-color: #f1f0f0; padding: 8px; border-radius: 10px; margin: 5px; display: inline-block; float: left; clear: both;'>
                    <b>@{sender}</b> <small>{time_sent}</small><br>{text}
                </div>
                """, unsafe_allow_html=True)

# 2. Input Box
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    with col1:
        new_msg = st.text_input("Message...", placeholder="Type here...", label_visibility="collapsed")
    with col2:
        sent = st.form_submit_button("➤")
    
    if sent and new_msg:
        db.send_group_message(st.session_state["user"], room, new_msg)
        st.rerun()