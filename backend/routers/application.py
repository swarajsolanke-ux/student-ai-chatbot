# application.py - Part of routers module
from fastapi import APIRouter
from sqlite import get_db

router = APIRouter(prefix="/application")

@router.post("/apply")
def apply(user_id: int, university_id: int):
    db = get_db()
    db.execute(
        "INSERT INTO applications (user_id, university_id, status) VALUES (?, ?, ?)",
        (user_id, university_id, "Submitted")
    )
    db.commit()
    return {"status": "submitted"}
