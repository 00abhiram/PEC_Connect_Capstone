import sqlite3
import hashlib


def init_db():
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()

    # 1. Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY,
                  password TEXT,
                  role TEXT,
                  year TEXT,
                  points INTEGER)''')

    # 2. Notes Table
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  subject TEXT,
                  title TEXT,
                  link TEXT,
                  price INTEGER,
                  uploader TEXT,
                  note_type TEXT,
                  contact TEXT)''')

    # 3. Mentors Table
    c.execute('''CREATE TABLE IF NOT EXISTS mentors
                 (user_id TEXT PRIMARY KEY,
                  subject_expertise TEXT,
                  hourly_rate INTEGER,
                  contact_number TEXT,
                  bio TEXT,
                  FOREIGN KEY(user_id) REFERENCES users(username))''')

    # 4. Forum (Doubts)
    c.execute('''CREATE TABLE IF NOT EXISTS forum
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user TEXT,
                  question TEXT,
                  answer TEXT,
                  upvotes INTEGER DEFAULT 0)''')

    # 5. Interview Experiences (NEW FEATURE)
    c.execute('''CREATE TABLE IF NOT EXISTS interview_experiences
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_name TEXT NOT NULL,
                  company_name TEXT NOT NULL,
                  role TEXT NOT NULL,
                  interview_rounds TEXT,
                  questions_asked TEXT,
                  experience TEXT,
                  tips TEXT,
                  posted_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

    conn.commit()
    conn.close()


# -----------------------------
# Helper Functions
# -----------------------------

def add_user(username, password, role, year):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute("INSERT INTO users VALUES (?,?,?,?,0)",
                  (username, hashed_pw, role, year))
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
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hashed_pw))
    data = c.fetchone()
    conn.close()
    return data
