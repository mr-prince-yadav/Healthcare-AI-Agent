# reminder.py
import sqlite3
import json
from datetime import datetime, timedelta
import time
from relay_email import send_email

DB_FILE = "users.db"

# -------------------- Database helpers --------------------
def get_conn():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def load_all_profiles():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT username, data FROM profiles")
    rows = cur.fetchall()
    conn.close()
    profiles = {}
    for username, data in rows:
        profiles[username] = json.loads(data)
    return profiles

def update_profile(username, profile_data):
    """Update profile JSON in DB"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE profiles SET data=? WHERE username=?", (json.dumps(profile_data), username))
    conn.commit()
    conn.close()

# -------------------- Sent trackers --------------------
sent_medication_reminders = set()  # (username, med_name, date)
sent_appointment_reminders = set()  # (username, appt_str)
sent_immediate_appointments = set()  # (username, appt_str, action)

# -------------------- Reminder & Immediate email logic --------------------
def check_and_send_reminders():
    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    current_day_abbr = now.strftime("%a")  # "Mon", "Tue", etc.

    profiles = load_all_profiles()

    for username, profile in profiles.items():
        email = profile.get("email")
        if not email:
            continue

        # ----- Medication reminders (1 min before) -----
        for med in profile.get("medication_list", []):
            med_time = datetime.strptime(med["time"], "%H:%M").time()
            med_dt = datetime.combine(now.date(), med_time)
            reminder_dt = med_dt - timedelta(minutes=1)  # 1 min before

            # Only send if today is in selected days
            if current_day_abbr not in med.get("days", []):
                continue

            key = (username, med["med_name"], today_str)
            if key in sent_medication_reminders:
                continue

            # Send if current time is within a 2-minute window around reminder
            if reminder_dt <= now <= reminder_dt + timedelta(minutes=2):
                subject = f"Medication Reminder: {med['med_name']}"
                body = f"Dear {profile.get('name','User')},\n\nIt's almost time to take {med['med_name']} at {med['time']} today."
                sent = send_email(to=email, subject=subject, body=body)
                if sent:
                    sent_medication_reminders.add(key)
                    print(f"[{now}] Medication reminder sent to {username} for {med['med_name']}")
                else:
                    print(f"[{now}] Failed to send medication reminder to {username}")


        # ----- Appointment reminders (1 min before) -----
        for appt in profile.get("appointments", []):
            try:
                appt_date = datetime.strptime(appt.split()[0], "%Y-%m-%d").date()
                appt_time = datetime.strptime(appt.split()[1], "%H:%M:%S").time()
                appt_dt = datetime.combine(appt_date, appt_time)
                reminder_dt = appt_dt - timedelta(minutes=1)

                key = (username, appt)
                if key not in sent_appointment_reminders:
                    if reminder_dt <= now < reminder_dt + timedelta(seconds=30):
                        subject = "Appointment Reminder"
                        body = f"Dear {profile.get('name','User')},\n\nReminder: You have an upcoming appointment:\n{appt}"
                        sent = send_email(to=email, subject=subject, body=body)
                        if sent:
                            sent_appointment_reminders.add(key)
                            print(f"[{now}] Appointment reminder sent to {username} for {appt}")
                        else:
                            print(f"[{now}] Failed to send appointment reminder to {username}")
            except Exception as e:
                print(f"[{now}] Error parsing appointment for {username}: {e}")

# ----- Immediate appointment emails -----
def send_appointment_email(username, appointment_str, action, new_appt=None):
    """
    action: 'scheduled', 'deleted', 'rescheduled'
    new_appt: optional, required if action=='rescheduled'
    """
    profiles = load_all_profiles()
    profile = profiles.get(username)
    if not profile:
        return

    email = profile.get("email")
    if not email:
        return

    key = (username, appointment_str, action)
    if key in sent_immediate_appointments:
        return

    if action == "scheduled":
        subject = "Appointment Scheduled"
        body = f"Dear {profile.get('name','User')},\n\nYour appointment has been scheduled:\n{appointment_str}"
    elif action == "deleted":
        subject = "Appointment Cancelled"
        body = f"Dear {profile.get('name','User')},\n\nYour appointment scheduled for {appointment_str} has been cancelled."
    elif action == "rescheduled":
        subject = "Appointment Rescheduled"
        if new_appt:
            body = f"Dear {profile.get('name','User')},\n\nYour appointment has been rescheduled:\nFrom: {appointment_str}\nTo: {new_appt}"
        else:
            body = f"Dear {profile.get('name','User')},\n\nYour appointment has been rescheduled:\n{appointment_str}"
    else:
        return

    sent = send_email(to=email, subject=subject, body=body)
    if sent:
        sent_immediate_appointments.add(key)
        print(f"[{datetime.now()}] {action.capitalize()} email sent to {username} for {appointment_str}")
    else:
        print(f"[{datetime.now()}] Failed to send {action} email to {username}")
# -------------------- Run continuously --------------------
if __name__ == "__main__":
    print("[INFO] Reminder service started...")
    while True:
        try:
            check_and_send_reminders()
        except Exception as e:
            print(f"[ERROR] Exception in reminder loop: {e}")
        time.sleep(15)  # check every 15 seconds
