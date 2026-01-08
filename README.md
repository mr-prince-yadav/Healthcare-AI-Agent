# Healthcare Agent

---

A Streamlit-based healthcare assistant application that enables users to manage personal health data, track vitals, schedule medications and appointments, receive AI-driven health insights, and access mental health support. Email notifications are delivered using Relay Webhook.

---

## Healthcare Agent – Streamlit App

This project is a web-based healthcare assistant built using Streamlit. It provides an integrated interface for users to monitor health metrics, receive reminders, and interact with AI-powered health services.

---

## Features

### Authentication

- User signup and login with secure password hashing  
- Session-based authentication  
- First-time profile setup and profile editing  

### Profile Management

- Personal details: name, age, height, weight, gender, email  
- Medical conditions for personalized recommendations  
- Profile image upload  
- Persistent storage using SQLite  

### Health Tracking

- Track heart rate, steps, sleep, and blood glucose  
- Automatic BMI calculation  
- Rule-based health condition evaluation  
- AI-generated health improvement recommendations  

### Medication Reminder

- Schedule medications by selected days (Mon–Sun)  
- One-minute prior reminder logic  
- In-app alerts  
- Email notifications via Relay Webhook  
- Duplicate reminder prevention  

### Appointment Scheduler

- Schedule, reschedule, and cancel appointments  
- Doctor assignment by category (General, Emergency, Mental Health)  
- Instant email confirmation  
- Automatic appointment reminders  

### Symptom Checker

- AI-assisted symptom analysis  
- Categorizes symptoms into General, Emergency, or Mental Health  
- Stores last reported symptoms  
- Uses LangGraph-based workflow routing  

### Mental Health Chat

- AI-powered mental health assistant  
- Context-aware responses  
- Optional chat reset  
- Session-based persistence  

### Help Chat

- AI-powered help chatbot  
- Provides guidance based on app context and user profile  

---

## Tech Stack

- Frontend & Backend: Streamlit  
- Database: SQLite  
- AI / NLP: Google Gemini via LangChain  
- Workflow Engine: LangGraph  
- Email Notifications: Relay Webhook  
- Configuration: python-dotenv  

---

## Project Structure

```
healthcare-agent/
├── app.py # Main Streamlit application
├── auth.py # Authentication and user table logic
├── ui.py # UI rendering functions
├── graph_builder.py # LangGraph symptom analysis workflow
├── functions.py # LLM helpers and message handling
├── health_engine.py # Health recommendation engine
├── reminder.py # Background reminder service
├── relay_email.py # Email sending via Relay Webhook
├── config.py # Configuration and API keys
├── users.db # SQLite database
├── loading.png # UI asset
├── requirements.txt # Python dependencies
├── .env # Environment variables
├── LICENSE
└── README.md
```

---

## Environment Variables

Create a `.env` file:
```
GOOGLE_API_KEY=your_google_api_key
RELAY_WEBHOOK_URL=your_relay_webhook_url
```


---

## Running the Application

Install dependencies:
```
pip install -r requirements.txt
```

Run the Streamlit app:
```
streamlit run app.py
```

---

## Security

- Passwords are hashed  
- No plaintext credentials stored  
- Medical data stored locally using SQLite  

---

## Future Enhancements

- Cloud database integration  
- Predictive health analytics  
- SMS and mobile push notifications  
- Telemedicine and video consultation  
- Multi-language support  

---

## License

This project is licensed under the MIT License.