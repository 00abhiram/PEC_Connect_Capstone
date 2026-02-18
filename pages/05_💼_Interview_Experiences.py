import streamlit as st
import sqlite3

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Interview Experiences | PEC",
    page_icon="💼",
    layout="wide"
)

st.title("💼 PEC Campus Interview Hub")
st.caption("Learn from real placement experiences shared by seniors.")
st.markdown("---")

# ---------------------------------------------------
# Dropdown Data
# ---------------------------------------------------
companies_list = [
    "TCS", "Infosys", "Wipro", "Accenture",
    "Cognizant", "Capgemini", "Tech Mahindra",
    "HCL", "Deloitte", "Amazon", "Microsoft",
    "Other"
]

roles_list = [
    "Software Developer",
    "Data Analyst",
    "System Engineer",
    "Graduate Trainee",
    "Intern",
    "Other"
]

question_topics = [
    "Data Structures",
    "Algorithms",
    "DBMS",
    "Operating Systems",
    "Computer Networks",
    "OOPS",
    "Aptitude",
    "HR Questions",
    "Technical Interview",
    "Managerial Round",
    "Other"
]

# ---------------------------------------------------
# Database Connection
# ---------------------------------------------------
conn = sqlite3.connect("pec_data.db")
c = conn.cursor()

# ---------------------------------------------------
# Share Experience Section
# ---------------------------------------------------
st.subheader("🚀 Share Your Interview Experience")

with st.form("interview_form", clear_on_submit=True):

    col1, col2 = st.columns(2)

    with col1:
        student_name = st.text_input("👤 Your Name (Optional)")

        # Company Selection
        selected_company = st.selectbox("🏢 Company Name", companies_list)

        if selected_company == "Other":
            custom_company = st.text_input("✏️ Enter Company Name")
            company_name = custom_company
        else:
            company_name = selected_company

        # Role Selection
        selected_role = st.selectbox("💼 Role Applied For", roles_list)

        if selected_role == "Other":
            custom_role = st.text_input("✏️ Enter Role")
            role = custom_role
        else:
            role = selected_role

    with col2:
        # Topics Selection
        selected_topics = st.multiselect(
            "📚 Questions Related To",
            question_topics
        )

        if "Other" in selected_topics:
            custom_topic = st.text_input("✏️ Enter Other Topic")
            if custom_topic:
                selected_topics = [t for t in selected_topics if t != "Other"]
                selected_topics.append(custom_topic)

        difficulty = st.slider(
            "⭐ Difficulty Level (1 = Easy, 5 = Hard)",
            1, 5, 3
        )

    interview_rounds = st.text_area("📝 Interview Rounds (Explain briefly)")
    experience = st.text_area("📖 Overall Experience")
    tips = st.text_area("🎯 Tips for Juniors")

    submit = st.form_submit_button("🚀 Submit Experience")

# ---------------------------------------------------
# After Submission
# ---------------------------------------------------
if submit:
    if company_name and role and experience:

        if not student_name:
            student_name = "Anonymous"

        topics_string = ", ".join(selected_topics)

        additional_info = f"Tips: {tips} | Difficulty: {difficulty}/5"

        c.execute("""
            INSERT INTO interview_experiences
            (student_name, company_name, role,
             interview_rounds, questions_asked,
             experience, tips)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            student_name,
            company_name,
            role,
            interview_rounds,
            topics_string,
            experience,
            additional_info
        ))

        conn.commit()

        st.success("✅ Experience Submitted Successfully!")
        st.toast("Your contribution will help many juniors! 🚀")
        st.balloons()

    else:
        st.error("⚠️ Please fill required fields (Company, Role, Experience).")

st.markdown("---")

# ---------------------------------------------------
# Display Experiences
# ---------------------------------------------------
st.subheader("📚 Shared Interview Experiences")

c.execute("SELECT * FROM interview_experiences ORDER BY posted_on DESC")
experiences = c.fetchall()

if experiences:
    for exp in experiences:
        with st.container():
            st.markdown(f"### 🏢 {exp[2]} — {exp[3]}")
            st.write(f"👤 **Student:** {exp[1]}")
            st.write(f"📝 **Rounds:** {exp[4]}")
            st.write(f"📚 **Topics Covered:** {exp[5]}")
            st.write(f"📖 **Experience:** {exp[6]}")
            st.write(f"🎯 **Additional Info:** {exp[7]}")
            st.markdown("---")
else:
    st.info("No interview experiences shared yet. Be the first to contribute! 🚀")

conn.close()
