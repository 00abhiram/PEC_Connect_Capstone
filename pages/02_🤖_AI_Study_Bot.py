import streamlit as st
import google.generativeai as genai
import time
from google.api_core import exceptions
from PIL import Image  # <--- NEW IMPORT

# --- LOAD CUSTOM LOGO ---
# Even though this file is in "pages/", Streamlit runs from the root,
# so we can still look for "favicon.png" directly.
try:
    favicon = Image.open("favicon.png")
except FileNotFoundError:
    favicon = "🤖"  # Fallback emoji

# --- PAGE SETUP ---
st.set_page_config(
    page_title="AI Tutor | PEC",
    page_icon=favicon,  # <--- UPDATED HERE
    layout="wide"
)

# ... (Keep the rest of your code exactly the same from here down)

# --- CUSTOM CSS FOR CHAT ---
st.markdown("""
<style>
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #f1f8e9;
        border-left: 5px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 PEC AI 'Fail-to-Pass' Engine")
st.caption("Your Personal Tutor, Strict Examiner, and Diagram Artist (R24 Syllabus).")

# --- CONNECT TO GEMINI ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        # Fallback if secret not found (useful for local dev if key is pasted directly)
        # st.warning("⚠️ Using fallback API key setup...") 
        pass 

    # --- MODEL HUNTER FUNCTION ---
    def get_working_model():
        candidates = [
            "gemini-2.0-flash-lite-preview-02-05", 
            "gemini-2.0-flash",                     
            "gemini-1.5-flash",                     
            "gemini-1.5-pro",
        ]
        
        for model_name in candidates:
            try:
                test_model = genai.GenerativeModel(model_name)
                test_model.generate_content("test")
                return test_model 
            except Exception:
                continue
        return None

    if "ai_model" not in st.session_state:
        with st.spinner("🔄 Syncing with Google Gemini..."):
            st.session_state.ai_model = get_working_model()

    model = st.session_state.ai_model

    if not model:
        st.error("❌ Could not connect to Gemini. Please check your API Key or Quota.")
        st.stop()

except Exception as e:
    st.error(f"⚠️ Connection Error: {e}")
    st.stop()

# --- HELPER FUNCTION: SMART RETRY ---
def ask_ai(prompt):
    try:
        return model.generate_content(prompt).text
    except exceptions.ResourceExhausted:
        with st.spinner("⚠️ High traffic. Waiting 10s for free tier..."):
            time.sleep(10)
            try:
                return model.generate_content(prompt).text
            except:
                return "⚠️ AI is currently overloaded. Please try again in 30 seconds."
    except Exception as e:
        return f"Error: {str(e)}"

# --- SIDEBAR: CONTROLS ---
with st.sidebar:
    st.header("🧠 Select Mode")
    mode = st.radio("Choose AI Tool:", 
        ["💬 Chat Tutor", "📝 Strict Examiner (Grader)", "🎨 Diagram Generator"]
    )
    
    st.divider()
    
    st.header("⚙️ Exam Settings")
    
    # --- UPDATED JNTUH R24 SUBJECT LIST ---
    subject = st.selectbox("Current Subject", [
        "Matrices and Calculus (M1)",
        "Ordinary Differential Equations & Vector Calculus (M2)",
        "Applied Physics",
        "Engineering Chemistry",
        "C Programming & Data Structures",
        "Python Programming",
        "Computer Aided Engineering Graphics",
        "Basic Electrical Engineering (BEE)",
        "Electronic Devices and Circuits",
        "English for Skill Enhancement",
        "IT Workshop",
        "Discrete Mathematics"
    ])
    
    days_left = st.slider("Days until Exam?", 1, 30, 3)
    
    # Dynamic Goal Display
    if days_left <= 2:
        st.error(f"🔥 **PANIC MODE:** Pass {subject} in {days_left} days!")
    elif days_left <= 7:
        st.warning(f"⚠️ **Urgent:** Pass {subject} in {days_left} days.")
    else:
        st.success(f"🎯 **Goal:** Pass {subject} in {days_left} days.")

# ==========================================
# MODE 1: CHAT TUTOR
# ==========================================
if mode == "💬 Chat Tutor":
    st.subheader(f"💬 {subject} Concept Explainer")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": f"I am your {subject} Tutor. What topic is confusing you?"})

    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input(f"Ask about {subject}..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("🤖 Thinking..."):
            # Context-Aware Prompt
            urgency = "EXTREMELY SHORT and SIMPLE (Crash Course style)" if days_left < 2 else "detailed with examples"
            
            full_prompt = f"""
            Role: Expert Engineering Professor for {subject} (JNTUH R24 Regulation).
            Context: Student has {days_left} days before the exam.
            Question: '{prompt}'
            Task: Explain this concept clearly. Keep the explanation {urgency}. 
            Use real-world analogies if possible.
            """
            response_text = ask_ai(full_prompt)
            
            st.session_state.messages.append({"role": "assistant", "content": response_text})
            with st.chat_message("assistant"):
                st.markdown(response_text)

# ==========================================
# MODE 2: STRICT EXAMINER
# ==========================================
elif mode == "📝 Strict Examiner (Grader)":
    st.subheader("📝 Roast My Answer (Auto-Grader)")
    st.markdown("Paste a question and your answer. I will grade it like a **Strict JNTUH External Examiner**.")
    
    col1, col2 = st.columns(2)
    with col1:
        question = st.text_input("Exam Question", placeholder="Ex: Define Kirchhoff's Current Law")
    with col2:
        max_marks = st.slider("Max Marks", 5, 15, 5)
        
    student_answer = st.text_area("Your Answer", height=150, placeholder="Type your answer here...")
    
    if st.button("👨‍🏫 Grade My Answer"):
        if not student_answer:
            st.warning("Please write an answer first!")
        else:
            with st.spinner("🔍 Examiner is checking your paper..."):
                grading_prompt = f"""
                You are a strict engineering professor grading a JNTUH R24 exam paper. 
                Subject: {subject}
                Question: {question}
                Student Answer: {student_answer}
                Max Marks: {max_marks}
                
                Task:
                1. Give a score (e.g., 3/{max_marks}).
                2. List MISSING KEYWORDS that caused mark loss.
                3. Rewrite the "Perfect 5-Mark Answer" exactly how a topper would write it.
                """
                response_text = ask_ai(grading_prompt)
                st.markdown(response_text)

# ==========================================
# MODE 3: DIAGRAM GENERATOR
# ==========================================
elif mode == "🎨 Diagram Generator":
    st.subheader("🎨 Instant Engineering Diagrams")
    st.markdown("Can't remember the block diagram? Type the topic, and I'll draw it.")
    
    diagram_topic = st.text_input("What diagram do you need?", placeholder="Ex: Flowchart of While Loop")
    
    if st.button("✨ Generate Diagram"):
        with st.spinner("🎨 Drawing..."):
            code_prompt = f"""
            Create a simple Graphviz DOT code for a: {diagram_topic} related to {subject}.
            Only output the code inside ```dot ... ``` block. Do not add explanations.
            Make it professional and easy to read.
            """
            response_text = ask_ai(code_prompt)
            
            try:
                if "```dot" in response_text:
                    dot_code = response_text.split("```dot")[1].split("```")[0].strip()
                    st.graphviz_chart(dot_code)
                    st.success(f"Here is the diagram for {diagram_topic}.")
                else:
                    st.error("AI couldn't generate a valid diagram. Try a simpler topic.")
            except:
                st.error("Error drawing diagram. Please try again.")