AI Prompt Management System using Flask, MongoDB & Groq API

Overview

AI Prompt Management System is a backend AI integration project built using Python Flask, MongoDB, and Groq API.

The system accepts user questions through REST APIs, fetches prompt templates from MongoDB, dynamically replaces placeholders, sends prompts to AI models, stores request-response history, and returns AI-generated responses.

---

Features

- Flask REST APIs
- MongoDB integration
- Dynamic prompt template management
- Groq AI model integration
- Request/response history storage
- Asynchronous batch processing
- Postman API testing support

---

Tech Stack

- Python
- Flask
- MongoDB
- PyMongo
- Groq API

---

Project Structure

AI Prompt Management System
│
├── .venv
├── .env
├── app.py
├── requirements.txt
├── README.md

---

Setup Instructions

1. Clone Repository

git clone <https://github.com/Roshankumar200/AI-Prompt-Management-System>
cd AI-Prompt-Management-System

---

2. Create Virtual Environment

python -m venv .venv

Activate virtual environment:

Windows

source .venv/Scripts/activate

Linux / Mac

source .venv/bin/activate

---

3. Install Dependencies

pip install -r requirements.txt

---

MongoDB Configuration

Make sure MongoDB server is running locally.

Update MongoDB connection inside "app.py":

client = MongoClient(
    host="localhost",
    port=27017,
    username="admin",
    password="your_password",
    authSource="admin"
)

---

Environment Variables

Create ".env" file and add:

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.1-8b-instant

---

Run Project

python app.py

Server will start at:

http://127.0.0.1:5000

---

Browser Testing

Seed Prompt Template

Open browser:

http://127.0.0.1:5000/seed

---

Test AI Response

Open browser:

http://127.0.0.1:5000/test

---

API Testing using Postman

Single Question API

Endpoint

POST http://127.0.0.1:5000/ask

Request Body

{
  "userInput": "What is Artificial Intelligence?"
}

Response

{
  "response": "Artificial Intelligence is..."
}

---

Batch API

Endpoint

POST http://127.0.0.1:5000/ask-batch

Request Body

{
  "userInputs": [
    "What is AI?",
    "Explain DBMS",
    "What is Python?"
  ]
}

---

Database Collections

prompts

Stores AI prompt templates.

history

Stores request and response history.

---
