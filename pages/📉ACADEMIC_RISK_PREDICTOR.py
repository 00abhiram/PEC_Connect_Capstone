import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Academic Risk Predictor", page_icon="📉", layout="wide")

# ===== TITLE =====
# ===== TITLE =====
st.markdown("""
<div style='background: linear-gradient(90deg,#8B0000,#FF4B4B);
            padding:25px;
            border-radius:18px;
            color:white;
            text-align:center;
            margin-bottom:35px;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);'>
    <h1 style='font-size:40px; font-weight:900; margin-bottom:5px;'>
        📉 <b>ACADEMIC RISK PREDICTOR</b>
    </h1>
    <p style='font-size:18px; margin-top:10px;'>
        🎓 AI-Powered Early Warning & Performance Analysis System
    </p>
</div>
""", unsafe_allow_html=True)


# ===== INPUT SECTION =====
st.markdown("## 📋 Enter Student Details")

col1, col2 = st.columns(2)

with col1:
    attendance = st.slider("📅 Attendance (%)", 0, 100, 75)
    internal_marks = st.slider("📝 Internal Marks (%)", 0, 100, 60)

with col2:
    study_hours = st.slider("📚 Study Hours per Day", 0, 12, 4)
    backlogs = st.slider("❗ Number of Backlogs", 0, 10, 0)

# ===== PREDICTION BUTTON =====
if st.button("🔍 Predict Academic Risk", use_container_width=True):

    # Simulated Model Logic (Replace with your real model if needed)
    risk_score = 0

    if attendance < 60:
        risk_score += 25
    if internal_marks < 50:
        risk_score += 30
    if study_hours < 2:
        risk_score += 20
    if backlogs > 2:
        risk_score += 25

    risk_percentage = min(risk_score, 100)

    st.divider()

    # ===== VISUAL RISK BAR =====
    st.markdown("### 📊 Risk Level")
    st.progress(risk_percentage / 100)

    st.markdown(f"### 🔢 Risk Probability: **{risk_percentage}%**")

    # ===== RISK STATUS =====
    if risk_percentage >= 70:
        st.error("🔴 HIGH RISK – Immediate Intervention Needed")
    elif risk_percentage >= 40:
        st.warning("🟡 MODERATE RISK – Needs Attention")
    else:
        st.success("🟢 LOW RISK – Student Performing Well")

    # ===== REASONS =====
    st.markdown("### 🧠 Key Risk Factors Identified")

    if attendance < 60:
        st.write("• Low attendance affecting performance.")
    if internal_marks < 50:
        st.write("• Weak internal marks.")
    if study_hours < 2:
        st.write("• Insufficient daily study time.")
    if backlogs > 2:
        st.write("• Multiple backlogs increasing risk.")

    # ===== PERSONALIZED SUGGESTIONS =====
    st.markdown("### 🎯 Recommended Action Plan")

    if risk_percentage >= 70:
        st.write("✔ Meet academic mentor immediately.")
        st.write("✔ Join peer tutoring sessions.")
        st.write("✔ Create structured study timetable.")
        st.write("✔ Attend all remaining classes without fail.")

    elif risk_percentage >= 40:
        st.write("✔ Improve attendance consistency.")
        st.write("✔ Increase daily study hours by 1–2 hours.")
        st.write("✔ Focus on weak subjects.")

    else:
        st.write("✔ Maintain current performance.")
        st.write("✔ Keep consistent attendance and preparation.")