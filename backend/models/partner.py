
from pydantic import BaseModel

class Partner(BaseModel):
    id: int
    name: str
    category: str
