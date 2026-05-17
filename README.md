<img width="1918" height="1133" alt="Screenshot 2026-05-17 190423" src="https://github.com/user-attachments/assets/ba4a7ea2-3646-46e2-a0ec-334cec70edbf" /># Noto - Note it down

A clean and aesthetic full-stack notes application built with **FastAPI**, **SQLite**, and a simple frontend using **HTML, CSS, and JavaScript**.
Users can register, login securely using JWT authentication, create notes, edit them, delete them, and even share notes with other users.

Built as a personal learning project to understand:

* Backend APIs
* Authentication
* CRUD operations
* Database handling
* Frontend ↔ Backend connectivity
* Deployment using Render

---

##  Live Demo

### Frontend

[Notes App Frontend](https://notes-app-frontend-gm1k.onrender.com)

### Backend API

[FastAPI Backend](https://notes-app-5aut.onrender.com)

### GitHub Repository

[GitHub Repo](https://github.com/obu-subiksha-o/Notes-app)

---

#  Features

* User Registration & Login
* JWT Authentication
* Create Notes
* Edit Notes
* Delete Notes
* Share Notes with Other Users
* Notification System
* Dark Mode Toggle
* Search Notes
* Responsive & Aesthetic UI
* Backend deployed on Render
* Frontend deployed separately on Render

---

#  Tech Stack

## Frontend

* HTML
* CSS
* JavaScript

## Backend

* FastAPI
* SQLAlchemy
* SQLite
* JWT Authentication
* Uvicorn

## Deployment

* Render

---

#  Screenshots

## Login Page

<img width="1918" height="1133" alt="Screenshot 2026-05-17 190423" src="https://github.com/user-attachments/assets/0ec0e7cf-33a9-4ef2-86f6-50931235bf75"/>


---

## Dashboard

<img width="1918" height="1137" alt="Screenshot 2026-05-17 190707" src="https://github.com/user-attachments/assets/eb3b09b1-aeef-47b8-b742-7ce5a053a766"/>

---

## Notifications

<<img width="1918" height="1138" alt="Screenshot 2026-05-17 190720" src="https://github.com/user-attachments/assets/c5fd2a51-8942-42b7-8a08-1a5702dbf8aa"/>


---

#  Installation

## Clone the repository

```bash
git clone https://github.com/obu-subiksha-o/Notes-app.git
```

## Move into the project folder

```bash
cd Notes-app
```

## Create virtual environment

```bash
python -m venv venv
```

## Activate virtual environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

#  Run Backend

```bash
uvicorn main:app --reload
```

Backend runs on:

```bash
http://127.0.0.1:8000
```

---

#  Project Structure

```bash
Notes-app/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── main.py
├── auth.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
└── notes.db
```

---

#  Authentication

This project uses:

* JWT Tokens
* Password Hashing using Passlib + Bcrypt
* Protected Routes using FastAPI Security

---

#  What I Learned

While building this project, I learned:

* Building REST APIs using FastAPI
* Connecting frontend and backend
* Authentication flow using JWT
* Database relationships using SQLAlchemy
* Hosting frontend and backend separately
* Debugging deployment issues on Render (pain. actual pain.)

---

#  Future Improvements

* Rich text editor
* Profile system
* Real-time notifications
* File/image uploads
* Better mobile responsiveness
* PostgreSQL support
* Docker deployment

---

#  Author

Made by Obu Subiksha!
