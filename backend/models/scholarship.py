
from pydantic import BaseModel

class Scholarship(BaseModel):
    id: int
    name: str
    min_gpa: float
