import streamlit as st
import database as db
import time

# --- PAGE SETUP ---
st.set_page_config(page_title="Resources | PEC", page_icon="📚", layout="wide")

# Initialize DB connection (Uses your Supabase setup)
db.init_db()

# --- PROFESSIONAL CSS ---
st.markdown("""
<style>
    .resource-card {
        background: white; border: 1px solid #e2e8f0; border-radius: 12px;
        padding: 20px; margin-bottom: 15px; transition: transform 0.2s;
    }
    .resource-card:hover { border-color: #3b82f6; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
    
    .type-badge {
        font-size: 0.7rem; font-weight: 700; padding: 2px 8px; border-radius: 10px;
        text-transform: uppercase; margin-bottom: 8px; display: inline-block;
    }
    .badge-pdf { background: #fee2e2; color: #991b1b; }
    .badge-lab { background: #fef3c7; color: #92400e; }
    .badge-pyq { background: #dcfce7; color: #166534; }
    .badge-xerox { background: #eff6ff; color: #1e40af; }
    
    .price-tag { font-size: 1.1rem; font-weight: 800; color: #0f172a; }
</style>
""", unsafe_allow_html=True)

st.title("📚 PEC Resource Center")
st.caption("Access verified study materials, lab manuals, and previous papers.")

# --- HELPERS ---
BRANCHES = ["CSE", "CSE-AIML", "ECE", "EEE", "Civil", "Mech", "IT"]
SUBJECT_LIST = ["M1", "M2", "BEE", "Chemistry", "Physics", "Python", "Data Structures", "OS", "DBMS", "AI/ML", "General"]

def delete_resource(note_id):
    """Deletes a note from Supabase"""
    try:
        db.supabase.table("notes").delete().eq("id", note_id).execute()
        return True
    except:
        return False

# --- NAVIGATION TABS ---
tabs = st.tabs([
    "📄 Digital Notes", 
    "🧪 Lab & Viva",
    "📜 Syllabus",
    "❓ Question Papers", 
    "🖨️ Buy Xerox", 
    "📤 Upload / Sell"
])

# ==========================================
# TAB 1: DIGITAL NOTES (PDFs)
# ==========================================
with tabs[0]:
    st.subheader("📖 Free Digital Notes")
    c1, c2 = st.columns(2)
    s_query = c1.text_input("Search Subject", key="search_pdf")
    f_branch = c2.selectbox("Branch", ["All"] + BRANCHES, key="filt_pdf")
    
    # Query Supabase
    try:
        res = db.supabase.table("notes").select("*").eq("note_type", "PDF")
        if f_branch != "All": res = res.ilike("title", f"%{f_branch}%")
        if s_query: res = res.ilike("subject", f"%{s_query}%")
        notes = res.execute().data
    except: notes = []

    if not notes:
        st.info("No notes found.")
    else:
        for n in notes:
            with st.container(border=True):
                ca, cb = st.columns([4, 1])
                with ca:
                    st.markdown(f"**{n['subject']}** — {n['title']}")
                    st.caption(f"Uploaded by: {n['uploader']}")
                with cb:
                    st.link_button("⬇ Download", n['link'], use_container_width=True)
                    if "user" in st.session_state and st.session_state["user"] == n['uploader']:
                        if st.button("🗑️ Delete", key=f"del_{n['id']}"):
                            if delete_resource(n['id']):
                                st.success("Deleted!")
                                time.sleep(1)
                                st.rerun()

# ==========================================
# TAB 2 & 3 & 4: Lab / Syllabus / PYQ
# ==========================================
# (Applying similar logic for these tabs using the Supabase data structure)
types = {"🧪 Lab Manuals": "LAB", "📜 Syllabus": "SYLLABUS", "❓ PYQs": "PYQ"}
for idx, (label, db_type) in enumerate(types.items(), start=1):
    with tabs[idx]:
        st.subheader(label)
        try:
            items = db.supabase.table("notes").select("*").eq("note_type", db_type).execute().data
        except: items = []
        
        if not items:
            st.info(f"No {label} available yet.")
        else:
            for i in items:
                with st.container(border=True):
                    c1, c2 = st.columns([4, 1])
                    c1.markdown(f"**{i['title']}**")
                    c1.caption(f"Category: {i['subject']} | Added by {i['uploader']}")
                    c2.link_button("View/Download", i['link'], use_container_width=True)
                    if "user" in st.session_state and st.session_state["user"] == i['uploader']:
                        if st.button("🗑️ Remove", key=f"del_i_{i['id']}"):
                            delete_resource(i['id'])
                            st.rerun()

# ==========================================
# TAB 5: XEROX MARKET (Selling Hard Copies)
# ==========================================
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
                    st.link_button("💬 WhatsApp Seller", wa_link, type="primary", use_container_width=True)
                    
                    # Delete Option for Seller
                    if "user" in st.session_state and st.session_state["user"] == item['uploader']:
                        st.write("")
                        if st.button("🗑️ Mark as Sold", key=f"sold_{item['id']}", use_container_width=True):
                            delete_resource(item['id'])
                            st.success("Listing Removed!")
                            st.rerun()

# ==========================================
# TAB 6: UPLOAD RESOURCE
# ==========================================
with tabs[5]:
    st.subheader("📤 Contribute a Resource")
    if "user" not in st.session_state:
        st.error("Please Login to upload study materials.")
    else:
        with st.form("upload_form"):
            cat = st.selectbox("Category", ["Digital Note", "Lab Manual", "Syllabus Copy", "Question Paper", "Xerox (Sell)"])
            sub = st.selectbox("Subject", SUBJECT_LIST)
            
            # Form Logic
            title = st.text_input("Title / Description", placeholder="e.g., Unit 1-3 Handwritten Notes")
            link = st.text_input("Link", placeholder="Google Drive or PDF Link (N/A for Xerox)")
            
            # Logic for Xerox Selling
            c1, c2 = st.columns(2)
            price = c1.number_input("Price (Set 0 for Free)", value=0)
            contact = c2.text_input("Contact Number (WhatsApp)", value="91")
            
            # Map Category to DB Type
            db_type_map = {
                "Digital Note": "PDF", "Lab Manual": "LAB", 
                "Syllabus Copy": "SYLLABUS", "Question Paper": "PYQ", "Xerox (Sell)": "XEROX"
            }
            
            if st.form_submit_button("🚀 Publish to PEC Market"):
                if title and (link or cat == "Xerox (Sell)"):
                    upload_data = {
                        "subject": sub,
                        "title": title,
                        "link": link if link else "N/A",
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
                    st.warning("Please fill in the title and link.")