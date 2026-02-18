import streamlit as st
import re

st.set_page_config(
    page_title="Career Scam Analyzer",
    page_icon="🛡",
    layout="wide"
)

# Navigation helper
if st.button("⬅ Back to Dashboard"):
    st.switch_page("app.py")

# ===== HEADER =====
st.markdown("""
<div style='background: linear-gradient(90deg,#141E30,#243B55);
            padding:25px; border-radius:18px; color:white;
            text-align:center; margin-bottom:25px;
            box-shadow: 0 6px 14px rgba(0,0,0,0.25);'>
    <h1 style='font-size:38px; font-weight:900; margin-bottom:8px;'>
        🛡 CAREER SCAM ANALYZER
    </h1>
    <p style='font-size:17px; opacity:0.95;'>
        🚨 AI-Powered Job & Internship Fraud Detection System
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📩 Paste Job Offer / Internship Message Below")
job_text = st.text_area("Enter job/internship message", height=220)

if st.button("🔍 Analyze Offer", use_container_width=True):
    if job_text.strip() == "":
        st.warning("⚠ Please paste a job or internship message first.")
    else:
        suspicious_keywords = {
            "registration fee": 20, "processing fee": 20, "send money": 20,
            "security deposit": 20, "urgent hiring": 10, "limited seats": 10,
            "guaranteed job": 20, "no interview": 15, "whatsapp only": 15,
            "telegram": 15, "upi": 20, "pay immediately": 20
        }

        risk_score = 0
        detected_words = []
        text_lower = job_text.lower()

        for word, score in suspicious_keywords.items():
            if word in text_lower:
                risk_score += score
                detected_words.append(word)

        if re.search(r"\b@gmail\.com\b|\b@yahoo\.com\b", text_lower):
            risk_score += 15
            detected_words.append("Free email domain used (@gmail/@yahoo)")

        if re.search(r"\b\d{10}\b", text_lower):
            risk_score += 10
            detected_words.append("Phone number provided in text")

        scam_probability = min(risk_score, 100)

        st.divider()
        st.markdown("## 📊 Scam Risk Level")
        st.progress(scam_probability / 100)
        st.markdown(f"### 🔢 Scam Probability: **{scam_probability}%**")

        if scam_probability >= 70:
            st.error("🔴 HIGH RISK – Very Likely Scam")
        elif scam_probability >= 40:
            st.warning("🟡 MODERATE RISK – Suspicious Offer")
        else:
            st.success("🟢 LOW RISK – Appears Safer (Verify Anyway)")

        if detected_words:
            st.markdown("### ⚠ Suspicious Indicators Detected")
            for word in detected_words:
                st.write(f"• {word}")

        st.markdown("### 🤖 AI Analysis Explanation")
        if scam_probability >= 70:
            st.write("Legitimate companies never ask for upfront payments or security deposits. This is a common fraud tactic.")
        elif scam_probability >= 40:
            st.write("Some suspicious patterns were detected. Verify the recruiter on LinkedIn before sharing personal info.")
        else:
            st.write("No strong scam indicators detected. Always check the official company website for the job listing.")