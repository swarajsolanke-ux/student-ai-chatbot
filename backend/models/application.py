# application.py - Part of models module
from pydantic import BaseModel

class Application(BaseModel):
    user_id: int
    university_id: int
    status: str
