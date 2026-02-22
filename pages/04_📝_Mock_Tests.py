import streamlit as st
import ai_engine as ai
import re
import datetime
import random
import database as db

db.init_db()

st.markdown("""
<style>
    #MainMenu, footer { visibility: hidden !important; }
    html, body { font-family: 'Segoe UI', sans-serif; }
    
    /* Keep header visible for sidebar toggle */
    header { visibility: visible !important; }
    
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
    
    .page-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 25px 30px; border-radius: 16px; margin-bottom: 25px;
    }
    .page-title { color: white; font-size: 1.8rem; font-weight: 800; margin: 0; }
    .page-subtitle { color: rgba(255,255,255,0.85); font-size: 0.95rem; margin-top: 6px; }
    
    .config-card {
        background: white; border: 1px solid #e2e8f0;
        border-radius: 16px; padding: 25px; margin-bottom: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    }
    .config-title {
        font-size: 1.2rem; font-weight: 700; color: #1e293b;
        margin-bottom: 20px; display: flex; align-items: center; gap: 10px;
    }
    
    .question-card {
        background: white; border: 1px solid #e2e8f0;
        border-radius: 16px; padding: 25px; margin-bottom: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    }
    .question-number {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white; padding: 8px 16px; border-radius: 20px;
        font-size: 0.85rem; font-weight: 700; display: inline-block; margin-bottom: 15px;
    }
    .question-text {
        font-size: 1.05rem; color: #1e293b; line-height: 1.6;
        margin-bottom: 20px; font-weight: 500;
    }
    
    .option-btn {
        display: block; width: 100%; padding: 15px 20px;
        margin-bottom: 12px; border: 2px solid #e2e8f0;
        border-radius: 12px; background: #f8fafc;
        text-align: left; font-size: 0.95rem; color: #334155;
        cursor: pointer; transition: all 0.2s;
    }
    .option-btn:hover {
        border-color: #667eea; background: #f1f5f9;
    }
    .option-selected {
        border-color: #667eea; background: #e0e7ff;
        color: #4338ca; font-weight: 600;
    }
    .option-correct {
        border-color: #10b981; background: #d1fae5;
        color: #065f46; font-weight: 600;
    }
    .option-wrong {
        border-color: #ef4444; background: #fee2e2;
        color: #991b1b; font-weight: 600;
    }
    
    .result-box {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white; padding: 30px; border-radius: 16px;
        text-align: center; margin-bottom: 25px;
    }
    .result-score { font-size: 3rem; font-weight: 800; }
    .result-label { font-size: 1.1rem; opacity: 0.9; }
    
    .solution-card {
        background: #f8fafc; border-left: 4px solid #10b981;
        padding: 20px; border-radius: 0 12px 12px 0; margin-top: 15px;
    }
    .solution-title {
        color: #10b981; font-weight: 700; margin-bottom: 10px;
    }
    
    .year-chip {
        background: linear-gradient(135deg, #667eea20, #764ba220);
        color: #475569; padding: 6px 14px; border-radius: 20px;
        font-size: 0.8rem; font-weight: 600; margin-right: 8px;
    }
    
    .stat-card {
        background: white; border: 1px solid #e2e8f0;
        border-radius: 12px; padding: 20px; text-align: center;
    }
    .stat-number { font-size: 1.8rem; font-weight: 800; color: #667eea; }
    .stat-label { font-size: 0.85rem; color: #64748b; }
    
    .difficulty-easy { background: #d1fae5; color: #059669; }
    .difficulty-medium { background: #fef3c7; color: #d97706; }
    .difficulty-hard { background: #fee2e2; color: #dc2626; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1 class="page-title">📝 Mock Tests</h1>
    <p class="page-subtitle">Practice with exam-like conditions and track your progress</p>
</div>
""", unsafe_allow_html=True)

SUBJECTS_BY_YEAR = {
    "1st Year": ["M1 - Matrices & Calculus", "M2 - Differential Equations & Vector Calculus", "Engineering Chemistry", "Applied Physics", "Programming for Problem Solving (C)", "Python Programming", "Basic Electrical Engineering", "Engineering Drawing", "Engineering Workshop", "IT Workshop", "English - Communication Skills", "Environmental Science"],
    "2nd Year - CSE": ["Discrete Mathematics", "Data Structures", "Digital Logic Design", "Computer Organization & Architecture", "Object Oriented Programming (Java)", "Operating Systems", "Database Management Systems", "Software Engineering", "Probability & Statistics", "Computer Graphics"],
    "2nd Year - CSE-AIML": ["Discrete Mathematics", "Data Structures", "Digital Logic Design", "Computer Organization & Architecture", "Object Oriented Programming (Python)", "Operating Systems", "Database Management Systems", "Probability & Statistics", "Linear Algebra", "AI Fundamentals"],
    "2nd Year - ECE": ["Electronic Devices & Circuits", "Network Theory", "Signals & Systems", "Analog Electronics", "Digital Electronics", "Electromagnetic Waves", "Microprocessors & Microcontrollers", "Control Systems"],
    "2nd Year - EEE": ["Electrical Circuit Analysis", "Electrical Machines - I", "Power Systems - I", "Control Systems", "Power Electronics", "Measurements & Instrumentation"],
    "2nd Year - Mechanical": ["Engineering Mechanics", "Strength of Materials", "Fluid Mechanics", "Thermodynamics", "Manufacturing Processes", "Kinematics of Machinery"],
    "2nd Year - Civil": ["Building Materials & Construction", "Surveying", "Structural Analysis - I", "Concrete Technology", "Hydraulics & Hydraulic Machines"],
    "3rd Year - CSE": ["Algorithms", "Compiler Design", "Computer Networks", "Artificial Intelligence", "Machine Learning", "Data Science", "Cloud Computing", "Web Technologies", "DevOps"],
    "3rd Year - CSE-AIML": ["Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision", "Data Science", "AI Algorithms", "Neural Networks", "Reinforcement Learning", "Cloud Computing", "DevOps"],
    "3rd Year - ECE": ["Communication Theory", "Digital Signal Processing", "VLSI Design", "Microwave Engineering", "Antenna & Wave Propagation", "Embedded Systems"],
    "3rd Year - EEE": ["Power Systems - II", "Power System Analysis", "Power Electronics", "Renewable Energy Sources", "Electrical Drives"],
    "3rd Year - Mechanical": ["Thermal Engineering", "Heat Transfer", "Design of Machine Elements", "CAD/CAM", "Industrial Engineering"],
    "3rd Year - Civil": ["Structural Analysis - II", "RCC & Steel Structures", "Geotechnical Engineering", "Water Resources Engineering", "Transportation Engineering"],
    "4th Year - CSE": ["Deep Learning", "Big Data Analytics", "Cybersecurity", "Internet of Things (IoT)", "Blockchain Technology"],
    "4th Year - CSE-AIML": ["Advanced Deep Learning", "Computer Vision", "Reinforcement Learning", "AI Ethics", "Edge AI", "Federated Learning", "Generative AI", "AI in Healthcare"],
    "4th Year - ECE": ["Wireless Communications", "Optical Communications", "Image Processing", "Neural Networks & Fuzzy Logic"],
    "4th Year - EEE": ["Power System Protection", "Smart Grid", "Renewable Energy Systems", "Electric Vehicles"],
    "4th Year - Mechanical": ["Refrigeration & Air Conditioning", "Automobile Engineering", "Robotics & Automation", "Finite Element Analysis"],
    "4th Year - Civil": ["Prestressed Concrete", "Bridge Engineering", "Environmental Engineering", "Construction Management"],
    "Labs": ["C Programming Lab", "Python Lab", "Data Structures Lab", "DBMS Lab", "OS Lab", "AI/ML Lab", "Java Programming Lab"],
    "Other": ["GATE Preparation", "Interview Preparation", "Aptitude & Reasoning", "Competitive Coding"]
}

ALL_SUBJECTS = []
for year_subjects in SUBJECTS_BY_YEAR.values():
    ALL_SUBJECTS.extend(year_subjects)
ALL_SUBJECTS = sorted(ALL_SUBJECTS)

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = []
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

def parse_quiz(text):
    questions = []
    raw_qs = text.split('### Q')[1:]
    for q_raw in raw_qs:
        try:
            lines = q_raw.strip().split('\n')
            q_text = lines[0].strip()
            if q_text and q_text[0].isdigit(): 
                parts = q_text.split('.', 1)
                if len(parts) > 1: 
                    q_text = parts[1].strip()
            
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
                    if clean_ans: 
                        correct = clean_ans.split(" ")[0].upper().strip()
                if "**Suggested Answer:**" in line: 
                    explanation = line.split(":", 1)[1].strip()
            
            if len(options) >= 2:
                questions.append({"q": q_text, "opts": options[:4], "ans": correct, "expl": explanation})
        except: 
            continue
    return questions

with st.container(border=True):
    st.markdown('<div class="config-title">⚙️ Exam Configuration</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        exam_year = st.selectbox("📚 Year", list(SUBJECTS_BY_YEAR.keys()))
    with c2:
        subject = st.selectbox("📖 Subject", SUBJECTS_BY_YEAR[exam_year])
    
    c3, c4 = st.columns(2)
    with c3:
        difficulty = st.selectbox("📊 Difficulty", ["Easy", "Medium", "Hard"])
    with c4:
        exam_date = st.date_input("📅 Exam Date", min_value=datetime.date.today())

    days_left = (exam_date - datetime.date.today()).days
    
    if days_left == 0:
        st.error("🚨 EXAM IS TODAY! All the best!")
    elif days_left < 7:
        st.warning(f"🔥 Only {days_left} days left! Stay focused!")
    else:
        st.success(f"📅 {days_left} days remaining - Keep preparing!")

st.markdown("---")

c_gen, c_clear = st.columns([4, 1])
with c_gen:
    difficulty_color = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}[difficulty]
    if st.button(f"{difficulty_color} Generate Questions", type="primary", use_container_width=True):
        with st.spinner(f"🤖 Generating {difficulty} level questions for {subject}..."):
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

with c_clear:
    if st.button("🗑️ Clear", use_container_width=True):
        st.session_state.quiz_data = []
        st.session_state.user_answers = {}
        st.session_state.submitted = False
        st.rerun()

if st.session_state.quiz_data:
    st.markdown("---")
    
    if not st.session_state.submitted:
        st.markdown("### 📋 Answer the Questions")
        
        for i, q in enumerate(st.session_state.quiz_data):
            with st.container(border=True):
                st.markdown(f'<div class="question-number">Question {i+1} of {len(st.session_state.quiz_data)}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="question-text">{q["q"]}</div>', unsafe_allow_html=True)
                
                options = [opt.split(') ')[1] if ') ' in opt else opt for opt in q['opts']]
                option_labels = [opt.split(')')[0] for opt in q['opts']]
                
                selected_idx = None
                for idx, opt in enumerate(q['opts']):
                    if st.session_state.user_answers.get(i) == opt:
                        selected_idx = idx
                        break
                
                selected = st.radio(
                    "Select your answer:",
                    q['opts'],
                    key=f"q_{i}",
                    index=selected_idx
                )
                if selected:
                    st.session_state.user_answers[i] = selected
        
        st.markdown("---")
        if st.button("✅ Submit Answers", type="primary", use_container_width=True):
            st.session_state.submitted = True
            st.rerun()
    
    else:
        score = 0
        for i, q in enumerate(st.session_state.quiz_data):
            user_val = st.session_state.user_answers.get(i, "")
            user_ans = user_val.split(')')[0].strip() if user_val else ""
            if user_ans == q['ans']:
                score += 1
        
        percentage = (score / len(st.session_state.quiz_data)) * 100
        
        if "user" in st.session_state:
            db.save_test_result(
                st.session_state.user,
                subject,
                score,
                len(st.session_state.quiz_data),
                difficulty
            )
        
        if percentage >= 70:
            result_msg = "🎉 Excellent! You Passed!"
            result_color = "#10b981"
        elif percentage >= 50:
            result_msg = "👍 Good Effort! Keep Practicing"
            result_color = "#f59e0b"
        else:
            result_msg = "📚 Need More Practice"
            result_color = "#ef4444"
        
        st.markdown(f"""
        <div class="result-box">
            <div class="result-score">{score} / {len(st.session_state.quiz_data)}</div>
            <div class="result-label">{result_msg}</div>
            <div style="margin-top: 10px; opacity: 0.8;">Score: {percentage:.0f}%</div>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{score}</div><div class="stat-label">Correct</div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{len(st.session_state.quiz_data) - score}</div><div class="stat-label">Wrong</div></div>', unsafe_allow_html=True)
        with c3:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{percentage:.0f}%</div><div class="stat-label">Score</div></div>', unsafe_allow_html=True)
        
        st.markdown("### 📝 Detailed Solutions")
        
        for i, q in enumerate(st.session_state.quiz_data):
            user_val = st.session_state.user_answers.get(i, "")
            user_ans = user_val.split(')')[0].strip() if user_val else ""
            is_correct = user_ans == q['ans']
            
            with st.expander(f"Q{i+1}: {q['q'][:60]}... {'✅' if is_correct else '❌'}"):
                st.markdown("**Your Answer:**")
                if user_val:
                    st.markdown(f"📍 {user_val}")
                else:
                    st.markdown("⚪ Not attempted")
                
                st.markdown("**Correct Answer:**")
                correct_opt = [opt for opt in q['opts'] if opt.startswith(q['ans'] + ')')][0]
                st.markdown(f"✅ {correct_opt}")
                
                st.markdown(f"""
                <div class="solution-card">
                    <div class="solution-title">📝 Explanation</div>
                    {q['expl'] if q['expl'] else "No explanation available."}
                </div>
                """, unsafe_allow_html=True)
        
        paper_content = f"""
===========================================================
         PALLAVI ENGINEERING COLLEGE - PEC CONNECT
              MOCK TEST - R24 PATTERN
===========================================================
Subject: {subject}
Difficulty: {difficulty}
Date: {datetime.date.today()}
Score: {score}/{len(st.session_state.quiz_data)} ({percentage:.0f}%)

===========================================================
"""
        for i, q in enumerate(st.session_state.quiz_data):
            paper_content += f"\nQ{i+1}: {q['q']}\n"
            for opt in q['opts']:
                paper_content += f"  {opt}\n"
            paper_content += f"Answer: {q['ans']}\n"
            paper_content += f"Explanation: {q['expl']}\n"
            paper_content += "-" * 50 + "\n"

        st.download_button(
            label="📥 Download Question Paper & Solutions",
            data=paper_content,
            file_name=f"{subject.replace(' ', '_')}_MockTest.txt",
            mime="text/plain",
            use_container_width=True
        )

else:
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px; background: #f8fafc; border-radius: 16px; border: 2px dashed #cbd5e1;">
        <h2 style="color: #64748b; margin-bottom: 10px;">📚 Ready to Practice?</h2>
        <p style="color: #94a3b8;">Configure your exam above and generate questions to start practicing</p>
    </div>
    """, unsafe_allow_html=True)
