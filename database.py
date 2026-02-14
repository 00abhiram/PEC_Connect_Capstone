import sqlite3
import hashlib

def init_db():
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    
    # 1. USERS TABLE (Now with 'avatar' column)
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, role TEXT, year TEXT, points INTEGER, avatar TEXT)''')
    
    # MIGRATION: Check if 'avatar' column exists (for existing databases)
    c.execute("PRAGMA table_info(users)")
    columns = [info[1] for info in c.fetchall()]
    if 'avatar' not in columns:
        c.execute("ALTER TABLE users ADD COLUMN avatar TEXT")

    # 2. NOTES TABLE
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  subject TEXT, title TEXT, link TEXT, 
                  price INTEGER, uploader TEXT, 
                  note_type TEXT, contact TEXT)''')
    
    # 3. MENTORS TABLE
    c.execute('''CREATE TABLE IF NOT EXISTS mentors
                 (user_id TEXT, subject_expertise TEXT, hourly_rate INTEGER, 
                  contact_number TEXT, bio TEXT)''')
    
    # 4. TEST RESULTS TABLE
    c.execute('''CREATE TABLE IF NOT EXISTS test_results
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT, subject TEXT, score INTEGER, 
                  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # 5. FORUM QUESTIONS TABLE
    c.execute('''CREATE TABLE IF NOT EXISTS forum_questions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT, subject TEXT, question_text TEXT, 
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # 6. FORUM ANSWERS TABLE
    c.execute('''CREATE TABLE IF NOT EXISTS forum_answers
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  question_id INTEGER, username TEXT, answer_text TEXT, 
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # 7. STUDY GROUP CHATS TABLE
    c.execute('''CREATE TABLE IF NOT EXISTS study_chats
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT, room_name TEXT, message TEXT, 
                  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    # 8. ROOM NAMES TABLE
    c.execute('''CREATE TABLE IF NOT EXISTS study_rooms
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  room_name TEXT UNIQUE)''')

    # --- Pre-populate Default Rooms if empty ---
    c.execute("SELECT count(*) FROM study_rooms")
    if c.fetchone()[0] == 0:
        defaults = ["☕ General Lounge", "🔥 Exam Panic Room", "📐 M1 Survivors", 
                    "🐍 Python Coders", "⚛️ Chemistry Lab", "🌙 Late Night Grind"]
        for r in defaults:
            c.execute("INSERT OR IGNORE INTO study_rooms (room_name) VALUES (?)", (r,))

    conn.commit()
    conn.close()

# ==========================================
# 👤 USER AUTHENTICATION & PROFILE
# ==========================================

def add_user(username, password, role, year):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    try:
        # Default points = 0, Default avatar = NULL
        c.execute("INSERT INTO users VALUES (?,?,?,?,0, NULL)", (username, hashed_pw, role, year))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def check_login(username, password):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_pw))
    data = c.fetchone()
    conn.close()
    return data

def update_avatar(username, base64_img):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    c.execute("UPDATE users SET avatar = ? WHERE username = ?", (base64_img, username))
    conn.commit()
    conn.close()

def get_user_avatar(username):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    c.execute("SELECT avatar FROM users WHERE username = ?", (username,))
    res = c.fetchone()
    conn.close()
    return res[0] if res else None

def get_leaderboard():
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    # Get Top 10 users sorted by points
    c.execute("SELECT username, points, role, year FROM users ORDER BY points DESC LIMIT 10")
    data = c.fetchall()
    conn.close()
    return data

# ==========================================
# 📚 NOTES MARKETPLACE
# ==========================================

def add_note(subject, title, link, price, uploader, note_type, contact):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO notes (subject, title, link, price, uploader, note_type, contact) VALUES (?,?,?,?,?,?,?)",
              (subject, title, link, price, uploader, note_type, contact))
    conn.commit()
    conn.close()

def get_all_notes():
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    data = c.fetchall()
    conn.close()
    return data

# ==========================================
# 📝 MOCK TESTS & POINTS
# ==========================================

def save_test_result(username, subject, score):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO test_results (username, subject, score) VALUES (?,?,?)", (username, subject, score))
    # +10 Points for taking a test
    c.execute("UPDATE users SET points = points + 10 WHERE username=?", (username,))
    conn.commit()
    conn.close()

def get_user_progress(username):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    c.execute("SELECT id, username, subject, score, date FROM test_results WHERE username=?", (username,))
    data = c.fetchall()
    conn.close()
    return data

# ==========================================
# 🗣️ DOUBT FORUM
# ==========================================

def post_question(username, subject, text):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO forum_questions (username, subject, question_text) VALUES (?,?,?)", (username, subject, text))
    conn.commit()
    conn.close()

def get_questions(subject_filter=None):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    if subject_filter and subject_filter != "All":
        c.execute("SELECT * FROM forum_questions WHERE subject=? ORDER BY id DESC", (subject_filter,))
    else:
        c.execute("SELECT * FROM forum_questions ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data

def post_answer(question_id, username, text):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO forum_answers (question_id, username, answer_text) VALUES (?,?,?)", (question_id, username, text))
    # +5 Points for helping others
    c.execute("UPDATE users SET points = points + 5 WHERE username=?", (username,))
    conn.commit()
    conn.close()

def get_answers(question_id):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM forum_answers WHERE question_id=?", (question_id,))
    data = c.fetchall()
    conn.close()
    return data

# ==========================================
# 👥 STUDY GROUPS & ROOMS
# ==========================================

def send_group_message(username, room, message):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO study_chats (username, room_name, message) VALUES (?,?,?)", (username, room, message))
    # +1 Point for being active in study groups
    c.execute("UPDATE users SET points = points + 1 WHERE username=?", (username,))
    conn.commit()
    conn.close()

def get_group_messages(room):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM study_chats WHERE room_name=? ORDER BY id ASC", (room,))
    data = c.fetchall()
    conn.close()
    return data

def create_new_room(room_name):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO study_rooms (room_name) VALUES (?)", (room_name,))
        conn.commit()
        return True
    except:
        return False # Room probably already exists
    finally:
        conn.close()

def get_all_rooms():
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    c.execute("SELECT room_name FROM study_rooms")
    data = c.fetchall()
    conn.close()
    # Convert list of tuples [('A',), ('B',)] to list ['A', 'B']
    return [r[0] for r in data]