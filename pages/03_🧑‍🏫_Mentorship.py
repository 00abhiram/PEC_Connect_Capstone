import streamlit as st
import database as db

db.init_db()

# Check for admin
is_admin = st.session_state.get("is_admin", False)

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
    
    .admin-banner {
        background: linear-gradient(135deg, #dc2626, #991b1b);
        color: white; padding: 10px 20px; border-radius: 10px;
        margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center;
    }
    .admin-banner h3 { margin: 0; }
    
    .page-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 25px 30px; border-radius: 16px; margin-bottom: 25px;
        position: relative; overflow: hidden;
    }
    .page-header::before {
        content: ''; position: absolute; top: -50%; right: -10%;
        width: 200px; height: 200px; background: rgba(255,255,255,0.1);
        border-radius: 50%;
    }
    .page-title { color: white; font-size: 1.8rem; font-weight: 800; margin: 0; }
    .page-subtitle { color: rgba(255,255,255,0.85); font-size: 0.95rem; margin-top: 6px; }
    
    .mentor-card {
        background: white; border: 1px solid #e2e8f0; border-radius: 16px;
        padding: 20px; margin-bottom: 20px; transition: all 0.3s ease;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    }
    .mentor-card:hover { 
        transform: translateY(-4px); 
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.15); 
        border-color: #667eea;
    }
    
    .mentor-header {
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #f1f5f9;
    }
    .mentor-name { font-size: 1.1rem; font-weight: 700; color: #1e293b; }
    .mentor-rating { 
        background: linear-gradient(135deg, #fef3c7, #fde68a); color: #b45309;
        padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;
    }
    .mentor-rating-new {
        background: linear-gradient(135deg, #e0e7ff, #c7d2fe); color: #4338ca;
        padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;
    }
    
    .mentor-body { display: flex; gap: 15px; margin-bottom: 15px; }
    .mentor-avatar { width: 70px; height: 70px; border-radius: 12px; object-fit: cover; }
    .mentor-info { flex: 1; }
    .mentor-subjects { 
        display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px;
    }
    .subject-tag {
        background: #f1f5f9; color: #475569; padding: 3px 10px;
        border-radius: 8px; font-size: 0.7rem; font-weight: 600;
    }
    .subject-tag-purple {
        background: linear-gradient(135deg, #667eea20, #764ba220); 
        color: #475569; padding: 3px 10px;
        border-radius: 8px; font-size: 0.7rem; font-weight: 600;
    }
    
    .mentor-bio { 
        color: #64748b; font-size: 0.85rem; line-height: 1.5;
        margin-bottom: 15px; padding: 12px; background: #f8fafc;
        border-radius: 10px;
    }
    
    .mentor-footer {
        display: flex; justify-content: space-between; align-items: center;
        padding-top: 15px; border-top: 1px solid #f1f5f9;
    }
    .mentor-price {
        font-size: 1.4rem; font-weight: 800; color: #667eea;
    }
    .mentor-price span { font-size: 0.8rem; color: #94a3b8; font-weight: 400; }
    
    .mentor-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white; padding: 5px 12px;
        border-radius: 20px; font-size: 0.7rem; font-weight: 700;
        letter-spacing: 0.5px;
    }
    .mentor-badge-new {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white; padding: 5px 12px;
        border-radius: 20px; font-size: 0.7rem; font-weight: 700;
    }
    .mentor-badge-top {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white; padding: 5px 12px;
        border-radius: 20px; font-size: 0.7rem; font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

if is_admin:
    st.markdown("""
    <div class="admin-banner">
        <h3>🛡️ Admin Mode - Full Access</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
    <h1 class="page-title">🧑‍🏫 Mentorship Program</h1>
    <p class="page-subtitle">Connect with senior mentors for personalized academic guidance</p>
</div>
""", unsafe_allow_html=True)

SUBJECTS_BY_YEAR = {
    "1st Year": [
        "M1 - Matrices & Calculus",
        "M2 - Ordinary Differential Equations & Vector Calculus",
        "Engineering Chemistry",
        "Advanced Engineering Physics",
        "Programming for Problem Solving (C)",
        "Python Programming",
        "C Programming & Data Structures",
        "Basic Electrical Engineering",
        "Introduction to Electrical Engineering",
        "Engineering Drawing & Computer Aided Drafting",
        "Computer Aided Engineering Graphics",
        "Engineering Workshop",
        "IT Workshop",
        "English - Communication Skills",
        "English for Skill Enhancement",
        "Environmental Science",
        "Elements of Computer Science & Engineering",
    ],
    "2nd Year - CSE": [
        "Discrete Mathematics",
        "Data Structures",
        "Digital Logic Design",
        "Computer Organization & Architecture",
        "Object Oriented Programming (Java)",
        "Object Oriented Programming through C++",
        "Operating Systems",
        "Database Management Systems",
        "Formal Languages & Automata Theory",
        "Software Engineering",
        "Probability & Statistics",
        "Computer Graphics",
        "Java Programming",
    ],
    "2nd Year - ECE": [
        "Electronic Devices & Circuits",
        "Network Theory",
        "Signals & Systems",
        "Analog Electronics",
        "Digital Electronics",
        "Electromagnetic Waves",
        "Electronic Circuit Analysis",
        "Data Communications & Computer Networks",
        "Microprocessors & Microcontrollers",
        "Control Systems",
        "Probability & Statistics",
    ],
    "2nd Year - EEE": [
        "Electrical Circuit Analysis",
        "Electrical Machines - I",
        "Power Systems - I",
        "Control Systems",
        "Electronic Devices & Circuits",
        "Network Theory",
        "Signals & Systems",
        "Analog Electronics",
        "Digital Electronics",
        "Measurements & Instrumentation",
        "Power Electronics",
    ],
    "2nd Year - Mechanical": [
        "Engineering Mechanics",
        "Strength of Materials",
        "Fluid Mechanics",
        "Thermodynamics",
        "Manufacturing Processes",
        "Kinematics of Machinery",
        "Machine Drawing",
        "Material Science",
        "Metal Cutting & Machine Tools",
        "Theory of Machines",
    ],
    "2nd Year - Civil": [
        "Building Materials & Construction",
        "Surveying",
        "Strength of Materials",
        "Fluid Mechanics",
        "Engineering Mechanics",
        "Structural Analysis - I",
        "Concrete Technology",
        "Hydraulics & Hydraulic Machines",
        "Engineering Geology",
        "Building Planning & Drawing",
    ],
    "3rd Year - CSE": [
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
        "Distributed Databases",
        "Blockchain Technology",
        "Internet of Things (IoT)",
        "Mobile App Development",
        "Software Testing Methodologies",
        "Computer Networks",
    ],
    "3rd Year - ECE": [
        "Communication Theory",
        "Digital Signal Processing",
        "VLSI Design",
        "Microwave Engineering",
        "Antenna & Wave Propagation",
        "Wireless Communications",
        "Optical Communications",
        "Embedded Systems",
        "Digital Image Processing",
        "Microcontrollers & Applications",
        "Verilog HDL",
        "CMOS VLSI Design",
        "Satellite Communications",
        "Radar Systems",
    ],
    "3rd Year - EEE": [
        "Power Systems - II",
        "Power System Analysis",
        "Power System Protection",
        "Electrical Machines - II",
        "Power Electronics",
        "Renewable Energy Sources",
        "Smart Grid",
        "Electrical Drives",
        "High Voltage Engineering",
        "Power System Operation & Control",
        "Switchgear & Protection",
    ],
    "3rd Year - Mechanical": [
        "Thermal Engineering - I",
        "Thermal Engineering - II",
        "Design of Machine Elements",
        "Heat Transfer",
        "Refrigeration & Air Conditioning",
        "Automobile Engineering",
        "CAD/CAM",
        "Finite Element Analysis",
        "Industrial Engineering",
        "Robotics & Automation",
        "Production Planning & Control",
        "Engineering Metallurgy",
    ],
    "3rd Year - Civil": [
        "Structural Analysis - II",
        "RCC & Steel Structures",
        "Geotechnical Engineering",
        "Water Resources Engineering",
        "Transportation Engineering",
        "Environmental Engineering",
        "Foundation Engineering",
        "Earthquake Resistant Design",
        "Advanced Reinforced Concrete Structures",
        "Bridge Engineering",
        "Construction Technology & Management",
    ],
    "4th Year - CSE": [
        "Deep Learning",
        "Big Data Analytics",
        "Cybersecurity",
        "Natural Language Processing",
        "Computer Vision",
        "Cloud Native Computing",
        "Quantum Computing",
        "DevSecOps",
        "Microservices Architecture",
        "Data Warehousing & Mining",
        "Adhoc & Sensor Networks",
        "Neural Networks & Fuzzy Logic",
    ],
    "4th Year - ECE": [
        "Digital Signal Processing",
        "Embedded Systems",
        "Wireless Sensor Networks",
        "Image Processing",
        "Neural Networks & Fuzzy Logic",
        "Microwave & Radar Engineering",
        "VLSI Design & Testing",
        "IoT & Smart Cities",
        "5G Communications",
        "Advanced Communications",
        "FPGA Design",
    ],
    "4th Year - EEE": [
        "Power System Analysis",
        "Power System Protection",
        "Switchgear & Protection",
        "Electrical Drives & Controls",
        "Smart Grid Technologies",
        "Renewable Energy Systems",
        "HVDC Transmission",
        "Power Quality",
        "Electric Vehicles",
        "Energy Management",
        "Power System Operation & Control",
    ],
    "4th Year - Mechanical": [
        "Design of Machine Elements",
        "Refrigeration & Air Conditioning",
        "Automobile Engineering",
        "CAD/CAM/CAE",
        "Finite Element Analysis",
        "Robotics & Automation",
        "Industrial Engineering",
        "Thermal Power Engineering",
        "Computational Fluid Dynamics",
        "Additive Manufacturing",
        "Product Design & Development",
    ],
    "4th Year - Civil": [
        "RCC & Steel Structures",
        "Prestressed Concrete",
        "Bridge Engineering",
        "Geotechnical Engineering",
        "Water Resources Engineering",
        "Transportation Engineering",
        "Environmental Engineering",
        "Structural Dynamics",
        "Earthquake Engineering",
        "Construction Management",
        "Advanced Steel Structures",
    ],
    "Labs": [
        "C Programming Lab",
        "Python Lab",
        "Data Structures Lab",
        "DBMS Lab",
        "OS Lab",
        "Computer Networks Lab",
        "AI/ML Lab",
        "Java Programming Lab",
        "Software Engineering Lab",
        "Web Technologies Lab",
        "Machine Learning Lab",
        "Deep Learning Lab",
        "Cyber Security Lab",
        "Cloud Computing Lab",
        "IoT Lab",
        "Microprocessors Lab",
        "Microcontrollers Lab",
        "VLSI Lab",
        "Digital Electronics Lab",
        "Analog Electronics Lab",
        "Signal Processing Lab",
        "Communication Systems Lab",
        "Power Electronics Lab",
        "Power Systems Lab",
        "Electrical Machines Lab",
        "Control Systems Lab",
        "Physics Lab",
        "Chemistry Lab",
        "Electrical & Electronics Lab",
        "Strength of Materials Lab",
        "Surveying Lab",
        "Fluid Mechanics Lab",
        "CAD Lab",
        "CAM Lab",
        "Workshop Practice Lab",
        "Engineering Workshop Lab",
    ],
    "Other": [
        "General",
        "All Branches",
        "GATE Preparation",
        "GRE/GMAT Preparation",
        "Interview Preparation",
        "Competitive Coding",
        "Aptitude & Reasoning",
        "Project Guidance",
        "Internship Help",
        "Placement Training",
        "Resume Building",
        "Group Discussion Tips",
        "Technical Interview Prep",
        "Programming Fundamentals",
        "Data Structures & Algorithms",
    ]
}

ALL_SUBJECTS = []
for year_subjects in SUBJECTS_BY_YEAR.values():
    ALL_SUBJECTS.extend(year_subjects)

tab1, tab2 = st.tabs(["🔍 Find a Mentor", "🚀 Become a Mentor"])

with tab1:
    mentors = db.get_all_mentors()
    
    st.markdown('<div class="filter-section">', unsafe_allow_html=True)
    
    c_search, c_year, c_subj = st.columns([2, 1.5, 2])
    
    with c_search:
        search_name = st.text_input("🔍 Search by Name", placeholder="Enter mentor name...")
    
    with c_year:
        selected_year = st.selectbox("📚 Select Year", ["All Years"] + list(SUBJECTS_BY_YEAR.keys()))
    
    with c_subj:
        if selected_year == "All Years":
            subject_options = ALL_SUBJECTS
        else:
            subject_options = SUBJECTS_BY_YEAR[selected_year]
        subject_filter = st.selectbox("🎯 Subject", ["All Subjects"] + subject_options)
    
    c_sort, c_price = st.columns([1.5, 1])
    
    with c_sort:
        sort_by = st.selectbox("📊 Sort By", ["Rating (High to Low)", "Price (Low to High)", "Most Reviews"])
    
    with c_price:
        max_price = st.select_slider("💰 Budget/hr", options=[0, 50, 100, 150, 200, 300, 500, 1000], value=500)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    filtered = []
    for m in mentors:
        if subject_filter != "All Subjects" and subject_filter not in m['skills']:
            continue
        if m['rate'] > max_price:
            continue
        if search_name:
            details = db.get_user_details(m['username'])
            fullname = details.get('full_name', m['username']) if details else m['username']
            if search_name.lower() not in fullname.lower():
                continue
        filtered.append(m)
    
    def get_rating(username):
        return db.get_mentor_avg_rating(username)
    
    def get_review_count(username):
        return len(db.get_mentor_reviews(username))
    
    if sort_by == "Rating (High to Low)":
        filtered.sort(key=lambda x: get_rating(x['username']), reverse=True)
    elif sort_by == "Price (Low to High)":
        filtered.sort(key=lambda x: x['rate'])
    elif sort_by == "Most Reviews":
        filtered.sort(key=lambda x: get_review_count(x['username']), reverse=True)
    elif sort_by == "Most Sessions":
        filtered.sort(key=lambda x: get_review_count(x['username']), reverse=True)

    if not filtered:
        st.info("No mentors found matching your criteria. Try adjusting your filters.")
        st.markdown("""
        <div style="text-align: center; padding: 40px; background: #f8fafc; border-radius: 12px; border: 2px dashed #cbd5e1;">
            <h3 style="color: #64748b;">😔 No mentors found</h3>
            <p style="color: #94a3b8;">Be the first to become a mentor for this subject!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .highlight-stat {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white; padding: 20px; border-radius: 16px;
                text-align: center; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            .highlight-stat-num { font-size: 2rem; font-weight: 800; }
            .highlight-stat-label { font-size: 0.85rem; opacity: 0.9; }
        </style>
        """, unsafe_allow_html=True)
        
        total_reviews = 0
        total_rating = 0
        for m in filtered:
            revs = db.get_mentor_reviews(m['username'])
            if revs:
                total_rating += sum(r['rating'] for r in revs)
                total_reviews += len(revs)
        
        avg_rating = total_rating / total_reviews if total_reviews > 0 else 0
        avg_price = sum(m['rate'] for m in filtered) / len(filtered) if filtered else 0
        price_display = "FREE" if avg_price == 0 else f"₹{int(avg_price)}"
        
        c_stats1, c_stats2, c_stats3 = st.columns(3)
        
        with c_stats1:
            st.markdown(f"""
            <div class="highlight-stat">
                <div class="highlight-stat-num">{len(filtered)}</div>
                <div class="highlight-stat-label">Mentors Found</div>
            </div>
            """, unsafe_allow_html=True)
        
        with c_stats2:
            if avg_rating > 0:
                st.markdown(f"""
                <div class="highlight-stat">
                    <div class="highlight-stat-num">⭐ {avg_rating:.1f}</div>
                    <div class="highlight-stat-label">Average Rating</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="highlight-stat">
                    <div class="highlight-stat-num">- ⭐</div>
                    <div class="highlight-stat-label">No Reviews Yet</div>
                </div>
                """, unsafe_allow_html=True)
        
        with c_stats3:
            st.markdown(f"""
            <div class="highlight-stat">
                <div class="highlight-stat-num">{price_display}</div>
                <div class="highlight-stat-label">Avg. Price/hr</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
          
        for i, m in enumerate(filtered):
            username = m['username']
            details = db.get_user_details(username)
            fullname = details.get('full_name', username) if details else username

            reviews = db.get_mentor_reviews(username)
            rating = db.get_mentor_avg_rating(username)
            review_count = len(reviews)
            
            rating_text = f"⭐ {rating}/5" if rating > 0 else "🌟 New"
            badge_text = "🌟 New Mentor" if rating == 0 else ("🏆 Top Rated" if rating >= 4.5 else "✅ Verified")
            price_text = "FREE" if m['rate'] == 0 else f"₹{m['rate']}/hr"
            
            msg = f"Hi {fullname}, I found your profile on PEC Connect Mentorship Program. I'm interested in learning {subject_filter} from you. Could you please share your availability for a session?"
            
            skills = m['skills'].split(",")[:3]
            bio_text = m['bio'][:80] + "..." if len(m['bio']) > 80 else m['bio']
            
            with st.container(border=True):
                # Admin controls at top
                if is_admin:
                    c_admin1, c_admin2, c_admin3 = st.columns([1, 1, 4])
                    with c_admin1:
                        if st.button("🗑️ Delete", key=f"del_mentor_{m['username']}"):
                            db.delete_mentor(m['username'])
                            st.success("Mentor deleted!")
                            st.rerun()
                    with c_admin2:
                        if st.button("⚠️ Warn", key=f"warn_mentor_{m['username']}"):
                            warning_msg = f"Your mentor profile has been removed for violating community guidelines."
                            db.send_warning(username, warning_msg)
                            db.delete_mentor(m['username'])
                            st.warning("Warning sent and mentor deleted!")
                            st.rerun()
                
                c_top1, c_top2 = st.columns([4, 1])
                with c_top1:
                    st.markdown(f"### {fullname}")
                with c_top2:
                    st.markdown(f"**:green[{badge_text}]**")
                
                c_avatar, c_info = st.columns([1, 4])
                with c_avatar:
                    avatar_url = db.get_avatar_url(username)
                    st.image(avatar_url, width=80)
                with c_info:
                    st.markdown(f"**{rating_text}** · {review_count} reviews")
                    for s in skills:
                        st.caption(f"• {s.strip()[:25]}")
                
                st.markdown(f"_{bio_text}_")
                
                c_price, c_contact, c_review = st.columns([1, 2, 2])
                with c_price:
                    st.markdown(f"**{price_text}**")
                with c_contact:
                    msg_link = f"https://wa.me/{m['contact']}?text={msg}"
                    st.link_button("📩 Contact Mentor", msg_link, type="primary", use_container_width=True)
                with c_review:
                    with st.expander("📝 Reviews"):
                        if reviews:
                            for rev in reviews:
                                reviewer = db.get_user_details(rev['reviewer_username'])
                                reviewer_name = reviewer.get('full_name', rev['reviewer_username']) if reviewer else rev['reviewer_username']
                                stars = "⭐" * rev['rating']
                                st.markdown(f"**{reviewer_name}** {stars}")
                                st.caption(f"_{rev['review_text']}_")
                                st.divider()
                        else:
                            st.info("No reviews yet!")
                        
                        user_logged_in = "user" in st.session_state
                        is_own_profile = user_logged_in and st.session_state["user"] == username
                        already_reviewed = False
                        if user_logged_in and not is_own_profile:
                            already_reviewed = db.has_reviewed(username, st.session_state["user"])
                        
                        if user_logged_in and not is_own_profile and not already_reviewed:
                            st.markdown("---")
                            st.markdown("**Write a Review**")
                            col_rate, col_text = st.columns([1, 2])
                            with col_rate:
                                review_rating = st.selectbox("Rating", [5, 4, 3, 2, 1], key=f"rate_{username}")
                            with col_text:
                                review_text = st.text_area("Review", placeholder="Share your experience...", key=f"text_{username}", label_visibility="collapsed")
                            if st.button("Submit", type="primary", key=f"btn_{username}"):
                                if review_text:
                                    try:
                                        result = db.add_mentor_review(username, st.session_state["user"], review_rating, review_text)
                                        if result == "already_reviewed":
                                            st.warning("Already reviewed!")
                                        else:
                                            st.success("Review submitted!")
                                            st.rerun()
                                    except Exception as e:
                                        st.error(f"Error: {e}")
                                else:
                                    st.error("Write a review!")
                        elif already_reviewed:
                            st.success("✅ You reviewed this mentor")
                        elif not user_logged_in:
                            st.warning("Login to review")
                        elif is_own_profile:
                            st.info("Cannot review yourself")
            
            st.markdown("")

with tab2:
    st.markdown("""
    <style>
        .become-mentor-header {
            background: linear-gradient(135deg, #10b981, #059669);
            padding: 20px; border-radius: 12px; color: white; margin-bottom: 20px;
        }
    </style>
    <div class="become-mentor-header">
        <h2 style="margin: 0;">🚀 Become a Mentor</h2>
        <p style="margin: 5px 0 0 0; opacity: 0.9;">Share your knowledge, earn money & build your reputation</p>
    </div>
    """, unsafe_allow_html=True)
    
    if "user" not in st.session_state:
        st.warning("🔐 Please login to create a mentor profile.")
        st.stop()
        
    my_user = st.session_state["user"]
    
    exists = next((m for m in mentors if m['username'] == my_user), None)
    
    if exists:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #d1fae5, #a7f3d0); padding: 20px; border-radius: 12px; border: 2px solid #10b981; margin-bottom: 20px;">
            <h3 style="margin: 0 0 10px 0; color: #065f46;">🎉 Your Mentor Profile is Live!</h3>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("👤 View Your Profile Details"):
            details = db.get_user_details(my_user)
            fullname = details.get('full_name', my_user) if details else my_user
            st.markdown(f"**Name:** {fullname}")
            st.markdown(f"**Rate:** ₹{exists['rate']}/hr")
            st.markdown(f"**WhatsApp:** {exists['contact']}")
            st.markdown(f"**Subjects:** {exists['skills']}")
            st.markdown(f"**Bio:** {exists['bio']}")
            
            reviews = db.get_mentor_reviews(my_user)
            if reviews:
                avg_rating = db.get_mentor_avg_rating(my_user)
                st.markdown(f"**⭐ Average Rating:** {avg_rating}/5 ({len(reviews)} reviews)")
            else:
                st.markdown("**⭐ No reviews yet**")
        
        c_edit, c_del = st.columns(2)
        with c_edit:
            if st.button("✏️ Edit Profile", use_container_width=True):
                st.session_state.edit_mentor_profile = True
        with c_del:
            if st.button("🗑️ Delete Profile", type="primary", use_container_width=True):
                db.delete_mentor(my_user)
                st.success("Profile deleted!")
                st.rerun()
        
        if st.session_state.get('edit_mentor_profile', False):
            st.markdown("---")
            st.markdown("### ✏️ Edit Your Profile")
            
            ALL_MENTOR_SUBJECTS = []
            for year_subjects in SUBJECTS_BY_YEAR.values():
                ALL_MENTOR_SUBJECTS.extend(year_subjects)
            ALL_MENTOR_SUBJECTS = sorted(ALL_MENTOR_SUBJECTS)
            
            current_skills = [s.strip() for s in exists['skills'].split(',')]
            
            with st.form("edit_mentor"):
                new_skills = st.multiselect(
                    "🎯 Subjects you can teach:", 
                    ALL_MENTOR_SUBJECTS, 
                    default=current_skills,
                    key="edit_mentor_subjects"
                )
                
                c1, c2 = st.columns(2)
                new_rate = c1.number_input("💰 Hourly Rate (₹)", value=int(exists['rate']), step=50, help="Set 0 for Free sessions")
                new_contact = c2.text_input("📱 WhatsApp Number", value=str(exists['contact']), help="Include country code")
                
                new_bio = st.text_area("✍️ About You", value=exists['bio'], height=100)
                
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True):
                        if new_skills and new_contact and new_bio:
                            s_str = ", ".join(new_skills)
                            db.update_mentor(my_user, s_str, new_rate, new_contact, new_bio)
                            st.success("Profile updated successfully!")
                            st.session_state.edit_mentor_profile = False
                            st.rerun()
                        else:
                            st.error("Please fill all fields!")
                with col_cancel:
                    if st.form_submit_button("❌ Cancel", use_container_width=True):
                        st.session_state.edit_mentor_profile = False
                        st.rerun()
    else:
        c_benefit1, c_benefit2, c_benefit3 = st.columns(3)
        with c_benefit1:
            st.info("💰 **Earn Money**\n\nSet your own rates and earn while teaching")
        with c_benefit2:
            st.info("📈 **Build Reputation**\n\nGet reviews and ratings to boost your profile")
        with c_benefit3:
            st.info("🤝 **Help Peers**\n\nShare knowledge and help juniors succeed")
        
        st.markdown("###")
        
        ALL_MENTOR_SUBJECTS = []
        for year_subjects in SUBJECTS_BY_YEAR.values():
            ALL_MENTOR_SUBJECTS.extend(year_subjects)
        ALL_MENTOR_SUBJECTS = sorted(ALL_MENTOR_SUBJECTS)
        
        with st.form("new_mentor"):
            st.markdown("**🎯 Select subjects you can teach:**")
            skills = st.multiselect(
                "Subjects (Select all that apply):", 
                ALL_MENTOR_SUBJECTS, 
                key="mentor_subjects",
                help=f"Total {len(ALL_MENTOR_SUBJECTS)} subjects available"
            )
            
            with st.expander("📚 Filter by Year (optional)"):
                selected_years_filter = st.multiselect(
                    "Filter view by year:", 
                    list(SUBJECTS_BY_YEAR.keys()),
                    key="year_filter"
                )
                if selected_years_filter:
                    filtered_subjects = []
                    for yr in selected_years_filter:
                        filtered_subjects.extend(SUBJECTS_BY_YEAR.get(yr, []))
                    st.caption(f"Showing subjects from: {', '.join(selected_years_filter)} ({len(filtered_subjects)} subjects)")
            
            c1, c2 = st.columns(2)
            rate = c1.number_input("💰 Hourly Rate (₹)", value=150, step=50, help="Set 0 for Free sessions")
            contact = c2.text_input("📱 WhatsApp Number", value="91", help="Include country code")
            
            bio = st.text_area("✍️ About You (Your Pitch)", placeholder="I scored 98% in M1. I explain concepts using real-life examples and make difficult topics easy...", height=100)
            
            st.markdown("---")
            if st.form_submit_button("🚀 Publish Profile", type="primary", use_container_width=True):
                if skills and contact and bio:
                    s_str = ", ".join(skills)
                    db.register_mentor(my_user, s_str, rate, contact, bio)
                    st.balloons()
                    st.success("🎉 Profile Published Successfully!")
                    st.rerun()
                else:
                    st.error("⚠️ Please fill all fields - Subjects, WhatsApp number, and Bio are required!")