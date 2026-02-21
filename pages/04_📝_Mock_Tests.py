import streamlit as st
import ai_engine as ai
import re
import datetime

st.set_page_config(page_title="Exam Simulator", page_icon="📝", layout="wide")

st.markdown("""
<style>
    /* 1. Exam Header */
    .exam-header {
        background: linear-gradient(90deg, #1e293b, #0f172a);
        color: white; padding: 20px; border-radius: 12px;
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* 2. Question Card */
    .q-card {
        background: white; padding: 25px; border-radius: 10px;
        border: 1px solid #e2e8f0; border-left: 5px solid #6366f1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .q-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.05);
    }
    .q-title { font-weight: 700; font-size: 1.1rem; color: #1e293b; }
    
    /* 3. Detailed Solution Box */
    .solution-box {
        background: #f8fafc; border: 1px dashed #cbd5e1;
        padding: 15px; border-radius: 8px; margin-top: 15px;
        font-size: 0.95rem; color: #334155;
    }
</style>
""", unsafe_allow_html=True)

if "quiz_data" not in st.session_state: st.session_state.quiz_data = []
if "user_answers" not in st.session_state: st.session_state.user_answers = {}
if "submitted" not in st.session_state: st.session_state.submitted = False

def parse_quiz(text):
    questions = []
    raw_qs = text.split('### Q')[1:]
    for q_raw in raw_qs:
        try:
            lines = q_raw.strip().split('\n')
            q_text = lines[0].strip()
            if q_text[0].isdigit(): 
                parts = q_text.split('.', 1)
                if len(parts) > 1: q_text = parts[1].strip()
            
            options = []
            correct = "A" 
            explanation = ""
            
            for line in lines:
                line = line.strip()
                if line.startswith(('A)', 'B)', 'C)', 'D)')): 
                    options.append(line)
                if "**Correct Answer:**" in line: 
                    raw_ans = line.split(":", 1)[1]
                    clean_ans = raw_ans.replace("*", "").replace(")", "").strip()
                    if clean_ans: correct = clean_ans.split(" ")[0].upper().strip()
                if "**Suggested Answer:**" in line: 
                    explanation = line.split(":", 1)[1].strip()
            
            if len(options) >= 4:
                questions.append({"q": q_text, "opts": options[:4], "ans": correct, "expl": explanation})
        except: continue
    return questions

with st.sidebar:
    st.subheader("⚙️ Exam Configuration")
    
    subject = st.selectbox(
        "Select Subject", 
        [
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
            "Discrete Mathematics",
            "Data Structures"
        ]
    )
    
    difficulty = st.select_slider("Difficulty Level", options=["Easy", "Medium", "Hard"], value="Medium")
    st.caption(f"Regulation: **R24 / PR24**")
    
    st.divider()
    
    st.subheader("⏳ Exam Countdown")
    days = st.slider("Days remaining for Exam?", 0, 30, 3)
    
    if days == 0:
        st.error("🚨 EXAM IS TODAY! Good Luck!")
    elif days < 3:
        st.warning(f"🔥 Urgent: Only {days} days left!")
    else:
        st.success(f"📅 {days} Days to prepare.")

st.markdown(f"""
<div class="exam-header">
    <div>
        <h2 style="margin:0; color:white;">PEC Exam Portal</h2>
        <small>Artificial Intelligence Powered Assessment (R24 Pattern)</small>
    </div>
    <div style="text-align:right;">
        <div style="font-size:1.5rem; font-weight:800;">{subject.split('(')[0]}</div>
        <div style="opacity:0.8;">{difficulty} Mode</div>
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("⚡ Generate New Question Paper", type="primary", use_container_width=True):
    with st.spinner(f"🤖 Analyzing {subject} syllabus (R24) & drafting questions..."):
        try:
            raw_text = ai.generate_mock_test(f"{subject} (JNTUH R24 Regulation)", difficulty)
            
            if raw_text:
                st.session_state.quiz_data = parse_quiz(raw_text)
                st.session_state.user_answers = {}
                st.session_state.submitted = False
                st.rerun()
            else:
                st.error("AI returned empty response. Please try again.")
        except Exception as e:
            st.error(f"Error: {e}")

if st.session_state.quiz_data:
    with st.form("exam_form"):
        for i, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"""
            <div class="q-card">
                <div class="q-title">Q{i+1}. {q['q']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.session_state.user_answers[i] = st.radio(
                "Choose your answer:", q['opts'], key=f"q{i}", index=None, disabled=st.session_state.submitted
            )
            
            if st.session_state.submitted:
                user_val = st.session_state.user_answers.get(i)
                user_ans = user_val.split(')')[0].strip() if user_val else "None"
                
                if user_ans == q['ans']:
                    st.success("✅ Correct Answer")
                else:
                    st.error(f"❌ Wrong. Correct Option: {q['ans']}")
                
                st.markdown(f"""
                <div class="solution-box">
                    <b>📝 Suggested Answer (Detailed Step-by-Step):</b><br>
                    {q['expl']}
                </div>
                """, unsafe_allow_html=True)

        if not st.session_state.submitted:
            if st.form_submit_button("✅ Submit Final Answers", type="primary"):
                st.session_state.submitted = True
                st.rerun()
        else:
            st.form_submit_button("Result Generated Below 👇", disabled=True)

    if st.session_state.submitted:
        score = 0
        for i, q in enumerate(st.session_state.quiz_data):
            user_val = st.session_state.user_answers.get(i, "")
            user_letter = user_val.split(')')[0].strip() if user_val else ""
            if user_letter == q['ans']:
                score += 1
        
        st.divider()
        c1, c2 = st.columns([1, 3])
        with c1:
            st.metric("Final Score", f"{score} / {len(st.session_state.quiz_data)}")
        with c2:
            if score >= 3:
                st.success("🎉 You passed! Download the paper to revise.")
            else:
                st.error("⚠️ Needs Improvement. Download the solutions.")

        paper_content = f"""
============================================================
              PALLAVI ENGINEERING COLLEGE
           AI-GENERATED EXAM PAPER (R24 - {difficulty})
============================================================
Subject: {subject}
Date: {datetime.date.today()}
Score Obtained: {score}/{len(st.session_state.quiz_data)}

"""
        for i, q in enumerate(st.session_state.quiz_data):
            paper_content += f"\nQ{i+1}: {q['q']}\n"
            paper_content += "-" * 50 + "\n"
            paper_content += f"Correct Option: {q['ans']}\n"
            paper_content += f"SUGGESTED SOLUTION:\n{q['expl']}\n"
            paper_content += "=" * 60 + "\n"

        st.download_button(
            label="📥 Download Question Paper & Solutions",
            data=paper_content,
            file_name=f"{subject.replace(' ', '_')}_Mock_Test.txt",
            mime="text/plain",
            use_container_width=True
        )

elif not st.session_state.quiz_data:
    st.info("👈 Select a subject from the sidebar and click 'Generate' to start.")