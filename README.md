# 🚀 AI Prompt Management System

Backend AI integration project built using **Python Flask**, **MongoDB**, and **Groq API**.

---

# 📌 Overview

AI Prompt Management System is a REST API based backend project that:

* Accepts user questions through APIs
* Fetches prompt templates from MongoDB
* Dynamically replaces placeholders
* Sends prompts to Groq AI models
* Stores request/response history
* Returns AI-generated responses
* Supports asynchronous batch processing

---

# ✨ Features

* ✅ Flask REST APIs
* ✅ MongoDB Integration
* ✅ Dynamic Prompt Templates
* ✅ Groq AI Integration
* ✅ Request/Response History Storage
* ✅ Async Batch Processing
* ✅ Postman API Testing

---

# 🛠️ Tech Stack

| Technology | Usage                |
| ---------- | -------------------- |
| Python     | Backend Language     |
| Flask      | REST API Framework   |
| MongoDB    | Database             |
| PyMongo    | MongoDB Connector    |
| Groq API   | AI Model Integration |
| Asyncio    | Async Processing     |

---

# 📁 Project Structure

```bash
AI-Prompt-Management-System/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env
```

---

# ⚙️ Setup Instructions

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Roshankumar200/AI-Prompt-Management-System.git

cd AI-Prompt-Management-System
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

### Windows

```bash
source .venv/Scripts/activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🍃 MongoDB Configuration

Make sure MongoDB server is running locally.

Update MongoDB connection inside `app.py`:

```python
client = MongoClient(
    host="localhost",
    port=27017,
    username=os.getenv("MONGO_USER"),
    password=os.getenv("MONGO_PASSWORD"),
    authSource="admin"
)
```

---

# 🔐 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key

GROQ_MODEL=llama-3.1-8b-instant

MONGO_USER=your_mongodb_username

MONGO_PASSWORD=your_mongodb_password
```

---

# ▶️ Run Project

```bash
python app.py
```

Server starts at:

```bash
http://127.0.0.1:5000
```

---

# 🌐 Browser Testing

## Seed Prompt Template

Open in browser:

```bash
http://127.0.0.1:5000/seed
```

---

## Test AI Response

Open in browser:

```bash
http://127.0.0.1:5000/test
```

---

# 📮 API Testing Using Postman

---

# 🔹 Single Question API

## Endpoint

```http
POST http://127.0.0.1:5000/ask
```

## Request Body

```json
{
  "userInput": "What is DBMS?"
}
```

## Response

```json
{
  "response": "DBMS is..."
}
```

---

# 🔹 Batch API

## Endpoint

```http
POST http://127.0.0.1:5000/ask-batch
```

## Request Body

```json
{
  "userInputs": [
    "What is AI?",
    "Explain DBMS",
    "What is Python?"
  ]
}
```

---

# 🗂️ Database Collections

| Collection | Description                         |
| ---------- | ----------------------------------- |
| prompts    | Stores AI prompt templates          |
| history    | Stores request and response history |

---
