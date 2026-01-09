# auth.py
import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth
import json

# ------------------ FIREBASE ADMIN INIT ------------------
if not firebase_admin._apps:
    # Load JSON from Streamlit secrets
    cred_dict = st.secrets["firebase_json"]

    # Fix the private key newlines (very important!)
    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")

    # Initialize Firebase
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

# ------------------ USER MANAGEMENT ------------------
def create_user(email: str, password: str) -> bool:
    """
    Create a user in Firebase Authentication.
    """
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return True
    except firebase_admin.exceptions.FirebaseError as e:
        print(f"[Firebase Error] {e}")
        return False
    except Exception as e:
        print(f"[Error] {e}")
        return False


def authenticate_user(email: str, password: str) -> bool:
    """
    Authenticate a user via Firebase Admin SDK (verify if exists).
    Firebase Admin SDK cannot sign in, but we can check if user exists.
    """
    try:
        user = auth.get_user_by_email(email)
        # For real password verification, you would need Firebase client SDK (not Admin)
        return True if user else False
    except firebase_admin.exceptions.FirebaseError:
        return False
    except Exception:
        return False
