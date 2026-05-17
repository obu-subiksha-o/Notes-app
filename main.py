from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base, SessionLocal
from models import User, Note
from schemas import (
    UserCreate,
    UserLogin,
    NoteCreate,
    ShareNote
)
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)

app = FastAPI()

security = HTTPBearer()

# =========================================
# CORS
# =========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# DATABASE
# =========================================

Base.metadata.create_all(bind=engine)

# =========================================
# TEMP NOTIFICATION STORAGE
# =========================================

notifications_store = {}

# =========================================
# DATABASE SESSION
# =========================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# =========================================
# AUTH USER
# =========================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    email = verify_token(token)

    if not email:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

# =========================================
# HOME
# =========================================

@app.get("/")
def home():

    return {
        "message": "API Working"
    }

# =========================================
# REGISTER
# =========================================

@app.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = User(
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return {
        "message": "User registered successfully"
    }

# =========================================
# LOGIN
# =========================================

@app.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    valid_password = verify_password(
        user.password,
        existing_user.password
    )

    if not valid_password:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub": existing_user.email
        }
    )

    return {
        "access_token": access_token
    }

# =========================================
# CREATE NOTE
# =========================================

@app.post("/notes")
def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_note = Note(
        title=note.title,
        content=note.content,
        owner_id=current_user.id
    )

    db.add(new_note)

    db.commit()

    db.refresh(new_note)

    return {
        "message": "Note created successfully",
        "note": {
            "id": new_note.id,
            "title": new_note.title,
            "content": new_note.content
        }
    }

# =========================================
# GET NOTES
# =========================================

@app.get("/notes")
def get_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    my_notes = db.query(Note).filter(
        Note.owner_id == current_user.id
    ).all()

    shared_notes = db.query(Note).filter(
        Note.shared_with.contains(current_user.email)
    ).all()

    return {
        "my_notes": [
            {
                "id": note.id,
                "title": note.title,
                "content": note.content
            }
            for note in my_notes
        ],

        "shared_notes": [
            {
                "id": note.id,
                "title": note.title,
                "content": note.content
            }
            for note in shared_notes
        ]
    }

# =========================================
# UPDATE NOTE
# =========================================

@app.put("/notes/{note_id}")
def update_note(
    note_id: int,
    updated_note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()

    if not note:

        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    note.title = updated_note.title
    note.content = updated_note.content

    db.commit()

    db.refresh(note)

    return {
        "message": "Note updated successfully"
    }

# =========================================
# DELETE NOTE
# =========================================

@app.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()

    if not note:

        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    db.delete(note)

    db.commit()

    return {
        "message": "Note deleted successfully"
    }

# =========================================
# SHARE NOTE
# =========================================

@app.post("/notes/{note_id}/share")
def share_note(
    note_id: int,
    share_data: ShareNote,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    note = db.query(Note).filter(
        Note.id == note_id,
        Note.owner_id == current_user.id
    ).first()

    if not note:

        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    shared_user = db.query(User).filter(
        User.email == share_data.share_with_email
    ).first()

    if not shared_user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    current_shared = []

    if note.shared_with:
        current_shared = note.shared_with.split(",")

    # prevent duplicate share
    if share_data.share_with_email in current_shared:

        return {
            "message": "Note already shared"
        }

    current_shared.append(
        share_data.share_with_email
    )

    note.shared_with = ",".join(current_shared)

    # notifications
    if share_data.share_with_email not in notifications_store:

        notifications_store[
            share_data.share_with_email
        ] = []

    notifications_store[
        share_data.share_with_email
    ].append({

        "message":
        f"{current_user.email} shared '{note.title}' with you",

        "read": False
    })

    db.commit()

    return {
        "message":
        f"Note shared with {share_data.share_with_email}"
    }

# =========================================
# GET NOTIFICATIONS
# =========================================

@app.get("/notifications")
def get_notifications(
    current_user: User = Depends(get_current_user)
):

    user_email = current_user.email

    if user_email not in notifications_store:

        notifications_store[user_email] = []

    unread_notifications = [
        notification
        for notification in notifications_store[user_email]
        if not notification["read"]
    ]

    return unread_notifications

# =========================================
# MARK READ
# =========================================

@app.post("/notifications/read")
def mark_notifications_read(
    current_user: User = Depends(get_current_user)
):

    user_notifications = notifications_store.get(
        current_user.email,
        []
    )

    for notification in user_notifications:

        notification["read"] = True

    return {
        "message": "Notifications marked as read"
    }