import streamlit as st
import google.generativeai as genai
from groq import Groq
import time
import re
import base64
from io import BytesIO

# Sidebar toggle CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
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
    
    /* Main Background */
    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* Custom Header */
    .custom-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 20px 32px;
        margin: -10px -1000px 20px -1000px;
        position: relative;
        left: 50%;
        right: 50%;
        width: 2000px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .header-left { display: flex; align-items: center; gap: 16px; }
    .header-logo {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    .header-title {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .header-subtitle {
        color: #94a3b8;
        font-size: 0.875rem;
        font-weight: 400;
    }
    .header-badge {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .status-dot-header {
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Control Bar */
    .control-bar {
        background: #f1f5f9;
        border-radius: 12px;
        padding: 12px 16px;
        margin: 16px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
        flex-wrap: wrap;
    }
    .control-section {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    .controls-right {
        margin-left: auto;
    }
    .mode-btn {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 8px 14px;
        font-size: 0.85rem;
        font-weight: 500;
        color: #475569;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .mode-btn:hover {
        background: #e2e8f0;
        border-color: #cbd5e1;
    }
    .mode-btn.active {
        background: #1e293b;
        border-color: #1e293b;
        color: white;
    }
    .year-select {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 0.85rem;
        color: #475569;
        cursor: pointer;
    }
    
    .sidebar-header {
        padding: 20px;
        border-bottom: 1px solid #e2e8f0;
    }
    .sidebar-section {
        padding: 16px 20px;
    }
    .sidebar-label {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 12px;
    }
    
    /* Mode Selector Cards */
    .mode-card {
        background: #f8fafc;
        border: 2px solid transparent;
        border-radius: 14px;
        padding: 16px;
        cursor: pointer;
        transition: all 0.25s ease;
        text-align: center;
        margin-bottom: 8px;
    }
    .mode-card:hover {
        background: #f1f5f9;
        border-color: #cbd5e1;
        transform: translateY(-2px);
    }
    .mode-card.active {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }
    .mode-icon {
        font-size: 1.75rem;
        margin-bottom: 8px;
    }
    .mode-title {
        font-weight: 600;
        font-size: 0.9rem;
        color: #1e293b;
        margin-bottom: 4px;
    }
    .mode-desc {
        font-size: 0.75rem;
        color: #64748b;
    }
    
    /* Chat Container */
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Message Bubbles */
    .message-wrapper {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 24px;
        animation: slideIn 0.3s ease;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .message-wrapper.user {
        flex-direction: row-reverse;
    }
    .message-avatar {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
    }
    .message-avatar.user {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    .message-avatar.ai {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    .message-bubble {
        max-width: 75%;
        padding: 16px 20px;
        border-radius: 18px;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .message-bubble.user {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-bottom-right-radius: 4px;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.25);
    }
    .message-bubble.ai {
        background: white;
        color: #1e293b;
        border-bottom-left-radius: 4px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    
    /* Input Area */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        border-top: 1px solid #e2e8f0;
        padding: 16px 24px 24px;
        z-index: 100;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.05);
    }
    .input-wrapper {
        max-width: 800px;
        margin: 0 auto;
        background: #ffffff;
        border: 2px solid #1e293b;
        border-radius: 12px;
        padding: 4px 4px 4px 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.2s ease;
    }
    .input-wrapper:focus-within {
        border-color: #1e293b;
        box-shadow: 0 0 0 3px rgba(30, 41, 59, 0.2);
    }
    .input-field {
        flex: 1;
        border: none;
        background: transparent;
        font-size: 1rem;
        color: #1e293b;
        outline: none;
        padding: 12px 0;
    }
    .input-field::placeholder {
        color: #64748b;
    }
    
    /* Style for Streamlit inputs inside input wrapper */
    .input-wrapper .stTextInput input {
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        padding: 12px 8px !important;
        color: #1e293b !important;
    }
    .input-wrapper .stTextInput input::placeholder {
        color: #64748b !important;
    }
    .input-wrapper .stTextInput input:focus {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    /* Button styling */
    .input-wrapper .stButton > button {
        border-radius: 12px !important;
        padding: 8px 12px !important;
    }
    .input-wrapper .stButton > button[kind="secondary"] {
        background: #f1f5f9 !important;
        border: 1px solid #e2e8f0 !important;
    }
    .input-wrapper .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border: none !important;
        padding: 10px 16px !important;
    }
    .attach-btn {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        border: none;
        background: #f1f5f9;
        color: #64748b;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        transition: all 0.2s ease;
    }
    .attach-btn:hover {
        background: #e2e8f0;
        color: #3b82f6;
    }
    .send-btn {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        border: none;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    .send-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
    }
    .send-btn:disabled {
        background: #cbd5e1;
        cursor: not-allowed;
        box-shadow: none;
    }
    
    /* Attachments Preview */
    .attachments-bar {
        max-width: 800px;
        margin: 0 auto 12px;
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        padding: 0 24px;
    }
    .attachment-chip {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 8px 14px;
        font-size: 0.8rem;
        display: flex;
        align-items: center;
        gap: 8px;
        color: #475569;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    .attachment-chip .remove {
        cursor: pointer;
        color: #94a3b8;
        font-weight: bold;
    }
    .attachment-chip .remove:hover {
        color: #ef4444;
    }
    
    /* Popover Styling */
    .attach-popover {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    }
    .attach-option {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .attach-option:hover {
        background: #f1f5f9;
    }
    .attach-icon {
        width: 40px;
        height: 40px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    .attach-icon.pdf { background: #fee2e2; color: #ef4444; }
    .attach-icon.image { background: #dbeafe; color: #3b82f6; }
    .attach-icon.link { background: #d1fae5; color: #10b981; }
    
    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        max-width: 500px;
        margin: 40px auto;
    }
    .empty-icon {
        font-size: 4rem;
        margin-bottom: 20px;
    }
    .empty-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 12px;
    }
    .empty-desc {
        color: #64748b;
        font-size: 1rem;
        line-height: 1.6;
    }
    .suggestion-chips {
        display: flex;
        gap: 10px;
        justify-content: center;
        flex-wrap: wrap;
        margin-top: 24px;
    }
    .suggestion-chip {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 10px 18px;
        font-size: 0.85rem;
        color: #475569;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .suggestion-chip:hover {
        background: #3b82f6;
        color: white;
        border-color: #3b82f6;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25);
    }
    
    /* Tool Cards in Sidebar */
    .tool-card {
        background: #f8fafc;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 10px;
        border: 1px solid #e2e8f0;
    }
    .tool-card.active {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-color: #3b82f6;
    }
    
    /* Status Indicators */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .status-pill.online {
        background: #d1fae5;
        color: #059669;
    }
    .status-pill.offline {
        background: #fee2e2;
        color: #dc2626;
    }
    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
    }
    .status-pill.online .status-dot { background: #10b981; }
    .status-pill.offline .status-dot { background: #ef4444; }
    
    /* Loading Animation */
    .typing-indicator {
        display: flex;
        gap: 4px;
        padding: 16px 20px;
    }
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #94a3b8;
        border-radius: 50%;
        animation: bounce 1.4s infinite;
    }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-8px); }
    }
    
    /* Exam Mode Toggle */
    .exam-toggle {
        background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Divider */
    hr { border: none; border-top: 1px solid #e2e8f0; margin: 20px 0; }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>
""", unsafe_allow_html=True)

SUBJECTS_BY_YEAR = {
    "1st Year": ["M1 - Matrices & Calculus", "M2 - Differential Equations & Vector Calculus", "Engineering Chemistry", "Applied Physics", "Programming for Problem Solving (C)", "Python Programming", "Basic Electrical Engineering", "Engineering Drawing", "Engineering Workshop", "IT Workshop", "English - Communication Skills", "Environmental Science"],
    "2nd Year": ["Discrete Mathematics", "Data Structures", "Digital Logic Design", "Computer Organization & Architecture", "Object Oriented Programming (Java/C++)", "Operating Systems", "Database Management Systems", "Formal Languages & Automata Theory", "Software Engineering", "Probability & Statistics", "Electronic Devices & Circuits", "Network Theory", "Signals & Systems", "Analog Electronics", "Digital Electronics"],
    "3rd Year": ["Algorithms", "Compiler Design", "Computer Networks", "Cryptography & Network Security", "Artificial Intelligence", "Machine Learning", "Data Science", "Cloud Computing", "DevOps", "Web Technologies", "Microprocessors & Microcontrollers"],
    "4th Year": ["Deep Learning", "Big Data", "Mobile App Development", "Blockchain Technology", "Internet of Things (IoT)", "Cybersecurity", "VLSI Design", "Digital Signal Processing", "Embedded Systems", "Image Processing", "Wireless Communications"],
    "Labs": ["C Programming Lab", "Python Lab", "Data Structures Lab", "DBMS Lab", "OS Lab", "CN Lab", "AI/ML Lab"],
    "Other": ["General", "All Branches"]
}

ALL_SUBJECTS = []
for year_subjects in SUBJECTS_BY_YEAR.values():
    ALL_SUBJECTS.extend(year_subjects)

try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        st.session_state["gemini_status"] = True
    else:
        st.session_state["gemini_status"] = False
except:
    st.session_state["gemini_status"] = False

try:
    if "GROQ_API_KEY" in st.secrets:
        groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        st.session_state["groq_status"] = True
    else:
        st.session_state["groq_status"] = False
except:
    st.session_state["groq_status"] = False

def ask_ai_engine(prompt):
    if st.session_state.get("gemini_status", False):
        try:
            response = gemini_model.generate_content(prompt)
            return response.text
        except: pass
    
    if st.session_state.get("groq_status", False):
        try:
            chat_completion = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"❌ Error: {e}"
    
    return "⚠️ AI services are currently unavailable. Please check API configuration."

if "tool_mode" not in st.session_state:
    st.session_state["tool_mode"] = "tutor"

user = st.session_state.get("user", "guest")
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = {}
if user not in st.session_state["chat_history"]:
    st.session_state["chat_history"][user] = []

if "attached_files" not in st.session_state:
    st.session_state["attached_files"] = []
if "attached_url" not in st.session_state:
    st.session_state["attached_url"] = ""
if "last_msg" not in st.session_state:
    st.session_state["last_msg"] = ""

# Custom Header with integrated controls
gemini_ok = st.session_state.get("gemini_status", False)
groq_ok = st.session_state.get("groq_status", False)

status_color = "#10b981" if gemini_ok or groq_ok else "#ef4444"
status_text = "AI Online" if gemini_ok or groq_ok else "AI Offline"

st.markdown(f"""
<div class="custom-header">
    <div class="header-left">
        <div class="header-logo">🧠</div>
        <div>
            <div class="header-title">PEC AI Study Bot</div>
            <div class="header-subtitle">Your Personal JNTUH Professor</div>
        </div>
    </div>
    <div class="header-badge" style="background: {status_color};">
        <span class="status-dot-header"></span>
        {status_text}
    </div>
</div>
""", unsafe_allow_html=True)

# Integrated Control Bar
st.markdown("### 🎯 AI Mode")

# Subject and Exam Mode
c1, c2, c3 = st.columns([2, 2, 1])
with c1:
    year_select = st.selectbox("📚 Year", list(SUBJECTS_BY_YEAR.keys()), key="year_sel")
with c2:
    current_subject = st.selectbox("📖 Subject", SUBJECTS_BY_YEAR[year_select], key="subj_sel")
with c3:
    exam_mode = st.toggle("🔥 Exam", value=False, help="Short answers")

st.markdown("")  # Small gap

# Mode buttons row
mode_cols = st.columns(4)

modes = [
    ("tutor", "💬", "AI Tutor"),
    ("examiner", "📝", "Strict Examiner"),
    ("diagram", "🎨", "Diagram Gen"),
    ("explainer", "📖", "Concept Explain")
]

current_mode = st.session_state.get("tool_mode", "tutor")

for idx, (mode_id, icon, title) in enumerate(modes):
    with mode_cols[idx]:
        is_active = current_mode == mode_id
        bg = "#1e293b" if is_active else "#f1f5f9"
        color = "white" if is_active else "#475569"
        border = "2px solid #1e293b" if is_active else "2px solid #e2e8f0"
        
        btn_html = f"""
        <div style="background:{bg}; color:{color}; border:{border}; 
            border-radius:10px; padding:12px; text-align:center; margin-bottom:8px;">
            <div style="font-size:1.2rem;">{icon}</div>
            <div style="font-size:0.8rem; font-weight:600;">{title}</div>
        </div>
        """
        st.markdown(btn_html, unsafe_allow_html=True)
        
        if st.button(f"{icon} {title}", key=f"mode_btn_{mode_id}", 
                     type="primary" if is_active else "secondary", use_container_width=True):
            st.session_state["tool_mode"] = mode_id
            st.rerun()

st.markdown("---")

# === AI TUTOR MODE ===
if st.session_state["tool_mode"] == "tutor":
    
    # Get messages - properly from session_state
    user = st.session_state.get("user", "guest")
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = {}
    if user not in st.session_state["chat_history"]:
        st.session_state["chat_history"][user] = []
    
    messages = st.session_state["chat_history"][user]
    
    # Show attachments
    has_attachments = (st.session_state["attached_files"] or 
                       st.session_state["attached_url"])
    
    if has_attachments:
        st.markdown('<div class="attachments-bar">', unsafe_allow_html=True)
        
        for f in st.session_state["attached_files"]:
            st.markdown(f'''
            <div class="attachment-chip">
                📄 {f.name[:20]}{'...' if len(f.name)>20 else ''}
                <span class="remove" onclick="fetch('/?clear_file={f.name}', {{method:'POST'}}).then(()=>window.location.reload())">×</span>
            </div>
            ''', unsafe_allow_html=True)
        
        if st.session_state["attached_url"]:
            st.markdown(f'''
            <div class="attachment-chip">
                🔗 {st.session_state["attached_url"][:30]}...
                <span class="remove" onclick="window.location.reload()">×</span>
            </div>
            ''', unsafe_allow_html=True)
        
        if st.button("🗑️ Clear All", key="clear_attach"):
            st.session_state["attached_files"] = []
            st.session_state["attached_url"] = ""
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if not messages:
        st.markdown(f"""
        <div class="empty-state">
            <div class="empty-icon">🧠</div>
            <div class="empty-title">Welcome to PEC AI Study Bot!</div>
            <div class="empty-desc">
                I'm your personal AI tutor for <b>{current_subject}</b>.<br>
                Ask me anything, share files, or get help with your studies.
            </div>
            <div class="suggestion-chips">
                <div class="suggestion-chip" onclick="document.querySelector('[data-testid=stTextInput] input').focus()">
                    Explain {list(SUBJECTS_BY_YEAR['1st Year'])[0]}
                </div>
                <div class="suggestion-chip" onclick="document.querySelector('[data-testid=stTextInput] input').focus()">
                    What is {list(SUBJECTS_BY_YEAR['3rd Year'])[4]}?
                </div>
                <div class="suggestion-chip" onclick="document.querySelector('[data-testid=stTextInput] input').focus()">
                    Help with assignment
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Show messages
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        
        avatar = "👤" if role == "user" else "🧠"
        bubble_class = "user" if role == "user" else "ai"
        
        st.markdown(f"""
        <div class="message-wrapper {role}">
            <div class="message-avatar {bubble_class}">{avatar}</div>
            <div class="message-bubble {bubble_class}">{content}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input area
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Better column layout for input area
    input_col1, input_col2, input_col3 = st.columns([1, 12, 2])
    
    with input_col1:
        with st.popover("📎", help="Attach files"):
            st.markdown("**📎 Attach PDF Files**")
            
            up_file = st.file_uploader(
                "Upload", 
                type=["pdf"],
                label_visibility="collapsed"
            )
            
            if up_file:
                if up_file not in st.session_state["attached_files"]:
                    st.session_state["attached_files"].append(up_file)
                    st.success("📄 Attached!")
                    st.rerun()
            
            st.markdown("---")
            st.markdown("**🔗 Add Link**")
            url_in = st.text_input("URL", placeholder="https://...", key="pop_url")
            if url_in:
                st.session_state["attached_url"] = url_in
                st.success("🔗 Added!")
                st.rerun()
    
    with input_col2:
        # Use a dynamic key to force input clear
        input_key = f"chat_input_{st.session_state.get('msg_count', 0)}"
        
        user_input = st.text_input(
            "Message", 
            placeholder=f"Ask anything about {current_subject}...",
            label_visibility="collapsed",
            key=input_key,
            disabled=False
        )
    
    with input_col3:
        send_btn = st.button("➤", type="primary", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle message
    if (user_input or send_btn) and user_input:
        if user_input != st.session_state.get("last_msg"):
            st.session_state["last_msg"] = user_input
            
            if user_input.startswith("http://") or user_input.startswith("https://"):
                st.session_state["attached_url"] = user_input
            
            messages.append({"role": "user", "content": user_input})
            
            with st.spinner("🤔 Thinking..."):
                content_context = ""
                
                if st.session_state["attached_files"]:
                    for f in st.session_state["attached_files"][:2]:
                        try:
                            import PyPDF2
                            reader = PyPDF2.PdfReader(f)
                            text = ""
                            for p in reader.pages[:3]:
                                text += p.extract_text() + "\n"
                            content_context += f"\n📄 {f.name}:\n{text[:2000]}\n"
                        except: 
                            content_context += f"\n📄 {f.name}:\n[File content could not be extracted]\n"
                
                if st.session_state["attached_url"]:
                    content_context += f"\n🔗 Reference: {st.session_state['attached_url']}\n"
                
                tone = "short, bullet points" if exam_mode else "detailed, friendly"
                
                prompt = f"""You are a helpful AI tutor for JNTUH students.
Subject: {current_subject}
Tone: {tone}
Current Exam Mode: {'ENABLED - give short answers' if exam_mode else 'Normal mode'}

{content_context}

User Question: {user_input}

Provide a clear, well-structured answer. Use formatting (bold, lists) where appropriate."""

                response = ask_ai_engine(prompt)
                messages.append({"role": "assistant", "content": response})
            
            st.session_state["chat_history"][user] = messages
            
            # Clear attachments after sending
            st.session_state["attached_files"] = []
            st.session_state["attached_url"] = ""
            
            # Increment counter to clear input field
            st.session_state["msg_count"] = st.session_state.get("msg_count", 0) + 1
            
            st.rerun()

# === STRICT EXAMINER MODE ===
elif st.session_state["tool_mode"] == "examiner":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                border-radius: 16px; padding: 24px; margin-bottom: 24px;">
        <h3 style="margin: 0 0 8px 0; color: #92400e;">📝 Strict Examiner Mode</h3>
        <p style="margin: 0; color: #b45309;">
            Paste your exam question and answer. I'll grade it strictly like a JNTUH external examiner!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_q, col_m = st.columns([3, 1])
    with col_q:
        q_text = st.text_input("📝 Exam Question", placeholder="e.g., Explain Kirchhoff's Current Law with example")
    with col_m:
        max_marks = st.number_input("Max Marks", min_value=2, max_value=15, value=5)
        
    ans_text = st.text_area("✍️ Your Answer", height=180, placeholder="Write your answer here...")
    
    if st.button("👨‍🏫 Grade My Answer", type="primary", use_container_width=True):
        if q_text and ans_text:
            with st.spinner("🔍 Analyzing your answer like a strict examiner..."):
                grading_prompt = f"""
Act as a STRICT JNTUH External Examiner for {current_subject}.

QUESTION: {q_text}
STUDENT ANSWER: {ans_text}
MAX MARKS: {max_marks}

Grade strictly! Provide in this format:
1. **Score**: X/{max_marks}
2. **Verdict**: PASS/FAIL
3. **Mistakes**: Key points missed
4. **What was good**: Correct points
5. **Model Answer**: Perfect answer for full marks
6. **Suggestion**: How to improve

Be harsh but fair."""
                result = ask_ai_engine(grading_prompt)
                st.markdown("---")
                st.markdown(result)
        else:
            st.warning("Please enter both question and your answer!")

# === DIAGRAM GENERATOR MODE ===
elif st.session_state["tool_mode"] == "diagram":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                border-radius: 16px; padding: 24px; margin-bottom: 24px;">
        <h3 style="margin: 0 0 8px 0; color: #1e40af;">🎨 Diagram Generator</h3>
        <p style="margin: 0; color: #1e3a8a;">
            Generate flowcharts, block diagrams, mind maps, and more!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col_topic1, col_topic2 = st.columns([3, 1])
    with col_topic1:
        topic = st.text_input("📌 What diagram do you need?", placeholder="e.g., Flowchart of Binary Search Algorithm")
    with col_topic2:
        dia_type = st.selectbox("Type", ["Flowchart", "Block Diagram", "Mind Map", "UML Class", "Network"])
    
    if st.button("✨ Generate Diagram", type="primary", use_container_width=True):
        with st.spinner("🎨 Drawing diagram..."):
            dia_prompt = f"""
Generate a valid Graphviz DOT code for a {dia_type} about: "{topic}" related to {current_subject}.

RULES:
- Output ONLY the code inside ```dot ... ``` block
- NO explanations, just code
- Use professional styling (rounded rectangles, clean edges)
- For flowcharts use: box, diamond, oval, arrow
- Rank direction: TB or LR
- Add colors and gradient styles
"""
            
            res = ask_ai_engine(dia_prompt)
            
            try:
                if "```dot" in res:
                    code = res.split("```dot")[1].split("```")[0].strip()
                    st.graphviz_chart(code)
                elif "```graphviz" in res:
                    code = res.split("```graphviz")[1].split("```")[0].strip()
                    st.graphviz_chart(code)
                else:
                    st.warning("AI couldn't generate diagram. Here's the response:")
                    st.code(res)
            except Exception as e:
                st.error(f"Could not render: {e}")
                st.code(res if 'res' in locals() else "No code")

# === CONCEPT EXPLAINER MODE ===
elif st.session_state["tool_mode"] == "explainer":
    st.markdown("""
    <div style="background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                border-radius: 16px; padding: 24px; margin-bottom: 24px;">
        <h3 style="margin: 0 0 8px 0; color: #065f46;">📖 Concept Explainer</h3>
        <p style="margin: 0; color: #047857;">
            Get detailed explanations with YouTube videos & Instagram Reels!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    concept = st.text_input("🎯 What concept do you want to learn?", 
                           placeholder="e.g., Linked Lists in Data Structures")
    
    if st.button("📖 Explain & Find Videos", type="primary", use_container_width=True):
        with st.spinner("📚 Creating your lesson..."):
            explain_prompt = f"""
Explain: {concept} for {current_subject} (JNTUH R24).

Provide:
1. **Definition**: Clear definition
2. **Key Points**: 5-7 important points  
3. **Real-life Example**: Practical use
4. **Diagram**: How to draw it
5. **Exam Questions**: 2-3 important questions

Be detailed and exam-focused!"""
            result = ask_ai_engine(explain_prompt)
            
            st.markdown("---")
            st.markdown("### 📖 Detailed Explanation")
            st.markdown(result)
            
            st.markdown("---")
            
            col_yt, col_ig = st.columns(2)
            
            with col_yt:
                st.markdown("### 🎬 YouTube Videos")
                yt_terms = [
                    f"{concept} {current_subject} JNTUH",
                    f"{concept} tutorial beginners",
                    f"{concept} exam prep"
                ]
                for term in yt_terms:
                    yt_url = f"https://youtube.com/results?search_query={term.replace(' ', '+')}"
                    st.markdown(f"📺 [{term}]({yt_url})")
            
            with col_ig:
                st.markdown("### 🎬 Instagram Reels")
                ig_terms = [f"{concept} explained", f"{concept} short", f"{concept} tricks"]
                for term in ig_terms:
                    ig_url = f"https://instagram.com/explore/tags/{term.replace(' ', '')}/"
                    st.markdown(f"🎬 [{term}]({ig_url})")

# Clear chat button
st.markdown("<br><br>", unsafe_allow_html=True)
if st.button("🗑️ Clear Chat History", use_container_width=False):
    st.session_state["chat_history"][user] = []
    st.session_state["last_msg"] = ""
    st.rerun()
