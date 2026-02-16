import streamlit as st
import google.generativeai as genai
from groq import Groq
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Tutor | PEC",
    page_icon="🧠",
    layout="wide"
)

# --- PROFESSIONAL UI STYLING (Gemini/ChatGPT Style) ---
st.markdown("""
<style>
    /* Main Chat Container */
    .stChatMessage {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        border: 1px solid #f1f5f9;
    }
    
    /* User Message Bubble */
    [data-testid="stChatMessageUser"] {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
    }
    
    /* AI Message Bubble */
    [data-testid="stChatMessageAssistant"] {
        background-color: #ffffff;
        border-left: 4px solid #10b981;
    }
    
    /* Sidebar Status Badges */
    .status-indicator {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .status-active { background: #dcfce7; color: #15803d; border: 1px solid #86efac; }
    .status-inactive { background: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }

    /* Titles & Headers */
    h1 { letter-spacing: -1px; font-weight: 800 !important; color: #1e293b; }
    .subtitle { color: #64748b; font-size: 1.1rem; margin-top: -15px; }
</style>
""", unsafe_allow_html=True)

# --- JNTUH R24/R22 COMPLETE SYLLABUS LIST ---
SUBJECTS = {
    "I Year (Freshman)": [
        "Matrices and Calculus (M1)", "ODE & Vector Calculus (M2)", 
        "Engineering Chemistry", "Applied Physics", 
        "C Programming & Data Structures", "Python Programming", 
        "Basic Electrical Engineering (BEE)", "Computer Aided Engineering Graphics", 
        "Engineering Workshop", "English for Skill Enhancement"
    ],
    "II Year (Sophomore)": [
        "Discrete Mathematics", "Digital Electronics", 
        "Computer Organization & Architecture (COA)", "Object Oriented Programming (Java)", 
        "Database Management Systems (DBMS)", "Operating Systems (OS)", 
        "Software Engineering", "Design & Analysis of Algorithms (DAA)", 
        "Business Economics & Financial Analysis"
    ],
    "III Year (Junior)": [
        "Computer Networks", "Web Technologies", 
        "Artificial Intelligence", "Machine Learning", 
        "Formal Languages & Automata Theory", "Compiler Design", 
        "Data Analytics", "Information Security", "Cloud Computing"
    ],
    "IV Year (Senior)": [
        "Deep Learning", "Natural Language Processing (NLP)", 
        "Big Data Analytics", "Cyber Security", 
        "Internet of Things (IoT)", "Blockchain Technology", 
        "Project Management", "Entrepreneurship"
    ]
}

# --- INITIALIZE AI ENGINES ---
# 1. Google Gemini (Primary)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
        st.session_state["gemini_status"] = True
    else:
        st.session_state["gemini_status"] = False
except:
    st.session_state["gemini_status"] = False

# 2. Groq Llama-3 (Reliable Backup)
try:
    if "GROQ_API_KEY" in st.secrets:
        groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        st.session_state["groq_status"] = True
    else:
        st.session_state["groq_status"] = False
except:
    st.session_state["groq_status"] = False

# --- SMART ROUTING FUNCTION ---
def ask_ai_engine(prompt, engine_preference="Auto"):
    """
    Intelligent switching between Gemini and Groq.
    """
    # Attempt 1: Gemini
    if st.session_state["gemini_status"]:
        try:
            response = gemini_model.generate_content(prompt)
            return response.text
        except Exception:
            pass # Silently failover to Groq

    # Attempt 2: Groq (Updated to latest model)
    if st.session_state["groq_status"]:
        try:
            chat_completion = groq_client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile", # <--- UPDATED MODEL HERE
            )
            # Returning answer without the "Backup" label as requested
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"❌ System Error: Both AI engines are unreachable. ({e})"

    return "❌ API Keys not found. Please check secrets.toml."

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.title("⚙️ Neural Config")
    
    # Connection Status
    c1, c2 = st.columns(2)
    with c1:
        status = "active" if st.session_state["gemini_status"] else "inactive"
        st.markdown(f'<span class="status-indicator status-{status}">Gemini 1.5</span>', unsafe_allow_html=True)
    with c2:
        status = "active" if st.session_state["groq_status"] else "inactive"
        st.markdown(f'<span class="status-indicator status-{status}">Llama 3.3</span>', unsafe_allow_html=True)
        
    st.divider()

    # Tool Selector
    tool_mode = st.selectbox("Select AI Tool", ["💬 AI Tutor", "📝 Strict Examiner", "🎨 Diagram Generator"])
    
    st.divider()
    
    # Subject Selector
    st.markdown("**📚 Select Subject**")
    year_select = st.selectbox("Year", list(SUBJECTS.keys()), label_visibility="collapsed")
    current_subject = st.selectbox("Subject", SUBJECTS[year_select], label_visibility="collapsed")
    
    st.divider()
    
    # Exam Mode Toggle
    exam_mode = st.toggle("🔥 Panic Mode (Exam Prep)", value=False, help="Switches AI to give short, bullet-point answers suitable for exams.")
    
    # Clear Chat
    if st.button("🗑️ Reset Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- MAIN PAGE HEADER ---
st.title("🧠 PEC AI Knowledge Engine")
st.markdown(f'<div class="subtitle">Your 24/7 Personal Professor for <b>{current_subject}</b></div>', unsafe_allow_html=True)
st.divider()

# ==========================================
# MODE 1: CHAT TUTOR
# ==========================================
if tool_mode == "💬 AI Tutor":
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": f"Hi! I'm ready to help with **{current_subject}**. What topic shall we cover?"}]

    # Render Chat History
    for msg in st.session_state.messages:
        avatar = "🧑‍🎓" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input(f"Ask about {current_subject}..."):
        # 1. User Message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(prompt)

        # 2. AI Response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Analyzing..."):
                tone = "extremely concise, point-wise (Exam Style)" if exam_mode else "detailed, conceptual, with examples"
                
                full_prompt = f"""
                You are an expert Professor for JNTUH B.Tech (R24 Regulation).
                Subject: {current_subject}
                Context: {prompt}
                Tone: {tone}
                
                Instructions:
                - Explain clearly and accurately.
                - If code is required, provide clean, commented code.
                - Use formatting (bolding, lists) to make it readable.
                """
                
                response = ask_ai_engine(full_prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# ==========================================
# MODE 2: STRICT EXAMINER
# ==========================================
elif tool_mode == "📝 Strict Examiner":
    st.subheader("📝 Auto-Grader & Improver")
    st.info("Paste an exam question and your answer. I will grade it like a strict external examiner.")
    
    col_q, col_m = st.columns([3, 1])
    with col_q:
        q_text = st.text_input("Exam Question", placeholder="e.g. Define Kirchhoff's Voltage Law")
    with col_m:
        max_marks = st.number_input("Max Marks", min_value=2, max_value=15, value=5)
        
    ans_text = st.text_area("Your Answer", height=200, placeholder="Type your answer here...")
    
    if st.button("👨‍🏫 Grade My Answer", type="primary"):
        if q_text and ans_text:
            with st.spinner("Grading papers..."):
                grading_prompt = f"""
                Act as a strict JNTUH External Examiner.
                Subject: {current_subject}
                Question: {q_text}
                Student Answer: {ans_text}
                Max Marks: {max_marks}
                
                Provide:
                1. Score (X/{max_marks})
                2. Verdict (Pass/Fail)
                3. Missing Keywords (What did the student miss?)
                4. Model Answer (The perfect answer for full marks)
                """
                result = ask_ai_engine(grading_prompt)
                st.markdown(result)
        else:
            st.warning("Please provide both the question and your answer.")

# ==========================================
# MODE 3: DIAGRAM GENERATOR
# ==========================================
elif tool_mode == "🎨 Diagram Generator":
    st.subheader("🎨 Engineering Diagram Generator")
    st.caption("Generate Flowcharts, Block Diagrams, and Mind Maps instantly.")
    
    topic = st.text_input("What diagram do you need?", placeholder="e.g. Flowchart of While Loop")
    
    if st.button("✨ Generate Diagram", type="primary"):
        with st.spinner("Drawing..."):
            dia_prompt = f"""
            Generate a valid Graphviz DOT code for a diagram about: "{topic}" related to {current_subject}.
            - Output ONLY the code inside ```dot ... ``` block.
            - Do not write any explanations.
            - Use professional styling (rectangles, clean edges).
            - Rank direction: Top to Bottom (TB).
            """
            
            res = ask_ai_engine(dia_prompt)
            
            # Extract and Render Code
            try:
                if "```dot" in res:
                    code = res.split("```dot")[1].split("```")[0].strip()
                    st.graphviz_chart(code)
                elif "```graphviz" in res:
                    code = res.split("```graphviz")[1].split("```")[0].strip()
                    st.graphviz_chart(code)
                else:
                    st.error("AI could not generate a valid diagram. Please try a simpler topic.")
            except Exception as e:
                st.error(f"Rendering Error: {e}")