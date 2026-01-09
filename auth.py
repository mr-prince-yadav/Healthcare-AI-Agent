# auth.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import json
import sqlite3

# ------------------- Firebase Admin Init -------------------
if not firebase_admin._apps:
    cred_json = st.secrets["firebase_json"]  # JSON string from secrets
    cred_dict = json.loads(cred_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

# ------------------- SQLite fallback -------------------
DB_FILE = st.secrets["database"]["db_name"]

def get_conn():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def create_users_table():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)")
    conn.commit()
    conn.close()

# ------------------- User functions -------------------
def create_user(username: str, password: str) -> bool:
    """
    Create a user in Firebase Auth and SQLite.
    """
    try:
        # Firebase Admin creates user
        auth.create_user(email=username, password=password)
        # Also store locally in SQLite
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO users(username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error creating user: {e}")
        return False

def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticate user using local SQLite (Admin SDK cannot verify passwords directly)
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    conn.close()
    if row and row[0] == password:
        return True
    return False
