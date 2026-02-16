# Math Quiz & Progress Tracking API

## 📌 Project Overview

This project is a Django REST API designed to deliver math quizzes to students and track their learning progress.
It allows a user to start a quiz, receive randomized questions, and (in later phases) submit answers and analyze performance.

This project is being developed as part of a capstone exercise focused on backend architecture, API design, and version-controlled development.

---

## ⚙️ Tech Stack

* Python 3.x
* Django
* Django REST Framework
* SQLite (development database)
* Git & GitHub

---

## 🏗️ Current Features (Part 3)

### ✔ Topic Retrieval

`GET /api/topics/`

Returns available quiz topics.

Example Response:

```json
[
  {
    "id": 1,
    "name": "Fractions",
    "description": "Basic operations involving fractions"
  }
]
```

---

### ✔ Start Quiz

`POST /api/quizzes/start/`

Creates a quiz session and returns 5 randomized questions.

Example Request:

```json
{
  "student_identifier": "student_001",
  "topic_id": 1
}
```

Example Response:

```json
{
  "quiz_session_id": 3,
  "topic": { "id": 1, "name": "Fractions" },
  "questions": [...]
}
```

---

## 📂 Project Structure

```
math-quiz-api/
│
├── quiz/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│
├── math_api/
│   ├── settings.py
│   ├── urls.py
│
└── manage.py
```

---

## 🚀 Running the Project Locally

### 1️⃣ Clone Repository

```
git clone <repo-url>
cd math-quiz-api
```

### 2️⃣ Create Virtual Environment

```
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
```

### 3️⃣ Install Dependencies

```
pip install django djangorestframework
```

### 4️⃣ Run Migrations

```
python manage.py migrate
```

### 5️⃣ Start Server

```
python manage.py runserver
```

API available at:

```
http://127.0.0.1:8000/api/
```

---

## 🔄 Upcoming Features

* Quiz submission and scoring
* Student performance analytics
* Difficulty adaptation
* Automated testing

---

## 🎯 Learning Goals

This project demonstrates:

* REST API design using Django
* Database modeling for educational systems
* Git branch-based workflow
* Incremental feature development

---

## 👤 Author

Jonathan Odey
