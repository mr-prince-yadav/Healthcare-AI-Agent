import requests
import streamlit as st

# Firebase Web API key from Streamlit Secrets
FIREBASE_API_KEY = st.secrets["firebase"]["firebase_api_key"]

BASE_URL = "https://identitytoolkit.googleapis.com/v1"


def create_user(username: str, password: str) -> bool:
    """
    Sign up user in Firebase.
    Username is treated as email.
    """
    url = f"{BASE_URL}/accounts:signUp?key={FIREBASE_API_KEY}"
    payload = {
        "email": username,
        "password": password,
        "returnSecureToken": True
    }

    r = requests.post(url, json=payload)
    return r.status_code == 200


def authenticate_user(username: str, password: str) -> bool:
    """
    Login user via Firebase.
    """
    url = f"{BASE_URL}/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {
        "email": username,
        "password": password,
        "returnSecureToken": True
    }

    r = requests.post(url, json=payload)
    return r.status_code == 200
