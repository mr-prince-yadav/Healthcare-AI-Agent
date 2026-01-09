import os
from dotenv import load_dotenv

load_dotenv(override=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY not found")

RELAY_WEBHOOK_URL = os.getenv("RELAY_WEBHOOK_URL")
if not RELAY_WEBHOOK_URL:
    raise RuntimeError("RELAY_WEBHOOK_URL not found")
