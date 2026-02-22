import streamlit as st
import database as db
import time

db.init_db()

# Check for admin
is_admin = st.session_state.get("is_admin", False)

st.markdown("""
<style>
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
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
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px 30px; border-radius: 16px; margin-bottom: 25px;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.25);
    }
    .page-title { color: white; font-size: 1.8rem; font-weight: 800; margin: 0; }
    .page-subtitle { color: rgba(255,255,255,0.85); font-size: 0.95rem; margin-top: 6px; }
    
    .resource-card {
        background: white; border: 1px solid #e2e8f0; border-radius: 16px;
        padding: 18px; margin-bottom: 14px; transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .resource-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    .resource-title { font-weight: 700; font-size: 1.1rem; color: #1e293b; margin-bottom: 6px; }
    .resource-meta { font-size: 0.85rem; color: #64748b; margin-bottom: 4px; }
    .resource-price { font-weight: 700; font-size: 1.2rem; color: #10b981; }
    .resource-price.free { color: #667eea; }
    
    .star-rating { color: #fbbf24; }
    .star-filled { color: #fbbf24; }
    .star-empty { color: #d1d5db; }
    
    .upload-section {
        background: #f8fafc; border: 2px dashed #cbd5e1; border-radius: 12px;
        padding: 30px; text-align: center; margin-bottom: 20px;
    }
    .upload-section:hover { border-color: #667eea; background: #f0f5ff; }
    
    .admin-banner {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white; padding: 10px 20px; border-radius: 10px;
        margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;
    }
    .admin-banner h3 { margin: 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1 class="page-title">📚 Notes Marketplace</h1>
    <p class="page-subtitle">Access verified study materials, lab manuals & previous papers</p>
</div>
""", unsafe_allow_html=True)

if is_admin:
    st.markdown("""
    <div class="admin-banner">
        <h3>🛡️ Admin Mode - Full Access</h3>
    </div>
    """, unsafe_allow_html=True)

def get_star_display(rating):
    if not rating or rating == 0:
        return "No ratings yet"
    full = int(rating)
    html = f"<span class='star-rating'>"
    for i in range(5):
        if i < full:
            html += f"<span class='star-filled'>★</span>"
        else:
            html += f"<span class='star-empty'>★</span>"
    html += f"</span> ({rating}/5)"
    return html

st.title("📚 PEC Resource Center")
st.caption("Access verified study materials, lab manuals, and previous papers.")

BRANCHES = ["CSE", "CSE-AIML", "CSE-DS", "ECE", "EEE", "Civil", "Mech", "IT", "Chemical", "Biotech"]

SUBJECTS_BY_YEAR = {
    "1st Year": [
        "M1 - Matrices & Calculus",
        "M2 - Differential Equations & Vector Calculus",
        "Engineering Chemistry",
        "Applied Physics",
        "Programming for Problem Solving (C)",
        "Python Programming",
        "Basic Electrical Engineering",
        "Engineering Drawing",
        "Engineering Workshop",
        "IT Workshop",
        "English - Communication Skills",
        "Environmental Science",
    ],
    "2nd Year": [
        "Discrete Mathematics",
        "Data Structures",
        "Digital Logic Design",
        "Computer Organization & Architecture",
        "Object Oriented Programming (Java/C++)",
        "Operating Systems",
        "Database Management Systems",
        "Formal Languages & Automata Theory",
        "Software Engineering",
        "Probability & Statistics",
        "Electronic Devices & Circuits",
        "Network Theory",
        "Signals & Systems",
        "Analog Electronics",
        "Digital Electronics",
        "Electrical Circuit Analysis",
        "Electrical Machines - I",
        "Power Systems - I",
        "Control Systems",
        "Engineering Mechanics",
        "Strength of Materials",
        "Fluid Mechanics",
        "Building Materials & Construction",
        "Surveying",
        "Thermodynamics",
        "Manufacturing Processes",
        "Kinematics of Machinery",
    ],
    "3rd Year": [
        "Algorithms",
        "Compiler Design",
        "Computer Networks",
        "Cryptography & Network Security",
        "Artificial Intelligence",
        "Machine Learning",
        "Data Science",
        "Cloud Computing",
        "DevOps",
        "Web Technologies",
        "Microprocessors & Microcontrollers",
        "Electromagnetic Waves",
        "Communication Theory",
        "Power Electronics",
        "Electrical Machines - II",
        "Measurements & Instrumentation",
        "Concrete Technology",
        "Structural Analysis - I",
        "Theory of Machines",
        "Machine Drawing",
    ],
    "4th Year": [
        "Deep Learning",
        "Big Data",
        "Mobile App Development",
        "Blockchain Technology",
        "Internet of Things (IoT)",
        "Cybersecurity",
        "Distributed Systems",
        "Theory of Computation",
        "Computer Graphics",
        "VLSI Design",
        "Antenna & Wave Propagation",
        "Microwave Engineering",
        "Digital Signal Processing",
        "Embedded Systems",
        "Wireless Communications",
        "Optical Communications",
        "Image Processing",
        "Neural Networks & Fuzzy Logic",
        "Power Systems - II",
        "Power System Analysis",
        "Power System Protection",
        "Renewable Energy Sources",
        "Smart Grid",
        "Electrical Drives",
        "Structural Analysis - II",
        "RCC & Steel Structures",
        "Geotechnical Engineering",
        "Water Resources Engineering",
        "Transportation Engineering",
        "Environmental Engineering",
        "Heat Transfer",
        "Design of Machine Elements",
        "Refrigeration & Air Conditioning",
        "Automobile Engineering",
        "CAD/CAM",
        "Finite Element Analysis",
        "Industrial Engineering",
        "Robotics & Automation",
    ],
    "Labs": [
        "C Programming Lab",
        "Python Lab",
        "Data Structures Lab",
        "DBMS Lab",
        "OS Lab",
        "CN Lab",
        "AI/ML Lab",
        "Java Programming Lab",
        "Software Engineering Lab",
        "Physics Lab",
        "Chemistry Lab",
        "Electrical Lab",
    ],
    "Other": [
        "General",
        "All Branches"
    ]
}

ALL_SUBJECTS = []
for year_subjects in SUBJECTS_BY_YEAR.values():
    ALL_SUBJECTS.extend(year_subjects)
ALL_SUBJECTS = sorted(ALL_SUBJECTS)

def delete_resource(note_id):
    try:
        db.supabase.table("notes").delete().eq("id", note_id).execute()
        return True
    except:
        return False

tabs = st.tabs([
    "📄 Digital Notes", 
    "🧪 Lab & Viva",
    "📜 Syllabus",
    "❓ Question Papers", 
    "🖨️ Buy Xerox", 
    "📤 Upload / Sell"
])

with tabs[0]:
    st.subheader("📖 Free Digital Notes")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        f_year = st.selectbox("Year", ["All Years"] + list(SUBJECTS_BY_YEAR.keys()), key="filt_year")
    with col2:
        if f_year == "All Years":
            s_query = st.selectbox("Subject", ["All Subjects"] + ALL_SUBJECTS, key="search_pdf")
        else:
            s_query = st.selectbox("Subject", ["All Subjects"] + SUBJECTS_BY_YEAR[f_year], key="search_pdf")
    with col3:
        min_rating = st.selectbox("Rating", ["All", "★ 1+", "★★ 2+", "★★★ 3+", "★★★★ 4+", "★★★★★ 5"], index=0)
    
    rating_map = {"All": 0, "★ 1+": 1, "★★ 2+": 2, "★★★ 3+": 3, "★★★★ 4+": 4, "★★★★★ 5": 5}
    min_rating_val = rating_map.get(min_rating, 0)
    
    try:
        res = db.supabase.table("notes").select("*").eq("note_type", "PDF")
        if s_query and s_query != "All Subjects": res = res.ilike("subject", f"%{s_query}%")
        notes = res.execute().data
    except: notes = []
    
    if min_rating_val > 0:
        notes = [n for n in notes if (n.get("avg_rating") or 0) >= min_rating_val]

    if not notes:
        st.info("No notes found.")
    else:
        for n in notes:
            with st.container(border=True):
                ca, cb, cc = st.columns([3, 1.5, 0.5])
                with ca:
                    is_verified = n.get("is_verified", False)
                    verified_badge = " ✅" if is_verified else ""
                    st.markdown(f"**{n['subject']}** — {n['title']}{verified_badge}")
                    
                    avg_rating = n.get("avg_rating") or 0
                    rating_count = n.get("rating_count") or 0
                    if avg_rating > 0:
                        st.markdown(f"<div>{get_star_display(avg_rating)} · {rating_count} reviews</div>", unsafe_allow_html=True)
                    else:
                        st.caption("No ratings yet")
                    st.caption(f"📤 Uploaded by: {n['uploader']}")
                with cb:
                    st.link_button("⬇ Download", n['link'], use_container_width=True)
                with cc:
                    if is_admin:
                        c_del, c_warn = st.columns(2)
                        with c_del:
                            if st.button("🗑️", key=f"del_{n['id']}"):
                                db.delete_note(n['id'])
                                st.success("Deleted!")
                                time.sleep(1)
                                st.rerun()
                        with c_warn:
                            if st.button("⚠️", key=f"warn_{n['id']}"):
                                warning_msg = f"Your note '{n['title']}' has been removed for violating community guidelines."
                                db.send_warning(n['uploader'], warning_msg)
                                db.delete_note(n['id'])
                                st.warning("Warning sent and note deleted!")
                                time.sleep(1)
                                st.rerun()
                    elif "user" in st.session_state and st.session_state["user"] == n['uploader']:
                        if st.button("🗑️", key=f"del_{n['id']}"):
                            if delete_resource(n['id']):
                                st.success("Deleted!")
                                time.sleep(1)
                                st.rerun()
                
                with st.expander("⭐ Rate & Review"):
                    if "user" in st.session_state:
                        st.markdown("**Select Rating:**")
                        col_star1, col_star2, col_star3, col_star4, col_star5 = st.columns(5)
                        selected_rating = 5
                        with col_star1:
                            if st.button("★", key=f"s1_{n['id']}"):
                                selected_rating = 1
                        with col_star2:
                            if st.button("★★", key=f"s2_{n['id']}"):
                                selected_rating = 2
                        with col_star3:
                            if st.button("★★★", key=f"s3_{n['id']}"):
                                selected_rating = 3
                        with col_star4:
                            if st.button("★★★★", key=f"s4_{n['id']}"):
                                selected_rating = 4
                        with col_star5:
                            if st.button("★★★★★", key=f"s5_{n['id']}"):
                                selected_rating = 5
                        
                        st.markdown(f"<div style='text-align:center; font-size:1.2rem; margin:10px 0;'>Selected: {selected_rating} ★</div>", unsafe_allow_html=True)
                        
                        with st.form(f"rate_{n['id']}"):
                            review = st.text_area("Write a review (optional)", key=f"rev_{n['id']}")
                            if st.form_submit_button("Submit Review"):
                                db.rate_note(n['id'], selected_rating)
                                if review:
                                    db.add_note_review(n['id'], st.session_state["user"], review)
                                st.success("Thanks for your feedback!")
                                time.sleep(1)
                                st.rerun()
                    else:
                        st.info("Login to rate and review")
                    
                    reviews = db.get_note_reviews(n['id'])
                    if reviews:
                        st.markdown("### Recent Reviews")
                        for r in reviews[:3]:
                            st.markdown(f"**@{r['username']}**: {r['review']}")

types = {"🧪 Lab Manuals": "LAB", "📜 Syllabus": "SYLLABUS", "❓ PYQs": "PYQ"}
for idx, (label, db_type) in enumerate(types.items(), start=1):
    with tabs[idx]:
        st.subheader(label)
        
        col_filter1, col_filter2 = st.columns(2)
        with col_filter1:
            filter_year = st.selectbox(f"Year ({label})", ["All Years"] + list(SUBJECTS_BY_YEAR.keys()), key=f"year_{db_type}")
        with col_filter2:
            if filter_year == "All Years":
                filter_subject = st.selectbox(f"Subject ({label})", ["All Subjects"] + ALL_SUBJECTS, key=f"filt_{db_type}")
            else:
                filter_subject = st.selectbox(f"Subject ({label})", ["All Subjects"] + SUBJECTS_BY_YEAR[filter_year], key=f"filt_{db_type}")
        
        min_rating = st.selectbox("Rating", ["All", "★ 1+", "★★ 2+", "★★★ 3+", "★★★★ 4+", "★★★★★ 5"], index=0, key=f"rat_{db_type}")
        
        rating_map = {"All": 0, "★ 1+": 1, "★★ 2+": 2, "★★★ 3+": 3, "★★★★ 4+": 4, "★★★★★ 5": 5}
        min_rating_val = rating_map.get(min_rating, 0)
        
        try:
            res = db.supabase.table("notes").select("*").eq("note_type", db_type)
            if filter_subject and filter_subject != "All Subjects":
                res = res.ilike("subject", f"%{filter_subject}%")
            items = res.execute().data
        except: items = []
        
        if filter_year != "All Years":
            year_subjects = SUBJECTS_BY_YEAR.get(filter_year, [])
            items = [i for i in items if i.get("subject") in year_subjects]
        
        if min_rating_val > 0:
            items = [i for i in items if (i.get("avg_rating") or 0) >= min_rating_val]
        
        if not items:
            st.info(f"No {label} available yet.")
        else:
            for i in items:
                with st.container(border=True):
                    c1, c2, c3 = st.columns([3, 1, 0.5])
                    with c1:
                        is_verified = i.get("is_verified", False)
                        verified_badge = " ✅" if is_verified else ""
                        st.markdown(f"**{i['title']}**{verified_badge}")
                        
                        avg_rating = i.get("avg_rating") or 0
                        rating_count = i.get("rating_count") or 0
                        if avg_rating > 0:
                            st.markdown(f"<div>{get_star_display(avg_rating)} · {rating_count} reviews</div>", unsafe_allow_html=True)
                        else:
                            st.caption("No ratings yet")
                        st.caption(f"📂 {i['subject']} | 👤 {i['uploader']}")
                    with c2:
                        st.link_button("⬇ Download", i['link'], use_container_width=True)
                    with c3:
                        if "user" in st.session_state and st.session_state["user"] == i['uploader']:
                            if st.button("🗑️", key=f"del_{i['id']}"):
                                delete_resource(i['id'])
                                st.rerun()
                    
                    with st.expander("⭐ Rate & Review"):
                        if "user" in st.session_state:
                            with st.form(f"rate_{i['id']}"):
                                rating = st.select_slider("Your Rating", options=[1, 2, 3, 4, 5], value=5)
                                review = st.text_area("Write a review (optional)", key=f"rev_{i['id']}")
                                if st.form_submit_button("Submit Review"):
                                    db.rate_note(i['id'], rating)
                                    if review:
                                        db.add_note_review(i['id'], st.session_state["user"], review)
                                    st.success("Thanks for your feedback!")
                                    time.sleep(1)
                                    st.rerun()
                        else:
                            st.info("Login to rate and review")
                    if "user" in st.session_state and st.session_state["user"] == i['uploader']:
                        if st.button("🗑️ Remove", key=f"del_i_{i['id']}"):
                            delete_resource(i['id'])
                            st.rerun()

with tabs[4]:
    st.subheader("🖨️ Buy Hard Copy Xerox")
    try:
        xerox = db.supabase.table("notes").select("*").eq("note_type", "XEROX").execute().data
    except: xerox = []
    
    if not xerox:
        st.warning("No Xerox listings available.")
    else:
        cols = st.columns(3)
        for i, item in enumerate(xerox):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"### {item['subject']}")
                    st.write(f"_{item['title']}_")
                    st.markdown(f"<div class='price-tag'>₹{item['price']}</div>", unsafe_allow_html=True)
                    st.caption(f"Seller: {item['uploader']}")
                    
                    wa_link = f"https://wa.me/{item['contact']}?text=Hi, I want to buy {item['title']} notes."
                    
                    # Action buttons
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        st.link_button("💬 WhatsApp", wa_link, type="primary", use_container_width=True)
                    with btn_col2:
                        if "user" in st.session_state and st.session_state["user"] == item['uploader']:
                            if st.button("🗑️ Delete", key=f"del_xerox_{item['id']}", use_container_width=True):
                                delete_resource(item['id'])
                                st.success("Deleted!")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.caption("")

with tabs[5]:
    st.subheader("📤 Contribute a Resource")
    if "user" not in st.session_state:
        st.error("Please Login to upload study materials.")
    else:
        col_cat, col_year, col_sub = st.columns([2, 1, 2])
        with col_cat:
            cat = st.selectbox("Category", ["Digital Note", "Lab Manual", "Syllabus Copy", "Question Paper", "Xerox (Sell)"])
        with col_year:
            year = st.selectbox("Year", list(SUBJECTS_BY_YEAR.keys()))
        with col_sub:
            sub = st.selectbox("Subject", SUBJECTS_BY_YEAR[year])
        
        if cat != "Xerox (Sell)":
            if "source_option" not in st.session_state:
                st.session_state["source_option"] = "📄 Upload PDF"
            
            col_radio1, col_radio2 = st.columns([1, 1])
            with col_radio1:
                if st.button("📄 Upload PDF", use_container_width=True, type="primary" if st.session_state["source_option"] == "📄 Upload PDF" else "secondary"):
                    st.session_state["source_option"] = "📄 Upload PDF"
                    st.rerun()
            with col_radio2:
                if st.button("🔗 Google Drive Link", use_container_width=True, type="primary" if st.session_state["source_option"] == "🔗 Google Drive Link" else "secondary"):
                    st.session_state["source_option"] = "🔗 Google Drive Link"
                    st.rerun()
        
        with st.form("upload_form"):
            title = st.text_input("Title / Description", placeholder="e.g., Unit 1-3 Complete Handwritten Notes")
            
            db_type_map = {
                "Digital Note": "PDF", "Lab Manual": "LAB", 
                "Syllabus Copy": "SYLLABUS", "Question Paper": "PYQ", "Xerox (Sell)": "XEROX"
            }
            
            if cat == "Xerox (Sell)":
                st.markdown("---")
                st.markdown("### 🖨️ Xerox Details")
                
                col_cond1, col_cond2 = st.columns(2)
                with col_cond1:
                    condition = st.selectbox("Notes Condition", ["New (Unused)", "Good (Slightly Used)", "Fair (Moderate Notes)", "Photostat Copy"])
                with col_cond2:
                    pages = st.number_input("Total Pages", min_value=1, value=10)
                
                col_price1, col_price2 = st.columns(2)
                with col_price1:
                    price = st.number_input("Price (₹)", min_value=0, value=10)
                with col_price2:
                    contact = st.text_input("WhatsApp Number", value="91")
                
                topics = st.text_area("Topics Covered (Optional)", placeholder="e.g., Unit 1: Linear Algebra, Unit 2: Differential Equations")
                
                st.caption("💡 Seller contact will be shared with buyers via WhatsApp")
                
                link = None
                pdf_file = None
            else:
                st.markdown("---")
                st.markdown("### 📋 Note Details")
                
                col_note1, col_note2 = st.columns(2)
                with col_note1:
                    note_type = st.selectbox("Note Type", ["Handwritten", "Typed/Printed", "Mixed", "Lecture Slides", "Teacher's Notes"])
                with col_note2:
                    units_covered = st.text_input("Units Covered", placeholder="e.g., Unit 1, 2 & 3 or All Units")
                
                language = st.selectbox("Language", ["English", "Telugu", "Hindi", "Other"])
                
                topics = st.text_area("Topics Covered", placeholder="e.g., Matrices, Eigen Values, Cauchy Theorem, Linear Algebra fundamentals...")
                quality = st.selectbox("Quality", ["Excellent - Clear & Readable", "Good - Slightly Messy", "Average - Needs Improvement"])
                year_pattern = st.selectbox("Exam Pattern", ["University Exams", "Internal Exams", "Both", "Not Sure"])
                
                st.caption("💡 Pages count will be shown from the uploaded PDF automatically")
                
                st.markdown("---")
                st.markdown("### 📎 Upload Source")
                
                source_option = st.session_state.get("source_option", "📄 Upload PDF")
                
                link = None
                pdf_file = None
                
                if source_option == "📄 Upload PDF":
                    pdf_file = st.file_uploader("Upload PDF (Max 200MB)", type=["pdf"])
                    if pdf_file:
                        file_size_mb = pdf_file.size / (1024 * 1024)
                        st.success(f"Selected: {pdf_file.name} ({file_size_mb:.1f} MB)")
                        if file_size_mb > 200:
                            st.warning("⚠️ File exceeds 200MB. Consider using Google Drive link instead.")
                else:
                    link = st.text_input("Google Drive Link", placeholder="https://drive.google.com/...")
                    st.caption("💡 Make sure the link has 'Anyone with link' access")
                
                price = 0
                contact = ""
                pages = 0
            
            if st.form_submit_button("🚀 Publish to PEC Market"):
                final_link = link
                
                if pdf_file:
                    file_size_mb = pdf_file.size / (1024 * 1024)
                    if file_size_mb > 200:
                        st.error("File too large (over 200MB). Please use Google Drive link instead.")
                        st.stop()
                    
                    file_bytes = pdf_file.getvalue()
                    file_type = pdf_file.type
                    final_link = db.upload_note_file(
                        st.session_state["user"], 
                        file_bytes, 
                        pdf_file.name, 
                        file_type
                    )
                    if not final_link:
                        st.error("Failed to upload PDF. Please try again.")
                        st.stop()
                
                if title and (final_link or cat == "Xerox (Sell)"):
                    upload_data = {
                        "subject": sub,
                        "title": title,
                        "link": final_link if final_link else "N/A",
                        "price": price,
                        "uploader": st.session_state["user"],
                        "note_type": db_type_map[cat],
                        "contact": contact
                    }
                    try:
                        db.supabase.table("notes").insert(upload_data).execute()
                        st.success("Successfully Shared with the Campus!")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Upload failed: {e}")
                else:
                    st.warning("Please fill in the title and upload a file or link.")