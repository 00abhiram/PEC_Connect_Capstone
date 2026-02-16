import streamlit as st
from supabase import create_client, Client
import hashlib

# ==========================================
# 🔌 CONNECT TO SUPABASE
# ==========================================
@st.cache_resource
def init_connection():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"❌ Supabase Connection Error: {e}")
        return None

supabase: Client = init_connection()

def init_db():
    pass

# ==========================================
# 👤 USER & AUTH
# ==========================================
def add_user(username, password, role, year, full_name="", email=""):
    try:
        exists = supabase.table("users").select("username").eq("username", username).execute()
        if exists.data: return False
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        data = {
            "username": username, "password": hashed_pw, "role": role,
            "year": year, "full_name": full_name, "email": email,
            "points": 0, "avatar": "" 
        }
        supabase.table("users").insert(data).execute()
        return True
    except: return False

def check_login(username, password):
    try:
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        response = supabase.table("users").select("*").eq("username", username).execute()
        if response.data:
            user = response.data[0]
            if user['password'] == hashed_pw or user['password'] == password:
                return user 
        return None
    except: return None

def get_user_details(username):
    try:
        res = supabase.table("users").select("*").eq("username", username).execute()
        return res.data[0] if res.data else None
    except: return None

def get_leaderboard():
    try: return supabase.table("users").select("*").order("points", desc=True).limit(20).execute().data
    except: return []

def search_users(query):
    try:
        return supabase.table("users").select("*").or_(f"full_name.ilike.%{query}%,username.ilike.%{query}%,skills.ilike.%{query}%").execute().data
    except: return []

# ==========================================
# 🖼️ AVATAR & STORAGE (OPTIMIZED)
# ==========================================
def update_avatar(username, file_bytes, file_type):
    """
    Uploads image to Supabase Storage Bucket and saves the URL.
    """
    try:
        file_ext = file_type.split("/")[-1]
        file_path = f"{username}_avatar.{file_ext}"
        
        # 1. Upload to 'avatars' bucket
        supabase.storage.from_("avatars").upload(
            file_path, 
            file_bytes, 
            {"content-type": file_type, "upsert": "true"}
        )
        
        # 2. Get Public URL
        public_url = supabase.storage.from_("avatars").get_public_url(file_path)
        
        # 3. Save URL to DB
        supabase.table("users").update({"avatar": public_url}).eq("username", username).execute()
        return True
    except Exception as e:
        print(f"Upload Error: {e}")
        return False

def get_user_avatar(username):
    """Returns the raw avatar field (URL or Base64)"""
    try:
        res = supabase.table("users").select("avatar").eq("username", username).execute()
        return res.data[0]['avatar'] if res.data else None
    except: return None

def get_avatar_url(username):
    """
    Smart Helper: Returns a valid image URL for any user.
    Handles: Cloud URL (New) | Base64 (Old) | Dicebear (Default)
    """
    try:
        raw = get_user_avatar(username)
        if raw:
            # If it's a Cloud URL or valid Base64
            if "http" in str(raw): return raw
            if len(str(raw)) > 100: return f"data:image/png;base64,{raw}"
        
        # Default Fallback
        return f"https://api.dicebear.com/7.x/identicon/svg?seed={username}"
    except:
        return f"https://api.dicebear.com/7.x/identicon/svg?seed={username}"

# ==========================================
# 🌐 NETWORK & MESSAGING
# ==========================================
def get_connection_status(sender, receiver):
    try:
        res = supabase.table("connections").select("status").or_(
            f"and(sender.eq.{sender},receiver.eq.{receiver}),and(sender.eq.{receiver},receiver.eq.{sender})"
        ).execute()
        return res.data[0]['status'] if res.data else None
    except: return None

def send_connection_request(sender, receiver):
    try:
        if get_connection_status(sender, receiver): return False
        supabase.table("connections").insert({"sender": sender, "receiver": receiver, "status": "pending"}).execute()
        return True
    except: return False

def get_pending_requests(username):
    try:
        res = supabase.table("connections").select("*").eq("receiver", username).eq("status", "pending").execute()
        return res.data
    except: return []

def respond_to_request(sender, receiver, action):
    try:
        if action == "accept":
            supabase.table("connections").update({"status": "accepted"}).match({"sender": sender, "receiver": receiver}).execute()
        elif action == "reject":
            supabase.table("connections").delete().match({"sender": sender, "receiver": receiver}).execute()
        return True
    except: return False

def send_message(sender, receiver, content):
    try:
        supabase.table("messages").insert({"sender_username": sender, "receiver_username": receiver, "content": content}).execute()
        return True
    except: return False

def get_chat_history(user1, user2):
    try:
        return supabase.table("messages").select("*").or_(
            f"and(sender_username.eq.{user1},receiver_username.eq.{user2}),and(sender_username.eq.{user2},receiver_username.eq.{user1})"
        ).order("created_at", desc=False).execute().data
    except: return []

# ==========================================
# 👥 STUDY GROUPS & FORUM
# ==========================================
def get_all_rooms():
    try:
        res = supabase.table("study_rooms").select("room_name").execute()
        return [r['room_name'] for r in res.data] if res.data else ["☕ General Lounge"]
    except: return ["☕ General Lounge"]

def create_new_room(room_name):
    try:
        exists = supabase.table("study_rooms").select("*").eq("room_name", room_name).execute()
        if exists.data: return False
        supabase.table("study_rooms").insert({"room_name": room_name}).execute()
        return True
    except: return False

def get_group_messages(room_name):
    try:
        return supabase.table("study_chats").select("*").eq("room_name", room_name).order("timestamp", desc=False).execute().data
    except: return []

def send_group_message(username, room, message):
    try:
        supabase.table("study_chats").insert({"username": username, "room_name": room, "message": message}).execute()
    except: pass

def get_questions(subject_filter=None):
    try:
        q = supabase.table("forum_questions").select("*").order("id", desc=True)
        if subject_filter and subject_filter != "All": q = q.eq("subject", subject_filter)
        return q.execute().data
    except: return []

def post_question(username, subject, text):
    try: supabase.table("forum_questions").insert({"username": username, "subject": subject, "question_text": text}).execute()
    except: pass

def get_answers(q_id):
    try: return supabase.table("forum_answers").select("*").eq("question_id", q_id).order("id", desc=False).execute().data
    except: return []

def post_answer(q_id, username, text):
    try: supabase.table("forum_answers").insert({"question_id": q_id, "username": username, "answer_text": text}).execute()
    except: pass

def upvote_question(q_id):
    try:
        supabase.rpc("increment_upvotes", {"row_id": q_id}).execute()
        return True
    except: return False

def mark_solved(q_id):
    try:
        supabase.table("forum_questions").update({"is_solved": True}).eq("id", q_id).execute()
        return True
    except: return False

# ==========================================
# 🎓 ACADEMICS (TESTS, MENTORS, NOTES)
# ==========================================
def get_user_test_history(username):
    try: return supabase.table("test_results").select("*").eq("username", username).execute().data
    except: return []

def get_all_mentors():
    try: return supabase.table("mentors").select("*").execute().data
    except: return []

def register_mentor(username, skills, rate, contact, bio):
    try:
        data = {"username": username, "skills": skills, "rate": rate, "contact": contact, "bio": bio}
        supabase.table("mentors").upsert(data).execute()
        supabase.table("users").update({"role": "Mentor"}).eq("username", username).execute()
        return True
    except: return False

def delete_mentor(username):
    try:
        supabase.table("mentors").delete().eq("username", username).execute()
        supabase.table("users").update({"role": "Student"}).eq("username", username).execute()
        return True
    except: return False

def get_user_notes(username):
    try: return supabase.table("notes").select("*").eq("uploader", username).execute().data
    except: return []

def get_verified_skills(username):
    try:
        results = supabase.table("test_results").select("*").eq("username", username).execute().data
        if not results: return []
        
        best_scores = {}
        for r in results:
            sub, score = r['subject'], r['score']
            if sub not in best_scores or score > best_scores[sub]:
                best_scores[sub] = score
        
        return [sub for sub, score in best_scores.items() if score >= 8]
    except: return []