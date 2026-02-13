import streamlit as st
import google.generativeai as genai
import json
import re # We use this to clean the messy AI output

# --- PAGE SETUP ---
st.set_page_config(page_title="Mock Tests | PEC", page_icon="📝", layout="wide")

st.title("📝 PEC AI Exam Simulator")
st.caption("Generate unlimited practice questions for R18/R22 subjects instantly.")

# --- CONNECT TO GEMINI (With Model Hunter) ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        st.error("⚠️ API Key missing! Check .streamlit/secrets.toml")
        st.stop()

    def get_working_model():
        candidates = [
            "gemini-2.0-flash-lite-preview-02-05", 
            "gemini-2.0-flash",                     
            "gemini-2.5-flash",                     
            "gemini-1.5-flash-latest",
            "gemini-1.5-flash"
        ]
        for model_name in candidates:
            try:
                full_name = f"models/{model_name}" if "models/" not in model_name else model_name
                test_model = genai.GenerativeModel(model_name)
                test_model.generate_content("test")
                return test_model 
            except Exception:
                continue
        return None

    if "quiz_model" not in st.session_state:
        with st.spinner("🔄 Syncing AI for Mock Tests..."):
            st.session_state.quiz_model = get_working_model()

    model = st.session_state.quiz_model

    if not model:
        st.error("❌ Could not connect to AI. Please check API Key.")
        st.stop()

except Exception as e:
    st.error(f"⚠️ Connection Error: {e}")
    st.stop()

# --- SESSION STATE ---
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "score" not in st.session_state:
    st.session_state.score = None

# --- SIDEBAR: TEST CONFIG ---
with st.sidebar:
    st.header("⚙️ Configure Test")
    
    SUBJECTS = [
        "M1 (Matrices)", "BEE (Electrical)", "Chemistry", "Python Programming", 
        "Data Structures", "Java Programming", "DBMS (Database)", 
        "Operating Systems (OS)", "Digital Logic Design (DLD)", "Computer Org (COA)",
        "AI & ML", "Cyber Security"
    ]
    
    subject = st.selectbox("Select Subject", SUBJECTS)
    difficulty = st.select_slider("Difficulty Level", options=["Easy", "Medium", "Hard"])
    
    st.divider()
    if st.button("🚀 Start New Test"):
        st.session_state.quiz_data = None
        st.session_state.user_answers = {}
        st.session_state.score = None
        st.rerun()

# --- MAIN LOGIC ---

# 1. GENERATE QUIZ
if st.session_state.quiz_data is None:
    st.info(f"Ready to generate a **{difficulty}** level test for **{subject}**.")
    
    if st.button("⚡ Generate Questions"):
        with st.spinner(f"🤖 AI is writing unique {subject} questions..."):
            try:
                # STRICT Prompt to prevent bad characters
                prompt = f"""
                Create a customized multiple-choice quiz for {subject} (JNTUH B.Tech Level: {difficulty}).
                Generate exactly 5 questions.
                
                IMPORTANT RULES:
                1. Output ONLY a valid JSON Array.
                2. Do NOT use LaTeX or backslashes (e.g., avoid \lambda, \frac). Use plain text (e.g., 'lambda', 'fraction').
                3. Do NOT use markdown formatting like ```json.
                
                Format:
                [
                    {{
                        "question": "Question text?",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_answer": "Option B",
                        "explanation": "Brief reason why."
                    }}
                ]
                """
                response = model.generate_content(prompt)
                text_data = response.text.strip()
                
                # Cleanup 1: Remove Markdown wrappers
                if "```json" in text_data:
                    text_data = text_data.split("```json")[1].split("```")[0]
                elif "```" in text_data:
                    text_data = text_data.split("```")[1].split("```")[0]
                
                # Cleanup 2: Fix bad backslashes (The "Invalid Escape" Fix)
                # This replaces single backslashes \ with double \\ so JSON can read them
                text_data = text_data.replace("\\", "\\\\")

                st.session_state.quiz_data = json.loads(text_data)
                st.rerun()
                
            except Exception as e:
                st.error("⚠️ AI Error. Please click 'Start New Test' and try again.")
                st.caption(f"Details: {e}")

# 2. DISPLAY QUIZ
elif st.session_state.score is None:
    st.subheader(f"📝 Exam: {subject}")
    
    answered = len(st.session_state.user_answers)
    st.progress(answered / 5, text=f"{answered}/5 Answered")
    
    for i, q in enumerate(st.session_state.quiz_data):
        st.markdown(f"**Q{i+1}. {q['question']}**")
        
        user_choice = st.radio(
            "Select Answer:", 
            q['options'], 
            key=f"q{i}", 
            index=None
        )
        
        if user_choice:
            st.session_state.user_answers[i] = user_choice
        
        st.divider()
    
    if st.button("✅ Submit Test"):
        if len(st.session_state.user_answers) < 5:
            st.warning("Please answer all 5 questions first!")
        else:
            score = 0
            for i, q in enumerate(st.session_state.quiz_data):
                if st.session_state.user_answers.get(i) == q['correct_answer']:
                    score += 1
            st.session_state.score = score
            st.rerun()

# 3. DISPLAY RESULTS
else:
    score = st.session_state.score
    
    st.title("📊 Test Results")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Score", f"{score}/5")
    c2.metric("Percentage", f"{(score/5)*100}%")
    
    if score >= 4:
        c3.success("Result: PASS (Excellent)")
        st.balloons()
    elif score >= 2:
        c3.warning("Result: AVERAGE")
    else:
        c3.error("Result: FAIL")

    st.divider()
    
    st.subheader("📝 Question Analysis")
    for i, q in enumerate(st.session_state.quiz_data):
        user_ans = st.session_state.user_answers.get(i)
        correct_ans = q['correct_answer']
        
        with st.expander(f"Q{i+1}: {q['question']}", expanded=True):
            if user_ans == correct_ans:
                st.success(f"✅ Your Answer: {user_ans}")
            else:
                st.error(f"❌ Your Answer: {user_ans}")
                st.success(f"✅ Correct Answer: {correct_ans}")
            
            st.info(f"💡 **Explanation:** {q['explanation']}")

    if st.button("🔄 Take Another Test"):
        st.session_state.quiz_data = None
        st.session_state.user_answers = {}
        st.session_state.score = None
        st.rerun()