# university.py - Part of models module
from pydantic import BaseModel

class University(BaseModel):
    id: int
    name: str
    country: str
    tuition_fee: int
    min_gpa: float
