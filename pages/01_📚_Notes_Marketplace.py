import streamlit as st
import sqlite3

# Connect to DB
conn = sqlite3.connect('pec_data.db')
c = conn.cursor()

st.set_page_config(page_title="Resources | PEC", page_icon="📚", layout="wide")

st.title("📚 PEC Resource Center")
st.caption("One-stop shop for Notes, Labs, Syllabus, and Question Papers.")

# --- NAVIGATION TABS (Now 6 Tabs for better organization) ---
tabs = st.tabs([
    "📄 Digital Notes", 
    "🧪 Lab & Viva",
    "📜 Syllabus",
    "❓ Question Papers", 
    "🖨️ Buy Xerox", 
    "📤 Upload / Sell"
])

# Define Branches List (Added CSE-AIML)
BRANCHES = ["CSE", "CSE-AIML", "ECE", "EEE", "Civil", "Mech", "IT"]

# --- TAB 1: DIGITAL NOTES (PDFs) ---
with tabs[0]:
    st.subheader("📖 Free Digital Notes")
    col1, col2 = st.columns(2)
    search_sub = col1.text_input("Search Subject", key="pdf_search")
    filter_branch = col2.selectbox("Filter Branch", ["All"] + BRANCHES, key="pdf_branch")
    
    query = "SELECT * FROM notes WHERE note_type='PDF'"
    if search_sub:
        query += f" AND subject LIKE '%{search_sub}%'"
    if filter_branch != "All":
        query += f" AND title LIKE '%{filter_branch}%'"
    
    c.execute(query)
    pdfs = c.fetchall()
    
    if not pdfs:
        st.info("No PDFs found for this selection.")
    else:
        for note in pdfs:
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"**{note[1]}**") # Subject
                    st.caption(f"{note[2]} • Uploaded by {note[5]}")
                with c2:
                    st.link_button("⬇ Download", note[3])

# --- TAB 2: LAB MANUALS & VIVA (NEW!) ---
with tabs[1]:
    st.subheader("🧪 Lab Manuals & Viva Q&A")
    st.info("Find corrected lab records and important viva questions here.")
    
    c.execute("SELECT * FROM notes WHERE note_type='LAB'")
    labs = c.fetchall()
    
    if not labs:
        st.warning("No Lab materials uploaded yet.")
    else:
        for item in labs:
            with st.expander(f"🧪 {item[1]} ({item[2]})"): # Subject (Type)
                st.write(f"**Uploaded by:** {item[5]}")
                st.link_button("View Document", item[3])

# --- TAB 3: SYLLABUS COPIES (NEW!) ---
with tabs[2]:
    st.subheader("📜 Official Syllabus (R18/R22)")
    st.success("Always study the right topics. Download official JNTUH syllabus copies.")
    
    c.execute("SELECT * FROM notes WHERE note_type='SYLLABUS'")
    syllabi = c.fetchall()
    
    if not syllabi:
        st.info("No Syllabus copies uploaded yet.")
    else:
        for s in syllabi:
            # Display as a clean list
            col_a, col_b = st.columns([3, 1])
            col_a.markdown(f"**{s[1]}** - {s[2]}") # e.g., CSE - R18
            col_b.link_button("📄 Open PDF", s[3])
            st.divider()

# --- TAB 4: QUESTION PAPERS (Updated with Mids) ---
with tabs[3]:
    st.subheader("❓ Previous Year Question Papers (PYQ)")
    
    # Advanced Filters
    c1, c2, c3 = st.columns(3)
    sel_branch = c1.selectbox("Branch", ["All"] + BRANCHES, key="pyq_branch")
    sel_exam = c2.selectbox("Exam Type", ["All", "Semester", "Mid-1", "Mid-2"], key="pyq_type")
    sel_year = c3.selectbox("Year", ["All", "2023", "2022", "2021", "2020"], key="pyq_year")
    
    query = "SELECT * FROM notes WHERE note_type='PYQ'"
    if sel_branch != "All":
        query += f" AND title LIKE '%{sel_branch}%'"
    if sel_exam != "All":
        query += f" AND title LIKE '%{sel_exam}%'"
    if sel_year != "All":
        query += f" AND title LIKE '%{sel_year}%'"
        
    c.execute(query)
    pyqs = c.fetchall()
    
    if not pyqs:
        st.info("No Question Papers match your filters.")
    else:
        for paper in pyqs:
            with st.container(border=True):
                st.markdown(f"**{paper[1]}**") # Subject
                st.caption(f"📄 {paper[2]}") # Full Title (e.g. CSE - 2023 - Mid-1)
                st.link_button("View Paper", paper[3])

# --- TAB 5: XEROX MARKET ---
with tabs[4]:
    st.subheader("🖨️ Buy Hard Copy Xerox")
    
    c.execute("SELECT * FROM notes WHERE note_type='XEROX'")
    items = c.fetchall()
    
    if not items:
        st.warning("No Xerox copies for sale.")
    else:
        cols = st.columns(3)
        for i, item in enumerate(items):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"### {item[1]}") # Subject
                    st.write(f"**{item[2]}**") # Title
                    st.markdown(f"#### Price: ₹{item[4]}")
                    wa_url = f"https://wa.me/{item[7]}?text=Hi, I want to buy your {item[1]} notes."
                    st.link_button("💬 Chat on WhatsApp", wa_url, type="primary")

# --- TAB 6: UPLOAD EVERYTHING ---
with tabs[5]:
    st.subheader("📤 Upload Resource")
    
    if "user" not in st.session_state:
        st.error("Please Login to upload.")
    else:
        # Category Selector
        category = st.radio("Select Category", 
            ["📄 Digital Note", "🧪 Lab Manual / Viva", "📜 Syllabus Copy", "❓ Question Paper", "🖨️ Xerox (Sell)"],
            horizontal=True
        )
        
        with st.form("upload_form"):
            # Common Fields
            subj = st.selectbox("Subject Name", ["M1", "BEE", "Chemistry", "Python", "Data Structures", "OS", "DBMS", "AI/ML", "General"])
            
            # Dynamic Logic
            title = ""
            price = 0
            contact = "N/A"
            link = ""
            note_type_db = "PDF" # Default

            if category == "❓ Question Paper":
                c1, c2, c3 = st.columns(3)
                branch = c1.selectbox("Branch", BRANCHES)
                year = c2.selectbox("Year", ["2023", "2022", "2021", "2020"])
                exam = c3.selectbox("Exam", ["Semester", "Mid-1", "Mid-2"])
                title = f"{branch} - {year} - {exam}" # Auto-Title
                link = st.text_input("Drive Link (PDF)")
                note_type_db = "PYQ"

            elif category == "🧪 Lab Manual / Viva":
                doc_type = st.selectbox("Type", ["Lab Record", "Viva Questions"])
                title = st.text_input("Title", value=f"{doc_type} - {subj}")
                link = st.text_input("Drive Link (PDF)")
                note_type_db = "LAB"

            elif category == "📜 Syllabus Copy":
                branch = st.selectbox("Branch", BRANCHES)
                reg = st.selectbox("Regulation", ["R22", "R18"])
                title = f"{branch} - {reg} Syllabus"
                link = st.text_input("Drive Link (PDF)")
                note_type_db = "SYLLABUS"
                subj = "General" # Syllabus is usually general

            elif category == "🖨️ Xerox (Sell)":
                title = st.text_input("Description (e.g., Full Spiral)")
                price = st.number_input("Price (₹)", value=100)
                contact = st.text_input("WhatsApp Number")
                link = "N/A"
                note_type_db = "XEROX"

            else: # Digital Note
                title = st.text_input("Title (e.g., Unit 1 Handwritten)")
                branch = st.selectbox("Branch", ["All"] + BRANCHES) # Optional tagging
                if branch != "All":
                    title += f" ({branch})"
                link = st.text_input("Drive Link")
                note_type_db = "PDF"

            submitted = st.form_submit_button("🚀 Upload Resource")
            
            if submitted:
                c.execute("INSERT INTO notes (subject, title, link, price, uploader, note_type, contact) VALUES (?,?,?,?,?,?,?)",
                          (subj, title, link, price, st.session_state["user"], note_type_db, contact))
                conn.commit()
                st.success("Uploaded successfully!")

conn.close()