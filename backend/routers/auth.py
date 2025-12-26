# auth.py - Part of routers module
from fastapi import APIRouter

router = APIRouter(prefix="/auth")

@router.post("/login")
def login():
    return {"user_id": 1}
