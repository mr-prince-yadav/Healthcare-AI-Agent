import sqlite3
import hashlib
import streamlit as st  # import to access secrets

# Use Streamlit secrets for DB name
DB_NAME = st.secrets["database"]["db_name"]

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_users_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username: str, password: str) -> bool:
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(username: str, password: str) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT password FROM users WHERE username = ?",
        (username,)
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        return False

    return row[0] == hash_password(password)
