import streamlit as st
import database as db
import time

st.set_page_config(page_title="Messages", page_icon="💬", layout="wide")
db.init_db()

if "user" not in st.session_state:
    st.warning("Please Login.")
    st.stop()
partner = st.session_state.get("chat_with")
me = st.session_state["user"]
st.markdown("""
<style>
    .chat-container {
        padding: 10px;
        border-radius: 10px;
        background-color: #e5ddd5; /* WhatsApp BG Color */
        height: 500px;
        overflow-y: scroll;
        display: flex;
        flex-direction: column;
    }
    .msg-bubble {
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        max-width: 70%;
        font-size: 0.95rem;
        position: relative;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    .msg-me {
        background-color: #dcf8c6; /* Green for Me */
        align-self: flex-end;
        margin-left: auto;
        border-top-right-radius: 0;
    }
    .msg-other {
        background-color: #ffffff; /* White for Other */
        align-self: flex-start;
        margin-right: auto;
        border-top-left-radius: 0;
    }
    .msg-time {
        font-size: 0.7rem;
        color: #999;
        text-align: right;
        margin-top: 4px;
        display: block;
    }
    .chat-header {
        background: white; padding: 15px; border-bottom: 1px solid #ddd;
        display: flex; align-items: center; gap: 10px; margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

c1, c2 = st.columns([1, 3])
with c1:
    st.subheader("📥 Inbox")
    if st.button("⬅️ Find People", use_container_width=True):
        st.switch_page("pages/09_🌐_Campus_Network.py")
    
    st.divider()
    if partner:
        st.info(f"🟢 Chatting with **@{partner}**")
    else:
        st.caption("Select a friend from the Network page to start chatting.")

with c2:
    if not partner:
        st.image("https://cdn-icons-png.flaticon.com/512/1041/1041916.png", width=100)
        st.markdown("### Select a conversation")
    else:
        st.markdown(f"""
        <div class="chat-header">
            <h3>@{partner}</h3>
        </div>
        """, unsafe_allow_html=True)
        msgs = db.get_chat_history(me, partner)
        with st.container(height=450):
            for m in msgs:
                is_me = m['sender_username'] == me
                css_class = "msg-me" if is_me else "msg-other"
                align = "right" if is_me else "left"
                time_str = m['created_at'][11:16]
                
                st.markdown(f"""
                <div style="display: flex; justify-content: {align};">
                    <div class="msg-bubble {css_class}">
                        {m['content']}
                        <span class="msg-time">{time_str}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        with st.form("chat_input", clear_on_submit=True):
            c_in, c_btn = st.columns([6, 1])
            text = c_in.text_input("Message...", placeholder="Type a message...", label_visibility="collapsed")
            sent = c_btn.form_submit_button("➤")
            
            if sent and text:
                db.send_message(me, partner, text)
                st.rerun()