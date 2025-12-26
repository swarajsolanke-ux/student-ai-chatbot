# user.py - Part of models module
from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str | None = None
    phone: str | None = None
