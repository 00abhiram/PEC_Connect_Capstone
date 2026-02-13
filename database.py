import sqlite3
import hashlib

def init_db():
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    
    # 1. Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT, role TEXT, year TEXT, points INTEGER)''')

    # 2. Notes Table
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  subject TEXT, title TEXT, link TEXT, 
                  price INTEGER, uploader TEXT, 
                  note_type TEXT, contact TEXT)''')
    
    # 3. Mentors Table (UPDATED to 5 Columns)
    c.execute('''CREATE TABLE IF NOT EXISTS mentors
                 (user_id TEXT PRIMARY KEY, 
                  subject_expertise TEXT, 
                  hourly_rate INTEGER, 
                  contact_number TEXT, 
                  bio TEXT,
                  FOREIGN KEY(user_id) REFERENCES users(username))''')
    
    # 4. Forum (Doubts)
    c.execute('''CREATE TABLE IF NOT EXISTS forum
                 (id INTEGER PRIMARY KEY, user TEXT, question TEXT, 
                  answer TEXT, upvotes INTEGER)''')

    conn.commit()
    conn.close()

# Helper Functions
def add_user(username, password, role, year):
    conn = sqlite3.connect('pec_data.db')
    c = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute("INSERT INTO users VALUES (?,?,?,?,0)", (username, hashed_pw, role, year))
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