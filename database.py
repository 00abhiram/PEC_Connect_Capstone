import streamlit as st
from supabase import create_client, Client
import hashlib
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

def update_password(username, new_password):
    try:
        hashed_pw = hashlib.sha256(new_password.encode()).hexdigest()
        supabase.table("users").update({"password": hashed_pw}).eq("username", username).execute()
        return True
    except: return False

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

def get_user_details(username):
    try:
        res = supabase.table("users").select("*").eq("username", username).execute()
        return res.data[0] if res.data else None
    except: return None

def get_user_avatar(username):
    try:
        user = get_user_details(username)
        return user.get('avatar', '') if user else ''
    except: return ''

def get_avatar_url(username):
    try:
        user = get_user_details(username)
        if user and user.get('avatar'):
            avatar = user['avatar']
            if "http" in str(avatar):
                return avatar
            if len(str(avatar)) > 100:
                return f"data:image/png;base64,{avatar}"
        return f"https://api.dicebear.com/7.x/identicon/svg?seed={username}"
    except: return f"https://api.dicebear.com/7.x/identicon/svg?seed={username}"

def get_all_users():
    try:
        return supabase.table("users").select("*").execute().data
    except: return []

def get_leaderboard():
    try: return supabase.table("users").select("*").order("points", desc=True).limit(100).execute().data
    except: return []

def get_full_leaderboard():
    try:
        users = supabase.table("users").select("username", "points", "full_name", "year").order("points", desc=True).execute().data or []
        
        if not users:
            return []
        
        result = []
        for user in users:
            username = user.get('username', '')
            if not username:
                continue
            
            test_results = []
            try:
                test_results = supabase.table("test_results").select("score", "total_questions").eq("username", username).execute().data or []
            except:
                pass
            
            user['tests_taken'] = len(test_results)
            test_points = 0
            for t in test_results:
                try:
                    if t.get('total_questions', 0) and t.get('total_questions', 0) > 0:
                        test_points += int((t.get('score', 0) or 0) / t['total_questions'] * 100)
                except:
                    pass
            user['test_points'] = test_points
            
            answers = []
            try:
                answers = supabase.table("forum_answers").select("id").eq("username", username).execute().data or []
            except:
                pass
            user['answers_given'] = len(answers)
            user['forum_points'] = len(answers) * 10
            
            mentor = []
            try:
                mentor = supabase.table("mentors").select("username").eq("username", username).execute().data or []
            except:
                pass
            user['is_mentor'] = len(mentor) > 0
            user['mentor_points'] = 100 if user['is_mentor'] else 0
            
            base_points = user.get('points', 0) or 0
            total_points = base_points + test_points + user['forum_points'] + user['mentor_points']
            user['points'] = total_points
            
            result.append(user)
        
        result.sort(key=lambda x: x.get('points', 0), reverse=True)
        return result
    except Exception as e:
        print(f"Leaderboard error: {e}")
        return []

def send_message(sender, receiver, content):
    try:
        supabase.table("messages").insert({
            "sender_username": sender,
            "receiver_username": receiver,
            "content": content
        }).execute()
        return True
    except: return False

def get_chat_history(user1, user2):
    try:
        return supabase.table("messages").select("*").or_(
            f"and(sender_username.eq.{user1},receiver_username.eq.{user2}),and(sender_username.eq.{user2},receiver_username.eq.{user1})"
        ).order("created_at", desc=False).execute().data
    except: return []

def get_all_messages():
    try:
        return supabase.table("messages").select("*").order("created_at", desc=True).execute().data
    except: return []

def get_user_conversations(username):
    try:
        sent = supabase.table("messages").select("receiver").eq("sender", username).execute().data
        received = supabase.table("messages").select("sender").eq("receiver", username).execute().data
        users = set()
        for m in sent:
            if m.get('receiver'): users.add(m['receiver'])
        for m in received:
            if m.get('sender'): users.add(m['sender'])
        return list(users)
    except: return []

def get_all_chatrooms():
    try:
        return supabase.table("chat_rooms").select("*").execute().data
    except: return []

def delete_chat_message(msg_id):
    try:
        supabase.table("messages").delete().eq("id", msg_id).execute()
        return True
    except: return False

def delete_message(msg_id):
    return delete_chat_message(msg_id)

def clear_chat(user1, user2):
    try:
        supabase.table("messages").delete().eq("sender_username", user1).eq("receiver_username", user2).execute()
        supabase.table("messages").delete().eq("sender_username", user2).eq("receiver_username", user1).execute()
        return True
    except: return False

def delete_study_message(msg_id):
    try:
        supabase.table("study_chat").delete().eq("id", msg_id).execute()
        return True
    except: return False

def get_all_study_messages():
    try:
        return supabase.table("study_chat").select("*").order("created_at", desc=True).execute().data
    except: return []

def delete_room(room_name):
    try:
        supabase.table("study_rooms").delete().eq("room_name", room_name).execute()
        supabase.table("study_chat").delete().eq("room_name", room_name).execute()
        return True
    except: return False

def get_all_rooms():
    try:
        return supabase.table("study_rooms").select("*").execute().data
    except: return []

def create_alert(alert_text):
    try:
        supabase.table("alerts").insert({"message": alert_text}).execute()
        return True
    except: return False

def get_alerts():
    try:
        return supabase.table("alerts").select("*").order("created_at", desc=True).execute().data
    except: return []

def delete_alert(alert_id):
    try:
        supabase.table("alerts").delete().eq("id", alert_id).execute()
        return True
    except: return False

def create_notification_request(title, description, date, requested_by):
    try:
        supabase.table("notification_requests").insert({
            "title": title,
            "description": description,
            "date": date,
            "requested_by": requested_by,
            "status": "pending"
        }).execute()
        return True
    except: return False

def get_notification_requests():
    try:
        return supabase.table("notification_requests").select("*").order("created_at", desc=True).execute().data
    except: return []

def approve_notification_request(req_id, title, description, date):
    try:
        # Update request status
        supabase.table("notification_requests").update({"status": "approved"}).eq("id", req_id).execute()
        # Create the alert notification
        alert_msg = f"{title} | {description} | Date: {date}"
        supabase.table("alerts").insert({"message": alert_msg}).execute()
        return True
    except: return False

def reject_notification_request(req_id):
    try:
        supabase.table("notification_requests").update({"status": "rejected"}).eq("id", req_id).execute()
        return True
    except: return False

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

def post_question(username, subject, text, image_url=""):
    try: 
        data = {"username": username, "subject": subject, "question_text": text}
        if image_url:
            data["image_url"] = image_url
        supabase.table("forum_questions").insert(data).execute()
        return True
    except Exception as e:
        print(f"Error posting question: {e}")
        return False

def upload_doubt_image(file_bytes, file_type, username):
    try:
        import uuid
        file_ext = file_type.split("/")[-1]
        unique_name = f"doubt_{username}_{uuid.uuid4().hex[:8]}.{file_ext}"
        
        result = supabase.storage.from_("avatars").upload(
            unique_name,
            file_bytes,
            {"content-type": file_type, "upsert": "true"}
        )
        public_url = supabase.storage.from_("avatars").get_public_url(unique_name)
        return public_url
    except Exception as e:
        print(f"Upload Error: {e}")
        return ""

def get_answers(q_id):
    try: return supabase.table("forum_answers").select("*").eq("question_id", q_id).order("id", desc=False).execute().data
    except: return []

def post_answer(q_id, username, text):
    try: supabase.table("forum_answers").insert({"question_id": q_id, "username": username, "answer_text": text}).execute()
    except: pass

def upvote_question(q_id, username):
    try:
        existing = supabase.table("question_votes").select("*").eq("question_id", q_id).eq("username", username).execute()
        if existing.data:
            return False
        supabase.table("question_votes").insert({"question_id": q_id, "username": username}).execute()
        supabase.rpc("increment_upvotes", {"row_id": q_id}).execute()
        return True
    except: return False

def get_user_votes(username):
    try:
        votes = supabase.table("question_votes").select("question_id").eq("username", username).execute()
        return [v['question_id'] for v in votes.data]
    except: return []

def delete_question(q_id):
    try:
        supabase.table("forum_answers").delete().eq("question_id", q_id).execute()
        supabase.table("question_votes").delete().eq("question_id", q_id).execute()
        supabase.table("forum_questions").delete().eq("id", q_id).execute()
        return True
    except: return False

def mark_solved(q_id):
    try:
        supabase.table("forum_questions").update({"is_solved": True}).eq("id", q_id).execute()
        return True
    except: return False
def get_user_test_history(username):
    try: return supabase.table("test_results").select("*").eq("username", username).execute().data
    except: return []

def save_test_result(username, subject, score, total_questions, difficulty):
    try:
        data = {
            "username": username,
            "subject": subject,
            "score": score,
            "total_questions": total_questions,
            "difficulty": difficulty
        }
        supabase.table("test_results").insert(data).execute()
        return True
    except Exception as e:
        print(f"Error saving test result: {e}")
        return False

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

def add_mentor_review(mentor_username, reviewer_username, rating, review_text):
    try:
        existing = supabase.table("mentor_reviews").select("*").eq("mentor_username", mentor_username).eq("reviewer_username", reviewer_username).execute()
        if existing.data:
            return "already_reviewed"
        data = {
            "mentor_username": mentor_username,
            "reviewer_username": reviewer_username,
            "rating": rating,
            "review_text": review_text
        }
        supabase.table("mentor_reviews").insert(data).execute()
        return True
    except: return False

def has_reviewed(mentor_username, reviewer_username):
    try:
        existing = supabase.table("mentor_reviews").select("*").eq("mentor_username", mentor_username).eq("reviewer_username", reviewer_username).execute()
        return len(existing.data) > 0
    except: return False

def update_mentor_review(mentor_username, reviewer_username, rating, review_text):
    try:
        data = {"rating": rating, "review_text": review_text}
        supabase.table("mentor_reviews").update(data).eq("mentor_username", mentor_username).eq("reviewer_username", reviewer_username).execute()
        return True
    except: return False

def get_mentor_reviews(mentor_username):
    try:
        return supabase.table("mentor_reviews").select("*").eq("mentor_username", mentor_username).execute().data
    except: return []

def get_mentor_avg_rating(mentor_username):
    try:
        reviews = get_mentor_reviews(mentor_username)
        if not reviews:
            return 0
        total = sum(r['rating'] for r in reviews)
        return round(total / len(reviews), 1)
    except: return 0

def update_mentor(username, skills, rate, contact, bio):
    try:
        data = {"skills": skills, "rate": rate, "contact": contact, "bio": bio}
        supabase.table("mentors").update(data).eq("username", username).execute()
        return True
    except: return False

def get_user_notes(username):
    try: return supabase.table("notes").select("*").eq("uploader", username).execute().data
    except: return []

def get_pending_requests(username):
    try:
        return supabase.table("connections").select("*").eq("receiver", username).eq("status", "pending").execute().data
    except: return []

def send_connection_request(sender, receiver):
    try:
        supabase.table("connections").insert({
            "sender": sender,
            "receiver": receiver,
            "status": "pending"
        }).execute()
        return True
    except: return False

def accept_connection(sender, receiver):
    try:
        supabase.table("connections").update({"status": "accepted"}).eq("sender", sender).eq("receiver", receiver).execute()
        return True
    except: return False

def reject_connection(sender, receiver):
    try:
        supabase.table("connections").delete().eq("sender", sender).eq("receiver", receiver).execute()
        return True
    except: return False

def get_connection_status(user1, user2):
    try:
        result = supabase.table("connections").select("status").eq("sender", user1).eq("receiver", user2).execute()
        if result.data:
            return result.data[0].get("status")
        result2 = supabase.table("connections").select("status").eq("sender", user2).eq("receiver", user1).execute()
        if result2.data:
            return result2.data[0].get("status")
        return None
    except: return None

def delete_user(username):
    return delete_user_data(username)

def send_warning(username, message):
    try:
        supabase.table("warnings").insert({"username": username, "message": message}).execute()
        return True
    except: return False

def delete_user_data(username):
    try:
        supabase.table("connections").delete().eq("sender", username).execute()
        supabase.table("connections").delete().eq("receiver", username).execute()
        supabase.table("messages").delete().eq("sender_username", username).execute()
        supabase.table("messages").delete().eq("receiver_username", username).execute()
        supabase.table("study_chats").delete().eq("username", username).execute()
        supabase.table("forum_answers").delete().eq("username", username).execute()
        supabase.table("forum_questions").delete().eq("username", username).execute()
        supabase.table("test_results").delete().eq("username", username).execute()
        supabase.table("notes").delete().eq("uploader", username).execute()
        supabase.table("mentors").delete().eq("username", username).execute()
        supabase.table("users").delete().eq("username", username).execute()
        return True
    except Exception as e:
        print(f"Delete Error: {e}")
        return False

def get_verified_skills(username):
    try:
        results = supabase.table("test_results").select("*").eq("username", username).execute().data
        if not results: return []
        
        best_scores = {}
        for r in results:
            sub, score = r['subject'], r['subject']
            if sub not in best_scores or score > best_scores[sub]:
                best_scores[sub] = score
        
        return [sub for sub, score in best_scores.items() if score >= 8]
    except: return []

def rate_note(note_id, rating):
    try:
        note = supabase.table("notes").select("rating_count, total_rating").eq("id", note_id).execute()
        if note.data:
            current_count = note.data[0].get("rating_count", 0) or 0
            current_total = note.data[0].get("total_rating", 0) or 0
            new_count = current_count + 1
            new_total = current_total + rating
            new_avg = round(new_total / new_count, 1)
            
            is_verified = True if new_count >= 3 and new_avg >= 4.0 else False
            
            supabase.table("notes").update({
                "rating_count": new_count,
                "total_rating": new_total,
                "avg_rating": new_avg,
                "is_verified": is_verified
            }).eq("id", note_id).execute()
            return True
        return False
    except Exception as e:
        print(f"Rate Note Error: {e}")
        return False

def add_note_review(note_id, username, review):
    try:
        supabase.table("note_reviews").insert({
            "note_id": note_id,
            "username": username,
            "review": review
        }).execute()
        return True
    except Exception as e:
        print(f"Add Review Error: {e}")
        return False

def get_note_reviews(note_id):
    try:
        return supabase.table("note_reviews").select("*").eq("note_id", note_id).order("id", desc=True).execute().data
    except: return []

def get_notes_with_filters(subject=None, min_rating=0, note_type=None):
    try:
        query = supabase.table("notes").select("*")
        if subject and subject != "All":
            query = query.ilike("subject", f"%{subject}%")
        if note_type:
            query = query.eq("note_type", note_type)
        results = query.execute().data
        
        if min_rating > 0:
            results = [r for r in results if (r.get("avg_rating") or 0) >= min_rating]
        
        return results
    except Exception as e:
        print(f"Filter Error: {e}")
        return []